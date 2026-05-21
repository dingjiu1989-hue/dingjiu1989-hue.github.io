# Troubleshooting & Known Issues

> Living document. Add new issues here as they are discovered and resolved.

---

## robots.txt Counter Gets Stale

**Symptoms:** The log message says "21 AI crawler rules" but the actual count is different.

**Root cause:** The counter is a hardcoded string in `scripts/gen_ai_friendly.py` (line 479). It's not computed from the actual rules list.

**Fix:** Update the number manually when adding/removing crawlers. Current count: 23.

**Current crawler list (23):** Googlebot, Bingbot, GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, anthropic-ai, Google-Extended, PerplexityBot, meta-externalagent, FacebookBot, cohere-ai, CCBot, Applebot, Amazonbot, GrokBot, xAI, Bytespider, YouBot, PetalBot, plus `*` catch-all.

---

## Daily Article Lost from articles.json After Git Rebase

**Symptoms:** Article md file exists, HTML was built via fallback, but the article is missing from `articles.json` and won't appear in the sitemap.

**Root cause:** During `git rebase`, the auto-generated `articles.json` had conflicts. Resolving with `--ours` (remote) accepted a version that was generated before the daily article was registered.

**Fix:** Re-run `register_new_articles.py` to pick up the md file, then rebuild:
```bash
python3 scripts/register_new_articles.py
python3 scripts/gen_en_site.py
```

**Prevention:** After any rebase involving `articles.json`, verify the article count matches expectations.

---

## Freshness Bump Was Changing Publication Dates (Not lastActive)

## Freshness Bump Was Changing Publication Dates (Not lastActive)

**Symptoms:** Old articles appeared to be published on today's date. The `date` field in `articles.json` was being overwritten with the current date, making a January article look like it was published in May.

**Root cause:** `update_stats()` in `maintenance.py` used `post['date'] = TODAY` instead of `post['lastActive'] = TODAY`. This corrupted the original publication dates of 3 random articles per maintenance run.

**Fix (2026-05-21):** `update_stats()` now bumps `lastActive` only, leaving `date` untouched. Uses a 30-day staleness threshold:
```python
la = post.get('lastActive') or post['date']
if la < threshold.isoformat():
    post['lastActive'] = TODAY
```

**Impact:** 5 articles bumped per run, 2x/day via maintenance.yml → ~308 eligible → full cycle in ~31 days. Bumped articles get updated `dateModified` JSON-LD, sitemap `<lastmod>`, and visible "Last active" badge.

**Files involved:**
- `scripts/maintenance.py` — `update_stats()` function
- `scripts/bump_freshness.py` — new standalone script (same logic, for manual use)

**Note:** This bug was introduced in a previous maintenance refactor. The original intent was always to bump freshness signals, not publication dates.

## CLS (Cumulative Layout Shift) from JS-Injected Nav/Footer

**Symptoms:** Page content jumps after load when JavaScript injects the navigation bar and footer. Lighthouse/PageSpeed flags CLS > 0.1.

**Root cause:** Nav and footer are loaded via `js/include.js` and injected after page render. Without reserved space, all content below shifts down.

**Fix (2026-05-20):** Added `min-height` CSS placeholders in `css/style.css`:
```css
#nav-placeholder { min-height: 48px; }
#footer-placeholder { min-height: 100px; }
```

**Files involved:**
- `css/style.css` — `.nav-placeholder` and `.footer-placeholder` min-height rules

---

## LCP (Largest Contentful Paint) Too Slow

**Symptoms:** LCP > 2.5s on article pages. The cover image (1200x630 PNG) is the LCP element.

**Root cause:** Cover images were served as 1200x630 PNG without optimization, loaded without priority hints.

**Fix (2026-05-20):** Three-pronged optimization:
1. `fetchpriority="high"` + `decoding="sync"` on cover `<img>`
2. `<link rel="preload" as="image" type="image/webp" fetchpriority="high">` in `<head>`
3. WebP conversion: `gen_covers.py` now generates `.webp` versions (quality=82)
4. `<picture>` element with WebP source + PNG fallback

**Cover images:** 1000 covers converted (25.7MB → 15.8MB, 38% reduction).

**Files involved:**
- `scripts/gen_en_site.py` — article template, `<picture>` element, preload link
- `scripts/gen_covers.py` — WebP generation with Pillow

