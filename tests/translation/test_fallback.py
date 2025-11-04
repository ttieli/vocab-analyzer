"""
Unit tests for TranslationChain and TranslationResult.

Tests fallback order, cache integration, tier availability, and graceful degradation.
Target coverage: 80%+ enforced by CI (pytest-cov with --cov-fail-under=80)
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile

from src.vocab_analyzer.translation.fallback import TranslationChain, TranslationResult


@pytest.fixture
def temp_cache_file():
    """Create temporary cache file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        temp_path = Path(f.name)
    yield temp_path
    if temp_path.exists():
        temp_path.unlink()


@pytest.fixture
def temp_dict_dir():
    """Create temporary dictionaries directory."""
    import shutil
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    if temp_dir.exists():
        shutil.rmtree(temp_dir)


@pytest.fixture
def mock_ecdict_matcher():
    """Create mock ECDICT matcher."""
    matcher = Mock()
    matcher._word_index = {
        "hello": {
            "translation": "int. 喂；你好",
            "pos": "int",
            "phonetic": "həˈləʊ",
            "collins": 5,
            "oxford": 1,
            "level": "A1"
        },
        "sophisticated": {
            "translation": "a. 精密的, 复杂的, 久经世故的",
            "pos": "adj",
            "phonetic": "səˈfɪstɪkeɪtɪd",
            "collins": 3,
            "oxford": 1,
            "level": "B2"
        }
    }
    return matcher


@pytest.fixture
def translation_chain(temp_cache_file, temp_dict_dir, mock_ecdict_matcher):
    """Create TranslationChain for testing."""
    return TranslationChain(
        cache_file=temp_cache_file,
        dictionaries_dir=temp_dict_dir,
        ecdict_matcher=mock_ecdict_matcher
    )


class TestTranslationResult:
    """Test TranslationResult class."""

    def test_init_success(self):
        """TranslationResult initializes with all fields."""
        result = TranslationResult(
            source_text="hello",
            target_text="你好",
            translation_type="word",
            source="ecdict",
            confidence_score=0.95
        )

        assert result.source_text == "hello"
        assert result.target_text == "你好"
        assert result.translation_type == "word"
        assert result.source == "ecdict"
        assert result.confidence_score == 0.95
        assert result.error is None
        assert result.metadata == {}

    def test_init_with_error(self):
        """TranslationResult handles error cases."""
        result = TranslationResult(
            source_text="test",
            target_text=None,
            translation_type="word",
            source="error",
            confidence_score=0.0,
            error="Translation failed"
        )

        assert result.target_text is None
        assert result.error == "Translation failed"

    def test_init_with_metadata(self):
        """TranslationResult stores metadata."""
        metadata = {"dictionary": "OALD9", "level": "B2"}
        result = TranslationResult(
            source_text="test",
            target_text="测试",
            translation_type="word",
            source="mdict",
            confidence_score=0.90,
            metadata=metadata
        )

        assert result.metadata == metadata

    def test_to_dict(self):
        """to_dict() serializes result correctly."""
        result = TranslationResult(
            source_text="test",
            target_text="测试",
            translation_type="word",
            source="ecdict",
            confidence_score=0.95,
            metadata={"level": "A1"}
        )

        d = result.to_dict()

        assert d["source_text"] == "test"
        assert d["target_text"] == "测试"
        assert d["translation_type"] == "word"
        assert d["source"] == "ecdict"
        assert d["confidence_score"] == 0.95
        assert d["error"] is None
        assert d["metadata"] == {"level": "A1"}

    def test_is_success_true(self):
        """is_success() returns True for successful translation."""
        result = TranslationResult(
            source_text="test",
            target_text="测试",
            translation_type="word",
            source="ecdict",
            confidence_score=0.95
        )

        assert result.is_success() is True

    def test_is_success_false_no_translation(self):
        """is_success() returns False when target_text is None."""
        result = TranslationResult(
            source_text="test",
            target_text=None,
            translation_type="word",
            source="error",
            confidence_score=0.0
        )

        assert result.is_success() is False

    def test_is_success_false_with_error(self):
        """is_success() returns False when error present."""
        result = TranslationResult(
            source_text="test",
            target_text="测试",
            translation_type="word",
            source="ecdict",
            confidence_score=0.95,
            error="Some error"
        )

        assert result.is_success() is False


