# Contract: handleWordClick()

**Purpose**: Handle word click in reading view, open modal with word details and translation

**Location**: `src/vocab_analyzer/web/static/app.js` (new function)

---

## Function Signature

```javascript
/**
 * Handle word click in reading view - open modal with word details
 * 
 * @param {string} word - Lemmatized word (from data-word attribute)
 * @returns {void} - Opens modal by calling showWordDetails()
 */
function handleWordClick(word) {
    // Implementation...
}
```

---

## Input Specification

### Parameter: `word` (string)

**Source**: `onclick` attribute in generated HTML span

**Format**: Lemmatized word or phrasal verb phrase

**Examples**:
- `"ambitious"` → regular word
- `"entrepreneur"` → regular word
- `"make up"` → phrasal verb (full phrase, not just "make")

**Validation**:
- MUST be non-empty string
- MUST exist in `window.currentAnalysisResults.words` or `.phrasal_verbs`

---

## Output Specification

### Return Value: `void`

Function does NOT return a value. It performs side effect:
- Opens word detail modal by calling `showWordDetails(wordData)`

---

## Processing Algorithm

### Step 1: Validate Input

```javascript
if (!word || typeof word !== 'string') {
    console.error('Invalid word:', word);
    return;
}
```

### Step 2: Find Word Data in Analysis Results

```javascript
// Check regular words
let wordData = window.currentAnalysisResults.words?.find(w => 
    w.word.toLowerCase() === word.toLowerCase()
);

// If not found, check phrasal verbs
if (!wordData) {
    const phraseData = window.currentAnalysisResults.phrasal_verbs?.find(pv => 
        pv.phrase.toLowerCase() === word.toLowerCase()
    );
    
    if (phraseData) {
        // Normalize phrasal verb data to match word structure
        wordData = {
            ...phraseData,
            word: phraseData.phrase  // Use "word" key for consistency
        };
    }
}
```

### Step 3: Open Modal

```javascript
if (wordData) {
    showWordDetails(wordData);  // Reuse existing modal function (Feature 004)
} else {
    console.error('Word not found in analysis results:', word);
}
```

---

## Integration with Existing Modal (Feature 004)

### `showWordDetails(wordData)` Function

**Location**: `src/vocab_analyzer/web/static/app.js` (existing function from Feature 004)

**Expected Input**:
```javascript
{
    word: "ambitious",
    cefr_level: "C1",
    count: 12,
    examples: [
        "The ambitious entrepreneur started a company.",
        "Her ambitious goals drove her forward."
    ]
}
```

**Behavior**:
1. Opens modal (`#word-modal`)
2. Displays word, CEFR badge, frequency count
3. Auto-loads Chinese translation (Feature 002)
   - Shows cached translation immediately if available
   - Shows skeleton screen + loads from API if not cached
4. Displays example sentences
5. Handles modal close (X button, outside click, Escape key)

**No changes needed** to `showWordDetails()` - it already handles both words and phrasal verbs.

---

## Scroll Position Preservation

**Requirement**: Modal open/close MUST NOT change scroll position in reading view

**Implementation**: Already handled by existing modal system (Feature 004)
- Modal uses `position: fixed` (does not affect document flow)
- Closing modal does NOT trigger scroll events
- Reading panel maintains `scrollTop` value

**Testing**: Open modal, scroll modal content, close modal → reading view scroll unchanged

---

## Edge Cases

| Scenario | Expected Behavior |
|----------|------------------|
| **Word not in analysis results** | Log error, do not open modal |
| **Empty word string** | Log error, do not open modal |
| **Phrasal verb (multi-word)** | Find in `phrasal_verbs`, normalize to word structure, open modal |
| **Word with different case** | Case-insensitive match, open modal |
| **Rapid clicking (spam clicks)** | Modal opens once, subsequent clicks ignored (modal already open) |
| **Click during modal open animation** | No issue (modal system handles state) |

---

## Performance Requirements

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Lookup Time** | <10ms | Array.find() on ~3000 words |
| **Modal Open Time** | <100ms | From click to modal visible |
| **No Jank** | 60fps | No scroll stutter when modal opens |

---

## Integration Points

### Called By:
- `onclick` attribute in generated HTML spans

**HTML Example**:
```html
<span class="cefr-word" 
      data-word="ambitious" 
      data-level="C1"
      onclick="handleWordClick('ambitious')">ambitious</span>
```

### Calls:
1. `showWordDetails(wordData)` - Existing modal function (Feature 004)
2. `console.error()` - Error logging (if word not found)

---

## Accessibility Considerations

### Keyboard Navigation Support

**Requirement**: Users should be able to open modal with Enter key (not just click)

**Implementation**: Add `keydown` event listener to `.cefr-word` spans

```javascript
// Add to initReadingView()
document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && e.target.classList.contains('cefr-word')) {
        const word = e.target.getAttribute('data-word');
        handleWordClick(word);
    }
});
```

**Testing**: Tab to colored word, press Enter → modal opens

---

## Testing Checklist

- [ ] Clicking regular word opens modal with correct data
- [ ] Clicking phrasal verb opens modal with correct data
- [ ] Modal displays CEFR level badge correctly
- [ ] Modal loads translation (cached or fresh)
- [ ] Modal displays example sentences
- [ ] Clicking X closes modal
- [ ] Clicking outside modal closes modal
- [ ] Pressing Escape closes modal
- [ ] Scroll position preserved after modal close
- [ ] Rapid clicking does not cause errors
- [ ] Enter key on focused word opens modal (keyboard nav)
- [ ] Word not in analysis results logs error, does not crash

---

**Status**: ✅ Contract Defined - Ready for Implementation
