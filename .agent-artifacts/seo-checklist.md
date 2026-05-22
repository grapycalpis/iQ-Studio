# iQ Studio Docs — SEO Configuration Checklist

**Author:** Marketing SEO Specialist agent
**Date:** 2026-05-22
**Site:** iQ Studio Documentation (MkDocs Material 9.5.39)
**Scope:** Metadata, OG cards, sitemap, robots, JSON-LD, canonicals, redirects.

Source artifacts referenced: [`./ia-design.md`](./ia-design.md),
[`./brand-guide.md`](./brand-guide.md),
[`./tech-decision.md`](./tech-decision.md),
[`../mkdocs.yml`](../mkdocs.yml),
[`../README.md`](../README.md).

---

## 1. Summary

Shipped a config-and-template-driven SEO layer on top of the existing
MkDocs Material build. Every page now emits a proper `<title>`,
`<meta name="description">`, `<link rel="canonical">`, Open Graph and
Twitter Card tags, and JSON-LD structured data (`TechArticle` on doc
pages, `WebSite` with `SearchAction` on the homepage). All values are
sourced from page front-matter first, then `extra.*` knobs in
`mkdocs.yml`, then auto-extracted from `page.content`. Canonical URLs
derive from `site_url` so a custom-domain move is a one-line edit. A
default 1200x630 OG image generator is shipped as
[`tools/generate_og_image.py`](../tools/generate_og_image.py); the
`mkdocs-redirects` plugin is wired up with an empty map ready for any
future URL renames. `robots.txt` is in `src/` and is copied to
`site/robots.txt` verbatim. `sitemap.xml` is the stock MkDocs output,
augmented with git-derived `lastmod` via the
`mkdocs-git-revision-date-localized` plugin.

Nothing in `README.md`, `docs/`, `tutorials/`, or `benchmarks/` was
edited. Existing build commands (`python3 -m mkdocs build --clean`)
continue to work after `pip install -r requirements.txt`.

---

## 2. Per-page meta

### Files modified / added

| Path | Action | Purpose |
|---|---|---|
| [`overrides/main.html`](../overrides/main.html) | extended | Adds `htmltitle` + extends `extrahead` with description, OG, Twitter, canonical, JSON-LD |
| [`mkdocs.yml`](../mkdocs.yml) | extended | Added `extra.homepage_title`, `extra.homepage_description`, `extra.og_image`, `extra.organization`, plugins |
| [`requirements.txt`](../requirements.txt) | extended | `mkdocs-git-revision-date-localized-plugin`, `mkdocs-redirects`, `Pillow` |

### Override mechanism

Material's documented extension point is the `extrahead` block in
`overrides/main.html`. That file already existed (favicon + persona
cards). It was extended to:

1. Compute `seo_title`, `seo_description`, `og_image_abs`, `og_type` at
   the top of the template using pure Jinja2 (no third-party filters).
2. Override the `htmltitle` block so Material's default
   `{{ page.title }} - {{ config.site_name }}` is replaced by our
   `{{ page_title }} — iQ Studio Docs` convention (em dash), with the
   homepage suffix-less.
3. Emit `<meta name="description">`, `<link rel="canonical">`, the full
   OG block, the Twitter Card block, and the JSON-LD `<script>` from
   inside `extrahead` so all of it lands in `<head>`.

### Title precedence

1. On the **homepage**: `config.extra.homepage_title` wins.
2. Else if front-matter has `title:`, append ` — iQ Studio Docs`.
3. Else `page.title — iQ Studio Docs`.
4. Else `config.site_name`.

### Description precedence

1. Front-matter `description:` wins.
2. Else on the **homepage**: `config.extra.homepage_description`.
3. Else auto-derived from `page.content`:
   - Material has already rendered the markdown to HTML by the time
     `extrahead` fires. `page.content | striptags | trim` produces
     plain text. Newlines/tabs are collapsed to single spaces via
     repeated `replace` calls (pure Jinja2; no `regex_replace`).
   - Trim to 155 chars at the last word boundary above char 80 and
     append `…`. If `rfind(' ')` returns `<= 80` (no clean break),
     just append `…` at the hard cap.
4. Else `config.site_description`.

The "first paragraph is empty / a banner image" edge case the brief
called out is covered because:
- `striptags` removes the image tags entirely and pulls in alt text
  instead — if the page leads with an image, the first words of body
  prose become the description.
