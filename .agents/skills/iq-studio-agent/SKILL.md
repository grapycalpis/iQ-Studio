---
name: iq-studio-agent
description: "Use for general iQ-Studio repository changes and routing: launcher changes, mod/ Python modules, shell scripts, tutorials, README updates, benchmarks, AVL docs, SDK docs, model-deploy workflows, offline package docs, and deciding which focused iQ-Studio skill to apply. Use iq-studio-literacy for prose standards and iq-studio-formatting for Markdown structure. Do not use for unrelated repositories."
---

# iQ-Studio Agent

## Overview

Use this skill for repeatable iQ-Studio repository work and skill routing. It points agents to the durable project entry guide and the focused literacy, formatting, and commit-log skills without duplicating their rules.

Expected output: a scoped code or documentation change, plus verification results that match the files touched.

## Workflow

1. Read `.agents/IQS.md` before making or reviewing changes.
2. Identify the task type: launcher/core Python, shell script, tutorial, benchmark, AVL, SDK, model-deploy, or general documentation.
3. Search existing files for the closest local pattern before adding a new structure or convention.
4. If changing documentation prose, use `iq-studio-literacy`.
5. If changing Markdown structure, links, images, notes, or code fences, use `iq-studio-formatting`.
6. If drafting or reviewing commit messages, use `iq-studio-commit-log`.
7. Keep implementation and documentation changes scoped to the request, and preserve offline workflows and existing launcher behavior unless the task explicitly changes them.

## Skill Boundaries

- Use this skill for repo context, architecture, workflow, and code/documentation impact analysis.
- Use `iq-studio-literacy` for naming, capitalization, grammar, status wording, punctuation, and prose polish.
- Use `iq-studio-formatting` for headings, image paths, notes, links, code fences, and audit-tool compliance.
- Use `iq-studio-commit-log` for commit message style, staged-scope checks, and commit-splitting guidance.

## Gotchas

- Do not add scripts, references, assets, or optional metadata unless they materially improve repeatability.
- Do not duplicate the focused literacy or formatting rules in this skill.
- Do not change offline workflows, launcher behavior, or documentation categories as a side effect of unrelated edits.

## Verification

- Prefer the repository tools when documentation is touched:
  - `python3 tools/audit_content.py`
  - `python3 tools/get_headings.py`
- For launcher or module changes, run focused checks or tests that exercise the changed path when available.
- Before finishing, consider whether a new reusable pattern or friction point belongs in `.agents/IQS.md` or one of the focused skills.
