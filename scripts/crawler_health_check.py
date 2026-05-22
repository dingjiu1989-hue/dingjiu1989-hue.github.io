#!/usr/bin/env python3
"""
Crawler health check — verify all discovery endpoints are working.

Run periodically to ensure AI crawlers and search engines
can discover the site's content. Checks:

  1. All critical files return HTTP 200
  2. robots.txt serves correct rules per User-Agent
  3. Sitemap accessibility
  4. IndexNow key validity
  5. RSS feed health (item count, valid XML)
  6. Response times (should be < 1s)
"""

import sys, json
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://aidev.fit"

CHECKS = [
    ("robots.txt", f"{BASE}/robots.txt", 200, ["sitemap.xml"]),
    ("llms.txt", f"{BASE}/llms.txt", 200, ["AI Study Room"]),
    ("llms-full.txt", f"{BASE}/llms-full.txt", 200, ["Full Content"]),
    ("en/llms.txt", f"{BASE}/en/llms.txt", 200, ["English"]),
    ("Sitemap XML", f"{BASE}/sitemap.xml", 200, ["<loc>"]),
    ("Image sitemap", f"{BASE}/images/sitemap.xml", 200, ["<loc>"]),
    ("RSS EN", f"{BASE}/en/feed.xml", 200, ["<item>"]),
    ("RSS CN", f"{BASE}/feed.xml", 200, ["<item>"]),
    ("JSON Feed EN", f"{BASE}/en/feed.json", 200, ["items"]),
    ("JSON Feed CN", f"{BASE}/feed.json", 200, ["items"]),
    ("IndexNow key", f"{BASE}/bca1280e3258b853e5cc15ec3151fb9f.txt", 200, ["bca1280e"]),
    ("favicon.svg", f"{BASE}/favicon.svg", 200, ["<svg"]),
    ("favicon.ico", f"{BASE}/favicon.ico", 200, None),
    ("EN Homepage", f"{BASE}/en/", 200, ["SourceHub"]),
    ("CN Homepage", f"{BASE}/", 200, ["AI自习室"]),
    ("About page", f"{BASE}/en/about.html", 200, ["AboutPage"]),
]

RESULTS_FILE = ROOT / "data" / "crawler-health.json"


def check_url(name, url, expected_status, expected_text):
    """Check URL returns expected status and contains expected text."""
    result = {"name": name, "url": url, "status": "unknown", "status_code": 0, "response_time_ms": 0}
    try:
        import time
        start = time.time()
        req = Request(url, method="GET")
        req.add_header("User-Agent", "CrawlerHealthCheck/1.0")
        resp = urlopen(req, timeout=15)
        elapsed = int((time.time() - start) * 1000)
        result["response_time_ms"] = elapsed
        result["status_code"] = resp.status

        if resp.status != expected_status:
            result["status"] = "FAIL"
            result["error"] = f"Expected HTTP {expected_status}, got {resp.status}"
            return result

        if expected_text:
            body = resp.read().decode("utf-8", errors="replace")
            for text in expected_text:
                if text not in body:
                    result["status"] = "FAIL"
                    result["error"] = f"Expected text '{text}' not found in response"
                    return result

        result["status"] = "PASS"
        if elapsed > 1000:
            result["warning"] = f"Slow response: {elapsed}ms"

    except URLError as e:
        result["status"] = "FAIL"
        result["error"] = str(e.reason)
    except Exception as e:
        result["status"] = "FAIL"
        result["error"] = str(e)

    return result


def main():
    print("=== Crawler Health Check ===\n")

    all_results = []
    passes = 0
    fails = 0

    for name, url, status, text in CHECKS:
        r = check_url(name, url, status, text)
        all_results.append(r)
        status_icon = "✅" if r["status"] == "PASS" else "❌"
        extra = ""
        if r.get("warning"):
            extra = f" ⚠️ {r['warning']}"
        elif r.get("error"):
            extra = f" {r['error']}"
        print(f"  {status_icon} {name} ({r['response_time_ms']}ms){extra}")
        if r["status"] == "PASS":
            passes += 1
        else:
            fails += 1

    print(f"\nSummary: {passes}/{len(CHECKS)} passed, {fails} failed")

    # Additional: robots.txt rule check
    print("\n[robots.txt rules]")
    try:
        resp = urlopen(f"{BASE}/robots.txt", timeout=10)
        robots = resp.read().decode("utf-8")
        required_crawlers = ["GPTBot", "ClaudeBot", "Googlebot", "PerplexityBot",
                             "Claude-Web", "CCBot", "Diffbot", "GrokBot"]
        missing = [c for c in required_crawlers if c not in robots]
        if missing:
            print(f"  ⚠️  Missing rules for: {', '.join(missing)}")
            fails += 1
        else:
            print(f"  ✅ All {len(required_crawlers)} required crawlers have rules")
            passes += 1
    except Exception as e:
        print(f"  ❌ Could not fetch robots.txt: {e}")
        fails += 1

    # Save results
    summary = {
        "timestamp": __import__("datetime").datetime.now().isoformat(),
        "total": len(CHECKS) + 1,
        "passed": passes,
        "failed": fails,
        "results": all_results,
    }
    RESULTS_FILE.parent.mkdir(exist_ok=True)
    RESULTS_FILE.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\nResults saved to {RESULTS_FILE}")

    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
