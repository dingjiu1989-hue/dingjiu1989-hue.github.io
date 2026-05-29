#!/usr/bin/env python3
"""Add batch-generated AI analyst reports to analysis.html search cards.

Extracts company metadata from articles.json and generates simplified
COMPANIES_DATA entries, then injects them into analysis.html.
"""
import json, re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
ANALYSIS_HTML = BASE / 'ai-analyst' / 'analysis.html'
ARTICLES_CN = BASE / 'articles.json'
ARTICLES_EN = BASE / 'en' / 'articles.json'

# Hand-written reports that are already in COMPANIES_DATA (skip these)
HAND_WRITTEN_SLUGS = {
    'nvidia-2026', 'google-2026', 'microsoft-2026', 'amazon-2026',
    'meta-2026', 'tsmc-2026', 'broadcom-2026', 'tencent-2026',
    'apple-2026', 'baba-2026', 'xiaomi-group-2026', 'huahong-semiconductor-2026',
    'oracle-2026', 'netflix-2026', 'asml-2026', 'amd-2026', 'catl-2026',
    'ccb-2026', 'micron-2026',
    '600036-2026', '600900-2026', '601988-2026', '601398-2026', '601288-2026',
}

# Sector color mapping
SECTOR_COLORS = {
    '半导体': 'red-600',
    '金融': 'blue-600',
    '新能源': 'green-600',
    '公用事业': 'yellow-500',
    'AI': 'purple-600',
    '科技': 'blue-600',
    '通信': 'indigo-600',
    '消费电子': 'orange-500',
}

def slug_to_ticker(slug):
    """Extract ticker from slug like '002156-2026' → '002156.SZ'"""
    code = slug.split('-')[0]
    if code.isdigit():
        if code.startswith('6') or code.startswith('688'):
            return f'{code}.SH'
        elif code.startswith('0') or code.startswith('3'):
            return f'{code}.SZ'
    return code

def get_sector_color(sector):
    return SECTOR_COLORS.get(sector, 'blue-600')

def make_entry(post, board_posts):
    """Generate a simplified COMPANIES_DATA entry from articles.json post data."""
    slug = post['slug']
    code = slug.split('-')[0]
    title = post.get('title', '')
    description = post.get('description', '')[:120]

    # Determine company name and Chinese name from title
    name = title
    name_cn = title

    # Map some known names
    name_map = {
        '688981-2026': ('SMIC', '中芯国际'),
        '688041-2026': ('Hygon', '海光信息'),
        '002371-2026': ('NAURA', '北方华创'),
        '603501-2026': ('Will Semiconductor', '韦尔股份'),
        '688012-2026': ('AMEC', '中微公司'),
        '688256-2026': ('Cambricon', '寒武纪'),
        '603986-2026': ('GigaDevice', '兆易创新'),
        '002049-2026': ('Unigroup Guoxin', '紫光国微'),
        '600584-2026': ('JCET', '长电科技'),
        '688008-2026': ('Montage Technology', '澜起科技'),
        '300782-2026': ('Maxscend', '卓胜微'),
        '300661-2026': ('SG Micro', '圣邦股份'),
        '300223-2026': ('Ingenic', '北京君正'),
        '002185-2026': ('Huatian Technology', '华天科技'),
        '002156-2026': ('Tongfu Microelectronics', '通富微电'),
    }

    if slug in name_map:
        name, name_cn = name_map[slug]

    # Determine sector from first tag or description
    tags = post.get('tags', [])
    sector = '科技'
    if '投资分析' in tags:
        sector = '金融'
    if name_cn in ('中芯国际', '海光信息', '韦尔股份', '中微公司', '紫光国微',
                    '长电科技', '澜起科技', '卓胜微', '圣邦股份', '北京君正',
                    '华天科技', '通富微电', '兆易创新', '寒武纪', '北方华创',
                    'NAURA'):
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
