#!/usr/bin/env python3
"""Submit URLs to IndexNow (Bing, Yandex, Seznam) for instant crawling.

IndexNow is supported by Bing, Yandex, Seznam, and Naver.
Bing's index feeds ChatGPT, DuckDuckGo, Copilot, and other AI search products.

Key file: https://dingjiu1989-hue.github.io/KEY.txt
API: POST https://api.indexnow.org/indexnow
"""

import json, re, sys, os
from pathlib import Path
from datetime import datetime, timezone
import _ssl_compat  # noqa
from urllib.request import Request, urlopen
from urllib.error import URLError
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
SITEMAP = ROOT / 'sitemap.xml'
TRACKING = ROOT / 'data' / 'indexnow-submitted.json'
KEY = 'bca1280e3258b853e5cc15ec3151fb9f'
HOST = 'dingjiu1989-hue.github.io'

ENDPOINTS = [
    'https://api.indexnow.org/indexnow',
    'https://www.bing.com/indexnow',
    'https://yandex.com/indexnow',
]


def load_sitemap_urls():
    content = SITEMAP.read_text(encoding='utf-8')
    urls = re.findall(r'<loc>([^<]+)</loc>', content)
    return urls


def load_tracking():
    if TRACKING.exists():
        return json.loads(TRACKING.read_text(encoding='utf-8'))
    return {'submitted': {}, 'last_run': None}


def save_tracking(data):
    TRACKING.parent.mkdir(exist_ok=True)
    TRACKING.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')


def submit_urls(urls, endpoint):
    """Submit up to 10,000 URLs per request (IndexNow limit)."""
    body = json.dumps({
        'host': HOST,
        'key': KEY,
        'keyLocation': f'https://{HOST}/{KEY}.txt',
        'urlList': urls,
    }).encode('utf-8')

    req = Request(endpoint, data=body, headers={
        'Content-Type': 'application/json; charset=utf-8',
    })

    try:
        resp = urlopen(req, timeout=30)
        return resp.status, resp.read().decode('utf-8')
    except URLError as e:
        code = getattr(e, 'code', 0)
        # IndexNow returns 202 Accepted — treat as success
        if code == 202:
            return 200, 'Accepted'
        return code, str(e.reason)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'diff'

    all_urls = load_sitemap_urls()
    tracking = load_tracking()
    submitted_before = tracking['submitted']

    if mode == 'all':
        to_submit = [u for u in all_urls if u not in submitted_before]
    else:
        # Diff mode: submit URLs never submitted before
        to_submit = [u for u in all_urls if u not in submitted_before]

    if not to_submit:
        print('No new URLs to submit. All sitemap URLs already submitted.')
        return 0

    print(f'Submitting {len(to_submit)} URLs to IndexNow...')

    # Submit in batches of 5000 (generous margin under 10K limit)
    batch_size = 5000
    success_count = 0
    now = datetime.now(timezone.utc).isoformat()

    for i in range(0, len(to_submit), batch_size):
        batch = to_submit[i:i + batch_size]
        for ep in ENDPOINTS:
            status, body = submit_urls(batch, ep)
            ep_name = urlparse(ep).netloc
            if status == 200:
                print(f'  {ep_name}: OK ({len(batch)} URLs)')
                success_count += 1
            else:
                print(f'  {ep_name}: FAIL ({status}) — {body[:200]}')

        # Track these URLs as submitted
        for u in batch:
            submitted_before[u] = now

    tracking['last_run'] = now
    save_tracking(tracking)

    print(f'\nDone. {len(to_submit)} URLs submitted, tracking updated.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
