"""
TranslationChain for three-tier translation fallback.

This module coordinates ECDICT → Mdict → Argos Translate fallback logic
with automatic caching and confidence scoring.
"""

from typing import Optional, Dict, Any
from pathlib import Path
import logging

from .cache import TranslationCache
from .translator import ArgosTranslator
from .dictionary import MdictDictionary

# Configure logging
logger = logging.getLogger(__name__)


class TranslationResult:
    """
    Result from translation chain with source tracking.

    Attributes:
        source_text: Original English text
        target_text: Chinese translation
        translation_type: Type (word/phrase/sentence)
        source: Translation source (ecdict/mdict/argos/cached)
        confidence_score: Quality estimate (0.0-1.0)
        error: Error message if translation failed
        metadata: Additional information from source
    """

    def __init__(
        self,
        source_text: str,
        target_text: Optional[str],
        translation_type: str,
        source: str,
        confidence_score: float,
        error: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.source_text = source_text
        self.target_text = target_text
        self.translation_type = translation_type
        self.source = source
        self.confidence_score = confidence_score
        self.error = error
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert result to dictionary.

        Returns:
            Dictionary representation
        """
        return {
            "source_text": self.source_text,
            "target_text": self.target_text,
            "translation_type": self.translation_type,
            "source": self.source,
            "confidence_score": self.confidence_score,
            "error": self.error,
            "metadata": self.metadata
        }

    def is_success(self) -> bool:
        """Check if translation was successful."""
        return self.target_text is not None and self.error is None


class TranslationChain:
    """
    Three-tier translation fallback chain with caching.

    Fallback order:
    1. Check cache first (instant)
    2. ECDICT - Fast dictionary lookup (~1ms)
    3. Mdict - Professional dictionaries (~10ms)
    4. Argos Translate - Neural MT (~100ms)

    Confidence scores:
    - ECDICT: 0.95 (authoritative dictionary)
    - Mdict: 0.90 (professional dictionaries)
    - Argos: 0.70 (ML translation, variable quality)
    - Cached: Original confidence preserved

    Attributes:
        cache: Translation cache instance
        ecdict_matcher: ECDICT word matcher (optional)
        mdict_manager: Mdict dictionary manager
        argos_translator: Argos Translate instance
    """

    def __init__(
        self,
        cache_file: Optional[Path | str] = None,
        dictionaries_dir: Optional[Path | str] = None,
        ecdict_matcher: Optional[Any] = None
    ):
        """
        Initialize translation chain.

        Args:
            cache_file: Path to translation cache JSON
            dictionaries_dir: Path to .mdx dictionaries
            ecdict_matcher: LevelMatcher instance with ECDICT loaded
        """
        # Initialize components
        self.cache = TranslationCache(
            cache_file=cache_file or "data/translation_cache.json"
        )

        self.ecdict_matcher = ecdict_matcher

        self.mdict_manager = MdictDictionary(
            dictionaries_dir=dictionaries_dir or "data/dictionaries"
        )

        self.argos_translator = ArgosTranslator()

        logger.info("TranslationChain initialized")

    def translate(
        self,
        text: str,
        translation_type: Optional[str] = None
    ) -> TranslationResult:
        """
        Translate text using fallback chain.

        Args:
            text: Source English text
            translation_type: Type hint (word/phrase/sentence), auto-inferred if None

        Returns:
            TranslationResult with translation or error
        """
        # Validate input
        if not text or not text.strip():
            return TranslationResult(
                source_text=text,
                target_text=None,
                translation_type="unknown",
                source="error",
                confidence_score=0.0,
                error="Empty text"
            )

        text = text.strip()

        # Infer type if not provided
        if translation_type is None:
            translation_type = self._infer_type(text)

        # 1. Check cache first
        cached = self.cache.get(text, translation_type)
        if cached:
            logger.debug(f"Cache hit: {text}")
            return TranslationResult(
                source_text=text,
                target_text=cached["target_text"],
                translation_type=translation_type,
                source="cached",
                confidence_score=cached["confidence_score"],
                metadata={"original_source": cached["source"]}
            )

        # 2. Try ECDICT (fast dictionary lookup)
        if translation_type == "word":
            ecdict_result = self._try_ecdict(text)
            if ecdict_result:
                # Cache and return
                self.cache.set(
                    text=text,
                    translation=ecdict_result["translation"],
                    translation_type=translation_type,
                    source="ecdict",
                    confidence_score=0.95
                )
                return TranslationResult(
                    source_text=text,
                    target_text=ecdict_result["translation"],
                    translation_type=translation_type,
                    source="ecdict",
                    confidence_score=0.95,
                    metadata=ecdict_result.get("metadata", {})
                )

        # 3. Try Mdict dictionaries
        mdict_result = self._try_mdict(text)
        if mdict_result:
            # Cache and return
            self.cache.set(
                text=text,
                translation=mdict_result["translation"],
                translation_type=translation_type,
                source="mdict",
                confidence_score=0.90
            )
            return TranslationResult(
                source_text=text,
                target_text=mdict_result["translation"],
                translation_type=translation_type,
                source="mdict",
                confidence_score=0.90,
                metadata=mdict_result.get("metadata", {})
            )

        # 4. Fall back to Argos Translate
        argos_result = self._try_argos(text, translation_type)
        if argos_result and argos_result["target_text"]:
            # Cache and return
            self.cache.set(
                text=text,
                translation=argos_result["target_text"],
                translation_type=translation_type,
                source="argos",
                confidence_score=argos_result["confidence_score"]
            )
            return TranslationResult(
                source_text=text,
                target_text=argos_result["target_text"],
                translation_type=translation_type,
                source="argos",
                confidence_score=argos_result["confidence_score"]
            )

        # All sources failed
        error_msg = argos_result.get("error", "Translation unavailable") if argos_result else "All translation sources failed"
        return TranslationResult(
            source_text=text,
            target_text=None,
            translation_type=translation_type,
            source="error",
            confidence_score=0.0,
            error=error_msg
        )

    def _infer_type(self, text: str) -> str:
        """
        Infer translation type from text.

        Args:
            text: Source text

        Returns:
            Inferred type (word/phrase/sentence)
        """
        word_count = len(text.split())

        if word_count == 1:
            return "word"
        elif word_count <= 5:
            return "phrase"
        else:
            return "sentence"

    def _try_ecdict(self, word: str) -> Optional[Dict[str, Any]]:
        """
        Try ECDICT lookup.

        Args:
            word: Single word to look up

        Returns:
            Dict with translation and metadata, or None if not found
        """
        if not self.ecdict_matcher:
            logger.debug("ECDICT matcher not available")
            return None

        try:
            # Query ECDICT word index
            word_lower = word.lower()

            if not hasattr(self.ecdict_matcher, '_word_index'):
                logger.warning("ECDICT word index not loaded")
                return None

            word_data = self.ecdict_matcher._word_index.get(word_lower)

            if not word_data:
                logger.debug(f"Word not found in ECDICT: {word}")
                return None

            # Extract translation
            translation = word_data.get("translation", "")

            if not translation:
                logger.debug(f"No translation in ECDICT for: {word}")
                return None

            # Build metadata
            metadata = {
                "pos": word_data.get("pos", ""),
                "phonetic": word_data.get("phonetic", ""),
                "collins": word_data.get("collins", 0),
                "oxford": word_data.get("oxford", 0),
                "level": word_data.get("level", "")
            }

            logger.debug(f"ECDICT hit: {word} → {translation[:50]}...")

            return {
                "translation": translation,
                "metadata": metadata
            }

        except Exception as e:
            logger.error(f"ECDICT lookup error for '{word}': {e}")
            return None

    def _try_mdict(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Try Mdict dictionary lookup.

        Args:
            text: Text to look up

        Returns:
            Dict with translation and metadata, or None if not found
        """
        try:
            result = self.mdict_manager.query_word(text)

            if not result:
                logger.debug(f"Word not found in Mdict: {text}")
                return None

            logger.debug(f"Mdict hit: {text} from {result['dictionary']}")

            return {
                "translation": result["definition"],
                "metadata": {
                    "dictionary": result["dictionary"],
                    "priority": result["priority"]
                }
            }

        except Exception as e:
            logger.error(f"Mdict lookup error for '{text}': {e}")
            return None

    def _try_argos(
        self,
        text: str,
        translation_type: str
    ) -> Optional[Dict[str, Any]]:
        """
        Try Argos Translate.

        Args:
            text: Text to translate
            translation_type: Type (word/phrase/sentence)

        Returns:
            Translation result dict
        """
        try:
            result = self.argos_translator.safe_translate(text, translation_type)

            if result and result.get("target_text"):
                logger.debug(f"Argos hit: {text} → {result['target_text'][:50]}...")
            else:
                logger.debug(f"Argos translation failed: {result.get('error', 'Unknown error')}")

            return result

        except Exception as e:
            logger.error(f"Argos translation error for '{text}': {e}")
            return {
                "source_text": text,
                "target_text": None,
                "translation_type": translation_type,
                "source": "argos",
                "confidence_score": 0.0,
                "error": str(e)
            }

    def get_available_sources(self) -> Dict[str, bool]:
        """
        Check which translation sources are available.

        Returns:
            Dict mapping source name to availability
        """
        return {
            "cache": True,  # Always available
            "ecdict": self.ecdict_matcher is not None and hasattr(self.ecdict_matcher, '_word_index'),
            "mdict": self.mdict_manager.is_available(),
            "argos": self.argos_translator.is_available()
        }

    def save_cache(self) -> None:
        """Persist translation cache to disk."""
        self.cache.save()

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get translation cache statistics."""
        return self.cache.get_stats()
