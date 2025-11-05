# Implementation Tasks: Advanced Interaction & Layout Optimization

**Feature**: 004-advanced-interaction
**Branch**: `004-advanced-interaction`
**Generated**: 2025-11-04
**Total Tasks**: 35 tasks across 7 phases

---

## Task Summary

**By Phase**:
- Phase 1 (Setup): 3 tasks
- Phase 2 (Foundational): 4 tasks
- Phase 3 (US1 - P0): 8 tasks
- Phase 4 (US2 - P1): 6 tasks
- Phase 5 (US3 - P1): 5 tasks
- Phase 6 (US4 - P2): 5 tasks
- Phase 7 (Polish): 4 tasks

**By User Story**:
- US1 (One-Click Discovery): 8 tasks
- US2 (Widescreen Layout): 6 tasks
- US3 (Mobile Touch): 5 tasks
- US4 (Keyboard Navigation): 5 tasks

**Parallelization Opportunities**: 15 tasks marked [P] can run in parallel within their phases

---

## Implementation Strategy

### MVP Scope (Recommended First Delivery)

**Phase 3 Only**: User Story 1 (One-Click Discovery)
- Simplifies word lookup interaction (30% faster)
- Removes cognitive overhead ("翻" button confusion)
- Delivers immediate value to all users
- Estimated: 8-10 hours

**Rationale**: US1 is marked P0 (critical priority) and is independently testable. Delivers core value without requiring responsive layout or accessibility enhancements.

### Incremental Delivery Path

```
MVP (US1) → US2 (Widescreen) → US3 (Mobile) → US4 (Accessibility) → Polish
  ↓            ↓                  ↓              ↓                    ↓
8-10h        6-8h               5-6h           4-5h                 3-4h
```

**Total Implementation Time**: 26-33 hours (3-4 days focused work)

---

## Phase 1: Setup & Validation

**Goal**: Validate prerequisites and prepare development environment

**Duration**: 1-2 hours

### Tasks

- [X] T001 Validate Feature 003 design tokens exist in src/vocab_analyzer/web/static/styles.css
  - **Verify**: `:root` selector contains --space-*, --color-*, --shadow-* tokens
  - **Success**: All required tokens documented in research.md Decision 2 are present
  - **Blocker**: If tokens missing, must add them before proceeding

