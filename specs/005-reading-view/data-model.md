# Phase 1: Data Model & Structures
## Feature 005 - Immersive Full-Text Reading View

**Date**: 2025-11-05  
**Status**: Complete

---

## Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER UPLOADS BOOK FILE                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              BACKEND /api/analyze ENDPOINT                       │
│              (Existing - NO CHANGES)                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼ Returns JSON response
┌─────────────────────────────────────────────────────────────────┐
│                 ANALYSIS RESULTS OBJECT                          │
│  {                                                              │
│    processed_text: "Full book text...",                        │
│    analysis_results: {                                          │
│      words: [...],                                              │
│      phrasal_verbs: [...],                                      │
│      statistics: {...}                                          │
│    }                                                            │
│  }                                                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼ Stored in global variable
┌─────────────────────────────────────────────────────────────────┐
│            window.currentAnalysisResults (app.js)                │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼ User clicks "Reading View" tab
┌─────────────────────────────────────────────────────────────────┐
│         parseTextForReading(processedText, results)              │
│         - Splits text into paragraphs                           │
│         - Tokenizes words (preserves whitespace)                │
│         - Matches tokens to vocabulary data                     │
│         - Applies filters (CEFR level, search term)             │
│         - Builds HTML with <span> wrappers                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼ HTML string
┌─────────────────────────────────────────────────────────────────┐
│           document.getElementById('reading-content')             │
│           .innerHTML = generatedHTML                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼ Rendered in browser
┌─────────────────────────────────────────────────────────────────┐
│              READING VIEW (User sees colored text)               │
│  User clicks word → handleWordClick(word) → showWordDetails()   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core Data Structures

### 1. Analysis Results Object (Existing - NO CHANGES)

**Source**: Backend `/api/analyze` endpoint response  
**Storage**: `window.currentAnalysisResults` (global variable in `app.js`)

```javascript
{
  // Raw processed text with normalized words
  "processed_text": "The ambitious entrepreneur started a company. She wanted to make a difference.",
  
  // Analysis results
  "analysis_results": {
    // Regular vocabulary words
    "words": [
      {
        "word": "ambitious",           // Lemmatized base form
        "cefr_level": "C1",           // CEFR level (A1-C2+)
        "count": 12,                  // Frequency in text
        "examples": [                 // Example sentences from book
          "The ambitious entrepreneur started a company.",
          "Her ambitious goals drove her forward."
        ],
        "word_type": "adjective"      // Part of speech (optional)
      },
      {
        "word": "entrepreneur",
        "cefr_level": "C1",
        "count": 8,
        "examples": ["..."]
      }
      // ... more words
    ],
    
    // Phrasal verbs
    "phrasal_verbs": [
      {
        "phrase": "make up",           // Full phrasal verb
        "cefr_level": "B1",
        "count": 5,
        "examples": ["They make up 20% of the population."],
        "type": "separable"            // separable/inseparable
      }
      // ... more phrasal verbs
    ],
    
    // Statistics (displayed in summary section)
    "statistics": {
      "total_words": 15234,
      "unique_words": 3421,
      "level_distribution": {
        "A1": 450,
        "A2": 320,
        "B1": 580,
        "B2": 720,
        "C1": 890,
        "C2": 261,
        "C2+": 200
      }
    }
  }
}
```

**Access Pattern**:
```javascript
// Global reference (set after analysis completes)
window.currentAnalysisResults = response.analysis_results;

// Usage in reading view
const processedText = window.currentAnalysisResults.processed_text;
const words = window.currentAnalysisResults.words;
const phrasal_verbs = window.currentAnalysisResults.phrasal_verbs;
```

---

### 2. Filter State (Existing - Shared with Vocabulary View)

**Storage**: DOM state (active button) + function parameter  
**Scope**: Global (affects both vocabulary list and reading view)

```javascript
// Current active CEFR level filter
// Read from DOM: document.querySelector('.filter-btn.active')?.getAttribute('data-level')
// Values: 'all', 'A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'C2+'

// Current search term
// Read from DOM: document.getElementById('word-search')?.value.toLowerCase()
// Example: "make" (highlights all words containing "make")
```

**Access Pattern**:
```javascript
function parseTextForReading(processedText, analysisResults) {
    // Read current filter state
    const activeLevel = document.querySelector('.filter-btn.active')?.getAttribute('data-level') || 'all';
    const searchTerm = document.getElementById('word-search')?.value.toLowerCase() || '';
    
    // Apply filters when building HTML...
}
```

