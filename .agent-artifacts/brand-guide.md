# iQ Studio Documentation Site — Brand Guide

**Author:** Brand Guardian agent
**Date:** 2026-05-22
**Scope:** Visual identity, type system, voice, and theming tokens for the
iQ Studio Launcher documentation/user-guide site. The site is an official
Innodisk product surface and must read as a native member of the Innodisk
product family.

---

## 1. Source extraction summary

Innodisk's public site (`innodisk.com`) is a Nuxt/Vue SPA. The HTML body that
`WebFetch` returns is post-processed and strips inline styles and stylesheet
links, so the first round of fetches surfaced *no* color information. The
working extraction path was:

1. `curl` the rendered HTML of `https://www.innodisk.com/en` →
   `/tmp/innodisk_home.html`. The `<head>` references hashed Nuxt CSS bundles,
   e.g. `/_nuxt/entry.FGUXsY83.css`, `/_nuxt/Main.ashzKQ4w.css`,
   `/_nuxt/Index.CemCJW5-.css`, `/_nuxt/Section.BmlxDJMY.css`.
2. `curl` each bundle and grep for `#xxxxxx`, `font-family:`, and `:root`
   blocks.

### Where each value came from (verbatim from the production CSS)

| Token | Hex | Source CSS file | Selector / variable name |
|---|---|---|---|
| Brand red (primary) | `#ec1b23` | `entry.FGUXsY83.css` | `:root { --color-primary:#ec1b23; --color-inno-red:#ec1b23; }` |
| White | `#fff` | `entry.FGUXsY83.css` | `:root { --color-white:#fff; }` |
| Black | `#000` | `entry.FGUXsY83.css` | `:root { --color-black:#000; }` |
| Light gray (divider/surface) | `#e2e2e2` | `entry.FGUXsY83.css` | `:root { --color-inno-gray-light:#e2e2e2; }` |
| Mid gray (muted text) | `#959595` | `entry.FGUXsY83.css` | `:root { --color-inno-gray:#959595; }` |
| Dark navy (heading/ink) | `#16272e` | `entry.FGUXsY83.css` | `:root { --color-inno-blue-dark:#16272e; }` |
| Link / action blue | `#0046ff` | `entry.FGUXsY83.css` | `:root { --color-inno-blue:#0046ff; }` |
| Info / highlight blue (light) | `#00b4ff` | `entry.FGUXsY83.css` | `:root { --color-inno-blue-light:#00b4ff; }` |
| Accent orange | `#ff6900` | `entry.FGUXsY83.css` | `:root { --color-inno-orange:#ff6900; }` |
| Accent yellow | `#fabe23` | `entry.FGUXsY83.css` | `:root { --color-inno-yellow:#fabe23; }` |
| Accent magenta | `#be0078` | `entry.FGUXsY83.css` | `:root { --color-inno-magenta:#be0078; }` |
| Accent pink (`f0f`) | `#f0f` | `entry.FGUXsY83.css` | `:root { --color-inno-pink:#f0f; }` |
| Success green (dark) | `#007800` | `entry.FGUXsY83.css` | `:root { --color-inno-green:#007800; }` |
| Success green (bright) | `#00dc00` | `entry.FGUXsY83.css` | `:root { --color-inno-green-light:#00dc00; }` |
| Body background | resolves to `#fff` | `entry.FGUXsY83.css` | `--body-bg-color: var(--color-white)` |
| Body text | resolves to `#000` | `entry.FGUXsY83.css` | `--body-text-color: var(--color-black)` |
| Body font stack | `Avenir Next LT Pro, Noto Sans TC` | `entry.FGUXsY83.css` | `--font-family-avenir`, applied on `body { font-family: var(--font-family-avenir) }` |
| Display font stack | `Barlow Condensed, Noto Sans TC` | `entry.FGUXsY83.css` | `--font-family-barlow` |
| Locale-swapped CJK fallback | `Noto Sans JP`, `Noto Sans KR` | `entry.FGUXsY83.css` | `:root:lang(jp) { --font-family-avenir: ... Noto Sans JP } :root:lang(kr) { ... Noto Sans KR }` |
| Self-hosted webfonts | `/fonts/AvenirNextLTPro-Regular.otf` (400), `/fonts/AvenirNextLTPro-Demi.otf` (600), `/fonts/NotoSansKR-VariableFont_wght.ttf`, `/fonts/NotoSansJP-VariableFont_wght.ttf` | `entry.FGUXsY83.css` | `@font-face` blocks |
| Favicon | `/favicon.ico` | `home.html <head>` | `<link rel="icon" href="/favicon.ico" type="image/x-icon">` |

### Verbatim tone-of-voice samples

Pulled from `https://www.innodisk.com/en/industries/data-center` via WebFetch:

> "The lines between application-specific servers are fading as computing
> spreads from hyperscalers and large-scale data centers to smaller
> enterprise server rooms and remote edge locations."

> "Data center memory and storage must be fast enough to enable
> lightning-fast boot times and data delivery, reliable through heavy loads,
> and with a large capacity for parallel delivery of resources."

> "Our DRAM modules, industrial-grade SSDs, and other expansion solutions
> are engineered for challenging environments, providing broad temperature
> tolerance and exceptional reliability."

> "At Innodisk, we believe that any challenge can be overcome through
> cooperation."

### URLs fetched

