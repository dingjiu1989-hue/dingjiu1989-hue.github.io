#!/usr/bin/env python3
"""Generate Google News sitemap (articles from last 48 hours only).

Output: /en/news-sitemap.xml
Regenerate daily to keep within the 48-hour window.
"""
import json
from pathlib import Path
from datetime import datetime, timedelta

ROOT = Path(__file__).resolve().parent.parent
EN_JSON = ROOT / 'en' / 'articles.json'
CN_JSON = ROOT / 'articles.json'
OUTPUT = ROOT / 'en' / 'news-sitemap.xml'
BASE = 'https://aidev.fit'
TODAY = datetime.now()
CUTOFF = (TODAY - timedelta(hours=48)).strftime('%Y-%m-%d')

def gen_news_sitemap():
    data = json.loads(EN_JSON.read_text(encoding='utf-8'))
    urls = []
    for board in data['boards']:
        for art in board.get('posts', []):
            pub_date = art.get('date', '')
            if pub_date < CUTOFF:
                continue
            slug = art['slug']
            loc = f'{BASE}/en/{board["id"]}/{slug}.html'
            # Map board_id to Google News genre
            genres = {
                'daily': 'PressRelease',
                'ai': 'Blog',
                'tech': 'ProductAnnouncement',
                'compare': 'ProductAnnouncement',
                'sidehustle': 'Blog',
                'tools': 'ProductAnnouncement',
                'security': 'Blog',
                'database': 'Blog',
                'architecture': 'Blog',
            }
            genre = genres.get(board['id'], 'Blog')
            urls.append({
                'loc': loc,
                'pub_date': pub_date,
                'title': art['title'],
                'genre': genre,
                'keywords': ', '.join(art.get('tags', [])),
            })

    if not urls:
        print(f'  No articles found since {CUTOFF}. Writing empty sitemap.')
        # Still write an empty sitemap to prevent 404s
        OUTPUT.write_text('''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">
</urlset>''', encoding='utf-8')
        return

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">',
    ]
    for u in sorted(urls, key=lambda x: x['pub_date'], reverse=True):
        lines.append('  <url>')
        lines.append(f'    <loc>{u["loc"]}</loc>')
        lines.append('    <news:news>')
        lines.append('      <news:publication>')
        lines.append('        <news:name>AI Study Room</news:name>')
        lines.append('        <news:language>en</news:language>')
        lines.append('      </news:publication>')
        lines.append(f'      <news:publication_date>{u["pub_date"]}T12:00:00Z</news:publication_date>')
        lines.append(f'      <news:title><![CDATA[{u["title"]}]]></news:title>')
        lines.append(f'      <news:genres>{u["genre"]}</news:genres>')
        if u['keywords']:
            lines.append(f'      <news:keywords>{u["keywords"]}</news:keywords>')
        lines.append('    </news:news>')
        lines.append('  </url>')

    lines.append('</urlset>')
    OUTPUT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'  News sitemap: {OUTPUT} ({len(urls)} articles)')

if __name__ == '__main__':
    gen_news_sitemap()
