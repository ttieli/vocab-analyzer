# Feature Specification: Immersive Full-Text Reading View

**Feature Branch**: `005-reading-view`
**Created**: 2025-11-05
**Status**: Draft
**Input**: Add immersive full-text reading view with CEFR-colored, clickable words for in-context vocabulary learning

---

## Executive Summary

### What We're Building

A focused reading experience that transforms the vocabulary analyzer from an analysis tool into an immersive learning environment. This feature adds a dedicated "全文阅读" (Full-Text Reading) view where learners can read the entire analyzed book with CEFR-colored words that are clickable for instant definitions.

**Core Value Proposition**: Enable learners to practice reading in context while seamlessly accessing vocabulary support, creating a natural bridge between vocabulary analysis and actual reading practice.

**Key Capabilities**:
1. **Contextual Reading**: Display full processed text with CEFR color-coding for immediate difficulty assessment
2. **One-Click Definitions**: Click any word to see translation and details (reuses existing modal from Feature 004)
3. **Clean Reading Interface**: Minimal distractions - just text and color coding, no badges or clutter
4. **Performance**: Renders 300KB+ texts in under 1 second with smooth scrolling

---

## Clarifications

### Session 2025-11-05

- Q: How to handle phrasal verbs in reading view? → A: Color only individual words (first word of multi-word phrasal verbs like "make" in "make up")
- Q: Should we show a CEFR legend in reading view? → A: No legend - reading view shows only word underline colors to indicate CEFR levels, no detailed explanations
- Q: What to do if processed_text is missing or empty? → A: Always show reading tab, display "暂无文本 / No text available" message in panel

---

## User Scenarios & Testing

### User Story 1 - Seamless View Switching (Priority: P0)

**Description**: After completing vocabulary analysis, learners can instantly switch between vocabulary list view and full-text reading view without losing filters or state.

**Why this priority**: This is the entry point to the feature - users need discoverable, friction-free access to the reading view. Poor integration would render the feature invisible.

**Independent Test**: Complete a book analysis, switch to reading view, apply a CEFR filter in vocabulary view, then verify reading view highlights only those words.

**Acceptance Scenarios**:

1. **Given** user completes book analysis **When** results page displays **Then** tab navigation shows three tabs: "单词 / Words", "短语动词 / Phrasal Verbs", "全文阅读 / Reading View"
2. **Given** user views vocabulary list **When** user clicks "全文阅读" tab **Then** view transitions smoothly (200-300ms fade), showing full processed text with CEFR-colored words
3. **Given** user applies CEFR filter "B2" in vocabulary view **When** user switches to reading view **Then** only B2 words are highlighted in color, others display in default text color
4. **Given** user scrolls to 50% position in reading view **When** user switches to vocabulary tab and back **Then** reading view preserves scroll position (localStorage)
5. **Given** user searches for "make" in vocabulary view **When** user switches to reading view **Then** matching words are highlighted with yellow background + CEFR color
6. **Given** reading view is active **When** user clicks "Analyze Another Book" **Then** all state clears (filters, scroll position, cached data)

**Key Integration Points**:
- Reuse existing tab navigation system (Feature 004)
- Integrate with existing CEFR filter state
- Integrate with existing word search functionality
- Share scroll position state with vocabulary tabs

---

### User Story 2 - In-Context Word Lookup (Priority: P0)

**Description**: While reading, learners click any colored word to see its translation, CEFR level, and examples without losing their place in the text.

**Why this priority**: This is the core interaction that justifies the reading view - seamless vocabulary support during reading. Must feel natural and instant.

**Independent Test**: Open reading view, click any colored word, verify modal opens with translation, click X or Escape, verify modal closes and reading position is preserved.

**Acceptance Scenarios**:

1. **Given** user reads in reading view **When** user hovers over colored word **Then** cursor changes to pointer, word background lightens slightly (hover state)
2. **Given** user clicks colored word "ambitious" (C1) **When** modal opens **Then** modal displays word, C1 badge, auto-loaded Chinese translation, frequency count, 3-5 example sentences from the book
3. **Given** modal is open **When** translation is cached **Then** Chinese translation displays immediately with "缓存" label (reuse Feature 002 cache)
4. **Given** modal is open **When** translation not cached **Then** skeleton screen appears, translation loads within 2 seconds (reuse Feature 002 API)
5. **Given** user clicks word "make up" (phrasal verb) **When** modal opens **Then** modal correctly identifies as phrasal verb, shows both words highlighted, loads phrasal verb translation
6. **Given** modal is open **When** user clicks X, outside modal, or presses Escape **Then** modal closes, focus returns to reading view at same scroll position
7. **Given** user clicks non-colored word (proper noun, A1 word filtered out) **When** clicking **Then** no modal opens, word behaves as regular text

