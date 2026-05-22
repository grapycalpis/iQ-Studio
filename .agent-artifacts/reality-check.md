# iQ-Studio Documentation Site — Pre-Launch Reality Check

**Tester**: TestingRealityChecker (Integration Agent)
**Date**: 2026-05-22
**Build under test**: `mkdocs build --clean` against repo `dev` branch, served from `site/` on `http://127.0.0.1:8765`
**Server log**: `/tmp/srv.log`
**Source of truth**: `.agent-artifacts/docs-inventory.md`, `.agent-artifacts/ux-research.md`, `mkdocs.yml`

---

## 1. Verdict

**NO-GO**. The homepage is functionally broken for any visitor who tries to click the in-content links (22 of 30 content links 404), 12 of 12 photos on `q911/yocto/` and all photos on `q911/ubuntu/` render as broken-image placeholders, the configured GitHub repo `InnoIPC-Innodisk/iQ-Studio` returns 404 (so every "Edit on GitHub" link 404s and a key cross-site link in the page chrome dead-ends), and the homepage overflows horizontally at 360 px.

---

## 2. Evidence Summary

What was actually tested:

- **Build**: `mkdocs build --clean` succeeded (1.57 s) with 3 WARNING lines and 2 INFO-level broken-target reports that match the inventory's P0 list.
- **Pages sampled**: 10 (Home, Starting Guides hub, q911/yocto, flash-image, OTA, applications/iqs-vlm, sdks/iqs-streampipe, model-deploy/yolo26, avl/mipi-camera, benchmarks/iqs-streampipe). All 10 returned HTTP 200.
- **In-content links audited**: 47 (homepage 30 + 17 across the other 9 sampled pages); **24 broken** (22 on the homepage body + the documented `ota → IQS.md` + the documented `yolo26 → q911-README#adb` anchor).
- **Images audited**: 58 in rendered HTML on the sampled pages; **12 are 404** (all 12 photos on `q911/yocto/` plus a separate confirmation that `q911/ubuntu/` exhibits the same pattern → **at least 20 broken images across the q911 OS pages alone**).
- **Videos / `<source>` tags**: 0 `<video>` tags rendered. The mp4 referenced by `benchmarks/iqs-streampipe/` is a plain link (HTTP 200) but never embedded. The github-user-attachments URL inside `sdks/iqs-vlm/` renders as a bare URL inside `<p>` — no playable video.
- **GIFs > 10 MB**: 5 (vlm-demo 19.3 MB; streampipe gif0 18.8 MB used by 2 pages; streampipe gif2 17.0 MB; streampipe gif1 13.6 MB; iqs-vlm-demo also = same 19.3 MB on homepage). One mp4 11.9 MB.
- **User journeys walked**: 9 (A1, A2, A3, B1, B2, B3, C1, C2, C3) — every page on each journey returns 200, but **6 journeys hit at least one broken in-page link** that the user is expected to click.
- **Search**: 5 queries against `site/search/search_index.json` (193 indexed docs).
- **Viewports**: 4 (360, 768, 1280, 1920) via `google-chrome --headless` screenshots of the homepage and the content-heavy yolo26 page.
- **Dark-mode persistence**: verified by JS-code inspection of `site/assets/javascripts/bundle.525ec568.min.js` and the inline `__md_scope` / `__md_set` / `__md_get` boot scripts in the rendered HTML, plus a CDP-driven `localStorage` round-trip test.
- **Edit-on-GitHub**: 5 sampled pages, all 5 edit URLs constructed; HTTP-tested externally.

Tool inventory: `mkdocs 1.6.1`, `Google Chrome 147` (headless), `curl`, `python3` with `urllib`, `websocket-client`. No Playwright (not installed; using `google-chrome --headless` + DevTools Protocol).

---

## 3. Blockers (Must Fix Before Launch)

### B1. Homepage body — 22 of 30 in-content links 404
- **Where**: `/` (`README.md` rendered as `site/index.html`)
- **What**: README contains a raw-HTML "Explore Documentation & Resources" `<table>` whose `<a href>` values are literal markdown filenames (`./tutorials/.../README.md`). mkdocs only rewrites markdown-syntax links, not raw HTML. The rendered links therefore point at `.md` files that do not exist in the built site (the site uses `use_directory_urls: true`, so e.g. `tutorials/starting-guides/README.md` should be `tutorials/starting-guides/`).
- **Evidence**:
  - `mkdocs build` WARNING: `Doc file 'index.md' contains a link './README.md#explore-documentation--resources', but the target 'README.md' is not found among documentation files.`
  - HTTP probe (recorded in `.agent-artifacts/screenshots/asset-audit.json` under key `"/"`): 22 internal links 404, e.g. `./tutorials/starting-guides/README.md`, `./benchmarks/innoppe/README.md`, `./LICENSE`, `./tutorials/applications/iqs-yolov10n/README.md` — all returning HTTP 404.
  - README source confirmation: `README.md` lines 138-151 contain literal `<li><a href="./tutorials/starting-guides/README.md">…</a></li>` entries.
