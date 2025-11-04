"""HTTP route handlers for the web interface.

This module defines the Flask blueprint and route handlers for
file upload, analysis, progress tracking, and result download.
"""

import os
import threading
from pathlib import Path
from uuid import UUID

from flask import Blueprint, Response, current_app, jsonify, request, send_file, stream_with_context
from werkzeug.utils import secure_filename

from .progress import ProgressState, ProgressTracker
from .session import ErrorInfo, SessionStatus, UploadedFile, create_session, get_session

# Create blueprint for web routes
web_bp = Blueprint('web', __name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'.txt', '.pdf', '.docx'}


@web_bp.route('/', methods=['GET'])
def index():
    """Serve the main web interface.

    Returns:
        HTML page for the web interface
    """
    return send_file(
        Path(__file__).parent / 'static' / 'index.html',
        mimetype='text/html'
    )


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed.

    Args:
        filename: Name of the uploaded file

    Returns:
        True if file type is allowed, False otherwise
    """
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


@web_bp.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and initiate analysis.

    Returns:
        JSON response with session ID and filename, or error message
    """
    # Check if file is present
    if 'file' not in request.files:
        return jsonify({
            "error": "NO_FILE",
            "message": "No file provided in the request"
        }), 400

    file = request.files['file']

    # Check if filename is empty
    if file.filename == '':
        return jsonify({
            "error": "NO_FILE",
            "message": "No file selected"
        }), 400

    # Validate file type
    if not allowed_file(file.filename):
        return jsonify({
            "error": "INVALID_FILE_TYPE",
            "message": f"File type not supported. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        }), 400

    # Save file securely
    filename = secure_filename(file.filename)
    upload_folder = Path(current_app.config['UPLOAD_FOLDER'])
    upload_folder.mkdir(parents=True, exist_ok=True)

    file_path = upload_folder / filename
    file.save(str(file_path))

    # Get file size
    file_size = file_path.stat().st_size

    # Create uploaded file object
    uploaded_file = UploadedFile(
        filename=filename,
        file_path=file_path,
        file_type=file_path.suffix.lower(),
        size_bytes=file_size
    )

    # Create session
    session = create_session(uploaded_file)

    # Start analysis in background thread
    thread = threading.Thread(
        target=analyze_file_background,
        args=(session.session_id,)
    )
    thread.daemon = True
    thread.start()

    return jsonify({
        "session_id": str(session.session_id),
        "filename": filename,
        "status": "processing"
    }), 200


@web_bp.route('/progress/<session_id>', methods=['GET'])
def progress_stream(session_id: str):
    """Stream real-time progress updates via Server-Sent Events.

    Args:
        session_id: UUID string of the session

    Returns:
        SSE stream with progress/complete/error events
    """
    try:
        # Parse session ID
        session_uuid = UUID(session_id)
    except ValueError:
        return jsonify({
            "error": "INVALID_SESSION_ID",
            "message": "Invalid session ID format"
        }), 400

    # Get session
    session = get_session(session_uuid)
    if not session:
        return jsonify({
            "error": "SESSION_NOT_FOUND",
            "message": "Session not found or has expired"
        }), 404

    def generate():
        """Generate SSE events for progress updates."""
        import time

        # Keep streaming while analysis is in progress
        while True:
            session = get_session(session_uuid)

            if not session:
                # Session expired or deleted
                yield ProgressTracker.format_error_event(session or create_mock_error_session())
                break

            # Send current progress
            if session.status == SessionStatus.COMPLETED:
                yield ProgressTracker.format_complete_event(session)
                break
            elif session.status == SessionStatus.FAILED:
                yield ProgressTracker.format_error_event(session)
                break
            else:
                yield ProgressTracker.format_progress_event(session)

            # Wait before next update
            time.sleep(0.5)

    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        }
    )


def create_mock_error_session():
    """Create a mock session for error reporting when session is not found."""
    from uuid import uuid4
    from pathlib import Path

    uploaded_file = UploadedFile(
        filename="unknown",
        file_path=Path("/tmp/unknown"),
        file_type=".txt",
        size_bytes=0
    )

    error = ErrorInfo(
        code="SESSION_EXPIRED",
        message="Session not found or has expired",
        details="The analysis session may have been cleaned up"
    )

    session = create_session(uploaded_file)
    session.mark_failed(error)
    return session


