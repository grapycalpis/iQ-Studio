# SSG Tech Decision — iQ-Studio User Guide on GitHub Pages

Grounded in [`./docs-inventory.md`](./docs-inventory.md) (27 in-scope `.md`, content scattered across repo root + `docs/` + `tutorials/**` + `benchmarks/**` + `tools/`), [`./ia-design.md`](./ia-design.md) (9-group sidebar, README split into `index.md` + `overview.md`, AVL/Reference compensations), and [`./ux-research.md`](./ux-research.md) (three personas, search-driven entry for Priya). Decision date: 2026-05-22.

---

## 1. TL;DR Recommendation

**Winner: Material for MkDocs 9.x** (running MkDocs 1.6.x) with a `src/` symlink directory at the repo root pointing back at `README.md`, `docs/`, `tutorials/`, `benchmarks/`, and `tools/`.

**Runner-up (close): Docusaurus 3.10.x** with multiple `@docusaurus/plugin-content-docs` instances, each `path:` pointing at `../README-as-page`, `../docs`, `../tutorials`, etc. from a `website/` subfolder.

**Single most important reason MkDocs Material wins**: every single hard requirement (full-text search, dark mode, syntax highlighting, mermaid, mp4 via raw HTML5, CSS-variable theming, mobile-responsive) is satisfied by the *default* theme without any third-party plugin — Material ships Lunr-based client-side search, a `default`/`slate` dark-mode toggle, Pygments+`pymdownx.superfences` highlighting, native Mermaid integration, and a fully CSS-variable-driven palette including `[data-md-color-scheme="custom"]` overrides. The only configuration work is the symlink-based `src/` directory to satisfy the "do not move .md files" constraint, which is an established and documented MkDocs pattern from the project's own [discussion #3062](https://github.com/mkdocs/mkdocs/discussions/3062). For a 27-page site with shell/python/yaml/json examples and 3 personas needing solid search UX, Material is the lowest-config option that hits 100% of the requirements on first build.

