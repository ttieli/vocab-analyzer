"""
Utility functions for vocab-analyzer.
"""
from .cache import (
    SimpleCache,
    cached_property,
    clear_all_caches,
    get_phrase_cache,
    get_vocabulary_cache,
    memoize,
)
from .file_utils import (
    check_file_exists,
    check_file_size,
    ensure_directory_exists,
    get_file_extension,
    get_file_name_without_extension,
    get_output_file_path,
    read_file_safely,
    validate_file_for_analysis,
    write_file_safely,
)
from .text_utils import (
    clean_text,
    contains_digit,
    extract_context_around_word,
    extract_sentences_with_word,
    is_all_punctuation,
    is_likely_proper_noun,
    normalize_word,
    remove_extra_whitespace,
    remove_punctuation,
    split_sentences,
    truncate_text,
    word_count,
)

__all__ = [
    # Cache utilities
    "SimpleCache",
    "cached_property",
    "memoize",
    "get_vocabulary_cache",
    "get_phrase_cache",
    "clear_all_caches",
    # File utilities
    "check_file_exists",
    "check_file_size",
    "get_file_extension",
    "ensure_directory_exists",
    "get_file_name_without_extension",
    "validate_file_for_analysis",
    "get_output_file_path",
    "read_file_safely",
    "write_file_safely",
    # Text utilities
    "clean_text",
    "split_sentences",
    "remove_extra_whitespace",
    "truncate_text",
    "extract_context_around_word",
    "is_likely_proper_noun",
    "normalize_word",
    "contains_digit",
    "is_all_punctuation",
    "remove_punctuation",
    "word_count",
    "extract_sentences_with_word",
]
