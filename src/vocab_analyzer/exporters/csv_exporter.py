"""
CSV exporter for vocabulary analysis results.
"""
import csv
from pathlib import Path
from typing import Optional

from ..models import VocabularyAnalysis


class CsvExporter:
    """
    Exporter for CSV format output.
    """

    def __init__(self, delimiter: str = ",", include_header: bool = True):
        """
        Initialize CSV exporter.

        Args:
            delimiter: CSV delimiter (default: ",")
            include_header: Whether to include header row (default: True)
        """
        self.delimiter = delimiter
        self.include_header = include_header

    def export(
        self,
        analysis: VocabularyAnalysis,
        output_file: str,
        include_examples: bool = False,
        include_phrases: bool = True,
    ) -> None:
        """
        Export analysis to CSV format.

        Args:
            analysis: VocabularyAnalysis object to export
            output_file: File path to write CSV
            include_examples: Whether to include example sentences
            include_phrases: Whether to export phrases to separate file

        Raises:
            IOError: If file cannot be written
        """
        try:
            # Ensure directory exists
            Path(output_file).parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, "w", encoding="utf-8", newline="") as f:
                # Define CSV columns
                if include_examples:
                    fieldnames = [
                        "word",
                        "level",
                        "word_type",
                        "frequency",
                        "definition_cn",
                        "phonetic",
                        "original_forms",
                        "examples",
                    ]
                else:
                    fieldnames = [
                        "word",
                        "level",
                        "word_type",
                        "frequency",
                        "definition_cn",
                        "phonetic",
                        "original_forms",
                    ]

                writer = csv.DictWriter(
                    f, fieldnames=fieldnames, delimiter=self.delimiter, extrasaction="ignore"
                )

                # Write header
                if self.include_header:
                    writer.writeheader()

                # Write word rows
                for word in analysis.words.values():
                    row = {
                        "word": word.word,
                        "level": word.level,
                        "word_type": word.word_type,
                        "frequency": word.frequency,
                        "definition_cn": word.definition_cn,
                        "phonetic": word.phonetic or "",
                        "original_forms": "; ".join(word.original_forms),
                    }

                    if include_examples:
                        row["examples"] = " | ".join(word.examples)

                    writer.writerow(row)

            # Export phrases to separate file if requested
            if include_phrases and analysis.phrases:
                phrases_output = str(Path(output_file).with_stem(Path(output_file).stem + "_phrases"))
                self.export_phrases(analysis, phrases_output, include_examples)

        except IOError as e:
            raise IOError(f"Failed to write CSV file {output_file}: {e}")

    def export_phrases(
        self,
        analysis: VocabularyAnalysis,
        output_file: str,
        include_examples: bool = False,
    ) -> None:
        """
        Export phrasal verbs to CSV format.

        Args:
            analysis: VocabularyAnalysis object to export
            output_file: File path to write CSV
            include_examples: Whether to include example sentences

        Raises:
            IOError: If file cannot be written
        """
        try:
            # Ensure directory exists
            Path(output_file).parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, "w", encoding="utf-8", newline="") as f:
                # Define CSV columns for phrases
                if include_examples:
                    fieldnames = [
                        "phrase",
                        "level",
                        "phrase_type",
                        "separable",
                        "frequency",
                        "definition",
                        "definition_cn",
                        "examples",
                    ]
                else:
                    fieldnames = [
                        "phrase",
                        "level",
                        "phrase_type",
                        "separable",
                        "frequency",
                        "definition",
                        "definition_cn",
                    ]

                writer = csv.DictWriter(
                    f, fieldnames=fieldnames, delimiter=self.delimiter, extrasaction="ignore"
                )

                # Write header
                if self.include_header:
                    writer.writeheader()

                # Write phrase rows
                for phrase in analysis.phrases.values():
                    row = {
                        "phrase": phrase.phrase,
                        "level": phrase.level,
                        "phrase_type": phrase.phrase_type,
                        "separable": "Yes" if phrase.separable else "No",
                        "frequency": phrase.frequency,
                        "definition": phrase.definition,
                        "definition_cn": phrase.definition_cn,
                    }

                    if include_examples:
                        row["examples"] = " | ".join(phrase.examples)

                    writer.writerow(row)

        except IOError as e:
            raise IOError(f"Failed to write phrases CSV file {output_file}: {e}")

    def export_by_level(
        self, analysis: VocabularyAnalysis, output_dir: str, include_examples: bool = False
    ) -> None:
        """
        Export analysis to separate CSV files per CEFR level.

        Args:
            analysis: VocabularyAnalysis object to export
            output_dir: Directory to write CSV files
            include_examples: Whether to include example sentences

        Raises:
            IOError: If files cannot be written
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        levels = ["A1", "A2", "B1", "B2", "C1", "C2", "C2+"]

        for level in levels:
            words_at_level = analysis.get_words_by_level(level)

            if not words_at_level:
                continue

            # Create a temporary analysis with just this level
            level_analysis = VocabularyAnalysis(source_file=f"{analysis.source_file}_{level}")
            for word in words_at_level:
                level_analysis.add_word(word)

            # Export to file
            output_file = output_path / f"level_{level}.csv"
            self.export(level_analysis, str(output_file), include_examples=include_examples)

    def __repr__(self) -> str:
        """String representation."""
        return f"CsvExporter(delimiter='{self.delimiter}')"
