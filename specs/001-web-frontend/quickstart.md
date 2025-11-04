# Quick Start: Web Frontend Implementation

**Feature**: Web Frontend for Vocabulary Analyzer
**Date**: 2025-11-04
**For**: Developers implementing this feature

## Overview

This guide provides a quick reference for implementing the web frontend feature. It outlines the **minimal steps** needed to build a functional web interface following the research and design specifications.

## Prerequisites

Before starting implementation:

1. **Existing codebase working**: Ensure CLI tool runs successfully
2. **Python 3.10+**: Confirm Python version
3. **Virtual environment active**: `source venv/bin/activate`
4. **All dependencies installed**: `pip install -r requirements.txt`

Verify with:
```bash
vocab-analyzer --version  # Should work
vocab-analyzer analyze data/sample_books/sample.txt  # Should work
```

## Implementation Checklist

### Phase 1: Setup (30 minutes)

- [ ] Install Flask: `pip install Flask>=3.0.0`
- [ ] Update `requirements.txt` with Flask
- [ ] Install dev dependency: `pip install pytest-flask>=1.3.0`
- [ ] Update `requirements-dev.txt` with pytest-flask
- [ ] Create directory structure:
  ```bash
  mkdir -p src/vocab_analyzer/web/static
  mkdir -p src/vocab_analyzer/web/templates
  mkdir -p tests/web
  ```

### Phase 2: Backend Core (2-3 hours)

**Files to create** (in order):

1. **`src/vocab_analyzer/web/__init__.py`**
   - Empty or simple imports

2. **`src/vocab_analyzer/web/session.py`** (~100 lines)
   - Implement data models from `data-model.md`:
     - `UploadSession`
     - `UploadedFile`
     - `ProgressState`
     - `ErrorInfo`
     - Supporting enums (SessionStatus, ProcessingStage, FileType)
   - In-memory session storage: `sessions: Dict[str, UploadSession] = {}`
   - Helper: `cleanup_expired_sessions()` function

3. **`src/vocab_analyzer/web/progress.py`** (~50 lines)
   - `ProgressTracker` class
   - Methods:
     - `update_stage(session_id, stage, percentage, message)`
     - `get_current_progress(session_id)`
   - SSE event formatting helper

4. **`src/vocab_analyzer/web/routes.py`** (~150 lines)
   - Import existing: `from vocab_analyzer.core.analyzer import VocabularyAnalyzer`
   - Routes (refer to `contracts/web-api.yaml`):
     - `GET /` → serve static/index.html
     - `POST /upload` → handle file upload, create session, start analysis
     - `GET /progress/<session_id>` → SSE stream
     - `GET /download/<session_id>/<format>` → return analysis file
   - Use existing exporters:
     ```python
     from vocab_analyzer.exporters.json_exporter import JsonExporter
     from vocab_analyzer.exporters.csv_exporter import CsvExporter
     from vocab_analyzer.exporters.markdown_exporter import MarkdownExporter
     ```

5. **`src/vocab_analyzer/web/app.py`** (~50 lines)
   - Flask app factory pattern:
     ```python
     def create_app(config=None):
         app = Flask(__name__, static_folder='static')
         app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
         # Register routes...
         return app
     ```
   - Cleanup scheduler (simple background thread or before_request hook)
   - Error handlers for 400, 404, 413, 500

**Key Integration Points**:

```python
# In routes.py - Upload handler
analyzer = VocabularyAnalyzer()  # Reuse existing facade
result = analyzer.analyze(temp_file_path)  # Returns VocabularyAnalysis

# Update progress during analysis (intercept stages):
# Option 1: Monkey-patch progress callbacks
# Option 2: Add optional progress_callback param to analyzer (modify core - AVOID)
# Option 3: Estimate progress based on stage completion (SIMPLEST)

# Stage estimation (no core changes):
progress_map = {
    "extraction_complete": 15,
    "tokenization_complete": 40,
    "phrase_detection_complete": 60,
    "level_matching_complete": 80,
    "statistics_complete": 95,
}
```

### Phase 3: Frontend (2-3 hours)

**Files to create**:

