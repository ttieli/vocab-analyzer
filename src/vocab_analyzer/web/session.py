"""Session management for web uploads and analysis.

This module provides data models and management for upload sessions,
tracking file uploads, progress states, and analysis results.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Optional
from uuid import UUID, uuid4


class SessionStatus(Enum):
    """Status of an upload session."""

    PENDING = "pending"
    VALIDATING = "validating"
    EXTRACTING = "extracting"
    TOKENIZING = "tokenizing"
    DETECTING_PHRASES = "detecting_phrases"
    MATCHING_LEVELS = "matching_levels"
    GENERATING_STATS = "generating_stats"
    COMPLETED = "completed"
    FAILED = "failed"


class ProgressState(Enum):
    """Progress states with their percentage mappings."""

    VALIDATING = 5
    EXTRACTING = 15
    TOKENIZING = 40
    DETECTING_PHRASES = 60
    MATCHING_LEVELS = 80
    GENERATING_STATS = 95
    COMPLETED = 100


@dataclass
class ErrorInfo:
    """Information about an error that occurred during processing."""

    code: str
    message: str
    details: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class UploadedFile:
    """Represents an uploaded book file."""

    filename: str
    file_path: Path
    file_type: str
    size_bytes: int
    upload_timestamp: datetime = field(default_factory=datetime.utcnow)

    def cleanup(self) -> None:
        """Remove the temporary uploaded file."""
        if self.file_path.exists():
            self.file_path.unlink()


@dataclass
class UploadSession:
    """Represents a single analysis session for an uploaded file."""

    session_id: UUID
    uploaded_file: UploadedFile
    status: SessionStatus
    progress_percentage: int = 0
    result: Optional[dict] = None
    error: Optional[ErrorInfo] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: datetime = field(default_factory=lambda: datetime.utcnow() + timedelta(hours=1))

    def update_progress(self, state: ProgressState) -> None:
        """Update session progress based on processing state.

        Args:
            state: Current processing state
        """
        self.progress_percentage = state.value
        self.status = SessionStatus[state.name]

    def mark_completed(self, result: dict) -> None:
        """Mark session as completed with analysis results.

        Args:
            result: Vocabulary analysis results dictionary
        """
        self.status = SessionStatus.COMPLETED
        self.progress_percentage = 100
        self.result = result

    def mark_failed(self, error: ErrorInfo) -> None:
        """Mark session as failed with error information.

        Args:
            error: Error information describing the failure
        """
        self.status = SessionStatus.FAILED
        self.error = error

    def is_expired(self) -> bool:
        """Check if the session has expired.

        Returns:
            True if session has expired, False otherwise
        """
        return datetime.utcnow() > self.expires_at

    def cleanup(self) -> None:
        """Clean up session resources including uploaded file."""
        self.uploaded_file.cleanup()


# Global session storage (in-memory dictionary)
# In a production environment, this would be replaced with Redis or similar
_sessions: dict[UUID, UploadSession] = {}


def create_session(uploaded_file: UploadedFile) -> UploadSession:
    """Create a new upload session.

    Args:
        uploaded_file: The uploaded file information

    Returns:
        Newly created upload session
    """
    session = UploadSession(
        session_id=uuid4(),
        uploaded_file=uploaded_file,
        status=SessionStatus.PENDING
    )
    _sessions[session.session_id] = session
    return session


def get_session(session_id: UUID) -> Optional[UploadSession]:
    """Retrieve a session by ID.

    Args:
        session_id: UUID of the session to retrieve

    Returns:
        Upload session if found, None otherwise
    """
    return _sessions.get(session_id)


def cleanup_expired_sessions() -> int:
    """Remove all expired sessions and clean up their resources.

    Returns:
        Number of sessions cleaned up
    """
    expired_ids = [
        sid for sid, session in _sessions.items()
        if session.is_expired()
    ]

    for session_id in expired_ids:
        session = _sessions.pop(session_id)
        session.cleanup()

    return len(expired_ids)
