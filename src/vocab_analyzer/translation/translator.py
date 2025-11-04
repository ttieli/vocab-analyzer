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
    Supports word, phrase, and sentence translation with 500 character limit.

    Attributes:
        model_loaded: Whether translation model has been loaded
        translate_func: Argos translate function (loaded lazily)
    """

    MAX_TEXT_LENGTH = 500

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
            self._argos_translate = argostranslate.translate
            self.translate_func = argostranslate.translate.translate

            # Test that model works
            try:
                test_result = self.translate_func("test", "en", "zh")
                if not test_result:
                    raise RuntimeError(
                        "Translation returned empty result. "
                        "Model may not be installed."
                    )
            except Exception as e:
                raise RuntimeError(
                    f"English→Chinese model not available: {e}\\n"
                    "Run: python scripts/setup_translation.py"
                ) from e

            self.model_loaded = True
            logger.info("Argos Translate model loaded successfully")

        except ImportError as e:
            raise ImportError(
                "argostranslate not installed. "
                "Install with: pip install argostranslate"
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

        if len(text) > self.MAX_TEXT_LENGTH:
            return {
                "source_text": text,
                "target_text": None,
                "translation_type": translation_type,
                "source": "argos",
                "confidence_score": 0.0,
                "error": f"Text exceeds {self.MAX_TEXT_LENGTH} character limit"
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
