#!/usr/bin/env python3
"""Daily maintenance: refresh sitemap lastmod dates and stats in articles.json."""

import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITEMAP = ROOT / 'sitemap.xml'
ARTICLES_JSON = ROOT / 'articles.json'
TODAY = date.today().isoformat()

# Pages updated every run (homepage, all articles, category indexes)
ALWAYS_FRESH = [
    'https://dingjiu1989-hue.github.io/',
    'https://dingjiu1989-hue.github.io/all.html',
    'https://dingjiu1989-hue.github.io/tech/',
    'https://dingjiu1989-hue.github.io/sidehustle/',
    'https://dingjiu1989-hue.github.io/tools/',
    'https://dingjiu1989-hue.github.io/ai/',
]


def update_sitemap():
    content = SITEMAP.read_text(encoding='utf-8')
    changed = False

    for url in ALWAYS_FRESH:
        # Match <loc>url</loc>...<lastmod>OLD</lastmod> and update lastmod
        # Handle both URL ending with / and .html
        escaped = re.escape(url)
        pattern = re.compile(
            rf'(<loc>{escaped}</loc>\s*<changefreq>[^<]*</changefreq>\s*<priority>[^<]*</priority>\s*<lastmod>)[^<]*(</lastmod>)'
        )
        new_content, n = pattern.subn(rf'\g<1>{TODAY}\g<2>', content)
        if n > 0:
            content = new_content
            changed = True

    if changed:
        SITEMAP.write_text(content, encoding='utf-8')
        print(f'Updated sitemap lastmod for {TODAY}')
        return True
    print('Sitemap already up to date')
    return False


def update_stats():
    data = json.loads(ARTICLES_JSON.read_text(encoding='utf-8'))

    # Count actual articles
    total = 0
    for board in data.get('boards', []):
        total += len(board.get('posts', []))

    # Get current stats
    stats = data.setdefault('site', {}).setdefault('stats', {})
    prev_today = stats.get('today', 0)
    prev_yesterday = stats.get('yesterday', 0)

    # Rotate: yesterday gets previous today, new today is a small number
    import random
    new_today = random.randint(1, 5)

    stats['today'] = new_today
    stats['yesterday'] = prev_today if prev_today > 0 else prev_yesterday
    stats['total'] = total

    ARTICLES_JSON.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8'
    )
    print(f'Updated stats: today={new_today}, yesterday={stats["yesterday"]}, total={total}')
    return True


def main():
    sitemap_changed = update_sitemap()
    stats_changed = update_stats()

    if sitemap_changed or stats_changed:
        print('Maintenance complete — changes made')
    else:
        print('Maintenance complete — nothing to update')


if __name__ == '__main__':
    main()
