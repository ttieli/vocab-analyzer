# Research: UI/UX Optimization

**Feature**: UI/UX Optimization
**Date**: 2025-11-04
**Phase**: 0 - Outline & Research

## Research Objectives

This document resolves technical unknowns and establishes best practices for implementing the UI/UX optimization feature.

---

## 1. CSS Architecture & Design Tokens

### Decision: Use CSS Custom Properties (CSS Variables) for Design System

**Rationale**:
- The existing codebase already uses CSS variables (`:root` selectors) - maintaining consistency
- CSS custom properties provide runtime theme flexibility without rebuild
- Better browser support (IE11 not a target based on modern browser assumption)
- Enables future dark mode / theme switching without architectural changes

**Implementation Approach**:
- Extend existing `:root` variables with spacing scale, typography scale
- Create semantic token layers: primitive tokens → semantic tokens → component tokens
- Example structure:
  ```css
  :root {
    /* Spacing primitives */
    --space-1: 0.25rem;  /* 4px */
    --space-2: 0.5rem;   /* 8px */
    --space-3: 0.75rem;  /* 12px */
    --space-4: 1rem;     /* 16px */
    --space-6: 1.5rem;   /* 24px */
    --space-8: 2rem;     /* 32px */

    /* Typography scale */
    --font-size-sm: 0.875rem;   /* 14px */
    --font-size-base: 1rem;      /* 16px */
    --font-size-lg: 1.125rem;    /* 18px */
    --font-size-xl: 1.25rem;     /* 20px */
    --font-size-2xl: 1.5rem;     /* 24px */
    --font-size-3xl: 1.875rem;   /* 30px */

    /* Line heights */
    --line-height-tight: 1.25;
    --line-height-normal: 1.5;
    --line-height-relaxed: 1.75;
  }
  ```

**Alternatives Considered**:
- **Sass variables**: Requires build step, not runtime flexible
- **Tailwind CSS**: Too large dependency for incremental improvements
- **Inline styles**: Poor maintainability, no cascade benefits

**References**:
- MDN: CSS Custom Properties for Cascading Variables
- Material Design: Design Tokens specification
- Existing project: `src/vocab_analyzer/web/static/styles.css` lines 9-21

---

## 2. Responsive Design Strategy

### Decision: Mobile-First CSS with Progressive Enhancement

**Rationale**:
- Aligns with spec requirement for 4 breakpoints (small mobile → desktop)
- Forces consideration of mobile constraints first (bandwidth, screen size)
- Reduces CSS size (desktop overrides vs. mobile overrides)
- Current CSS doesn't have extensive responsive rules - fresh start opportunity

**Breakpoint Strategy**:
```css
/* Mobile-first: base styles for < 375px */
/* No media query - default styles */

/* Small mobile: 375px+ */
@media (min-width: 375px) {
  /* Slightly larger touch targets, more spacing */
}

/* Mobile: 768px+ (tablets) */
@media (min-width: 768px) {
  /* Multi-column layouts, larger fonts */
}

/* Tablet: 1024px+ */
@media (min-width: 1024px) {
  /* Desktop layouts, hover effects prominent */
}

/* Desktop: 1280px+ */
@media (min-width: 1280px) {
  /* Maximum content width, optional sidebars */
}
```

**Container Query Alternative** (Deferred to future):
- Modern approach but requires more complex refactoring
- Browser support not yet universal (Safari 16+ only)
- Not needed for this phase - layout simple enough for viewport queries

**Alternatives Considered**:
- **Desktop-first**: Requires more override CSS for mobile
- **Fixed breakpoints only**: Less flexible, can leave gaps
- **Fluid typography/spacing**: Adds complexity with clamp() functions

**References**:
- Existing project: `src/vocab_analyzer/web/static/styles.css` (currently desktop-focused)
- Bootstrap breakpoints: Industry-standard reference
- Tailwind CSS breakpoints: Modern defaults

---

## 3. Accessibility (WCAG AA Compliance)

### Decision: Automated Testing + Manual Audit for Contrast & Focus