- `https://www.innodisk.com/en` — homepage (HTML + CSS bundles)
- `https://www.innodisk.com/en/products/flash-storage/pcie-m2` — product list
- `https://www.innodisk.com/en/products/flash-storage/pcie-m2/m2-p42-4te2-icell` — product detail
- `https://www.innodisk.com/en/industries/data-center` — body-copy source
- `https://www.innodisk.com/_nuxt/entry.FGUXsY83.css` — primary design tokens
- `https://www.innodisk.com/_nuxt/Main.ashzKQ4w.css`,
  `/_nuxt/Index.CemCJW5-.css`, `/_nuxt/Section.BmlxDJMY.css` — confirmed
  re-use of the same hex set
- `https://www.innodisk.com/en/about` and `/en/about-us` — both returned
  **404**, so a dedicated About page could not be sampled. Tone samples
  above come from the Industries page instead.

### `TO_VERIFY` items remaining

Every hex in the Innodisk-source table is **directly observed in production
CSS**, no `TO_VERIFY` needed. The items below are derived/specified rather
than fetched and are explicitly flagged:

1. **`TO_VERIFY` — iQ Studio logo dominant palette.** The PNG at
   `./docs/fig/iq-studio-logo.png` is a glossy app-icon-style mark on a
   rounded white tile. Visible bands include a warm red, a cool blue, and a
   violet/magenta gradient running through "fader" strokes, plus a dark gray
   horizontal element near the top. No pixel-sampling tool was available in
   this session, so the hexes below are *visually estimated* from the
   rendered image:
   - red band ≈ `#E94B5C` (close to but distinctly *softer* than the
     parent `#ec1b23` — closer to a coral than the corporate red)
   - blue band ≈ `#2A9DE0`
   - violet/magenta blend ≈ `#8E6BD6`
   - top dark element ≈ `#2C2C2C`
   - tile background ≈ `#FAFAFA` (off-white)
   These should be re-sampled with a pixel inspector before being treated
   as canonical sub-brand tokens. Reconciliation rule in §3 below.
2. **`TO_VERIFY` — dark-mode "raised surface" elevation hex `#1a2b33`.**
   This is a derived lift of `--color-inno-blue-dark #16272e` (+4 L*) for
   card backgrounds; it does not appear in Innodisk source CSS.
3. **`TO_VERIFY` — info/tip/warning/danger callout backgrounds in §4.**
   These are tinted from the observed accent hues (red, blue-light,
   yellow, green) at low saturation to meet AA contrast with their text
   color; they don't appear verbatim in Innodisk CSS.
4. **`TO_VERIFY` — lifted red `#ff6b70` for dark mode.** Derived for AA
   compliance against the dark surfaces; not in source.
5. **`TO_VERIFY` — Innodisk does not publish a `meta theme-color` tag.**
   The recommended `#ec1b23` value for the doc-site theme-color is inferred
   from `--color-primary`, not directly read from a meta tag.

**Total `TO_VERIFY` count: 5.** Everything in the parent palette in §2 is
directly observed.

---

## 2. Innodisk parent palette (observed)

Pulled verbatim from `_nuxt/entry.FGUXsY83.css` `:root`:

| Semantic role | Token name (source) | Hex | Notes |
|---|---|---|---|
| Brand primary / CTA | `--color-primary`, `--color-inno-red` | `#ec1b23` | Single brand color, used as the only "hot" accent |
| Surface / page bg | `--color-white` (`--body-bg-color`) | `#ffffff` | Always-light page background on innodisk.com |
| Ink / body text | `--color-black` (`--body-text-color`) | `#000000` | High contrast body type |
| Heading / dark ink | `--color-inno-blue-dark` | `#16272e` | Used as the "near-black with a green-blue cast" — Innodisk's preferred non-pure-black ink |
| Border / divider | `--color-inno-gray-light` | `#e2e2e2` | Card outlines, hairlines |
| Muted / secondary text | `--color-inno-gray` | `#959595` | Captions, metadata |
| Link / data action | `--color-inno-blue` | `#0046ff` | Saturated blue |
| Highlight blue | `--color-inno-blue-light` | `#00b4ff` | Promo/feature accents |
| Accent — warm | `--color-inno-orange` | `#ff6900` | Industry charts |
| Accent — yellow | `--color-inno-yellow` | `#fabe23` | Industry charts |
| Accent — magenta | `--color-inno-magenta` | `#be0078` | Industry charts |
| Accent — pink | `--color-inno-pink` | `#f0f` (= `#ff00ff`) | Data viz only |
| Success — base | `--color-inno-green` | `#007800` | |
| Success — bright | `--color-inno-green-light` | `#00dc00` | Status indicators |

### Key parent-brand observations

- Innodisk uses **black-on-white as the default**, with `#16272e` as a
  softer ink when type sits on photography. There is **no dark-mode** on
  innodisk.com itself, so any dark-mode tokens we ship are net-new.
- There is **exactly one brand red**: `#ec1b23`. It is the *only* hot
  accent across the whole site. Reuse it sparingly — for primary CTAs and
  active states, not for decoration.
- The "accent rainbow" (orange/yellow/magenta/pink/green/blue) is reserved
  for **data visualization and segmentation graphics**. Do not adopt those
  hues as UI chrome on the doc site.

---

## 3. iQ Studio logo palette reconciliation

### Logo observations (from `./docs/fig/iq-studio-logo.png`)

The iQ Studio mark is rendered as a macOS-style rounded-square app icon on
a near-white tile. It shows three horizontal "slider" rows whose tracks
gradient from a warm red on the left through a violet into a cyan/blue on
the right, plus a darker horizontal "ruler" near the top.