- **User impact**: every link in the homepage's "Explore Documentation & Resources" section dead-ends. This is the *primary* navigation table on the homepage for Persona C and the secondary entry point for Personas A and B.
- **Severity**: **P0**. Homepage is the canonical entry; failing every body link breaks all three personas' primary funnel.
- **Fix**: either (a) rewrite the table to use mkdocs-rewritten markdown links, (b) use the site's mkdocs-canonical URLs in the raw HTML (`./tutorials/starting-guides/`, no `README.md`), or (c) per the inventory's §8 recommendation, split README → slim `index.md` and delete the resource table entirely (sidebar covers it).

### B2. `tutorials/starting-guides/q911/yocto/` — all 12 photos 404 (and same bug on `…/ubuntu/`)
- **Where**: `/tutorials/starting-guides/q911/yocto/` and `/tutorials/starting-guides/q911/ubuntu/`
- **What**: Both pages are deep `.md` files (not `README.md`), so with `use_directory_urls: true` they become `/yocto/index.html` and `/ubuntu/index.html`. The pages use raw-HTML `<img src="./fig/connect_dp_boot.png">` (mkdocs does *not* rewrite raw-HTML `src` paths). At runtime the browser resolves `./fig/...` against `/tutorials/starting-guides/q911/yocto/` → `/tutorials/starting-guides/q911/yocto/fig/connect_dp_boot.png` which **does not exist**. The actual files live at `/tutorials/starting-guides/q911/fig/...`.
- **Evidence**:
  - HEAD `/tutorials/starting-guides/q911/yocto/fig/connect_dp_boot.png` → **404**.
  - HEAD `/tutorials/starting-guides/q911/fig/connect_dp_boot.png` → **200**.
  - Source: `tutorials/starting-guides/q911/yocto.md` lines 38, 41, 55, 59, 70, 73, 90, 103, 106, 131, 142, 150 all use `./fig/...`.
  - Same for `tutorials/starting-guides/q911/ubuntu.md` line 42+ (`./fig/connect_dp_boot.png`, `./fig/ubuntu.png`, …).
  - Screenshot: `.agent-artifacts/screenshots/yocto-broken-imgs-1280.png` — visible empty image slots for every photo in the page body. Also `ubuntu-broken-imgs-1280.png`.
- **User impact**: hits **Journey A1** (Wei wants to flash + get a shell) and **Journey B2** (Priya needs ADB push instructions). These are the two highest-traffic step-by-step pages; both render with every photo broken.
- **Severity**: **P0**. The yocto.md commit (`fe670b8: refactor: split q911 guide by OS`) introduced this bug — the split moved the `.md` one directory deeper without updating the `./fig/` relative path, and because mkdocs cannot rewrite raw HTML `src`, the build emits no warning.
- **Fix**: change the raw `<img src="./fig/...">` to `<img src="../fig/...">` in both `yocto.md` and `ubuntu.md` (15+ replacements), or move `fig/` into per-OS subfolders. Add a CI check that asserts every rendered `<img src>` resolves with HTTP 200.

