# Contract: parseTextForReading()

**Purpose**: Parse processed text into reading view HTML with CEFR-colored, clickable word spans

**Location**: `src/vocab_analyzer/web/static/app.js` (new function)

---

## Function Signature

```javascript
/**
 * Parse processed text into reading view HTML with CEFR-colored, clickable words
 * 
 * @param {string} processedText - Full book text from analysis results
 * @param {Object} analysisResults - Analysis results containing words and phrasal verbs
 * @param {Array<Object>} analysisResults.words - Array of word objects with CEFR levels
 * @param {Array<Object>} analysisResults.phrasal_verbs - Array of phrasal verb objects
 * @returns {void} - Directly updates DOM (document.getElementById('reading-content').innerHTML)
 */
function parseTextForReading(processedText, analysisResults) {
    // Implementation...
}
```

---

## Input Specification

### Parameter 1: `processedText` (string)

**Source**: `window.currentAnalysisResults.processed_text`

**Format**: Plain text with normalized words, paragraphs separated by `\n\n`

**Example**:
```text
The ambitious entrepreneur started a company.\n\nShe wanted to make a difference in the world.
```

**Validation**:
- MUST be non-null, non-empty string
- If empty/null, render empty state message

### Parameter 2: `analysisResults` (Object)

**Source**: `window.currentAnalysisResults`

**Structure**:
```javascript
{
    words: [
        {
            word: "ambitious",
            cefr_level: "C1",
            count: 12,
            examples: ["..."]
        },
        // ... more words
    ],
    phrasal_verbs: [
        {
            phrase: "make up",
            cefr_level: "B1",
            count: 5,
            examples: ["..."]
        },
        // ... more phrasal verbs
    ]
}
```

**Validation**:
- MUST have `.words` array (can be empty)
- `.phrasal_verbs` array optional (defaults to empty)

---

## Output Specification

### Return Value: `void`

Function does NOT return a value. It directly updates the DOM:

```javascript
document.getElementById('reading-content').innerHTML = generatedHTML;
```

### Generated HTML Structure

**Paragraph-level**:
```html
<p>Sentence text with colored words.</p>
<p>Another paragraph.</p>
```

**Word-level** (for vocabulary words):
```html
<span class="cefr-word" 
      data-word="ambitious" 
      data-level="C1"
      onclick="handleWordClick('ambitious')">ambitious</span>
```

**Search match highlighting**:
```html
<span class="cefr-word search-match" 
      data-word="make" 
      data-level="A1"
      onclick="handleWordClick('make')">make</span>
```

---

## Processing Algorithm

### Step 1: Input Validation

```javascript
// Validate processedText
if (!processedText || processedText.trim().length === 0) {
    renderEmptyState();
    return;
}

// Validate analysisResults
if (!analysisResults || !analysisResults.words) {
    console.error('Invalid analysisResults');
    renderEmptyState();
    return;
}
```

### Step 2: Build Word Lookup Map (O(1) access)

```javascript
const wordLookupMap = new Map();

// Index words
analysisResults.words?.forEach(word => {
    wordLookupMap.set(word.word.toLowerCase(), {
        ...word,
        type: 'word'
    });
});

// Index phrasal verbs
analysisResults.phrasal_verbs?.forEach(pv => {
    wordLookupMap.set(pv.phrase.toLowerCase(), {
        ...pv,
        word: pv.phrase,
        type: 'phrasal_verb'
    });
});
```

### Step 3: Get Current Filter State

```javascript
const activeLevel = document.querySelector('.filter-btn.active')?.getAttribute('data-level') || 'all';
const searchTerm = document.getElementById('word-search')?.value.toLowerCase() || '';
```

### Step 4: Split Text into Paragraphs

```javascript
const paragraphs = processedText.split('\n\n').filter(p => p.trim().length > 0);
```

### Step 5: Process Each Paragraph

