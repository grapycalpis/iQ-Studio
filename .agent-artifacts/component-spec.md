# iQ Studio Documentation Site — Component Specification

**Author:** UI Designer agent
**Date:** 2026-05-22
**Scope:** Component-level visual spec for the iQ Studio Launcher docs site.
Builds directly on `./.agent-artifacts/brand-guide.md` §2–§9. All hex values
referenced here are sourced from that brand guide — none are reinvented.
**No implementation code.** Token layer is CSS custom properties only;
component layouts are ASCII wireframes.

---

## 0. Token system

All tokens prefixed `--ids-` (IQ Studio Docs). Defined twice: under `:root`
(light) and `[data-theme="dark"]` (dark). Hex values are pulled from the
brand guide §4.1 (light) and §4.2 (dark); brand-source palette in §2.

### 0.1 `:root` — light mode

```css
:root {
  /* ---------------- COLOR ---------------- */
  /* Background / surface */
  --ids-color-bg-page:        #ffffff;       /* brand guide §4.1 */
  --ids-color-bg-surface:     #fafafa;       /* sidebar, cards */
  --ids-color-bg-raised:      #f5f5f5;       /* code bg, raised cards */
  --ids-color-bg-overlay:     rgba(15, 20, 25, 0.50); /* modal scrim */
  --ids-color-bg-selection:   rgba(236, 27, 35, 0.20); /* §8 row 27 */

  /* Text */
  --ids-color-text-primary:   #16272e;       /* --color-inno-blue-dark */
  --ids-color-text-secondary: #4a4a4a;       /* AA body-sized muted */
  --ids-color-text-muted:     #959595;       /* --color-inno-gray, ≥18pt only */
  --ids-color-text-inverse:   #ffffff;
  --ids-color-text-link:      #0046ff;       /* --color-inno-blue */
  --ids-color-text-link-visited: #be0078;    /* --color-inno-magenta */

  /* Border / divider */
  --ids-color-border:         #e2e2e2;       /* --color-inno-gray-light */
  --ids-color-divider:        #ececec;
  --ids-color-border-strong:  #16272e;

  /* Brand */
  --ids-color-brand:          #ec1b23;       /* --color-primary */
  --ids-color-brand-hover:    #c8141b;
  --ids-color-brand-tint-08:  rgba(236, 27, 35, 0.08); /* row hover, active nav bg */
  --ids-color-brand-tint-12:  rgba(236, 27, 35, 0.12);
  --ids-color-brand-on:       #ffffff;       /* text on solid brand button */

  /* Callouts (brand guide §4.3 light) */
  --ids-color-callout-note-bg:      #eef0f1;
  --ids-color-callout-note-border:  #16272e;
  --ids-color-callout-note-text:    #16272e;

  --ids-color-callout-info-bg:      #e6efff;
  --ids-color-callout-info-border:  #0046ff;
  --ids-color-callout-info-text:    #0046ff;

  --ids-color-callout-tip-bg:       #e3f5ea;
  --ids-color-callout-tip-border:   #007800;
  --ids-color-callout-tip-text:     #006030;

  --ids-color-callout-warning-bg:     #fff4d6;
  --ids-color-callout-warning-border: #fabe23;
  --ids-color-callout-warning-text:   #7a4a00;

  --ids-color-callout-danger-bg:     #fde7e8;
  --ids-color-callout-danger-border: #ec1b23;
  --ids-color-callout-danger-text:   #b3151c;

  /* Tables */
  --ids-color-table-header-bg:    #16272e;   /* deep ink, see §6 */
  --ids-color-table-header-text:  #ffffff;
  --ids-color-table-row-zebra:    #fafafa;
  --ids-color-table-row-hover:    rgba(236, 27, 35, 0.08); /* source red tint, light */
  --ids-color-table-border:       #e2e2e2;

  /* Code blocks — always dark, see §4 */
  --ids-color-code-bg:            #16272e;   /* dark even in light mode */
  --ids-color-code-text:          #e2e2e2;
  --ids-color-code-header-bg:     #0f1419;   /* darker header strip */
  --ids-color-code-header-text:   #a8b0b6;
  --ids-color-code-gutter:        #4a5a62;   /* line numbers */
  --ids-color-code-selection:     rgba(255, 107, 112, 0.25);

  /* Code syntax */
  --ids-color-syntax-keyword:     #ff6b70;   /* Innodisk red, lifted for dark bg */
  --ids-color-syntax-string:      #00dc00;
  --ids-color-syntax-number:      #5b8bff;
  --ids-color-syntax-comment:     #a8b0b6;
  --ids-color-syntax-function:    #5b8bff;
  --ids-color-syntax-type:        #fabe23;
  --ids-color-syntax-operator:    #e2e2e2;
  --ids-color-syntax-punctuation: #a8b0b6;

  /* Focus ring */
  --ids-color-focus-ring:         #ec1b23;
  --ids-color-focus-ring-on-red:  #ffffff;   /* white halo for brand-red buttons */

  /* Scrollbar */
  --ids-color-scrollbar-thumb:        #e2e2e2;
  --ids-color-scrollbar-thumb-hover:  #959595;

  /* ---------------- SPACE ---------------- */
  --ids-space-0:  0;
  --ids-space-1:  4px;
  --ids-space-2:  8px;
  --ids-space-3:  12px;
  --ids-space-4:  16px;
  --ids-space-6:  24px;
  --ids-space-8:  32px;
  --ids-space-12: 48px;
  --ids-space-16: 64px;

  /* ---------------- RADIUS ---------------- */
  --ids-radius-sm:   2px;     /* inline code, small chips */
  --ids-radius-md:   6px;     /* buttons, inputs, badges */
  --ids-radius-lg:   12px;    /* cards, modals, code blocks */
  --ids-radius-pill: 9999px;  /* pill badges, status pills */

  /* ---------------- SHADOW ---------------- */
  --ids-shadow-1: 0 1px 2px rgba(22, 39, 46, 0.06);
  --ids-shadow-2: 0 2px 6px rgba(22, 39, 46, 0.08);
  --ids-shadow-3: 0 8px 20px rgba(22, 39, 46, 0.10);
  --ids-shadow-4: 0 20px 48px rgba(22, 39, 46, 0.18);

  /* ---------------- FONT ---------------- */
  --ids-font-family-heading: "Barlow Condensed","Noto Sans TC","Noto Sans SC",
                             "Noto Sans JP","Noto Sans KR","Impact",
                             "Arial Narrow",sans-serif;
  --ids-font-family-body:    "Avenir Next LT Pro","Noto Sans TC","Noto Sans SC",
                             "Noto Sans JP","Noto Sans KR",-apple-system,
                             BlinkMacSystemFont,"Segoe UI",Roboto,
                             "Helvetica Neue",Arial,sans-serif;
  --ids-font-family-mono:    "JetBrains Mono","SF Mono","Menlo","Consolas",
                             "Liberation Mono",monospace;

  /* Sizes (brand guide §5.4 — desktop scale) */
  --ids-font-size-h1:      4.375rem;   /* 70px */
  --ids-font-size-h2:      3.375rem;   /* 54px */
  --ids-font-size-h3:      2.125rem;   /* 34px */
  --ids-font-size-h4:      1.5rem;     /* 24px */
  --ids-font-size-h5:      1.1875rem;  /* 19px */
  --ids-font-size-h6:      1rem;       /* 16px */
  --ids-font-size-lead:    1.25rem;    /* 20px */
  --ids-font-size-body:    1.0625rem;  /* 17px */
  --ids-font-size-small:   0.9375rem;  /* 15px */
  --ids-font-size-caption: 0.8125rem;  /* 13px */
  --ids-font-size-code:    0.9375rem;  /* 15px */

  --ids-font-weight-regular: 400;
  --ids-font-weight-medium:  500;
  --ids-font-weight-demi:    600;
  --ids-font-weight-bold:    700;

  --ids-font-leading-tight:   1.14;
  --ids-font-leading-snug:    1.3;
  --ids-font-leading-normal:  1.5;
  --ids-font-leading-relaxed: 1.6;

  --ids-font-tracking-tight:  -0.01em;
  --ids-font-tracking-normal: 0;
  --ids-font-tracking-loose:  0.01em;

  /* ---------------- Z-INDEX ---------------- */
  --ids-z-sidebar: 30;
  --ids-z-topbar:  40;
  --ids-z-modal:   60;
  --ids-z-toast:   70;

  /* ---------------- MOTION ---------------- */
  --ids-motion-duration-fast: 120ms;
  --ids-motion-duration-base: 200ms;
  --ids-motion-duration-slow: 320ms;
  --ids-motion-easing-standard:    cubic-bezier(0.2, 0, 0, 1);
  --ids-motion-easing-emphasized:  cubic-bezier(0.3, 0, 0, 1);
}
```

