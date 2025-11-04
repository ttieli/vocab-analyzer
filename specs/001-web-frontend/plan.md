# Implementation Plan: Web Frontend for Vocabulary Analyzer

**Branch**: `001-web-frontend` | **Date**: 2025-11-04 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-web-frontend/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a simple web interface for the Vocabulary Analyzer that allows users to upload book files (TXT, PDF, DOCX), analyze them using the existing VocabularyAnalyzer engine, and view/download results in multiple formats. The solution uses Flask (minimal Python web framework) with Server-Sent Events (SSE) for real-time progress updates, avoiding complexity of WebSockets or JavaScript frameworks.

**Technical Approach**: Single-page Flask application with vanilla JavaScript frontend, leveraging existing vocab_analyzer core completely unchanged, implementing session-based file handling with temporary storage cleanup.

## Technical Context

**Language/Version**: Python 3.10+ (matching existing project)
**Primary Dependencies**: Flask 3.0+ (web framework), existing vocab_analyzer modules (unchanged)
**Storage**: Temporary filesystem storage for uploaded files (auto-cleanup after processing)
**Testing**: pytest (existing framework), added web endpoint testing with Flask test client
**Target Platform**: Local development server (Flask built-in) / production deployment via Gunicorn or Waitress
**Project Type**: Web application (minimal - single Flask app, no separate frontend build)
**Performance Goals**: Process 100-page book in <60 seconds (reuses existing analyzer performance), <2s page load time
**Constraints**: Single concurrent analysis per user session, 50MB max upload size, desktop browsers only (Chrome/Firefox/Safari/Edge)
**Scale/Scope**: Personal/small team usage (not designed for high concurrency), ~5-10 concurrent users max

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Simplicity & Maintainability ✅

- **Flask chosen**: Minimal web framework, no frontend build step required
- **Vanilla JavaScript**: No React/Vue/Angular complexity, simple SSE for progress
- **Reuse existing code**: Zero changes to vocab_analyzer core modules
- **Single responsibility**: Web layer only handles HTTP, delegates all analysis to existing modules

### Principle II: Modular Architecture ✅

- **New module**: `src/vocab_analyzer/web/` contains only web-specific code
- **Clean interface**: Web module imports existing analyzer facade, no internal coupling
- **Independent testing**: Web endpoints tested separately from core logic
- **No module changes**: All 6 existing modules (extraction, NLP, phrase, level, stats, export) unchanged

### Principle III: Data Quality First ✅

- **Input validation**: File type/size validation before passing to existing extractors
- **Reuse validators**: Existing file validation in extractors unchanged
- **Error handling**: Web layer catches and presents errors from analyzer
- **No data modification**: Analysis results passed through unchanged from core

### Principle IV: Test-Driven Development ✅

- **Coverage target**: 80% overall maintained, 100% for new web endpoints
- **Test types**: Unit tests for routes, integration tests for upload → analysis → download flow
- **Reuse fixtures**: Same test corpus from tests/fixtures/ used for web integration tests
- **CI/CD compatible**: Flask test client integrates with existing pytest setup

### Principle V: CLI-First Design ✅

- **CLI preserved**: Web interface is additive, CLI remains primary/unchanged
- **Same output**: Web downloads produce identical files to CLI (reuses exporters)
- **No web-only features**: All functionality available via CLI
- **Documentation**: Web interface documented as optional enhancement

### Principle VI: Project Organization & Structure ⚠️ **REQUIRES JUSTIFICATION**

**Violation**: Adding `src/vocab_analyzer/web/` directory + static files

**Justification**:
- Web module follows same pattern as existing modules (analyzers/, exporters/, etc.)
- Static files (HTML/CSS/JS) go in `src/vocab_analyzer/web/static/` (standard Flask convention)
- Alternative considered: Separate `web/` top-level directory rejected because:
  - Breaks single-package paradigm of project
  - Complicates imports and testing
  - Flask best practice is static files within package
- **Minimal footprint**: <5 files total (app.py, upload.html, progress.js, style.css)

### Code Quality Standards ✅

- **PEP 8 compliance**: All new Python code follows existing standards
- **Type annotations**: Flask routes fully type-annotated
- **Docstrings**: Google-style docstrings for all web functions
- **Linting**: Passes pylint/flake8 with score ≥8.5

### Performance Standards ✅

