#!/usr/bin/env python3
"""
Ping search engines and WebSub hub after site updates.

Called after maintenance to notify:
  - Google (sitemap ping → triggers recrawl)
  - Bing Webmaster (sitemap ping)
  - WebSub hub (PubSubHubbub → notifies RSS subscribers)
  - IndexNow (Bing/Yandex — reuse existing key)

This dramatically reduces the time between content updates and search engine discovery.
"""

import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://aidev.fit"
SITEMAP = f"{BASE}/sitemap.xml"
RSS_EN = f"{BASE}/en/feed.xml"
RSS_CN = f"{BASE}/feed.xml"
WEBS_HUB = "https://pubsubhubbub.appspot.com/"
INDEXNOW_KEY = "bca1280e3258b853e5cc15ec3151fb9f"


def ping(url, label, timeout=15):
    """GET ping — fire and forget."""
    try:
        req = Request(url, method="GET")
        req.add_header("User-Agent", "AidevFitPingBot/1.0")
        resp = urlopen(req, timeout=timeout)
        print(f"  {label}: HTTP {resp.status}")
        return True
    except URLError as e:
        code = getattr(e, "code", 0)
        msg = str(e.reason) if hasattr(e, "reason") else "timeout"
        print(f"  {label}: {code} {msg}")
        return False


def ping_post(url, data, label, content_type="application/x-www-form-urlencoded"):
    """POST ping with form data."""
    try:
        body = data.encode("utf-8") if isinstance(data, str) else data
        req = Request(url, data=body, method="POST")
        req.add_header("Content-Type", content_type)
        req.add_header("User-Agent", "AidevFitPingBot/1.0")
        resp = urlopen(req, timeout=15)
        print(f"  {label}: HTTP {resp.status}")
        return True
    except URLError as e:
        code = getattr(e, "code", 0)
        msg = str(e.reason) if hasattr(e, "reason") else "timeout"
        print(f"  {label}: {code} {msg}")
        return False


def ping_google():
    """Ping Google to recrawl sitemap."""
    url = f"https://www.google.com/ping?sitemap={SITEMAP}"
    return ping(url, "Google")


def ping_bing():
    """Ping Bing Webmaster with sitemap."""
    url = f"https://www.bing.com/webmaster/ping.aspx?siteMap={SITEMAP}"
    return ping(url, "Bing")


def ping_yandex():
    """Ping Yandex with sitemap."""
    url = f"https://webmaster.yandex.com/site/update?url={SITEMAP}"
    return ping(url, "Yandex")


def ping_websub_hub():
    """Notify WebSub hub of RSS feed updates.
    This triggers push notifications to all subscribers (including AI crawlers
    that monitor RSS feeds).
    """
    data_en = f"hub.url={RSS_EN}&hub.mode=publish"
    data_cn = f"hub.url={RSS_CN}&hub.mode=publish"
    r1 = ping_post(WEBS_HUB, data_en, "WebSub EN")
    r2 = ping_post(WEBS_HUB, data_cn, "WebSub CN")
    return r1 and r2


def ping_indexnow():
    """Trigger IndexNow for the full sitemap.
    Bing's index powers ChatGPT, Copilot, DuckDuckGo, and other AI search.
    """
    import json
    body = json.dumps({
        "host": "aidev.fit",
        "key": INDEXNOW_KEY,
        "keyLocation": f"https://aidev.fit/{INDEXNOW_KEY}.txt",
        "urlList": [SITEMAP],
    })
    return ping_post(
        "https://api.indexnow.org/indexnow",
        body,
        "IndexNow API",
        content_type="application/json; charset=utf-8",
    )


def main():
    print("=== Ping Search Engines ===")
    print(f"  Sitemap: {SITEMAP}\n")

    print("[1/6] Google sitemap ping")
    ping_google()

    print("[2/6] Bing sitemap ping")
    ping_bing()

    print("[3/6] Yandex sitemap ping")
    ping_yandex()

    print("[4/6] WebSub hub (RSS publish)")
    ping_websub_hub()

    print("[5/6] IndexNow (Bing/Yandex)")
    ping_indexnow()

    print("[6/6] Backup IndexNow endpoints")
    for ep in ["https://www.bing.com/indexnow", "https://yandex.com/indexnow"]:
        import json
        body = json.dumps({
            "host": "aidev.fit",
            "key": INDEXNOW_KEY,
            "keyLocation": f"https://aidev.fit/{INDEXNOW_KEY}.txt",
            "urlList": [SITEMAP],
        })
        ping_post(ep, body, f"IndexNow {ep.split('/')[2]}",
                  content_type="application/json; charset=utf-8")

    print("\nDone. Engines notified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
