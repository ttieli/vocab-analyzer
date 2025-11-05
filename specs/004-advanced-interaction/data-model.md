# Data Model: UI Component Structure & Responsive Behavior

**Feature**: 004-advanced-interaction
**Date**: 2025-11-04
**Status**: ✅ Complete

---

## Overview

This document defines the structure of UI components for the Advanced Interaction & Layout Optimization feature. Since this is a **UI-only feature** with no backend changes, this "data model" describes **visual component specifications** rather than database entities.

**Key Principle**: All components use existing design tokens from Feature 003 for consistency and maintainability.

---

## Component Hierarchy

```
Responsive Container System
├── Tab Navigation Component
│   ├── Tab Button (Words)
│   └── Tab Button (Phrasal Verbs)
├── Tab Content Panel (Words)
│   ├── Filter Controls
│   ├── Search Input
│   └── Word Card Grid
│       └── Word Card Component (repeating)
└── Tab Content Panel (Phrasal Verbs)
    ├── Filter Controls
    ├── Search Input
    └── Phrase Card Grid
        └── Phrase Card Component (repeating)

Detail Modal Component (overlay)
├── Modal Backdrop
└── Modal Content
    ├── Word Display
    ├── CEFR Badge
    ├── Translation Section (with Loading State)
    ├── Frequency Display
    └── Example Sentences
        └── Example Translation Toggle (repeating)
```

---

## Component 1: Responsive Container System

**Purpose**: Adapts layout width and spacing based on screen size

### Structure

```html
<div class="container">
  <!-- Page content -->
</div>
```

### CSS Specifications

```css
/* Mobile (0px - 767px) */
.container {
  width: 100%;
  padding: 0 var(--space-5); /* 20px */
  margin: 0 auto;
}

/* Tablet (768px - 1023px) */
@media (min-width: 768px) {
  .container {
    max-width: 720px;
    padding: 0 var(--space-6); /* 24px */
  }
}

/* Desktop (1024px - 1279px) */
@media (min-width: 1024px) {
  .container {
    max-width: 960px;
    padding: 0 var(--space-8); /* 32px */
  }
}

/* Large Desktop (1280px - 1439px) */
@media (min-width: 1280px) {
  .container {
    max-width: 1280px;
  }
}

/* Extra Large Desktop (1440px+) */
@media (min-width: 1440px) {
  .container {
    max-width: 1400px;
  }
}
```

### Responsive Behavior Matrix

| Breakpoint | Min Width | Max Width | Side Padding | Behavior |
|------------|-----------|-----------|--------------|----------|
| xs | 0px | - | 20px | Full width with breathing room |
| sm | 375px | - | 20px | Full width (same as xs) |
| md | 768px | 720px | 24px | Fixed max-width, centered |
| lg | 1024px | 960px | 32px | Fixed max-width, centered |
| xl | 1280px | 1280px | 32px | Fixed max-width, centered |
| xxl | 1440px | 1400px | 32px | Fixed max-width, centered |

**Design Tokens Used**:
- `--space-5` (20px) - Mobile padding
- `--space-6` (24px) - Tablet padding
- `--space-8` (32px) - Desktop padding

---

## Component 2: Tab Navigation Component

**Purpose**: Switches between Words and Phrasal Verbs content with persistent state

### Structure

```html
<div class="tab-navigation" role="tablist" aria-label="Vocabulary Categories">
  <button class="tab-button active"
          role="tab"
          aria-selected="true"
          aria-controls="words-panel"
          data-tab="words">
    <span class="tab-label">
      <span class="tab-label-primary">单词 (152)</span>
      <span class="tab-label-secondary"> / Words</span>
    </span>
  </button>

  <button class="tab-button"
          role="tab"
          aria-selected="false"
          aria-controls="phrases-panel"
          data-tab="phrases">
    <span class="tab-label">
      <span class="tab-label-primary">短语动词 (37)</span>
      <span class="tab-label-secondary"> / Phrasal Verbs</span>
    </span>
  </button>
</div>

<div id="words-panel" class="tab-content active" role="tabpanel" aria-labelledby="words-tab">
  <!-- Words content -->
</div>

<div id="phrases-panel" class="tab-content" role="tabpanel" aria-labelledby="phrases-tab">
  <!-- Phrases content -->
</div>
```

