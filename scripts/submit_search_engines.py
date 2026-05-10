#!/usr/bin/env python3
"""Submit sitemap to multiple search engines beyond IndexNow.

IndexNow already covers: Bing, Yandex, Naver, Seznam, Brave, DuckDuckGo
This script handles: Google, Internet Archive, and other services.

Runs on GitHub Actions (Ubuntu) — no macOS LibreSSL issues.
"""

import json, re, sys
from pathlib import Path
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import URLError

ROOT = Path(__file__).resolve().parent.parent
SITEMAP = ROOT / 'sitemap.xml'
TRACKING = ROOT / 'data' / 'search-engine-submitted.json'
BASE = 'https://dingjiu1989-hue.github.io'


def load_sitemap_urls():
    content = SITEMAP.read_text(encoding='utf-8')
    return re.findall(r'<loc>([^<]+)</loc>', content)


def load_tracking():
    if TRACKING.exists():
        return json.loads(TRACKING.read_text(encoding='utf-8'))
    return {'submitted': {}, 'last_run': None}


def save_tracking(data):
    TRACKING.parent.mkdir(exist_ok=True)
    TRACKING.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')


def submit_google_indexing(urls):
    """Submit URLs to Google Indexing API via simple ping.

    Google deprecated the sitemap ping, but you can still use
    https://www.google.com/ping?sitemap=URL for a best-effort signal.
    """
    results = []
    for url in urls[:50]:  # batch limit
        try:
            ping_url = f'https://www.google.com/ping?sitemap={url}'
            req = Request(ping_url)
            resp = urlopen(req, timeout=15)
            results.append((url, resp.status))
        except URLError as e:
            code = getattr(e, 'code', 0)
            # 410 means deprecated but doesn't break anything
            if code == 410:
                results.append((url, 410))
            else:
                results.append((url, f'FAIL: {e.reason}'))
    return results


def submit_internet_archive(urls):
    """Request Internet Archive to save/crawl our pages."""
    results = []
    for url in urls[:10]:  # limit to avoid rate limiting
        try:
            save_url = f'https://web.archive.org/save/{url}'
            req = Request(save_url, method='POST')
            resp = urlopen(req, timeout=30)
            results.append((url, resp.status))
        except URLError as e:
            code = getattr(e, 'code', 0)
            # IA returns 403 for some content policies — skip silently
            results.append((url, code if code else f'FAIL: {e.reason}'))
    return results


def submit_mojeek(urls):
    """Submit URLs to Mojeek (UK privacy search engine).

    Mojeek has a simple URL submission endpoint.
    """
    results = []
    for url in urls[:10]:
        try:
            mojeek_url = f'https://www.mojeek.com/search?q=site%3A{url}&submit=Submit'
            # Their add URL endpoint
            add_url = f'https://www.mojeek.com/add?url={url}'
            req = Request(add_url)
            resp = urlopen(req, timeout=15)
            results.append((url, resp.status))
        except URLError as e:
            results.append((url, f'FAIL: {e.reason}'))
    return results


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'
    all_urls = load_sitemap_urls()
    tracking = load_tracking()
    submitted_before = tracking.get('submitted', {})

    if mode == 'diff':
        to_submit = [u for u in all_urls if u not in submitted_before]
    else:
        # 'all' mode — submit homepage and sitemap
        to_submit = [BASE + '/', BASE + '/en/', BASE + '/sitemap.xml']

    if not to_submit:
        print('No new URLs to submit.')
        return 0

    print(f'Submitting {len(to_submit)} URLs to additional search engines...')
    now = datetime.now(timezone.utc).isoformat()

    # Google (best-effort, deprecated endpoint)
    print('\n--- Google (ping) ---')
    results = submit_google_indexing(to_submit)
    for url, status in results[:3]:
        print(f'  {url[:60]}... → {status}')
    if len(results) > 3:
        print(f'  ... and {len(results) - 3} more')

    # Internet Archive
    print('\n--- Internet Archive (wayback) ---')
    ia_urls = to_submit[:5]  # fewer to avoid rate limits
    results = submit_internet_archive(ia_urls)
    for url, status in results:
        short = url.replace(BASE, '')
        print(f'  {short} → {status}')

    # Mojeek — only submit key pages
    print('\n--- Mojeek ---')
    results = submit_mojeek(to_submit[:5])
    for url, status in results:
        short = url.replace(BASE, '')
        print(f'  {short} → {status}')

    # Update tracking
    for url in to_submit:
        submitted_before[url] = now

    tracking['last_run'] = now
    save_tracking(tracking)

    print(f'\nDone. {len(to_submit)} URLs processed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