**Technical Requirements**:
- Reuse `showWordDetails()` from `app.js:444` (Feature 004)
- Reuse translation caching from Feature 002
- Reuse modal HTML structure and CSS
- Add click handlers only to CEFR-colored words
- Preserve scroll position across modal open/close

---

### User Story 3 - Comfortable Reading Experience (Priority: P1)

**Description**: The reading view provides professional typography, proper spacing, and visual hierarchy optimized for extended reading sessions.

**Why this priority**: Poor typography causes eye strain and reduces comprehension. This feature aims to support 30+ minute reading sessions, requiring professional-grade readability.

**Independent Test**: Open 50-page book in reading view, read for 10 minutes, verify text is easy to scan, paragraphs are clearly separated, and line length is comfortable (60-80 characters per line).

**Acceptance Scenarios**:

1. **Given** user opens reading view **When** viewing text **Then** line height is 1.6-1.8, font size 16-18px (responsive), max line width 75ch (680-750px)
2. **Given** reading view displays **When** viewing paragraphs **Then** paragraph spacing is 1.5em, first line has no indent (modern web style)
3. **Given** user views text on desktop (1440px) **When** container expands **Then** text column max-width is 800px (centered), wide margins prevent eye strain
4. **Given** user views text on mobile (375px) **When** container scales **Then** font size reduces to 16px, margins shrink to 16px (maximizes readable area)
5. **Given** text contains multiple paragraphs **When** scrolling **Then** scroll is smooth (no jank), colored words maintain legibility against background
6. **Given** user reads for 5+ minutes **When** evaluating comfort **Then** no eye strain, text color contrast meets WCAG AA (4.5:1 minimum for colored words)

