#!/usr/bin/env python3
"""Weekly maintenance: refresh sitemap, RSS, health check, and ping GSC.
Keeps freshness signals active for search crawlers.
"""
import subprocess, sys, json
from pathlib import Path
from datetime import datetime, timezone as tz

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://dingjiu1989-hue.github.io"

def run(cmd, desc):
    print(f"\n{'='*60}")
    print(f"  {desc}")
    print(f"{'='*60}")
    r = subprocess.run(cmd, shell=True, cwd=str(ROOT), capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  ERROR: {r.stderr[-300:]}")
    else:
        print(r.stdout[-500:] if len(r.stdout) > 500 else r.stdout)
    return r.returncode == 0

def resubmit_sitemaps():
    """Resubmit sitemap + RSS feeds to GSC to trigger recrawl."""
    TOKEN_FILE = ROOT / "data" / "gsc-token.json"
    if not TOKEN_FILE.exists():
        print("  No GSC token, skipping sitemap resubmission")
        return True

    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build

        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), ["https://www.googleapis.com/auth/webmasters"])
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())

        service = build("searchconsole", "v1", credentials=creds)

        feeds = [
            f"{SITE}/sitemap.xml",
            f"{SITE}/en/feed.xml",
            f"{SITE}/feed.xml",
        ]
        ok = True
        for feed in feeds:
            try:
                service.sitemaps().submit(siteUrl=SITE + "/", feedpath=feed).execute()
                print(f"  Submitted: {feed}")
            except Exception as e:
                print(f"  Submit error ({feed}): {e}")
                ok = False
        return ok
    except Exception as e:
        print(f"  GSC API error: {e}")
        return False

def main():
    print(f"Weekly Maintenance — {datetime.now(tz.utc).isoformat()}")
    ok = True

    ok &= run("python3 scripts/add_en_seo.py", "Update sitemap + hreflang")
    ok &= run("python3 scripts/gen_rss.py", "Refresh RSS feeds")
    ok &= run("python3 scripts/gen_ai_friendly.py", "AI-friendly artifacts (llms.txt + MD + robots.txt)")
    ok &= run("python3 scripts/monitor_seo.py", "SEO health check")
    ok &= resubmit_sitemaps()

    # Read latest health report for summary
    health_file = ROOT / "data" / "seo-health.json"
    if health_file.exists():
        report = json.loads(health_file.read_text(encoding="utf-8"))
        warnings = report.get("warnings", [])
        if warnings:
            print(f"\n  WARNINGS: {warnings}")
        else:
            print(f"\n  All systems healthy")

    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