| Element | Estimated hex | `TO_VERIFY` |
|---|---|---|
| Tile background | `#FAFAFA` | yes |
| Warm red (left handles) | `#E94B5C` | yes |
| Blue (right handles) | `#2A9DE0` | yes |
| Violet midpoint | `#8E6BD6` | yes |
| Top dark bar | `#2C2C2C` | yes |

### Reconciliation strategy

The logo's red is **softer / pinker** than the corporate `#ec1b23`. Two
plausible reasons: (a) compression artifacts and gloss highlights from the
PNG render, (b) the logo was designed as a sub-brand mark before strict
parent-brand color matching, common with engineering-led products.

**Rule of thumb for the doc site:**

1. **Parent palette wins for all UI chrome.** Top-bar background, primary
   CTA, link color, focus rings, brand stripe in the footer — all use
   `#ec1b23` from `--color-primary`. This guarantees the doc site reads as
   a native Innodisk property.
2. **The logo is shown as-is, unmodified.** Don't recolor the artwork to
   force it to match the parent red — that would damage the sub-brand
   asset. Place it on white (light mode) or on a near-white plate
   (`#FAFAFA`) inside the dark-mode top bar so the gradient still pops.
3. **The sub-brand cyan/violet in the logo is decorative only.** Do not
   promote those hues into the design-token layer. They live inside the
   logo bitmap and nowhere else.
4. **If a future "iQ Studio" wordmark or favicon mark is produced**, push
   to align its red to `#ec1b23` so it inherits from the corporate
   palette. Flag this as a brand-evolution item.

### Diagram color conventions (from `./docs/fig/`)

Files inspected:

- `iqs-struct.png` — six green-tinted callout pills (Start Guide, Core,
  Techblocks, SDK, Integrations, Benchmark) circling a dark-green central
  pill labeled "iQ studio". The greens here are draw.io defaults
  (approx `#82B366` / `#0E8A4E`), **not** part of the Innodisk palette.
- `iqs-online-flow.svg` — orange-tinted swimlane (`#ffe6cc` fill /
  `#ffb570` stroke, both draw.io defaults) with white process boxes.
- `iqs-offline-flow.svg` — yellow-tinted swimlane (`#fff2cc` fill /
  `#ffce9f` stroke, draw.io defaults).

These were drawn in draw.io with stock colors and **do not currently
follow the brand palette**. Recommendation (flag as cleanup, not blocking):
when these diagrams are re-exported, retint the pills/swimlanes to:

- "online" lane → `--color-inno-blue-light #00b4ff` at 12% alpha
- "offline" lane → `--color-inno-yellow #fabe23` at 12% alpha
- structural callout pills → `--color-inno-blue-dark #16272e` text on
  `--color-inno-gray-light #e2e2e2` fill, with the centerpiece in solid
  brand red `#ec1b23` so the iQ Studio core reads as the focal point.

---

## 4. Doc-site palette — light mode and dark mode

The doc-site theme is a **two-mode adaptation of the parent palette**.
Light mode mirrors innodisk.com directly. Dark mode is net-new and has
been engineered so the brand red still passes WCAG AA on dark surfaces.

### 4.1 Semantic tokens — light mode

