# iQ Studio Docs — Information Architecture Design

Source-of-truth inputs: [`./docs-inventory.md`](./docs-inventory.md) and [`./ux-research.md`](./ux-research.md). Every decision below traces back to a specific inventory item or persona journey. Personas referenced: **Wei** (system integrator), **Priya** (ML engineer), **Dan** (application/runtime developer).

Note on ordering authority: the inventory established (§6) that `tutorials/metadata.json` is **not** an IA descriptor — it is a launcher autotag→`run.sh` map. README is therefore the only ordering authority, and the inventory's recommended top-level nav (§5) overrides README in two places where README has known IA defects. Those overrides are flagged with **Why:** notes below.

---

## 1. Full sitemap

Tree below mirrors the inventory's recommended top-level nav (§5) and folder topology. Each leaf is annotated with its source file path so a sidebar generator can produce it mechanically.

- **Home** — `README.md` (slimmed) → published as `index.md`
  - **Why:** Inventory §8 recommends splitting `README.md` into a slim landing page (`index.md`) and an `overview.md`. Phase 1 ships this split.
- **Overview / Architecture** — new page, lifted from README's "Core Software Stack & Architecture" section
  - **Why:** Inventory §8. The QLI/BSP/kernel mapping is the deepest reference content in the repo and is currently buried inside the marketing README.
- **Getting Started** — `tutorials/starting-guides/README.md`
  - **Quickstart** — new page lifted from `README.md#quick-start` (Phase 1 stub; full lift in Phase 2)
    - **Why:** Inventory §4 P2 — "No dedicated Quickstart page; current quickstart is a section anchor in README."
  - **Q911 Platform Quick Start Guide** — `tutorials/starting-guides/q911/README.md`
    - **Yocto Linux Interaction Guide** — `tutorials/starting-guides/q911/yocto.md`
    - **Ubuntu Interaction Guide** — `tutorials/starting-guides/q911/ubuntu.md`
  - **Q911 Image Flashing Guide** — `tutorials/starting-guides/flash-image/README.md`
  - **Qualcomm OTA Guide** — `tutorials/starting-guides/ota/README.md`
- **Applications** — `tutorials/applications/README.md`
  - **iQS-VLM** — `tutorials/applications/iqs-vlm/README.md`
  - **iQS-Streampipe** — `tutorials/applications/iqs-streampipe/README.md`
  - **iQS-YOLOv10n** — `tutorials/applications/iqs-yolov10n/README.md`
- **SDKs** — `tutorials/sdks/README.md`
  - **iQS-OGenie: Run Your Own Demo with OGenie Server** — `tutorials/sdks/iqs-ogenie/README.md`
  - **iQS-VLM: Interact with OGenie via Open WebUI** — `tutorials/sdks/iqs-vlm/README.md`
  - **iQS-Streampipe: Change Custom Model and Video Source** — `tutorials/sdks/iqs-streampipe/README.md`
- **Model Deploy** — `tutorials/model-deploy/README.md`
  - **CV / YOLO26: Convert, Optimize, Infer** — `tutorials/model-deploy/cv/yolo26/README.md`
- **AVL (Approved Vendor List)** — `tutorials/avl/README.md`
  - **GMSL Camera** — `tutorials/avl/gmsl-camera/README.md`
  - **MIPI Camera** — `tutorials/avl/mipi-camera/README.md`
  - **Why (placement of children):** Inventory §1 + §4 P1 — the AVL hub has zero outbound `.md` links to its children. The sidebar must surface them even if the hub README does not, otherwise Persona A's Journey A2 dead-ends on the hub.
- **Benchmarks** — `benchmarks/README.md`
  - **InnoPPE: Jetson AGX vs. QCS9075** — `benchmarks/innoppe/README.md`
  - **Multi-stream Streampipe** — `benchmarks/iqs-streampipe/README.md`
  - **Perception Model** — `benchmarks/perception_model/README.md`
