"""
Translation configuration loader.

This module loads translation settings from YAML configuration file
with default fallbacks for missing values.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import logging

# Configure logging
logger = logging.getLogger(__name__)


class TranslationConfig:
    """
    Translation configuration manager.

    Loads settings from data/translation_config.yaml with sensible defaults.
    All configuration values are accessible as attributes.

    Attributes:
        cache_enabled: Whether translation caching is enabled
        cache_file_path: Path to cache JSON file
        cache_expiry_days: Days before cache entries expire
        ecdict_enabled: Whether ECDICT is enabled
        mdict_enabled: Whether Mdict dictionaries are enabled
        argos_enabled: Whether Argos Translate is enabled
        ... (and many more)
    """

    # Default configuration
    DEFAULTS = {
        "cache": {
            "enabled": True,
            "file_path": "data/translation_cache.json",
            "expiry_days": 30,
            "auto_save_interval": 300,
            "max_entries": 10000
        },
        "ecdict": {
            "enabled": True,
            "vocabulary_file": "data/dictionaries/ECDICT/ecdict.csv",
            "confidence_score": 0.95
        },
        "mdict": {
            "enabled": True,
            "dictionaries_dir": "data/dictionaries",
            "confidence_score": 0.90,
            "priorities": {
                "oald": 1,
                "ldoce": 2,
                "collins": 3,
                "default": 5
            }
        },
        "argos": {
            "enabled": True,
            "model_dir": "data/translation_models",
            "source_lang": "en",
            "target_lang": "zh",
            "confidence": {
                "word": 0.75,
                "phrase": 0.70,
                "sentence": 0.70,
                "long_sentence": 0.60
            },
            "max_text_length": 500,
            "long_sentence_threshold": 20
        },
        "chain": {
            "timeout_ms": {
                "ecdict": 10,
                "mdict": 50,
                "argos": 5000
            },
            "max_retries": 0,
            "retry_delay_ms": 0
        },
        "logging": {
            "enabled": True,
            "level": "INFO",
            "log_translations": False,
            "log_cache_hits": False
        },
        "performance": {
            "lazy_loading": True,
            "preload_ecdict": True,
            "preload_mdict": False,
            "preload_argos": False
        },
        "features": {
            "auto_detect_type": True,
            "cache_negative_results": False,
            "parallel_lookup": False
        }
    }

    def __init__(self, config_file: Optional[Path | str] = None):
        """
        Initialize configuration loader.

        Args:
            config_file: Path to YAML config file (optional)
        """
        self.config_file = Path(config_file) if config_file else Path("data/translation_config.yaml")
        self._config: Dict[str, Any] = {}

        # Load configuration
        self.load()

    def load(self) -> None:
        """
        Load configuration from file with defaults.

        If file doesn't exist or has errors, uses default configuration.
        Logs warnings for missing or invalid values.
        """
        # Start with defaults
        self._config = self._deep_copy(self.DEFAULTS)

        # Try to load from file
        if not self.config_file.exists():
            logger.warning(
                f"Config file not found: {self.config_file}. Using defaults."
            )
            return

        try:
            import yaml

            with open(self.config_file, 'r', encoding='utf-8') as f:
                user_config = yaml.safe_load(f)

            if user_config:
                # Merge user config with defaults
                self._config = self._deep_merge(self._config, user_config)
                logger.info(f"Loaded configuration from {self.config_file}")
            else:
                logger.warning(f"Empty config file: {self.config_file}. Using defaults.")

        except ImportError:
            logger.error(
                "PyYAML not installed. Cannot load config file. Using defaults. "
                "Install with: pip install pyyaml"
            )
        except Exception as e:
            logger.error(
                f"Failed to load config from {self.config_file}: {e}. Using defaults."
            )

    def _deep_copy(self, d: Dict) -> Dict:
        """Deep copy dictionary."""
        import copy
        return copy.deepcopy(d)

    def _deep_merge(self, base: Dict, override: Dict) -> Dict:
        """
        Deep merge two dictionaries.

        Args:
            base: Base dictionary (defaults)
            override: Override dictionary (user config)

        Returns:
            Merged dictionary
        """
        result = base.copy()

        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                # Recursively merge nested dicts
                result[key] = self._deep_merge(result[key], value)
            else:
                # Override value
                result[key] = value

        return result

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value by dot-notation path.

        Args:
            key_path: Dot-separated path (e.g., "cache.enabled")
            default: Default value if not found

        Returns:
            Configuration value or default

        Example:
            config.get("cache.enabled")  # Returns True
            config.get("cache.expiry_days")  # Returns 30
            config.get("mdict.priorities.oald")  # Returns 1
        """
        keys = key_path.split(".")
        value = self._config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def to_dict(self) -> Dict[str, Any]:
        """
        Get full configuration as dictionary.

        Returns:
            Complete configuration dict
        """
        return self._config.copy()

    # Convenience properties for common settings

    @property
    def cache_enabled(self) -> bool:
        """Whether translation caching is enabled."""
        return self.get("cache.enabled", True)

    @property
    def cache_file_path(self) -> str:
        """Path to cache JSON file."""
        return self.get("cache.file_path", "data/translation_cache.json")

    @property
    def cache_expiry_days(self) -> int:
        """Days before cache entries expire."""
        return self.get("cache.expiry_days", 30)

    @property
    def cache_auto_save_interval(self) -> int:
        """Auto-save interval in seconds."""
        return self.get("cache.auto_save_interval", 300)

    @property
    def cache_max_entries(self) -> int:
        """Maximum cache entries."""
        return self.get("cache.max_entries", 10000)

    @property
    def ecdict_enabled(self) -> bool:
        """Whether ECDICT is enabled."""
        return self.get("ecdict.enabled", True)

    @property
    def ecdict_vocabulary_file(self) -> str:
        """Path to ECDICT CSV file."""
        return self.get("ecdict.vocabulary_file", "data/dictionaries/ECDICT/ecdict.csv")

    @property
    def ecdict_confidence_score(self) -> float:
        """Confidence score for ECDICT translations."""
        return self.get("ecdict.confidence_score", 0.95)

    @property
    def mdict_enabled(self) -> bool:
        """Whether Mdict is enabled."""
        return self.get("mdict.enabled", True)

    @property
    def mdict_dictionaries_dir(self) -> str:
        """Path to Mdict dictionaries directory."""
        return self.get("mdict.dictionaries_dir", "data/dictionaries")

    @property
    def mdict_confidence_score(self) -> float:
        """Confidence score for Mdict translations."""
        return self.get("mdict.confidence_score", 0.90)

    @property
    def mdict_priorities(self) -> Dict[str, int]:
        """Dictionary priorities mapping."""
        return self.get("mdict.priorities", {
            "oald": 1,
            "ldoce": 2,
            "collins": 3,
            "default": 5
        })

    @property
    def argos_enabled(self) -> bool:
        """Whether Argos Translate is enabled."""
        return self.get("argos.enabled", True)

    @property
    def argos_max_text_length(self) -> int:
        """Maximum text length for Argos."""
        return self.get("argos.max_text_length", 500)

    @property
    def argos_confidence_word(self) -> float:
        """Confidence score for word translations."""
        return self.get("argos.confidence.word", 0.75)

    @property
    def argos_confidence_phrase(self) -> float:
        """Confidence score for phrase translations."""
        return self.get("argos.confidence.phrase", 0.70)

    @property
    def argos_confidence_sentence(self) -> float:
        """Confidence score for sentence translations."""
        return self.get("argos.confidence.sentence", 0.70)

    @property
    def argos_long_sentence_threshold(self) -> int:
        """Word count threshold for long sentences."""
        return self.get("argos.long_sentence_threshold", 20)

    @property
    def auto_detect_type(self) -> bool:
        """Whether to auto-detect translation type."""
        return self.get("features.auto_detect_type", True)

    @property
    def cache_negative_results(self) -> bool:
        """Whether to cache failed translations."""
        return self.get("features.cache_negative_results", False)

    @property
    def lazy_loading(self) -> bool:
        """Whether to use lazy loading."""
        return self.get("performance.lazy_loading", True)

    @property
    def preload_ecdict(self) -> bool:
        """Whether to preload ECDICT at startup."""
        return self.get("performance.preload_ecdict", True)

    @property
    def logging_enabled(self) -> bool:
        """Whether logging is enabled."""
        return self.get("logging.enabled", True)

    @property
    def logging_level(self) -> str:
        """Logging level."""
        return self.get("logging.level", "INFO")

    def __repr__(self) -> str:
        """String representation of config."""
        return f"TranslationConfig(file={self.config_file})"


