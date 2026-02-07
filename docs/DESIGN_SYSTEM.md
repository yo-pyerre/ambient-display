# Design System

This document defines the visual design language for the Raspberry Pi Art Display frontend. All new UI components should follow these guidelines to maintain a cohesive aesthetic.

## Design Philosophy: "Soft Mono"

The interface follows a **soft monochromatic** aesthetic characterized by:
- Dark, near-black backgrounds with warm off-white text
- Monospace typography throughout
- Subtle transparency and blur effects
- Fluid, viewport-responsive sizing
- Minimal but purposeful animations
- Grid-based layouts with hairline separators

This design creates a refined, technical aesthetic suitable for a wall-mounted display that's meant to recede into the background while remaining readable and elegant.

## Color Palette

### Core Colors

```css
/* Backgrounds */
--ds-bg-primary: #111113;              /* Near-black charcoal - primary backgrounds */
--ds-bg-overlay: rgba(0, 0, 0, 0.55);  /* Semi-transparent black with blur */

/* Text */
--ds-text-primary: #e8e6e3;                    /* Warm off-white - primary text */
--ds-text-secondary: rgba(232, 230, 227, 0.35); /* 35% opacity - secondary text */
--ds-text-tertiary: rgba(232, 230, 227, 0.18);  /* 18% opacity - labels, hints */

/* Borders & Dividers */
--ds-border: rgba(232, 230, 227, 0.07);  /* 7% opacity - subtle borders */

/* Accents */
--ds-highlight: rgba(255, 255, 255, 0.025);  /* 2.5% opacity - subtle highlights */
--ds-highlight-white: rgba(255, 255, 255, 0.85); /* 85% opacity - white text on dark translucent */
```

### Usage Guidelines

| Color | Use For | Example |
|-------|---------|---------|
| `#111113` | Main backgrounds, card backgrounds | Morning overlay background |
| `#e8e6e3` | Primary content (time, temperature, values) | Clock display, temperature values |
| `rgba(232, 230, 227, 0.35)` | Secondary content (descriptions, conditions) | Weather description, date |
| `rgba(232, 230, 227, 0.18)` | Labels, hints, low-emphasis text | Grid labels ("humidity", "wind") |
| `rgba(232, 230, 227, 0.07)` | Borders, dividers, cell gaps | Grid cell separators |
| `rgba(255, 255, 255, 0.025)` | Subtle background highlights | "Today" cell highlight |

**Note**: Always use the same base color (`232, 230, 227`) with varying opacity rather than different gray values. This maintains color harmony.

## Typography

### Font Stack

```css
font-family: "SF Mono", "Cascadia Code", "Fira Code", "Consolas", "Monaco", monospace;
```

This monospace stack prioritizes modern code fonts with excellent readability. The fallback to system monospace ensures functionality across all platforms.

### Sizing Strategy

Use `clamp()` for all font sizes to create fluid, responsive typography:

```css
/* Pattern: clamp(min, preferred, max) */
font-size: clamp(12px, 1.5vw, 28px);
```

**Common size ranges:**
- **Large headings** (clock): `clamp(3rem, 10vw, 12rem)`
- **Medium headings** (temperature): `clamp(26px, 4vw, 72px)`
- **Body text**: `clamp(12px, 1.5vw, 28px)`
- **Small text** (labels): `clamp(8px, 1vw, 20px)`
- **Tiny text**: `clamp(10px, 1.2vw, 24px)`

### Text Treatment

```css
/* Labels should be lowercase with letter spacing */
text-transform: lowercase;
letter-spacing: 0.06em; /* or 0.08em for very small text */

/* Numeric displays should use tabular figures */
font-variant-numeric: tabular-nums;

/* Large headings get negative letter spacing */
letter-spacing: -0.04em; /* for very large text */
letter-spacing: -0.03em; /* for large text */
```

### Examples

