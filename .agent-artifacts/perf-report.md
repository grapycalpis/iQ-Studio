# iQ-Studio Documentation Site — Performance Report

**Date:** 2026-05-22
**Auditor:** Performance Benchmarker agent
**Site under test:** MkDocs Material build at `./site/` served via
`python3 -m http.server 8765 --directory site` on `http://127.0.0.1:8765/`.
**Tool:** Lighthouse 6.5.0 (CLI), Google Chrome 147.0.7727.137 headless.

## Methodology

- The repo's `./site/` directory was already built (`mkdocs build` output, MkDocs
  Material 9.5.39 per `overrides/main.html:144`). It was served by Python's stdlib
  `http.server` on port 8765 (no gzip / brotli — both relevant for byte-weight
  measurements below).
- Lighthouse was run **once per page per form factor** (mobile + desktop). Mobile uses
  Lighthouse 6.5's default Moto G4-class emulation (Slow 4G ≈ 1.6 Mbps, 150 ms RTT,
  CPU 4× slowdown). Desktop uses a custom config at `/tmp/lh-desktop.json`
  (10 Mbps, 40 ms RTT, 1× CPU). Single-run scores have ±2-5 noise; treat values as
  indicative, not authoritative.
- **Why Lighthouse 6.5 (not 10/11):** the only Node available on this host is
  v10.19.0 (`/usr/bin/node`). Modern Lighthouse requires Node 18+ and uses ESM /
  class fields that fail to parse on Node 10. LH 6.5 is the newest version that
  installs cleanly. It scores against the older v6 weighting (LCP/TBT/CLS, FCP,
  Speed Index, TTI; no INP — INP is reported below as "TBT" since LH 6.5 had not
  yet adopted INP). All other audits (render-blocking, modern-image-formats,
  uses-responsive-images, image-alt, color-contrast, canonical, tap-targets,
  document-title, robots) are present.
- **Canonical caveat:** every page declares `<link rel="canonical">` pointing at
  `https://innoipc-innodisk.github.io/iQ-Studio/...`. Because Lighthouse loaded the
  page from `http://127.0.0.1:8765`, the host mismatches and the canonical audit
  fails locally. **On production this audit passes** — the canonicals are correct
  per `overrides/main.html:175-177`. SEO scores below should be treated as ~5
  points conservative for this reason.

## Executive Summary

**Overall verdict: FAIL against the >95 target on Performance and SEO across all
three pages on both form factors.** Accessibility and Best Practices land at
92-94 — close but not at target.

The single dominant problem is **uncompressed, unsized images**:

1. **`tutorials/applications/iqs-vlm/fig/vlm-demo.gif` (18.4 MB)** is embedded
   directly on the homepage (`README.md:48`). On simulated mobile this single
   asset stretches LCP to **107.9 s** and TTI to **55.5 s**. This is by far the
   highest-impact single defect.
2. **`docs/fig/iq-studio-logo.png` (1.1 MB, 1024×1024)** is loaded on **every page**
   as the header logo, but rendered at ~24×24 in the chrome. ~1.05 MB is wasted on
   every navigation. This is the main reason why image-light pages (yocto, streampipe)
   still ship >1 MB.
3. **No `loading="lazy"` on inline `<img>` tags** in the `<table>` / raw-HTML
   layouts of `tutorials/starting-guides/q911/yocto.md` (12 images), `ubuntu.md`
   (8 images), `README.md`, etc. Every above-the-fold *and* below-the-fold image
   is fetched before LCP.

**Top 3 wins available (ranked by impact):**

1. **Replace `vlm-demo.gif` with an MP4 + poster JPG (`<video preload="none">`)**
   — saves ~18 MB on homepage, will lift mobile Perf from 36 → ~75+ and drop
   homepage LCP from 108 s to <3 s. Effort: S. Files: `README.md:48`,
   `tutorials/applications/iqs-vlm/fig/vlm-demo.gif`.
2. **Resize `iq-studio-logo.png` to a 192×192 PNG (≈10 KB) + add a 32×32
   favicon-class variant.** Saves ~1.05 MB per page on a site that already serves
   *every* page with this logo. Effort: S. Files: `docs/fig/iq-studio-logo.png`,
   `mkdocs.yml:55` (`theme.logo`).
3. **Add `loading="lazy"` and explicit `width`/`height` attributes to all `<img>`
   tags in raw-HTML blocks**, and start a PNG→WebP migration for the 30
   screenshots >500 KB (36.2 MB total). Effort: M. Files:
   `tutorials/starting-guides/q911/yocto.md` (12 imgs), `ubuntu.md` (8),
   `README.md` (5), various `tutorials/.../fig/*.png`.

