<!--
═══════════════════════════════════════════════════════════════════════════════
SYNC IMPACT REPORT - Constitution Amendment
═══════════════════════════════════════════════════════════════════════════════
Version Change: 1.0.0 → 1.1.0 (Minor Amendment - New Principle Added)

Modified Principles:
  None - All existing principles unchanged

Added Sections:
  ✓ Principle VI: Project Organization & Structure (NEW)
    - Clean root directory policy
    - Structured directory layout requirements
    - File placement guidelines
    - Documentation organization

Removed Sections:
  None

Template Sync Status:
  ✅ .specify/templates/plan-template.md - Project Structure section aligns with new principle
  ✅ .specify/templates/tasks-template.md - Path conventions compatible with new structure
  ✅ .specify/templates/spec-template.md - No changes required
  ✅ .specify/templates/checklist-template.md - No changes required

Follow-up Actions:
  □ Create project README.md with quickstart guide referencing this constitution
  □ Setup .pylintrc and pyproject.toml for code quality enforcement
  □ Create test corpus directory structure under tests/fixtures/
  □ Setup GitHub Actions or equivalent CI/CD pipeline
  □ Reorganize any existing files to comply with new structure principle (if needed)

Deferred Items:
  None - All placeholders filled with concrete values

Amendment Summary:
  - Added Principle VI: Project Organization & Structure
  - Mandates clean root directory (minimal files)
  - Defines standard directory layout: src/, tests/, data/, docs/, config/
  - Specifies where each type of file belongs
  - Enforces "everything in its place" philosophy
  - Version bumped to 1.1.0 (MINOR: new principle added)

Rationale for Version Bump:
  - MINOR increment (1.0.0 → 1.1.0) because:
    - New principle added (materially expanded governance)
    - No backward-incompatible changes to existing principles
    - Existing code may need reorganization but functionality unchanged
    - Additive change only (no removals or redefinitions)

═══════════════════════════════════════════════════════════════════════════════
-->

# English Vocabulary Analyzer Constitution

## Core Principles

### I. Simplicity & Maintainability

**Core Philosophy**: "简单至上 - 不过度设计,优先正确性而非性能"

This project MUST prioritize straightforward solutions over complex architectures. Every technical decision should favor clarity and maintainability.

**Non-Negotiable Rules**:
- Prefer simple, readable code over clever optimizations
- Each module handles one specific responsibility
- Use only essential dependencies: spaCy, pandas, PyPDF2, python-docx, standard library
- Function and variable names MUST be self-documenting (no abbreviations unless standard)
- Avoid premature optimization - correctness first, performance second
- YAGNI principle strictly enforced: implement features only when needed

**Rationale**: This is a personal/small-team tool. Code maintainability and ease of understanding outweigh performance optimizations. A clear codebase allows future enhancements without technical debt.

---

### II. Modular Architecture

**Core Philosophy**: "模块化架构 - 6个独立模块,低耦合,易测试"

The system MUST be decomposed into six independent modules with clear interfaces and minimal coupling.

**Required Modules**:
1. **Text Extraction Module**: Handles TXT/PDF/DOCX file parsing
2. **NLP Processing Module**: Tokenization, lemmatization, POS tagging (spaCy)
3. **Phrase Detection Module**: Identifies phrasal verbs and collocations
4. **Level Matching Module**: Maps words to CEFR levels (A1-C2)
5. **Statistics & Analysis Module**: Frequency counts, distribution analysis
6. **Output Generation Module**: Produces JSON/CSV/Markdown formats

**Non-Negotiable Rules**:
- Each module MUST be importable and usable independently
- Module interfaces defined through clear input/output contracts (type-annotated)
- No direct cross-dependencies: modules communicate through defined data structures
- Each module has its own test suite (unit tests)
- Shared data structures defined in a common `models.py` file

**Rationale**: Modular design enables independent testing, parallel development, and easy replacement of components (e.g., swapping NLP library).

---

### III. Data Quality First

**Core Philosophy**: "数据质量第一 - >95%等级匹配准确率,数据可追溯"

Accuracy of vocabulary level matching is paramount. Every word's assigned level MUST be traceable to its source.