### B3. GitHub repo `InnoIPC-Innodisk/iQ-Studio` is 404 → every "Edit on GitHub" link and the repo-icon header link is broken
- **Where**: All 27 pages. `mkdocs.yml` line 23 sets `repo_url: https://github.com/InnoIPC-Innodisk/iQ-Studio` and line 25 sets `edit_uri: edit/main/`.
- **What**: the repo URL returns HTTP 404 (publicly inaccessible — either private, doesn't exist under this org, or org slug is wrong). Every `Edit on GitHub` link is therefore broken, as is the top-right "InnoIPC-Innodisk/iQ-Studio" repo badge.
- **Evidence** (all curl-checked externally with `-L`):
  - `https://github.com/InnoIPC-Innodisk/iQ-Studio` → **404**
  - `https://github.com/InnoIPC-Innodisk/iQ-Studio/edit/main/index.md` → **404**
  - `https://github.com/InnoIPC-Innodisk/iQ-Studio/edit/main/tutorials/starting-guides/q911/yocto.md` → **404**
  - `https://github.com/InnoIPC-Innodisk/iQ-Studio/edit/main/tutorials/applications/iqs-vlm/README.md` → **404**
  - `https://github.com/InnoIPC-Innodisk/iQ-Studio/edit/main/tutorials/sdks/iqs-streampipe/README.md` → **404**
  - `https://github.com/InnoIPC-Innodisk/iQ-Studio/edit/main/tutorials/model-deploy/cv/yolo26/README.md` → **404**
  - `https://raw.githubusercontent.com/InnoIPC-Innodisk/iQ-Studio/main/README.md` → **404**
- **Severity**: **P0** if the site is meant to be a public docs site with working contributor flow; **P1** if the repo will be made public at launch time (in which case launch must wait for the repo to be public).
- **Fix**: confirm the public repo URL and update `mkdocs.yml` `repo_url`. If the repo will remain private, disable `content.action.edit` in `theme.features` to suppress broken edit links and consider removing the repo badge.

### B4. Homepage edit URL targets `index.md` which doesn't exist on the GitHub side
- **Where**: `/` page-header pencil icon.
- **What**: Even if B3 is fixed (repo made public), the homepage `index.md` is a build-time symlink (`src/index.md → ../README.md`). `edit_uri: edit/main/` combined with the file name produces `https://github.com/.../edit/main/index.md` — but the repo source-of-truth file is `README.md` at the root. Symlinks under `src/` are gitignored per `mkdocs.yml` comments.
- **Evidence**:
  - Rendered homepage edit link: `https://github.com/InnoIPC-Innodisk/iQ-Studio/edit/main/index.md`
  - `mkdocs.yml` line 27: `docs_dir: src` and the inline comment "Symlinks are gitignored".
  - Verified that no `index.md` will be committed to the repo at `main`.
- **Severity**: **P1**. Subtler than B3 — even with a public repo, the homepage pencil will continue to 404.
- **Fix**: either commit a stub `index.md` at repo root that re-includes README, or set a per-page `edit_url` override on the homepage that points at `README.md`.

### B5. Horizontal overflow at 360 px viewport
- **Where**: Home page (and likely all pages — measured on home).
- **What**: At a 360 px viewport, content extends beyond the viewport on the right. The "Pick Your Path" `<grid-cards>` cards do not wrap their copy to the available width — text like "Install iQ Studio Launcher on your" and the next section heading "Show Performance, Spark Im…" are clipped at the right edge.
- **Evidence**:
  - Screenshot `.agent-artifacts/screenshots/home-360.png` (360 × 900): "Install iQ Studio Launcher on your\nrun your first build." — first line cut off mid-word.
  - Screenshot `.agent-artifacts/screenshots/home-360-tall.png` (360 × 2400 — full page): every grid-card right edge is clipped; later in the page, "Show Performance, Spark Im…" is cut off mid-word.
  - 768 / 1280 / 1920 screenshots (`home-768.png`, `home-1280.png`, `home-1920.png`) all render clean — issue is mobile-only.
- **Severity**: **P0** for any audience on phones (Persona A integrators on the bench frequently use phones; Persona B/C have laptops, but this still affects discoverability and SEO mobile-usability).
- **Fix**: review the `<grid-cards>` / inline-`<table>` CSS for `width: 100%` / `max-width: 100%` and word-wrap; specifically the inline-styled HTML cards in `README.md` ("Pick Your Path" three-column layout uses `<table>` with fixed cell widths).

### B6. The `applications/iqs-vlm/` page still serves an oversized 19 MB GIF embedded directly in the homepage
- **Where**: `/` and `/tutorials/applications/iqs-vlm/`
- **What**: `vlm-demo.gif` = 19.3 MB. The repo includes `tools/compress_gifs.sh` (gifski-based, flags ≥ 20 MB per its threshold) which has not yet been run on this asset, despite the recent commit `chore: move the camera intro to other repo` suggesting active asset triage.
- **Evidence**: `ls -la site/tutorials/applications/iqs-vlm/fig/vlm-demo.gif` → 19297222 bytes. Streampipe `gif0.gif` (used by 2 pages) = 18.8 MB. `gif2.gif` = 17.0 MB. `gif1.gif` = 13.6 MB. `iqs-yolov10n/fig/gif0.gif` = 9.0 MB. Total `site/` weight = 156 MB.
- **Severity**: **P1**. Homepage hero GIF >10 MB on the same page that's also the SEO landing breaks Lighthouse mobile (the entire `iqs-vlm` page weight is dominated by this single asset), and Persona C's "30-second demo" entry blows the LCP budget.
- **Fix**: run `tools/compress_gifs.sh` (or lower its threshold below 20 MB) and either replace with `.webp` / `.mp4`-with-poster or transcode the GIF.

---

## 4. Non-Blocking Issues (Fix Soon)

### N1. `tutorials/starting-guides/ota/README.md` → `../../../IQS.md` 404 (known P0 from inventory)
- HTTP probe confirms 404. Inventory called this out. Fix per inventory §4 P0 #1.
- Evidence: `mkdocs build` INFO line + `curl -I` `http://127.0.0.1:8765/IQS.md` → 404.

### N2. `tutorials/model-deploy/cv/yolo26/` → broken anchor on q911/README (known P0 from inventory)
- mkdocs warned: `does not contain an anchor '#interact-with-the-system-using-adb-over-usb-type-c'`. The anchor lives in `q911/yocto.md` not `q911/README.md`. Persona B's primary YOLO-deploy journey ends on a 404-equivalent.

### N3. `sdks/iqs-vlm/` GitHub user-attachments URL renders as bare text
- Rendered HTML: `<p>https://github.com/user-attachments/assets/fda1d4a4-2ef7-40ff-910b-47d563fc3273</p>` (verified by curl + grep). GitHub auto-embed only works on github.com; on mkdocs Pages it is unembedded plain text.
- Persona C's VLM journey loses its primary demo asset.
- Screenshot: `.agent-artifacts/screenshots/sdks-iqs-vlm-1280.png`.
- Fix: re-record / re-upload to repo and embed via `<video controls poster="…">`.

### N4. Search "OTA update" — top result is irrelevant
- Query `OTA update` returns 5 doc matches; top match by index order is "User prompt customization" (`tutorials/sdks/iqs-vlm/#user-prompt-customization`) — coincidentally contains both words but is unrelated. The actual OTA page is hit #3.
- All other 4 queries (`flash Q911`, `YOLO deploy`, `MIPI camera`, `VLM`) return a relevant top hit.
- Lower priority because mkdocs-material's lunr ranking uses term frequency and title boost in the UI, not raw index order — the UI may surface the OTA page first. Without driving the actual UI, only the raw-index hit list is testable.

### N5. `tutorials/avl/` hub does not link to its `gmsl-camera/` / `mipi-camera/` children (known P1 from inventory)
- Journey A2 (Wei wires up a camera) hits a dead-end on the AVL hub. Children are only reachable via the sidebar nav, not in-page.

### N6. `tutorials/applications/iqs-yolov10n/` is a forward-link dead-end (known P1 from inventory)
- 0 outbound `.md` links. Persona B Journey B3 ends without a "now port your own model" handoff.

### N7. Multiple oversized GIFs (10-19 MB each)
- See B6. Below the P0 line because they're not the homepage hero. Still blow mobile page-weight budgets on `applications/iqs-streampipe/`, `sdks/iqs-streampipe/`, `applications/iqs-yolov10n/`.

### N8. `mkdocs.yml` site_url points at `https://innoipc-innodisk.github.io/iQ-Studio/` but the repo at `InnoIPC-Innodisk/iQ-Studio` returns 404
- Implies GitHub Pages will fail to publish too (no source repo). Verify the actual Pages deployment target. The `sitemap.xml` already bakes the canonical URL — if Pages doesn't publish, every search-engine `<link rel=canonical>` points at a dead URL.

### N9. Homepage GIF + mp4 + multi-GIF asset bloat = 156 MB total site
- Pages CDN serves it, but Cloudflare / GitHub Pages caching and Lighthouse will all complain. Below P0 because the site loads — just slowly.

---

## 5. What Was NOT Tested (and Why)

- **Full keyboard / screen-reader accessibility**: out of scope for this gate (an a11y-report.md already exists in `.agent-artifacts/`).
- **mkdocs-material `navigation.instant` live runtime in headless Chrome**: in CDP-driven tests, the instant-nav AJAX shim hijacks the body content with `thunk.js`, so `Runtime.evaluate` against the post-navigation body returns the thunk shell rather than the rendered page. Workaround: verified palette persistence by inspecting the JS bundle + inline boot script + CDP-driven `localStorage` round-trip — that is sufficient to assert the design is correct, but I did **not** capture a literal "toggle button → navigate → toggle survived" UI screenshot loop with the rendered theme applied. Note this as a gap if you want a UI-level video.
- **External GitHub repo for Q911 manifests**: recent commit `fe670b8` linked to OS manifest repos. The OTA / starting-guides pages contain links like `https://github.com/InnoIPC-Innodisk/iQ-…` (per inventory §3) that I did not exhaustively curl-spider. The repo URL pattern is the same as B3, so they are likely all 404. If B3 is fixed, re-run a full external-link sweep before launch.
- **PDF / `<details>` / mermaid code-block rendering**: the inventory mentions mermaid is configured. Not validated visually because the sampled pages don't contain a mermaid diagram in their main body (only the inventory itself, which isn't part of the build per `mkdocs.yml` `exclude_docs`).
- **Sitemap completeness**: spot-checked first 20 lines only. All 27 inventory pages should appear; not exhaustively verified.
- **Cross-browser**: only Chromium / Google Chrome 147 tested. No Safari, no Firefox.
- **Tablet portrait/landscape distinction**: only the 4 widths in the brief were screenshot-captured.