class TestTranslationChainInit:
    """Test TranslationChain initialization."""

    def test_init_defaults(self, temp_cache_file, temp_dict_dir):
        """Chain initializes with default paths."""
        chain = TranslationChain(
            cache_file=temp_cache_file,
            dictionaries_dir=temp_dict_dir
        )

        assert chain.cache is not None
        assert chain.ecdict_matcher is None
        assert chain.mdict_manager is not None
        assert chain.argos_translator is not None

    def test_init_with_ecdict(self, temp_cache_file, temp_dict_dir, mock_ecdict_matcher):
        """Chain initializes with ECDICT matcher."""
        chain = TranslationChain(
            cache_file=temp_cache_file,
            dictionaries_dir=temp_dict_dir,
            ecdict_matcher=mock_ecdict_matcher
        )

        assert chain.ecdict_matcher is mock_ecdict_matcher


class TestTranslationChainValidation:
    """Test input validation."""

    def test_translate_empty_text(self, translation_chain):
        """Empty text returns error result."""
        result = translation_chain.translate("")

        assert result.is_success() is False
        assert result.error == "Empty text"
        assert result.confidence_score == 0.0

    def test_translate_whitespace_only(self, translation_chain):
        """Whitespace-only text returns error result."""
        result = translation_chain.translate("   ")

        assert result.is_success() is False
        assert result.error == "Empty text"


class TestTranslationChainInference:
    """Test translation type inference."""

    def test_infer_type_single_word(self, translation_chain):
        """Single word inferred as 'word'."""
        inferred = translation_chain._infer_type("hello")
        assert inferred == "word"

    def test_infer_type_phrase(self, translation_chain):
        """2-5 words inferred as 'phrase'."""
        assert translation_chain._infer_type("run out") == "phrase"
        assert translation_chain._infer_type("look up to someone") == "phrase"

    def test_infer_type_sentence(self, translation_chain):
        """6+ words inferred as 'sentence'."""
        text = "This is a complete sentence with many words"
        assert translation_chain._infer_type(text) == "sentence"


class TestTranslationChainCacheIntegration:
    """Test cache integration."""

    def test_cache_hit_returns_immediately(self, translation_chain):
        """Cache hit bypasses fallback chain."""
        # Pre-populate cache
        translation_chain.cache.set(
            text="cached",
            translation="缓存的",
            translation_type="word",
            source="ecdict",
            confidence_score=0.95
        )

        result = translation_chain.translate("cached", "word")

        assert result.is_success() is True
        assert result.target_text == "缓存的"
        assert result.source == "cached"
        assert result.metadata["original_source"] == "ecdict"

    def test_successful_translation_cached(self, translation_chain):
        """Successful translation is cached."""
        # Mock ECDICT to return result
        result = translation_chain.translate("hello", "word")

        assert result.is_success() is True

        # Second call should hit cache
        result2 = translation_chain.translate("hello", "word")
        assert result2.source == "cached"


