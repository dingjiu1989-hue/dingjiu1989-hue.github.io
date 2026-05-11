#!/usr/bin/env python3
"""Share new articles to Twitter/X and LinkedIn.

Two ways to authenticate with X (tried in order):
  1. OAuth 2.0 PKCE with refresh token (preferred)
     Env vars: X_CLIENT_ID, X_CLIENT_SECRET, X_REFRESH_TOKEN
  2. OAuth 1.0a (legacy, may be credits-depleted on free tier)
     Env vars: X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET

  LinkedIn:
    - LINKEDIN_ACCESS_TOKEN

To get OAuth 2.0 refresh token:
  python3 scripts/x_oauth2_setup.py

Tracks published posts in data/social-shared.json.
"""

import base64, json, os, sys, re, urllib.parse
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


def x_basic_auth(client_id, client_secret):
    raw = f'{client_id}:{client_secret}'
    return 'Basic ' + base64.b64encode(raw.encode()).decode()


def x_refresh_access_token(client_id, client_secret, refresh_token):
    """Use a refresh token to get a fresh OAuth 2.0 access token."""
    data = urllib.parse.urlencode({
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
    }).encode()
    req = Request('https://api.twitter.com/2/oauth2/token', data=data,
                  headers={
                      'Content-Type': 'application/x-www-form-urlencoded',
                      'Authorization': x_basic_auth(client_id, client_secret),
                  })
    try:
        resp = urlopen(req, timeout=15)
        tokens = json.loads(resp.read().decode())
        return tokens.get('access_token', '')
    except URLError as e:
        body = e.read().decode() if hasattr(e, 'read') else ''
        raise RuntimeError(f'OAuth2 refresh failed: {e.code} {body[:200]}')


def post_to_x_oauth2(client_id, client_secret, refresh_token, text, url):
    """Post to X using OAuth 2.0 with refresh token (no credit depletion on some accounts)."""
    from urllib.request import Request, urlopen

    # Get a fresh access token
    access_token = x_refresh_access_token(client_id, client_secret, refresh_token)

    # Post the tweet
    tweet = f'{text}\n\n{url}'
    body = json.dumps({'text': tweet}).encode()
    req = Request('https://api.twitter.com/2/tweets', data=body,
                  headers={
                      'Authorization': f'Bearer {access_token}',
                      'Content-Type': 'application/json',
                  })
    try:
        resp = urlopen(req, timeout=15)
        result = json.loads(resp.read().decode())
        return {'ok': True, 'id': result.get('data', {}).get('id', '')}
    except URLError as e:
        code = getattr(e, 'code', 0)
        body = e.read().decode() if hasattr(e, 'read') else ''
        return {'ok': False, 'error': f'{code}: {body[:200]}'}


def post_to_x(api_key, api_secret, access_token, access_secret, text, url):
    """Post to Twitter/X using v2 API with OAuth 1.0a."""
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

    # X (Twitter) - prefer OAuth 2.0, fallback to OAuth 1.0a
    x_client_id = os.environ.get('X_CLIENT_ID')
    x_client_secret = os.environ.get('X_CLIENT_SECRET')
    x_refresh_token = os.environ.get('X_REFRESH_TOKEN')
    x_oauth2_available = all([x_client_id, x_client_secret, x_refresh_token])

    x_key = os.environ.get('X_API_KEY')
    x_secret = os.environ.get('X_API_SECRET')
    x_token = os.environ.get('X_ACCESS_TOKEN')
    x_token_secret = os.environ.get('X_ACCESS_SECRET')
    x_oauth1_available = all([x_key, x_secret, x_token, x_token_secret])

    x_available = x_oauth2_available or x_oauth1_available

    # LinkedIn
    li_token = os.environ.get('LINKEDIN_ACCESS_TOKEN')
    li_available = bool(li_token)

    if not x_available and not li_available:
        print('No API credentials configured.')
        print('  For OAuth 2.0: Set X_CLIENT_ID, X_CLIENT_SECRET, X_REFRESH_TOKEN')
        print('  For OAuth 1.0a: Set X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET')
        print('  For LinkedIn: Set LINKEDIN_ACCESS_TOKEN')
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
            if x_oauth2_available:
                r = post_to_x_oauth2(x_client_id, x_client_secret, x_refresh_token, share_text, url)
            else:
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