# Global singleton instance
_config_instance: Optional[TranslationConfig] = None


def get_config(config_file: Optional[Path | str] = None) -> TranslationConfig:
    """
    Get global configuration instance (singleton).

    Args:
        config_file: Path to config file (only used on first call)

    Returns:
        TranslationConfig instance
    """
    global _config_instance

    if _config_instance is None:
        _config_instance = TranslationConfig(config_file)

    return _config_instance


def reload_config(config_file: Optional[Path | str] = None) -> TranslationConfig:
    """
    Reload configuration (useful for testing or config changes).

    Args:
        config_file: Path to config file

    Returns:
        New TranslationConfig instance
    """
    global _config_instance
    _config_instance = TranslationConfig(config_file)
    return _config_instance


class CEFRDefinitionLoader:
    """
    Loader for CEFR level definitions.

    Loads bilingual CEFR level descriptions from JSON file.
    """

    def __init__(self, definitions_file: Optional[Path | str] = None):
        """
        Initialize CEFR definition loader.

        Args:
            definitions_file: Path to CEFR definitions JSON file
        """
        if definitions_file is None:
            # Default to data/cefr_definitions.json relative to project root
            definitions_file = Path(__file__).parent.parent.parent.parent / "data" / "cefr_definitions.json"

        self.definitions_file = Path(definitions_file)
        self._definitions = None
        self._load()

    def _load(self):
        """Load CEFR definitions from JSON file."""
        import json

        try:
            with open(self.definitions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._definitions = data
                logger.info(f"Loaded {len(data.get('levels', {}))} CEFR level definitions from {self.definitions_file}")
        except Exception as e:
            logger.error(f"Failed to load CEFR definitions from {self.definitions_file}: {e}")
            self._definitions = {"version": "1.0", "levels": {}}

    def get_all_levels(self) -> Dict[str, Any]:
        """
        Get all CEFR level definitions.

        Returns:
            Dictionary with version, last_updated, and levels
        """
        return self._definitions

    def get_level(self, level_code: str) -> Optional[Dict[str, Any]]:
        """
        Get definition for a specific CEFR level.

        Args:
            level_code: CEFR level code (e.g., 'A1', 'B2', 'C2+')

        Returns:
            Level definition dict or None if not found
        """
        levels = self._definitions.get("levels", {})
        return levels.get(level_code.upper())

    def validate_all(self) -> bool:
        """
        Validate that all required CEFR levels are present.

        Returns:
            True if all 7 levels (A1-C2+) are defined
        """
        required_levels = ["A1", "A2", "B1", "B2", "C1", "C2", "C2+"]
        levels = self._definitions.get("levels", {})
        return all(level in levels for level in required_levels)
