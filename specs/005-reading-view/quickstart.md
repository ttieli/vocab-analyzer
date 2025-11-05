# Quickstart Guide: Feature 005 - Immersive Reading View

**Last Updated**: 2025-11-05  
**Branch**: `005-reading-view`

---

## Prerequisites

### Required Setup (Already Completed)

- ✅ Python 3.10+ environment with Flask 3.0+
- ✅ Existing vocab_analyzer web application running
- ✅ Feature 002 (Translation API) implemented
- ✅ Feature 003 (Design Tokens) implemented
- ✅ Feature 004 (Tab Navigation + Modal) implemented

### Browser Requirements

- Modern browser with JavaScript enabled
- Chrome 90+, Safari 14+, Firefox 88+, or Edge 90+ recommended

---

## Development Setup

### 1. Create Feature Branch

```bash
cd "/Users/tieli/Library/Mobile Documents/com~apple~CloudDocs/铁力个人资料/20251103 English Vocabulary"
git checkout -b 005-reading-view
```

### 2. Verify Existing Implementation

```bash
# Start development server
cd src
python -m vocab_analyzer.web.app

# Open browser to http://127.0.0.1:5000
# Verify existing features work:
# - Upload a sample text file
# - Check "Words" and "Phrasal Verbs" tabs display correctly
# - Click a word → modal opens with translation
```

### 3. Prepare Test Files

**Create test corpus** in `tests/fixtures/reading-view/`:

```bash
mkdir -p tests/fixtures/reading-view
```

**Small test file** (`small.txt` - ~100 words):
```text
The ambitious entrepreneur started a company. She wanted to make a difference in the world. Her innovative ideas attracted investors.

The business grew rapidly. They hired talented people. The team worked hard every day.
```

**Medium test file** (`medium.txt` - ~5,000 words):
- Copy a short story or article (5-10 pages)
- Example: A chapter from "Pride and Prejudice" or similar public domain text

**Large test file** (`large.txt` - ~50,000 words):
- Copy a full book or long document
- Example: "Pride and Prejudice" full text (300KB)

---

## Implementation Workflow

### Phase 1: Core Reading View (4-6 hours)

**Goal**: Get basic reading view working with colored, clickable words

#### Step 1.1: Add HTML Structure (30 min)

**File**: `src/vocab_analyzer/web/static/index.html`

**Location**: After line 136 (after phrasal verbs tab button)

```html
<!-- Add third tab button -->
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
```

**Location**: After line 161 (after phrases-panel)

```html
<!-- Add reading panel -->
<div id="reading-panel"
     class="tab-panel"
     role="tabpanel"
     aria-labelledby="reading-tab"
     tabindex="0"
     hidden>
    <div class="reading-container">
        <div class="reading-content" id="reading-content">
            <!-- Populated by JavaScript -->
        </div>
    </div>
</div>
```

**Test**: Refresh page, verify third tab appears (no functionality yet)

#### Step 1.2: Add CSS Styles (45 min)

**File**: `src/vocab_analyzer/web/static/styles.css`

**Location**: End of file (~line 2100+)

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

/* Empty state */
.empty-state {
    text-align: center;
    color: var(--text-secondary);
    padding: var(--space-12);
    font-size: var(--font-size-lg);
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
        max-width: 75ch;
    }
}
```

**Test**: Refresh page, styles applied (though no content yet)

#### Step 1.3: Implement Core JavaScript Functions (2-3 hours)

**File**: `src/vocab_analyzer/web/static/app.js`

**Location**: End of file (after existing functions)

**Add these functions** (see contracts for full implementations):
1. `parseTextForReading(processedText, analysisResults)`
2. `findWordData(token, wordLookupMap)`
3. `handleWordClick(word)`
4. `initReadingView()`
5. `updateReadingView()`
6. `saveReadingPosition()`
7. `restoreReadingPosition()`
8. `clearReadingState()`

**Integration points**:
```javascript
// Add to existing DOMContentLoaded handler
document.addEventListener('DOMContentLoaded', () => {
    // ... existing code ...
    
    // Initialize reading view
    initReadingView();
});

// Add to existing filter button handler
levelFilters.addEventListener('click', (e) => {
    // ... existing filter logic ...
    
    // Update reading view if active
    updateReadingView();
});

// Add to existing search input handler
wordSearch.addEventListener('input', () => {
    // ... existing search logic ...
    
    // Update reading view if active
    updateReadingView();
});