## Pages Audited

| # | Page | URL (local) | Why chosen |
|---|------|------------|------------|
| 1 | Homepage | `http://127.0.0.1:8765/` | Renders `README.md` (the symlinked `src/index.md`) plus the persona-cards `<nav>` injected by `overrides/main.html:283-323`. Contains the worst single asset (`vlm-demo.gif`, 18.4 MB) and three diagram PNGs. Representative of the landing experience for first-time visitors. |
| 2 | Deep doc page | `http://127.0.0.1:8765/tutorials/starting-guides/q911/yocto/` | `tutorials/starting-guides/q911/yocto.md` — prose + 12 `<img>` tags in `<table>` layouts (no `alt`, no `loading="lazy"`, no width/height attrs — `style="max-height:100%; max-width:100%"` only). Representative of the high-detail walkthrough pages. |
| 3 | Page that links/embeds an mp4 | `http://127.0.0.1:8765/benchmarks/iqs-streampipe/` | `benchmarks/iqs-streampipe/README.md` references the 12 MB `fig/nv_qc_live.mp4` plus a 274 KB poster JPG. **The mp4 is rendered as a plain anchor (`<a href="…mp4">here</a>`), not as a `<video>` tag** (see "Video poster strategy" below). The 2.0 MB `Open WebUI demo.mp4` (with its 47 KB poster) is similarly *only present as a file*, not embedded. So no page on this site currently embeds a `<video>` element. |

## Lighthouse Results

### Scores (out of 100)

| Page | FF | Perf | A11y | BP | SEO | vs targets |
|---|---|---:|---:|---:|---:|---|
| Home | Mobile | **36** | 93 | 93 | 81* | **FAIL** Perf, FAIL A11y, FAIL BP, FAIL SEO (canonical artifact + tap-targets) |
| Home | Desktop | **44** | 93 | 93 | 83* | **FAIL** Perf, FAIL A11y, FAIL BP, FAIL SEO |
| Yocto | Mobile | **48** | 94 | 93 | 86* | **FAIL** Perf, FAIL A11y, FAIL BP, FAIL SEO |
| Yocto | Desktop | **82** | 94 | 93 | 83* | FAIL Perf (target 95), FAIL A11y, FAIL BP, FAIL SEO |
| Streampipe | Mobile | **48** | 92 | 93 | 79* | FAIL all |
| Streampipe | Desktop | **85** | 94 | 93 | 75* | FAIL all (video-heavy allowance: even at 90 floor, still FAIL) |

`*` SEO score is depressed by ~5 points because Lighthouse loaded the site from
`127.0.0.1` so the absolute `<link rel="canonical">` (pointing at
`innoipc-innodisk.github.io`) fails the `canonical` audit. **In production these
SEO scores should jump to ~85-91.**

### Core Web Vitals

(LH 6.5 reports TBT instead of INP. Targets shown are INP/TBT < 200 ms.)

| Page | FF | LCP | CLS | TBT | FCP | SI | TTI |
|---|---|---:|---:|---:|---:|---:|---:|
| Target | — | **<2.5 s** | **<0.1** | **<200 ms** | <1.8 s | <3.4 s | <3.8 s |
| Home | Mobile | **107.9 s ❌** | 0.018 ✅ | 110 ms ✅ | 4.5 s ❌ | 54.6 s ❌ | 55.5 s ❌ |
| Home | Desktop | **17.7 s ❌** | 0.006 ✅ | 10 ms ✅ | 1.0 s ✅ | 7.4 s ❌ | 9.2 s ❌ |
| Yocto | Mobile | **12.3 s ❌** | 0.014 ✅ | 80 ms ✅ | 4.4 s ❌ | 7.3 s ❌ | 7.7 s ❌ |
| Yocto | Desktop | **2.7 s ❌** | 0.005 ✅ | 0 ms ✅ | 1.0 s ✅ | 1.3 s ✅ | 1.6 s ✅ |
| Streampipe | Mobile | **11.9 s ❌** | 0.042 ✅ | 100 ms ✅ | 4.5 s ❌ | 6.5 s ❌ | 8.0 s ❌ |
| Streampipe | Desktop | **2.4 s ✅** | 0.006 ✅ | 10 ms ✅ | 1.0 s ✅ | 1.2 s ✅ | 1.6 s ✅ |