1. **`src/vocab_analyzer/web/static/index.html`** (~200 lines)
   - Single page with 3 sections:
     - Upload form (hidden after upload)
     - Progress display (hidden until upload)
     - Results display (hidden until complete)
   - Use semantic HTML5, accessible forms
   - Example structure:
     ```html
     <div id="upload-section">
       <form id="upload-form">
         <input type="file" accept=".txt,.pdf,.docx" required>
         <button type="submit">Analyze</button>
       </form>
     </div>
     <div id="progress-section" hidden>
       <progress id="progress-bar" max="100"></progress>
       <p id="progress-message"></p>
     </div>
     <div id="results-section" hidden>
       <div id="statistics"></div>
       <div id="download-buttons"></div>
     </div>
     ```

2. **`src/vocab_analyzer/web/static/styles.css`** (~100 lines)
   - Clean, minimal styling
   - Responsive layout (flexbox/grid)
   - Progress bar styling
   - Download button styles
   - No frameworks - plain CSS

3. **`src/vocab_analyzer/web/static/app.js`** (~150 lines)
   - Vanilla JavaScript (ES6+)
   - Key functions:
     ```javascript
     // Upload handler
     async function uploadFile(file) {
       const formData = new FormData();
       formData.append('file', file);
       const response = await fetch('/upload', {
         method: 'POST',
         body: formData
       });
       const data = await response.json();
       startProgressTracking(data.session_id);
     }

     // SSE progress tracking
     function startProgressTracking(sessionId) {
       const eventSource = new EventSource(`/progress/${sessionId}`);
       eventSource.addEventListener('progress', (e) => {
         const data = JSON.parse(e.data);
         updateProgressBar(data.percentage);
       });
       eventSource.addEventListener('complete', (e) => {
         const data = JSON.parse(e.data);
         showResults(data);
         eventSource.close();
       });
       eventSource.addEventListener('error', (e) => {
         handleError(JSON.parse(e.data));
         eventSource.close();
       });
     }

     // Show download options
     function showResults(data) {
       // Display statistics
       // Show download buttons for JSON/CSV/Markdown
     }
     ```

### Phase 4: Testing (2-3 hours)

**Test files to create**:

1. **`tests/web/conftest.py`**
   - Pytest fixtures:
     ```python
     @pytest.fixture
     def client():
         app = create_app({'TESTING': True})
         return app.test_client()

     @pytest.fixture
     def sample_txt_file():
         return (io.BytesIO(b"Sample text"), "test.txt")
     ```

2. **`tests/web/test_routes.py`** (~100 lines)
   - Test each endpoint:
     ```python
     def test_upload_valid_file(client, sample_txt_file):
         response = client.post('/upload', data={'file': sample_txt_file})
         assert response.status_code == 200
         data = response.get_json()
         assert 'session_id' in data

     def test_upload_no_file(client):
         response = client.post('/upload')
         assert response.status_code == 400

     def test_progress_stream(client, sample_txt_file):
         # Upload, get session_id, then test SSE stream
         ...

     def test_download_json(client):
         # Complete upload → analysis → download
         ...
     ```

3. **`tests/web/test_integration.py`** (~50 lines)
   - End-to-end test:
     ```python
     def test_full_workflow(client):
         # Upload → Progress → Download → Verify content
         ...
     ```

4. **Run tests**:
   ```bash
   pytest tests/web/ -v --cov=vocab_analyzer.web
   # Target: 100% coverage for web module
   ```

### Phase 5: CLI Integration (30 minutes)

1. **Add web command to CLI**:

   Edit `src/vocab_analyzer/cli/main.py`:
   ```python
   @click.command()
   @click.option('--port', default=5000, help='Port to run web server')
   @click.option('--host', default='127.0.0.1', help='Host to bind to')
   @click.option('--debug', is_flag=True, help='Enable debug mode')
   def web(port, host, debug):
       """Launch web interface for vocabulary analysis."""
       from vocab_analyzer.web.app import create_app
       app = create_app()
       click.echo(f"Starting web interface at http://{host}:{port}")
       app.run(host=host, port=port, debug=debug)

   cli.add_command(web)
   ```

2. **Test CLI command**:
   ```bash
   vocab-analyzer web --debug
   # Visit http://127.0.0.1:5000
   ```

