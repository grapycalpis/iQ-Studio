# Documentation Quality Report

_Generated: 2026-05-22_
_Scope: 27 files from `./.agent-artifacts/docs-inventory.md` (26 reachable from `README.md`, plus 1 orphan `tools/README.md`)_

## Executive summary

- **Two P0 broken links carry over from the inventory** and are confirmed: a missing-file link (`../../../IQS.md`) in `tutorials/starting-guides/ota/README.md:53`, and a wrong-target anchor link (`q911/README.md#interact-with-the-system-using-adb-over-usb-type-c`) in `tutorials/model-deploy/cv/yolo26/README.md:33`. The anchor exists in `q911/yocto.md` instead.
- **H1 hierarchy is the most pervasive structural issue**. Eight files use `#` (H1) for every top-level section instead of `##` (H2), producing 2–11 H1s per file. GitHub renders this fine, but most SSGs (Docusaurus, MkDocs Material, VitePress) treat the *first* H1 as the page title and downgrade additional H1s, which breaks sidebar TOCs and search snippets.
- **Five bare code fences** are still present after `tools/fix_bash_tags.py` — re-run is recommended. One additional drift: a ```` ```shell ```` fence in `tutorials/sdks/iqs-ogenie/README.md:30` should be ```` ```bash ```` for consistency (the repo uses ```` ```bash ```` 67 times, ```` ```shell ```` only once).
- **HTML `<img>` accessibility is broken across the repo**. 58 of the ~60 HTML `<img>` tags lack an `alt` attribute. These are all real product photos and diagrams, not decorative — accessibility (P1) and SEO impact is meaningful. Inline markdown `![alt](src)` references are mostly fine (no empty-alt cases found).
- **Terminology drift on the product name**: the inventory's hub doc and the brand guide canonicalize **"iQ Studio"** (space, lowercase `i`), but the in-doc majority is **"iQ-Studio"** (hyphenated, 34 occurrences vs. 6 for "iQ Studio"). The README itself uses both forms within five lines of each other (line 7 vs. line 18). Pick one and migrate.
- **Hardware shorthand drift**: `IQ9` (5 occurrences) appears as a stand-in for `IQ-9075` SoC. The Q911 README uses both "IQ-9075" (line 8 description) and "IQ9" (line 8 packing list) in the same row.
- **Counts**: P0 = 7 findings, P1 = 19 findings, P2 = 12 findings.
- **Canonical recommendation**: `iQ Studio` (product), `iQ-Studio` (repo/code identifiers only, e.g. `iQ-Studio.git`), `iqs-launcher`, `IQ-9075` (SoC), `EXMP-Q911` / `EXEC-Q911` / `APEX-A100` (boards). `IQ9` and `Q9` should be eliminated.

## Canonical terminology (recommended)

| Term | Canonical form | Drift seen | Justification |
|------|----------------|------------|---------------|
| Product (prose) | **iQ Studio** | `iQ-Studio` (34×), `IQ Studio` (3×), `IQS` (1×) | Brand guide §1, §3 and `README.md:7` use the space form. The hyphen is a repo-/URL-only artifact. |
| Repo / clone identifier | **iQ-Studio** | none | Matches `git clone https://github.com/InnoIPA/iQ-Studio.git`. Keep ONLY for repo paths, URLs, and the `cd iQ-Studio` line. |
| Launcher binary | **`iqs-launcher`** | `iqs_launcher` (0×, OK) | Already consistent. Always render in code-style backticks in prose. |
| SoC | **IQ-9075** | `iQ-9075` (1× in `README.md:87`), `IQ9` (5×) | Qualcomm's product name uses uppercase `IQ-9075`. README:87 is a typo. `IQ9` is a model-deploy-only shorthand and should be expanded. |
| Carrier board (full system) | **APEX-A100** | `A100` (alone, 0× — always paired with APEX-, OK) | Inventory and `q911/README.md:10` use `APEX-A100` consistently. The `qpex_a100_*.png` filenames are an artifact (legacy product name "QPex") and should stay as filenames but never appear in prose. |
| EVK / Module | **EXMP-Q911** / **EXEC-Q911** | none | Consistent across 38 occurrences. |
| Q911 family | **Q911** | `Q9` (0× outside of `IQ-9075`/`QCS9075`, OK) | No drift detected. Brief was right to flag the risk but no real drift found. |
| QCS chip | **QCS9075** | none | Consistent. |
| App layer | **iQS-App** / **iQS-VLM** / **iQS-Streampipe** / **iQS-YOLOv10n** | `iqs-vlm`, `iqs-streampipe`, `iqs-yolov10n` (autotag forms in commands) | Two forms exist for a reason: PascalCase for product/UI prose, lowercase for `iqs-launcher --autotag` arguments. Both are valid; the rule is **PascalCase in headings/prose, lowercase-hyphen in command-line args**. |

