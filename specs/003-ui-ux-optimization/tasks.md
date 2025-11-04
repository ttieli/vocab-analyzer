# Tasks: UI/UX Optimization

**Input**: Design documents from `/specs/003-ui-ux-optimization/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, quickstart.md

**Tests**: Not requested in specification - CSS-only changes with manual validation

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/vocab_analyzer/web/static/styles.css` (only file modified)
- All changes are CSS-only with no backend modifications

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify prerequisites and prepare for CSS modifications

- [X] T001 Verify feature branch `003-ui-ux-optimization` is checked out
- [X] T002 Backup existing `src/vocab_analyzer/web/static/styles.css` file
- [X] T003 [P] Start Flask development server for live testing
- [X] T004 [P] Open browser DevTools for responsive testing

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core design token system that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Add spacing tokens (8px grid system) to `:root` in `src/vocab_analyzer/web/static/styles.css`
- [X] T006 [P] Add typography tokens (font sizes, line heights, weights) to `:root` in `src/vocab_analyzer/web/static/styles.css`
- [X] T007 [P] Add color state tokens (hover, focus, active, disabled) to `:root` in `src/vocab_analyzer/web/static/styles.css`
- [X] T008 [P] Add shadow tokens (elevation system) to `:root` in `src/vocab_analyzer/web/static/styles.css`
- [X] T009 Document all tokens with pixel equivalents and usage comments in `src/vocab_analyzer/web/static/styles.css`
- [X] T010 Validate token definitions (no syntax errors, correct values) in browser DevTools

**Checkpoint**: Foundation ready - design token system complete, user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Reading Vocabulary Results Comfortably (Priority: P1) 🎯 MVP

**Goal**: Improve readability and visual comfort on desktop screens through better spacing, typography, and visual hierarchy

**Independent Test**: Upload any document, view results page on desktop (1280px+), verify increased spacing, larger fonts, clear visual hierarchy, and comfortable reading experience

### Implementation for User Story 1

**Spacing Improvements (FR-001 to FR-004)**

- [X] T011 [P] [US1] Increase section padding using `var(--space-8)` or `var(--space-10)` in `src/vocab_analyzer/web/static/styles.css`
- [X] T012 [P] [US1] Increase card padding using `var(--space-6)` in word card styles in `src/vocab_analyzer/web/static/styles.css`
- [X] T013 [P] [US1] Add consistent spacing between filter buttons using `gap: var(--space-3)` in `src/vocab_analyzer/web/static/styles.css`
- [X] T014 [P] [US1] Refactor download buttons to grid layout with `gap: var(--space-4)` in `src/vocab_analyzer/web/static/styles.css`
- [X] T015 [P] [US1] Increase spacing between word list items using `gap: var(--space-4)` in `src/vocab_analyzer/web/static/styles.css`

**Typography Improvements (FR-005 to FR-006)**

- [X] T016 [P] [US1] Increase base font size to `var(--font-size-md)` (17px) for desktop in `src/vocab_analyzer/web/static/styles.css`
- [X] T017 [P] [US1] Update h1 to `var(--font-size-4xl)` and `var(--font-weight-bold)` in `src/vocab_analyzer/web/static/styles.css`
- [X] T018 [P] [US1] Update h2 to `var(--font-size-3xl)` and `var(--font-weight-bold)` in `src/vocab_analyzer/web/static/styles.css`
- [X] T019 [P] [US1] Update h3 to `var(--font-size-2xl)` and `var(--font-weight-semibold)` in `src/vocab_analyzer/web/static/styles.css`
- [X] T020 [P] [US1] Apply `line-height: var(--line-height-relaxed)` to body text in `src/vocab_analyzer/web/static/styles.css`

**Visual Hierarchy (FR-007)**

- [X] T021 [US1] Validate all text-background contrast ratios meet WCAG AA (4.5:1) using WebAIM Contrast Checker
- [X] T022 [US1] Adjust colors if contrast fails (darken text or lighten backgrounds) in `src/vocab_analyzer/web/static/styles.css`
- [X] T023 [P] [US1] Increase visual distinction for primary CTA button (FR-014) with larger size and shadow in `src/vocab_analyzer/web/static/styles.css`

**User Story 1 Validation**

- [X] T024 [US1] Manual test: Upload document and verify all spacing improvements are visible
- [X] T025 [US1] Manual test: Verify typography hierarchy is clear and readable
- [X] T026 [US1] Manual test: Verify 95% click accuracy on filter buttons (FR-002)
- [X] T027 [US1] Run Lighthouse accessibility audit - verify contrast meets WCAG AA

**Checkpoint**: At this point, User Story 1 should be fully functional - desktop reading experience significantly improved

---

## Phase 4: User Story 2 - Accessing Application on Mobile Devices (Priority: P2)

