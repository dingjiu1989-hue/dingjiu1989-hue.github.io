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

def _cn_exists(board_id, slug=''):
    """Check if a Chinese counterpart page exists on disk."""
    if slug:
        return (ROOT / board_id / f'{slug}.html').exists()
    return (ROOT / board_id / 'index.html').exists()


def update_sitemap():
    sitemap = SITEMAP.read_text(encoding='utf-8')

    # Add xhtml namespace if not present
    if 'xmlns:xhtml' not in sitemap:
        sitemap = sitemap.replace(
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">'
        )

    en_data = json.loads(EN_ARTICLES_JSON.read_text(encoding='utf-8'))

    # Collect all English URLs with hreflang pairs
    new_urls = []

    # English homepage — Chinese homepage always exists
    en_home = f'{BASE}/en/'
    if en_home not in sitemap:
        hreflang_xml = (
            f'    <xhtml:link rel="alternate" hreflang="en" href="{en_home}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="zh-CN" href="{BASE}/"/>'
        )
        new_urls.append((en_home, 'daily', '1.0', hreflang_xml))
        print(f'  + sitemap: {en_home}')

    # English category pages — only add zh-CN hreflang if Chinese category exists
    for board in en_data['boards']:
        cat_url = f'{BASE}/en/{board["id"]}/'
        if cat_url not in sitemap:
            cn_cat_exists = _cn_exists(board['id'])
            if cn_cat_exists:
                hreflang_xml = (
                    f'    <xhtml:link rel="alternate" hreflang="en" href="{cat_url}"/>\n'
                    f'    <xhtml:link rel="alternate" hreflang="zh-CN" href="{BASE}/{board["id"]}/"/>'
                )
            else:
                hreflang_xml = f'    <xhtml:link rel="alternate" hreflang="en" href="{cat_url}"/>'
            new_urls.append((cat_url, 'daily', '0.8', hreflang_xml))
            print(f'  + sitemap: {cat_url}')

    # English article pages — only add zh-CN hreflang if Chinese article exists
    for board in en_data['boards']:
        for art in board['posts']:
            art_url = f'{BASE}/en/{board["id"]}/{art["slug"]}.html'
            if art_url not in sitemap:
                cn_exists = _cn_exists(board['id'], art['slug'])
                if cn_exists:
                    hreflang_xml = (
                        f'    <xhtml:link rel="alternate" hreflang="en" href="{art_url}"/>\n'
                        f'    <xhtml:link rel="alternate" hreflang="zh-CN" href="{BASE}/{board["id"]}/{art["slug"]}.html"/>'
                    )
                else:
                    hreflang_xml = f'    <xhtml:link rel="alternate" hreflang="en" href="{art_url}"/>'
                new_urls.append((art_url, 'weekly', '0.7', hreflang_xml))
                print(f'  + sitemap: {art_url}')

    if new_urls:
        entries = []
        for url, freq, priority, hreflang in new_urls:
            entries.append(
                f'  <url>\n'
                f'    <loc>{url}</loc>\n'
                f'    <changefreq>{freq}</changefreq>\n'
                f'    <priority>{priority}</priority>\n'
                f'    <lastmod>{TODAY}</lastmod>\n'
                f'{hreflang}\n'
                f'  </url>'
            )
        sitemap = sitemap.replace('</urlset>', '\n'.join(entries) + '\n</urlset>')

    # Retroactively add missing en hreflang to existing English URLs
    import re
    for board in en_data['boards']:
        for art in board['posts']:
            art_url = f'{BASE}/en/{board["id"]}/{art["slug"]}.html'
            cn_url = f'{BASE}/{board["id"]}/{art["slug"]}.html'
            cn_exists = _cn_exists(board['id'], art['slug'])
            if art_url in sitemap and f'<xhtml:link rel="alternate" hreflang="en" href="{art_url}"/>' not in sitemap:
                if cn_exists:
                    hreflang_xml = (
                        f'    <xhtml:link rel="alternate" hreflang="en" href="{art_url}"/>\n'
                        f'    <xhtml:link rel="alternate" hreflang="zh-CN" href="{cn_url}"/>'
                    )
                else:
                    hreflang_xml = f'    <xhtml:link rel="alternate" hreflang="en" href="{art_url}"/>'
                sitemap = sitemap.replace(
                    f'{art_url}</loc>\n    <changefreq>',
                    f'{art_url}</loc>\n{hreflang_xml}\n    <changefreq>'
                )
                print(f'  + hreflang: {art_url}')
    # Category pages
    for board in en_data['boards']:
        cat_en = f'{BASE}/en/{board["id"]}/'
        cat_cn = f'{BASE}/{board["id"]}/'
        if cat_en in sitemap and f'hreflang="en" href="{cat_en}"' not in sitemap:
            if _cn_exists(board['id']):
                hreflang_xml = (
                    f'    <xhtml:link rel="alternate" hreflang="en" href="{cat_en}"/>\n'
                    f'    <xhtml:link rel="alternate" hreflang="zh-CN" href="{cat_cn}"/>'
                )
            else:
                hreflang_xml = f'    <xhtml:link rel="alternate" hreflang="en" href="{cat_en}"/>'
            sitemap = sitemap.replace(
                f'{cat_en}</loc>\n    <changefreq>',
                f'{cat_en}</loc>\n{hreflang_xml}\n    <changefreq>'
            )
            print(f'  + hreflang: {cat_en}')
    # English homepage — Chinese homepage always exists
    en_home = f'{BASE}/en/'
    if en_home in sitemap and f'hreflang="en" href="{en_home}"' not in sitemap:
        hreflang_xml = (
            f'    <xhtml:link rel="alternate" hreflang="en" href="{en_home}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="zh-CN" href="{BASE}/"/>'
        )
        sitemap = sitemap.replace(
            f'{en_home}</loc>\n    <changefreq>',
            f'{en_home}</loc>\n{hreflang_xml}\n    <changefreq>'
        )
        print(f'  + hreflang: {en_home}')

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
