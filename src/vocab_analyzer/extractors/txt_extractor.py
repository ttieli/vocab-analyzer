"""
Text file extractor for .txt files.
"""
from .base import BaseExtractor


class TxtExtractor(BaseExtractor):
    """
    Extractor for plain text files (.txt).
    """

    def __init__(self, encoding: str = "utf-8"):
        """
        Initialize TXT extractor.

        Args:
            encoding: Text file encoding (default: utf-8)
        """
        self.encoding = encoding

    def extract(self, file_path: str) -> str:
        """
        Extract text from a .txt file.

        Args:
            file_path: Path to the text file

        Returns:
            File content as string

        Raises:
            FileNotFoundError: If file doesn't exist
            UnicodeDecodeError: If file encoding is incorrect
            IOError: If file cannot be read
        """
        self.validate_file(file_path)

        try:
            with open(file_path, "r", encoding=self.encoding) as f:
                text = f.read()

            if not text.strip():
                raise ValueError(f"File is empty: {file_path}")

            return text

        except UnicodeDecodeError as e:
            raise UnicodeDecodeError(
                self.encoding,
                e.object,
                e.start,
                e.end,
                f"Failed to decode file with {self.encoding} encoding. "
                "Try a different encoding or check the file.",
            )

        except IOError as e:
            raise IOError(f"Failed to read file {file_path}: {e}")

    def __repr__(self) -> str:
        """String representation."""
        return f"TxtExtractor(encoding='{self.encoding}')"
