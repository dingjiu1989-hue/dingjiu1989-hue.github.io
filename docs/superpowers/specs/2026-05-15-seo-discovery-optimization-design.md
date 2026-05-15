# SEO Discovery Optimization — Design Spec

**Date:** 2026-05-15
**Status:** approved
**Scope:** Crawler/AI discovery optimization (Phase 1 of 2)

## Goal

Maximize content discoverability for search engines and AI crawlers across all 854 EN + 60 CN articles.

## Changes

### 1. llms.txt — Cover missing boards (gen_ai_friendly.py)

**Problem:** `gen_llms_txt()` and `gen_en_llms_txt()` hardcode 5 boards (tech, sidehustle, tools, ai, compare). Security, database, architecture boards (~300 articles) are invisible to AI crawlers that read llms.txt.

**Fix:** Replace hardcoded board list with dynamic iteration over `en_data["boards"]`. Add missing entries to `BOARD_NAMES_EN` dict.

### 2. llms-full.txt — Clean formatting (gen_ai_friendly.py)

**Problem:** Duplicate H1 headings and excessive blank lines in the generated Markdown (visible in sample: `# API Gateway Implementation Guide` appears 4+ times with blanks).

**Fix:** Strip leading `# Title` line from html2text output (already present in metadata header). Collapse consecutive blank lines.

### 3. Related articles — Server-side render (gen_en_site.py)

**Problem:** `make_article_html()` wraps `related_html` with `<div id="related-posts" style="display:none;">` — only visible after render.js executes. Non-JS crawlers (Bingbot, GPTBot, ClaudeBot) miss internal link graph entirely.

**Fix:** Render `related_html` directly in initial HTML. Remove `<noscript>` duplication and JS-dependent wrapper. Keep the `related-grid` class for styling.

### 4. Image sitemap — New (scripts/gen_image_sitemap.py)

**Problem:** No image sitemap exists. 854 cover images (1200x630 PNG) are discoverable only through page-level crawling. Google Images and multimodal AI models benefit from explicit image metadata.

**Fix:** New script generates `/images/sitemap.xml` referencing all cover images with `<image:image>`, `<image:loc>`, `<image:title>`, `<image:caption>` tags.

## Execution Order

```
gen_ai_friendly.py  →  gen_en_site.py (rebuild 854 pages)  →  gen_image_sitemap.py
```

## Files Modified

| File | Change |
|------|--------|
| `scripts/gen_ai_friendly.py` | Dynamic board iteration, BOARD_NAMES_EN extended, formatting fixes |
| `scripts/gen_en_site.py` | SSR related articles in make_article_html() |
| `scripts/gen_image_sitemap.py` | **New file** — image sitemap generator |

## Rollback

Revert commits. No database, no external services. All output is static files.
