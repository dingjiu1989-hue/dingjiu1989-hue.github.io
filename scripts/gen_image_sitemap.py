#!/usr/bin/env python3
"""Generate /images/sitemap.xml — image sitemap for all article cover images.

Google Images and multimodal AI crawlers (GPT-4V, Claude Vision) use image
sitemaps to discover and index images. Each article has a 1200x630 cover PNG.
"""

import json
from pathlib import Path
from datetime import date
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://dingjiu1989-hue.github.io"
TODAY = date.today().isoformat()

EN_ARTICLES = ROOT / "en" / "articles.json"
CN_ARTICLES = ROOT / "articles.json"


def gen_image_sitemap():
    urls = []

    # English articles
    if EN_ARTICLES.exists():
        en_data = json.loads(EN_ARTICLES.read_text(encoding="utf-8"))
        for board in en_data["boards"]:
            for art in board["posts"]:
                slug = art["slug"]
                board_id = board["id"]
                page_url = f"{BASE}/en/{board_id}/{slug}.html"
                img_url = f"{BASE}/images/covers/en/{board_id}/{slug}.png"
                title = art.get("title", "")
                urls.append((page_url, img_url, title))

    # Chinese articles
    if CN_ARTICLES.exists():
        cn_data = json.loads(CN_ARTICLES.read_text(encoding="utf-8"))
        for board in cn_data.get("boards", []):
            for art in board.get("posts", []):
                slug = art["slug"]
                board_id = board["id"]
                page_url = f"{BASE}/{board_id}/{slug}.html"
                img_url = f"{BASE}/images/covers/zh/{board_id}/{slug}.png"
                title = art.get("title", "")
                urls.append((page_url, img_url, title))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
    ]

    for page_url, img_url, title in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{escape(page_url)}</loc>")
        lines.append("    <image:image>")
        lines.append(f"      <image:loc>{escape(img_url)}</image:loc>")
        if title:
            lines.append(f"      <image:title>{escape(title)}</image:title>")
            lines.append(f"      <image:caption>{escape(f'Cover image for: {title}')}</image:caption>")
        lines.append("    </image:image>")
        lines.append("  </url>")

    lines.append("</urlset>")

    content = "\n".join(lines)
    out_path = ROOT / "images" / "sitemap.xml"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    print(f"  Image sitemap: {len(urls)} images -> {out_path}")


if __name__ == "__main__":
    print("=== Image Sitemap Generator ===\n")
    gen_image_sitemap()
    print("\nDone.")