- **Reference**
  - **How to Use iqs-launcher** — `docs/how-to-use-iqs-launcher.md`
  - **(Phase 2)** Glossary — new page
  - **(Phase 2)** Troubleshooting — new aggregator page
    - **Why:** Inventory §4 P2 — both missing. Aggregator pulls from the `#known-issue` anchors in `tutorials/applications/iqs-streampipe/README.md` and `tutorials/sdks/iqs-streampipe/README.md` and the troubleshooting tail of `docs/how-to-use-iqs-launcher.md`.
- **Changelog** — `docs/changelog.md` *(rendered in sidebar footer slot, see §2)*

**Excluded from the published site:**
- `tools/README.md` — inventory §4 P1 marks this as an orphan and a contributor-internal doc, not user-facing. Excluded from Pages build. If the team wants it discoverable, it should live behind a `CONTRIBUTING.md` link in the repo root, not in user docs.

---

## 2. Sidebar design

### Top-level groups

The sidebar mirrors the §1 sitemap. Order is fixed (does not re-sort by recency or usage) so deep-linked readers (Persona A and B both arrive via deep links per ux-research §3) see a stable mental map.

| # | Group | Index page | Default state |
|---|---|---|---|
| 1 | Home | `index.md` | — (no children, single page) |
| 2 | Overview | `overview.md` | — (no children, single page) |
| 3 | Getting Started | `tutorials/starting-guides/README.md` | **Expanded by default** |
| 4 | Applications | `tutorials/applications/README.md` | Collapsed |
| 5 | SDKs | `tutorials/sdks/README.md` | Collapsed |
| 6 | Model Deploy | `tutorials/model-deploy/README.md` | Collapsed |
| 7 | AVL | `tutorials/avl/README.md` | Collapsed |
| 8 | Benchmarks | `benchmarks/README.md` | Collapsed |
| 9 | Reference | aggregator page | Collapsed |
| 10 | Changelog | `docs/changelog.md` | — (rendered as a separate footer-pinned link below the main groups) |

- **Why Getting Started is the only group expanded by default:** All three personas' Journey 1 (Wei A1 flash, Priya B1 evaluation→benchmarks, Dan C1 30-second demo) begin in this section or directly adjacent to it, and ux-research §3 ranks "homepage browse" as Medium-to-High for every persona. An expanded Getting Started reduces clicks for the most common first session.
- **Why Changelog is footer-pinned:** Inventory §4 P1 — "Changelog is a leaf orphan from the section graph … should still appear in the sidebar/footer nav." Pinning it below the main groups gives it persistent discoverability without diluting the top-level taxonomy.

### Active page highlight

- Active page: solid left-border accent (4px) in `--primary-color`, background tinted with `--bg-secondary`, text in `--text-primary` semibold.
- Active page's parent group: chevron rotated to expanded state and the group title rendered semibold; if the group is collapsed when navigation occurs, it auto-expands.
- Sibling pages of the active page: rendered at normal weight in `--text-secondary` color.
- Focus ring (keyboard tab): 2px outline in `--accent-color` for WCAG 2.1 AA.

### Depth limit

- **Hard depth limit: 3 levels** in the sidebar (group → page → sub-page). Inventory §1 confirms max graph depth is 3, so no group needs deeper nesting.
- Q911's `yocto.md` and `ubuntu.md` sit at depth 3 under "Q911 Platform Quick Start Guide". They render as indented children of the Q911 entry rather than as separate top-level pages.
- **Why no auto-generated heading-anchor links in the sidebar:** the in-page right-rail TOC (§3) handles intra-page navigation. Mixing both in the sidebar creates a noisy tree, especially for long pages like `tutorials/model-deploy/cv/yolo26/README.md` (159 lines, many H2s).

### Mobile / narrow-viewport behavior

- < 768px: sidebar collapses behind a hamburger; opens as a full-height overlay drawer with the same group structure.
- Active page is auto-scrolled into view inside the drawer on open.

---

## 3. Navigation rules

### Sidebar collapse behavior