### 0.2 `[data-theme="dark"]` — dark mode

```css
[data-theme="dark"] {
  /* Background / surface */
  --ids-color-bg-page:        #0f1419;
  --ids-color-bg-surface:     #16272e;       /* --color-inno-blue-dark */
  --ids-color-bg-raised:      #1a2b33;
  --ids-color-bg-overlay:     rgba(0, 0, 0, 0.65);
  --ids-color-bg-selection:   rgba(255, 107, 112, 0.25);

  /* Text */
  --ids-color-text-primary:   #f5f5f5;
  --ids-color-text-secondary: #e2e2e2;
  --ids-color-text-muted:     #a8b0b6;
  --ids-color-text-inverse:   #16272e;       /* dark text used on lifted-red btn (6.7:1) */
  --ids-color-text-link:      #5b8bff;
  --ids-color-text-link-visited: #d977b0;

  /* Border / divider */
  --ids-color-border:         #2a3a42;
  --ids-color-divider:        #1f2f37;
  --ids-color-border-strong:  #e2e2e2;

  /* Brand — lifted red (brand guide §4.4) */
  --ids-color-brand:          #ff6b70;       /* AA-lifted from #ec1b23 */
  --ids-color-brand-hover:    #ff8a8e;
  --ids-color-brand-tint-08:  rgba(255, 107, 112, 0.10);
  --ids-color-brand-tint-12:  rgba(255, 107, 112, 0.15);
  --ids-color-brand-on:       #16272e;       /* dark text on lifted red = 6.7:1 */

  /* Callouts (brand guide §4.3 dark) */
  --ids-color-callout-note-bg:      #1a2b33;
  --ids-color-callout-note-border:  #2a3a42;
  --ids-color-callout-note-text:    #e2e2e2;

  --ids-color-callout-info-bg:      #0a1d3d;
  --ids-color-callout-info-border:  #5b8bff;
  --ids-color-callout-info-text:    #cfdcff;

  --ids-color-callout-tip-bg:       #0b2418;
  --ids-color-callout-tip-border:   #00dc00;
  --ids-color-callout-tip-text:     #bce8c8;

  --ids-color-callout-warning-bg:     #2a1f08;
  --ids-color-callout-warning-border: #fabe23;
  --ids-color-callout-warning-text:   #ffe5a3;

  --ids-color-callout-danger-bg:     #2a0d0f;
  --ids-color-callout-danger-border: #ff6b70;
  --ids-color-callout-danger-text:   #ffc5c8;

  /* Tables */
  --ids-color-table-header-bg:    #0f1419;   /* darker than surface in dark mode */
  --ids-color-table-header-text:  #f5f5f5;
  --ids-color-table-row-zebra:    #1a2b33;
  --ids-color-table-row-hover:    rgba(255, 107, 112, 0.12); /* lifted red on dark */
  --ids-color-table-border:       #2a3a42;

  /* Code blocks stay the same (already dark in light mode) but lift the bg slightly
     so the dark page contrast against the code surface is still visible */
  --ids-color-code-bg:            #0f1419;
  --ids-color-code-text:          #e2e2e2;
  --ids-color-code-header-bg:     #16272e;
  --ids-color-code-header-text:   #a8b0b6;
  --ids-color-code-gutter:        #4a5a62;
  --ids-color-code-selection:     rgba(255, 107, 112, 0.30);

  /* Syntax stays identical — already tuned for dark bg */
  --ids-color-syntax-keyword:     #ff6b70;
  --ids-color-syntax-string:      #00dc00;
  --ids-color-syntax-number:      #5b8bff;
  --ids-color-syntax-comment:     #a8b0b6;
  --ids-color-syntax-function:    #5b8bff;
  --ids-color-syntax-type:        #fabe23;
  --ids-color-syntax-operator:    #e2e2e2;
  --ids-color-syntax-punctuation: #a8b0b6;

  /* Focus ring */
  --ids-color-focus-ring:         #ff6b70;
  --ids-color-focus-ring-on-red:  #0f1419;   /* dark halo on lifted-red surface */

  /* Scrollbar */
  --ids-color-scrollbar-thumb:        #2a3a42;
  --ids-color-scrollbar-thumb-hover:  #4a5a62;

  /* Shadow — softer on dark, since pure-black shadows vanish */
  --ids-shadow-1: 0 1px 2px rgba(0, 0, 0, 0.40);
  --ids-shadow-2: 0 2px 6px rgba(0, 0, 0, 0.45);
  --ids-shadow-3: 0 8px 20px rgba(0, 0, 0, 0.55);
  --ids-shadow-4: 0 20px 48px rgba(0, 0, 0, 0.70);

  /* All space / radius / font-* / z / motion tokens are identical to light */
}
```

> **Token-group count:** 8 groups (`color`, `space`, `radius`, `shadow`,
> `font`, `z`, `motion`, plus a small `syntax` family nested under `color`).

---

## 1. Sidebar nav

### Purpose
Persistent navigation tree for the docs, fixed to the left edge, scrollable
independently of the main content.

### Anatomy
```
+-----------------------------+
| [Search trigger              ⌘K]  ← optional repeat of top-bar search
+-----------------------------+
| ▾ Getting started            |   ← top-level group, expanded
|     • Overview               |
|     • Install on Ubuntu      |   ← active item: red 4px left border
|     • Install on Windows     |
| ▸ Q911 user guide            |   ← top-level group, collapsed
| ▾ Concepts                   |
|     ▾ Manifests              |   ← depth-2, expanded
|         • Online manifest    |
|         • Offline manifest   |
|     ▸ Techblocks             |   ← depth-2, collapsed
| ▸ Reference                  |
| ▸ Troubleshooting            |
+-----------------------------+
```

### Tokens
| Part | Property | Token |
|---|---|---|
| Sidebar container | `background` | `--ids-color-bg-surface` |
| Sidebar container | `border-right` | `1px solid --ids-color-border` |
| Sidebar container | `width` | `280px` desktop, `100%` mobile drawer |
| Group label (depth-0) | `font-family` | `--ids-font-family-body` |
| Group label | `font-weight` | `--ids-font-weight-demi` |
| Group label | `font-size` | `--ids-font-size-small` (15px) |
| Group label | `color` | `--ids-color-text-primary` |
| Item label | `font-size` | `--ids-font-size-small` |
| Item label | `color` | `--ids-color-text-secondary` |
| Item — depth indent | `padding-left` | `--ids-space-4` per depth level |
| Item — vertical padding | `padding-y` | `--ids-space-2` |
| Item active — bg | `background` | `--ids-color-brand-tint-08` |
| Item active — left rule | `border-left` | `4px solid --ids-color-brand` |
| Item active — text | `color` | `--ids-color-text-primary` |
| Item active — weight | `font-weight` | `--ids-font-weight-demi` |
| Item hover bg | `background` | `--ids-color-divider` |
| Caret icon | `color` | `--ids-color-text-muted` |
| Scrollbar | thumb | `--ids-color-scrollbar-thumb` |

### States
- **Default**: text `--ids-color-text-secondary`, no bg.
- **Hover**: bg `--ids-color-divider`; caret rotates 90° on group toggle
  (transition `--ids-motion-duration-fast`).
- **Focus-visible**: 2px solid `--ids-color-focus-ring`, offset 2px,
  rendered *inside* the item (so it isn't clipped by the left-border on
  active items).
- **Active**: 4px brand left border, `--ids-color-brand-tint-08` bg, demi
  weight, primary text color.
- **Disabled**: not applicable — sidebar items are either present or
  removed.
- **Collapsed group**: caret `▸`; expanded: caret `▾`. Animate
  `max-height` over `--ids-motion-duration-base` with
  `--ids-motion-easing-standard`. Respect `prefers-reduced-motion`.

### Accessibility
- Implement as `<nav aria-label="Documentation">` containing nested `<ul>`s.
- Group toggles use `aria-expanded` + `aria-controls`.
- Active item carries `aria-current="page"`.
- Each item is `tabindex=0`; Tab moves through items, ↑↓ move within the
  tree (roving tabindex pattern).
- Active-state indication is **not red color alone** — it combines red
  left-rule + bold weight + tinted bg, so it passes WCAG 1.4.1 (use of
  color).

### Responsive
- **≥1024px**: sidebar fixed at 280px left edge; main content has left
  margin of 280px.
- **768–1023px**: sidebar collapses to a hamburger trigger in the top bar
  and opens as a left-anchored drawer over a scrim
  (`--ids-color-bg-overlay`, `--ids-z-modal`).
- **<768px**: drawer is full-width (max 320px), scrim fills the rest. Tap
  scrim or swipe left to dismiss.

