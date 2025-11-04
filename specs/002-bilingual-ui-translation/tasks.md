# Implementation Tasks: Bilingual UI with CEFR Descriptions and Local Translation

**Feature Branch**: `002-bilingual-ui-translation`
**Created**: 2025-11-04
**Status**: Ready for Implementation
**Related**: [spec.md](./spec.md) | [plan.md](./plan.md) | [research.md](./research.md) | [data-model.md](./data-model.md)

---

## Feature Summary

This feature adds a bilingual English/Chinese interface with local offline translation capabilities to the vocabulary analyzer. The system uses a three-tier fallback chain for translations:

1. **ECDICT** (Primary) - Fast dictionary lookup for common words (<1ms)
2. **Mdict** (Optional) - Professional dictionaries for detailed definitions (~10ms)
3. **Argos Translate** (Fallback) - Neural machine translation for any content (~100ms)

**Key Capabilities**:
- Bilingual UI showing English and Chinese simultaneously
- CEFR level descriptions with educational tooltips and modals
- On-demand translation for untranslated words, phrases, and sentences
- Persistent translation cache to avoid redundant operations
- 100% offline operation (no internet required)

**User Stories**:
- **US1 (P1)**: Bilingual Interface Navigation - All UI text in English/Chinese
- **US2 (P2)**: CEFR Level Education - Interactive level descriptions with examples
- **US3 (P1)**: Local Translation - Translate untranslated content offline

---

## Task Organization

Tasks are organized into 6 phases, with user stories implemented independently:

- **Phase 1**: Setup & Dependencies (Project initialization)
- **Phase 2**: Foundational Infrastructure (Core services used by all stories)
- **Phase 3**: User Story 1 (P1) - Bilingual Interface Navigation
- **Phase 4**: User Story 3 (P1) - Local Translation of Untranslated Content
- **Phase 5**: User Story 2 (P2) - CEFR Level Education
- **Phase 6**: Polish & Documentation (Final touches)

**Parallelization Strategy**: Tasks marked with `[P]` can be executed in parallel with other `[P]` tasks in the same phase.

---

## Phase 1: Setup & Dependencies

**Goal**: Initialize project environment and install required dependencies.

**Dependencies**: None (entry point)

### Tasks

- [X] T001 Install argostranslate package in requirements.txt
  - Add `argostranslate>=1.9.0` to requirements.txt
  - Verify installation with `import argostranslate`

- [X] T002 Install mdict-query library from GitHub
  - Add `readmdict>=0.1.0` to requirements.txt (replaced mdict-query)
  - Verify with `import readmdict`

- [X] T003 Create data directory structure for translation files
  - Create `data/translation_models/` with .gitignore
  - Create `data/dictionaries/` with README.md for user instructions
  - Create `data/cefr_data/` for CEFR definitions

- [X] T004 Download and install Argos Translate English→Chinese model
  - Create `scripts/setup_translation.py` to automate model download
  - Test model loading and verify translation works
  - Expected: ~100MB download, 2-4 second first translation

- [X] T005 Create initial translation cache file
  - Initialize `data/translation_cache.json` with empty structure
  - Include version, metadata, and entries fields
  - Set proper file permissions (644)

---

## Phase 2: Foundational Infrastructure

**Goal**: Build core translation services and data models that support all user stories.

**Dependencies**: Phase 1 complete

### Tasks

- [X] T006 Create TranslationCache entity class in src/vocab_analyzer/translation/cache.py
  - Implement get(), set(), exists(), clear_old(), save(), load() methods
  - Use cache key format: `{translation_type}:{lowercase_text}`
  - Include validation rules from data-model.md

- [X] T007 [P] Write unit tests for TranslationCache in tests/translation/test_cache.py
  - Test cache CRUD operations
  - Test cache expiration (30-day default)
  - Test cache persistence to/from JSON
  - **Coverage**: Minimum 80% enforced by CI (pytest-cov with --cov-fail-under=80)

