#!/usr/bin/env python3
"""
AI Crawler Activity Tracker for GitHub Pages site.

Since GitHub Pages has no server logs, we use multiple signals:
  1. GSC search analytics → proxies Googlebot crawl activity
  2. GSC URL Inspection → index coverage for key pages
  3. Sitemap health → are crawlers able to discover all URLs?
  4. AI-friendly file accessibility → llms.txt, llms-full.txt, robots.txt
  5. Trend comparison → detect anomalies (drops in impressions = possible crawl issue)

Output: data/crawl-stats.json (historical trend data)
"""

import json, sys, time, os
from pathlib import Path
from datetime import date, datetime, timedelta

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://aidev.fit"
DATA_DIR = ROOT / "data"
STATS_FILE = DATA_DIR / "crawl-stats.json"

TODAY = date.today().isoformat()
NOW = datetime.now().isoformat()

try:
    import requests
except ImportError:
    print("ERROR: requests library required. Run: pip3 install requests")
    sys.exit(1)

HTTP_TIMEOUT = 15
USER_AGENT = "CrawlTracker/1.0 (AI crawler monitoring)"


# ═══════════════════════════════════════════════════════════════════════════
# 1. AI-friendly file accessibility
# ═══════════════════════════════════════════════════════════════════════════

AI_FILES = [
    {"path": "/llms.txt", "desc": "AI crawler site index"},
    {"path": "/llms-full.txt", "desc": "Full English training content"},
    {"path": "/llms-full-cn.txt", "desc": "Full Chinese training content"},
    {"path": "/robots.txt", "desc": "Crawler rules"},
    {"path": "/sitemap.xml", "desc": "XML sitemap"},
    {"path": "/en/feed.xml", "desc": "English RSS feed"},
    {"path": "/feed.xml", "desc": "Chinese RSS feed"},
]

MD_SAMPLES = [
    "/md/en/ai/best-llms-for-coding-2026.md",
    "/md/en/tech/rust-for-javascript-developers.md",
    "/md/zh/tech/docker-quickstart.md",
]


def check_ai_files():
    """Verify all AI-friendly files are accessible and return sizes."""
    results = {"checked": 0, "ok": 0, "errors": [], "total_kb": 0, "files": []}

    for f in AI_FILES:
        url = f"{BASE}{f['path']}"
        try:
            r = requests.head(url, timeout=HTTP_TIMEOUT, headers={"User-Agent": USER_AGENT}, allow_redirects=True)
            size_kb = 0
            if r.status_code == 200:
                # Get actual size with GET for key files
                if f["path"] in ("/llms.txt", "/robots.txt", "/sitemap.xml"):
                    r2 = requests.get(url, timeout=HTTP_TIMEOUT, headers={"User-Agent": USER_AGENT})
                    size_kb = len(r2.content) / 1024
                results["ok"] += 1
            else:
                results["errors"].append({"file": f["path"], "status": r.status_code, "desc": f["desc"]})
            results["files"].append({
                "path": f["path"], "desc": f["desc"],
                "status": r.status_code, "size_kb": round(size_kb, 1),
            })
        except Exception as e:
            results["errors"].append({"file": f["path"], "error": str(e)[:120], "desc": f["desc"]})
        results["checked"] += 1

    # Sample Markdown copies
    for path in MD_SAMPLES:
        url = f"{BASE}{path}"
        try:
            r = requests.head(url, timeout=HTTP_TIMEOUT, headers={"User-Agent": USER_AGENT}, allow_redirects=True)
            if r.status_code != 200:
                results["errors"].append({"file": path, "status": r.status_code, "desc": "MD copy"})
        except Exception as e:
            results["errors"].append({"file": path, "error": str(e)[:120], "desc": "MD copy"})

    results["health_pct"] = round(results["ok"] / max(results["checked"], 1) * 100, 1)
    return results


# ═══════════════════════════════════════════════════════════════════════════
# 2. Sitemap coverage — how many URLs are Google discovering?
# ═══════════════════════════════════════════════════════════════════════════

def check_sitemap_coverage():
    """Parse sitemap and check how many URLs are discoverable."""
    try:
        r = requests.get(f"{BASE}/sitemap.xml", timeout=HTTP_TIMEOUT, headers={"User-Agent": USER_AGENT})
        r.raise_for_status()
    except Exception as e:
        return {"error": str(e), "total_urls": 0, "en_urls": 0, "cn_urls": 0}

    import re
    urls = re.findall(r"<loc>([^<]+)</loc>", r.text)
    en_urls = [u for u in urls if "/en/" in u]
    cn_urls = [u for u in urls if "/en/" not in u and u != f"{BASE}/"]

    # Check lastmod dates
    lastmods = re.findall(r"<lastmod>([^<]+)</lastmod>", r.text)
    recent = [lm for lm in lastmods if lm >= "2026-01-01"]

    return {
        "total_urls": len(urls),
        "en_urls": len(en_urls),
        "cn_urls": len(cn_urls),
        "recently_updated": len(recent),
        "oldest_lastmod": min(lastmods) if lastmods else None,
        "newest_lastmod": max(lastmods) if lastmods else None,
    }