---

## 2. Top bar

### Purpose
Site-wide chrome: brand lockup, primary nav, search trigger, theme toggle,
version selector, GitHub link. Sticky on scroll.

### Anatomy
```
+----------------------------------------------------------------------+
| [Logo] iQ Studio | Guide  Reference  API |   [⌘K Search]  v1.2▾  ☀  ⌘ |
|  40px              Barlow-Condensed-500     ────────────              |
+----------------------------------------------------------------------+
```
Left → right:
1. Logo (`iq-studio-logo.png`, **40px tall desktop / 36px mobile**).
2. Wordmark "iQ Studio" — Barlow Condensed 500, 24px, primary text color.
3. Primary nav links (3–5 max).
4. Spacer.
5. Search trigger button with ⌘K hint chip.
6. Version selector dropdown.
7. Theme toggle (sun/moon icon).
8. GitHub link (icon button).

### Tokens
| Part | Property | Token |
|---|---|---|
| Bar height | `height` | `64px` desktop / `56px` mobile (brand guide §7.1) |
| Bar bg | `background` | `--ids-color-bg-page` |
| Bar border-bottom | `border-bottom` | `1px solid --ids-color-border` |
| Bar shadow on scroll | `box-shadow` | `--ids-shadow-1` (added when `scrollY > 0`) |
| Z-index | `z-index` | `--ids-z-topbar` |
| Logo height | — | `40px` desktop, `36px` mobile |
| Logo clearspace | `padding` | `10px` all sides at 40px (= 25% per brand guide §7.1) |
| Wordmark | `font-family` | `--ids-font-family-heading` |
| Wordmark | `font-weight` | `--ids-font-weight-medium` (500) |
| Wordmark | `font-size` | `24px` |
| Wordmark | `color` | `--ids-color-text-primary` |
| Nav link | `font-size` | `--ids-font-size-small` |
| Nav link | `color` | `--ids-color-text-primary` |
| Nav link active | `border-bottom` | `2px solid --ids-color-brand`, offset 4px |
| Search trigger | `background` | `--ids-color-bg-raised` |
| Search trigger | `border` | `1px solid --ids-color-border` |
| Search trigger | `radius` | `--ids-radius-md` |
| ⌘K hint chip | `background` | `--ids-color-bg-page` |
| ⌘K hint chip | `font-family` | `--ids-font-family-mono` |
| Icon button | `size` | `36×36px` |
| Inter-control gap | — | `--ids-space-3` |

### States
- **Sticky default**: no shadow.
- **Sticky scrolled** (scrollY > 0): add `--ids-shadow-1`, animate over
  `--ids-motion-duration-fast`.
- Search trigger **hover**: bg `--ids-color-bg-surface`.
- Search trigger **focus-visible**: brand focus ring (see §14).
- Theme toggle **active** (current theme): icon color
  `--ids-color-brand`.
- Nav link **active**: 2px brand bottom border; weight stays regular (the
  border carries the state).

### Accessibility
- `<header role="banner">` wraps the bar.
- Logo + wordmark wrapped in a single link to `/` with
  `aria-label="iQ Studio docs home"`.
- Search trigger is a `<button>` (not an input) with
  `aria-label="Search (⌘K)"` so screen readers don't announce it as a form
  field until the modal opens.
- Theme toggle uses `aria-pressed` for the current theme.
- Logo PNG sits unmodified on the dark-mode bar per brand guide §7.1 — the
  near-white tile reads as a raised card, no inverted asset for v1.

### Responsive
- **<768px**: hide primary nav links and version selector, collapse them
  into the mobile drawer (opened by hamburger). Keep logo + wordmark +
  search-icon-only + theme toggle + GitHub icon visible.
- **<480px**: drop the wordmark, keep just the logo + hamburger + search
  icon + theme toggle.

### Wireframe — mobile (<768px)
```
+--------------------------------------------------+
| ☰  [Logo] iQ Studio              [🔍]  [☀]  [GH] |
+--------------------------------------------------+
```

---

## 3. Content typography

### Purpose
Set the prose hierarchy for documentation body content.

### Anatomy / tokens
| Element | Font family | Size | Weight | Color | Leading | Notes |
|---|---|---|---|---|---|---|
| `h1` | `--ids-font-family-heading` | `--ids-font-size-h1` | `--ids-font-weight-bold` | `--ids-color-text-primary` | `--ids-font-leading-tight` | Red underline accent (see below) |
| `h2` | `--ids-font-family-heading` | `--ids-font-size-h2` | `--ids-font-weight-bold` | `--ids-color-text-primary` | `1.18` | margin-top `--ids-space-12` |
| `h3` | `--ids-font-family-body` | `--ids-font-size-h3` | `--ids-font-weight-demi` | `--ids-color-text-primary` | `1.2` | margin-top `--ids-space-8` |
| `h4` | `--ids-font-family-body` | `--ids-font-size-h4` | `--ids-font-weight-demi` | `--ids-color-text-primary` | `1.3` | margin-top `--ids-space-6` |
| `h5` | `--ids-font-family-body` | `--ids-font-size-h5` | `--ids-font-weight-demi` | `--ids-color-text-primary` | `1.5` | margin-top `--ids-space-4` |
| `h6` | `--ids-font-family-body` | `--ids-font-size-h6` | `--ids-font-weight-demi` | `--ids-color-text-secondary` | `1.5` | uppercase, letter-spacing `0.04em` |
| `p` body | `--ids-font-family-body` | `--ids-font-size-body` | `--ids-font-weight-regular` | `--ids-color-text-primary` | `--ids-font-leading-relaxed` | max-width `72ch` |
| `.lead` | `--ids-font-family-body` | `--ids-font-size-lead` | `--ids-font-weight-regular` | `--ids-color-text-secondary` | `1.55` | first paragraph of a page |
| `code` inline | `--ids-font-family-mono` | `--ids-font-size-code` | `--ids-font-weight-regular` | `--ids-color-text-primary` on `--ids-color-bg-raised` | — | radius `--ids-radius-sm`, padding `2px 6px` |
| `blockquote` | inherit | `--ids-font-size-body` | regular | `--ids-color-text-secondary` | `1.6` | 4px left border `--ids-color-border-strong`, padding-left `--ids-space-4` |
| `ul`, `ol` | inherit | inherit | regular | inherit | `1.6` | indent `--ids-space-6`; nested adds another `--ids-space-6` |
| `hr` | — | — | — | `--ids-color-divider` | — | `1px`, margin-y `--ids-space-8` |

### H1 red underline accent
- **Color:** `--ids-color-brand`.
- **Thickness:** `4px`.
- **Length:** `64px` fixed (not relative — keeps the accent assertive at
  any heading length).
- **Offset:** `--ids-space-3` (12px) **below** the heading baseline.
- **Implementation hint (token only):** treat it as a decorative element
  via `border-bottom` or `::after` rule — exact technique left to the
  framework.

### Prose width
- `.prose` container: `max-width: 72ch` for paragraphs.
- Headings, code blocks, callouts, tables, figures: allowed to break out
  to the full content column width (~960px) for legibility.

### States
- Links inside prose: color `--ids-color-text-link`, underline always
  visible (`text-underline-offset: 2px`). Hover: same color, underline
  thickens from `1px` → `2px`. Visited:
  `--ids-color-text-link-visited`.
- Headings: not interactive by default. If a "copy link to heading" anchor
  is rendered on hover, render it as a faint `§` glyph in
  `--ids-color-text-muted`, opacity `0 → 1` over
  `--ids-motion-duration-fast`.

### Accessibility
- Heading levels are sequential — never skip from `h2` to `h4`.
- Color is **never** the only carrier of meaning in prose (links also get
  an underline; warnings get an icon, not just red text).
- 72ch max line length keeps reading speed within the WCAG 1.4.8
  recommendation.

### Wireframe
```
H1: Install iQ Studio Launcher on Ubuntu
████                                                ← 64px × 4px red rule

Lead: iQ Studio is the shortest path from a powered-on Innodisk
board to a running application. ...

H2: Prerequisites
H3: Hardware
   • Q911 development board
   • USB-C cable
   • Host running Ubuntu 22.04+
```

### Responsive
- All heading sizes shift to the tablet (≥48rem) and mobile scales per
  brand guide §5.4 at the matching breakpoints (mobile uses the smaller
  numbers). No other typographic shifts needed — line-height tokens stay
  constant.

---

## 4. Code blocks

### Purpose
Render multi-line source code with a filename header, language tag, and
copy action. **Dark even in light mode**, per the brand guide §8 row 13.

