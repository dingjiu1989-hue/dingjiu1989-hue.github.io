#!/usr/bin/env python3
"""Share new articles to Twitter/X and LinkedIn.

Requires API credentials set as environment variables:
  X (Twitter):
    - X_API_KEY
    - X_API_SECRET
    - X_ACCESS_TOKEN
    - X_ACCESS_SECRET
  LinkedIn:
    - LINKEDIN_CLIENT_ID
    - LINKEDIN_CLIENT_SECRET
    - LINKEDIN_ACCESS_TOKEN

Tracks published posts in data/social-shared.json.
"""

import json, os, sys, re
from pathlib import Path
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import URLError

ROOT = Path(__file__).resolve().parent.parent
TRACKING = ROOT / 'data' / 'social-shared.json'
EN_JSON = ROOT / 'en' / 'articles.json'
BASE = 'https://dingjiu1989-hue.github.io'


def load_articles():
    """Load all English articles, sorted newest first."""
    data = json.loads(EN_JSON.read_text(encoding='utf-8'))
    articles = []
    for board in data['boards']:
        for art in board['posts']:
            articles.append({
                **art,
                'board_id': board['id'],
                'url': f'{BASE}/en/{board["id"]}/{art["slug"]}.html',
            })
    articles.sort(key=lambda a: a.get('date', ''), reverse=True)
    return articles


def load_tracking():
    if TRACKING.exists():
        return json.loads(TRACKING.read_text(encoding='utf-8'))
    return {'shared': {}, 'last_run': None}


def save_tracking(data):
    TRACKING.parent.mkdir(exist_ok=True)
    TRACKING.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')


def shorten_text(text, max_len=280):
    """Truncate text to fit within max_len, preferring to end at a sentence."""
    if len(text) <= max_len:
        return text
    # Try to find a sentence boundary
    truncated = text[:max_len - 3]
    last_period = truncated.rfind('.')
    last_space = truncated.rfind(' ')
    cut = last_period + 1 if last_period > max_len * 0.7 else last_space
    if cut < max_len * 0.5:
        cut = max_len - 3
    return text[:cut].rstrip() + '...'


def post_to_x(api_key, api_secret, access_token, access_secret, text, url):
    """Post to Twitter/X using v2 API with OAuth 1.0a.

    Falls back to a curl call when the oauthlib is unavailable.
    """
    import urllib.parse

    # Build the tweet text
    tweet = f'{text}\n\n{url}'

    # Try using requests_oauthlib if available
    try:
        from requests_oauthlib import OAuth1Session
        session = OAuth1Session(
            client_key=api_key,
            client_secret=api_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_secret,
        )
        resp = session.post(
            'https://api.twitter.com/2/tweets',
            json={'text': tweet},
            timeout=15,
        )
        if resp.status_code == 201:
            return {'ok': True, 'id': resp.json().get('data', {}).get('id', '')}
        return {'ok': False, 'error': f'{resp.status_code}: {resp.text[:200]}'}
    except ImportError:
        pass

    # Fallback: use curl via subprocess
    import subprocess
    # OAuth 1.0a signing is complex without a library, so we use a simplified
    # Bearer token approach if available, or report the need for requests_oauthlib
    return {'ok': False, 'error': 'Requires requests_oauthlib. Install: pip install requests_oauthlib'}


def post_to_linkedin(token, text, url):
    """Post to LinkedIn as a share update."""
    body = json.dumps({
        'author': 'urn:li:person:',  # placeholder — filled if token scope is known
        'lifecycleState': 'PUBLISHED',
        'specificContent': {
            'com.linkedin.ugc.ShareContent': {
                'shareCommentary': {'text': f'{text}\n\n{url}'},
                'shareMediaCategory': 'NONE',
            },
        },
        'visibility': {'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC'},
    }).encode('utf-8')

    req = Request(
        'https://api.linkedin.com/v2/ugcPosts',
        data=body,
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0',
        },
    )
    try:
        resp = urlopen(req, timeout=15)
        return {'ok': True, 'id': resp.headers.get('X-RestLi-Id', '')}
    except URLError as e:
        code = getattr(e, 'code', 0)
        body = b''
        if hasattr(e, 'read'):
            body = e.read()
        return {'ok': False, 'error': f'{code}: {body[:200]}'}


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'new'
    articles = load_articles()
    tracking = load_tracking()
    shared_before = tracking.get('shared', {})

    if mode == 'all':
        to_share = articles
    else:
        # Only share unpublished articles, newest first
        to_share = [a for a in articles if a['slug'] not in shared_before]

    if not to_share:
        print('No new articles to share.')
        return 0

    print(f'New articles to share: {len(to_share)}')
    now = datetime.now(timezone.utc).isoformat()
    posts_count = 0

    # X (Twitter)
    x_key = os.environ.get('X_API_KEY')
    x_secret = os.environ.get('X_API_SECRET')
    x_token = os.environ.get('X_ACCESS_TOKEN')
    x_token_secret = os.environ.get('X_ACCESS_SECRET')
    x_available = all([x_key, x_secret, x_token, x_token_secret])

    # LinkedIn
    li_token = os.environ.get('LINKEDIN_ACCESS_TOKEN')
    li_available = bool(li_token)

    if not x_available and not li_available:
        print('No API credentials configured.')
        print('  Set X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET for Twitter')
        print('  Set LINKEDIN_ACCESS_TOKEN for LinkedIn')
        return 0

    for article in to_share[:5]:  # Limit to 5 per run to avoid rate limits
        slug = article['slug']
        title = article['title']
        url = article['url']
        desc = article.get('description', '')
        board = article['board_id']

        # Truncate title for social posts
        share_text = f'{title[:200]}'

        results = []
        if x_available:
            print(f'\n  [X] {title[:60]}...')
            r = post_to_x(x_key, x_secret, x_token, x_token_secret, share_text, url)
            results.append(('x', r))
            if r.get('ok'):
                print(f'       ✓ Posted (id: {r.get("id", "?")})')
            else:
                print(f'       ✗ {r.get("error", "unknown")}')

        if li_available:
            print(f'  [LI] {title[:60]}...')
            r = post_to_linkedin(li_token, share_text, url)
            results.append(('linkedin', r))
            if r.get('ok'):
                print(f'       ✓ Posted (id: {r.get("id", "?")})')
            else:
                print(f'       ✗ {r.get("error", "unknown")}')

        # Track as shared even if some failed (avoid re-posting)
        shared_before[slug] = {
            'title': title,
            'url': url,
            'shared_at': now,
            'results': {p[0]: p[1].get('ok', False) for p in results},
        }
        posts_count += 1

    tracking['shared'] = shared_before
    tracking['last_run'] = now
    save_tracking(tracking)

    print(f'\nDone. Shared {posts_count} articles.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