- **Multi-open accordion**. Multiple groups can be expanded simultaneously. Single-open would force Wei to re-expand "Getting Started" every time he bounces over to "AVL" for camera info (Journey A2), which the inventory already flagged as a friction point.
- **Persisted across sessions** via `localStorage` key `iq-studio-docs:sidebar-state`. Storing per-group boolean (`{ "starting-guides": true, "applications": false, ... }`).
- **Auto-expand on navigation**: clicking a link inside a collapsed group expands that group; collapsing a group does not navigate.

### Right-rail in-page TOC

- Generated from `h2` and `h3` only. `h1` is excluded (it is the page title shown in the breadcrumb/header). `h4`+ are excluded — they add noise without aiding navigation.
- **Sticky** with `position: sticky; top: var(--header-height)`. Hidden under 1024px (TOC collapses to a "On this page" disclosure widget above the article body).
- **Auto-highlight current section** using `IntersectionObserver` with `rootMargin: '-20% 0px -70% 0px'` so a heading becomes "active" when it crosses the upper third of the viewport. Smooth scroll on click.
- **Why this matters most for the YOLO26 page:** `tutorials/model-deploy/cv/yolo26/README.md` is Priya's primary landing page (ux-research §3, "Preferred entry: Search-driven deep link"). A robust right-rail TOC lets her skip past intro material straight to the ADB push section — partially compensating for the P0 broken anchor (`#interact-with-the-system-using-adb-over-usb-type-c`) that currently breaks Journey B2.

### Breadcrumbs

- Format: `Home / <Group> / <Page> [/ <Sub-page>]`. Separator is a slash with 8px horizontal padding.
- Position: directly below the top nav header, above the page H1.
- Clickability: every segment except the last is a link to that page's index. Last segment is the current page name in `--text-primary`, not a link.
- Mobile: full breadcrumb collapses to "← <Parent>" only.
- **Why:** Wei (Journey A2) gets stranded on the AVL hub because the hub itself has no child links (inventory §4 P1). A clickable "Home / AVL" breadcrumb gives him a one-click escape back to a level where children are listed in the sidebar, even if the AVL hub README is not fixed pre-launch.

### Prev / Next page navigation

- Bottom of every content page. Order follows the sidebar (i.e. the §1 sitemap, depth-first).
- **Skips across group boundaries** (so reaching the last page of "Getting Started" → OTA puts "Next: Applications hub" on the next-button). Does **not** skip group hubs.
- Format: two-column footer, "← Prev: <Title>" left, "Next: <Title> →" right. If at start/end, the corresponding cell is empty (not a disabled button — visual asymmetry is intentional).
- **Why follow sidebar order, not link graph:** the link graph in inventory §9 is dense with cross-section back-references (e.g. q911 → applications, sdks, avl, benchmarks). Following the graph would create whiplash navigation. Sidebar order is the published reading path.

### "Edit on GitHub" link

- Rendered top-right of every content page, next to the H1.
- Resolves to: `https://github.com/InnoIPC-Innodisk/iQ-Studio/edit/main/<source-file-path>` where `<source-file-path>` is the exact path from §1 (e.g. `tutorials/starting-guides/q911/yocto.md`).
- For pages that don't yet exist as `.md` files (Phase 1 Quickstart, Phase 2 Glossary, Troubleshooting), the link points to the issue tracker with a pre-filled title `docs: contribute to <page>`.
- **Why `main` not the build SHA:** docs contributors expect to PR against `main`. Pinning to a build SHA would land them on a detached snapshot they cannot edit.

---

## 4. Search

### Trigger

- Keyboard shortcut: **⌘K** on macOS, **Ctrl+K** on Windows/Linux. Detected via `navigator.platform` / `navigator.userAgentData`.
- Visible search button in the top nav, right-aligned, label "Search docs ⌘K". Clicking opens the same modal.
- `/` as a secondary shortcut, opt-in via a setting (off by default to avoid hijacking native find).
- **Escape** closes the modal and restores focus to the trigger button.

### Index scope

