#!/usr/bin/env python3
"""Weekly maintenance: refresh sitemap, RSS, and run health check.
Keeps freshness signals active for search crawlers.
"""
import subprocess, sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent

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

def main():
    print(f"Weekly Maintenance — {datetime.now().isoformat()}")
    ok = True

    ok &= run("python3 scripts/add_en_seo.py", "Update sitemap + hreflang")
    ok &= run("python3 scripts/gen_rss.py", "Refresh RSS feeds")
    ok &= run("python3 scripts/monitor_seo.py", "SEO health check")

    # Check GSC sitemap status
    print(f"\n{'='*60}")
    print(f"  Reminder: Check GSC sitemap status")
    print(f"  https://search.google.com/search-console/sitemaps")
    print(f"{'='*60}")

    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
