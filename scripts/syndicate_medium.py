#!/usr/bin/env python3
"""
Syndicate articles to Medium via their API.

Strategy:
- Post full articles on Medium with canonical URL pointing back to our site
- Medium has DA ~95 and huge built-in audience
- canonicalUrl tells search engines our site is the original source
- Medium appears prominently in Google search results

Auth:
  Get Medium Integration Token at: https://medium.com/me/settings/security
  Set env var: MEDIUM_TOKEN

Note: The Medium API was officially deprecated in 2023 but still functions.
Alternative: Use RSS Import at https://medium.com/me/settings/rss
"""
import json, os, sys, time
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
TRACKING = ROOT / 'data' / 'medium-published.json'
EN_JSON = ROOT / 'en' / 'articles.json'
BASE = 'https://aidev.fit'
MEDIUM_API = 'https://api.medium.com/v1'

TOKEN = os.environ.get('MEDIUM_TOKEN')
if not TOKEN:
    print('ERROR: Set MEDIUM_TOKEN env var')
    print('Get your token at: https://medium.com/me/settings/security')
    sys.exit(1)


def medium_request(method, path, data=None):
    from urllib.request import Request, urlopen
    from urllib.error import URLError

    url = f'{MEDIUM_API}{path}'
    body = json.dumps(data).encode('utf-8') if data else None
    req = Request(url, data=body, method=method, headers={
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'AI-Study-Room-Syndicator/1.0',
    })
    try:
        resp = urlopen(req, timeout=30)
        return json.loads(resp.read().decode('utf-8'))
    except URLError as e:
        body = b''
        if hasattr(e, 'read'):
            body = e.read()
        error_msg = f'HTTP {getattr(e, "code", 0)}: {body[:300].decode()}'
        print(f'  Medium API error: {error_msg}')
        return None


def get_me():
    """Get Medium user info."""
    result = medium_request('GET', '/me')
    if result and 'data' in result:
        return result['data']
    return None


def create_post(author_id, title, content, tags, canonical_url,
                content_format='markdown', publish_status='public'):
    """Create a post on Medium."""
    data = {
        'title': title[:100],  # Medium ignores titles longer than 100
        'contentFormat': content_format,
        'content': content,
        'canonicalUrl': canonical_url,
        'publishStatus': publish_status,
        'tags': tags[:3],  # Medium only uses first 3 tags
        'notifyFollowers': True,
    }
    result = medium_request('POST', f'/users/{author_id}/posts', data)
    if result and 'data' in result:
        return result['data']
    return None


def load_articles():
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


def parse_tags(tags_val):
    if isinstance(tags_val, list):
        raw = tags_val
    elif isinstance(tags_val, str):
        raw = [t.strip() for t in tags_val.split(',') if t.strip()]
    else:
        return []
    clean = []
    for t in raw:
        t = t.strip().lower()
        if t and len(t) <= 25:
            clean.append(t)
    return clean[:3]


def make_content(art, board_id):
    """Build Medium article body from markdown content."""
    md_path = ROOT / 'md' / 'en' / board_id / f'{art["slug"]}.md'
    if not md_path.exists():
        print(f'  Markdown file not found: {md_path}')
        return None

    md_content = md_path.read_text(encoding='utf-8')
    # Remove frontmatter
    if md_content.startswith('---'):
        end = md_content.find('---', 3)
        if end > 0:
            md_content = md_content[end + 3:].strip()

    original_url = f'{BASE}/en/{board_id}/{art["slug"]}.html'
    tags = parse_tags(art.get('tags', ''))
    home_url = f'{BASE}/en/?utm_source=medium&utm_medium=syndication&utm_campaign=ai-daily-digest'
    track_url = original_url + '?utm_source=medium&utm_medium=syndication&utm_campaign=ai-daily-digest'

    # Attribution header — canonical source notice
    preamble = (
        f'> *Originally published on [AI Study Room]({track_url}).*\n'
        f'> *Check the original for the most up-to-date version and related articles.*\n\n'
    )

    # Signature footer — site branding + tracking link
    sig = (
        f'\n\n---\n\n'
        f'*This post is part of the [AI Study Room]({home_url}) — '
        f'a curated library of 900+ articles on AI tools, programming, '
        f'and developer resources. '
        f'Explore more at [aidev.fit]({home_url}).*\n'
    )
    return preamble + md_content + sig


def main():
    # Verify auth and get user info first
    print('Authenticating with Medium...')
    me = get_me()
    if not me:
        print('ERROR: Could not authenticate. Check your MEDIUM_TOKEN.')
        print('Get a token at: https://medium.com/me/settings/security')
        return 1

    username = me.get('username', 'unknown')
    author_id = me.get('id', '')
    print(f'Authenticated as: @{username} (id: {author_id[:12]}...)')

    articles = load_articles()
    tracking = load_tracking()
    shared_before = tracking.get('shared', {})

    # Filter out already-shared articles
    to_share = [a for a in articles if not shared_before.get(a['slug'], {}).get('ok', False)]

    if not to_share:
        print('No new articles to share on Medium.')
        return 0

    # Limit per run (Medium has no strict rate limit, but be gentle)
    batch = to_share[:5]
    print(f'Publishing {len(batch)} articles to Medium...')

    now = datetime.now(timezone.utc).isoformat()
    posted = 0

    for article in batch:
        slug = article['slug']
        title = article['title']
        url = article['url']
        board = article['board_id']
        tags = parse_tags(article.get('tags', ''))

        content = make_content(article, board)
        if not content:
            continue

        print(f'\n  [Medium] {title[:60]}...')

        result = create_post(author_id, title, content, tags, url)
        if result:
            post_url = result.get('url', '')
            print(f'       ✓ Published: {post_url}')
            shared_before[slug] = {
                'title': title,
                'url': url,
                'medium_url': post_url,
                'shared_at': now,
                'ok': True,
            }
            posted += 1
        else:
            print(f'       ✗ Failed')
            shared_before[slug] = {
                'title': title,
                'url': url,
                'shared_at': now,
                'ok': False,
            }

        # Be gentle with rate limits
        time.sleep(2)

    tracking['shared'] = shared_before
    tracking['last_run'] = now
    save_tracking(tracking)

    print(f'\nDone. {posted} articles published to Medium.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