- [X] T008 Create ArgosTranslator service class in src/vocab_analyzer/translation/translator.py
  - Implement lazy loading strategy (load model on first use)
  - Add safe_translate() with error handling
  - Support word, phrase, and sentence translation types
  - Maximum text length: 500 characters

- [X] T009 [P] Write unit tests for ArgosTranslator in tests/translation/test_translator.py
  - Test lazy model loading
  - Test translation for words, phrases, sentences
  - Test error handling (empty text, too long, model not installed)
  - Test translation caching
  - **Coverage**: Minimum 80% enforced by CI (pytest-cov with --cov-fail-under=80)

- [X] T010 Create MdictDictionary manager class in src/vocab_analyzer/translation/dictionary.py
  - Implement auto-discovery of .mdx files in data/dictionaries/
  - Add lazy loading with SQLite indexing
  - Handle missing dictionaries gracefully
  - Implement query_word() with priority-based lookup

- [X] T011 [P] Write unit tests for MdictDictionary in tests/translation/test_dictionary.py
  - Test dictionary discovery
  - Test lazy loading and indexing
  - Test word lookup with case-insensitivity
  - Test graceful degradation when no dictionaries present
  - **Coverage**: Minimum 80% enforced by CI (pytest-cov with --cov-fail-under=80)

- [X] T012 Create TranslationChain fallback service in src/vocab_analyzer/translation/fallback.py
  - Implement ECDICT → Mdict → Argos fallback logic
  - Add TranslationResult class with source tracking
  - Include confidence scores: ECDICT (0.95), Mdict (0.90), Argos (0.70)
  - Integrate with TranslationCache for automatic caching

- [X] T013 [P] Write unit tests for TranslationChain in tests/translation/test_fallback.py
  - Test fallback order execution
  - Test cache hit bypasses fallback
  - Test each tier independently
  - Test graceful degradation when tiers unavailable
  - **Coverage**: Minimum 80% enforced by CI (pytest-cov with --cov-fail-under=80)

- [X] T014 Create translation configuration loader in src/vocab_analyzer/translation/config.py
  - Load settings from data/translation_config.yaml
  - Include cache settings, dictionary priorities, performance limits
  - Provide default values if config missing

---

## Phase 3: User Story 1 (P1) - Bilingual Interface Navigation

**Goal**: Implement bilingual UI showing all interface text in English and Chinese simultaneously.

**Dependencies**: Phase 2 complete

**Independent Test**: Navigate all pages and verify every UI element displays both English and Chinese text.

### Tasks

- [X] T015 Create bilingual UI strings data file in data/ui_strings.json
  - Include all categories: navigation, buttons, labels, errors, loading
  - Follow BilingualString schema from data-model.md
  - Cover ~50 UI strings for complete interface

- [X] T016 Create BilingualStringLoader class in src/vocab_analyzer/translation/strings.py
  - Implement load(), get_bilingual(), get_all_strings(), format_bilingual()
  - Cache strings in memory after loading
  - Provide fallback for missing strings

- [X] T017 [P] Write unit tests for BilingualStringLoader in tests/translation/test_strings.py
  - Test string loading from JSON
  - Test filtering by category
  - Test bilingual formatting with separator
  - **Coverage**: Minimum 80% enforced by CI (pytest-cov with --cov-fail-under=80)

- [ ] T018 Update base HTML template with bilingual structure in src/vocab_analyzer/web/templates/base.html
  - Add bilingual title pattern: "English / 中文"
  - Update navigation menu with bilingual links
  - Include bilingual footer

- [ ] T019 Update upload page template in src/vocab_analyzer/web/templates/upload.html
  - Bilingual page heading
  - Bilingual form labels and hints
  - Bilingual file format description
  - Bilingual submit button

- [ ] T020 Update results page template in src/vocab_analyzer/web/templates/results.html
  - Bilingual section headings (Statistics, CEFR Distribution, Word List)
  - Bilingual table headers
  - Bilingual status messages

