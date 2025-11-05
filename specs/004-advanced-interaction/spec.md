# Feature Specification: Advanced Interactive Learning Experience

**Feature Branch**: `004-advanced-interaction`
**Created**: 2025-11-04
**Status**: Draft
**Input**: Comprehensive UI/UX optimization - unified interaction, widescreen layouts, professional visual polish

---

## Executive Summary

### What We're Building

A comprehensive UI/UX transformation that elevates the vocabulary analyzer from a functional tool into a professional, immersive learning platform. This feature delivers three major improvements:

1. **Simplified Interaction Model**: Single-click access to complete word information (definition, level, frequency, examples) - removing cognitive overhead
2. **Optimized Screen Utilization**: Tab-based navigation and responsive layouts adapting from mobile (375px) to ultra-wide displays (1440px+)
3. **Professional Visual Polish**: Enhanced hover states, loading animations, WCAG 2.1 AA compliance, refined spacing/typography

**Core Value Proposition**: Transform from "functional tool" to "immersive learning platform" by eliminating interaction friction and maximizing content visibility across all devices.

---

## User Scenarios & Testing

### User Story 1 - One-Click Word Discovery (Priority: P0)

**Description**: Learners access complete word information with a single card click - no decision-making about which button to press.

**Why this priority**: This is the most critical user interaction - every vocabulary review session involves hundreds of word lookups. Current split between "card click" (examples) and "翻 button" (translation) creates cognitive load and slows learning.

**Independent Test**: Can be tested by clicking any word card and verifying all information (word, CEFR level, Chinese translation, frequency, examples) appears in one modal without additional clicks.

**Acceptance Scenarios**:

1. **Given** user views vocabulary list **When** user clicks any word card **Then** detail modal opens showing word, CEFR level badge, auto-loaded Chinese translation, frequency count, and 3-5 example sentences
2. **Given** detail modal is open **When** translation is cached **Then** Chinese definition displays immediately with "缓存" label
3. **Given** detail modal is open **When** translation not cached **Then** skeleton screen appears with "正在加载释义..." and translation loads within 2 seconds
4. **Given** translation request fails **When** user views modal **Then** friendly error "暂时无法获取释义" shows with retry button, but CEFR/frequency/examples remain visible
5. **Given** user clicks example sentence "翻译" button **When** translation loads **Then** translation displays below sentence in yellow background, button changes to "✕" close icon
6. **Given** detail modal is open **When** user clicks X button, outside modal, or presses Escape **Then** modal closes and returns to vocabulary list

**Key Changes from Current State**:
- Remove independent "翻" button from word cards
- Entire card becomes single clickable area
- Translation loads automatically (not on-demand)
- All information in one unified view

---

### User Story 2 - Widescreen-Optimized Study (Priority: P1)

**Description**: Desktop users (1280px+ screens) see content utilize full screen width with tab-based navigation, eliminating wasted space and split-column distractions.

**Why this priority**: Large percentage of learners use desktop computers (60% estimated) with wide monitors. Current 800px max-width wastes valuable screen real estate and forces unnecessary scrolling.

**Independent Test**: Can be tested by opening results page on 1440px+ screen and verifying container expands to 1400px, word cards display in 5-6 columns, and tab navigation replaces side-by-side word/phrase layout.

**Acceptance Scenarios**:

1. **Given** user opens results page on 1440px screen **When** page loads **Then** container expands to 1400px max-width (vs 800px before), word cards display in 5-6 column grid
2. **Given** vocabulary list displays **When** user sees navigation **Then** tabs show "单词 (152) / Words" and "短语动词 (37) / Phrasal Verbs" with active tab highlighted (blue text, blue bottom border)
3. **Given** user applies CEFR filter "B2" and searches "make" **When** user switches from "单词" to "短语动词" tab **Then** filter and search persist, showing B2 phrasal verbs containing "make", counts update dynamically
4. **Given** user clicks inactive tab **When** transition occurs **Then** content fades out/in smoothly (200-300ms), no layout jumps or flickers
5. **Given** user views content area **When** scrolling **Then** single unified scroll region (not split left-right columns)