---

## 6. Screenshot / Evidence Artifact Paths

All under `/media/ccs/HueiRu_disk2/github-current/grapycalpis/iQ-Studio/.agent-artifacts/`:

- `reality-check.md` — this report
- `screenshots/asset-audit.json` — full per-page link/img/video HTTP-status data (machine-readable, includes the 22 broken homepage links and 12 broken yocto images)
- `screenshots/home-360.png` — homepage 360 × 900 (visible horizontal overflow / clipped card text — B5)
- `screenshots/home-360-tall.png` — homepage 360 × 2400 full-page (confirms clipping persists down the page)
- `screenshots/home-768.png` — homepage 768 × 900 (renders correctly)
- `screenshots/home-1280.png` — homepage 1280 × 900 (renders correctly)
- `screenshots/home-1920.png` — homepage 1920 × 900 (renders correctly)
- `screenshots/home-1920-full.png` — homepage 1920 × 1080 (renders correctly, with sidebar visible)
- `screenshots/yolo26-360.png`, `yolo26-768.png`, `yolo26-1280.png`, `yolo26-1920.png` — content-heavy yolo26 page across all 4 viewports
- `screenshots/yolo26-360-full.png`, `yolo26-360-tall.png` — yolo26 page full-height at 360
- `screenshots/yocto-broken-imgs-1280.png` — direct visual evidence of B2 (empty image slots throughout the q911 yocto page)
- `screenshots/ubuntu-broken-imgs-1280.png` — same bug on `q911/ubuntu/`
- `screenshots/sdks-iqs-vlm-1280.png` — direct visual evidence of N3 (bare github user-attachments URL where a demo video should be)
- `/tmp/srv.log` — http.server access log
- `/tmp/chrome*.log` — chromium headless logs (CDP runs)

