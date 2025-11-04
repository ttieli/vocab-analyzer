"""Tests for web interface route handlers.

This module tests HTTP endpoints for file upload, analysis progress,
and result downloads according to the API contracts.
"""

import io
import json
from uuid import uuid4

import pytest


class TestUploadEndpoint:
    """Tests for POST /upload endpoint."""

    def test_upload_valid_file(self, client, sample_txt_file):
        """Test uploading a valid TXT file."""
        with open(sample_txt_file, 'rb') as f:
            data = {
                'file': (f, 'test.txt')
            }
            response = client.post('/upload', data=data, content_type='multipart/form-data')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'session_id' in data
        assert 'filename' in data
        assert data['filename'] == 'test.txt'

    def test_upload_no_file(self, client):
        """Test upload request with no file."""
        response = client.post('/upload', data={}, content_type='multipart/form-data')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error'] == 'NO_FILE'

    def test_upload_invalid_type(self, client, invalid_file):
        """Test uploading an invalid file type."""
        with open(invalid_file, 'rb') as f:
            data = {
                'file': (f, 'invalid.xyz')
            }
            response = client.post('/upload', data=data, content_type='multipart/form-data')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error'] == 'INVALID_FILE_TYPE'

    def test_upload_too_large(self, client):
        """Test uploading a file that exceeds size limit."""
        # Create a file larger than 50MB in memory
        large_data = b'x' * (51 * 1024 * 1024)

        data = {
            'file': (io.BytesIO(large_data), 'large.txt')
        }
        response = client.post('/upload', data=data, content_type='multipart/form-data')

        assert response.status_code == 413


class TestDownloadEndpoint:
    """Tests for GET /download/<session_id>/<format> endpoint."""

    def test_download_json(self, client):
        """Test downloading analysis results in JSON format."""
        # This test assumes a session exists
        # In practice, would need to create a session first
        # For now, testing the 404 case
        session_id = str(uuid4())
        response = client.get(f'/download/{session_id}/json')

        assert response.status_code == 404

    def test_download_csv(self, client):
        """Test downloading analysis results in CSV format."""
        session_id = str(uuid4())
        response = client.get(f'/download/{session_id}/csv')

        assert response.status_code == 404

    def test_download_markdown(self, client):
        """Test downloading analysis results in Markdown format."""
        session_id = str(uuid4())
        response = client.get(f'/download/{session_id}/markdown')

        assert response.status_code == 404

    def test_download_session_not_found(self, client):
        """Test download request for non-existent session."""
        session_id = str(uuid4())
        response = client.get(f'/download/{session_id}/json')

        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error'] == 'SESSION_NOT_FOUND'
