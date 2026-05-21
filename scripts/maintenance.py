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
EN_ARTICLES_JSON = ROOT / 'en' / 'articles.json'
FEED_XML = ROOT / 'feed.xml'
EN_FEED_XML = ROOT / 'en' / 'feed.xml'
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
    # English pages
    f'{BASE_URL}/en/',
    f'{BASE_URL}/en/tech/',
    f'{BASE_URL}/en/sidehustle/',
    f'{BASE_URL}/en/tools/',
    f'{BASE_URL}/en/ai/',
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
def run_health_checks(data, en_data=None):
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

    def check_article_files(boards, prefix=''):
        """Check .html files exist for articles in a boards list."""
        missing = []
        for board in boards:
            for post in board.get('posts', []):
                html_path = ROOT / prefix / board['id'] / f"{post['slug']}.html"
                if not html_path.exists():
                    missing.append(str(html_path))
        return missing

    # 2b. Check Chinese article files
    log('Checking Chinese article files…')
    issues.extend(f'Missing file: {p}' for p in check_article_files(data.get('boards', [])))

    # 2c. Check English article files
    if en_data:
        log('Checking English article files…')
        issues.extend(f'Missing file: {p}' for p in check_article_files(en_data.get('boards', []), prefix='en'))

    # 2d. Check sitemap covers all articles from JSON
    sitemap_locs = set(urls)
    for board in data.get('boards', []):
        for post in board.get('posts', []):
            expected = f'{BASE_URL}/{board["id"]}/{post["slug"]}.html'
            if expected not in sitemap_locs:
                issues.append(f'Sitemap missing: {expected}')
    if en_data:
        for board in en_data.get('boards', []):
            for post in board.get('posts', []):
                expected = f'{BASE_URL}/en/{board["id"]}/{post["slug"]}.html'
                if expected not in sitemap_locs:
                    issues.append(f'Sitemap missing: {expected}')

    # 2e. Check category index pages exist
    for board in data.get('boards', []):
        idx = ROOT / board['id'] / 'index.html'
        if not idx.exists():
            issues.append(f'Missing category index: {idx}')
    if en_data:
        for board in en_data.get('boards', []):
            idx = ROOT / 'en' / board['id'] / 'index.html'
            if not idx.exists():
                issues.append(f'Missing English category index: {idx}')

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
# 3. RSS FEEDS
# ══════════════════════════════════════════════════════════════════════
def generate_rss(data, path, lang, site_url=BASE_URL):
    site = data.get('site', {})
    items = []

    for board in data.get('boards', []):
        for post in board.get('posts', []):
            if lang == 'en':
                url = f'{site_url}/en/{board["id"]}/{post["slug"]}.html'
            else:
                url = f'{site_url}/{board["id"]}/{post["slug"]}.html'
            items.append(f'''    <item>
      <title><![CDATA[{post['title']}]]></title>
      <link>{url}</link>
      <guid isPermaLink="true">{url}</guid>
      <description><![CDATA[{post.get('description', '')}]]></description>
      <category>{board['name']}</category>
      <pubDate>{post['date']}T08:00:00+08:00</pubDate>
    </item>''')

    feed_url = f'{site_url}/{path.relative_to(ROOT)}'
    rss = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>{site.get('name', '资料库')}</title>
  <link>{site_url}{'/en' if lang == 'en' else ''}</link>
  <description>{site.get('tagline', '')}</description>
  <language>{'en-US' if lang == 'en' else 'zh-CN'}</language>
  <lastBuildDate>{TODAY}T08:00:00+08:00</lastBuildDate>
  <atom:link href="{feed_url}" rel="self" type="application/rss+xml"/>
{''.join(items)}
</channel>
</rss>
'''
    path.write_text(rss, encoding='utf-8')
    log(f'RSS feed generated ({lang}): {len(data.get("boards", []))} boards')


# ══════════════════════════════════════════════════════════════════════
# 4. STATS ROTATION
# ══════════════════════════════════════════════════════════════════════
def update_stats(data, json_path):
    import random

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

    total = sum(len(b.get('posts', [])) for b in data.get('boards', []))
    stats = data.setdefault('site', {}).setdefault('stats', {})
    prev_today = stats.get('today', 0)
    new_today = len(bumped) + random.randint(0, 2)
    stats['today'] = new_today
    stats['yesterday'] = prev_today if prev_today > 0 else stats.get('yesterday', 0)
    stats['total'] = total

    json_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8'
    )
    log(f'Stats ({json_path.name}): today={new_today} yesterday={stats["yesterday"]} total={total}')


# ══════════════════════════════════════════════════════════════════════
# 7. GOOGLE SEARCH CONSOLE SITEMAP SUBMISSION
# ══════════════════════════════════════════════════════════════════════

def submit_sitemap_gsc():
    """Resubmit sitemaps to Google Search Console to trigger recrawl."""
    TOKEN_FILE = ROOT / "data" / "gsc-token.json"
    if not TOKEN_FILE.exists():
        log('No GSC token, skipping sitemap submission')
        return True

    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build

        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), ["https://www.googleapis.com/auth/webmasters"])
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())

        service = build("searchconsole", "v1", credentials=creds)
        feeds = [
            f"{BASE_URL}/sitemap.xml",
            f"{BASE_URL}/images/sitemap.xml",
        ]
        for feed in feeds:
            try:
                service.sitemaps().submit(siteUrl=BASE_URL + "/", feedpath=feed).execute()
                log(f'GSC submitted: {feed}')
            except Exception as e:
                log(f'GSC submit error ({feed}): {e}')
        return True
    except Exception as e:
        log(f'GSC API error: {e}')
        return False


# ══════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════
def main():
    print(f'=== Maintenance {TODAY} ===')

    print('[1/6] Sitemap freshness')
    update_sitemap()

    # Load data
    data = json.loads(ARTICLES_JSON.read_text(encoding='utf-8'))
    en_data = None
    if EN_ARTICLES_JSON.exists():
        en_data = json.loads(EN_ARTICLES_JSON.read_text(encoding='utf-8'))

    print('[2/6] Health checks')
    health = run_health_checks(data, en_data)

    print('[3/6] Chinese RSS feed')
    generate_rss(data, FEED_XML, 'zh')

    print('[4/6] Chinese stats rotation')
    update_stats(data, ARTICLES_JSON)

    print('[5/6] English RSS feed')
    if en_data:
        generate_rss(en_data, EN_FEED_XML, 'en')
    else:
        log('No English data, skipping')

    print('[6/6] English stats rotation')
    if en_data:
        update_stats(en_data, EN_ARTICLES_JSON)
    else:
        log('No English data, skipping')

    print('[7/7] GSC sitemap submission')
    submit_sitemap_gsc()

    print('Done.')
    if not health['healthy']:
        print(f'⚠ {len(health["issues"])} health issue(s) found — maintenance still completed')


if __name__ == '__main__':
    main()
