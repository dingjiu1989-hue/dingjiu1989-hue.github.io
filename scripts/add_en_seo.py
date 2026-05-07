#!/usr/bin/env python3
"""Update sitemap.xml with English URLs and add hreflang to Chinese pages."""
import json, re
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parent.parent
ARTICLES_JSON = ROOT / 'articles.json'
EN_ARTICLES_JSON = ROOT / 'en' / 'articles.json'
SITEMAP = ROOT / 'sitemap.xml'
TODAY = date.today().isoformat()
BASE = 'https://dingjiu1989-hue.github.io'

# ── 1. Update sitemap.xml ──────────────────────────────────────────────

def update_sitemap():
    sitemap = SITEMAP.read_text(encoding='utf-8')

    # Add xhtml namespace if not present
    if 'xmlns:xhtml' not in sitemap:
        sitemap = sitemap.replace(
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">'
        )

    en_data = json.loads(EN_ARTICLES_JSON.read_text(encoding='utf-8'))

    # Collect all English URLs from articles.json
    new_urls = []

    # English homepage
    en_home = f'{BASE}/en/'
    if en_home not in sitemap:
        new_urls.append((en_home, 'daily', '1.0'))
        print(f'  + sitemap: {en_home}')

    # English category pages
    for board in en_data['boards']:
        cat_url = f'{BASE}/en/{board["id"]}/'
        if cat_url not in sitemap:
            new_urls.append((cat_url, 'daily', '0.8'))
            print(f'  + sitemap: {cat_url}')

    # English article pages
    for board in en_data['boards']:
        for art in board['posts']:
            art_url = f'{BASE}/en/{board["id"]}/{art["slug"]}.html'
            if art_url not in sitemap:
                new_urls.append((art_url, 'weekly', '0.7'))
                print(f'  + sitemap: {art_url}')

    if new_urls:
        entries = []
        for url, freq, priority in new_urls:
            entries.append(
                f'  <url>\n'
                f'    <loc>{url}</loc>\n'
                f'    <changefreq>{freq}</changefreq>\n'
                f'    <priority>{priority}</priority>\n'
                f'    <lastmod>{TODAY}</lastmod>\n'
                f'  </url>'
            )
        sitemap = sitemap.replace('</urlset>', '\n'.join(entries) + '\n</urlset>')

    SITEMAP.write_text(sitemap, encoding='utf-8')
    print(f'  Sitemap updated with {len(new_urls)} new URLs')


# ── 2. Add hreflang to Chinese article pages ───────────────────────────

def add_hreflang():
    """Add bilingual hreflang links to Chinese article pages."""
    en_data = json.loads(EN_ARTICLES_JSON.read_text(encoding='utf-8'))
    updated = 0

    for board in en_data['boards']:
        for art in board['posts']:
            cn_path = ROOT / board['id'] / f'{art["slug"]}.html'
            if not cn_path.exists():
                print(f'  SKIP (missing): {cn_path}')
                continue

            html = cn_path.read_text(encoding='utf-8')

            en_url = f'{BASE}/en/{board["id"]}/{art["slug"]}.html'
            cn_url = f'{BASE}/{board["id"]}/{art["slug"]}.html'
            en_tag = f'<link rel="alternate" hreflang="en" href="{en_url}">'
            cn_tag = f'<link rel="alternate" hreflang="zh-CN" href="{cn_url}">'

            if en_tag in html:
                continue  # already done

            # Add both hreflang tags after stylesheet link
            html = html.replace(
                '<link rel="stylesheet" href="/css/style.css">',
                f'<link rel="stylesheet" href="/css/style.css">\n    {cn_tag}\n    {en_tag}'
            )

            cn_path.write_text(html, encoding='utf-8')
            updated += 1

    # Category pages
    for board in en_data['boards']:
        cat_path = ROOT / board['id'] / 'index.html'
        if not cat_path.exists():
            continue
        html = cat_path.read_text(encoding='utf-8')
        en_url = f'{BASE}/en/{board["id"]}/'
        cn_url = f'{BASE}/{board["id"]}/'
        en_tag = f'<link rel="alternate" hreflang="en" href="{en_url}">'
        cn_tag = f'<link rel="alternate" hreflang="zh-CN" href="{cn_url}">'
        if en_tag in html:
            continue
        html = html.replace(
            '<link rel="stylesheet" href="/css/style.css">',
            f'<link rel="stylesheet" href="/css/style.css">\n    {cn_tag}\n    {en_tag}'
        )
        cat_path.write_text(html, encoding='utf-8')
        updated += 1

    # Chinese homepage
    hp_path = ROOT / 'index.html'
    html = hp_path.read_text(encoding='utf-8')
    en_tag = f'<link rel="alternate" hreflang="en" href="{BASE}/en/">'
    cn_tag = f'<link rel="alternate" hreflang="zh-CN" href="{BASE}/">'
    if en_tag not in html:
        html = html.replace(
            '<link rel="stylesheet" href="css/style.css">',
            f'<link rel="stylesheet" href="css/style.css">\n    {cn_tag}\n    {en_tag}'
        )
        hp_path.write_text(html, encoding='utf-8')
        updated += 1

    print(f'  hreflang added to {updated} Chinese pages')


# ── Run ─────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    update_sitemap()
    add_hreflang()
    print('\nDone.')