**Typography Specifications**:
- Font family: System font stack (inherit from existing styles.css)
- Font size: 16px (mobile) → 18px (tablet+)
- Line height: 1.7 (optimal for extended reading)
- Line length: 60-75 characters per line (max-width: 75ch or 800px)
- Paragraph spacing: 1.5em bottom margin
- CEFR word colors: Inherit from existing `--cefr-a1` through `--cefr-c2-plus` tokens
- Background: White (#FFFFFF) with subtle texture optional
- Text color: Dark gray (#2c3e50) for uncolored words

---

### User Story 4 - Performance with Large Texts (Priority: P1)

**Description**: Reading view renders and scrolls smoothly even with 300KB+ text files (approximately 50,000 words or 150-200 pages).

**Why this priority**: Many classic novels and textbooks exceed 200 pages. Slow rendering or janky scrolling would make the feature unusable for real books.

**Independent Test**: Upload a 300KB text file (e.g., "Pride and Prejudice"), analyze it, switch to reading view, verify it renders in <1 second, and scrolling is smooth at 60fps.

**Acceptance Scenarios**:

1. **Given** user analyzes 300KB text file **When** switching to reading view **Then** initial render completes in <1 second, shows skeleton screen during processing if needed
2. **Given** reading view loads 50,000 words **When** user scrolls rapidly **Then** scrolling maintains 60fps, no visible lag or stuttering
3. **Given** text contains 5,000 CEFR-colored words **When** rendering **Then** color styling completes without blocking UI thread (requestIdleCallback or CSS)
4. **Given** user applies filter "C1 only" **When** view re-renders **Then** update completes in <300ms with smooth transition
5. **Given** large text is displayed **When** user clicks word **Then** modal opens in <100ms (no delay from page complexity)

**Performance Requirements**:
- Initial render: <1s for 300KB text
- Scroll performance: 60fps (16ms frame budget)
- Filter re-render: <300ms
- Modal open time: <100ms
- Memory usage: <50MB additional for reading view (profile with Chrome DevTools)
- Virtual scrolling: NOT required for MVP (HTML/CSS can handle 300KB efficiently)

**Implementation Notes**:
- Use `<span class="cefr-word" data-word="..." data-level="B2">` for colored words
- Avoid excessive DOM depth (paragraphs → spans, no nested divs)
- Use CSS classes for colors (not inline styles)
- Consider `will-change: transform` for scroll container if needed
- Profile with Lighthouse Performance audit (score >90)

---

## Technical Architecture

### Data Flow

```
Analysis Results (app.js state)
    ↓
processedText (already exists in results.analysis_results)
    ↓
parseTextForReading(processedText) → HTML with <span> wrappers
    ↓
Render in #reading-panel (new tab panel)
    ↓
Attach click handlers to .cefr-word spans
    ↓
Click → showWordDetails(wordData) [reuse Feature 004]
```

### Component Structure

```
Tab Navigation (existing)
    ├── Words Tab (existing)
    ├── Phrasal Verbs Tab (existing)
    └── Reading View Tab (NEW)
        └── #reading-panel (NEW)
            ├── .reading-container (NEW)
            │   └── .reading-content (NEW)
            │       └── <p> paragraphs with <span class="cefr-word">
            └── Word Detail Modal (reuse existing)
```

### File Changes

**HTML** (`index.html` lines ~111-161):
```html
<!-- Add third tab button after phrasal verbs tab -->
<button class="tab-btn"
        id="reading-tab"
        role="tab"
        aria-selected="false"
        aria-controls="reading-panel"
        data-tab="reading">
    <span class="bilingual">
        <span class="cn">全文阅读</span>
        <span class="en">Reading View</span>
    </span>
</button>

<!-- Add reading panel after phrases-panel -->
<div id="reading-panel"
     class="tab-panel"
     role="tabpanel"
     aria-labelledby="reading-tab"
     tabindex="0"
     hidden>
    <div class="reading-container">
        <div class="reading-content" id="reading-content">
            <!-- Processed text will be populated by JavaScript -->
        </div>
    </div>
</div>
```

**CSS** (`styles.css` new section ~line 2100+):
```css
/* ============================================
   Feature 005: Immersive Reading View
   ============================================ */

/* Reading container - centered column */
.reading-container {
    width: 100%;
    max-width: 800px;
    margin: 0 auto;
    padding: var(--space-6) var(--space-4);
}

/* Reading content - typography optimized */
.reading-content {
    font-family: var(--font-family);
    font-size: 16px;
    line-height: 1.7;
    color: var(--text-primary);
}

.reading-content p {
    margin-bottom: 1.5em;
}

/* CEFR colored words - clickable */
.cefr-word {
    cursor: pointer;
    border-bottom: 1px dotted currentColor;
    transition: background-color 0.15s ease;
}

.cefr-word:hover {
    background-color: rgba(0, 0, 0, 0.05);
}

/* Apply CEFR colors */
.cefr-word[data-level="A1"] { color: var(--cefr-a1); }
.cefr-word[data-level="A2"] { color: var(--cefr-a2); }
.cefr-word[data-level="B1"] { color: var(--cefr-b1); }
.cefr-word[data-level="B2"] { color: var(--cefr-b2); }
.cefr-word[data-level="C1"] { color: var(--cefr-c1); }
.cefr-word[data-level="C2"] { color: var(--cefr-c2); }
.cefr-word[data-level="C2+"] { color: var(--cefr-c2-plus); }

/* Search highlighting */
.cefr-word.search-match {
    background-color: rgba(255, 235, 59, 0.4);
}

/* Responsive typography */
@media (min-width: 768px) {
    .reading-content {
        font-size: 18px;
    }
    .reading-container {
        padding: var(--space-8) var(--space-6);
    }
}

@media (min-width: 1024px) {
    .reading-content {
        max-width: 75ch; /* ~60-75 characters per line */
    }
}
```

**JavaScript** (`app.js` new functions):
```javascript
// Parse processed text into reading view HTML
function parseTextForReading(processedText, analysisResults) {
    const container = document.getElementById('reading-content');
    if (!container) return;

    // Get current filter state
    const activeLevel = document.querySelector('.filter-btn.active')?.getAttribute('data-level');
    const searchTerm = document.getElementById('word-search')?.value.toLowerCase() || '';

    // Split into paragraphs
    const paragraphs = processedText.split('\n\n').filter(p => p.trim());

    // Build HTML
    let html = '';
    paragraphs.forEach(para => {
        html += '<p>';

        // Tokenize paragraph into words
        const tokens = para.split(/(\s+)/); // Preserve whitespace

        tokens.forEach(token => {
            if (!token.trim()) {
                html += token; // Whitespace
                return;
            }

            // Check if token is a known vocabulary word
            const wordData = findWordData(token, analysisResults);

            if (wordData) {
                // Apply filter
                if (activeLevel !== 'all' && wordData.cefr_level !== activeLevel) {
                    html += token; // Not filtered, show as plain text
                    return;
                }

                // Check search match
                const matchesSearch = !searchTerm || token.toLowerCase().includes(searchTerm);
                const searchClass = matchesSearch ? ' search-match' : '';

                // Create colored, clickable span
                html += `<span class="cefr-word${searchClass}"
                              data-word="${wordData.word}"
                              data-level="${wordData.cefr_level}"
                              onclick="handleWordClick('${wordData.word}')">${token}</span>`;
            } else {
                html += token; // Regular text
            }
        });

        html += '</p>';
    });

    container.innerHTML = html;
}

// Find word data in analysis results
function findWordData(token, analysisResults) {
    const normalized = token.toLowerCase().replace(/[^\w]/g, '');

    // Search in words
    const wordMatch = analysisResults.words?.find(w =>
        w.word.toLowerCase() === normalized
    );
    if (wordMatch) return wordMatch;

    // Search in phrasal verbs
    const phraseMatch = analysisResults.phrasal_verbs?.find(pv =>
        pv.phrase.toLowerCase() === normalized
    );
    if (phraseMatch) return { ...phraseMatch, word: phraseMatch.phrase };

    return null;
}

// Handle word click in reading view
function handleWordClick(word) {
    // Find word data
    const wordData = window.currentAnalysisResults.words?.find(w => w.word === word) ||
                     window.currentAnalysisResults.phrasal_verbs?.find(pv => pv.phrase === word);

    if (wordData) {
        showWordDetails(wordData); // Reuse existing modal function
    }
}

// Save/restore scroll position
function saveReadingPosition() {
    const panel = document.getElementById('reading-panel');
    if (panel) {
        localStorage.setItem('reading-scroll-position', panel.scrollTop);
    }
}

function restoreReadingPosition() {
    const panel = document.getElementById('reading-panel');
    const savedPosition = localStorage.getItem('reading-scroll-position');
    if (panel && savedPosition) {
        panel.scrollTop = parseInt(savedPosition, 10);
    }
}

// Initialize reading view when tab is activated
function initReadingView() {
    const readingTab = document.getElementById('reading-tab');
    if (!readingTab) return;

    readingTab.addEventListener('click', () => {
        if (window.currentAnalysisResults && window.currentAnalysisResults.processed_text) {
            parseTextForReading(
                window.currentAnalysisResults.processed_text,
                window.currentAnalysisResults
            );
            restoreReadingPosition();
        }
    });

    // Save scroll position when switching away
    const allTabs = document.querySelectorAll('.tab-btn');
    allTabs.forEach(tab => {
        if (tab.id !== 'reading-tab') {
            tab.addEventListener('click', saveReadingPosition);
        }
    });
}

// Update reading view when filters change
function updateReadingView() {
    const readingPanel = document.getElementById('reading-panel');
    if (readingPanel && !readingPanel.hidden) {
        parseTextForReading(
            window.currentAnalysisResults.processed_text,
            window.currentAnalysisResults
        );
    }
}
```

**Integration Points**:
1. Call `initReadingView()` after tab navigation initializes (in `updateWordDisplay()`)
2. Call `updateReadingView()` in existing filter and search handlers
3. Store `results.analysis_results` in `window.currentAnalysisResults` for access

---

## Backend Requirements

### API Changes

**NO NEW APIs REQUIRED** - Reading view uses existing data:
- `processedText` already returned by `/api/analyze` endpoint
- `analysis_results` already contains word/phrase data with CEFR levels
- Translation API (Feature 002) already implemented

### Data Model

**Existing Data** (no changes needed):
```python
{
    "processed_text": "Full text with normalized words...",
    "analysis_results": {
        "words": [
            {
                "word": "ambitious",
                "cefr_level": "C1",
                "count": 12,
                "examples": ["sentence 1", "sentence 2", ...]
            },
            ...
        ],
        "phrasal_verbs": [...]
    }
}
```

**Frontend State** (new):
```javascript
window.currentAnalysisResults = {
    processed_text: "...",
    words: [...],
    phrasal_verbs: [...]
};

localStorage.setItem('reading-scroll-position', scrollTop);
```

---

## Non-Functional Requirements

### Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Initial render (300KB text) | <1s | Chrome DevTools Performance tab |
| Scroll performance | 60fps | FPS meter during rapid scroll |
| Filter re-render | <300ms | Performance.now() before/after |
| Modal open latency | <100ms | Click to modal visible |
| Memory overhead | <50MB | Chrome DevTools Memory profiler |

### Accessibility (WCAG 2.1 AA)

- **Keyboard Navigation**: Tab to reading view tab, Enter to activate, Tab through colored words, Enter to open modal, Escape to close
- **Screen Reader**: Reading panel has `role="tabpanel"`, ARIA labels on tab button, colored words have accessible names
- **Color Contrast**: All CEFR colors meet 4.5:1 contrast ratio against white background (validate with axe DevTools)
- **Focus Indicators**: Colored words show `:focus-visible` outline when tabbed to

### Browser Compatibility

- Chrome 90+ (primary)
- Safari 14+ (macOS/iOS)
- Firefox 88+
- Edge 90+

### Responsive Breakpoints

| Breakpoint | Container Width | Font Size | Margins |
|------------|----------------|-----------|---------|
| <768px (mobile) | 100% | 16px | 16px |
| 768-1024px (tablet) | 720px | 18px | 24px |
| 1024-1440px (desktop) | 800px | 18px | 48px |
| 1440px+ (wide) | 800px | 18px | auto (centered) |

---

## Quality Assurance

### Testing Checklist

**Functional Testing**:
- [ ] Tab navigation includes "全文阅读" tab
- [ ] Clicking reading tab displays processed text
- [ ] CEFR-colored words render correctly (A1-C2+)
- [ ] Clicking colored word opens modal with translation
- [ ] Modal reuses existing showWordDetails() function
- [ ] Filter "B2" in vocabulary view highlights only B2 words in reading view
- [ ] Search "make" in vocabulary view highlights matching words in reading view
- [ ] Scroll position persists when switching tabs
- [ ] Non-colored words (filtered out) are not clickable

**Performance Testing**:
- [ ] 300KB text renders in <1 second
- [ ] Scrolling maintains 60fps (FPS meter)
- [ ] Filter re-render completes in <300ms
- [ ] Modal opens in <100ms

**Accessibility Testing**:
- [ ] Keyboard: Tab to reading tab, Enter to activate, Tab through words
- [ ] Screen reader announces "Reading View" tab correctly
- [ ] CEFR colors meet 4.5:1 contrast ratio (axe DevTools)
- [ ] Focus indicators visible on colored words

**Cross-Browser Testing**:
- [ ] Chrome: All features work
- [ ] Safari: All features work
- [ ] Firefox: All features work
- [ ] Mobile Safari (iOS): Touch targets 44x44px, scrolling smooth

**Edge Cases**:
- [ ] Empty processed_text: Shows "No text available" message
- [ ] Very short text (100 words): Renders correctly, no layout issues
- [ ] Very long text (500KB): Performance acceptable or shows warning
- [ ] Text with special characters (unicode): Renders correctly
- [ ] No internet (cached translations): Modal shows cached data correctly

---

## Success Metrics

### User Adoption
- **Target**: 40% of users who complete analysis switch to reading view at least once
- **Measurement**: Track tab click events (Google Analytics or internal telemetry)

### Engagement
- **Target**: Average reading session duration >5 minutes
- **Measurement**: Track time spent in reading view (session storage)

### Feature Utility
- **Target**: 30% of word lookups happen in reading view (vs vocabulary list)
- **Measurement**: Track `showWordDetails()` source (reading view vs vocabulary list)

### Performance
- **Target**: 95% of users experience <1s render time for their texts
- **Measurement**: RUM (Real User Monitoring) with Performance API

---

## Open Questions & Decisions

### Resolved Decisions

1. **Q: Should we add chapter/section navigation?**
   - **A**: NO - Keep MVP simple. Reading view is for immersive reading, not structural navigation. Users can use browser Find (Ctrl+F) for now.

2. **Q: Should we implement virtual scrolling for very large texts?**
   - **A**: NO for MVP - Modern browsers handle 300KB text efficiently. Add only if performance testing reveals issues.

3. **Q: Should we allow font size customization?**
   - **A**: NO for MVP - Use responsive defaults (16px mobile, 18px desktop). Can add in future iteration if users request it.

4. **Q: Should uncolored words (filtered out) be grayed out or black?**
   - **A**: BLACK - Maintain normal reading flow. Graying out would be distracting and reduce readability.

5. **Q: How to handle phrasal verbs in reading view?**
   - **A**: Color only individual words - for multi-word phrasal verbs like "make up", only the first word ("make") is colored. When clicked, `findWordData()` detects the full phrasal verb and displays the complete definition in the modal.
   - **Rationale**: Simplest implementation, avoids multi-word span detection complexity, allows for future enhancement based on user feedback.

6. **Q: Should we show a CEFR legend in reading view?**
   - **A**: NO - Reading view shows only word underline colors (dotted border-bottom) to indicate CEFR levels. No legend, labels, or explanations displayed. Maintains clean, immersive reading experience.
   - **Rationale**: Users learn colors from vocabulary view tabs. Adding legend would clutter interface and distract from reading flow. Can add in future if user testing reveals confusion.

7. **Q: What to do if processed_text is missing or empty?**
   - **A**: Always show the "全文阅读 / Reading View" tab. Display bilingual empty state message "暂无文本 / No text available" in the reading panel when text is missing or empty.
   - **Rationale**: More transparent UX - users understand why reading view is empty. Hiding tab would be confusing. Allows for error recovery if analysis needs to be retried. Consistent with existing patterns (other tabs show empty states).

### Open Questions (To Be Resolved During Implementation)

**None** - All critical ambiguities have been resolved during clarification session 2025-11-05.

---

## Implementation Phases

### Phase 1: Core Reading View (MVP)
**Goal**: Get basic reading view working with colored, clickable words
**Estimated Time**: 4-6 hours

- [T001] Add "全文阅读" tab button to HTML
- [T002] Add `#reading-panel` container to HTML
- [T003] Create CSS for `.reading-container` and `.reading-content`
- [T004] Add CSS for `.cefr-word` coloring and hover states
- [T005] Implement `parseTextForReading()` function
- [T006] Implement `findWordData()` helper
- [T007] Implement `handleWordClick()` with modal integration
- [T008] Call `initReadingView()` in initialization flow
- [T009] Test with sample text (100 words)

### Phase 2: Filter & Search Integration
**Goal**: Make reading view respect vocabulary filters and search
**Estimated Time**: 2-3 hours

- [T010] Update `parseTextForReading()` to respect active CEFR filter
- [T011] Update `parseTextForReading()` to highlight search matches
- [T012] Add `updateReadingView()` to filter button handlers
- [T013] Add `updateReadingView()` to search input handler
- [T014] Test filter changes reflect in reading view
- [T015] Test search highlighting works correctly

### Phase 3: State Persistence & Polish
**Goal**: Save scroll position, smooth transitions, edge cases
**Estimated Time**: 2-3 hours

- [T016] Implement `saveReadingPosition()` on tab switch
- [T017] Implement `restoreReadingPosition()` on tab activate
- [T018] Add smooth fade transition when switching to reading view
- [T019] Handle empty `processed_text` - display "暂无文本 / No text available" message, keep tab visible
- [T020] Add responsive typography (16px → 18px)
- [T021] Test scroll position persistence across tab switches

### Phase 4: Performance Optimization
**Goal**: Ensure smooth performance with large texts
**Estimated Time**: 3-4 hours

- [T022] Profile rendering with 300KB text (Chrome DevTools)
- [T023] Optimize `parseTextForReading()` if needed (batch DOM updates)
- [T024] Add `requestIdleCallback` for non-critical rendering if needed
- [T025] Test scroll performance (60fps validation)
- [T026] Add loading skeleton if render takes >500ms
- [T027] Validate Lighthouse Performance score >90

### Phase 5: Accessibility & Validation
**Goal**: WCAG 2.1 AA compliance, cross-browser testing
**Estimated Time**: 2-3 hours

- [T028] Add keyboard navigation to colored words (Tab/Enter)
- [T029] Validate ARIA attributes on reading panel
- [T030] Run axe DevTools scan, fix violations
- [T031] Test color contrast for all CEFR colors
- [T032] Test on Safari, Firefox, Edge
- [T033] Test on mobile (iOS Safari, Chrome Android)
- [T034] Final regression testing (all 4 user stories)
- [T035] Update documentation and close feature

**Total Estimated Time**: 13-19 hours

---

## Dependencies

### Existing Features (Reuse)
- **Feature 002**: Translation API and caching (for modal translations)
- **Feature 003**: Design tokens (CEFR colors, spacing, typography)
- **Feature 004**: Tab navigation system, `showWordDetails()` modal, keyboard navigation

### External Libraries
- None required - Pure HTML/CSS/JavaScript implementation

### Data Requirements
- `processed_text` from backend analysis (already exists)
- `analysis_results.words` and `analysis_results.phrasal_verbs` (already exists)

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Performance issues with 500KB+ texts | Medium | High | Profile early, add virtual scrolling if needed, show warning for very large files |
| Phrasal verb detection complexity | Low | Low | RESOLVED: Color first word only, `findWordData()` detects full phrase on click |
| User confusion about colored vs plain text | Low | Medium | Add optional legend in future iteration if user testing reveals confusion |
| Scroll jank on low-end devices | Medium | Medium | Test on mid-range Android device, optimize DOM structure if needed |
| Translation API timeout in modal | Low | Low | Already handled by Feature 002 error states |

---

## Rollout Plan

### Development
1. Create branch `005-reading-view`
2. Implement phases 1-5 sequentially
3. Self-test each phase before proceeding
4. Document IMPLEMENTATION_STATUS.md after each phase

### Testing
1. Manual testing on Chrome (primary)
2. Cross-browser testing (Safari, Firefox, Edge)
3. Mobile testing (iOS Safari, Chrome Android)
4. Performance profiling with 100KB, 300KB, 500KB test files
5. Accessibility audit with axe DevTools

### Deployment
1. Merge to main after all tests pass
2. Deploy to production (existing Flask deployment process)
3. Monitor error logs for JavaScript errors
4. Collect user feedback via GitHub issues or feedback form

### Monitoring
1. Track reading view tab click rate
2. Monitor average session duration in reading view
3. Monitor performance metrics (render time, scroll FPS)
4. Collect qualitative feedback from early users

---

## Future Enhancements (Out of Scope for MVP)

1. **Chapter Navigation**: Auto-detect chapters, add quick navigation sidebar
2. **Font Customization**: Allow users to change font size, family, line height
3. **Reading Progress**: Track reading position across sessions, show progress bar
4. **Bookmarks**: Let users save positions in text with notes
5. **Export Highlighted Words**: Export all colored words as vocabulary list
6. **Audio Narration**: Text-to-speech integration for listening practice
7. **Split View**: Show vocabulary list sidebar alongside reading view
8. **Dark Mode**: Add dark theme for reading view (reduce eye strain)
9. **CEFR Legend**: Optional always-visible legend showing color meanings
10. **Phrasal Verb Multi-Word Highlighting**: Color entire phrasal verb span

---

## Appendix

### CEFR Color Palette (Existing Tokens)
```css
--cefr-a1: #22c55e;       /* Green - Beginner */
--cefr-a2: #3b82f6;       /* Blue - Elementary */
--cefr-b1: #f59e0b;       /* Orange - Intermediate */
--cefr-b2: #ef4444;       /* Red - Upper Intermediate */
--cefr-c1: #a855f7;       /* Purple - Advanced */
--cefr-c2: #ec4899;       /* Pink - Proficient */
--cefr-c2-plus: #991b1b;  /* Dark Red - Beyond C2 */
```

### Typography Reference
```css
--font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
               "Helvetica Neue", Arial, sans-serif;
--text-primary: #2c3e50;
--space-4: 16px;
--space-6: 24px;
--space-8: 32px;
```

### Example HTML Output
```html
<div class="reading-content">
    <p>
        The <span class="cefr-word" data-word="ambitious" data-level="C1"
                  onclick="handleWordClick('ambitious')">ambitious</span>
        young <span class="cefr-word" data-word="entrepreneur" data-level="C1"
                    onclick="handleWordClick('entrepreneur')">entrepreneur</span>
        started a new company.
    </p>
    <p>
        She wanted to <span class="cefr-word search-match" data-word="make"
                            data-level="A1" onclick="handleWordClick('make')">make</span>
        a difference in the world.
    </p>
</div>
```

---

**Document Version**: 1.0
**Last Updated**: 2025-11-05
**Author**: System (based on user requirements)
**Status**: Ready for Implementation