- **Indexed**: page titles, all heading levels (`h1`–`h4`), body prose, code-block bodies, and image `alt` text.
- **Excluded from index**: HTML comments, the `<details>` summary attribute when collapsed (still indexed but de-weighted), the sidebar/breadcrumb/footer chrome.
- **Weighting**: title 10×, H1 8×, H2 4×, H3 2×, body 1×, code-block 1.5× (code blocks get a slight boost because Wei and Priya both search for exact commands — `iqs-launcher --autotag`, `EDL`, `fastboot`, `qmqui`).
- **Why include code blocks:** Persona C Journey C1 explicitly searches "iqs-launcher autotag" (ux-research §3). The autotag string only appears in code fences and inline code in `docs/how-to-use-iqs-launcher.md`.

### Result grouping

Results group by the top-level sidebar section, preserving sitemap order:

```
Getting Started        (3 hits)
  Q911 Quick Start Guide
    > … iqs-launcher --autotag iqs-vlm-demo …
  Yocto Linux Interaction Guide
    > … ADB over USB Type-C …

Model Deploy           (2 hits)
  CV / YOLO26: Convert, Optimize, Infer
    > …
```

- Group headers are non-clickable section labels.
- Each result shows: page title, breadcrumb, and a 2-line snippet centered on the matched term (term **bolded** in the snippet).
- Maximum 5 results per group on the initial render; "Show all in <Group>" link expands.

### Keyboard navigation

- `↑` / `↓` move selection across results (wraps within group, then to next group).
- `Enter` navigates to the selected result.
- `Tab` cycles into filter chips (see below); `Shift+Tab` reverses.
- Selected result has a 2px `--accent-color` ring and `--bg-secondary` background.

### Filter chips

Above the results, three optional filter chips: `Tutorials`, `SDKs & Apps`, `Benchmarks`. Clicking narrows the result groups. State does not persist across modal openings — each search starts fresh.

### Snippet preview behavior

- 160-character window centered on the first match within the indexed field.
- Match term is wrapped in `<mark>`, styled with `background: rgba(var(--accent-color-rgb), 0.25)`.
- For code-block matches, the snippet is rendered in a monospace font with `white-space: pre`, truncated to 160 chars.
- Multiple matches in the same page produce up to 2 snippet lines per result (separated by a faint divider) so Priya can see both "ADB" and "model push" hits on the same page without expanding.

---

## 5. Landing page

Inventory §1 Top recommendation and §8 explicitly recommend splitting `README.md`. Phase 1 ships this split. Landing page design follows.

### Hero (above the fold)

- **Headline**: `iQ Studio — the AI runtime launcher for Dragonwing edge devices.`
  - **Why this copy:** README currently uses "Show Performance, Spark Imagination" — strong marketing tone but light on what the product *is*. Grounded copy: the inventory describes iQ Studio as an AI runtime / launcher (`iqs-launcher --autotag <name>`) for Qualcomm Dragonwing-based edge devices (Q911, A100). The proposed headline preserves the marketing tagline as a sub-headline.
- **Sub-headline**: `Show Performance, Spark Imagination.` *(retained from current README)*
- **Primary CTA**: `git clone … && ./install.sh` rendered as a one-line copy-to-clipboard code block with a copy-icon button.
- **Secondary CTA**: "Flash a board in 10 minutes →" linking to `tutorials/starting-guides/q911/README.md`.

### Three persona entry cards

Card titles match the persona job names from `ux-research.md` §1. Card order follows the inventory's "Pick Your Path" three-column funnel (already validated copy):

| Card | Persona target | Card title | Body | Primary link |
|---|---|---|---|---|
| 1 | Wei | **Flash my device** | "Bring up a Q911 board, pick Yocto or Ubuntu, and confirm boot over ADB." | `tutorials/starting-guides/q911/README.md` |
| 2 | Priya | **Deploy a model** | "Convert and quantize your YOLO model, run it on the QCS9075 NPU, and compare against Jetson AGX Orin." | `tutorials/model-deploy/cv/yolo26/README.md` |
| 3 | Dan | **Explore SDKs** | "Customize iQS-Streampipe, iQS-VLM, or iQS-YOLOv10n — swap models, video sources, or wire up OGenie + Open WebUI." | `tutorials/sdks/README.md` |

