# iQ-Studio Docs Deployment Runbook

## Overview

The `Deploy Docs` workflow (`.github/workflows/deploy-docs.yml`) builds the
MkDocs Material site from this repository and publishes it to GitHub Pages on
every push to `main` that touches docs-affecting paths, and on manual
`workflow_dispatch`. It does not touch application code (`launcher.py`,
`iqs-launcher.sh`, `install.sh`, `mod/`, `binaries/`, `src/*.py`) and does not
run any tests against them. Deployment uses the modern GitHub Pages Actions
artifact pattern (`actions/upload-pages-artifact` + `actions/deploy-pages`) —
there is no `gh-pages` branch, each deploy is an immutable artifact, and
concurrency is governed by the `pages` group.

## Enabling Pages in repo settings

One-time setup, performed by a repo admin:

1. Open the repository on GitHub: `InnoIPC-Innodisk/iQ-Studio`.
2. Go to `Settings` -> `Pages`.
3. Under `Build and deployment` -> `Source`, select `GitHub Actions`.
4. No branch needs to be selected under this model. There is no `gh-pages`
   branch to configure.
5. Save. The site is provisioned by the first successful run of the
   `Deploy Docs` workflow, not by toggling this setting. Either push a
   docs-touching commit to `main` or trigger `workflow_dispatch` from the
   `Actions` tab to bootstrap the site.

The published URL after first deploy will be:
`https://innoipc-innodisk.github.io/iQ-Studio/`

## README additions

Paste the following into `README.md`. The runbook does not modify `README.md`
itself; this is the canonical text to copy.

Build status badge (place near the top of the file):

```markdown
[![Docs](https://github.com/InnoIPC-Innodisk/iQ-Studio/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/InnoIPC-Innodisk/iQ-Studio/actions/workflows/deploy-docs.yml)
```

Documentation section (anywhere appropriate in the README):

```markdown
## Documentation

Full documentation is published at
<https://innoipc-innodisk.github.io/iQ-Studio/>.

The site is built from `mkdocs.yml` and deployed automatically by the
`Deploy Docs` GitHub Actions workflow on every push to `main` that touches
`docs/`, `tutorials/`, `benchmarks/`, `README.md`, `mkdocs.yml`,
`requirements.txt`, or `overrides/`. To enable or re-enable Pages on a
fresh fork, see `.agent-artifacts/deploy-runbook.md`.
```

## Custom domain (CNAME) - optional

To serve the docs at a custom domain such as `iqs.innodisk.com`:

### 1. Make GitHub Pages publish the CNAME file

The site is built from `docs_dir: src`, but `src/` is a symlink-staging
directory (most of its contents are gitignored symlinks recreated at build
time). Committing a `CNAME` file directly into `src/` would either be
overwritten by build-time symlinking logic or look out of place alongside the
generated symlinks.

The simplest and most robust approach is:

1. Commit a plain-text file at `docs/CNAME` containing only the hostname
   (no `http://`, no trailing slash, no newline shenanigans). Example:

   ```text
   iqs.innodisk.com
   ```

2. Add a build-time copy step in `.github/workflows/deploy-docs.yml`,
   immediately after `mkdocs build --strict`, so the file lands at the root
   of the published site:

   ```yaml
   - name: Copy CNAME into built site
     run: cp docs/CNAME site/CNAME
   ```

   This is preferred over symlinking `docs/CNAME` into `src/` because it
   keeps the CNAME outside the MkDocs nav/index machinery entirely and never
   shows up as a page.

### 2. DNS records at the registrar

| Domain type | Record type | Name | Value                                         |
|-------------|-------------|------|-----------------------------------------------|
| Subdomain   | CNAME       | iqs  | `innoipc-innodisk.github.io.`                 |
| Apex        | A           | @    | `185.199.108.153`                             |
| Apex        | A           | @    | `185.199.109.153`                             |
| Apex        | A           | @    | `185.199.110.153`                             |
| Apex        | A           | @    | `185.199.111.153`                             |

Use CNAME for a subdomain (recommended). Use the four `A` records only if
serving from an apex domain.

### 3. Configure GitHub and MkDocs

1. After DNS has propagated, go to `Settings` -> `Pages` -> `Custom domain`,
   enter `iqs.innodisk.com`, and save. Wait for the DNS check to pass.
