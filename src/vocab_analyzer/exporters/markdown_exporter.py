"""
Markdown exporter for vocabulary analysis results.
"""
from pathlib import Path
from typing import Optional

from ..models import VocabularyAnalysis


class MarkdownExporter:
    """
    Exporter for Markdown format output.
    """

    def __init__(self, include_toc: bool = True):
        """
        Initialize Markdown exporter.

        Args:
            include_toc: Whether to include table of contents (default: True)
        """
        self.include_toc = include_toc

    def export(
        self,
        analysis: VocabularyAnalysis,
        output_file: str,
        include_examples: bool = True,
        include_phrases: bool = True,
    ) -> str:
        """
        Export analysis to Markdown format.

        Args:
            analysis: VocabularyAnalysis object to export
            output_file: File path to write Markdown
            include_examples: Whether to include example sentences
            include_phrases: Whether to include phrasal verbs section

        Returns:
            Markdown string

        Raises:
            IOError: If file cannot be written
        """
        md_parts = []

        # Title
        md_parts.append(f"# Vocabulary Analysis: {Path(analysis.source_file).name}\n")
        md_parts.append(f"**Analysis Date**: {analysis.analysis_date.strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Statistics
        md_parts.append("\n## Statistics\n")
        stats = analysis.statistics
        md_parts.append(f"- **Total Unique Words**: {stats['total_unique_words']}")
        md_parts.append(
            f"- **Total Word Occurrences**: {stats['total_word_occurrences']}"
        )
        if include_phrases and analysis.phrases:
            md_parts.append(f"- **Total Unique Phrases**: {len(analysis.phrases)}")
            total_phrase_occurrences = sum(p.frequency for p in analysis.phrases.values())
            md_parts.append(f"- **Total Phrase Occurrences**: {total_phrase_occurrences}\n")
        else:
            md_parts.append("")

        # Level distribution
        md_parts.append("\n### CEFR Level Distribution\n")
        md_parts.append("| Level | Count | Percentage |")
        md_parts.append("|-------|-------|------------|")

        level_dist = stats.get("level_distribution", {})
        for level in ["A1", "A2", "B1", "B2", "C1", "C2", "C2+"]:
            if level in level_dist:
                count = level_dist[level]["count"]
                percentage = level_dist[level]["percentage"]
                md_parts.append(f"| {level} | {count} | {percentage:.1f}% |")

        # Word type distribution
        if "word_type_distribution" in stats:
            md_parts.append("\n### Word Type Distribution\n")
            md_parts.append("| Type | Count |")
            md_parts.append("|------|-------|")

            for word_type, count in sorted(
                stats["word_type_distribution"].items(), key=lambda x: x[1], reverse=True
            ):
                md_parts.append(f"| {word_type} | {count} |")

        # Table of contents
        if self.include_toc:
            md_parts.append("\n## Table of Contents\n")
            for level in ["A1", "A2", "B1", "B2", "C1", "C2", "C2+"]:
                words_at_level = analysis.get_words_by_level(level)
                if words_at_level:
                    md_parts.append(f"- [{level} Level Words](#level-{level.lower()})")

        # Words by level
        md_parts.append("\n## Vocabulary by CEFR Level\n")

        for level in ["A1", "A2", "B1", "B2", "C1", "C2", "C2+"]:
            words_at_level = analysis.get_words_by_level(level)

            if not words_at_level:
                continue

            md_parts.append(f"\n### Level {level}\n")

            # Sort by frequency
            sorted_words = sorted(words_at_level, key=lambda w: w.frequency, reverse=True)

            for word in sorted_words:
                # Word header
                md_parts.append(f"\n#### {word.word}")

                # Details
                details = []
                details.append(f"**Type**: {word.word_type}")
                details.append(f"**Frequency**: {word.frequency}")

                if word.definition_cn:
                    details.append(f"**Chinese**: {word.definition_cn}")

                if word.phonetic:
                    details.append(f"**Phonetic**: {word.phonetic}")

                if word.original_forms:
                    forms = ", ".join(word.original_forms)
                    details.append(f"**Forms**: {forms}")

                md_parts.append(" | ".join(details))

                # Examples
                if include_examples and word.examples:
                    md_parts.append("\n**Examples**:")
                    for i, example in enumerate(word.examples, 1):
                        md_parts.append(f"{i}. {example}")

        # Phrasal Verbs section
        if include_phrases and analysis.phrases:
            md_parts.append("\n## Phrasal Verbs\n")

            # Sort by frequency
            sorted_phrases = sorted(
                analysis.phrases.values(), key=lambda p: p.frequency, reverse=True
            )

            # Group by level
            phrases_by_level = {}
            for phrase in sorted_phrases:
                if phrase.level not in phrases_by_level:
                    phrases_by_level[phrase.level] = []
                phrases_by_level[phrase.level].append(phrase)

            for level in ["B1", "B2", "C1", "C2"]:
                if level not in phrases_by_level:
                    continue

                phrases = phrases_by_level[level]
                md_parts.append(f"\n### Level {level} Phrasal Verbs ({len(phrases)})\n")

                for phrase in phrases:
                    # Phrase header
                    separable_marker = " (separable)" if phrase.separable else ""
                    md_parts.append(f"\n#### {phrase.phrase}{separable_marker}")

                    # Details
                    details = []
                    details.append(f"**Frequency**: {phrase.frequency}")

                    if phrase.definition:
                        details.append(f"**Definition**: {phrase.definition}")

                    if phrase.definition_cn:
                        details.append(f"**中文**: {phrase.definition_cn}")

                    md_parts.append(" | ".join(details))

                    # Examples
                    if include_examples and phrase.examples:
                        md_parts.append("\n**Examples**:")
                        for i, example in enumerate(phrase.examples, 1):
                            md_parts.append(f"{i}. {example}")

        # Combine all parts
        markdown = "\n".join(md_parts)

        # Write to file
        try:
            Path(output_file).parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(markdown)
        except IOError as e:
            raise IOError(f"Failed to write Markdown file {output_file}: {e}")

        return markdown

    def __repr__(self) -> str:
        """String representation."""
        return f"MarkdownExporter(include_toc={self.include_toc})"
