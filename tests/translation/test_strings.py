"""
Unit tests for BilingualStringLoader.

Tests loading, retrieval, formatting, and error handling of bilingual UI strings.
Target coverage: 80%+ enforced by CI (pytest-cov with --cov-fail-under=80)
"""

import json
import pytest
from pathlib import Path
import tempfile

from src.vocab_analyzer.translation.strings import BilingualStringLoader, get_loader, reload_strings


@pytest.fixture
def temp_strings_file():
    """Create temporary UI strings JSON file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding='utf-8') as f:
        temp_path = Path(f.name)

        # Write sample strings
        data = {
            "version": "1.0",
            "last_updated": "2025-11-04",
            "categories": ["navigation", "buttons", "errors"],
            "strings": {
                "navigation.home": {
                    "key": "navigation.home",
                    "text_en": "Home",
                    "text_cn": "首页",
                    "context": "Main navigation",
                    "category": "navigation"
                },
                "navigation.upload": {
                    "key": "navigation.upload",
                    "text_en": "Upload",
                    "text_cn": "上传",
                    "context": "Upload page",
                    "category": "navigation"
                },
                "buttons.analyze": {
                    "key": "buttons.analyze",
                    "text_en": "Analyze",
                    "text_cn": "分析",
                    "context": "Analyze button",
                    "category": "buttons"
                },
                "errors.file_too_large": {
                    "key": "errors.file_too_large",
                    "text_en": "File too large",
                    "text_cn": "文件过大",
                    "context": "File size error",
                    "category": "errors"
                }
            }
        }

        json.dump(data, f, ensure_ascii=False, indent=2)

    yield temp_path

    # Cleanup
    if temp_path.exists():
        temp_path.unlink()


@pytest.fixture
def loader(temp_strings_file):
    """Create BilingualStringLoader with temp file."""
    return BilingualStringLoader(strings_file=temp_strings_file)


class TestBilingualStringLoaderInit:
    """Test initialization."""

    def test_init_loads_file(self, temp_strings_file):
        """Loader auto-loads file on initialization."""
        loader = BilingualStringLoader(strings_file=temp_strings_file)

        assert len(loader.strings) > 0
        assert loader.version == "1.0"
        assert loader.last_updated == "2025-11-04"

    def test_init_missing_file(self):
        """Loader handles missing file gracefully."""
        loader = BilingualStringLoader(strings_file="nonexistent.json")

        assert len(loader.strings) == 0
        assert loader.version == "unknown"

    def test_init_default_path(self):
        """Loader uses default path if none provided."""
        loader = BilingualStringLoader()

        assert loader.strings_file == Path("data/ui_strings.json")


class TestBilingualStringLoaderLoad:
    """Test loading functionality."""

    def test_load_success(self, temp_strings_file):
        """Successfully loads strings from file."""
        loader = BilingualStringLoader(strings_file=temp_strings_file)

        assert loader.load() is True
        assert len(loader.strings) == 4
        assert "navigation.home" in loader.strings

    def test_load_missing_file(self, loader):
        """Returns False for missing file."""
        result = loader.load("nonexistent.json")

        assert result is False

    def test_load_invalid_json(self):
        """Handles invalid JSON gracefully."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            temp_path = Path(f.name)
            f.write("{invalid json}")

        loader = BilingualStringLoader(strings_file=temp_path)
        result = loader.load()

        assert result is False

        temp_path.unlink()

    def test_load_missing_strings_key(self):
        """Handles missing 'strings' key."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding='utf-8') as f:
            temp_path = Path(f.name)
            json.dump({"version": "1.0"}, f)

        loader = BilingualStringLoader(strings_file=temp_path)
        result = loader.load()

        assert result is False

        temp_path.unlink()

    def test_load_metadata(self, loader):
        """Loads metadata correctly."""
        assert loader.version == "1.0"
        assert loader.last_updated == "2025-11-04"
        assert "navigation" in loader.categories
        assert "buttons" in loader.categories


class TestBilingualStringLoaderRetrieval:
    """Test string retrieval methods."""

    def test_get_bilingual_success(self, loader):
        """get_bilingual() returns text_en and text_cn."""
        result = loader.get_bilingual("navigation.home")

        assert result is not None
        assert result["text_en"] == "Home"
        assert result["text_cn"] == "首页"

    def test_get_bilingual_missing_key(self, loader):
        """get_bilingual() returns None for missing key."""
        result = loader.get_bilingual("nonexistent.key")

        assert result is None

    def test_get_success(self, loader):
        """get() returns complete string data."""
        result = loader.get("navigation.home")

        assert result is not None
        assert result["text_en"] == "Home"
        assert result["text_cn"] == "首页"
        assert result["category"] == "navigation"
        assert result["context"] == "Main navigation"

    def test_get_missing_key(self, loader):
        """get() returns None for missing key."""
        result = loader.get("nonexistent.key")

        assert result is None

    def test_get_english(self, loader):
        """get_english() returns English text only."""
        result = loader.get_english("navigation.home")

        assert result == "Home"

    def test_get_english_missing_key(self, loader):
        """get_english() returns default for missing key."""
        result = loader.get_english("nonexistent.key", default="DEFAULT")

        assert result == "DEFAULT"

    def test_get_english_empty_default(self, loader):
        """get_english() returns empty string by default."""
        result = loader.get_english("nonexistent.key")

        assert result == ""

    def test_get_chinese(self, loader):
        """get_chinese() returns Chinese text only."""
        result = loader.get_chinese("navigation.home")

        assert result == "首页"

    def test_get_chinese_missing_key(self, loader):
        """get_chinese() returns default for missing key."""
        result = loader.get_chinese("nonexistent.key", default="默认")

        assert result == "默认"

    def test_get_all_strings_no_filter(self, loader):
        """get_all_strings() returns all strings without filter."""
        result = loader.get_all_strings()

        assert len(result) == 4
        assert "navigation.home" in result
        assert "buttons.analyze" in result

    def test_get_all_strings_filtered(self, loader):
        """get_all_strings() filters by category."""
        result = loader.get_all_strings(category="navigation")

        assert len(result) == 2
        assert "navigation.home" in result
        assert "navigation.upload" in result
        assert "buttons.analyze" not in result

    def test_get_all_strings_empty_category(self, loader):
        """get_all_strings() returns empty for nonexistent category."""
        result = loader.get_all_strings(category="nonexistent")

        assert len(result) == 0

    def test_get_by_category(self, loader):
        """get_by_category() returns strings in category."""
        result = loader.get_by_category("buttons")

        assert len(result) == 1
        assert "buttons.analyze" in result


class TestBilingualStringLoaderFormatting:
    """Test string formatting methods."""

    def test_format_bilingual_default_separator(self, loader):
        """format_bilingual() uses default ' / ' separator."""
        result = loader.format_bilingual("navigation.home")

        assert result == "Home / 首页"

    def test_format_bilingual_custom_separator(self, loader):
        """format_bilingual() uses custom separator."""
        result = loader.format_bilingual("navigation.home", separator=" - ")

        assert result == "Home - 首页"

    def test_format_bilingual_missing_key(self, loader):
        """format_bilingual() shows missing key message."""
        result = loader.format_bilingual("nonexistent.key")

        assert "[Missing: nonexistent.key]" in result


class TestBilingualStringLoaderUtilities:
    """Test utility methods."""

    def test_has_key_true(self, loader):
        """has_key() returns True for existing key."""
        assert loader.has_key("navigation.home") is True

    def test_has_key_false(self, loader):
        """has_key() returns False for missing key."""
        assert loader.has_key("nonexistent.key") is False

    def test_get_categories(self, loader):
        """get_categories() returns list of categories."""
        categories = loader.get_categories()

        assert "navigation" in categories
        assert "buttons" in categories
        assert "errors" in categories

    def test_get_stats(self, loader):
        """get_stats() returns statistics."""
        stats = loader.get_stats()

        assert stats["total_strings"] == 4
        assert stats["version"] == "1.0"
        assert stats["last_updated"] == "2025-11-04"
        assert "strings_by_category" in stats
        assert stats["strings_by_category"]["navigation"] == 2
        assert stats["strings_by_category"]["buttons"] == 1
        assert stats["strings_by_category"]["errors"] == 1

    def test_reload(self, loader):
        """reload() reloads strings from file."""
        original_count = len(loader.strings)

        # Reload should work
        result = loader.reload()

        assert result is True
        assert len(loader.strings) == original_count

    def test_repr(self, loader):
        """__repr__() returns string representation."""
        repr_str = repr(loader)

        assert "BilingualStringLoader" in repr_str
        assert "strings=4" in repr_str


class TestBilingualStringLoaderSingleton:
    """Test singleton pattern."""

    def test_get_loader_singleton(self, temp_strings_file):
        """get_loader() returns singleton instance."""
        loader1 = get_loader(temp_strings_file)
        loader2 = get_loader()

        assert loader1 is loader2

    def test_reload_strings_creates_new_instance(self, temp_strings_file):
        """reload_strings() creates new instance."""
        loader1 = get_loader(temp_strings_file)
        loader2 = reload_strings(temp_strings_file)

        # Both should have data
        assert len(loader1.strings) > 0
        assert len(loader2.strings) > 0


class TestBilingualStringLoaderEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_strings_file(self):
        """Handles empty strings section."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding='utf-8') as f:
            temp_path = Path(f.name)
            json.dump({"version": "1.0", "strings": {}}, f)

        loader = BilingualStringLoader(strings_file=temp_path)

        assert len(loader.strings) == 0
        assert loader.version == "1.0"

        temp_path.unlink()

    def test_unicode_handling(self, temp_strings_file):
        """Handles Unicode characters correctly."""
        loader = BilingualStringLoader(strings_file=temp_strings_file)

        chinese_text = loader.get_chinese("navigation.home")

        assert chinese_text == "首页"
        assert len(chinese_text) == 2  # 2 Chinese characters

    def test_category_not_in_metadata(self):
        """Handles strings with categories not in metadata list."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding='utf-8') as f:
            temp_path = Path(f.name)
            data = {
                "version": "1.0",
                "categories": ["navigation"],  # Only navigation listed
                "strings": {
                    "other.key": {
                        "key": "other.key",
                        "text_en": "Other",
                        "text_cn": "其他",
                        "category": "other"  # Category not in metadata
                    }
                }
            }
            json.dump(data, f, ensure_ascii=False)

        loader = BilingualStringLoader(strings_file=temp_path)

        # Should still work
        result = loader.get_all_strings(category="other")
        assert len(result) == 1

        temp_path.unlink()
