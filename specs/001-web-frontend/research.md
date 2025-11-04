# Technical Research: Web Frontend for Vocabulary Analyzer

**Feature**: Web Frontend for Vocabulary Analyzer
**Date**: 2025-11-04
**Status**: Complete

## Research Summary

This document captures the technical decisions and research conducted for implementing a web-based interface for the vocabulary analyzer. Given the requirement "用当前项目框架选择最简方案实现" (use current project framework, choose simplest solution), all research prioritized minimal complexity and maximum reuse of existing code.

## Key Technical Decisions

### 1. Web Framework Selection

**Decision**: Flask 3.0+

**Rationale**:
- **Minimal dependency**: Flask is a micro-framework with zero mandatory dependencies beyond Werkzeug and Jinja2
- **Python ecosystem fit**: Integrates seamlessly with existing Python 3.10+ codebase
- **No build step**: Serves static files directly, no Node.js/npm required
- **Development simplicity**: Built-in dev server, simple routing, minimal boilerplate
- **Production ready**: Can be deployed with Gunicorn/Waitress for production use

**Alternatives Considered**:

1. **FastAPI**
   - **Pros**: Modern, async, automatic OpenAPI docs
   - **Cons**: Overkill for simple upload/download; async complexity unnecessary (existing analyzer is synchronous); ASGI deployment more complex than WSGI
   - **Rejected**: Adds complexity without proportional benefit for this use case

2. **Django**
   - **Pros**: Batteries-included, admin interface, ORM
   - **Cons**: Heavy framework (100+ dependencies); requires models/migrations for features we don't need; violates "simplicity first" principle
   - **Rejected**: Massive overkill for a simple file upload interface

3. **Streamlit/Gradio**
   - **Pros**: Extremely simple for data apps, auto-generates UI from Python code
   - **Cons**: Very opinionated UI (hard to customize); adds 100+ transitive dependencies; designed for data science demos, not production apps
   - **Rejected**: Dependencies violate minimal-dependency principle; insufficient control over UX

### 2. Real-time Progress Updates

**Decision**: Server-Sent Events (SSE)

