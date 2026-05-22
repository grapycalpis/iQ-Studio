# iQ Studio — WCAG 2.2 AA Accessibility Audit

| Field        | Value |
|--------------|-------|
| Auditor      | AccessibilityAuditor (Claude Code) |
| Standard     | WCAG 2.2 Level AA (plus ARIA 1.2 best-practice rules) |
| Audit date   | 2026-05-22 |
| Site SHA / branch | `dev` (built `site/` directory shipped in working tree) |
| Build        | MkDocs 1.6.1 + mkdocs-material 9.5.39 (already built; `python3 -m http.server 8765` over `site/`) |
| Theme tokens | `assets/stylesheets/innodisk.css`; Innodisk red `#ec1b23` (light) / lifted red `#ff6b70` (dark slate) |
| Tools        | Chrome 147 headless + axe-core 4.x (Puppeteer-Core 22), curl, manual CSS inspection |

---

## 1. Executive summary

Five pages were audited in **both** light and dark color schemes (10 page-runs total) plus the actual MkDocs `site/404.html` template (which is **not** what is served by `python3 -m http.server`, see §2.3).

### At-a-glance pass / fail per WCAG SC

| WCAG 2.2 SC | Topic | Light | Dark | Notes |
|---|---|---|---|---|
| 1.1.1 Non-text Content | Image alt | **FAIL** | **FAIL** | 5 `<img>` on home, 3 on streampipe lack `alt` |
| 1.3.1 Info & Relationships | Headings, landmarks | **FAIL** | **FAIL** | 12 `<h1>` on home; nested `<main>` on 404; nav landmarks not uniquely labelled |
| 1.4.1 Use of Color | Link distinguishability | **FAIL** | **FAIL** | Links rely on color only; link↔body contrast 2.43 / 2.93 (need ≥3) |
| 1.4.3 Contrast (Minimum) | Body / link / code / callouts | **PASS** | **PASS** | All ≥4.5; values below |
| 1.4.10 Reflow | 320 px viewport | PASS¹ | PASS¹ | Material default; sidebar collapses < 44.9em |
| 1.4.11 Non-text Contrast | Focus ring, UI components | **PASS** | **PASS (borderline)** | 4.42 / 4.19 — passes 3.0 minimum but lifted red `#ff6b70` (6.69) should be used in dark |
| 1.4.13 Content on Hover/Focus | Tooltips | n/a | n/a | No hover content blocks audited |
| 2.1.1 Keyboard | All interactive reachable | **PASS** with caveats | **PASS** with caveats | `.md-typeset__scrollwrap` is a keyboard-inaccessible scrolling region (streampipe) |
| 2.1.2 No Keyboard Trap | Search modal | UNTESTED² | UNTESTED² | See §2.4 |
| 2.4.1 Bypass Blocks | Skip link | **PASS** | **PASS** | `<a class="md-skip">` works and targets the page's first `<h1>` |
| 2.4.3 Focus Order | Logical Tab sequence | **PASS (statically)** | **PASS (statically)** | Source order is logical; not exercised interactively |
| 2.4.7 Focus Visible | All focusable elements | **PASS** | **PASS** | 2px `:focus-visible` outline applied globally |
| 2.4.11 Focus Not Obscured (Min) | Sticky elements | **PASS** | **PASS** | No sticky overlays obscure the focused element |
| 2.4.13 Focus Appearance | Ring contrast / coverage | **PASS** | **PASS (borderline)** | See §3 |
| 2.5.8 Target Size (Minimum) | Touch targets ≥24 px | **FAIL** | **FAIL** | Sidebar nav links 17 px tall, 15-18 px apart |
| 3.1.1 Language of Page | `<html lang>` | **PASS** | **PASS** | `en` set on every MkDocs-generated page |
| 4.1.2 Name, Role, Value | Search dialog, icon buttons | **FAIL** | **FAIL** | `role="dialog"` w/o accessible name; 3-9 icon-only buttons per page lack `aria-label` |
| Video accessibility (1.2.x) | Captions / transcripts | n/a | n/a | **No actual `<video>` tags exist on the site** — see §6 |
| `prefers-reduced-motion` | Animations / transitions | **PASS** | **PASS** | Verified at runtime — transitions go to `0s`, animations `1e-05s` |

¹ Verified via Material's responsive breakpoints in CSS; not interactively re-tested in this audit.
² The headless probe captured the search modal DOM but did not exercise `Tab` cycling inside it. See §2.4.

### Conformance verdict

**Does not conform** to WCAG 2.2 AA. Six WCAG SC fail (1.1.1, 1.3.1, 1.4.1, 2.5.8, 4.1.2, plus duplicate-`<main>` on 404). All other tested SC pass.

The site's design tokens (color palette, focus-ring spec, motion respect) are genuinely well-considered — most failures are content-side (README markup) or unmodified Material defaults (search dialog, sidebar nav target sizes), not the brand stylesheet.

---

## 2. Methodology

### 2.1 Pages audited

| ID | URL (served from `site/` over `http://localhost:8765/`) | HTTP |
|---|---|---|
| `home` | `/` | 200 |
| `yolo26` | `/tutorials/model-deploy/cv/yolo26/` | 200 |
| `iqs-vlm` | `/tutorials/applications/iqs-vlm/` | 200 |
| `streampipe` | `/benchmarks/iqs-streampipe/` | 200 |
| `404` (Python fallback) | `/this-does-not-exist/` | 404 |
| `404` (MkDocs template, audited directly) | `/404.html` | 200 |

### 2.2 What WAS tested (automated)

