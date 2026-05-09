#!/usr/bin/env python3
"""
Build cross-platform identity mapping for schema.org sameAs.
Queries Dev.to API and reads Hashnode tracking to build
data/sameas-urls.json — used by gen_en_site.py for Article schema.
"""
import _ssl_compat  # noqa
import json, os, sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEVTO_KEY_PATH = ROOT / ".devto-key"
HASHNODE_TRACK = ROOT / "data" / "hashnode-published.json"
OUTPUT = ROOT / "data" / "sameas-urls.json"

# ── Dev.to published articles ─────────────────────────────────────────

def get_devto_articles():
    """Query Dev.to API for published articles. Returns {slug: devto_url}."""
    if not DEVTO_KEY_PATH.exists():
        print("  Dev.to: no API key file, skipping")
        return {}

    token = DEVTO_KEY_PATH.read_text().strip()
    result = {}
    page = 1

    while True:
        req = Request(
            f"https://dev.to/api/articles/me?page={page}&per_page=100",
            headers={"api-key": token, "User-Agent": "SourceHub/1.0"}
        )
        try:
            resp = urlopen(req, timeout=30)
            articles = json.loads(resp.read().decode())
        except HTTPError as e:
            print(f"  Dev.to API error: {e.code}")
            break
        except Exception as e:
            print(f"  Dev.to request failed: {e}")
            break

        if not articles:
            break

        for art in articles:
            canon = art.get("canonical_url", "")
            if "dingjiu1989-hue.github.io" in canon:
                slug = canon.split("/")[-1].replace(".html", "")
                result[slug] = art["url"]

        page += 1
        if len(articles) < 100:
            break

    print(f"  Dev.to: {len(result)} published articles with URLs")
    return result


# ── Hashnode published articles ──────────────────────────────────────

def get_hashnode_articles():
    """Read Hashnode tracking file. Returns {slug: hashnode_url}."""
    if not HASHNODE_TRACK.exists():
        print("  Hashnode: no tracking file, skipping")
        return {}

    data = json.loads(HASHNODE_TRACK.read_text())
    result = {}
    if isinstance(data, dict):
        # New format: {slug: url}
        for slug, url in data.items():
            if url:
                result[slug] = url
    elif isinstance(data, list):
        # Legacy format: list of slugs (no URLs)
        print("  Hashnode: legacy format, no URLs available")
        return {}

    print(f"  Hashnode: {len(result)} published with URLs")
    return result


# ── Build sameAs mapping ─────────────────────────────────────────────

def build():
    devto = get_devto_articles()
    hashnode = get_hashnode_articles()

    sameas = {}
    for slug, devto_url in devto.items():
        urls = []
        if devto_url:
            urls.append(devto_url)
        # TODO: add hashnode URLs once tracking includes them
        # if slug in hashnode and hashnode[slug]:
        #     urls.append(hashnode[slug])
        if urls:
            sameas[slug] = urls

    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps(sameas, indent=2, ensure_ascii=False))
    total = len(sameas)
    url_count = sum(len(v) for v in sameas.values())
    print(f"  Wrote {total} entries ({url_count} URLs) -> {OUTPUT}")


if __name__ == "__main__":
    build()