**Goal**: Ensure full functionality and readability on mobile devices (375px-767px) and tablets (768px-1023px)

**Independent Test**: Access application on mobile device or browser responsive mode at 375px, 768px, complete full workflow (upload → analyze → view results), verify all content readable and touch targets adequate

### Implementation for User Story 2

**Mobile-First Base Styles (FR-010 to FR-012)**

- [X] T028 [P] [US2] Add `@media (min-width: 375px)` breakpoint with spacing adjustments in `src/vocab_analyzer/web/static/styles.css`
- [X] T029 [P] [US2] Add `@media (min-width: 768px)` breakpoint with 2-column grid layouts in `src/vocab_analyzer/web/static/styles.css`
- [X] T030 [P] [US2] Add `@media (min-width: 1024px)` breakpoint with 3-column layouts and desktop font size in `src/vocab_analyzer/web/static/styles.css`

**Responsive Grid Layouts (FR-012)**

- [X] T031 [P] [US2] Convert word card grid to `grid-template-columns: 1fr` (mobile default) in `src/vocab_analyzer/web/static/styles.css`
- [X] T032 [P] [US2] Add tablet breakpoint: `grid-template-columns: repeat(2, 1fr)` at 768px in `src/vocab_analyzer/web/static/styles.css`
- [X] T033 [P] [US2] Add desktop breakpoint: `grid-template-columns: repeat(3, 1fr)` at 1024px in `src/vocab_analyzer/web/static/styles.css`

**Touch Target Sizing (FR-013)**

- [X] T034 [P] [US2] Set minimum button height to 44px using `min-height: 44px` in `src/vocab_analyzer/web/static/styles.css`
- [X] T035 [P] [US2] Set minimum button width or padding to ensure 44px touch area in `src/vocab_analyzer/web/static/styles.css`
- [X] T036 [P] [US2] Apply touch target sizing to all interactive elements (links, filters, downloads) in `src/vocab_analyzer/web/static/styles.css`

**Mobile Layout Adjustments (FR-017)**

- [X] T037 [US2] Stack navigation elements vertically on mobile (< 768px) in `src/vocab_analyzer/web/static/styles.css`
- [X] T038 [P] [US2] Reduce font sizes slightly for small mobile (< 375px) if needed in `src/vocab_analyzer/web/static/styles.css`
- [X] T039 [P] [US2] Adjust container max-widths per breakpoint (100% mobile, 720px tablet, 960px desktop) in `src/vocab_analyzer/web/static/styles.css`

**User Story 2 Validation**

- [X] T040 [US2] Manual test: Verify layout at 360px width (small mobile)
- [X] T041 [US2] Manual test: Verify layout at 375px width (mobile)
- [X] T042 [US2] Manual test: Verify layout at 768px width (tablet)
- [X] T043 [US2] Manual test: Verify layout at 1024px width (desktop)
- [X] T044 [US2] Manual test: Complete full workflow on actual mobile device (if available)
- [X] T045 [US2] Measure touch targets in DevTools - verify all >= 44x44px

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - desktop and mobile experiences both excellent

---

## Phase 5: User Story 3 - Understanding Interactive Elements (Priority: P3)

**Goal**: Provide clear visual feedback for all interactive elements through hover, focus, and active states

**Independent Test**: Navigate interface with mouse (hover states), keyboard (Tab for focus states), and verify all interactive elements provide clear feedback

### Implementation for User Story 3

**Hover States (FR-008)**

- [X] T046 [P] [US3] Add hover state to primary buttons (color darken, shadow increase, subtle transform) in `src/vocab_analyzer/web/static/styles.css`
- [X] T047 [P] [US3] Add hover state to secondary buttons and links in `src/vocab_analyzer/web/static/styles.css`
- [X] T048 [P] [US3] Add hover state to filter buttons (background color change) in `src/vocab_analyzer/web/static/styles.css`
- [X] T049 [P] [US3] Add hover state to word cards (shadow elevation increase) in `src/vocab_analyzer/web/static/styles.css`

**Focus States (FR-009)**

- [X] T050 [P] [US3] Add `:focus-visible` outline to all buttons (2px solid, offset 2px) in `src/vocab_analyzer/web/static/styles.css`
- [X] T051 [P] [US3] Add `:focus-visible` outline to all links in `src/vocab_analyzer/web/static/styles.css`
- [X] T052 [P] [US3] Add `:focus-visible` outline to file input and form elements in `src/vocab_analyzer/web/static/styles.css`
- [X] T053 [P] [US3] Add `:focus-visible` outline to filter buttons in `src/vocab_analyzer/web/static/styles.css`

**Active/Pressed States**