The pattern is uniform: **CLS and TBT pass everywhere** (this is a static doc site
with very little JS, and Material handles layout reservation reasonably). LCP and
FCP fail on every mobile run because three render-blocking stylesheets total
~165 KB and a third-party Google Fonts CSS round-trip is on the critical path,
and on mobile this adds up to ~2.85 s before first paint. **LCP then balloons on
the homepage because the 18.4 MB GIF is in the document and the browser fetches
it before paint settles.**

## Core Web Vitals Deep Dive

### LCP element per page

- **Home (mobile):** `<p class="ids-persona-card__desc">` — text inside the
  injected persona-cards `<nav>` (`overrides/main.html:290`). The LCP element
  itself is small text, BUT measured LCP is 107.9 s because Lighthouse defers the
  LCP timestamp until layout settles after the 18 MB GIF and the 1.1 MB logo
  finish loading. Once those are gone, LCP collapses to a sub-second range.
- **Yocto (mobile):** the first `<p>` in `article.md-content__inner` (the lead
  paragraph "This guide covers system interaction on Yocto Linux…"). Text-LCP.
  Measured at 12.3 s — bottlenecked by the 2.85 s render-blocking CSS chain plus
  the 1.1 MB logo download (header-logo is in the critical render path).
- **Streampipe (mobile):** the first `<p>` "This topic describes a multi-stream
  inference benchmark…". Same text-LCP pattern, same bottleneck.

**Insight: all three pages are text-LCP** (no hero image above the fold). That
means LCP improvements come from removing render-blocking CSS, deferring fonts,
and ridding the page of large eagerly-loaded assets — *not* from optimising a
specific hero.

### CLS sources

CLS passes on all six runs. Top shifters were:

- Homepage: `<a class="ids-persona-card">` and `.ids-persona-card__cta` (cumulative
  score 0.018). The persona cards have no explicit `min-height` and reflow once
  webfonts swap.
- Streampipe mobile: the LCP `<p>` itself (0.028) and the bullet list after
  (0.013) — both caused by font-swap reflow (see Font section).

No image-driven CLS detected because the raw `<img>` tags use `style="width:50%"`
or `style="max-width:100%"` and the table cells are constrained, so reserved
space is mostly stable. **Once `loading="lazy"` is added (recommendation §3),
make sure `width`/`height` HTML attributes are added at the same time** —
otherwise lazy images that scroll into view *will* introduce CLS.

### INP / TBT contributors

TBT is below 200 ms on every page (peak 110 ms on homepage mobile). The only
non-trivial scripts are:

- `assets/javascripts/bundle.525ec568.min.js` — Material's instant-loading +
  search bundle, 106 KB (108 KB transferred). Render-blocking-eligible but
  loaded with `defer` by Material.
- `search/search_index.json` — 82 KB XHR, loaded lazily for search.