- [X] T002 Create backup of current styles.css and templates for rollback safety
  - **Files**: src/vocab_analyzer/web/static/styles.css, src/vocab_analyzer/web/templates/*.html
  - **Command**: `cp styles.css styles.css.backup-$(date +%Y%m%d)`
  - **Success**: Backup files created with timestamp

- [X] T003 Start development server and verify baseline functionality
  - **Command**: `python -m vocab_analyzer.web.app`
  - **Verify**: http://127.0.0.1:5000 loads, upload works, results page renders
  - **Success**: All existing features functional before modifications

---

## Phase 2: Foundational Infrastructure

**Goal**: Add responsive container system and base styles needed by all user stories

**Duration**: 2-3 hours

**Why Foundational**: Responsive containers are used by all user stories and must be implemented first

### Tasks

- [X] T004 [P] Implement responsive container system with 5 breakpoints in src/vocab_analyzer/web/static/styles.css
  - **Breakpoints**: 375px (sm), 768px (md), 1024px (lg), 1280px (xl), 1440px+ (xxl)
  - **Container widths**: Mobile 100%, Tablet 720px, Desktop 960px, Large 1280px, XL 1400px
  - **Reference**: data-model.md Component 1, research.md Decision 4
  - **Test**: Chrome DevTools responsive mode, verify width at each breakpoint

- [X] T005 [P] Implement word card grid responsive layout in src/vocab_analyzer/web/static/styles.css
  - **Columns**: Mobile 1, Tablet 2-3 (auto-fill), Desktop 4, Large 5, XL 5-6
  - **CSS**: Use CSS Grid with `grid-template-columns: repeat(auto-fill, minmax(...))`
  - **Reference**: data-model.md Component 3, research.md Decision 4
  - **Test**: Verify column count at each breakpoint

- [X] T006 [P] Add focus indicator styles for keyboard navigation in src/vocab_analyzer/web/static/styles.css
  - **Styles**: `:focus-visible { outline: 2px solid var(--focus-ring); outline-offset: 2px; }`
  - **Remove default**: `:focus { outline: none; }` (only for keyboard, not mouse)
  - **Reference**: data-model.md Component 5, research.md Decision 7
  - **Test**: Tab through page, verify blue outline visible on keyboard focus

- [X] T007 Validate all foundational styles work at all breakpoints
  - **Test**: Responsive container widths, grid columns, focus indicators
  - **Tools**: Chrome DevTools responsive mode (375px, 768px, 1024px, 1280px, 1440px)
  - **Success**: No horizontal scrolling, all layouts functional

---

## Phase 3: User Story 1 - One-Click Word Discovery (Priority: P0)

**Goal**: Simplify word lookup by removing "翻" button and making entire card clickable

**User Story**: As a language learner, I want to click once on any word to see its definition and examples, so I can learn efficiently without extra steps.

**Success Criteria**:
- SC-001: Users complete lookup 30% faster (measure: time from click to modal display)
- SC-002: 95%+ click accuracy (no accidental taps on adjacent elements)
- SC-008: CSS file size remains <100KB (current 35KB, target ~50KB)
- SC-010: Translation loads <2s (95th percentile)
- SC-011: Keyboard navigation functional (Tab, Enter, Escape)

**Independent Test**: Click any word card → Modal opens showing word, CEFR level, auto-loaded translation, frequency, examples → Close modal via X, backdrop, or Escape

**Duration**: 8-10 hours

### Tasks

#### 3.1 Word Card Enhancement

- [X] T008 [P] [US1] Remove "翻" translation button from word cards in src/vocab_analyzer/web/static/index.html
  - **Find**: `<button class="translate-btn">翻</button>` or similar
  - **Remove**: Entire button element
  - **Verify**: Word cards show only word text, CEFR badge, frequency (no button)

- [X] T009 [P] [US1] Make entire word card clickable in src/vocab_analyzer/web/static/styles.css
  - **Add**: `cursor: pointer;` to `.word-card`
  - **Add**: `tabindex="0" role="button"` attributes to card HTML
  - **Add**: ARIA label: `aria-label="View details for '{word}'"`
  - **Reference**: data-model.md Component 3
  - **Test**: Click anywhere on card (not just text), verify modal opens

- [X] T010 [P] [US1] Implement card hover states with 3px lift and shadow deepening in src/vocab_analyzer/web/static/styles.css
  - **Hover**: `transform: translateY(-3px); box-shadow: var(--shadow-large); border-color: var(--primary-color);`
  - **Active**: `transform: translateY(-1px); box-shadow: var(--shadow-medium);`
  - **Transition**: `200ms ease-out` for smooth animation
  - **Reference**: data-model.md Component 3, research.md Decision 10
  - **Test**: Hover over card, verify lift animation is smooth (60fps)

- [X] T011 [US1] Add click event handlers to word cards in src/vocab_analyzer/web/static/app.js
  - **JavaScript**: `document.querySelectorAll('.word-card').forEach(card => card.addEventListener('click', ...));`
  - **Function**: Call existing `openWordModal(word)` function
  - **Keyboard**: Handle Enter/Space keys for accessibility
  - **Reference**: quickstart.md Phase 2
  - **Test**: Click card, press Enter on focused card, verify both open modal

#### 3.2 Modal Enhancement

- [X] T012 [P] [US1] Implement responsive modal widths in src/vocab_analyzer/web/static/styles.css
  - **Mobile**: 90% width, Tablet 80% max 600px, Desktop 60% max 700px, XL max 800px
  - **Media queries**: Use 5 breakpoints from Phase 2
  - **Reference**: data-model.md Component 4, spec.md FR-026
  - **Test**: Open modal at each breakpoint, verify width adapts

- [X] T013 [P] [US1] Add skeleton loading screens for translation section in src/vocab_analyzer/web/static/styles.css
  - **Structure**: Gray rectangles matching content shape, shimmer animation
  - **Keyframe**: `@keyframes shimmer { 0% { left: -100%; } 100% { left: 100%; } }`
  - **Loading text**: "正在加载... / Loading..." (bilingual)
  - **Reference**: data-model.md Component 5, research.md Decision 5
  - **Test**: Open modal, verify skeleton appears before translation loads

- [X] T014 [US1] Update modal to auto-load Chinese translation on open in src/vocab_analyzer/web/static/app.js
  - **Logic**: Check cache → show immediately with "缓存" label OR fetch via `/api/translate` → show skeleton during load
  - **Error handling**: Show friendly error "暂时无法获取释义" with retry button if API fails
  - **Success**: Show translation with fade-in animation (opacity 0→1)
  - **Reference**: spec.md FR-004, FR-005
  - **Test**: Open modal for cached word (instant), uncached word (skeleton then translation), offline (error message)

- [X] T015 [US1] Validate User Story 1 independently - test one-click word discovery workflow
  - **Test Scenarios**: From spec.md acceptance scenarios 1-6
  - **Measure**: Time from card click to modal full display (target: 30% faster than baseline)
  - **Measure**: Click accuracy (95%+ first-tap success)
  - **Success**: All 6 acceptance scenarios pass

---

## Phase 4: User Story 2 - Widescreen-Optimized Study (Priority: P1)

**Goal**: Maximize screen space utilization with tab-based navigation and expanded containers

**User Story**: As a desktop user, I want the interface to use my full screen space effectively, so I can see more vocabulary at once and focus better.

**Success Criteria**:
- SC-003: Screen space utilization increases 30% on desktop (1400px vs 800px = 75% increase)
- SC-004: Interface functional at 375px width (zero horizontal scrolling)
- SC-009: Tab transition completes within 200-300ms without jank

**Independent Test**: Open results on 1440px+ screen → Container expands to 1400px → Word cards display in 5-6 columns → Click tab to switch between Words/Phrasal Verbs → Filter and search persist across tabs

**Duration**: 6-8 hours

### Tasks

#### 4.1 Tab Navigation System

- [X] T016 [P] [US2] Replace side-by-side word/phrase columns with tab HTML structure in src/vocab_analyzer/web/templates/results.html
  - **Remove**: Existing two-column layout (if present)
  - **Add**: Tab navigation HTML with role="tablist", role="tab", role="tabpanel"
  - **Tabs**: "单词 (152) / Words" and "短语动词 (37) / Phrasal Verbs"
  - **Reference**: data-model.md Component 2, quickstart.md Phase 3
  - **Content**: Move word list to `<div id="words-panel" role="tabpanel">`, phrases to `<div id="phrases-panel">`

- [X] T017 [P] [US2] Implement tab button styles with active/inactive states in src/vocab_analyzer/web/static/styles.css
  - **Active**: Blue text (#2563eb), blue 3px bottom border, font-weight 600
  - **Inactive**: Gray text (#6b7280), no border, font-weight 400
  - **Hover (inactive)**: Light gray background (#f3f4f6), darker text (#1f2937)
  - **Transition**: `200ms ease-out` for smooth color changes
  - **Reference**: data-model.md Component 2, spec.md FR-008
  - **Test**: Click tabs, verify active styling updates, hover over inactive tabs

- [X] T018 [P] [US2] Add tab switching JavaScript with fade transition in src/vocab_analyzer/web/static/app.js
  - **Click handler**: Toggle `.active` class on buttons and content panels
  - **Transition**: Fade out old content (opacity 1→0, 100ms), fade in new content (opacity 0→1, 200ms, 100ms delay)
  - **ARIA**: Update `aria-selected` attribute on tab buttons
  - **Reference**: data-model.md Component 2, research.md Decision 3
  - **Test**: Click tabs, verify smooth 300ms transition with no layout jumps

- [X] T019 [US2] Implement tab state persistence with localStorage in src/vocab_analyzer/web/static/app.js
  - **Save**: `localStorage.setItem('activeTab', 'words'|'phrases')` on tab switch
  - **Restore**: Read localStorage on page load, activate saved tab
  - **Persist filters/search**: Save `activeFilters` and `searchQuery` objects, reapply on tab switch
  - **Reference**: data-model.md State Persistence, spec.md FR-010
  - **Test**: Switch tabs, refresh page, verify active tab and filters restored

#### 4.2 Responsive Label and Dynamic Counts

- [X] T020 [P] [US2] Add responsive tab labels (bilingual desktop, simplified mobile) in src/vocab_analyzer/web/static/styles.css
  - **Mobile (<768px)**: Hide `.tab-label-secondary` (English part), show only Chinese + count
  - **Desktop (768px+)**: Show both primary and secondary labels
  - **CSS**: `@media (max-width: 767px) { .tab-label-secondary { display: none; } }`
  - **Reference**: data-model.md Component 2, spec.md FR-007
  - **Test**: Resize window, verify labels simplify on mobile

- [X] T021 [US2] Validate User Story 2 independently - test widescreen layout and tab navigation
  - **Test Scenarios**: From spec.md acceptance scenarios 1-5
  - **Measure**: Content area width on 1440px screen (target: 1400px)
  - **Measure**: Tab transition timing (target: <300ms)
  - **Success**: All 5 acceptance scenarios pass, no layout jumps

---

## Phase 5: User Story 3 - Mobile-Optimized Touch Interaction (Priority: P1)

**Goal**: Ensure touch-friendly interface with 44x44px minimum touch targets

**User Story**: As a mobile user, I want to easily access the app on my phone with touch-friendly controls, so I can review vocabulary anywhere.

**Success Criteria**:
- SC-002: 95%+ first-tap success rate (no accidental taps)
- SC-004: Functional at 375px width (zero horizontal scrolling)
- SC-007: All interactive elements ≥44x44px on mobile

**Independent Test**: Open app on 375px mobile device → All buttons/cards/tabs are 44x44px → Tap word card → Modal opens and fits screen → Tap tabs → Content switches → No horizontal scrolling anywhere

**Duration**: 5-6 hours

### Tasks

- [X] T022 [P] [US3] Enforce 44x44px minimum touch targets on mobile in src/vocab_analyzer/web/static/styles.css
  - **Elements**: `.word-card`, `.tab-button`, `button`, `.clickable`
  - **CSS**: `@media (max-width: 767px) { min-height: 44px; min-width: 44px; }`
  - **Padding**: Ensure adequate padding (e.g., `padding: var(--space-2) var(--space-4);`)
  - **Reference**: data-model.md Component 2/3, research.md Decision 7
  - **Test**: Use Chrome DevTools, inspect element, check Computed → height/width ≥44px

- [X] T023 [P] [US3] Add mobile-specific modal styles (90% width, 5% margins) in src/vocab_analyzer/web/static/styles.css
  - **Mobile (<768px)**: `.modal-content { width: 90%; margin: 0 var(--space-5); }`
  - **Max-height**: `90vh` to prevent viewport overflow
  - **Overflow**: `overflow-y: auto;` for scrollable content
  - **Reference**: data-model.md Component 4
  - **Test**: Open modal on 375px screen, verify fits without horizontal scroll

- [X] T024 [P] [US3] Simplify tab labels for mobile screens in src/vocab_analyzer/web/templates/results.html
  - **HTML**: Add CSS classes `.tab-label-primary` (Chinese + count) and `.tab-label-secondary` (English)
  - **Mobile display**: Hide secondary via CSS (already in T020)
  - **Example**: "单词 (152)" only on mobile, "单词 (152) / Words" on desktop
  - **Reference**: spec.md FR-007

- [X] T025 [US3] Test touch target accuracy on actual mobile device or DevTools
  - **Method**: Manual tapping test on iPhone/Android or DevTools mobile emulation
  - **Success**: 95%+ first-tap success, no accidental taps on adjacent elements
  - **Measure**: Using Chrome DevTools → Inspect → Computed tab → Verify dimensions
  - **Reference**: spec.md SC-007

- [X] T026 [US3] Validate User Story 3 independently - test mobile touch interaction
  - **Test Scenarios**: From spec.md acceptance scenarios 1-5
  - **Device**: Real mobile device or DevTools emulation (iPhone 12, Pixel 5)
  - **Success**: All 5 acceptance scenarios pass, touch targets measured ≥44x44px

---

## Phase 6: User Story 4 - Keyboard-Accessible Navigation (Priority: P2)

**Goal**: Full keyboard navigation support and WCAG 2.1 AA compliance

**User Story**: As a keyboard-only user, I want to navigate the app using only my keyboard, so I can access all features without a mouse.

**Success Criteria**:
- SC-005: Lighthouse accessibility score 100
- SC-006: axe DevTools 0 violations
- SC-011: Keyboard navigation completes full workflow (browse → open details → switch tabs → close)
- SC-012: User satisfaction feedback shows positive trend

**Independent Test**: Unplug mouse → Tab through page → All elements reachable → Focus indicators visible → Enter opens modal → Arrow keys switch tabs → Escape closes modal → Full workflow completable

**Duration**: 4-5 hours

### Tasks

- [X] T027 [P] [US4] Implement Tab key navigation order for word cards in src/vocab_analyzer/web/static/index.html
  - **HTML**: Ensure `.word-card` has `tabindex="0"` (if not already from T009)
  - **Order**: Logical sequence (tabs → filters → search → cards → modal)
  - **Test**: Tab through page, verify order makes sense

- [X] T028 [P] [US4] Add Arrow key navigation for tab switching in src/vocab_analyzer/web/static/app.js
  - **Left Arrow**: Focus previous tab (wrap to last if at first)
  - **Right Arrow**: Focus next tab (wrap to first if at last)
  - **Auto-activate**: Focus + activate tab on arrow key press
  - **Reference**: data-model.md Accessibility, research.md Decision 7
  - **Test**: Focus tab, press Left/Right arrows, verify tabs switch

- [X] T029 [P] [US4] Implement Escape key to close modal in src/vocab_analyzer/web/static/app.js
  - **Event**: `document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && modalOpen) closeModal(); });`
  - **Return focus**: After closing, return focus to triggering word card
  - **Reference**: data-model.md Component 4, spec.md FR-027
  - **Test**: Open modal, press Escape, verify modal closes and focus returns

- [X] T030 [US4] Run Lighthouse accessibility audit and fix any violations
  - **Command**: Chrome DevTools → Lighthouse → Accessibility → Analyze
  - **Target**: Score 100 with zero violations
  - **Common issues**: Missing ARIA labels, insufficient contrast, missing focus indicators
  - **Reference**: spec.md SC-005, research.md Decision 7
  - **Success**: 100 score achieved

- [X] T031 [US4] Validate User Story 4 independently - test keyboard-only navigation
  - **Test Scenarios**: From spec.md acceptance scenarios 1-5
  - **Method**: Unplug mouse, complete full workflow using only keyboard
  - **Success**: All 5 acceptance scenarios pass, Lighthouse 100, axe 0 violations

---

## Phase 7: Polish & Cross-Cutting Concerns

**Goal**: Final testing, validation, and documentation

**Duration**: 3-4 hours

### Tasks

- [X] T032 [P] Run axe DevTools accessibility scan and fix violations
  - **Tool**: Install axe DevTools extension, scan page
  - **Target**: 0 violations
  - **Reference**: spec.md SC-006
  - **Success**: Zero violations reported

- [X] T033 Validate CSS file size remains under 100KB limit
  - **Command**: `ls -lh src/vocab_analyzer/web/static/styles.css`
  - **Baseline**: ~35KB before feature
  - **Target**: <100KB after feature (~50KB expected)
  - **Reference**: spec.md SC-008
  - **Success**: File size confirmed <100KB

- [X] T034 Cross-browser testing (Chrome, Safari, Firefox minimum)
  - **Browsers**: Chrome 120+, Safari 17+, Firefox 121+
  - **Test**: All breakpoints, all interactive states, all user stories
  - **Success**: No browser-specific bugs, consistent behavior across browsers

- [X] T035 Complete full regression testing checklist from spec.md
  - **User Story 1**: 6 acceptance scenarios
  - **User Story 2**: 5 acceptance scenarios
  - **User Story 3**: 5 acceptance scenarios
  - **User Story 4**: 5 acceptance scenarios
  - **Edge Cases**: 5 edge case scenarios from spec.md
  - **Success**: All 26 scenarios pass

---

## Dependency Graph

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational) ← [Must complete before user stories]
    ↓
    ├─→ Phase 3 (US1 - P0) [INDEPENDENT] ← MVP
    ├─→ Phase 4 (US2 - P1) [INDEPENDENT]
    ├─→ Phase 5 (US3 - P1) [INDEPENDENT]
    └─→ Phase 6 (US4 - P2) [INDEPENDENT]
         ↓
    Phase 7 (Polish) ← [After all user stories complete]
```

**Key Dependencies**:
- **Foundational (Phase 2) BLOCKS all user stories**: Responsive containers and base styles must exist first
- **User Stories (Phases 3-6) are INDEPENDENT**: Can be implemented in any order after Phase 2
- **Recommended Order**: P0 → P1 → P1 → P2 (priority-driven)
- **MVP Path**: Phase 1 → Phase 2 → Phase 3 → Phase 7 (minimal viable delivery)

---

## Parallel Execution Examples

### Phase 2 (Foundational) - 3 parallel tasks
```bash
# Terminal 1
Task T004: Implement responsive containers

# Terminal 2
Task T005: Implement grid layout

# Terminal 3
Task T006: Add focus indicators
```

**Why**: Different CSS sections, no file conflicts

### Phase 3 (US1) - 3 parallel tasks after T011 completes
```bash
# Terminal 1
Task T012: Implement modal responsive widths (CSS)

# Terminal 2
Task T013: Add skeleton screens (CSS)

# After T011-T013 complete:
# Terminal 3
Task T014: Update modal auto-load logic (JavaScript)
```

**Why**: T012-T013 are CSS-only, independent. T014 depends on T011 (click handlers) completing first.

### Phase 4 (US2) - 2 parallel tasks after T016 completes
```bash
# Terminal 1
Task T017: Tab button styles (CSS)

# Terminal 2
Task T020: Responsive tab labels (CSS)

# After T016-T017 complete:
# Terminal 3
Task T018: Tab switching JavaScript (requires HTML from T016)
Task T019: State persistence (extends T018)
```

### Phase 5 (US3) - 3 parallel tasks
```bash
# Terminal 1
Task T022: Touch target sizing (CSS)

# Terminal 2
Task T023: Mobile modal styles (CSS)

# Terminal 3
Task T024: Simplify tab labels HTML (HTML)
```

### Phase 6 (US4) - 3 parallel tasks
```bash
# Terminal 1
Task T027: Tab order HTML

# Terminal 2
Task T028: Arrow key navigation (JavaScript)

# Terminal 3
Task T029: Escape key handler (JavaScript)
```

**Note**: Tasks marked [P] can run in parallel. Tasks without [P] have dependencies on prior tasks completing.

---

## Testing Strategy

### Manual Testing Checklist

**Per User Story** (independently testable):
- [ ] US1: One-click discovery (8 checks from spec.md)
- [ ] US2: Widescreen layout (6 checks)
- [ ] US3: Mobile touch (5 checks)
- [ ] US4: Keyboard navigation (5 checks)

**Cross-Cutting**:
- [ ] 5 responsive breakpoints (375px, 768px, 1024px, 1280px, 1440px)
- [ ] 5 edge cases (translation failure, long words, slow network, small screens, keyboard traps)

### Automated Testing

**Lighthouse Audit** (target: 100 accessibility score):
```bash
# Chrome DevTools → Lighthouse → Accessibility → Analyze
# Expected: 100 score, 0 violations
```

**axe DevTools Scan** (target: 0 violations):
```bash
# Install extension: https://www.deque.com/axe/devtools/
# Run: Scan ALL of my page
# Expected: 0 violations
```

**Performance Validation**:
```bash
# Check CSS file size
ls -lh src/vocab_analyzer/web/static/styles.css
# Expected: <100KB (~50KB)

# Check animation performance
# Chrome DevTools → Performance → Record → Interact
# Expected: 60fps, transitions <300ms
```

---

## Task Validation Checklist

**Format Compliance**:
- [x] All 35 tasks follow checkbox format `- [ ] [TaskID] [P?] [Story?] Description with file path`
- [x] Task IDs sequential (T001-T035)
- [x] [P] markers on 15 parallelizable tasks
- [x] [Story] labels on all user story phase tasks (US1-US4)
- [x] All tasks include specific file paths

**Completeness**:
- [x] Setup phase: 3 tasks (prerequisites, backup, baseline)
- [x] Foundational phase: 4 tasks (containers, grid, focus, validation)
- [x] User Story 1 (P0): 8 tasks (card enhancement, modal enhancement, validation)
- [x] User Story 2 (P1): 6 tasks (tab navigation, responsive labels, validation)
- [x] User Story 3 (P1): 5 tasks (touch targets, mobile modal, validation)
- [x] User Story 4 (P2): 5 tasks (keyboard navigation, accessibility audits, validation)
- [x] Polish phase: 4 tasks (final testing, validation, cross-browser)

**Independent Testability**:
- [x] Each user story has validation task at end of phase
- [x] Each user story maps to acceptance scenarios from spec.md
- [x] User stories can be implemented in any order after Foundational phase

**Dependency Clarity**:
- [x] Dependency graph shows clear completion order
- [x] Parallel execution examples provided for each phase
- [x] MVP scope clearly defined (Phases 1-3 + 7)

---

**Tasks.md Status**: ✅ **COMPLETE & VALIDATED**
**Ready for**: Implementation (start with Phase 1)
**Estimated Total Time**: 26-33 hours (3-4 days focused work)
**MVP Time**: 12-15 hours (Phases 1-3 + 7)
