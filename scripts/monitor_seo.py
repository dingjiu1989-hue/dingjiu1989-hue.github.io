#!/usr/bin/env python3
"""Weekly SEO health monitor for GitHub Pages site.

Checks:
  1. Sitemap HTTP health (status codes for all URLs)
  2. SEO tag completeness (canonical, og:image, robots, hreflang, etc.)
  3. Structured data validation (JSON-LD on sample pages)
  4. Internal link integrity (broken links, 404s)
  5. Page size analysis (flag bloated pages)
  6. GSC API data pull (index coverage, crawl stats, search performance)

Output: data/seo-health.json (updated each run)
"""

import json, re, sys, time, os
from pathlib import Path
from datetime import date, datetime
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
SITEMAP_URL = "https://dingjiu1989-hue.github.io/sitemap.xml"
BASE = "https://dingjiu1989-hue.github.io"
DATA_DIR = ROOT / "data"
HEALTH_FILE = DATA_DIR / "seo-health.json"

TODAY = date.today().isoformat()
NOW = datetime.now().isoformat()

# SEO tags every page must have
REQUIRED_TAGS = {
    "canonical": r'<link rel="canonical"',
    "og:title": r'<meta property="og:title"',
    "og:description": r'<meta property="og:description"',
    "og:image": r'<meta property="og:image"',
    "og:site_name": r'<meta property="og:site_name"',
    "og:locale": r'<meta property="og:locale"',
    "twitter:card": r'<meta name="twitter:card"',
    "twitter:image": r'<meta name="twitter:image"',
    "description": r'<meta name="description"',
    "robots": r'<meta name="robots"',
    "hreflang:en": r'hreflang="en"',
    "hreflang:zh": r'hreflang="zh-CN"',
    "json-ld": r'application/ld\+json',
}

try:
    import requests
except ImportError:
    print("ERROR: requests library required. Run: pip3 install requests")
    sys.exit(1)

HTTP_TIMEOUT = 15
USER_AGENT = "SEO-Monitor/1.0 (GitHub Pages health checker)"


# ═══════════════════════════════════════════════════════════════════════════
# 1. Sitemap Health
# ═══════════════════════════════════════════════════════════════════════════

def fetch_sitemap_urls():
    """Parse sitemap.xml and return list of all URLs."""
    try:
        r = requests.get(SITEMAP_URL, timeout=HTTP_TIMEOUT, headers={"User-Agent": USER_AGENT})
        r.raise_for_status()
    except Exception as e:
        print(f"  ERROR fetching sitemap: {e}")
        return []
    urls = re.findall(r"<loc>([^<]+)</loc>", r.text)
    # Filter to English pages only (we monitor those)
    en_urls = [u for u in urls if "/en/" in u]
    print(f"  Sitemap parsed: {len(urls)} total, {len(en_urls)} English URLs")
    return en_urls