### Phase 6: Documentation (1 hour)

1. **Update main README.md**:
   - Add "Web Interface" section
   - Include screenshot (optional)
   - Basic usage instructions

2. **Create `docs/web_interface.md`**:
   - Detailed usage guide
   - Troubleshooting
   - Browser requirements
   - FAQ

## Development Workflow

### Running the Web Interface

**Development Mode**:
```bash
vocab-analyzer web --debug
# Auto-reload enabled, detailed error pages
```

**Production Mode** (for testing production config):
```bash
pip install gunicorn  # Or waitress on Windows
gunicorn -w 4 -b 127.0.0.1:8000 vocab_analyzer.web.app:app
```

### Testing Workflow

```bash
# Unit tests only
pytest tests/web/test_routes.py -v

# Integration tests
pytest tests/web/ -v

# With coverage
pytest tests/web/ --cov=vocab_analyzer.web --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Code Quality Checks

```bash
# Format code
black src/vocab_analyzer/web/
isort src/vocab_analyzer/web/

# Lint
pylint src/vocab_analyzer/web/ --rcfile=.pylintrc
flake8 src/vocab_analyzer/web/

# Type check
mypy src/vocab_analyzer/web/
```

## Troubleshooting

### Issue: Import errors when running web command

**Solution**: Ensure package is installed in editable mode:
```bash
pip install -e .
```

### Issue: Flask not found

**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

### Issue: SSE not working in browser

**Solution**: Check browser console for errors. Ensure:
- `Content-Type: text/event-stream` header set
- Trailing newline after each SSE message
- EventSource API supported (all modern browsers)

### Issue: File upload fails immediately

**Solution**: Check:
- File size limit (50MB)
- File type (TXT/PDF/DOCX only)
- Browser console for error messages
- Server logs for detailed error

### Issue: Progress stuck at certain percentage

**Solution**: Check server logs. Likely:
- Analysis error (check temp file permissions)
- spaCy model not loaded (`python -m spacy download en_core_web_sm`)
- Insufficient memory for large files

## Next Steps

After completing implementation:

1. **Manual Testing**:
   - Test with all three file types (TXT, PDF, DOCX)
   - Test with small, medium, and large files
   - Test error cases (invalid files, too large, corrupted)
   - Test on multiple browsers

2. **Code Review**:
   - Self-review against constitution principles
   - Check compliance with `specs/001-web-frontend/plan.md`
   - Verify no changes to existing core modules

3. **Documentation**:
   - Add docstrings to all functions
   - Update README with web interface instructions
   - Create user guide in docs/

4. **Prepare for PR**:
   - Run full test suite: `pytest`
   - Check coverage: `pytest --cov`
   - Run linters: `black`, `isort`, `pylint`, `flake8`
   - Commit with clear message

5. **Ready for `/speckit.tasks`**:
   - Once plan is validated, run `/speckit.tasks` to generate detailed task breakdown
   - Tasks will reference this quickstart for implementation steps

## Key Principles

Throughout implementation, remember:

1. **Reuse over reinvent**: Never duplicate analyzer logic; always import and call existing functions
2. **Simplicity first**: Resist urge to add features not in spec
3. **Type safety**: All functions must have type annotations
4. **Test coverage**: Aim for 100% on new code
5. **No core changes**: Existing modules remain untouched

## Estimated Timeline

**Total**: 10-12 hours for solo developer

- Setup: 0.5 hours
- Backend: 3 hours
- Frontend: 3 hours
- Testing: 2-3 hours
- CLI integration: 0.5 hours
- Documentation: 1-2 hours
- Testing and polish: 1-2 hours

**Checkpoints**:
- ✅ 4 hours: Backend routes working (can upload, get session)
- ✅ 7 hours: Frontend working (can analyze, see progress)
- ✅ 10 hours: Tests passing, documentation complete
- ✅ 12 hours: Code review done, ready for PR

## Support

If stuck, refer to:
- `research.md`: Technology choices and rationale
- `data-model.md`: Data structures and validation rules
- `contracts/web-api.yaml`: API specification with examples
- Existing code: CLI implementation in `src/vocab_analyzer/cli/`

Questions? Check the feature spec and constitution for guidance on trade-offs.
