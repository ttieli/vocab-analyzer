"""Tests for progress tracking functionality.

This module tests the ProgressTracker class and its SSE event formatting capabilities.
"""

import json
from datetime import datetime
from uuid import uuid4

import pytest

from vocab_analyzer.web.progress import ProgressTracker
from vocab_analyzer.web.session import (
    ErrorInfo,
    ProgressState,
    SessionStatus,
    UploadedFile,
    UploadSession,
)


class TestProgressTracker:
    """Tests for ProgressTracker class."""

    def test_format_progress_event(self):
        """Test formatting progress update as SSE event."""
        # Create sample session
        uploaded_file = UploadedFile(
            filename="test.txt",
            file_path="/tmp/test.txt",
            file_type=".txt",
            size_bytes=1024
        )

        session = UploadSession(
            session_id=uuid4(),
            uploaded_file=uploaded_file,
            status=SessionStatus.TOKENIZING,
            progress_percentage=40
        )

        # Format as SSE event
        event = ProgressTracker.format_progress_event(session)

        # Verify SSE format
        assert event.startswith('event: progress\n')
        assert 'data: ' in event
        assert event.endswith('\n\n')

        # Parse data
        lines = event.split('\n')
        data_line = [line for line in lines if line.startswith('data: ')][0]
        data = json.loads(data_line[6:])

        assert 'session_id' in data
        assert 'status' in data
        assert 'progress' in data
        assert 'stage' in data
        assert data['status'] == 'tokenizing'
        assert data['progress'] == 40

    def test_format_complete_event(self):
        """Test formatting completion event."""
        uploaded_file = UploadedFile(
            filename="test.txt",
            file_path="/tmp/test.txt",
            file_type=".txt",
            size_bytes=1024
        )

        session = UploadSession(
            session_id=uuid4(),
            uploaded_file=uploaded_file,
            status=SessionStatus.COMPLETED,
            progress_percentage=100
        )

        # Format as SSE event
        event = ProgressTracker.format_complete_event(session)

        # Verify SSE format
        assert event.startswith('event: complete\n')
        assert 'data: ' in event
        assert event.endswith('\n\n')

        # Parse data
        lines = event.split('\n')
        data_line = [line for line in lines if line.startswith('data: ')][0]
        data = json.loads(data_line[6:])

        assert data['status'] == 'completed'
        assert data['progress'] == 100

    def test_format_error_event(self):
        """Test formatting error event."""
        uploaded_file = UploadedFile(
            filename="test.txt",
            file_path="/tmp/test.txt",
            file_type=".txt",
            size_bytes=1024
        )

        error = ErrorInfo(
            code="ANALYSIS_ERROR",
            message="Test error message",
            details="Detailed error information"
        )

        session = UploadSession(
            session_id=uuid4(),
            uploaded_file=uploaded_file,
            status=SessionStatus.FAILED,
            error=error
        )

        # Format as SSE event
        event = ProgressTracker.format_error_event(session)

        # Verify SSE format
        assert event.startswith('event: error\n')
        assert 'data: ' in event
        assert event.endswith('\n\n')

        # Parse data
        lines = event.split('\n')
        data_line = [line for line in lines if line.startswith('data: ')][0]
        data = json.loads(data_line[6:])

        assert data['status'] == 'failed'
        assert 'error' in data
        assert data['error']['code'] == 'ANALYSIS_ERROR'
        assert data['error']['message'] == 'Test error message'

    def test_update_stage(self):
        """Test updating session progress stage."""
        uploaded_file = UploadedFile(
            filename="test.txt",
            file_path="/tmp/test.txt",
            file_type=".txt",
            size_bytes=1024
        )

        session = UploadSession(
            session_id=uuid4(),
            uploaded_file=uploaded_file,
            status=SessionStatus.PENDING,
            progress_percentage=0
        )

        # Update to extracting stage
        session.update_progress(ProgressState.EXTRACTING)

        assert session.status == SessionStatus.EXTRACTING
        assert session.progress_percentage == 15

    def test_stage_percentage_mapping(self):
        """Test that progress states map to correct percentages."""
        test_cases = [
            (ProgressState.VALIDATING, 5),
            (ProgressState.EXTRACTING, 15),
            (ProgressState.TOKENIZING, 40),
            (ProgressState.DETECTING_PHRASES, 60),
            (ProgressState.MATCHING_LEVELS, 80),
            (ProgressState.GENERATING_STATS, 95),
            (ProgressState.COMPLETED, 100),
        ]

        for state, expected_percentage in test_cases:
            assert state.value == expected_percentage, f"{state.name} should map to {expected_percentage}%"

    def test_sse_event_formatting(self):
        """Test SSE event string formatting."""
        uploaded_file = UploadedFile(
            filename="test.txt",
            file_path="/tmp/test.txt",
            file_type=".txt",
            size_bytes=1024
        )

        session = UploadSession(
            session_id=uuid4(),
            uploaded_file=uploaded_file,
            status=SessionStatus.DETECTING_PHRASES,
            progress_percentage=60
        )

        event = ProgressTracker.format_progress_event(session)

        # Verify proper SSE format (must end with \n\n)
        assert event.endswith('\n\n')

        # Verify event type line
        lines = event.split('\n')
        assert lines[0] == 'event: progress'

        # Verify data line is valid JSON
        data_line = lines[1]
        assert data_line.startswith('data: ')
        json_str = data_line[6:]
        data = json.loads(json_str)  # Should not raise

        # Verify required fields
        assert all(key in data for key in ['session_id', 'status', 'progress', 'stage'])

    def test_progress_event_includes_stage_name(self):
        """Test that progress events include human-readable stage name."""
        uploaded_file = UploadedFile(
            filename="test.txt",
            file_path="/tmp/test.txt",
            file_type=".txt",
            size_bytes=1024
        )

        session = UploadSession(
            session_id=uuid4(),
            uploaded_file=uploaded_file,
            status=SessionStatus.MATCHING_LEVELS,
            progress_percentage=80
        )

        event = ProgressTracker.format_progress_event(session)

        # Parse and verify stage field
        lines = event.split('\n')
        data_line = [line for line in lines if line.startswith('data: ')][0]
        data = json.loads(data_line[6:])

        assert 'stage' in data
        assert data['stage'] == 'MATCHING_LEVELS'