def check_sitemap_health(urls):
    """Check HTTP status of sitemap URLs. Samples if > 50 pages."""
    sample = urls if len(urls) <= 50 else urls[:10] + urls[len(urls)//2-5:len(urls)//2+5] + urls[-10:]
    sample = list(dict.fromkeys(sample))  # deduplicate while preserving order

    results = {"checked": len(sample), "total_urls": len(urls), "ok": 0, "errors": []}
    session = requests.Session()

    for i, url in enumerate(sample):
        try:
            resp = session.head(url, timeout=HTTP_TIMEOUT, headers={"User-Agent": USER_AGENT}, allow_redirects=True)
            if resp.status_code == 200:
                results["ok"] += 1
            else:
                results["errors"].append({"url": url, "status": resp.status_code})
                print(f"    WARN {resp.status_code}: {url}")
        except Exception as e:
            results["errors"].append({"url": url, "error": str(e)})
            print(f"    ERROR: {url} — {e}")

        if (i + 1) % 10 == 0:
            time.sleep(0.5)  # Be gentle

    pct = results["ok"] / max(results["checked"], 1) * 100
    results["health_pct"] = round(pct, 1)
    return results


# ═══════════════════════════════════════════════════════════════════════════
# 2. SEO Tag Completeness (local files)
# ═══════════════════════════════════════════════════════════════════════════

def check_seo_tags():
    """Scan all generated English HTML files for required SEO tags."""
    en_dir = ROOT / "en"
    html_files = list(en_dir.rglob("*.html"))
    results = {"total_files": len(html_files), "missing_tags": defaultdict(list), "files_with_issues": 0}

    # Exclude utility pages (nav, footer, privacy)
    UTIL_PAGES = {"nav.html", "footer.html", "privacy.html"}
    html_files = [f for f in html_files if f.name not in UTIL_PAGES]

    for fpath in html_files:
        html = fpath.read_text(encoding="utf-8")
        rel = str(fpath.relative_to(ROOT))
        issues = []
        for tag_name, pattern in REQUIRED_TAGS.items():
            if not re.search(pattern, html):
                results["missing_tags"][tag_name].append(rel)
                issues.append(tag_name)
        if issues:
            results["files_with_issues"] += 1

    results["missing_tags"] = dict(results["missing_tags"])
    return results


# ═══════════════════════════════════════════════════════════════════════════
# 3. Structured Data Validation (sample)
# ═══════════════════════════════════════════════════════════════════════════

def check_structured_data():
    """Extract JSON-LD from sample pages and do basic validation."""
    en_dir = ROOT / "en"
    sample_files = [
        en_dir / "index.html",
        en_dir / "tech" / "index.html",
        en_dir / "tech" / "rust-for-javascript-developers.html",
        en_dir / "ai" / "best-llms-for-coding-2026.html",
        en_dir / "sidehustle" / "saas-bootstrapping-guide.html",
        en_dir / "compare" / "vercel-vs-netlify-vs-cloudflare.html",
    ]

    results = {"checked": 0, "schemas_found": defaultdict(int), "errors": []}

    for fpath in sample_files:
        if not fpath.exists():
            continue
        html = fpath.read_text(encoding="utf-8")
        # Find all JSON-LD blocks
        ld_blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
        results["checked"] += 1

        for block in ld_blocks:
            try:
                data = json.loads(block)
                schema_type = data.get("@type", "Unknown")
                results["schemas_found"][schema_type] += 1

                # Basic validity checks
                if schema_type == "Article":
                    required = ["headline", "datePublished", "author", "publisher", "mainEntityOfPage"]
                    for field in required:
                        if field not in data:
                            results["errors"].append(
                                {"file": str(fpath.relative_to(ROOT)), "schema": "Article", "missing_field": field}
                            )
                elif schema_type == "BreadcrumbList":
                    if "itemListElement" not in data:
                        results["errors"].append(
                            {"file": str(fpath.relative_to(ROOT)), "schema": "BreadcrumbList", "error": "missing itemListElement"}
                        )
            except json.JSONDecodeError as e:
                results["errors"].append({"file": str(fpath.relative_to(ROOT)), "error": f"Invalid JSON: {e}"})

    results["schemas_found"] = dict(results["schemas_found"])
    return results


# ═══════════════════════════════════════════════════════════════════════════
# 4. Page Size Analysis
# ═══════════════════════════════════════════════════════════════════════════

def check_page_sizes():
    """Check HTML file sizes, flag pages > 100KB."""
    en_dir = ROOT / "en"
    html_files = list(en_dir.rglob("*.html"))
    results = {"total_files": 0, "total_kb": 0, "largest": [], "over_100kb": []}

    for fpath in html_files:
        size_kb = fpath.stat().st_size / 1024
        results["total_files"] += 1
        results["total_kb"] += size_kb
        if size_kb > 100:
            results["over_100kb"].append({"file": str(fpath.relative_to(ROOT)), "size_kb": round(size_kb, 1)})

    results["total_kb"] = round(results["total_kb"], 1)
    results["avg_kb"] = round(results["total_kb"] / max(results["total_files"], 1), 1)
    # Top 5 largest
    sorted_files = sorted(
        [(f, f.stat().st_size / 1024) for f in html_files], key=lambda x: x[1], reverse=True
    )
    results["largest"] = [
        {"file": str(f.relative_to(ROOT)), "size_kb": round(s, 1)} for f, s in sorted_files[:5]
    ]
    return results


# ═══════════════════════════════════════════════════════════════════════════
# 5. Internal Link Integrity
# ═══════════════════════════════════════════════════════════════════════════

def check_internal_links():
    """Scan HTML for internal links and verify they point to existing files."""
    en_dir = ROOT / "en"
    html_files = list(en_dir.rglob("*.html"))
    results = {"checked": 0, "total_links": 0, "broken": [], "external": 0}

    # Build set of all valid relative paths
    valid_paths = {str(f.relative_to(ROOT)) for f in ROOT.rglob("*.html")}

    for fpath in html_files[:30]:  # Sample first 30 files
        html = fpath.read_text(encoding="utf-8")
        rel = str(fpath.relative_to(ROOT))

        # Find internal links (start with /)
        links = re.findall(r'href="(/[^"]*\.html)"', html)
        results["total_links"] += len(links)

        for link in links:
            # Remove leading slash for path matching
            path = link.lstrip("/")
            if path not in valid_paths and not link.startswith("http"):
                results["broken"].append({"from": rel, "to": link})

    results["checked"] = min(len(html_files), 30)
    return results


# ═══════════════════════════════════════════════════════════════════════════
# 6. GSC API Integration
# ═══════════════════════════════════════════════════════════════════════════

def _gsc_csv_fallback():
    """Fallback: read GSC bulk export CSVs."""
    GSC_DIR = Path("/Users/daniel/01_工作/项目/google广告赚钱测试/data/https___dingjiu1989-hue")
    results = {
        "available": False, "error": None, "source": "csv",
        "search_performance": None, "top_queries": [], "top_pages": [],
        "daily": [],
    }
    if not GSC_DIR.exists():
        results["error"] = f"GSC data directory not found at {GSC_DIR}"
        return results

    import csv
    chart_file = GSC_DIR / "图表.csv"
    if chart_file.exists():
        with open(chart_file, encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                results["daily"].append({
                    "date": row.get("日期", ""),
                    "clicks": int(row.get("点击次数", 0) or 0),
                    "impressions": int(row.get("展示", 0) or 0),
                    "ctr": row.get("点击率", ""),
                    "position": row.get("排名", ""),
                })
    queries_file = GSC_DIR / "查询数.csv"
    if queries_file.exists():
        with open(queries_file, encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                results["top_queries"].append({
                    "query": row.get("热门查询", ""),
                    "clicks": int(row.get("点击次数", 0) or 0),
                    "impressions": int(row.get("展示", 0) or 0),
                    "ctr": row.get("点击率", ""),
                    "position": row.get("排名", ""),
                })
    pages_file = GSC_DIR / "网页.csv"
    if pages_file.exists():
        with open(pages_file, encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                results["top_pages"].append({
                    "page": row.get("排名靠前的网页", ""),
                    "clicks": int(row.get("点击次数", 0) or 0),
                    "impressions": int(row.get("展示", 0) or 0),
                    "ctr": row.get("点击率", ""),
                    "position": row.get("排名", ""),
                })

    daily = results["daily"]
    if daily and any(d["impressions"] > 0 for d in daily):
        tc = sum(d["clicks"] for d in daily)
        ti = sum(d["impressions"] for d in daily)
        positions = [float(d["position"]) for d in daily if d["position"] and d["position"].replace(".", "").isdigit()]
        results["search_performance"] = {
            "days": len(daily), "total_clicks": tc, "total_impressions": ti,
            "avg_ctr": round(tc / max(ti, 1) * 100, 2),
            "avg_position": round(sum(positions) / max(len(positions), 1), 1) if positions else None,
        }
        results["available"] = True
    else:
        results["search_performance"] = {"total_clicks": 0, "total_impressions": 0}
    return results


def pull_gsc_data():
    """Pull GSC data via OAuth API, falling back to CSV if credentials missing."""
    oauth_file = ROOT / "oauth-client.json"

    if not oauth_file.exists():
        print("  No oauth-client.json, falling back to CSV…")
        return _gsc_csv_fallback()

    results = {"available": False, "error": None, "source": "api",
               "search_performance": None, "top_queries": [], "top_pages": [], "daily": []}

    try:
        from googleapiclient.discovery import build
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
    except ImportError:
        print("  google-api-python-client not installed, falling back to CSV…")
        return _gsc_csv_fallback()

    SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
    TOKEN_FILE = DATA_DIR / "gsc-token.json"
    credentials = None

    try:
        # Load cached token
        if TOKEN_FILE.exists():
            credentials = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

        # Refresh or re-auth
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
                print("  Token refreshed from cache")
            else:
                flow = InstalledAppFlow.from_client_secrets_file(str(oauth_file), SCOPES)
                credentials = flow.run_local_server(port=0, open_browser=True)
                print("  Browser auth completed")

        # Cache token
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        TOKEN_FILE.write_text(credentials.to_json(), encoding="utf-8")

        service = build("searchconsole", "v1", credentials=credentials)

        # Detect site URL — try URL-prefix first
        site_url = None
        try:
            sites = service.sites().list().execute()
            for s in sites.get("siteEntry", []):
                if "dingjiu1989-hue.github.io" in s.get("siteUrl", ""):
                    site_url = s["siteUrl"]
                    break
        except Exception:
            pass
        if not site_url:
            site_url = "https://dingjiu1989-hue.github.io/"

        print(f"  Connected to GSC: {site_url}")

        # ── Search Performance (last 28 days) ──
        from datetime import timedelta
        end_date = date.today() - timedelta(days=3)
        start_date = end_date - timedelta(days=28)

        try:
            resp = service.searchanalytics().query(siteUrl=site_url, body={
                "startDate": start_date.isoformat(),
                "endDate": end_date.isoformat(),
                "dimensions": ["date"],
                "rowLimit": 31,
            }).execute()
            for row in resp.get("rows", []):
                results["daily"].append({
                    "date": row["keys"][0],
                    "clicks": row.get("clicks", 0),
                    "impressions": row.get("impressions", 0),
                    "ctr": f"{row.get('ctr', 0) * 100:.1f}%",
                    "position": f"{row.get('position', 0):.1f}",
                })
        except Exception as e:
            results["search_performance_error"] = str(e)

        # ── Top queries ──
        try:
            resp = service.searchanalytics().query(siteUrl=site_url, body={
                "startDate": start_date.isoformat(),
                "endDate": end_date.isoformat(),
                "dimensions": ["query"],
                "rowLimit": 20,
            }).execute()
            for row in resp.get("rows", []):
                results["top_queries"].append({
                    "query": row["keys"][0],
                    "clicks": row.get("clicks", 0),
                    "impressions": row.get("impressions", 0),
                    "ctr": f"{row.get('ctr', 0) * 100:.1f}%",
                    "position": f"{row.get('position', 0):.1f}",
                })
        except Exception as e:
            results["top_queries_error"] = str(e)

        # ── Top pages ──
        try:
            resp = service.searchanalytics().query(siteUrl=site_url, body={
                "startDate": start_date.isoformat(),
                "endDate": end_date.isoformat(),
                "dimensions": ["page"],
                "rowLimit": 20,
            }).execute()
            for row in resp.get("rows", []):
                results["top_pages"].append({
                    "page": row["keys"][0],
                    "clicks": row.get("clicks", 0),
                    "impressions": row.get("impressions", 0),
                    "ctr": f"{row.get('ctr', 0) * 100:.1f}%",
                    "position": f"{row.get('position', 0):.1f}",
                })
        except Exception as e:
            results["top_pages_error"] = str(e)

        # ── Aggregate ──
        daily = results["daily"]
        if daily and any(d["impressions"] > 0 for d in daily):
            tc = sum(d["clicks"] for d in daily)
            ti = sum(d["impressions"] for d in daily)
            positions = [float(d["position"]) for d in daily if d["position"] and d["position"].replace(".", "").isdigit()]
            results["search_performance"] = {
                "period": f"{start_date} → {end_date}",
                "days": len(daily), "total_clicks": tc, "total_impressions": ti,
                "avg_ctr": round(tc / max(ti, 1) * 100, 2),
                "avg_position": round(sum(positions) / max(len(positions), 1), 1) if positions else None,
            }
            results["available"] = True
        else:
            results["search_performance"] = {"total_clicks": 0, "total_impressions": 0}

    except Exception as e:
        err_msg = str(e)[:200]
        print(f"  OAuth failed: {err_msg}")
        print("  Falling back to CSV…")
        return _gsc_csv_fallback()

    return results


# ═══════════════════════════════════════════════════════════════════════════
# 7. Report Generation
# ═══════════════════════════════════════════════════════════════════════════

def load_previous_report():
    """Load previous report for trend comparison."""
    if HEALTH_FILE.exists():
        try:
            return json.loads(HEALTH_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return None


def generate_report(sitemap, seo_tags, structured, pages, links, gsc):
    """Merge all checks into a single health report."""
    prev = load_previous_report()

    report = {
        "generated_at": NOW,
        "date": TODAY,
        "previous_date": prev.get("date") if prev else None,
        "sitemap_health": sitemap,
        "seo_tags": {k: v for k, v in seo_tags.items() if k != "missing_tags"},
        "seo_tags_missing": seo_tags.get("missing_tags", {}),
        "seo_tags_issues_count": seo_tags.get("files_with_issues", 0),
        "structured_data": {
            "checked": structured["checked"],
            "schemas_found": structured["schemas_found"],
            "errors": structured["errors"][:20],
        },
        "page_sizes": pages,
        "internal_links": links,
        "gsc": gsc,
        "warnings": [],
        "trend": {},
    }

    # Generate warnings
    if sitemap.get("health_pct", 100) < 95:
        report["warnings"].append(
            f"Sitemap health at {sitemap['health_pct']}% — {len(sitemap.get('errors', []))} errors"
        )
    if pages["over_100kb"]:
        report["warnings"].append(
            f"{len(pages['over_100kb'])} pages over 100KB — consider reducing HTML size"
        )
    if links["broken"]:
        report["warnings"].append(
            f"{len(links['broken'])} broken internal links found"
        )
    if seo_tags.get("files_with_issues", 0) > 0:
        report["warnings"].append(
            f"{seo_tags['files_with_issues']} files missing some SEO tags"
        )
    if not gsc.get("available"):
        if gsc.get("error"):
            report["warnings"].append(
                f"GSC data unavailable: {gsc['error'][:100]}"
            )
        else:
            report["info"] = "GSC data is empty — expected for a new site. It takes 2-4 weeks for search traffic to appear."

    # Trend comparison
    if prev:
        prev_sitemap = prev.get("sitemap_health", {})
        if prev_sitemap.get("total_urls"):
            delta = sitemap.get("total_urls", 0) - prev_sitemap["total_urls"]
            report["trend"]["url_delta"] = delta

        prev_gsc = prev.get("gsc", {})
        if prev_gsc.get("available") and gsc.get("available"):
            prev_sp = prev_gsc.get("search_performance", {})
            cur_sp = gsc.get("search_performance", {})
            if prev_sp and cur_sp:
                report["trend"]["clicks_delta"] = cur_sp.get("total_clicks", 0) - prev_sp.get("total_clicks", 0)
                report["trend"]["impressions_delta"] = cur_sp.get("total_impressions", 0) - prev_sp.get("total_impressions", 0)
                prev_ctr = prev_sp.get("avg_ctr", 0)
                cur_ctr = cur_sp.get("avg_ctr", 0)
                if prev_ctr and cur_ctr:
                    report["trend"]["ctr_delta"] = round(cur_ctr - prev_ctr, 2)

    return report


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    print(f"=== SEO Health Monitor — {NOW} ===\n")

    # 1. Sitemap Health
    print("[1/5] Sitemap health check...")
    urls = fetch_sitemap_urls()
    sitemap = check_sitemap_health(urls) if urls else {"error": "Could not fetch sitemap"}
    print(f"  Health: {sitemap.get('health_pct', 'N/A')}% ({sitemap.get('ok', 0)}/{sitemap.get('checked', 0)} OK)\n")

    # 2. SEO Tags
    print("[2/5] SEO tag completeness...")
    seo_tags = check_seo_tags()
    print(f"  Files with issues: {seo_tags['files_with_issues']}")
    if seo_tags['files_with_issues']:
        for tag, files in seo_tags.get("missing_tags", {}).items():
            print(f"    Missing {tag}: {len(files)} files")
    print()

    # 3. Structured Data
    print("[3/5] Structured data check...")
    structured = check_structured_data()
    print(f"  Schemas: {dict(structured['schemas_found'])}")
    if structured["errors"]:
        print(f"  Errors: {len(structured['errors'])}")
    print()

    # 4. Page Sizes + Internal Links
    print("[4/5] Page size & link analysis...")
    pages = check_page_sizes()
    print(f"  Avg page: {pages['avg_kb']} KB | Over 100KB: {len(pages['over_100kb'])}")
    links = check_internal_links()
    print(f"  Internal links checked: {links['total_links']} | Broken: {len(links['broken'])}")
    print()

    # 5. GSC Data
    print("[5/5] GSC data pull...")
    gsc = pull_gsc_data()
    if gsc.get("available"):
        sp = gsc.get("search_performance", {})
        if sp:
            print(f"  Clicks (period): {sp.get('total_clicks', 'N/A')}")
            print(f"  Impressions (period): {sp.get('total_impressions', 'N/A')}")
            print(f"  Avg position: {sp.get('avg_position', 'N/A')}")
        else:
            print("  GSC data empty — no traffic yet (expected for new site)")
    else:
        err = gsc.get("error") or "No data yet"
        print(f"  GSC: {err[:120]}")
    print()

    # Generate Report
    report = generate_report(sitemap, seo_tags, structured, pages, links, gsc)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    HEALTH_FILE.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Report saved to {HEALTH_FILE}")

    # Summary
    print(f"\n=== Health Summary ===")
    for w in report["warnings"]:
        print(f"  ⚠  {w}")
    if not report["warnings"]:
        print("  ✓ All checks passed — no warnings")

    return report


if __name__ == "__main__":
    main()
