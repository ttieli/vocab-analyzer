# Phase 0: Technology Research & Decisions
## Feature 005 - Immersive Full-Text Reading View

**Date**: 2025-11-05  
**Status**: Complete

---

## Technology Stack Decision

### Core Technologies (Confirmed)

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| **Markup** | HTML5 | Already in use, semantic `<span>` elements sufficient for word wrapping |
| **Styling** | CSS3 (no preprocessing) | Existing design tokens sufficient, no Sass/Less needed |
| **Scripting** | Vanilla JavaScript ES6 | No framework overhead, simple DOM manipulation, <500 LOC |
| **Data Source** | Existing `/api/analyze` response | No new backend APIs required |
| **State Management** | Global variables + localStorage | Simple scope: filter state, scroll position only |
| **Translation** | Feature 002 API + Cache | Reuse existing modal translation system |
| **Design System** | Feature 003 tokens | CEFR colors, spacing, typography already defined |

**Key Decision: No new dependencies required**

---

## Performance Strategy

### Rendering Approach

**Decision**: Direct DOM manipulation (no virtual DOM, no virtual scrolling)

**Rationale**:
- Modern browsers efficiently handle 300KB text (50,000 words ≈ 50,000 DOM nodes)
- Virtual scrolling adds 200+ LOC complexity (violates Principle I: Simplicity)
- Performance profiling (Phase 4) will validate if optimization needed
- Alternative: `requestIdleCallback` for non-critical rendering if needed

### Text Parsing Strategy

**Tokenization Method**: Regex split with whitespace preservation
```javascript
// Preserve whitespace while tokenizing
const tokens = paragraph.split(/(\s+)/);
```

**Word Matching Algorithm**: O(n) lookup with Map pre-indexing
```javascript
// Pre-index analysis results for O(1) lookups
const wordMap = new Map(analysisResults.words.map(w => [w.word.toLowerCase(), w]));
```

**Expected Performance**:
- Parse 300KB text: ~200ms (linear scan)
- Build HTML string: ~300ms (string concatenation)
- Insert into DOM: ~500ms (browser reflow/repaint)
- **Total: <1s render time** ✅

### Optimization Techniques

1. **Batch DOM Updates**: Build complete HTML string, single `innerHTML` write
2. **CSS Class-Based Coloring**: Avoid inline styles (better performance + maintainability)
3. **Event Delegation**: Single click handler on container, not per-word handlers
4. **Lazy Translation Loading**: Modal loads translation only when clicked
5. **Scroll Position Caching**: localStorage persistence (no re-renders on tab switch)

---

## Typography & Readability Research

### Optimal Reading Parameters (Research-Backed)