def analyze_file_background(session_id: UUID):
    """Analyze uploaded file in background thread.

    Args:
        session_id: UUID of the session to process
    """
    session = get_session(session_id)
    if not session:
        return

    try:
        # Import analyzer (done here to avoid circular imports)
        from ..core.analyzer import VocabularyAnalyzer
        import time

        # Update progress: Validating (5%)
        session.update_progress(ProgressState.VALIDATING)
        time.sleep(0.2)  # Small delay for UI to register

        # Create analyzer
        analyzer = VocabularyAnalyzer()

        # Update progress: Extracting (15%)
        session.update_progress(ProgressState.EXTRACTING)
        time.sleep(0.2)

        # Analyze file - this is the main work
        # The analyzer does: extraction, tokenization, phrase detection, level matching, stats
        # We'll update progress as we go

        # Update progress: Tokenizing (40%)
        session.update_progress(ProgressState.TOKENIZING)

        # Perform actual analysis
        result = analyzer.analyze(str(session.uploaded_file.file_path))

        # Update progress: Detecting phrases (60%)
        session.update_progress(ProgressState.DETECTING_PHRASES)
        time.sleep(0.1)

        # Update progress: Matching levels (80%)
        session.update_progress(ProgressState.MATCHING_LEVELS)
        time.sleep(0.1)

        # Update progress: Generating stats (95%)
        session.update_progress(ProgressState.GENERATING_STATS)
        time.sleep(0.1)

        # Convert result to dictionary for JSON serialization
        # For now, store the result object directly
        # We'll serialize it when downloading
        session.mark_completed(result)

    except Exception as e:
        error = ErrorInfo(
            code="ANALYSIS_ERROR",
            message=str(e),
            details=f"Error analyzing file: {session.uploaded_file.filename}"
        )
        session.mark_failed(error)


@web_bp.route('/download/<session_id>/<format>', methods=['GET'])
def download_result(session_id: str, format: str):
    """Download analysis results in specified format.

    Args:
        session_id: UUID string of the session
        format: Export format (json, csv, markdown)

    Returns:
        File download response or error JSON
    """
    try:
        # Parse session ID
        session_uuid = UUID(session_id)
    except ValueError:
        return jsonify({
            "error": "INVALID_SESSION_ID",
            "message": "Invalid session ID format"
        }), 400

    # Get session
    session = get_session(session_uuid)
    if not session:
        return jsonify({
            "error": "SESSION_NOT_FOUND",
            "message": "Session not found or has expired"
        }), 404

    # Check if analysis is complete
    if session.status != SessionStatus.COMPLETED:
        if session.status == SessionStatus.FAILED:
            return jsonify({
                "error": "ANALYSIS_FAILED",
                "message": session.error.message if session.error else "Analysis failed"
            }), 500
        else:
            return jsonify({
                "error": "ANALYSIS_PENDING",
                "message": f"Analysis is still in progress ({session.status.value})"
            }), 202

    # Get result
    result = session.result
    if not result:
        return jsonify({
            "error": "NO_RESULT",
            "message": "No analysis result available"
        }), 500

    # Export based on format
    try:
        # Import exporters
        from ..exporters import CsvExporter, JsonExporter, MarkdownExporter

        # Create temporary export file
        import tempfile
        export_file = tempfile.NamedTemporaryFile(
            mode='w',
            delete=False,
            suffix=f'.{format}'
        )
        export_path = export_file.name
        export_file.close()

        # Export using appropriate exporter
        if format == 'json':
            exporter = JsonExporter()
            exporter.export(result, export_path, include_words=True, include_phrases=True)
            mimetype = 'application/json'
            download_name = f'{session.uploaded_file.filename}.json'

        elif format == 'csv':
            exporter = CsvExporter()
            exporter.export(result, export_path, include_examples=False)
            mimetype = 'text/csv'
            download_name = f'{session.uploaded_file.filename}.csv'

        elif format in ['markdown', 'md']:
            exporter = MarkdownExporter()
            exporter.export(result, export_path, include_examples=False)
            mimetype = 'text/markdown'
            download_name = f'{session.uploaded_file.filename}.md'

        else:
            return jsonify({
                "error": "INVALID_FORMAT",
                "message": f"Invalid export format: {format}. Supported: json, csv, markdown"
            }), 400

        # Send file
        return send_file(
            export_path,
            mimetype=mimetype,
            as_attachment=True,
            download_name=download_name
        )

    except Exception as e:
        return jsonify({
            "error": "EXPORT_ERROR",
            "message": f"Error exporting results: {str(e)}"
        }), 500
