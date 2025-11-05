# Developer Quickstart: Advanced Interaction & Layout Optimization

**Feature**: 004-advanced-interaction
**Date**: 2025-11-04
**Audience**: Developers implementing this feature

---

## Quick Reference

**What**: UI/UX enhancement - CSS/HTML/JS changes only, no backend
**Time**: 22-31 hours estimated (3-4 days focused work)
**Files**: 4 main files + design token validation
**Testing**: Manual + automated accessibility (Lighthouse, axe DevTools)

---

## Prerequisites

### Before You Start

1. **Verify Feature 003 Design Tokens**:
   ```bash
   grep -A 50 ":root {" src/vocab_analyzer/web/static/styles.css | grep "^  --"
   ```
   Confirm tokens exist: `--space-*`, `--color-*`, `--shadow-*`

2. **Checkout Feature Branch**:
   ```bash
   git checkout 004-advanced-interaction
   ```

3. **Read Documentation**:
   - `specs/004-advanced-interaction/spec.md` - Requirements
   - `specs/004-advanced-interaction/research.md` - Technical decisions
   - `specs/004-advanced-interaction/data-model.md` - Component specs

4. **Start Development Server**:
   ```bash
   cd "/path/to/project"
   source venv/bin/activate
   python -m vocab_analyzer.web.app
   # Open http://127.0.0.1:5000
   ```

---

## Files to Modify

### Primary Modification (60% of effort)

**File**: `src/vocab_analyzer/web/static/styles.css`
- **Current**: ~35KB
- **Target**: ~50KB (+15KB)
- **Changes**: Add responsive containers, tab navigation styles, enhanced card hover states, modal responsive widths, skeleton screens

### Minor Updates (30% of effort)

**File**: `src/vocab_analyzer/web/static/app.js`
- **Changes**: ~50 lines
  - Tab switching logic
  - State persistence (localStorage)
  - Filter/search sync across tabs
  - Modal focus management (already exists, enhance if needed)

**File**: `src/vocab_analyzer/web/static/index.html`
- **Changes**: ~20 lines
  - Add CSS classes for responsive containers
  - Update word card structure (remove "翻" button)

**File**: `src/vocab_analyzer/web/templates/results.html`
- **Changes**: ~100 lines
  - Replace side-by-side columns with tab navigation HTML
  - Add tab buttons with ARIA attributes
  - Update modal structure for responsive widths

### Validation Only (10% of effort)

**Files**: No changes, just verify compatibility
- `src/vocab_analyzer/web/templates/base.html`
- `src/vocab_analyzer/web/templates/upload.html`

---

## Implementation Sequence

### Phase 1: Responsive Container (2-3 hours)

**Goal**: Add 5 breakpoints with adaptive container widths

**Steps**:
1. Open `src/vocab_analyzer/web/static/styles.css`
2. Find or create `.container` class
3. Add media queries:

```css
/* Mobile (default) */
.container {
  width: 100%;
  padding: 0 var(--space-5); /* 20px */
  margin: 0 auto;
}

/* Tablet (768px+) */
@media (min-width: 768px) {
  .container {
    max-width: 720px;
    padding: 0 var(--space-6); /* 24px */
  }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
  .container {
    max-width: 960px;
    padding: 0 var(--space-8); /* 32px */
  }
}

/* Large Desktop (1280px+) */
@media (min-width: 1280px) {
  .container {
    max-width: 1280px;
  }
}

/* Extra Large (1440px+) */
@media (min-width: 1440px) {
  .container {
    max-width: 1400px;
  }
}
```

**Test**: Use Chrome DevTools responsive mode to verify at each breakpoint

---

### Phase 2: Word Card Enhancement (3-4 hours)

**Goal**: Make entire card clickable, remove "翻" button, add hover states

