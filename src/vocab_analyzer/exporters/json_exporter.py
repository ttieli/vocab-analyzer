"""
JSON exporter for vocabulary analysis results.
"""
import json
from pathlib import Path
from typing import Optional

from ..models import VocabularyAnalysis


class JsonExporter:
    """
    Exporter for JSON format output.
    """

    def __init__(self, indent: int = 2, ensure_ascii: bool = False):
        """
        Initialize JSON exporter.

        Args:
            indent: Indentation level for pretty printing (default: 2)
            ensure_ascii: Whether to escape non-ASCII characters (default: False)
        """
        self.indent = indent
        self.ensure_ascii = ensure_ascii

    def export(
        self,
        analysis: VocabularyAnalysis,
        output_file: Optional[str] = None,
        include_words: bool = True,
        include_phrases: bool = True,
    ) -> str:
        """
        Export analysis to JSON format.

        Args:
            analysis: VocabularyAnalysis object to export
            output_file: Optional file path to write (if None, returns string)
            include_words: Whether to include word details
            include_phrases: Whether to include phrase details

        Returns:
            JSON string

        Raises:
            IOError: If file cannot be written
        """
        # Convert to dictionary
        data = analysis.to_dict(include_words=include_words, include_phrases=include_phrases)

        # Convert to JSON
        json_str = json.dumps(data, indent=self.indent, ensure_ascii=self.ensure_ascii)

        # Write to file if specified
        if output_file:
            try:
                Path(output_file).parent.mkdir(parents=True, exist_ok=True)
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(json_str)
            except IOError as e:
                raise IOError(f"Failed to write JSON file {output_file}: {e}")

        return json_str

    def __repr__(self) -> str:
        """String representation."""
        return f"JsonExporter(indent={self.indent})"