- **Why Priya's card links directly to YOLO26, not the Model Deploy hub:** ux-research §3 marks the YOLO26 page as Priya's "Preferred entry … single most reference-dense AI page in the repo." Saving a click on the highest-intent entry point.
- **Why Dan's card links to SDKs hub, not a specific SDK:** Dan's three sub-journeys (C1 demo, C2 streampipe customize, C3 VLM OGenie) all converge on the SDKs hub. Letting the hub disambiguate is better than guessing his variant.

### Quick-link grid (predicted-traffic, grounded in ux-research journeys)

A four-column grid below the persona cards. Items are ordered by predicted total traffic across all three personas' journeys:

1. **Q911 Quick Start** → `tutorials/starting-guides/q911/README.md` *(Wei A1 + Priya B2 ADB step + Dan partial)*
2. **30-Second Demo (iqs-launcher)** → `docs/how-to-use-iqs-launcher.md` *(Dan C1 critical path; the only doc that explains autotag)*
3. **Image Flashing** → `tutorials/starting-guides/flash-image/README.md` *(Wei A1 deep-link target per ux-research §3)*
4. **YOLO26 Deploy** → `tutorials/model-deploy/cv/yolo26/README.md` *(Priya B2 highest-intent entry)*
5. **Multi-stream Benchmarks** → `benchmarks/iqs-streampipe/README.md` *(Priya B1 evaluation entry)*
6. **iQS-Streampipe (App)** → `tutorials/applications/iqs-streampipe/README.md` *(Dan C2 entry)*
7. **iQS-VLM (App)** → `tutorials/applications/iqs-vlm/README.md` *(Dan C3 entry, also Wei A2 exit handoff)*
8. **OTA Updates** → `tutorials/starting-guides/ota/README.md` *(Wei A3, even though P0 broken-link risk)*

### Recent-changelog widget

- **Include it.** A small "Recent updates" panel below the quick-link grid, showing the latest 3 entries from `docs/changelog.md`.
- **Why:** inventory §3 confirms changelog is an active leaf reachable from README, and recent commits ("split q911 guide by OS", "tools: add compress_gifs.sh") indicate the docs are evolving frequently enough that returning visitors benefit from a "what changed" surface. Footer-pin in the sidebar (§2) covers persistent discovery; this widget covers "what's new since I last visited."
- Parsing: regex-extract the top three `## <version>` blocks from `docs/changelog.md` at build time; render version + date + 1-line summary.

### What the landing page intentionally does NOT include

- **The long "Explore Documentation & Resources" HTML table** from current README. Inventory §8: "The HTML resource table in the current README's 'Explore Documentation & Resources' should be deleted entirely in the Pages context. Its job is replaced by the site's sidebar/nav."
- **The Core Software Stack & Architecture** section. Moves to `overview.md` per inventory §8.

---

## 6. Media handling strategy

The inventory's Appendix C (§11) catalogs: 1 referenced mp4, 1 orphan mp4, 1 github user-attachments video URL, and 7 GIFs. Strategy below addresses each class.

### MP4 files

- **Embed as HTML5 `<video>` with `poster` image, controls visible, NOT autoplay.**
  ```html
  <video controls preload="metadata" poster="fig/nv_qc_live-poster.jpg" width="100%">
    <source src="fig/nv_qc_live.mp4" type="video/mp4">
    <track kind="captions" src="fig/nv_qc_live.vtt" srclang="en" label="English" default>
    <p>Your browser does not support HTML5 video. <a href="fig/nv_qc_live.mp4">Download the video</a>.</p>
  </video>
  ```
