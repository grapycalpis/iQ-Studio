<!--
 Copyright (c) 2025 Innodisk Corp.
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->
# iQ-Studio Content Formatting Standards

This document is an extension of `IQS.md`, focusing on specific formatting details for Markdown content. It aims to ensure high consistency in structure, aesthetics, and indexability across all documentation.

## 1. Visual Resources (Visuals)

- **Storage Path**: All images (PNG/JPG) and GIFs must be stored in a `fig/` or `img/` directory at the same level as the corresponding README.
- **Syntax Requirements**:
  - Standard Markdown: `![alt text](./fig/image.png)`
  - HTML Centering: `<div align="center"><img src="./fig/image.png" width="80%"></div>`
- **Strict Prohibition**: Do not store images in the root or tutorial parent directories; keep the directory tree clean.

## 2. Heading Strategy (Headings)

Based on the **"Contextual Wording Strategy"**:

- **Presentation Layer (Strict)**: Root `README.md` and `tutorials/applications/` must strictly align with `## How to Deploy` and `## How to Use`.
- **Developer Layer (Contextual)**: `sdks/`, `avl/`, and `benchmarks/` are permitted to retain context-specific wording (e.g., `## Testing Method`).
- **Hierarchy Integrity**: Do not skip heading levels (e.g., jumping from `#` to `###`). Ensure a logical progression: `#` -> `##` -> `###`.

## 3. Code Blocks

- **Language Labels**: Every ` ``` ` must be followed by a language label to enable syntax highlighting.
  - Terminal commands: Use ` ```bash `.
  - Python code: Use ` ```python `.
  - JSON configuration: Use ` ```json `.
- **Command Format**: In `bash` blocks, use a `$` prefix to indicate user-input commands.

## 4. Warnings, Notes, and Tips (Quotes & Notes)

- **Quote Syntax**: All `Note:`, `Notice:`, and `Warning:` messages must start with a Markdown Quote (`>`).
  - **Correct**: `> Note: This config is not default.`
  - **Incorrect**: `Note: This config is not default.` (Rendering as a standard paragraph lacks visual emphasis.)
- **Tips**: Use emojis for better visual guidance: `> 💡 **Tip:** ...`

## 5. Resource Linking (Links)

- **Relative Paths Only**: Do not use `file:///`, absolute drive paths, or absolute website URLs for local project files.
  - **Correct**: `[Link](../../README.md)`
  - **Incorrect**: `[Link](D:/repo/README.md)`
- **File Links**: Use the file's basename as the link text to improve readability.

## 6. Document Quality Control (Audit Tools)

To maintain our high standards, we provide automated tools in the `tools/` directory. Contributors are encouraged to run these before submitting a PR:

- **`audit_content.py`**: Validates image paths, code block labels, quote syntax, and relative links.
  - **Execution**: `python tools/audit_content.py`
- **`fix_bash_tags.py`**: Automatically detects and fixes missing language tags in code blocks.
  - **Execution**: `python tools/fix_bash_tags.py`
- **`get_headings.py`**: Reviews and prints the document heading hierarchy for all Markdown files.
  - **Execution**: `python tools/get_headings.py`

---
*This is a living document and will be updated as the project evolves.*