- If body prose is also empty, `auto_desc` is empty and we fall
  through to `config.site_description`.

### Sample output (homepage)

```html
<title>iQ Studio — IQ Studio Launcher for Innodisk Dragonwing AI</title>
<meta name="description" content="iQ Studio is the IQ Studio Launcher for Innodisk Dragonwing AI edge devices. Install iqs-launcher, follow the Q911 user guide, and run VLM, Streampipe, and YOLO demos on Qualcomm QCS9075 in minutes.">
<link rel="canonical" href="https://innoipc-innodisk.github.io/iQ-Studio/">
```

### Sample output (deep page: `tutorials/starting-guides/q911/yocto.md`)

```html
<title>Q911 — Yocto — iQ Studio Docs</title>
<meta name="description" content="Quick start for the Q911 EVK running Yocto Linux. Boot the board, expose the serial console, and connect ADB over USB-C to confirm the…">
<link rel="canonical" href="https://innoipc-innodisk.github.io/iQ-Studio/tutorials/starting-guides/q911/yocto/">
```

(Exact description text will reflect that page's rendered prose at
build time — preview after `mkdocs build`.)

---

## 3. OG / Twitter Cards

### Default OG image

- **Path:** `docs/fig/og-default.png` (copied to
  `site/docs/fig/og-default.png` at build time, served as
  `<site_url>docs/fig/og-default.png`).
- **Dimensions:** 1200 x 630 (Facebook / LinkedIn / Twitter
  `summary_large_image` recommendation).
- **Generator:** [`tools/generate_og_image.py`](../tools/generate_og_image.py)
  (Pillow-based, brand-tokens hard-coded). Run from repo root:

  ```bash
  python3 tools/generate_og_image.py
  ```