**Rationale**:
- Spec requires WCAG AA (4.5:1 contrast for normal text, 3:1 for large)
- Existing colors may not meet standards - audit required
- Focus indicators currently missing from UI

**Implementation Tools**:
1. **Contrast Checking**:
   - Use WebAIM Contrast Checker or browser devtools
   - Test all text-background combinations
   - Document passing colors in design token comments

2. **Focus Indicators**:
   - Add `:focus-visible` pseudo-class (modern browsers)
   - Fallback `:focus` for older browsers
   - Use outline with offset for clarity:
     ```css
     button:focus-visible {
       outline: 2px solid var(--primary-color);
       outline-offset: 2px;
     }
     ```

3. **Automated Testing**:
   - Lighthouse accessibility audit (built into Chrome DevTools)
   - axe DevTools browser extension for detailed reports
   - Run before/after comparison

**Touch Target Sizing**:
- Minimum 44x44px per spec requirement (FR-013)
- Apply to all interactive elements (buttons, links, form controls)
- Use padding to expand hit area without visual size change

**Alternatives Considered**:
- **WCAG AAA**: Higher standard but not required; deferred
- **Pa11y/Cypress axe plugin**: CI integration - good but overkill for this phase

**References**:
- WCAG 2.1 Level AA Guidelines
- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/
- Apple Human Interface Guidelines (Touch Target Sizes)

---

## 4. Typography Best Practices

### Decision: System Font Stack with Increased Base Size

**Rationale**:
- Existing font stack is good (system fonts, no external dependencies)
- Current base font size: implicit 16px (browser default)
- Increase to 17-18px for better readability per spec

**Typography Decisions**:
1. **Base Font Size**:
   - Desktop: 17px (1.0625rem)
   - Mobile: 16px (preserve browser default for bandwidth)

2. **Heading Scale**:
   - h1: 2.25rem (36px) - currently 2.5rem, reduce slightly
   - h2: 1.875rem (30px) - add distinct size
   - h3: 1.5rem (24px) - add distinct size
   - Create clear hierarchy (1.33 ratio between levels)

3. **Line Height**:
   - Body text: 1.6 (currently 1.6 - keep)
   - Headings: 1.2-1.3 (tighter for visual impact)
   - UI elements: 1.5 (balance density with readability)

4. **Font Weights**:
   - Regular: 400 (body text)
   - Medium: 500 (emphasis)
   - Semi-bold: 600 (subheadings, UI labels)
   - Bold: 700 (headings, primary actions)

**Alternatives Considered**:
- **Web fonts (Google Fonts)**: Adds network dependency, against constitution simplicity
- **Variable fonts**: Modern but increases complexity
- **Rem-only sizing**: Better but requires base font-size declaration

**References**:
- Existing project: `src/vocab_analyzer/web/static/styles.css` lines 24-54
- Practical Typography by Matthew Butterick
- Material Design Typography

---

## 5. Layout & Spacing System

### Decision: 8px Grid System with Consistent Spacing Scale

**Rationale**:
- Most design systems use 4px or 8px base units for visual rhythm
- 8px better for accessibility (larger touch targets)
- Current CSS has inconsistent spacing - standardize on scale

**Spacing Scale** (8px base):
```
--space-0: 0
--space-1: 0.25rem  (4px)  - tight inline spacing
--space-2: 0.5rem   (8px)  - base unit
--space-3: 0.75rem  (12px) - small gaps
--space-4: 1rem     (16px) - default spacing
--space-5: 1.25rem  (20px) - medium gaps
--space-6: 1.5rem   (24px) - section spacing
--space-8: 2rem     (32px) - large gaps
--space-10: 2.5rem  (40px) - major sections
--space-12: 3rem    (48px) - hero spacing
```

**Application Guidelines**:
- **Card padding**: `var(--space-6)` (24px) - currently 2rem (32px), reduce slightly for more space efficiency
- **Section margins**: `var(--space-8)` or `var(--space-10)` between major sections
- **Button padding**: `var(--space-3)` vertical, `var(--space-6)` horizontal (12px x 24px)
- **Grid gaps**: `var(--space-4)` for card grids, `var(--space-2)` for button groups