| Token | Hex | Source / derivation |
|---|---|---|
| `--bg-page` | `#ffffff` | `--color-white` |
| `--bg-surface` | `#fafafa` | derived (slight off-white for cards) `TO_VERIFY` |
| `--bg-raised` | `#f5f5f5` | derived (sidebars, code blocks) `TO_VERIFY` |
| `--text-primary` | `#16272e` | `--color-inno-blue-dark` (Innodisk's preferred ink, 15.4:1 on white) |
| `--text-secondary` | `#4a4a4a` | derived (`#959595` is too light for body, 3:1; `#4a4a4a` gets 8.86:1) `TO_VERIFY` |
| `--text-muted` | `#959595` | `--color-inno-gray` (3:1 on white — large-text only) |
| `--text-inverse` | `#ffffff` | `--color-white` |
| `--border` | `#e2e2e2` | `--color-inno-gray-light` |
| `--divider` | `#ececec` | derived `TO_VERIFY` |
| `--accent-primary` (CTA, focus ring, active nav) | `#ec1b23` | `--color-primary` |
| `--accent-primary-hover` | `#c8141b` | derived (~12% darker) `TO_VERIFY` |
| `--link` | `#0046ff` | `--color-inno-blue` (6.33:1 on white) |
| `--link-visited` | `#be0078` | `--color-inno-magenta` |
| `--code-bg` | `#f5f5f5` | derived `TO_VERIFY` |
| `--code-text` | `#16272e` | mirrors `--text-primary` |

### 4.2 Semantic tokens — dark mode

| Token | Hex | Notes |
|---|---|---|
| `--bg-page` | `#0f1419` | derived dark surface, slightly cooler than #16272e `TO_VERIFY` |
| `--bg-surface` | `#16272e` | `--color-inno-blue-dark` — Innodisk's own dark ink reused as our dark canvas |
| `--bg-raised` | `#1a2b33` | derived raised card `TO_VERIFY` |
| `--text-primary` | `#f5f5f5` | 16.98:1 on `--bg-page` |
| `--text-secondary` | `#e2e2e2` | `--color-inno-gray-light` repurposed as light text (14.29:1) |
| `--text-muted` | `#a8b0b6` | derived for AA muted (8.42:1) `TO_VERIFY` |
| `--text-inverse` | `#0f1419` | |
| `--border` | `#2a3a42` | derived `TO_VERIFY` |
| `--divider` | `#1f2f37` | derived `TO_VERIFY` |
| `--accent-primary` (lifted red) | `#ff6b70` | **AA-lifted from `#ec1b23`** — see §4.4 |
| `--accent-primary-hover` | `#ff8a8e` | derived `TO_VERIFY` |
| `--link` | `#5b8bff` | lifted from `#0046ff` (5.80:1 on `#0f1419`) `TO_VERIFY` |
| `--link-visited` | `#d977b0` | lifted from `#be0078` `TO_VERIFY` |
| `--code-bg` | `#16272e` | `--color-inno-blue-dark` |
| `--code-text` | `#e2e2e2` | |

### 4.3 Callout tokens (light mode; mirror on dark with surface inverted)

Callout types follow the common docs convention (note, tip, info, warning,
danger). Backgrounds are the relevant Innodisk hue tinted to ~10% alpha
over white; text and border are the saturated hue or a dark/light variant
that meets AA on the tinted background. All ratios computed; see §4.4.

| Type | bg (light) | border (light) | text (light) | AA ratio |
|---|---|---|---|---|
| `info` | `#e6efff` `TO_VERIFY` | `#0046ff` (`--color-inno-blue`) | `#0046ff` | 5.47:1 |
| `tip` | `#e3f5ea` `TO_VERIFY` | `#007800` (`--color-inno-green`) | `#006030` `TO_VERIFY` | 6.82:1 |
| `note` | `#eef0f1` `TO_VERIFY` | `#16272e` (`--color-inno-blue-dark`) | `#16272e` | ~13:1 |
| `warning` | `#fff4d6` `TO_VERIFY` | `#fabe23` (`--color-inno-yellow`) | `#7a4a00` `TO_VERIFY` | 6.83:1 |
| `danger` | `#fde7e8` `TO_VERIFY` | `#ec1b23` (`--color-primary`) | `#b3151c` `TO_VERIFY` | 5.84:1 |

Callout tokens — dark mode counterparts (swap bg/text):

| Type | bg (dark) | border (dark) | text (dark) |
|---|---|---|---|
| `info` | `#0a1d3d` `TO_VERIFY` | `#5b8bff` `TO_VERIFY` | `#cfdcff` `TO_VERIFY` |
| `tip` | `#0b2418` `TO_VERIFY` | `#00dc00` (`--color-inno-green-light`) | `#bce8c8` `TO_VERIFY` |
| `note` | `#1a2b33` `TO_VERIFY` | `#2a3a42` `TO_VERIFY` | `#e2e2e2` |
| `warning` | `#2a1f08` `TO_VERIFY` | `#fabe23` | `#ffe5a3` `TO_VERIFY` |
| `danger` | `#2a0d0f` `TO_VERIFY` | `#ff6b70` | `#ffc5c8` `TO_VERIFY` |

### 4.4 WCAG AA contrast audit for the brand red

Formula: WCAG 2.1 relative-luminance contrast ratio,
`(L1 + 0.05) / (L2 + 0.05)`, where `L` is computed per
`https://www.w3.org/TR/WCAG21/#dfn-relative-luminance`. Values below
computed in Python with that exact formula:

| Pair | Ratio | AA normal (≥4.5) | AA large (≥3.0) |
|---|---|---|---|
| `#ec1b23` on `#ffffff` (light mode brand red) | **4.42:1** | borderline FAIL (–0.08) | PASS |
| `#ec1b23` on `#16272e` (dark mode bg, source red) | **3.48:1** | FAIL | PASS |
| `#ec1b23` on `#0f1419` (dark mode page bg, source red) | **4.19:1** | FAIL | PASS |
| `#ff5a60` on `#0f1419` (lift candidate A) | **6.07:1** | PASS | PASS |
| `#ff6b70` on `#0f1419` (**chosen lift**) | **6.69:1** | PASS | PASS |
| `#ff6b70` on `#16272e` | 5.61:1 (recomputed) | PASS | PASS |

**Findings:**

1. The source red on white is **4.42:1**, which is just below the AA
   normal-text threshold of 4.5:1. For *large text* (≥18pt or ≥14pt bold)
   and for *graphical UI controls* (which only need 3:1 per WCAG 1.4.11),
   `#ec1b23` is fine. **For body-text-sized red, do not rely on the brand
   red alone — pair it with weight 600+ and/or supplement with an
   underline / icon**. This matches innodisk.com's own usage (red is
   reserved for buttons, decorative slashes, and large headings).
2. On dark surfaces the source red **fails AA**. We lift it for dark mode
   only to **`#ff6b70` (6.69:1)** — still recognizably the Innodisk red,
   but bright enough to meet AA for any text size.
3. The lift is applied **only via the dark-mode override** of
   `--accent-primary`. The parent brand red is never altered in light
   mode.

---

## 5. Typography stack

Innodisk ships two production typefaces, both self-hosted as
`@font-face` declarations on innodisk.com. We adopt the same stack so the
doc site type-matches the corporate site.

### 5.1 Body (and default UI text)

```css
font-family:
  "Avenir Next LT Pro",
  "Noto Sans TC",      /* Traditional Chinese — Innodisk is Taiwanese */
  "Noto Sans SC",      /* Simplified Chinese */
  "Noto Sans JP",      /* matches innodisk.com :lang(jp) swap */
  "Noto Sans KR",      /* matches innodisk.com :lang(kr) swap */
  -apple-system, BlinkMacSystemFont,
  "Segoe UI", Roboto, "Helvetica Neue", Arial,
  sans-serif;
```

