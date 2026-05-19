#!/usr/bin/env python3
"""
Generate AI-friendly artifacts:
  1. /md/ — clean Markdown copies of every article (AI trains better on MD than HTML)
  2. /llms.txt — site index for AI crawlers (Anthropic/OpenAI/Perplexity read this first)
  3. /llms-full.txt — all content in one file (for training datasets)
  4. robots.txt — explicitly welcome AI crawlers
"""

import json, re, html2text
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://dingjiu1989-hue.github.io"
TODAY = date.today().isoformat()

MD_DIR = ROOT / "md"
EN_ARTICLES = ROOT / "en" / "articles.json"
CN_ARTICLES = ROOT / "articles.json"

h = html2text.HTML2Text()
h.body_width = 0
h.ignore_emphasis = False
h.ignore_links = False
h.ignore_images = True
h.protect_links = True
h.unicode_snob = True


# ── 1. Generate Markdown copies ────────────────────────────────────────

def extract_body(html):
    """Extract article body HTML and convert to Markdown."""
    m = re.search(r'<div class="article-body">(.*?)</article>', html, re.DOTALL)
    if not m:
        return None
    body_html = m.group(1)
    return h.handle(body_html).strip()


def gen_markdown_copies():
    """Generate /md/en/board/slug.md for every article.
    Uses a FRESH html2text instance (not the shared global) to avoid corruption
    from processing 850 articles sequentially.
    """
    import html2text as ht
    local_h = ht.HTML2Text()
    local_h.body_width = 0
    local_h.ignore_emphasis = False
    local_h.ignore_links = False
    local_h.ignore_images = True
    local_h.protect_links = True
    local_h.unicode_snob = True

    def _extract(html):
        m = re.search(r'<div class="article-body">(.*?)</article>', html, re.DOTALL)
        if not m:
            return None
        return local_h.handle(m.group(1)).strip()

    MD_DIR.mkdir(exist_ok=True)
    (MD_DIR / "en").mkdir(exist_ok=True)

    en_data = json.loads(EN_ARTICLES.read_text(encoding="utf-8"))
    total = 0

    for board in en_data["boards"]:
        (MD_DIR / "en" / board["id"]).mkdir(exist_ok=True)
        for art in board["posts"]:
            html_path = ROOT / "en" / board["id"] / f'{art["slug"]}.html'
            if not html_path.exists():
                continue
            html = html_path.read_text(encoding="utf-8")
            md_body = _extract(html)
            if not md_body:
                continue

            md = f"""---
title: "{art['title']}"
description: "{art.get('description', '')}"
date: {art['date']}
board: {board['id']}
url: {BASE}/en/{board['id']}/{art['slug']}.html
---

# {art['title']}

{md_body}
"""
            (MD_DIR / "en" / board["id"] / f'{art["slug"]}.md').write_text(md, encoding="utf-8")
            total += 1

    # Chinese articles (count existing markdown files — no ZH HTML generated)
    cn_md_dir = MD_DIR / "zh"
    cn_md_dir.mkdir(exist_ok=True)
    if CN_ARTICLES.exists():
        cn_data = json.loads(CN_ARTICLES.read_text(encoding="utf-8"))
        for board in cn_data.get("boards", []):
            (cn_md_dir / board["id"]).mkdir(exist_ok=True)
            for art in board.get("posts", []):
                path = cn_md_dir / board["id"] / f'{art["slug"]}.md'
                if path.exists():
                    total += 1

    print(f"  Markdown copies: {total} articles -> /md/")
    return total


# ── 2. Generate llms.txt ───────────────────────────────────────────────

BOARD_NAMES_EN = {
    "tech": "Tech Tutorials",
    "sidehustle": "Side Hustle Guides",
    "tools": "Tool Recommendations",
    "ai": "AI & LLM Tutorials",
    "compare": "Tool Comparisons",
    "security": "Security Guides",
    "database": "Database Tutorials",
    "architecture": "Architecture Patterns",
}
BOARD_NAMES_CN = {
    "tech": "技术教程",
    "sidehustle": "副业指南",
    "tools": "工具推荐",
    "ai": "AI教程",
    "compare": "对比评测",
    "security": "安全指南",
    "database": "数据库教程",
    "architecture": "架构模式",
}