- **Why click-to-play (controls-only) over autoplay-muted-loop:** the only currently-referenced mp4 (`benchmarks/iqs-streampipe/fig/nv_qc_live.mp4`) is a benchmark demo. Autoplay would steal attention away from the surrounding tables. The reader chose to come to a benchmarks page; let them choose when to play.
- **Build step:** ensure mp4 files are copied into the Pages build output (currently only linked as a plain href per inventory §11 — would 404 on Pages).
- **Orphan asset:** `tutorials/applications/iqs-vlm/fig/Open WebUI demo.mp4` is referenced by no `.md` (inventory §11). Either delete it or wire it into `tutorials/applications/iqs-vlm/README.md` as the demo embed. **Recommendation: wire it in** — it directly replaces the un-renderable github user-attachments URL in the companion SDK page (inventory §3, line 116). Rename to remove the space in the filename (`open-webui-demo.mp4`).

### GitHub user-attachments video URL

- **Problem:** `tutorials/sdks/iqs-vlm/README.md` line 34 embeds `https://github.com/user-attachments/assets/fda1d4a4-…`. This renders on github.com but is a bare URL on Pages (inventory §11, ux-research Persona C C1 break point).
- **Fix:** download the asset, store as `tutorials/sdks/iqs-vlm/fig/open-webui-interaction.mp4`, embed with the same `<video controls>` pattern. Add to `tools/compress_gifs.sh` companion or a sibling `tools/normalize_video_assets.sh`.

### GIF files

Seven GIFs ranging across applications, sdks, and model-deploy (inventory §11). The repo already ships `tools/compress_gifs.sh` (gifski-based, scans for files ≥ 20 MB) per recent commit `3cad70f`.

- **Render natively as `<img>`** when ≤ 2 MB. They are autoplay-loop by GIF format default — acceptable for short demos.
- **Lazy-load all GIFs** with native `loading="lazy"` attribute. Tutorial pages frequently embed GIFs below the fold (e.g. `tutorials/sdks/iqs-streampipe/README.md` has 2 GIFs).
- **For GIFs > 5 MB**, convert to `<video autoplay muted loop playsinline>` at build time (smaller payload, same visual behavior). The build script reads each GIF's file size and emits either an `<img>` tag or a `<video>` tag accordingly.
- **For GIFs > 10 MB**, render as a click-to-load placeholder: a static first-frame poster with a "▶ Play demo (12 MB)" overlay. Click swaps in the actual asset. This protects mobile readers and Priya on a tethered hotel-Wi-Fi search session.

### File-size thresholds (summary)

| Asset type | Threshold | Behavior |
|---|---|---|
| GIF | ≤ 2 MB | `<img loading="lazy">` direct |
| GIF | 2–5 MB | `<img loading="lazy">` + width-cap to keep layout stable |
| GIF | 5–10 MB | Convert to `<video autoplay muted loop playsinline preload="none" loading="lazy">` |
| GIF | > 10 MB | Click-to-load placeholder with file-size disclosed |
| MP4 | any | `<video controls preload="metadata" poster=...>` |
| PNG / JPG | > 200 KB | `loading="lazy"`; consider WebP conversion in Phase 2 |
| SVG | any | inline-able; no lazy load needed (already small) |

### Lazy-load mechanism

- Primary: native `loading="lazy"` attribute on `<img>` and `<iframe>`. Supported in all evergreen browsers.
- For `<video>`: use `preload="none"` + Intersection Observer to set `preload="metadata"` when within 200px of the viewport. Avoids fetching the poster image for off-screen videos.

### `prefers-reduced-motion`

- CSS media query honored globally:
  ```css
  @media (prefers-reduced-motion: reduce) {
    video[autoplay] { /* pause and show poster */ }
    img[src$=".gif"] { /* swap to a static first-frame png if available */ }
  }
  ```
- Build step generates a first-frame `.png` for every GIF and stores it alongside (`gif0.gif` → `gif0.first-frame.png`). The reduced-motion CSS swaps to the PNG.

### Captions and transcripts

- Every embedded `<video>` must ship a `<track kind="captions">` `.vtt` file. For Phase 1, if captions aren't ready, the build emits a warning but does not block.
- Long benchmark videos (`nv_qc_live.mp4`) should additionally have a prose transcript section below the embed describing the visible comparison. Inventory §11 calls this asset out as "headline 'live comparison' evidence."

