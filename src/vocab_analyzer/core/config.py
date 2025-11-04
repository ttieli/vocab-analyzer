"""
Configuration management for vocab-analyzer.
"""
import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


class Config:
    """
    Configuration manager for vocab-analyzer.

    Loads configuration from YAML files and provides convenient access to settings.
    """

    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration.

        Args:
            config_file: Path to custom config file. If None, uses default config.
        """
        self._config: Dict[str, Any] = {}
        self._config_file = config_file
        self.load_config()

    def load_config(self) -> None:
        """Load configuration from YAML file."""
        if self._config_file:
            config_path = Path(self._config_file)
        else:
            # Use default config
            config_path = self._get_default_config_path()

        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with open(config_path, "r", encoding="utf-8") as f:
            self._config = yaml.safe_load(f) or {}

    def _get_default_config_path(self) -> Path:
        """
        Get path to default configuration file.

        Returns:
            Path to default config file
        """
        # Try to find config relative to package root
        current_file = Path(__file__)
        package_root = current_file.parent.parent.parent.parent
        config_path = package_root / "config" / "default_config.yaml"

        if config_path.exists():
            return config_path

        # Fallback: try current working directory
        cwd_config = Path.cwd() / "config" / "default_config.yaml"
        if cwd_config.exists():
            return cwd_config

        raise FileNotFoundError("Could not locate default_config.yaml")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by dot-notation key.

        Examples:
            config.get("data.vocabularies_dir")
            config.get("nlp.batch_size", 100)

        Args:
            key: Configuration key in dot notation
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        keys = key.split(".")
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value by dot-notation key.

        Args:
            key: Configuration key in dot notation
            value: Value to set
        """
        keys = key.split(".")
        config = self._config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

    def get_data_path(self, data_type: str) -> Path:
        """
        Get path to data file or directory.

        Args:
            data_type: Type of data (vocabularies_dir, cefr_wordlist, etc.)

        Returns:
            Path object to the data location
        """
        path_str = self.get(f"data.{data_type}")
        if not path_str:
            raise ValueError(f"Data path not configured for: {data_type}")

        path = Path(path_str)

        # Make path absolute if relative
        if not path.is_absolute():
            # Resolve relative to project root
            package_root = Path(__file__).parent.parent.parent.parent
            path = package_root / path

        return path

    @property
    def nlp_model(self) -> str:
        """Get NLP model name."""
        return self.get("nlp.model", "en_core_web_sm")

    @property
    def nlp_batch_size(self) -> int:
        """Get NLP processing batch size."""
        return self.get("nlp.batch_size", 100)

    @property
    def min_word_length(self) -> int:
        """Get minimum word length for analysis."""
        return self.get("analysis.min_word_length", 2)

    @property
    def max_word_length(self) -> int:
        """Get maximum word length for analysis."""
        return self.get("analysis.max_word_length", 45)

    @property
    def exclude_numbers(self) -> bool:
        """Whether to exclude numbers from analysis."""
        return self.get("analysis.exclude_numbers", True)

    @property
    def exclude_punctuation(self) -> bool:
        """Whether to exclude punctuation from analysis."""
        return self.get("analysis.exclude_punctuation", True)

    @property
    def enable_phrases(self) -> bool:
        """Whether phrase detection is enabled."""
        return self.get("analysis.enable_phrases", True)

    @property
    def max_phrase_length(self) -> int:
        """Get maximum number of words in a phrase."""
        return self.get("analysis.max_phrase_length", 4)

    @property
    def default_level_unknown(self) -> str:
        """Get default CEFR level for unknown words."""
        return self.get("analysis.default_level_unknown", "C2+")

    @property
    def output_formats(self) -> list:
        """Get supported output formats."""
        return self.get("output.formats", ["json", "csv", "markdown"])

    @property
    def default_output_format(self) -> str:
        """Get default output format."""
        return self.get("output.default_format", "json")

    @property
    def include_examples(self) -> bool:
        """Whether to include example sentences in output."""
        return self.get("output.include_examples", True)

    @property
    def max_examples_per_word(self) -> int:
        """Get maximum number of examples per word."""
        return self.get("output.max_examples_per_word", 3)

    @property
    def cache_vocabulary(self) -> bool:
        """Whether to cache vocabulary lookups."""
        return self.get("performance.cache_vocabulary", True)

    @property
    def cache_phrases(self) -> bool:
        """Whether to cache phrase lookups."""
        return self.get("performance.cache_phrases", True)

    @property
    def log_level(self) -> str:
        """Get logging level."""
        return self.get("logging.level", "INFO")

    def to_dict(self) -> Dict[str, Any]:
        """
        Get full configuration as dictionary.

        Returns:
            Complete configuration dictionary
        """
        return self._config.copy()

    def __repr__(self) -> str:
        """String representation of Config."""
        return f"Config(file='{self._config_file or 'default'}')"

    def __str__(self) -> str:
        """User-friendly string representation."""
        return f"Configuration loaded from: {self._config_file or 'default config'}"