```javascript
let html = '';

paragraphs.forEach(para => {
    html += '<p>';
    
    // Tokenize paragraph (preserve whitespace)
    const tokens = para.split(/(\s+)/);  // Captures whitespace in groups
    
    tokens.forEach(token => {
        if (!token.trim()) {
            // Whitespace - preserve as-is
            html += token;
            return;
        }
        
        // Normalize token for lookup
        const normalized = token.toLowerCase().replace(/[^\w]/g, '');
        const wordData = wordLookupMap.get(normalized);
        
        if (wordData) {
            // Apply CEFR level filter
            if (activeLevel !== 'all' && wordData.cefr_level !== activeLevel) {
                html += token;  // Show as plain text
                return;
            }
            
            // Check search match
            const matchesSearch = !searchTerm || normalized.includes(searchTerm);
            const searchClass = matchesSearch ? ' search-match' : '';
            
            // Generate colored span
            html += `<span class="cefr-word${searchClass}" 
                          data-word="${escapeHtml(wordData.word)}" 
                          data-level="${wordData.cefr_level}"
                          onclick="handleWordClick('${escapeHtml(wordData.word)}')">${escapeHtml(token)}</span>`;
        } else {
            // Regular text
            html += escapeHtml(token);
        }
    });
    
    html += '</p>';
});
```

### Step 6: Update DOM

```javascript
const container = document.getElementById('reading-content');
if (container) {
    container.innerHTML = html;
}
```

---

## Helper Functions Required

### `escapeHtml(text)`

```javascript
/**
 * Escape HTML entities to prevent XSS
 * @param {string} text - Text to escape
 * @returns {string} - HTML-safe text
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
```

### `renderEmptyState()`

```javascript
/**
 * Render empty state message when no text available
 * @returns {void} - Updates DOM
 */
function renderEmptyState() {
    const container = document.getElementById('reading-content');
    if (container) {
        container.innerHTML = `
            <p class="empty-state bilingual">
                <span class="cn">暂无文本</span>
                <span class="en">No text available</span>
            </p>
        `;
    }
}
```

---

## Performance Requirements

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Tokenization** | <200ms for 300KB text | `console.time('tokenize')` |
| **HTML Generation** | <300ms | `console.time('html-build')` |
| **DOM Update** | <500ms | `console.time('dom-update')` |
| **Total Function Time** | <1s | Chrome DevTools Performance tab |

---

## Edge Cases

| Scenario | Expected Behavior |
|----------|------------------|
| **Empty `processedText`** | Render empty state message |
| **No matching words** | Show all text as plain (no colored words) |
| **Very short text (<100 words)** | Render normally, no special handling |
| **Very long text (>500KB)** | May take >1s (acceptable, profiling in Phase 4) |
| **Special characters (unicode)** | Escape and render correctly |
| **Filter "B2" with no B2 words** | Show all text as plain (no colored words) |
| **Search term not found** | Show all words colored (no search highlights) |

---

## Integration Points

### Called By:
1. `initReadingView()` - On tab activation (first render)
2. `updateReadingView()` - On filter/search change (re-render)

### Calls:
1. `escapeHtml()` - XSS protection
2. `renderEmptyState()` - Empty text handling
3. `handleWordClick()` (via onclick attribute) - Word click handler

---

## Testing Checklist

- [ ] Renders 100-word text correctly (all paragraphs, colored words)
- [ ] Renders 50,000-word text in <1s
- [ ] Applies CEFR filter correctly (only filtered level colored)
- [ ] Applies search term correctly (yellow highlights)
- [ ] Handles empty `processedText` (shows empty state)
- [ ] Handles text with no vocabulary matches (plain text)
- [ ] Preserves whitespace and punctuation
- [ ] Escapes HTML entities (no XSS vulnerabilities)
- [ ] Re-renders correctly on filter change
- [ ] Re-renders correctly on search input

---

**Status**: ✅ Contract Defined - Ready for Implementation