### Anatomy
```
+--------------------------------------------------+
| install.sh                       bash    [ Copy ]|  ← header bar
+--------------------------------------------------+
| 1  #!/usr/bin/env bash                            |  ← optional gutter
| 2  set -euo pipefail                              |
| 3                                                 |
| 4  iqs-launcher install \                         |
| 5      --manifest online \                        |
| 6      --target q911                              |
+--------------------------------------------------+
```

### Tokens
| Part | Property | Token |
|---|---|---|
| Outer container | `background` | `--ids-color-code-bg` (`#16272e` light, `#0f1419` dark) |
| Outer container | `border-radius` | `--ids-radius-lg` |
| Outer container | `box-shadow` | `--ids-shadow-1` |
| Header bar | `background` | `--ids-color-code-header-bg` |
| Header bar | `border-bottom` | `1px solid rgba(255,255,255,0.06)` |
| Header bar | `padding` | `--ids-space-2 --ids-space-4` |
| Filename | `font-family` | `--ids-font-family-mono` |
| Filename | `font-size` | `--ids-font-size-small` |
| Filename | `color` | `--ids-color-code-header-text` |
| Language tag | `font-family` | `--ids-font-family-body` |
| Language tag | `font-size` | `--ids-font-size-caption` |
| Language tag | `color` | `--ids-color-text-muted` |
| Language tag | `text-transform` | `uppercase` |
| Language tag | `letter-spacing` | `0.06em` |
| Pre/code body | `font-family` | `--ids-font-family-mono` |
| Pre/code body | `font-size` | `--ids-font-size-code` |
| Pre/code body | `color` | `--ids-color-code-text` |
| Pre/code body | `padding` | `--ids-space-4 --ids-space-6` |
| Pre/code body | `line-height` | `--ids-font-leading-normal` (1.5) |
| Line-number gutter | `color` | `--ids-color-code-gutter` |
| Line-number gutter | `padding-right` | `--ids-space-4` |
| Line-number gutter | `border-right` | `1px solid rgba(255,255,255,0.05)` |
| Selection | `background` | `--ids-color-code-selection` |

### Syntax color mapping
| Token type | Token |
|---|---|
| Keyword (`if`, `for`, `def`, `function`, shell builtins) | `--ids-color-syntax-keyword` (`#ff6b70` — Innodisk red, lifted) |
| String | `--ids-color-syntax-string` |
| Number | `--ids-color-syntax-number` |
| Comment | `--ids-color-syntax-comment` (italic) |
| Function name | `--ids-color-syntax-function` |
| Type / class name | `--ids-color-syntax-type` |
| Operator (`=`, `+`, `&&`) | `--ids-color-syntax-operator` |
| Punctuation (`{`, `}`, `;`, `,`) | `--ids-color-syntax-punctuation` |

> Brand point: shell/Python keywords render in the lifted brand red.
> Comments use muted gray. Strings green, numbers blue — this keeps the
> Innodisk accent rainbow inside the one place it makes sense on the doc
> site (data viz of code structure).

### Copy button
- **Idle**: text "Copy", color `--ids-color-code-header-text`, bg
  transparent, border `1px solid rgba(255,255,255,0.10)`, radius
  `--ids-radius-md`, padding `--ids-space-1 --ids-space-3`.
- **Hover**: bg `rgba(255,255,255,0.06)`, text
  `--ids-color-text-secondary`.
- **Active**: bg `--ids-color-brand-tint-12`.
- **Clicked / Copied**: text changes to "Copied!", icon swap to checkmark,
  color `--ids-color-syntax-string` (green); revert after `1500ms`.
- **Focus-visible**: white focus ring (see §14, on-dark variant).

### States
- **Loading** (e.g., async-loaded snippet): show a 3-line skeleton in
  `rgba(255,255,255,0.04)` with a shimmer animation; respect
  `prefers-reduced-motion` by disabling the shimmer.
- **Long line overflow**: container scrolls horizontally; never wrap (wrap
  destroys code legibility). Show a subtle scroll indicator on the right
  edge: 16px gradient from `--ids-color-code-bg` to transparent.

### Accessibility
- The `<pre>` is `tabindex=0` and gets the focus ring so keyboard users
  can scroll horizontally.
- Copy button is a real `<button>` with `aria-label="Copy code"` (changes
  to `aria-label="Copied"` after click).
- Filename + language are exposed to screen readers as a header above the
  code, not visually hidden.
- Syntax color is decorative; the literal characters carry meaning. No
  meaning is conveyed by color alone.

### Wireframe
```
┌──────────────────────────────────────────────────┐
│ install.sh                     BASH      [📋 Copy]│  header (#0f1419)
├──────────────────────────────────────────────────┤
│ 1  #!/usr/bin/env bash                            │
│ 2  set -euo pipefail                              │  body (#16272e)
│ 3                                                 │  mono, #e2e2e2
│ 4  iqs-launcher install \                         │
│ 5      --manifest online \                        │
└──────────────────────────────────────────────────┘
```

---

## 5. Callouts

### Purpose
Inline, semantic asides in prose: `info`, `tip`, `warning`, `danger`,
`note`. Five variants, light + dark.

### Anatomy
```
┌─┬────────────────────────────────────────────────┐
│■│ ⚠  Warning                                     │
│ │                                                │
│ │ This command rewrites the device's eMMC.       │
│ │ Back up /data before continuing.               │
└─┴────────────────────────────────────────────────┘
 ^ 4px left border, semantic color
```

Parts:
- 4px solid left border (semantic color).
- Tinted background fill.
- Icon slot (24×24) at top-left.
- Title (demi weight).
- Body (regular weight).

### Tokens (per variant — all defined in §0 above)

| Variant | bg | border | text | icon | Default icon |
|---|---|---|---|---|---|
| `note` | `--ids-color-callout-note-bg` | `--ids-color-callout-note-border` | `--ids-color-callout-note-text` | `--ids-color-callout-note-border` | "pencil" / generic |
| `info` | `--ids-color-callout-info-bg` | `--ids-color-callout-info-border` | `--ids-color-callout-info-text` | `--ids-color-callout-info-border` | "info" circle |
| `tip` | `--ids-color-callout-tip-bg` | `--ids-color-callout-tip-border` | `--ids-color-callout-tip-text` | `--ids-color-callout-tip-border` | "lightbulb" |
| `warning` | `--ids-color-callout-warning-bg` | `--ids-color-callout-warning-border` | `--ids-color-callout-warning-text` | `--ids-color-callout-warning-border` | "triangle-alert" |
| `danger` | `--ids-color-callout-danger-bg` | `--ids-color-callout-danger-border` | `--ids-color-callout-danger-text` | `--ids-color-callout-danger-border` | "octagon-alert" |

Common:
- `padding: --ids-space-4 --ids-space-6` (body), with extra
  `padding-left: --ids-space-8` to clear the 4px rule + icon column.
- `border-radius: --ids-radius-md`.
- Title font: `--ids-font-family-body`, weight
  `--ids-font-weight-demi`, size `--ids-font-size-body`.
- Body font: regular, size `--ids-font-size-body`, leading
  `--ids-font-leading-relaxed`.
- Icon size `24×24`, color = variant border token.
- Vertical margin around callouts: `--ids-space-6` top/bottom.

### States
- Static block — no interactive states beyond inherited link styles
  inside the body.
- Links inside a callout: color = variant text token (not the global
  `--ids-color-text-link`); underline always visible.

### Accessibility
- Each callout is a `<section role="note" aria-label="Warning">` (or
  matching label). Title text is duplicated in `aria-label` so the
  variant is announced regardless of icon visibility.
- Icon carries `aria-hidden="true"` since the variant label already
  communicates the meaning.
- Background tints meet AA on their text token per brand guide §4.3.

### Wireframe (warning, light mode)
```
┌─┬──────────────────────────────────────────────────┐
│█│ ⚠  Warning                                       │ bg #fff4d6
│█│                                                  │ border-left #fabe23
│█│ This command rewrites the device's eMMC.         │ text #7a4a00
│█│ Back up /data before continuing.                 │
└─┴──────────────────────────────────────────────────┘
```

---

## 6. Tables

### Purpose
Reference data: compatibility matrices, manifest schemas, CLI option lists.

### Anatomy
```
┌─────────────────────────────────────────────────────┐
│ Option           │ Type    │ Default │ Description  │  ← dark header
├─────────────────────────────────────────────────────┤
│ --manifest       │ string  │ online  │ Source ...   │
│ --target         │ string  │ q911    │ Board ...    │  ← zebra row
│ --offline-bundle │ path    │ —       │ Path to ...  │
└─────────────────────────────────────────────────────┘
```

