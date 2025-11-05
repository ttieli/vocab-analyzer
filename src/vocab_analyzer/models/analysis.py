"""
VocabularyAnalysis dataclass for representing complete analysis results.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

from .phrase import Phrase
from .word import Word


@dataclass
class VocabularyAnalysis:
    """
    Represents the complete vocabulary analysis results for a text.

    Attributes:
        source_file: Path to the analyzed file
        words: Dictionary mapping lemmatized words to Word objects
        phrases: Dictionary mapping phrases to Phrase objects
        statistics: Dictionary containing analysis statistics
        metadata: Additional metadata about the analysis
        analysis_date: Timestamp of when analysis was performed
        processed_text: Full text content (for reading view in web interface)
    """

    source_file: str
    words: Dict[str, Word] = field(default_factory=dict)
    phrases: Dict[str, Phrase] = field(default_factory=dict)
    statistics: Dict[str, any] = field(default_factory=dict)
    metadata: Dict[str, any] = field(default_factory=dict)
    analysis_date: Optional[datetime] = None
    processed_text: Optional[str] = None

    def __post_init__(self) -> None:
        """Initialize analysis date if not provided."""
        if self.analysis_date is None:
            self.analysis_date = datetime.now()

        # Initialize basic statistics if not present
        if not self.statistics:
            self.statistics = self._calculate_statistics()

    def add_word(self, word: Word) -> None:
        """
        Add or update a word in the analysis.

        If word already exists, merge the data (increment frequency, add examples).

        Args:
            word: Word object to add
        """
        if word.word in self.words:
            # Word exists, merge data
            existing = self.words[word.word]
            existing.increment_frequency(word.frequency)

            # Merge examples
            for example in word.examples:
                existing.add_example(example)

            # Merge original forms
            for form in word.original_forms:
                existing.add_original_form(form)
        else:
            # New word, add it
            self.words[word.word] = word

        # Recalculate statistics
        self.statistics = self._calculate_statistics()

    def add_phrase(self, phrase: Phrase) -> None:
        """
        Add or update a phrase in the analysis.

        If phrase already exists, merge the data (increment frequency, add examples).

        Args:
            phrase: Phrase object to add
        """
        if phrase.phrase in self.phrases:
            # Phrase exists, merge data
            existing = self.phrases[phrase.phrase]
            existing.increment_frequency(phrase.frequency)

            # Merge examples
            for example in phrase.examples:
                existing.add_example(example)
        else:
            # New phrase, add it
            self.phrases[phrase.phrase] = phrase

        # Recalculate statistics
        self.statistics = self._calculate_statistics()

    def get_words_by_level(self, level: str) -> List[Word]:
        """
        Get all words at a specific CEFR level.

        Args:
            level: CEFR level (A1, A2, B1, B2, C1, C2, C2+)

        Returns:
            List of Word objects at the specified level
        """
        return [word for word in self.words.values() if word.level == level]

    def get_phrases_by_level(self, level: str) -> List[Phrase]:
        """
        Get all phrases at a specific CEFR level.

        Args:
            level: CEFR level (A1, A2, B1, B2, C1, C2, C2+)

        Returns:
            List of Phrase objects at the specified level
        """
        return [phrase for phrase in self.phrases.values() if phrase.level == level]

    def get_words_by_type(self, word_type: str) -> List[Word]:
        """
        Get all words of a specific part of speech.

        Args:
            word_type: Part of speech (noun, verb, adj, adv, etc.)

        Returns:
            List of Word objects of the specified type
        """
        return [word for word in self.words.values() if word.word_type == word_type]

    def get_top_words(self, n: int = 20, level: Optional[str] = None) -> List[Word]:
        """
        Get the top N most frequent words, optionally filtered by level.

        Args:
            n: Number of top words to return
            level: Optional CEFR level filter

        Returns:
            List of Word objects sorted by frequency (descending)
        """
        words = self.words.values()
        if level:
            words = [w for w in words if w.level == level]

        return sorted(words, key=lambda w: w.frequency, reverse=True)[:n]

    def _calculate_statistics(self) -> Dict[str, any]:
        """
        Calculate comprehensive statistics about the vocabulary.

        Returns:
            Dictionary containing various statistics
        """
        stats = {
            "total_unique_words": len(self.words),
            "total_unique_phrases": len(self.phrases),
            "total_word_occurrences": sum(w.frequency for w in self.words.values()),
            "total_phrase_occurrences": sum(p.frequency for p in self.phrases.values()),
        }

        # Level distribution for words
        level_distribution = {}
        for level in ["A1", "A2", "B1", "B2", "C1", "C2", "C2+"]:
            words_at_level = self.get_words_by_level(level)
            level_distribution[level] = {
                "count": len(words_at_level),
                "percentage": (
                    len(words_at_level) / len(self.words) * 100 if self.words else 0
                ),
            }
        stats["level_distribution"] = level_distribution

        # Word type distribution
        word_type_distribution = {}
        for word in self.words.values():
            word_type = word.word_type
            if word_type not in word_type_distribution:
                word_type_distribution[word_type] = 0
            word_type_distribution[word_type] += 1
        stats["word_type_distribution"] = word_type_distribution

        # Phrase type distribution
        phrase_type_distribution = {}
        for phrase in self.phrases.values():
            phrase_type = phrase.phrase_type
            if phrase_type not in phrase_type_distribution:
                phrase_type_distribution[phrase_type] = 0
            phrase_type_distribution[phrase_type] += 1
        stats["phrase_type_distribution"] = phrase_type_distribution

        return stats

    def to_dict(self, include_words: bool = True, include_phrases: bool = True) -> dict:
        """
        Convert VocabularyAnalysis to dictionary representation.

        Args:
            include_words: Whether to include full word details
            include_phrases: Whether to include full phrase details

        Returns:
            Dictionary with analysis results
        """
        result = {
            "source_file": self.source_file,
            "analysis_date": self.analysis_date.isoformat() if self.analysis_date else None,
            "statistics": self.statistics,
            "metadata": self.metadata,
            "processed_text": self.processed_text,
        }

        if include_words:
            result["words"] = [word.to_dict() for word in self.words.values()]

        if include_phrases:
            result["phrases"] = [phrase.to_dict() for phrase in self.phrases.values()]

        return result

    @classmethod
    def from_dict(cls, data: dict) -> "VocabularyAnalysis":
        """
        Create VocabularyAnalysis instance from dictionary.

        Args:
            data: Dictionary containing analysis data

        Returns:
            VocabularyAnalysis instance
        """
        analysis = cls(
            source_file=data["source_file"],
            statistics=data.get("statistics", {}),
            metadata=data.get("metadata", {}),
        )

        # Parse analysis date
        if "analysis_date" in data and data["analysis_date"]:
            analysis.analysis_date = datetime.fromisoformat(data["analysis_date"])

        # Reconstruct words
        if "words" in data:
            analysis.words = {
                word_data["word"]: Word.from_dict(word_data) for word_data in data["words"]
            }

        # Reconstruct phrases
        if "phrases" in data:
            analysis.phrases = {
                phrase_data["phrase"]: Phrase.from_dict(phrase_data)
                for phrase_data in data["phrases"]
            }

        return analysis

    def __str__(self) -> str:
        """String representation of VocabularyAnalysis."""
        return (
            f"Analysis of '{self.source_file}': "
            f"{len(self.words)} unique words, {len(self.phrases)} phrases"
        )

    def __repr__(self) -> str:
        """Detailed representation of VocabularyAnalysis."""
        return (
            f"VocabularyAnalysis(source='{self.source_file}', "
            f"words={len(self.words)}, phrases={len(self.phrases)})"
        )