Weights to load: **400** (regular) and **600** (demi). These are the only
weights Innodisk loads (`AvenirNextLTPro-Regular.otf`,
`AvenirNextLTPro-Demi.otf`). Add an **italic 400** if the doc system needs
emphasis runs in body copy.

**Licensing note.** Avenir Next LT Pro is a Linotype/Monotype foundry
font and is **not free**. Innodisk has a corporate license to self-host
the OTF files. Two options for the doc site:

1. (Preferred, simplest) Mirror Innodisk's webfonts under
   `./docs/_static/fonts/` once the corporate license is confirmed to
   cover the doc-site domain. `TO_VERIFY` with Innodisk legal/IT before
   committing the binaries.
2. Fall back to a free near-equivalent if licensing isn't extended.
   Recommended substitute: **Inter** (variable, free, similar humanist
   sans). The `--font-family-avenir` token can be redefined per-deploy.

### 5.2 Display / headings

Innodisk uses **Barlow Condensed** (`--font-family-barlow`) for headlines
and feature numerals. It is **SIL OFL** — free to ship — so no licensing
worry:

```css
font-family:
  "Barlow Condensed",
  "Noto Sans TC", "Noto Sans SC",
  "Noto Sans JP", "Noto Sans KR",
  "Impact", "Arial Narrow", sans-serif;
```

Weights to load: **500** (medium) and **700** (bold). Use only for `h1`,
`h2`, and oversized hero numerals (e.g., "iQ Studio v1.0"). All h3 and
below stay in Avenir / Inter so the doc body doesn't get visually loud.

### 5.3 Monospace

**Choice: JetBrains Mono.**

Justification:

| Candidate | Verdict |
|---|---|
| **JetBrains Mono** | Designed for code; deep variable-weight axis; **distinguishes `0` / `O`, `1` / `l` / `I` cleanly** without leaning on programming ligatures; free (Apache 2.0); broad Latin Extended coverage; ships variable so we only pay for one file. **Pick.** |
| Fira Code | Excellent ligatures, but ligatures actively *hurt* a docs site (newcomers don't understand what `=>` renders as). Same readability otherwise. |
| IBM Plex Mono | Beautiful, but its `0`/`O` distinction is weaker and it carries IBM brand association that conflicts with Innodisk. |

```css
font-family:
  "JetBrains Mono",
  "SF Mono", "Menlo", "Consolas",
  "Liberation Mono", monospace;
```

Weights to load: **400** and **600**. Disable programming ligatures
(`font-variant-ligatures: none`) in the doc site CSS — docs readers
should see the literal source characters.

### 5.4 Full type scale

Mirrors Innodisk's own scale (`--font-size-h1`...`h5` from their
`:root`), expressed at the **64rem (lg)** breakpoint, which is the size
most users will see on a desktop docs page. Mobile values follow the
default `:root` scale, tablet uses the `48rem` scale.

| Token | Desktop (≥64rem) | Tablet (≥48rem) | Mobile | Line-height | Letter-spacing |
|---|---|---|---|---|---|
| `h1` | `4.375rem` / 70px | `4rem` / 64px | `3rem` / 48px | `1.14` | `-0.01em` |
| `h2` | `3.375rem` / 54px | `3rem` / 48px | `2rem` / 32px | `1.18` | `0` |
| `h3` | `2.125rem` / 34px | `1.875rem` / 30px | `1.5rem` / 24px | `1.2` | `0` |
| `h4` | `1.5rem` / 24px | `1.375rem` / 22px | `1.25rem` / 20px | `1.3` | `0` |
| `h5` | `1.1875rem` / 19px | `1.125rem` / 18px | `1.0625rem` / 17px | `1.5` | `0` |
| `h6` | `1rem` / 16px (derived) | same | same | `1.5` | `0.01em` |
| `body` | `1.0625rem` / 17px | same | same | `1.6` | `0.01em` |
| `small` | `0.9375rem` / 15px | same | `0.875rem` / 14px | `1.6` | `0.01em` |
| `caption` (derived `TO_VERIFY`) | `0.8125rem` / 13px | same | `0.75rem` / 12px | `1.5` | `0.02em` |
| `code` (mono) | `0.9375rem` / 15px | same | same | `1.5` | `0` |

**Notes for docs context:** docs sites use much larger doses of `h3`–`h6`
than marketing sites. Don't be tempted to upsize Innodisk's already-large
`h1`/`h2` for the docs landing page — keep them as specified so the doc
hero matches the corporate hero scale exactly.

---

## 6. Tone of voice

Innodisk writes like a **B2B industrial-grade engineering company**:
confident, technical, partner-oriented, with a small dose of marketing
energy ("lightning-fast", "blazing-fast"). The doc site should sound like
the same author writing **technical instructions** — preserve the
confidence and precision, **drop the marketing energy** for procedural
copy, **keep it** for landing/overview pages.

### Five do / don't pairs with example microcopy