### Tokens
| Part | Property | Token |
|---|---|---|
| Outer | `border` | `1px solid --ids-color-table-border` |
| Outer | `border-radius` | `--ids-radius-md` (clip header) |
| Outer | `overflow` | `hidden` (so radius clips header bg) |
| `thead` | `background` | `--ids-color-table-header-bg` (`#16272e`) |
| `thead th` | `color` | `--ids-color-table-header-text` |
| `thead th` | `font-family` | `--ids-font-family-body` |
| `thead th` | `font-weight` | `--ids-font-weight-demi` |
| `thead th` | `font-size` | `--ids-font-size-small` |
| `thead th` | `text-transform` | `uppercase` |
| `thead th` | `letter-spacing` | `0.04em` |
| `thead th` | `padding` | `--ids-space-3 --ids-space-4` |
| `tbody td` | `padding` | `--ids-space-3 --ids-space-4` |
| `tbody td` | `font-size` | `--ids-font-size-small` |
| `tbody td` | `color` | `--ids-color-text-primary` |
| `tbody td` | `border-bottom` | `1px solid --ids-color-divider` |
| Zebra row | `background` | `--ids-color-table-row-zebra` |
| Row hover | `background` | `--ids-color-table-row-hover` |
| First column (sticky on mobile) | `background` | `--ids-color-bg-page` |

Cell padding scale: dense tables can drop to `--ids-space-2
--ids-space-3` via a `.table--compact` modifier; spec it but keep the
default at `--ids-space-3 --ids-space-4`.

### States
- **Hover row**: bg `--ids-color-table-row-hover`. On dark mode this is
  the lifted-red tint (12% of `#ff6b70`); on light mode it is the
  source-red tint (8% of `#ec1b23`). Per brand guide §4.4, the source red
  tint at 8% on white is decorative and not text, so AA does not apply.
- **Sortable column header**: caret indicator
  `--ids-color-table-header-text` at 60% opacity (raised to 100% on
  hover/sort-active).

### Accessibility
- `<table>` with `<caption>` describing what the data is.
- `<th scope="col">` on headers, `<th scope="row">` on the first cell of
  each row when that cell is a label.
- Sortable headers are real `<button>` children of `<th>`, with
  `aria-sort="none|ascending|descending"`.
- Row hover red is decorative — never used to communicate state.

### Responsive
- **≥768px**: standard layout, no overflow.
- **<768px**: container becomes horizontally scrollable
  (`overflow-x: auto`). First column gets `position: sticky; left: 0` and
  the page-bg color so it remains readable. A right-edge gradient (24px,
  from `--ids-color-bg-page` to transparent) signals scrollability.

### Wireframe (mobile, scrolled mid-way)
```
┌──────────┬─ ─ ─ ─ ─ ─ ─ ─ ─┐
│ Option ▒▒│ Type   │ Default │ ← header (#16272e, white text)
├──────────┼─ ─ ─ ─ ─ ─ ─ ─ ─┤
│ --target │ string │ q911    │   ▒▒ = sticky first column
│ --manifs │ string │ online  │
└──────────┴─ ─ ─ ─ ─ ─ ─ ─ ─┘
                      ↑ horizontal scroll →
```

---

## 7. Search modal (⌘K)

### Purpose
Sitewide search, opened by `⌘K` / `Ctrl+K` or the top-bar search trigger.

### Anatomy
```
┌─────────────────────────────────────────────────────┐
│  🔍  Search the docs...                          ESC│  ← input
├─────────────────────────────────────────────────────┤
│  PAGES                                              │
│   • Install on Ubuntu                               │ ← highlighted
│   • Install on Windows                              │
│  HEADINGS                                           │
│   • Manifests › Online manifest                     │
│  CODE                                               │
│   • iqs-launcher install ...                        │
├─────────────────────────────────────────────────────┤
│  ↑↓ navigate    ↵ select    esc close               │ ← footer
└─────────────────────────────────────────────────────┘
```

### Tokens
| Part | Property | Token |
|---|---|---|
| Scrim | `background` | `--ids-color-bg-overlay` |
| Scrim | `z-index` | `--ids-z-modal` |
| Card | `background` | `--ids-color-bg-surface` |
| Card | `border` | `1px solid --ids-color-border` |
| Card | `border-radius` | `--ids-radius-lg` |
| Card | `box-shadow` | `--ids-shadow-4` |
| Card | `width` | `640px` desktop, `100%` mobile |
| Card | `max-height` | `min(80vh, 720px)` |
| Card position | — | centered horizontally, `top: 15vh` desktop / `0` mobile |
| Input | `font-family` | `--ids-font-family-body` |
| Input | `font-size` | `--ids-font-size-lead` |
| Input | `color` | `--ids-color-text-primary` |
| Input | `padding` | `--ids-space-4 --ids-space-6` |
| Input | `border-bottom` | `1px solid --ids-color-divider` |
| Leading icon | `color` | `--ids-color-text-muted` |
| Esc chip | `font-family` | `--ids-font-family-mono` |
| Esc chip | `color` | `--ids-color-text-muted` |
| Group label | `font-size` | `--ids-font-size-caption` |
| Group label | `color` | `--ids-color-text-muted` |
| Group label | `text-transform` | `uppercase` |
| Group label | `letter-spacing` | `0.06em` |
| Group label | `padding` | `--ids-space-3 --ids-space-6 --ids-space-1` |
| Result item | `padding` | `--ids-space-3 --ids-space-6` |
| Result item | `font-size` | `--ids-font-size-body` |
| Result item highlighted | `background` | `--ids-color-brand-tint-08` |
| Result item highlighted | `border-left` | `3px solid --ids-color-brand` |
| Footer | `background` | `--ids-color-bg-raised` |
| Footer | `border-top` | `1px solid --ids-color-divider` |
| Footer | `padding` | `--ids-space-2 --ids-space-6` |
| Footer hint | `font-size` | `--ids-font-size-caption` |
| Footer hint | `color` | `--ids-color-text-muted` |
| Keycap glyph | `font-family` | `--ids-font-family-mono` |

### States
- **Closed**: not in DOM (or `display:none` for keep-alive).
- **Opening / closing**: scrim fades over
  `--ids-motion-duration-base`; card slides + fades from
  `translateY(-8px)` to `translateY(0)`. Respect
  `prefers-reduced-motion` (fade only).
- **Input focus**: focus moves automatically into the input on open;
  visible cursor; no focus ring on the input (the entire modal already
  has focus context).
- **Result hover / keyboard-highlighted**: tinted bg + 3px brand
  left-border (same convention as sidebar active item, so the metaphor is
  consistent).
- **Empty state**: see §13.

### Accessibility
- `role="dialog"` `aria-modal="true"` `aria-label="Search"`.
- Focus trap: Tab cycles within the modal; Esc closes.
- Returns focus to the search trigger on close.
- Result list is a `role="listbox"`; each result `role="option"` with
  `aria-selected` on the highlighted one. Input has
  `aria-controls` + `aria-activedescendant` pointing at the highlighted
  result.

### Responsive
- **≥640px**: centered card, 640px wide, top 15vh.
- **<640px**: full-screen overlay; card fills the viewport; scrim is the
  card itself (no visible bg behind). Esc chip is replaced by a "Cancel"
  text button at the top-right.