- [ ] T021 Create CSS styles for bilingual text in src/vocab_analyzer/web/static/styles.css
  - Add .bilingual-text, .bilingual-heading, .bilingual-button classes
  - Support responsive layout (stack vertically on mobile)
  - Include Chinese font stack (PingFang SC, Noto Sans SC, Microsoft YaHei)
  - Handle text overflow for longer Chinese translations

- [ ] T022 [P] Create JavaScript bilingual utilities in src/vocab_analyzer/web/static/bilingual.js
  - Implement createBilingualText() helper
  - Add showBilingualError() for error messages
  - Include bilingual loading states

- [ ] T023 Update Flask routes to pass bilingual strings in src/vocab_analyzer/web/routes.py
  - Load BilingualStringLoader at startup
  - Pass UI strings to all templates
  - Handle bilingual error messages

- [ ] T024 Add API endpoint GET /api/ui/strings in src/vocab_analyzer/web/app.py
  - Implement endpoint per contracts/translation-api.yaml
  - Support optional category filter
  - Return bilingual strings in JSON format

- [ ] T025 [P] Write integration tests for bilingual UI in tests/web/test_bilingual_ui.py
  - Test all pages render with bilingual text
  - Test navigation menu accessibility
  - Test responsive layout on mobile viewport
  - Test accessibility with lang attributes
  - **Coverage**: Minimum 80% enforced by CI (pytest-cov with --cov-fail-under=80)

- [ ] T026 Test bilingual UI in multiple browsers
  - Chrome: Verify text rendering and Chinese fonts
  - Firefox: Verify text rendering and Chinese fonts
  - Safari: Verify text rendering and Chinese fonts
  - Edge: Verify text rendering and Chinese fonts
  - Document any browser-specific issues

---

## Phase 4: User Story 3 (P1) - Local Translation of Untranslated Content

**Goal**: Implement on-demand translation for words, phrases, and sentences without Chinese translations using local offline models.

**Dependencies**: Phase 2 complete (can run parallel with Phase 3)

**Independent Test**: Identify untranslated content, click "Translate" button, verify translation appears instantly without network requests.

### Tasks

- [ ] T027 Add translation API endpoint POST /api/translate in src/vocab_analyzer/web/app.py
  - Implement per contracts/translation-api.yaml specification
  - Validate request body (source_text, translation_type)
  - Return TranslationResponse with source and confidence score
  - Handle errors with bilingual error messages

- [ ] T028 [P] Write unit tests for translation API in tests/web/test_translation_api.py
  - Test valid translation requests for word, phrase, sentence
  - Test validation errors (empty text, too long, invalid type)
  - Test cache hit returns cached result
  - Test fallback chain integration
  - **Coverage**: Minimum 80% enforced by CI (pytest-cov with --cov-fail-under=80)

- [ ] T029 Add "Translate" buttons to word detail modal in src/vocab_analyzer/web/templates/word_detail.html
  - Show button when translation missing
  - Button text: "Translate / 翻译"
  - Include loading state: "Translating... / 翻译中..."

- [ ] T030 Add "Translate" buttons to phrase list view
  - Detect phrases without Chinese translations
  - Add translate button with icon
  - Display translation result inline

- [ ] T031 Add "Translate" buttons to example sentences
  - Detect sentences without translations
  - Add "Translate this sentence / 翻译此句" button
  - Display translation below original sentence

- [ ] T032 Create JavaScript translation handler in src/vocab_analyzer/web/static/translation.js
  - Implement handleTranslate() function
  - Call POST /api/translate endpoint
  - Show loading state during translation
  - Display result with source indicator
  - Handle errors with bilingual messages

- [ ] T033 Add translation result display components
  - Create translation result card/box
  - Show source: "ECDICT / ECDICT词典", "Mdict / Mdict词典", "Argos / Argos翻译"
  - Include confidence indicator
  - Cache translations for subsequent views

