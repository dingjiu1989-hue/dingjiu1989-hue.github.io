# Troubleshooting & Known Issues

## GSC Sitemap "无法抓取" (Can't Crawl)

**Symptoms:** Google Search Console shows all sitemaps as "无法抓取" with "未知" type and 0 discovered pages.

**Root cause:** RSS feeds (`en/feed.xml`, `feed.xml`) were submitted to GSC as sitemaps. RSS uses a different XML schema (`<item>`, `<title>`, `<description>` tags) than sitemaps (`<url>`, `<loc>`, `<lastmod>`). GSC cannot parse RSS XML and marks them as failed.

**Fix (2026-05-21):** Removed RSS feed URLs from `submit_sitemap_gsc()` in `scripts/maintenance.py`. Only `sitemap.xml` and `images/sitemap.xml` are now submitted.

**Files involved:**
- `scripts/maintenance.py` — `submit_sitemap_gsc()` function, the `feeds` list

**To re-submit after fix:**
```bash
python3 -c "
from pathlib import Path
import sys
sys.path.insert(0, '.')
from scripts.maintenance import submit_sitemap_gsc
submit_sitemap_gsc()
"
```

**Expected resolution time:** 24-48 hours for GSC to recrawl and update status.

---

## GSC OAuth Token Expired

**Symptoms:** `google.auth.exceptions.RefreshError: invalid_grant` when running maintenance or weekly audit scripts.

**Root cause:** GSC OAuth refresh token expired (valid ~6 months). Token was originally authorized 2026-05-15.

**Fix (2026-05-20):** Delete old token and re-authorize via local server flow:
```bash
rm data/gsc-token.json
python3 -c "
from google_auth_oauthlib.flow import InstalledAppFlow
flow = InstalledAppFlow.from_client_secrets_file('oauth-client.json', ['https://www.googleapis.com/auth/webmasters'])
creds = flow.run_local_server(port=0, open_browser=True)
import json
with open('data/gsc-token.json', 'w') as f:
    json.dump(json.loads(creds.to_json()), f)
"
```

**Files involved:**
- `data/gsc-token.json` — OAuth token file
- `oauth-client.json` — Google Cloud OAuth client (SourceHub SEO project)

**Next token expiry:** ~2026-11-20 (re-authorize when `invalid_grant` appears).

---

## RSS Feed URL Changes

**Symptoms:** `gen_daily_news.py` shows `[skip] HTTP Error 404` or `[skip] HTTP Error 308` for RSS feeds.

**Known failures and fixes:**

| Source | Old URL (broken) | New URL (working) | Date fixed |
|--------|------------------|-------------------|------------|
| The Verge AI | `https://www.theverge.com/ai-artificial-intelligence/rss.xml` | `https://www.theverge.com/rss/ai-artificial-intelligence/index.xml` | 2026-05-21 |
| Ars Technica AI | `https://feeds.arstechnica.com/arstechnica/ai` | `https://arstechnica.com/tag/ai/feed/` | 2026-05-21 |
| VentureBeat AI | `https://venturebeat.com/category/ai/feed/` | `https://venturebeat.com/category/ai/feed` (no trailing slash) | 2026-05-21 |
| Anthropic Blog | `https://www.anthropic.com/feed.xml` | Removed (no working feed URL found) | 2026-05-21 |

**To add/replace a feed:**
Edit the `RSS_FEEDS` list at the top of `scripts/gen_daily_news.py`.

**Current working feeds (9):**
TechCrunch AI, The Verge AI, Ars Technica AI, VentureBeat AI, VentureBeat (main), MIT Tech Review AI, ZDNet AI, MarkTechPost, NVIDIA Blog.

---

## Dev.to Syndication Stuck (422 "Canonical url already taken")

**Symptoms:** `syndicate_devto.py` fails with `422 Canonical url already taken` for all articles.

