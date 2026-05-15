#!/usr/bin/env python3
"""
Bing Webmaster Tools sync: submit new URLs, pull search performance & crawl data.

Bing's index powers ChatGPT, Copilot, DuckDuckGo, and other AI search products.
This runs daily to keep Bing aware of all content.

API: https://ssl.bing.com/webmaster/api.svc/json/<endpoint>?apikey=KEY
Quota: 100 URLs/day, 1700/month via SubmitUrl
"""

import json, os, sys, time, urllib.request, urllib.parse, urllib.error
from pathlib import Path
from datetime import date, datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://dingjiu1989-hue.github.io/"
def _load_api_key():
    key = os.environ.get("BING_WEBMASTER_KEY", "")
    if key:
        return key
    key_file = ROOT / "data" / ".bing-key"
    if key_file.exists():
        return key_file.read_text(encoding="utf-8").strip()
    return ""

API_KEY = _load_api_key()
BASE = "https://ssl.bing.com/webmaster/api.svc/json"
DATA_DIR = ROOT / "data"
TRACKING_FILE = DATA_DIR / "bing-submitted.json"


def api_get(endpoint, params=None):
    url = f"{BASE}/{endpoint}?apikey={API_KEY}"
    if params:
        url += "&" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=20) as resp:
            return json.loads(resp.read())
    except Exception as e:
        return {"error": str(e)[:200]}


def api_post(endpoint, data):
    url = f"{BASE}/{endpoint}?apikey={API_KEY}"
    body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=body,
        headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        error_data = {}
        try:
            error_data = json.loads(body)
        except Exception:
            pass
        return {"error": error_data.get("Message", str(e)), "http_error_body": body[:300]}
    except Exception as e:
        return {"error": str(e)[:200]}


def load_tracking():
    if TRACKING_FILE.exists():
        return json.loads(TRACKING_FILE.read_text(encoding="utf-8"))
    return {"submitted": {}, "last_run": None}


def save_tracking(data):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    TRACKING_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def submit_new_urls():
    """Submit up to 90 URLs/day (leaving 10 buffer for manual use)."""
    tracking = load_tracking()
    submitted = tracking.get("submitted", {})
    today = date.today().isoformat()

    # Count today's submissions
    today_count = sum(1 for ts in submitted.values() if ts.startswith(today))
    daily_limit = 90
    remaining = daily_limit - today_count
    if remaining <= 0:
        print(f"  Daily quota reached ({today_count}/{daily_limit}), skipping")
        return 0

    # Collect all article URLs
    en_articles = ROOT / "en" / "articles.json"
    if not en_articles.exists():
        print("  No en/articles.json found")
        return 0

    en_data = json.loads(en_articles.read_text(encoding="utf-8"))
    all_urls = []
    for board in en_data["boards"]:
        for art in board["posts"]:
            all_urls.append(f"{SITE}en/{board['id']}/{art['slug']}.html")

    # Chinese articles
    cn_articles = ROOT / "articles.json"
    if cn_articles.exists():
        cn_data = json.loads(cn_articles.read_text(encoding="utf-8"))
        for board in cn_data.get("boards", []):
            for art in board.get("posts", []):
                all_urls.append(f"{SITE}{board['id']}/{art['slug']}.html")

    # Also submit key SEO pages
    key_pages = [
        f"{SITE}en/",
        f"{SITE}",
        f"{SITE}sitemap.xml",
        f"{SITE}images/sitemap.xml",
        f"{SITE}robots.txt",
        f"{SITE}llms.txt",
        f"{SITE}llms-full.txt",
        f"{SITE}en/feed.xml",
        f"{SITE}feed.xml",
        f"{SITE}en/feed.json",
        f"{SITE}feed.json",
    ]
    for board_id in ["ai", "tech", "tools", "sidehustle", "compare", "security", "database", "architecture"]:
        key_pages.append(f"{SITE}en/{board_id}/")

    all_urls = key_pages + all_urls

    # Filter already submitted
    new_urls = [u for u in all_urls if u not in submitted][:remaining]

    if not new_urls:
        print(f"  All URLs already submitted ({len(submitted)} total)")
        return 0

    print(f"  Submitting {len(new_urls)} new URLs (quota: {remaining})...")
    ok = 0
    quota_exceeded = False
    now = datetime.now(timezone.utc).isoformat()
    for url in new_urls:
        resp = api_post("SubmitUrl", {"siteUrl": SITE, "url": url})
        if "error" not in resp:
            ok += 1
            submitted[url] = now
        elif "quota" in str(resp.get("http_error_body", "")).lower() or "quota" in str(resp).lower():
            quota_exceeded = True
            print(f"  Daily quota reached, stopping ({ok} submitted this run)")
            break
        time.sleep(0.15)

    tracking["submitted"] = submitted
    tracking["last_run"] = now
    save_tracking(tracking)
    if not quota_exceeded:
        print(f"  {ok}/{len(new_urls)} submitted, {len(submitted)} total tracked")
    return ok