Raw command outputs are inline above; the asset-audit.json captures the per-link HTTP status for every reference on every sampled page.

---

## 7. Required Fixes Before a Re-Test

Listed in priority order:

1. **B1** — fix homepage resource-table links (raw HTML in README → mkdocs-canonical URLs or delete the table).
2. **B2** — fix `./fig/` paths in `q911/yocto.md` and `q911/ubuntu.md` (point at `../fig/...` or move the assets).
3. **B3** — confirm the public GitHub repo URL and update `mkdocs.yml`; if private, disable the edit-link feature.
4. **B4** — once B3 is fixed, override the homepage edit URL to `README.md`.
5. **B5** — fix horizontal-overflow on the "Pick Your Path" cards at 360 px.
6. **B6** — run `tools/compress_gifs.sh` on `vlm-demo.gif` (and the four other 10+ MB GIFs in N7).
7. **N1**, **N2** — fix the inventory's P0 broken links (`ota → IQS.md`, `yolo26 → q911 anchor`).
8. **N3** — re-host the VLM SDK demo video so it renders embedded on the Pages site.

After fixes, re-run this exact test pass. The reality-check passes when:
- The homepage body has 0 broken in-content links.
- `q911/yocto/` and `q911/ubuntu/` each render their photos (visual screenshot evidence).
- Every "Edit on GitHub" URL returns HTTP 200 (curl-tested).
- 360 px viewport screenshot has no clipped content.
- Homepage `vlm-demo` asset is under 5 MB (or transcoded to `<video>` with a sub-MB poster).
- B/N issues 1-3 from the inventory are closed.

Until then: **NO-GO**.
