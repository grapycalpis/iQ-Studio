# iQ Studio Docs — UX Research

Grounded in `./.agent-artifacts/docs-inventory.md`. All page references use the inventory's paths and titles. No personas, journeys, or claims are invented beyond what the inventory documents.

---

## 1. Personas

Three personas chosen because the docs inventory contains three distinct content clusters with non-overlapping primary readers:

- **Starting Guides + AVL + Flash + OTA** → hardware bring-up reader.
- **Applications + SDKs** → model/runtime customization reader.
- **Model Deploy + Benchmarks** → AI engineer porting a model from training to the device.

The "embedded developer evaluating the platform" archetype from the brief collapses into either the integrator (if the eval is hardware-led) or the ML engineer (if the eval is model-led) — there is no separate evaluation-only content (no FAQ, no separate datasheet page, no eval-kit landing) so a dedicated evaluator persona would not have a unique journey through the inventory. Better to treat evaluation as a shared *first visit* mode of the three personas below.

---

### Persona A — "Wei, the System Integrator"

**Role**: Embedded systems integrator bringing a Q911 board (Dragonwing QCS9075) up for a customer or internal pilot.

**Goals on this docs site**:
- Flash a fresh image on Q911 hardware and confirm boot.
- Pick the right OS variant (Yocto vs. Ubuntu) and know how that choice affects everything downstream.
- Connect a camera from the AVL (GMSL or MIPI) and verify it streams.
- Set up OTA so future field updates don't need a re-flash.

**Pain points / constraints**:
- On a deadline — usually has the board on the bench, EDL cable plugged in, and needs commands that work the first time.
- AVL hub ([tutorials/avl/README.md](../tutorials/avl/README.md)) does not link to its [gmsl-camera/README.md](../tutorials/avl/gmsl-camera/README.md) or [mipi-camera/README.md](../tutorials/avl/mipi-camera/README.md) children, so once they reach AVL from a "Next Steps" link they're stuck unless they remember to go back to root README.
- The AVL camera pages are stubs (10–11 lines) — likely insufficient when actually wiring up hardware.
- The OTA page references a broken `../../../IQS.md` link, which will dead-end a reader trying to follow the recommended workflow.

**Technical proficiency**: High on Linux, BSP, U-Boot/fastboot/EDL flashing, ADB, kernel/Yocto version tables. Limited on AI/ML internals.

**Key questions on arrival**:
- "Which image do I flash for this board rev and which kernel does it ship?"
- "What's the EDL/QFIL procedure for Q911?"
- "Which cameras are on the AVL and which interface (MIPI vs. GMSL) does my unit support?"
- "How do I get a shell — ADB over USB-C? Serial?"
- "Can I OTA-update later without re-flashing?"

---

### Persona B — "Priya, the ML Engineer"

**Role**: ML/computer-vision engineer responsible for getting a trained model (typically YOLO-family, sometimes VLM) running on the QCS9075 NPU at acceptable accuracy and throughput.

**Goals on this docs site**:
- Convert a YOLO model to the device runtime format and quantize to INT8.
- Understand what "FP32 → INT8" actually costs in accuracy (the [tutorials/model-deploy/README.md](../tutorials/model-deploy/README.md) page ships fp32/int8 comparison images).
- Decide whether to use a ready-made app demo ([applications/iqs-yolov10n](../tutorials/applications/iqs-yolov10n/README.md)) or to deploy a bring-your-own model via [model-deploy/cv/yolo26](../tutorials/model-deploy/cv/yolo26/README.md).
- Confirm performance vs. Jetson AGX Orin using [benchmarks/perception_model/README.md](../benchmarks/perception_model/README.md) and [benchmarks/iqs-streampipe/README.md](../benchmarks/iqs-streampipe/README.md).

