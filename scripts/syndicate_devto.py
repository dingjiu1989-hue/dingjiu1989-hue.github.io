#!/usr/bin/env python3
"""
Syndicate articles to dev.to via their API.

Strategy:
- Post a summary/teaser on dev.to with a canonical URL pointing back to our site
- dev.to has DA 90+ and is heavily crawled by AI (GPTBot, ClaudeBot, PerplexityBot)
- The canonical link tells search engines our site is the original source
- AI crawlers discover our content through dev.to's high-authority domain

Rate limit: dev.to allows 3 articles/hour on free tier.
"""
import json, time, os, sys
from pathlib import Path
from datetime import date

import _ssl_compat  # noqa: F401 — fix macOS LibreSSL TLS 1.3 issue

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://dingjiu1989-hue.github.io"

# Read API key from env var or file
API_KEY = os.environ.get("DEVTO_API_KEY")
if not API_KEY:
    key_file = ROOT / ".devto-key"
    if key_file.exists():
        API_KEY = key_file.read_text(encoding="utf-8").strip()

if not API_KEY:
    print("ERROR: Set DEVTO_API_KEY env var or create .devto-key file")
    print("Get your key at: https://dev.to/settings/extensions")
    sys.exit(1)

import subprocess
import urllib.request
import urllib.error

DEVTO_API = "https://dev.to/api"

def _use_curl():
    """Check if we should use curl (macOS LibreSSL workaround)."""
    import ssl
    return 'LibreSSL' in ssl.OPENSSL_VERSION

def devto_request(method, path, data=None):
    url = f"{DEVTO_API}{path}"

    if _use_curl():
        # macOS LibreSSL can't talk to Fastly CDN — use curl instead
        try:
            args = ['curl', '-s', '--max-time', '30', '-X', method,
                    '-H', f'api-key: {API_KEY}',
                    '-H', 'Content-Type: application/json',
                    '-H', 'User-Agent: AI-Study-Room-Syndicator/1.0']
            if data:
                args += ['-d', json.dumps(data)]
            args.append(url)
            result = subprocess.run(args, capture_output=True, text=True, timeout=35)
            if result.returncode == 0 and result.stdout.strip():
                parsed = json.loads(result.stdout)
                if isinstance(parsed, dict) and 'error' in parsed:
                    return parsed
                return parsed
            return None
        except Exception as e:
            print(f"  curl error: {e}")
            return None

    import urllib.request
    import urllib.error
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("api-key", API_KEY)
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "AI-Study-Room-Syndicator/1.0")
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8")
        if e.code == 429:
            return {"error": "rate_limit", "retry_after": 300}
        print(f"  API error ({e.code}): {err[:200]}")
        return None

def get_published_slugs():
    """Get list of already-published dev.to article slugs."""
    slugs = set()
    page = 1
    while True:
        articles = devto_request("GET", f"/articles/me?page={page}&per_page=100")
        if not articles:
            break
        for art in articles:
            # Extract our source slug from canonical URL
            canon = art.get("canonical_url", "")
            if "dingjiu1989-hue.github.io" in canon:
                slug = canon.split("/")[-1].replace(".html", "")
                slugs.add(slug)
        page += 1
        if len(articles) < 100:
            break
    return slugs

def parse_tags(tags_val):
    """Normalize tags to a list of dev.to-valid tag strings."""
    if isinstance(tags_val, list):
        raw = tags_val
    elif isinstance(tags_val, str):
        raw = [t.strip() for t in tags_val.split(',') if t.strip()]
    else:
        return []
    import re
    clean = []
    for t in raw:
        t = t.lower().replace(' ', '').replace('-', '')
        t = re.sub(r'[^a-z0-9]', '', t)  # dev.to allows only alphanumeric
        if t:
            clean.append(t)
    return clean


def make_article_body(art, board_id, en_data):
    """Build dev.to article body from markdown content."""
    md_path = ROOT / "md" / "en" / board_id / f'{art["slug"]}.md'
    if not md_path.exists():
        return None

    md_content = md_path.read_text(encoding="utf-8")
    # Remove frontmatter
    if md_content.startswith("---"):
        end = md_content.find("---", 3)
        if end > 0:
            md_content = md_content[end + 3:].strip()

    original_url = f"{BASE}/en/{board_id}/{art['slug']}.html"

    # Build a dev.to-optimized post with canonical link back to our site
    body = f"""---
title: "{art['title']}"
published: true
description: "{art.get('description', '')[:200]}"
tags: {', '.join(parse_tags(art.get('tags', ''))[:4])}
canonical_url: "{original_url}"
---

> *This article was originally published on [AI Study Room]({original_url}). For the full version with working code examples and related articles, visit the original post.*

{md_content[:5000]}

---

**Read the full article on [AI Study Room]({original_url})** for complete code examples, comparison tables, and related resources.

*Found this useful? Check out more [developer guides and tool comparisons]({BASE}/en/) on AI Study Room.*
"""
    return body

def main():
    en_json = ROOT / "en" / "articles.json"
    if not en_json.exists():
        print("ERROR: articles.json not found")
        return

    en_data = json.loads(en_json.read_text(encoding="utf-8"))

    # Flatten articles
    all_articles = []
    for board in en_data["boards"]:
        for art in board["posts"]:
            all_articles.append((board["id"], art))

    # Sort by board priority (Compare = highest CPC, then Tools, then others)
    board_priority = {"compare": 0, "tools": 1, "ai": 2, "tech": 3, "sidehustle": 4}
    all_articles.sort(key=lambda x: (board_priority.get(x[0], 99), x[1]["date"]), reverse=False)

    # Get already-published slugs
    published = get_published_slugs()
    print(f"Already published on dev.to: {len(published)}")

    # Pick articles to publish (limit: 3 per run per dev.to rate limits)
    to_publish = []
    for board_id, art in all_articles:
        if art["slug"] not in published:
            to_publish.append((board_id, art))
        if len(to_publish) >= 3:
            break

    if not to_publish:
        print("All articles already syndicated!")
        return

    print(f"Publishing up to {len(to_publish)} articles to dev.to...")
    published_count = 0
    for i, (board_id, art) in enumerate(to_publish):
        body = make_article_body(art, board_id, en_data)
        if not body:
            print(f"  SKIP (no markdown): {art['slug']}")
            continue

        article_data = {
            "article": {
                "title": art["title"],
                "description": art.get("description", "")[:200],
                "body_markdown": body,
                "published": True,
                "tags": parse_tags(art.get("tags", ""))[:4],
                "canonical_url": f"{BASE}/en/{board_id}/{art['slug']}.html",
            }
        }

        result = devto_request("POST", "/articles", article_data)
        if isinstance(result, dict) and result.get("url"):
            devto_url = result.get("url", "unknown")
            print(f"  [{i+1}/{len(to_publish)}] {art['title'][:60]}...")
            print(f"         URL: {devto_url}")
            published_count += 1
        elif isinstance(result, dict) and result.get("error") == "rate_limit":
            print(f"  ⏳ Rate limited. Stopping batch. Published {published_count} this run.")
            break
        else:
            print(f"  [{i+1}/{len(to_publish)}] FAILED: {art['title'][:60]}...")

        # Respect rate limit — dev.to allows ~3 articles per 15 min
        if i < len(to_publish) - 1:
            time.sleep(90)

    print(f"\nDone. {published_count} articles syndicated to dev.to this run.")

if __name__ == "__main__":
    main()
