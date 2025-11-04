"""
Pytest configuration and fixtures for vocab-analyzer tests.
"""
import json
from pathlib import Path

import pytest


@pytest.fixture
def fixtures_dir():
    """Return the fixtures directory path."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_text():
    """Sample English text for testing."""
    return """
    The quick brown fox jumps over the lazy dog. This is a simple sentence.
    I am learning English vocabulary at different levels.
    She has been studying for her IELTS exam.
    """


@pytest.fixture
def sample_wordlist():
    """Sample CEFR wordlist for testing."""
    return [
        {"word": "quick", "level": "A2", "pos": "adj"},
        {"word": "brown", "level": "A1", "pos": "adj"},
        {"word": "jump", "level": "A2", "pos": "verb"},
        {"word": "lazy", "level": "B1", "pos": "adj"},
        {"word": "simple", "level": "A2", "pos": "adj"},
        {"word": "learn", "level": "A1", "pos": "verb"},
        {"word": "vocabulary", "level": "B1", "pos": "noun"},
        {"word": "study", "level": "A2", "pos": "verb"},
        {"word": "exam", "level": "B1", "pos": "noun"},
    ]


@pytest.fixture
def sample_phrases():
    """Sample phrasal verbs for testing."""
    return [
        {
            "verb": "look up +",
            "definition": "search for information",
            "separable": True,
        },
        {
            "verb": "give up",
            "definition": "stop trying",
            "separable": False,
        },
        {
            "verb": "put * off +",
            "definition": "postpone",
            "separable": True,
        },
    ]


@pytest.fixture
def cefr_ielts_mapping():
    """Sample CEFR-IELTS mapping for testing."""
    return {
        "A1": {"ielts_min": 2.0, "ielts_max": 3.0},
        "A2": {"ielts_min": 3.0, "ielts_max": 4.0},
        "B1": {"ielts_min": 4.5, "ielts_max": 5.5},
        "B2": {"ielts_min": 6.0, "ielts_max": 6.5},
        "C1": {"ielts_min": 7.0, "ielts_max": 8.0},
        "C2": {"ielts_min": 8.5, "ielts_max": 9.0},
        "C2+": {"ielts_min": 9.0, "ielts_max": 9.0},
    }


@pytest.fixture
def temp_text_file(tmp_path):
    """Create a temporary text file for testing."""
    file_path = tmp_path / "test.txt"
    content = "This is a test file. It contains some English text for vocabulary analysis."
    file_path.write_text(content, encoding="utf-8")
    return file_path


@pytest.fixture
def temp_config_file(tmp_path):
    """Create a temporary config file for testing."""
    config_path = tmp_path / "test_config.yaml"
    config_content = """
    data:
      vocabularies_dir: "data/vocabularies"
      cefr_wordlist: "data/vocabularies/cefr_wordlist.csv"

    nlp:
      model: "en_core_web_sm"
      batch_size: 50

    analysis:
      min_word_length: 2
      exclude_numbers: true
    """
    config_path.write_text(config_content)
    return config_path