**Alternatives Considered**:
- **4px base**: Finer control but harder to maintain consistency
- **Golden ratio spacing**: Too complex for this project scale
- **Tailwind spacing**: Good reference but we're not using Tailwind

**References**:
- Material Design: 8dp grid system
- Apple Human Interface Guidelines: 8pt spacing
- Existing project: Currently ad-hoc spacing (1rem, 2rem, 0.5rem mixed)

---

## 6. Interactive State Design

### Decision: Three-State Visual Feedback (Normal, Hover, Active/Focus)

**Rationale**:
- Spec requires "pronounced hover effects" (FR-008) and "visible focus states" (FR-009)
- Current CSS has basic hover but no focus indicators
- Need consistent pattern across all interactive elements

**State Definitions**:

1. **Normal State**:
   - Base colors and styles
   - Subtle shadow or border for affordance

2. **Hover State** (mouse users):
   - Color shift (darken 10-15% or add overlay)
   - Shadow increase (elevation effect)
   - Cursor change (`cursor: pointer`)
   - Example:
     ```css
     button:hover {
       background: var(--primary-hover);
       box-shadow: 0 4px 6px rgba(0,0,0,0.15);
       transform: translateY(-1px);
     }
     ```

3. **Active/Pressed State**:
   - Deeper color shift
   - Reduced shadow (pressed effect)
   - Example:
     ```css
     button:active {
       transform: translateY(0);
       box-shadow: 0 1px 2px rgba(0,0,0,0.1);
     }
     ```

4. **Focus State** (keyboard users):
   - Distinct outline (not just border color change)
   - Use `:focus-visible` to avoid hover + focus conflict
   - Example:
     ```css
     button:focus-visible {
       outline: 2px solid var(--primary-color);
       outline-offset: 2px;
     }
     ```

**Disabled State**:
- Reduced opacity (0.5-0.6)
- Cursor: not-allowed
- No hover/active states

**Alternatives Considered**:
- **Four-state with :hover:active**: Too complex, diminishing returns
- **Animated transitions**: Nice-to-have but spec excludes animations (out of scope)
- **Ripple effects**: Material Design pattern but adds complexity

**References**:
- Existing project: Basic hover on `.file-label:hover` (lines 92-95)
- Material Design: State layers
- Bootstrap: Interactive states reference

---

## 7. CSS Organization Strategy

### Decision: Utility-Last with Component-Based Organization

**Rationale**:
- Existing CSS is already component-organized (file upload, progress, results)
- Utility-last approach: components first, utilities for overrides
- Avoid utility-first (Tailwind) complexity for incremental changes

**CSS File Structure** (single file, sections):
```css
/* 1. Reset & Base */
/* 2. Design Tokens (CSS Variables) */
/* 3. Typography */
/* 4. Layout Utilities (spacing, grid) */
/* 5. Components (upload, progress, cards, filters, etc.) */
/* 6. Responsive Overrides (mobile-first media queries) */
/* 7. Print Styles (optional) */
```

**Naming Convention**:
- **BEM-lite**: Block names only, avoid excessive nesting
- Example: `.card`, `.card-title`, `.filter-button`, `.word-item`
- **Utility classes**: `.mt-4`, `.hidden`, `.text-center` (minimal, only common patterns)

**Alternatives Considered**:
- **OOCSS**: Too abstract for simple UI
- **Atomic CSS**: Against simplicity principle
- **CSS Modules**: Requires build step, overkill for single-page app

**References**:
- Existing project: Single `styles.css` file (good, maintain)
- CUBE CSS methodology: Composition > Utility > Block > Exception

---

## 8. Testing & Validation Strategy

### Decision: Manual Testing with Automated Accessibility Checks

**Rationale**:
- No automated UI testing framework in project (per constitution, keep simple)
- Manual testing with checklist sufficient for UI changes
- Automated accessibility checks using browser tools

**Testing Approach**:

1. **Visual Regression** (Manual):
   - Before/after screenshots at each breakpoint
   - Test in Chrome, Firefox, Safari (Edge optional - Chromium-based)
   - Checklist in tasks.md for each user story