**Rationale**:
- **Simplicity**: SSE is HTTP-based, uses standard Flask response streaming
- **Browser support**: Native EventSource API in all modern browsers (no library needed)
- **Unidirectional fit**: Server → client progress updates (client doesn't need to send data during analysis)
- **No extra dependencies**: Works with standard Flask, no WebSocket library required
- **Fallback friendly**: Degrades to polling if SSE unavailable

**Alternatives Considered**:

1. **WebSockets**
   - **Pros**: Bidirectional, lower latency
   - **Cons**: Requires additional library (Flask-SocketIO + gevent/eventlet); overkill for one-way progress updates; deployment complexity (sticky sessions, WebSocket proxying)
   - **Rejected**: Bidirectional capability not needed, adds unnecessary complexity

2. **Polling**
   - **Pros**: Extremely simple, works everywhere
   - **Cons**: Higher server load (repeated requests); delayed updates (polling interval); poor user experience for real-time feedback
   - **Rejected**: Inferior UX compared to SSE, which is equally simple

3. **Long Polling**
   - **Pros**: Better than polling, widely compatible
   - **Cons**: More complex than SSE; requires timeout handling and reconnection logic; still higher overhead than SSE
   - **Rejected**: SSE is simpler and more efficient for this use case

### 3. Frontend Technology

**Decision**: Vanilla JavaScript (ES6+) with no framework

**Rationale**:
- **Zero build step**: No webpack, Vite, or bundler required
- **Minimal dependencies**: No npm packages, no node_modules directory
- **Browser native APIs**: Fetch API, EventSource (SSE), FormData - all built-in
- **Maintainability**: Simple, readable code; no framework version churn
- **Fast load time**: <10KB total JavaScript (single file), instant page load

**Alternatives Considered**:

1. **React/Vue/Svelte**
   - **Pros**: Component model, reactive state, large ecosystems
   - **Cons**: Requires Node.js build tooling; 100+ npm packages; overkill for 3 UI states (upload form, progress bar, results view); violates simplicity principle
   - **Rejected**: Massive complexity for a simple single-page interface

2. **Alpine.js/htmx**
   - **Pros**: Lightweight, no build step, declarative syntax
   - **Cons**: Still external dependencies (CDN or vendored); learning curve for syntax; vanilla JS is simpler for this scope
   - **Rejected**: Vanilla JS is sufficient and has zero dependencies

3. **jQuery**
   - **Pros**: Familiar, simplifies DOM manipulation
   - **Cons**: Outdated (modern JS has equivalent APIs); 30KB library for features we don't need
   - **Rejected**: Modern browser APIs (fetch, querySelector, addEventListener) cover all needs

### 4. Session Management

**Decision**: Flask session cookies with temporary file storage

**Rationale**:
- **Stateless design**: Each upload gets unique session ID, no server-side state persistence
- **Auto-cleanup**: Temporary files deleted after analysis or on error (using `tempfile.mkdtemp()`)
- **Security**: Uses Werkzeug's `secure_filename()` to prevent path traversal
- **Scalability**: No shared state between requests (can scale horizontally if needed)

**Alternatives Considered**:

1. **Database storage (SQLite/PostgreSQL)**
   - **Pros**: Persistent job tracking, can query history
   - **Cons**: Adds database dependency; requires schema migrations; violates "no persistence" privacy principle from constitution
   - **Rejected**: Unnecessary persistence; constitution requires local-only processing

2. **In-memory queue (Redis/RQ)**
   - **Pros**: Better for background job processing
   - **Cons**: Adds Redis dependency; overkill for single-user sessions; requires additional deployment infrastructure
   - **Rejected**: Too complex for the simple "one analysis per session" requirement

3. **Files in user upload directory**
   - **Pros**: Simple, no database
   - **Cons**: Clutters filesystem; requires manual cleanup; security risk if paths not sanitized
   - **Rejected**: `tempfile` module provides safer, automatic cleanup

### 5. File Upload Handling

**Decision**: Flask streaming upload with size limit enforcement

**Rationale**:
- **Memory efficient**: Streams large files (up to 50MB) without loading fully into memory
- **Early validation**: Check size before processing (reject if >50MB)
- **Werkzeug integration**: Built-in `secure_filename()` prevents path traversal
- **Format validation**: Magic number check (file header) confirms actual type vs extension

**Implementation**:
```python
# Size limit enforced in Flask config
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB

# Stream to temp file
with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp:
    file.save(tmp.name)
```

**Alternatives Considered**:

1. **Load entire file into memory**
   - **Pros**: Simpler code
   - **Cons**: 50MB file = 50MB RAM spike; poor scalability; potential DoS vector
   - **Rejected**: Unacceptable for larger files

2. **Chunked upload with JavaScript**
   - **Pros**: Can show upload progress
   - **Cons**: Complex client-side code; requires additional server endpoints; unnecessary for 50MB limit
   - **Rejected**: Flask streaming is simpler and sufficient

### 6. Error Handling Strategy

**Decision**: Structured error responses with user-friendly messages

**Rationale**:
- **User-facing errors**: Clear messages ("File too large", "Unsupported format") not stack traces
- **Developer debugging**: Full stack trace logged server-side with request context
- **HTTP status codes**: Proper codes (400 bad request, 413 payload too large, 500 server error)
- **Graceful degradation**: Partial analysis results returned if possible (e.g., analysis fails at statistics stage, still return words)

**Error Categories**:
1. **Upload errors** (400): Invalid file type, file too large, corrupted file
2. **Processing errors** (500): Extractor failure, NLP processing error, disk space issues
3. **Session errors** (404): Invalid session ID, expired temporary file

**Alternatives Considered**:

1. **Generic error messages**
   - **Pros**: Simpler code
   - **Cons**: Poor UX; users don't know what went wrong
   - **Rejected**: Constitution requires "clear feedback for all user actions"

2. **Client-side validation only**
   - **Pros**: Faster feedback
   - **Cons**: Easily bypassed; server must validate anyway (security)
   - **Rejected**: Server-side validation is mandatory; client-side is enhancement

## Technology Integration

### Dependencies Added

**New Runtime Dependencies**:
```
Flask>=3.0.0
```

**New Development Dependencies**:
```
pytest-flask>=1.3.0  # Flask test client integration
```

**Total Dependency Increase**: 2 packages (Flask + pytest-flask)

**Transitive Dependencies**: ~5 packages (Werkzeug, Jinja2, Click, MarkupSafe, ItsDangerous)

**Impact Analysis**:
- ✅ Minimal: Flask is lightweight compared to alternatives
- ✅ Well-maintained: Flask 3.0 released 2023, active development
- ✅ Python 3.10+ compatible: Matches existing project requirement
- ✅ No conflicts: No overlapping dependencies with existing stack (spaCy, pandas, etc.)

### Performance Considerations

**Expected Performance**:
- **Page load**: <1 second (static files served from package)
- **Upload time**: Network-dependent (~1-2s for 10MB file on local network)
- **Analysis time**: Same as CLI (reuses analyzer completely)
  - Small files (<5 pages): <3 seconds
  - Medium files (20-50 pages): <20 seconds
  - Large files (100+ pages): <60 seconds
- **Download time**: <500ms (results already generated during analysis)

**Optimization Strategies**:
1. **No database queries**: All in-memory/filesystem operations
2. **Streaming responses**: SSE and file downloads use Flask streaming
3. **Cached static files**: Browser caching headers set for CSS/JS (1 hour)
4. **Compression**: Gzip compression for text responses (enabled in production WSGI server)

### Security Measures

**Input Validation**:
1. **File extension whitelist**: Only `.txt`, `.pdf`, `.docx` accepted
2. **Magic number check**: Verify file header matches extension (prevents rename attacks)
3. **Size limit**: Hard 50MB limit enforced at Flask config level
4. **Filename sanitization**: `secure_filename()` removes path traversal characters

**Session Security**:
1. **Secret key**: Flask session cookie signed with secret key (prevent tampering)
2. **Temporary files**: Stored in OS temp directory with restrictive permissions
3. **Auto-cleanup**: Files deleted after 1 hour or on successful completion (whichever first)
4. **No logging of content**: Only filenames and metadata logged, never file contents

**Web Security Headers**:
```python
# Set in Flask response headers
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Content-Security-Policy: default-src 'self'
```

## Testing Strategy

### Test Coverage Plan

**Unit Tests** (`tests/web/test_routes.py`):
- Upload endpoint validation (file type, size, missing file)
- Session creation and cleanup
- Error handling (malformed requests)
- Download endpoint (format selection, missing results)

**Integration Tests** (`tests/web/test_upload.py`):
- End-to-end upload → analyze → download flow
- Progress SSE stream validation
- Concurrent session isolation (multiple users)
- Temporary file cleanup verification

**Contract Tests** (`tests/web/test_sse.py`):
- SSE message format validation
- Progress percentage updates (0% → 100%)
- Error event handling
- Reconnection behavior

**Test Fixtures**:
- Reuse existing `tests/fixtures/` corpus (small/medium/large books)
- Add malformed files: corrupted PDF, renamed .exe → .txt, empty file

**Coverage Target**: 100% for web module (matches critical path requirement from constitution)

## Deployment Considerations

### Development Deployment

**Command**:
```bash
# Add to setup.py console scripts
vocab-analyzer-web  # Launches Flask dev server on http://127.0.0.1:5000
```

**Configuration**:
- Debug mode enabled
- Auto-reload on code changes
- Detailed error pages

### Production Deployment

**WSGI Server**: Gunicorn (Unix) or Waitress (Windows)

**Command**:
```bash
gunicorn -w 4 -b 0.0.0.0:8000 vocab_analyzer.web.app:app
```

**Configuration**:
- 4 worker processes (adjust based on CPU cores)
- Timeout: 120s (for large file processing)
- Max requests: 1000 (worker restart for memory leak prevention)
- Logging: Access log + error log to files

**Reverse Proxy**: Nginx (optional, for SSL/caching)

```nginx
location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    client_max_body_size 50M;  # Match upload limit
}
```

### Docker Deployment (Optional)

**Dockerfile** (if requested):
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm
COPY . .
EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "vocab_analyzer.web.app:app"]
```

## Open Questions & Future Enhancements

### Resolved Questions

All technical unknowns have been resolved through research. No blockers remain.

### Future Enhancement Opportunities

**Phase 3 Considerations** (not in current scope):

1. **Multi-file batch upload**: Analyze multiple books in sequence
   - Requires job queue (could use simple in-memory queue)
   - UI shows list of files with individual progress bars

2. **Result history**: Save recent analyses in browser localStorage
   - Client-side only (no server storage)
   - Allows user to revisit results without re-analyzing

3. **Enhanced visualization**: Interactive charts for CEFR distribution
   - Could use Chart.js (small library, no build step)
   - Shows distribution trends, word frequency graphs

4. **Custom wordlist upload**: Let users provide their own CEFR lists
   - Temporarily override default wordlist for one analysis
   - Useful for domain-specific vocabulary

5. **Export to Anki**: Generate Anki flashcard deck from analysis
   - Requires Anki deck format research
   - Could be new exporter module (`exporters/anki_exporter.py`)

**Priority**: All enhancements deferred until MVP web interface is validated with users.

## References

### Documentation Consulted

1. **Flask Documentation**: https://flask.palletsprojects.com/en/3.0.x/
   - Quickstart, Uploading Files, Streaming, Error Handling
2. **MDN Web Docs - Server-Sent Events**: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events
   - EventSource API, SSE message format
3. **Werkzeug Documentation**: https://werkzeug.palletsprojects.com/
   - `secure_filename()`, security considerations
4. **Python tempfile module**: https://docs.python.org/3/library/tempfile.html
   - Temporary file handling, cleanup strategies

### Code Examples Reviewed

1. **Flask File Upload Examples**: Official Flask documentation snippets
2. **SSE with Flask**: Community examples on GitHub (flask-sse patterns)
3. **Vanilla JS Fetch API**: MDN examples for file upload with FormData

## Conclusion

All technical decisions have been made with the constitution's "simplicity first" principle as the primary driver. The chosen stack (Flask + vanilla JavaScript + SSE) represents the **minimal viable complexity** for delivering the required functionality:

- **Zero changes** to existing vocab_analyzer core
- **One new dependency** (Flask) with minimal transitive packages
- **No build tooling** required (no npm, webpack, etc.)
- **Single-page interface** (<500 lines of code total)
- **Production-ready** from day one (WSGI deployment)

No unresolved technical questions remain. Implementation can proceed to Phase 1 (data model and contracts).