- **Reuses existing**: All performance optimizations in core preserved
- **No degradation**: Web layer adds <100ms overhead for request handling
- **Streaming uploads**: Uses Flask streaming for large file uploads
- **Async processing**: SSE allows non-blocking progress updates

### Security & Privacy ✅

- **File validation**: Magic number check + size limit (50MB) enforced
- **Path sanitization**: Werkzeug secure_filename() prevents path traversal
- **Temporary files**: Auto-cleanup with tempfile module + after-request hooks
- **No persistence**: Files deleted after analysis, no database/logging of content
- **Local by default**: Same privacy as CLI (all processing local)

## Project Structure

### Documentation (this feature)

```text
specs/001-web-frontend/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
│   └── web-api.yaml     # OpenAPI spec for web endpoints
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

**Structure Decision**: Extended single project structure. The existing `src/vocab_analyzer/` package is extended with a new `web/` module, following the same modular pattern as existing components (cli/, exporters/, analyzers/, etc.). This maintains project simplicity while adding web capability as an optional interface.

```text
src/vocab_analyzer/
├── __init__.py
├── __main__.py
├── analyzers/           # UNCHANGED - existing statistics module
├── cli/                 # UNCHANGED - existing CLI commands
├── core/                # UNCHANGED - existing analyzer facade
├── exporters/           # UNCHANGED - JSON/CSV/Markdown exporters
├── extractors/          # UNCHANGED - TXT/PDF/DOCX extractors
├── matchers/            # UNCHANGED - CEFR level matching
├── models/              # UNCHANGED - Word/Phrase/Analysis data models
├── processors/          # UNCHANGED - NLP tokenization/phrase detection
├── utils/               # UNCHANGED - file/text/cache utilities
└── web/                 # NEW - Web interface module
    ├── __init__.py
    ├── app.py           # Flask application factory
    ├── routes.py        # HTTP route handlers
    ├── session.py       # Session management for uploads
    ├── progress.py      # SSE progress tracking
    ├── static/          # Frontend assets
    │   ├── index.html   # Single-page interface
    │   ├── styles.css   # Minimal styling
    │   └── app.js       # Vanilla JS (SSE client, upload, download)
    └── templates/       # Flask templates (optional - only if using Jinja2 for error pages)
        └── error.html   # (optional)

tests/
├── fixtures/            # UNCHANGED - existing test corpus
├── unit/                # UNCHANGED - existing unit tests
├── integration/         # UNCHANGED - existing integration tests
└── web/                 # NEW - Web-specific tests
    ├── test_routes.py   # Test HTTP endpoints
    ├── test_upload.py   # Test file upload flow
    └── test_sse.py      # Test progress streaming

config/
└── web_config.yaml      # NEW - Web server configuration (optional)

docs/
└── web_interface.md     # NEW - Web UI user guide
```

**Key Design Points**:

1. **Zero changes to existing modules**: All 10 existing directories (analyzers/ through utils/) remain completely unchanged
2. **Web as peer module**: `web/` follows same pattern as `cli/`, `exporters/`, etc.
3. **Static files within package**: Flask convention, simplifies deployment (single package install)
4. **Minimal frontend**: 3 files (HTML/CSS/JS), no build step, no npm/node dependencies
5. **Test isolation**: New `tests/web/` directory parallel to existing test structure

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Adding `web/` module with static files | Web interface requires serving HTML/CSS/JS and handling HTTP requests - cannot be done via CLI | **Alt 1: Separate web repository** - Rejected: duplicates vocab_analyzer dependency, complicates deployment/installation<br>**Alt 2: Top-level `web/` directory** - Rejected: breaks single-package paradigm, complicates imports (`from vocab_analyzer.core` vs `from vocab_analyzer.web`)<br>**Alt 3: External tool (Gradio/Streamlit)** - Rejected: adds heavy dependency (100+ packages), less control over UX |
| Static files in `src/vocab_analyzer/web/static/` | Flask requires serving static files; standard convention is within package | **Alt 1: Root-level `static/`** - Rejected: violates Principle VI (no non-source files in root or src/)<br>**Alt 2: `data/web_assets/`** - Rejected: `data/` is for vocabulary lists/dictionaries per constitution, not application assets<br>**Alt 3: CDN for JS/CSS** - Rejected: requires internet, defeats local-first privacy principle |

**Justification Summary**: The web module addition is the **minimal viable approach** that respects existing architecture. It adds exactly 1 new module (like adding a new exporter or extractor) and <500 lines of code total. All alternatives either violate more principles or add significantly more complexity.