### CSS Specifications

```css
/* Tab container */
.tab-navigation {
  display: flex;
  gap: var(--space-2); /* 8px */
  border-bottom: 2px solid var(--border-color);
  margin-bottom: var(--space-6); /* 24px */
}

/* Tab button - Base */
.tab-button {
  background: transparent;
  border: none;
  border-bottom: 3px solid transparent;
  padding: var(--space-3) var(--space-4); /* 12px 16px */
  color: var(--text-secondary); /* #6b7280 gray */
  font-size: 16px;
  font-weight: 400;
  cursor: pointer;
  transition: background-color 200ms ease-out, color 200ms ease-out, border-color 200ms ease-out;
  min-height: 44px; /* Touch target (mobile) */
  min-width: 44px;
  position: relative;
  bottom: -2px; /* Align with container border */
}

/* Tab button - Active state */
.tab-button.active {
  color: var(--primary-color); /* #2563eb blue */
  border-bottom-color: var(--primary-color);
  font-weight: 600;
}

/* Tab button - Hover (inactive only) */
.tab-button:not(.active):hover {
  background-color: var(--background-hover); /* #f3f4f6 */
  color: var(--text-primary); /* #1f2937 */
}

/* Tab button - Focus */
.tab-button:focus-visible {
  outline: 2px solid var(--focus-ring);
  outline-offset: 2px;
}

/* Tab content panels */
.tab-content {
  display: none;
  opacity: 0;
  transition: opacity 200ms ease-in-out;
}

.tab-content.active {
  display: block;
  opacity: 1;
}

/* Mobile - Hide secondary label */
@media (max-width: 767px) {
  .tab-label-secondary {
    display: none;
  }
}

/* Desktop - Show bilingual labels */
@media (min-width: 768px) {
  .tab-label-secondary {
    display: inline;
    color: var(--text-secondary);
  }
}
```

### State Management (JavaScript)

```javascript
// Tab state persistence
const activeTab = localStorage.getItem('activeTab') || 'words';
const activeFilters = JSON.parse(localStorage.getItem('activeFilters') || '{}');
const searchQuery = localStorage.getItem('searchQuery') || '';

// Tab switching
function switchTab(tabId) {
  // Update UI
  document.querySelectorAll('.tab-button').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.tab === tabId);
    btn.setAttribute('aria-selected', btn.dataset.tab === tabId);
  });

  document.querySelectorAll('.tab-content').forEach(panel => {
    panel.classList.toggle('active', panel.id === `${tabId}-panel`);
  });

  // Persist state
  localStorage.setItem('activeTab', tabId);

  // Apply persisted filters and search
  applyFilters(activeFilters);
  applySearch(searchQuery);
}
```

### Interactive States

| State | Visual Indicators | Trigger |
|-------|-------------------|---------|
| Default (Inactive) | Gray text, no border, regular weight | Initial render |
| Active | Blue text, blue bottom border (3px), bold weight | Tab clicked or page load |
| Hover (Inactive) | Light gray background, darker text | Mouse over inactive tab |
| Focus | Blue outline (2px), 2px offset | Keyboard Tab key |
| Active + Focus | Blue outline + active styling | Keyboard navigation to active tab |