**CSS Changes** (`styles.css`):
```css
.word-card {
  cursor: pointer;
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-base);
  transition: transform 200ms ease-out, box-shadow 200ms ease-out, border-color 200ms ease-out;
  padding: var(--space-4);
  border-radius: 8px;
  min-height: 44px; /* Mobile touch target */
}

.word-card:hover {
  border-color: var(--primary-color); /* Blue */
  transform: translateY(-3px); /* Lift 3px */
  box-shadow: var(--shadow-large);
}

.word-card:active {
  transform: translateY(-1px);
  box-shadow: var(--shadow-medium);
}

.word-card:focus-visible {
  outline: 2px solid var(--focus-ring);
  outline-offset: 2px;
}

/* Grid - responsive columns */
.word-grid {
  display: grid;
  gap: var(--space-4);
}

@media (max-width: 767px) {
  .word-grid { grid-template-columns: 1fr; }
}

@media (min-width: 768px) and (max-width: 1023px) {
  .word-grid { grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); }
}

@media (min-width: 1024px) and (max-width: 1279px) {
  .word-grid { grid-template-columns: repeat(4, 1fr); }
}

@media (min-width: 1280px) and (max-width: 1439px) {
  .word-grid { grid-template-columns: repeat(5, 1fr); }
}

@media (min-width: 1440px) {
  .word-grid { grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); }
}
```

**HTML Changes** (`index.html` or `results.html`):
- Remove `<button class="translate-btn">翻</button>` from word cards
- Add `tabindex="0" role="button"` to `.word-card` div
- Add click handler in JavaScript

**JavaScript Changes** (`app.js`):
```javascript
// Make cards clickable
document.querySelectorAll('.word-card').forEach(card => {
  card.addEventListener('click', () => {
    const word = card.dataset.word;
    openWordModal(word); // Existing function
  });

  // Keyboard accessibility
  card.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      card.click();
    }
  });
});
```

**Test**: Click cards, verify modal opens, test hover states, test keyboard (Tab + Enter)

---

### Phase 3: Tab Navigation (4-5 hours)

**Goal**: Replace side-by-side columns with tab-based navigation

**HTML Changes** (`results.html`):
```html
<!-- Replace existing side-by-side layout -->
<div class="tab-navigation" role="tablist" aria-label="Vocabulary Categories">
  <button class="tab-button active"
          role="tab"
          aria-selected="true"
          aria-controls="words-panel"
          data-tab="words">
    <span class="tab-label-primary">单词 (<span class="word-count">152</span>)</span>
    <span class="tab-label-secondary"> / Words</span>
  </button>

  <button class="tab-button"
          role="tab"
          aria-selected="false"
          aria-controls="phrases-panel"
          data-tab="phrases">
    <span class="tab-label-primary">短语动词 (<span class="phrase-count">37</span>)</span>
    <span class="tab-label-secondary"> / Phrasal Verbs</span>
  </button>
</div>

<div id="words-panel" class="tab-content active" role="tabpanel">
  <!-- Word cards -->
</div>

<div id="phrases-panel" class="tab-content" role="tabpanel" hidden>
  <!-- Phrase cards -->
</div>
```

**CSS Changes** (`styles.css`):
```css
.tab-navigation {
  display: flex;
  gap: var(--space-2);
  border-bottom: 2px solid var(--border-color);
  margin-bottom: var(--space-6);
}

.tab-button {
  background: transparent;
  border: none;
  border-bottom: 3px solid transparent;
  padding: var(--space-3) var(--space-4);
  color: var(--text-secondary);
  font-size: 16px;
  font-weight: 400;
  cursor: pointer;
  transition: all 200ms ease-out;
  min-height: 44px;
  position: relative;
  bottom: -2px;
}

.tab-button.active {
  color: var(--primary-color);
  border-bottom-color: var(--primary-color);
  font-weight: 600;
}

.tab-button:not(.active):hover {
  background-color: var(--background-hover);
  color: var(--text-primary);
}

.tab-content {
  display: none;
}

.tab-content.active {
  display: block;
}

/* Hide English labels on mobile */
@media (max-width: 767px) {
  .tab-label-secondary { display: none; }
}
```