| Surface | Don't (off-brand) | Do (on-brand) |
|---|---|---|
| **Primary CTA** | "Let's get started! 🚀" | "Get started" |
| **Empty state (no devices)** | "Looks like nothing's here yet... why not add one?" | "No devices detected. Connect a Q911 board over USB or run `iqs-launcher scan` to discover devices on the network." |
| **Error message** | "Oops! Something went wrong." | "Manifest fetch failed: HTTP 503 from `https://manifest.innodisk.com`. Retry, or switch to offline mode with `--manifest local`." |
| **Section intro (overview page)** | "Welcome to iQ Studio — your one-stop shop for everything edge AI!" | "iQ Studio is the shortest path from a powered-on Innodisk board to a running application. Use the Launcher to install platform images, fetch SDK packages, and run integration examples in one workflow." |
| **Warning callout** | "Heads up — be careful with this!" | "This command rewrites the device's eMMC. Back up `/data` before continuing." |

Operating principles:

1. **Address the engineer, not the procurement officer.** No "exceptional value across all sectors." Just "what to type, what to expect."
2. **Lead with verbs.** "Install...", "Run...", "Verify..." — never "You can now..." or "Feel free to..."
3. **Name the command, the file, the host.** If a sentence could apply to any product, rewrite it until it could only apply to iQ Studio on a Q911.
4. **Mirror Innodisk's collaborative framing** ("we believe that any challenge can be overcome through cooperation") on the *overview* and *contributing* pages — drop it from reference and how-to pages.
5. **Avoid emoji and exclamation marks** in body copy. They're absent from innodisk.com and they make industrial product docs feel toy-like.

---

## 7. Logo and favicon strategy

### 7.1 Top-bar logo

Asset: `./docs/fig/iq-studio-logo.png` (1133 KB, square format,
~1024×1024 nominal based on file size).

**Rendered specs:**

