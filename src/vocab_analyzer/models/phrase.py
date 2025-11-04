"""
Phrase dataclass for representing phrasal verbs and multi-word expressions.
"""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Phrase:
    """
    Represents a phrasal verb or multi-word expression.

    Attributes:
        phrase: The phrasal verb (e.g., "look up", "give up")
        phrase_type: Type of phrase (phrasal_verb, idiom, collocation)
        level: CEFR level (A1, A2, B1, B2, C1, C2, C2+)
        separable: Whether the phrase is separable (e.g., "look it up" vs "look up it")
        definition: English definition or explanation
        definition_cn: Chinese translation/definition
        frequency: Number of occurrences in the source text
        examples: List of example sentences containing this phrase
    """

    phrase: str
    phrase_type: str = "phrasal_verb"
    level: str = "B1"
    separable: bool = False
    definition: str = ""
    definition_cn: str = ""
    frequency: int = 0
    examples: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate phrase data after initialization."""
        if not self.phrase:
            raise ValueError("Phrase cannot be empty")

        valid_levels = {"A1", "A2", "B1", "B2", "C1", "C2", "C2+"}
        if self.level not in valid_levels:
            raise ValueError(f"Invalid CEFR level: {self.level}. Must be one of {valid_levels}")

        valid_types = {"phrasal_verb", "idiom", "collocation", "compound"}
        if self.phrase_type not in valid_types:
            raise ValueError(
                f"Invalid phrase type: {self.phrase_type}. Must be one of {valid_types}"
            )

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

    def increment_frequency(self, count: int = 1) -> None:
        """
        Increment the phrase frequency count.

        Args:
            count: Number to increment by (default: 1)
        """
        if count < 0:
            raise ValueError("Cannot increment frequency by negative value")
        self.frequency += count

    @staticmethod
    def parse_phrasal_verb_notation(verb_notation: str) -> tuple[str, bool]:
        """
        Parse phrasal verb notation to extract phrase and separability.

        Notation examples:
            "look up +" -> ("look up", False) - has object but not separable
            "blow * up +" -> ("blow up", True) - separable with object
            "give up" -> ("give up", False) - no object

        Args:
            verb_notation: The verb notation string with markers

        Returns:
            Tuple of (cleaned_phrase, is_separable)
        """
        # Remove trailing markers
        cleaned = verb_notation.replace(" +", "").strip()

        # Check for separability marker
        is_separable = " * " in cleaned or cleaned.endswith(" *")

        # Remove separability marker
        cleaned = cleaned.replace(" * ", " ").replace(" *", "").strip()

        return cleaned, is_separable

    def to_dict(self) -> dict:
        """
        Convert Phrase to dictionary representation.

        Returns:
            Dictionary with all phrase attributes
        """
        return {
            "phrase": self.phrase,
            "phrase_type": self.phrase_type,
            "level": self.level,
            "separable": self.separable,
            "definition": self.definition,
            "definition_cn": self.definition_cn,
            "frequency": self.frequency,
            "examples": self.examples,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Phrase":
        """
        Create Phrase instance from dictionary.

        Args:
            data: Dictionary containing phrase attributes

        Returns:
            Phrase instance
        """
        return cls(
            phrase=data["phrase"],
            phrase_type=data.get("phrase_type", "phrasal_verb"),
            level=data.get("level", "B1"),
            separable=data.get("separable", False),
            definition=data.get("definition", ""),
            definition_cn=data.get("definition_cn", ""),
            frequency=data.get("frequency", 0),
            examples=data.get("examples", []),
        )

    def __str__(self) -> str:
        """String representation of Phrase."""
        sep_marker = " (separable)" if self.separable else ""
        return f"{self.phrase}{sep_marker} ({self.level}) - freq: {self.frequency}"

    def __repr__(self) -> str:
        """Detailed representation of Phrase."""
        return (
            f"Phrase(phrase='{self.phrase}', type='{self.phrase_type}', "
            f"level='{self.level}', separable={self.separable}, frequency={self.frequency})"
        )
