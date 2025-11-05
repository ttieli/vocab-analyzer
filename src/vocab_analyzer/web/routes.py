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
from .history import get_history_manager

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


@web_bp.route('/analyze-text', methods=['POST'])
def analyze_text():
    """Handle text input and initiate analysis.

    Request Body:
        text: Raw text content to analyze (required)
        source_name: Optional name for the text source (default: "pasted_text")

    Returns:
        JSON response with session ID and source name, or error message
    """
    # Get JSON data
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "NO_DATA",
            "message": "No JSON data provided"
        }), 400

    # Get text content
    text = data.get('text', '').strip()

    if not text:
        return jsonify({
            "error": "NO_TEXT",
            "message": "No text content provided"
        }), 400

    # Check text length (max 1MB of text = ~1,000,000 chars)
    if len(text) > 1_000_000:
        return jsonify({
            "error": "TEXT_TOO_LONG",
            "message": "Text content exceeds 1,000,000 characters"
        }), 400

    # Get source name
    source_name = data.get('source_name', 'pasted_text')

    # Save text to temporary file
    import tempfile
    temp_file = tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.txt',
        delete=False,
        encoding='utf-8'
    )
    temp_file.write(text)
    temp_file.close()

    file_path = Path(temp_file.name)

    # Create uploaded file object
    uploaded_file = UploadedFile(
        filename=source_name,
        file_path=file_path,
        file_type='.txt',
        size_bytes=len(text.encode('utf-8'))
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
        "source_name": source_name,
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

        # Save analysis to history
        try:
            history_manager = get_history_manager()
            history_manager.save_analysis(result, session.uploaded_file.filename)
            current_app.logger.info(f"Saved analysis to history for file: {session.uploaded_file.filename}")
        except Exception as e:
            # Log error but don't fail the analysis if history save fails
            current_app.logger.error(f"Failed to save analysis to history: {e}")

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


@web_bp.route('/api/ui/strings', methods=['GET'])
def get_ui_strings():
    """Get bilingual UI strings.

    Query Parameters:
        category: Optional filter by category (navigation, buttons, labels, errors, loading)

    Returns:
        JSON response with bilingual UI strings
    """
    try:
        from ..translation.strings import BilingualStringLoader

        loader = BilingualStringLoader()
        category = request.args.get('category')

        if category:
            strings = loader.get_strings_by_category(category)
        else:
            strings = loader.get_all_strings()

        return jsonify({
            "version": "1.0",
            "category": category if category else "all",
            "strings": strings
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error loading UI strings: {e}")
        return jsonify({
            "error": "STRINGS_LOAD_ERROR",
            "message": "Failed to load UI strings"
        }), 500


@web_bp.route('/api/cefr', methods=['GET'])
def get_all_cefr_levels():
    """Get all CEFR level descriptions.

    Returns:
        JSON response with all CEFR level definitions
    """
    try:
        from ..translation.config import CEFRDefinitionLoader

        loader = CEFRDefinitionLoader()
        cefr_data = loader.get_all_levels()

        return jsonify(cefr_data), 200

    except Exception as e:
        current_app.logger.error(f"Error loading CEFR definitions: {e}")
        return jsonify({
            "success": False,
            "error": "Failed to load CEFR definitions",
            "error_cn": "无法加载 CEFR 定义",
            "code": "CEFR_LOAD_ERROR"
        }), 500


@web_bp.route('/api/cefr/<level>', methods=['GET'])
def get_cefr_level(level: str):
    """Get CEFR level description by level code.

    Args:
        level: CEFR level code (A1, A2, B1, B2, C1, C2, C2+)

    Returns:
        JSON response with CEFR level definition or error
    """
    try:
        from ..translation.config import CEFRDefinitionLoader

        loader = CEFRDefinitionLoader()
        level_data = loader.get_level(level.upper())

        if not level_data:
            return jsonify({
                "success": False,
                "error": "CEFR level not found",
                "error_cn": "未找到 CEFR 级别",
                "code": "LEVEL_NOT_FOUND"
            }), 404

        return jsonify(level_data), 200

    except Exception as e:
        current_app.logger.error(f"Error loading CEFR level {level}: {e}")
        return jsonify({
            "success": False,
            "error": "Failed to load CEFR level",
            "error_cn": "无法加载 CEFR 级别",
            "code": "CEFR_LOAD_ERROR"
        }), 500


@web_bp.route('/api/translate', methods=['POST'])
def translate_text():
    """Translate English text to Chinese using fallback chain.

    Request Body:
        source_text: English text to translate (required)
        translation_type: Type of content (word, phrase, sentence) (required)
        user_context: Optional context hint

    Returns:
        JSON response with translation or error
    """
    try:
        # Get request data
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data provided",
                "error_cn": "未提供 JSON 数据",
                "code": "NO_DATA"
            }), 400

        source_text = data.get('source_text', '').strip()
        translation_type = data.get('translation_type', 'word')

        # Validate required fields
        if not source_text:
            return jsonify({
                "success": False,
                "error": "source_text cannot be empty",
                "error_cn": "源文本不能为空",
                "code": "EMPTY_TEXT"
            }), 400

        # Type-specific character limits (matching translator.py)
        max_lengths = {
            'word': 100,
            'phrase': 200,
            'sentence': 2000
        }
        max_length = max_lengths.get(translation_type, 500)

        if len(source_text) > max_length:
            return jsonify({
                "success": False,
                "error": f"source_text exceeds {max_length} characters for {translation_type}",
                "error_cn": f"源文本超过 {max_length} 字符（{translation_type}类型）",
                "code": "TEXT_TOO_LONG"
            }), 400

        if translation_type not in ['word', 'phrase', 'sentence']:
            return jsonify({
                "success": False,
                "error": "translation_type must be one of: word, phrase, sentence",
                "error_cn": "翻译类型必须是以下之一: word, phrase, sentence",
                "code": "INVALID_TYPE"
            }), 400

        # Perform translation
        from ..translation.fallback import TranslationChain

        chain = TranslationChain()
        result = chain.translate(
            text=source_text,
            translation_type=translation_type
        )

        # Check if translation was successful
        if not result.is_success():
            return jsonify({
                "success": False,
                "error": result.error or "Translation failed",
                "error_cn": "翻译失败",
                "code": "TRANSLATION_FAILED"
            }), 500

        # Convert TranslationResult to dict for JSON response
        import time
        response = {
            "success": True,
            "translation": result.target_text,
            "source": result.source,
            "cached": result.source == "cached",
            "confidence_score": result.confidence_score,
            "timestamp": int(time.time())
        }

        return jsonify(response), 200

    except Exception as e:
        current_app.logger.error(f"Translation error: {e}")
        return jsonify({
            "success": False,
            "error": "Translation failed",
            "error_cn": "翻译失败",
            "code": "TRANSLATION_FAILED"
        }), 500


@web_bp.route('/api/history', methods=['GET'])
def get_history():
    """Get all analysis history entries.

    Returns:
        JSON response with list of all history entries (metadata only)
    """
    try:
        history_manager = get_history_manager()
        entries = history_manager.get_all_entries()

        return jsonify({
            "success": True,
            "count": len(entries),
            "entries": entries
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error retrieving history: {e}")
        return jsonify({
            "success": False,
            "error": "Failed to retrieve history",
            "error_cn": "无法获取历史记录",
            "code": "HISTORY_LOAD_ERROR"
        }), 500


@web_bp.route('/api/history/<int:analysis_id>', methods=['GET'])
def get_history_analysis(analysis_id: int):
    """Get a specific analysis from history.

    Args:
        analysis_id: ID of the analysis to retrieve

    Returns:
        JSON response with full analysis data or error
    """
    try:
        history_manager = get_history_manager()
        analysis = history_manager.get_analysis(analysis_id)

        if not analysis:
            return jsonify({
                "success": False,
                "error": "Analysis not found",
                "error_cn": "未找到分析记录",
                "code": "ANALYSIS_NOT_FOUND"
            }), 404

        return jsonify({
            "success": True,
            "analysis": analysis
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error retrieving analysis {analysis_id}: {e}")
        return jsonify({
            "success": False,
            "error": "Failed to retrieve analysis",
            "error_cn": "无法获取分析记录",
            "code": "ANALYSIS_LOAD_ERROR"
        }), 500


@web_bp.route('/api/history/<int:analysis_id>', methods=['DELETE'])
def delete_history_analysis(analysis_id: int):
    """Delete a specific analysis from history.

    Args:
        analysis_id: ID of the analysis to delete

    Returns:
        JSON response with success status or error
    """
    try:
        history_manager = get_history_manager()
        success = history_manager.delete_analysis(analysis_id)

        if not success:
            return jsonify({
                "success": False,
                "error": "Analysis not found",
                "error_cn": "未找到分析记录",
                "code": "ANALYSIS_NOT_FOUND"
            }), 404

        return jsonify({
            "success": True,
            "message": "Analysis deleted successfully",
            "message_cn": "分析记录已删除"
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error deleting analysis {analysis_id}: {e}")
        return jsonify({
            "success": False,
            "error": "Failed to delete analysis",
            "error_cn": "无法删除分析记录",
            "code": "ANALYSIS_DELETE_ERROR"
        }), 500