- [ ] T034 [P] Write integration tests for translation UI in tests/web/test_translation_ui.py
  - Test translate button appears for untranslated content
  - Test translation request flow
  - Test loading state transitions
  - Test translation result display
  - Test error handling
  - **Edge Case Tests** (from spec.md Edge Cases section):
    1. Rare/technical vocabulary: Test Argos fallback for words not in ECDICT/Mdict
    2. Long text (>500 chars): Verify truncation or split handling, display error message
    3. Insufficient memory: Simulate low-memory condition, verify graceful degradation
    4. Chinese text overflow: Test UI layout with very long Chinese translations (>100 chars)
    5. Rapid CEFR description clicks: Test no race conditions or duplicate modal renders
  - **Coverage**: Minimum 80% enforced by CI (pytest-cov with --cov-fail-under=80)

- [ ] T035 Test offline translation functionality
  - Disconnect network (WiFi off or browser offline mode)
  - Verify translations still work
  - Check no network errors in console
  - **Performance Measurement** (FR-017 validation):
    - Instrument code with `time.time()` before button click and after result display
    - Log end-to-end translation time to console
    - First translation (cold start): MUST be ≤3.0 seconds
    - Cached translation: MUST be ≤0.5 seconds
    - FAIL test if any translation exceeds threshold
    - Record results in test report

- [ ] T036 Implement translation performance optimization
  - Ensure model lazy loading works correctly
  - Verify cache hit avoids redundant translations
  - Test memory usage (<500MB with Argos loaded)
  - Profile translation speed for typical use cases

---

## Phase 5: User Story 2 (P2) - CEFR Level Education

**Goal**: Provide interactive CEFR level descriptions to help users understand proficiency levels.

**Dependencies**: Phase 2 complete (can run after Phase 3 or 4)

**Independent Test**: Click any CEFR level badge and verify comprehensive description popup appears with bilingual content.

### Tasks

- [ ] T037 Create CEFR definitions data file in data/cefr_definitions.json
  - Include all 7 levels: A1, A2, B1, B2, C1, C2, C2+
  - Follow CEFRDefinition schema from data-model.md
  - Include bilingual descriptions, vocabulary sizes, example words, learning contexts
  - Source content from research.md (Council of Europe CEFR)

- [ ] T038 Create CEFRDefinitionLoader class in src/vocab_analyzer/translation/cefr_loader.py
  - Implement load(), get_by_level(), get_all(), validate_all() methods
  - Load definitions at application startup
  - Cache in memory (small data ~20KB)

- [ ] T039 [P] Write unit tests for CEFRDefinitionLoader in tests/translation/test_cefr_loader.py
  - Test loading all 7 levels
  - Test get_by_level() for valid and invalid codes
  - Test validation of completeness
  - **Coverage**: Minimum 80% enforced by CI (pytest-cov with --cov-fail-under=80)

- [ ] T040 Add CEFR API endpoint GET /api/cefr/{level} in src/vocab_analyzer/web/app.py
  - Implement per contracts/translation-api.yaml
  - Return CEFRDefinition for specific level
  - Handle 404 for invalid level codes

- [ ] T041 Add CEFR API endpoint GET /api/cefr for all levels
  - Return all 7 CEFR level definitions
  - Include version and last_updated metadata
  - Cache response (static data)

- [ ] T042 [P] Write unit tests for CEFR API in tests/web/test_cefr_api.py
  - Test GET /api/cefr/{level} for all levels
  - Test GET /api/cefr returns all levels
  - Test 404 for invalid level code
  - **Coverage**: Minimum 80% enforced by CI (pytest-cov with --cov-fail-under=80)

- [ ] T043 Update CEFR level badges in results template
  - Add clickable badges with level codes (A1, A2, etc.)
  - Include info icon (ⓘ) to indicate interactive
  - Add data-level attribute for JavaScript handling

- [ ] T044 Create CEFR tooltip component in src/vocab_analyzer/web/templates/components/cefr_tooltip.html
  - Show on hover: level name in English/Chinese
  - Display hint: "Click for details / 点击查看详情"
  - Position tooltip near badge

- [ ] T045 Create CEFR modal component in src/vocab_analyzer/web/templates/components/cefr_modal.html
  - Include modal title with level badge and bilingual name
  - Show full bilingual description
  - Display vocabulary size range
  - List example words
  - Show learning context
  - Add close button: "Close / 关闭"