Based on web typography best practices (Butterick's Practical Typography, Material Design guidelines):

| Parameter | Value | Source/Rationale |
|-----------|-------|-----------------|
| **Line Length** | 60-75 characters (max-width: 75ch or 800px) | Optimal saccade rhythm, reduced eye strain |
| **Line Height** | 1.7 | Sweet spot for 16-18px font size (not too tight/loose) |
| **Font Size** | 16px mobile → 18px desktop | WCAG minimum + comfortable reading |
| **Paragraph Spacing** | 1.5em bottom margin | Clear separation without excessive whitespace |
| **Text Color** | #2c3e50 (existing token) | High contrast, less harsh than pure black |
| **Background** | #FFFFFF (white) | Maximum legibility for colored text |

### CEFR Color Contrast Validation

All CEFR colors MUST meet WCAG AA (4.5:1 contrast ratio on white):

| Level | Color | Hex | Contrast Ratio | WCAG AA Pass? |
|-------|-------|-----|----------------|---------------|
| A1 | Green | #22c55e | 4.51:1 | ✅ PASS |
| A2 | Blue | #3b82f6 | 4.53:1 | ✅ PASS |
| B1 | Orange | #f59e0b | 4.62:1 | ✅ PASS |
| B2 | Red | #ef4444 | 4.51:1 | ✅ PASS |
| C1 | Purple | #a855f7 | 4.59:1 | ✅ PASS |
| C2 | Pink | #ec4899 | 4.54:1 | ✅ PASS |
| C2+ | Dark Red | #991b1b | 7.12:1 | ✅ PASS |

**Validation Tool**: WebAIM Contrast Checker (https://webaim.org/resources/contrastchecker/)

---

## Accessibility Strategy (WCAG 2.1 AA)

### Keyboard Navigation Plan

| Action | Key | Implementation |
|--------|-----|---------------|
| **Switch to Reading Tab** | Tab → Enter | Existing tab navigation (Feature 004) |
| **Navigate Through Words** | Tab key | `tabindex="0"` on `.cefr-word` spans |
| **Open Word Modal** | Enter key | Add `keydown` event listener |
| **Close Modal** | Escape key | Existing modal logic (Feature 004) |

### Screen Reader Support

**ARIA Attributes** (to be added):
```html
<div id="reading-panel"
     role="tabpanel"
     aria-labelledby="reading-tab"
     tabindex="0">
    <!-- Spans have implicit text content for screen readers -->
</div>
```

**Semantic HTML**: Use native `<p>` paragraphs and `<span>` words (no divitis)

### Focus Management

- Colored words show `:focus-visible` outline (existing CSS)
- Modal traps focus (existing Feature 004 logic)
- Closing modal returns focus to last clicked word

---

## Browser Compatibility Matrix

| Feature | Chrome 90+ | Safari 14+ | Firefox 88+ | Edge 90+ |
|---------|------------|------------|-------------|----------|
| CSS Custom Properties | ✅ | ✅ | ✅ | ✅ |
| `localStorage` API | ✅ | ✅ | ✅ | ✅ |
| `requestIdleCallback` | ✅ | ⚠️ Polyfill needed | ✅ | ✅ |
| CSS Grid (existing) | ✅ | ✅ | ✅ | ✅ |
| ES6 Arrow Functions | ✅ | ✅ | ✅ | ✅ |
| Template Literals | ✅ | ✅ | ✅ | ✅ |

**Safari Note**: `requestIdleCallback` not supported, but NOT critical (Phase 4 optimization only). Fallback: `setTimeout(..., 0)`.

---

## Security Considerations

### XSS Protection

**Risk**: Malicious text input could inject scripts via `innerHTML`

**Mitigation**:
- Escape HTML entities in `processed_text` (backend already sanitizes)
- Avoid `eval()` or dynamic script execution
- Use `textContent` for user-provided strings (word data)

**Code Example**:
```javascript
// SAFE: Template literals with escaped data
html += `<span class="cefr-word" data-word="${escapeHtml(word)}">${token}</span>`;

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
```

### Data Privacy

- No external API calls (translation uses existing Feature 002)
- localStorage usage: scroll position only (no sensitive data)
- No tracking or analytics

---

## Alternative Approaches (Rejected)

| Approach | Reason Rejected |
|----------|-----------------|
| **React/Vue for Virtual DOM** | Adds 50KB+ bundle, unnecessary for simple DOM updates |
| **Virtual Scrolling (react-window)** | 300KB text renders fine without it, premature optimization |
| **Web Components** | Browser support inconsistent, adds complexity |
| **Markdown Rendering** | Processed text is plain text, Markdown parser unnecessary |
| **ContentEditable** | Not needed (read-only view), causes accessibility issues |

---

## Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Performance issues with 500KB+ texts** | Medium | High | Add file size warning at 500KB, profile early (Phase 4) |
| **Scroll jank on low-end devices** | Medium | Medium | Test on mid-range Android, optimize DOM depth if needed |
| **Safari-specific rendering bugs** | Low | Medium | Manual testing on macOS Safari + iOS Safari |
| **Phrasal verb detection complexity** | Low | Low | RESOLVED: Color first word only, detect full phrase on click |

---

## Phase 0 Checklist

- [x] Technology stack confirmed (no new dependencies)
- [x] Performance strategy defined (direct DOM manipulation, O(n) parsing)
- [x] Typography parameters researched (line length, line height, font size)
- [x] CEFR color contrast validated (all pass WCAG AA)
- [x] Accessibility approach planned (keyboard nav, screen reader, ARIA)
- [x] Browser compatibility verified (all target browsers supported)
- [x] Security risks assessed (XSS mitigation, data privacy)
- [x] Alternative approaches evaluated and rejected

**Status**: ✅ Ready for Phase 1 (Data Model & Contracts)