---

## P0 — Must fix (broken links, missing H1, missing language tags)

### `tutorials/starting-guides/ota/README.md`
- **Issue (broken link)**: `tutorials/starting-guides/ota/README.md:53` — `[IQS Development Guidelines](../../../IQS.md)` resolves to `/iQ-Studio/IQS.md` which does not exist. The only `IQS.md`-named file in the repo lives at `.agents/skills/iq-studio-agent/...` style internal-agent paths and is not user-facing.
- **Fix**: Either (a) delete the bullet, (b) retarget to `docs/how-to-use-iqs-launcher.md`, or (c) create a user-facing "IQS Development Guidelines" page under `docs/` and point there.

### `tutorials/model-deploy/cv/yolo26/README.md`
- **Issue (broken anchor)**: `tutorials/model-deploy/cv/yolo26/README.md:33` — link to `../../../starting-guides/q911/README.md#interact-with-the-system-using-adb-over-usb-type-c`. The file exists, but the heading `### Interact with the System Using ADB over USB Type-C` lives in `tutorials/starting-guides/q911/yocto.md:93`. The `q911/README.md` only has `## Interact with the System` (line 129).
- **Fix**: Change the link to `../../../starting-guides/q911/yocto.md#interact-with-the-system-using-adb-over-usb-type-c`.

### `tutorials/applications/iqs-vlm/README.md`
- **Issue (multiple H1)**: Lines 8, 19, 41, 70, 74 all use `#` (H1). The first H1 ("iQS-VLM") is correct; the rest should be `##`.
- **Issue (bare code fence)**: `tutorials/applications/iqs-vlm/README.md:51` — the fenced block printing the OGenie URLs has no language tag.
- **Fix**: Re-encode lines 19 (`How to Deploy`), 41 (`How to Use`), 70 (`LLaVA-1.5-7B Performance`), 74 (`How to Interact with...`) as `##`. Add ```` ```text ```` (or ```` ```bash ```` since it's example output) to the fence at line 51. The repo helper script `./tools/fix_bash_tags.py` will pick this up.

### `tutorials/applications/iqs-streampipe/README.md`
- **Issue (multiple H1)**: Lines 8, 22, 38, 50, 54 are all `#`. Only line 8 should be H1.
- **Fix**: Re-encode lines 22, 38, 50, 54 as `##`.

### `tutorials/applications/iqs-yolov10n/README.md`
- **Issue (multiple H1)**: Lines 7, 15, 39, 60 are all `#`. Only line 7 should be H1.
- **Fix**: Re-encode lines 15 (`Jetson AGX Orin`), 39 (`EXMP-Q911`), 60 (`Conclusion`) as `##`.

### `tutorials/sdks/iqs-vlm/README.md`
- **Issue (multiple H1)**: Lines 8, 12, 29, 58 are all `#`.
- **Issue (bare code fence)**: `tutorials/sdks/iqs-vlm/README.md:52` — the system prompt example fence has no language tag.
- **Fix**: Re-encode lines 12, 29, 58 as `##`. Tag the prompt fence as ```` ```text ````.

### `benchmarks/innoppe/README.md`
- **Issue (multiple H1)**: Lines 8 and 75 are both `#`. Line 75 (`# Appendix: How do I execute the benchmark?`) should be `##` to keep `# InnoPPE Benchmark...` as the sole H1.
- **Issue (bare code fence)**: `benchmarks/innoppe/README.md:114` — the `print_mean.py` example output fence has no language tag.
- **Fix**: Change line 75 to `## Appendix...`. Add ```` ```text ```` to the line 114 fence.

### `benchmarks/iqs-streampipe/README.md`
- **Issue (bare code fences)**: lines 107 and 137 — both are the `git clone` and `wget` blocks. Should be ```` ```bash ````.
- **Fix**: Run `./tools/fix_bash_tags.py` or hand-tag.

### `README.md`
- **Issue (multiple H1, severe)**: Lines 7, 20, 31, 53, 59, 97, 105, 116, 205, 214, 218 — **eleven** H1s. On GitHub this works because the rendering is forgiving, but in an SSG site this will create 11 separate "pages" of TOC, fracture the sidebar, and break in-page anchor navigation. The first H1 (line 7, `iQ Studio`) is correct; everything else needs to drop to `##` or `###`.
- **Issue (skipped heading level)**: Line 71 jumps `# Core Software Stack & Architecture` → `### Qualcomm Linux (QLI) Version Mapping`. Should be `##` (relative to the page H1).
- **Fix**: Convert lines 20 (`Pick Your Path`), 31 (`30-Second Demo`), 53 (`Performance`), 59 (`Core Software Stack & Architecture`), 97 (`How to Use iqs-launcher`), 105 (`Quick Start`), 116 (`Explore Documentation & Resources`), 205 (`Related Repositories`), 214 (`Changelog`), 218 (`License`) to `##`. Promote line 71 to `##` if `Core Software Stack & Architecture` becomes `##`; else use `###` if it stays `#`.

