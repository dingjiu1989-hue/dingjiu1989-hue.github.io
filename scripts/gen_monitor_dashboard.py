#!/usr/bin/env python3
"""Generate an SEO + AI Crawler monitoring dashboard HTML page.

Reads data/crawl-stats.json and data/seo-health.json, produces en/monitor/ page.
"""
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / 'data'
OUT_DIR = ROOT / 'en' / 'monitor'
BASE = 'https://dingjiu1989-hue.github.io'


def load_json(path):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding='utf-8'))
        except Exception:
            return None
    return None


def time_ago(iso_str):
    if not iso_str:
        return 'never'
    try:
        dt = datetime.fromisoformat(iso_str)
        delta = datetime.now() - dt
        if delta.days > 0:
            return f'{delta.days}d ago'
        if delta.seconds > 3600:
            return f'{delta.seconds // 3600}h ago'
        return f'{delta.seconds // 60}m ago'
    except Exception:
        return iso_str


def main():
    crawl = load_json(DATA_DIR / 'crawl-stats.json')
    seo = load_json(DATA_DIR / 'seo-health.json')

    # Metrics from crawl data
    impressions = crawl.get('gsc_crawl_proxy', {}).get('total_impressions', 0) if crawl else 0
    clicks = crawl.get('gsc_crawl_proxy', {}).get('total_clicks', 0) if crawl else 0
    active_days = crawl.get('gsc_crawl_proxy', {}).get('active_days', 0) if crawl else 0
    ai_health = crawl.get('ai_files', {}).get('health_pct', 0) if crawl else 0
    total_urls = crawl.get('sitemap_coverage', {}).get('total_urls', 0) if crawl else 0
    en_articles = crawl.get('content_freshness', {}).get('en_articles', 0) if crawl else 0
    cn_articles = crawl.get('content_freshness', {}).get('cn_articles', 0) if crawl else 0
    articles_week = crawl.get('content_freshness', {}).get('articles_this_week', 0) if crawl else 0

    # Summary lines
    summary = crawl.get('summary', []) if crawl else []
    gsc_daily = crawl.get('gsc_crawl_proxy', {}).get('daily', []) if crawl else []
    last_updated = crawl.get('generated_at', '') if crawl else ''

    # SEO health
    seo_issues = seo.get('seo_tags_issues_count', 0) if seo else 0
    schema_ok = len(seo.get('structured_data', {}).get('errors', [])) == 0 if seo else True
    broken_links = len(seo.get('internal_links', {}).get('broken', [])) if seo else 0

    # Build daily chart data
    daily_chart = []
    for d in gsc_daily[-30:]:
        daily_chart.append({
            'date': d.get('date', '')[-5:],
            'impressions': d.get('impressions', 0),
            'clicks': d.get('clicks', 0),
        })

    # Max for scaling
    max_imp = max([d['impressions'] for d in daily_chart] + [1])

    # GSC last 7 days
    last7 = gsc_daily[-7:] if len(gsc_daily) >= 7 else gsc_daily
    last7_imp = sum(d.get('impressions', 0) for d in last7)
    last7_clicks = sum(d.get('clicks', 0) for d in last7)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SEO & Crawler Monitor — SourceHub</title>