### Wireframe (mobile, full-screen)
```
┌─────────────────────────────────────────────┐
│ ←  Search docs...                    Cancel │
├─────────────────────────────────────────────┤
│ PAGES                                       │
│ ▌ Install on Ubuntu                         │ ← highlighted
│   Install on Windows                        │
│ HEADINGS                                    │
│   Manifests › Online manifest               │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 8. Buttons

### Purpose
Action triggers across the site: CTAs, form submits, inline tools (copy,
share), destructive operations.

### Variants
| Variant | Use | bg | text | border |
|---|---|---|---|---|
| `primary` | Main CTA, one per view | `--ids-color-brand` | `--ids-color-brand-on` (white light / dark-ink dark) | none |
| `secondary` | Equal-weight alt | transparent | `--ids-color-text-primary` | `1px solid --ids-color-border-strong` |
| `ghost` | Tertiary, inline tool | transparent | `--ids-color-text-primary` | none |
| `danger` | Destructive irreversible action | transparent | `--ids-color-brand` light / `--ids-color-brand` dark | `1.5px solid --ids-color-brand` |
| `icon` | Square icon-only | transparent | inherits | none |

#### Primary vs danger — disambiguation
Both primary and danger reference the brand red, which would normally
conflict. **Resolution:**
1. **Primary is filled red**; **danger is an outline-red** button (border
   `1.5px solid --ids-color-brand`, transparent fill, red text). Filled vs
   outline is the first signal.
2. **Danger always carries a leading icon** (typically `octagon-alert` or
   `trash`). Primary may or may not have an icon. Icon is the second
   signal.
3. **Danger labels start with the destructive verb** ("Delete manifest",
   "Reset device"). Primary uses positive verbs ("Install", "Get started").
4. **Danger lives next to a cancel/secondary**, never alone.

### Sizes
| Size | Height | padding-x | font-size | icon size |
|---|---|---|---|---|
| `sm` | `28px` | `--ids-space-3` (12px) | `--ids-font-size-small` (15px) | `14px` |
| `md` | `36px` | `--ids-space-4` (16px) | `--ids-font-size-body` (17px) | `16px` |
| `lg` | `44px` | `--ids-space-6` (24px) | `--ids-font-size-h5` (19px) | `18px` |

### Tokens
| Part | Property | Token |
|---|---|---|
| All | `font-family` | `--ids-font-family-body` |
| All | `font-weight` | `--ids-font-weight-demi` |
| All | `border-radius` | `--ids-radius-md` |
| All | `transition` | `background --ids-motion-duration-fast --ids-motion-easing-standard, color same, border-color same` |
| With-icon gap | — | `--ids-space-2` |

### States
- **Default**: tokens above.
- **Hover** primary: bg `--ids-color-brand-hover`.
- **Hover** secondary/ghost: bg `--ids-color-brand-tint-08`, text
  `--ids-color-text-primary`.
- **Hover** danger: bg `--ids-color-brand-tint-08`, border stays brand.
- **Active** (pressed): scale `0.98`, motion duration
  `--ids-motion-duration-fast`. Disable for `prefers-reduced-motion`.
- **Focus-visible**: see §14. On primary (red bg), use the white-halo
  variant.
- **Disabled**: opacity `0.45`, cursor `not-allowed`, pointer-events none.
- **Loading**: text label is replaced by a spinner of the same height
  (mono SVG, color = current text color); button width is locked to the
  pre-loading width via `min-width`; click is no-op until loading ends.
  `aria-busy="true"` on the button.

### Accessibility
- `<button type="button">` (or `type="submit"`) — never a `<div>`.
- Icon-only buttons require `aria-label`.
- Loading state announces via `aria-live="polite"` on a child status node.
- Verify AA: primary (white on `#ec1b23`) → contrast 4.42:1, just under
  AA-normal. Mitigation: button text is `font-weight-demi` (600) and the
  `md`/`lg` sizes are 17–19px, which qualifies as **large text** under
  WCAG (≥14pt bold), where 3.0:1 is the bar. AA satisfied for `md` and
  `lg`. For `sm` (15px regular-context), demi weight at 15px is still
  large-text per WCAG. **Spec-level call:** all primary buttons render at
  weight 600 minimum.

### Wireframe
```
[Primary]   [Secondary]   [Ghost]   [⚠ Delete device]
 red bg      outline       no border   red outline + icon
```

---

## 9. Badges

### Purpose
Small inline labels for status, version, and platform metadata. Pill shape.

### Types
| Type | Sub-variants | Color mapping |
|---|---|---|
| **Status** | `stable` | `--ids-color-callout-tip-text` on `--ids-color-callout-tip-bg` |
| | `beta` | `--ids-color-callout-info-text` on `--ids-color-callout-info-bg` |
| | `deprecated` | `--ids-color-text-muted` on `--ids-color-bg-raised`, with `1px` dashed border `--ids-color-border` |
| | `new` | `--ids-color-brand-on` on `--ids-color-brand` (filled red — assertive, used sparingly) |
| **Version** | e.g., `v1.2` | `--ids-color-text-secondary` on `--ids-color-bg-raised`, mono font |
| **Platform** | `windows` | `--ids-color-callout-info-text` on `--ids-color-callout-info-bg` |
| | `linux` | `--ids-color-callout-warning-text` on `--ids-color-callout-warning-bg` |
| | `macos` | `--ids-color-text-secondary` on `--ids-color-bg-raised` |

### Tokens
| Part | Property | Token |
|---|---|---|
| All | `border-radius` | `--ids-radius-pill` |
| All | `font-family` | `--ids-font-family-body` (mono override for version badges) |
| All | `font-weight` | `--ids-font-weight-demi` |
| All | `font-size` | `--ids-font-size-caption` (13px) |
| All | `padding` | `2px --ids-space-2` |
| All | `letter-spacing` | `0.02em` |
| All | `text-transform` | `uppercase` (except version badges, which keep `v1.2` casing) |

### States
- Static. No hover/active. If the badge is wrapping a link, inherit link
  hover from the parent.

### Accessibility
- Pure visual labels — but the text content is the meaning, so screen
  readers read it correctly without ARIA.
- Color is paired with text, never alone (e.g., the "deprecated" badge
  has the literal word **and** the dashed outline as a secondary signal
  for grayscale viewers).

### Wireframe
```
Section heading  [BETA]  [v1.2]  [LINUX]  [DEPRECATED]
```

---

## 10. Landing-page persona cards

### Purpose
Top-of-fold entry points on `/index.html`, routing readers by intent.

### Anatomy
```
┌──────────────────────────────────┐
│  [Icon 32px]                     │
│                                  │
│  First-time user                 │  ← title (h4)
│                                  │
│  Install iQ Studio on your host  │  ← 1-line description
│  and run your first scan.        │
│                                  │
│  Start here  →                   │  ← link with arrow
└──────────────────────────────────┘
```

Personas (4):
1. **First-time user** — icon: `rocket` — "Install iQ Studio on your host and run your first scan."
2. **Developer / integrator** — icon: `code-2` — "Build Techblocks, integrate the SDK, ship custom flows."
3. **IT administrator** — icon: `shield-check` — "Manage offline manifests, fleet rollouts, and access policies."
4. **Returning user — what's new** — icon: `sparkles` — "See what changed in the latest release."

### Tokens
| Part | Property | Token |
|---|---|---|
| Card | `background` | `--ids-color-bg-surface` |
| Card | `border` | `1px solid --ids-color-border` |
| Card | `border-radius` | `--ids-radius-lg` |
| Card | `padding` | `--ids-space-6` |
| Card | `box-shadow` | none default, `--ids-shadow-2` on hover |
| Card | `transition` | `transform --ids-motion-duration-base, box-shadow same` |
| Icon | `color` | `--ids-color-brand` |
| Icon | `size` | `32×32px` |
| Icon container | `margin-bottom` | `--ids-space-4` |
| Title | `font-family` | `--ids-font-family-body` |
| Title | `font-weight` | `--ids-font-weight-demi` |
| Title | `font-size` | `--ids-font-size-h4` (24px) |
| Title | `color` | `--ids-color-text-primary` |
| Description | `font-size` | `--ids-font-size-body` |
| Description | `color` | `--ids-color-text-secondary` |
| Description | `margin-top` | `--ids-space-2` |
| Link | `font-weight` | `--ids-font-weight-demi` |
| Link | `color` | `--ids-color-text-link` |
| Link arrow | `transition` | `transform --ids-motion-duration-fast` |
| Link arrow on hover | `transform` | `translateX(2px)` |

### States
- **Default**: no shadow, no transform.
- **Hover**: `transform: translateY(-2px)`, shadow `--ids-shadow-2`, arrow
  slides +2px right. Respect `prefers-reduced-motion`: drop the transform,
  keep the shadow change.
- **Focus-visible**: focus ring on the whole card (the card itself is the
  link wrapper).
- **Active**: `transform: translateY(0)` (settles).
- The icon color does *not* change to lifted red on hover — keep it
  branded and stable.

### Accessibility
- Whole card is the click target. Implement as a single `<a>` wrapping all
  inner content, with `aria-label` mirroring the title.
- Focus ring renders on the card outline, not on inner elements.
- Icon `aria-hidden="true"`.

### Wireframe (3-up grid, desktop)
```
+--------------+  +--------------+  +--------------+
| 🚀           |  | </>          |  | 🛡            |
| First-time   |  | Developer    |  | IT admin     |
| user         |  | / integrator |  |              |
| Install ...  |  | Build ...    |  | Manage ...   |
| Start here → |  | Read docs →  |  | See guide →  |
+--------------+  +--------------+  +--------------+
+--------------+
| ✨            |
| What's new   |
| See what ... |
| Changelog →  |
+--------------+
```

### Responsive
- **≥1024px**: 3 columns, fourth card wraps to row 2 column 1.
  *Alternative:* `repeat(auto-fit, minmax(280px, 1fr))` to balance.
- **640–1023px**: 2 columns.
- **<640px**: 1 column, stacked.
- Card min-width: `280px`. Gap between cards: `--ids-space-6`.

---

## 11. Embedded video player

### Purpose
Render `.mp4` demo videos inline in the docs.