def gen_llms_txt():
    """Generate /llms.txt — AI crawler site index."""
    en_data = json.loads(EN_ARTICLES.read_text(encoding="utf-8"))

    lines = [
        "# AI Study Room / AI自习室",
        f"> Bilingual developer resource: {sum(len(b['posts']) for b in en_data['boards'])} English + {sum(len(b.get('posts', [])) for b in json.loads(CN_ARTICLES.read_text(encoding='utf-8')).get('boards', [])) if CN_ARTICLES.exists() else 0} Chinese articles.",
        f"> Tech tutorials, tool comparisons, side-hustle guides, and AI development.",
        f"> Updated: {TODAY}",
        "",
        "## Quick Links",
        f"- Home (EN): {BASE}/en/",
        f"- Home (CN): {BASE}/",
        f"- Full content (EN): {BASE}/llms-full.txt",
        f"- Full content (CN): {BASE}/llms-full-cn.txt",
        f"- Sitemap: {BASE}/sitemap.xml",
        f"- RSS (EN): {BASE}/en/feed.xml",
        f"- RSS (CN): {BASE}/feed.xml",
        "",
    ]

    for board in en_data["boards"]:
        posts = board["posts"]
        if not posts:
            continue
        board_name = BOARD_NAMES_EN.get(board["id"], board["id"].title())
        lines.append(f"## {board_name} ({len(posts)} articles)")
        lines.append("")
        for art in posts:
            url = f"{BASE}/en/{board['id']}/{art['slug']}.html"
            md_url = f"{BASE}/md/en/{board['id']}/{art['slug']}.md"
            desc = art.get("description", "")[:120]
            lines.append(f"- [{art['title']}]({url}) — [md]({md_url})")
            if desc:
                lines.append(f"  {desc}")
        lines.append("")

    # Chinese articles
    if CN_ARTICLES.exists():
        cn_data = json.loads(CN_ARTICLES.read_text(encoding="utf-8"))
        lines.append("## 中文内容 / Chinese Content")
        lines.append("")
        for board in cn_data.get("boards", []):
            posts = board.get("posts", [])
            if not posts:
                continue
            board_name = BOARD_NAMES_CN.get(board["id"], board["id"])
            lines.append(f"### {board_name} ({len(posts)} 篇)")
            lines.append("")
            for art in posts:
                url = f"{BASE}/{board['id']}/{art['slug']}.html"
                md_url = f"{BASE}/md/zh/{board['id']}/{art['slug']}.md"
                desc = art.get("description", "")[:120]
                lines.append(f"- [{art['title']}]({url}) — [md]({md_url})")
                if desc:
                    lines.append(f"  {desc}")
            lines.append("")

    content = "\n".join(lines)
    (ROOT / "llms.txt").write_text(content, encoding="utf-8")
    print(f"  llms.txt: {content.count(chr(10))} lines written")

    # Also generate English-only llms.txt at /en/llms.txt
    gen_en_llms_txt(en_data)


def gen_en_llms_txt(en_data):
    """Generate /en/llms.txt — English-only AI crawler index.
    GPTBot, ClaudeBot, and PerplexityBot check /llms.txt AND /en/llms.txt
    for language-specific content discovery.
    """
    lines = [
        "# SourceHub — Developer Tutorials & Tools",
        f"> {sum(len(b['posts']) for b in en_data['boards'])} English articles on tech tutorials, tool comparisons, side-hustle guides, and AI development.",
        f"> Updated: {TODAY}",
        "",
        "## Quick Links",
        f"- Home: {BASE}/en/",
        f"- Full content: {BASE}/en/llms-full.txt",
        f"- Sitemap: {BASE}/sitemap.xml",
        f"- RSS: {BASE}/en/feed.xml",
        f"- JSON Feed: {BASE}/en/feed.json",
        f"- Markdown copies: {BASE}/md/en/",
        "",
    ]

    for board in en_data["boards"]:
        posts = board["posts"]
        if not posts:
            continue
        board_name = BOARD_NAMES_EN.get(board["id"], board["id"].title())
        lines.append(f"## {board_name} ({len(posts)} articles)")
        lines.append("")
        for art in posts:
            url = f"{BASE}/en/{board['id']}/{art['slug']}.html"
            md_url = f"{BASE}/md/en/{board['id']}/{art['slug']}.md"
            desc = art.get("description", "")[:120]
            lines.append(f"- [{art['title']}]({url}) — [md]({md_url})")
            if desc:
                lines.append(f"  {desc}")
        lines.append("")

    content = "\n".join(lines)
    (ROOT / "en" / "llms.txt").write_text(content, encoding="utf-8")
    print(f"  en/llms.txt: {content.count(chr(10))} lines written")