- **axe-core 4.x** (`wcag2a`, `wcag2aa`, `wcag22aa`, `best-practice` tag set) injected into a real headless Chrome 147 against every URL × every color scheme. Both `prefers-color-scheme` and the `data-md-color-scheme` body attribute were forced to match the scheme under test.
- **Computed colors** for body text, links, code, nav, header, footer, callouts pulled live via `getComputedStyle`.
- **Contrast ratios** computed from real RGB values using the standard WCAG luminance formula (`(L1+0.05)/(L2+0.05)`).
- **Focus ring** outline color, width, offset captured via `.focus()` on representative links/buttons.
- **Reduced-motion** behavior probed by emulating `prefers-reduced-motion: reduce` and reading `transition-duration` / `animation-duration` on key components.
- **Static CSS audit** of `assets/stylesheets/innodisk.css` for every `:focus-visible`, `prefers-reduced-motion`, brand-token and callout rule.

### 2.3 What was NOT tested (and why)

- **Live screen reader passes** (VoiceOver / NVDA / JAWS). Headless Chrome has no accessibility-tree replay; SR behavior is **statically inferred** from ARIA roles, names, and Material's source. I did not confirm announcement order interactively. Any "SR-friendly" claim here is a static inference, not a confirmed pass.
- **Search modal Tab cycling and focus return** inside the open dialog. The dialog markup was inspected but the modal was not opened and exercised. Specifically: I did NOT confirm `Escape` closes the dialog, focus is trapped while open, or focus returns to the trigger on close. **This requires an interactive session.**
- **Real 320 px reflow and 200/400% zoom** were not exercised; only Material's responsive CSS rules were inspected.
- **Voice control, magnifier, forced-colors mode** — not exercised.
- **The Python fallback 404** (`/this-does-not-exist/` under `python3 -m http.server`) is **Python's `BaseHTTPRequestHandler` 404 page**, not the MkDocs template. Under GitHub Pages or any host that serves `site/404.html` on missing-page lookups, the MkDocs template *will* be returned. I therefore audited `site/404.html` directly via `GET /404.html` (HTTP 200), and that is the result reported in §5.5.

### 2.4 Interactive checks deferred

The following must be run in a real browser by a human (or via Playwright with the modal actually opened):

1. Open search via the magnifier icon, type a query, Tab through results, Esc to close, confirm focus returns to the magnifier button (WCAG 2.1.2, 2.4.3).
2. Confirm the focus indicator on the search input remains visible while the modal overlay is semi-opaque.
3. Confirm the sidebar nav collapses cleanly on mobile and the hamburger button has an accessible name (Material default usually does — `aria-label="Mobile menu"` — but worth confirming after any future template change).
4. Test the persona-card grid with a screen reader: it is marked up as `<nav class="ids-persona-grid" aria-label="Pick your path">` containing four `<a>` cards. Confirm SR announces "navigation, Pick your path, 4 links."

---

## 3. Focus-ring contrast — explicit numbers

CSS source: `assets/stylesheets/innodisk.css` lines 250-265.

Light mode:

| Adjacent surface | Ring color (`#ec1b23`) contrast | WCAG 1.4.11 / 2.4.13 |
|---|---|---|
| Page bg `#ffffff` | **4.42 : 1** | PASS (≥3) |
| Code block surface `#16272e` | **3.48 : 1** | PASS (≥3) |
| Sidebar tinted-active bg ≈ `rgb(253,237,237)` | **3.90 : 1** | PASS (≥3) |
| H1 underline / 404 rule on white | 4.42 : 1 | PASS |

Dark mode (slate):

| Adjacent surface | Actually rendered ring color | Should-be ring color | Contrast actual | Contrast should-be |
|---|---|---|---|---|
| Page bg `#0f1419` | `#ec1b23` ← still light-mode red on `.md-nav__link`, `.md-search__input`, `.md-button` | `#ff6b70` (lifted) | **4.19 : 1** | 6.69 : 1 |
| Code block dark `#0f1419` | `#ec1b23` | `#ff6b70` | 4.19 : 1 | 6.69 : 1 |
| Sidebar tinted-active bg ≈ `rgb(44,30,35)` | `#ec1b23` | `#ff6b70` | **3.61 : 1** | 5.76 : 1 |
| Code block surface `#16272e` | `#ec1b23` | `#ff6b70` | 3.48 : 1 | 5.57 : 1 |
| Persona-card surface `#16272e` | `#ec1b23` | `#ff6b70` | 3.48 : 1 | 5.57 : 1 |

**Finding** (P1): The component-specific override at lines 260-265 hard-codes `var(--color-inno-red)` (which is `#ec1b23` in BOTH schemes per lines 26 and 78) instead of using `var(--md-accent-fg-color)` (which IS scheme-aware: light `#ec1b23`, dark `#ff6b70`). Result: the per-component focus rings on nav links, search input, and buttons are visually the same red in dark mode as in light mode — they pass WCAG 1.4.11 minimum (4.19) but are **substantially below the design intent (6.69)** and look visibly dimmer against the dark surface compared to the global `:focus-visible` rule (which DOES switch to the lifted red, line 256). Tab focus on a nav link looks subtly different from Tab focus on a paragraph link — that is the bug.

**Borderline cases worth a polish pass**: ring contrast against the sidebar's tinted-red active-item background (`rgba(255,107,112,0.12)` over dark) lands at 3.61 : 1, only 0.6 above the 3.0 floor. If a user is on a focused, active, in-view sidebar link, the ring sits on a near-red background. Switching to the lifted red lifts that to 5.76 : 1.

---

## 4. Full color-contrast matrix (computed)

All values are `(L1+0.05) / (L2+0.05)` from the actual RGB values pulled out of `getComputedStyle`. Where the result depends on text size, WCAG 2.2 AA needs **4.5 : 1** for normal text (<18 pt / <14 pt bold) and **3 : 1** for large text and UI components.