---

## WebP Cover Images Not Generated

**Symptoms:** All covers are PNG only; `images/covers/en/` has no `.webp` files.

**Root cause:** `gen_covers.py` only saved PNG, not WebP.

**Fix (2026-05-20):** Added WebP output to `gen_covers.py`:
```python
img.save(webp_path, "WEBP", quality=82)
```

**To regenerate missing WebP covers:**
```bash
python3 scripts/gen_covers.py
```

---

## GSC OAuth redirect_uri Error

**Symptoms:** Browser shows "Missing required parameter: redirect_uri" when authorizing GSC OAuth.

**Root cause:** Opening the authorization URL directly in a browser vs. using `flow.run_local_server()`. The latter creates a local HTTP server with the correct `redirect_uri` (http://localhost:PORT/), which the former lacks.

**Fix (2026-05-20):** Delete old token and use `run_local_server`:
```bash
rm data/gsc-token.json
python3 -c "
from google_auth_oauthlib.flow import InstalledAppFlow
flow = InstalledAppFlow.from_client_secrets_file('oauth-client.json',
    ['https://www.googleapis.com/auth/webmasters'])
creds = flow.run_local_server(port=0, open_browser=True)
import json
with open('data/gsc-token.json', 'w') as f:
    json.dump(json.loads(creds.to_json()), f)
"
```

---

## GSC OAuth Token Expired

**Symptoms:** `google.auth.exceptions.RefreshError: invalid_grant` when running maintenance or weekly audit scripts.

**Root cause:** GSC OAuth refresh token expired (valid ~6 months). Token was originally authorized 2026-05-15.

**Fix (2026-05-20):** Same procedure as above — delete token and re-authorize via `run_local_server()`.

**Files involved:**
- `data/gsc-token.json` — OAuth token file
- `oauth-client.json` — Google Cloud OAuth client (SourceHub SEO project)

**Next token expiry:** ~2026-11-20.

---

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
import sys; sys.path.insert(0, '.')
from scripts.maintenance import submit_sitemap_gsc
submit_sitemap_gsc()
"
```

**Expected resolution time:** 24-48 hours for GSC to recrawl and update status.

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

**To add/replace a feed:** Edit the `RSS_FEEDS` list at the top of `scripts/gen_daily_news.py`.

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

**To force refresh cache:** Delete `.devto-published-cache.json` and re-run syndication.

---

## Dev.to Syndication Circuit Breaker

**Symptoms:** Syndication stops after 2 consecutive failures.

**Design:** `syndicate_devto.py` has a circuit breaker that stops publishing after 2 consecutive failures.

**Reset:**
```bash
python3 scripts/syndicate_devto.py --force
```
Or delete the circuit breaker state file.

**Check status:**
```bash
python3 scripts/syndicate_devto.py --dry-run
```

---

## `maintenance.py` vs `maintain.py` Confusion

**Symptoms:** Workflow or cron references `maintenance.py` when it should reference `maintain.py` or vice versa.

**Root cause:** Two files with similar names:
- `scripts/maintenance.py` — Daily ops: sitemap freshness, RSS, GSC submission, health checks
- `scripts/maintain.py` — Weekly: full rebuild + dev.to syndication

**Fix:** Always check which file is appropriate for the task. The GitHub Actions workflows reference the correct one (`maintenance.yml` → `maintenance.py`).

---

## Git Push Rejected (Remote Ahead)

**Symptoms:** `git push` fails with "Updates were rejected because the remote contains work that you do not have locally."

**Root cause:** GitHub Actions workflows (`maintenance.yml`, `devto-syndicate.yml`, `daily-news.yml`) commit changes between local commits.

**Fix:**
```bash
git pull --rebase origin main
git push origin main
```

**Common after:** running the full pipeline locally while GitHub Actions is also running.

---

## Python Version / Library Warnings

**Symptoms:** Non-blocking warnings during script execution:
```
FutureWarning: You are using a Python version 3.9 past its end of life
NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+
```

**Root cause:** MacOS ships Python 3.9, which is EOL. Google's libraries now require 3.10+. urllib3 v2 requires OpenSSL 1.1.1+ but LibreSSL 2.8.3 is installed.

**Impact:** None. All scripts work correctly. Warnings can be safely ignored.

**Recommended fix:** Install Python 3.11+ via Homebrew:
```bash
brew install python@3.11
```

---

## Duplicate Title Headings in MD Files

**Symptoms:** 623 article files had 10,000+ redundant heading tags that duplicated the article title, causing poor SEO heading structure.

**Root cause:** The original article generation pipeline inserted the article title as an H1 inside the markdown body, while the page template also rendered it as an HTML `<h1>`. On each rebuild cycle, the inflation compounded.

**Fix (2026-05-20):** Added `_strip_title_headings()` in `gen_en_site.py` that strips markdown headings matching the article title from the body content.

**Residual risk:** Old files may still have shifted heading levels (e.g., H2 where H3 should be). The fix prevents new inflation but does not retroactively fix all files.

---

## Heading Level Inflation in MD→HTML Conversion

**Symptoms:** Every rebuild cycle increases heading levels (h1→h2→h3→...), degrading SEO and readability.

**Root cause:** `md_to_html()` in `gen_en_site.py` increments heading levels (e.g., `#` → `<h2>` instead of `<h1>`). Combined with duplicate title headings, each rebuild on the same md file compounds the shift.

**Fix (2026-05-20):** `_strip_title_headings()` removes markdown headings matching the article title. The page template provides the H1; body headings should remain at their natural level.

**Check for residual inflation:**
```bash
grep -c '<h2>' en/tech/some-article.html  # Should only have 1-2 H2s per article
```

---

## all.html Size Over 100KB

**Symptoms:** `en/all.html` exceeds 100 KB, impacting page load performance.

**Root cause:** Full article metadata list with date strings in every list item.

**Fix (2026-05-20):** Removed `<small>` date wrappers and `title` attribute dates. Final size: 97 KB from 132 KB.

**If it grows again:** Check `gen_en_site.py` — the `all.html` generation section. Compact list items further if needed.

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
- RSS reader compatibility: < 1 MB recommended for `en/feed.xml` (borderline)

---

## CN Site Registration Missing Boards

**Symptoms:** `register_new_articles.py` crashes on `StopIteration` for CN articles.

**Root cause:** CN `articles.json` doesn't have a `daily` board, but `md/zh/daily/` directory exists with files.

**Fix:** No fix needed — CN site has fewer boards than EN. The EN registration succeeds (857+ articles), and the CN failure is non-fatal.

---

## Giscus Comments Not Loading

**Symptoms:** Comments section is empty or doesn't load on article pages.

**Checklist:**
1. Page has `<script src="https://giscus.app/client.js">` with correct `data-repo`, `data-repo-id`, `data-category-id`?
2. GitHub Discussions enabled on the repo?
3. Giscus app installed on the repo?
4. Browser console shows CSP or CORS errors?

**Giscus config (in `gen_en_site.py`):**
```
data-repo: "dingjiu1989-hue/dingjiu1989-hue.github.io"
data-repo-id: "R_kgDOSWcDOw"
data-category: "Announcements"
data-category-id: "DIC_kwDOSWcDO84C9bsh"
data-mapping: "pathname"
```

---

## GitHub Actions Workflow Failures

**Symptoms:** GitHub Actions workflow fails with unclear error message.

### Common causes and fixes:

**1. The `GITHUB_TOKEN` doesn't have write permission.**
- Fix: Workflow `permissions:` block needs `contents: write`

**2. Python script crashed mid-way.**
- Fix: Check the workflow log for the exact Python error. Most failures are from `register_new_articles.py` CN board crash (harmless) or OAuth token expiry (needs re-auth).

**3. Workflow not triggering on schedule.**
- Fix: Ensure the cron expression uses UTC (GitHub Actions default). The workflow must have been pushed to the default branch (`main`).

**4. "Could not apply" during `git pull --rebase` in workflow.**
- Fix: This happens when two workflows commit simultaneously. The commit gets orphaned and needs a manual rebase.

---

## Adding a New Issue

When you discover a new problem:

1. Add a new `## Title` section to this file with:
   - **Symptoms** — what you observed
   - **Root cause** — why it happened
   - **Fix** — what was changed (with code/config snippets)
   - **Files involved** — which files were modified
   - **Date** — when it was fixed
2. Commit and push the updated file:
   ```bash
   git add docs/troubleshooting.md
   git commit -m "docs: add troubleshooting entry for <issue>"
   git push
   ```