class TestTranslationChainECDICT:
    """Test ECDICT tier."""

    def test_ecdict_word_success(self, translation_chain):
        """ECDICT successfully translates word."""
        result = translation_chain.translate("hello", "word")

        assert result.is_success() is True
        assert result.target_text == "int. 喂；你好"
        assert result.source == "ecdict"
        assert result.confidence_score == 0.95
        assert "level" in result.metadata

    def test_ecdict_case_insensitive(self, translation_chain):
        """ECDICT lookup is case-insensitive."""
        result = translation_chain.translate("HELLO", "word")

        assert result.is_success() is True
        assert result.target_text == "int. 喂；你好"

    def test_ecdict_not_found_falls_back(self, translation_chain):
        """ECDICT miss falls back to next tier."""
        with patch.object(translation_chain.mdict_manager, 'query_word', return_value=None):
            with patch.object(translation_chain.argos_translator, 'safe_translate') as mock_argos:
                mock_argos.return_value = {
                    "target_text": "未知的",
                    "confidence_score": 0.70
                }

                result = translation_chain.translate("unknownword", "word")

                # Should have tried argos after ECDICT miss
                assert mock_argos.called

    def test_ecdict_not_available_skips(self, temp_cache_file, temp_dict_dir):
        """Chain works without ECDICT matcher."""
        chain = TranslationChain(
            cache_file=temp_cache_file,
            dictionaries_dir=temp_dict_dir,
            ecdict_matcher=None  # No ECDICT
        )

        with patch.object(chain.mdict_manager, 'query_word', return_value=None):
            with patch.object(chain.argos_translator, 'safe_translate') as mock_argos:
                mock_argos.return_value = {
                    "target_text": "测试",
                    "confidence_score": 0.70
                }

                result = chain.translate("test", "word")

                # Should skip ECDICT and use Argos
                assert result.source == "argos"


class TestTranslationChainMdict:
    """Test Mdict tier."""

    def test_mdict_fallback_after_ecdict_miss(self, translation_chain):
        """Mdict is tried after ECDICT miss."""
        with patch.object(translation_chain.mdict_manager, 'query_word') as mock_mdict:
            mock_mdict.return_value = {
                "word": "test",
                "definition": "<html>test definition</html>",
                "dictionary": "OALD9",
                "priority": 1
            }

            result = translation_chain.translate("unknownword", "word")

            assert result.is_success() is True
            assert result.source == "mdict"
            assert result.confidence_score == 0.90
            assert result.metadata["dictionary"] == "OALD9"

    def test_mdict_handles_phrases(self, translation_chain):
        """Mdict can translate phrases."""
        with patch.object(translation_chain.mdict_manager, 'query_word') as mock_mdict:
            mock_mdict.return_value = {
                "word": "run out",
                "definition": "用完；耗尽",
                "dictionary": "LDOCE6",
                "priority": 2
            }

            result = translation_chain.translate("run out", "phrase")

            assert result.is_success() is True
            assert result.source == "mdict"


class TestTranslationChainArgos:
    """Test Argos Translate tier."""

    def test_argos_fallback_after_all_miss(self, translation_chain):
        """Argos is final fallback."""
        with patch.object(translation_chain.mdict_manager, 'query_word', return_value=None):
            with patch.object(translation_chain.argos_translator, 'safe_translate') as mock_argos:
                mock_argos.return_value = {
                    "source_text": "unknown phrase",
                    "target_text": "未知短语",
                    "translation_type": "phrase",
                    "source": "argos",
                    "confidence_score": 0.70,
                    "error": None
                }

                result = translation_chain.translate("unknown phrase", "phrase")

                assert result.is_success() is True
                assert result.source == "argos"
                assert result.confidence_score == 0.70

    def test_argos_handles_sentences(self, translation_chain):
        """Argos translates full sentences."""
        with patch.object(translation_chain.mdict_manager, 'query_word', return_value=None):
            with patch.object(translation_chain.argos_translator, 'safe_translate') as mock_argos:
                mock_argos.return_value = {
                    "source_text": "Time is running out.",
                    "target_text": "时间不多了。",
                    "translation_type": "sentence",
                    "source": "argos",
                    "confidence_score": 0.70,
                    "error": None
                }

                result = translation_chain.translate("Time is running out.")

                assert result.is_success() is True
                assert result.target_text == "时间不多了。"


