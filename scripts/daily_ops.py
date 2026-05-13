#!/usr/bin/env python3
"""
Daily operations: crawler relations + forum activity simulation.
Run once per day to keep the site looking active and maintain AI crawler relationships.

Crawler relations:
  - IndexNow URL submission (Bing → ChatGPT/Copilot/DuckDuckGo)
  - AI-friendly file health check (llms.txt, robots.txt, sitemap)
  - Sitemap + RSS freshness

Forum simulation:
  - Adds replies to random articles
  - Updates today/yesterday stats
  - Flags hot discussions
  - Bumps article dates on recently active posts
"""
import json, random, sys, time
from pathlib import Path
from datetime import date, datetime, timedelta
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
EN_ARTICLES = ROOT / "en" / "articles.json"
CN_ARTICLES = ROOT / "articles.json"

# ── Config ──────────────────────────────────────────────
REPLIES_PER_RUN = (8, 25)       # random range of replies to distribute
HOT_THRESHOLD = 5               # articles with >= this many replies get 🔥 hot tag
STATS_TODAY = 3                 # today's new posts (looks active but not spammy)
STATS_YESTERDAY = 570           # yesterday's activity baseline
BUMP_FRESH_COUNT = 3            # articles to date-bump per run


def simulate_forum():
    """Add forum activity signals — replies, hot tags, fresh dates."""
    changed = 0

    for articles_path in [EN_ARTICLES, CN_ARTICLES]:
        if not articles_path.exists():
            continue
        data = json.loads(articles_path.read_text(encoding="utf-8"))

        # Update site stats
        data["site"]["stats"]["today"] = STATS_TODAY
        data["site"]["stats"]["yesterday"] = STATS_YESTERDAY

        # Collect all articles
        all_articles = []
        for board in data["boards"]:
            for art in board["posts"]:
                all_articles.append((board, art))

        # Distribute replies randomly
        total_replies = random.randint(*REPLIES_PER_RUN)
        num_recipients = min(total_replies, max(1, len(all_articles) // 4))
        recipients = random.sample(all_articles, num_recipients)
        replies_left = total_replies
        for i, (board, art) in enumerate(recipients):
            share = replies_left // (num_recipients - i) if i < num_recipients else replies_left
            if share > 0:
                art["replies"] = art.get("replies", 0) + share
                replies_left -= share

        # Flag hot articles
        for board in data["boards"]:
            for art in board["posts"]:
                if art.get("replies", 0) >= HOT_THRESHOLD and not art.get("hot"):
                    art["hot"] = True
                    changed += 1

        # Mark recently active articles (separate from publication date)
        bumpable = [a for _, a in all_articles if a.get("replies", 0) > 0]
        if bumpable:
            today_str = date.today().isoformat()
            for art in random.sample(bumpable, min(BUMP_FRESH_COUNT, len(bumpable))):
                art["lastActive"] = today_str
                changed += 1

        articles_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n"
        )

    return changed


def run_indexnow():
    """Submit sitemap URLs to IndexNow (Bing/Yandex)."""
    import subprocess, re
    r = subprocess.run(
        ["python3", "scripts/indexnow_submit.py"],
        capture_output=True, text=True, cwd=str(ROOT), timeout=60
    )
    if r.returncode == 0:
        m = re.search(r'(\d+)\s+URLs?\s+submitted', r.stdout)
        if m:
            return int(m.group(1))
        return r.stdout.strip()[-100:] or "ok"
    return f"error: {r.stderr[:200]}"


def check_ai_files():
    """Check that key AI-friendly files are accessible and not stale."""
    import urllib.request
    import urllib.error

    BASE = "https://dingjiu1989-hue.github.io"
    checks = {
        "/llms.txt": "AI site index",
        "/llms-full.txt": "Full EN content",
        "/llms-full-cn.txt": "Full CN content",
        "/robots.txt": "Crawler rules",
        "/sitemap.xml": "XML sitemap",
        "/en/feed.xml": "EN RSS",
        "/md/en/tech/api-gateway-implementation.md": "MD copies sample",
    }

    statuses = {}
    for path, desc in checks.items():
        url = f"{BASE}{path}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "DailyOps/1.0"})
            resp = urllib.request.urlopen(req, timeout=15)
            size = len(resp.read())
            healthy = resp.status == 200 and size > 100
            statuses[desc] = f"{'OK' if healthy else 'SMALL'} ({size//1024}KB)" if healthy else f"SMALL ({size}B)"
        except Exception as e:
            statuses[desc] = f"FAIL: {str(e)[:60]}"

    return statuses


def main():
    today = date.today().isoformat()
    print(f"=== Daily Ops — {today} ===\n")

    # 1. IndexNow submission (crawler relations)
    print("▶ Crawler relations: IndexNow")
    ix_result = run_indexnow()
    print(f"  IndexNow: {ix_result}")

    # 2. AI file health check
    print("\n▶ AI file health:")
    for desc, status in check_ai_files().items():
        print(f"  {desc}: {status}")

    # 3. Forum activity simulation
    print("\n▶ Forum simulation:")
    changed = simulate_forum()
    print(f"  {changed} articles updated (replies/hot/dates)")

    # 4. Regenerate site + AI-friendly files + RSS
    print("\n▶ Site rebuild:")
    import subprocess
    for step, cmd in [
        ("Site HTML", ["python3", "scripts/gen_en_site.py"]),
        ("AI files", ["python3", "scripts/gen_ai_friendly.py"]),
    ]:
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT), timeout=300)
        if r.returncode == 0:
            last_line = [l for l in r.stdout.strip().split("\n") if l][-1] if r.stdout.strip() else ""
            print(f"  {step}: OK — {last_line[:80]}")
        else:
            print(f"  {step}: FAIL — {r.stderr[:200]}")
            return 1

    # 5. RSS feeds
    print("\n▶ RSS/Feeds:")
    for cmd in [
        ["python3", "scripts/gen_rss.py"],
        ["python3", "scripts/generate_json_feed.py"],
    ]:
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT), timeout=60)
        if r.returncode == 0:
            print(f"  {' '.join(cmd[2:])}: OK")
        else:
            print(f"  {' '.join(cmd[2:])}: FAIL")

    print(f"\n✓ Daily ops complete — {today}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
