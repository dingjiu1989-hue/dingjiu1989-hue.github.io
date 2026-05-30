#!/usr/bin/env python3
"""Add batch-generated AI analyst reports to analysis.html search cards.

Extracts company metadata from articles.json and generates simplified
COMPANIES_DATA entries, then injects them into analysis.html.
"""
import json, re
from pathlib import Path

from card_data import (
    HAND_WRITTEN_SLUGS, NAME_MAP, SEMICONDUCTOR_CODES,
    slug_to_ticker, get_sector_color,
)

BASE = Path(__file__).resolve().parent.parent
ANALYSIS_HTML = BASE / 'ai-analyst' / 'analysis.html'
ARTICLES_CN = BASE / 'articles.json'
ARTICLES_EN = BASE / 'en' / 'articles.json'


def make_entry(post, board_posts):
    """Generate a simplified COMPANIES_DATA entry from articles.json post data."""
    slug = post['slug']
    code = slug.split('-')[0]
    description = post.get('description', '')[:120]

    # Determine company name
    if slug in NAME_MAP:
        name, name_cn = NAME_MAP[slug]
    else:
        title = post.get('title', '')
        name = title
        name_cn = title

    # Determine sector
    tags = post.get('tags', [])
    sector = '科技'
    if '投资分析' in tags:
        sector = '金融'
    if code in SEMICONDUCTOR_CODES:
        sector = '半导体'

    return {
        'slug': slug,
        'name': name,
        'nameCn': name_cn,
        'ticker': slug_to_ticker(slug),
        'exchange': 'SSE' if slug_to_ticker(slug).endswith('.SH') else 'SZSE',
        'sector': sector,
        'sectorEn': sector,
        'marketCap': '—',
        'revenue': '—',
        'revenueGrowth': '—',
        'netIncome': '—',
        'revenueRank': 'AI 深度研究报告',
        'pe': '—',
        'grossMargin': '—',
        'operatingMargin': '—',
        'rating': '中性',
        'ratingEn': 'Neutral',
        'ratingColor': get_sector_color(sector),
        'summary': description or f'{name_cn}全面分析报告，覆盖财务、技术面、竞品对比、估值与风险。',
        'highlights': ['AI 驱动深度研究', '8 段式买方分析', 'Chart.js 数据可视化'],
        'reportDate': post.get('date', '2026-05-29'),
        'reportUrl': f'{slug}.html',
    }


def main():
    articles = json.loads(ARTICLES_CN.read_text(encoding='utf-8'))
    html_content = ANALYSIS_HTML.read_text(encoding='utf-8')

    # Find the COMPANIES_DATA object
    match = re.search(r'var COMPANIES_DATA = ({.*?});\s*\n', html_content, re.DOTALL)
    if not match:
        print('ERROR: Could not find COMPANIES_DATA in analysis.html')
        return

    companies_data = json.loads(match.group(1))
    existing_slugs = {c['slug'] for c in companies_data['companies']}

    # Find batch reports not yet in COMPANIES_DATA
    new_entries = []
    for board in articles['boards']:
        if board['id'] == 'ai-analyst':
            for post in board['posts']:
                slug = post['slug']
                if slug not in existing_slugs:
                    entry = make_entry(post, board['posts'])
                    new_entries.append(entry)

    if not new_entries:
        print('All reports already in COMPANIES_DATA')
        return

    print(f'Adding {len(new_entries)} new entries to COMPANIES_DATA')
    for e in new_entries:
        print(f'  {e["slug"]}: {e["name"]} ({e["nameCn"]})')

    # Append new entries
    companies_data['companies'].extend(new_entries)
    companies_data['meta']['totalCompanies'] = len(companies_data['companies'])

    # Serialize with compact JSON
    new_json = json.dumps(companies_data, ensure_ascii=False, separators=(',', ':'))

    # Replace in HTML
    new_html = html_content[:match.start(1)] + new_json + html_content[match.end(1):]
    ANALYSIS_HTML.write_text(new_html, encoding='utf-8')
    print(f'\nDone. Total companies: {len(companies_data["companies"])}')

    # Also update the "覆盖 N 家" text in og:description
    new_html2 = ANALYSIS_HTML.read_text(encoding='utf-8')
    new_html2 = re.sub(
        r'覆盖 \d+ 家头部公司',
        f'覆盖 {len(companies_data["companies"])} 家头部公司',
        new_html2,
    )
    ANALYSIS_HTML.write_text(new_html2, encoding='utf-8')
    print('Updated company count in meta description.')


if __name__ == '__main__':
    main()