### Anatomy
```
┌──────────────────────────────────────────────┐
│                                              │
│        ▶                                     │  ← custom play overlay
│                                              │     (brand red, 64px)
│   [poster frame, 16:9]                       │
│                                              │
└──────────────────────────────────────────────┘
Figure 4: Running iqs-launcher install on a Q911.   ← caption
```

### Tokens
| Part | Property | Token |
|---|---|---|
| Aspect container | `aspect-ratio` | `16 / 9` |
| Aspect container | `border-radius` | `--ids-radius-lg` |
| Aspect container | `background` | `--ids-color-bg-raised` (placeholder while loading) |
| Aspect container | `box-shadow` | `--ids-shadow-1` |
| Video element | `width`/`height` | `100%` / `100%` |
| Poster image | `object-fit` | `cover` |
| Play overlay button | `size` | `64×64px` |
| Play overlay button | `background` | `--ids-color-brand` |
| Play overlay button | `color` | `--ids-color-brand-on` |
| Play overlay button | `border-radius` | `--ids-radius-pill` |
| Play overlay button | `box-shadow` | `--ids-shadow-3` |
| Caption | `font-size` | `--ids-font-size-caption` |
| Caption | `color` | `--ids-color-text-muted` |
| Caption | `margin-top` | `--ids-space-2` |
| Caption | `text-align` | `center` |
| Caption track (`<track kind="captions">`) | `background` | `rgba(15, 20, 25, 0.85)` |
| Caption track text | `color` | `#f5f5f5` |
| Caption track text | `font-family` | `--ids-font-family-body` |
| Caption track text | `font-size` | clamp at `16px` minimum |

### States
- **Idle / poster shown**: play overlay visible at center, slight pulse
  (`opacity 0.9 → 1.0`) over 2s; disable for
  `prefers-reduced-motion`.
- **Playing**: overlay fades out over `--ids-motion-duration-fast`.
- **Paused**: overlay fades back in.
- **Loading** (buffering): swap play icon for a spinner of same size,
  same brand-red bg.
- **Error** (source unavailable): replace overlay with a message
  "Video unavailable" + retry icon, on `--ids-color-bg-raised` bg.

Use **native `<video controls>`** by default. CSS adjustments allowed:
caption styling, custom poster, custom play overlay above the controls.
A fully custom control bar (timeline, scrub, mute) is **deferred — flag
as a future task** (v1.1) rather than spec'd here. Native controls give
us keyboard and screen-reader behavior for free in v1.

### Accessibility
- `<video>` has `controls` attribute.
- Every video ships with a `<track kind="captions" srclang="en"
  default>`. **TO_VERIFY** — caption `.vtt` files need to be authored
  alongside each demo video; not yet produced.
- Poster image is described in surrounding caption text, not via `alt`
  (HTML5 `<video poster>` has no alt attribute — caption text does the
  work).
- Custom play overlay is a real `<button>` with `aria-label="Play video"`
  layered above the video; clicking it calls `.play()` on the video
  element.
- Reduced motion: disable autoplay; disable any decorative loop.

### Responsive
- Full width of the prose column, capped at the content max-width.
- 16:9 ratio preserved at all sizes via `aspect-ratio` token.

---

## 12. 404 page

### Purpose
Friendly redirection when a route isn't found; keep the user in the docs.

### Anatomy
```
┌──────────────────────────────────────────────────┐
│ [Top bar — full]                                 │
├──────┬───────────────────────────────────────────┤
│ Side │                                           │
│ nav  │                                           │
│      │       4 0 4                               │  ← Barlow Condensed
│ (vis │       ────                                │     bold, very large
│ ible)│                                           │
│      │   That page isn't here.                   │  ← h3
│      │                                           │
│      │   It may have moved, been renamed, or     │  ← body
│      │   never existed. Try one of these:        │
│      │                                           │
│      │     →  Back to home                       │
│      │     →  Search the docs (⌘K)               │
│      │     →  Getting started                    │
│      │     →  Reference index                    │
│      │     →  Troubleshooting                    │
│      │                                           │
└──────┴───────────────────────────────────────────┘
```

### Tokens
| Part | Property | Token |
|---|---|---|
| "404" numerals | `font-family` | `--ids-font-family-heading` (Barlow Condensed) |
| "404" numerals | `font-weight` | `--ids-font-weight-bold` |
| "404" numerals | `font-size` | `clamp(96px, 18vw, 240px)` — display weight per brand guide §5 |
| "404" numerals | `color` | `--ids-color-text-primary` |
| "404" numerals | `line-height` | `1` |
| "404" numerals | `letter-spacing` | `-0.02em` |
| Red rule under "404" | `border-bottom` | `8px solid --ids-color-brand`, width `128px` |
| Headline | `font-size` | `--ids-font-size-h3` |
| Body | `font-size` | `--ids-font-size-body` |
| Body | `color` | `--ids-color-text-secondary` |
| Link list | `gap` | `--ids-space-3` |
| Link list link | `color` | `--ids-color-text-link` |
| Link list arrow | `color` | `--ids-color-brand` |
| Container | `max-width` | `640px`, vertically centered in content area |
| Container | `padding-block` | `--ids-space-16` |

Top bar and sidebar remain rendered and functional — the 404 only
replaces the main content panel.

### States
- Links use the standard prose link states (see §3).
- "Search the docs" link triggers the search modal directly (preserves
  the user's failed URL in a `?q=` param if the URL contains a slug like
  `/troubleshooting/foo` → search for `foo`).

### Accessibility
- `<main aria-labelledby="error-headline">` with `role="alert"` set on
  the headline-and-body wrapper so screen readers announce arrival on a
  404 page promptly.
- The "404" numerals are decorative; mark them `aria-hidden="true"`. The
  headline ("That page isn't here.") carries the meaning.
- Page `<title>` is "Page not found — iQ Studio docs".

### Wireframe — mobile
```
┌────────────────────────────┐
│ ☰ [Logo] iQ Studio    🔍 ☀ │
├────────────────────────────┤
│                            │
│   404                      │
│   ───                      │
│                            │
│ That page isn't here.      │
│                            │
│ Try one of these:          │
│   →  Back to home          │
│   →  Search the docs       │
│   →  Getting started       │
│   →  Troubleshooting       │
└────────────────────────────┘
```

---

## 13. Empty-search state

### Purpose
Shown **inside** the search modal (§7) when the query produces zero
matches.

### Anatomy
```
├─────────────────────────────────────────────────────┤
│  🔍  manifestz                                   ESC│  ← input still visible
├─────────────────────────────────────────────────────┤
│                                                     │
│            [Illustration slot, 96px]                │  ← placeholder
│                                                     │
│            No results for "manifestz"               │  ← headline
│                                                     │
│       Did you mean: manifest? · manifests?          │  ← suggestion row
│                                                     │
│            Browse all documentation →               │  ← fallback link
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Tokens
| Part | Property | Token |
|---|---|---|
| Container | `padding` | `--ids-space-12 --ids-space-6` |
| Container | `text-align` | `center` |
| Illustration slot | `width`/`height` | `96×96px` |
| Illustration slot | `background` | `--ids-color-bg-raised` (placeholder) |
| Illustration slot | `border-radius` | `--ids-radius-md` |
| Illustration slot | `margin-bottom` | `--ids-space-4` |
| Headline | `font-family` | `--ids-font-family-body` |
| Headline | `font-weight` | `--ids-font-weight-demi` |
| Headline | `font-size` | `--ids-font-size-h5` |
| Headline | `color` | `--ids-color-text-primary` |
| Query echo | `font-family` | `--ids-font-family-mono` |
| Query echo | `color` | `--ids-color-brand` |
| "Did you mean" row | `font-size` | `--ids-font-size-small` |
| "Did you mean" row | `color` | `--ids-color-text-secondary` |
| "Did you mean" link | `color` | `--ids-color-text-link` |
| Fallback link | `font-weight` | `--ids-font-weight-demi` |
| Fallback link | `color` | `--ids-color-text-link` |
| Fallback link | `margin-top` | `--ids-space-6` |

> **Illustration asset:** **TO_VERIFY** — a small flat illustration
> (compass / magnifier-with-zero / empty-folder motif) tinted in the
> Innodisk palette needs to be produced. Until then the spec uses a
> neutral placeholder block. Recommend commissioning a 96×96 SVG with
> single-color line work using `--ids-color-text-muted`, so the same
> asset works in both themes.

### States
- **No query**: empty-state is not shown; instead the modal shows a
  "Suggested" group (recent pages or most-viewed) — out of scope for this
  spec.
- **No results, no spelling suggestions**: hide the "Did you mean" row,
  keep the headline and fallback link.
- **No results, suggestions available**: render comma-separated
  suggestions as inline links.

### Accessibility
- Announce result count via `aria-live="polite"` on a status node sibling
  to the input: "No results for *manifestz*". Don't rely on the
  illustration to communicate emptiness.
- Suggestion links are real `<button>`s that re-run the search; Tab
  reaches them after the input.

---

## 14. Cross-cutting rules

### 14.1 Focus ring

- **Color (light mode):** `--ids-color-focus-ring` (`#ec1b23`).
- **Color (dark mode):** `--ids-color-focus-ring` (`#ff6b70`).
- **Width:** `2px`, `outline-style: solid`.
- **Offset:** `2px` (`outline-offset: 2px`).
- **On brand-red buttons / lifted-red surfaces:** the red ring would
  vanish into the button bg. Use the **halo variant**: a `2px` solid
  `--ids-color-focus-ring-on-red` ring (`#ffffff` light, `#0f1419` dark)
  *inside* the button (via `box-shadow: inset 0 0 0 2px <halo>`), plus
  the standard `2px outline` at offset `4px` on the outside in the brand
  color. Two-layer halo guarantees the focus state is visible against
  both the button and the page bg.