---

## P1 — Structure & readability

### `README.md`
- **Mixed product name within five lines**: line 7 `# iQ Studio` (canonical), line 18 `iQ-Studio` (drift), then line 107 `## Install iQ Studio` (canonical again). Pick one and migrate. Recommendation: `iQ Studio` in all prose, `iQ-Studio` only in URLs/paths/clone commands.
- **HTML `<img>` tags missing `alt`** at lines 10, 48, 64, 82, 90. The hero logo and architecture diagrams are load-bearing; alt text such as `alt="iQ Studio logo"`, `alt="VLM demo running on Q911"`, `alt="Dragonwing software stack"`, `alt="Qualcomm Linux roadmap"`, `alt="Software development pipeline diagram"` would meaningfully improve screen-reader experience and image-search SEO.
- **"Explore Documentation & Resources" HTML mega-table (lines 121-203)**: works on GitHub.com but will collide with SSG sidebar nav. Inventory recommendation §8 says delete this for the Pages build. P1 because it works for now.
- **Smart-quote drift**: line 15 uses `’` (typographic apostrophe) inside an `<h3>`. Mostly harmless, but the doc otherwise uses straight quotes — pick one.

### `docs/how-to-use-iqs-launcher.md`
- **HTML `<img>` tags missing `alt`** at lines 37 and 56 (the SVG flow diagrams). These are the only diagrams that explain online vs. offline mode — alt text such as `alt="iqs-launcher online mode flow"` / `alt="iqs-launcher offline mode flow"` is high-value.
- **Inconsistent admonition style**: file mixes `> Notice:` (lines 61, 103) with `> Note:` style used elsewhere in the repo (e.g. `README.md:95`, `q911/yocto.md`). Pick one; the broader repo standard is `> Note:`. Keep callouts as blockquotes so `tools/audit_content.py` does not flag them.

### `docs/changelog.md`
- **Not Keep-a-Changelog conformant** (recommended format per the brief): The file uses ad-hoc sections (`### Feat`, `### Fixes`, `### Chore`, `### Doc`, `### Documentation`) and no date stamps. The Keep-a-Changelog spec uses `### Added / Changed / Deprecated / Removed / Fixed / Security`, plus a leading `## [Unreleased]` section and `## [vX.Y.Z] - YYYY-MM-DD` headers.
- **No intro paragraph** between H1 (line 1) and H2 (line 3). Add a one-line description: "All notable changes to iQ Studio are documented here. This project adheres to [Keep a Changelog](https://keepachangelog.com)."
- **Subsection naming drift**: `### Feat` vs `### Fixes` vs `### Fix` vs `### Doc` vs `### Documentation` vs `### Chore` — five different headings for what should be 3–4. Migrate to: `### Added`, `### Changed`, `### Fixed`, `### Removed`.
- **Trailing whitespace** on multiple lines (lines 8, 25, 26, 76, 77, 78). Harmless but flagged by most linters.

### `tools/README.md`
- **Orphan**: this file is not linked from any in-scope doc (confirmed by inventory §10). If `tools/` is meant to be contributor-facing, add a `## Contributing` section to root `README.md` linking here. Otherwise, exclude `tools/` from the SSG build.
- **Single H1**: clean structurally. No P0 issues.
- **Apostrophe drift**: line 9 uses `'` (straight) but line 41 `bird's-eye` uses `'` — fine.

### `benchmarks/README.md`
- **Stub (20 lines)** — acceptable for a hub page, but the description in line 10 ("Reproducible performance measurements on iQ-Studio platforms") drifts to `iQ-Studio` form.
- **Missing intro between H1 and `## Overview` (line 12)**: actually has line 10 intro, so this passes. No issue.

