"""
Statistics analyzer for vocabulary analysis results.
"""
from typing import Dict, List

from ..models import VocabularyAnalysis, Word


class StatisticsAnalyzer:
    """
    Analyzer for generating statistics and insights from vocabulary analysis.
    """

    @staticmethod
    def generate_summary(analysis: VocabularyAnalysis) -> Dict[str, any]:
        """
        Generate a comprehensive summary of the analysis.

        Args:
            analysis: VocabularyAnalysis object

        Returns:
            Dictionary with summary statistics
        """
        stats = analysis.statistics.copy()

        # Add additional insights
        stats["insights"] = StatisticsAnalyzer._generate_insights(analysis)

        return stats

    @staticmethod
    def _generate_insights(analysis: VocabularyAnalysis) -> List[str]:
        """
        Generate human-readable insights from the analysis.

        Args:
            analysis: VocabularyAnalysis object

        Returns:
            List of insight strings
        """
        insights = []
        stats = analysis.statistics

        total_words = stats.get("total_unique_words", 0)
        if total_words == 0:
            return ["No vocabulary found in the text."]

        # Level distribution insights
        level_dist = stats.get("level_distribution", {})

        # Find dominant level
        max_level = None
        max_count = 0
        for level, data in level_dist.items():
            if data["count"] > max_count:
                max_count = data["count"]
                max_level = level

        if max_level:
            percentage = level_dist[max_level]["percentage"]
            insights.append(
                f"The text is dominated by {max_level} level vocabulary ({percentage:.1f}%)."
            )

        # Beginner vs advanced
        beginner_count = (
            level_dist.get("A1", {}).get("count", 0)
            + level_dist.get("A2", {}).get("count", 0)
        )
        advanced_count = (
            level_dist.get("C1", {}).get("count", 0)
            + level_dist.get("C2", {}).get("count", 0)
            + level_dist.get("C2+", {}).get("count", 0)
        )

        beginner_pct = (beginner_count / total_words * 100) if total_words > 0 else 0
        advanced_pct = (advanced_count / total_words * 100) if total_words > 0 else 0

        if beginner_pct > 60:
            insights.append(
                "This text is suitable for beginners (60%+ A1-A2 vocabulary)."
            )
        elif advanced_pct > 30:
            insights.append(
                "This text contains significant advanced vocabulary (30%+ C1-C2)."
            )

        # Difficulty estimate
        difficulty = StatisticsAnalyzer._estimate_difficulty(level_dist)
        insights.append(f"Estimated difficulty: {difficulty}")

        # Word type insights
        word_type_dist = stats.get("word_type_distribution", {})
        if word_type_dist:
            most_common_type = max(word_type_dist.items(), key=lambda x: x[1])
            insights.append(
                f"Most common word type: {most_common_type[0]} ({most_common_type[1]} words)"
            )

        return insights

    @staticmethod
    def _estimate_difficulty(level_dist: Dict[str, Dict]) -> str:
        """
        Estimate overall text difficulty based on level distribution.

        Args:
            level_dist: Level distribution dictionary

        Returns:
            Difficulty estimate (Beginner, Elementary, Intermediate, Upper-Intermediate, Advanced)
        """
        # Calculate weighted average
        level_weights = {
            "A1": 1,
            "A2": 2,
            "B1": 3,
            "B2": 4,
            "C1": 5,
            "C2": 6,
            "C2+": 7,
        }

        total_weight = 0
        total_count = 0

        for level, data in level_dist.items():
            if level in level_weights:
                count = data.get("count", 0)
                total_weight += level_weights[level] * count
                total_count += count

        if total_count == 0:
            return "Unknown"

        avg_weight = total_weight / total_count

        # Map to difficulty levels
        if avg_weight < 1.5:
            return "Beginner (A1)"
        elif avg_weight < 2.5:
            return "Elementary (A2)"
        elif avg_weight < 3.5:
            return "Intermediate (B1)"
        elif avg_weight < 4.5:
            return "Upper-Intermediate (B2)"
        elif avg_weight < 5.5:
            return "Advanced (C1)"
        else:
            return "Proficiency (C2)"

    @staticmethod
    def get_top_words_by_level(
        analysis: VocabularyAnalysis, n: int = 10
    ) -> Dict[str, List[Word]]:
        """
        Get top N words for each CEFR level.

        Args:
            analysis: VocabularyAnalysis object
            n: Number of top words per level

        Returns:
            Dictionary mapping level to list of top words
        """
        result = {}

        for level in ["A1", "A2", "B1", "B2", "C1", "C2", "C2+"]:
            words = analysis.get_words_by_level(level)
            if words:
                # Sort by frequency
                sorted_words = sorted(words, key=lambda w: w.frequency, reverse=True)
                result[level] = sorted_words[:n]

        return result

    @staticmethod
    def get_frequency_distribution(analysis: VocabularyAnalysis) -> Dict[str, int]:
        """
        Get distribution of word frequencies.

        Args:
            analysis: VocabularyAnalysis object

        Returns:
            Dictionary mapping frequency ranges to word counts
        """
        ranges = {
            "1": 0,  # Words appearing once
            "2-5": 0,
            "6-10": 0,
            "11-20": 0,
            "21-50": 0,
            "50+": 0,
        }

        for word in analysis.words.values():
            freq = word.frequency

            if freq == 1:
                ranges["1"] += 1
            elif freq <= 5:
                ranges["2-5"] += 1
            elif freq <= 10:
                ranges["6-10"] += 1
            elif freq <= 20:
                ranges["11-20"] += 1
            elif freq <= 50:
                ranges["21-50"] += 1
            else:
                ranges["50+"] += 1

        return ranges

    @staticmethod
    def print_summary(analysis: VocabularyAnalysis) -> None:
        """
        Print a formatted summary to console.

        Args:
            analysis: VocabularyAnalysis object
        """
        summary = StatisticsAnalyzer.generate_summary(analysis)

        print("\n" + "=" * 60)
        print(f"Vocabulary Analysis Summary: {analysis.source_file}")
        print("=" * 60 + "\n")

        # Basic stats
        print(f"Total Unique Words: {summary['total_unique_words']}")
        print(f"Total Word Occurrences: {summary['total_word_occurrences']}\n")

        # Level distribution
        print("CEFR Level Distribution:")
        print("-" * 40)
        level_dist = summary.get("level_distribution", {})
        for level in ["A1", "A2", "B1", "B2", "C1", "C2", "C2+"]:
            if level in level_dist:
                data = level_dist[level]
                count = data["count"]
                percentage = data["percentage"]
                bar = "█" * int(percentage / 2)  # Simple bar chart
                print(f"  {level:4} | {count:4} | {percentage:5.1f}% | {bar}")

        # Insights
        if "insights" in summary:
            print("\nInsights:")
            print("-" * 40)
            for insight in summary["insights"]:
                print(f"  • {insight}")

        print("\n" + "=" * 60 + "\n")
