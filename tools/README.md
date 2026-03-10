# iQ-Studio Contributor Tools

This directory contains automation scripts designed to maintain the high quality and consistency of the iQ-Studio documentation. Contributors are encouraged to use these tools to ensure compliance with the [IQS_FORMATTING.md](../IQS_FORMATTING.md) standards before submitting a Pull Request.

---

## 1. Included Files

| File | Purpose | Action Type |
| :--- | :--- | :--- |
| **`audit_content.py`** | Validates document compliance (images, quotes, links, tags). | **Analysis/Audit** |
| **`fix_bash_tags.py`** | Automatically fixes missing language tags in code blocks. | **Modification** |
| **`get_headings.py`** | Extracts and displays the heading hierarchy of all Markdown files. | **Overview/Navigation** |

---

## 2. Usage

These scripts are written in Python and should be executed from the project root or the `tools/` directory.

### Audit Your Content
Use this to check for formatting errors across the project.
```bash
python tools/audit_content.py
```

### Auto-Fix Code Blocks
Use this to automatically append `bash` or `python` tags to empty code blocks.
```bash
python tools/fix_bash_tags.py
```

### View Project Hierarchy
Use this to get a quick bird's-eye view of all document structures.
```bash
python tools/get_headings.py
```

---

## 3. Examples: Input & Output

### `audit_content.py`
*   **Input**: Scans all `.md` files for image pathing, note syntax, and link types.
*   **Output**: A checklist of compliance issues or a success message.
    *   **Success Output**: `No issues found! Perfect compliance.`
    *   **Failure Output**:
        ```text
        ### tutorials/starting-guides/README.md
        - [ ] Image not in fig/ or img/ directory: ./logo.png
        - [ ] Line 42: Note/Warning not properly quoted (missing '>').
        ```

### `fix_bash_tags.py`
*   **Input**: Markdown files with untagged code blocks (e.g., ` ``` ` followed immediately by a command).
*   **Output**: **In-place modification** of the files.
    *   **Example Input**:
        ```markdown
        ```
        $ git clone ...
        ```
        ```
    *   **Example Output**:
        ```markdown
        ```bash
        $ git clone ...
        ```
        ```

### `get_headings.py`
*   **Input**: All Markdown files in the repository.
*   **Output**: A tree-like structure of headings printed to the terminal.
    *   **Example Output**:
        ```text
        FILE: README.md
          # iQ Studio
          ## Core Software Stack & Architecture
          ## How to Deploy
        ```

---
> Note: These tools are strictly for documentation quality control and do not impact the core application logic.
