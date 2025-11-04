# Data Model: UI/UX Optimization

**Feature**: UI/UX Optimization
**Date**: 2025-11-04
**Phase**: 1 - Design & Contracts

## Overview

This feature is CSS-only and doesn't introduce new data structures or backend entities. However, it does define design system tokens as data that drive the visual presentation layer.

---

## Design System Tokens

Design tokens are the visual design atoms of the UI system - named entities that store visual design attributes. They are implemented as CSS Custom Properties (CSS Variables) but conceptually represent structured data.

### Entity: Design Token

**Purpose**: Named visual design value that can be referenced throughout the CSS
**Storage**: CSS Custom Properties in `:root` selector
**Scope**: Global (available to all styles)

**Attributes**:
- **name** (string): CSS variable name (e.g., `--space-4`, `--font-size-lg`)
- **value** (string): CSS value (e.g., `1rem`, `1.125rem`, `#2563eb`)
- **category** (enum): `spacing` | `typography` | `color` | `shadow` | `breakpoint`
- **description** (string): Human-readable purpose (stored in CSS comment)

**Validation Rules**:
- Names MUST follow kebab-case convention
- Names MUST start with category prefix (`--space-`, `--font-`, `--color-`, etc.)
- Values MUST be valid CSS values for their property type
- All tokens MUST have inline documentation (comment)

---

## Token Categories

### 1. Spacing Tokens

**Purpose**: Define consistent whitespace scale using 8px grid system

**Schema**:
```css
:root {
  --space-0: 0;           /* No spacing */
  --space-1: 0.25rem;     /* 4px - tight inline spacing */
  --space-2: 0.5rem;      /* 8px - base unit */
  --space-3: 0.75rem;     /* 12px - small gaps */
  --space-4: 1rem;        /* 16px - default spacing */
  --space-5: 1.25rem;     /* 20px - medium gaps */
  --space-6: 1.5rem;      /* 24px - section spacing */
  --space-8: 2rem;        /* 32px - large gaps */
  --space-10: 2.5rem;     /* 40px - major sections */
  --space-12: 3rem;       /* 48px - hero spacing */
}
```

**Usage Guidelines**:
- Card padding: `--space-6` (24px)
- Section margins: `--space-8` to `--space-10`
- Button padding: `--space-3` (vertical) × `--space-6` (horizontal)
- Grid gaps: `--space-4` for card grids, `--space-2` for button groups

---

### 2. Typography Tokens

**Purpose**: Define consistent font sizing, line height, and weight scale

**Font Size Scale**:
```css
:root {
  --font-size-xs: 0.75rem;    /* 12px - captions, labels */
  --font-size-sm: 0.875rem;   /* 14px - secondary text */
  --font-size-base: 1rem;      /* 16px - body text (mobile) */
  --font-size-md: 1.0625rem;   /* 17px - body text (desktop) */
  --font-size-lg: 1.125rem;    /* 18px - large body text */
  --font-size-xl: 1.25rem;     /* 20px - h3 */
  --font-size-2xl: 1.5rem;     /* 24px - h3 */
  --font-size-3xl: 1.875rem;   /* 30px - h2 */
  --font-size-4xl: 2.25rem;    /* 36px - h1 */
}
```

**Line Height Scale**:
```css
:root {
  --line-height-tight: 1.25;    /* Headings */
  --line-height-snug: 1.375;    /* UI elements */
  --line-height-normal: 1.5;    /* Default */
  --line-height-relaxed: 1.625; /* Body text */
  --line-height-loose: 1.75;    /* Long-form content */
}
```

**Font Weight Scale**:
```css
:root {
  --font-weight-normal: 400;    /* Body text */
  --font-weight-medium: 500;    /* Emphasis */
  --font-weight-semibold: 600;  /* Subheadings, UI labels */
  --font-weight-bold: 700;      /* Headings, CTAs */
}
```

---

### 3. Color Tokens

**Purpose**: Define consistent color palette with semantic naming

