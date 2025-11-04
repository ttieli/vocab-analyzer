"""
PDF file extractor using PyPDF2.
"""
from PyPDF2 import PdfReader

from .base import BaseExtractor


class PdfExtractor(BaseExtractor):
    """
    Extractor for PDF files using PyPDF2.
    """

    def __init__(self, max_pages: int = 1000):
        """
        Initialize PDF extractor.

        Args:
            max_pages: Maximum number of pages to extract (default: 1000)
        """
        self.max_pages = max_pages

    def extract(self, file_path: str) -> str:
        """
        Extract text from a PDF file.

        Args:
            file_path: Path to the PDF file

        Returns:
            Extracted text as string

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If PDF is encrypted or invalid
            IOError: If PDF cannot be read
        """
        self.validate_file(file_path)

        try:
            reader = PdfReader(file_path)

            # Check if PDF is encrypted
            if reader.is_encrypted:
                raise ValueError(
                    f"PDF file is encrypted and cannot be read: {file_path}. "
                    "Please decrypt the PDF first."
                )

            num_pages = len(reader.pages)

            if num_pages == 0:
                raise ValueError(f"PDF file has no pages: {file_path}")

            # Limit pages to max_pages
            pages_to_extract = min(num_pages, self.max_pages)

            # Extract text from all pages
            text_parts = []
            for page_num in range(pages_to_extract):
                page = reader.pages[page_num]
                text = page.extract_text()
                if text:
                    text_parts.append(text)

            full_text = "\n\n".join(text_parts)

            if not full_text.strip():
                raise ValueError(f"No text could be extracted from PDF: {file_path}")

            return full_text

        except Exception as e:
            if isinstance(e, (ValueError, FileNotFoundError)):
                raise
            raise IOError(f"Failed to extract text from PDF {file_path}: {e}")

    def __repr__(self) -> str:
        """String representation."""
        return f"PdfExtractor(max_pages={self.max_pages})"
