"""
Mdict dictionary manager for enhanced word lookups.

This module provides integration with Mdict (.mdx) dictionaries for
professional English definitions and examples.
"""

import time
from pathlib import Path
from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class MdictDictionary:
    """
    Manager for Mdict (.mdx) dictionary files.

    Features:
    - Auto-discovery of .mdx files in data/dictionaries/
    - Lazy loading with error handling
    - Priority-based lookup
    - Graceful degradation when dictionaries unavailable

    Attributes:
        dictionaries_dir: Directory containing .mdx files
        dictionaries: List of discovered dictionaries
        loaded_dicts: Cache of loaded dictionary instances
    """

    def __init__(self, dictionaries_dir: Path | str = "data/dictionaries"):
        """
        Initialize Mdict dictionary manager.

        Args:
            dictionaries_dir: Directory containing .mdx files
        """
        self.dictionaries_dir = Path(dictionaries_dir)
        self.dictionaries: List[Dict[str, Any]] = []
        self.loaded_dicts: Dict[str, Any] = {}
        self._readmdict = None

        # Discover dictionaries
        self.discover_dictionaries()

    def discover_dictionaries(self) -> List[Dict[str, Any]]:
        """
        Auto-discover .mdx files in dictionaries directory.

        Returns:
            List of dictionary info dicts
        """
        self.dictionaries = []

        if not self.dictionaries_dir.exists():
            logger.warning(
                f"Dictionaries directory not found: {self.dictionaries_dir}"
            )
            return self.dictionaries

        # Find all .mdx files
        mdx_files = list(self.dictionaries_dir.glob("*.mdx"))

        # Priority mapping (you can customize this)
        priority_map = {
            "oald": 1,      # Oxford Advanced Learner's Dictionary
            "ldoce": 2,     # Longman Dictionary
            "collins": 3,   # Collins COBUILD
        }

        for mdx_file in mdx_files:
            # Derive name from filename
            name = mdx_file.stem

            # Determine priority
            priority = 5  # Default
            for key, prio in priority_map.items():
                if key.lower() in name.lower():
                    priority = prio
                    break

            # Create dictionary info
            dict_info = {
                "dictionary_name": name,
                "file_path": mdx_file,
                "priority": priority,
                "is_available": False,  # Will check on first load
                "last_checked": int(time.time()),
                "index_path": None,
                "entry_count": None,
                "load_error": None
            }

            self.dictionaries.append(dict_info)

        # Sort by priority (lower number = higher priority)
        self.dictionaries.sort(key=lambda d: d["priority"])

        logger.info(f"Discovered {len(self.dictionaries)} dictionaries")

        return self.dictionaries

    def _load_readmdict(self) -> bool:
        """
        Load readmdict library.

        Returns:
            True if loaded successfully
        """
        if self._readmdict is not None:
            return True

        try:
            import readmdict
            self._readmdict = readmdict
            return True
        except ImportError:
            logger.error("readmdict not installed. Install with: pip install readmdict")
            return False

    def _load_dictionary(self, dict_info: Dict[str, Any]) -> Optional[Any]:
        """
        Load a specific dictionary.

        Args:
            dict_info: Dictionary information dict

        Returns:
            MDX instance or None if failed
        """
        file_path = dict_info["file_path"]

        # Check if already loaded
        if str(file_path) in self.loaded_dicts:
            return self.loaded_dicts[str(file_path)]

        # Load readmdict
        if not self._load_readmdict():
            dict_info["load_error"] = "readmdict not installed"
            dict_info["is_available"] = False
            return None

        # Try to load dictionary
        try:
            from readmdict import MDX
            mdx = MDX(str(file_path))

            # Update dict info
            dict_info["is_available"] = True
            dict_info["load_error"] = None
            dict_info["last_checked"] = int(time.time())

            # Cache loaded dictionary
            self.loaded_dicts[str(file_path)] = mdx

            logger.info(f"Loaded dictionary: {dict_info['dictionary_name']}")

            return mdx

        except Exception as e:
            error_msg = f"Failed to load dictionary: {str(e)}"
            dict_info["load_error"] = error_msg[:500]  # Limit to 500 chars
            dict_info["is_available"] = False
            logger.error(f"Error loading {dict_info['dictionary_name']}: {e}")
            return None

    def query_word(self, word: str) -> Optional[Dict[str, Any]]:
        """
        Query word across all dictionaries (priority order).

        Args:
            word: Word to look up (case-insensitive)

        Returns:
            Dictionary result or None if not found:
            {
                "word": str,
                "definition": str,
                "dictionary": str,
                "priority": int
            }
        """
        if not word or not word.strip():
            return None

        word = word.strip().lower()

        # Try each dictionary in priority order
        for dict_info in self.dictionaries:
            mdx = self._load_dictionary(dict_info)

            if mdx is None:
                continue  # Skip unavailable dictionaries

            try:
                # Query dictionary
                result = mdx.lookup(word)

                if result:
                    # Result can be list or single item
                    if isinstance(result, list) and len(result) > 0:
                        definition = result[0]
                    else:
                        definition = str(result)

                    return {
                        "word": word,
                        "definition": definition,
                        "dictionary": dict_info["dictionary_name"],
                        "priority": dict_info["priority"]
                    }

            except Exception as e:
                logger.error(
                    f"Error querying {dict_info['dictionary_name']}: {e}"
                )
                continue

        # Not found in any dictionary
        return None

    def get_available_dictionaries(self) -> List[Dict[str, Any]]:
        """
        Get list of available dictionaries.

        Returns:
            List of dictionary info dicts (only available ones)
        """
        available = []

        for dict_info in self.dictionaries:
            # Try to load if not checked yet
            if not dict_info["is_available"]:
                self._load_dictionary(dict_info)

            if dict_info["is_available"]:
                available.append(dict_info)

        return available

    def is_available(self) -> bool:
        """
        Check if any dictionaries are available.

        Returns:
            True if at least one dictionary is available
        """
        return len(self.get_available_dictionaries()) > 0
