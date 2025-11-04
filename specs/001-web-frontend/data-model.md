# Data Model: Web Frontend

**Feature**: Web Frontend for Vocabulary Analyzer
**Date**: 2025-11-04
**Status**: Complete

## Overview

This document defines the data models for the web frontend feature. Most data structures are **reused from existing vocab_analyzer models** (Word, Phrase, VocabularyAnalysis). Only web-specific session management requires new models.

## Design Principles

1. **Reuse over reinvention**: Leverage existing models from `src/vocab_analyzer/models/`
2. **Stateless sessions**: No persistent storage, temporary files only
3. **Immutable results**: Analysis results are read-only once generated
4. **Auto-cleanup**: All temporary data has TTL and cleanup hooks

## Core Data Models

### 1. UploadSession (New)

**Purpose**: Track a single file upload and analysis session

**Location**: `src/vocab_analyzer/web/session.py`

**Fields**:

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| `session_id` | str | Unique identifier (UUID4) | Required, immutable |
| `uploaded_file` | UploadedFile | File metadata and path | Required |
| `status` | SessionStatus | Current processing status | Required, enum |
| `progress` | ProgressState | Real-time progress tracking | Required |
| `result` | VocabularyAnalysis \| None | Analysis output (when complete) | Optional |
| `error` | ErrorInfo \| None | Error details (if failed) | Optional |
| `created_at` | datetime | Session creation timestamp | Required, UTC |
| `expires_at` | datetime | Auto-cleanup time (created_at + 1 hour) | Required, UTC |

**Relationships**:
- Contains one `UploadedFile`
- Contains one `ProgressState`
- May contain one `VocabularyAnalysis` (reuses existing model)
- May contain one `ErrorInfo`

**State Transitions**:
```
CREATED → VALIDATING → PROCESSING → COMPLETED
                    ↓             ↓
                  FAILED        FAILED
```

**Lifecycle**:
1. Created when user uploads file
2. Updated during validation and processing
3. Terminal states: COMPLETED or FAILED
4. Auto-deleted 1 hour after creation (regardless of state)

**Example**:
```python
@dataclass
class UploadSession:
    session_id: str
    uploaded_file: UploadedFile
    status: SessionStatus
    progress: ProgressState
    result: Optional[VocabularyAnalysis] = None
    error: Optional[ErrorInfo] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(hours=1))
```

---

### 2. UploadedFile (New)

**Purpose**: Metadata for uploaded book file

**Location**: `src/vocab_analyzer/web/session.py`

**Fields**:

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| `original_filename` | str | User's filename (unsanitized) | Required |
| `safe_filename` | str | Sanitized filename (Werkzeug) | Required, no path chars |
| `file_path` | Path | Temporary file location | Required, absolute path |
| `file_type` | FileType | Detected file format | Required, enum (TXT/PDF/DOCX) |
| `file_size` | int | Size in bytes | Required, >0, ≤50MB |
| `mime_type` | str | MIME type from magic number | Required |
| `uploaded_at` | datetime | Upload completion time | Required, UTC |

**Validation Rules**:
- `file_size`: Maximum 50 MB (50 * 1024 * 1024 bytes)
- `file_type`: Must be one of FileType.TXT, FileType.PDF, FileType.DOCX
- `mime_type`: Must match file_type (prevents renamed .exe → .txt attacks)
- `file_path`: Must be in OS temporary directory (security)

**Example**:
```python
@dataclass
class UploadedFile:
    original_filename: str
    safe_filename: str
    file_path: Path
    file_type: FileType
    file_size: int
    mime_type: str
    uploaded_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
```

---

### 3. ProgressState (New)

**Purpose**: Track real-time analysis progress for SSE updates

**Location**: `src/vocab_analyzer/web/progress.py`

**Fields**:

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| `stage` | ProcessingStage | Current processing stage | Required, enum |
| `stage_name` | str | Human-readable stage name | Required |
| `percentage` | int | Overall progress (0-100) | Required, 0 ≤ x ≤ 100 |
| `message` | str | Detailed status message | Optional |
| `started_at` | datetime | Analysis start time | Required, UTC |
| `updated_at` | datetime | Last progress update | Required, UTC |

**Processing Stages** (Enum):
```python
class ProcessingStage(Enum):
    VALIDATING = "validating"       # File validation (5%)
    EXTRACTING = "extracting"       # Text extraction (15%)
    TOKENIZING = "tokenizing"       # NLP processing (40%)
    DETECTING_PHRASES = "phrases"   # Phrasal verb detection (60%)
    MATCHING_LEVELS = "levels"      # CEFR level matching (80%)
    GENERATING_STATS = "statistics" # Statistics calculation (95%)
    COMPLETED = "completed"         # Done (100%)
```

