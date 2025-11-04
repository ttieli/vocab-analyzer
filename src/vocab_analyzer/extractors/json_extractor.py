"""
JSON file extractor for structured text data.
"""
import json

from .base import BaseExtractor


class JsonExtractor(BaseExtractor):
    """
    Extractor for JSON files containing text data.

    Supports extracting text from:
    - Simple string values
    - Arrays of strings
    - Nested objects with text fields
    """

    def __init__(self, text_field: str = "text"):
        """
        Initialize JSON extractor.

        Args:
            text_field: Field name to extract text from (default: "text")
        """
        self.text_field = text_field

    def extract(self, file_path: str) -> str:
        """
        Extract text from a JSON file.

        Args:
            file_path: Path to the JSON file

        Returns:
            Extracted text as string

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If JSON is invalid or has wrong structure
            IOError: If file cannot be read
        """
        self.validate_file(file_path)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Extract text based on JSON structure
            text = self._extract_text_from_data(data)

            if not text.strip():
                raise ValueError(f"No text found in JSON file: {file_path}")

            return text

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in {file_path}: {e}")

        except IOError as e:
            raise IOError(f"Failed to read JSON file {file_path}: {e}")

    def _extract_text_from_data(self, data) -> str:
        """
        Recursively extract text from JSON data structure.

        Args:
            data: JSON data (dict, list, or string)

        Returns:
            Extracted text
        """
        if isinstance(data, str):
            # Direct string
            return data

        elif isinstance(data, list):
            # Array of items
            text_parts = []
            for item in data:
                text = self._extract_text_from_data(item)
                if text:
                    text_parts.append(text)
            return "\n\n".join(text_parts)

        elif isinstance(data, dict):
            # Object with fields
            # First try to find the specified text field
            if self.text_field in data:
                return self._extract_text_from_data(data[self.text_field])

            # Otherwise, try common text field names
            for field_name in ["text", "content", "body", "description", "value"]:
                if field_name in data:
                    return self._extract_text_from_data(data[field_name])

            # If no text field found, concatenate all string values
            text_parts = []
            for value in data.values():
                if isinstance(value, str):
                    text_parts.append(value)
                elif isinstance(value, (list, dict)):
                    text = self._extract_text_from_data(value)
                    if text:
                        text_parts.append(text)

            return "\n\n".join(text_parts)

        else:
            # Other types (numbers, booleans, None)
            return ""

    def __repr__(self) -> str:
        """String representation."""
        return f"JsonExtractor(text_field='{self.text_field}')"
