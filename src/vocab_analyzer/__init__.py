"""
Vocab Analyzer - English Book Vocabulary Level Analysis Tool

A CLI tool for analyzing English texts and classifying vocabulary by CEFR levels (A1-C2).
"""

__version__ = "0.1.0"
__author__ = "Development Team"
__license__ = "MIT"

# Core components
from .core.analyzer import VocabularyAnalyzer
from .core.config import Config

# Data models
from .models import Phrase, VocabularyAnalysis, Word

# Exporters
from .exporters import CsvExporter, JsonExporter, MarkdownExporter

# Main CLI
from .cli.main import cli

__all__ = [
    # Core
    "VocabularyAnalyzer",
    "Config",
    # Models
    "Word",
    "Phrase",
    "VocabularyAnalysis",
    # Exporters
    "JsonExporter",
    "CsvExporter",
    "MarkdownExporter",
    # CLI
    "cli",
    # Metadata
    "__version__",
]