**JavaScript Changes** (`app.js`):
```javascript
// Tab switching with state persistence
function switchTab(tabId) {
  // Update UI
  document.querySelectorAll('.tab-button').forEach(btn => {
    const isActive = btn.dataset.tab === tabId;
    btn.classList.toggle('active', isActive);
    btn.setAttribute('aria-selected', isActive);
  });

  document.querySelectorAll('.tab-content').forEach(panel => {
    const isActive = panel.id === `${tabId}-panel`;
    panel.classList.toggle('active', isActive);
    panel.hidden = !isActive;
  });

  // Persist state
  localStorage.setItem('activeTab', tabId);

  // Apply filters/search
  applyFilters();
  applySearch();
}

// Event listeners
document.querySelectorAll('.tab-button').forEach(tab => {
  tab.addEventListener('click', () => switchTab(tab.dataset.tab));

  // Keyboard navigation
  tab.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') {
      const next = tab.nextElementSibling;
      if (next) { next.focus(); next.click(); }
    } else if (e.key === 'ArrowLeft') {
      const prev = tab.previousElementSibling;
      if (prev) { prev.focus(); prev.click(); }
    }
  });
});

// Restore active tab on page load
const savedTab = localStorage.getItem('activeTab') || 'words';
switchTab(savedTab);
```

**Test**: Click tabs, verify content switches, test keyboard (Arrow keys), refresh page (state persists)

---

### Phase 4: Modal Enhancements (3-4 hours)

**Goal**: Responsive modal widths, skeleton loading screens, error states

**CSS Changes** (`styles.css`):
```css
/* Modal responsive widths */
.modal-content {
  background: white;
  border-radius: 12px;
  padding: var(--space-6);
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-large);
}

@media (max-width: 767px) {
  .modal-content {
    width: 90%;
    margin: 0 var(--space-5);
  }
}

@media (min-width: 768px) and (max-width: 1023px) {
  .modal-content {
    width: 80%;
    max-width: 600px;
  }
}

@media (min-width: 1024px) and (max-width: 1439px) {
  .modal-content {
    width: 60%;
    max-width: 700px;
  }
}

@media (min-width: 1440px) {
  .modal-content {
    max-width: 800px;
    width: 60%;
  }
}

/* Skeleton screens */
.skeleton {
  background-color: var(--border-color);
  border-radius: 4px;
  position: relative;
  overflow: hidden;
}

.skeleton::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.6) 50%, transparent 100%);
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { left: -100%; }
  100% { left: 100%; }
}

.translation-skeleton {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  padding: var(--space-4);
}

.skeleton-line {
  height: 16px;
  width: 100%;
}

.skeleton-line:nth-child(2) { width: 80%; }
.skeleton-line:nth-child(3) { width: 60%; }

/* Error state */
.translation-error {
  text-align: center;
  color: var(--error-text);
  padding: var(--space-4);
}

.btn-retry {
  margin-top: var(--space-2);
  padding: var(--space-2) var(--space-4);
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  min-height: 36px;
}
```

**JavaScript** (modal already exists, enhance if needed):
- Show skeleton while loading translation
- Hide skeleton when translation loads
- Show error state if translation fails

**Test**: Open modal, verify skeleton appears, verify responsive widths at all breakpoints

---

### Phase 5: Accessibility & Polish (2-3 hours)

**Goal**: WCAG AA compliance, keyboard navigation, focus indicators

**Focus Indicators** (`styles.css`):
```css
/* Remove default outline */
:focus {
  outline: none;
}

/* Custom focus indicator (keyboard only) */
:focus-visible {
  outline: 2px solid var(--focus-ring);
  outline-offset: 2px;
  box-shadow: var(--focus-ring-shadow);
}
```

**Touch Targets (Mobile)** (`styles.css`):
```css
/* Ensure all interactive elements are 44x44px on mobile */
@media (max-width: 767px) {
  button, .clickable, .word-card, .tab-button {
    min-height: 44px;
    min-width: 44px;
  }
}
```

**Test**:
1. **Keyboard Navigation**: Tab through page, verify focus indicators visible
2. **Lighthouse Audit**: Run audit, target 100 accessibility score
3. **axe DevTools**: Run scan, target 0 violations
4. **Touch Targets**: Measure with DevTools, verify all ≥44x44px on mobile

---

## Testing Checklist

### Before Committing

