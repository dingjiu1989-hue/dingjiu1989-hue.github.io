#!/usr/bin/env python3
"""
Syndicate articles to WordPress.com via the REST API.

Strategy:
- Post full articles on WordPress.com with prominent link back to original
- WordPress.com has DA ~94, passes link equity
- Republishing spreads content discovery

Auth:
  Get access token via: python3 scripts/wp_oauth2_setup.py
  Set env var: WP_ACCESS_TOKEN

  Or save to data/wp-tokens.json via the setup script.
"""
import json, os, sys, time, html as html_mod
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
TRACKING = ROOT / 'data' / 'wp-published.json'
EN_JSON = ROOT / 'en' / 'articles.json'
BASE = 'https://dingjiu1989-hue.github.io'
WP_API = 'https://public-api.wordpress.com/rest/v1.1'

# Try to get token from env var, then from local file
TOKEN = os.environ.get('WP_ACCESS_TOKEN')
if not TOKEN:
    token_file = ROOT / 'data' / 'wp-tokens.json'
    if token_file.exists():
        data = json.loads(token_file.read_text(encoding='utf-8'))
        TOKEN = data.get('access_token', '')

SITE_ID = os.environ.get('WP_SITE_ID')
if not SITE_ID:
    token_file = ROOT / 'data' / 'wp-tokens.json'
    if token_file.exists():
        data = json.loads(token_file.read_text(encoding='utf-8'))
        SITE_ID = data.get('blog_id', '')


def wp_request(method, path, data=None):
    from urllib.request import Request, urlopen
    from urllib.error import URLError

    url = f'{WP_API}{path}'
    body = None
    if data:
        # WP API v1.1 expects form-encoded data for posts/new
        import urllib.parse
        body = urllib.parse.urlencode(data).encode('utf-8')

    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'User-Agent': 'AI-Study-Room-Syndicator/1.0',
    }
    if body:
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

    req = Request(url, data=body, method=method, headers=headers)
    try:
        resp = urlopen(req, timeout=30)
        return json.loads(resp.read().decode('utf-8'))
    except URLError as e:
        body = b''
        if hasattr(e, 'read'):
            body = e.read()
        error_msg = f'HTTP {getattr(e, "code", 0)}: {body[:500].decode()}'
        print(f'  WP API error: {error_msg}')
        return None


def load_articles():
    if not EN_JSON.exists():
        print(f'ERROR: {EN_JSON} not found')
        sys.exit(1)

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


def md_to_html(md_text):
    """Convert markdown to HTML using the markdown library if available."""
    try:
        import markdown as md_lib
        return md_lib.markdown(md_text, extensions=['fenced_code', 'codehilite', 'tables'])
    except ImportError:
        # Simple fallback for basic markdown
        lines = md_text.split('\n')
        html_parts = []
        in_code = False
        for line in lines:
            if line.startswith('```'):
                if in_code:
                    html_parts.append('</code></pre>')
                    in_code = False
                else:
                    html_parts.append('<pre><code>')
                    in_code = True
            elif in_code:
                html_parts.append(html_mod.escape(line) + '\n')
            elif line.startswith('## '):
                html_parts.append(f'<h2>{line[3:]}</h2>')
            elif line.startswith('### '):
                html_parts.append(f'<h3>{line[4:]}</h3>')
            elif line.startswith('# '):
                html_parts.append(f'<h1>{line[2:]}</h1>')
            elif line.startswith('- '):
                html_parts.append(f'<li>{line[2:]}</li>')
            elif line.startswith('1. '):
                html_parts.append(f'<li>{line[3:]}</li>')
            elif line.strip() == '':
                html_parts.append('<br>')
            else:
                html_parts.append(f'<p>{line}</p>')
        return '\n'.join(html_parts)


