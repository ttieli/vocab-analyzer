"""Analysis history management for vocabulary analyzer.

This module provides functionality to save and retrieve analysis results,
maintaining a persistent history of all analyses performed.
"""

import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from uuid import UUID

from vocab_analyzer.models.analysis import VocabularyAnalysis

logger = logging.getLogger(__name__)


@dataclass
class AnalysisHistoryEntry:
    """Represents a single entry in the analysis history."""

    id: int
    filename: str
    timestamp: str
    file_path: str
    total_words: int
    total_unique_words: int


class AnalysisHistoryManager:
    """Manages the persistent storage of analysis history."""

    def __init__(self, history_dir: Optional[Path] = None):
        """Initialize the history manager.

        Args:
            history_dir: Directory to store analysis history.
                        Defaults to data/analysis_history/
        """
        if history_dir is None:
            # Default to data/analysis_history in project root
            project_root = Path(__file__).parent.parent.parent.parent
            history_dir = project_root / "data" / "analysis_history"

        self.history_dir = Path(history_dir)
        self.metadata_file = self.history_dir / "metadata.json"

        # Ensure directory exists
        self.history_dir.mkdir(parents=True, exist_ok=True)

        # Initialize or load metadata
        self._load_metadata()

    def _load_metadata(self) -> None:
        """Load or initialize the metadata file."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.next_id = data.get("next_id", 1)
                    self.entries = [
                        AnalysisHistoryEntry(**entry) for entry in data.get("analyses", [])
                    ]
                logger.info(f"Loaded {len(self.entries)} history entries")
            except Exception as e:
                logger.error(f"Error loading metadata: {e}")
                self.next_id = 1
                self.entries = []
        else:
            self.next_id = 1
            self.entries = []
            self._save_metadata()

    def _save_metadata(self) -> None:
        """Save the metadata file."""
        try:
            data = {
                "next_id": self.next_id,
                "analyses": [asdict(entry) for entry in self.entries],
            }
            with open(self.metadata_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.debug("Metadata saved successfully")
        except Exception as e:
            logger.error(f"Error saving metadata: {e}")
            raise

    def save_analysis(
        self, analysis: VocabularyAnalysis, original_filename: str
    ) -> int:
        """Save an analysis to history.

        Args:
            analysis: The VocabularyAnalysis object to save
            original_filename: Original name of the uploaded file

        Returns:
            int: The ID assigned to this analysis
        """
        try:
            # Generate new ID
            analysis_id = self.next_id
            self.next_id += 1

            # Create file path
            file_path = f"analysis_{analysis_id}.json"
            full_path = self.history_dir / file_path

            # Convert analysis to dictionary using built-in method
            analysis_dict = analysis.to_dict(include_words=True, include_phrases=True)

            # Add history-specific fields
            analysis_dict["id"] = analysis_id
            analysis_dict["filename"] = original_filename
            analysis_dict["timestamp"] = datetime.now().isoformat()

            # Save analysis file
            with open(full_path, "w", encoding="utf-8") as f:
                json.dump(analysis_dict, f, indent=2, ensure_ascii=False)

            # Create metadata entry
            entry = AnalysisHistoryEntry(
                id=analysis_id,
                filename=original_filename,
                timestamp=datetime.now().isoformat(),
                file_path=file_path,
                total_words=analysis.statistics.get("total_word_occurrences", 0),
                total_unique_words=analysis.statistics.get("total_unique_words", 0),
            )

            # Add to entries list and save metadata
            self.entries.append(entry)
            self._save_metadata()

            logger.info(f"Saved analysis {analysis_id} for file '{original_filename}'")
            return analysis_id

        except Exception as e:
            logger.error(f"Error saving analysis: {e}")
            raise

    def get_all_entries(self) -> List[Dict]:
        """Get all history entries (metadata only).

        Returns:
            List of dictionaries containing entry metadata
        """
        # Return in reverse order (newest first)
        return [asdict(entry) for entry in reversed(self.entries)]

    def get_analysis(self, analysis_id: int) -> Optional[Dict]:
        """Get a specific analysis by ID.

        Args:
            analysis_id: The ID of the analysis to retrieve

        Returns:
            Dictionary containing the full analysis data, or None if not found
        """
        try:
            # Find the entry
            entry = next((e for e in self.entries if e.id == analysis_id), None)
            if not entry:
                logger.warning(f"Analysis {analysis_id} not found")
                return None

            # Load the analysis file
            full_path = self.history_dir / entry.file_path
            if not full_path.exists():
                logger.error(f"Analysis file not found: {full_path}")
                return None

            with open(full_path, "r", encoding="utf-8") as f:
                return json.load(f)

        except Exception as e:
            logger.error(f"Error loading analysis {analysis_id}: {e}")
            return None

    def delete_analysis(self, analysis_id: int) -> bool:
        """Delete an analysis from history.

        Args:
            analysis_id: The ID of the analysis to delete

        Returns:
            bool: True if deleted successfully, False otherwise
        """
        try:
            # Find the entry
            entry = next((e for e in self.entries if e.id == analysis_id), None)
            if not entry:
                logger.warning(f"Analysis {analysis_id} not found")
                return False

            # Delete the analysis file
            full_path = self.history_dir / entry.file_path
            if full_path.exists():
                full_path.unlink()

            # Remove from entries and save metadata
            self.entries.remove(entry)
            self._save_metadata()

            logger.info(f"Deleted analysis {analysis_id}")
            return True

        except Exception as e:
            logger.error(f"Error deleting analysis {analysis_id}: {e}")
            return False


# Global instance
_history_manager: Optional[AnalysisHistoryManager] = None


def get_history_manager() -> AnalysisHistoryManager:
    """Get or create the global history manager instance."""
    global _history_manager
    if _history_manager is None:
        _history_manager = AnalysisHistoryManager()
    return _history_manager
