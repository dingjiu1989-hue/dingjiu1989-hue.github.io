#!/usr/bin/env python3
"""SourceHub Weekly Audit: content inventory, SEO health, GSC analysis, growth recommendations."""

import json, csv, re, sys
from collections import defaultdict, Counter
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARTICLES_JSON = ROOT / 'articles.json'
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

    return {
        'total': total, 'by_board': by_board,
        'ages': ages, 'top_tags': tags.most_common(10),
        'boards': boards,
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

    # Content volume check
    if inv['total'] < 50:
        recs.append(f"内容量：{inv['total']}/50 — 距 AdSense 门槛还差 {50 - inv['total']} 篇，预计 {(50 - inv['total']) // 5 + 1} 周达标")
    else:
        recs.append(f"内容量：{inv['total']} 篇，已达到 AdSense 申请门槛")

    # Board balance
    counts = list(inv['by_board'].values())
    if counts and max(counts) > min(counts) * 2:
        smallest = min(inv['by_board'], key=inv['by_board'].get)
        largest = max(inv['by_board'], key=inv['by_board'].get)
        recs.append(f"版块失衡：{largest}({inv['by_board'][largest]}篇) vs {smallest}({inv['by_board'][smallest]}篇)，建议补齐 {smallest}")

    # Freshness
    if inv['ages']['this_week'] < 3:
        recs.append(f"本周新增仅 {inv['ages']['this_week']} 篇，建议维持每周 3-5 篇节奏，搜索引擎偏好活跃站点")

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
    lines = [
        f'# SourceHub 周度审计报告',
        f'**日期**: {TODAY}',
        f'**审计周期**: {WEEK_AGO} → {TODAY}',
        '',
        '## 内容概览',
        f'- 总文章数: **{inv["total"]}**',
        f'- 版块分布: ' + ' | '.join(f'{k}: {v}' for k, v in inv['by_board'].items()),
        f'- 本周新增: {inv["ages"]["this_week"]} 篇',
        f'- 1-2周内: {inv["ages"]["1-2_weeks"]} 篇',
        f'- 较旧内容: {inv["ages"]["older"]} 篇',
        '',
        '## 热门标签',
        ' | '.join(f'`{t}`({c})' for t, c in inv['top_tags'][:8]),
        '',
        '## 搜索表现',
    ]

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

    lines += ['', '---', f'*自动生成于 {TODAY} · SourceHub 运营系统*']

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