def make_content(art, board_id):
    """Build WordPress.com article from markdown content."""
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

    # Convert to HTML
    body_html = md_to_html(md_content)

    # Wrap with attribution header and "read more" footer
    content_html = (
        f'<blockquote>'
        f'This article was originally published on <a href="{original_url}"><strong>AI Study Room</strong></a>. '
        f'Visit the original post for the complete version with working code examples and related articles.'
        f'</blockquote>\n\n'
        f'{body_html}\n\n'
        f'<hr>\n'
        f'<p><em>Read the full article with complete code examples at '
        f'<a href="{original_url}">{original_url}</a></em></p>'
    )
    return content_html


def get_tags(art):
    """Extract clean tags for WordPress."""
    tags = art.get('tags', [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(',') if t.strip()]
    return [t[:25] for t in tags[:10]]  # Max 10 tags


def syncable_tags(art):
    """Map board to WordPress category."""
    board = art.get('board_id', '')
    board_map = {
        'ai': 'Artificial Intelligence',
        'tech': 'Technology',
        'tools': 'Developer Tools',
        'sidehustle': 'Side Hustle',
        'compare': 'Comparison',
    }
    return board_map.get(board, 'Technology')


def create_post(title, content_html, tags, category, status='publish'):
    """Create a post on WordPress.com."""
    data = {
        'title': title[:200],
        'content': content_html,
        'tags': ','.join(tags),
        'categories': category,
        'status': status,
    }
    return wp_request('POST', f'/sites/{SITE_ID}/posts/new', data)


def get_sites():
    """List user's WordPress.com sites (to find the right site ID)."""
    return wp_request('GET', '/me/sites')


def main():
    global SITE_ID
    if not TOKEN:
        print('ERROR: Set WP_ACCESS_TOKEN env var')
        print('  Or run: python3 scripts/wp_oauth2_setup.py')
        return 1

    if not SITE_ID:
        print('WP_SITE_ID not set. Fetching your sites...')
        sites_resp = get_sites()
        if not sites_resp or 'sites' not in sites_resp:
            print('ERROR: Could not fetch sites. Check your token.')
            return 1
        sites = sites_resp['sites']
        if not sites:
            print('ERROR: No WordPress.com sites found.')
            return 1
        print('  Available sites:')
        for s in sites:
            print(f'    - {s.get("name", "?")} ({s.get("URL", "?")})')
            print(f'      ID: {s.get("ID", "?")}')
        # Use the first site
        SITE_ID = sites[0]['ID']
        name = sites[0].get('name', '?')
        url = sites[0].get('URL', '?')
        print(f'\nUsing: {name} ({url}) — Site ID: {SITE_ID}')

    articles = load_articles()
    tracking = load_tracking()
    shared_before = tracking.get('shared', {})

    to_share = [a for a in articles if not shared_before.get(a['slug'], {}).get('ok', False)]

    if not to_share:
        print('No new articles to share on WordPress.com.')
        return 0

    batch = to_share[:5]  # Max 5 per run
    print(f'Publishing {len(batch)} articles to WordPress.com...')

    now = datetime.now(timezone.utc).isoformat()
    posted = 0

    for article in batch:
        slug = article['slug']
        title = article['title']
        url = article['url']
        board = article['board_id']

        content_html = make_content(article, board)
        if not content_html:
            continue

        tags = get_tags(article)
        category = syncable_tags(article)

        print(f'\n  [WP] {title[:60]}...')

        result = create_post(title, content_html, tags, category)
        if result and 'ID' in result:
            post_url = result.get('URL', '')
            print(f'       ✓ Published: {post_url}')
            shared_before[slug] = {
                'title': title,
                'url': url,
                'wp_url': post_url,
                'shared_at': now,
                'ok': True,
            }
            posted += 1
        else:
            err = result.get('message', 'unknown error') if result else 'no response'
            print(f'       ✗ Failed: {err}')
            shared_before[slug] = {
                'title': title,
                'url': url,
                'shared_at': now,
                'ok': False,
                'error': str(err)[:100],
            }

        time.sleep(1)  # Be gentle

    tracking['shared'] = shared_before
    tracking['last_run'] = now
    save_tracking(tracking)

    print(f'\nDone. {posted} articles published to WordPress.com.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
