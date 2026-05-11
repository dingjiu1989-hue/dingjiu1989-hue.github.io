#!/usr/bin/env python3
"""Share new articles to X/Twitter via Buffer API.

Buffer API: https://api.buffer.com (GraphQL)

Requirements:
  - BUFFER_API_KEY env var / GitHub Secret
  - A connected Twitter channel in Buffer

Flow:
  1. Fetch new EN articles
  2. Check tracking for already-shared
  3. Post to Buffer queue (addToQueue mode, up to 3 per run)
  4. Update tracking file

Tracks published posts in data/buffer-shared.json.
"""

import json, os, sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
TRACKING = ROOT / 'data' / 'buffer-shared.json'
EN_JSON = ROOT / 'en' / 'articles.json'
BASE = 'https://dingjiu1989-hue.github.io'

# Buffer config
BUFFER_KEY = os.environ.get('BUFFER_API_KEY', '')
CHANNEL_ID = '6a01c814090476fb9909b6e6'  # X/Twitter channel
BUFFER_URL = 'https://api.buffer.com'


def buffer_graphql(query, variables=None):
    """Send a GraphQL request to Buffer API."""
    from urllib.request import Request, urlopen
    from urllib.error import URLError

    body = json.dumps({'query': query, 'variables': variables or {}}).encode()
    req = Request(BUFFER_URL, data=body, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {BUFFER_KEY}',
    })
    try:
        resp = urlopen(req, timeout=15)
        return json.loads(resp.read().decode())
    except URLError as e:
        body = e.read().decode() if hasattr(e, 'read') else ''
        return {'errors': [{'message': f'HTTP {e.code}: {body[:200]}'}]}


def create_post(text, url, mode='addToQueue'):
    """Create a post on Buffer for the X channel."""
    post_text = f'{text}\n{url}'

    mutation = '''
    mutation CreatePost($text: String!, $channelId: String!, $mode: PostMode!) {
      createPost(input: {
        text: $text,
        channelId: $channelId,
        schedulingType: automatic,
        mode: $mode
      }) {
        ... on PostActionSuccess {
          post { id text }
        }
        ... on MutationError { message }
      }
    }
    '''
    variables = {
        'text': post_text,
        'channelId': CHANNEL_ID,
        'mode': mode,
    }
    result = buffer_graphql(mutation, variables)
    if 'errors' in result:
        msg = result['errors'][0].get('message', str(result['errors']))
        return {'ok': False, 'error': msg}

    data = result.get('data', {}).get('createPost', {})
    if 'post' in data:
        return {'ok': True, 'id': data['post'].get('id', '')}

    # MutationError
    err_msg = data.get('message', str(result))
    return {'ok': False, 'error': err_msg}


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


def main():
    if not BUFFER_KEY:
        print('ERROR: Set BUFFER_API_KEY env var')
        return 1

    mode = sys.argv[1] if len(sys.argv) > 1 else 'new'
    articles = load_articles()
    tracking = load_tracking()
    shared_before = tracking.get('shared', {})

    if mode == 'all':
        to_share = articles
    else:
        to_share = [a for a in articles if a['slug'] not in shared_before]

    if not to_share:
        print('No new articles to share via Buffer.')
        return 0

    print(f'New articles to share via Buffer: {len(to_share)}')
    now = datetime.now(timezone.utc).isoformat()
    posted = 0

    for article in to_share[:3]:  # Max 3 per run
        slug = article['slug']
        title = article['title']
        url = article['url']
        desc = article.get('description', '')
        board = article['board_id']

        # Build tweet text: title (max 240 chars) + hashtags
        tags = get_tags(article)
        tag_str = ' ' + ' '.join(tags) if tags else ''
        tweet_text = f'{title[:240 - len(tag_str)]}{tag_str}'

        print(f'\n  [Buffer] {title[:60]}...')
        r = create_post(tweet_text, url)
        if r.get('ok'):
            print(f'       ✓ Queued (id: {r.get("id", "?")})')
        else:
            print(f'       ✗ {r.get("error", "unknown")[:100]}')

        shared_before[slug] = {
            'title': title,
            'url': url,
            'shared_at': now,
            'platform': 'buffer',
            'ok': r.get('ok', False),
        }
        posted += 1

    tracking['shared'] = shared_before
    tracking['last_run'] = now
    save_tracking(tracking)

    print(f'\nDone. {posted} articles queued via Buffer.')
    return 0


def get_tags(article):
    """Generate hashtags from article tags/board."""
    tags = article.get('tags', [])
    board = article.get('board_id', '')
    result = []

    # Add board-based hashtag
    board_map = {'ai': '#AI', 'tech': '#Tech', 'tools': '#DevTools', 'sidehustle': '#SideHustle'}
    if board in board_map:
        result.append(board_map[board])

    # Add tag-based hashtags (max 2)
    for t in tags[:2]:
        tag = t.replace(' ', '').replace('-', '')
        if tag.lower() not in ['chrome', 'git', 'ai', 'api', 'aws', 'css', 'html']:
            tag = '#' + tag[:20]
        else:
            tag = '#' + tag
        if tag not in result:
            result.append(tag)

    return result[:3]  # Max 3 hashtags


if __name__ == '__main__':
    sys.exit(main())