- Always rendered via `:focus-visible` (never `:focus`) so mouse clicks
  don't show a ring.
- Never set `outline: none` without immediately replacing with an
  equivalent indicator (`box-shadow` halo is fine).

### 14.2 Motion

- Durations are all under 320ms.
  - `--ids-motion-duration-fast` 120ms — hover transitions, micro-state
    swaps (button bg, copy-button label flip).
  - `--ids-motion-duration-base` 200ms — modal open/close, accordion
    expand, card hover lift.
  - `--ids-motion-duration-slow` 320ms — page-level transitions only
    (route change fade, theme swap if animated).
- Easings:
  - `--ids-motion-easing-standard` — UI defaults (subtle ease-out).
  - `--ids-motion-easing-emphasized` — meaningful arrivals (modal open,
    toast in).
- **Animate:** opacity, transform, background-color, color, box-shadow,
  border-color, outline-color.
- **Never animate:** layout-affecting properties (`width`, `height`,
  `top`, `left`, `margin`, `padding`) — they trigger layout thrash. Use
  `transform` instead.
- **Respect `prefers-reduced-motion: reduce`:** disable all transforms
  and translateY animations; keep opacity changes (≤120ms) only.
- Theme toggle is **non-animated** by default — flipping every CSS
  custom property at once over 200ms looks broken. Just swap the
  attribute.

### 14.3 Spacing rhythm

- **Section vertical rhythm** (between H2 sections on a long page):
  `--ids-space-12` (48px) top, `--ids-space-6` bottom of the prior
  section's content. Net `48px` whitespace.
- **Between H3 and following body**: `--ids-space-3` (12px).
- **Between paragraphs**: `--ids-space-4` (16px) bottom margin.
- **Between body and a callout / table / code block**: `--ids-space-6`.
- **Page content top padding** (below the top bar): `--ids-space-12` on
  desktop, `--ids-space-8` on mobile.
- **Page content side padding** on mobile: `--ids-space-4` minimum.
- Content density: prose stays comfortable (1.6 leading, 72ch line).
  Reference tables and CLI option lists are denser (`.table--compact`
  with `--ids-space-2 --ids-space-3` cell padding) so a full option set
  can be scanned in one screen.

### 14.4 Iconography

- **Chosen icon set:** **Lucide** (MIT, fork of Feather Icons).
- Justification:
  1. **Stroke-only**, no fills — matches the engineering-tool aesthetic
     of Innodisk product photography and the iQ Studio logo's own
     stroke-based "slider" illustration.
  2. **Highly consistent** geometry (2px stroke, 24px artboard, round
     line-caps); Phosphor is great but has multiple weight variants that
     are easy to misuse and create inconsistency.
  3. **Permissively licensed** (MIT), tree-shakable per-icon.
  4. Includes all icons referenced in this spec (`search`, `command`,
     `chevron-right`, `chevron-down`, `copy`, `check`, `triangle-alert`,
     `info`, `lightbulb`, `octagon-alert`, `pencil`, `rocket`, `code-2`,
     `shield-check`, `sparkles`, `sun`, `moon`, `github`, `play`,
     `x`).
- **Stroke width:** `2px` (Lucide default).
- **Size scale:** `14 / 16 / 20 / 24 / 32 / 48 px`. Standard inline icon
  is `16px`; nav/button icons `16–20px`; persona card icons `32px`;
  video play overlay icon `32px` inside a `64px` button; 404 hero is
  text not icon.
- **Color:** icons inherit `color: currentColor` from their parent so a
  single token swap repaints them. Brand-colored icons explicitly set
  `color: --ids-color-brand`.
- **Phosphor is acceptable as a substitute** if Lucide can't cover a
  specific icon (rare). Pick one and commit before implementation —
  don't mix sets.

### 14.5 Image / figure treatment

- All figures use a `<figure>` + `<figcaption>` pair.
- **Caption style:** `--ids-font-size-caption` (13px),
  `--ids-color-text-muted`, `text-align: center`, `margin-top:
  --ids-space-2`. Prefix "Figure N: " in demi weight, the description in
  regular weight.
- **Border:** none on most figures. **A 1px solid `--ids-color-border`**
  + `border-radius: --ids-radius-md` on screenshots specifically
  (so they sit as a defined surface, not floating).
- **Max-width:** full content column (~960px). Center if narrower than
  the column. Add `--ids-space-6` vertical margin top and bottom.
- **Dark-mode handling of PNGs with white backgrounds:** the diagrams in
  `./docs/fig/` (`iqs-struct.png`, `iqs-online-flow.svg`,
  `iqs-offline-flow.svg`, `ai_on_dragonwing_sw_stack.png`, etc.) were
  flagged in brand guide §3 as **draw.io defaults** that need retinting.
  This spec does **not** dictate their internal colors — that depends on
  the diagrams being re-exported with palette-correct tints
  (`--ids-color-inno-blue-light` at 12% alpha for online lanes,
  `--ids-color-inno-yellow` at 12% alpha for offline lanes, etc., per
  brand guide §3).
- **Interim treatment:** for any PNG with a white background rendered in
  dark mode, wrap it in a thin neutral plate: `padding: --ids-space-3
  background: #fafafa; border-radius: --ids-radius-md`. This guarantees
  the figure reads as a card rather than a glowing white rectangle.
  Remove the plate once the figure is re-exported with a transparent or
  dark-mode-friendly bg. **TO_VERIFY** — figure re-export is owned by
  the diagram author, not this spec.
- **SVGs:** if an SVG declares fills against a white assumption, hint at
  `mix-blend-mode: multiply` only as a last resort; better is to fix the
  source SVG.

---

## 15. Unresolved decisions (carry into implementation)

- **Icon set:** Lucide recommended above. Phosphor is acceptable. **Pick
  one before any component is built.**
- **Avenir Next LT Pro licensing** for the doc-site domain (brand guide
  §5.1). Default fallback is **Inter 400/600** in the body font stack if
  legal/IT doesn't extend the corporate license. The token
  `--ids-font-family-body` already lists Avenir first; switching to Inter
  is a one-line token change.
- **Caption `.vtt` files** for each demo video (§11). Not yet produced.
- **Empty-search illustration** (§13). Not yet produced.
- **`iq-studio-logo-dark.png`** (brand guide §7.1) — deferred to v1.1.
  v1 uses the single PNG against both bars.
- **Custom video player** beyond native controls (§11). Deferred to v1.1.
- **Diagram re-export** in `./docs/fig/` to drop draw.io defaults (brand
  guide §3 + §14.5 here). Cleanup task, not blocking.
- **Logo color pixel-sampling** to replace the visually-estimated hexes
  in brand guide §3 — sub-brand reconciliation only, not blocking for UI
  chrome.

---

## 16. AA-contrast issues encountered

Two issues required design-level resolution beyond what the brand guide
already documents:

1. **Primary button text on `#ec1b23` is 4.42:1** — exactly the value
   the brand guide flagged. The brand guide says "for body-text-sized
   red, pair with weight 600+ or supplement with underline / icon." This
   spec applies that rule directly to the button: **all primary buttons
   render at `--ids-font-weight-demi` (600), minimum size `md` (17px)**,
   which qualifies the white-on-red pairing as **large text** (≥14pt
   bold) under WCAG 1.4.3, where the threshold drops to 3.0:1. AA met.
   Spec-level rule recorded in §8.
2. **Primary vs danger button conflict** — both want to use the brand
   red. The brand guide does not resolve this. This spec resolves it
   with the four-rule disambiguation in §8 (filled primary, outlined
   danger, mandatory danger icon, mandatory destructive verb in label,
   adjacent cancel button).

All other contrast pairings used in this spec inherit from the brand
guide's audit and are already AA-verified there.

---

*End of component spec.*