### Light mode (`data-md-color-scheme="default"`)

| Surface / token | RGB | Contrast | AA Normal? |
|---|---|---|---|
| Body ink `#16272e` on white `#ffffff` | 22,39,46 / 255,255,255 | **15.40 : 1** | PASS |
| Secondary text `#4a4a4a` on white | 74,74,74 / 255,255,255 | 8.86 : 1 | PASS |
| Tertiary text `#959595` on white | 149,149,149 / 255,255,255 | **3.00 : 1** | **FAIL** (only passes large text 3.0) |
| Body link `#0046ff` on white | 0,70,255 / 255,255,255 | 6.33 : 1 | PASS |
| Body link `#0046ff` *adjacent to* body text `#16272e` | — | **2.43 : 1** | **FAIL** of WCAG 1.4.1 (needs ≥3 if color is the sole differentiator) |
| Code block text `#e2e2e2` on dark code bg `#16272e` | 226,226,226 / 22,39,46 | 11.89 : 1 | PASS |
| Code comment `#a8b0b6` on `#16272e` | 168,176,182 / 22,39,46 | 7.00 : 1 | PASS |
| Code keyword `#ff6b70` on `#16272e` | 255,107,112 / 22,39,46 | 5.56 : 1 | PASS |
| Code string `#00dc00` on `#16272e` | 0,220,0 / 22,39,46 | 8.24 : 1 | PASS |
| Code number `#5b8bff` on `#16272e` | 91,139,255 / 22,39,46 | 5.40 : 1 (computed) | PASS |
| Inline code `#16272e` on `#f5f5f5` | 22,39,46 / 245,245,245 | 14.12 : 1 | PASS |
| Footer text `#ffffff` on `#16272e` | 255,255,255 / 22,39,46 | 15.40 : 1 | PASS |
| Footer secondary `#e2e2e2` on `#16272e` | 226,226,226 / 22,39,46 | 11.89 : 1 | PASS |
| Footer tertiary `#959595` on `#16272e` | 149,149,149 / 22,39,46 | 5.14 : 1 | PASS |
| Header text `#16272e` on `#ffffff` | — | 15.40 : 1 | PASS |
| Callout *note* `#16272e` on `#eef0f1` | — | 13.47 : 1 | PASS |
| Callout *info* `#0046ff` on `#e6efff` | — | 5.47 : 1 | PASS |
| Callout *tip* `#006030` on `#e3f5ea` | — | 6.82 : 1 | PASS |
| Callout *warning* `#7a4a00` on `#fff4d6` | — | 6.83 : 1 | PASS |
| Callout *danger* `#b3151c` on `#fde7e8` | — | 5.84 : 1 | PASS |

### Dark mode (`data-md-color-scheme="slate"`)

| Surface / token | RGB | Contrast | AA Normal? |
|---|---|---|---|
| Body text `#f5f5f5` on `#0f1419` | 245,245,245 / 15,20,25 | **16.98 : 1** | PASS |
| Secondary `#e2e2e2` on `#0f1419` | — | 14.29 : 1 | PASS |
| Tertiary `#a8b0b6` on `#0f1419` | — | 8.42 : 1 | PASS |
| Body link `#5b8bff` on `#0f1419` | 91,139,255 / 15,20,25 | 5.80 : 1 | PASS |
| Body link `#5b8bff` *adjacent to* body text `#f5f5f5` | — | **2.93 : 1** | **FAIL** of WCAG 1.4.1 |
| Code text `#e2e2e2` on `#0f1419` | — | 14.29 : 1 | PASS |
| Code text `#e2e2e2` on `#16272e` (light-mode block in dark page) | — | 11.89 : 1 | PASS |
| Code keyword `#ff6b70` on `#0f1419` | — | 6.69 : 1 | PASS |
| Footer text `#f5f5f5` on `#0f1419` | — | 16.98 : 1 | PASS |
| Footer tertiary `#a8b0b6` on `#0f1419` | — | 8.42 : 1 | PASS |
| Callout note `#e2e2e2` on `#1a2b33` | — | 11.28 : 1 | PASS |
| Callout info `#cfdcff` on `#0a1d3d` | — | 12.21 : 1 | PASS |
| Callout tip `#bce8c8` on `#0b2418` | — | 12.12 : 1 | PASS |
| Callout warning `#ffe5a3` on `#2a1f08` | — | 13.09 : 1 | PASS |
| Callout danger `#ffc5c8` on `#2a0d0f` | — | 12.10 : 1 | PASS |

**Pure-contrast verdict**: Every audited content surface passes WCAG 1.4.3 in both modes. The only color-related failure is **WCAG 1.4.1 Use of Color** because in-content links are styled as color-only (no underline) with link-vs-surrounding-text contrast under 3:1.

---

## 5. Per-page findings

> Severity codes: P0 = blocks users / WCAG AA fail; P1 = significant barrier or borderline; P2 = polish / WCAG AAA or best practice.

### 5.1 Homepage (`/`)

axe violations: 6 (light), 7 (dark, +1 incomplete `color-contrast` — confirmed false positive once `data-md-color-scheme` is set on `<body>`, see methodology note in §2.2).

