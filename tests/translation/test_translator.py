"""
Unit tests for ArgosTranslator.

Tests lazy model loading, translation for different types, error handling.
Target coverage: 80%+ enforced by CI (pytest-cov with --cov-fail-under=80)
"""

import pytest
from unittest.mock import Mock, patch, MagicMock

from src.vocab_analyzer.translation.translator import ArgosTranslator


@pytest.fixture
def translator():
    """Create ArgosTranslator instance for testing."""
    return ArgosTranslator()


class TestArgosTranslatorInit:
    """Test translator initialization."""

    def test_init_not_loaded(self, translator):
        """Translator initializes without loading model."""
        assert translator.model_loaded is False
        assert translator.translate_func is None


class TestArgosTranslatorLazyLoading:
    """Test lazy model loading."""

    @patch('src.vocab_analyzer.translation.translator.argostranslate')
    def test_load_model_success(self, mock_argos, translator):
        """Model loads successfully on first use."""
        # Mock the translate module
        mock_translate = Mock()
        mock_translate.translate = Mock(return_value="测试")
        mock_argos.translate = mock_translate

        translator._load_model()

        assert translator.model_loaded is True
        assert translator.translate_func is not None

    @patch('src.vocab_analyzer.translation.translator.argostranslate')
    def test_load_model_only_once(self, mock_argos, translator):
        """Model loads only once (lazy loading)."""
        mock_translate = Mock()
        mock_translate.translate = Mock(return_value="测试")
        mock_argos.translate = mock_translate

        translator._load_model()
        first_func = translator.translate_func

        translator._load_model()
        second_func = translator.translate_func

        assert first_func is second_func  # Same function instance

    def test_load_model_import_error(self, translator):
        """Raises ImportError if argostranslate not installed."""
        with patch.dict('sys.modules', {'argostranslate': None}):
            with pytest.raises(ImportError, match="argostranslate not installed"):
                translator._load_model()

    @patch('src.vocab_analyzer.translation.translator.argostranslate')
    def test_load_model_no_translation_model(self, mock_argos, translator):
        """Raises RuntimeError if translation model not available."""
        mock_translate = Mock()
        mock_translate.translate = Mock(return_value="")  # Empty result
        mock_argos.translate = mock_translate

        with pytest.raises(RuntimeError, match="Model may not be installed"):
            translator._load_model()


class TestArgosTranslatorSafeTranslate:
    """Test safe_translate method."""

    @patch('src.vocab_analyzer.translation.translator.argostranslate')
    def test_translate_word_success(self, mock_argos, translator):
        """Successfully translates a word."""
        mock_translate = Mock()
        mock_translate.translate = Mock(return_value="你好")
        mock_argos.translate = mock_translate

        result = translator.safe_translate("hello", "word")

        assert result["source_text"] == "hello"
        assert result["target_text"] == "你好"
        assert result["translation_type"] == "word"
        assert result["source"] == "argos"
        assert result["confidence_score"] == 0.75  # Word boost
        assert result["error"] is None

    @patch('src.vocab_analyzer.translation.translator.argostranslate')
    def test_translate_phrase_success(self, mock_argos, translator):
        """Successfully translates a phrase."""
        mock_translate = Mock()
        mock_translate.translate = Mock(return_value="用完")
        mock_argos.translate = mock_translate

        result = translator.safe_translate("run out", "phrase")

        assert result["target_text"] == "用完"
        assert result["translation_type"] == "phrase"
        assert result["confidence_score"] == 0.70  # Base confidence

    @patch('src.vocab_analyzer.translation.translator.argostranslate')
    def test_translate_sentence_success(self, mock_argos, translator):
        """Successfully translates a sentence."""
        mock_translate = Mock()
        mock_translate.translate = Mock(return_value="你好吗?")
        mock_argos.translate = mock_translate

        result = translator.safe_translate("How are you?", "sentence")

        assert result["target_text"] == "你好吗?"
        assert result["translation_type"] == "sentence"
        assert result["confidence_score"] == 0.70

    def test_translate_empty_text(self, translator):
        """Empty text returns error result."""
        result = translator.safe_translate("", "word")

        assert result["target_text"] is None
        assert result["error"] == "Empty text"
        assert result["confidence_score"] == 0.0

    def test_translate_whitespace_only(self, translator):
        """Whitespace-only text returns error result."""
        result = translator.safe_translate("   ", "word")

        assert result["target_text"] is None
        assert result["error"] == "Empty text"

    def test_translate_text_too_long(self, translator):
        """Text exceeding 500 chars returns error."""
        long_text = "a" * 501

        result = translator.safe_translate(long_text, "word")

        assert result["target_text"] is None
        assert "exceeds 500 character limit" in result["error"]
        assert result["confidence_score"] == 0.0

    def test_translate_text_at_limit(self, translator):
        """Text at 500 char limit is accepted."""
        text_at_limit = "a" * 500

        with patch('src.vocab_analyzer.translation.translator.argostranslate') as mock:
            mock.translate.translate = Mock(return_value="翻译")
            result = translator.safe_translate(text_at_limit, "word")

        # Should not error on length
        assert "exceeds" not in result.get("error", "")

    @patch('src.vocab_analyzer.translation.translator.argostranslate')
    def test_translate_model_load_failure(self, mock_argos, translator):
        """Model load failure returns error result."""
        mock_argos.translate.translate = Mock(side_effect=Exception("Model error"))

        result = translator.safe_translate("test", "word")

        assert result["target_text"] is None
        assert "error" in result
        assert result["confidence_score"] == 0.0

    @patch('src.vocab_analyzer.translation.translator.argostranslate')
    def test_translate_returns_empty(self, mock_argos, translator):
        """Empty translation result handled gracefully."""
        mock_translate = Mock()
        mock_translate.translate = Mock(side_effect=["test", ""])  # First for load test, second empty
        mock_argos.translate = mock_translate

        # First call loads model
        translator._load_model()

        # Second call with empty result
        with patch.object(translator, 'translate_func', return_value=""):
            result = translator.safe_translate("test", "word")

        assert result["target_text"] is None
        assert "empty result" in result["error"].lower()

    @patch('src.vocab_analyzer.translation.translator.argostranslate')
    def test_translate_exception_handling(self, mock_argos, translator):
        """Translation exceptions handled gracefully."""
        mock_translate = Mock()
        mock_translate.translate = Mock(side_effect=["test", Exception("Network error")])
        mock_argos.translate = mock_translate

        translator._load_model()

        with patch.object(translator, 'translate_func', side_effect=Exception("Test error")):
            result = translator.safe_translate("test", "word")

        assert result["target_text"] is None
        assert "error" in result
        assert "Test error" in result["error"]

    @patch('src.vocab_analyzer.translation.translator.argostranslate')
    def test_translate_strips_whitespace(self, mock_argos, translator):
        """Input text is stripped of whitespace."""
        mock_translate = Mock()
        mock_translate.translate = Mock(return_value="你好")
        mock_argos.translate = mock_translate

        result = translator.safe_translate("  hello  ", "word")

        # Should call with stripped text
        assert result["source_text"] == "  hello  "  # Original preserved
        assert result["target_text"] == "你好"


