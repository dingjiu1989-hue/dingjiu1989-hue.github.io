#!/usr/bin/env python3
"""Generate JSON Feed (jsonfeed.org) with full article content for AI crawlers.

JSON Feed is preferred by many AI training pipelines and LLM-based readers.
This reads article bodies directly, providing full content_text + content_html.

Generates: /en/feed.json (English) and /feed.json (Chinese)
"""

import json, re, sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
EN_ARTICLES = ROOT / 'en' / 'articles.json'
CN_ARTICLES = ROOT / 'articles.json'
SITE_URL = 'https://aidev.fit'


def get_body(slug, board_id, lang="en"):
    """Read article body from md file, fall back to 'Content coming soon.'"""
    md_path = ROOT / 'md' / lang / board_id / f'{slug}.md'
    if md_path.exists():
        content = md_path.read_text(encoding='utf-8')
        if content.startswith('---'):
            end = content.find('---', 3)
            if end > 0:
                content = content[end + 3:].strip()
        try:
            import markdown as md_lib
            html = md_lib.markdown(content, extensions=['fenced_code', 'codehilite', 'tables'])
        except ImportError:
            html = f'<pre>{content}</pre>'
        if html.strip():
            return html
    return '<p>Content coming soon.</p>'


def build_feed(articles_path, title, language, output_path, feed_url_slug, url_prefix='en'):
    """Build a JSON Feed v1.1 file with full article content."""
    data = json.loads(articles_path.read_text(encoding='utf-8'))

    items = []
    for board in data['boards']:
        for art in board['posts']:
            md_lang = 'zh' if language == 'zh-CN' else 'en'
            body_html = get_body(art['slug'], board['id'], md_lang)
            body_text = re.sub(r'<[^>]+>', ' ', body_html)
            body_text = re.sub(r'\s+', ' ', body_text).strip()

            # Strip leading H1/H2 markdown heading + title duplicate from body
            body_text = re.sub(r'^#+\s*', '', body_text)
            body_text = re.sub(r'^\s*' + re.escape(art['title']) + r'\s*', '', body_text, count=1)
            body_html_nodup = re.sub(
                r'<h[12][^>]*>' + re.escape(art['title']) + r'</h[12]>', '', body_html, count=1
            )

            if url_prefix:
                art_url = f"{SITE_URL}/{url_prefix}/{board['id']}/{art['slug']}.html"
            else:
                art_url = f"{SITE_URL}/{board['id']}/{art['slug']}.html"
            entry = {
                'id': art_url,
                'url': art_url,
                'title': art['title'],
                'content_text': body_text,
                'content_html': body_html_nodup.strip(),
                'summary': art.get('description', ''),
                'date_published': art['date'],
                'date_modified': art.get('lastActive', art['date']),
                'tags': art.get('tags', []),
            }
            items.append(entry)

    # Sort by date descending
    items.sort(key=lambda x: x.get('date_published', ''), reverse=True)
    # Limit to 200 most recent for feed file size
    items = items[:200]

    feed = {
        'version': 'https://jsonfeed.org/version/1.1',
        'title': title,
        'home_page_url': f'{SITE_URL}/en/' if language == 'en' else f'{SITE_URL}/',
        'feed_url': f'{SITE_URL}/{feed_url_slug}',
        'description': f'{title} — developer tutorials, tool comparisons, and guides',
        'language': language,
        'items': items,
    }

    output_path.write_text(
        json.dumps(feed, indent=2, ensure_ascii=False),
        encoding='utf-8'
    )
    return len(items)


def main():
    results = {}

    if EN_ARTICLES.exists():
        n = build_feed(EN_ARTICLES, 'AI Study Room (English)', 'en',
                       ROOT / 'en' / 'feed.json', 'en/feed.json')
        results['en/feed.json'] = n

    if CN_ARTICLES.exists():
        n = build_feed(CN_ARTICLES, 'AI自习室 (中文)', 'zh-CN',
                       ROOT / 'feed.json', 'feed.json', url_prefix='')
        results['feed.json'] = n

    print('JSON Feed generation complete (full content):')
    for path, count in results.items():
        # Show file size
        fsize = (ROOT / path).stat().st_size
        print(f'  {path}: {count} items, {fsize//1024} KB')
    return 0


if __name__ == '__main__':
    sys.exit(main())