**Pain points / constraints**:
- Often does *not* own the hardware — depends on someone else's bring-up. Will arrive at model-deploy pages without having read flash/OTA pages.
- The YOLO26 page links to an ADB anchor on [q911/README.md](../tutorials/starting-guides/q911/README.md) that is broken — the ADB content is actually on [q911/yocto.md](../tutorials/starting-guides/q911/yocto.md). When Priya clicks "how do I push my converted model onto the board?", she lands on the q911 README and has to hunt for ADB instructions.
- [tutorials/applications/iqs-yolov10n/README.md](../tutorials/applications/iqs-yolov10n/README.md) has zero outbound `.md` links — a reader who runs the demo and asks "now how do I swap in my own model?" hits a dead end. The funnel closes prematurely.
- There is no glossary; terms like OGenie, libGenie, HTP, QLI, autotag appear without definition (per inventory's "Missing common pages").

**Technical proficiency**: High on PyTorch/ONNX, quantization, training. Medium on edge-runtime specifics (QNN, HTP backend, the iqs-launcher tool). Low on board flashing.

**Key questions on arrival**:
- "How do I convert a YOLO model to run on QCS9075 NPU?"
- "What's the INT8 accuracy hit and is it documented?"
- "How does QCS9075 perform vs. Jetson AGX Orin on perception workloads?"
- "Is there a pre-built YOLO demo I can run to sanity-check before porting my own?"
- "How do I push my converted model to the device?"

---

### Persona C — "Dan, the Application/Runtime Developer"

**Role**: Developer customizing one of the three shipping applications (iQS-VLM, iQS-Streampipe, iQS-YOLOv10n) — usually swapping in a custom model, custom video source, or driving OGenie/Open WebUI for a VLM use case.

**Goals on this docs site**:
- Run the 30-second demo (linked from README) to confirm the runtime works on the bench.
- Understand the relationship between an **application** (e.g. [applications/iqs-streampipe](../tutorials/applications/iqs-streampipe/README.md)) and its companion **SDK** (e.g. [sdks/iqs-streampipe](../tutorials/sdks/iqs-streampipe/README.md)) — the "how to customize" recipe lives on the SDK side.
- For VLM: talk to the OGenie server via Open WebUI ([sdks/iqs-vlm](../tutorials/sdks/iqs-vlm/README.md)) and learn how to wire their own demo into OGenie ([sdks/iqs-ogenie](../tutorials/sdks/iqs-ogenie/README.md)).
- Learn the launcher mechanics: autotag, `iqs-launcher --autotag <name>`, the offline/online flow diagrams in [docs/how-to-use-iqs-launcher.md](../docs/how-to-use-iqs-launcher.md).

**Pain points / constraints**:
- Application↔SDK split is correct but non-obvious — only repeat visitors learn that "change the custom model" lives in the SDK page, not the application page. First-timers may search the application page for customization steps that aren't there.
- The VLM SDK page embeds a github user-attachments video URL that only renders on github.com — if this site is published on Pages, Dan sees a bare URL where a demo should be.
- Known-issues are scattered in section anchors on [applications/iqs-streampipe](../tutorials/applications/iqs-streampipe/README.md#known-issue) and [sdks/iqs-streampipe](../tutorials/sdks/iqs-streampipe/README.md#known-issue) with no troubleshooting hub.
- [docs/how-to-use-iqs-launcher.md](../docs/how-to-use-iqs-launcher.md) is the only doc that explains autotag, but it isn't surfaced from the SDK or application hubs — only from root README.

**Technical proficiency**: High on Python, shell, model invocation, ROS-adjacent runtimes. Medium on quantization (knows enough to consume INT8 weights). Variable on Linux internals — may or may not have done their own flash.

**Key questions on arrival**:
- "How do I run the demo without reading the whole README?"
- "How do I change the video source in iQS-Streampipe?"
- "How does OGenie expose models to Open WebUI?"
- "What does `iqs-launcher --autotag iqs-vlm-demo` actually do?"
- "Where are known issues for the streampipe app?"

---

## 2. User Journeys

### Persona A — Wei (Integrator)

#### Journey A1: First bring-up — flash an image and get a shell

- **Entry**: [README.md](../README.md) (sees "Pick Your Path" → Getting Started column)
- **Step**: [tutorials/starting-guides/README.md](../tutorials/starting-guides/README.md)
- **Step**: [tutorials/starting-guides/q911/README.md](../tutorials/starting-guides/q911/README.md) ("Q911 Platform Quick Start Guide")
- **Branch on OS choice**: [q911/yocto.md](../tutorials/starting-guides/q911/yocto.md) *or* [q911/ubuntu.md](../tutorials/starting-guides/q911/ubuntu.md)
- **Step (Ubuntu path only)**: [tutorials/starting-guides/flash-image/README.md](../tutorials/starting-guides/flash-image/README.md) — Ubuntu page is the only OS page that explicitly forwards here
- **Exit (success)**: Has a flashed board and an ADB shell from the OS-variant page's "Interact with the System using ADB over USB Type-C" section (lives in [yocto.md](../tutorials/starting-guides/q911/yocto.md), not the q911 README).
- **Likely break point**: The [q911/README.md](../tutorials/starting-guides/q911/README.md) is a *hub*, but a reader skimming for ADB steps may stop scrolling there and miss that the actual ADB walkthrough is one click deeper in `yocto.md` / `ubuntu.md`. The broken anchor from yolo26 → q911-README#adb (P0 in inventory) is symptomatic of this same trap.

#### Journey A2: Wire up an AVL camera and confirm video

- **Entry**: [README.md](../README.md) AVL row, or [q911/README.md](../tutorials/starting-guides/q911/README.md) "Next Steps" link to AVL
- **Step**: [tutorials/avl/README.md](../tutorials/avl/README.md) (19-line overview, 3 png stack images)
- **Step**: from the AVL hub the user is *stuck* — the hub has 0 outbound `.md` links to its children (P1 issue in inventory). They must back out to root README to find [gmsl-camera/README.md](../tutorials/avl/gmsl-camera/README.md) or [mipi-camera/README.md](../tutorials/avl/mipi-camera/README.md).
- **Step**: chosen camera stub (10–11 lines) — likely insufficient detail; both stubs link forward to [applications/iqs-streampipe](../tutorials/applications/iqs-streampipe/README.md) as the way to actually exercise the camera.
- **Exit (success)**: Runs `iqs-launcher --autotag iqs-streampipe` and sees a stream from the connected camera ([applications/iqs-streampipe/fig/gif0.gif](../tutorials/applications/iqs-streampipe/fig/gif0.gif)).
- **Likely break point**: AVL hub navigation dead-end. Also: the camera stubs are too thin for actual wiring/pinout/known-good cable selection that integrators expect — a real integrator may bounce out to an external vendor repo.

#### Journey A3: Set up OTA for field updates

- **Entry**: [README.md](../README.md) Getting Started column, OTA row
- **Step**: [tutorials/starting-guides/ota/README.md](../tutorials/starting-guides/ota/README.md) (53 lines, 2 png)
- **Likely break point**: P0 broken link on this page — `../../../IQS.md` resolves to a non-existent file. A reader following the recommended workflow hits a 404 and may abandon thinking the docs are stale.
- **Exit (success)**: OTA understanding without follow-through to a downstream page — OTA is the last link in the chain; the page has no "now go test it on a real demo" handoff.

---

### Persona B — Priya (ML Engineer)

#### Journey B1: "Can this board run my YOLO model fast enough?" (evaluation mode)

- **Entry**: [benchmarks/perception_model/README.md](../benchmarks/perception_model/README.md) (likely arrives via Google search for "QCS9075 vs Jetson Orin perception benchmark") or via [README.md](../README.md) → benchmarks table.
- **Step**: [benchmarks/iqs-streampipe/README.md](../benchmarks/iqs-streampipe/README.md) ("Multi-stream inference status on Jetson AGX and Qualcomm QCS9075") — confirms throughput on multi-stream.
- **Step**: [benchmarks/iqs-streampipe/README.md](../benchmarks/iqs-streampipe/README.md) links forward to [applications/iqs-streampipe](../tutorials/applications/iqs-streampipe/README.md) for the actual app.
- **Exit (success)**: Decides the platform is viable, bookmarks the model-deploy guide for a later session.
- **Likely break point**: The mp4 referenced by [benchmarks/iqs-streampipe](../benchmarks/iqs-streampipe/README.md) ([nv_qc_live.mp4](../benchmarks/iqs-streampipe/fig/nv_qc_live.mp4)) is a plain link, not embedded — and will 404 on Pages unless the build includes it. The headline "live comparison" evidence may be unreachable.

#### Journey B2: Convert and deploy a YOLO model end-to-end

- **Entry**: search for "YOLO Q911 deploy" or "QCS9075 quantize YOLO" → lands directly on [tutorials/model-deploy/cv/yolo26/README.md](../tutorials/model-deploy/cv/yolo26/README.md). Alternative entry: [README.md](../README.md) → [tutorials/model-deploy/README.md](../tutorials/model-deploy/README.md) (which shows the fp32/int8 png comparison and a flow gif).
- **Step**: [tutorials/model-deploy/cv/yolo26/README.md](../tutorials/model-deploy/cv/yolo26/README.md) (159 lines, 8 png) — the substantive how-to.
- **Step**: needs to push the converted model to the device; clicks the "Interact with the System using ADB over USB Type-C" anchor.
- **Likely break point**: P0 broken anchor — link targets [q911/README.md](../tutorials/starting-guides/q911/README.md) but the section actually lives in [q911/yocto.md](../tutorials/starting-guides/q911/yocto.md). Reader lands on the q911 hub and has to scroll/skim to figure out where ADB instructions actually live.
- **Step**: [tutorials/starting-guides/q911/yocto.md](../tutorials/starting-guides/q911/yocto.md) (if they find it) — gets ADB push working.
- **Exit (success)**: Runs the converted YOLO model on-device.

#### Journey B3: Try the pre-built YOLO demo before porting

- **Entry**: [README.md](../README.md) → [tutorials/applications/iqs-yolov10n/README.md](../tutorials/applications/iqs-yolov10n/README.md)
- **Step**: Runs the demo via `iqs-launcher --autotag iqs-yolov10n`; sees [applications/iqs-yolov10n/fig/gif0.gif](../tutorials/applications/iqs-yolov10n/fig/gif0.gif).
- **Exit (intended success)**: Wants to follow forward to "how do I swap this for my own weights?"
- **Likely break point**: [applications/iqs-yolov10n/README.md](../tutorials/applications/iqs-yolov10n/README.md) has **zero outbound `.md` links** (P1 in inventory). The applications hub also doesn't link to the YOLO26 deploy tutorial. So the natural next question — "how do I deploy mine?" — has no in-page path. Reader must bounce back to root README and navigate to Model Deploy on their own.

---

### Persona C — Dan (Application/Runtime Developer)

#### Journey C1: 30-second demo to first-screen-pixels

- **Entry**: [README.md](../README.md) (homepage, sees "30-Second Demo" with vlm-demo gif)
- **Step**: [README.md#quick-start](../README.md) `git clone … && ./install.sh`
- **Step**: [docs/how-to-use-iqs-launcher.md](../docs/how-to-use-iqs-launcher.md) for the actual `iqs-launcher --autotag …` invocation (2 svg flow diagrams: offline + online)
- **Exit (success)**: Runs `iqs-launcher --autotag iqs-vlm-demo` and sees Open WebUI come up.
- **Likely break point**: For the VLM demo, the user is then expected to go to [sdks/iqs-vlm/README.md](../tutorials/sdks/iqs-vlm/README.md) to learn the Open WebUI interaction — but that page's central demo video is a github user-attachments URL that won't render on GitHub Pages (P3 in inventory).

#### Journey C2: Customize Streampipe — different model, different video source

- **Entry**: [tutorials/applications/iqs-streampipe/README.md](../tutorials/applications/iqs-streampipe/README.md) (runs the demo first to see what it does)
- **Step**: forward link to [tutorials/sdks/iqs-streampipe/README.md](../tutorials/sdks/iqs-streampipe/README.md) ("iQS-Streampipe: How to Change the Custom Model and Video Source")
- **Exit (success)**: Has a custom-model, custom-source streampipe instance running, demonstrated by [sdks/iqs-streampipe/fig/gif2.gif](../tutorials/sdks/iqs-streampipe/fig/gif2.gif).
- **Likely break point**: If they search the **application** page for customization steps and don't notice the small forward-link to the SDK page, they may believe customization isn't documented. The mental model "applications = demo, SDKs = recipe" is correct but not signposted on the hubs ([tutorials/applications/README.md](../tutorials/applications/README.md) is 19 lines, [tutorials/sdks/README.md](../tutorials/sdks/README.md) is 19 lines — neither explains the split).

#### Journey C3: VLM — wire your own demo into OGenie

- **Entry**: [tutorials/applications/iqs-vlm/README.md](../tutorials/applications/iqs-vlm/README.md) (after running `iqs-launcher --autotag iqs-vlm-demo`)
- **Step**: [tutorials/sdks/iqs-vlm/README.md](../tutorials/sdks/iqs-vlm/README.md) — Open WebUI interaction with OGenie server
- **Step**: [tutorials/sdks/iqs-ogenie/README.md](../tutorials/sdks/iqs-ogenie/README.md) ("Run Your Own Demo with OGenie Server") — has cross-links to both VLM pages, making this the natural triangulation point for OGenie users.
- **Exit (success)**: Their own demo registered as an OGenie-served model.
- **Likely break point**: `iqs-ogenie` is listed in `tutorials/metadata.json` as an autotag that runs the *same* `run.sh` as `iqs-vlm-demo`, but the docs don't explain this overload. A reader who runs `iqs-launcher --autotag iqs-ogenie` expecting a different demo gets the VLM demo — confusing without a glossary or autotag table.

---

## 3. Entry-Path Predictions

For each persona, predicted entry mix and reasoning grounded in the docs.

### Persona A — Wei (Integrator)

| Entry channel | Likelihood | Reasoning |
|---|---|---|
| **GitHub direct link** | High | Integrators receive a link from a sales engineer or internal wiki pointing at `tutorials/starting-guides/q911/README.md` or directly at `flash-image/README.md`. The "Q911 Platform Quick Start Guide" title is exactly the deep-link bait. |
| **Homepage browse** | Medium | If they hit root [README.md](../README.md), the "Pick Your Path" three-column funnel sends them to Getting Started immediately. Inventory notes this column is "excellent funnel copy." |
| **Search** | Low | Hardware bring-up engineers more often follow handoff links than search; their query terms ("QCS9075 EDL flash", "Q911 fastboot") are specific enough but the docs use product-marketing names (iQ Studio) not always the underlying SoC vocabulary, so SEO matches are weaker. |

**Preferred entry**: Direct deep link to [tutorials/starting-guides/q911/README.md](../tutorials/starting-guides/q911/README.md) or [tutorials/starting-guides/flash-image/README.md](../tutorials/starting-guides/flash-image/README.md). The recent commit history ("split q911 guide by OS and link manifest repos") confirms the team is treating the OS-split q911 page as the canonical share-link landing.

### Persona B — Priya (ML Engineer)

| Entry channel | Likelihood | Reasoning |
|---|---|---|
| **Search** | High | ML engineers searching "YOLO Q911 deploy", "QCS9075 quantize INT8", "QNN YOLO26" will land on [tutorials/model-deploy/cv/yolo26/README.md](../tutorials/model-deploy/cv/yolo26/README.md) (the page title is "Model Deploy: How to Convert, Optimize, and Perform Inference with YOLO26 Models") or on a benchmarks page if they searched "QCS9075 vs Jetson Orin". The 8 png screenshots and 159-line depth make this page strong organic-rank bait. |
| **Homepage browse** | Medium | If they arrive at [README.md](../README.md) first, the "Pick Your Path" middle column "Deploy Models" routes them appropriately. The benchmarks links in README also catch the "is it fast enough?" visitor. |
| **GitHub direct link** | Medium | A teammate links them to [tutorials/model-deploy/README.md](../tutorials/model-deploy/README.md) (the fp32/int8 image is screenshot-worthy in chat) or to a specific benchmark report. |

**Preferred entry**: Search-driven deep link into [tutorials/model-deploy/cv/yolo26/README.md](../tutorials/model-deploy/cv/yolo26/README.md). This is the single most reference-dense AI page in the repo and it's the only one with substantive long-form conversion content. The broken anchor in this same page (P0 in inventory) hits this persona's most-likely first session — high priority to fix before any analytics-driven UX iteration.

### Persona C — Dan (Application/Runtime Developer)

| Entry channel | Likelihood | Reasoning |
|---|---|---|
| **Homepage browse** | High | Dan typically arrives via the GitHub repo root for the "30-Second Demo" gif and Quick Start install command. The vlm-demo.gif on [README.md](../README.md) is explicitly framed as a hook. |
| **GitHub direct link** | High | Cross-team handoffs ("here's how to swap the model in streampipe") will deep-link to [tutorials/sdks/iqs-streampipe/README.md](../tutorials/sdks/iqs-streampipe/README.md) — the page title is the exact phrasing of the customization recipe. |
| **Search** | Medium | Searches for "Open WebUI OGenie", "iqs-launcher autotag", "VLM demo Qualcomm" land on [sdks/iqs-vlm](../tutorials/sdks/iqs-vlm/README.md), [docs/how-to-use-iqs-launcher.md](../docs/how-to-use-iqs-launcher.md), and [applications/iqs-vlm](../tutorials/applications/iqs-vlm/README.md) respectively. |

**Preferred entry**: Homepage. Dan is the persona most aligned with the README's current marketing-style funnel; the "Pick Your Path" right column ("Customize / Build") routes them into Applications and SDKs. The inventory's recommendation to split README into a slim `index.md` plus an `overview.md` should preserve this hook — it is working as designed for Persona C.

---

## Cross-cutting friction observations (per inventory)

These are not journeys, but observed friction patterns that affect all three personas:

- **Section hub pages are too thin to onboard** ([avl/README.md](../tutorials/avl/README.md), [applications/README.md](../tutorials/applications/README.md), [sdks/README.md](../tutorials/sdks/README.md), [starting-guides/README.md](../tutorials/starting-guides/README.md) all under 20 lines). A reader landing on a hub from search or a sidebar click does not get enough context to choose a child page.
- **The two P0 broken links both block primary journeys**: OTA → IQS.md kills Journey A3 success state; YOLO26 → ADB kills Journey B2 success state.
- **No troubleshooting hub, no glossary, no FAQ** — all three personas would benefit, especially Priya (terms like HTP, libGenie, QLI undefined) and Dan (autotag overloading explained nowhere).
- **AVL hub has 0 child links** — Journey A2 break point is structural, not content-thin.
- **YOLO10n leaf has no forward path** — Journey B3 break point is structural.

---

**Researcher**: UX Researcher agent
**Research date**: 2026-05-22
**Source of truth**: [.agent-artifacts/docs-inventory.md](./docs-inventory.md)