```css
/* Clock display */
.morning-clock {
    font-size: clamp(3rem, 10vw, 12rem);
    font-weight: 400;
    color: #e8e6e3;
    letter-spacing: -0.04em;
    line-height: 1;
    font-variant-numeric: tabular-nums;
}

/* Grid labels */
.detail-label {
    font-size: clamp(8px, 1vw, 20px);
    color: rgba(232, 230, 227, 0.18);
    text-transform: lowercase;
    letter-spacing: 0.08em;
}
```

## Layout Patterns

### Grid-Based Layouts

Use CSS Grid with 1px gaps for separated cell layouts:

```css
.grid-container {
    display: grid;
    grid-template-columns: repeat(4, 1fr); /* or any column count */
    gap: 1px;
    background: rgba(232, 230, 227, 0.07); /* Gap color */
    border-radius: clamp(6px, 0.8vw, 16px);
    overflow: hidden;
}

.grid-cell {
    background: #111113; /* Cell background */
    padding: clamp(12px, 2vw, 36px);
}
```

**Why this pattern?**: The 1px gap creates subtle cell separation without heavy borders. The background color of the container shows through the gaps.

### Border Radius

Always use responsive border radius:

```css
border-radius: clamp(6px, 0.8vw, 16px);
```

Apply to: cards, grids, buttons, panels

### Spacing & Padding

Use `clamp()` for all spacing to maintain proportions:

```css
/* Padding */
padding: clamp(12px, 2vw, 36px);
padding: 0 clamp(20px, 3vw, 60px); /* Horizontal only */

/* Margins */
margin-bottom: clamp(16px, 2.5vh, 40px);
margin-bottom: clamp(32px, 6vh, 96px); /* Larger spacing */

/* Gaps */
gap: clamp(12px, 2vw, 36px);
gap: clamp(4px, 0.6vw, 14px); /* Smaller gaps */
```

## Visual Effects

### Backdrop Blur

For translucent overlays over content:

```css
.translucent-bar {
    background: rgba(0, 0, 0, 0.55);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px); /* Safari support */
}
```

### Transitions

Standard transition for state changes:

```css
transition: opacity 0.4s ease, transform 0.4s ease;
transition: opacity 0.5s ease; /* Longer for major state changes */
```

### Entrance Animations

Components should fade in with subtle upward motion:

```css
/* Initial state */
.component {
    opacity: 0;
    transform: translateY(10px);
    transition: opacity 0.4s ease 0.2s, transform 0.4s ease 0.2s; /* 0.2s delay */
}

/* Active state */
.component.visible {
    opacity: 1;
    transform: translateY(0);
}
```

### Hover States

Minimal hover effects for kiosk mode (most interactions are keyboard/remote):

```css
.interactive-element:hover {
    background-color: rgba(255, 255, 255, 0.05);
    transition: background-color 0.2s ease;
}
```

## Component Patterns

### Full-Screen Overlay

```css
.overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: #111113;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: opacity 0.5s ease;
    z-index: 100;
}

.overlay.hidden {
    opacity: 0;
    pointer-events: none;
}
```

### Bottom Bar

```css
.bottom-bar {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: clamp(36px, 5vh, 80px);
    background: rgba(0, 0, 0, 0.55);
    backdrop-filter: blur(24px);
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    display: flex;
    align-items: center;
    padding: 0 clamp(16px, 2.5vw, 48px);
    gap: clamp(16px, 2.5vw, 48px);
}
```

### Content Card

```css
.card {
    width: 100%;
    max-width: clamp(400px, 55vw, 1200px);
    padding: 0 clamp(20px, 3vw, 60px);
    opacity: 0;
    transform: translateY(10px);
    transition: opacity 0.4s ease 0.2s, transform 0.4s ease 0.2s;
}
```

### Data Grid