class TestTranslationChainFallbackOrder:
    """Test fallback execution order."""

    def test_fallback_order_cache_first(self, translation_chain):
        """Cache is checked before any tier."""
        translation_chain.cache.set(
            text="test",
            translation="缓存",
            translation_type="word",
            source="ecdict",
            confidence_score=0.95
        )

        result = translation_chain.translate("test", "word")

        # Should return cached result, not call ECDICT
        assert result.source == "cached"

    def test_fallback_order_ecdict_before_mdict(self, translation_chain):
        """ECDICT is tried before Mdict."""
        # Word exists in ECDICT
        result = translation_chain.translate("hello", "word")

        assert result.source == "ecdict"  # Should not reach Mdict

    def test_fallback_order_mdict_before_argos(self, translation_chain):
        """Mdict is tried before Argos."""
        with patch.object(translation_chain.mdict_manager, 'query_word') as mock_mdict:
            mock_mdict.return_value = {
                "word": "unknown",
                "definition": "from mdict",
                "dictionary": "OALD9",
                "priority": 1
            }

            with patch.object(translation_chain.argos_translator, 'safe_translate') as mock_argos:
                result = translation_chain.translate("unknown", "word")

                # Should not call Argos if Mdict succeeded
                assert result.source == "mdict"
                assert not mock_argos.called


class TestTranslationChainGracefulDegradation:
    """Test graceful handling of tier failures."""

    def test_all_sources_fail(self, temp_cache_file, temp_dict_dir):
        """Returns error when all sources fail."""
        chain = TranslationChain(
            cache_file=temp_cache_file,
            dictionaries_dir=temp_dict_dir,
            ecdict_matcher=None  # No ECDICT
        )

        with patch.object(chain.mdict_manager, 'query_word', return_value=None):
            with patch.object(chain.argos_translator, 'safe_translate') as mock_argos:
                mock_argos.return_value = {
                    "source_text": "test",
                    "target_text": None,
                    "translation_type": "word",
                    "source": "argos",
                    "confidence_score": 0.0,
                    "error": "Model not available"
                }

                result = chain.translate("test", "word")

                assert result.is_success() is False
                assert result.error is not None

    def test_ecdict_error_continues_fallback(self, translation_chain):
        """ECDICT error doesn't stop fallback."""
        # Simulate ECDICT error by removing word index
        translation_chain.ecdict_matcher._word_index = None

        with patch.object(translation_chain.mdict_manager, 'query_word') as mock_mdict:
            mock_mdict.return_value = {
                "word": "test",
                "definition": "from mdict",
                "dictionary": "OALD9",
                "priority": 1
            }

            result = translation_chain.translate("test", "word")

            # Should continue to Mdict after ECDICT error
            assert result.source == "mdict"


class TestTranslationChainAvailability:
    """Test source availability checking."""

    def test_get_available_sources_all(self, translation_chain):
        """get_available_sources() reports all sources."""
        with patch.object(translation_chain.mdict_manager, 'is_available', return_value=True):
            with patch.object(translation_chain.argos_translator, 'is_available', return_value=True):
                sources = translation_chain.get_available_sources()

                assert sources["cache"] is True
                assert sources["ecdict"] is True
                assert sources["mdict"] is True
                assert sources["argos"] is True

    def test_get_available_sources_partial(self, temp_cache_file, temp_dict_dir):
        """get_available_sources() reports partial availability."""
        chain = TranslationChain(
            cache_file=temp_cache_file,
            dictionaries_dir=temp_dict_dir,
            ecdict_matcher=None
        )

        sources = chain.get_available_sources()

        assert sources["cache"] is True
        assert sources["ecdict"] is False
        assert sources["mdict"] is False  # No .mdx files in temp dir
        assert sources["argos"] is False  # Model not installed in test env


class TestTranslationChainCacheManagement:
    """Test cache management operations."""

    def test_save_cache(self, translation_chain):
        """save_cache() persists cache to disk."""
        translation_chain.cache.set(
            text="test",
            translation="测试",
            translation_type="word",
            source="ecdict",
            confidence_score=0.95
        )

        translation_chain.save_cache()

        # Verify file was created
        assert translation_chain.cache.cache_file.exists()

    def test_get_cache_stats(self, translation_chain):
        """get_cache_stats() returns statistics."""
        translation_chain.cache.set(
            text="test",
            translation="测试",
            translation_type="word",
            source="ecdict",
            confidence_score=0.95
        )

        stats = translation_chain.get_cache_stats()

        assert "total_entries" in stats
        assert stats["total_entries"] >= 1