**Design Tokens Used**:
- `--space-2` (8px) - Gap between tabs
- `--space-3` (12px) - Vertical padding
- `--space-4` (16px) - Horizontal padding
- `--space-6` (24px) - Bottom margin
- `--primary-color` (#2563eb) - Active tab color
- `--text-secondary` (#6b7280) - Inactive tab color
- `--text-primary` (#1f2937) - Hover text color
- `--background-hover` (#f3f4f6) - Hover background
- `--border-color` (#e5e7eb) - Container border
- `--focus-ring` (#2563eb) - Focus indicator

---

## Component 3: Word Card Component

**Purpose**: Displays individual word/phrase with CEFR level, entire card clickable

### Structure

```html
<div class="word-card" tabindex="0" role="button" aria-label="View details for 'example'">
  <div class="word-card-header">
    <span class="word-text">example</span>
    <span class="cefr-badge cefr-b1">B1</span>
  </div>
  <div class="word-card-meta">
    <span class="frequency-count">Frequency: 42</span>
  </div>
</div>
```

### CSS Specifications

```css
/* Word card grid container */
.word-grid {
  display: grid;
  gap: var(--space-4); /* 16px */
  margin-bottom: var(--space-8); /* 32px */
}

/* Mobile (1 column) */
@media (max-width: 767px) {
  .word-grid {
    grid-template-columns: 1fr;
  }
}

/* Tablet (2-3 columns) */
@media (min-width: 768px) and (max-width: 1023px) {
  .word-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  }
}

/* Desktop (4 columns) */
@media (min-width: 1024px) and (max-width: 1279px) {
  .word-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

/* Large Desktop (5 columns) */
@media (min-width: 1280px) and (max-width: 1439px) {
  .word-grid {
    grid-template-columns: repeat(5, 1fr);
  }
}

/* Extra Large Desktop (5-6 columns) */
@media (min-width: 1440px) {
  .word-grid {
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    /* Auto-fill creates 5-6 columns at 1400px container width */
  }
}

/* Individual card */
.word-card {
  background: white;
  border: 1px solid var(--border-color); /* #e5e7eb */
  border-radius: 8px;
  padding: var(--space-4); /* 16px */
  cursor: pointer;
  box-shadow: var(--shadow-base);
  transition: transform 200ms ease-out, box-shadow 200ms ease-out, border-color 200ms ease-out;
  min-height: 44px; /* Touch target (mobile) */
  display: flex;
  flex-direction: column;
  gap: var(--space-2); /* 8px */
}

/* Hover state */
.word-card:hover {
  border-color: var(--primary-color); /* #2563eb */
  transform: translateY(-3px);
  box-shadow: var(--shadow-large);
}

/* Active/pressed state */
.word-card:active {
  transform: translateY(-1px);
  box-shadow: var(--shadow-medium);
}

/* Focus state */
.word-card:focus-visible {
  outline: 2px solid var(--focus-ring);
  outline-offset: 2px;
}

/* Card header */
.word-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--space-2);
}

.word-text {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  word-break: break-word;
}

.cefr-badge {
  font-size: 12px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 12px;
  text-transform: uppercase;
  flex-shrink: 0;
}

/* CEFR level colors (existing from Feature 003) */
.cefr-a1 { background: #C8E6C9; color: #1B5E20; }
.cefr-a2 { background: #A5D6A7; color: #1B5E20; }
.cefr-b1 { background: #FFF9C4; color: #F57F17; }
.cefr-b2 { background: #FFE082; color: #F57F17; }
.cefr-c1 { background: #FFAB91; color: #BF360C; }
.cefr-c2 { background: #EF9A9A; color: #B71C1C; }

/* Card metadata */
.word-card-meta {
  font-size: 14px;
  color: var(--text-secondary);
}
```

### Interactive States

| State | Transform | Shadow | Border | Trigger |
|-------|-----------|--------|--------|---------|
| Default | none | Base | Light gray | - |
| Hover | translateY(-3px) | Large | Blue | Mouse over |
| Active | translateY(-1px) | Medium | Blue | Mouse/touch down |
| Focus | none | Base | Blue outline (2px) | Keyboard Tab |

**Design Tokens Used**:
- `--space-2` (8px) - Internal gaps
- `--space-4` (16px) - Card padding, grid gap
- `--space-8` (32px) - Grid bottom margin
- `--border-color` (#e5e7eb) - Default border
- `--primary-color` (#2563eb) - Hover/focus border
- `--text-primary` (#1f2937) - Word text
- `--text-secondary` (#6b7280) - Metadata text
- `--shadow-base`, `--shadow-medium`, `--shadow-large` - Elevation states
- `--focus-ring` (#2563eb) - Focus outline

**Note**: **"翻" translation button removed** - entire card is clickable, no separate button needed (FR-002)

---

## Component 4: Detail Modal Component

**Purpose**: Displays complete word information with auto-loaded translation

### Structure

```html
<div class="modal" role="dialog" aria-modal="true" aria-labelledby="modal-title">
  <div class="modal-backdrop"></div>
  <div class="modal-content">
    <button class="modal-close" aria-label="Close">&times;</button>

    <h2 id="modal-title" class="modal-word">example</h2>
    <span class="cefr-badge cefr-b1">B1</span>

    <div class="modal-translation">
      <!-- Loading state -->
      <div class="translation-skeleton">
        <div class="skeleton-line" style="width: 80%;"></div>
        <div class="skeleton-line" style="width: 60%;"></div>
        <p class="loading-text">正在加载... / Loading...</p>
      </div>

      <!-- Loaded state -->
      <div class="translation-content">
        <p class="translation-text">例子；实例；范例</p>
        <span class="translation-source">缓存</span>
      </div>

      <!-- Error state -->
      <div class="translation-error">
        <p>暂时无法获取释义</p>
        <button class="btn-retry">重试</button>
      </div>
    </div>

    <div class="modal-frequency">
      <strong>Frequency:</strong> 42 occurrences
    </div>

    <div class="modal-examples">
      <h3>Example Sentences</h3>
      <div class="example-item">
        <p class="example-sentence">This is an example sentence.</p>
        <button class="example-translate-btn" aria-label="Translate this sentence">翻译</button>
        <div class="example-translation" hidden>
          <p>这是一个示例句子。</p>
          <button class="example-translation-close" aria-label="Hide translation">&times;</button>
        </div>
      </div>
      <!-- More examples... -->
    </div>
  </div>
</div>
```

### CSS Specifications

```css
/* Modal backdrop */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1000;
  display: none; /* Hidden by default */
  align-items: center;
  justify-content: center;
}

.modal.active {
  display: flex;
}

.modal-backdrop {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: -1;
}

/* Modal content - Responsive widths */
.modal-content {
  background: white;
  border-radius: 12px;
  padding: var(--space-6); /* 24px */
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-large);
  position: relative;
}

/* Mobile (<768px) - 90% width */
@media (max-width: 767px) {
  .modal-content {
    width: 90%;
    margin: 0 var(--space-5); /* 20px */
  }
}

/* Tablet (768-1024px) - 80% width, max 600px */
@media (min-width: 768px) and (max-width: 1023px) {
  .modal-content {
    width: 80%;
    max-width: 600px;
  }
}

/* Desktop (1024-1440px) - 60% width, max 700px */
@media (min-width: 1024px) and (max-width: 1439px) {
  .modal-content {
    width: 60%;
    max-width: 700px;
  }
}

/* Large Desktop (1440px+) - max 800px */
@media (min-width: 1440px) {
  .modal-content {
    max-width: 800px;
    width: 60%;
  }
}

/* Modal header */
.modal-word {
  font-size: 36px;
  font-weight: 700;
  color: var(--primary-color);
  margin-bottom: var(--space-2);
}

.modal-close {
  position: absolute;
  top: var(--space-4);
  right: var(--space-4);
  background: transparent;
  border: none;
  font-size: 32px;
  color: var(--text-secondary);
  cursor: pointer;
  line-height: 1;
  padding: var(--space-2);
  min-width: 44px;
  min-height: 44px;
  transition: color 150ms ease-out;
}

.modal-close:hover {
  color: var(--text-primary);
}

/* Translation section */
.modal-translation {
  margin: var(--space-4) 0;
  padding: var(--space-4);
  background: var(--background-hover);
  border-radius: 8px;
}

/* Skeleton loading state */
.translation-skeleton {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.skeleton-line {
  height: 16px;
  background: var(--border-color);
  border-radius: 4px;
  position: relative;
  overflow: hidden;
}

.skeleton-line::before {
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

.loading-text {
  font-size: 14px;
  color: var(--text-secondary);
  text-align: center;
  margin-top: var(--space-2);
}

/* Loaded translation */
.translation-content {
  font-size: 16px;
  line-height: 1.6;
  color: var(--text-primary);
}

.translation-source {
  display: inline-block;
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: var(--space-1);
}

/* Error state */
.translation-error {
  text-align: center;
  color: var(--error-text);
}

.btn-retry {
  margin-top: var(--space-2);
  padding: var(--space-2) var(--space-4);
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  min-height: 36px;
  transition: background-color 150ms ease-out;
}

.btn-retry:hover {
  background: var(--primary-hover);
}

/* Example sentences */
.modal-examples {
  margin-top: var(--space-6);
}

.modal-examples h3 {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: var(--space-3);
}

.example-item {
  margin-bottom: var(--space-4);
  padding: var(--space-3);
  border: 1px solid var(--border-color);
  border-radius: 8px;
}

.example-sentence {
  font-size: 16px;
  line-height: 1.6;
  margin-bottom: var(--space-2);
}

.example-translate-btn {
  padding: var(--space-1) var(--space-3);
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  min-height: 36px;
  transition: background-color 150ms ease-out;
}

.example-translate-btn:hover {
  background: var(--primary-hover);
}

.example-translation {
  margin-top: var(--space-2);
  padding: var(--space-3);
  background: #FEF3C7; /* Yellow background */
  border-radius: 6px;
  position: relative;
}

.example-translation-close {
  position: absolute;
  top: var(--space-2);
  right: var(--space-2);
  background: transparent;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: var(--text-secondary);
  line-height: 1;
}
```

### Modal State Diagram

```
[Closed] --click card--> [Opening]
                            |
                            v
                      [Open + Loading]
                      /              \
                     /                \
            [Translation Loaded]   [Translation Failed]
                    |                    |
                    |                    v
                    |              [Show Error + Retry]
                    |                    |
                    v                    |
            [User Interacts]             |
            - View examples  <-----------+
            - Translate sentences
            - Scroll content
                    |
                    v
            [User Closes]
            - Click X
            - Click backdrop
            - Press Escape
                    |
                    v
                [Closed]
```

**Design Tokens Used**:
- All spacing tokens (`--space-1` through `--space-8`)
- All color tokens (`--primary-*`, `--text-*`, `--border-*`, `--error-*`)
- All shadow tokens (`--shadow-*`)
- `--focus-ring` for accessibility

---

## Component 5: Loading State Components

**Purpose**: Skeleton screens prevent layout shifts during content loading

### Skeleton Screen Specifications

```css
/* Generic skeleton element */
.skeleton {
  background-color: var(--border-color); /* #e5e7eb */
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
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.6) 50%,
    transparent 100%
  );
  animation: shimmer 1.5s infinite;
}

/* Specific skeleton shapes */
.skeleton-title {
  height: 36px;
  width: 60%;
  margin-bottom: var(--space-4);
}

.skeleton-paragraph {
  height: 16px;
  margin-bottom: var(--space-2);
}

.skeleton-paragraph:last-child {
  width: 80%;
}

/* Loading text (bilingual) */
.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-6);
  color: var(--text-secondary);
}

.loading-spinner {
  width: 24px;
  height: 24px;
  border: 3px solid var(--border-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

**Layout Shift Prevention**:
- Reserve space with `min-height` matching expected content
- Use CSS Grid with fixed row heights for predictable layout
- Load skeletons immediately (no delay)
- Fade in content (opacity transition) to avoid jarring replacement

---

## Responsive Behavior Summary

### Breakpoint Overview

| Name | Min Width | Container | Grid Cols | Touch Targets | Font Size | Tab Labels |
|------|-----------|-----------|-----------|---------------|-----------|------------|
| **xs** | 0px | 100% (20px margins) | 1 | 44x44px | 16px | 简化 (简体中文 only) |
| **sm** | 375px | 100% (20px margins) | 1 | 44x44px | 16px | 简化 (Chinese only) |
| **md** | 768px | 720px max | 2-3 | 44x44px | 16px | 双语 (Bilingual) |
| **lg** | 1024px | 960px max | 4 | 44x44px | 17px | 双语 (Bilingual) |
| **xl** | 1280px | 1280px max | 5 | 44x44px | 17px | 双语 (Bilingual) |
| **xxl** | 1440px+ | 1400px max | 5-6 | 44x44px | 17px | 双语 (Bilingual) |

### Component Adaptations

**Word Card Grid**:
- Mobile (xs/sm): 1 column, vertical stack
- Tablet (md): 2-3 columns using `auto-fill`
- Desktop (lg): 4 columns, fixed grid
- Large (xl): 5 columns, fixed grid
- XL (xxl): 5-6 columns using `auto-fill` with 220px min-width

**Detail Modal**:
- Mobile: 90% width with 5% margins
- Tablet: 80% width, max 600px
- Desktop: 60% width, max 700px
- Large: 60% width, max 800px

**Tab Navigation**:
- Mobile: Chinese label + count only ("单词 (152)")
- Desktop: Bilingual labels ("单词 (152) / Words")

---

## Design Token Reference

### Complete Token Set (From Feature 003)

```css
:root {
  /* Spacing (8px grid) */
  --space-0: 0;
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;

  /* Colors - Primary */
  --primary-color: #2563eb;
  --primary-hover: #1d4ed8;
  --primary-active: #1e40af;

  /* Colors - Text */
  --text-primary: #1f2937;
  --text-secondary: #6b7280;

  /* Colors - UI */
  --border-color: #e5e7eb;
  --background-hover: #f3f4f6;
  --focus-ring: #2563eb;

  /* Colors - Feedback */
  --error-text: #dc2626;
  --error-background: #fef2f2;
  --success-text: #059669;
  --success-background: #d1fae5;

  /* Shadows */
  --shadow-base: 0 1px 3px rgba(0,0,0,0.1);
  --shadow-medium: 0 4px 6px rgba(0,0,0,0.1);
  --shadow-large: 0 10px 15px rgba(0,0,0,0.1);
  --focus-ring-shadow: 0 0 0 2px rgba(37,99,235,0.5);
}
```

---

## Accessibility Specifications

### Keyboard Navigation Map

```
Tab Order (Desktop):
1. Tab Button (Words)
2. Tab Button (Phrasal Verbs)
3. Filter Controls
4. Search Input
5. Word Card 1
6. Word Card 2
7. ...
8. Word Card N

Modal Open (Word Card focused):
1. Modal Close Button
2. Example Translate Button 1
3. Example Translate Button 2
4. ...

Keyboard Shortcuts:
- Tab: Next element
- Shift+Tab: Previous element
- Enter/Space: Activate button/card
- Escape: Close modal
- Arrow Left/Right: Switch tabs (when tab focused)
```

### ARIA Attributes

```html
<!-- Tab Navigation -->
<div role="tablist" aria-label="Vocabulary Categories">
  <button role="tab" aria-selected="true" aria-controls="words-panel">Words</button>
</div>
<div role="tabpanel" id="words-panel" aria-labelledby="words-tab">...</div>

<!-- Modal -->
<div role="dialog" aria-modal="true" aria-labelledby="modal-title">
  <h2 id="modal-title">Word Details</h2>
</div>

<!-- Interactive Cards -->
<div role="button" tabindex="0" aria-label="View details for 'example'">...</div>
```

### Focus Management

- **Focus Trap**: Modal traps focus (Tab cycles within modal)
- **Return Focus**: Closing modal returns focus to triggering element
- **Visible Indicators**: All focusable elements have 2px blue outline
- **Skip Links**: Not needed (simple single-page layout)

---

## State Persistence

### LocalStorage Schema

```javascript
{
  "activeTab": "words" | "phrases",
  "activeFilters": {
    "level": ["B1", "B2"] | null,
    "type": "all" | "verbs" | "nouns"
  },
  "searchQuery": "make" | "",
  "lastVisited": "2025-11-04T12:00:00Z"
}
```

### State Synchronization

**Tab Switch Behavior**:
1. User switches from "Words" to "Phrasal Verbs" tab
2. Save active tab to localStorage
3. Apply existing filters to new tab content
4. Preserve search query across tabs
5. Update tab counts dynamically (e.g., "短语动词 (37)" → "短语动词 (12)" after B2 filter)

---

## Data Model Complete

**Status**: ✅ All UI components defined
**Next Phase**: Generate quickstart.md (developer implementation guide)
**Ready For**: Implementation task breakdown via `/speckit.tasks`