2. **Responsive Testing**:
   - Browser DevTools device emulation
   - Test actual devices if available (phone, tablet)
   - Breakpoints: 360px, 768px, 1024px, 1440px

3. **Accessibility Audit**:
   - Lighthouse accessibility score (target: 100)
   - axe DevTools scan (0 violations target)
   - Keyboard navigation manual test (tab through all interactive elements)
   - Screen reader spot-check (VoiceOver/NVDA) - optional, best effort

4. **Contrast Validation**:
   - WebAIM Contrast Checker for all text-background pairs
   - Document passing combinations in design tokens

5. **Performance**:
   - Lighthouse performance score (should remain >90)
   - CSS file size (<100KB uncompressed - currently ~15KB, plenty of room)

**Acceptance Criteria Per User Story**:
- Each user story in spec has specific acceptance scenarios
- Convert to manual test cases in tasks.md
- Pass/fail for each scenario before marking complete

**Alternatives Considered**:
- **Percy/Chromatic**: Visual regression tools - overkill, adds CI complexity
- **Cypress/Playwright**: UI testing frameworks - against simplicity
- **WebPageTest**: Performance monitoring - not needed for CSS-only changes

**References**:
- Spec success criteria (SC-001 through SC-008)
- Existing project: No automated UI tests (manual testing acceptable)

---

## 9. Performance Considerations

### Decision: CSS-Only Changes, No JavaScript Performance Impact

**Rationale**:
- All changes are CSS-only (no new JavaScript)
- Modern CSS features (custom properties, flexbox, grid) are performant
- No animations or transitions in scope (per spec out-of-scope)

**Performance Metrics** (from spec success criteria):
- **No impact on existing metrics**: Analysis time unchanged
- **CSS file size**: Keep under 100KB (currently ~15KB, adding ~5-10KB for improvements)
- **Render blocking**: Single CSS file, no @import (good)
- **Browser compatibility**: Modern browsers only (no IE11 polyfills needed)

**Optimizations**:
- Use logical properties where possible (`inline-start` vs `left` for RTL future-proofing)
- Avoid expensive selectors (deep nesting, universal selectors in scope)
- Group media queries at end of file (better compression)

**No Changes Needed**:
- No lazy loading (single CSS file, ~20KB total acceptable)
- No critical CSS extraction (small file, fast enough)
- No CSS-in-JS (against constitution, adds complexity)

**Alternatives Considered**:
- **PostCSS/Autoprefixer**: Build complexity not justified
- **CSS minification**: Can add later, not critical at this scale
- **CSS Grid polyfills**: Not needed (modern browsers only)

**References**:
- Existing project: Single CSS file, no build step (good)
- Web.dev: Optimize CSS

---

## Summary of Research Decisions

| Area | Decision | Rationale |
|------|----------|-----------|
| **CSS Architecture** | CSS Custom Properties (CSS Variables) | Already in use, runtime flexible, no build step |
| **Responsive Strategy** | Mobile-first with 4 breakpoints | Aligns with spec, smaller CSS, progressive enhancement |
| **Accessibility** | WCAG AA + automated testing | Meets spec requirement, automated tools available |
| **Typography** | Increased base size (17px), system fonts | Better readability, no external dependencies |
| **Spacing System** | 8px grid with consistent scale | Visual rhythm, accessibility-friendly sizes |
| **Interactive States** | 3-state feedback (hover, active, focus) | Meets spec requirements, accessible |
| **CSS Organization** | Component-based, single file | Matches existing structure, simple to maintain |
| **Testing** | Manual with automated a11y checks | No UI testing framework, sufficient for CSS changes |
| **Performance** | CSS-only, no JS impact | Changes don't affect analysis performance |

---

## Next Steps (Phase 1)

With research complete, proceed to:
1. **Data Model**: Define design token structure (spacing, typography, colors)
2. **Contracts**: No API contracts needed (CSS-only changes)
3. **Quickstart**: Update with CSS modification guidelines
4. **Implementation**: Begin with Phase 2 task breakdown
