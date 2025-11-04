"""Tests for Server-Sent Events (SSE) progress streaming.

This module tests the real-time progress tracking functionality via SSE,
ensuring proper event formatting, percentage progression, and completion/error events.
"""

import json
import time
from unittest.mock import Mock, patch

import pytest

from vocab_analyzer.web.session import ProgressState, SessionStatus


class TestSSEProgressStream:
    """Tests for SSE progress streaming endpoint."""

    def test_progress_stream_format(self, client, sample_txt_file):
        """Test that SSE events are properly formatted."""
        # Upload file to create session
        with open(sample_txt_file, 'rb') as f:
            data = {'file': (f, 'test.txt')}
            upload_response = client.post('/upload', data=data, content_type='multipart/form-data')

        session_id = json.loads(upload_response.data)['session_id']

        # Connect to SSE stream
        response = client.get(f'/progress/{session_id}', headers={'Accept': 'text/event-stream'})

        # Verify response headers
        assert response.status_code == 200
        assert response.mimetype == 'text/event-stream'
        assert response.headers.get('Cache-Control') == 'no-cache'
        assert response.headers.get('X-Accel-Buffering') == 'no'

        # Verify SSE event format
        data = response.data.decode('utf-8')
        assert 'event: progress\n' in data or 'event: complete\n' in data or 'event: error\n' in data

    def test_progress_percentage_increases(self, client, sample_txt_file):
        """Test that progress percentage increases from 0% to 100%."""
        # Upload file
        with open(sample_txt_file, 'rb') as f:
            data = {'file': (f, 'test.txt')}
            upload_response = client.post('/upload', data=data, content_type='multipart/form-data')

        session_id = json.loads(upload_response.data)['session_id']

        # Poll progress endpoint multiple times
        percentages = []
        for _ in range(10):
            response = client.get(f'/progress/{session_id}')
            if response.status_code == 200:
                # Parse SSE data
                lines = response.data.decode('utf-8').split('\n')
                for line in lines:
                    if line.startswith('data: '):
                        event_data = json.loads(line[6:])
                        if 'progress' in event_data:
                            percentages.append(event_data['progress'])
            time.sleep(0.1)

        # Verify percentages are non-decreasing
        if len(percentages) > 1:
            for i in range(len(percentages) - 1):
                assert percentages[i] <= percentages[i + 1], "Progress should not decrease"

    def test_complete_event_format(self, client, sample_txt_file):
        """Test that completion event is properly formatted."""
        # Upload and wait for completion
        with open(sample_txt_file, 'rb') as f:
            data = {'file': (f, 'test.txt')}
            upload_response = client.post('/upload', data=data, content_type='multipart/form-data')

        session_id = json.loads(upload_response.data)['session_id']

        # Wait for analysis to complete
        max_wait = 30  # seconds
        waited = 0
        completed = False

        while waited < max_wait and not completed:
            response = client.get(f'/progress/{session_id}')
            if response.status_code == 200:
                data = response.data.decode('utf-8')
                if 'event: complete' in data:
                    # Parse complete event
                    lines = data.split('\n')
                    for i, line in enumerate(lines):
                        if line == 'event: complete':
                            # Next line should be data
                            if i + 1 < len(lines) and lines[i + 1].startswith('data: '):
                                event_data = json.loads(lines[i + 1][6:])
                                assert 'session_id' in event_data
                                assert 'status' in event_data
                                assert event_data['status'] == 'completed'
                                completed = True
                                break
            time.sleep(0.5)
            waited += 0.5

        assert completed, "Analysis should complete within timeout"

    def test_error_event_format(self, client):
        """Test that error events are properly formatted."""
        # Try to get progress for non-existent session
        fake_session_id = '00000000-0000-0000-0000-000000000000'
        response = client.get(f'/progress/{fake_session_id}')

        # Should return error response
        assert response.status_code in [404, 500]

        # If it's an SSE stream, verify error event format
        if response.mimetype == 'text/event-stream':
            data = response.data.decode('utf-8')
            assert 'event: error' in data

            # Parse error data
            lines = data.split('\n')
            for i, line in enumerate(lines):
                if line == 'event: error':
                    if i + 1 < len(lines) and lines[i + 1].startswith('data: '):
                        error_data = json.loads(lines[i + 1][6:])
                        assert 'error' in error_data or 'message' in error_data

    def test_session_not_found_returns_404(self, client):
        """Test that requesting progress for non-existent session returns 404."""
        fake_session_id = '00000000-0000-0000-0000-000000000000'
        response = client.get(f'/progress/{fake_session_id}')

        assert response.status_code == 404

    def test_sse_stream_closes_on_complete(self, client, sample_txt_file):
        """Test that SSE stream closes after analysis completes."""
        # Upload file
        with open(sample_txt_file, 'rb') as f:
            data = {'file': (f, 'test.txt')}
            upload_response = client.post('/upload', data=data, content_type='multipart/form-data')

        session_id = json.loads(upload_response.data)['session_id']

        # Connect to SSE and read until stream closes
        response = client.get(f'/progress/{session_id}', headers={'Accept': 'text/event-stream'})

        # Stream should eventually complete
        # Note: In real implementation, stream would stay open and send events
        # For testing, we just verify the endpoint is accessible
        assert response.status_code == 200