# ═══════════════════════════════════════════════════════════════════════════
# 3. Content freshness — are we adding content regularly?
# ═══════════════════════════════════════════════════════════════════════════

def check_content_freshness():
    """Check how recently content was added/updated."""
    en_articles = ROOT / "en" / "articles.json"
    cn_articles = ROOT / "articles.json"

    result = {"en_articles": 0, "cn_articles": 0, "latest_date": None, "articles_this_week": 0}

    if en_articles.exists():
        en_data = json.loads(en_articles.read_text(encoding="utf-8"))
        for board in en_data.get("boards", []):
            posts = board.get("posts", [])
            result["en_articles"] += len(posts)

    if cn_articles.exists():
        cn_data = json.loads(cn_articles.read_text(encoding="utf-8"))
        for board in cn_data.get("boards", []):
            posts = board.get("posts", [])
            result["cn_articles"] += len(posts)
            for art in posts:
                d = art.get("date", "")
                if d and (result["latest_date"] is None or d > result["latest_date"]):
                    result["latest_date"] = d
                # Articles added in the last 14 days
                if d >= (date.today() - timedelta(days=14)).isoformat():
                    result["articles_this_week"] += 1

    return result


# ═══════════════════════════════════════════════════════════════════════════
# 4. GSC crawl data (Googlebot proxy)
# ═══════════════════════════════════════════════════════════════════════════

def pull_gsc_crawl_data():
    """Pull GSC search analytics as a proxy for Googlebot crawl activity.
    More impressions → more crawl activity. We also check URL inspection
    for key pages.
    """
    oauth_file = ROOT / "oauth-client.json"

    if not oauth_file.exists():
        return _gsc_csv_crawl_fallback()

    try:
        from googleapiclient.discovery import build
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
    except ImportError:
        return _gsc_csv_crawl_fallback()

    SCOPES = ["https://www.googleapis.com/auth/webmasters"]
    TOKEN_FILE = DATA_DIR / "gsc-token.json"
    credentials = None

    try:
        if TOKEN_FILE.exists():
            credentials = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                # In CI, browser auth is not possible — fall back to CSV
                if os.environ.get("CI") or not sys.stdin.isatty():
                    print("  Running in CI/non-interactive mode, falling back to CSV")
                    return _gsc_csv_crawl_fallback()
                flow = InstalledAppFlow.from_client_secrets_file(str(oauth_file), SCOPES)
                credentials = flow.run_local_server(port=0, open_browser=True)
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        TOKEN_FILE.write_text(credentials.to_json(), encoding="utf-8")

        service = build("searchconsole", "v1", credentials=credentials)

        site_url = None
        try:
            sites = service.sites().list().execute()
            for s in sites.get("siteEntry", []):
                if "dingjiu1989-hue.github.io" in s.get("siteUrl", "") or "aidev.fit" in s.get("siteUrl", ""):
                    site_url = s["siteUrl"]
                    break
        except Exception:
            pass
        if not site_url:
            site_url = f"{BASE}/"

        end_date = date.today() - timedelta(days=3)
        start_date = end_date - timedelta(days=28)

        # Search analytics by date
        daily = []
        try:
            resp = service.searchanalytics().query(siteUrl=site_url, body={
                "startDate": start_date.isoformat(),
                "endDate": end_date.isoformat(),
                "dimensions": ["date"],
                "rowLimit": 31,
            }).execute()
            for row in resp.get("rows", []):
                daily.append({
                    "date": row["keys"][0],
                    "clicks": row.get("clicks", 0),
                    "impressions": row.get("impressions", 0),
                    "ctr": round(row.get("ctr", 0) * 100, 2),
                    "position": round(row.get("position", 0), 1),
                })
        except Exception as e:
            print(f"  Search analytics error: {e}")

        # Index coverage — inspect key pages via URL Inspection API
        KEY_PAGES = [
            f"{BASE}/",
            f"{BASE}/en/",
            f"{BASE}/en/ai/",
            f"{BASE}/en/tech/",
            f"{BASE}/llms.txt",
        ]
        inspections = []
        for page_url in KEY_PAGES:
            try:
                result = service.urlInspection().index(
                    body={"inspectionUrl": page_url, "siteUrl": site_url}
                ).execute()
                inspection = result.get("inspectionResult", {})
                index_status = inspection.get("indexStatusResult", {})
                inspections.append({
                    "url": page_url,
                    "coverageState": index_status.get("coverageState", "unknown"),
                    "lastCrawlTime": index_status.get("lastCrawlTime", None),
                    "crawledAs": index_status.get("crawledAs", "unknown"),
                    "robotsTxtState": index_status.get("robotsTxtState", "unknown"),
                    "pageFetchState": index_status.get("pageFetchState", "unknown"),
                    "indexingState": index_status.get("indexingState", "unknown"),
                })
            except Exception as e:
                err_msg = str(e)[:200]
                # URL Inspection API may not be available in all GSC API versions
                if "unexpected keyword" in err_msg.lower() or "has no attribute" in err_msg.lower():
                    inspections.append({"url": page_url, "note": "URL Inspection API not available in this client version"})
                else:
                    inspections.append({"url": page_url, "error": err_msg})

        # Aggregate
        total_impressions = sum(d["impressions"] for d in daily)
        total_clicks = sum(d["clicks"] for d in daily)
        active_days = sum(1 for d in daily if d["impressions"] > 0)
        indexed_pages = sum(1 for i in inspections if i.get("coverageState") == "Published")

        return {
            "source": "api",
            "available": True,
            "period": f"{start_date} → {end_date}",
            "total_impressions": total_impressions,
            "total_clicks": total_clicks,
            "active_days": active_days,
            "avg_ctr": round(total_clicks / max(total_impressions, 1) * 100, 2),
            "avg_position": round(sum(d["position"] for d in daily) / max(len(daily), 1), 1),
            "daily_avg_impressions": round(total_impressions / max(active_days, 1), 1),
            "daily": daily,
            "key_page_inspections": inspections,
            "indexed_key_pages": indexed_pages,
            "total_key_pages": len(KEY_PAGES),
        }

    except Exception as e:
        print(f"  GSC API error: {e}")
        return _gsc_csv_crawl_fallback()