**Stage Progress Mapping**:
- VALIDATING: 0-5%
- EXTRACTING: 5-15%
- TOKENIZING: 15-40%
- DETECTING_PHRASES: 40-60%
- MATCHING_LEVELS: 60-80%
- GENERATING_STATS: 80-95%
- COMPLETED: 95-100%

**Example**:
```python
@dataclass
class ProgressState:
    stage: ProcessingStage
    stage_name: str
    percentage: int
    message: str = ""
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
```

---

### 4. ErrorInfo (New)

**Purpose**: Structured error information for failed analyses

**Location**: `src/vocab_analyzer/web/session.py`

**Fields**:

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| `error_code` | str | Machine-readable error code | Required |
| `error_message` | str | User-friendly error message | Required |
| `error_stage` | ProcessingStage | Stage where error occurred | Required |
| `technical_details` | str | Stack trace / debug info | Optional, logged only |
| `occurred_at` | datetime | Error timestamp | Required, UTC |

**Error Codes**:
- `UPLOAD_INVALID_TYPE`: Unsupported file format
- `UPLOAD_TOO_LARGE`: File exceeds 50MB limit
- `UPLOAD_CORRUPTED`: File cannot be read
- `EXTRACTION_FAILED`: Text extraction error
- `PROCESSING_FAILED`: NLP processing error
- `INTERNAL_ERROR`: Unexpected server error

**Example**:
```python
@dataclass
class ErrorInfo:
    error_code: str
    error_message: str
    error_stage: ProcessingStage
    technical_details: str = ""
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
```

---

## Reused Models (Existing)

These models are **unchanged** and reused from `src/vocab_analyzer/models/`:

### Word (Existing)

**Source**: `src/vocab_analyzer/models/word.py`

**Usage**: Individual word entries in analysis results

**Key Fields**:
- `lemma`: Base form of word
- `level`: CEFR level (A1-C2+)
- `frequency`: Occurrence count in text
- `chinese_translation`: Chinese definition (from ECDICT)
- `example_sentences`: Sample usages from source text

**Reuse Justification**: Core vocabulary data structure, already has all needed fields

---

### Phrase (Existing)

**Source**: `src/vocab_analyzer/models/phrase.py`

**Usage**: Phrasal verb entries in analysis results

**Key Fields**:
- `phrase`: Full phrasal verb (e.g., "look up")
- `level`: CEFR level
- `frequency`: Occurrence count
- `is_separable`: Whether verb can be split (e.g., "look it up")
- `example_sentences`: Sample usages

**Reuse Justification**: Phrasal verb structure is complete, no web-specific changes needed

---

### VocabularyAnalysis (Existing)

**Source**: `src/vocab_analyzer/models/analysis.py`

**Usage**: Complete analysis results (stored in UploadSession.result)

**Key Fields**:
- `words`: List of Word objects organized by CEFR level
- `phrases`: List of Phrase objects
- `statistics`: VocabularyStatistics (counts, distributions)
- `metadata`: AnalysisMetadata (source file, processing time)

**Reuse Justification**: This is the primary output of vocab_analyzer core; web interface simply displays/downloads it

---

## Data Flow

### Upload to Analysis Flow

```
User Upload
    ↓
1. Create UploadSession (session_id, status=CREATED)
    ↓
2. Create UploadedFile (save to tempfile, validate)
    ↓
3. Update ProgressState (stage=VALIDATING, 5%)
    ↓
4. Invoke existing VocabularyAnalyzer.analyze(file_path)
    ├── Update ProgressState at each stage
    ├── EXTRACTING (15%)
    ├── TOKENIZING (40%)
    ├── DETECTING_PHRASES (60%)
    ├── MATCHING_LEVELS (80%)
    └── GENERATING_STATS (95%)
    ↓
5. Store VocabularyAnalysis in session.result
    ↓
6. Update status=COMPLETED, progress=100%
    ↓
7. Client requests download (JSON/CSV/Markdown)
    ↓
8. Reuse existing exporters (JsonExporter, CsvExporter, MarkdownExporter)
    ↓
9. Return file to client
    ↓
10. Auto-cleanup after 1 hour (delete temp file, remove session)
```

### Error Handling Flow

```
Error Occurs at Stage X
    ↓
1. Catch exception in analyzer wrapper
    ↓
2. Create ErrorInfo (error_code, message, stage=X)
    ↓
3. Update session.status = FAILED
    ↓
4. Update session.error = ErrorInfo
    ↓
5. Send SSE error event to client
    ↓
6. Display user-friendly error message
    ↓
7. Log technical details server-side (stack trace)
    ↓
8. Cleanup temp file immediately (don't wait for TTL)
```

## Serialization

### Session Storage

**Format**: In-memory dictionary (server-side)

