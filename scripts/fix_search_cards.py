#!/usr/bin/env python3
"""Fix batch-generated search cards: short names, correct sectors, clean summaries."""
import json, re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
ANALYSIS_HTML = BASE / 'ai-analyst' / 'analysis.html'

# Hand-written reports that ALREADY have correct names (DON'T touch these)
HAND_WRITTEN_SLUGS = {
    'nvidia-2026', 'google-2026', 'microsoft-2026', 'amazon-2026',
    'meta-2026', 'tsmc-2026', 'broadcom-2026', 'tencent-2026',
    'apple-2026', 'baba-2026', 'xiaomi-group-2026', 'huahong-semiconductor-2026',
    'oracle-2026', 'netflix-2026', 'asml-2026', 'amd-2026', 'catl-2026',
    'ccb-2026', 'micron-2026',
    '600036-2026', '600900-2026', '601988-2026', '601398-2026', '601288-2026',
}

# Company name mapping: slug -> (short_name, name_cn)
NAME_MAP = {
    '600460-2026': ('Silan Micro', '士兰微'),
    '688396-2026': ('China Resources Microelectronics', '华润微'),
    '688099-2026': ('Amlogic', '晶晨股份'),
    '688385-2026': ('Fudan Micro', '复旦微电'),
    '688052-2026': ('Novosense Micro', '纳芯微'),
    '688536-2026': ('3Peak', '思瑞浦'),
    '688047-2026': ('Loongson', '龙芯中科'),
    '688126-2026': ('NSIG', '沪硅产业'),
    '688019-2026': ('Anji Micro', '安集科技'),
    '688072-2026': ('Piotech', '拓荆科技'),
}

# Stock codes that should be '半导体' sector
SEMICONDUCTOR_CODES = {
    '688981', '688041', '002371', '603501', '688012', '688256', '603986',
    '002049', '600584', '688008', '300782', '300661', '300223', '002185',
    '002156', '600460', '688396', '688099', '688385', '688052',
    '688536', '688047', '688126', '688019', '688072',
}

def is_batch_entry(slug, c):
    """Check if this card is a batch-generated entry (not hand-written)."""
    if slug in HAND_WRITTEN_SLUGS:
        return False
    code = slug.split('-')[0]
    # Numeric code = stock A-share = batch-generated
    if code.isdigit():
        return True
    # Has long auto-generated title
    if '全面分析报告' in c.get('name', '') or '全面分析报告' in c.get('nameCn', ''):
        return True
    return False

def clean_summary(text):
    """Remove markdown formatting artifacts from summary text."""
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\\n\\n', ' ', text)
    text = re.sub(r'\\n', ' ', text)
    text = text.replace('**', '')
    if len(text) > 150:
        text = text[:147] + '...'
    return text.strip()

def get_name_cn(slug):
    """Extract short Chinese name from slug."""
    if slug in NAME_MAP:
        return NAME_MAP[slug][1]
    code = slug.split('-')[0]
    return code

def get_name(slug):
    """Get short English name."""
    if slug in NAME_MAP:
        return NAME_MAP[slug][0]
    return slug.split('-')[0]

def get_sector(slug):
    code = slug.split('-')[0]
    if code in SEMICONDUCTOR_CODES:
        return '半导体'
    return '科技'

def get_rating_color(sector):
    colors = {'半导体': 'red-600', '金融': 'blue-600', '科技': 'blue-600', '新能源': 'green-600'}
    return colors.get(sector, 'blue-600')

def main():
    html_content = ANALYSIS_HTML.read_text(encoding='utf-8')
    match = re.search(r'var COMPANIES_DATA = ({.*?});', html_content, re.DOTALL)
    if not match:
        print('ERROR: Could not find COMPANIES_DATA')
        return

    companies_data = json.loads(match.group(1))
    fixed = 0
    skipped = 0

    for c in companies_data['companies']:
        slug = c['slug']
        code = slug.split('-')[0]

        if not is_batch_entry(slug, c):
            skipped += 1
            continue

        needs_fix = False

        # Fix name/long title
        if slug in NAME_MAP:
            en_name, cn_name = NAME_MAP[slug]
            if c['name'] != en_name:
                c['name'] = en_name
                needs_fix = True
            if c['nameCn'] != cn_name:
                c['nameCn'] = cn_name
                needs_fix = True
        elif '全面分析报告' in c.get('name', '') or '全面分析报告' in c.get('nameCn', ''):
            short = get_name_cn(slug)
            if short != code:
                c['name'] = short
                c['nameCn'] = short
                needs_fix = True

        # Fix sector
        correct_sector = get_sector(slug)
        if c.get('sector') != correct_sector:
            c['sector'] = correct_sector
            c['sectorEn'] = correct_sector
            c['ratingColor'] = get_rating_color(correct_sector)
            needs_fix = True

        # Fix summary (remove markdown)
        summary = c.get('summary', '')
        clean = clean_summary(summary)
        if clean != summary:
            c['summary'] = clean
            needs_fix = True

        # Fix highlights
        highlights = c.get('highlights', [])
        if highlights == ['AI 驱动深度研究', '8 段式买方分析', 'Chart.js 数据可视化']:
            sector_highlights = {
                '半导体': ['国产替代核心标的', '周期反转受益', 'AI 驱动深度研究'],
                '科技': ['AI 驱动深度研究', '行业龙头地位', '8 段式买方分析'],
            }
            c['highlights'] = sector_highlights.get(correct_sector, highlights)
            needs_fix = True

        if needs_fix:
            fixed += 1
            print(f'  Fixed: {slug} → {c["name"]} ({c["nameCn"]}) sector={c["sector"]}')

    # Build and write back
    new_json = json.dumps(companies_data, ensure_ascii=False, separators=(',', ':'))
    new_html = html_content[:match.start(1)] + new_json + html_content[match.end(1):]

    # Also update og:description count
    new_html = re.sub(
        r'覆盖 \d+ 家头部公司',
        f'覆盖 {len(companies_data["companies"])} 家头部公司',
        new_html,
    )
    new_html = re.sub(
        r'覆盖 NVIDIA、Apple、台积电、宁德时代等 \d+ 家',
        f'覆盖 NVIDIA、Apple、台积电、宁德时代等 {len(companies_data["companies"])} 家',
        new_html,
    )

    ANALYSIS_HTML.write_text(new_html, encoding='utf-8')
    print(f'\nDone. Fixed {fixed} batch entries. Skipped {skipped} hand-written. Total: {len(companies_data["companies"])}')

if __name__ == '__main__':
    main()
