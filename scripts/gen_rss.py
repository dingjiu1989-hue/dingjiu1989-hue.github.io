#!/usr/bin/env python3
"""Generate RSS 2.0 feeds for English and Chinese articles.

Google discovers new pages faster via RSS/Atom feeds than sitemaps alone.
Most recent 50 articles get full <content:encoded> for RSS readers and AI consumption.
Total limited to 100 items to keep file size reasonable.
"""

import json, re
from pathlib import Path
from datetime import datetime, timezone as tz
from email.utils import format_datetime

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://aidev.fit"
TODAY = datetime.now(tz.utc)

def _rfc822(date_str):
    """Convert YYYY-MM-DD to RFC 822 datetime."""
    dt = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=tz.utc)
    return format_datetime(dt, usegmt=True)


def get_body_html(slug, board_id, lang="en"):
    """Read article body from md file, convert to HTML."""
    md_path = ROOT / 'md' / lang / board_id / f'{slug}.md'
    if md_path.exists():
        content = md_path.read_text(encoding='utf-8')
        if content.startswith('---'):
            end = content.find('---', 3)
            if end > 0:
                content = content[end + 3:].strip()
        try:
            import markdown as md_lib
            html = md_lib.markdown(content, extensions=['fenced_code', 'codehilite', 'tables'])
        except ImportError:
            html = f'<pre>{content}</pre>'
        # Strip leading H1 title duplicate
        return html.strip()
    return '<p>Content coming soon.</p>'


def cdata(text):
    """Wrap text in CDATA, escaping any ]]> sequences."""
    safe = text.replace(']]>', ']]]]><![CDATA[>')
    return f'<![CDATA[{safe}]]>'


def build_feed(articles_json, base_path, title, description, lang, homepage):
    """Build RSS 2.0 XML string from articles.json with full content for recent items."""
    data = json.loads(articles_json.read_text(encoding="utf-8"))

    posts = []
    for board in data["boards"]:
        for post in board["posts"]:
            posts.append({**post, "board": board["id"]})
    posts.sort(key=lambda p: p["date"], reverse=True)
    posts = posts[:100]  # Keep feed to 100 most recent

    items = []
    for i, p in enumerate(posts):
        url = f'{BASE}/{base_path}/{p["board"]}/{p["slug"]}.html' if base_path else f'{BASE}/{p["board"]}/{p["slug"]}.html'

        # Full content for most recent 50
        content_encoded = ''
        if i < 50:
            try:
                md_lang = 'zh' if lang == 'zh-CN' else 'en'
                body = get_body_html(p['slug'], p['board'], md_lang)
                # Strip H1 title duplicate from body
                body = re.sub(r'<h[12][^>]*>' + re.escape(p['title']) + r'</h[12]>', '', body, count=1)
                content_encoded = f'\n      <content:encoded>{cdata(body)}</content:encoded>'
            except Exception:
                pass

        items.append(
            f"    <item>\n"
            f"      <title>{cdata(p['title'])}</title>\n"
            f"      <link>{url}</link>\n"
            f"      <guid isPermaLink=\"true\">{url}</guid>\n"
            f"      <description>{cdata(p.get('description', ''))}</description>{content_encoded}\n"
            f"      <pubDate>{_rfc822(p['date'])}</pubDate>\n"
            f"    </item>"
        )

    now_rfc = format_datetime(TODAY, usegmt=True)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">
  <channel>
    <title>{title}</title>
    <link>{homepage}</link>
    <description>{description}</description>
    <language>{lang}</language>
    <lastBuildDate>{now_rfc}</lastBuildDate>
    <atom:link href="{homepage.rstrip('/')}/feed.xml" rel="self" type="application/rss+xml"/>
    <atom:link rel="hub" href="https://pubsubhubbub.appspot.com/"/>
{chr(10).join(items)}
  </channel>
</rss>"""


def main():
    # English feed
    en_json = ROOT / "en" / "articles.json"
    if en_json.exists():
        feed = build_feed(
            en_json, base_path="en",
            title="AI Study Room – English",
            description="Developer tutorials, comparisons, side-hustle guides, and AI insights.",
            lang="en", homepage=f"{BASE}/en/",
        )
        out = ROOT / "en" / "feed.xml"
        out.write_text(feed, encoding="utf-8")
        print(f"  en/feed.xml — {feed.count('<item>')} articles, {out.stat().st_size//1024} KB")

    # Chinese feed
    cn_json = ROOT / "articles.json"
    if cn_json.exists():
        feed = build_feed(
            cn_json, base_path="",
            title="AI自习室 – 中文",
            description="开发者教程、工具对比、副业指南、AI洞见。",
            lang="zh-CN", homepage=f"{BASE}/",
        )
        out = ROOT / "feed.xml"
        out.write_text(feed, encoding="utf-8")
        print(f"  feed.xml — {feed.count('<item>')} articles, {out.stat().st_size//1024} KB")

    print("RSS feeds generated (full content for recent 50).")


if __name__ == "__main__":
    main()
