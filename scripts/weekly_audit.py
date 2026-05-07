#!/usr/bin/env python3
"""SourceHub Weekly Audit: content inventory, SEO health, GSC analysis, growth recommendations."""

import json, csv, re, sys
from collections import defaultdict, Counter
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARTICLES_JSON = ROOT / 'articles.json'
EN_ARTICLES_JSON = ROOT / 'en' / 'articles.json'
DATA_DIR = ROOT / 'data'
REPORT_FILE = ROOT / 'data' / 'weekly-report.md'
TODAY = date.today()
WEEK_AGO = TODAY - timedelta(days=7)


def content_inventory():
    """Count articles, analyze distribution and freshness."""
    data = json.loads(ARTICLES_JSON.read_text(encoding='utf-8'))
    boards = data.get('boards', [])

    total = sum(len(b.get('posts', [])) for b in boards)
    by_board = {b['name']: len(b.get('posts', [])) for b in boards}

    # Age distribution
    ages = {'this_week': 0, '1-2_weeks': 0, '2-4_weeks': 0, 'older': 0}
    tags = Counter()
    for b in boards:
        for p in b.get('posts', []):
            d = date.fromisoformat(p['date'])
            days_ago = (TODAY - d).days
            if days_ago <= 7:
                ages['this_week'] += 1
            elif days_ago <= 14:
                ages['1-2_weeks'] += 1
            elif days_ago <= 28:
                ages['2-4_weeks'] += 1
            else:
                ages['older'] += 1
            for t in p.get('tags', []):
                tags[t] += 1

    # English content
    en_total = 0
    en_by_board = {}
    en_ages = {'this_week': 0, '1-2_weeks': 0, '2-4_weeks': 0, 'older': 0}
    en_tags = Counter()
    if EN_ARTICLES_JSON.exists():
        en_data = json.loads(EN_ARTICLES_JSON.read_text(encoding='utf-8'))
        en_boards = en_data.get('boards', [])
        en_total = sum(len(b.get('posts', [])) for b in en_boards)
        en_by_board = {b['name']: len(b.get('posts', [])) for b in en_boards}
        for b in en_boards:
            for p in b.get('posts', []):
                d = date.fromisoformat(p['date'])
                days_ago = (TODAY - d).days
                if days_ago <= 7:
                    en_ages['this_week'] += 1
                elif days_ago <= 14:
                    en_ages['1-2_weeks'] += 1
                elif days_ago <= 28:
                    en_ages['2-4_weeks'] += 1
                else:
                    en_ages['older'] += 1
                for t in p.get('tags', []):
                    en_tags[t] += 1

    return {
        'total': total, 'by_board': by_board,
        'ages': ages, 'top_tags': tags.most_common(10),
        'boards': boards,
        'en_total': en_total, 'en_by_board': en_by_board,
        'en_ages': en_ages, 'en_top_tags': en_tags.most_common(10),
    }


def parse_gsc():
    """Parse GSC CSV exports if available."""
    results = {'queries': [], 'pages': [], 'found': False}
    for f in sorted(DATA_DIR.glob('gsc-*.csv'), reverse=True):
        if 'queries' in f.name.lower():
            try:
                with open(f, newline='', encoding='utf-8') as fh:
                    reader = csv.DictReader(fh)
                    for row in reader:
                        results['queries'].append(row)
                results['found'] = True
            except Exception:
                pass
        if 'pages' in f.name.lower():
            try:
                with open(f, newline='', encoding='utf-8') as fh:
                    reader = csv.DictReader(fh)
                    for row in reader:
                        results['pages'].append(row)
                results['found'] = True
            except Exception:
                pass

    if results['found']:
        # Top queries by clicks
        queries = sorted(results['queries'],
                        key=lambda r: int(r.get('点击次数', 0) or r.get('Clicks', 0)),
                        reverse=True)[:10]
        total_clicks = sum(int(r.get('点击次数', 0) or r.get('Clicks', 0)) for r in results['queries'])
        total_impressions = sum(int(r.get('展示次数', 0) or r.get('Impressions', 0)) for r in results['queries'])
        avg_position = sum(float(r.get('排名', 0) or r.get('Position', 99)) for r in results['queries'])
        if len(results['queries']) > 0:
            avg_position /= len(results['queries'])
        results['summary'] = {
            'total_clicks': total_clicks,
            'total_impressions': total_impressions,
            'avg_position': avg_position,
            'top_queries': queries,
        }
    return results