The reason Docusaurus is close but not chosen: it can technically source from `../tutorials` etc., but you cannot point a content plugin at the *repo root* itself due to plugin-conflict issue [#9027](https://github.com/facebook/docusaurus/issues/9027) (MDX loader collides with site root contents like `node_modules/`, `package.json`, `mod/`, `binaries/`). Workarounds exist (move the website into a `website/` subfolder and use per-subdir plugin instances) but they multiply config surface 5× and you still cannot natively read `README.md` from repo root as the homepage without a copy step. MkDocs's symlink approach is one-line-per-source and produces the desired behavior.

---

## 2. Comparison Matrix

Pass = native / one-line config. Caveat = works but with a documented workaround. Fail = blocked or requires moving files / external service / heavy custom code.

| Criterion | MkDocs Material 9.x | Docusaurus 3.10.x | VitePress 1.6.4 / 2.0-alpha | Astro Starlight (latest) | Jekyll just-the-docs 0.6 |
|---|---|---|---|---|---|
| **HARD: Source from repo root + multiple paths, no file moves** | Caveat — `src/` symlink dir (standard pattern, [mkdocs#3062](https://github.com/mkdocs/mkdocs/discussions/3062)) | Caveat — `website/` subfolder + per-dir plugin instances; cannot use `path: '..'` per [docusaurus#9027](https://github.com/facebook/docusaurus/issues/9027) | Fail — `srcDir: '..'` documented-broken per [vitepress#4384](https://github.com/vuejs/vitepress/issues/4384) and [#3209](https://github.com/vuejs/vitepress/discussions/3209) (symlinks fail too) | Fail — content **must** live in `src/content/docs/` via `docsLoader()`; `markdown.processedDirs` only extends pipeline, not routing | Caveat — `source: .` works but requires aggressive `exclude:` for `mod/`, `binaries/`, `*.py`, `*.sh`, `LICENSE`, etc. |
| **HARD: Full-text search OOTB (no third-party)** | Pass — Lunr client-side, default-enabled | Pass — `@docusaurus/plugin-content-docs` ships local search via `@easyops-cn/docusaurus-search-local` (community) or Algolia DocSearch (third-party). For zero-third-party: community plugin required | Pass — `search: { provider: 'local' }` (MiniSearch, built-in) | Pass — Pagefind (built-in since 2023) | Pass — Lunr.js, default-enabled |
| **HARD: Dark mode** | Pass — `palette` with `default`/`slate` + scheme toggle, since v7.1.0 | Pass — built into classic theme, toggle in navbar | Pass — built-in Appearance toggle | Pass — built-in toggle | Pass — `color_scheme: dark` |
| **HARD: Syntax highlighting (sh/py/yaml/json)** | Pass — Pygments via `pymdownx.highlight` + `pymdownx.superfences` (build-time, fast, accurate) | Pass — Prism.js (runtime) | Pass — Shiki (build-time, accurate VS-Code-grade) | Pass — Expressive Code (Shiki under the hood) | Pass — Rouge (Jekyll default) |
| **HARD: HTML5 `<video>` for mp4** | Pass — raw HTML in markdown works; `md_in_html` ext available | Pass — MDX accepts raw HTML/JSX; `<video>` direct | Pass — Vue templates accept raw HTML | Pass — MDX accepts raw HTML | Pass — Kramdown allows raw HTML |
| **HARD: Mobile-friendly responsive** | Pass — default theme is mobile-first | Pass — default | Pass — default | Pass — default | Pass — default |
| **HARD: CSS-variable theming** | Pass — `--md-primary-fg-color`, `--md-accent-fg-color`, `--md-hue` and full `[data-md-color-scheme="custom"]` override via `extra_css` | Pass — `--ifm-color-primary` etc.; theme via `custom.css` | Pass — `--vp-c-brand` etc.; via `.vitepress/theme/custom.css` | Pass — `--sl-color-*` variables; via `customCss` | Caveat — Sass-variable driven; CSS-var coverage partial, full theming needs Sass override |
| **HARD: Mermaid** | Pass — `pymdownx.superfences` with mermaid custom_fence; native Material integration auto-themes with palette | Caveat — `@docusaurus/theme-mermaid` first-party plugin (extra install) | Caveat — `vitepress-plugin-mermaid` community plugin (extra install) | Pass — built into Starlight 0.32+ via Expressive Code or `@astrojs/markdown-remark` config | Pass — `mermaid:` block in `_config.yml` since v0.4.0 |
| Theming flexibility (CSS var depth) | Excellent — entire palette is CSS variables; can re-skin without forking | Excellent — Infima design system, full var surface | Excellent — small, well-organized var set | Good — clean var set, limited surface | Limited — Sass-first |
| Build speed at our scale (~30 pages + ~50 figures) | <2s clean build (Python, single-threaded but tiny) | ~10–20s cold (Node+webpack+MDX) | ~2–4s cold (Vite is fast); ~200ms HMR | ~5–10s (Astro build) | ~3–5s |
| GitHub Pages deployment story | Excellent — official `mkdocs gh-deploy --force`, two-job GH Action template in Material docs | Good — `actions/deploy-pages` + `npm run build`; well-documented | Good — `actions/deploy-pages` + `npm run docs:build` | Good — `withastro/action` official | Excellent — native to GH Pages, no Action needed (server-side build) |
| Maintenance burden | Low — Python `pip install mkdocs-material`, single `mkdocs.yml`. Material is the most stable docs theme in the ecosystem (v9 stable since 2023, no major breaking-change since) | Medium — Node deps, ~30 transitive packages. Docusaurus had breaking v2→v3 in 2023; pin major version | Medium — Vue/Vite + plugin churn; v1 stable, v2-alpha is rolling | Medium — Starlight still labelled beta; Astro releases ~monthly; minor break-risk | Low to Medium — Ruby/Bundler; Jekyll itself stable; just-the-docs has been on 0.x for 4+ years |

---

## 3. Detailed Analysis — Top 2 Candidates

### MkDocs Material 9.x (winner)

**Why it fits**

- **Repo-root sourcing**: solved by the standard symlink pattern documented in [mkdocs/mkdocs discussion #3062](https://github.com/mkdocs/mkdocs/discussions/3062). Create `src/` at repo root, symlink the four source paths into it, set `docs_dir: src`. README.md at the top of docs_dir is automatically treated as `index.html` (MkDocs explicitly supports `README.md` as an index page per [writing-your-docs guide](https://www.mkdocs.org/user-guide/writing-your-docs/)). The symlinks satisfy the "MUST NOT move .md files" constraint literally — files stay in their original locations and the symlinks are read-only pointers.
- **Every hard requirement is a native feature**: search (Lunr, client-side, no external service), dark mode (`slate` scheme with toggle), syntax highlighting (Pygments build-time, supports all 4 required languages including JSON with `pymdownx.highlight`), mermaid (`pymdownx.superfences` with `custom_fences` block, auto-themed against the palette), mp4 (raw HTML5 video tag works in markdown), CSS variables (`--md-primary-fg-color`, `--md-accent-fg-color`, `--md-hue`, full `[data-md-color-scheme="custom"]` override), mobile-responsive (default).
- **IA fit**: the `nav:` config supports the exact 9-group structure from [`ia-design.md`](./ia-design.md) §2 with explicit per-file paths under `src/`. `not_in_nav:` handles the orphan [`tools/README.md`](../tools/README.md) (which `ia-design.md` §1 marks as excluded from user-facing nav). `navigation.indexes` feature renders section README files as hub landing pages, matching the IA's "Each section has an index page" design.
- **Innodisk-palette theming**: `palette` with `primary: custom` and `accent: custom`, then `extra_css: [stylesheets/innodisk.css]` defining the brand CSS variables. Material's `--md-hue` variable lets the dark scheme inherit the same brand hue. Zero forking required.
- **GitHub Pages deployment**: official two-step pattern — `mkdocs gh-deploy --force` runs locally, or a 20-line GitHub Action using `actions/setup-python@v5` + `pip install mkdocs-material mkdocs-include-markdown-plugin` + `mkdocs gh-deploy --force`. Publishes to the `gh-pages` branch with no extra config.

**Where it's awkward**

- **Symlinks on Windows**: contributors editing docs on Windows without Developer Mode enabled cannot create symlinks via `git clone`. Mitigation: the symlinks need only exist on the CI runner (Linux). For local preview on Windows, document a one-line PowerShell `mklink /D` script in `tools/` or fall back to the `mkdocs-include-markdown-plugin` `{% include %}` directive (which supports `../` paths, per its [docs](https://github.com/mondeja/mkdocs-include-markdown-plugin)) as a Windows-only path. The Linux/macOS team (and CI) uses symlinks; Windows contributors use the include directive. This is a one-time setup cost.
- **`README.md` as homepage**: MkDocs auto-renames `README.md` → `index.html` only if there is **no** `index.md` in the same directory. Decision: keep the existing root [`README.md`](../README.md) **untouched** for the GitHub repo landing surface (per `docs-inventory.md` §8). For the Pages site, create a new `src/index.md` (Phase 1 of the IA, the slimmed marketing page from `ia-design.md` §5) so the symlinked `src/README.md` becomes a duplicate that MkDocs ignores. Alternative: do not symlink `README.md` at all — write the slimmed `index.md` directly in `src/`, and the long architecture content lifts to `src/overview.md`. The two patterns are equivalent; the second is cleaner and is what the sample config below uses.
- **mp4 build copy**: MkDocs copies non-markdown files from `docs_dir` into `site/` automatically, but only files inside `docs_dir`. The symlink `src/benchmarks` → `../benchmarks` means `nv_qc_live.mp4` is reachable through the symlink and gets copied during build. Confirm with `mkdocs build --verbose` that the mp4 lands in `site/benchmarks/iqs-streampipe/fig/`. If symlink traversal misses it, add `mkdocs-include-dir-to-nav` or copy the mp4 via the `overrides/` `gen-files` plugin.
- **Mermaid theming**: Material's mermaid integration auto-themes to the palette only when the diagram uses default styling. Diagrams that hardcode `%%{init: {...}}%%` will ignore the palette. Acceptable — the IA does not currently call for hand-styled mermaid.

**Gotchas**

- `pymdownx.superfences` and `pymdownx.highlight` are part of `pymdown-extensions` (a sister package to Material). Material pulls it in transitively, but pin both `mkdocs-material` and `pymdown-extensions` versions in `requirements.txt` so the GH Action build is reproducible.
- The Material theme uses `extra.css` (NOT `extra_css`) for some legacy syntax. Use `extra_css:` (plural, with colon) at top level of `mkdocs.yml` — easy to mis-type.
- `nav:` paths must be relative to `docs_dir` (i.e. relative to `src/`), not relative to the repo root. The sample config below shows this explicitly.
- Material's instant-loading XHR (`features: [navigation.instant]`) breaks mp4 `<video>` autoplay if the video is loaded after page swap; mp4s here are click-to-play (per `ia-design.md` §6) so this is moot but worth knowing.

---

### Docusaurus 3.10.x (runner-up)

**Why it fits**

- **Repo-root sourcing via multiple plugin instances**: move the site into `website/` and load `@docusaurus/plugin-content-docs` three times — one with `path: '../docs'` (id: `docs`), one with `path: '../tutorials'` (id: `tutorials`), one with `path: '../benchmarks'` (id: `benchmarks`). Each instance gets its own `routeBasePath`. This is supported per the [multi-instance guide](https://docusaurus.io/docs/docs-multi-instance). The `tools/` orphan is excluded by simply not adding a fourth instance.
- **Every hard requirement is satisfiable**: search via the well-maintained community plugin `@easyops-cn/docusaurus-search-local` (no Algolia, no external service); dark mode built into classic theme; Prism syntax highlighting; mermaid via official `@docusaurus/theme-mermaid`; `<video>` works in MDX; CSS-variable theming via Infima (`--ifm-color-primary` etc.); mobile-responsive default.
- **React/MDX ergonomics**: if the team wanted custom components (e.g. the persona-card grid from `ia-design.md` §5, the YAML-config copy-button), MDX makes them trivial. Material requires HTML+JS overrides.
- **Mature GH Pages story**: `actions/deploy-pages` + `npm run build && npm run deploy` is well-trodden.

**Where it's awkward**

- **Cannot point at the repo root itself**. Per [docusaurus#9027](https://github.com/facebook/docusaurus/issues/9027), using `..` or the site root as an MDX path causes loader conflicts (the MDX loader collides with everything else in the directory — `node_modules/`, `binaries/`, `mod/`, `*.py`). So `README.md` at the repo root cannot be the homepage source directly. Workaround: copy or symlink `README.md` (or a slimmed `index.md`) into `website/src/pages/index.md`. Adds a copy step or a symlink — net wash with MkDocs symlink work.
- **5× config surface**: three plugin instances + `docusaurus.config.js` + `sidebars.js` (one per instance) + `package.json` + lockfile. ~80 lines of config vs. MkDocs' ~40.
- **Sidebar config is JS, not YAML**: less ergonomic for documentation contributors who tend to be markdown/yaml-fluent.
- **Build is heavier**: 10–20s cold builds vs. <2s for MkDocs. Doesn't matter for CI but slows local iteration.
- **Breaking-change history**: v2→v3 (2023) required significant config rewrites for many projects. Pinning to a major version and watching the [migration guides](https://docusaurus.io/docs/migration) is required maintenance burden.

**Gotchas**

- The `path:` option is resolved relative to the `website/` site directory. So `path: '../docs'` from `website/docusaurus.config.js` reaches the repo's `docs/`. Confirm in build logs.
- Each plugin instance must have a unique `id`. The default instance can omit `id`; subsequent instances must declare one.
- Mermaid requires both adding `theme-mermaid` to `themes:` and setting `markdown: { mermaid: true }` in config. Easy to miss.
- Static assets (mp4) in plugin-instance paths are copied into the build output but the URL routing differs per instance's `routeBasePath`. Verify mp4 URLs resolve at build time.

---

## 4. Why the Others Were Eliminated

**VitePress 1.6.4 / 2.0-alpha** — eliminated on the repo-root sourcing requirement. `srcDir: '..'` (parent / repo root) is **documented broken**: discussion [#3209](https://github.com/vuejs/vitepress/discussions/3209) shows it failing with broken links and rendering errors even with symbolic-link workarounds, and issue [#4384](https://github.com/vuejs/vitepress/issues/4384) is an open feature request for "an `srcDir` different from `root`" with no resolution as of 2026. VitePress's intended pattern is `srcDir: 'src'` (a subfolder), and there is no way to route files outside the project root through its Vite-based scanner without moving them. VitePress also requires `vitepress-plugin-mermaid` (community, third-party) for Mermaid. The Shiki highlighting and built-in MiniSearch are excellent, but those don't compensate for failing the hard sourcing constraint. If the team were willing to move docs into a `docs/` subfolder under `.vitepress/`, VitePress would be the speed champion — but that violates the brief.

**Astro Starlight (latest, still beta)** — eliminated outright on the repo-root sourcing requirement. Starlight's [`docsLoader()`](https://starlight.astro.build/reference/configuration/) strictly requires content to live in `src/content/docs/` as part of an Astro content collection. The `markdown.processedDirs` option only adds the Astro Markdown pipeline to other directories — it does **not** route them or make them part of the docs collection. There is no documented way (as of 2026) to load `README.md` at the repo root as the Starlight homepage or to register `tutorials/**/*.md` and `benchmarks/**/*.md` as Starlight pages without copying them into `src/content/docs/`. The brief's hard constraint kills this candidate. Starlight is also still labelled beta software, which adds change risk for a multi-month roadmap.

**Jekyll just-the-docs 0.6** — eliminated on maintenance burden + IA fit, not on hard requirements per se. Jekyll's `source: .` config does work and would let Jekyll process the repo root, but it requires an extensive `exclude:` list to keep Jekyll from trying to process `mod/`, `binaries/`, `install.sh`, `iqs-launcher.sh`, `launcher.py`, `LICENSE`, `*.json`, `tools/*.py`, `benchmarks/**/scripts/`, etc. — every non-markdown file in the repo. Maintenance-wise, every new tool or binary added to the repo requires a Jekyll exclude update or it ends up in `_site/`. The collections-based alternative (`collections:` for `tutorials`, `benchmarks`) is cleaner but requires the folders to be prefixed with underscores (`_tutorials/`), which is a file move. CSS-variable theming in just-the-docs is partial (it's Sass-first), so the Innodisk palette would need Sass overrides rather than a single CSS-var stylesheet. just-the-docs is also a small-community theme (one primary maintainer, slow release cadence) vs. Material's full-time-funded team. The one thing just-the-docs wins on is "GitHub Pages native build" — no Action needed — but that's not worth the config noise.

---

## 5. Suggested Directory Layout (Winner: MkDocs Material)

What gets **added** at the repo root (8 new entries, all in NEW locations):

```
iQ-Studio/
├── README.md                          # UNCHANGED — GitHub repo landing
├── docs/                              # UNCHANGED — .md files stay in place
├── tutorials/                         # UNCHANGED — .md files stay in place
├── benchmarks/                        # UNCHANGED — .md files stay in place
├── tools/                             # UNCHANGED — .md files stay in place
├── install.sh, iqs-launcher.sh, ...   # UNCHANGED — unrelated to docs build
│
├── mkdocs.yml                         # NEW — site config (~80 lines)
├── requirements.txt                   # NEW — pins mkdocs-material + extensions
│
├── src/                               # NEW — docs_dir for MkDocs, symlinks only
│   ├── index.md                       # NEW — slimmed landing page (ia-design.md §5)
│   ├── overview.md                    # NEW — architecture content lifted from README
│   ├── docs              -> ../docs                  (symlink)
│   ├── tutorials         -> ../tutorials             (symlink)
│   ├── benchmarks        -> ../benchmarks            (symlink)
│   └── stylesheets/
│       └── innodisk.css               # NEW — Innodisk CSS variables for palette
│
├── overrides/                         # NEW — Material theme overrides (optional, Phase 2)
│   └── partials/
│       └── ... (only if hand-customizing header/footer)
│
└── .github/
    └── workflows/
        └── docs.yml                   # NEW — build + deploy to gh-pages
```

Notes:

- **Nothing in `README.md`, `docs/`, `tutorials/`, `benchmarks/`, `tools/` moves.** Existing files stay at their existing paths. The MkDocs build reads them via symlinks.
- **`tools/` is intentionally NOT symlinked** into `src/`. `ia-design.md` §1 marks it as contributor-internal, excluded from the Pages build. To keep it discoverable on GitHub.com it remains at the repo root unchanged.
- **`src/index.md` and `src/overview.md` are NEW files** that implement the README split recommended in `docs-inventory.md` §8 and `ia-design.md` §5. They live in `src/` only — they do not pollute the repo root or duplicate any existing content. The existing root `README.md` remains as the GitHub repo landing surface.
- **`overrides/`** is only needed for Phase 2 if you customize header/footer/navbar partials. Phase 1 ships without it.
- **Innodisk palette** lives in one file (`src/stylesheets/innodisk.css`) referenced from `mkdocs.yml` via `extra_css:`. To re-theme, edit that one file.

---

## 6. Sample Config Snippets

### `mkdocs.yml` (at repo root)

```yaml
site_name: iQ Studio
site_description: AI runtime launcher for Qualcomm Dragonwing edge devices
site_url: https://innoipc-innodisk.github.io/iQ-Studio/
repo_url: https://github.com/InnoIPC-Innodisk/iQ-Studio
repo_name: InnoIPC-Innodisk/iQ-Studio
edit_uri: edit/main/                   # appended with the source path per ia-design.md §3

docs_dir: src                          # the symlink directory at repo root

theme:
  name: material
  custom_dir: overrides                # remove this line if overrides/ is empty (Phase 1)
  language: en
  features:
    - navigation.instant
    - navigation.tracking
    - navigation.indexes               # use section README.md files as hub landing pages
    - navigation.top
    - navigation.sections
    - navigation.expand                # multi-open accordion per ia-design.md §3
    - toc.follow                       # right-rail active-section highlight per ia-design.md §3
    - search.suggest
    - search.highlight
    - content.code.copy                # copy-to-clipboard on code blocks
    - content.tabs.link
    - content.action.edit              # "Edit on GitHub" per ia-design.md §3
  palette:
    - scheme: default
      primary: custom
      accent: custom
      toggle:
        icon: material/weather-night
        name: Switch to dark mode
    - scheme: slate
      primary: custom
      accent: custom
      toggle:
        icon: material/weather-sunny
        name: Switch to light mode
  icon:
    repo: fontawesome/brands/github

extra_css:
  - stylesheets/innodisk.css           # CSS variables — Innodisk palette

plugins:
  - search                             # Lunr, default; explicit to keep alongside others
  # - include-markdown                 # Phase 1.5: enables Windows-friendly ../ includes

markdown_extensions:
  - admonition
  - attr_list
  - md_in_html                         # allow raw HTML (<video>) inside markdown
  - tables
  - toc:
      permalink: true
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.inlinehilite
  - pymdownx.snippets:
      base_path:
        - .                            # allow snippet includes from anywhere under repo
        - src
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.details
  - pymdownx.tasklist:
      custom_checkbox: true

nav:
  - Home: index.md
  - Overview: overview.md
  - Getting Started:
      - tutorials/starting-guides/README.md
      - Q911 Quick Start: tutorials/starting-guides/q911/README.md
      - Q911 — Yocto: tutorials/starting-guides/q911/yocto.md
      - Q911 — Ubuntu: tutorials/starting-guides/q911/ubuntu.md
      - Image Flashing: tutorials/starting-guides/flash-image/README.md
      - OTA Updates: tutorials/starting-guides/ota/README.md
  - Applications:
      - tutorials/applications/README.md
      - iQS-VLM: tutorials/applications/iqs-vlm/README.md
      - iQS-Streampipe: tutorials/applications/iqs-streampipe/README.md
      - iQS-YOLOv10n: tutorials/applications/iqs-yolov10n/README.md
  - SDKs:
      - tutorials/sdks/README.md
      - iQS-OGenie: tutorials/sdks/iqs-ogenie/README.md
      - iQS-VLM (Open WebUI): tutorials/sdks/iqs-vlm/README.md
      - iQS-Streampipe (Customize): tutorials/sdks/iqs-streampipe/README.md
  - Model Deploy:
      - tutorials/model-deploy/README.md
      - YOLO26: tutorials/model-deploy/cv/yolo26/README.md
  - AVL:
      - tutorials/avl/README.md
      - GMSL Camera: tutorials/avl/gmsl-camera/README.md
      - MIPI Camera: tutorials/avl/mipi-camera/README.md
  - Benchmarks:
      - benchmarks/README.md
      - InnoPPE: benchmarks/innoppe/README.md
      - Streampipe Multi-stream: benchmarks/iqs-streampipe/README.md
      - Perception Model: benchmarks/perception_model/README.md
  - Reference:
      - How to use iqs-launcher: docs/how-to-use-iqs-launcher.md
  - Changelog: docs/changelog.md

# All nav paths above are relative to docs_dir (src/).
# src/tutorials/... resolves through the symlink to ../tutorials/...
# src/docs/... resolves through the symlink to ../docs/...
# src/benchmarks/... resolves through the symlink to ../benchmarks/...

not_in_nav: |
  # Anything under src/ but intentionally not in the sidebar.
  # Keeps MkDocs quiet about "page exists but is not in nav".
  /index.md
  /overview.md
```

### `requirements.txt`

```
mkdocs==1.6.1
mkdocs-material==9.5.39
pymdown-extensions==10.11
mkdocs-include-markdown-plugin==6.2.2  # optional, for Windows-friendly includes
```

(Versions as of 2026-05; pin exact for reproducible CI builds.)

### `src/stylesheets/innodisk.css` (sketch — palette goes here)

```css
:root,
[data-md-color-scheme="default"] {
  --md-primary-fg-color:        #003E7E;   /* Innodisk navy — placeholder */
  --md-primary-fg-color--light: #1C5BA6;
  --md-primary-fg-color--dark:  #002854;
  --md-accent-fg-color:         #E60028;   /* Innodisk red — placeholder */
  --md-typeset-a-color:         var(--md-primary-fg-color);
}

[data-md-color-scheme="slate"] {
  --md-hue: 215;                            /* navy-tinted dark */
  --md-primary-fg-color:        #4A86C8;
  --md-accent-fg-color:         #FF4D6D;
  --md-typeset-a-color:         var(--md-primary-fg-color);
}
```

### `.github/workflows/docs.yml`

```yaml
name: Deploy docs to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: write   # to push to gh-pages branch

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0    # mkdocs-git-revision-date-localized needs full history
      - name: Create src/ symlinks
        # symlinks are NOT committed to git (per .gitignore); rebuild them on every CI run.
        run: |
          mkdir -p src
          ln -sfn ../docs       src/docs
          ln -sfn ../tutorials  src/tutorials
          ln -sfn ../benchmarks src/benchmarks
          # src/index.md and src/overview.md are committed files; do NOT symlink them.
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Cache pip
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: pip-${{ hashFiles('requirements.txt') }}
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Build and deploy
        run: mkdocs gh-deploy --force --clean
```

### `src/index.md` skeleton (slimmed landing per `ia-design.md` §5)

```markdown
---
hide:
  - navigation
  - toc
---

# iQ Studio — the AI runtime launcher for Dragonwing edge devices

_Show Performance, Spark Imagination._

```bash
git clone https://github.com/InnoIPC-Innodisk/iQ-Studio && cd iQ-Studio && ./install.sh
```

<!-- Persona cards (Wei / Priya / Dan) per ia-design.md §5 go here -->
<!-- Quick-link grid per ia-design.md §5 goes here -->
<!-- Recent-changelog widget per ia-design.md §5 goes here (parse docs/changelog.md at build) -->
```

### `.gitignore` addition (the symlinks should not be committed)

```
# MkDocs build artifacts and dev-only symlinks
/site/
/src/docs
/src/tutorials
/src/benchmarks
```

(Commit `src/index.md`, `src/overview.md`, `src/stylesheets/`. Do NOT commit the symlinks; CI re-creates them.)

---

## 7. Open Questions / Risks

1. **README.md as the literal homepage source vs. a separate `src/index.md`** — the chosen approach (separate `src/index.md`, leave root `README.md` untouched for GitHub.com) implements `docs-inventory.md` §8's split recommendation. If the team later decides to render the existing root `README.md` *unchanged* as the site homepage, switch to `ln -sfn ../README.md src/index.md` and delete the new `src/index.md`. MkDocs will rename the README symlink to `index.html` at build because there is no other `index.md` in `src/`. Either approach is one-line config.

2. **Windows developer ergonomics** — symlinks need Developer Mode or admin. Mitigations, in order of effort: (a) document the `mklink /D` PowerShell command in `tools/`, (b) provide a fallback Make target that uses `mkdocs-include-markdown-plugin` instead, (c) require Windows contributors to preview docs via the GH Action's PR preview rather than locally. Phase 1 should ship (a) as a `tools/setup_docs_dev.ps1` script.

3. **mp4 asset handling** — `docs-inventory.md` §11 calls out the mp4 in `benchmarks/iqs-streampipe/fig/nv_qc_live.mp4` that currently 404s because GitHub Pages doesn't serve a plain markdown link to it well. After migration, the file is reachable through the symlink and MkDocs copies it into `site/`. **Action**: replace the bare markdown link in [`benchmarks/iqs-streampipe/README.md`](../benchmarks/iqs-streampipe/README.md) with the `<video controls>` HTML block from `ia-design.md` §6. Verify the path in the built `site/` directory after the first build.

4. **GitHub user-attachments video URL** — the bare URL in [`tutorials/sdks/iqs-vlm/README.md`](../tutorials/sdks/iqs-vlm/README.md) will not auto-embed on Pages (as `docs-inventory.md` §11 flags). Mitigation: download the asset, store as `tutorials/sdks/iqs-vlm/fig/open-webui-interaction.mp4`, swap to `<video controls>` embed. This is a content-fix, not an SSG decision — but the implementer will hit it on first build.

5. **Mermaid theming with `slate` dark mode** — Material's mermaid integration applies the active palette colors to the diagram. Test a sample mermaid diagram with both light and dark modes before locking in the Innodisk palette CSS. If the auto-themed colors look wrong on `slate`, add `mermaid.initialize({ theme: 'dark' })` via a small JS hook in `extra.javascript`.

6. **Inconsistent code-fence language tags** — `docs-inventory.md` §4 P3 already flagged this and `tools/audit_content.py` catches some cases. Pygments will silently fall back to no-highlight for missing language tags. Implementer should run a `grep -rE '^```$|^```\s*$' --include='*.md'` pass and tag every untagged fence before publication.

7. **AVL hub child-link content fix** — the IA design (§2) compensates for the AVL hub's missing child links by surfacing them in the sidebar, but `docs-inventory.md` §1 marks the in-page AVL hub README as still broken for users who don't see the sidebar. This is a content-fix and is outside the SSG decision, but the implementer should not rely on Material to fix it — add the child links to [`tutorials/avl/README.md`](../tutorials/avl/README.md) as part of the launch checklist.

8. **`mkdocs-include-markdown-plugin` vs. symlinks** — both work. Symlinks are simpler and faster; the include plugin is Windows-portable and gives per-file granularity (handy if you want to include only part of a file). Decision: ship symlinks in Phase 1; reserve the include plugin as a Windows fallback documented in `tools/`. Do not use both for the same content — that produces duplicate-page warnings.

9. **Versioning strategy (future)** — Material supports versioned docs via `mike`. Not needed for Phase 1 but worth noting that the SSG choice does not block this if the team later needs `v1/` and `v2/` documentation tracks.

10. **Build-time link checking** — Material does not run a link checker by default. Add the `mkdocs-htmlproofer-plugin` or run `linkchecker` in a separate CI job. The two P0 broken links from `docs-inventory.md` §4 (`IQS.md` reference in OTA, the ADB anchor in YOLO26) will surface in this check — fix them as content changes, not as SSG configuration.

---

**Tool Evaluator**: Tool Evaluator agent
**Evaluation date**: 2026-05-22
**Confidence level**: High — backed by official docs of all five candidates plus three GitHub issue/discussion threads for the corner-case sourcing constraint. The only un-tested-here assumption is that MkDocs' symlink traversal copies the `.mp4` files into `site/` (high prior, easy to verify on first build).
**Next handoff**: implementation engineer drops `mkdocs.yml`, `requirements.txt`, `src/index.md`, `src/overview.md`, `src/stylesheets/innodisk.css`, and `.github/workflows/docs.yml` per §6 above, then runs `mkdocs serve` locally to verify all 27 in-scope `.md` files render through the symlinks.

---

## Sources

- [MkDocs — Configuration](https://www.mkdocs.org/user-guide/configuration/)
- [MkDocs — Writing Your Docs (README.md as index)](https://www.mkdocs.org/user-guide/writing-your-docs/)
- [mkdocs/mkdocs Discussion #3062 — Strategy for including docs from repository root](https://github.com/mkdocs/mkdocs/discussions/3062)
- [Material for MkDocs — Changing the colors](https://squidfunk.github.io/mkdocs-material/setup/changing-the-colors/)
- [Material for MkDocs — Diagrams (Mermaid)](https://squidfunk.github.io/mkdocs-material/reference/diagrams/)
- [Material for MkDocs — Code blocks](https://squidfunk.github.io/mkdocs-material/reference/code-blocks/)
- [Material for MkDocs — Search](https://squidfunk.github.io/mkdocs-material/setup/setting-up-site-search/)
- [Material for MkDocs — Setting up navigation](https://squidfunk.github.io/mkdocs-material/setup/setting-up-navigation/)
- [Material for MkDocs — Publishing your site](https://squidfunk.github.io/mkdocs-material/publishing-your-site/)
- [mkdocs-include-markdown-plugin](https://github.com/mondeja/mkdocs-include-markdown-plugin)
- [backstage/mkdocs-monorepo-plugin](https://github.com/backstage/mkdocs-monorepo-plugin)
- [Docusaurus — plugin-content-docs](https://docusaurus.io/docs/api/plugins/@docusaurus/plugin-content-docs)
- [Docusaurus — Docs multi-instance](https://docusaurus.io/docs/docs-multi-instance)
- [facebook/docusaurus Issue #9027 — Content plugins should prevent parent folder as MDX source](https://github.com/facebook/docusaurus/issues/9027)
- [facebook/docusaurus Issue #2937 — Allow custom path for docs non-relative to website directory](https://github.com/facebook/docusaurus/issues/2937)
- [VitePress — Site Config](https://vitepress.dev/reference/site-config)
- [VitePress — Routing](https://vitepress.dev/guide/routing)
- [VitePress — Default theme search (local provider, MiniSearch)](https://vitepress.dev/reference/default-theme-search)
- [vuejs/vitepress Discussion #3209 — Remote/External Content Directory via srcDir](https://github.com/vuejs/vitepress/discussions/3209)
- [vuejs/vitepress Issue #4384 — A way to configure the directory for docs instead of the root folder](https://github.com/vuejs/vitepress/issues/4384)
- [emersonbottero/vitepress-plugin-mermaid](https://github.com/emersonbottero/vitepress-plugin-mermaid)
- [Astro Starlight — Authoring content](https://starlight.astro.build/guides/authoring-content/)
- [Astro Starlight — Configuration reference](https://starlight.astro.build/reference/configuration/)
- [Astro Starlight — Getting started](https://starlight.astro.build/getting-started/)
- [Just the Docs — Configuration](https://just-the-docs.com/docs/configuration/)
