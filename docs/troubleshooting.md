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

## Custom Domain Migration (github.io → aidev.fit)

**Symptoms:** Site was served from `https://dingjiu1989-hue.github.io` but needed a custom domain (`aidev.fit`) for brand trust, SEO, and professional appearance.

**Root cause:** Initial deployment used GitHub Pages default domain. As the site grew to 900+ articles, a custom domain was needed.

**Migration steps (2026-05-22):**
1. Registered `aidev.fit` at DNSPod
2. Created `scripts/site_config.py` as single source of truth for `BASE_URL`, `SITE_DOMAIN`, `SITE_NAME`
3. Updated all active scripts to import from `site_config.py` or sed-replace hardcoded URLs
4. Created `CNAME` file at repo root with `aidev.fit`
5. Added 2 A records in DNSPod: `185.199.108.153` and `185.199.109.153` (free tier limit)
6. Rebuilt all generated files with new BASE_URL
7. Updated static pages: about.html, privacy.html, articles.json (EN + CN)

**Files modified:**
- `scripts/site_config.py` (new) — centralized config
- `scripts/gen_en_site.py` — import site_config, `{BASE}` in templates
- `scripts/gen_ai_friendly.py` — import site_config, f-string robots.txt
- `scripts/gen_rss.py`, `scripts/generate_json_feed.py` — sed replace
- `scripts/maintenance.py` — sed replace + fix freshness bugs
- `scripts/maintain.py` — sed replace
- `scripts/indexnow_submit.py` — HOST change
- `scripts/gen_daily_news.py` — User-Agent + frontmatter URLs
- `scripts/syndicate_devto.py`, `syndicate_hashnode.py`, `syndicate_medium.py` — BASE URL
- `scripts/track_crawlers.py` — BASE URL + GSC siteUrl check
- `scripts/add_en_seo.py`, `scripts/gen_image_sitemap.py` — sed replace
- `CNAME` (new) — aidev.fit
- `CLAUDE.md` — updated domain reference
- `en/about.html`, `en/privacy.html`, `en/articles.json`, `articles.json` — static URL updates

**Pending:**
- Register `https://aidev.fit` in Google Search Console
- Resubmit sitemaps to GSC
- DNS propagation may take minutes to hours
- GitHub Pages will auto-detect CNAME and enable `aidev.fit` with HTTPS

---

## GitHub Actions: ModuleNotFoundError from Missing PYTHONPATH

**Symptoms:** CI job fails immediately with:
```
ModuleNotFoundError: No module named 'html2text'
ModuleNotFoundError: No module named 'scripts'
ModuleNotFoundError: No module named 'site_config'
```

**Root cause (triple failure):**

1. **`PYTHONPATH=.` missing** — any script that does `from scripts.site_config import ...` needs `PYTHONPATH=.` in the environment. This applies to: `gen_en_site.py`, `gen_ai_friendly.py`, `gen_rss.py`, `generate_json_feed.py`, `indexnow_submit.py`.

2. **`html2text markdown Pillow` not installed** — these are runtime dependencies for site/feed generation, not just local dev deps. Every workflow that calls gen scripts needs `pip install Pillow html2text markdown` before running them.

3. **Subprocess calls inside Python scripts** — `maintain.py` uses `subprocess.run(cmd, shell=True)` to call other scripts. These also need PYTHONPATH. Fix either in the caller (prefix cmd) or in the workflow (set PYTHONPATH in env).

**Fix (2026-05-25):** Applied to `maintenance.yml`, `daily-news.yml`, `weekly-maintenance.yml`, and `scripts/maintain.py`:
- Added `PYTHONPATH=.` before every script call that imports from `scripts.*`
- Added `pip install Pillow html2text markdown` as a dedicated step (before any generation scripts)
- In `maintain.py`, changed `python3 scripts/gen_ai_friendly.py` → `PYTHONPATH=. python3 scripts/gen_ai_friendly.py`

**Files involved:**
- `.github/workflows/maintenance.yml`
- `.github/workflows/daily-news.yml`
- `.github/workflows/weekly-maintenance.yml`
- `scripts/maintain.py`

---

## GitHub Actions: Non-Critical Steps Failing Entire Workflow

**Symptoms:** `weekly-maintenance.yml` fails at "Run maintenance" step with exit code 1, skipping all subsequent steps (IndexNow, search engine submission, JSON feeds, social syndication, commit).

**Root cause:** `maintain.py` uses `ok &= run(...)` for every step. If any step fails (GSC OAuth, Bing sync), `ok` becomes `False` and `main()` returns 1. The GSC/Bing steps depend on external services and OAuth tokens that routinely expire on CI runners.

**Fix (2026-05-25):** Made non-critical steps non-blocking in `scripts/maintain.py`:
```python
# Before:
ok &= run("python3 scripts/bing_sync.py", "Bing Webmaster sync")
ok &= resubmit_sitemaps()

# After:
run("python3 scripts/bing_sync.py", "Bing Webmaster sync")  # non-blocking
resubmit_sitemaps()  # non-blocking: GSC OAuth may fail on CI
```