def generate_recommendations(inv, gsc):
    """Generate actionable recommendations based on audit data."""
    recs = []

    # Content volume check — combined Chinese + English
    total_all = inv['total'] + inv.get('en_total', 0)
    recs.append(f"内容总量：中文 {inv['total']} 篇 + 英文 {inv.get('en_total', 0)} 篇 = {total_all} 篇")

    # Board balance (Chinese)
    counts = list(inv['by_board'].values())
    if counts and max(counts) > min(counts) * 2:
        smallest = min(inv['by_board'], key=inv['by_board'].get)
        largest = max(inv['by_board'], key=inv['by_board'].get)
        recs.append(f"中文版块失衡：{largest}({inv['by_board'][largest]}篇) vs {smallest}({inv['by_board'][smallest]}篇)，建议补齐 {smallest}")

    # Freshness (Chinese)
    if inv['ages']['this_week'] < 3:
        recs.append(f"中文本周新增仅 {inv['ages']['this_week']} 篇，建议维持每周 3-5 篇节奏，搜索引擎偏好活跃站点")

    # English freshness
    en_ages = inv.get('en_ages', {})
    if inv.get('en_total', 0) > 0 and en_ages.get('this_week', 0) < 1:
        recs.append(f"英文内容本周无更新，建议通过 maintenance.py 定期更新日期以保持搜索引擎活跃信号")

    # English board balance
    en_by_board = inv.get('en_by_board', {})
    en_counts = list(en_by_board.values())
    if en_counts and max(en_counts) > min(en_counts) * 2:
        smallest = min(en_by_board, key=en_by_board.get)
        largest = max(en_by_board, key=en_by_board.get)
        recs.append(f"英文版块失衡：{largest}({en_by_board[largest]}篇) vs {smallest}({en_by_board[smallest]}篇)，建议补齐 {smallest}")

    # GSC insights
    if gsc.get('found') and gsc.get('summary'):
        s = gsc['summary']
        recs.append(f"搜索流量：{s['total_clicks']} 次点击，{s['total_impressions']} 次展示，平均排名 {s['avg_position']:.1f}")
        if s['avg_position'] > 20:
            recs.append("平均排名 > 20，建议：更新旧文章 + 增加长尾关键词覆盖")
        if s['total_clicks'] < 10:
            recs.append("点击量极低，通常是索引未完成或内容未匹配搜索需求，继续扩量")

        # Identify winning topics
        top_q = s.get('top_queries', [])
        if top_q:
            for q in top_q[:3]:
                keyword = q.get('搜索词', q.get('Query', ''))
                clicks = q.get('点击次数', q.get('Clicks', '?'))
                recs.append(f"  🎯 潜力关键词: 「{keyword}」({clicks} 点击) — 考虑围绕此主题扩展更多内容")

    if not gsc.get('found'):
        recs.append("无 GSC 数据 — 需导出 Search Console 报告到 data/ 目录以启用数据分析")

    return recs


def write_report(inv, gsc, recs):
    """Generate markdown report and save to data/weekly-report.md."""
    en_total = inv.get('en_total', 0)
    total_all = inv['total'] + en_total

    lines = [
        f'# AI Study Room 周度审计报告',
        f'**日期**: {TODAY}',
        f'**审计周期**: {WEEK_AGO} → {TODAY}',
        '',
        '## 内容概览',
        f'- 总文章数: **{total_all}** (中文 {inv["total"]} + 英文 {en_total})',
        '',
        '### 中文内容',
        f'- 版块分布: ' + ' | '.join(f'{k}: {v}' for k, v in inv['by_board'].items()),
        f'- 本周活跃: {inv["ages"]["this_week"]} 篇',
        f'- 1-2周内: {inv["ages"]["1-2_weeks"]} 篇',
        f'- 较旧内容: {inv["ages"]["older"]} 篇',
    ]

    if en_total > 0:
        lines += [
            '',
            '### 英文内容',
            f'- 版块分布: ' + ' | '.join(f'{k}: {v}' for k, v in inv.get('en_by_board', {}).items()),
            f'- 本周活跃: {inv.get("en_ages", {}).get("this_week", 0)} 篇',
            f'- 1-2周内: {inv.get("en_ages", {}).get("1-2_weeks", 0)} 篇',
            f'- 较旧内容: {inv.get("en_ages", {}).get("older", 0)} 篇',
        ]

    lines += [
        '',
        '## 热门标签 (中文)',
        ' | '.join(f'`{t}`({c})' for t, c in inv['top_tags'][:8]),
    ]

    if inv.get('en_top_tags'):
        lines += [
            '',
            '## 热门标签 (英文)',
            ' | '.join(f'`{t}`({c})' for t, c in inv['en_top_tags'][:8]),
        ]

    lines += ['', '## 搜索表现']

    if gsc.get('found') and gsc.get('summary'):
        s = gsc['summary']
        lines += [
            f'- 总点击: {s["total_clicks"]}',
            f'- 总展示: {s["total_impressions"]}',
            f'- 平均排名: {s["avg_position"]:.1f}',
            '',
            '### Top 搜索词',
        ]
        for q in s.get('top_queries', [])[:10]:
            kw = q.get('搜索词', q.get('Query', '?'))
            cl = q.get('点击次数', q.get('Clicks', '?'))
            imp = q.get('展示次数', q.get('Impressions', '?'))
            pos = q.get('排名', q.get('Position', '?'))
            lines.append(f'- 「{kw}」 — {cl} 点击, {imp} 展示, 排名 {pos}')
    else:
        lines.append('\n> ⚠️ 无 GSC 数据。将 Search Console CSV 导出放到 `data/` 目录即可自动分析。')

    lines += ['', '## 行动建议', '']
    for i, r in enumerate(recs, 1):
        lines.append(f'{i}. {r}')

    lines += ['', '---', f'*自动生成于 {TODAY} · AI Study Room 运营系统*']

    report = '\n'.join(lines) + '\n'
    REPORT_FILE.write_text(report, encoding='utf-8')
    return report


def main():
    print(f'=== SourceHub Weekly Audit ({TODAY}) ===\n')
    inv = content_inventory()
    gsc = parse_gsc()
    recs = generate_recommendations(inv, gsc)
    report = write_report(inv, gsc, recs)
    print(report)
    return 0


if __name__ == '__main__':
    sys.exit(main())