def pull_all_data():
    """Pull all available data from Bing Webmaster API.
    Saves to data/bing-stats.json for historical tracking.
    """
    now = datetime.now(timezone.utc).isoformat()
    stats = {
        "pulled_at": now,
        "date": date.today().isoformat(),
        "endpoints": {},
    }

    # All known working endpoints
    endpoints = {
        "rank_traffic": ("GetRankAndTrafficStats", {"siteUrl": SITE}),
        "keyword_stats": ("GetKeywordStats", {"siteUrl": SITE}),
        "crawl_settings": ("GetCrawlSettings", {"siteUrl": SITE}),
        "crawl_issues": ("GetCrawlIssues", {"siteUrl": SITE}),
        "submission_quota": ("GetUrlSubmissionQuota", {"siteUrl": SITE}),
        "sitemaps": ("GetSitemapList", {"siteUrl": SITE}),
    }

    for name, (endpoint, params) in endpoints.items():
        resp = api_get(endpoint, params)
        d = resp.get("d", None)
        err = resp.get("error") or resp.get("http_error")
        if err:
            stats["endpoints"][name] = {"status": "error", "error": str(err)[:200]}
        elif d is not None:
            if isinstance(d, list):
                stats["endpoints"][name] = {"status": "ok", "count": len(d), "data": d}
            elif isinstance(d, dict):
                stats["endpoints"][name] = {"status": "ok", "data": d}
            else:
                stats["endpoints"][name] = {"status": "ok", "data": d}
        else:
            stats["endpoints"][name] = {"status": "unknown", "raw": json.dumps(resp)[:500]}

    # Load previous stats for trend comparison
    stats_file = DATA_DIR / "bing-stats.json"
    previous = None
    if stats_file.exists():
        try:
            previous = json.loads(stats_file.read_text(encoding="utf-8"))
        except Exception:
            pass
    stats["previous_date"] = previous.get("date") if previous else None

    # Save
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    stats_file.write_text(json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8")

    return stats


def print_data_summary(stats):
    """Print a human-readable summary of pulled data."""
    ep = stats.get("endpoints", {})

    # Quota
    quota = ep.get("submission_quota", {}).get("data", {})
    if isinstance(quota, dict):
        print(f"  URL Quota: {quota.get('DailyQuota', '?')}/day, {quota.get('MonthlyQuota','?')}/month")

    # Sitemaps
    sm = ep.get("sitemaps", {})
    if sm.get("status") == "ok" and isinstance(sm.get("data"), list):
        print(f"  Sitemaps: {len(sm['data'])} registered")
        for s in sm["data"]:
            if isinstance(s, dict):
                print(f"    - {s.get('Url', s.get('url', '?'))[:80]}")

    # Rank & Traffic
    rt = ep.get("rank_traffic", {})
    if rt.get("status") == "ok":
        data = rt.get("data", [])
        if isinstance(data, list) and data:
            print(f"  Rank/Traffic: {len(data)} data points")
            for item in data[:5]:
                print(f"    {item}")
        else:
            print("  Rank/Traffic: no data yet (expected for new site)")

    # Keywords
    kw = ep.get("keyword_stats", {})
    if kw.get("status") == "ok":
        data = kw.get("data", [])
        if isinstance(data, list) and data:
            print(f"  Keywords: {len(data)} tracked")
            for item in data[:5]:
                print(f"    {item}")

    # Crawl
    cs = ep.get("crawl_settings", {})
    if cs.get("status") == "ok":
        print(f"  Crawl settings: {json.dumps(cs.get('data', {}))[:200]}")


def main():
    if not API_KEY:
        print("BING_WEBMASTER_KEY env var not set. Skipping Bing sync.")
        return 1

    print(f"=== Bing Webmaster Sync — {datetime.now(timezone.utc).isoformat()} ===\n")

    # 1. Submit new URLs
    print("[1/2] URL submission...")
    submit_new_urls()

    # 2. Pull all data
    print("\n[2/3] Pulling Bing data...")
    stats = pull_all_data()
    print_data_summary(stats)

    print("\nDone. Data saved to data/bing-stats.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
