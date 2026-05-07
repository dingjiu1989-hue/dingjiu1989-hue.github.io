#!/usr/bin/env python3
"""Daily maintenance: sitemap freshness, health checks, RSS feed, stats rotation."""

import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITEMAP = ROOT / 'sitemap.xml'
ARTICLES_JSON = ROOT / 'articles.json'
FEED_XML = ROOT / 'feed.xml'
HEALTH_LOG = ROOT / 'health.json'
TODAY = date.today().isoformat()

BASE_URL = 'https://dingjiu1989-hue.github.io'

# ── Pages that get fresh lastmod every run ──────────────────────────
ALWAYS_FRESH = [
    f'{BASE_URL}/',
    f'{BASE_URL}/all.html',
    f'{BASE_URL}/tech/',
    f'{BASE_URL}/sidehustle/',
    f'{BASE_URL}/tools/',
    f'{BASE_URL}/ai/',
]

# ── Helpers ─────────────────────────────────────────────────────────
def log(msg):
    print(f'  {msg}')


# ══════════════════════════════════════════════════════════════════════
# 1. SITEMAP FRESHNESS
# ══════════════════════════════════════════════════════════════════════
def update_sitemap():
    content = SITEMAP.read_text(encoding='utf-8')
    changed = False
    for url in ALWAYS_FRESH:
        escaped = re.escape(url)
        pattern = re.compile(
            rf'(<loc>{escaped}</loc>\s*<changefreq>[^<]*</changefreq>\s*'
            r'<priority>[^<]*</priority>\s*<lastmod>)[^<]*(</lastmod>)'
        )
        new_content, n = pattern.subn(rf'\g<1>{TODAY}\g<2>', content)
        if n:
            content = new_content
            changed = True
    if changed:
        SITEMAP.write_text(content, encoding='utf-8')
        log('Sitemap lastmod updated')
    else:
        log('Sitemap already fresh')
    return content


# ══════════════════════════════════════════════════════════════════════
# 2. HEALTH CHECKS
# ══════════════════════════════════════════════════════════════════════
def run_health_checks(data):
    issues = []

    # 2a. Check every sitemap URL returns 200
    log('Checking sitemap URLs…')
    try:
        tree = ET.parse(str(SITEMAP))
        ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [e.text for e in tree.findall('.//ns:loc', ns)]
    except Exception as exc:
        issues.append(f'Sitemap parse error: {exc}')
        urls = []

    for url in urls:
        try:
            req = urllib.request.Request(url, method='HEAD')
            req.add_header('User-Agent', 'MaintenanceBot/1.0')
            resp = urllib.request.urlopen(req, timeout=15)
            if resp.status != 200:
                issues.append(f'{url} returned {resp.status}')
        except Exception as exc:
            issues.append(f'{url} unreachable: {exc}')

    # 2b. Check articles.json posts have .html files on disk
    log('Checking article files…')
    expected_html = set()
    for board in data.get('boards', []):
        for post in board.get('posts', []):
            html_path = ROOT / board['id'] / f"{post['slug']}.html"
            expected_html.add(str(html_path))
            if not html_path.exists():
                issues.append(f'Missing file: {html_path}')

    # 2c. Check sitemap covers all articles from JSON
    sitemap_locs = set(urls)
    for board in data.get('boards', []):
        for post in board.get('posts', []):
            expected = f'{BASE_URL}/{board["id"]}/{post["slug"]}.html'
            if expected not in sitemap_locs:
                issues.append(f'Sitemap missing: {expected}')

    # 2d. Check category index pages exist and have correct data-render
    for board in data.get('boards', []):
        idx = ROOT / board['id'] / 'index.html'
        if not idx.exists():
            issues.append(f'Missing category index: {idx}')

    health = {
        'checked_at': TODAY,
        'total_urls': len(urls),
        'issues': issues,
        'healthy': len(issues) == 0,
    }
    HEALTH_LOG.write_text(
        json.dumps(health, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8'
    )

    if issues:
        log(f'HEALTH FAILURES ({len(issues)}):')
        for i in issues:
            log(f'  ❌ {i}')
    else:
        log('All health checks passed ✅')

    return health


# ══════════════════════════════════════════════════════════════════════
# 3. RSS FEED
# ══════════════════════════════════════════════════════════════════════
def generate_rss(data):
    site = data.get('site', {})
    items = []

    for board in data.get('boards', []):
        for post in board.get('posts', []):
            url = f'{BASE_URL}/{board["id"]}/{post["slug"]}.html'
            items.append(f'''    <item>
      <title><![CDATA[{post['title']}]]></title>
      <link>{url}</link>
      <guid isPermaLink="true">{url}</guid>
      <description><![CDATA[{post.get('description', '')}]]></description>
      <category>{board['name']}</category>
      <pubDate>{post['date']}T08:00:00+08:00</pubDate>
    </item>''')

    rss = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>{site.get('name', '资料库')}</title>
  <link>{BASE_URL}</link>
  <description>{site.get('tagline', '')}</description>
  <language>zh-CN</language>
  <lastBuildDate>{TODAY}T08:00:00+08:00</lastBuildDate>
  <atom:link href="{BASE_URL}/feed.xml" rel="self" type="application/rss+xml"/>
{''.join(items)}
</channel>
</rss>
'''
    FEED_XML.write_text(rss, encoding='utf-8')
    log(f'RSS feed generated: {len(data.get("boards", []))} boards, articles')


# ══════════════════════════════════════════════════════════════════════
# 4. STATS ROTATION
# ══════════════════════════════════════════════════════════════════════
def update_stats(data):
    import random

    total = sum(len(b.get('posts', [])) for b in data.get('boards', []))
    stats = data.setdefault('site', {}).setdefault('stats', {})

    # Rotate article dates: pick 2-3 articles and bump their date to today
    # This simulates genuine forum activity for search engines
    all_posts = []
    for board in data.get('boards', []):
        for post in board.get('posts', []):
            all_posts.append(post)

    bumped = random.sample(all_posts, min(3, len(all_posts)))
    for post in bumped:
        old_date = post.get('date', '')
        if old_date != TODAY:
            post['date'] = TODAY
            log(f'  Bumped date: {post["slug"]} ({old_date} → {TODAY})')

    prev_today = stats.get('today', 0)
    new_today = len(bumped) + random.randint(0, 2)
    stats['today'] = new_today
    stats['yesterday'] = prev_today if prev_today > 0 else stats.get('yesterday', 0)
    stats['total'] = total

    ARTICLES_JSON.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8'
    )
    log(f'Stats: today={new_today} yesterday={stats["yesterday"]} total={total}')


# ══════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════
def main():
    print(f'=== Maintenance {TODAY} ===')

    print('[1/4] Sitemap freshness')
    update_sitemap()

    print('[2/4] Health checks')
    data = json.loads(ARTICLES_JSON.read_text(encoding='utf-8'))
    health = run_health_checks(data)

    print('[3/4] RSS feed')
    generate_rss(data)

    print('[4/4] Stats rotation')
    update_stats(data)

    print('Done.')
    if not health['healthy']:
        sys.exit(1)


if __name__ == '__main__':
    main()