```css
.data-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: rgba(232, 230, 227, 0.07);
    margin-bottom: clamp(20px, 3vh, 52px);
    border-radius: clamp(6px, 0.8vw, 16px);
    overflow: hidden;
}

.data-cell {
    background: #111113;
    padding: clamp(12px, 2vw, 36px);
    text-align: center;
}

.data-label {
    font-size: clamp(8px, 1vw, 20px);
    color: rgba(232, 230, 227, 0.18);
    text-transform: lowercase;
    letter-spacing: 0.08em;
    margin-bottom: clamp(4px, 0.6vh, 12px);
}

.data-value {
    font-size: clamp(13px, 1.6vw, 32px);
    color: #e8e6e3;
}
```

## Responsive Design

### Mobile Breakpoint

```css
@media (max-width: 768px) {
    /* Reduce grid columns */
    .data-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    /* Stack flex layouts */
    .flex-container {
        flex-direction: column;
    }

    /* Use fixed sizing where clamp() doesn't work well */
    .small-text {
        font-size: 12px;
    }
}
```

## Do's and Don'ts

### ✅ Do

- Use the monospace font stack for all text
- Apply `clamp()` for fluid sizing of fonts, padding, and spacing
- Use the established color palette with opacity variations
- Create 1px grid gaps with background color showing through
- Apply subtle entrance animations (opacity + translateY)
- Use backdrop blur for translucent overlays
- Keep letter-spacing tight for large text, loose for small labels
- Use tabular numbers for time and numeric displays

### ❌ Don't

- Use sans-serif or serif fonts
- Use fixed pixel sizes (except as min/max in clamp)
- Introduce new colors outside the `#e8e6e3` / `#111113` palette
- Create thick borders or dividers
- Add excessive animations or transitions
- Use bright colors or high-contrast accent colors
- Mix monospace with other font styles
- Forget `-webkit-backdrop-filter` for Safari support

## Examples from Existing Components

### Morning Display Clock

```css
.morning-clock {
    font-size: clamp(3rem, 10vw, 12rem);
    font-weight: 400;
    color: #e8e6e3;
    letter-spacing: -0.04em;
    line-height: 1;
    font-variant-numeric: tabular-nums;
}
```

**Demonstrates**: Large responsive text, tabular numbers, negative letter spacing

### Weather Bar

```css
.weather-bar {
    background: rgba(0, 0, 0, 0.55);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border-top: 1px solid rgba(255, 255, 255, 0.06);
}
```

**Demonstrates**: Translucent overlay, backdrop blur, subtle border

### Detail Grid

```css
.morning-details {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: rgba(232, 230, 227, 0.07);
    border-radius: clamp(6px, 0.8vw, 16px);
    overflow: hidden;
}
```

**Demonstrates**: Grid with 1px gaps, responsive border radius

## Adding New Components

When creating a new UI component:

1. **Start with structure**: Use the appropriate layout pattern (overlay, bar, card, grid)
2. **Apply typography**: Use the monospace font stack and clamp() sizing
3. **Use the color palette**: Stick to `#111113` and `#e8e6e3` with opacity variations
4. **Add spacing**: Apply consistent clamp()-based padding and margins
5. **Implement effects**: Add backdrop blur if translucent, entrance animation if appropriate
6. **Test responsiveness**: Verify the component scales well from mobile to large screens
7. **Reference existing code**: Look at `frontend/styles.css` lines 352-641 for examples

## CSS Design Tokens

Design tokens are defined in `frontend/styles.css` as CSS custom properties:

```css
:root {
    /* Design System Tokens - "soft mono" aesthetic */
    --ds-bg-primary: #111113;
    --ds-text-primary: #e8e6e3;
    --ds-text-secondary: rgba(232, 230, 227, 0.35);
    --ds-text-tertiary: rgba(232, 230, 227, 0.18);
    --ds-border: rgba(232, 230, 227, 0.07);
    --ds-highlight: rgba(255, 255, 255, 0.025);
    --ds-font-mono: "SF Mono", "Cascadia Code", "Fira Code", "Consolas", "Monaco", monospace;
    --ds-radius: clamp(6px, 0.8vw, 16px);
    --ds-blur: blur(24px);
    --ds-transition: 0.4s ease;
}
```

Use these tokens in new CSS to ensure consistency and make global changes easier.