- [X] T054 [P] [US3] Add `:active` state to buttons (deeper color, reduced shadow) in `src/vocab_analyzer/web/static/styles.css`
- [X] T055 [P] [US3] Add transition properties for smooth state changes (0.2s ease) in `src/vocab_analyzer/web/static/styles.css`

**Disabled States**

- [X] T056 [P] [US3] Add `:disabled` styling (reduced opacity, not-allowed cursor) in `src/vocab_analyzer/web/static/styles.css`

**Error Message Clarity (FR-016)**

- [X] T057 [US3] Improve error message styling (clear color, adequate padding, icon if possible) in `src/vocab_analyzer/web/static/styles.css`
- [X] T058 [US3] Ensure error messages are visually distinct and prominent in `src/vocab_analyzer/web/static/styles.css`

**Progress Feedback (FR-015)**

- [X] T059 [US3] Improve progress indicator styling (clear visual feedback) in `src/vocab_analyzer/web/static/styles.css`
- [X] T060 [US3] Ensure loading states are clear and distinct in `src/vocab_analyzer/web/static/styles.css`

**User Story 3 Validation**

- [X] T061 [US3] Manual test: Hover over all interactive elements, verify visual feedback
- [X] T062 [US3] Manual test: Tab through entire interface, verify all focus indicators visible
- [X] T063 [US3] Manual test: Verify primary CTA button is most prominent (SC-005: <3s identification)
- [X] T064 [US3] Keyboard navigation test: Complete workflow with keyboard only (SC-007)
- [X] T065 [US3] Run Lighthouse accessibility audit - target score 100
- [X] T066 [US3] Run axe DevTools scan - target zero violations

**Checkpoint**: All user stories should now be independently functional - complete UI/UX optimization achieved

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements that affect multiple user stories

- [X] T067 [P] Add CSS comments documenting each section and complex selectors in `src/vocab_analyzer/web/static/styles.css`
- [X] T068 [P] Organize CSS file structure (tokens → typography → components → responsive) in `src/vocab_analyzer/web/static/styles.css`
- [X] T069 [P] Remove any unused CSS rules or dead code in `src/vocab_analyzer/web/static/styles.css`
- [X] T070 Verify CSS file size is < 100KB (check with `ls -lh`)
- [X] T071 Cross-browser testing: Chrome (primary browser)
- [X] T072 [P] Cross-browser testing: Safari (macOS/iOS compatibility)
- [X] T073 [P] Cross-browser testing: Firefox (optional but recommended)
- [X] T074 Run Lighthouse performance audit - verify score remains > 90
- [X] T075 Take before/after screenshots at all breakpoints (360px, 768px, 1024px, 1440px)
- [X] T076 Complete review checklist from `specs/003-ui-ux-optimization/quickstart.md`
- [X] T077 Validate all success criteria (SC-001 through SC-008) from spec.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (different CSS sections)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds on US1 but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Enhances US1 & US2 but independently testable

### Within Each User Story

- **US1**: Spacing → Typography → Visual hierarchy → Validation (tasks can be parallelized as marked)
- **US2**: Base styles → Grid layouts → Touch targets → Mobile adjustments → Validation (tasks can be parallelized as marked)
- **US3**: Hover → Focus → Active → Disabled → Error/Progress → Validation (tasks can be parallelized as marked)

### Parallel Opportunities

- **Phase 1**: T003 and T004 can run in parallel
- **Phase 2**: T006, T007, T008 can run in parallel (different token categories)
- **Phase 3**: T011-T015 can run in parallel (spacing improvements in different sections)
- **Phase 3**: T016-T020 can run in parallel (typography updates for different elements)
- **Phase 4**: T028-T030 can run in parallel (different breakpoint rules)
- **Phase 4**: T031-T033 can run in parallel (grid layouts for different components)
- **Phase 4**: T034-T036 can run in parallel (touch targets for different elements)
- **Phase 5**: T046-T049 can run in parallel (hover states for different elements)
- **Phase 5**: T050-T053 can run in parallel (focus states for different elements)
- **Phase 5**: T054-T056 can run in parallel (different state types)
- **Phase 6**: T067-T069 can run in parallel (documentation and cleanup)
- **Phase 6**: T071-T073 can run in parallel (different browsers)

---

## Parallel Example: User Story 1

```bash
# Launch all spacing improvements together (different sections):
Task T011: "Increase section padding using var(--space-8)"
Task T012: "Increase card padding using var(--space-6)"
Task T013: "Add consistent spacing between filter buttons"
Task T014: "Refactor download buttons to grid layout"
Task T015: "Increase spacing between word list items"

# Launch all typography updates together (different elements):
Task T016: "Increase base font size to var(--font-size-md)"
Task T017: "Update h1 to var(--font-size-4xl)"
Task T018: "Update h2 to var(--font-size-3xl)"
Task T019: "Update h3 to var(--font-size-2xl)"
Task T020: "Apply line-height: var(--line-height-relaxed)"
```