- Top-bar height: **64px** at desktop, **56px** at mobile.
- Logo height inside the bar: **40px desktop, 36px mobile** (i.e., bar
  height minus 12–16px of vertical padding so the rounded-square mark
  doesn't kiss the divider).
- Logo plus wordmark: render the PNG followed by the wordmark
  "**iQ Studio**" set in **Barlow Condensed 500**, 24px, color
  `--text-primary`, vertical-centered.
- **Clearspace:** minimum padding equal to **25 % of the logo height** on
  all four sides — i.e., for a 40px-tall logo, leave 10px of clear
  background around it.
- **Minimum render size:** 24px square. Below that, the slider strokes in
  the mark become unreadable; switch to a glyph fallback (see favicon).

**Dark-mode handling:**

The logo PNG is a **glossy mark on a near-white tile**. Inverting it to a
black tile would destroy the gradient legibility.

- **Light mode:** show the PNG directly on `--bg-page` (`#ffffff`).
- **Dark mode:** show the **same PNG** on the dark bar. Because the tile
  is `~#FAFAFA`, it sits as a slightly raised "card" against
  `--bg-surface` (`#16272e`) — which is actually a nice tactile effect
  and consistent with macOS dock icons. **No inverted asset is needed
  for v1.**
- **Flag for v1.1:** If product design wants a true dark-mode-native
  variant (transparent background, lighter inks, brighter slider
  handles), commission a `iq-studio-logo-dark.png` and reference it via
  CSS `prefers-color-scheme`. **`TO_VERIFY` — asset not yet produced.**

### 7.2 Favicon strategy

The full slider-icon mark **does not survive at 16×16 / 32×32** — the
three horizontal sliders blur into a single muddy band. The mark has no
naturally separable monogram. Recommendation: ship a **two-asset favicon
system**:

1. **At 180px and above** (apple-touch-icon, manifest 192, manifest 512):
   use the existing `iq-studio-logo.png` rescaled. The slider detail
   reads fine at these sizes.
2. **At 32px and below** (`favicon.ico` 16/32): ship a **monogram
   fallback**: the text "**iQ**" set in **Barlow Condensed 700**, white
   on a `#ec1b23` rounded-square (`border-radius: 22%`). This re-uses
   the parent brand red so the browser tab visually links to
   innodisk.com tabs.

**Required favicon assets to produce** (none exist in repo yet —
`TO_VERIFY`, all to be generated):

| File | Size | Source artwork | Notes |
|---|---|---|---|
| `/static/favicon.ico` | 16, 32 (multi-res ICO) | "iQ" monogram on `#ec1b23` | Browser tab |
| `/static/favicon-16.png` | 16×16 | monogram | Modern browsers |
| `/static/favicon-32.png` | 32×32 | monogram | Modern browsers |
| `/static/apple-touch-icon.png` | 180×180 | `iq-studio-logo.png` rescaled | iOS home screen |
| `/static/icon-192.png` | 192×192 | `iq-studio-logo.png` rescaled | PWA manifest |
| `/static/icon-512.png` | 512×512 | `iq-studio-logo.png` rescaled | PWA manifest, splash |
| `/static/icon.svg` (optional) | scalable | re-drawn vector of monogram | Modern browsers prefer SVG favicon |

Add to the doc-site `<head>`:

```html
<link rel="icon" type="image/svg+xml" href="/static/icon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/static/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/static/favicon-16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/static/apple-touch-icon.png">
<link rel="manifest" href="/static/site.webmanifest">
<meta name="theme-color" content="#ec1b23">  <!-- TO_VERIFY: not present on innodisk.com -->
```

---

## 8. Side-by-side mapping — Innodisk source → doc-site usage

Each row maps a concrete brand element from `innodisk.com` (or its
production CSS variable) to its concrete usage in the doc-site theme.

| # | UI element | Innodisk source (verbatim) | Doc-site light | Doc-site dark | CSS token to use |
|---|---|---|---|---|---|
| 1 | Page background | `body { background-color: var(--body-bg-color) }` resolves to `#fff` | `#ffffff` | `#0f1419` | `--bg-page` |
| 2 | Body text | `body { color: var(--body-text-color) }` resolves to `#000` | `#16272e` | `#f5f5f5` | `--text-primary` |
| 3 | Top-bar / nav background | innodisk.com nav is white over hero photography | `#ffffff` with `1px` bottom border `#e2e2e2` | `#16272e` with `1px` bottom border `#2a3a42` | `--bg-page` + `--border` |
| 4 | Top-bar logo lockup | `/images/logo.png`, ~40px tall | `iq-studio-logo.png` 40px + "iQ Studio" wordmark | same logo, white-text wordmark | n/a |
| 5 | Primary CTA / "Get started" button bg | `--color-primary #ec1b23` | `#ec1b23` | `#ff6b70` (AA-lifted) | `--accent-primary` |
| 6 | Primary CTA text | `--color-white #fff` | `#ffffff` | `#16272e` (dark-on-lifted-red is more readable at 6.7:1 than white-on-lifted-red) | `--text-inverse` (light) / `--text-primary` (dark) |
| 7 | Inline link | (Innodisk uses subtle red underlines + `--color-inno-blue #0046ff` for data) | `#0046ff` (`--color-inno-blue`) | `#5b8bff` (lifted) | `--link` |
| 8 | Visited link | n/a in source | `#be0078` (`--color-inno-magenta`) | `#d977b0` (lifted) | `--link-visited` |
| 9 | Headings (`h1`–`h6`) | typeset in Barlow Condensed at h1/h2, Avenir at h3–h6 | same; color `--text-primary` (`#16272e`) | same; color `#f5f5f5` | `--text-primary` + Barlow Condensed for h1/h2 |
| 10 | Body copy | Avenir Next LT Pro 400, 17px, line-height 1.6 | identical | identical | `--font-family-avenir` |
| 11 | Muted / caption | Innodisk uses `--color-inno-gray #959595` | `#4a4a4a` for body-sized muted text (AA), `#959595` for ≥18pt only | `#a8b0b6` | `--text-secondary` / `--text-muted` |
| 12 | Divider / hairline | `--color-inno-gray-light #e2e2e2` (used on `footer { border-top: 1px solid ... }`) | `#e2e2e2` | `#2a3a42` | `--border` |
| 13 | Code-block background | n/a (innodisk.com has no code blocks) | `#f5f5f5` `TO_VERIFY` | `#16272e` (re-use Innodisk's dark ink as our dark code bg — instant brand-fit) | `--code-bg` |
| 14 | Code-block text | n/a | `#16272e` | `#e2e2e2` | `--code-text` |
| 15 | Inline `<code>` | n/a | `#16272e` on `#f5f5f5` rounded-2px | `#e2e2e2` on `#1a2b33` rounded-2px | `--code-bg` + `--code-text` |
| 16 | Syntax — keyword | n/a | `#be0078` (magenta) | `#d977b0` | use `--color-inno-magenta` family |
| 17 | Syntax — string | n/a | `#007800` | `#00dc00` | `--color-inno-green*` |
| 18 | Syntax — comment | n/a | `#959595` | `#a8b0b6` | `--text-muted` |
| 19 | Syntax — function/number | n/a | `#0046ff` | `#5b8bff` | `--color-inno-blue*` |
| 20 | Callout — note | n/a | bg `#eef0f1` / border `#16272e` / text `#16272e` | bg `#1a2b33` / border `#2a3a42` / text `#e2e2e2` | `--callout-note-*` |
| 21 | Callout — info | n/a | bg `#e6efff` / border + text `#0046ff` | bg `#0a1d3d` / border `#5b8bff` / text `#cfdcff` | `--callout-info-*` |
| 22 | Callout — tip / success | n/a | bg `#e3f5ea` / border `#007800` / text `#006030` | bg `#0b2418` / border `#00dc00` / text `#bce8c8` | `--callout-tip-*` |
| 23 | Callout — warning | n/a | bg `#fff4d6` / border `#fabe23` / text `#7a4a00` | bg `#2a1f08` / border `#fabe23` / text `#ffe5a3` | `--callout-warning-*` |
| 24 | Callout — danger | n/a | bg `#fde7e8` / border `#ec1b23` / text `#b3151c` | bg `#2a0d0f` / border `#ff6b70` / text `#ffc5c8` | `--callout-danger-*` |
| 25 | Footer background | innodisk.com footer is dark (the only dark surface on the corporate site) — visible in CSS as `footer { border-top: 1px solid var(--color-black) }` over implied dark background | `#16272e` with `--text-inverse` text — this is the **one place light mode borrows the dark ink as a surface**, matching innodisk.com's own footer treatment | `#0f1419` | `--footer-bg` (= `--color-inno-blue-dark` in light, `--bg-page` in dark) |
| 26 | Focus ring | n/a in source | `2px solid #ec1b23` with `2px` offset | `2px solid #ff6b70` with `2px` offset | `--accent-primary` |
| 27 | Selection (text highlight) | n/a | `#ec1b23` @ 20% / text `#16272e` | `#ff6b70` @ 25% / text `#f5f5f5` | derived |
| 28 | Scrollbar thumb | n/a | `#e2e2e2` (hover `#959595`) | `#2a3a42` (hover `#4a5a62`) | `--border` |
| 29 | Sidebar bg | n/a | `#fafafa` (`--bg-surface`) | `#16272e` (`--bg-surface`) | `--bg-surface` |
| 30 | Active sidebar item | n/a | left-border `4px #ec1b23` + bg `#fde7e8` + text `#16272e` | left-border `4px #ff6b70` + bg `#2a0d0f` + text `#f5f5f5` | `--accent-primary` |

---

## 9. Implementation snippet (drop-in for the doc-site theme)

```css
/* ============================================================
   iQ Studio docs theme — derived from innodisk.com production CSS
   Pulled from /_nuxt/entry.FGUXsY83.css :root
   ============================================================ */
:root {
  /* Parent brand (verbatim from innodisk.com) */
  --color-white: #fff;
  --color-black: #000;
  --color-primary: #ec1b23;
  --color-inno-red: #ec1b23;
  --color-inno-gray-light: #e2e2e2;
  --color-inno-gray: #959595;
  --color-inno-blue: #0046ff;
  --color-inno-blue-light: #00b4ff;
  --color-inno-blue-dark: #16272e;
  --color-inno-orange: #ff6900;
  --color-inno-yellow: #fabe23;
  --color-inno-magenta: #be0078;
  --color-inno-pink: #f0f;
  --color-inno-green: #007800;
  --color-inno-green-light: #00dc00;

  /* Fonts (verbatim) */
  --font-family-avenir: "Avenir Next LT Pro", "Noto Sans TC",
    "Noto Sans SC", "Noto Sans JP", "Noto Sans KR",
    -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    "Helvetica Neue", Arial, sans-serif;
  --font-family-barlow: "Barlow Condensed", "Noto Sans TC",
    "Noto Sans SC", "Noto Sans JP", "Noto Sans KR",
    "Impact", "Arial Narrow", sans-serif;
  --font-family-mono: "JetBrains Mono", "SF Mono", "Menlo",
    "Consolas", "Liberation Mono", monospace;

  /* Doc-site semantic tokens — light */
  --bg-page: var(--color-white);
  --bg-surface: #fafafa;
  --bg-raised: #f5f5f5;
  --text-primary: var(--color-inno-blue-dark);
  --text-secondary: #4a4a4a;
  --text-muted: var(--color-inno-gray);
  --text-inverse: var(--color-white);
  --border: var(--color-inno-gray-light);
  --divider: #ececec;
  --accent-primary: var(--color-primary);
  --accent-primary-hover: #c8141b;
  --link: var(--color-inno-blue);
  --link-visited: var(--color-inno-magenta);
  --code-bg: #f5f5f5;
  --code-text: var(--color-inno-blue-dark);
  --footer-bg: var(--color-inno-blue-dark);
  --footer-text: var(--color-white);
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg-page: #0f1419;
    --bg-surface: var(--color-inno-blue-dark);   /* #16272e */
    --bg-raised: #1a2b33;
    --text-primary: #f5f5f5;
    --text-secondary: var(--color-inno-gray-light);
    --text-muted: #a8b0b6;
    --text-inverse: var(--color-inno-blue-dark);
    --border: #2a3a42;
    --divider: #1f2f37;
    --accent-primary: #ff6b70;                   /* AA-lifted from #ec1b23 */
    --accent-primary-hover: #ff8a8e;
    --link: #5b8bff;
    --link-visited: #d977b0;
    --code-bg: var(--color-inno-blue-dark);
    --code-text: var(--color-inno-gray-light);
    --footer-bg: var(--bg-page);
    --footer-text: var(--text-primary);
  }
}

body {
  background-color: var(--bg-page);
  color: var(--text-primary);
  font-family: var(--font-family-avenir);
  font-size: 1.0625rem;       /* 17px, matches innodisk.com --font-size-base */
  line-height: 1.6;
  letter-spacing: 0.01em;
}

h1, h2 { font-family: var(--font-family-barlow); font-weight: 700; }
h3, h4, h5, h6 { font-family: var(--font-family-avenir); font-weight: 600; }

code, pre { font-family: var(--font-family-mono); font-variant-ligatures: none; }

a { color: var(--link); text-decoration: underline; text-underline-offset: 2px; }
a:visited { color: var(--link-visited); }

.btn-primary {
  background: var(--accent-primary);
  color: var(--text-inverse);
  border: 0;
}
.btn-primary:hover { background: var(--accent-primary-hover); }

:focus-visible { outline: 2px solid var(--accent-primary); outline-offset: 2px; }
```

---

## 10. Quick implementation checklist

- [ ] Add the CSS snippet from §9 to the doc-site root stylesheet.
- [ ] Drop `iq-studio-logo.png` into the doc-site static path, render at
      40px in the top bar with the Barlow Condensed wordmark.
- [ ] Produce the 7 favicon assets listed in §7.2 (need design help —
      monogram on red square for ≤32px, scaled logo for ≥180px).
- [ ] Load Avenir Next LT Pro 400/600 and Barlow Condensed 500/700 — or
      substitute Inter 400/600 + Barlow Condensed 500/700 if Avenir
      licensing isn't extended to the doc-site domain.
- [ ] Load JetBrains Mono variable.
- [ ] Add `<meta name="theme-color" content="#ec1b23">`.
- [ ] Wire callouts (note / info / tip / warning / danger) to the tokens
      in §4.3.
- [ ] Re-export the diagrams in `./docs/fig/` to drop draw.io default
      colors in favor of Innodisk palette tints (deferred; not blocking).
- [ ] Pixel-sample `iq-studio-logo.png` to replace the §3 `TO_VERIFY`
      logo hexes with measured values.

---

*End of brand guide.*
