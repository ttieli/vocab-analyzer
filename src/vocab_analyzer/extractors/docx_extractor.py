"""
DOCX file extractor using python-docx.
"""
from docx import Document

from .base import BaseExtractor


class DocxExtractor(BaseExtractor):
    """
    Extractor for Microsoft Word DOCX files.
    """

    def __init__(self, max_paragraphs: int = 10000):
        """
        Initialize DOCX extractor.

        Args:
            max_paragraphs: Maximum number of paragraphs to extract (default: 10000)
        """
        self.max_paragraphs = max_paragraphs

    def extract(self, file_path: str) -> str:
        """
        Extract text from a DOCX file.

        Args:
            file_path: Path to the DOCX file

        Returns:
            Extracted text as string

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If DOCX is invalid or corrupted
            IOError: If DOCX cannot be read
        """
        self.validate_file(file_path)

        try:
            doc = Document(file_path)

            paragraphs = doc.paragraphs

            if not paragraphs:
                raise ValueError(f"DOCX file has no paragraphs: {file_path}")

            # Limit paragraphs to max_paragraphs
            paragraphs_to_extract = paragraphs[: self.max_paragraphs]

            # Extract text from paragraphs
            text_parts = []
            for para in paragraphs_to_extract:
                text = para.text.strip()
                if text:  # Skip empty paragraphs
                    text_parts.append(text)

            full_text = "\n\n".join(text_parts)

            if not full_text.strip():
                raise ValueError(f"No text could be extracted from DOCX: {file_path}")

            return full_text

        except Exception as e:
            if isinstance(e, (ValueError, FileNotFoundError)):
                raise
            raise IOError(f"Failed to extract text from DOCX {file_path}: {e}")

    def __repr__(self) -> str:
        """String representation."""
        return f"DocxExtractor(max_paragraphs={self.max_paragraphs})"