**Non-Negotiable Rules**:
- All input files MUST be validated before processing (file type, encoding, size limits)
- Level matching accuracy MUST exceed 95% against Cambridge vocabulary lists
- Every vocabulary entry MUST include source reference (which list/dictionary)
- Graceful degradation: if level unknown, mark as "C2+" (out-of-syllabus) rather than failing
- Data integrity checks: word form consistency, frequency counts, example sentence validity
- Errors MUST be logged with context (filename, line number, problematic word)

**Validation Requirements**:
- Cambridge vocabulary list completeness (no missing levels)
- Phrasal verb dictionary coverage (minimum 500 entries)
- Output data schema validation (JSON schema, CSV column integrity)

**Rationale**: Users rely on accurate level assignments for study planning. Incorrect data undermines the tool's core value proposition.

---

### IV. Test-Driven Development

**Core Philosophy**: "测试驱动 - 80%代码覆盖率,关键路径100%覆盖"

Testing is non-negotiable. All code MUST be accompanied by tests achieving specified coverage targets.

**Coverage Requirements**:
- **Overall Coverage**: Minimum 80% code coverage
- **Critical Path Coverage**: 100% coverage required for:
  - Text extraction functions (all file types)
  - Word lemmatization logic
  - Level matching algorithms
  - Phrase detection patterns
  - Output file generation

**Test Types Required**:
1. **Unit Tests**: Every module function with isolated dependencies (mocks/stubs)
2. **Integration Tests**: End-to-end file processing workflows (sample files → output validation)
3. **Performance Tests**: Processing speed benchmarks for standard file sizes
4. **Edge Case Tests**: Malformed PDFs, special characters, large files, empty inputs

**Test Data Requirements**:
- Maintain diverse test corpus under `tests/fixtures/`:
  - Small (1-page), medium (20-page), large (100+ page) files
  - Multiple formats: TXT, PDF, DOCX
  - Multiple genres: fiction, non-fiction, technical documentation
- Golden datasets: manually verified outputs for accuracy testing

**CI/CD Requirements**:
- Pre-commit hooks: linting + quick unit tests (<10s)
- Full test suite runs on every push to feature branches
- Performance regression alerts if processing time increases >20%

**Rationale**: Vocabulary analysis involves complex NLP and data matching. Comprehensive testing prevents regressions and ensures reliability.

---

### V. CLI-First Design

**Core Philosophy**: "CLI优先 - 命令行为主,清晰的进度反馈"

The primary interface MUST be a command-line tool with excellent usability and feedback.

**Non-Negotiable Rules**:
- **Primary Interface**: Command-line interface (CLI) using Python `argparse` or `click`
- **Stdin/Stdout Protocol**: Support piping and command chaining where applicable
- **Progress Feedback**: Visual progress indicators for operations >3 seconds (use `tqdm` or similar)
- **Error Messages**: Specific, actionable error messages (not stack traces for user-facing errors)
- **Multiple Output Formats**: JSON, CSV, Markdown - all equally supported, no "primary" format
- **Human-Readable Output**: Default terminal output uses tables/colors for readability (use `rich` or `tabulate`)

**CLI Design Standards**:
- Clear help text (`--help`) with examples
- Sensible defaults (no required flags unless absolutely necessary)
- Verbose mode (`--verbose`) for debugging
- Dry-run mode for preview without file writes
- Version display (`--version`)

**Rationale**: Command-line tools are fast, scriptable, and integrate well with workflows. Good UX (progress, errors) makes the tool approachable even for non-technical users.

---

### VI. Project Organization & Structure

**Core Philosophy**: "整体项目格式清晰 - 尽量少在根目录增加内容,每个代码和文本都在合适的位置"

The project structure MUST be clean, organized, and predictable. Root directory clutter is forbidden. Every file has a designated place.

**Root Directory Policy** (Maximum Simplicity):

The root directory MUST contain ONLY these essential files:
- `README.md` - Project overview and quickstart guide
- `LICENSE` - License file
- `pyproject.toml` or `setup.py` - Python project configuration
- `requirements.txt` - Python dependencies
- `.gitignore` - Git ignore rules
- `.pylintrc` - Linting configuration (optional, can be in `pyproject.toml`)

