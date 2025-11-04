"""
Level matcher for assigning CEFR levels to words and phrases.
"""
import csv
import json
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd


class LevelMatcher:
    """
    Matcher for assigning CEFR levels to vocabulary words.

    Uses ECDICT data with Oxford 3000 markers and frequency information
    to assign appropriate CEFR levels.
    """

    def __init__(
        self,
        vocabulary_file: Optional[str] = None,
        phrases_file: Optional[str] = None,
        use_cache: bool = True,
    ):
        """
        Initialize LevelMatcher.

        Args:
            vocabulary_file: Path to ECDICT CSV file (optional)
            phrases_file: Path to phrasal verbs JSON file (optional)
            use_cache: Whether to use lru_cache for lookups (default: True)
        """
        self.vocabulary_file = vocabulary_file
        self.phrases_file = phrases_file
        self.use_cache = use_cache
        self._vocabulary_df: Optional[pd.DataFrame] = None
        self._word_index: Dict[str, dict] = {}
        self._phrase_index: Dict[str, dict] = {}

        # Level assignment rules (based on frequency and oxford marker)
        self.level_rules = {
            "A1": {"oxford": 1, "frq_max": 50000, "collins": 5},
            "A2": {"oxford": 1, "frq_max": 30000, "collins": 4},
            "B1": {"oxford": 1, "frq_max": 15000, "collins": 3},
            "B2": {"frq_max": 8000, "collins": 2},
            "C1": {"frq_max": 3000, "collins": 1},
            "C2": {"frq_max": 1000},
        }

        # Phrasal verb level assignment (default levels)
        self.phrase_default_levels = {
            "common": "B1",  # Common phrasal verbs
            "intermediate": "B2",  # Less common
            "advanced": "C1",  # Rare or complex
        }

        if vocabulary_file:
            self.load_vocabulary(vocabulary_file)

        if phrases_file:
            self.load_phrasal_verbs(phrases_file)

    def load_vocabulary(self, file_path: str) -> None:
        """
        Load vocabulary data from ECDICT CSV file.

        Args:
            file_path: Path to ECDICT CSV file

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is invalid
        """
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"Vocabulary file not found: {file_path}")

        try:
            # Load CSV with pandas for efficient processing
            # Only load necessary columns to save memory
            columns_to_load = [
                "word",
                "translation",
                "pos",
                "collins",
                "oxford",
                "tag",
                "frq",
                "phonetic",
            ]

            self._vocabulary_df = pd.read_csv(
                file_path, usecols=lambda x: x in columns_to_load, low_memory=False
            )

            # Create word index for fast lookup
            self._build_word_index()

        except Exception as e:
            raise ValueError(f"Failed to load vocabulary file {file_path}: {e}")

    def _build_word_index(self) -> None:
        """Build index for fast word lookup."""
        if self._vocabulary_df is None:
            return

        self._word_index = {}

        for _, row in self._vocabulary_df.iterrows():
            word = str(row.get("word", "")).strip().lower()
            if not word:
                continue

            self._word_index[word] = {
                "translation": str(row.get("translation", "")),
                "pos": str(row.get("pos", "")),
                "collins": int(row.get("collins", 0)) if pd.notna(row.get("collins")) else 0,
                "oxford": int(row.get("oxford", 0)) if pd.notna(row.get("oxford")) else 0,
                "frq": int(row.get("frq", 0)) if pd.notna(row.get("frq")) else 0,
                "phonetic": str(row.get("phonetic", "")),
                "tag": str(row.get("tag", "")),
            }

    @lru_cache(maxsize=10000)
    def get_word_level(self, word: str, default: str = "C2+") -> str:
        """
        Get CEFR level for a word.

        Uses cached lookup for performance.

        Args:
            word: Word to look up (will be lowercased)
            default: Default level if word not found (default: "C2+")

        Returns:
            CEFR level (A1, A2, B1, B2, C1, C2, C2+)
        """
        word_lower = word.lower().strip()

        if not word_lower or word_lower not in self._word_index:
            return default

        word_data = self._word_index[word_lower]

        # Assign level based on rules
        level = self._assign_level(word_data)

        return level if level else default

    def _assign_level(self, word_data: dict) -> Optional[str]:
        """
        Assign CEFR level based on word data.

        Uses frequency, Oxford 3000 marker, and Collins rating.

        Args:
            word_data: Dictionary with word metadata

        Returns:
            CEFR level or None if cannot determine
        """
        collins = word_data.get("collins", 0)
        oxford = word_data.get("oxford", 0)
        frq = word_data.get("frq", 0)

        # High-frequency Oxford 3000 words -> A1/A2
        if oxford == 1:
            if collins >= 5 or frq >= 50000:
                return "A1"
            elif collins >= 4 or frq >= 30000:
                return "A2"
            elif frq >= 15000:
                return "B1"

        # Assign based on frequency and Collins rating
        if frq >= 15000 or collins >= 3:
            return "B1"
        elif frq >= 8000 or collins >= 2:
            return "B2"
        elif frq >= 3000 or collins >= 1:
            return "C1"
        elif frq >= 1000:
            return "C2"

        # Low frequency or no data
        return None

    def get_word_info(self, word: str) -> Optional[dict]:
        """
        Get complete information about a word.

        Args:
            word: Word to look up

        Returns:
            Dictionary with word info, or None if not found
        """
        word_lower = word.lower().strip()

        if word_lower not in self._word_index:
            return None

        word_data = self._word_index[word_lower].copy()
        word_data["level"] = self.get_word_level(word_lower)
        word_data["word"] = word_lower

        return word_data

    def get_translation(self, word: str) -> str:
        """
        Get Chinese translation for a word.

        Args:
            word: Word to translate

        Returns:
            Chinese translation or empty string if not found
        """
        word_info = self.get_word_info(word)
        if word_info:
            return word_info.get("translation", "")
        return ""

    def get_pos(self, word: str) -> str:
        """
        Get part of speech for a word.

        Args:
            word: Word to analyze

        Returns:
            POS tag or empty string if not found
        """
        word_info = self.get_word_info(word)
        if word_info:
            return word_info.get("pos", "")
        return ""

    def load_phrasal_verbs(self, file_path: str) -> None:
        """
        Load phrasal verbs from JSON file.

        Args:
            file_path: Path to phrasal verbs JSON file

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is invalid
        """
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"Phrasal verbs file not found: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                phrases_data = json.load(f)

            self._phrase_index = {}

            for phrase_obj in phrases_data:
                verb = phrase_obj.get("verb", "").strip()
                if not verb:
                    continue

                # Parse notation: "blow * up +" means separable
                separable = False
                clean_verb = verb

                if "*" in verb:
                    separable = True
                    clean_verb = verb.replace("*", "").replace("+", "").strip()
                    # Normalize spacing
                    clean_verb = " ".join(clean_verb.split())

                # Store both original and clean versions
                key = clean_verb.lower()

                self._phrase_index[key] = {
                    "phrase": clean_verb,
                    "original_notation": verb,
                    "separable": separable,
                    "definition": phrase_obj.get("definition", ""),
                    "examples": phrase_obj.get("examples", []),
                    "level": self._assign_phrase_level(clean_verb),
                }

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in phrasal verbs file: {e}")
        except Exception as e:
            raise ValueError(f"Failed to load phrasal verbs from {file_path}: {e}")

    def _assign_phrase_level(self, phrase: str) -> str:
        """
        Assign CEFR level to a phrasal verb.

        Args:
            phrase: Phrasal verb string

        Returns:
            CEFR level (B1, B2, or C1)
        """
        # Common phrasal verbs (very frequent in usage)
        common_phrases = {
            "get up",
            "wake up",
            "sit down",
            "stand up",
            "come in",
            "go out",
            "turn on",
            "turn off",
            "put on",
            "take off",
            "look at",
            "look for",
            "find out",
            "give up",
            "take care of",
        }

        phrase_lower = phrase.lower().strip()

        if phrase_lower in common_phrases:
            return "B1"

        # Check if base verb is high frequency -> intermediate
        parts = phrase_lower.split()
        if len(parts) > 0:
            base_verb = parts[0]
            word_info = self.get_word_info(base_verb)

            if word_info:
                verb_level = word_info.get("level", "C1")
                # If base verb is A1-B1, phrase is likely B2
                if verb_level in ["A1", "A2", "B1"]:
                    return "B2"

        # Default to C1 for less common phrasal verbs
        return "C1"

    @lru_cache(maxsize=1000)
    def match_phrase(self, phrase: str) -> Optional[dict]:
        """
        Match a phrasal verb and get its information.

        Args:
            phrase: Phrasal verb to match (e.g., "give up", "look for")

        Returns:
            Dictionary with phrase info, or None if not found
        """
        phrase_lower = phrase.lower().strip()

        if phrase_lower not in self._phrase_index:
            return None

        return self._phrase_index[phrase_lower].copy()

    def get_phrase_level(self, phrase: str, default: str = "B2") -> str:
        """
        Get CEFR level for a phrasal verb.

        Args:
            phrase: Phrasal verb to look up
            default: Default level if phrase not found

        Returns:
            CEFR level
        """
        phrase_info = self.match_phrase(phrase)
        if phrase_info:
            return phrase_info.get("level", default)
        return default

    def is_loaded(self) -> bool:
        """
        Check if vocabulary is loaded.

        Returns:
            True if vocabulary is loaded
        """
        return self._word_index is not None and len(self._word_index) > 0

    def is_phrases_loaded(self) -> bool:
        """
        Check if phrasal verbs are loaded.

        Returns:
            True if phrasal verbs are loaded
        """
        return self._phrase_index is not None and len(self._phrase_index) > 0

    def get_stats(self) -> dict:
        """
        Get statistics about loaded vocabulary.

        Returns:
            Dictionary with stats
        """
        return {
            "total_words": len(self._word_index),
            "total_phrases": len(self._phrase_index),
            "file_path": self.vocabulary_file,
            "phrases_file": self.phrases_file,
            "cache_enabled": self.use_cache,
        }

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"LevelMatcher(words={len(self._word_index)}, "
            f"phrases={len(self._phrase_index)}, "
            f"file='{self.vocabulary_file}')"
        )
