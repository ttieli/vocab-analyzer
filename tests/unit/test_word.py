"""
Unit tests for Word dataclass.
"""
import pytest

from vocab_analyzer.models import Word


class TestWord:
    """Test cases for Word dataclass."""

    def test_word_creation(self):
        """Test basic word creation."""
        word = Word(word="test", level="A1", word_type="noun")

        assert word.word == "test"
        assert word.level == "A1"
        assert word.word_type == "noun"
        assert word.frequency == 0
        assert word.examples == []

    def test_word_with_all_fields(self):
        """Test word creation with all fields."""
        word = Word(
            word="vocabulary",
            level="B1",
            word_type="noun",
            definition_cn="词汇",
            frequency=5,
            examples=["Example sentence."],
            phonetic="/vəˈkæbjʊləri/",
            original_forms=["vocabulary", "vocabularies"],
        )

        assert word.word == "vocabulary"
        assert word.level == "B1"
        assert word.word_type == "noun"
        assert word.definition_cn == "词汇"
        assert word.frequency == 5
        assert len(word.examples) == 1
        assert word.phonetic == "/vəˈkæbjʊləri/"
        assert len(word.original_forms) == 2

    def test_invalid_level_raises_error(self):
        """Test that invalid CEFR level raises ValueError."""
        with pytest.raises(ValueError, match="Invalid CEFR level"):
            Word(word="test", level="D1", word_type="noun")

    def test_empty_word_raises_error(self):
        """Test that empty word raises ValueError."""
        with pytest.raises(ValueError, match="Word cannot be empty"):
            Word(word="", level="A1", word_type="noun")

    def test_negative_frequency_raises_error(self):
        """Test that negative frequency raises ValueError."""
        with pytest.raises(ValueError, match="Frequency cannot be negative"):
            Word(word="test", level="A1", word_type="noun", frequency=-1)

    def test_add_example(self):
        """Test adding examples to word."""
        word = Word(word="test", level="A1", word_type="noun")

        word.add_example("This is a test.")
        assert len(word.examples) == 1
        assert "This is a test." in word.examples

        # Adding same example again should not duplicate
        word.add_example("This is a test.")
        assert len(word.examples) == 1

    def test_add_example_max_limit(self):
        """Test that examples are limited to max_examples."""
        word = Word(word="test", level="A1", word_type="noun")

        word.add_example("Example 1", max_examples=2)
        word.add_example("Example 2", max_examples=2)
        word.add_example("Example 3", max_examples=2)  # Should be ignored

        assert len(word.examples) == 2

    def test_increment_frequency(self):
        """Test incrementing word frequency."""
        word = Word(word="test", level="A1", word_type="noun")

        assert word.frequency == 0

        word.increment_frequency()
        assert word.frequency == 1

        word.increment_frequency(5)
        assert word.frequency == 6

    def test_increment_frequency_negative_raises_error(self):
        """Test that negative increment raises ValueError."""
        word = Word(word="test", level="A1", word_type="noun")

        with pytest.raises(ValueError, match="Cannot increment frequency by negative value"):
            word.increment_frequency(-1)

    def test_add_original_form(self):
        """Test adding original word forms."""
        word = Word(word="run", level="A1", word_type="verb")

        word.add_original_form("running")
        word.add_original_form("ran")
        assert len(word.original_forms) == 2

        # Adding duplicate should not duplicate
        word.add_original_form("running")
        assert len(word.original_forms) == 2

    def test_to_dict(self):
        """Test conversion to dictionary."""
        word = Word(
            word="test", level="A1", word_type="noun", definition_cn="测试", frequency=3
        )

        word_dict = word.to_dict()

        assert word_dict["word"] == "test"
        assert word_dict["level"] == "A1"
        assert word_dict["word_type"] == "noun"
        assert word_dict["definition_cn"] == "测试"
        assert word_dict["frequency"] == 3

    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {
            "word": "test",
            "level": "A1",
            "word_type": "noun",
            "definition_cn": "测试",
            "frequency": 3,
            "examples": ["Test example."],
            "phonetic": "/test/",
            "original_forms": ["test", "tests"],
        }

        word = Word.from_dict(data)

        assert word.word == "test"
        assert word.level == "A1"
        assert word.frequency == 3
        assert len(word.examples) == 1
        assert word.phonetic == "/test/"

    def test_str_representation(self):
        """Test string representation."""
        word = Word(word="test", level="A1", word_type="noun", frequency=5)

        str_repr = str(word)
        assert "test" in str_repr
        assert "A1" in str_repr
        assert "noun" in str_repr
        assert "5" in str_repr

    def test_repr(self):
        """Test repr representation."""
        word = Word(word="test", level="A1", word_type="noun", frequency=5)

        repr_str = repr(word)
        assert "Word(" in repr_str
        assert "test" in repr_str