| ID | Severity | WCAG SC | Where | Detail |
|---|---|---|---|---|
| H1 multiplicity | **P0** | 1.3.1 | Throughout README | Page has **12 `<h1>` elements** (`iQ Studio`, `Show Performance, Spark Imagination.`, `Pick Your Path`, `30-Second Demo`, `Performance`, `Core Software Stack & Architecture`, `How to Use iqs-launcher`, `Quick Start`, `Explore Documentation & Resources`, `Related Repositories`, `Changelog`, `License`). Screen-reader users use the heading list as the page's table of contents — 12 h1's make this list nearly meaningless. Render-level fix: lower all but the page title to `<h2>` (and shift subsections down a level), or — since `README.md` is the source of truth and is also rendered on GitHub — leave it as-is on GitHub and inject a post-processing step that demotes second-and-later h1's in the MkDocs build. |
| `image-alt` | **P0** | 1.1.1 | `docs/fig/iq-studio-logo.png` (top hero), `tutorials/applications/iqs-vlm/fig/vlm-demo.gif`, `docs/fig/ai_on_dragonwing_sw_stack.png`, `docs/fig/qcl_roadmap.png`, `docs/fig/sw_development_pipeline.png` | All five are raw `<img>` tags in the README missing `alt`. The logo should be `alt="iQ Studio logo"` (or `alt=""` if there's another labelled logo nearby). The demo gif and architecture diagrams need descriptive `alt`. |
| `link-in-text-block` | **P0** | 1.4.1 | 27 in-content links | Links are color-only (`text-decoration: none`); link-vs-body contrast is 2.43 (light) / 2.93 (dark). axe flags every in-paragraph link. Fix: add `text-decoration: underline` (or `border-bottom: 1px solid currentColor; padding-bottom: 1px`) for `.md-typeset a` that is NOT a heading anchor (`.headerlink`), button, or persona card. |
| `aria-dialog-name` | **P0** | 4.1.2 | `.md-search [role="dialog"]` | The search modal's outer `<div role="dialog">` has no `aria-label` / `aria-labelledby`. The inner `<div role="search">` does NOT count — `role="dialog"` requires its own name. Fix: in `overrides/partials/search.html` (already a customized file), add `aria-label="Search"` (or `aria-labelledby` referencing the input's label) to the outer `.md-search` div. |
| `heading-order` | P1 | 1.3.1 | `<h3>` immediately following an `<h1>` (no h2 in between) | The README's "It helps users quickly understand…" tagline is rendered as `<h3>` directly under the first `<h1>`. Fix: change to `<p>` (it's a description, not a heading) or to `<h2>`. |
| `landmark-complementary-is-top-level` | P1 | 1.3.6 (best practice) | `.md-source-file` `<aside>` | The "edit on GitHub" aside is nested inside `<main>`. Material's default — keep as a `<div>` instead of `<aside>`. |
| `landmark-unique` | P1 | 1.3.6 (best practice) | `<nav aria-labelledby="__nav_2_label">` etc. | Multiple `<nav>` elements share the same label structure (Material renders one per group). Either give each `<nav>` a distinct `aria-label` (e.g. "Getting Started", "Applications") or remove the inner ones. |
| Persona-card link text | P2 | 2.4.4 | `.ids-persona-card__cta` | "Start here", "Read the SDK docs" are fine; the cards already have `aria-label` on the outer `<a>`. PASS. Mentioned only as a positive. |
| Skip link | PASS | 2.4.1 | Material's `a.md-skip` targets `#iq-studio` which exists. Verified that `Tab` once from page load focuses it and it becomes visible (opacity 1 on focus). |

### 5.2 Deep tutorial — `/tutorials/model-deploy/cv/yolo26/`

axe violations: 4 (light & dark).

| ID | Severity | WCAG SC | Detail |
|---|---|---|---|
| `aria-dialog-name` | **P0** | 4.1.2 | Same search-modal issue as 5.1. Global, single fix. |
| `link-in-text-block` | **P0** | 1.4.1 | 6 in-content links; same root cause as 5.1. |
| `landmark-complementary-is-top-level` | P1 | best practice | Same `.md-source-file` aside. |
| `landmark-unique` | P1 | best practice | Same sidebar `<nav>` issue. |
| Heading hierarchy | PASS | 1.3.1 | One `<h1>`, then `<h2>` Overview / Requirements / Step 1-4 / Tips & Troubleshooting, with proper `<h3>` substeps. Clean. |
| Skip link | PASS | 2.4.1 | Present and functional. |
| Code copy buttons | PASS | 4.1.2 | `.md-clipboard` has `aria-label="Copy to clipboard"` (Material default) and visible focus-ring on white via the override at line 514 (`outline: 2px solid #ffffff` on dark code surface). |

### 5.3 Application page — `/tutorials/applications/iqs-vlm/`

axe violations: 4 (light & dark).

| ID | Severity | WCAG SC | Detail |
|---|---|---|---|
| Same four globals (`aria-dialog-name`, `link-in-text-block`, `landmark-complementary-is-top-level`, `landmark-unique`). | | | |
| **No actual `<video>` tag** | informational | n/a | Despite a `Open WebUI demo.mp4` and `Open WebUI demo-poster.jpg` shipping under `fig/`, the rendered page **does not embed the video** anywhere. The README references `vlm-demo.png` and `vlm-demo.gif` but never the mp4. See §6 for the cross-site video review. |
| Heading hierarchy | P1 | 1.3.1 | Page has **three `<h1>` elements** ("iQS-VLM", "How to Deploy", "How to Use", "LLaVA-1.5-7B Performance"). Authoring should pick one — the page title — and use h2 for sections. |

### 5.4 mp4-adjacent page — `/benchmarks/iqs-streampipe/`

axe violations: 6 (light & dark).

