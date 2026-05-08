#!/usr/bin/env python3
"""Generate RSS 2.0 feeds for English and Chinese articles.

Google discovers new pages faster via RSS/Atom feeds than sitemaps alone.
Feeds are registered in HTML <head> via <link rel="alternate"> tags.
"""

import json
from pathlib import Path
from datetime import datetime, timezone as tz
from email.utils import format_datetime

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://dingjiu1989-hue.github.io"
TODAY = datetime.now(tz.utc)

def _rfc822(date_str):
    """Convert YYYY-MM-DD to RFC 822 datetime."""
    dt = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=tz.utc)
    return format_datetime(dt, usegmt=True)


def build_feed(articles_json, base_path, title, description, lang, homepage):
    """Build RSS 2.0 XML string from articles.json."""
    data = json.loads(articles_json.read_text(encoding="utf-8"))

    # Flatten all posts with board context, sort by date descending
    posts = []
    for board in data["boards"]:
        for post in board["posts"]:
            posts.append({
                **post,
                "board": board["id"],
            })
    posts.sort(key=lambda p: p["date"], reverse=True)

    items = []
    for p in posts:
        url = f'{BASE}/{base_path}/{p["board"]}/{p["slug"]}.html'
        items.append(
            f"    <item>\n"
            f"      <title><![CDATA[{p['title']}]]></title>\n"
            f"      <link>{url}</link>\n"
            f"      <guid isPermaLink=\"true\">{url}</guid>\n"
            f"      <description><![CDATA[{p.get('description', '')}]]></description>\n"
            f"      <pubDate>{_rfc822(p['date'])}</pubDate>\n"
            f"    </item>"
        )

    now_rfc = format_datetime(TODAY, usegmt=True)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{title}</title>
    <link>{homepage}</link>
    <description>{description}</description>
    <language>{lang}</language>
    <lastBuildDate>{now_rfc}</lastBuildDate>
    <atom:link href="{homepage.rstrip('/')}/feed.xml" rel="self" type="application/rss+xml"/>
{chr(10).join(items)}
  </channel>
</rss>"""


def main():
    # English feed
    en_json = ROOT / "en" / "articles.json"
    if en_json.exists():
        feed = build_feed(
            en_json,
            base_path="en",
            title="AI Study Room – English",
            description="Developer tutorials, comparisons, side-hustle guides, and AI insights.",
            lang="en",
            homepage=f"{BASE}/en/",
        )
        (ROOT / "en" / "feed.xml").write_text(feed, encoding="utf-8")
        print(f"  en/feed.xml — {feed.count('<item>')} articles")

    # Chinese feed
    cn_json = ROOT / "articles.json"
    if cn_json.exists():
        feed = build_feed(
            cn_json,
            base_path="",
            title="AI自习室 – 中文",
            description="开发者教程、工具对比、副业指南、AI洞见。",
            lang="zh-CN",
            homepage=f"{BASE}/",
        )
        (ROOT / "feed.xml").write_text(feed, encoding="utf-8")
        print(f"  feed.xml — {feed.count('<item>')} articles")

    print("RSS feeds generated.")


if __name__ == "__main__":
    main()