# ── 3. Generate llms-full.txt ──────────────────────────────────────────

def gen_llms_full():
    """Generate /llms-full.txt — all English article bodies in one Markdown file.
    This is used by AI training pipelines (they prefer one big file over crawling
    hundreds of small ones).

    Uses a FRESH html2text instance (not the shared global) to avoid corruption
    from processing 850 articles through gen_markdown_copies() first.
    """
    import html2text as ht
    local_h = ht.HTML2Text()
    local_h.body_width = 0
    local_h.ignore_emphasis = False
    local_h.ignore_links = False
    local_h.ignore_images = True
    local_h.protect_links = True
    local_h.unicode_snob = True

    def _extract(html):
        m = re.search(r'<div class="article-body">(.*?)</article>', html, re.DOTALL)
        if not m:
            return None
        return local_h.handle(m.group(1)).strip()

    en_data = json.loads(EN_ARTICLES.read_text(encoding="utf-8"))

    # Build article list first so we can generate a Table of Contents
    all_articles = []
    for board in en_data["boards"]:
        for art in board["posts"]:
            all_articles.append({**art, "board_id": board["id"]})

    full_lines = [
        "# AI Study Room — Full Content (English)",
        f"Generated: {TODAY}",
        f"Total articles: {len(all_articles)} across {len(en_data['boards'])} topic boards",
        f"License: Creative Commons Attribution 4.0 (CC BY 4.0)",
        f"License URL: https://creativecommons.org/licenses/by/4.0/",
        f"Site: {BASE}/en/",
        f"JSON Feed (full content): {BASE}/en/feed.json",
        f"RSS Feed: {BASE}/en/feed.xml",
        "",
        "## Table of Contents",
        "",
    ]

    # Generate TOC grouped by board, using explicit slug-based anchors
    for board in en_data["boards"]:
        board_name = BOARD_NAMES_EN.get(board["id"], board["id"].title())
        full_lines.append(f"### {board_name} ({len(board['posts'])} articles)")
        full_lines.append("")
        for art in board["posts"]:
            desc = art.get("description", "")[:100]
            full_lines.append(f"- [{art['title']}](#{art['slug']}) — {desc}")
        full_lines.append("")

    full_lines.append("---")
    full_lines.append("")

    for board in en_data["boards"]:
        for art in board["posts"]:
            html_path = ROOT / "en" / board["id"] / f'{art["slug"]}.html'
            if not html_path.exists():
                continue
            html = html_path.read_text(encoding="utf-8")
            body = _extract(html)
            if not body:
                continue
            # Clean up: strip article title H1s (already in metadata header),
            # compress consecutive blank lines, strip trailing whitespace
            body = body.replace(f'# {art["title"]}\n', '')
            body = body.replace(f'# {art["title"]} \n', '')
            body = re.sub(r'\n{3,}', '\n\n', body)
            body = body.strip()
            slug = art["slug"]
            title = art["title"]
            tags_str = ', '.join(art.get('tags', []))
            full_lines.append(f'## <a id="{slug}"></a>{title}')
            full_lines.append(f"URL: {BASE}/en/{board['id']}/{slug}.html")
            full_lines.append(f"Date: {art['date']} | Board: {board['id']} | Tags: {tags_str}")
            full_lines.append(f"Description: {art.get('description', '')}")
            full_lines.append("")
            full_lines.append(body)
            full_lines.append("")
            full_lines.append("---")
            full_lines.append("")

    content = "\n".join(full_lines)
    (ROOT / "llms-full.txt").write_text(content, encoding="utf-8")
    size_kb = len(content.encode("utf-8")) / 1024
    print(f"  llms-full.txt: {size_kb:.0f} KB written")

    # Also write English version at /en/llms-full.txt for AI crawlers
    # that check language-specific paths
    (ROOT / "en" / "llms-full.txt").write_text(content, encoding="utf-8")
    print(f"  en/llms-full.txt: {size_kb:.0f} KB written")

    # Chinese full content (read from markdown source — no ZH HTML generated)
    if CN_ARTICLES.exists():
        cn_data = json.loads(CN_ARTICLES.read_text(encoding="utf-8"))
        cn_lines = [
            "# AI自习室 — 全部内容 (中文)",
            f"Generated: {TODAY}",
            f"Total articles: {sum(len(b.get('posts', [])) for b in cn_data.get('boards', []))}",
            "",
            "---",
            "",
        ]
        for board in cn_data.get("boards", []):
            for art in board.get("posts", []):
                md_path = MD_DIR / "zh" / board["id"] / f'{art["slug"]}.md'
                if md_path.exists():
                    body = md_path.read_text(encoding="utf-8")
                    # Remove frontmatter
                    if body.startswith("---"):
                        end = body.find("---", 3)
                        if end > 0:
                            body = body[end + 3:].strip()
                else:
                    continue
                cn_lines.append(f"## {art['title']}")
                cn_lines.append(f"URL: {BASE}/zh/{board['id']}/{art['slug']}.html")
                cn_lines.append("")
                cn_lines.append(body)
                cn_lines.append("")
                cn_lines.append("---")
                cn_lines.append("")

        content_cn = "\n".join(cn_lines)
        (ROOT / "llms-full-cn.txt").write_text(content_cn, encoding="utf-8")
        size_kb = len(content_cn.encode("utf-8")) / 1024
        print(f"  llms-full-cn.txt: {size_kb:.0f} KB written")