### Accessibility for all media

- All `<img>` (including GIFs) must have a non-empty `alt`. Build-time lint blocks empty alts in tutorial pages.
- Decorative images (e.g. the logo) use `alt=""` explicitly to signal decorative.
- `aria-label` on `<video>` matching the surrounding caption text.

---

## 7. 404 page and empty-search-result copy

### 404 page

```
Headline:  This page doesn't exist (yet).

Body:      The docs site is still landing — some links from the old README
           may point to pages that have moved or haven't been published.
           Try one of these starting points, or use ⌘K / Ctrl+K to search.

Suggested links (clickable cards):
  • Q911 Quick Start Guide       → tutorials/starting-guides/q911/README.md
  • Deploy a YOLO model          → tutorials/model-deploy/cv/yolo26/README.md
  • Run the 30-second demo       → docs/how-to-use-iqs-launcher.md

Footer:    Found a broken link? [Report it on GitHub →]
           (links to: github.com/InnoIPC-Innodisk/iQ-Studio/issues/new?title=docs%3A+broken+link)
```

- **Why these three suggestions:** they map 1:1 to the three personas' preferred-entry pages from ux-research §3 (Wei → Q911 QSG, Priya → YOLO26, Dan → iqs-launcher how-to). A reader who 404s during initial research lands on one of them.
- **Why the "Report it on GitHub" footer:** the two P0 broken links in the inventory (OTA → `IQS.md`, YOLO26 → ADB anchor) will most likely surface as 404s during the migration window. Routing those reports to issues lets the team triage instead of losing them.

### Empty search-result copy

When `query.length > 0` and results are empty:

```
Headline:  No matches for "<query>".

Body:      Try a different term, or browse the docs by section.
           Popular searches:  iqs-launcher autotag · YOLO INT8 · ADB Type-C · OTA · Open WebUI

Browse-by-section fallback:
  [Getting Started]  [Applications]  [SDKs]  [Model Deploy]  [Benchmarks]
```

- **Why these popular searches:** each one is grounded in a specific persona journey term: `iqs-launcher autotag` (Dan C1, ux-research §3), `YOLO INT8` (Priya B2), `ADB Type-C` (Priya B2 break point + Wei A1 success state), `OTA` (Wei A3), `Open WebUI` (Dan C3).
- **Why include section chips:** ux-research's cross-cutting friction observation #1 — "Section hub pages are too thin to onboard." Even an empty-search state should give the reader a fast taxonomy escape, not just a "try different keywords" dead-end.
- **Initial empty state (query length 0):** show only the section chips and a faint "Type to search — titles, headings, prose, and code." hint, no popular-searches list (avoid keyword priming on first focus).

---

## Cross-references to the inventory

- Inventory P0 fixes (broken `IQS.md` link in OTA; broken ADB anchor in YOLO26) are **not** IA concerns per se — they're content fixes — but the IA design above mitigates both: the 404 page recovers the OTA case, the right-rail TOC + page-level "Edit on GitHub" link gives Priya a way to find the ADB section even if the anchor is broken.
- Inventory P1 fix (AVL hub missing child links) is **partially compensated for by the sidebar**: even before the hub README is fixed, the sidebar surfaces GMSL and MIPI children. The hub itself still needs the content fix before Wei's Journey A2 is fully unblocked.
- Inventory P2 missing pages (Quickstart, Glossary, Troubleshooting, FAQ): the IA reserves nav slots in §1 so they can be filled in Phase 2 without renumbering existing pages.

---

**Author**: ArchitectUX agent
**Design date**: 2026-05-22
**Phase 1 ship blockers**: AVL hub child links (inventory P1), README split into `index.md` + `overview.md` (inventory §8), OTA broken link content fix (inventory P0), YOLO26 ADB anchor retarget (inventory P0).
**Next handoff**: LuxuryDeveloper for design-system implementation (`css/design-system.css`, `css/layout.css`, `js/theme-manager.js`) per the foundation patterns in the agent's instruction file.