**Forbidden in Root**:
- ❌ No source code files (`.py` files belong in `src/`)
- ❌ No data files (CSV, JSON, TXT - belong in `data/`)
- ❌ No documentation beyond README (other docs go in `docs/`)
- ❌ No test files (belong in `tests/`)
- ❌ No configuration files beyond build/project config (app configs go in `config/`)
- ❌ No output files, logs, or temporary files
- ❌ No example files or sample inputs (belong in `examples/` or `data/samples/`)

**Standard Directory Layout**:

```
project-root/
├── README.md                    # Project overview (REQUIRED)
├── LICENSE                      # License file
├── pyproject.toml               # Python project config (or setup.py)
├── requirements.txt             # Dependencies
├── .gitignore                   # Git ignore rules
│
├── src/                         # ALL source code goes here
│   ├── __init__.py
│   ├── models.py                # Shared data structures
│   ├── text_extraction.py      # Module 1
│   ├── nlp_processing.py       # Module 2
│   ├── phrase_detection.py     # Module 3
│   ├── level_matching.py       # Module 4
│   ├── statistics.py           # Module 5
│   ├── output_generation.py    # Module 6
│   ├── cli.py                  # CLI entry point
│   └── utils.py                # Utility functions (if needed)
│
├── tests/                       # ALL test files go here
│   ├── __init__.py
│   ├── fixtures/               # Test data organized by size/type
│   │   ├── small/
│   │   ├── medium/
│   │   ├── large/
│   │   ├── edge_cases/
│   │   └── golden/             # Expected outputs for validation
│   ├── unit/                   # Unit tests (one file per module)
│   │   ├── test_text_extraction.py
│   │   ├── test_nlp_processing.py
│   │   └── ...
│   ├── integration/            # Integration tests
│   │   └── test_end_to_end.py
│   └── performance/            # Performance benchmarks
│       └── test_benchmarks.py
│
├── data/                        # ALL data files go here
│   ├── vocabulary/             # Vocabulary lists
│   │   ├── cambridge_a1.csv
│   │   ├── cambridge_a2.csv
│   │   └── ...
│   ├── phrasal_verbs.json      # Phrasal verb dictionary
│   ├── chinese_definitions.json # Optional Chinese translations
│   └── samples/                # Sample input files for demos
│       ├── sample_book.txt
│       └── sample_article.pdf
│
├── docs/                        # ALL documentation beyond README
│   ├── architecture.md         # System architecture overview
│   ├── data_sources.md         # Data source documentation
│   ├── api_reference.md        # Module API documentation
│   └── development_guide.md    # Developer setup and guidelines
│
├── config/                      # Application configuration files
│   ├── default_config.yaml     # Default configuration
│   └── config_schema.json      # Configuration schema
│
├── scripts/                     # Utility scripts (setup, data prep, etc.)
│   ├── download_vocabulary.py  # Script to fetch vocabulary lists
│   └── prepare_test_data.py    # Script to generate test fixtures
│
├── .github/                     # GitHub-specific files
│   └── workflows/
│       └── ci.yml              # CI/CD pipeline configuration
│
└── .specify/                    # Speckit framework files (project management)
    ├── memory/
    │   └── constitution.md     # This file
    └── templates/
```

**File Placement Rules**:

1. **Source Code**: ALL `.py` implementation files MUST be in `src/`
   - Entry point: `src/cli.py` or `src/__main__.py`
   - Modules: One file per module (principle II)
   - No subdirectories unless >10 modules (keep flat for simplicity)

2. **Tests**: ALL test files MUST be in `tests/` with parallel structure to `src/`
   - Test file naming: `test_<module_name>.py`
   - Test fixtures: `tests/fixtures/` organized by purpose

3. **Data Files**: ALL data files MUST be in `data/`
   - Vocabulary lists: `data/vocabulary/`
   - Sample inputs: `data/samples/`
   - No data files in `src/` or root

4. **Documentation**: Extended docs MUST be in `docs/`
   - Only `README.md` allowed in root
   - Architecture, design decisions, API docs: all in `docs/`

5. **Configuration**: Application configs MUST be in `config/`
   - Project build config (pyproject.toml) stays in root
   - Application runtime config: `config/`