**Structure**:
```python
# In web.app module
sessions: Dict[str, UploadSession] = {}

# Cleanup job (runs every 10 minutes)
def cleanup_expired_sessions():
    now = datetime.now(timezone.utc)
    expired = [sid for sid, session in sessions.items() if session.expires_at < now]
    for sid in expired:
        # Delete temp file
        session.uploaded_file.file_path.unlink(missing_ok=True)
        # Remove from memory
        del sessions[sid]
```

**Justification**: No persistence requirement (constitution: local processing only). In-memory storage is simplest and fastest.

### SSE Message Format

**Format**: JSON over Server-Sent Events

**Progress Update Message**:
```json
{
  "event": "progress",
  "data": {
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "stage": "tokenizing",
    "stage_name": "Tokenizing and lemmatizing words",
    "percentage": 40,
    "message": "Processing sentence batch 5/12"
  }
}
```

**Completion Message**:
```json
{
  "event": "complete",
  "data": {
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "download_urls": {
      "json": "/download/550e8400.../json",
      "csv": "/download/550e8400.../csv",
      "markdown": "/download/550e8400.../markdown"
    },
    "statistics": {
      "total_words": 6544,
      "unique_words": 2145,
      "phrasal_verbs": 18,
      "processing_time_seconds": 12.5
    }
  }
}
```

**Error Message**:
```json
{
  "event": "error",
  "data": {
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "error_code": "EXTRACTION_FAILED",
    "error_message": "Unable to extract text from PDF. The file may be corrupted or password-protected.",
    "error_stage": "extracting"
  }
}
```

### Download Response Format

**Format**: Reuses existing exporter output formats

**JSON** (from JsonExporter):
- Already defined in `src/vocab_analyzer/exporters/json_exporter.py`
- No changes required

**CSV** (from CsvExporter):
- Already defined in `src/vocab_analyzer/exporters/csv_exporter.py`
- Generates two files: `*_words.csv` and `*_phrases.csv`
- Web interface zips them together for single download

**Markdown** (from MarkdownExporter):
- Already defined in `src/vocab_analyzer/exporters/markdown_exporter.py`
- No changes required

## Validation Rules

### Upload Validation (Executed in order)

1. **File Presence Check**
   - Error if no file in request: `400 Bad Request`

2. **File Size Check**
   - Maximum: 50 MB
   - Error if exceeded: `413 Payload Too Large`

3. **File Extension Check**
   - Allowed: `.txt`, `.pdf`, `.docx`
   - Error if other: `400 Bad Request` ("Unsupported file type")

4. **Magic Number Check**
   - Verify file header matches extension
   - TXT: Check UTF-8 encoding
   - PDF: Check `%PDF-` header
   - DOCX: Check ZIP header + `word/` directory
   - Error if mismatch: `400 Bad Request` ("File type mismatch")

5. **Filename Sanitization**
   - Apply `werkzeug.utils.secure_filename()`
   - Remove path traversal characters: `/`, `\`, `..`
   - Preserve extension for type detection

### Session Validation

1. **Session ID Format**
   - Must be valid UUID4
   - Error if invalid: `400 Bad Request`

2. **Session Existence**
   - Must exist in sessions dict
   - Error if not found: `404 Not Found`

3. **Session Expiration**
   - Must be before `expires_at`
   - Error if expired: `410 Gone` ("Session expired")

## Database Schema

**Not Applicable**: No database used. All data is in-memory with temporary file storage.

**Justification**: Constitution requires local processing with no persistence. In-memory storage aligns with stateless design and auto-cleanup requirements.

## Migration Strategy

**Not Applicable**: No existing data to migrate. This is a new feature with no prior state.

## Testing Strategy

### Unit Tests

**Test Models**:
- `UploadSession` state transitions
- `ProgressState` percentage calculations
- `ErrorInfo` serialization
- Validation rule enforcement

**Test Fixtures**:
```python
# tests/web/conftest.py
@pytest.fixture
def sample_upload_session():
    return UploadSession(
        session_id=str(uuid.uuid4()),
        uploaded_file=create_sample_uploaded_file(),
        status=SessionStatus.CREATED,
        progress=ProgressState(stage=ProcessingStage.VALIDATING, ...)
    )
```

### Integration Tests

**Test Scenarios**:
- Upload valid file → session created with correct metadata
- Upload invalid file → error returned, no session created
- Complete analysis → VocabularyAnalysis stored in session.result
- Session expiration → cleanup deletes temp file and memory entry

**Coverage Target**: 100% of new models (UploadSession, UploadedFile, ProgressState, ErrorInfo)

## Conclusion

The data model design **maximizes reuse** of existing vocab_analyzer models (Word, Phrase, VocabularyAnalysis) and introduces **minimal new models** (4 classes, <200 lines) for web-specific session management. All models are designed for simplicity, type safety, and automatic cleanup.

No database or persistent storage is required, aligning with the constitution's local-first privacy principle.