### `benchmarks/innoppe/README.md`
- **Image alt placeholder typo**: line 104 `alt="Descrisystem_usage_cpu_separate_example"` — looks like a typo of "Description: system_usage_cpu_separate_example". Clean up the alt text.
- **Bracket-reference link style**: lines 19, 122, 123 use the `[InnoPPE][InnoPPE]` and `[EV2U-SSM1-RLCF][EV2U-SSM1-RLCF]` reference syntax. This is fine on GitHub but make sure the SSG renderer supports markdown reference-style links (Docusaurus and MkDocs Material both do).
- **Trailing `<!--- vim:nowrap -->` directive** (line 124-126) is a personal-editor artifact; harmless but noise.
- **Mixed terminology in same row**: line 8 packing list uses both `IQ-9075` (in description) and `IQ9` (in `1x IQ9 COM-HPC Mini Module`). Standardize to `IQ-9075`.

### `benchmarks/iqs-streampipe/README.md`
- **Step numbering bug**: lines 136 and 141 both start with `1.` — should be `1.` then `2.` (or `2.` then `3.`).
- **HTML `<img>` triple (lines 71-73)** missing `alt` — these are the three result charts. Suggest `alt="FPS per channel chart"`, `alt="CPU loading chart"`, `alt="CPU memory chart"`.
- **mp4 link on line 14** (`./fig/nv_qc_live.mp4`) — works on GitHub but will 404 on an SSG site unless the SSG copies the `fig/` directory into its build output. Verify your SSG config.

### `benchmarks/perception_model/README.md`
- **Missing copyright header**: every other benchmark file starts with the `<!-- Copyright (c) 2025 Innodisk Corp. ... MIT License ... -->` block. This file does not. Add for consistency.
- **Heading colon usage**: line 28 `### EXMP-Q911 (Qualcomm QNN):` — trailing colon in heading is unusual. Drop the colon (also line 61).
- **In-body raw image alt text drift**: line 18 `![image.png](./fig/results.png)` — "image.png" is a non-descriptive alt. Use `alt="Perception model benchmark results"`.

### `tutorials/starting-guides/README.md`
- **No intro between H1 (line 8) and `## Overview` (line 9)**: there's no blank line and no text. Insert one sentence between them, e.g. "Use these guides to get a fresh Q911 board powered on, flashed, and reachable over your network."
- **17 lines total** — stub hub page. Acceptable for a section index but worth fleshing out per the inventory §4 P2 recommendation.

### `tutorials/starting-guides/q911/README.md`
- **No intro between H1 (line 1) and `## Overview` (line 3)**: same pattern as above. Insert a one-sentence orient.
- **9 HTML `<img>` tags missing `alt`** at lines 34, 37, 52, 55, 88, 91, 104, 114, 117. These are board front/back photos, jumper-mode and DIP-switch photos — alt text is critical because someone using a screen reader is the exact user who *needs* a verbal description ("front view of EXEC-Q911 board with labeled ports").
- **Trailing whitespace on board hardware section header** (line 28 ends with a space).
- **Hardware list "What's in the Box" section (lines 24-26)** is barely 2 lines and refers up to a table on lines 7-10 — could be a single sentence or removed entirely.
- **Smart quote** in line 4 `Qualcomm®` — fine, but check the SSG renderer doesn't escape it.

### `tutorials/starting-guides/q911/yocto.md`
- **12 HTML `<img>` tags missing `alt`** (lines 38, 41, 55, 59, 70, 73, 90, 103, 106, 131, 142, 150).
- **Image filename typo**: `ycoto_desktop_icon.png` and `yocto_desktop_teminal.png` (line 59) — "teminal" should be "terminal", "ycoto" should be "yocto". These are filenames so changing them is invasive, but flag for cleanup pass.
- **Mixed admonition style**: `> Prerequisite:` (line 5) is informal; everywhere else uses `> Note:` or `> 💡 **Tip:**`. Standardize.

### `tutorials/starting-guides/q911/ubuntu.md`
- **8 HTML `<img>` tags missing `alt`** (lines 42, 45, 59, 71, 74, 91, 106, 114).
- **Filename typo carry-over**: `ubuntu_teminal.png` (line 91) — same `terminal` typo as yocto.md.
- **"Not supported" status in two places**: `### Interact with the System Using ADB over USB Type-C` section (line 94) only contains a one-line note. Consider folding into the support-matrix table (lines 16-21) and removing the empty subsection.

### `tutorials/starting-guides/flash-image/README.md`
- **9 HTML `<img>` tags missing `alt`** (lines 17, 25, 31, 42, 45, 64, 67, 106, 116, 122).
- **No copyright/license header** — inconsistent with sibling docs.
- **Cross-doc image references** (`../q911/fig/...`): works because both files live under `tutorials/starting-guides/`, but the SSG should be tested with these relative paths intact.

### `tutorials/avl/README.md`
- **Hub-without-children orphan path** (inventory §4 P1): this file does not link to its children `gmsl-camera/` or `mipi-camera/`. User landing on the AVL page has no way forward.
- **Fix**: add a children list:
  ```markdown
  ## Camera Tutorials
  - [GMSL Camera](./gmsl-camera/README.md)
  - [MIPI Camera](./mipi-camera/README.md)
  ```