6. **Scripts**: Utility scripts MUST be in `scripts/`
   - Data preparation, setup scripts, etc.
   - Not user-facing tools (those go in `src/cli.py`)

**Output File Management**:

- Generated output files (vocabulary analysis results) MUST NOT be in the repository
- Add to `.gitignore`: `*.vocab.json`, `*.vocab.csv`, `*.vocab.md`, `output/`
- Users generate output files in their working directory (not in project tree)
- Example in docs: `vocab_analyzer input.txt --output ~/Documents/results/`

**Enforcement**:

- Pre-commit hooks MUST reject commits with files in wrong locations
- CI pipeline checks directory structure compliance
- Code reviews MUST verify new files are in correct locations
- Exception process: if new top-level directory needed, MUST update this constitution first

**Rationale**: A clean, predictable structure makes the project easy to navigate, reduces cognitive load, and prevents the "where does this file go?" question. It also makes automation (CI/CD, tooling) straightforward and reliable.

---

## Code Quality Standards

### Python Code Standards

**Style Guide**: PEP 8 compliance is **mandatory**. No exceptions.

**Type Annotations**: All function signatures MUST include type hints:
```python
def extract_text(file_path: Path) -> str:
    """Extract text from file."""
    ...
```

**Docstrings**: Google-style docstrings required for all public functions and classes:
```python
def lemmatize_word(word: str, pos_tag: str) -> str:
    """Convert word to its dictionary base form.

    Args:
        word: The word to lemmatize
        pos_tag: Part-of-speech tag (NOUN, VERB, etc.)

    Returns:
        The lemmatized word form

    Raises:
        ValueError: If pos_tag is invalid
    """
    ...
```

**Code Formatting**: Use `black` for automatic formatting (line length: 88 characters)

**Linting**: Code MUST pass `pylint` and `flake8` checks with minimum score 8.5/10

**Import Organization**: Use `isort` for consistent import ordering

### Code Review Requirements

**Mandatory Process**:
- No direct commits to `main` branch
- All changes via feature branches and pull requests
- Author MUST self-review before requesting review
- PR MUST include:
  - Test results and coverage report
  - Updated documentation if CLI interface changes
  - Description of changes and testing approach

**Review Checklist**:
- [ ] Code follows PEP 8 and type annotations present
- [ ] Tests included and passing (coverage meets thresholds)
- [ ] No security vulnerabilities (input validation, path traversal, etc.)
- [ ] Performance acceptable (no obvious inefficiencies)
- [ ] Documentation updated if needed
- [ ] **Files in correct directories per Principle VI**

### Technical Debt Management

**TODO Comments**: MUST include reference and deadline:
```python
# TODO(2025-12-31): Replace with streaming parser for large files
```

**Workarounds**: Document with explanation and remediation plan:
```python
# WORKAROUND: PyPDF2 fails on password-protected PDFs
# Plan: Migrate to pdfplumber by Phase 3 (supports encryption)
```

**Dependencies**:
- Review and update quarterly
- Security patches applied within 7 days of disclosure
- Pin major versions in `requirements.txt`

**Refactoring**: Allocate 20% of development time to code cleanup and debt reduction

---

## Testing Requirements

### Test Coverage Targets

- **Minimum Overall**: 80% code coverage (enforced by CI/CD)
- **Critical Paths**: 100% coverage for:
  - `src/text_extraction.py`: All file type handlers
  - `src/nlp_processing.py`: Lemmatization, POS tagging
  - `src/level_matching.py`: CEFR level assignment logic
  - `src/phrase_detection.py`: Phrasal verb pattern matching
  - `src/output_generation.py`: All output format writers

### Test Data Requirements

**Test Corpus Structure**:
```
tests/fixtures/
├── small/          # 1-page files (<500 words)
├── medium/         # 20-page files (~5000 words)
├── large/          # 100+ page files (>20000 words)
├── edge_cases/     # Malformed, special chars, multi-language
└── golden/         # Manually verified expected outputs
```

**Required Test Files**:
- Fiction samples (e.g., Pride and Prejudice excerpt)
- Non-fiction samples (e.g., academic article)
- Technical documentation samples
- Edge cases: empty file, single sentence, special Unicode characters

### Continuous Testing