**Existing Colors** (preserve):
```css
:root {
  --primary-color: #2563eb;      /* Primary blue */
  --primary-hover: #1d4ed8;      /* Darker primary */
  --success-color: #10b981;      /* Green */
  --error-color: #ef4444;        /* Red */
  --text-color: #1f2937;         /* Dark gray */
  --text-secondary: #6b7280;     /* Medium gray */
  --background: #f9fafb;         /* Light gray bg */
  --card-background: #ffffff;    /* White */
  --border-color: #e5e7eb;       /* Light border */
}
```

**New Tokens** (add for state variations):
```css
:root {
  --primary-active: #1e40af;     /* Even darker for active state */
  --text-muted: #9ca3af;         /* Very light gray for disabled */
  --focus-ring: #2563eb;         /* Focus outline color */
  --hover-overlay: rgba(37, 99, 235, 0.1); /* Light blue overlay */
}
```

**Validation**:
- All text-background combinations MUST meet WCAG AA (4.5:1 contrast)
- Focus ring color MUST be visible against all backgrounds
- Hover states MUST be distinguishable from normal state

---

### 4. Shadow Tokens

**Purpose**: Define consistent elevation through shadows

**Existing Shadows** (preserve & extend):
```css
:root {
  --shadow: 0 1px 3px rgba(0, 0, 0, 0.1);           /* Base shadow */
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);        /* Medium elevation */
  --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.1);      /* Large cards */
  --shadow-focus: 0 0 0 3px rgba(37, 99, 235, 0.2); /* Focus ring shadow */
}
```

---

### 5. Breakpoint Tokens

**Purpose**: Define responsive breakpoints for media queries

**Schema**:
```css
:root {
  --breakpoint-sm: 375px;   /* Small mobile */
  --breakpoint-md: 768px;   /* Tablets */
  --breakpoint-lg: 1024px;  /* Desktop */
  --breakpoint-xl: 1280px;  /* Large desktop */
}
```

