# Implementation Plan: Immersive Full-Text Reading View

**Branch**: `005-reading-view` | **Date**: 2025-11-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-reading-view/spec.md`

## Summary

This feature adds a dedicated "全文阅读 / Reading View" tab that transforms the vocabulary analyzer into an immersive learning environment. Users can read the full analyzed text with CEFR-colored words that are clickable for instant definitions. The implementation is **frontend-only** (HTML/CSS/JavaScript), reusing existing backend APIs and translation infrastructure.

**Primary Requirement**: Enable learners to practice reading in context while seamlessly accessing vocabulary support without disrupting reading flow.

**Technical Approach**: 
- Pure frontend implementation using existing design tokens (Feature 003)
- Reuses tab navigation system (Feature 004) and translation caching (Feature 002)
- Parses `processed_text` from existing `/api/analyze` response
- Renders text as HTML with `<span>` wrappers for CEFR-colored words
- Achieves <1s render time for 300KB texts through efficient DOM manipulation

## Technical Context

**Language/Version**: JavaScript ES6 (minimal updates), HTML5, CSS3 (no preprocessing)  
**Primary Dependencies**: None (uses existing Flask 3.0+ backend, Feature 003 design tokens, vanilla JS)  
**Storage**: localStorage (scroll position persistence only)  
**Testing**: Manual browser testing (Chrome, Safari, Firefox, Edge), accessibility audit (axe DevTools)  
**Target Platform**: Web browsers (Chrome 90+, Safari 14+, Firefox 88+, Edge 90+)  
**Project Type**: Web application (frontend-only feature)  
**Performance Goals**: <1s render for 300KB text, 60fps scrolling, <300ms filter re-render, <100ms modal open  
**Constraints**: No new backend APIs, reuse existing data structures, WCAG 2.1 AA compliance required  
**Scale/Scope**: 3 frontend files modified (index.html, styles.css, app.js), 35 implementation tasks across 5 phases

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Constitution Compliance Analysis**:

✅ **Principle I: Simplicity & Maintainability**
- Frontend-only implementation (no new backend complexity)
- Reuses existing components (tab system, modal, translation API)
- Clear separation: reading view rendering isolated in dedicated functions
- No new dependencies required

✅ **Principle II: Modular Architecture**
- Reading view functions are self-contained (`parseTextForReading`, `findWordData`, `handleWordClick`)
- Clean interfaces: uses existing `showWordDetails()` modal function
- Independent from other modules (can be removed without breaking vocabulary/phrasal verb tabs)

✅ **Principle III: Data Quality First**
- No data modification (uses existing `processed_text` and `analysis_results`)
- Preserves original analysis accuracy (CEFR levels unchanged)
- Graceful degradation: empty text displays bilingual message

✅ **Principle IV: Test-Driven Development**
- Manual testing checklist covers functional, performance, accessibility, cross-browser
- Edge cases documented (empty text, large files, special characters)
- Performance profiling required (Chrome DevTools, Lighthouse)

✅ **Principle V: CLI-First Design**
- N/A (feature is web UI enhancement, CLI remains unchanged)

✅ **Principle VI: Project Organization & Structure**
- All changes confined to existing frontend files (`src/vocab_analyzer/web/static/`)
- No new files in root directory
- Documentation in `specs/005-reading-view/` (follows convention)

**GATE STATUS: ✅ PASSED - All principles satisfied, no violations to document**

## Project Structure

### Documentation (this feature)

```text
specs/005-reading-view/
├── plan.md              # This file (/speckit.plan command output)
├── spec.md              # Feature specification (already exists)
├── research.md          # Phase 0 output (technology decisions)
├── data-model.md        # Phase 1 output (data structures)
├── quickstart.md        # Phase 1 output (setup/testing guide)
├── contracts/           # Phase 1 output (function signatures)
│   ├── parseTextForReading.md
│   ├── findWordData.md
│   ├── handleWordClick.md
│   └── scroll-persistence.md
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
src/vocab_analyzer/web/static/
├── index.html           # MODIFIED: Add reading view tab + panel HTML (lines 111-161)
├── styles.css           # MODIFIED: Add reading view styles (new section ~line 2100+)
└── app.js               # MODIFIED: Add reading view logic (6 new functions ~500 LOC)
```

**Structure Decision**: Existing web application structure maintained. All changes are additive modifications to 3 existing frontend files. No new files created (keeps codebase simple per Principle I). Reading view logic integrated into existing `app.js` as a cohesive module of related functions.

## Complexity Tracking

**No violations to justify** - This feature adds a simple, self-contained enhancement without introducing architectural complexity or violating constitutional principles.