---

### 3. Word Lookup Map (NEW - Performance Optimization)

**Purpose**: O(1) word lookups instead of O(n) array scans  
**Lifecycle**: Built once per analysis, reused for all renders

```javascript
// Pre-indexed lookup map (built in parseTextForReading)
const wordLookupMap = new Map();

// Index regular words
analysisResults.words?.forEach(word => {
    wordLookupMap.set(word.word.toLowerCase(), {
        ...word,
        type: 'word'  // Distinguish from phrasal verbs
    });
});

// Index phrasal verbs
analysisResults.phrasal_verbs?.forEach(pv => {
    wordLookupMap.set(pv.phrase.toLowerCase(), {
        ...pv,
        word: pv.phrase,  // Normalize: phrasal verbs use "phrase" key
        type: 'phrasal_verb'
    });
});

// Fast O(1) lookup
const wordData = wordLookupMap.get(token.toLowerCase());
```

---

### 4. Scroll Position State (NEW - Persistence)

**Storage**: `localStorage` (persists across page reloads)  
**Lifecycle**: Saved on tab switch away, restored on tab switch back

```javascript
// LocalStorage keys
const SCROLL_POSITION_KEY = 'reading-scroll-position';

// Save (called when switching away from reading view)
function saveReadingPosition() {
    const panel = document.getElementById('reading-panel');
    if (panel) {
        localStorage.setItem(SCROLL_POSITION_KEY, panel.scrollTop.toString());
    }
}

// Restore (called when switching to reading view)
function restoreReadingPosition() {
    const panel = document.getElementById('reading-panel');
    const savedPosition = localStorage.getItem(SCROLL_POSITION_KEY);
    if (panel && savedPosition) {
        panel.scrollTop = parseInt(savedPosition, 10);
    }
}

// Clear (called on "Analyze Another Book")
function clearReadingState() {
    localStorage.removeItem(SCROLL_POSITION_KEY);
}
```

---

## HTML Structure (NEW)

### Reading View Tab Button

**Location**: `index.html` lines ~137-150 (after phrasal verbs tab)

```html
<!-- Add as third tab -->
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

### Reading View Panel

**Location**: `index.html` lines ~161-173 (after phrases-panel)

```html
<!-- Add as third tab panel -->
<div id="reading-panel"
     class="tab-panel"
     role="tabpanel"
     aria-labelledby="reading-tab"
     tabindex="0"
     hidden>
    <div class="reading-container">
        <div class="reading-content" id="reading-content">
            <!-- JavaScript will populate this with:
                 <p>
                     Word <span class="cefr-word" data-word="..." data-level="...">word</span> text.
                 </p>
            -->
        </div>
    </div>
</div>
```

### Generated HTML Output (JavaScript)

**Structure**: Paragraphs → Spans for colored words

```html
<!-- Example output for "The ambitious entrepreneur started a company." -->
<p>
    The 
    <span class="cefr-word" 
          data-word="ambitious" 
          data-level="C1"
          onclick="handleWordClick('ambitious')">ambitious</span> 
    <span class="cefr-word" 
          data-word="entrepreneur" 
          data-level="C1"
          onclick="handleWordClick('entrepreneur')">entrepreneur</span> 
    started a company.
</p>

<!-- With search highlighting (search term: "make") -->
<p>
    She wanted to 
    <span class="cefr-word search-match" 
          data-word="make" 
          data-level="A1"
          onclick="handleWordClick('make')">make</span> 
    a difference.
</p>
```

**Data Attributes**:
- `data-word`: Lemmatized word (for lookup in analysis results)
- `data-level`: CEFR level (A1-C2+) → used for CSS color targeting
- `onclick`: Inline event handler (simplest approach, no delegation needed)

---

## CSS Data Model (NEW)

### CEFR Color Classes

**Location**: `styles.css` (new section ~line 2100+)

```css
/* Apply CEFR colors via data attribute selector */
.cefr-word[data-level="A1"] { color: var(--cefr-a1); }  /* #22c55e - Green */
.cefr-word[data-level="A2"] { color: var(--cefr-a2); }  /* #3b82f6 - Blue */
.cefr-word[data-level="B1"] { color: var(--cefr-b1); }  /* #f59e0b - Orange */
.cefr-word[data-level="B2"] { color: var(--cefr-b2); }  /* #ef4444 - Red */
.cefr-word[data-level="C1"] { color: var(--cefr-c1); }  /* #a855f7 - Purple */
.cefr-word[data-level="C2"] { color: var(--cefr-c2); }  /* #ec4899 - Pink */
.cefr-word[data-level="C2+"] { color: var(--cefr-c2-plus); } /* #991b1b - Dark Red */