**Note**: These are defined for documentation but used directly in `@media` queries (CSS variables don't work in media queries currently).

---

## Token Usage Pattern

### Semantic Token Layer

**Purpose**: Abstract primitive tokens into component-specific semantic tokens

**Example - Button Tokens**:
```css
:root {
  /* Primitive references */
  --button-padding-y: var(--space-3);
  --button-padding-x: var(--space-6);
  --button-font-size: var(--font-size-base);
  --button-font-weight: var(--font-weight-semibold);
  --button-border-radius: 0.5rem;
  --button-min-height: 44px; /* Touch target requirement */
}
```

**Example - Card Tokens**:
```css
:root {
  --card-padding: var(--space-6);
  --card-gap: var(--space-4);
  --card-border-radius: 12px;
  --card-shadow: var(--shadow-lg);
}
```

This creates a two-tier system:
1. **Primitive tokens**: Raw values (`--space-4`, `--font-size-base`)
2. **Semantic tokens**: Component-specific references (`--button-padding-x`)

**Benefits**:
- Change all button padding by updating one semantic token
- Maintain consistency across similar components
- Self-documenting token names

---

## Component State Matrix

### Entity: Interactive State

**Purpose**: Define visual appearance for each interaction state

**States**:
- **normal**: Default resting state
- **hover**: Mouse cursor over element (desktop only)
- **active**: Element being pressed/clicked
- **focus**: Element has keyboard focus
- **disabled**: Element is not interactive

**Visual Properties Per State**:
- Background color
- Border color
- Text color
- Shadow elevation
- Transform (subtle movement)
- Cursor style

**State Transition Rules**:
```
normal → hover (on mouse enter)
hover → active (on mouse down)
active → normal (on mouse up)
normal → focus (on keyboard Tab)
focus → normal (on blur)
* → disabled (when disabled attribute present)
```

**Example State Definition** (Button):
```css
.button {
  /* Normal */
  background: var(--primary-color);
  color: white;
  box-shadow: var(--shadow);
  transform: translateY(0);
  transition: all 0.2s ease;
}

.button:hover {
  /* Hover */
  background: var(--primary-hover);
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

.button:active {
  /* Active */
  background: var(--primary-active);
  box-shadow: var(--shadow);
  transform: translateY(0);
}

.button:focus-visible {
  /* Focus */
  outline: 2px solid var(--focus-ring);
  outline-offset: 2px;
}

.button:disabled {
  /* Disabled */
  background: var(--text-muted);
  cursor: not-allowed;
  opacity: 0.6;
  box-shadow: none;
}
```

---

## Responsive Behavior Model

### Entity: Breakpoint Configuration

**Purpose**: Define how layout adapts at each screen size

**Attributes**:
- **breakpoint** (enum): `xs` | `sm` | `md` | `lg` | `xl`
- **min-width** (px): Minimum viewport width for this range
- **container-max-width** (px): Maximum content width
- **grid-columns** (number): Number of columns in card grid
- **spacing-scale** (multiplier): Spacing adjustment factor

**Breakpoint Matrix**:

| Breakpoint | Min Width | Container | Grid Cols | Spacing Adjustment | Font Size |
|------------|-----------|-----------|-----------|-------------------|-----------|
| xs (default) | 0px | 100% | 1 | 1.0x | base |
| sm | 375px | 100% | 1 | 1.0x | base |
| md | 768px | 720px | 2 | 1.1x | base |
| lg | 1024px | 960px | 3 | 1.2x | md (17px) |
| xl | 1280px | 1200px | 3-4 | 1.2x | md (17px) |

**Layout Adaptation Rules**:
1. **Stack to Grid**: Single column (mobile) → multi-column grid (tablet+)
2. **Spacing Increase**: Tighter spacing (mobile) → more generous (desktop)
3. **Font Size Bump**: 16px (mobile) → 17px (desktop) for body text
4. **Touch Target Adjustment**: Always 44px minimum, but desktop can use visual size < 44px with padding

---

## Accessibility Model

### Entity: Accessibility Requirement

**Purpose**: Define testable accessibility criteria per component

**Attributes**:
- **component** (string): Component name (button, card, input, etc.)
- **criteria** (enum): `contrast` | `focus-indicator` | `touch-target` | `keyboard-nav` | `screen-reader`
- **requirement** (string): Specific requirement (e.g., "4.5:1 contrast")
- **test-method** (enum): `automated` | `manual` | `visual-inspection`
- **pass-threshold** (string): Success criteria (e.g., "100%", "zero violations")

**Accessibility Matrix**:

| Component | Criteria | Requirement | Test Method | Pass Threshold |
|-----------|----------|-------------|-------------|----------------|
| All text | Contrast | 4.5:1 (normal), 3:1 (large) | Automated | 100% pass |
| All interactive | Focus indicator | Visible outline, 2px min | Visual inspection | 100% visible |
| Buttons | Touch target | 44x44px minimum | Measurement | 100% compliant |
| Forms | Labels | All inputs have labels | Automated | Zero violations |
| Navigation | Keyboard | All features accessible via Tab | Manual | 100% reachable |

---

## No Backend Data Changes

**Important**: This feature does NOT modify:
- Database schema
- API responses
- Data processing logic
- Vocabulary analysis algorithms
- File uploads/storage

All changes are purely presentational (CSS) with no impact on:
- `src/vocab_analyzer/core/` modules
- `src/vocab_analyzer/web/app.py` or `routes.py`
- Any Python code except potentially CSS file serving (no change expected)

---

## Token Documentation Standard

**Requirement**: All tokens MUST include inline documentation

**Format**:
```css
/* Token Category: Spacing */
:root {
  --space-4: 1rem; /* 16px - Default spacing for most UI elements */
  --space-6: 1.5rem; /* 24px - Card padding, section spacing */
}

/* Usage example:
.card {
  padding: var(--space-6);
  gap: var(--space-4);
}
*/
```

**Documentation Fields**:
1. **Pixel equivalent**: Always show px value in comment
2. **Usage guideline**: When to use this token
3. **Example**: Show real usage in comment block

---

## Summary

This data model defines:
- **Design Tokens**: 40+ tokens across 5 categories (spacing, typography, color, shadow, breakpoint)
- **State Model**: 5 interaction states with transition rules
- **Responsive Model**: 5 breakpoints with layout adaptation rules
- **Accessibility Model**: 5 criteria categories with test methods

All tokens are implemented as CSS Custom Properties, making them:
- Easily maintainable (single source of truth)
- Runtime flexible (can be overridden via JavaScript if needed later)
- Self-documenting (inline comments required)
- Testable (can extract and validate programmatically)

**No database or API changes required** - this is a pure frontend visual enhancement.
