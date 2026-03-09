# iQ-Studio Development & AI Agent Guidelines

This document serves as the supreme principle manual for iterating and developing iQ-Studio. It outlines the core philosophy, project structure, technical standards, and the required process for both human developers and AI agents (like Claude/Antigravity) working on this repository.

## 1. Core Philosophy

- **Show Performance, Spark Imagination**: The primary goal of iQ-Studio is to help users quickly understand and explore AI capabilities on edge hardware (e.g., Jetson, Qualcomm Dragonwing QCS9075). All development should align with making this experience seamless and inspiring.
- **Technical Context as a Bridge**: Provide clear documentation of the software stack (SW Stack). Bridging the gap between BSP/Firmware and high-level AI applications is essential for user trust and technical clarity.
- **Simplicity & User Experience (UX)**: Ensure the execution commands remain as simple as `./install.sh` and `iqs-launcher --autotag ...` or `--ipk ...`. Hide complex environment setups (like BSP version checking) behind robust scripts.
- **Documentation is a First-Class Citizen**: High-quality `README.md` files with clear instructions, tables, and images/GIFs are essential. Contributions without proper documentation are incomplete.
- **Incremental & Safe Progress**: Avoid breaking existing offline or online demos. Ensure backward compatibility when modifying the core `iqs-launcher` or `mod/` Python modules.

## 2. Project Architecture & Navigation

When adding new features or applications, strictly adhere to the existing directory structure:

- `tutorials/`: Heavily used for all guides.
  - `starting-guides/`: Boot up and flashing guides (e.g., Q911).
  - `avl/`: Approved Vendor List validations (Cameras, etc.).
  - `applications/`: Vertical scenario demos (e.g., `iqs-vlm`, `iqs-streampipe`).
  - `sdks/`: Advanced developer usage for the applications.
- `benchmarks/`: Performance benchmarks and comparisons.
- `docs/`: Core project documentation, topology figures, `changelog.md`, and offline package guides.
- `mod/`: Python backend for `iqs-launcher`. Contains the logical modules for `autotag`, `run`, `ipk`, and `utils`.
- **Root Scripts**: `iqs-launcher.sh` (entry point), `launcher.py` (main logic), `install.sh` (setup).

**Rule**: Any new application or benchmark must be categorized, linked in the main `README.md` resource table (under **Explore Documentation & Resources**), and have its own dedicated, detailed `README.md`.

## 3. Technical Standards

### Python Development (`launcher.py`, `mod/*.py`)
- **Robustness**: Always handle environmental edge cases (e.g., missing BSP versions, missing IPK files, or lack of internet) gracefully with clear error messages using the `logging` module. Avoid raw `print()` for system-level execution messages.
- **Modularity**: Maintain single responsibilities. `mod/autotag.py` handles image tagging, `mod/ipk.py` handles package installation, `mod/run.py` handles script execution. Do not overlap or mix these logically.
- **Dependencies**: Do not introduce new heavy dependencies in the core launcher unless absolutely necessary. The offline installation process must remain lightweight and viable.

### Shell Scripting (`install.sh`, `iqs-launcher.sh`)
- **Safety First**: Use `set -e` to fail fast on errors.
- **Path Management**: Always use absolute paths derived dynamically from the script root (e.g., `ROOT="$(dirname "$(readlink -f "$0")")"`). Never rely on the user's `pwd`.
- **Virtual Environments**: Ensure Python scripts are executed within `iqs-venv` in a controlled manner.

### Markdown & Documentation
- **Visuals**: Place images/GIFs inside a `fig/` or `img/` directory next to the corresponding `README.md` to keep the root directory of the tutorial clean.
- **Formatting**: Use tables for comparisons. Use bash code blocks for all terminal commands. Highlight important notes/warnings using Markdown quotes (`> Note: ...`).
- **Relative Links**: Always use relative links (e.g., `./README.md` or `../fig/img.png`) instead of absolute URLs to ensure they work seamlessly offline or in different repository forks.
- **Core README Structure**:
    - Every root or major component `README.md` must feature a **`Core Software Stack & Architecture`** section with layered diagrams (HW -> Kernel/QLI -> App).
    - Environment setup and repository installation must be titled **`How to Deploy`**.
    - **`Explore Documentation & Resources`** is the central hub for tutorials, SDKs, benchmarks, and vertical scenario demos (replaces the narrower "Application" or "Tutorials" labels).
    - **`How to Use`** is reserved for high-level interaction, application execution, or future prompt/MCP features.
    - Version mapping tables (Linux Kernel vs Yocto vs QLI) are mandatory for major platform updates.

## 4. AI Agent Workflow

When processing a user request in this repository, follow these strict steps:

### Phase 1: Planning & Context Gathering
1. **Understand the Request**: Identify if this is a new application tutorial, a core launcher bug fix, or a documentation/benchmark update.
2. **Review Existing Patterns**: Search through `mod/` or `tutorials/` to find similar implementations. Do not invent a new structural pattern if one already exists.
3. **Assess Impact**: Check if the requested change impacts offline mode workflows or specific BSP versions.

### Phase 2: Implementation (Iterative)
1. Write/Modify the code or markdown incrementally. Ensure syntax correctness.
2. If updating `mod/`, heavily consider how it might break `launcher.py` and existing applications.
3. For documentation updates, painstakingly verify that relative paths to images and other markdowns are mathematically correct relative to the file location.

### Phase 3: Verification & Polish
1. Check that the main `README.md` requires an update (e.g., adding a new tutorial to the Categories table).
2. Check if the `IQS.md` in `docs/` should be explicitly updated to reflect the new feature.
3. **Reflect & Distill**: Before finishing, ask: "Did I learn a new pattern or encounter a friction point that should be documented in `IQS.md`?" If yes, update this document immediately.
4. Review your changes against this `IQS.md` to ensure absolute compliance.

## 5. Continuous Evolution (Living Principles)

This document is not static. It survives through:
- **Refinement**: As the project grows (more hardware support, new SDKs), update the "Project Architecture" and "Technical Standards".
- **Resilience**: When a solution fails or a bug is found due to a missing guideline, add a preventative rule here.
- **Freshness**: Regularly audit `tutorials/` to ensure the categories in `README.md` and this manual remain accurate.

## 5. When Stuck or Blocked
- Stop after 3 failed logical attempts or if a hardware dependency blocks progress.
- Explain explicitly to the user what the error is and what approach failed.
- Ask the user for clarification or guidance on hardware/environment-specific issues (e.g., Jetson/Qualcomm quirks) that the AI cannot test directly.