/* Search match highlighting */
.cefr-word.search-match {
    background-color: rgba(255, 235, 59, 0.4);  /* Yellow highlight */
}
```

---

## State Transitions

### Tab Activation Flow

```
User clicks "全文阅读" tab
    ↓
Tab navigation handler (existing Feature 004)
    ↓
Check: Is reading-content empty?
    ├── YES → parseTextForReading() [first render]
    └── NO  → Skip render (already populated)
    ↓
restoreReadingPosition() [restore scroll]
    ↓
Reading view visible, user can interact
```

### Filter Change Flow

```
User clicks "B2" filter button
    ↓
Filter button handler (existing)
    ↓
Check: Is reading view active?
    ├── YES → updateReadingView() [re-render with new filter]
    └── NO  → Skip (will apply filter on next tab switch)
    ↓
Reading view shows only B2 words colored
```

### Search Input Flow

```
User types "make" in search box
    ↓
Search input handler (existing)
    ↓
Check: Is reading view active?
    ├── YES → updateReadingView() [re-render with search highlight]
    └── NO  → Skip (will apply search on next tab switch)
    ↓
Reading view highlights "make", "makes", "making" with yellow background
```

---

## Empty State Handling

### Scenario: Missing or Empty processed_text

**Detection**:
```javascript
if (!processedText || processedText.trim().length === 0) {
    // Show empty state message
}
```

**HTML Output**:
```html
<div class="reading-content">
    <p class="empty-state bilingual">
        <span class="cn">暂无文本</span>
        <span class="en">No text available</span>
    </p>
</div>
```

**CSS Styling**:
```css
.empty-state {
    text-align: center;
    color: var(--text-secondary);
    padding: var(--space-12);
    font-size: var(--font-size-lg);
}
```

---

## Data Validation

### Input Validation (parseTextForReading)

```javascript
function parseTextForReading(processedText, analysisResults) {
    // Validate inputs
    if (!processedText || typeof processedText !== 'string') {
        console.error('Invalid processedText:', processedText);
        return renderEmptyState();
    }
    
    if (!analysisResults || !analysisResults.words) {
        console.error('Invalid analysisResults:', analysisResults);
        return renderEmptyState();
    }
    
    // Proceed with parsing...
}
```

### Word Lookup Validation

```javascript
function findWordData(token, lookupMap) {
    // Normalize token (remove punctuation, lowercase)
    const normalized = token.toLowerCase().replace(/[^\w]/g, '');
    
    if (!normalized) {
        return null;  // Whitespace or punctuation only
    }
    
    // Lookup in map
    const wordData = lookupMap.get(normalized);
    return wordData || null;  // Return null if not found
}
```

---

## Performance Considerations

### Memory Footprint Estimate

| Data Structure | Size (300KB text) | Notes |
|---------------|------------------|-------|
| `processedText` (string) | ~300KB | Already in memory (from API response) |
| `wordLookupMap` (Map) | ~50KB | 3,000 words × ~16 bytes per entry |
| Generated HTML (string) | ~600KB | 2x original text (due to `<span>` wrappers) |
| DOM nodes | ~50MB | Browser-managed (50,000 nodes × 1KB avg) |
| **Total Additional Memory** | **~50MB** | Acceptable (modern browsers handle 100MB+ easily) |

### Rendering Performance Budget

| Operation | Target Time | Measurement Method |
|-----------|------------|-------------------|
| Parse text into tokens | <200ms | `console.time('parsing')` |
| Build HTML string | <300ms | `console.time('html-generation')` |
| Insert into DOM (`innerHTML`) | <500ms | `console.time('dom-insertion')` |
| **Total Render Time** | **<1s** | Chrome DevTools Performance tab |

---

## Phase 1 Checklist

- [x] Data flow architecture documented
- [x] Core data structures defined (existing + new)
- [x] HTML structure specified (tab button + panel)
- [x] Generated HTML format documented
- [x] CSS data model (color classes) specified
- [x] State transitions mapped
- [x] Empty state handling defined
- [x] Data validation approach documented
- [x] Memory/performance estimates calculated

**Status**: ✅ Ready for Phase 1 Contracts