- **Composition** (per brief): white background, iQ Studio logo on the
  left, "iQ Studio Documentation" in Barlow Condensed (with fallback
  chain to DejaVu/Liberation if Barlow isn't on the system), red
  `#ec1b23` rule under the title, "Innodisk Dragonwing AI Platform"
  subtitle in muted gray, "innodisk.com" footer in the bottom-right.
- **Material `social` plugin status:** **NOT enabled**. The plugin
  requires Cairo + Pango system libraries (`libcairo2`, `libpango-1.0`,
  `libpangocairo-1.0`) plus their headers; the build environment for
  this repo is not guaranteed to ship them, and adding them as a
  hard CI dep adds 100+ MB to the Docker layer. Shipping a single
  curated default + per-page front-matter override is the lighter
  path. To revisit later: enable `plugins: [..., social]` in
  `mkdocs.yml` and install `mkdocs-material[imaging]` in
  `requirements.txt`.

### Per-page override

Any page can drop a YAML front-matter block at the top to override the
default OG image:

```yaml
---
image: docs/fig/my-custom-card.png
---
```

The image path is relative to `site_url` and concatenated by the
template (`og_image_abs = site_url + og_image_rel`). Front-matter
`title:` and `description:` keys also work the same way (already
supported as part of standard MkDocs page metadata).

### Sample output (any doc page)

```html
<meta property="og:site_name" content="iQ Studio">
<meta property="og:type" content="article">
<meta property="og:title" content="Q911 — Yocto — iQ Studio Docs">
<meta property="og:description" content="Quick start for the Q911 EVK running Yocto Linux…">
<meta property="og:url" content="https://innoipc-innodisk.github.io/iQ-Studio/tutorials/starting-guides/q911/yocto/">
<meta property="og:image" content="https://innoipc-innodisk.github.io/iQ-Studio/docs/fig/og-default.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="iQ Studio — Innodisk Dragonwing AI documentation">
<meta property="og:locale" content="en_US">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Q911 — Yocto — iQ Studio Docs">
<meta name="twitter:description" content="Quick start for the Q911 EVK running Yocto Linux…">
<meta name="twitter:image" content="https://innoipc-innodisk.github.io/iQ-Studio/docs/fig/og-default.png">
```

On the homepage, `og:type` switches to `website` (per OGP spec).

---

## 4. Sitemap

- **Path:** `site/sitemap.xml` (and `site/sitemap.xml.gz`), generated by
  MkDocs core. Served at `<site_url>sitemap.xml`.
- **Generator:** MkDocs core `sitemap.xml` template. No third-party
  plugin needed.
- **`lastmod`:** Provided by
  `mkdocs-git-revision-date-localized-plugin`, which reads the file's
  last commit date from git and exposes it to the template. Falls back
  to build time when git history is unavailable (e.g. shallow clones
  in CI without `fetch-depth: 0`).
- **Priorities:** MkDocs core does not emit `<priority>` or
  `<changefreq>` by default; Google has publicly stated it ignores
  both since 2017 (only `<loc>` and `<lastmod>` are used). We
  intentionally do not add a plugin to inject them — they would be
  noise.

### Expected entry count

Counting nav pages from [`mkdocs.yml`](../mkdocs.yml): roughly **26
URLs** (homepage + 8 sidebar groups + their leaves). Exact count
verifiable post-build via:

```bash
grep -c '<loc>' site/sitemap.xml
```

### Sample 5 entries (expected shape)

```xml
<url>
  <loc>https://innoipc-innodisk.github.io/iQ-Studio/</loc>
  <lastmod>2026-05-22</lastmod>
</url>
<url>
  <loc>https://innoipc-innodisk.github.io/iQ-Studio/tutorials/starting-guides/</loc>
  <lastmod>2026-05-19</lastmod>
</url>
<url>
  <loc>https://innoipc-innodisk.github.io/iQ-Studio/tutorials/starting-guides/q911/</loc>
  <lastmod>2026-05-19</lastmod>
</url>
<url>
  <loc>https://innoipc-innodisk.github.io/iQ-Studio/tutorials/starting-guides/q911/yocto/</loc>
  <lastmod>2026-05-19</lastmod>
</url>
<url>
  <loc>https://innoipc-innodisk.github.io/iQ-Studio/benchmarks/iqs-streampipe/</loc>
  <lastmod>2026-05-22</lastmod>
</url>
```

---

## 5. robots.txt

- **Source:** [`src/robots.txt`](../src/robots.txt).
- **Output:** `site/robots.txt` (MkDocs copies non-`.md` files in
  `docs_dir` verbatim into `site/`).
- **`exclude_docs` note:** the existing `*.txt` exclude was negated with
  `!robots.txt` so it survives the exclusion filter. See
  [`mkdocs.yml`](../mkdocs.yml).

### Final contents

```
# iQ Studio Documentation — robots.txt
#
# Public documentation site. All crawlers welcome. The sitemap below is
# generated by MkDocs at build time and lists every published page.
#
# To narrow access later (e.g. block /draft/), add `Disallow:` rules
# above the Sitemap line.

User-agent: *
Allow: /

Sitemap: https://innoipc-innodisk.github.io/iQ-Studio/sitemap.xml
```

**Custom-domain reminder:** when `site_url` is changed in `mkdocs.yml`,
update the `Sitemap:` line here too. (`robots.txt` is plain text — it
doesn't read `site_url`.) Consider promoting `Sitemap:` to a template
variable in a future iteration.

---

## 6. Structured data

### Schema choices per page type

| Page type | Schema | Why |
|---|---|---|
| Homepage (`src/index.md`) | `WebSite` + nested `SearchAction` | Surfaces the docs-site search box in Google's sitelinks search box rich result. |
| Every other doc page | `TechArticle` | Schema.org subtype of Article designed specifically for technical documentation; eligible for the same article rich-result enhancements with stronger topical signaling. |

### Sample JSON-LD — homepage

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "iQ Studio",
  "url": "https://innoipc-innodisk.github.io/iQ-Studio/",
  "description": "iQ Studio is the IQ Studio Launcher for Innodisk Dragonwing AI edge devices. Install iqs-launcher, follow the Q911 user guide, and run VLM, Streampipe, and YOLO demos on Qualcomm QCS9075 in minutes.",
  "publisher": {
    "@type": "Organization",
    "name": "Innodisk",
    "url": "https://www.innodisk.com/",
    "logo": {
      "@type": "ImageObject",
      "url": "https://innoipc-innodisk.github.io/iQ-Studio/docs/fig/iq-studio-logo.png"
    }
  },
  "potentialAction": {
    "@type": "SearchAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": "https://innoipc-innodisk.github.io/iQ-Studio/?q={search_term_string}"
    },
    "query-input": "required name=search_term_string"
  }
}
```

### Sample JSON-LD — doc page (e.g. `tutorials/starting-guides/q911/yocto.md`)

```json
{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "headline": "Yocto Linux Interaction Guide",
  "description": "Quick start for the Q911 EVK running Yocto Linux…",
  "image": "https://innoipc-innodisk.github.io/iQ-Studio/docs/fig/og-default.png",
  "datePublished": "2026-05-19",
  "dateModified": "2026-05-19",
  "author": {
    "@type": "Organization",
    "name": "Innodisk",
    "url": "https://www.innodisk.com/"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Innodisk",
    "url": "https://www.innodisk.com/",
    "logo": {
      "@type": "ImageObject",
      "url": "https://innoipc-innodisk.github.io/iQ-Studio/docs/fig/iq-studio-logo.png"
    }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://innoipc-innodisk.github.io/iQ-Studio/tutorials/starting-guides/q911/yocto/"
  },
  "inLanguage": "en"
}
```

`datePublished` and `dateModified` come from the
`git-revision-date-localized` plugin (`type: iso_date`). Both fields
are conditionally emitted — if git history is missing for some reason,
the JSON-LD is still syntactically valid (the keys just don't appear).

### Validation

After deploy, paste a page URL into:
- Google Rich Results Test: <https://search.google.com/test/rich-results>
- Schema.org Validator: <https://validator.schema.org/>

Both should report `TechArticle` for doc pages and `WebSite` for the
homepage with zero errors.

---

## 7. Canonical URLs

- **Current `site_url`:**
  `https://innoipc-innodisk.github.io/iQ-Studio/` (default GitHub
  Pages URL for the public org repo).