def _gsc_csv_crawl_fallback():
    """Fallback: read GSC CSV exports for crawl proxy data."""
    GSC_DIR = Path("/Users/daniel/01_工作/项目/google广告赚钱测试/data/https___dingjiu1989-hue")
    if not GSC_DIR.exists():
        return {"source": "csv", "available": False, "error": f"GSC data dir not found"}

    import csv
    daily = []
    chart_file = GSC_DIR / "图表.csv"
    if chart_file.exists():
        with open(chart_file, encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                daily.append({
                    "date": row.get("日期", ""),
                    "clicks": int(row.get("点击次数", 0) or 0),
                    "impressions": int(row.get("展示", 0) or 0),
                    "ctr": float(row.get("点击率", "0").replace("%", "") or 0),
                    "position": float(row.get("排名", "99") or 99),
                })

    total_impressions = sum(d["impressions"] for d in daily)
    total_clicks = sum(d["clicks"] for d in daily)
    active_days = sum(1 for d in daily if d["impressions"] > 0)

    return {
        "source": "csv",
        "available": bool(daily),
        "total_impressions": total_impressions,
        "total_clicks": total_clicks,
        "active_days": active_days,
        "avg_ctr": round(total_clicks / max(total_impressions, 1) * 100, 2),
        "avg_position": round(sum(d["position"] for d in daily) / max(len(daily), 1), 1) if daily else None,
        "daily_avg_impressions": round(total_impressions / max(active_days, 1), 1),
        "daily": daily,
    }


# ═══════════════════════════════════════════════════════════════════════════
# 5. Cloudflare readiness check
# ═══════════════════════════════════════════════════════════════════════════

def check_cloudflare_readiness():
    """Check if the site could benefit from Cloudflare for bot analytics.
    Cloudflare free tier gives: Bot Fight Mode, WAF analytics, bot traffic dashboard.
    """
    # Check if already behind Cloudflare
    try:
        r = requests.get(f"{BASE}/", timeout=HTTP_TIMEOUT, headers={"User-Agent": USER_AGENT}, allow_redirects=True)
        headers = r.headers
        is_cloudflare = "cf-ray" in headers or "CF-RAY" in headers or "cloudflare" in headers.get("server", "").lower()
    except Exception:
        is_cloudflare = False

    return {
        "behind_cloudflare": is_cloudflare,
        "recommendation": (
            "Already behind Cloudflare — bot analytics available in Cloudflare Dashboard → Security → Bots"
            if is_cloudflare else
            "Add Cloudflare free tier for full bot analytics: DNS → Cloudflare nameservers, enable Bot Fight Mode, "
            "then monitor Security → Bots dashboard. No server logs on GitHub Pages."
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# 6. Report assembly
# ═══════════════════════════════════════════════════════════════════════════

def load_previous_stats():
    if STATS_FILE.exists():
        try:
            return json.loads(STATS_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return None


def build_report(ai_files, sitemap, freshness, gsc, cloudflare):
    prev = load_previous_stats()

    report = {
        "generated_at": NOW,
        "date": TODAY,
        "ai_files": ai_files,
        "sitemap_coverage": sitemap,
        "content_freshness": freshness,
        "gsc_crawl_proxy": gsc,
        "cloudflare": cloudflare,
        "summary": [],
        "trend": {},
    }

    # Generate summary signals
    if ai_files["errors"]:
        report["summary"].append(f"⚠ {len(ai_files['errors'])} AI-friendly file(s) unreachable")
    else:
        report["summary"].append("✓ All AI-friendly files accessible")

    if gsc.get("available"):
        impressions = gsc["total_impressions"]
        active = gsc["active_days"]
        report["summary"].append(
            f"Googlebot: {impressions} impressions / {active} active days → "
            f"~{gsc.get('daily_avg_impressions', 0)} impressions/day"
        )
        if "key_page_inspections" in gsc:
            indexed = gsc.get("indexed_key_pages", 0)
            total = gsc.get("total_key_pages", 0)
            report["summary"].append(f"Key pages indexed: {indexed}/{total}")
    else:
        report["summary"].append("GSC data unavailable — expected for very new site")

    if freshness["articles_this_week"] == 0:
        report["summary"].append("⚠ No articles added in the last 14 days — crawlers want fresh content")

    # Trend analysis
    if prev and prev.get("gsc_crawl_proxy", {}).get("available") and gsc.get("available"):
        prev_gsc = prev["gsc_crawl_proxy"]
        imp_delta = gsc["total_impressions"] - prev_gsc.get("total_impressions", 0)
        report["trend"]["impressions_delta"] = imp_delta
        if imp_delta < 0:
            pct = abs(imp_delta) / max(prev_gsc.get("total_impressions", 1), 1) * 100
            if pct > 20:
                report["summary"].append(f"⚠ Impressions dropped {pct:.0f}% — possible crawl issue")
        else:
            report["summary"].append(f"↑ Impressions +{imp_delta} since last check")

        prev_avg = prev_gsc.get("avg_position", 99)
        cur_avg = gsc.get("avg_position", 99)
        if cur_avg < prev_avg:
            report["trend"]["position_improved"] = round(prev_avg - cur_avg, 1)

    return report


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    print(f"=== AI Crawler Tracker — {NOW} ===\n")

    print("[1/4] Checking AI-friendly file accessibility...")
    ai_files = check_ai_files()
    print(f"  {ai_files['ok']}/{ai_files['checked']} accessible ({ai_files['health_pct']}%)")
    if ai_files["errors"]:
        for e in ai_files["errors"]:
            print(f"    ⚠ {e['file']}: {e.get('status', e.get('error', 'unknown'))}")

    print("\n[2/4] Checking sitemap coverage...")
    sitemap = check_sitemap_coverage()
    if "error" in sitemap:
        print(f"  ⚠ {sitemap['error']}")
    else:
        print(f"  {sitemap['total_urls']} URLs ({sitemap['en_urls']} EN + {sitemap['cn_urls']} CN)")

    print("\n[3/4] Checking content freshness...")
    freshness = check_content_freshness()
    print(f"  {freshness['en_articles'] + freshness['cn_articles']} total articles, "
          f"latest: {freshness['latest_date']}, "
          f"{freshness['articles_this_week']} added in last 14 days")

    print("\n[4/4] Pulling GSC crawl proxy data...")
    gsc = pull_gsc_crawl_data()
    if gsc.get("available"):
        print(f"  Source: {gsc['source']} | Impressions: {gsc['total_impressions']} | "
              f"Clicks: {gsc['total_clicks']} | Active days: {gsc['active_days']}")
    else:
        print(f"  Source: {gsc.get('source', 'none')} | {gsc.get('error', 'No data')}")

    cloudflare = check_cloudflare_readiness()

    # Build and save report
    report = build_report(ai_files, sitemap, freshness, gsc, cloudflare)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    STATS_FILE.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nReport saved to {STATS_FILE}")

    # Print summary
    print(f"\n=== Crawler Health Summary ===")
    for line in report["summary"]:
        print(f"  {line}")
    print(f"\nCloudflare: {cloudflare['recommendation']}")

    return report


if __name__ == "__main__":
    main()
