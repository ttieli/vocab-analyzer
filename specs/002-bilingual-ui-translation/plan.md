# Implementation Plan: Bilingual UI with CEFR Descriptions and Local Translation

**Branch**: `002-bilingual-ui-translation` | **Date**: 2025-11-04 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/002-bilingual-ui-translation/spec.md`

## Summary

This feature enhances the vocabulary analyzer with three integrated capabilities:

1. **Bilingual UI**: Display all interface text in both English and Chinese using consistent "English / 中文" formatting
2. **CEFR Education**: Provide interactive descriptions for each CEFR level (A1-C2+) to help users understand proficiency characteristics
3. **Local Translation**: Enable on-demand translation of untranslated words, phrases, and example sentences using offline models

**Technical Approach** (based on user recommendations):
- **ECDICT**: Retain existing database for fast base word translations
- **Mdict (.mdx)**: Add optional professional dictionaries (OALD9, LDOCE6, Collins) for enhanced definitions and examples
- **Argos Translate**: Integrate OpenNMT-based offline translation for phrasal verbs and sentences (~50MB English→Chinese model)

This architecture balances performance (ECDICT for common lookups), quality (Mdict for detailed definitions), and flexibility (Argos for dynamic translation), all while maintaining the fully offline requirement.

## Technical Context

**Language/Version**: Python 3.13+ (existing project standard)
**Primary Dependencies**:
- Flask 3.1+ (existing web framework)
- argostranslate 1.9+ (offline translation engine)
- readmdict or python-mdict (Mdict .mdx parser)
- ECDICT (existing - SQLite database)

**Storage**:
- SQLite (ECDICT existing database)
- Mdict .mdx files (100-500MB per dictionary, optional)
- Argos Translate models (~50MB English→Chinese package)
- Translation cache (local JSON/SQLite)
- CEFR descriptions (static JSON/YAML file)

**Testing**: pytest (existing test framework)

**Target Platform**:
- macOS/Linux/Windows (desktop operating systems)
- Web browser (for UI rendering)
- Offline-capable (no internet required after initial setup)

**Project Type**: Web application (enhancing existing Flask app from Feature 001)

**Performance Goals**:
- UI bilingual text rendering: <50ms overhead
- CEFR description display: <100ms (tooltip/modal interaction)
- Translation operations: <3 seconds per request (per spec SC-003)
- Translation cache hit: <10ms response time
- Model loading time: <5 seconds on first translation request

**Constraints**:
- **Fully offline**: No API calls, all processing local
- **Memory**: Models loaded lazily, max 200MB additional RAM for Argos model
- **Storage**: User storage requirement 500MB-1GB (models + optional dictionaries)
- **Compatibility**: Works with existing vocabulary analyzer data structures
- **UI responsiveness**: Bilingual text must not break existing layouts

**Scale/Scope**:
- UI elements: ~50 text strings to translate (buttons, labels, headings, errors)
- CEFR levels: 7 level descriptions (A1, A2, B1, B2, C1, C2, C2+)
- Translation requests: Assume 10-50 translations per user session (cached)
- Mdict dictionaries: Optional, user-provided (3 recommended options)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Compliance Analysis

✅ **Principle I: Simplicity & Maintainability**
- PASS: Using existing dependencies where possible (ECDICT, Flask)
- PASS: Adding minimal new dependencies (argostranslate, mdict parser)
- PASS: Each module has single responsibility (translation service, UI renderer, CEFR content loader)
- CONSIDERATION: Argos Translate is a new NLP dependency - justified for offline requirement

✅ **Principle II: Modular Architecture**
- PASS: Translation feature will be separate module `src/vocab_analyzer/translation/`
- PASS: Bilingual UI handled in existing `src/vocab_analyzer/web/` with template updates
- PASS: CEFR descriptions as static data service
- PASS: No cross-module dependencies - translation module is independent

✅ **Principle III: Data Quality First**
- PASS: Translation quality tracked (FR-014: cache translations for consistency)
- PASS: Fallback chain: ECDICT → Mdict → Argos Translate ensures coverage
- PASS: All translations cached locally for consistency and traceability

✅ **Principle IV: Test-Driven Development**
- PASS: Translation accuracy tests required (80-90% quality threshold)
- PASS: UI bilingual rendering tests (all strings present)
- PASS: CEFR description accessibility tests
- PASS: Offline mode tests (no network calls)

✅ **Principle V: CLI-First Design**
- PASS: Primary interface remains CLI
- PASS: Web interface is supplementary (existing from Feature 001)
- NOTE: This feature enhances web UI specifically, CLI not affected

✅ **Principle VI: Project Organization & Structure**
- PASS: New translation module goes in `src/vocab_analyzer/translation/`
- PASS: Mdict dictionaries stored in `data/dictionaries/` (optional, user-provided)
- PASS: Argos models in `data/translation_models/`
- PASS: CEFR descriptions in `data/cefr_definitions.json`
- PASS: Translation cache in local storage (not in repo)
- PASS: No root directory clutter

### Gate Evaluation

**VERDICT**: ✅ **PASS** - All constitutional principles satisfied

**Notes**:
- New `translation` module aligns with modular architecture principle
- Offline requirement justifies Argos Translate dependency
- Data files properly organized in `data/` directory
- Tests required for translation accuracy and UI rendering

## Project Structure

### Documentation (this feature)

```text
specs/002-bilingual-ui-translation/
├── plan.md              # This file
├── research.md          # Phase 0: Translation tech evaluation
├── data-model.md        # Phase 1: Translation cache, CEFR definitions
├── quickstart.md        # Phase 1: Setup guide for Argos + Mdict
├── contracts/           # Phase 1: Translation API contracts
│   └── translation-api.yaml  # Translation service endpoints
└── tasks.md             # Phase 2: Implementation tasks (created by /speckit.tasks)
```

### Source Code (repository root)

```text
src/vocab_analyzer/
├── web/                 # Existing web module (Feature 001)
│   ├── app.py           # Modified: add translation routes
│   ├── routes.py        # Modified: bilingual template rendering
│   ├── templates/       # Modified: bilingual UI strings
│   │   └── index.html   # Updated with bilingual text
│   └── static/
│       ├── app.js       # Modified: translation UI handlers
│       └── styles.css   # Modified: bilingual layout styles
│
├── translation/         # NEW module for translation features
│   ├── __init__.py
│   ├── translator.py    # Core translation service (Argos Translate)
│   ├── dictionary.py    # ECDICT + Mdict integration
│   ├── cache.py         # Translation cache manager
│   └── cefr_loader.py   # CEFR description loader
│
└── models.py            # Modified: add TranslationCache, CEFRDescription