**Responsive Behavior**:
- 1440px+: 1400px container, 5-6 columns
- 1280-1440px: 1280px container, 5 columns
- 1024-1280px: 960px container, 4 columns
- 768-1024px: 720px container, 2-3 columns
- <768px: 100% width, 1 column, simplified tab labels (Chinese + count only)

---

### User Story 3 - Mobile-Optimized Touch Interaction (Priority: P1)

**Description**: Mobile users (375px+ phones) interact accurately with touch-friendly targets and responsive layouts.

**Why this priority**: Mobile usage is significant (30% estimated) and current implementation has small touch targets that cause mis-taps and frustration.

**Independent Test**: Can be tested on 375px mobile device by tapping word cards, buttons, and tabs - all interactions should succeed on first tap with no horizontal scrolling.

**Acceptance Scenarios**:

1. **Given** user opens results on phone (375px width) **When** viewing list **Then** all interactive elements (cards, buttons, tabs) are 44x44px minimum, word cards display one per row
2. **Given** user taps word card **When** modal opens **Then** modal uses 90% screen width with 5% margins, all content fits without horizontal scroll
3. **Given** detail modal displays **When** user taps "翻译" button on example **Then** button target is large enough for thumb tap (44x44px), translation loads below sentence
4. **Given** user views tab navigation **When** tapping tabs **Then** tab buttons are 44x44px, labels simplify to "单词 (152)" (remove English on mobile)
5. **Given** user interacts with any element **When** tapping **Then** 95%+ first-tap success rate, no accidental taps on adjacent elements

---

### User Story 4 - Keyboard-Accessible Navigation (Priority: P2)

**Description**: Keyboard-only users (accessibility requirement) navigate entire interface using Tab, Enter, Arrow keys, and Escape.

**Why this priority**: WCAG 2.1 AA compliance requires full keyboard accessibility. While fewer users navigate exclusively by keyboard, this is legally required and improves power-user efficiency.

**Independent Test**: Can be tested by unplugging mouse and completing full workflow (browse words, open details, switch tabs, close modal) using only keyboard. All interactive elements must be reachable and have visible focus indicators.

**Acceptance Scenarios**:

1. **Given** user presses Tab key **When** navigating page **Then** focus cycles through: word cards → tab buttons → filter controls → search input with visible blue outline (2px solid, 2px offset)
2. **Given** word card has focus **When** user presses Enter or Space **Then** detail modal opens
3. **Given** modal is open **When** user presses Escape **Then** modal closes
4. **Given** tabs are focused **When** user presses Left/Right arrow keys **Then** active tab switches with smooth transition
5. **Given** user navigates with keyboard **When** any element receives focus **Then** focus indicator is clearly visible (`:focus-visible` only, not on mouse click)

---

### Edge Cases

#### Edge Case 1: Translation Service Unavailable

**Scenario**: User opens word details while translation API is down
**Expected Behavior**:
- Modal opens normally with word, CEFR level, frequency, examples visible
- Translation area shows: "暂时无法获取释义" (friendly error, no red scary boxes)
- Small "重试" button allows manual retry
- User can still view and interact with all other information
- No blocking or modal dismissal required

#### Edge Case 2: Extremely Long Words or Phrases

**Scenario**: User views long phrasal verb "take advantage of the opportunity"
**Expected Behavior**:
- Text uses `word-break: break-word` and `overflow-wrap: break-word`
- Text wraps naturally within card boundaries
- Card height adjusts to fit content
- No text truncation, ellipsis, or horizontal scroll
- All hover/click targets remain accurate

#### Edge Case 3: Slow Network Connection (3G)

**Scenario**: User on slow 3G connection opens word details
**Expected Behavior**:
- Modal opens immediately with skeleton screens (gray placeholders)
- "正在加载... / Loading..." indicator displays
- Layout remains stable (no content jumping when data loads)
- After 10s timeout, shows error with retry option
- User can close modal and try different words

#### Edge Case 4: Very Small Mobile Screen (360px)

**Scenario**: User on very small Android phone (360px width)
**Expected Behavior**:
- All layouts adjust responsively
- Touch targets maintain 44x44px minimum
- No horizontal scrolling occurs
- Font sizes remain readable (16px minimum)
- Modal fits within screen bounds with adequate margins

#### Edge Case 5: Keyboard Trap Prevention