**Root cause:** The `.devto-published-cache.json` file was initialized as `{"slugs": []}` on first run, but the API had already published ~800 articles. With an empty cache, `get_published_slugs()` kept returning nothing, so the script tried to publish articles dev.to already had.

**Fix (2026-05-20):** Added a check in `get_published_slugs()` at `scripts/syndicate_devto.py`:
```python
if cached_slugs:  # Only use cache if non-empty
    return cached_slugs
# Otherwise force refresh from API
```

**To force refresh cache:**
Delete `.devto-published-cache.json` and re-run syndication.

---

## Sitemap/Feed Size Too Large

**Symptoms:** Large files impacting GitHub Pages load time or GSC processing.

**Current sizes (2026-05-21):**

| File | Size | URLs/Items |
|------|------|------------|
| `sitemap.xml` | ~315 KB | 948 URLs |
| `images/sitemap.xml` | ~406 KB | 914 images |
| `en/feed.xml` | ~498 KB | 100 articles |
| `feed.xml` | ~39 KB | 65 articles |
| `en/feed.json` | ~3.9 MB | 200 items |

**Limits:**
- GSC sitemap: 50 MB, 50,000 URLs — safe
- GitHub Pages: 100 MB per file — safe
- RSS reader compatibility: < 1 MB recommended for `en/feed.xml` (borderline, truncate in `gen_rss.py` if needed)

---

## all.html Size Over 100KB

**Symptoms:** `en/all.html` exceeds 100 KB, impacting page load performance.

**Root cause:** Full article metadata list with date strings in every list item.

**Fix (2026-05-20):** Removed `<small>` date wrappers and `title` attribute dates. Final size: 97 KB from 132 KB.

**If it grows again:** Check `gen_en_site.py` — the `all.html` generation section. Compact list items further if needed.

---

## Heading Level Inflation in MD→HTML Conversion

**Symptoms:** Every rebuild cycle increases heading levels (h1→h2→h3→...), degrading SEO and readability.

**Root cause:** `md_to_html()` in `gen_en_site.py` increments heading levels (e.g., `#` → `<h2>` instead of `<h1>`), and each rebuild on the same md file compounds the shift.

**Fix (2026-05-20):** Added `_strip_title_headings()` that removes markdown headings matching the article title. The page template provides the H1; body headings should remain at their natural level.

**Status:** Residual issue — the fix prevents new inflation but existing files may still have shifted headings. Run a one-time scan to check.

---

## CN Site Registration Missing Boards

**Symptoms:** `register_new_articles.py` crashes on `StopIteration` for CN articles.

**Root cause:** CN `articles.json` doesn't have a `daily` board, but `md/zh/daily/` directory exists with files.

**Fix:** No fix needed — CN site has fewer boards than EN. The EN registration succeeds (857+ articles), and the CN failure is non-fatal. If CN daily board is ever needed, add it to `zh/articles.json`.

---

## Giscus Comments Not Loading

**Symptoms:** Comments section is empty or doesn't load on article pages.

**Checklist:**
1. Verify the page has `<script src="https://giscus.app/client.js">` with correct `data-repo`, `data-repo-id`, `data-category-id`
2. Check GitHub Discussions is enabled on the repo
3. Verify the Giscus app is installed on the repo
4. Check browser console for CSP or CORS errors

**Giscus config (in `gen_en_site.py`):**
```
data-repo: "dingjiu1989-hue/dingjiu1989-hue.github.io"
data-repo-id: "R_kgDOSWcDOw"
data-category: "Announcements"
data-category-id: "DIC_kwDOSWcDO84C9bsh"
data-mapping: "pathname"
```

---

## Dev.to Syndication Circuit Breaker

**Symptoms:** Syndication stops after 2 consecutive failures.

**Design:** `syndicate_devto.py` has a circuit breaker that stops publishing after 2 consecutive failures. Reset by re-running with `--force` or deleting the circuit breaker state.

**Check status:**
```bash
python3 scripts/syndicate_devto.py --dry-run
```