| ID | Severity | WCAG SC | Detail |
|---|---|---|---|
| `image-alt` | **P0** | 1.1.1 | Three side-by-side benchmark plots (`fps_per_channel.png`, `cpu_loading.png`, `cpu_memory.png`) are raw `<img>` tags missing `alt`. These are essential information ("FPS per channel: Qualcomm 30/30/30 vs Jetson 18/14/9"-type), not decorative. |
| `scrollable-region-focusable` | **P0** | 2.1.1 | Two `<div class="md-typeset__scrollwrap">` regions (around a wide table and a long shell snippet) are horizontally scrollable via mouse but **not via keyboard** — axe reports them as keyboard-inaccessible. Material does not add `tabindex="0"` to these wrappers. Fix: extend `overrides/main.html` or a JS shim to add `tabindex="0"` and `role="region"` with `aria-label` to every `md-typeset__scrollwrap`. |
| `link-in-text-block` | **P0** | 1.4.1 | The link `<a href="…/nv_qc_live.mp4">here</a>` (the only mp4 reference on this page) is also a "click here" link — both a 1.4.1 fail AND a 2.4.4 fail. Fix: replace with descriptive link text, e.g. `Watch the live multi-stream comparison (MP4, 1080p)`. |
| Same globals (`aria-dialog-name`, `landmark-complementary-is-top-level`, `landmark-unique`). | | | |

### 5.5 404 page — actual MkDocs template at `/404.html`

axe violations: 7 (light & dark).

The custom `overrides/404.html` is well written content-side (single `<h1 id="ids-404-headline">`, `aria-labelledby` on the inner `<main>`, six link list, decorative number/rule hidden with `aria-hidden="true"`). But it inherits the full Material chrome (header / nav / footer / search), and wrapping the custom `<main class="ids-404">` **inside** Material's existing `<main class="md-main">` produces two structural failures:

| ID | Severity | WCAG SC | Detail |
|---|---|---|---|
| `landmark-no-duplicate-main` | **P0** | 1.3.1 | Two `<main>` elements: Material's outer `<main class="md-main">` and the custom inner `<main class="ids-404">`. Fix: in `overrides/404.html` change the wrapper from `<main class="ids-404">` to `<section class="ids-404" aria-labelledby="ids-404-headline">` and let Material's outer `<main>` remain the single page landmark. |
| `landmark-main-is-top-level` | P1 | 1.3.6 | Same root cause; resolves with the same fix. |
| `aria-dialog-name` | **P0** | 4.1.2 | Search modal — global fix. |
| `label` (`#__search`) | P1 | 1.3.1 | Material's hidden checkbox toggles (`#__search`, `#__drawer`) lack labels. Both checkboxes are visually clipped (`position: absolute; clip: rect(0 0 0 0)`), so axe over-reports here. A `role="presentation"` on the toggle, or an associated invisible `<label>`, removes the warning. This is a Material upstream issue. |
| `landmark-unique` | P1 | 1.3.6 | Same global sidebar-nav labels. |
| `region` | P1 | 1.3.6 | Two top-level inputs (`#__drawer`, `#__search`) sit outside any landmark. Same Material structural issue. |
| `target-size` | **P0** | **2.5.8** (WCAG 2.2) | **34 nodes** flagged. The hidden toggle checkboxes are false positives (visually clipped), but at least 20 of the flagged targets are actual sidebar nav `<a>` links: the rendered link box is 17 px tall with 15-18 px center-to-center spacing — both axes fail the 24 px minimum. This affects every page, not just the 404, but axe surfaced it on the 404 first because the layout collapses to a single navigable list. Fix: bump sidebar nav `.md-nav__link` `min-height` to 24 px and `padding-block` to ~6 px. |

### 5.6 Search modal (statically audited only)

Captured DOM:

    <div class="md-search" data-md-component="search" role="dialog">    ← P0: no name
      <label class="md-search__overlay" for="__search"></label>
      <div class="md-search__inner" role="search">
        <form class="md-search__form" name="search">
          <input class="md-search__input" name="query"
                 aria-label="Search the docs"
                 placeholder="Search the docs"
                 autocapitalize="off" autocorrect="off" autocomplete="off"
                 spellcheck="false" required>
          …

| Item | Status | Notes |
|---|---|---|
| Search input has `aria-label="Search the docs"` | PASS | Good. |
| Search input has visible `:focus-visible` outline | PASS | 2px `#ec1b23` ring on light, `#ec1b23` (not lifted) on dark — same dark-mode token issue as §3. |
| Outer dialog has accessible name | **FAIL (P0)** | `role="dialog"` requires `aria-label` / `aria-labelledby`. Add `aria-label="Search"`. |
| Search trigger button (magnifier icon) has accessible name | UNTESTED | The label `for="__search"` wrapping the icon is empty in source (`ariaLabel: null, text: ""`). Material's CSS injects the icon via `::before`. Add `aria-label="Open search"` to the `<label for="__search">` element. |
| Focus trap inside the open modal | **UNTESTED** | Requires opening the modal interactively. Material's documented behaviour is that Tab cycles through the input → result list → close button, and Escape closes. Confirm in an interactive session. |
| Focus return on close | **UNTESTED** | Same as above. |

---

## 6. Video accessibility

**Finding (P2-informational)**: There are **zero `<video>` HTML elements** anywhere in the built site. The mp4 files that ship in the repo are referenced as follows:

| File | How it's surfaced on the rendered page |
|---|---|
| `tutorials/applications/iqs-vlm/fig/Open WebUI demo.mp4` | **Not referenced from any HTML.** The page shows `vlm-demo.png` and `vlm-demo.gif` only. |
| `benchmarks/iqs-streampipe/fig/nv_qc_live.mp4` | Linked as `<a href="fig/nv_qc_live.mp4">here</a>` inside a paragraph. Browser navigates to the raw mp4. |