data/
├── cefr_definitions.json     # NEW: Bilingual CEFR level descriptions
├── translation_models/       # NEW: Argos Translate en→zh model
│   └── .gitignore           # Ignore model files (user downloads)
├── dictionaries/            # NEW: Optional Mdict .mdx files
│   ├── .gitignore          # Ignore .mdx files (user-provided)
│   └── README.md           # Instructions for obtaining dictionaries
└── vocabulary/              # Existing: ECDICT, Cambridge lists

tests/
├── translation/             # NEW: Translation module tests
│   ├── test_translator.py   # Argos Translate integration tests
│   ├── test_dictionary.py   # Mdict + ECDICT tests
│   ├── test_cache.py        # Translation cache tests
│   └── test_cefr_loader.py  # CEFR description loading tests
│
└── web/                     # Existing: Web module tests
    ├── test_routes.py       # Modified: bilingual UI tests
    └── test_translation_ui.py  # NEW: Translation UI integration tests
```

**Structure Decision**: Web application structure (Option 2 adapted)

This feature enhances the existing Flask web application (Feature 001) by adding:
1. A new `translation/` module under `src/vocab_analyzer/` following modular architecture principle
2. Modified web templates and static files for bilingual UI
3. New data files in `data/` directory (CEFR descriptions, translation models, dictionaries)
4. Corresponding test files in `tests/translation/`

All changes comply with Principle VI (Project Organization) - no root directory clutter, proper file placement.

**Principle VI Subdirectory Justification** (Constitutional Compliance Verification):
The plan introduces subdirectory structure (`src/vocab_analyzer/translation/`). Constitution Principle VI states: "No subdirectories unless >10 modules (keep flat for simplicity)". Project verification confirms **37 Python modules** exist in `src/vocab_analyzer/`, exceeding the 10-module threshold. Therefore, subdirectory organization is **explicitly permitted** by the constitution.

## Complexity Tracking

> No constitutional violations requiring justification

The plan follows all six constitutional principles:
- Simplicity maintained (focused dependencies, clear module boundaries)
- Modular architecture preserved (independent translation module)
- Data quality enforced (translation caching, fallback chain)
- TDD approach (comprehensive testing plan)
- CLI-first maintained (web is supplementary)
- Clean structure (proper file organization)

## Phase 0: Research & Technology Selection

### Research Questions

Based on user recommendations and technical context, the following research is required:

1. **Argos Translate Integration**
   - How to download and install English→Chinese language package programmatically?
   - How to initialize translator efficiently (lazy loading vs. eager loading)?
   - What is actual model size and memory footprint?
   - Translation quality benchmarks for vocabulary vs. sentences?
   - Error handling for out-of-vocabulary terms?

2. **Mdict Integration**
   - Which Python library is most stable: `python-mdict` vs. `readmdict`?
   - How to parse .mdx files efficiently (stream vs. load-all)?
   - How to handle missing .mdx files gracefully (optional feature)?
   - Query performance: lookup time for single word?
   - Format of definition data (HTML? Plain text? Structured?)?

3. **ECDICT Integration**
   - Current usage in existing codebase (is it already integrated)?
   - Query interface and response format?
   - Coverage for phrasal verbs and collocations?
   - Performance characteristics (indexed lookups)?

4. **Translation Fallback Strategy**
   - Optimal fallback order: ECDICT → Mdict → Argos?
   - How to detect "no translation available" at each level?
   - Caching strategy across fallback chain?
   - User preferences for dictionary priority?

5. **Bilingual UI Implementation**
   - Flask template i18n patterns (Jinja2 best practices)?
   - JavaScript localization for dynamic content?
   - CSS layout considerations for Chinese text (longer than English)?
   - Accessibility considerations (screen readers with bilingual text)?

6. **CEFR Description Content**
   - Source for authoritative CEFR level descriptions?
   - How detailed should descriptions be (brief vs. comprehensive)?
   - Static JSON file vs. database storage?
   - UI pattern for displaying descriptions (tooltip, modal, sidebar)?

### Research Tasks

The following research will be conducted and documented in `research.md`:

- [ ] Argos Translate API evaluation and sample integration code
- [ ] Mdict library comparison (`python-mdict` vs. `readmdict`) with benchmarks
- [ ] ECDICT current integration analysis (review existing code)
- [ ] Translation fallback chain design and pseudo-code
- [ ] Flask bilingual template patterns and examples
- [ ] CEFR description content sourcing and format design
- [ ] Performance benchmarking plan for translation operations

**Output**: `specs/002-bilingual-ui-translation/research.md` with decisions, rationale, and code examples

## Phase 1: Design & Contracts

**Prerequisites**: `research.md` complete with all technology decisions finalized

### Data Model Design

**Entities to Model** (from feature spec):

1. **Translation Cache**
   - Purpose: Store user-generated translations to avoid redundant operations
   - Fields: source_text, target_text, timestamp, translation_type, source (ecdict/mdict/argos)
   - Persistence: Local JSON file or SQLite table

2. **CEFR Level Definition**
   - Purpose: Store bilingual descriptions for each CEFR level
   - Fields: level_code, name_en, name_cn, description_en, description_cn, vocabulary_size, example_contexts
   - Persistence: Static JSON file in `data/`

3. **Translation Request**
   - Purpose: Represent a single translation operation (runtime only)
   - Fields: source_text, translation_type (word/phrase/sentence), user_context
   - Lifecycle: Created on-demand, processed, discarded (no persistence)

4. **Mdict Dictionary Reference**
   - Purpose: Track available Mdict dictionaries
   - Fields: dictionary_name, file_path, priority, is_available
   - Persistence: Configuration file or auto-detected

**Output**: `specs/002-bilingual-ui-translation/data-model.md` with detailed entity specifications

### API Contracts

**Endpoints to Define** (based on functional requirements):

1. **POST /api/translate**
   - Request: `{ "text": "run out", "type": "phrase", "context": "word_detail" }`
   - Response: `{ "translation": "用完; 耗尽", "source": "argos", "cached": false }`
   - Purpose: Translate untranslated content (FR-009, FR-010, FR-011)

2. **GET /api/cefr/:level**
   - Request: Level code (A1, A2, B1, B2, C1, C2, C2+)
   - Response: `{ "level": "B2", "name_en": "Upper Intermediate", "name_cn": "中高级", "description_en": "...", "description_cn": "...", "vocabulary_size": "3000-4000" }`
   - Purpose: Fetch CEFR level descriptions (FR-005, FR-006)

3. **GET /api/ui/strings**
   - Request: None (or optional locale parameter for future)
   - Response: `{ "upload_title": "Vocabulary Analyzer / 词汇分析器", "choose_file": "Choose a file... / 选择文件...", ... }`
   - Purpose: Provide bilingual UI strings for dynamic rendering (FR-001)

**Output**: `specs/002-bilingual-ui-translation/contracts/translation-api.yaml` (OpenAPI specification)

### Quickstart Guide

**Content**:
1. Install Argos Translate and download English→Chinese model
2. (Optional) Obtain and configure Mdict dictionaries
3. Verify ECDICT integration
4. Test translation fallback chain
5. Run bilingual UI in development mode

**Output**: `specs/002-bilingual-ui-translation/quickstart.md`

### Agent Context Update

After completing design artifacts, run:

```bash
.specify/scripts/bash/update-agent-context.sh claude
```

This will add the following to `.specify/memory/claude.md`:
- Argos Translate usage patterns
- Mdict integration approach
- Translation module architecture
- Bilingual UI rendering strategy

## Phase 2: Task Generation

**Note**: Task generation is handled by `/speckit.tasks` command (separate from this plan).

Expected task categories based on this plan:

1. **Phase 1: Translation Module Foundation** (~8 tasks)
   - Setup Argos Translate integration
   - Implement Mdict dictionary loader
   - Create translation cache manager
   - Build ECDICT query wrapper
   - Implement fallback translation chain
   - Unit tests for translation module

2. **Phase 2: CEFR Descriptions** (~4 tasks)
   - Create CEFR descriptions JSON file (bilingual content)
   - Implement CEFR description loader service
   - Add API endpoint for CEFR lookups
   - Unit tests for CEFR module

3. **Phase 3: Bilingual UI** (~6 tasks)
   - Update all HTML templates with bilingual strings
   - Update CSS for bilingual text layout
   - Create UI strings configuration file
   - Implement JavaScript i18n helpers
   - Add bilingual error messages
   - UI rendering tests

4. **Phase 4: Translation UI Integration** (~5 tasks)
   - Add "Translate" buttons to word detail modals
   - Implement translation request handlers
   - Add loading states and error handling
   - Integrate translation cache display
   - End-to-end translation workflow tests

5. **Phase 5: CEFR Education UI** (~4 tasks)
   - Add CEFR info icons/tooltips to level badges
   - Implement CEFR description modal/popup
   - Style CEFR description displays
   - Accessibility tests for CEFR UI

6. **Phase 6: Polish & Documentation** (~3 tasks)
   - Update README with translation feature
   - Create Mdict dictionary setup guide
   - Performance testing and optimization
   - Final integration testing

**Total**: ~30 tasks estimated

## Re-Check Constitution After Design

*This section filled after Phase 1 design completion*

### Post-Design Compliance Review

✅ **Principle I: Simplicity & Maintainability** (Re-checked)
- PASS: Translation module has clear single responsibility
- PASS: Dependencies justified (Argos for offline, Mdict for quality)
- PASS: No premature optimization (simple caching, lazy model loading)

✅ **Principle II: Modular Architecture** (Re-checked)
- PASS: `translation/` module is independent and testable
- PASS: Clear interfaces defined in contracts/translation-api.yaml
- PASS: No tight coupling with web module (API-based communication)

✅ **Principle III: Data Quality First** (Re-checked)
- PASS: Translation fallback ensures coverage (ECDICT → Mdict → Argos)
- PASS: Translation cache provides consistency and traceability
- PASS: Source tracking (which dict/model provided translation)

✅ **Principle IV: Test-Driven Development** (Re-checked)
- PASS: Comprehensive test plan across all modules
- PASS: Unit tests for translation, cache, CEFR loader
- PASS: Integration tests for UI and translation workflow
- PASS: Performance tests for translation operations (<3s requirement)

✅ **Principle V: CLI-First Design** (Re-checked)
- PASS: CLI not affected, remains primary interface
- PASS: Web UI enhancement is supplementary

✅ **Principle VI: Project Organization & Structure** (Re-checked)
- PASS: All new files in proper locations:
  - Source: `src/vocab_analyzer/translation/`
  - Data: `data/cefr_definitions.json`, `data/translation_models/`, `data/dictionaries/`
  - Tests: `tests/translation/`
- PASS: No root directory clutter
- PASS: `.gitignore` updated for model files and optional dictionaries

### Final Gate Evaluation

**VERDICT**: ✅ **PASS** - Design maintains constitutional compliance

The design successfully balances:
- User requirements (offline translation, bilingual UI, CEFR education)
- Constitutional principles (simplicity, modularity, data quality, clean structure)
- Technical constraints (performance, storage, memory)

**Ready for**: `/speckit.tasks` to generate detailed implementation tasks

---

**Plan Status**: ✅ Complete (Phases 0-1 designed, ready for task generation)
**Next Command**: `/speckit.tasks` to create task breakdown from this plan
