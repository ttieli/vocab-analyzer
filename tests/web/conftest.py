"""Pytest fixtures for web interface tests.

This module provides shared fixtures for testing the Flask web interface,
including test clients, sample files, and session fixtures.
"""

import tempfile
from pathlib import Path

import pytest

from src.vocab_analyzer.web.app import create_app


@pytest.fixture
def app():
    """Create and configure a Flask application for testing.

    Yields:
        Flask application configured for testing
    """
    # Create temporary upload directory
    with tempfile.TemporaryDirectory() as tmpdir:
        config = {
            "TESTING": True,
            "UPLOAD_FOLDER": tmpdir,
            "SECRET_KEY": "test-secret-key",
        }

        app = create_app(config)
        yield app


@pytest.fixture
def client(app):
    """Create a Flask test client.

    Args:
        app: Flask application fixture

    Returns:
        Flask test client for making requests
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a Flask CLI test runner.

    Args:
        app: Flask application fixture

    Returns:
        Flask CLI test runner
    """
    return app.test_cli_runner()


@pytest.fixture
def sample_txt_file(tmp_path):
    """Create a sample TXT file for testing.

    Args:
        tmp_path: Pytest temporary directory fixture

    Returns:
        Path to the sample TXT file
    """
    content = """
    The quick brown fox jumps over the lazy dog.
    This is a sample text file for testing vocabulary analysis.
    It contains some common words and phrases to test the analyzer.
    """

    file_path = tmp_path / "sample.txt"
    file_path.write_text(content)
    return file_path


@pytest.fixture
def sample_large_file(tmp_path):
    """Create a large file exceeding size limit for testing.

    Args:
        tmp_path: Pytest temporary directory fixture

    Returns:
        Path to the large sample file
    """
    # Create a file larger than 50MB
    file_path = tmp_path / "large_file.txt"
    with open(file_path, 'wb') as f:
        f.write(b'x' * (51 * 1024 * 1024))  # 51MB
    return file_path


@pytest.fixture
def invalid_file(tmp_path):
    """Create an invalid file type for testing.

    Args:
        tmp_path: Pytest temporary directory fixture

    Returns:
        Path to the invalid file
    """
    file_path = tmp_path / "invalid.xyz"
    file_path.write_text("Invalid file content")
    return file_path