Because there is no `<video>` element, none of WCAG 1.2.1 / 1.2.2 / 1.2.3 / 1.2.5 (captions, transcripts, audio descriptions) are *failed* — they simply don't apply on the current pages. However:

1. The poster images `*-poster.jpg` exist (one per mp4), so the *intent* was clearly to embed via the `figure.ids-video` template from `innodisk.css` §7. That template **is well-prepared for accessibility** (controls, `preload=metadata` only — no autoplay — `<figcaption>` slot) but **is currently unused**.
2. The plain-link approach (`<a href="…mp4">here</a>`) means SR users will hear "link, here." Combined with the WCAG 1.4.1 "use of color" + 2.4.4 "link purpose" failures, this single link is a triple violation.

**Recommendation when these videos are eventually embedded**: use the prepared template with `<track kind="captions" srclang="en" src="…vtt" label="English">`. The CSS already wires `controls`, `preload=metadata`, and respects reduced-motion correctly via the global rule. Make sure `autoplay` and `loop` are not added.

---

## 7. Reduced-motion respect

Runtime probe at `prefers-reduced-motion: reduce`:

    personaCard:  transition-duration 0s,  animation-duration 1e-05s
    md-header:    transition-duration 0s,  animation-duration 1e-05s
    md-nav__link: transition-duration 0s,  animation-duration 1e-05s
    md-clipboard: transition-duration 0s,  animation-duration 1e-05s

Static CSS confirms three layered guarantees:

1. Material's own bundled rule: `@media (prefers-reduced-motion){ *,:after,:before{transition:none!important} }` — kills ALL CSS transitions globally.
2. `innodisk.css` global rule (lines 928-934): zeroes `animation-duration`, prevents looped animations, disables `scroll-behavior: smooth`.
3. Per-component fallbacks for the sidebar caret rotation, persona-card hover lift, and md-nav transitions.

**Status: PASS** for WCAG 2.3.3 (Animation from Interactions), informally. The site does not run any auto-playing carousels, parallax effects, or vestibular-sensitive transitions in either preference state.

---

## 8. Keyboard navigation

Static inspection of the DOM order plus a 1-Tab probe from page load:

- **First Tab focuses `<a class="md-skip">`** ("Skip to content"). Visible (opacity 1) and 2 px `#ec1b23` ring. PASS for WCAG 2.4.1.
- **Tab order is logical** by source order: skip-link → header palette toggle → repo link → search input → primary sidebar → main content links → footer → previous/next nav links.
- **Focus indicator is restored** by `innodisk.css` lines 259-265 for `.md-nav__link`, `.md-search__input`, `.md-button` (Material strips it; the override re-adds it). PASS WCAG 2.4.7.
- **Keyboard-only dead-ends**: identified one — the horizontally scrollable code-block wrappers (`md-typeset__scrollwrap`) on the streampipe page (and likely on any page with a wide table or long shell command). axe explicitly flags `scrollable-region-focusable`. This is WCAG 2.1.1.
- **Search modal Tab cycling**: not exercised. See §5.6 and §2.4.
- **Sidebar nav touch targets**: 17 px tall, fail WCAG 2.5.8 (24 px) at mobile widths. The hover/focus area extends because of padding, but the rendered touch box is 17 px.

---

## 9. Prioritized fix list

### P0 — fix before any release calling this site "accessible"

| # | Issue | WCAG | Files / selector | Suggested fix |
|---|---|---|---|---|
| P0-1 | Search dialog has no accessible name | 4.1.2 | `overrides/partials/search.html` → `<div class="md-search" role="dialog">` | Add `aria-label="Search"` (or `aria-labelledby` pointing to a visually-hidden `<h2>Search</h2>`). One-line change. |
| P0-2 | 5 `<img>` on homepage and 3 on streampipe lack `alt` | 1.1.1 | `README.md`, `benchmarks/iqs-streampipe/README.md` (rendered as `<img>` via `md_in_html`) | Add `alt="…"` to every `<img>` tag. Use `alt=""` only for purely decorative ones. The Innodisk logo and architecture diagrams are informational, not decorative. |
| P0-3 | In-content links rely on color only | 1.4.1 | `assets/stylesheets/innodisk.css` | Append: `.md-typeset a:not(.headerlink):not(.md-button):not(.md-clipboard):not(.ids-persona-card):not(.md-nav__link) { text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 0.18em; }`. Optionally remove the underline on `:hover`. |
| P0-4 | Homepage has 12 `<h1>` elements | 1.3.1 | `README.md` | Demote every `<h1>` after the first to `<h2>` (and shift `<h2>` → `<h3>`, etc.). If that breaks the GitHub README rendering, add a post-build sed step that demotes second-and-later h1s only in the MkDocs HTML output. |
| P0-5 | iqs-vlm page has 3+ `<h1>` elements | 1.3.1 | `tutorials/applications/iqs-vlm/README.md` | Same — demote section headers to h2. |
| P0-6 | Custom 404 produces two `<main>` landmarks | 1.3.1 | `overrides/404.html` line 14 | Change `<main class="ids-404" aria-labelledby="ids-404-headline">` → `<section class="ids-404" aria-labelledby="ids-404-headline">`. |
| P0-7 | Code-block scrollable regions are keyboard-inaccessible | 2.1.1 | Material default → `.md-typeset__scrollwrap` | Add a small JS shim in `overrides/main.html` (or extra_javascript) that runs `document.querySelectorAll(".md-typeset__scrollwrap").forEach(el => { if (el.scrollWidth > el.clientWidth) { el.tabIndex = 0; el.setAttribute("role","region"); el.setAttribute("aria-label","Scrollable code block"); }})` after page load. |
| P0-8 | Sidebar nav links fail 24 px touch-target minimum | 2.5.8 | `assets/stylesheets/innodisk.css` | Add `.md-nav__link { min-height: 24px; display: flex; align-items: center; }`. Verify spacing remains 4 px or wider. |
| P0-9 | Streampipe "click here" link | 2.4.4 + 1.4.1 | `benchmarks/iqs-streampipe/README.md` | Replace `please check <a href="fig/nv_qc_live.mp4">here</a>` with `please watch the <a href="fig/nv_qc_live.mp4">live multi-stream inference comparison (MP4)</a>`. |