- [ ] T046 Create CEFR modal JavaScript in src/vocab_analyzer/web/static/cefr.js
  - Implement showCEFRModal(level) to fetch and display level info
  - Call GET /api/cefr/{level} endpoint
  - Populate modal with bilingual content
  - Handle keyboard navigation (Escape to close)
  - Manage focus for accessibility

- [ ] T047 Add CSS styles for CEFR components in src/vocab_analyzer/web/static/styles.css
  - Style level badges with distinct colors per level
  - Style tooltip popup with proper positioning
  - Style modal overlay and content box
  - Ensure responsive design for mobile

- [ ] T048 [P] Write integration tests for CEFR UI in tests/web/test_cefr_ui.py
  - Test CEFR badge rendering
  - Test tooltip appears on hover
  - Test modal opens on click
  - Test modal displays correct bilingual content
  - Test modal closes on button click and Escape key
  - Test accessibility (keyboard navigation, ARIA labels)
  - **Coverage**: Minimum 80% enforced by CI (pytest-cov with --cov-fail-under=80)

- [ ] T049 Test CEFR descriptions content accuracy
  - Review all 7 level descriptions for correctness
  - Verify translations are accurate and natural
  - Confirm example words match level difficulty
  - Check vocabulary size ranges are realistic

---

## Phase 6: Polish & Documentation

**Goal**: Final testing, performance optimization, and documentation.

**Dependencies**: Phases 3, 4, 5 complete

### Tasks

- [ ] T050 [P] Run comprehensive end-to-end tests
  - Upload sample book and analyze vocabulary
  - Test bilingual UI navigation
  - Test CEFR level descriptions for all levels
  - Test translation for words, phrases, sentences
  - Verify offline functionality (no network)
  - Check browser compatibility (Chrome, Firefox, Safari, Edge)

- [ ] T051 [P] Performance testing and optimization
  - Benchmark translation speed for each tier:
    - Run 50 translation requests (10 unique + 40 repeated)
    - Calculate p50, p95, p99 latencies using Python `statistics` module
    - Verify p95 ≤3.0s for first translations, p95 ≤500ms for cached
    - Document results in performance_report.md
  - Measure cache hit rate after typical session (target >80% hits)
  - Profile memory usage with Argos model loaded:
    - Use `memory_profiler` or `tracemalloc` to measure RAM usage
    - Verify Argos model uses <300MB, total app <500MB
  - **Minimum Hardware Validation** (FR-013):
    - Test on 4GB RAM machine or simulate with Docker memory limits
    - Verify model loads in <5 seconds on minimum spec
    - Confirm no OOM errors or crashes
  - Optimize CSS for faster rendering (target <50ms)
  - Ensure lazy loading works correctly

- [ ] T052 Create user-facing documentation in README.md
  - Add "Bilingual UI" section describing feature
  - Document supported languages (English/Chinese)
  - Explain CEFR level system briefly
  - Note offline translation capability

- [ ] T053 Create developer documentation in specs/002-bilingual-ui-translation/implementation-notes.md
  - Document translation fallback chain architecture
  - Explain caching strategy and cache key format
  - Note Argos Translate setup requirements
  - Describe optional Mdict dictionary configuration
  - Include troubleshooting guide

- [ ] T054 Update quickstart.md with final setup instructions
  - Review all setup steps for accuracy
  - Add screenshots or diagrams if helpful
  - Include common troubleshooting issues
  - Verify all commands work as documented

- [ ] T055 Create Mdict dictionary setup guide in data/dictionaries/README.md
  - Explain what Mdict dictionaries are
  - List recommended dictionaries (OALD9, LDOCE6, Collins)
  - Provide instructions for obtaining .mdx files legally
  - Document how to add dictionaries to project
  - Note that dictionaries are optional

- [ ] T056 Add translation cache management documentation
  - Explain cache location and structure
  - Document cache_size and cleanup strategy
  - Provide command to clear cache if needed
  - Note automatic 30-day expiration

