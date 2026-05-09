#!/usr/bin/env python3
"""Syndicate English articles to Medium with canonical URLs.

Medium (DA 95+) supports canonical URLs — published articles point back to
our main site, passing full SEO value.

Setup:
  1. Get integration token: https://medium.com/me/settings/security
     Scroll to "Integration tokens", create one.
  2. Set env: MEDIUM_TOKEN=<your-token>
  3. Run: python3 scripts/syndicate_medium.py

API docs: https://github.com/Medium/medium-api-docs
"""

import json, os, re, sys, time
from pathlib import Path
from datetime import datetime, timezone
import _ssl_compat  # noqa
from urllib.request import Request, urlopen
from urllib.error import URLError

ROOT = Path(__file__).resolve().parent.parent
EN_ARTICLES = ROOT / 'en' / 'articles.json'
TRACKING = ROOT / 'data' / 'medium-published.json'
MEDIUM_API = 'https://api.medium.com/v1'

SITE = 'https://dingjiu1989-hue.github.io'

# Content boards to syndicate (all English boards)
BOARDS = ['tech', 'sidehustle', 'tools', 'ai', 'compare']

# Max articles per run (be respectful to Medium's API)
MAX_PER_RUN = 10


def get_token():
    token = os.environ.get('MEDIUM_TOKEN', '')
    if not token:
        print('ERROR: Set MEDIUM_TOKEN env var.')
        print('Get one at: https://medium.com/me/settings/security')
        sys.exit(1)
    return token


def api(path, token, body=None):
    url = f'{MEDIUM_API}{path}'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    data = json.dumps(body).encode('utf-8') if body else None
    req = Request(url, data=data, headers=headers, method='POST' if body else 'GET')
    try:
        resp = urlopen(req, timeout=30)
        return json.loads(resp.read().decode('utf-8'))
    except URLError as e:
        err_body = e.read().decode('utf-8') if hasattr(e, 'read') else str(e)
        print(f'  API error: {e.code} — {err_body[:300]}')
        return None


def get_user_id(token):
    """Get the authenticated user's ID."""
    result = api('/me', token)
    if result:
        uid = result.get('data', {}).get('id', '')
        print(f'  User ID: {uid}')
        return uid
    return None


def load_tracking():
    if TRACKING.exists():
        return json.loads(TRACKING.read_text(encoding='utf-8'))
    return {'published': {}, 'last_run': None}


def save_tracking(data):
    TRACKING.parent.mkdir(exist_ok=True)
    TRACKING.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')


def load_en_articles():
    """Load all English articles from articles.json."""
    data = json.loads(EN_ARTICLES.read_text(encoding='utf-8'))
    all_posts = []
    for board in data.get('boards', []):
        board_name = board.get('name', '')
        if board_name not in BOARDS:
            continue
        for post in board.get('posts', []):
            post['_board'] = board_name
            all_posts.append(post)
    return all_posts


def extract_markdown_body(post):
    """Read the article's .md file and return content with absolute URLs."""
    board = post['_board']
    slug = post['slug']
    md_path = ROOT / 'md' / 'en' / board / f'{slug}.md'

    if not md_path.exists():
        return None

    content = md_path.read_text(encoding='utf-8')

    # Convert relative links to absolute
    content = re.sub(
        r'\]\((/[^)]+)\)',
        rf']({SITE}\1)',
        content
    )

    return content


def build_canonical_url(post):
    board = post['_board']
    slug = post['slug']
    return f'{SITE}/en/{board}/{slug}.html'


def publish_to_medium(user_id, post, token):
    """Publish a single article to Medium."""
    md_body = extract_markdown_body(post)
    if not md_body:
        print(f'  SKIP (no .md file): {post["slug"]}')
        return None

    canonical = build_canonical_url(post)
    tags = [t.lower().replace(' ', '-') for t in post.get('tags', [])[:5]]

    body = {
        'title': post['title'],
        'contentFormat': 'markdown',
        'content': md_body,
        'canonicalUrl': canonical,
        'publishStatus': 'public',
        'tags': tags,
    }

    result = api(f'/users/{user_id}/posts', token, body)
    if result:
        post_data = result.get('data', {})
        return {
            'id': post_data.get('id'),
            'url': post_data.get('url'),
            'canonical': canonical,
            'published_at': post_data.get('publishedAt'),
        }
    return None


def main():
    token = get_token()
    print('Medium Syndication')
    print('==================')
    print()

    user_id = get_user_id(token)
    if not user_id:
        print('ERROR: Could not get user ID. Check your MEDIUM_TOKEN.')
        return 1

    tracking = load_tracking()
    published = tracking['published']
    articles = load_en_articles()
    print(f'Loaded {len(articles)} English articles from {len(BOARDS)} boards')

    # Find unpublished articles
    to_publish = []
    for post in articles:
        slug = post['slug']
        if slug not in published:
            to_publish.append(post)

    if not to_publish:
        print('All articles already published to Medium!')
        return 0

    print(f'Unpublished: {len(to_publish)}. Will publish up to {MAX_PER_RUN} this run.')
    print()

    count = 0
    for post in to_publish[:MAX_PER_RUN]:
        slug = post['slug']
        title = post.get('title', slug)
        print(f'  Publishing: {title[:80]}')
        result = publish_to_medium(user_id, post, token)

        if result:
            published[slug] = result
            print(f'    OK: {result["url"]}')
            print(f'    Canonical: {result["canonical"]}')
            count += 1
        else:
            print(f'    FAILED')

        # Rate limit: 1 request per 2 seconds
        if count < min(MAX_PER_RUN, len(to_publish)):
            time.sleep(2)

    tracking['last_run'] = datetime.now(timezone.utc).isoformat()
    save_tracking(tracking)

    print()
    print(f'Done. Published {count} articles this run.')
    print(f'Total on Medium: {len(published)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