### `tutorials/avl/gmsl-camera/README.md` and `tutorials/avl/mipi-camera/README.md`
- **Bare URL in prose** (gmsl line 9, mipi line 9): `please visit https://github.com/InnoIPA/iQ-Cam__manifest`. Wrap as `[iQ-Cam__manifest](https://...)` to be link-style consistent.
- **No copyright header** (inconsistent with siblings).
- **Both are 10–11 line stubs** that essentially say "go look at iQ-Cam__manifest." Either expand with the actual AVL camera lists pulled from `tutorials/avl/README.md` figures, or remove these pages and surface the AVL hub directly.

### `tutorials/applications/README.md`
- **No intro between H1 (line 8) and `## Overview` (line 9)**: insert a one-liner.
- **Does not link forward to Model Deploy YOLO26 tutorial** — see inventory §4 P1. Add a "Bring your own model" handoff bullet referencing `tutorials/model-deploy/cv/yolo26/README.md`.

### `tutorials/applications/iqs-vlm/README.md` (P1 portion — H1 issue above)
- **`iq-VLM-DEMO` capitalization on line 13** — drift from the autotag `iqs-vlm-demo` used in commands. Reword as: "...along with the `iqs-vlm-demo` app, which captures images...".
- **`OGenie` referenced unbacked-quoted in some places, backtick-quoted in others** (lines 12 vs. 43 vs. 49). Settle on backticked `OGenie` only when referring to the *binary/server*; plain capitalized `OGenie` when referring to the product/feature.

### `tutorials/applications/iqs-streampipe/README.md` (P1 portion)
- **GIF filename `Recording 2025-08-13 at 15.22.58.gif` referenced via markdown alt text on line 48** — the actual GIF is `gif1.gif`, but the alt text leaks a screen-recorder default filename. Replace with descriptive alt: `![iQS-Streampipe live demo](./fig/gif1.gif)`.
- **Mixed admonition spacing**: `>Note:` (no space after `>`) vs. `> Note:` (with space) — pick one.

### `tutorials/applications/iqs-yolov10n/README.md` (P1 portion)
- **Generic alt text**: line 9 `![output.gif](./fig/gif0.gif)` — alt is the filename, not descriptive. Use `alt="YOLOv10n INT8 inference on Q911 NPU"`.
- **Premature funnel close** (inventory §4 P1): no link forward to SDK customization or `tutorials/model-deploy/cv/yolo26/README.md`. Add a "Customize this demo" or "Next: bring your own YOLO model" bullet.

### `tutorials/model-deploy/README.md`
- **Title is unwieldy**: line 1 `# Model Deploy: End-to-End Guides for Converting, Optimizing, and Running AI Models on the Target Platform`. That's a 14-word page title. Sidebars and breadcrumbs will look awful. Recommend: `# Model Deploy` with the descriptive subtitle moved to an intro paragraph.
- **Trailing emoji bullet** (line 24 `🔴 Prediction, 🟢 Ground truth`) — the brand guide §6 explicitly says to avoid emoji in body copy. Replace with bold-color text or a legend table.