Lighthouse reports **49 KiB of unused JS** in the Material bundle (mostly the
instant-nav, code-copy, and tab features that aren't exercised on the LCP). Not
worth ripping out — the JS isn't where the perf budget is going.

## Diagnostics

### Font loading strategy

**Current state (`site/index.html:34-38`, same on every page — Material default,
not customised):**

```html
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Inter:300,300i,400,400i,700,700i%7CJetBrains+Mono:400,400i,700,700i&display=fallback">
<style>:root{--md-text-font:"Inter";--md-code-font:"JetBrains Mono"}</style>
```

Findings:

- Fonts are **served from Google Fonts CDN**, not self-hosted. Three .woff2 files
  fetched per page (Inter, JetBrains Mono, Barlow Condensed) totalling ~92 KB.
- `preconnect` to `fonts.gstatic.com` is present (good). But no `preconnect` to
  `fonts.googleapis.com` — the CSS request is on the critical path and incurs a
  fresh TCP/TLS handshake. Lighthouse measured **780 ms** wasted on this request
  on mobile (see render-blocking table below).
- `display=fallback` is used. **This is the wrong choice for a doc site.**
  `fallback` gives a 100 ms block period and a 3 s swap period — fonts that
  download slowly (>3 s) NEVER swap in. The Material default elsewhere is
  `display=swap`. Recommendation: change to `swap`.
- No `<link rel="preload">` for the actual woff2 files. The browser doesn't
  discover them until after the CSS is parsed (~780 ms in on mobile). Preloading
  the two body weights (Inter 400, Inter 700) would shave several hundred ms off
  the font-swap event.
- **Barlow Condensed** is also fetched (14.6 KB woff2) but is **not declared in
  `mkdocs.yml:69-74`** (only Inter + JetBrains Mono are). It's pulled in by
  `assets/stylesheets/innodisk.css` and bills as a third-party font. If it's not
  used in body text, it can be dropped entirely.
- No font-subsetting. Each woff2 carries the full Latin glyph set (~47 KB for
  Inter alone). For an English-only doc site, a subset of `latin-ext` or just
  `U+0000-00FF + U+2026 + U+2014` etc. could halve the woff2 size — but only
  worth doing if fonts are self-hosted.

**Recommendations (file:line):**

1. `mkdocs.yml:69-74` — leave `theme.font.text: Inter` and
   `theme.font.code: JetBrains Mono` as-is, OR switch to Material's `font: false`
   mode and self-host. Self-hosting moves font bytes onto the same origin (skips
   the third-party DNS/TLS) and lets us preload them.
2. `assets/stylesheets/innodisk.css` — find and remove the Barlow Condensed
   `@import url(...)` (the woff2 is auto-loaded; without an import the
   `fonts.gstatic.com` request for it disappears).
3. To override the `display=fallback` (which is hard-coded in the Material 9.5
   theme), add the following to `overrides/main.html` inside the `extrahead`
   block (right after the favicons, ~line 168):

   ```html
   <link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>
   <link rel="preload" as="font" type="font/woff2" crossorigin
         href="https://fonts.gstatic.com/s/inter/v20/UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa1ZL7W0Q5nw.woff2">
   ```

   (The URL above is the actual one Material requested in the LH run; pin it or
   rely on Google's auto-redirect.)

### Image format (PNG → WebP)

**Quantified inventory** (across `docs/`, `tutorials/`, `benchmarks/`,
excluding the persona-icon SVGs in `assets/`):

| Format | Count | Total size | Notes |
|---|---:|---:|---|
| PNG | 72 | **41.13 MB** | 30 files are >500 KB (sum **36.2 MB** — i.e. 88% of all PNG bytes live in the top 30 files) |
| GIF | 7 | **94.48 MB** | Three copies of the same `gif0.gif`/`gif1.gif`/`gif2.gif` under `tutorials/applications/iqs-streampipe/fig/` and `tutorials/sdks/iqs-streampipe/fig/`. **vlm-demo.gif (18.4 MB) is on the homepage.** |
| MP4 | 2 | 13.36 MB | nv_qc_live.mp4 (11.4 MB), Open WebUI demo.mp4 (2.0 MB). Neither is embedded as `<video>` — see next section. |
| JPG | 3 | 1.76 MB | Two video posters (good) + og-default.png (which is named .png but the table doesn't count it here). |
| WebP | 0 | — | **None.** |
| AVIF | 0 | — | None. |

**Sample large-PNG analysis** (dimensions via `identify`, sizes via `stat`):

| File | Dim | Bytes | Displayed at | Verdict |
|---|---|---:|---|---|
| `docs/fig/iq-studio-logo.png` | 1024×1024 | 1,133,196 | ~24×24 in header (`md-logo` CSS, `site/index.html:174,317`), 30% width as hero (`README.md:10`) | **Egregious.** Should be a 192×192 PNG (~10 KB) for the hero hero and a 48×48 (~3 KB) variant for the header. Or convert to a 256×256 WebP (~6 KB). |
| `tutorials/starting-guides/q911/fig/ycoto_desktop_icon.png` | 1710×964 | 2,788,286 | `style="width:50%"` on a max-960 layout = ~480 wide | Resize to 960×541 and convert to WebP. Expected ~80 KB (97% reduction). |
| `tutorials/applications/iqs-streampipe/fig/image0.png` | 4880×2300 | 2,664,782 | `width="100%"` on max ~720 page width = ~720 wide | Resize to 1440×679 + WebP. Expected ~100 KB (96% reduction). |
| `tutorials/applications/iqs-vlm/fig/vlm-demo.png` | 1677×938 | 1,477,823 | `width="100%"` ~720 wide | Resize 1440 + WebP. ~120 KB. |
| `docs/fig/ai_on_dragonwing_sw_stack.png` | 4265×2668 | 292,503 | 80% width | Already reasonably sized in bytes (it's a flat diagram), but 4265 px is 6× more than rendered. Resize to 1440. ~110 KB. |
| `docs/fig/sw_development_pipeline.png` | 4416×1730 | 219,156 | 80% width | Resize to 1440. ~80 KB. |

**Estimated savings from PNG → WebP + resize:**

- **Header logo alone:** 1.13 MB → 6 KB × number-of-pages. There are 35 published
  pages (per `mkdocs.yml` nav). Aggregate first-visit savings across a tab-hopping
  session ≈ 35 MB (browser does cache after the first hit, so realistically
  ~1.1 MB savings per *cold* page load = roughly the entire current page weight
  for yocto/streampipe/most pages).
- **30 large PNGs:** measured aggregate 36.2 MB. WebP @ q=80 typically yields
  70-90% reduction on screenshots; assume 80% conservatively → ~7 MB. Net saving
  ~29 MB across the site.
- Lighthouse's `modern-image-formats` audit didn't fire on any page because the
  pages I sampled don't *load* the worst offenders inline (vlm-demo.gif is loaded
  on the homepage but it's already a GIF, not PNG, so the audit ignores it).

**How images are referenced today:**

- Markdown image syntax `![alt](./fig/foo.png)` is used in some places (see
  `README.md:48` — wait, that's HTML; `benchmarks/iqs-streampipe/README.md` has
  2 `![]` images).
- **Raw `<img>` HTML tags dominate** in walkthrough pages (`q911/yocto.md` has 12,
  `q911/ubuntu.md` has 8, `q911/README.md` has 9, `flash-image/README.md` and
  others). They use **inline `style="width:50%"` or `style="max-width:100%"`** but
  **no `width`/`height` HTML attributes, no `loading="lazy"`, no
  `decoding="async"`, and many have no `alt`** (Lighthouse `image-alt` failed on
  both yocto and streampipe; on homepage it flagged the logo `<img>` and the
  big GIF).

**Recommendations (file:line):**

1. **`docs/fig/iq-studio-logo.png`** — replace with two artifacts:
   - `docs/fig/iq-studio-logo.png` resized to 192×192 (or whatever the hero
     render size is on `README.md:10`).
   - A second 48×48 for the header-logo. Point `mkdocs.yml:55`
     (`theme.logo: docs/fig/iq-studio-logo.png`) at the small one. *This single
     change is the highest-leverage perf fix because the logo is on every page.*
2. **PNG → WebP migration.** Two acceptable strategies:
   - **A. Build-time conversion** with a `tools/convert_images.sh` that walks
     `docs/`, `tutorials/`, `benchmarks/`, and for every `*.png` > 100 KB emits a
     sibling `.webp` at q=80. Then a quick `sed` pass turns `.png` references into
     `.webp` (back up the originals). Effort: S.
   - **B. Markdown-friendlier:** emit `<picture>` wrappers so legacy clients still
     get PNG. More work, more HTML. For a doc site, strategy A is fine.
3. **Resize before encoding.** Most screenshots are 4× larger than display size.
   The `imagemagick` one-liner `mogrify -path . -resize 1440x\> -format webp -quality 80 *.png`
   handles this. Could be wrapped in `tools/compress_images.sh` (a sibling to
   the existing `tools/compress_gifs.sh`).
4. **For the walkthrough pages** (`q911/yocto.md`, `q911/ubuntu.md`,
   `q911/README.md`, `flash-image/README.md`, etc.) — replace every `<img src=…
   style="width:50%">` with `<img src=… width="480" height="270" loading="lazy"
   decoding="async" alt="…descriptive…">`. The explicit width/height (HTML attrs,
   not inline style) gives the browser intrinsic ratio for CLS-free lazy loading.

### Video poster strategy

**Findings:**

1. `benchmarks/iqs-streampipe/fig/nv_qc_live.mp4` (11.4 MB) is referenced in
   `benchmarks/iqs-streampipe/README.md:14` as **a plain link**:

   ```markdown
   please check [here](./fig/nv_qc_live.mp4).
   ```

   The neighbouring **`nv_qc_live-poster.jpg` (268 KB)** exists in the same dir
   but is not referenced anywhere. The user clicks the link and the browser
   either downloads the mp4 or opens it as a top-level page — no inline player.

2. `tutorials/applications/iqs-vlm/fig/Open WebUI demo.mp4` (2.0 MB) is **not
   referenced from any markdown** (`grep -rn "Open WebUI demo.mp4"` finds zero
   hits in the docs sources). The poster JPG (46 KB) exists but is orphaned.

3. `assets/stylesheets/innodisk.css:802-833` already defines a CSS component
   (`.md-typeset figure.ids-video`) intended for `<video controls preload="metadata"
   poster="…">` markup, complete with 16:9 framing and dark-mode treatment.
   **This component is currently unused.** It's a finished feature waiting for
   content.

4. `mkdocs.yml:101` enables `md_in_html` (comment: "raw `<video>` tags inside
   markdown (ia-design.md §6)"). The infrastructure is in place; the markdown
   never invokes it.

**Recommendations (file:line):**

1. **`benchmarks/iqs-streampipe/README.md:14`** — replace the plain link with the
   `ids-video` figure:

   ```html
   <figure class="ids-video" markdown>
     <div class="ids-video__frame">
       <video controls preload="none"
              poster="./fig/nv_qc_live-poster.jpg"
              width="1280" height="720">
         <source src="./fig/nv_qc_live.mp4" type="video/mp4">
         Your browser does not support the video tag.
         <a href="./fig/nv_qc_live.mp4">Download the video.</a>
       </video>
     </div>
     <figcaption>Live multi-stream YOLO inference on QCS9075.</figcaption>
   </figure>
   ```

   Key attribute: `preload="none"` — the 11.4 MB mp4 is not fetched until the
   user clicks play. The poster JPG (268 KB) is shown instead. **This gives the
   user a visual without paying the 11.4 MB tax on every page load.**
   The CSS already styles it (lines 802-833 of `innodisk.css`).

2. **`tutorials/applications/iqs-vlm/README.md`** — currently embeds
   `vlm-demo.gif` (18.4 MB) on line 16. **Replace it with an mp4-with-poster
   wrapper.** A 15-second GIF at the typical iQS-VLM dimensions transcodes to a
   ~1-2 MB H.264 mp4. (The companion 2.0 MB `Open WebUI demo.mp4` + 46 KB poster
   in the same dir suggests this is already the intended pattern.) Same goes for
   `README.md:48` (homepage uses the same gif).

3. **Optimise the poster JPGs.** `nv_qc_live-poster.jpg` is 268 KB — `mozjpeg
   -quality 75` typically takes it to ~60-90 KB at 1280×720. `Open WebUI
   demo-poster.jpg` at 46 KB is already fine.

4. **Consider WebP posters.** For poster images that are rarely above the fold,
   a WebP at q=80 will be 30-50% smaller than the equivalent JPG. Minor win.

### JS bundle size

**Measured (`find ./site -name "*.js" -printf "%s %p\n"`):**

- **`site/assets/javascripts/bundle.525ec568.min.js`** — 108,360 B (~106 KB
  transferred, no gzip). Material's main bundle (instant-nav, search, code-copy,
  palette toggle, tabs).
- **`site/assets/javascripts/workers/search.6ce7567c.min.js`** — 39,565 B,
  fetched as a worker only when search is invoked. Not on the critical path.
- **`site/assets/javascripts/lunr/wordcut.js`** — 677,463 B. **This is Thai
  word-segmentation data** for lunr-thai. It's enormous (660 KB raw) but
  it's only fetched if the user searches in Thai. With our nav containing only
  English content this file should never be requested. Confirmed via LH: not in
  any of the six network-requests lists.
- **30 small lunr language stemmers** under `site/assets/javascripts/lunr/min/`
  (Arabic, Turkish, Greek, Spanish, etc.), each 1-22 KB. Same story — fetched on
  demand only when search detects a non-English query. None loaded on the
  measured runs.
- **No custom JS in `overrides/` or `assets/`.** Nothing beyond what Material
  ships.

**Render-blocking analysis (Lighthouse `render-blocking-resources`):**

| Resource | Bytes | wastedMs (mobile) | Notes |
|---|---:|---:|---|
| `assets/stylesheets/main.8c3ca2c6.min.css` | 131,738 | ~3,000 ms | Material core CSS. Loaded as `<link rel="stylesheet">` in the document `<head>`. |
| `assets/stylesheets/innodisk.css` | 32,213 | ~1,080 ms | Site override. |
| `assets/stylesheets/palette.06af60db.min.css` | 12,709 | ~630 ms | Material palette (used for `custom` palette colors). |
| `https://fonts.googleapis.com/css?family=Inter…` | 1,308 | ~780 ms | Third-party Google Fonts CSS. |

Total **2.7-2.9 s of render-blocking** on mobile. No `<script>` is
render-blocking (Material's `bundle.525ec568.min.js` ships as `defer`).

**Unused JS:** Lighthouse reports ~46-49 KiB potential savings from
`bundle.525ec568.min.js` across all six runs. That's reasonable for a generic
theme bundle; not worth pursuing.

**Recommendations:**

1. **The render-blocking CSS chain is the real JS-side fix.** Specifically:
   - `innodisk.css` (32 KB) is a render-blocking 4th request and contributes
     ~1080 ms. Audit what's in it — anything that's only used below the fold or
     in print can be moved to a separate `print.css` (`media="print"`) or inlined
     critically.
   - The Google Fonts CSS (1.3 KB but 780 ms because it's third-party) can be
     replaced with a self-hosted `@font-face` block in `innodisk.css`. Eliminates
     two third-party requests entirely.
2. **Move search-worker pre-warm out of the critical path.** Material already
   does this. No action.
3. **Don't pre-fetch instant-navigation neighbours.** Currently `navigation.instant`
   is enabled (`mkdocs.yml:64`). This is fine — Material rate-limits these
   prefetches and they're idle-time only. Keep.

## Prioritized Recommendations

Numbered in descending impact. Estimates are based on the Lighthouse-measured
deltas (mobile, since mobile is where targets fail).

| # | Change | Impact | Effort | Files / lines |
|---|---|---|---|---|
| 1 | **Replace `vlm-demo.gif` with `<video preload="none" poster=…>` mp4.** Re-encode the 18.4 MB GIF as ~2 MB H.264 mp4 + generate a poster JPG. | Homepage **LCP 108 s → ~3 s, mobile Perf 36 → ~75**. Also fixes `iqs-vlm/README.md`. | S (transcode + 2 markdown swaps) | `README.md:48`, `tutorials/applications/iqs-vlm/README.md:16`, `tutorials/applications/iqs-vlm/fig/vlm-demo.gif` (replace) |
| 2 | **Resize `iq-studio-logo.png` to 192×192 + serve a 48×48 for the header.** Currently 1024×1024 / 1.1 MB. | **-1.05 MB / page on every page**; helps mobile LCP on yocto/streampipe by ~600-800 ms. | S | `docs/fig/iq-studio-logo.png`, `mkdocs.yml:55`, `README.md:10` (hero) |
| 3 | **Convert all PNGs >100 KB to WebP @ q=80 and resize to max 1440 px wide.** 30 PNGs → ~7 MB total (was 36.2 MB). | Page weight cut 70-90% on every walkthrough page. Mobile yocto LCP est. **12.3 s → 4 s**. | M (build script + bulk rename) | `tools/compress_images.sh` (new), `docs/fig/*.png`, `tutorials/**/fig/*.png`, `benchmarks/**/fig/*.png` |
| 4 | **Add `loading="lazy" decoding="async" width=… height=… alt="…"`** to every raw `<img>` HTML tag. | Cuts above-the-fold image bytes by ~50% on multi-image pages. Fixes A11y `image-alt` audit (currently 92-94 → 100). Locks in CLS. | M | 12 imgs in `tutorials/starting-guides/q911/yocto.md`, 8 in `ubuntu.md`, 9 in `q911/README.md`, 5 in `README.md`, dozens elsewhere |
| 5 | **Embed `nv_qc_live.mp4` as `<video preload="none" poster=…>` instead of a plain link.** | Eliminates broken UX (clicking link downloads/opens 11.4 MB); uses the existing 268 KB poster. | S | `benchmarks/iqs-streampipe/README.md:14` |
| 6 | **Self-host Inter + JetBrains Mono and drop Barlow Condensed.** Add `@font-face` in `innodisk.css` and `<link rel="preload">` in `overrides/main.html`. Switch `display=fallback` → `display=swap`. | -780 ms render-blocking on mobile. Mobile FCP est. **4.5 s → 3.0 s**. | M (find Material override hook for font URL) | `mkdocs.yml:69-74`, `overrides/main.html` (extrahead block ~line 168), `assets/stylesheets/innodisk.css` |
| 7 | **Fix tap-target overlap on homepage tables.** Persona-card grid tap targets currently overlap (LH flagged "GMSL Camera" / "MIPI Camera" 47×15 px adjacents). | A11y 93 → 100, mobile UX. | S | `README.md` table around line ~110 (where the per-tutorial nav table lives), or add CSS rule for `.md-typeset td > ul > li > a { padding: 12px 0; }` in `innodisk.css`. |
| 8 | **Fix heading-order violations on homepage.** `<h3>` jumps without `<h2>` in `README.md` (LH `5-165-H3` snippet `<h3 align="center">`). | A11y +1-2 points. | S | `README.md` — change the centered `<h3>` tagline to `<h2>` or strip semantic heading and use `<p class="hero-tagline">`. |
| 9 | **Add `<link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>`** (only googleapis is missing; gstatic is already there). Subsumed by #6 if fonts are self-hosted. | -100-300 ms TTFB on font CSS request, mobile only. | XS | `overrides/main.html` extrahead block. |
| 10 | **Compress the orphan `nv_qc_live-poster.jpg` (268 KB → ~80 KB) with mozjpeg.** | -200 KB once #5 ships. | XS | `benchmarks/iqs-streampipe/fig/nv_qc_live-poster.jpg` (re-encode in place). |
| 11 | **Audit `innodisk.css` (32 KB) for critical-vs-non-critical rules.** Inline `<style>` the above-the-fold rules (logo, nav, persona cards, body type) and `<link rel="stylesheet" media="print" onload="this.media='all'">` the rest. | -1080 ms render-blocking on mobile. | M | `assets/stylesheets/innodisk.css`, `overrides/main.html`. |
| 12 | **GIF cleanup beyond #1**: `tutorials/applications/iqs-streampipe/fig/gif0.gif` (18.8 MB) and `tutorials/sdks/iqs-streampipe/fig/gif0.gif` (18.8 MB, same file) are duplicated. Either symlink or move into a single canonical path and link both pages to it. Convert to mp4 as well. | -56 MB total repo / -36 MB on the affected pages once fetched. | S | `tutorials/applications/iqs-streampipe/fig/`, `tutorials/sdks/iqs-streampipe/fig/`. Note: `tools/compress_gifs.sh` already exists per the recent commit `3cad70f tools: add compress_gifs.sh to flag and re-encode oversized GIFs` — **run it on these files**. |

## Targets vs measured: summary verdict per page

| Page | Form factor | Targets met? | Notes |
|---|---|---|---|
| Homepage | Mobile | **FAIL** (Perf 36/95, A11y 93/95, BP 93/95, SEO 81/95; LCP 108 s/2.5 s; CLS ✅; FCP ❌) | Dominated by 18.4 MB GIF. After fix #1, will fail by less; needs fixes 2-3 to reach 90. |
| Homepage | Desktop | **FAIL** (Perf 44/95; LCP 17.7 s) | Desktop still pulls the GIF, just faster network. Same fixes apply. |
| Yocto | Mobile | **FAIL** (Perf 48/95; LCP 12.3 s) | After #2 + #3 + #4 + #6, projected 85-90. |
| Yocto | Desktop | **FAIL** (Perf 82/95; LCP 2.7 s) | Close. Fix #2 alone could push to 90+. |
| Streampipe | Mobile | **FAIL** (Perf 48/95) | After #2 + #3 + #4 + #6, projected 85-90. |
| Streampipe | Desktop | **FAIL** (Perf 85/90 video-allowance, LCP 2.4 s ✅) | A11y 94 fails 95 target by 1pt due to `color-contrast` on a code-block span. Easily fixable in `innodisk.css`. |

## Appendix: Raw data

- **Lighthouse JSON + HTML reports** (open the HTML files in a browser for the
  full report):
  - `./.agent-artifacts/lighthouse/home-mobile.report.html` + `.json`
  - `./.agent-artifacts/lighthouse/home-desktop.report.html` + `.json`
  - `./.agent-artifacts/lighthouse/yocto-mobile.report.html` + `.json`
  - `./.agent-artifacts/lighthouse/yocto-desktop.report.html` + `.json`
  - `./.agent-artifacts/lighthouse/streampipe-mobile.report.html` + `.json`
  - `./.agent-artifacts/lighthouse/streampipe-desktop.report.html` + `.json`
- **Lighthouse desktop config used:** `/tmp/lh-desktop.json` (extends
  `lighthouse:default` with desktop form-factor + 10 Mbps / 40 ms / 1× CPU).
- **Asset inventory summary:**
  - PNG: 72 files, 41.13 MB total; 30 files >500 KB account for 36.20 MB.
  - GIF: 7 files, 94.48 MB total (includes duplicates of gif0/gif1/gif2 in two
    iqs-streampipe locations).
  - MP4: 2 files, 13.36 MB total — neither embedded as `<video>`; both have
    poster JPGs already.
  - WebP / AVIF: 0 files.
  - Fonts: 0 self-hosted; 3 Google-Fonts woff2 (Inter, JetBrains Mono, Barlow
    Condensed) ~92 KB.
  - CSS: 175 KB total across 3 stylesheets (main 128 KB, innodisk 32 KB,
    palette 12 KB), all render-blocking.
  - JS: 106 KB Material bundle (deferred), 40 KB search worker (lazy), ~700 KB
    lunr language stemmers (lazy, never loaded on English nav).