**Scenario**: User tabs through interface and enters modal
**Expected Behavior**:
- Tab key cycles within modal when open (focus doesn't escape to background)
- Escape key always exits modal and returns focus to triggering element
- Shift+Tab moves backward through focusable elements
- No element creates keyboard trap (can always tab out)

---

## Requirements

### Functional Requirements

**Core Interaction Model**:

- **FR-001**: System MUST make entire word card clickable (not just text) with visual hover feedback (border color change to blue, 3px lift, shadow deepening, 200ms transition)
- **FR-002**: System MUST remove independent "翻" (translation) button from word cards - translation loads automatically in detail modal
- **FR-003**: System MUST open detail modal on card click showing: word (36px+, bold, blue), CEFR badge, Chinese translation (auto-loaded), frequency, example sentences
- **FR-004**: System MUST automatically request Chinese translation when modal opens - display skeleton screen if loading, show cached translation immediately if available
- **FR-005**: System MUST display friendly error "暂时无法获取释义" with retry button if translation fails, while keeping CEFR/frequency/examples visible

**Tab Navigation System**:

- **FR-006**: System MUST replace side-by-side word/phrase columns with tab-based navigation showing two tabs: "单词 ({count})" and "短语动词 ({count})"
- **FR-007**: Desktop view (768px+) MUST show bilingual tab labels: "单词 (152) / Words", mobile (<768px) MUST show simplified labels: "单词 (152)"
- **FR-008**: Active tab MUST display: blue text (#2563eb), 3px solid blue bottom border, font-weight 600; inactive tabs: gray text (#6b7280), no border, font-weight 400
- **FR-009**: Tab switching MUST trigger simple fade transition (outgoing: opacity 1→0 in 100ms, incoming: opacity 0→1 in 200ms after 100ms delay, total 300ms, ease-in-out timing) with no layout jumps or content flickering
- **FR-010**: System MUST persist filter and search state when switching tabs (e.g., B2 filter + "make" search applies to both Words and Phrasal Verbs)
- **FR-011**: Tab counts MUST update dynamically based on active filters (e.g., filtering B2 changes count from "单词 (152)" to "单词 (48)")

**Responsive Layout**:

- **FR-012**: Container max-width MUST adapt to screen size:
  - <768px: 100% width with 20px side margins
  - 768-1024px: 720px max-width
  - 1024-1280px: 960px max-width
  - 1280-1440px: 1280px max-width
  - 1440px+: 1400px max-width
- **FR-013**: Word card grid MUST adjust column count:
  - <768px: 1 column
  - 768-1024px: 2-3 columns
  - 1024-1280px: 4 columns
  - 1280-1440px: 5 columns
  - 1440px+: 5-6 columns

**Interactive Visual Feedback**:

- **FR-014**: Primary buttons MUST provide hover state: darker background (#1d4ed8), lift 2px, shadow deepens; active state: even darker (#1e40af), press down 2px
- **FR-015**: Secondary buttons MUST provide hover state: border darkens, light gray background (#f9fafb), shadow appears
- **FR-016**: Inactive tabs MUST provide hover state: light gray background (#f3f4f6), text darkens to #374151
- **FR-017**: All transitions MUST use ease-out timing function with durations: 100-150ms (button clicks), 200-300ms (cards/modals/tabs), 300-500ms (list filtering)

**Accessibility & Touch Targets**:

- **FR-018**: All interactive elements (cards, buttons, tabs, inputs) MUST have 44x44px minimum height/width on mobile (<768px) for touch accuracy
- **FR-019**: All focusable elements MUST display 2px solid blue (#2563eb) focus indicator with 2px offset when focused via keyboard (`:focus-visible` only, not mouse clicks)
- **FR-020**: All text MUST meet WCAG 2.1 AA contrast ratios: primary text (#1f2937) 4.9:1, secondary text (#6b7280) 4.54:1, buttons 4.5:1+ on respective backgrounds
- **FR-021**: Keyboard navigation MUST support: Tab (next element), Shift+Tab (previous), Enter/Space (activate), Escape (close modal), Left/Right arrows (switch tabs when focused)

**Loading & Error States**:

- **FR-022**: Translation loading MUST display skeleton screens (gray #e5e7eb rectangles matching final content shape) with 1.5s shimmer animation (left-to-right sweep)
- **FR-023**: Loading indicators MUST show "正在加载... / Loading..." text in both Chinese and English
- **FR-024**: Failed translation MUST show friendly error "暂时无法获取释义" with small "重试" button, without blocking access to other modal content
- **FR-025**: Slow network (>2s load) MUST maintain layout stability - no content jumping when translations load

**Modal Behavior**:

- **FR-026**: Detail modal width MUST adapt: mobile (<768px) 90% width, tablet (768-1024px) 80% max 600px, desktop (1024-1440px) 60% max 700px, ultra-wide (1440px+) max 800px
- **FR-027**: Modal MUST close via: X button (top-right), clicking outside modal area, pressing Escape key
- **FR-028**: Example sentences MUST have individual "翻译" toggle buttons - click to load/show translation below sentence (yellow background), click again (now showing "✕") to hide

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users complete vocabulary lookup (click word → view definition) 30% faster than current implementation (measure: time from card click to modal full display)
- **SC-002**: Click accuracy rate reaches 95%+ on first tap (mobile) or click (desktop) with no accidental adjacent element activation
- **SC-003**: Screen space utilization increases 30% on desktop (1440px+ screens) - measure: content area width 1400px vs previous 800px = 75% increase
- **SC-004**: Interface remains fully functional at 375px width with zero horizontal scrolling (test: all features accessible, all text readable)
- **SC-005**: Lighthouse accessibility audit achieves score of 100 with zero violations (automated test via Chrome DevTools)
- **SC-006**: axe DevTools scan reports zero accessibility violations (automated test via browser extension)
- **SC-007**: All interactive elements measure 44x44px minimum on mobile screens (manual DevTools measurement)
- **SC-008**: CSS file size remains under 100KB total (current: 35KB, target: <100KB including all new styles)
- **SC-009**: Tab transition completes within 200-300ms without visible jank (measure: Chrome DevTools Performance panel)
- **SC-010**: Translation auto-load succeeds within 2 seconds for 95th percentile of requests (measure: server logs)
- **SC-011**: Keyboard navigation completes full workflow (browse → open details → switch tabs → close) without mouse (test: unplug mouse, attempt all tasks)
- **SC-012**: User satisfaction feedback shows positive trend with phrases like "clearer," "easier," "faster," or "more professional" (post-release survey)

---

## Key Entities

> **Note**: This is a UI/UX feature - no new data entities are introduced. Changes affect presentation layer only.

### Modified Display Elements

**Word Card (Visual Component)**
- Entire card area becomes clickable target (not just text portion)
- Independent "翻" translation button removed
- Enhanced hover state: border changes to blue (#2563eb), card lifts 3px (`transform: translateY(-3px)`), shadow deepens
- Enforced touch target: 44x44px minimum height on mobile

**Detail Modal (Visual Component)**
- Content structure: word display (36px bold blue) → CEFR badge → auto-loaded translation → frequency → examples
- Translation area: skeleton screen during load, cached translations display instantly
- Example translations: individual toggle buttons per sentence
- Error handling: friendly messages, non-blocking retry buttons
- Responsive width: 90% (mobile) → 80% (tablet) → 60% (desktop) → max 800px (ultra-wide)

**Tab Navigation (New Visual Component)**
- Two tabs: "Words" and "Phrasal Verbs" with dynamic counts
- Active styling: blue text, blue bottom border, bold font
- Inactive styling: gray text, regular font, light gray hover background
- State persistence: filters and search preserved across tab switches
- Bilingual labels (desktop) vs simplified labels (mobile)

**Responsive Container (Visual Component)**
- Breakpoint-specific max-widths: 100% → 720px → 960px → 1280px → 1400px
- Always centered on screen
- Adaptive word card grid: 1 → 2-3 → 4 → 5 → 5-6 columns

---

## Assumptions & Constraints

### Assumptions

1. **Browser Support**: Users access via modern browsers (Chrome, Firefox, Safari, Edge) within last 2 versions supporting CSS Custom Properties, Flexbox, Grid
2. **Translation API Performance**: Backend translation endpoint maintains <5% error rate and <2s average response time (95th percentile)
3. **Network Conditions**: Majority of users have stable 3G or better connections
4. **Device Distribution**: Approximately 60% desktop, 30% mobile, 10% tablet (informs testing priorities)
5. **Content Characteristics**: Typical word/phrase length <50 characters (edge cases up to 100 characters handled via word-wrap)
6. **Translation Caching**: Backend implements translation caching to reduce redundant API calls
7. **User Workflow**: Users primarily access vocabulary list after document analysis completes (not during upload/processing)

### Constraints

**Technical Constraints**:
- **CSS-Only Implementation**: All visual changes must be pure CSS/HTML - no JavaScript refactoring allowed (maintains project simplicity)
- **Existing HTML Structure**: Must work with current Flask template structure without breaking changes
- **File Size Limit**: Total CSS file must remain <100KB for performance (current: 35KB, headroom: 65KB)
- **No New Dependencies**: Cannot add CSS frameworks, icon libraries, or build tools
- **Browser Compatibility**: Must support all modern browser CSS features (Custom Properties, Flexbox, Grid)

**Design Constraints**:
- **CEFR Color Preservation**: Existing level colors (#4CAF50 for A1, #F44336 for C2, etc.) must remain unchanged
- **Bilingual Requirement**: All UI elements show both English and Chinese (desktop) or Chinese only (mobile)
- **Design Token System**: Must use existing tokens from Feature 003 (--space-*, --color-*, --shadow-*)
- **Accessibility Standards**: Must meet WCAG 2.1 Level AA with no exceptions

**Business Constraints**:
- **No Backend Changes**: Backend API endpoints remain unchanged - this is UI-only enhancement
- **Backward Compatibility**: Existing bookmarks and URLs must continue to function
- **Rollback Safety**: Changes must be revertible without data loss or user disruption

---

## Dependencies

### Internal Dependencies

1. **Feature 003: UI/UX Optimization** (Status: ✅ Complete, merged to main)
   - Provides: Design token system (--space-*, --color-*, --shadow-*)
   - Required for: Consistent spacing, colors, shadows across all new styles
   - Impact: Critical - cannot implement without these tokens

2. **Feature 002: Bilingual UI Translation** (Status: ✅ Complete)
   - Provides: Translation API endpoint `/api/translate`
   - Required for: Auto-loading Chinese translations in detail modal
   - Impact: High - feature degrades gracefully if API unavailable (shows error)

3. **Existing Flask Templates** (Current main branch)
   - Provides: HTML structure for results page
   - Required for: CSS selectors and DOM manipulation
   - Impact: Medium - changes to HTML may require CSS adjustments

4. **Existing JavaScript** (Current main branch)
   - Provides: Modal open/close, AJAX translation requests
   - Required for: Interactive behavior
   - Impact: Medium - may need minor updates for tab switching logic

### External Dependencies

**None** - This feature has no external library or service dependencies beyond those already in the project.

### Dependency Risks

| Dependency | Risk Level | Mitigation Strategy |
|------------|------------|---------------------|
| Feature 003 tokens | Low | Tokens already merged and stable - validate names before implementation |
| Translation API | Medium | Handle errors gracefully with retry - feature works without translations |
| HTML structure | Low | Use semantic class names, avoid overly specific selectors |
| Browser CSS support | Low | Target modern browsers only, document minimum versions |

---

## Out of Scope

The following items are explicitly **not included** in this feature:

### Functional Exclusions

1. **Advanced Translation Features**: Translation history, favorites, multiple sources, user edits, quality ratings
2. **Content Management**: Word list export/import, custom grouping, study progress tracking, flashcard mode
3. **Personalization**: User preferences (e.g., "always show translations"), theme customization, font size controls, layout density options
4. **Social Features**: Sharing lists, collaborative study, comments/annotations, teacher-student communication
5. **Advanced Search**: Regular expressions, phonetic search, search history, saved searches
6. **Gamification**: Study timers, progress bars, achievement badges, leaderboards

### Technical Exclusions

1. **Backend Enhancements**: API optimization, database schema changes, improved translation caching (relies on existing backend)
2. **Advanced Interactions**: Drag-and-drop, multi-select bulk operations, gesture controls (swipe, pinch), voice commands
3. **Offline Capabilities**: Service workers, offline caching, Progressive Web App features, local storage
4. **Analytics**: User behavior tracking, heatmaps, A/B testing infrastructure, custom event logging

### Future Considerations

Items that may become separate features:
- **Dark Mode Theme** (CSS-only theme switcher)
- **Advanced Filtering** (filter by frequency, part of speech, custom tags)
- **Pronunciation Audio** (requires audio file integration)
- **Word Etymology** (requires external data source)

---

## Open Questions

~~**[NEEDS CLARIFICATION: Tab Content Transition Animation Style]**~~ ✅ **RESOLVED**

**Context**: FR-009 specifies "tab switching MUST trigger 200-300ms fade transition" but exact animation behavior was not defined in the original requirements.

**Decision**: **Option A - Simple Fade (opacity 0 → 1)**

**Rationale**:
- Simplest to implement with lowest risk of layout issues
- 200ms duration provides quick, responsive feel
- No layout shifts or content jumping
- Works consistently across all content lengths and breakpoints
- Aligns with project simplicity principle (CSS-only, no JavaScript complexity)

**Implementation Details** (for FR-009):
- Outgoing tab content: fade out (opacity 1 → 0, 100ms)
- Incoming tab content: fade in (opacity 0 → 1, 200ms) with 100ms delay
- Total transition time: 300ms (within 200-300ms requirement)
- Timing function: `ease-in-out` for smooth start and end
- No transform properties (prevents layout shifts)
- Content visibility managed via `display: none` after fade-out completes

---

## Appendix

### Glossary

| Term | Definition |
|------|------------|
| **CEFR** | Common European Framework of Reference for Languages - standardized proficiency levels A1 (beginner) through C2 (mastery) |
| **Skeleton Screen** | Placeholder UI with gray boxes matching content shape, displayed during loading to prevent layout shifts |
| **Design Tokens** | CSS Custom Properties (variables) ensuring consistent spacing, colors, typography (e.g., `--space-4`, `--primary-color`) |
| **Touch Target** | Minimum tappable area for mobile interactions - WCAG recommends 44x44px to prevent mis-taps |
| **Focus Indicator** | Visual outline showing which element has keyboard focus, required for accessibility (e.g., blue 2px border) |
| **Modal** | Overlay window displaying content above main page, typically with darkened backdrop |
| **Breakpoint** | Screen width threshold where responsive layout changes (e.g., 768px transitions from mobile to tablet layout) |
| **WCAG 2.1 AA** | Web Content Accessibility Guidelines Level AA - legally required standard for accessibility compliance |
| **Contrast Ratio** | Luminance difference between text and background - 4.5:1 minimum for normal text, 3:1 for large text (WCAG AA) |
| **Shimmer Effect** | Animated gradient sweep across skeleton screens simulating loading progress |

### Reference Documents

| Document | Location | Purpose |
|----------|----------|---------|
| Feature 003 Specification | `specs/003-ui-ux-optimization/spec.md` | Foundation design token system |
| Feature 003 Data Model | `specs/003-ui-ux-optimization/data-model.md` | CSS token structure reference |
| WCAG 2.1 Quick Reference | https://www.w3.org/WAI/WCAG21/quickref/ | Accessibility compliance standards |
| Current Styles | `src/vocab_analyzer/web/static/styles.css` | Existing CSS to enhance (35KB baseline) |
| Flask Template | `src/vocab_analyzer/web/static/index.html` | HTML structure for selectors |
| WebAIM Contrast Checker | https://webaim.org/resources/contrastchecker/ | Tool for validating color contrast |

---

**Specification Status**: ✅ **VALIDATED & APPROVED** - Ready for Planning

**Validation Summary**:
- ✅ All 13 quality checks passed (see `checklists/requirements.md`)
- ✅ [NEEDS CLARIFICATION] marker resolved (tab animation: Option A - Simple fade)
- ✅ Specification completeness: 100%
- ✅ Traceability: All requirements mapped to user stories and success criteria
- ✅ Constitution compliance: Full compliance with all 6 principles

**Next Steps**:
1. ✅ **Clarification Complete**: Tab transition animation defined (simple fade, 300ms total)
2. ✅ **Validation Complete**: Quality checklist passed with 13/13 checks
3. 🚀 **Ready for Planning**: Use `/speckit.plan` to generate implementation plan

**Prepared by**: Claude (Speckit Framework)
**Review Date**: 2025-11-04
**Validation Date**: 2025-11-04
**Status**: Approved for Implementation Planning