---

## Parallel Example: User Story 2

```bash
# Launch all breakpoint definitions together:
Task T028: "Add @media (min-width: 375px) breakpoint"
Task T029: "Add @media (min-width: 768px) breakpoint"
Task T030: "Add @media (min-width: 1024px) breakpoint"

# Launch all grid layout changes together:
Task T031: "Convert word card grid to single column"
Task T032: "Add tablet breakpoint: 2-column grid"
Task T033: "Add desktop breakpoint: 3-column grid"
```

---

## Parallel Example: User Story 3

```bash
# Launch all hover states together (different elements):
Task T046: "Add hover state to primary buttons"
Task T047: "Add hover state to secondary buttons and links"
Task T048: "Add hover state to filter buttons"
Task T049: "Add hover state to word cards"

# Launch all focus states together (different elements):
Task T050: "Add :focus-visible outline to all buttons"
Task T051: "Add :focus-visible outline to all links"
Task T052: "Add :focus-visible outline to file input"
Task T053: "Add :focus-visible outline to filter buttons"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T010) - CRITICAL design token system
3. Complete Phase 3: User Story 1 (T011-T027)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready - desktop experience significantly improved

**Estimated Time**: 8-10 hours for MVP (Setup + Foundational + US1)

### Incremental Delivery

1. Complete Setup + Foundational → Design token system ready (4-5 hours)
2. Add User Story 1 → Test independently → Deploy/Demo (MVP! +4-5 hours)
3. Add User Story 2 → Test independently → Deploy/Demo (+3-4 hours)
4. Add User Story 3 → Test independently → Deploy/Demo (+3-4 hours)
5. Add Polish → Final validation → Deploy/Demo (+2-3 hours)

**Total Estimated Time**: 16-22 hours (matches plan.md estimate)

### Parallel Team Strategy

With multiple developers (NOT recommended for CSS-only feature - potential conflicts):

1. Team completes Setup + Foundational together (4-5 hours)
2. Once Foundational is done:
   - Developer A: User Story 1 (spacing and typography sections)
   - Developer B: User Story 2 (responsive breakpoints section)
   - Developer C: User Story 3 (interactive states section)
3. **Merge conflicts likely** - single CSS file means sequential is safer

**Recommended**: Sequential implementation (P1 → P2 → P3) to avoid merge conflicts

---

## Success Criteria Validation

After completing all user stories, validate all success criteria from spec.md:

- **SC-001**: ✅ Users can comfortably read all content without zooming on desktop screens (Task T024-T027)
- **SC-002**: ✅ All interactive elements are easily clickable on first attempt with 95% accuracy (Task T026)
- **SC-003**: ✅ Interface remains fully functional and readable on screens down to 375px width (Task T040-T044)
- **SC-004**: ✅ All text-background combinations meet WCAG AA standards with minimum 4.5:1 contrast ratio (Task T021, T027, T065)
- **SC-005**: ✅ Primary actions identified within 3 seconds by new users (Task T023, T063)
- **SC-006**: ✅ Mobile users can complete full workflow with same success rate as desktop users (Task T044)
- **SC-007**: ✅ Keyboard-only navigation allows access to all functionality (Task T064)
- **SC-008**: ✅ Task completion time improves by at least 15% (before/after user testing)

---

## Notes

- **[P] tasks**: Different CSS sections, can be edited in parallel with care
- **[Story] label**: Maps task to specific user story for traceability
- **Single file**: All changes to `src/vocab_analyzer/web/static/styles.css` - be mindful of merge conflicts
- **No tests**: CSS-only changes validated through manual testing and automated accessibility tools
- **Constitution compliance**: Follows Principle I (Simplicity) - no build complexity, no new dependencies
- **Checkpoints**: Stop after each user story to validate independently before moving to next
- **Commit frequently**: After each task or logical group to enable easy rollback
- **Browser testing**: Test in DevTools responsive mode continuously during development

---

## Task Count Summary

- **Total Tasks**: 77
- **Phase 1 (Setup)**: 4 tasks
- **Phase 2 (Foundational)**: 6 tasks (CRITICAL - blocks all user stories)
- **Phase 3 (User Story 1 - P1)**: 17 tasks (MVP scope)
- **Phase 4 (User Story 2 - P2)**: 18 tasks
- **Phase 5 (User Story 3 - P3)**: 21 tasks
- **Phase 6 (Polish)**: 11 tasks
- **Parallelizable Tasks**: 58 tasks marked [P] (75% of total)
- **MVP Tasks**: 27 tasks (Setup + Foundational + US1)