**Pre-Commit Hooks**:
- Run `black`, `isort`, `pylint`, `flake8`
- Run quick unit tests (<10 seconds)
- Check file placement (reject files in wrong directories)

**CI/CD Pipeline**:
- Full test suite on every push (GitHub Actions or equivalent)
- Performance benchmarks tracked (compare against baseline)
- Coverage report uploaded to dashboard

**Performance Monitoring**:
- Alert if processing time for benchmark file increases >20%
- Track memory usage for large files (alert if exceeds 500MB)

---

## Performance Standards

### Processing Speed Targets

| File Size | Target Time | Max Acceptable |
|-----------|-------------|----------------|
| Small (<5 pages) | <3 seconds | 5 seconds |
| Medium (20-50 pages) | <20 seconds | 30 seconds |
| Large (100+ pages) | <60 seconds | 90 seconds |

**Measurement**: Total wall-clock time from CLI invocation to output file written

### Optimization Guidelines

**Required Optimizations**:
1. **Global Model Loading**: Load spaCy model once per session (not per file)
2. **Batch Processing**: Process sentences in batches of 100 for spaCy pipeline
3. **Dictionary Caching**: Cache vocabulary lookups for repeated words (use `functools.lru_cache`)
4. **Lazy Loading**: Load data files (vocabulary lists) only when needed

**Profiling Before Optimization**:
- Use `cProfile` to identify bottlenecks
- Only optimize after profiling confirms hotspot
- Document optimization reasoning in comments

**Forbidden Optimizations**:
- No multiprocessing in MVP (Phase 1) - adds complexity
- No caching to disk (increases complexity, security risks)
- No sacrificing readability for minor speed gains (<10%)

### Scalability Considerations

**Current Design (Phase 1-2)**:
- Single-threaded processing (simple, maintainable)
- Sequential file processing (batch mode for multiple files)
- Memory limit: Gracefully reject files exceeding 50MB with clear error message

**Future-Ready Design** (Phase 3+):
- Architecture allows adding multiprocessing (separate module)
- Can add streaming parser for very large files
- Can add local database for vocabulary cache

**Resource Limits**:
- Peak memory usage: <500MB for files up to 200 pages
- Disk usage: No temporary files left after processing (cleanup in `finally` blocks)
- CPU: Single core usage acceptable (no parallelism required for MVP)

---

## Data Management

### Data Source Requirements

**Required Data Files**:
1. **Cambridge CEFR Vocabulary Lists** (A1-C2)
   - Location: `data/vocabulary/cambridge_*.csv` (per Principle VI)
   - Format: CSV or JSON
   - Source: English Vocabulary Profile or equivalent open dataset
   - Required fields: `word`, `level`, `word_type`, `exam` (KET/PET/FCE/CAE/CPE)
   - Update frequency: Quarterly review for additions

2. **Phrasal Verb Dictionary**
   - Location: `data/phrasal_verbs.json` (per Principle VI)
   - Format: JSON
   - Minimum coverage: 500 common phrasal verbs
   - Required fields: `phrase`, `type` (separable/inseparable), `level`
   - Source: Open phrasal verb databases (e.g., Cambridge Phrasal Verbs)

3. **Chinese Definitions** (Optional)
   - Location: `data/chinese_definitions.json` (per Principle VI)
   - Format: JSON (word → definition mapping)
   - Source: StarDict open dictionaries or manual curation
   - Fallback: Online API (Youdao/Baidu) with rate limiting and error handling

**Data File Versioning**:
- Track data file versions in `config/config.yaml`
- Include version in output metadata (`vocabulary_list_version: "2025-Q1"`)
- Document data sources in `docs/data_sources.md`

### Data Validation

**Startup Validation**:
- Verify vocabulary list files exist in `data/vocabulary/` and parse correctly
- Check schema: required fields present, no missing levels
- Detect duplicates within lists (alert if found)
- Cross-reference: phrasal verbs reference valid words

**Runtime Validation**:
- Validate input files before processing (magic number, encoding)
- Reject files exceeding size limits (50MB) with clear error
- Sanitize file paths (prevent path traversal)

### Output Data Quality

**Consistency Requirements**:
- Same input file MUST produce identical output (deterministic)
- No randomness in processing or output ordering (sort deterministically)