- [ ] T057 Write system tests for complete workflows in tests/integration/test_bilingual_workflow.py
  - Test full user journey: upload → analyze → view results → translate → view CEFR
  - Test bilingual UI throughout workflow
  - Test offline operation
  - Verify no network requests to external services
  - Target: Cover all user stories end-to-end

- [ ] T058 Code review and refactoring
  - Review all new code for constitutional compliance
  - Check test coverage (target: 80%+ overall)
  - Refactor duplicated code
  - Ensure consistent coding style
  - Add docstrings to all public methods

- [ ] T059 Update project dependencies documentation
  - Document argostranslate version requirement
  - Note mdict-query installation from GitHub
  - List all new data files and their purposes
  - Update requirements.txt with final versions

- [ ] T060 Create release notes for Feature 002
  - Summarize bilingual UI capability
  - Highlight offline translation feature
  - Note CEFR educational descriptions
  - List any known limitations
  - Provide upgrade instructions from Feature 001

- [ ] T061 [P] Translation quality validation (SC-004 compliance)
  - Create gold standard test corpus in tests/fixtures/translation_corpus.json:
    - 100 test words (20 per CEFR level A1-C1)
    - Include human-verified Chinese translations
    - Cover diverse vocabulary: nouns, verbs, adjectives, phrasal verbs
  - Implement automated quality test in tests/translation/test_quality.py:
    - Translate all 100 words using Argos Translate
    - Compare output to gold standard translations
    - Use fuzzy matching (85%+ similarity counts as correct)
    - Calculate success rate: correct_translations / total_words
    - FAIL test if success rate <95% per SC-004 requirement
  - Document translation quality report with examples of failures
  - **Coverage**: Minimum 80% enforced by CI (pytest-cov with --cov-fail-under=80)

---

## MVP Scope Recommendation

For the **Minimum Viable Product (MVP)**, focus on the following phases:

✅ **Phase 1** (T001-T005): Setup & Dependencies - **REQUIRED**
✅ **Phase 2** (T006-T014): Foundational Infrastructure - **REQUIRED**
✅ **Phase 3** (T015-T026): User Story 1 - Bilingual UI - **P1 REQUIRED**
✅ **Phase 4** (T027-T036): User Story 3 - Local Translation - **P1 REQUIRED**
⚠️ **Phase 5** (T037-T049): User Story 2 - CEFR Education - **P2 OPTIONAL for MVP**
✅ **Phase 6** (T050-T060): Polish & Documentation - **REQUIRED**

**MVP Delivers**:
- Complete bilingual English/Chinese interface
- Offline translation for all untranslated content
- Three-tier fallback chain (ECDICT → Mdict → Argos)
- Persistent translation cache
- Basic documentation and tests

**Post-MVP** (P2):
- CEFR level education (interactive descriptions)
- Enhanced user experience
- Educational tooltips and modals

**Total MVP Tasks**: 51 tasks (excluding Phase 5)
**Total All Tasks**: 61 tasks

---

## Task Dependencies and Critical Path

**Critical Path** (must be completed in order):
1. Phase 1 (T001-T005) → Foundation
2. Phase 2 (T006-T014) → Core services
3. Phase 3 (T015-T026) → Bilingual UI (US1)
4. Phase 4 (T027-T036) → Translation (US3)
5. Phase 6 (T050-T060) → Polish

**Parallel Execution Opportunities**:
- **T007, T009, T011, T013** (Phase 2): All unit tests can run in parallel
- **T017, T022, T025** (Phase 3): Tests and JavaScript utilities parallel
- **T028, T034** (Phase 4): Translation tests parallel
- **T039, T042, T048** (Phase 5): CEFR tests parallel
- **T050, T051** (Phase 6): E2E tests and performance tests parallel

**Phase-Level Parallelism**:
- Phase 3 (US1) and Phase 4 (US3) can run partially in parallel after Phase 2
- Phase 5 (US2) can start after Phase 2, independent of Phases 3 and 4

