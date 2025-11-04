"""
Unit tests for TranslationCache.

Tests cache CRUD operations, expiration, and persistence.
Target coverage: 80%+ enforced by CI (pytest-cov with --cov-fail-under=80)
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
import pytest
import tempfile

from src.vocab_analyzer.translation.cache import TranslationCache


@pytest.fixture
def temp_cache_file():
    """Create a temporary cache file for testing."""
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".json",
        delete=False
    ) as f:
        temp_path = Path(f.name)

    yield temp_path

    # Cleanup
    if temp_path.exists():
        temp_path.unlink()


@pytest.fixture
def cache(temp_cache_file):
    """Create a TranslationCache instance for testing."""
    return TranslationCache(cache_file=temp_cache_file, cache_expiry_days=30)


class TestTranslationCacheInit:
    """Test cache initialization."""

    def test_init_creates_empty_cache(self, temp_cache_file):
        """Cache initializes with empty entries."""
        cache = TranslationCache(cache_file=temp_cache_file)
        assert cache.entries == {}
        assert cache.cache_expiry_days == 30

    def test_init_with_custom_expiry(self, temp_cache_file):
        """Cache accepts custom expiry days."""
        cache = TranslationCache(
            cache_file=temp_cache_file,
            cache_expiry_days=7
        )
        assert cache.cache_expiry_days == 7


class TestTranslationCacheCRUD:
    """Test cache CRUD operations."""

    def test_set_and_get_word(self, cache):
        """Can store and retrieve a word translation."""
        cache.set(
            text="hello",
            translation="你好",
            translation_type="word",
            source="ecdict",
            confidence_score=0.95
        )

        result = cache.get("hello", "word")
        assert result is not None
        assert result["source_text"] == "hello"
        assert result["target_text"] == "你好"
        assert result["translation_type"] == "word"
        assert result["source"] == "ecdict"
        assert result["confidence_score"] == 0.95
        assert result["access_count"] == 2  # Set=1, Get=1

    def test_set_and_get_phrase(self, cache):
        """Can store and retrieve a phrase translation."""
        cache.set(
            text="run out",
            translation="用完;耗尽",
            translation_type="phrase",
            source="argos",
            confidence_score=0.70
        )

        result = cache.get("run out", "phrase")
        assert result is not None
        assert result["target_text"] == "用完;耗尽"
        assert result["translation_type"] == "phrase"

    def test_get_nonexistent_returns_none(self, cache):
        """Getting nonexistent entry returns None."""
        result = cache.get("nonexistent", "word")
        assert result is None

    def test_exists_returns_true_for_cached(self, cache):
        """exists() returns True for cached entries."""
        cache.set("test", "测试", "word")
        assert cache.exists("test", "word") is True

    def test_exists_returns_false_for_missing(self, cache):
        """exists() returns False for missing entries."""
        assert cache.exists("missing", "word") is False

    def test_case_insensitive_lookup(self, cache):
        """Cache lookups are case-insensitive."""
        cache.set("Hello", "你好", "word")

        assert cache.get("hello", "word") is not None
        assert cache.get("HELLO", "word") is not None
        assert cache.get("HeLLo", "word") is not None

    def test_access_count_increments(self, cache):
        """Access count increments on each get()."""
        cache.set("test", "测试", "word")

        result1 = cache.get("test", "word")
        assert result1["access_count"] == 2

        result2 = cache.get("test", "word")
        assert result2["access_count"] == 3

        result3 = cache.get("test", "word")
        assert result3["access_count"] == 4


class TestTranslationCacheValidation:
    """Test input validation."""

    def test_set_empty_text_raises_error(self, cache):
        """Empty source text raises ValueError."""
        with pytest.raises(ValueError, match="Source text must be"):
            cache.set("", "测试", "word")

    def test_set_too_long_text_raises_error(self, cache):
        """Text exceeding 500 chars raises ValueError."""
        with pytest.raises(ValueError, match="Source text must be"):
            cache.set("a" * 501, "测试", "word")

    def test_set_empty_translation_raises_error(self, cache):
        """Empty translation raises ValueError."""
        with pytest.raises(ValueError, match="Translation must be"):
            cache.set("test", "", "word")

    def test_set_too_long_translation_raises_error(self, cache):
        """Translation exceeding 2000 chars raises ValueError."""
        with pytest.raises(ValueError, match="Translation must be"):
            cache.set("test", "测" * 2001, "word")

    def test_set_invalid_type_raises_error(self, cache):
        """Invalid translation_type raises ValueError."""
        with pytest.raises(ValueError, match="Invalid translation_type"):
            cache.set("test", "测试", "invalid_type")

    def test_set_invalid_source_raises_error(self, cache):
        """Invalid source raises ValueError."""
        with pytest.raises(ValueError, match="Invalid source"):
            cache.set("test", "测试", "word", source="invalid")

    def test_set_invalid_confidence_raises_error(self, cache):
        """Confidence score outside 0.0-1.0 raises ValueError."""
        with pytest.raises(ValueError, match="Confidence score"):
            cache.set("test", "测试", "word", confidence_score=1.5)

        with pytest.raises(ValueError, match="Confidence score"):
            cache.set("test", "测试", "word", confidence_score=-0.1)


class TestTranslationCacheExpiration:
    """Test cache expiration logic."""

    def test_clear_old_removes_expired(self, temp_cache_file):
        """clear_old() removes expired entries."""
        cache = TranslationCache(
            cache_file=temp_cache_file,
            cache_expiry_days=1  # 1 day expiry
        )

        # Add entry with old timestamp (2 days ago)
        cache.set("old", "旧的", "word")
        old_key = "word:old"
        cache.entries[old_key]["timestamp"] = int(
            (datetime.now() - timedelta(days=2)).timestamp()
        )

        # Add fresh entry
        cache.set("new", "新的", "word")

        # Clear old entries
        removed = cache.clear_old()

        assert removed == 1
        assert cache.exists("new", "word") is True
        assert cache.exists("old", "word") is False

    def test_get_returns_none_for_expired(self, temp_cache_file):
        """get() returns None and removes expired entries."""
        cache = TranslationCache(
            cache_file=temp_cache_file,
            cache_expiry_days=1
        )

        cache.set("test", "测试", "word")
        key = "word:test"

        # Make it expired
        cache.entries[key]["timestamp"] = int(
            (datetime.now() - timedelta(days=2)).timestamp()
        )

        result = cache.get("test", "word")
        assert result is None
        assert key not in cache.entries  # Removed automatically


class TestTranslationCachePersistence:
    """Test cache persistence to/from JSON."""

    def test_save_creates_file(self, cache, temp_cache_file):
        """save() creates JSON file."""
        cache.set("test", "测试", "word")
        cache.save()

        assert temp_cache_file.exists()

    def test_save_writes_valid_json(self, cache, temp_cache_file):
        """save() writes valid JSON structure."""
        cache.set("hello", "你好", "word")
        cache.set("world", "世界", "word")
        cache.save()

        with open(temp_cache_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert "version" in data
        assert "metadata" in data
        assert "entries" in data
        assert len(data["entries"]) == 2

    def test_load_restores_entries(self, temp_cache_file):
        """load() restores entries from file."""
        # Create and save cache
        cache1 = TranslationCache(cache_file=temp_cache_file)
        cache1.set("test", "测试", "word", source="ecdict")
        cache1.save()

        # Load in new instance
        cache2 = TranslationCache(cache_file=temp_cache_file)
        result = cache2.get("test", "word")

        assert result is not None
        assert result["target_text"] == "测试"
        assert result["source"] == "ecdict"

    def test_load_handles_missing_file(self, temp_cache_file):
        """load() handles missing file gracefully."""
        # Delete file if exists
        if temp_cache_file.exists():
            temp_cache_file.unlink()

        cache = TranslationCache(cache_file=temp_cache_file)
        assert cache.entries == {}

    def test_load_handles_invalid_json(self, temp_cache_file):
        """load() handles corrupted JSON gracefully."""
        # Write invalid JSON
        with open(temp_cache_file, "w") as f:
            f.write("{invalid json}")

        cache = TranslationCache(cache_file=temp_cache_file)
        assert cache.entries == {}


class TestTranslationCacheStats:
    """Test cache statistics."""

    def test_get_stats_empty_cache(self, cache):
        """get_stats() works on empty cache."""
        stats = cache.get_stats()

        assert stats["total_entries"] == 0
        assert stats["by_type"] == {}
        assert stats["by_source"] == {}
        assert stats["total_accesses"] == 0

    def test_get_stats_populated_cache(self, cache):
        """get_stats() provides accurate statistics."""
        cache.set("hello", "你好", "word", source="ecdict")
        cache.set("run out", "用完", "phrase", source="argos")
        cache.set("How are you?", "你好吗?", "sentence", source="argos")

        # Access some entries
        cache.get("hello", "word")
        cache.get("hello", "word")

        stats = cache.get_stats()

        assert stats["total_entries"] == 3
        assert stats["by_type"]["word"] == 1
        assert stats["by_type"]["phrase"] == 1
        assert stats["by_type"]["sentence"] == 1
        assert stats["by_source"]["ecdict"] == 1
        assert stats["by_source"]["argos"] == 2
        assert stats["total_accesses"] >= 5  # 3 sets + 2 gets