2. Tick `Enforce HTTPS` once the GitHub-issued certificate is provisioned
   (this can take a few minutes after the DNS check succeeds).
3. Update `site_url` in `mkdocs.yml` (the comment at line 19 already flags
   this) to the new domain so canonical URLs, sitemap, and OG tags are
   correct:

   ```yaml
   site_url: https://iqs.innodisk.com/
   ```

## Rollback procedure

Each Pages Actions deploy is an immutable artifact, so rollback never
requires touching a `gh-pages` branch. In order of preference:

1. **Re-run a known-good deployment** (fastest, no git changes):
   `Actions` tab -> `Deploy Docs` workflow -> select the last green run ->
   `Re-run all jobs`. The previous artifact is rebuilt from the same commit
   and re-uploaded.

2. **Revert the offending commit** (clean rebuild from a known state):

   ```bash
   git revert <bad-sha>
   git push origin main
   ```

   This triggers a fresh build on the reverted tree.

3. **Manual dispatch from a tag or branch** (deploy any historical commit
   without modifying `main`):
   `Actions` tab -> `Deploy Docs` -> `Run workflow` -> pick the ref (tag,
   commit SHA via branch, or branch name) -> `Run workflow`. Useful for
   ad-hoc rebuilds or hotfix branches.

Under the Pages Actions model, none of these options require modifying or
force-pushing any branch.

## Path filter coordination

The workflow only fires when docs-relevant paths change. Application-code
changes do not run the docs build, and vice versa. Future app-code CI should
mirror this discipline with its own `paths:` filter that excludes the docs
paths to avoid double-running on mixed commits.

| Path                                        | Triggers Deploy Docs | Triggers app CI (future) |
|---------------------------------------------|----------------------|--------------------------|
| `README.md`                                 | yes                  | no                       |
| `docs/**`                                   | yes                  | no                       |
| `tutorials/**`                              | yes                  | no                       |
| `benchmarks/**`                             | yes                  | no                       |
| `tools/README.md`                           | yes                  | no                       |
| `mkdocs.yml`                                | yes                  | no                       |
| `requirements.txt`                          | yes                  | no                       |
| `overrides/**`                              | yes                  | no                       |
| `.github/workflows/deploy-docs.yml`         | yes                  | no                       |
| `launcher.py`                               | no                   | yes                      |
| `iqs-launcher.sh`                           | no                   | yes                      |
| `install.sh`                                | no                   | yes                      |
| `mod/**`                                    | no                   | yes                      |
| `binaries/**`                               | no                   | yes                      |
| `src/*.py` (and Python package under `src/`)| no                   | yes                      |

## Local preview

Install dependencies and recreate the four gitignored symlinks before
serving or building locally:

```bash
pip install -r requirements.txt

ln -sfn ../README.md   src/index.md
ln -sfn ../docs        src/docs
ln -sfn ../tutorials   src/tutorials
ln -sfn ../benchmarks  src/benchmarks

mkdocs serve
```

CI runs `mkdocs build --strict`. Run the same locally before pushing to
catch broken links or nav misconfigurations that would otherwise fail the
deploy:

```bash
mkdocs build --strict
```

## Troubleshooting

| Symptom                                                | Likely cause / fix                                                                                                                  |
|--------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| Plugin `git-revision-date-localized` errors in CI      | Checkout must use `fetch-depth: 0`. The workflow already does this; verify it was not removed.                                       |
| `src/index.md` (or docs/tutorials/benchmarks) missing  | The symlink-recreate step did not run, or `.gitignore` is hiding them locally. Re-run the `ln -sfn` block above.                     |
| 404 on a page that clearly exists                      | `use_directory_urls: true` rewrites `foo.md` to `foo/`. Update internal links to the directory form, not the `.md` form.             |
| Deploy succeeded but site shows stale content          | GitHub Pages CDN cache. Wait roughly 60 seconds and hard-reload (Ctrl-Shift-R / Cmd-Shift-R). If still stale after a few minutes, re-run the workflow. |
| `mkdocs build --strict` fails on broken link warning   | Fix the link or remove the page from `nav`. Do not relax `--strict` in CI - it is the only line of defence against silent rot.       |
| First deploy never publishes                           | Confirm `Settings -> Pages -> Source = GitHub Actions`. The setting must be saved before the first workflow run will provision the site. |