# ── 4. Optimize robots.txt for AI crawlers ──────────────────────────────

def update_robots():
    """Explicitly welcome major AI crawlers."""
    robots = """# AI Study Room — robots.txt
# We explicitly welcome AI crawlers. Our content is here to be learned from.

# ── Search engines ──
User-agent: Googlebot
Allow: /
User-agent: Bingbot
Allow: /

# ── AI crawlers — WELCOME ──
# OpenAI (ChatGPT, GPTBot, SearchGPT)
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /

# Anthropic (Claude)
User-agent: ClaudeBot
Allow: /
User-agent: anthropic-ai
Allow: /

# Google AI
User-agent: Google-Extended
Allow: /

# Perplexity
User-agent: PerplexityBot
Allow: /

# Meta AI
User-agent: meta-externalagent
Allow: /
User-agent: FacebookBot
Allow: /

# Cohere
User-agent: cohere-ai
Allow: /

# Common Crawl (feeds many AI training datasets)
User-agent: CCBot
Allow: /

# Apple (Siri, Spotlight, Apple Intelligence)
User-agent: Applebot
Allow: /

# Amazon (Alexa, product search)
User-agent: Amazonbot
Allow: /

# ByteDance/TikTok
User-agent: Bytespider
Allow: /

# You.com AI search
User-agent: YouBot
Allow: /

# Huawei (Petal Search)
User-agent: PetalBot
Allow: /

# ── Misc web crawlers ──
User-agent: *
Allow: /

# ── AI-specific discovery ──
# /llms.txt — bilingual site index for AI crawlers
# /en/llms.txt — English-only site index
# /llms-full.txt — all English content in one file (1 MB)
# /en/llms-full.txt — English full content at /en/ path
# /llms-full-cn.txt — all Chinese content in one file (255 KB)
# /md/ — clean Markdown copies of every article (286 files)

# ── JSON Feeds (AI-friendly RSS alternative) ──
# /feed.json — Chinese content (60 items)
# /en/feed.json — English content (226 items)

# ── IndexNow (instant crawl signals to Bing/Yandex) ──
# We push URL updates to IndexNow on every content change.
# Bing's index powers ChatGPT, Copilot, DuckDuckGo, and other AI search.

Sitemap: https://dingjiu1989-hue.github.io/sitemap.xml
Sitemap: https://dingjiu1989-hue.github.io/images/sitemap.xml
"""
    (ROOT / "robots.txt").write_text(robots, encoding="utf-8")
    print("  robots.txt updated: 21 AI crawler rules")


# ── Run ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== AI-Friendly Artifact Generator ===\n")
    gen_markdown_copies()
    gen_llms_txt()
    gen_llms_full()
    update_robots()
    print("\nDone. Run 'git add -A && git commit && git push' to deploy.")