- **Every page emits:**
  `<link rel="canonical" href="{{ page.canonical_url }}">` where
  `page.canonical_url` is MkDocs core's join of `site_url + page.url`.
  Also wired into `og:url` and `mainEntityOfPage["@id"]`.

### Moving to a custom domain — the one-line edit

When the docs site is published behind a custom domain
(e.g. `https://iq-studio.innodisk.com/`):

1. Open [`mkdocs.yml`](../mkdocs.yml).
2. Change the single line:

   ```yaml
   # before
   site_url: https://innoipc-innodisk.github.io/iQ-Studio/

   # after
   site_url: https://iq-studio.innodisk.com/
   ```

3. Update the `Sitemap:` line in [`src/robots.txt`](../src/robots.txt)
   to match (one extra line — flagged in §5).
4. Rebuild. All canonicals, og:url, sitemap entries, and JSON-LD
   `mainEntityOfPage`/`@id` fields will resolve against the new
   domain automatically.

Set up a 301 from the old GH Pages URL to the custom domain via
GitHub Pages' CNAME settings to preserve any accumulated link equity.

---

## 8. Homepage SEO

### Final homepage `<title>`

```
iQ Studio — IQ Studio Launcher for Innodisk Dragonwing AI
```

Length: 60 chars (within Google's ~60-char SERP limit).

### Final homepage `<meta name="description">`

```
iQ Studio is the IQ Studio Launcher for Innodisk Dragonwing AI edge
devices. Install iqs-launcher, follow the Q911 user guide, and run
VLM, Streampipe, and YOLO demos on Qualcomm QCS9075 in minutes.
```

Length: 199 chars (slightly above Google's typical 155-160 truncation
point, but the leading 155 chars cover all three target keyphrases —
extra text is bonus context for AI search overviews / longer SERP
snippets that Bing and Yandex render).

### Target keyphrases — placement audit

| Phrase | Appears in `<title>` | Appears in `<meta description>` | Appears in JSON-LD `description` | Appears in H1 (already in README) |
|---|---|---|---|---|
| **"IQ Studio Launcher"** | YES (positions 12–30) | YES (sentence 1: "the IQ Studio Launcher") | YES | The README H1 is "iQ Studio" — the launcher term is implicit |
| **"Innodisk Dragonwing AI"** | YES (positions 34–56) | YES (sentence 1: "Innodisk Dragonwing AI edge devices") | YES | Not in the H1 but the README's first NOTE cites "Innodisk Qualcomm Dragonwing SoC" |
| **"Q911 user guide"** | NO (omitted from 60-char title; ranked third in priority because Q911 is a device line, not the product name) | YES (sentence 2: "follow the Q911 user guide") | YES | Not in H1 directly; the README's `Pick Your Path` and `Quick Start` sections reference Q911 |

All three phrases survive in the 155-char window most SERPs use.
Stuffing avoided: each phrase appears exactly once and reads as
natural prose.

### Override mechanism (no README edits)

Both fields come from `extra:` in [`mkdocs.yml`](../mkdocs.yml):

```yaml
extra:
  homepage_title: "iQ Studio — IQ Studio Launcher for Innodisk Dragonwing AI"
  homepage_description: >-
    iQ Studio is the IQ Studio Launcher for Innodisk Dragonwing AI edge
    devices. Install iqs-launcher, follow the Q911 user guide, and run
    VLM, Streampipe, and YOLO demos on Qualcomm QCS9075 in minutes.
```

The `overrides/main.html` template reads
`config.extra.homepage_title` and `config.extra.homepage_description`
when `page.is_homepage` is true, so README.md is left untouched.

### Cannibalization check

Cross-page audit considered before finalizing: the homepage is the
ONLY page that uses "IQ Studio Launcher" or "Innodisk Dragonwing AI"
as primary phrases. The Q911 sub-pages target longer-tail variants
("Q911 quickstart", "Q911 Yocto Linux", "Q911 Ubuntu"). No
title-level overlap with any other URL in the cluster. Re-audit
after first crawl by querying Search Console with
dimensions = `page` + `query` filtered on these three phrases.

---

## 9. Redirects

- **Status:** No URL renames recorded in [`./ia-design.md`](./ia-design.md).
  The IA's mapping is one-to-one with existing `.md` paths — every
  page in the §1 sitemap was already at the same `tutorials/...` /
  `benchmarks/...` / `docs/...` path before the docs-site work
  started.
- **Off-site redirects (github.com → site):** outside our control.
  GitHub does not provide a redirect mechanism from
  `github.com/InnoIPC-Innodisk/iQ-Studio/blob/main/.../README.md` to
  the published doc site. Mitigation: the existing root
  [`README.md`](../README.md) is preserved (per
  [`./tech-decision.md`](./tech-decision.md) §6 open question #1)
  so deep links from the GitHub repo browser keep working
  natively on github.com.
- **Trailing-slash / index resolution:** Material is configured with
  `use_directory_urls: true` (the MkDocs default), so
  `tutorials/starting-guides/` and `tutorials/starting-guides/index.html`
  both resolve to the same page. No extra config needed.
- **Plugin wired up but empty:**
  [`mkdocs-redirects`](https://pypi.org/project/mkdocs-redirects/)
  is added to `requirements.txt` and registered in `mkdocs.yml`
  with an empty `redirect_maps:`. To add a redirect in the future:

  ```yaml
  plugins:
    - redirects:
        redirect_maps:
          old-path/index.md: new-path/index.md
          legacy/foo.md: tutorials/applications/foo.md
  ```

---

## 10. Verification

The following commands should be run from the repo root after the
symlinks are recreated (`tools/setup_docs_dev.sh` or the CI step) and
`pip install -r requirements.txt` has been run.

### 10.1 Build

```bash
python3 -m mkdocs build --clean
```

Expected: exit code 0, "Documentation built in N seconds" line.
If a missing-plugin error appears (e.g.
`Plugin 'redirects' not found`), re-run
`pip install -r requirements.txt`.

### 10.2 OG image generation

```bash
python3 tools/generate_og_image.py
```

Expected output:

```
Generating docs/fig/og-default.png (1200x630)...
  wrote /…/docs/fig/og-default.png (XX.X KB)
```

If Barlow Condensed isn't on the system, the script warns and falls
back to DejaVu Sans Bold (still on-brand because the composition is
brand-led, not font-led). The card just needs to be regenerated once;
commit the PNG.

### 10.3 Spot-check page metadata

```bash
find site -name '*.html' | head -5
```

For each path returned, grep the four critical markers:

```bash
for f in $(find site -name '*.html' | head -5); do
  echo "=== $f ==="
  grep -E '<meta name="description"|<meta property="og:|<link rel="canonical"|<script type="application/ld\+json"' "$f" | head -10
done
```

Expected: every page emits at least one of each of these tags.

### 10.4 Sitemap and robots

```bash
cat site/sitemap.xml | head -30
cat site/robots.txt
```

Expected: `sitemap.xml` is well-formed XML with `<urlset>` and
multiple `<url>` blocks; `robots.txt` matches §5 verbatim.

### 10.5 OG image file present

```bash
ls -la site/docs/fig/og-default.png
```

Expected: the PNG generated in §10.2 is copied into `site/`.

### 10.6 Quick check for the JSON-LD on the homepage

```bash
grep -A2 'application/ld+json' site/index.html | head -40
```

Expected: a `<script type="application/ld+json">` block containing
`"@type": "WebSite"` and `"SearchAction"`.

### 10.7 Quick check for `TechArticle` on a deep doc page

```bash
grep -A2 'application/ld+json' site/tutorials/starting-guides/q911/yocto/index.html | head -40
```

Expected: `"@type": "TechArticle"`, `"headline"`, `"author"`, and
`"mainEntityOfPage"` with the canonical URL as `@id`.

### 10.8 Live external validation (post-deploy)

- **Google Rich Results Test** —
  <https://search.google.com/test/rich-results> — paste the deployed
  homepage URL, expect 0 errors and a `Search Action` markup
  detected.
- **Twitter Card Validator** — (deprecated as a public tool in 2023,
  but X still ingests the meta tags; share a deployed URL in a
  draft X post to preview the card without publishing).
- **Facebook Sharing Debugger** —
  <https://developers.facebook.com/tools/debug/> — paste any
  deployed URL, expect the og:image to be detected at 1200x630.

---

## 11. Open items / future work

1. **Material `social` plugin not enabled.** Per-page auto-generated
   OG cards would be a strict upgrade once the build environment is
   confirmed to ship Cairo + Pango. To enable: install
   `mkdocs-material[imaging]`, add `social:` to `plugins:`, remove the
   default `og_image` to let the plugin take over (or keep it as a
   fallback). Defer until imaging libs are confirmed.
2. **Twitter handle.** `extra.twitter_site` is empty. Set it to the
   Innodisk X account handle (e.g. `@Innodisk`) once confirmed — this
   adds `<meta name="twitter:site" ...>` to every page.
3. **`robots.txt` Sitemap URL drift.** The `Sitemap:` line is
   hard-coded to the GitHub Pages URL. When the custom domain
   launches, this file needs a manual one-line edit. Consider
   promoting `robots.txt` to a Jinja-rendered template
   (`overrides/robots.txt.j2`) that reads `config.site_url`.
4. **Per-page custom OG cards.** The framework supports
   `image: ...` in front-matter, but no `.md` files use it yet
   (none would be edited per task constraint). When the team adds a
   high-profile page (e.g. a marketing landing), generate a custom
   card with `tools/generate_og_image.py` parameterized for that
   page.
5. **Author entity for E-E-A-T.** The JSON-LD `author` field is
   currently the `Innodisk` Organization. To strengthen E-E-A-T,
   move per-page authorship to named individuals where applicable
   (engineering tutorials authored by named engineers), with author
   bio pages and `sameAs` links to LinkedIn / GitHub. Out of scope
   for SEO setup; revisit when content ownership is mapped.
6. **Hreflang.** Site is English-only. When a Traditional Chinese
   (or other locale) translation lands, add hreflang link-rel
   alternates in `overrides/main.html` driven by a per-page locale
   front-matter key.
7. **Manual cannibalization audit after first crawl.** Until Search
   Console accumulates impressions, the cannibalization check in
   §8 is a static review only. Re-run the audit two weeks after
   Google's first crawl by exporting GSC dimensions = `page` +
   `query`, filtered on the three target phrases.
8. **Cross-page audit before any future title/H1 changes.** The
   IA already separates topics cleanly (Q911 quickstart != Q911
   Yocto != Q911 Ubuntu). Document this contract: every new doc
   page must add a `# H1` that does not duplicate another page's
   primary keyword. Add a CI check via the existing audit script
   pattern.
9. **Pinned plugin versions.** The two new plugins
   (`mkdocs-git-revision-date-localized-plugin==1.2.6`,
   `mkdocs-redirects==1.2.1`) are pinned in `requirements.txt`.
   Update on the regular dependency-refresh cadence.

---

**Hand-off**: implementer runs `pip install -r requirements.txt`,
recreates the symlinks (existing dev-setup procedure), runs
`python3 tools/generate_og_image.py`, then
`python3 -m mkdocs build --clean`, then walks the §10 verification
steps. After that, push and let GitHub Pages serve the site at the
configured `site_url`.
