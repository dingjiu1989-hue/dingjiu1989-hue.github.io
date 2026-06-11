# AI Study Room (gh-pages-demo)

GitHub Pages static site: 850 EN + 150 ZH bilingual tech articles.
Live: https://aidev.fit (via ghost domain dingjiu1989-hue.github.io)

## Key Paths

| Path | Purpose |
|------|---------|
| `scripts/gen_en_site.py` | Build all EN HTML from `en/articles.json` |
| `scripts/gen_cn_site.py` | Build all CN HTML from `articles.json` |
| `scripts/gen_ai_friendly.py` | Generate llms.txt, llms-full.txt, robots.txt, /md/ |
| `scripts/gen_covers.py` | Generate 1200×630 PNG covers for all articles |
| `scripts/syndicate_devto.py` | Publish to dev.to (DA 90+) with canonical URLs |
| `scripts/syndicate_hashnode.py` | Publish to Hashnode (DA 80+) via GraphQL |
| `scripts/gen_rss.py` | Generate RSS feeds (EN + CN) |
| `scripts/generate_json_feed.py` | Generate JSON Feed (AI-friendly RSS) |
| `scripts/indexnow_submit.py` | Push URL changes to IndexNow (Bing) |
| `scripts/register_new_articles.py` | Register new articles into sitemap + feeds |
| `scripts/ping_search_engines.py` | Ping Google/Bing/WebSub/IndexNow after builds |
| `scripts/crawler_health_check.py` | Verify all crawler discovery endpoints (run hourly) |
| `scripts/gsc_analyze.py` | Pull GSC search performance report (28-day window) |
| `scripts/maintain.py` | Full rebuild: site + AI files + RSS + feeds + covers |
| `.github/workflows/maintenance.yml` | Hourly rebuild via GitHub Actions |
| `.github/workflows/devto-syndicate.yml` | Dev.to syndication every 3h |
| `data/syndication-log.json` | Daily publish tracking (cap: 200/day across platforms) |

## Quick Commands

```bash
# Full rebuild + syndication
python3 scripts/maintain.py

# Site only (HTML + CSS + JS)
python3 scripts/gen_en_site.py
python3 scripts/gen_cn_site.py

# AI-friendly files only
python3 scripts/gen_ai_friendly.py

# Covers only
python3 scripts/gen_covers.py

# Syndicate to dev.to (3 per run, 120s interval)
python3 scripts/syndicate_devto.py

# Push URLs to IndexNow
python3 scripts/indexnow_submit.py
```

## Conventions

- **All site content is auto-generated** from `en/articles.json` and `articles.json` (CN). Never edit HTML files directly.
- **Canonical URLs** point to `https://aidev.fit` for all syndicated copies.
- **html2text global instance** — always create a fresh instance per function; the shared global at module level corrupts after ~500 articles.
- **Images** live in `images/covers/en/{board}/{slug}.png` (1200×630, auto-generated).
- **Risk controls**: 3 articles/run, 120s between posts, circuit breaker at 2 failures, 200/day global cap.

## Key Architecture

- `gen_en_site.py` reads `en/articles.json` → generates `/en/{board}/{slug}.html` + homepage + sitemap + search index
- Boards: tech, sidehustle, tools, ai, compare, architecture, database, security (EN) + same 5 in ZH
- AI crawlers explicitly welcomed in `robots.txt` (28 crawler rules)
- JSON-LD structured data on every article page
- No framework, no build tool — raw HTML/CSS/JS, no dependencies beyond Python stdlib + Pillow + html2text

## Claude Code Hooks

Project-level hooks in `.claude/hooks/`:

| Hook | Event | Purpose |
|------|-------|---------|
| `dangerous-actions-blocker.sh` | PreToolUse (Bash) | Blocks `rm -rf` on project root, force-push to main; warns on `git reset --hard` |
| `site-regenerate-reminder.sh` | PostToolUse (Edit\|Write) | Reminds to regenerate HTML when `articles.json`, `gen_*.py`, or `md/` files change |
| `check-sensitive-files.sh` | UserPromptSubmit | Flags prompts mentioning push/deploy + sensitive keywords |

Permission deny list in `.claude/settings.json`:
- Blocks reading `.env`, `credentials*`, `*.pem`, `**/secrets/**`, `oauth-client.json`