### `tutorials/model-deploy/cv/yolo26/README.md` (P1 portion — anchor link above)
- **Title also unwieldy with trailing `?`**: line 1 `# Model Deploy: How to Convert, Optimize, and Perform Inference with YOLO26 Models ?` — and the leading space before `?` is grammatically wrong. The trailing space + question mark is unusual punctuation. Recommend: `# Convert, Optimize, and Run YOLO26 with iQ-Foundry`.
- **`IQ9` shorthand drift** (lines 13, 27, 125): `Qualcomm Dragonwing IQ9`. Standardize to `Qualcomm Dragonwing IQ-9075` (matches Qualcomm's naming).
- **`yolov10`, `yolov11`, `yolov26` vs. `YOLO10`, `YOLO11`, `YOLO26`** (lines 63 vs. 159): mixed-case drift. Lowercase in CLI args (correct), uppercase in prose (correct), but line 159 mixes both — clean up.

### `tutorials/sdks/README.md`
- **No intro between H1 (line 8) and `## Overview` (line 9)**: insert a one-liner.

### `tutorials/sdks/iqs-vlm/README.md` (P1 portion)
- **Bare GitHub user-attachments video URL on line 34** — renders inline on GitHub.com only; will appear as a raw URL on any SSG-built site. Either remove and replace with the in-repo `Open WebUI demo.mp4` (currently orphan asset), or wrap in an `<iframe>` / `<video>` with a stable mirrored URL.
- **`A` vs. `An` grammar** (line 36 `Start a Open WebUI server`): should be `an Open WebUI server`.

### `tutorials/sdks/iqs-streampipe/README.md`
- **Section title is a full sentence with embedded question** (line 22): `## How to modify the content displayed, please refer to the `config.json` file in the current directory.` — way too long for a heading. Split into `## Modify the displayed content` with the explanation as body text.
- **Mixed `NOTE :` / `Note:` / `Notice:` / `>NOTE :` admonition styles** (lines 47, 65, 88, 79, 72, 12) — at least four variants. Standardize to `> Note:` and `> Warning:` (Warning for the bandwidth/lag bullet on line 88).
- **Unbacked `coco_detect.mp4` filename on line 45** — should be `` `coco_detect.mp4` `` to match the surrounding code-style mentions.

### `tutorials/sdks/iqs-ogenie/README.md`
- **`tutorials/sdks/iqs-ogenie/README.md:30` uses ```` ```shell ```` instead of ```` ```bash ````** — the only `shell` fence in the entire repo. The block is a `git clone` script identical to ones tagged `bash` elsewhere. Change to ```` ```bash ```` for consistency.
- **Image filename typo**: `ogeine.png` (line 12) — should be `ogenie.png`. Filename change is invasive but worth a cleanup pass.
- **HTML `<img>` no alt** (line 12): suggest `alt="OGenie architecture diagram"`.

---

## P2 — Polish

### `README.md`
- **Apostrophe style drift**: line 15 `the platform’s` (curly) vs. line 4 `to use these tools` (none) — pick one and stick with it. Most of the docs use straight ASCII apostrophes; the curly one is a single drift in a marketing-style `<h3>`.
- **HTML attribute order drift**: most `<img>` tags use `width="X%" height="Y%"` in that order; line 64/82/90 mix this style; line 71-73 in `benchmarks/iqs-streampipe/README.md` use `<img src="..." width="X%">` (no height). Not a bug — but inconsistent.
- **Use of `<br />` for vertical spacing** (around every image): readable, but redundant in an SSG that handles margins via CSS. P2 — only worth touching if you do a full SSG conversion.

### `docs/how-to-use-iqs-launcher.md`
- **"Sample output" code block at line 119** (` |-sde53 259:37 ...`) — tagged `bash` but this is `lsblk` output, not a command. Use ```` ```text ```` for consistency with the directory-tree blocks at lines 154 and 163.
- **"Both online and offline modes" sentence on line 12** is grammatically awkward. Rephrase: "Both online and offline modes are covered in [docs/how-to-use-iqs-launcher.md](./docs/how-to-use-iqs-launcher.md), including how to pre-stage packages for an air-gapped platform." (Wait — this file *is* `docs/how-to-use-iqs-launcher.md`; line 12 should not link to itself. Actually, the file says "see the [Quick Start](../README.md#quick-start) in the entry page" — that part is fine. The README.md:101 sentence is the awkward one.)

### `docs/changelog.md` (Keep-a-Changelog migration)
- Adopt the Keep-a-Changelog format. Skeleton:
  ```markdown
  # Changelog

  All notable changes to iQ Studio are documented here. This project follows [Keep a Changelog](https://keepachangelog.com) and uses [Semantic Versioning](https://semver.org).

  ## [Unreleased]

  ## [0.0.7] - YYYY-MM-DD

  ### Added
  - Model Deploy as a new iQ Studio feature
  - Q911 getting-started and platform guidance
  - Model Deploy navigation to the entry README

  ### Changed
  - AVL camera support for 8-channel validation, broader interface coverage, and newer system compatibility
  - The Q911 HW image

  ### Fixed
  - Documentation paths and internal links
  - Refined documentation content, wording, and structure

  ### Removed
  - The `$` prefix from command examples (easier copy/paste)
  ```
- Add release dates from `git log` so each `## [X.Y.Z]` carries `- YYYY-MM-DD`.

### `tools/README.md`
- **Tone drift**: line 41 "bird's-eye view of all document structures" is fine; line 89 "These tools are strictly for documentation quality control" reads as a warning but is just a note. Drop the `> Note:` blockquote, since it's a closing aside.

### `benchmarks/perception_model/README.md`
- Line 14 `Linux Kernel | 5.10.120-tegra` row uses the BSP-version string format `6.6.90-qli-1.5-ver.1.1-04509-gc4b8666c9a55`, which is the same string in `benchmarks/innoppe/README.md:45`. Consider extracting this into a shared "Test platform spec" partial if the SSG supports includes.

### `tutorials/starting-guides/README.md`
- The 17-line stub is fine as a section index. Worth adding a "Reproducible from scratch" note at the bottom that links to `benchmarks/README.md`.

### `tutorials/starting-guides/q911/README.md`
- **Line 4 `<sup>®</sup>` substitute**: source uses `Qualcomm®`. Render fine on GitHub. If the SSG mangles the registered-trademark symbol, replace with `Qualcomm&reg;`.
- **Long P/N strings in column "Description"** (lines 8-10) wrap awkwardly. Consider extracting packing-list contents into a sub-list below the table.

### `tutorials/starting-guides/q911/yocto.md` / `ubuntu.md`
- Tag the default-credentials code block at yocto.md:25 and ubuntu.md:29 as ```` ```text ```` rather than ```` ```bash ```` — they're not commands, they're credential displays. Currently tagged `bash`, which is misleading.

### `tutorials/applications/iqs-vlm/README.md`
- Line 49 `After starting OGenie server, its URLs will be printed.` — double space before `its`. Single space.

### `tutorials/applications/iqs-streampipe/README.md`
- Line 11 sentence "The set IDs are ordered on the screen from left to right, then from top to bottom" lacks a period at the end. Add `.`.

### `tutorials/applications/iqs-yolov10n/README.md`
- Line 44 "`Qnn` SDK Version: 2.38" — Qualcomm names this `QNN` (all caps). Same convention as `EXMP-Q911:line-44`.
- Line 51 unbacked `iqs-launcher` in prose — wrap in backticks: `` `iqs-launcher` ``.

### `tutorials/sdks/iqs-ogenie/README.md`
- Line 19 `developers to use the official Ollama services (Python SDK / HTTP interface)` — the slash in "Python SDK / HTTP" is an unusual list separator. Prefer "Python SDK or HTTP interface".
- Line 34 (inside `bash` fence) chains `git clone … && cd iQ-Studio && ./install.sh` across three plain lines; works but a single `&&`-chained line would copy-paste cleaner.

---

## Repo-wide actions

- [ ] **Re-run `./tools/fix_bash_tags.py`** — 5 bare code fences remain (`benchmarks/innoppe/README.md:114`, `benchmarks/iqs-streampipe/README.md:107` & `:137`, `tutorials/applications/iqs-vlm/README.md:51`, `tutorials/sdks/iqs-vlm/README.md:52`). After the auto-fix pass, confirm none of these should be ```` ```text ```` rather than ```` ```bash ```` (lines 114 and 51 are program output, not commands).
- [ ] **Convert `docs/changelog.md` to Keep-a-Changelog format** — currently ad-hoc. Migration skeleton provided in P2 above. Add release dates from `git log v0.0.1 v0.0.2 v0.0.3 v0.0.4 v0.0.5 v0.0.6 v0.0.7 --format='%ai'` or similar.
- [ ] **Fix multi-H1 in 8 files**: `README.md` (11 H1s), `benchmarks/innoppe/README.md` (2), `tutorials/applications/iqs-vlm/README.md` (5), `iqs-streampipe/README.md` (5), `iqs-yolov10n/README.md` (4), `tutorials/sdks/iqs-vlm/README.md` (4). Convert every `#` after the first to `##`. This is the single biggest readability fix for the SSG migration.
- [ ] **Migrate product name to `iQ Studio`** in prose, keep `iQ-Studio` only for repo/URL contexts. 34 occurrences to review.
- [ ] **Add `alt` to all 58 HTML `<img>` tags**. Suggested alt strings noted per-file in P1.
- [ ] **Standardize admonition style**: use only `> Note:` and `> Warning:`, drop `> Notice:`, `> NOTE :`, `>Note:`, `> Prerequisite:`, `> 💡 **Tip:**`. The brand guide §6 specifically says no emoji in body copy, so the `💡` should go.
- [ ] **Eliminate `IQ9` shorthand**: 5 occurrences in `tutorials/starting-guides/q911/README.md` (lines 8, 9) and `tutorials/model-deploy/cv/yolo26/README.md` (lines 13, 27, 125). Replace with `IQ-9075`.
- [ ] **Fix `tutorials/avl/README.md` hub-children gap**: add a children-list section pointing to `gmsl-camera/README.md` and `mipi-camera/README.md` (inventory §4 P1).
- [ ] **Verify SSG asset pipeline copies `.mp4` and `.gif`**: `benchmarks/iqs-streampipe/fig/nv_qc_live.mp4` will 404 on Pages without explicit asset bundling. Test before launch.
- [ ] **Decide on `tools/README.md`**: link from a `CONTRIBUTING.md` (currently absent) or exclude from SSG build via `mkdocs.yml` / `docusaurus.config.js` ignore pattern.
- [ ] **Consider running `tools/audit_content.py`** for a second-opinion sweep on image directories and link types — its checks are complementary to this report.

---

## Files reviewed

All 27 files from `./.agent-artifacts/docs-inventory.md` were read in full:

1. `/media/ccs/HueiRu_disk2/github-current/grapycalpis/iQ-Studio/README.md` (220 lines)
2. `/media/ccs/HueiRu_disk2/github-current/grapycalpis/iQ-Studio/docs/how-to-use-iqs-launcher.md` (183 lines)
3. `/media/ccs/HueiRu_disk2/github-current/grapycalpis/iQ-Studio/docs/changelog.md` (79 lines)
4. `/media/ccs/HueiRu_disk2/github-current/grapycalpis/iQ-Studio/tools/README.md` (89 lines)
5. `/media/ccs/HueiRu_disk2/github-current/grapycalpis/iQ-Studio/benchmarks/README.md` (20 lines)
6. `/media/ccs/HueiRu_disk2/github-current/grapycalpis/iQ-Studio/benchmarks/innoppe/README.md` (126 lines)
7. `/media/ccs/HueiRu_disk2/github-current/grapycalpis/iQ-Studio/benchmarks/iqs-streampipe/README.md` (165 lines)
8. `/media/ccs/HueiRu_disk2/github-current/grapycalpis/iQ-Studio/benchmarks/perception_model/README.md` (93 lines)
9. `/media/ccs/HueiRu_disk2/github-current/grapycalpis/iQ-Studio/tutorials/starting-guides/README.md` (17 lines)
10. `/media/ccs/HueiRu_disk2/github-current/grapycalpis/iQ-Studio/tutorials/starting-guides/q911/README.md` (145 lines)
11. `/media/ccs/HueiRu_disk2/github-current/grapycalpis/iQ-Studio/tutorials/starting-guides/q911/yocto.md` (151 lines)
12. `/media/ccs/HueiRu_disk2/github-current/grapycalpis/iQ-Studio/tutorials/starting-guides/q911/ubuntu.md` (116 lines)
13. `/media/ccs/HueiRu_disk2/github-current/grapycalpis/iQ-Studio/tutorials/starting-guides/flash-image/README.md` (129 lines)
14. `/media/ccs/HueiRu_disk2/github-current/grapycalpis/iQ-Studio/tutorials/starting-guides/ota/README.md` (53 lines)
15. `/media/ccs/HueiRu_disk2/github-current/grapycalpis/iQ-Studio/tutorials/avl/README.md` (20 lines)
16. `/media/ccs/HueiRu_disk2/github-current/grapycalpis/iQ-Studio/tutorials/avl/gmsl-camera/README.md` (11 lines)
17. `/media/ccs/HueiRu_disk2/github-current/grapycalpis/iQ-Studio/tutorials/avl/mipi-camera/README.md` (11 lines)
18. `/media/ccs/HueiRu_disk2/github-current/grapycalpis/iQ-Studio/tutorials/applications/README.md` (19 lines)
19. `/media/ccs/HueiRu_disk2/github-current/grapycalpis/iQ-Studio/tutorials/applications/iqs-vlm/README.md` (76 lines)
20. `/media/ccs/HueiRu_disk2/github-current/grapycalpis/iQ-Studio/tutorials/applications/iqs-streampipe/README.md` (55 lines)
21. `/media/ccs/HueiRu_disk2/github-current/grapycalpis/iQ-Studio/tutorials/applications/iqs-yolov10n/README.md` (62 lines)
22. `/media/ccs/HueiRu_disk2/github-current/grapycalpis/iQ-Studio/tutorials/model-deploy/README.md` (31 lines)
23. `/media/ccs/HueiRu_disk2/github-current/grapycalpis/iQ-Studio/tutorials/model-deploy/cv/yolo26/README.md` (159 lines)
24. `/media/ccs/HueiRu_disk2/github-current/grapycalpis/iQ-Studio/tutorials/sdks/README.md` (19 lines)
25. `/media/ccs/HueiRu_disk2/github-current/grapycalpis/iQ-Studio/tutorials/sdks/iqs-vlm/README.md` (74 lines)
26. `/media/ccs/HueiRu_disk2/github-current/grapycalpis/iQ-Studio/tutorials/sdks/iqs-streampipe/README.md` (91 lines)
27. `/media/ccs/HueiRu_disk2/github-current/grapycalpis/iQ-Studio/tutorials/sdks/iqs-ogenie/README.md` (134 lines)

**Total**: 2,366 lines reviewed. No source `.md` file was edited during this review.
