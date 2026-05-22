#!/usr/bin/env python3
"""
Analyze Google Search Console data for aidev.fit.

Pulls search performance data from GSC API for the last 28 days
and generates a summary report: top queries, top pages, trends.
"""

import json, sys
from pathlib import Path
from datetime import date, timedelta

ROOT = Path(__file__).resolve().parent.parent
TOKEN_FILE = ROOT / "data" / "gsc-token.json"
SITE_URL = "https://aidev.fit/"

DAYS = 28
END = date.today()
START = END - timedelta(days=DAYS)


def gsc_request(service, body, row_limit=25):
    """Run a GSC searchAnalytics.query with error handling."""
    try:
        return service.searchanalytics().query(siteUrl=SITE_URL, body=body).execute()
    except Exception as e:
        print(f"  GSC API error: {e}")
        return None


def print_table(rows, headers, fields):
    """Print aligned table from rows of dicts."""
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, f in enumerate(fields):
            val = str(row.get(f, ""))
            col_widths[i] = max(col_widths[i], len(val))

    sep = "  ".join("-" * w for w in col_widths)
    header_line = "  ".join(h.ljust(w) for h, w in zip(headers, col_widths))
    print(f"  {header_line}")
    print(f"  {sep}")
    for row in rows:
        vals = "  ".join(str(row.get(f, "")).ljust(w) for f, w in zip(fields, col_widths))
        print(f"  {vals}")
    print()


def main():
    if not TOKEN_FILE.exists():
        print("ERROR: GSC token not found. Run gsc_auth_setup.py first.")
        return 1

    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE))
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    service = build("searchconsole", "v1", credentials=creds)

    print(f"=== GSC Report: {START} to {END} ({DAYS} days) ===\n")

    # ── 1. Aggregate totals ──
    totals_body = {
        "startDate": START.isoformat(),
        "endDate": END.isoformat(),
        "dimensions": [],
    }
    totals = gsc_request(service, totals_body)
    if totals and totals.get("rows"):
        r = totals["rows"][0]
        print(f"  Total clicks:      {r['clicks']:>8,}")
        print(f"  Total impressions: {r['impressions']:>8,}")
        print(f"  Avg CTR:           {r['ctr']*100:>7.2f}%")
        print(f"  Avg position:      {r['position']:>7.1f}")
        print()

    # ── 2. Top queries ──
    print("[Top queries by clicks]")
    q_body = {
        "startDate": START.isoformat(),
        "endDate": END.isoformat(),
        "dimensions": ["query"],
        "rowLimit": 15,
        "orderBy": [{"fieldName": "clicks", "sortOrder": "DESCENDING"}],
    }
    q_rows = gsc_request(service, q_body)
    if q_rows and q_rows.get("rows"):
        table = []
        for r in q_rows["rows"]:
            table.append({
                "query": r["keys"][0][:50],
                "clicks": r["clicks"],
                "impressions": r["impressions"],
                "ctr": f"{r['ctr']*100:.1f}%",
                "pos": f"{r['position']:.1f}",
            })
        print_table(table, ["Query", "Clicks", "Impr.", "CTR", "Pos"],
                    ["query", "clicks", "impressions", "ctr", "pos"])

    # ── 3. Top pages ──
    print("[Top pages by clicks]")
    p_body = {
        "startDate": START.isoformat(),
        "endDate": END.isoformat(),
        "dimensions": ["page"],
        "rowLimit": 15,
        "orderBy": [{"fieldName": "clicks", "sortOrder": "DESCENDING"}],
    }
    p_rows = gsc_request(service, p_body)
    if p_rows and p_rows.get("rows"):
        table = []
        for r in p_rows["rows"]:
            page = r["keys"][0].replace(SITE_URL, "/")[:55]
            table.append({
                "page": page,
                "clicks": r["clicks"],
                "impressions": r["impressions"],
                "ctr": f"{r['ctr']*100:.1f}%",
                "pos": f"{r['position']:.1f}",
            })
        print_table(table, ["Page", "Clicks", "Impr.", "CTR", "Pos"],
                    ["page", "clicks", "impressions", "ctr", "pos"])

    # ── 4. Daily trend ──
    print("[Daily trend (clicks)]")
    d_body = {
        "startDate": START.isoformat(),
        "endDate": END.isoformat(),
        "dimensions": ["date"],
        "rowLimit": DAYS,
        "orderBy": [{"fieldName": "date", "sortOrder": "ASCENDING"}],
    }
    d_rows = gsc_request(service, d_body)
    if d_rows and d_rows.get("rows"):
        dates = [r["keys"][0][5:] for r in d_rows["rows"]]  # MM-DD
        clicks = [r["clicks"] for r in d_rows["rows"]]
        # Mini sparkline — show min/max/avg
        print(f"  Date range: {dates[0]} to {dates[-1]}")
        print(f"  Min daily clicks: {min(clicks)}  Max: {max(clicks)}  Avg: {sum(clicks)//len(clicks)}")
        # Show last 7 days
        print(f"  Last 7 days: {' | '.join(f'{d}:{c}' for d,c in zip(dates[-7:], clicks[-7:]))}")
        print()

    # ── 5. Country breakdown ──
    print("[Top countries by clicks]")
    c_body = {
        "startDate": START.isoformat(),
        "endDate": END.isoformat(),
        "dimensions": ["country"],
        "rowLimit": 10,
        "orderBy": [{"fieldName": "clicks", "sortOrder": "DESCENDING"}],
    }
    c_rows = gsc_request(service, c_body)
    if c_rows and c_rows.get("rows"):
        table = []
        for r in c_rows["rows"]:
            table.append({
                "country": r["keys"][0].upper(),
                "clicks": r["clicks"],
                "impressions": r["impressions"],
                "ctr": f"{r['ctr']*100:.1f}%",
            })
        print_table(table, ["Country", "Clicks", "Impr.", "CTR"],
                    ["country", "clicks", "impressions", "ctr"])

    # ── 6. Device breakdown ──
    print("[Device breakdown]")
    dev_body = {
        "startDate": START.isoformat(),
        "endDate": END.isoformat(),
        "dimensions": ["device"],
        "rowLimit": 5,
        "orderBy": [{"fieldName": "clicks", "sortOrder": "DESCENDING"}],
    }
    dev_rows = gsc_request(service, dev_body)
    if dev_rows and dev_rows.get("rows"):
        total_clicks = sum(r["clicks"] for r in dev_rows["rows"])
        table = []
        for r in dev_rows["rows"]:
            pct = r["clicks"] / total_clicks * 100 if total_clicks else 0
            table.append({
                "device": r["keys"][0],
                "clicks": r["clicks"],
                "pct": f"{pct:.1f}%",
                "ctr": f"{r['ctr']*100:.1f}%",
                "pos": f"{r['position']:.1f}",
            })
        print_table(table, ["Device", "Clicks", "%", "CTR", "Pos"],
                    ["device", "clicks", "pct", "ctr", "pos"])

    print("=== End of GSC Report ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