---

## Test Coverage Requirements

Per constitution Principle IV (TDD with 80% coverage), each module requires:

✅ **Translation Module** (`src/vocab_analyzer/translation/`):
- cache.py: T007 (unit tests)
- translator.py: T009 (unit tests)
- dictionary.py: T011 (unit tests)
- fallback.py: T013 (unit tests)
- strings.py: T017 (unit tests)
- cefr_loader.py: T039 (unit tests)

✅ **Web Module** (`src/vocab_analyzer/web/`):
- API endpoints: T028 (translation), T042 (CEFR)
- UI components: T025 (bilingual UI), T034 (translation UI), T048 (CEFR UI)

✅ **Integration Tests**:
- T057: Complete workflow tests covering all user stories

**Target**: Minimum 80% code coverage across all new modules.

---

## Performance Targets

Per spec.md success criteria and research.md benchmarks:

| Operation | Target | Task Verification |
|-----------|--------|------------------|
| UI bilingual rendering | <50ms | T026 (browser tests) |
| ECDICT lookup | <10ms | T013 (fallback tests) |
| Mdict lookup | <50ms | T011 (dictionary tests) |
| Argos translation (first) | <3s | T035 (offline tests) |
| Argos translation (cached) | <500ms | T036 (performance tests) |
| Cache hit response | <100ms | T028 (API tests) |
| CEFR description display | <100ms | T048 (UI tests) |

**Memory Constraints**:
- Argos model loaded: <300MB RAM (T036)
- Total application: <500MB RAM (T051)

---

## Success Criteria Verification

Each user story has independent test criteria:

**US1 - Bilingual Interface Navigation** (Phase 3):
- ✅ T025: Verify 100% of UI text is bilingual
- ✅ T026: Test in 4 major browsers
- ✅ All navigation elements show English/Chinese

**US3 - Local Translation** (Phase 4):
- ✅ T034: Translate button appears for untranslated content
- ✅ T035: Translations work offline within 3 seconds
- ✅ T036: Cache hit reduces time to <100ms

**US2 - CEFR Education** (Phase 5):
- ✅ T048: Click CEFR badge shows full description
- ✅ T049: All 7 levels have accurate content
- ✅ Tooltips and modals are accessible

**Overall Feature** (Phase 6):
- ✅ T050: End-to-end workflow tests pass
- ✅ T051: Performance targets met
- ✅ T057: Complete user journey works offline

---

## Risk Mitigation

**Risk 1: Argos Translate model download fails**
- **Mitigation**: T004 includes retry logic and manual download fallback
- **Test**: T035 verifies offline functionality

**Risk 2: User lacks sufficient memory (<4GB RAM)**
- **Mitigation**: Lazy loading in T008, documentation in T053
- **Test**: T051 measures memory usage and sets expectations

**Risk 3: Mdict dictionaries not available**
- **Mitigation**: T011 handles graceful degradation, dictionaries optional
- **Test**: T011 verifies fallback to Argos works without Mdict

**Risk 4: Translation quality insufficient**
- **Mitigation**: Research.md notes 80-90% accuracy acceptable for education
- **Test**: T049 validates content accuracy, user feedback loop

**Risk 5: Chinese text rendering issues**
- **Mitigation**: T021 includes proper font stack, T026 tests multiple browsers
- **Test**: T026 verifies rendering in Chrome, Firefox, Safari, Edge

---

## Notes

- All file paths in tasks are absolute paths from project root
- Tasks marked `[P]` can be parallelized within their phase
- Each user story (US1, US2, US3) is independently testable and deliverable
- Translation cache persists across sessions (30-day expiration)
- Mdict dictionaries are optional; system works without them
- Argos Translate model is ~100MB download, required for translation fallback
- All operations work 100% offline after initial setup

---

**Document Status**: ✅ Complete
**Total Tasks**: 60
**MVP Tasks**: 50
**Estimated Effort**: 5-7 days for MVP (assuming 1 developer)
**Next Step**: Begin Phase 1 - Setup & Dependencies
