#!/usr/bin/env python3
"""Generate JSON Feed (jsonfeed.org) for AI crawlers and feed readers.

JSON Feed is the modern JSON alternative to RSS. Many AI training pipelines
and LLM-based feed readers prefer it over XML parsing.

Generates: /en/feed.json (English) and /feed.json (Chinese)
"""

import json, sys
from pathlib import Path
from datetime import datetime, timezone
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
EN_FEED_XML = ROOT / 'en' / 'feed.xml'
CN_FEED_XML = ROOT / 'feed.xml'

SITE_URL = 'https://dingjiu1989-hue.github.io'


def rss_to_json_feed(rss_path, title, language, output_path):
    """Convert RSS XML to JSON Feed v1.1 format."""
    tree = ET.parse(rss_path)
    channel = tree.find('channel')

    items = []
    for item in channel.findall('item'):
        title_el = item.find('title')
        link_el = item.find('link')
        desc_el = item.find('description')
        date_el = item.find('pubDate')

        if link_el is None:
            continue

        entry = {
            'id': link_el.text or '',
            'url': link_el.text or '',
            'title': title_el.text if title_el is not None else '',
        }

        if desc_el is not None and desc_el.text:
            entry['content_text'] = desc_el.text[:500]

        if date_el is not None and date_el.text:
            entry['date_published'] = date_el.text

        items.append(entry)

    feed = {
        'version': 'https://jsonfeed.org/version/1.1',
        'title': title,
        'home_page_url': f'{SITE_URL}/en/' if language == 'en' else f'{SITE_URL}/',
        'feed_url': f'{SITE_URL}/en/feed.json' if language == 'en' else f'{SITE_URL}/feed.json',
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

    if EN_FEED_XML.exists():
        n = rss_to_json_feed(EN_FEED_XML, 'AI Study Room (English)', 'en',
                             ROOT / 'en' / 'feed.json')
        results['en/feed.json'] = n

    if CN_FEED_XML.exists():
        n = rss_to_json_feed(CN_FEED_XML, 'AI自习室 (中文)', 'zh-CN',
                             ROOT / 'feed.json')
        results['feed.json'] = n

    print('JSON Feed generation complete:')
    for path, count in results.items():
        print(f'  {path}: {count} items')
    return 0


if __name__ == '__main__':
    sys.exit(main())
