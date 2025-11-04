"""
Base extractor abstract class for text extraction.
"""
from abc import ABC, abstractmethod


class BaseExtractor(ABC):
    """
    Abstract base class for text extractors.

    All extractors must implement the extract method to extract
    text from different file formats.
    """

    @abstractmethod
    def extract(self, file_path: str) -> str:
        """
        Extract text from a file.

        Args:
            file_path: Path to the file to extract text from

        Returns:
            Extracted text as string

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is invalid or extraction fails
        """
        pass

    def validate_file(self, file_path: str) -> None:
        """
        Validate that file exists and is readable.

        Args:
            file_path: Path to the file

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        from pathlib import Path

        if not Path(file_path).is_file():
            raise FileNotFoundError(f"File not found: {file_path}")