**Design principle:** Steps that depend on external services (GSC API, Bing Webmaster API) should log warnings but not fail the build. Only steps critical to content generation should gate the `ok` flag.

---

## CN RSS/JSON Feed: Wrong Content Language and Broken URLs

**Symptoms:**
- CN RSS (`feed.xml`) item URLs have double slash: `https://aidev.fit//daily/...`
- CN RSS `<content:encoded>` body is English (not Chinese)
- CN JSON Feed (`feed.json`) article URLs point to `/en/daily/...` instead of `/daily/...`

**Root cause (three bugs in gen_rss.py + generate_json_feed.py):**

1. **Double slash**: CN `base_path` is `""` (empty, because CN pages live at root). `f'{BASE}/{base_path}/{board}/{slug}.html'` → `https://aidev.fit//daily/...`.

2. **English body in CN RSS**: `get_body_html()` always reads from `ROOT / 'md' / 'en' / ...`. CN content is at `md/zh/`. Also, `lang` parameter in `build_feed()` is `zh-CN` but the filesystem directory is `zh` (not `zh-CN`).

3. **`/en/` prefix in CN JSON Feed**: `art_url = f"{SITE_URL}/en/{board['id']}/{art['slug']}.html"` — hardcoded `/en/` for all languages.

**Fix (2026-05-25):**

`gen_rss.py`:
```python
# URL: handle empty base_path to avoid double slash
url = f'{BASE}/{base_path}/{p["board"]}/{p["slug"]}.html' if base_path else f'{BASE}/{p["board"]}/{p["slug"]}.html'

# MD: map lang code to filesystem directory
md_lang = 'zh' if lang == 'zh-CN' else 'en'
body = get_body_html(p['slug'], p['board'], md_lang)
```

`generate_json_feed.py`:
```python
# URL: use url_prefix parameter ('' for CN, 'en' for EN)
if url_prefix:
    art_url = f"{SITE_URL}/{url_prefix}/{board['id']}/{art['slug']}.html"
else:
    art_url = f"{SITE_URL}/{board['id']}/{art['slug']}.html"

# MD: map language code
md_lang = 'zh' if language == 'zh-CN' else 'en'
body_html = get_body(art['slug'], board['id'], md_lang)
```

**CN vs EN URL structure (authoritative):**
| Aspect | EN | CN |
|--------|-----|-----|
| HTML pages | `/en/{board}/{slug}.html` | `/{board}/{slug}.html` |
| RSS feed | `/en/feed.xml` | `/feed.xml` |
| JSON Feed | `/en/feed.json` | `/feed.json` |
| MD source | `md/en/{board}/{slug}.md` | `md/zh/{board}/{slug}.md` |
| Language tag | `en`, `lang="en"` | `zh-CN`, `lang="zh-CN"` |
| No `/zh/` path exists — CN is the default language with hreflang alternates |

---

## Duplicate RSS Generation: maintenance.py Overwrites gen_rss.py Output

**Symptoms:** Remote RSS feeds have correct URLs but zero `content:encoded` elements. XML structure is simpler than expected — missing `xmlns:content` namespace, no `<category>` tags, different `<lastBuildDate>` format. Feeds generated locally via `gen_rss.py` look correct, but the deployed version on `aidev.fit` is different.

**Root cause:** `scripts/maintenance.py` had its own `generate_rss()` function (lines 179–213, now removed) that was completely independent of `scripts/gen_rss.py`. In the maintenance workflow, `gen_rss.py` ran first in the "Rebuild site" step (producing full-content feeds), then `maintenance.py` ran in the "Run maintenance" step and **overwrote** both `feed.xml` and `en/feed.xml` with metadata-only versions.

The duplicate had zero overlap with `gen_rss.py`:
- No `xmlns:content` namespace → no `<content:encoded>` elements
- No markdown body reading → description-only, no full article text
- No date sorting — boards iterated in JSON order
- No WebSub hub link
- No `content:encoded` CDATA blocks

**Fix (2026-05-25):** Removed `generate_rss()` function and its calls from `maintenance.py:main()`. RSS feed generation is now handled exclusively by `gen_rss.py`, which is called in the "Rebuild site" step before `maintenance.py` runs.

**Before (in maintenance.py `main()`):**
```python
print('[3/6] Chinese RSS feed')
generate_rss(data, FEED_XML, 'zh')
...
print('[5/6] English RSS feed')
if en_data:
    generate_rss(en_data, EN_FEED_XML, 'en')
```

**After:** These steps removed. The workflow already runs `python3 scripts/gen_rss.py` in the "Rebuild site" step, which produces full-content feeds with `content:encoded`.

**Files involved:**
- `scripts/maintenance.py` — deleted `generate_rss()` function (~35 lines) and 2 call sites in `main()`
- `scripts/gen_rss.py` — canonical RSS generator (unchanged, now not overwritten)

**Lesson:** When a workflow calls multiple scripts that touch the same output files, check whether later steps silently overwrite earlier ones. The `gen_rss.py` → `maintenance.py` ordering was the correct intent (full RSS → rest of maintenance), but the overwrite made the ordering harmful.

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
