"""
Data models for vocab-analyzer.
"""
from .analysis import VocabularyAnalysis
from .phrase import Phrase
from .word import Word

__all__ = ["Word", "Phrase", "VocabularyAnalysis"]