class TestArgosTranslatorConfidence:
    """Test confidence score estimation."""

    @patch('src.vocab_analyzer.translation.translator.argostranslate')
    def test_word_confidence_single_word(self, mock_argos, translator):
        """Single word gets confidence boost."""
        mock_translate = Mock()
        mock_translate.translate = Mock(return_value="测试")
        mock_argos.translate = mock_translate

        result = translator.safe_translate("test", "word")

        # Single word: 0.70 + 0.05 = 0.75
        assert result["confidence_score"] == 0.75

    @patch('src.vocab_analyzer.translation.translator.argostranslate')
    def test_word_confidence_multiple_words(self, mock_argos, translator):
        """Multiple words get base confidence."""
        mock_translate = Mock()
        mock_translate.translate = Mock(return_value="测试词组")
        mock_argos.translate = mock_translate

        result = translator.safe_translate("test phrase", "word")

        # Multiple words: base 0.70
        assert result["confidence_score"] == 0.70

    @patch('src.vocab_analyzer.translation.translator.argostranslate')
    def test_phrase_confidence(self, mock_argos, translator):
        """Phrases get base confidence."""
        mock_translate = Mock()
        mock_translate.translate = Mock(return_value="用完")
        mock_argos.translate = mock_translate

        result = translator.safe_translate("run out", "phrase")

        assert result["confidence_score"] == 0.70

    @patch('src.vocab_analyzer.translation.translator.argostranslate')
    def test_sentence_confidence_short(self, mock_argos, translator):
        """Short sentences get base confidence."""
        mock_translate = Mock()
        mock_translate.translate = Mock(return_value="你好吗?")
        mock_argos.translate = mock_translate

        result = translator.safe_translate("How are you?", "sentence")

        assert result["confidence_score"] == 0.70

    @patch('src.vocab_analyzer.translation.translator.argostranslate')
    def test_sentence_confidence_long(self, mock_argos, translator):
        """Long sentences get reduced confidence."""
        long_sentence = " ".join(["word"] * 25)  # 25 words
        mock_translate = Mock()
        mock_translate.translate = Mock(return_value="长句子")
        mock_argos.translate = mock_translate

        result = translator.safe_translate(long_sentence, "sentence")

        # Long sentence: 0.70 - 0.10 = 0.60
        assert result["confidence_score"] == 0.60


class TestArgosTranslatorAvailability:
    """Test is_available method."""

    @patch('src.vocab_analyzer.translation.translator.argostranslate')
    def test_is_available_when_model_loads(self, mock_argos, translator):
        """is_available returns True when model loads."""
        mock_translate = Mock()
        mock_translate.translate = Mock(return_value="测试")
        mock_argos.translate = mock_translate

        assert translator.is_available() is True

    def test_is_available_when_not_installed(self, translator):
        """is_available returns False when not installed."""
        with patch.dict('sys.modules', {'argostranslate': None}):
            assert translator.is_available() is False

    @patch('src.vocab_analyzer.translation.translator.argostranslate')
    def test_is_available_when_model_missing(self, mock_argos, translator):
        """is_available returns False when model not installed."""
        mock_translate = Mock()
        mock_translate.translate = Mock(return_value="")  # Empty = model missing
        mock_argos.translate = mock_translate

        assert translator.is_available() is False