<meta name="robots" content="noindex, nofollow">
<link rel="stylesheet" href="/css/style.css">
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; margin: 0; padding: 20px; color: #333; }}
  .container {{ max-width: 900px; margin: 0 auto; }}
  h1 {{ font-size: 1.5rem; margin-bottom: 4px; }}
  .subtitle {{ color: #666; font-size: 0.85rem; margin-bottom: 20px; }}
  .last-updated {{ color: #999; font-size: 0.8rem; }}

  .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin-bottom: 20px; }}
  .card {{ background: #fff; border-radius: 8px; padding: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
  .card .value {{ font-size: 1.8rem; font-weight: 700; line-height: 1.2; }}
  .card .label {{ font-size: 0.8rem; color: #666; margin-top: 4px; }}
  .card.positive .value {{ color: #22c55e; }}
  .card.warning .value {{ color: #f59e0b; }}
  .card.neutral .value {{ color: #3b82f6; }}
  .card.danger .value {{ color: #ef4444; }}

  .section {{ background: #fff; border-radius: 8px; padding: 16px; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
  .section h2 {{ font-size: 1rem; margin: 0 0 12px 0; padding-bottom: 8px; border-bottom: 1px solid #eee; }}

  .summary-item {{ padding: 6px 0; font-size: 0.9rem; }}
  .summary-item.ok {{ color: #22c55e; }}
  .summary-item.warn {{ color: #f59e0b; }}

  .bar-chart {{ display: flex; align-items: flex-end; gap: 2px; height: 120px; margin: 10px 0; }}
  .bar-group {{ flex: 1; display: flex; flex-direction: column; align-items: center; }}
  .bar-imp {{ width: 100%; background: #3b82f6; border-radius: 2px 2px 0 0; min-height: 2px; transition: height 0.3s; position: relative; }}
  .bar-clicks {{ width: 100%; background: #22c55e; border-radius: 2px 2px 0 0; min-height: 2px; }}
  .bar-date {{ font-size: 0.65rem; color: #999; margin-top: 4px; }}
  .legend {{ display: flex; gap: 16px; font-size: 0.8rem; margin: 8px 0; }}
  .legend-dot {{ display: inline-block; width: 10px; height: 10px; border-radius: 2px; margin-right: 4px; }}

  table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; }}
  th, td {{ text-align: left; padding: 6px 8px; border-bottom: 1px solid #eee; }}
  th {{ font-weight: 600; color: #555; }}

  .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
  @media (max-width: 600px) {{ .grid-2 {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body>
<div class="container">
  <h1>🔍 SEO & Crawler Monitor</h1>
  <p class="subtitle">Last updated: {time_ago(last_updated)} &middot; <span class="last-updated">{last_updated[:19]}</span></p>

  <div class="cards">
    <div class="card neutral">
      <div class="value">{impressions}</div>
      <div class="label">Total Search Impressions</div>
    </div>
    <div class="card neutral">
      <div class="value">{clicks}</div>
      <div class="label">Total Clicks</div>
    </div>
    <div class="card positive">
      <div class="value">{active_days}</div>
      <div class="label">Active Days (GSC)</div>
    </div>
    <div class="card neutral">
      <div class="value">{en_articles + cn_articles}</div>
      <div class="label">Total Articles</div>
    </div>
  </div>

  <div class="grid-2">
    <div class="section">
    <h2>Last 7 Days</h2>
    <table>
      <tr><th>Metric</th><th>Value</th></tr>
      <tr><td>Impressions (7d)</td><td><strong>{last7_imp}</strong></td></tr>
      <tr><td>Clicks (7d)</td><td><strong>{last7_clicks}</strong></td></tr>
      <tr><td>Articles added (14d)</td><td><strong>{articles_week}</strong></td></tr>
      <tr><td>AI file health</td><td><strong>{ai_health}%</strong></td></tr>
      <tr><td>Sitemap URLs</td><td><strong>{total_urls}</strong></td></tr>
    </table>
    </div>

    <div class="section">
    <h2>Health Checks</h2>
    <div>
      {"".join(
        f'<div class="summary-item {"ok" if s.startswith("✓") else "warn"}">{s}</div>'
        for s in summary
      ) or '<div class="summary-item">No data</div>'}
    </div>
    </div>
  </div>

  <div class="section">
    <h2>Daily Impressions (last {len(daily_chart)} days)</h2>
    <div class="legend">
      <span><span class="legend-dot" style="background:#3b82f6"></span> Impressions</span>
      <span><span class="legend-dot" style="background:#22c55e"></span> Clicks</span>
    </div>
    <div class="bar-chart">
    {"".join(
      f'<div class="bar-group"><div class="bar-imp" style="height:{max(4, d["impressions"] / max_imp * 100)}px" title="{d["impressions"]} impressions"></div><div class="bar-clicks" style="height:{max(2, d.get("clicks", 0) / max(max_imp, 1) * 100)}px" title="{d.get("clicks", 0)} clicks"></div><div class="bar-date">{d["date"]}</div></div>'
      for d in daily_chart[-30:]
    )}
    </div>
  </div>

  <div class="section">
    <h2>Site Overview</h2>
    <table>
      <tr><th>Metric</th><th>Value</th></tr>
      <tr><td>English articles</td><td>{en_articles}</td></tr>
      <tr><td>Chinese articles</td><td>{cn_articles}</td></tr>
      <tr><td>Sitemap URLs</td><td>{total_urls}</td></tr>
      <tr><td>Structured data errors</td><td>{0 if schema_ok else '⚠ Has errors'}</td></tr>
      <tr><td>Broken internal links</td><td>{broken_links}</td></tr>
      <tr><td>SEO tag issues</td><td>{seo_issues}</td></tr>
    </table>
  </div>

  <p class="last-updated">Generated by <code>scripts/gen_monitor_dashboard.py</code></p>
</div>
</body>
</html>'''

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / 'index.html').write_text(html, encoding='utf-8')
    print(f'Dashboard: {OUT_DIR / "index.html"}')
    print(f'  Impressions: {impressions} | Clicks: {clicks} | Days: {active_days}')
    print(f'  Articles: {en_articles} EN + {cn_articles} CN = {en_articles + cn_articles}')


if __name__ == '__main__':
    main()
