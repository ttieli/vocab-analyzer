"""
File operation utilities for vocab-analyzer.
"""
import os
from pathlib import Path
from typing import Optional


def check_file_exists(file_path: str) -> bool:
    """
    Check if a file exists.

    Args:
        file_path: Path to the file

    Returns:
        True if file exists, False otherwise
    """
    return Path(file_path).is_file()


def check_file_size(file_path: str) -> int:
    """
    Get file size in bytes.

    Args:
        file_path: Path to the file

    Returns:
        File size in bytes

    Raises:
        FileNotFoundError: If file doesn't exist
    """
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    return path.stat().st_size


def get_file_extension(file_path: str) -> str:
    """
    Get file extension (lowercase, without dot).

    Args:
        file_path: Path to the file

    Returns:
        File extension without dot (e.g., "txt", "pdf", "docx")

    Examples:
        >>> get_file_extension("document.PDF")
        'pdf'
        >>> get_file_extension("book.txt")
        'txt'
    """
    return Path(file_path).suffix.lstrip(".").lower()


def ensure_directory_exists(directory_path: str) -> Path:
    """
    Ensure a directory exists, create it if necessary.

    Args:
        directory_path: Path to the directory

    Returns:
        Path object to the directory
    """
    path = Path(directory_path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_file_name_without_extension(file_path: str) -> str:
    """
    Get filename without extension.

    Args:
        file_path: Path to the file

    Returns:
        Filename without extension

    Examples:
        >>> get_file_name_without_extension("/path/to/document.pdf")
        'document'
    """
    return Path(file_path).stem


def validate_file_for_analysis(file_path: str, max_size_mb: Optional[int] = None) -> tuple[bool, str]:
    """
    Validate that a file can be analyzed.

    Checks:
    - File exists
    - File is not empty
    - File extension is supported (txt, pdf, docx, json)
    - File size is within limits (if specified)

    Args:
        file_path: Path to the file
        max_size_mb: Maximum file size in MB (optional)

    Returns:
        Tuple of (is_valid, error_message)
        If valid, error_message is empty string
    """
    path = Path(file_path)

    # Check existence
    if not path.is_file():
        return False, f"File not found: {file_path}"

    # Check if empty
    if path.stat().st_size == 0:
        return False, f"File is empty: {file_path}"

    # Check extension
    ext = get_file_extension(file_path)
    supported_extensions = {"txt", "pdf", "docx", "json"}
    if ext not in supported_extensions:
        return False, f"Unsupported file type: .{ext}. Supported: {supported_extensions}"

    # Check size if limit specified
    if max_size_mb:
        size_mb = path.stat().st_size / (1024 * 1024)
        if size_mb > max_size_mb:
            return False, f"File too large: {size_mb:.1f}MB (max: {max_size_mb}MB)"

    return True, ""


def get_output_file_path(
    input_file: str, output_format: str, output_dir: Optional[str] = None
) -> Path:
    """
    Generate output file path based on input file and format.

    Args:
        input_file: Path to input file
        output_format: Output format (json, csv, md)
        output_dir: Optional output directory (defaults to same as input)

    Returns:
        Path object for output file

    Examples:
        >>> get_output_file_path("book.txt", "json")
        Path('book_vocab.json')
        >>> get_output_file_path("book.pdf", "csv", "output")
        Path('output/book_vocab.csv')
    """
    input_path = Path(input_file)
    base_name = input_path.stem

    # Generate output filename
    output_name = f"{base_name}_vocab.{output_format}"

    if output_dir:
        output_path = Path(output_dir) / output_name
        ensure_directory_exists(output_dir)
    else:
        output_path = input_path.parent / output_name

    return output_path


def read_file_safely(file_path: str, encoding: str = "utf-8") -> Optional[str]:
    """
    Safely read file content with error handling.

    Args:
        file_path: Path to the file
        encoding: File encoding (default: utf-8)

    Returns:
        File content as string, or None if error occurs
    """
    try:
        with open(file_path, "r", encoding=encoding) as f:
            return f.read()
    except (IOError, UnicodeDecodeError) as e:
        print(f"Error reading file {file_path}: {e}")
        return None


def write_file_safely(file_path: str, content: str, encoding: str = "utf-8") -> bool:
    """
    Safely write content to file with error handling.

    Args:
        file_path: Path to the file
        content: Content to write
        encoding: File encoding (default: utf-8)

    Returns:
        True if successful, False otherwise
    """
    try:
        # Ensure directory exists
        ensure_directory_exists(str(Path(file_path).parent))

        with open(file_path, "w", encoding=encoding) as f:
            f.write(content)
        return True
    except IOError as e:
        print(f"Error writing file {file_path}: {e}")
        return False
