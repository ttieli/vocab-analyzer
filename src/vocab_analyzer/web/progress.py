"""Progress tracking and SSE event formatting for web analysis.

This module provides progress tracking capabilities and Server-Sent Events
(SSE) formatting for real-time progress updates during vocabulary analysis.
"""

from typing import Optional

from .session import ProgressState, UploadSession


class ProgressTracker:
    """Tracks and formats progress updates for SSE streaming."""

    @staticmethod
    def format_progress_event(session: UploadSession) -> str:
        """Format a progress update as an SSE event.

        Args:
            session: Current upload session

        Returns:
            Formatted SSE event string
        """
        data = {
            "session_id": str(session.session_id),
            "status": session.status.value,
            "progress": session.progress_percentage,
            "stage": session.status.name
        }

        # Format as SSE event
        import json
        return f"event: progress\ndata: {json.dumps(data)}\n\n"

    @staticmethod
    def format_complete_event(session: UploadSession) -> str:
        """Format a completion event as an SSE event.

        Args:
            session: Completed upload session

        Returns:
            Formatted SSE completion event string
        """
        data = {
            "session_id": str(session.session_id),
            "status": "completed",
            "progress": 100
        }

        import json
        return f"event: complete\ndata: {json.dumps(data)}\n\n"

    @staticmethod
    def format_error_event(session: UploadSession) -> str:
        """Format an error event as an SSE event.

        Args:
            session: Failed upload session

        Returns:
            Formatted SSE error event string
        """
        error_data = {
            "session_id": str(session.session_id),
            "status": "failed",
            "error": {
                "code": session.error.code if session.error else "UNKNOWN",
                "message": session.error.message if session.error else "Unknown error",
                "details": session.error.details if session.error else None
            }
        }

        import json
        return f"event: error\ndata: {json.dumps(error_data)}\n\n"

    @staticmethod
    def update_and_format(session: UploadSession, state: ProgressState) -> str:
        """Update session progress and format as SSE event.

        Args:
            session: Upload session to update
            state: New progress state

        Returns:
            Formatted SSE progress event string
        """
        session.update_progress(state)
        return ProgressTracker.format_progress_event(session)
