"""
Word dataclass for representing individual vocabulary items.
"""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Word:
    """
    Represents a single vocabulary word with its metadata.

    Attributes:
        word: The lemmatized form of the word (lowercase)
        level: CEFR level (A1, A2, B1, B2, C1, C2, C2+)
        word_type: Part of speech (noun, verb, adj, adv, etc.)
        definition_cn: Chinese translation/definition
        frequency: Number of occurrences in the source text
        examples: List of example sentences containing this word
        phonetic: IPA phonetic transcription (optional)
        original_forms: Set of original word forms found in text
    """

    word: str
    level: str
    word_type: str
    definition_cn: str = ""
    frequency: int = 0
    examples: List[str] = field(default_factory=list)
    phonetic: Optional[str] = None
    original_forms: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate word data after initialization."""
        if not self.word:
            raise ValueError("Word cannot be empty")

        valid_levels = {"A1", "A2", "B1", "B2", "C1", "C2", "C2+"}
        if self.level not in valid_levels:
            raise ValueError(f"Invalid CEFR level: {self.level}. Must be one of {valid_levels}")

        if self.frequency < 0:
            raise ValueError("Frequency cannot be negative")

    def add_example(self, sentence: str, max_examples: int = 3) -> None:
        """
        Add an example sentence if not already present and limit not reached.

        Args:
            sentence: The example sentence to add
            max_examples: Maximum number of examples to keep (default: 3)
        """
        if sentence and sentence not in self.examples and len(self.examples) < max_examples:
            self.examples.append(sentence)

    def add_original_form(self, form: str) -> None:
        """
        Add an original word form if not already present.

        Args:
            form: The original word form found in text
        """
        if form and form not in self.original_forms:
            self.original_forms.append(form)

    def increment_frequency(self, count: int = 1) -> None:
        """
        Increment the word frequency count.

        Args:
            count: Number to increment by (default: 1)
        """
        if count < 0:
            raise ValueError("Cannot increment frequency by negative value")
        self.frequency += count

    def to_dict(self) -> dict:
        """
        Convert Word to dictionary representation.

        Returns:
            Dictionary with all word attributes
        """
        return {
            "word": self.word,
            "level": self.level,
            "word_type": self.word_type,
            "definition_cn": self.definition_cn,
            "frequency": self.frequency,
            "examples": self.examples,
            "phonetic": self.phonetic,
            "original_forms": self.original_forms,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Word":
        """
        Create Word instance from dictionary.

        Args:
            data: Dictionary containing word attributes

        Returns:
            Word instance
        """
        return cls(
            word=data["word"],
            level=data["level"],
            word_type=data["word_type"],
            definition_cn=data.get("definition_cn", ""),
            frequency=data.get("frequency", 0),
            examples=data.get("examples", []),
            phonetic=data.get("phonetic"),
            original_forms=data.get("original_forms", []),
        )

    def __str__(self) -> str:
        """String representation of Word."""
        return f"{self.word} ({self.level}, {self.word_type}) - freq: {self.frequency}"

    def __repr__(self) -> str:
        """Detailed representation of Word."""
        return (
            f"Word(word='{self.word}', level='{self.level}', "
            f"word_type='{self.word_type}', frequency={self.frequency})"
        )
