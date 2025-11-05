# Contract: Scroll Position Persistence

**Purpose**: Save and restore reading view scroll position across tab switches

**Location**: `src/vocab_analyzer/web/static/app.js` (3 new functions)

---

## Overview

Users switching between tabs (Words → Reading View → Phrasal Verbs) should NOT lose their reading position. Scroll position is saved to `localStorage` and restored when returning to reading view.

**Lifecycle**:
1. User reads to 50% of text (scrolled down)
2. User switches to "Words" tab
3. **saveReadingPosition()** called → saves scroll offset to localStorage
4. User switches back to "Reading View" tab
5. **restoreReadingPosition()** called → scrolls to saved offset
6. User clicks "Analyze Another Book"
7. **clearReadingState()** called → removes saved position

---

## Function 1: saveReadingPosition()

### Function Signature

```javascript
/**
 * Save current reading view scroll position to localStorage
 * Called when user switches away from reading view tab
 * 
 * @returns {void}
 */
function saveReadingPosition() {
    // Implementation...
}
```

### Implementation

```javascript
function saveReadingPosition() {
    const panel = document.getElementById('reading-panel');
    if (panel) {
        const scrollTop = panel.scrollTop;
        localStorage.setItem('reading-scroll-position', scrollTop.toString());
    }
}
```

### Trigger Points

**Called by**: Tab switch event listeners (when leaving reading view)

```javascript
// Add to initReadingView()
const allTabs = document.querySelectorAll('.tab-btn');
allTabs.forEach(tab => {
    if (tab.id !== 'reading-tab') {
        tab.addEventListener('click', () => {
            // Save scroll position before switching away
            saveReadingPosition();
        });
    }
});
```

### Edge Cases

| Scenario | Expected Behavior |
|----------|------------------|
| **Reading panel not yet rendered** | `panel` is null, do nothing |
| **User has not scrolled** | Save `scrollTop = 0` |
| **localStorage quota exceeded** | Silent fail (not critical feature) |

---

## Function 2: restoreReadingPosition()

### Function Signature

```javascript
/**
 * Restore reading view scroll position from localStorage
 * Called when user switches to reading view tab
 * 
 * @returns {void}
 */
function restoreReadingPosition() {
    // Implementation...
}
```

### Implementation

```javascript
function restoreReadingPosition() {
    const panel = document.getElementById('reading-panel');
    const savedPosition = localStorage.getItem('reading-scroll-position');
    
    if (panel && savedPosition) {
        const scrollTop = parseInt(savedPosition, 10);
        
        // Restore scroll position after DOM has rendered
        // Use setTimeout to ensure DOM is fully painted
        setTimeout(() => {
            panel.scrollTop = scrollTop;
        }, 0);
    }
}
```

### Trigger Points

**Called by**: Reading view tab activation

```javascript
// Add to initReadingView()
const readingTab = document.getElementById('reading-tab');
readingTab.addEventListener('click', () => {
    if (window.currentAnalysisResults && window.currentAnalysisResults.processed_text) {
        // Render reading view if needed
        parseTextForReading(
            window.currentAnalysisResults.processed_text,
            window.currentAnalysisResults
        );
        
        // Restore scroll position AFTER rendering
        restoreReadingPosition();
    }
});
```

### Edge Cases

| Scenario | Expected Behavior |
|----------|------------------|
| **No saved position** | `savedPosition` is null, do nothing |
| **Invalid saved value** | `parseInt()` returns NaN, do nothing |
| **Saved position exceeds content height** | Browser clamps to max scroll (natural behavior) |
| **DOM not fully rendered** | `setTimeout()` ensures scroll happens after paint |

---

## Function 3: clearReadingState()

### Function Signature

```javascript
/**
 * Clear all reading view state from localStorage
 * Called when user starts a new analysis ("Analyze Another Book")
 * 
 * @returns {void}
 */
function clearReadingState() {
    // Implementation...
}
```

### Implementation

```javascript
function clearReadingState() {
    localStorage.removeItem('reading-scroll-position');
}
```

### Trigger Points

**Called by**: "Analyze Another Book" button handler

```javascript
// Add to existing analyzeAnotherBtn event listener
analyzeAnotherBtn.addEventListener('click', () => {
    // Clear all state
    currentSessionId = null;
    analysisResults = null;
    currentFilter = 'all';
    searchTerm = '';
    
    // Clear reading view state
    clearReadingState();
    
    // Reset UI (existing logic)
    hideAllSections();
    showSection(uploadSection);
    // ...
});
```

### Edge Cases

| Scenario | Expected Behavior |
|----------|------------------|
| **No saved position** | `removeItem()` is idempotent, no error |
| **Multiple analyses in session** | Each new analysis clears previous state |

---

## localStorage Schema

### Key: `reading-scroll-position`

**Type**: `string` (numeric value as string)

**Format**: Scroll offset in pixels (e.g., `"1250"`)

**Examples**:
- `"0"` → Top of page
- `"1250"` → Scrolled 1250px down
- `"5000"` → Scrolled 5000px down (long text)

**Lifetime**: Persists across page reloads until cleared by `clearReadingState()`

---

## Performance Considerations

### Scroll Event Debouncing

**Question**: Should we save scroll position on every scroll event?

**Answer**: NO - Only save on tab switch
- Scroll events fire 60+ times per second (janky if saving to localStorage)
- Tab switch is infrequent (once per user action)
- Saving on tab switch is sufficient for UX

### Restore Timing

**Question**: When to restore scroll position?

**Answer**: After DOM rendering completes
- Use `setTimeout(..., 0)` to defer until next event loop tick
- Ensures DOM is fully painted before scrolling
- Alternative: `requestAnimationFrame()` (not necessary for this use case)

---

## Testing Checklist

### Save Functionality
- [ ] Scroll to 50% of text, switch to Words tab → position saved to localStorage
- [ ] Scroll to bottom, switch away → bottom position saved
- [ ] Not yet scrolled (scrollTop = 0), switch away → 0 saved
- [ ] Verify localStorage key exists: `reading-scroll-position`

### Restore Functionality
- [ ] Switch back to Reading View → scroll position restored correctly
- [ ] Saved position 1250px → scrolls to 1250px
- [ ] No saved position → starts at top (no scroll)
- [ ] Invalid saved value → starts at top (no crash)

### Clear Functionality
- [ ] Click "Analyze Another Book" → localStorage key removed
- [ ] Start new analysis → previous scroll position NOT restored

### Edge Cases
- [ ] Switch tabs rapidly (spam click) → no errors
- [ ] localStorage disabled (privacy mode) → no errors, feature degrades gracefully
- [ ] Very long text (scrollTop > 10,000px) → restores correctly

---

## Integration Points

### Called By:
1. Tab switch event listeners → `saveReadingPosition()`
2. Reading view tab activation → `restoreReadingPosition()`
3. "Analyze Another Book" button → `clearReadingState()`

### Calls:
- `localStorage.setItem()` - Web Storage API
- `localStorage.getItem()` - Web Storage API
- `localStorage.removeItem()` - Web Storage API

---

**Status**: ✅ Contract Defined - Ready for Implementation