- [ ] Desktop (1440px+): Container 1400px, cards 5-6 columns, tabs bilingual
- [ ] Desktop (1280-1439px): Container 1280px, cards 5 columns
- [ ] Desktop (1024-1279px): Container 960px, cards 4 columns
- [ ] Tablet (768-1023px): Container 720px, cards 2-3 columns
- [ ] Mobile (375-767px): Container 100%, cards 1 column, tabs simplified
- [ ] All interactive elements have hover states (cards, buttons, tabs)
- [ ] Skeleton screens appear during loading
- [ ] Error states show friendly messages
- [ ] Keyboard navigation works (Tab, Enter, Escape, Arrow keys)
- [ ] Focus indicators visible on all focusable elements
- [ ] Touch targets ≥44x44px on mobile (measure with DevTools)
- [ ] Lighthouse accessibility score: 100
- [ ] axe DevTools violations: 0
- [ ] CSS file size <100KB (check with `ls -lh styles.css`)
- [ ] No console errors in Chrome DevTools
- [ ] Tab state persists after page reload

### Cross-Browser Testing

- [ ] Chrome 120+: All features work
- [ ] Safari 17+: All features work
- [ ] Firefox 121+: All features work

---

## Common Pitfalls

### Issue: Focus Indicator Not Showing

**Problem**: Using `:focus` instead of `:focus-visible`
**Solution**: Always use `:focus-visible` for keyboard-only indicators

### Issue: Layout Shift When Content Loads

**Problem**: No reserved space for skeleton screens
**Solution**: Add `min-height` matching expected content height

### Issue: Tab State Lost on Refresh

**Problem**: Not using localStorage
**Solution**: Persist state with `localStorage.setItem('activeTab', tabId)`

### Issue: Touch Targets Too Small on Mobile

**Problem**: Forgetting `min-height: 44px` on buttons
**Solution**: Add media query for mobile touch target sizing

### Issue: Horizontal Scrolling on Mobile

**Problem**: Fixed widths instead of `width: 100%`
**Solution**: Use percentage widths and `max-width` instead of fixed widths

---

## Quick Reference: Design Tokens

```css
/* Spacing (8px grid) */
--space-1: 4px;    --space-2: 8px;    --space-3: 12px;
--space-4: 16px;   --space-5: 20px;   --space-6: 24px;
--space-8: 32px;   --space-10: 40px;  --space-12: 48px;

/* Colors */
--primary-color: #2563eb;      --primary-hover: #1d4ed8;
--text-primary: #1f2937;       --text-secondary: #6b7280;
--border-color: #e5e7eb;       --background-hover: #f3f4f6;
--focus-ring: #2563eb;         --error-text: #dc2626;

/* Shadows */
--shadow-base: 0 1px 3px rgba(0,0,0,0.1);
--shadow-medium: 0 4px 6px rgba(0,0,0,0.1);
--shadow-large: 0 10px 15px rgba(0,0,0,0.1);
```

---

## Debugging Tips

### Chrome DevTools

**Responsive Mode**: `Cmd+Shift+M` (Mac) / `Ctrl+Shift+M` (Windows)
- Test all breakpoints: 375px, 768px, 1024px, 1280px, 1440px

**Measure Touch Targets**:
1. Inspect element
2. Go to Computed tab
3. Check `height` and `width`
4. Verify ≥44px on mobile

**Performance Panel**:
- Record → Interact → Stop
- Check FPS (target: 60fps)
- Check animation timing (target: 200-300ms)

### Lighthouse Audit

1. Open DevTools → Lighthouse tab
2. Select "Accessibility" category
3. Click "Analyze page load"
4. Target: 100 score

### axe DevTools

1. Install extension: https://www.deque.com/axe/devtools/
2. Open extension panel
3. Click "Scan ALL of my page"
4. Target: 0 violations

---

## Getting Help

**Documentation**:
- `specs/004-advanced-interaction/spec.md` - Full requirements
- `specs/004-advanced-interaction/research.md` - Technical decisions
- `specs/004-advanced-interaction/data-model.md` - Component specs

**External Resources**:
- WCAG 2.1 AA: https://www.w3.org/WAI/WCAG21/quickref/?levels=aa
- CSS Grid Guide: https://css-tricks.com/snippets/css/complete-guide-grid/
- Flexbox Guide: https://css-tricks.com/snippets/css/a-guide-to-flexbox/

---

**Quickstart Complete**: Follow sequence Phase 1 → Phase 5, test thoroughly, commit when checklist complete