// Add to existing "Analyze Another Book" handler
analyzeAnotherBtn.addEventListener('click', () => {
    // ... existing reset logic ...
    
    // Clear reading state
    clearReadingState();
});
```

**Test**: 
1. Upload `tests/fixtures/reading-view/small.txt`
2. Click "全文阅读" tab
3. Verify colored words appear
4. Click a colored word → modal opens
5. Close modal → reading position preserved

---

### Phase 2: Filter & Search Integration (2-3 hours)

**Goal**: Make reading view respect vocabulary filters and search

**Changes**: Already included in `parseTextForReading()` implementation

**Test**:
1. Upload test file
2. Switch to reading view
3. Click "B2" filter → only B2 words colored
4. Type "make" in search box → matching words highlighted yellow
5. Clear search → highlights removed
6. Click "All Levels" → all words colored again

---

### Phase 3: State Persistence & Polish (2-3 hours)

**Goal**: Save scroll position, smooth transitions, edge cases

**Changes**: Already included in scroll persistence functions

**Test**:
1. Upload test file, switch to reading view
2. Scroll to 50% of text
3. Switch to "Words" tab
4. Switch back to "全文阅读" tab → scroll position restored
5. Click "Analyze Another Book" → state cleared
6. Upload empty file → "No text available" message shown

---

## Testing Checklist

### Functional Testing

Upload `small.txt` and verify:
- [ ] Reading view tab appears
- [ ] Clicking tab shows processed text
- [ ] CEFR-colored words render correctly (A1-C2+)
- [ ] Clicking colored word opens modal with translation
- [ ] Modal displays word, CEFR badge, examples, translation
- [ ] Filter "B2" → only B2 words colored
- [ ] Search "make" → matching words highlighted
- [ ] Scroll position persists across tab switches
- [ ] Non-colored words are not clickable

### Performance Testing

Upload `large.txt` (300KB) and verify:
- [ ] Render completes in <1 second
- [ ] Scrolling is smooth (60fps, no jank)
- [ ] Filter re-render completes in <300ms
- [ ] Modal opens in <100ms

### Accessibility Testing

- [ ] Tab key navigates to reading view tab
- [ ] Enter key activates reading view
- [ ] Tab key navigates through colored words
- [ ] Enter key on colored word opens modal
- [ ] Escape key closes modal
- [ ] Screen reader announces "Reading View" tab

### Cross-Browser Testing

Test on:
- [ ] Chrome (primary)
- [ ] Safari (macOS/iOS)
- [ ] Firefox
- [ ] Edge (optional)

### Edge Cases

- [ ] Empty processed_text → shows "No text available"
- [ ] Very short text (50 words) → renders correctly
- [ ] Very long text (500KB) → performance acceptable (may take >1s)
- [ ] Text with unicode characters → renders correctly
- [ ] No internet (cached translations) → modal shows cached data

---

## Debugging Tips

### Issue: Reading view is blank

**Check**:
1. Open browser DevTools Console
2. Look for errors in `parseTextForReading()`
3. Verify `window.currentAnalysisResults` exists:
   ```javascript
   console.log(window.currentAnalysisResults.processed_text);
   ```

### Issue: Words not colored

**Check**:
1. Verify CSS loaded (inspect element, check computed styles)
2. Check CEFR color tokens defined in `:root` (styles.css)
3. Verify `data-level` attribute on spans:
   ```javascript
   document.querySelectorAll('.cefr-word').forEach(span => {
       console.log(span.dataset.level);
   });
   ```

### Issue: Modal doesn't open

**Check**:
1. Verify `showWordDetails()` function exists (Feature 004)
2. Check browser console for errors
3. Test directly:
   ```javascript
   handleWordClick('ambitious');
   ```

### Issue: Scroll position not saved

**Check**:
1. Open browser DevTools → Application → Local Storage
2. Verify `reading-scroll-position` key exists
3. Check value is numeric string (e.g., `"1250"`)

---

## Performance Profiling

### Measure Render Time

```javascript
// Add to parseTextForReading()
console.time('parseTextForReading');
// ... existing code ...
console.timeEnd('parseTextForReading');
```

### Chrome DevTools Performance Tab

1. Open DevTools → Performance tab
2. Click Record
3. Switch to reading view
4. Stop recording
5. Analyze flame graph:
   - Scripting (JS execution) should be <500ms
   - Rendering (layout/paint) should be <500ms
   - Total <1s for 300KB text

### Lighthouse Audit

1. Open DevTools → Lighthouse tab
2. Select "Performance" category
3. Generate report
4. Target score: >90

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| **Tab doesn't appear** | Check HTML syntax, verify tab button ID is `reading-tab` |
| **No colors on words** | Check CSS loaded, CEFR tokens defined, data-level attributes present |
| **Modal doesn't open** | Verify Feature 004 implemented, `showWordDetails()` function exists |
| **Scroll jank** | Profile with Chrome DevTools, check DOM depth, consider virtual scrolling |
| **Filter doesn't work** | Verify `updateReadingView()` called in filter handler |
| **Search doesn't highlight** | Check `search-match` class added in `parseTextForReading()` |

---

## Next Steps

After completing implementation:
1. Run full testing checklist
2. Fix any bugs found
3. Profile performance with large files
4. Document any deviations from spec
5. Prepare for code review/merge

---

**Status**: ✅ Quickstart Guide Complete - Ready for Implementation