**Completeness Requirements**:
- Every unique word MUST be assigned a level or marked as "C2+" (out-of-syllabus)
- Example sentences MUST be actual excerpts from source text (no fabrication)
- Frequency counts MUST match actual occurrence counts

**Format Validation**:
- JSON output MUST validate against schema (use `jsonschema`)
- CSV output MUST have consistent columns and proper escaping
- Markdown output MUST render correctly in common viewers

---

## Security & Privacy

### Input Validation

**File Type Verification**:
- Verify file extensions match actual content (magic number check)
- Reject unexpected file types with clear error message

**Size Limits**:
- Reject files exceeding 50MB (prevents DoS, memory exhaustion)
- Warn if file >10MB (may take longer to process)

**Malicious Content Protection**:
- Basic checks for embedded scripts in PDFs (use safe parsing libraries)
- No execution of macros from DOCX files
- Sanitize all file paths provided by user (prevent directory traversal)

**Content Safety**:
- No assumptions about text content safety
- Handle Unicode properly (avoid encoding crashes)
- Gracefully handle null bytes and control characters

### Data Privacy

**Local Processing Default**:
- All core processing happens locally (no external API calls by default)
- No telemetry, usage statistics, or tracking
- No network access except optional translation API (user-controlled)

**User Control**:
- Clear warnings if using online translation API
- API keys stored in `config/` directory, never in `src/` (per Principle VI)
- Option to disable all network features (`--offline` flag)

**Temporary Files**:
- Clean up all temporary files after processing (use `tempfile` module)
- No sensitive data written to disk unencrypted
- No log files containing file contents

---

## Governance

### Constitution Authority

**Supreme Document**: This constitution is the highest authority for all technical decisions in this project. It overrides all other coding practices, preferences, or historical decisions.

**Compliance Required**:
- All pull requests MUST demonstrate constitutional compliance
- Code reviews MUST verify adherence to principles and standards
- Any deviation requires explicit justification and approval

**Exception Process**:
- Violations MUST be documented in PR description
- Include: rationale, impact analysis, duration (temporary vs. permanent)
- Temporary violations MUST include remediation plan with deadline

**Living Document**: This constitution is updated quarterly based on lessons learned, new requirements, or changed circumstances.

### Amendment Process

**Proposal Requirements**:
- Written proposal including:
  - Current text vs. proposed text
  - Rationale for change
  - Impact analysis (code, tests, documentation)
  - Migration plan if breaking change

**Review Period**:
- 7-day discussion period for proposed amendments
- Gather feedback, identify concerns, refine proposal

**Approval**:
- For personal project: self-approval after reflection period
- For team project: consensus required (all team members agree)

**Documentation**:
- All amendments logged in this file's sync impact report header
- Version incremented per semantic versioning rules
- Announcement to team (if applicable) with transition timeline

### Review Checkpoints

**Feature Completion Review**:
- Before merging feature branch, verify:
  - [ ] Code quality standards met (pylint score ≥8.5)
  - [ ] Test coverage targets met (80% overall, 100% critical paths)
  - [ ] Performance targets met (file size benchmarks)
  - [ ] Security validation passed (input validation, no vulnerabilities)
  - [ ] Documentation updated (CLI help, README if needed)
  - [ ] **Files in correct directories (Principle VI compliance)**

**Release Preparation Audit**:
- Before version release:
  - Constitutional compliance audit (all principles followed)
  - Full test suite passes
  - Performance benchmarks within targets
  - Data source versions documented
  - **Project structure validation (no files in wrong locations)**

**Monthly Review**:
- Review metrics:
  - Test coverage trends
  - Performance benchmark trends
  - Code quality scores (pylint/flake8)
  - Technical debt items (TODO count, age)
- Identify issues requiring attention

**Incident Retrospectives**:
- After bugs or production issues:
  - Root cause analysis
  - Constitutional gap analysis (what principle could prevent recurrence?)
  - Update constitution if systemic issue identified

---

**Version**: 1.1.0
**Ratified**: 2025-11-03
**Last Amended**: 2025-11-03
**Status**: Active

**Next Review Date**: 2026-02-03 (Quarterly Review)
