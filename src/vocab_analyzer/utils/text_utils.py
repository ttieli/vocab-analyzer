"""
Text processing utilities for vocab-analyzer.
"""
import re
from typing import List


def clean_text(text: str) -> str:
    """
    Clean text by normalizing whitespace and removing unwanted characters.

    Operations:
    - Remove multiple spaces
    - Remove multiple newlines
    - Strip leading/trailing whitespace
    - Normalize line endings

    Args:
        text: Input text to clean

    Returns:
        Cleaned text
    """
    if not text:
        return ""

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove multiple spaces
    text = re.sub(r" +", " ", text)

    # Remove multiple newlines (keep max 2 for paragraph separation)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Strip whitespace
    text = text.strip()

    return text


def split_sentences(text: str) -> List[str]:
    """
    Split text into sentences using simple rules.

    This is a basic implementation. For better results, use spaCy's
    sentence segmentation in the processor module.

    Args:
        text: Input text to split

    Returns:
        List of sentences
    """
    if not text:
        return []

    # Simple sentence splitting on common terminators
    # Note: This is basic; spaCy does a better job
    sentences = re.split(r"(?<=[.!?])\s+", text)

    # Filter out empty sentences and strip whitespace
    sentences = [s.strip() for s in sentences if s.strip()]

    return sentences


def remove_extra_whitespace(text: str) -> str:
    """
    Remove extra whitespace from text while preserving single spaces.

    Args:
        text: Input text

    Returns:
        Text with normalized whitespace
    """
    return " ".join(text.split())


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to maximum length, adding suffix if truncated.

    Args:
        text: Input text
        max_length: Maximum length including suffix
        suffix: Suffix to add when truncating (default: "...")

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text

    if max_length <= len(suffix):
        return suffix[:max_length]

    return text[: max_length - len(suffix)] + suffix


def extract_context_around_word(text: str, word: str, context_words: int = 10) -> List[str]:
    """
    Extract context snippets around occurrences of a word.

    Args:
        text: Full text to search
        word: Word to find
        context_words: Number of words to include before and after

    Returns:
        List of context snippets

    Examples:
        >>> text = "The quick brown fox jumps over the lazy dog"
        >>> extract_context_around_word(text, "fox", 2)
        ['... quick brown fox jumps over ...']
    """
    if not text or not word:
        return []

    # Split into words (simple tokenization)
    words = text.split()

    # Find indices where word appears (case-insensitive)
    word_lower = word.lower()
    indices = [i for i, w in enumerate(words) if w.lower() == word_lower]

    contexts = []
    for idx in indices:
        # Get context window
        start = max(0, idx - context_words)
        end = min(len(words), idx + context_words + 1)

        context_words_list = words[start:end]

        # Add ellipsis if truncated
        prefix = "... " if start > 0 else ""
        suffix = " ..." if end < len(words) else ""

        context = prefix + " ".join(context_words_list) + suffix
        contexts.append(context)

    return contexts


def is_likely_proper_noun(word: str) -> bool:
    """
    Simple heuristic to check if a word is likely a proper noun.

    Checks if word starts with uppercase letter.

    Args:
        word: Word to check

    Returns:
        True if likely a proper noun
    """
    if not word:
        return False

    return word[0].isupper()


def normalize_word(word: str) -> str:
    """
    Normalize word for comparison (lowercase, strip punctuation).

    Args:
        word: Word to normalize

    Returns:
        Normalized word
    """
    # Convert to lowercase
    word = word.lower()

    # Remove leading/trailing punctuation
    word = word.strip(".,!?;:\"'()[]{}").strip()

    return word


def contains_digit(text: str) -> bool:
    """
    Check if text contains any digits.

    Args:
        text: Text to check

    Returns:
        True if text contains at least one digit
    """
    return any(c.isdigit() for c in text)


def is_all_punctuation(text: str) -> bool:
    """
    Check if text consists only of punctuation characters.

    Args:
        text: Text to check

    Returns:
        True if text is all punctuation
    """
    if not text:
        return False

    import string

    return all(c in string.punctuation for c in text)


def remove_punctuation(text: str) -> str:
    """
    Remove all punctuation from text.

    Args:
        text: Input text

    Returns:
        Text without punctuation
    """
    import string

    return text.translate(str.maketrans("", "", string.punctuation))


def word_count(text: str) -> int:
    """
    Count words in text (simple whitespace-based).

    Args:
        text: Input text

    Returns:
        Number of words
    """
    if not text:
        return 0

    return len(text.split())


def extract_sentences_with_word(text: str, word: str, max_sentences: int = 3) -> List[str]:
    """
    Extract sentences containing a specific word.

    Args:
        text: Full text
        word: Word to search for
        max_sentences: Maximum number of sentences to return

    Returns:
        List of sentences containing the word
    """
    sentences = split_sentences(text)
    word_lower = word.lower()

    matching = []
    for sentence in sentences:
        if word_lower in sentence.lower():
            matching.append(sentence.strip())
            if len(matching) >= max_sentences:
                break

    return matching
