"""
Bilingual string loader for UI localization.

This module provides loading and formatting of bilingual English/Chinese UI strings
for simultaneous dual-language display.
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any
import logging

# Configure logging
logger = logging.getLogger(__name__)


class BilingualStringLoader:
    """
    Loader for bilingual UI strings.

    Loads English/Chinese string pairs from JSON for simultaneous dual-language
    display in the web interface.

    Attributes:
        strings_file: Path to ui_strings.json file
        strings: Dictionary of loaded string data
        version: Version of loaded strings
    """

    def __init__(self, strings_file: Optional[Path | str] = None):
        """
        Initialize bilingual string loader.

        Args:
            strings_file: Path to ui_strings.json (optional)
        """
        self.strings_file = Path(strings_file) if strings_file else Path("data/ui_strings.json")
        self.strings: Dict[str, Dict[str, Any]] = {}
        self.version: str = "unknown"
        self.last_updated: str = "unknown"
        self.categories: list = []

        # Auto-load on initialization
        self.load()

    def load(self, file_path: Optional[Path | str] = None) -> bool:
        """
        Load bilingual strings from JSON file.

        Args:
            file_path: Optional path override

        Returns:
            True if successful, False otherwise
        """
        target_file = Path(file_path) if file_path else self.strings_file

        if not target_file.exists():
            logger.warning(f"UI strings file not found: {target_file}")
            return False

        try:
            with open(target_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Validate structure
            if "strings" not in data:
                logger.error(f"Invalid UI strings file: missing 'strings' key")
                return False

            # Load metadata
            self.version = data.get("version", "unknown")
            self.last_updated = data.get("last_updated", "unknown")
            self.categories = data.get("categories", [])

            # Load strings
            self.strings = data["strings"]

            logger.info(
                f"Loaded {len(self.strings)} bilingual strings from {target_file} "
                f"(version {self.version})"
            )

            return True

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse UI strings JSON: {e}")
            return False
        except Exception as e:
            logger.error(f"Failed to load UI strings from {target_file}: {e}")
            return False

    def get_bilingual(self, key: str) -> Optional[Dict[str, str]]:
        """
        Get bilingual string by key.

        Args:
            key: String identifier (e.g., "navigation.home")

        Returns:
            Dict with text_en and text_cn, or None if not found
        """
        if key not in self.strings:
            logger.warning(f"String key not found: {key}")
            return None

        string_data = self.strings[key]

        return {
            "text_en": string_data.get("text_en", ""),
            "text_cn": string_data.get("text_cn", "")
        }

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Get complete string data by key.

        Args:
            key: String identifier

        Returns:
            Complete string dict with all fields, or None if not found
        """
        return self.strings.get(key)

    def get_all_strings(self, category: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
        """
        Get all strings or filter by category.

        Args:
            category: Optional category filter (e.g., "navigation", "errors")

        Returns:
            Dict mapping key to string data
        """
        if category is None:
            return self.strings.copy()

        # Filter by category
        filtered = {
            key: value
            for key, value in self.strings.items()
            if value.get("category") == category
        }

        return filtered

    def format_bilingual(self, key: str, separator: str = " / ") -> str:
        """
        Format bilingual string for display.

        Args:
            key: String identifier
            separator: Separator between English and Chinese

        Returns:
            Formatted string: "English / 中文"

        Example:
            format_bilingual("navigation.home") → "Home / 首页"
        """
        bilingual = self.get_bilingual(key)

        if not bilingual:
            return f"[Missing: {key}]"

        text_en = bilingual["text_en"]
        text_cn = bilingual["text_cn"]

        return f"{text_en}{separator}{text_cn}"

    def get_by_category(self, category: str) -> Dict[str, Dict[str, Any]]:
        """
        Get all strings for a specific category.

        Args:
            category: Category name (e.g., "navigation", "buttons")

        Returns:
            Dict of strings in the category
        """
        return self.get_all_strings(category=category)

    def has_key(self, key: str) -> bool:
        """
        Check if string key exists.

        Args:
            key: String identifier

        Returns:
            True if key exists
        """
        return key in self.strings

    def get_english(self, key: str, default: str = "") -> str:
        """
        Get English text only.

        Args:
            key: String identifier
            default: Default value if key not found

        Returns:
            English text or default
        """
        string_data = self.strings.get(key)

        if not string_data:
            return default

        return string_data.get("text_en", default)

    def get_chinese(self, key: str, default: str = "") -> str:
        """
        Get Chinese text only.

        Args:
            key: String identifier
            default: Default value if key not found

        Returns:
            Chinese text or default
        """
        string_data = self.strings.get(key)

        if not string_data:
            return default

        return string_data.get("text_cn", default)

    def get_categories(self) -> list:
        """
        Get list of available categories.

        Returns:
            List of category names
        """
        return self.categories.copy()

    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about loaded strings.

        Returns:
            Dict with statistics
        """
        # Count strings by category
        by_category = {}
        for string_data in self.strings.values():
            category = string_data.get("category", "uncategorized")
            by_category[category] = by_category.get(category, 0) + 1

        return {
            "total_strings": len(self.strings),
            "version": self.version,
            "last_updated": self.last_updated,
            "categories": self.categories,
            "strings_by_category": by_category
        }

    def reload(self) -> bool:
        """
        Reload strings from file.

        Returns:
            True if successful
        """
        return self.load()

    def __repr__(self) -> str:
        """String representation."""
        return f"BilingualStringLoader(file={self.strings_file}, strings={len(self.strings)})"


# Global singleton instance
_loader_instance: Optional[BilingualStringLoader] = None


def get_loader(strings_file: Optional[Path | str] = None) -> BilingualStringLoader:
    """
    Get global bilingual string loader instance (singleton).

    Args:
        strings_file: Path to ui_strings.json (only used on first call)

    Returns:
        BilingualStringLoader instance
    """
    global _loader_instance

    if _loader_instance is None:
        _loader_instance = BilingualStringLoader(strings_file)

    return _loader_instance


def reload_strings(strings_file: Optional[Path | str] = None) -> BilingualStringLoader:
    """
    Reload bilingual strings (useful for testing or updates).

    Args:
        strings_file: Path to ui_strings.json

    Returns:
        New BilingualStringLoader instance
    """
    global _loader_instance
    _loader_instance = BilingualStringLoader(strings_file)
    return _loader_instance