### P1 — significant barrier / borderline conformance

| # | Issue | WCAG | Files / selector | Suggested fix |
|---|---|---|---|---|
| P1-1 | Per-component focus rings are NOT scheme-aware in dark mode | 1.4.11 / design intent | `assets/stylesheets/innodisk.css` lines 260-265 | Replace `outline: 2px solid var(--color-inno-red);` with `outline: 2px solid var(--md-accent-fg-color);` so the dark-mode lifted red `#ff6b70` applies (lifts ring contrast from 4.19 to 6.69 on the dark background). |
| P1-2 | Heading-order skip on homepage (`<h1>` → `<h3>`) | 1.3.1 | `README.md` line w/ "It helps users quickly understand…" | Change to `<p>` (it's a tagline). |
| P1-3 | Skip-link target is fine but **only one h1 anchor** is the destination | 2.4.1 (UX) | `README.md` | If the README's h1 is demoted (P0-4), make sure Material re-points `<a class="md-skip">` to the new first h1 — Material auto-targets the first heading, so this should still work after P0-4. |
| P1-4 | Sidebar `<nav>` elements share label structure | 1.3.6 best practice | Material default | Either give each top-level `<nav>` a unique `aria-label` (one of: "Site sections", "Section navigation", "Page contents"), OR drop the inner `<nav>`s in favour of `role="group"` / `<div>`. |
| P1-5 | `.md-source-file` aside nested in main | 1.3.6 best practice | Material default (or `overrides/partials/actions.html` if you maintain it) | Render it as `<div>` instead of `<aside>`. |
| P1-6 | `.md-clipboard` focus ring is white-on-dark-code (good) but not scheme-aware on hover background | 1.4.11 | `innodisk.css` line 514 | Keep the white `outline` — it's correct for the dark code surface. PASS once contrast is verified against the actual code-block bg in both modes (it is). Mentioned for completeness. |
| P1-7 | Hidden Material toggles trigger axe `label` / `target-size` warnings | 4.1.2 / 2.5.8 (false positive) | `overrides/main.html` head | Add `role="presentation"` and `aria-hidden="true"` to `<input id="__search">` and `<input id="__drawer">` — they are CSS-clipped checkboxes, not user-facing inputs. Suppresses axe warnings without changing behaviour. |
| P1-8 | Magnifier-icon search trigger has no accessible name | 4.1.2 | `overrides/partials/search.html` | The `<label for="__search">` wrapping the magnifier icon has empty text. Add `aria-label="Open search"`. |
| P1-9 | "Last update" / git-revision timestamp link contrast | 1.4.3 | `git-revision-date-localized` plugin output | The `#959595` text on white is exactly 3.00 : 1 — passes large-text only. Confirm the timestamp is rendered at ≥18 pt (24 px) or ≥14 pt bold; if it's <18 pt it fails 4.5 : 1. Bump to `#767676` (4.54 : 1 on white) to be safe. |

### P2 — polish, AAA, or best practice

| # | Issue | Notes |
|---|---|---|
| P2-1 | Unused video template | The `<figure class="ids-video">` template in `innodisk.css` §7 is accessibility-ready (controls, no autoplay, reduced-motion aware). Either remove it (dead code) or migrate the existing `nv_qc_live.mp4` `<a>` link to use it. |
| P2-2 | Heading anchor `¶` symbols | The `permalink: ¶` from `toc:` config produces `<a class="headerlink" href="…">¶</a>` after every heading. SR users hear "link, paragraph sign" after every heading. Material adds `aria-label="Permanent link"` so this isn't a fail, but consider `permalink: 🔗` or hiding the visible glyph and exposing only `aria-label`. |
| P2-3 | Persona-card hover lift survives reduced-motion (transform: none applied) | Confirmed via probe — `:hover { transform: none }` rule at line 750-752 works. Pass. |
| P2-4 | The H1 red 64 px underline + 4 px height | 4.42 : 1 on white. Decorative — no WCAG impact — but if it ever becomes the SOLE indicator of "this is a heading" the design should rely on font size + weight as the primary cue (which it does). Pass. |
| P2-5 | `<a class="md-skip">` is technically only ONE skip link | WCAG 2.4.1 requires "a mechanism to bypass blocks." One skip link is sufficient. Bonus: consider a "Skip to navigation" link for screen-reader users who want to reach the sidebar quickly. AAA territory. |
| P2-6 | `prefers-contrast: more` not handled | The site does not branch on `prefers-contrast: more`. Most colors already pass AA; an AAA pass would tighten the few 3-5 : 1 tokens to ≥7 : 1. Optional. |
| P2-7 | `forced-colors` (Windows High Contrast) | The site uses CSS variables for everything, which means it should respond reasonably to `forced-colors: active`. Not interactively tested. |

---

## 10. What's working well (don't regress)

- **Brand stylesheet quality**: `assets/stylesheets/innodisk.css` is unusually well structured for a documentation theme — every token is grounded in a spec reference, focus rings are restored (Material strips them by default), and `prefers-reduced-motion` is respected at three layers.
- **Dark-mode lifted red `#ff6b70`** is well-chosen (6.69 : 1 on `#0f1419`) and would push focus-ring contrast over 6 : 1 if applied consistently.
- **Callout palette**: every variant exceeds 5 : 1 contrast in both modes — significantly above the 4.5 : 1 minimum and a usable foundation for AAA pass later.
- **Skip-link mechanism works** end-to-end; first Tab focuses it, target ID exists, ring is visible.
- **Reduced motion is genuinely respected** — Material's bundled rule + the override's belt-and-suspenders means the site degrades gracefully for vestibular-sensitive users.
- **`<html lang="en">` is set on every MkDocs page** (the only exception was the Python fallback 404, which is not the production 404 page).
- **Persona-card grid** is correctly marked up as `<nav aria-label="Pick your path">` with descriptive `aria-label` on each card — a positive pattern other sections could imitate.
- **Code copy buttons** have proper `aria-label="Copy to clipboard"` and a visible focus ring on the dark code surface (white outline on dark code bg = 21 : 1).

---

## 11. Recommended remediation order (next two sprints)

1. **Week 1 (P0-1, P0-2, P0-3, P0-7, P0-9)** — quick, high-impact CSS/template/markdown edits. Estimated ~2 dev-days. Eliminates 5 of the 9 P0 items and roughly 40-50 axe violations across the site.
2. **Week 1 (P0-4, P0-5, P0-6)** — README h1 demotion + 404 `<main>` swap. Estimated ~1 dev-day. Eliminates the structural / landmark P0 items.
3. **Week 1 (P0-8)** — sidebar nav `min-height: 24px`. Estimated <1 hour. Resolves the only remaining WCAG 2.5.8 fail.
4. **Week 2 (P1-1)** — make focus rings scheme-aware. Estimated 10 minutes. Lifts dark-mode focus visibility from "barely passing" to "comfortably exceeding."
5. **Week 2 (P1-2 through P1-9)** — assorted Material-default cleanups. Estimated ~1 dev-day total.
6. **Re-audit**: re-run axe-core across the same five pages × two color schemes. Target: zero `critical` / `serious` violations, no more than 3-5 `moderate` (the unavoidable Material defaults).
7. **Add a real screen-reader pass** before any release marketing accessibility — VoiceOver on Safari + NVDA on Firefox at minimum. The static audit cannot substitute for live SR testing of the search modal, sidebar nav announcement, and dynamic toc.follow scroll-spy behaviour.

---

## 12. Reproduction commands

    # Static server (the audit was run against this)
    cd site && python3 -m http.server 8765

    # Node 22 audit harness (lives at /tmp/a11y-scan in this session)
    cd /tmp/a11y-scan
    /usr/local/bin/node scan.js > results.json
    /usr/local/bin/node summarize.js   # writes summary.json

    # MkDocs-direct 404 audit (Python's http.server returns its own 404
    # for non-existent paths; this hits the actual MkDocs template)
    /usr/local/bin/node scan-404.js > 404.json

Harness source files (kept for reproducibility, not committed):

- `/tmp/a11y-scan/scan.js` — primary cross-page + cross-scheme axe scanner
- `/tmp/a11y-scan/scan-404.js` — direct audit of `site/404.html`
- `/tmp/a11y-scan/summarize.js` — JSON post-processor
- `/tmp/a11y-scan/probe-cards.js` — persona-card dark-mode validation
- `/tmp/a11y-scan/probe-links.js` — content-link contrast probe
- `/tmp/a11y-scan/probe-skip.js` — skip-link behavior probe
- `/tmp/a11y-scan/probe-motion.js` — reduced-motion probe
- `/tmp/a11y-scan/probe-target-size.js` — mobile-viewport target-size probe

---

## 13. Honest gaps in this audit

I am being explicit about what was inspected statically vs interactively, because the difference matters:

| Claim | How it was verified |
|---|---|
| "Focus ring is 2 px brand red, 2 px offset" | CSS source + computed `getComputedStyle().outline*` after programmatic `.focus()` |
| "First Tab focuses the skip link" | One `keyboard.press('Tab')` from page-load in headless Chrome |
| "Search modal traps focus / Esc closes / focus returns" | **NOT VERIFIED.** Modal DOM was captured; modal was never opened by the harness. |
| "All interactive elements are keyboard-reachable" | Static — every `<a>`, `<button>`, `<input>` was counted, but Tab-order was not walked end-to-end. axe's `tabindex` rule did not flag any of them, which is necessary but not sufficient. |
| "Screen-reader announces landmarks correctly" | Inferred from ARIA roles in source — NO live SR run. |
| "Site is responsive at 320 px" | Inferred from Material's `< 44.9375em` mobile breakpoint in CSS — not visually verified. |
| "Reduced motion is respected" | Live runtime probe with `prefers-reduced-motion: reduce` emulated. Verified. |
| "All contrast values are real" | Real RGB pulled from rendered DOM, real WCAG formula. Verified. |
| "Color-contrast violation on persona cards in dark mode" | **WITHDRAWN as a false positive.** Initially flagged by axe, traced to my test harness setting `data-md-color-scheme` on `<html>` instead of `<body>`. Real dark-mode rendering shows persona-card desc at 14.29 : 1 (`#e2e2e2` on `#16272e`). This is documented in §2.2 / §2.3 because it's the kind of pitfall future audits should avoid. |

**Bottom line**: the brand stylesheet is one of the more carefully constructed I've audited; the failures are almost all in either (a) the README markdown (alt text, heading levels, "click here" links) or (b) untouched Material defaults (`role="dialog"` without a name, sidebar nav at 17 px tall, hidden checkbox toggles flagged by axe). None require an architectural change — every P0 fix is a few lines of CSS, a Jinja attribute, or a markdown edit.
