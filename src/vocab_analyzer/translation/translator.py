"""
Argos Translate service for offline neural machine translation.

This module provides English→Chinese translation using Argos Translate
with lazy loading and error handling.
"""

from typing import Optional, Dict, Any
import logging

# Configure logging
logger = logging.getLogger(__name__)


class ArgosTranslator:
    """
    Offline neural machine translation using Argos Translate.

    Uses lazy loading strategy - model is loaded on first translation request.
    Supports word, phrase, and sentence translation with configurable limits.

    Attributes:
        model_loaded: Whether translation model has been loaded
        translate_func: Argos translate function (loaded lazily)
    """

    MAX_TEXT_LENGTH = 2000  # Increased for sentence translation
    MAX_WORD_LENGTH = 100   # For single words
    MAX_PHRASE_LENGTH = 200  # For phrases

    def __init__(self):
        """Initialize translator with lazy loading."""
        self.model_loaded = False
        self.translate_func = None
        self._argos_translate = None

    def _load_model(self) -> None:
        """
        Load Argos Translate model (lazy loading).

        Raises:
            ImportError: If argostranslate not installed
            RuntimeError: If English→Chinese model not found
        """
        if self.model_loaded:
            return

        try:
            import argostranslate.translate
            import argostranslate.package
            import ctranslate2
            import sentencepiece as spm

            self._argos_translate = argostranslate.translate

            # Load installed languages
            languages = argostranslate.translate.load_installed_languages()

            # Find English and Chinese
            en_lang = next((l for l in languages if l.code == 'en'), None)
            zh_lang = next((l for l in languages if l.code == 'zh'), None)

            if not en_lang or not zh_lang:
                raise RuntimeError(
                    "English→Chinese model not installed. "
                    "Run: python -m vocab_analyzer.translation.auto_setup"
                )

            # Get translation object
            self._translation = en_lang.get_translation(zh_lang)
            if not self._translation:
                raise RuntimeError(
                    "English→Chinese translation not available"
                )

            # Get the package for direct translation
            packages = argostranslate.package.get_installed_packages()
            self._pkg = next((p for p in packages if p.from_code == 'en' and p.to_code == 'zh'), None)

            if not self._pkg:
                raise RuntimeError("English→Chinese package not found")

            # Load translation components directly (bypass stanza)
            model_path = str(self._pkg.package_path / 'model')
            self._translator = ctranslate2.Translator(model_path)
            sp_model_path = str(self._pkg.package_path / 'sentencepiece.model')
            self._sp_processor = spm.SentencePieceProcessor(model_file=sp_model_path)

            # Create custom translate function
            def translate_func(text, from_code, to_code):
                # Simple sentence splitting (no stanza needed for words/phrases)
                sentences = [s.strip() for s in text.split('.') if s.strip()]
                if not sentences:
                    sentences = [text]

                result = ''
                for sentence in sentences:
                    tokenized = self._sp_processor.encode(sentence, out_type=str)
                    translated = self._translator.translate_batch([tokenized])
                    translated = translated[0][0]['tokens']
                    detokenized = ''.join(translated)
                    detokenized = detokenized.replace('▁', ' ')
                    result += detokenized
                    if len(sentences) > 1:
                        result += '. '

                # Remove leading space
                if result and result[0] == ' ':
                    result = result[1:]

                return result.strip()

            self.translate_func = translate_func

            # Test translation
            test_result = self.translate_func("test", "en", "zh")
            if not test_result:
                raise RuntimeError("Translation test failed")

            self.model_loaded = True
            logger.info("Argos Translate model loaded successfully")

        except ImportError as e:
            raise ImportError(
                f"Required library not installed: {e}. "
                "Install with: pip install argostranslate ctranslate2 sentencepiece"
            ) from e

    def safe_translate(
        self,
        text: str,
        translation_type: str = "word"
    ) -> Optional[Dict[str, Any]]:
        """
        Translate text with error handling.

        Args:
            text: Source English text
            translation_type: Type (word/phrase/sentence)

        Returns:
            Translation result dict or None if failed:
            {
                "source_text": str,
                "target_text": str,
                "translation_type": str,
                "source": "argos",
                "confidence_score": float,
                "error": str (if failed)
            }
        """
        # Validate input
        if not text or not text.strip():
            return {
                "source_text": text,
                "target_text": None,
                "translation_type": translation_type,
                "source": "argos",
                "confidence_score": 0.0,
                "error": "Empty text"
            }

        text = text.strip()

        # Determine appropriate length limit based on type
        if translation_type == "word":
            max_length = self.MAX_WORD_LENGTH
        elif translation_type == "phrase":
            max_length = self.MAX_PHRASE_LENGTH
        else:  # sentence
            max_length = self.MAX_TEXT_LENGTH

        if len(text) > max_length:
            return {
                "source_text": text,
                "target_text": None,
                "translation_type": translation_type,
                "source": "argos",
                "confidence_score": 0.0,
                "error": f"Text exceeds {max_length} character limit for {translation_type}"
            }

        # Load model if needed
        try:
            self._load_model()
        except (ImportError, RuntimeError) as e:
            logger.error(f"Failed to load model: {e}")
            return {
                "source_text": text,
                "target_text": None,
                "translation_type": translation_type,
                "source": "argos",
                "confidence_score": 0.0,
                "error": str(e)
            }

        # Translate
        try:
            translation = self.translate_func(text, "en", "zh")

            # Validate result
            if not translation:
                return {
                    "source_text": text,
                    "target_text": None,
                    "translation_type": translation_type,
                    "source": "argos",
                    "confidence_score": 0.0,
                    "error": "Translation returned empty result"
                }

            # Determine confidence based on type
            confidence = self._estimate_confidence(text, translation_type)

            return {
                "source_text": text,
                "target_text": translation,
                "translation_type": translation_type,
                "source": "argos",
                "confidence_score": confidence,
                "error": None
            }

        except Exception as e:
            logger.error(f"Translation failed for '{text}': {e}")
            return {
                "source_text": text,
                "target_text": None,
                "translation_type": translation_type,
                "source": "argos",
                "confidence_score": 0.0,
                "error": f"Translation error: {str(e)}"
            }

    def _estimate_confidence(
        self,
        text: str,
        translation_type: str
    ) -> float:
        """
        Estimate translation confidence based on text characteristics.

        Args:
            text: Source text
            translation_type: Type of translation

        Returns:
            Confidence score (0.0-1.0)
        """
        # Base confidence for Argos Translate
        base_confidence = 0.70

        # Adjust based on text length and type
        if translation_type == "word":
            # Single words are generally reliable
            if len(text.split()) == 1:
                return min(base_confidence + 0.05, 1.0)

        elif translation_type == "phrase":
            # Phrases are moderately reliable
            if len(text.split()) <= 3:
                return base_confidence

        elif translation_type == "sentence":
            # Longer sentences less reliable
            word_count = len(text.split())
            if word_count > 20:
                return max(base_confidence - 0.10, 0.5)

        return base_confidence

    def is_available(self) -> bool:
        """
        Check if translator is available.

        Returns:
            True if model can be loaded
        """
        try:
            self._load_model()
            return True
        except (ImportError, RuntimeError):
            return False
