#!/usr/bin/env python3
"""Fix batch-generated search cards: short names, correct sectors, clean summaries."""
import json, re
from pathlib import Path

from card_data import (
    HAND_WRITTEN_SLUGS, NAME_MAP, SEMICONDUCTOR_CODES,
    get_name, get_name_cn, get_sector, get_rating_color,
    is_batch_entry, clean_summary,
)

BASE = Path(__file__).resolve().parent.parent
ANALYSIS_HTML = BASE / 'ai-analyst' / 'analysis.html'


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
            code = slug.split('-')[0]
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
