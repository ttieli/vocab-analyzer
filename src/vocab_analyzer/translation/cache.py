"""
Translation cache for persistent storage of translations.

This module provides caching functionality to avoid redundant translation
operations. Translations are stored in a JSON file and expire after 30 days.
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List


class TranslationCache:
    """
    Persistent cache for translation results.

    Cache key format: {translation_type}:{lowercase_text}
    Example: "word:hello", "phrase:run out", "sentence:how are you"

    Attributes:
        cache_file: Path to the JSON cache file
        cache_expiry_days: Number of days before cache entries expire (default: 30)
        entries: In-memory cache dictionary
    """

    def __init__(
        self,
        cache_file: Path | str = "data/translation_cache.json",
        cache_expiry_days: int = 30
    ):
        """
        Initialize translation cache.

        Args:
            cache_file: Path to cache JSON file
            cache_expiry_days: Days before entries expire (default: 30)
        """
        self.cache_file = Path(cache_file)
        self.cache_expiry_days = cache_expiry_days
        self.entries: Dict[str, Dict[str, Any]] = {}

        # Load existing cache if available
        self.load()

    def _make_key(self, text: str, translation_type: str) -> str:
        """
        Generate cache key from text and type.

        Args:
            text: Source text to translate
            translation_type: Type (word/phrase/sentence)

        Returns:
            Cache key string
        """
        return f"{translation_type}:{text.lower().strip()}"

    def get(
        self,
        text: str,
        translation_type: str = "word"
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve translation from cache.

        Args:
            text: Source text
            translation_type: Type of translation

        Returns:
            Cached entry dict or None if not found/expired
        """
        key = self._make_key(text, translation_type)
        entry = self.entries.get(key)

        if not entry:
            return None

        # Check if expired
        if self._is_expired(entry):
            del self.entries[key]
            return None

        # Increment access count
        entry["access_count"] = entry.get("access_count", 1) + 1

        return entry

    def set(
        self,
        text: str,
        translation: str,
        translation_type: str = "word",
        source: str = "argos",
        confidence_score: float = 0.7
    ) -> None:
        """
        Store translation in cache.

        Args:
            text: Source English text
            translation: Target Chinese text
            translation_type: Type (word/phrase/sentence)
            source: Translation source (ecdict/mdict/argos)
            confidence_score: Quality estimate (0.0-1.0)

        Raises:
            ValueError: If validation fails
        """
        # Validate inputs
        if not text or len(text) > 500:
            raise ValueError("Source text must be 1-500 characters")

        if not translation or len(translation) > 2000:
            raise ValueError("Translation must be 1-2000 characters")

        if translation_type not in ["word", "phrase", "sentence"]:
            raise ValueError(
                f"Invalid translation_type: {translation_type}. "
                "Must be word/phrase/sentence"
            )

        if source not in ["ecdict", "mdict", "argos", "cached"]:
            raise ValueError(
                f"Invalid source: {source}. "
                "Must be ecdict/mdict/argos/cached"
            )

        if not (0.0 <= confidence_score <= 1.0):
            raise ValueError("Confidence score must be between 0.0 and 1.0")

        # Create entry
        key = self._make_key(text, translation_type)
        self.entries[key] = {
            "source_text": text,
            "target_text": translation,
            "timestamp": int(time.time()),
            "translation_type": translation_type,
            "source": source,
            "confidence_score": confidence_score,
            "access_count": 1
        }

    def exists(self, text: str, translation_type: str = "word") -> bool:
        """
        Check if translation exists in cache (and not expired).

        Args:
            text: Source text
            translation_type: Type of translation

        Returns:
            True if entry exists and not expired
        """
        return self.get(text, translation_type) is not None

    def clear_old(self) -> int:
        """
        Remove expired entries from cache.

        Returns:
            Number of entries removed
        """
        keys_to_remove = [
            key for key, entry in self.entries.items()
            if self._is_expired(entry)
        ]

        for key in keys_to_remove:
            del self.entries[key]

        return len(keys_to_remove)

    def _is_expired(self, entry: Dict[str, Any]) -> bool:
        """
        Check if cache entry has expired.

        Args:
            entry: Cache entry dictionary

        Returns:
            True if expired
        """
        timestamp = entry.get("timestamp", 0)
        entry_date = datetime.fromtimestamp(timestamp)
        expiry_date = entry_date + timedelta(days=self.cache_expiry_days)

        return datetime.now() > expiry_date

    def save(self) -> None:
        """
        Save cache to JSON file.

        Writes cache entries to disk with metadata.
        """
        # Ensure directory exists
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)

        # Prepare data structure
        data = {
            "version": "1.0.0",
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "total_entries": len(self.entries),
                "cache_expiry_days": self.cache_expiry_days
            },
            "entries": self.entries
        }

        # Write to file
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self) -> None:
        """
        Load cache from JSON file.

        If file doesn't exist or is invalid, starts with empty cache.
        """
        if not self.cache_file.exists():
            self.entries = {}
            return

        try:
            with open(self.cache_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.entries = data.get("entries", {})

            # Update metadata if present
            metadata = data.get("metadata", {})
            if "cache_expiry_days" in metadata:
                self.cache_expiry_days = metadata["cache_expiry_days"]

        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load cache file: {e}")
            self.entries = {}

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache stats
        """
        total = len(self.entries)
        by_type = {}
        by_source = {}
        total_accesses = 0

        for entry in self.entries.values():
            # Count by type
            t = entry.get("translation_type", "unknown")
            by_type[t] = by_type.get(t, 0) + 1

            # Count by source
            s = entry.get("source", "unknown")
            by_source[s] = by_source.get(s, 0) + 1

            # Sum accesses
            total_accesses += entry.get("access_count", 0)

        return {
            "total_entries": total,
            "by_type": by_type,
            "by_source": by_source,
            "total_accesses": total_accesses,
            "avg_accesses_per_entry": (
                total_accesses / total if total > 0 else 0
            )
        }
