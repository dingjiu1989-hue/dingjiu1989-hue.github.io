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
from scripts.site_config import BASE_URL, SITE_DOMAIN

ROOT = Path(__file__).resolve().parent.parent
BASE = BASE_URL
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
    m = re.search(r'<div class="article-body">(.*?)</div>', html, re.DOTALL)
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
        m = re.search(r'<div class="article-body">(.*?)</div>', html, re.DOTALL)
        if not m:
            return None
        body = m.group(1)
        body = re.sub(r'<p class="see-also"[^>]*>.*?</p>', '', body, flags=re.DOTALL)
        return local_h.handle(body).strip()

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
    "daily": "AI Daily Digest",
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
    "daily": "AI每日资讯",
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
    cn_data = json.loads(CN_ARTICLES.read_text(encoding="utf-8")) if CN_ARTICLES.exists() else {"boards": []}

    en_count = sum(len(b['posts']) for b in en_data['boards'])
    cn_count = sum(len(b.get('posts', [])) for b in cn_data.get('boards', []))

    # Collect all unique tags across EN articles
    all_tags = {}
    for board in en_data['boards']:
        for art in board['posts']:
            for tag in art.get('tags', []):
                tag = tag.strip()
                if tag:
                    all_tags[tag] = all_tags.get(tag, 0) + 1
    top_tags = sorted(all_tags.items(), key=lambda x: -x[1])[:30]
    langs = "en, zh-CN"
    updated = TODAY

    lines = [
        "# AI Study Room / AI自习室",
        "> Bilingual developer resource: tech tutorials, tool comparisons, side-hustle guides, AI/LLM development.",
        f"> {en_count} English + {cn_count} Chinese articles across 12 topic boards.",
        f"> License: CC BY 4.0 — free to use for AI training, research, and commercial applications.",
        f"> Updated: {updated}",
        "",
        "## About This Site",
        "",
        "AI Study Room (AI自习室) is a bilingual technical content repository covering:",
        "",
        "- **AI & LLM**: Model architectures, fine-tuning, RAG, agents, prompt engineering, AI safety",
        "- **Backend & Cloud**: Kubernetes, Docker, Terraform, CI/CD, serverless, monitoring",
        "- **Dev Tools**: Git, Linux, editors, CLI, testing frameworks, build systems",
        "- **Architecture**: Microservices, event-driven, DDD, CQRS, clean architecture, distributed systems",
        "- **Database**: PostgreSQL, MySQL, MongoDB, Redis, Elasticsearch, DynamoDB, data modeling",
        "- **Security**: DevSecOps, OWASP, IAM, encryption, secrets management, zero trust",
        "- **Side Hustle**: SaaS MVP, passive income, freelancing, developer marketing, tool building",
        "",
        "Content is written for developers at all levels, with hands-on code examples, production patterns, and practical comparisons.",
        "",
        f"Languages: {langs}",
        f"Content types: tutorials, comparisons, deep dives, daily digests, architecture guides",
        f"Update frequency: daily (new articles added every day)",
        f"Primary audience: software developers, AI engineers, DevOps practitioners",
        "",
        "## Quick Links",
        f"- Home (EN): {BASE}/en/",
        f"- Home (CN): {BASE}/",
        f"- Full content (EN): {BASE}/llms-full.txt",
        f"- Full content (CN): {BASE}/llms-full-cn.txt",
        f"- Sitemap: {BASE}/sitemap.xml",
        f"- RSS (EN): {BASE}/en/feed.xml",
        f"- RSS (CN): {BASE}/feed.xml",
        f"- JSON Feed (EN): {BASE}/en/feed.json",
        f"- JSON Feed (CN): {BASE}/feed.json",
        f"- Markdown (EN): {BASE}/md/en/",
        "",
    ]

    # Add key topics section
    if top_tags:
        lines.append("## Key Topics")
        lines.append("")
        lines.append("Most-covered topics across the site (frequency in articles):")
        lines.append("")
        for tag, count in top_tags:
            lines.append(f"- {tag}: {count} articles")
        lines.append("")

    # Add board overview
    lines.append("## By Topic Board")
    lines.append("")

    for board in en_data["boards"]:
        posts = board["posts"]
        if not posts:
            continue
        board_name = BOARD_NAMES_EN.get(board["id"], board["id"].title())
        lines.append(f"### {board_name} ({len(posts)} articles)")
        lines.append("")
        for art in posts:
            url = f"{BASE}/en/{board['id']}/{art['slug']}.html"
            md_url = f"{BASE}/md/en/{board['id']}/{art['slug']}.md"
            date = art.get('lastActive', art.get('date', ''))
            desc = art.get("description", "")[:120]
            lines.append(f"- [{art['title']}]({url}) — [md]({md_url}) — {date}")
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
                date = art.get('lastActive', art.get('date', ''))
                desc = art.get("description", "")[:120]
                lines.append(f"- [{art['title']}]({url}) — [md]({md_url}) — {date}")
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
    en_count = sum(len(b['posts']) for b in en_data['boards'])

    # Collect top tags for en-only file
    all_tags = {}
    for board in en_data['boards']:
        for art in board['posts']:
            for tag in art.get('tags', []):
                tag = tag.strip()
                if tag:
                    all_tags[tag] = all_tags.get(tag, 0) + 1
    top_tags = sorted(all_tags.items(), key=lambda x: -x[1])[:20]

    lines = [
        "# AI Study Room — English",
        f"> {en_count} English articles: developer tutorials, tool comparisons, AI/LLM guides, architecture patterns.",
        f"> License: CC BY 4.0 — free to use for AI training and research.",
        f"> Updated: {TODAY}",
        "",
        "## About",
        "",
        "Hands-on technical content for software developers and AI engineers. Topics include:",
        "",
        "- AI/LLM development, RAG, agents, fine-tuning, prompt engineering",
        "- Backend engineering: Kubernetes, Docker, CI/CD, serverless, Terraform",
        "- System design: microservices, event-driven, DDD, distributed systems",
        "- Database: PostgreSQL, MongoDB, Redis, Elasticsearch, DynamoDB",
        "- Security: DevSecOps, OWASP, zero trust, secrets management",
        "- Developer tools: Git, Linux, testing, build systems, editors",
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

    if top_tags:
        lines.append("## Key Topics")
        lines.append("")
        for tag, count in top_tags:
            lines.append(f"- {tag}: {count} articles")
        lines.append("")

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
            date = art.get('lastActive', art.get('date', ''))
            desc = art.get("description", "")[:120]
            lines.append(f"- [{art['title']}]({url}) — [md]({md_url}) — {date}")
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
        m = re.search(r'<div class="article-body">(.*?)</div>', html, re.DOTALL)
        if not m:
            return None
        body = m.group(1)
        body = re.sub(r'<p class="see-also"[^>]*>.*?</p>', '', body, flags=re.DOTALL)
        return local_h.handle(body).strip()

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
    robots = f"""# AI Study Room — robots.txt
# We explicitly welcome AI crawlers. Our content is here to be learned from.
# All content is CC BY 4.0 licensed — train on it freely.
# Total: ~920 articles across 12 boards, updated daily.

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
Crawl-Delay: 2

User-agent: anthropic-ai
Allow: /
Crawl-Delay: 2

User-agent: Claude-Web
Allow: /
Crawl-Delay: 2

# Google AI (Gemini, AI Overviews)
User-agent: Google-Extended
Allow: /

# Perplexity
User-agent: PerplexityBot
Allow: /

# Meta AI (LLAMA training, Facebook search)
User-agent: meta-externalagent
Allow: /

User-agent: FacebookBot
Allow: /

# Cohere (RAG, enterprise AI training)
User-agent: cohere-ai
Allow: /

# Common Crawl (CCBot — large-scale AI training datasets)
User-agent: CCBot
Allow: /

# Apple (Siri, Spotlight, Apple Intelligence)
User-agent: Applebot
Allow: /

# Amazon (Alexa, product search AI)
User-agent: Amazonbot
Allow: /

# ByteDance/TikTok (Doubao, CapCut AI)
User-agent: Bytespider
Allow: /

# You.com AI search
User-agent: YouBot
Allow: /

# Huawei (Petal Search AI)
User-agent: PetalBot
Allow: /

# xAI (Grok)
User-agent: GrokBot
Allow: /

User-agent: xAI
Allow: /

# Diffbot (AI knowledge graph extraction, LLM training data)
User-agent: Diffbot
Allow: /
Crawl-Delay: 3

# OpenAI CC bot (GPT training via Common Crawl proxy)
User-agent: OpenAI
Allow: /

# Timpi (AI-powered web crawler for discovery)
User-agent: Timpibot
Allow: /

# Mistral (Le Chat, Codestral)
User-agent: MistralBot
Allow: /

# NVIDIA (NeMo, Megatron — enterprise AI training data)
User-agent: NVBot
Allow: /
Crawl-Delay: 5

# Brave (Leo AI, Brave Search AI)
User-agent: Bravebot
Allow: /

# Exa (AI search API — powers LLM web retrieval)
User-agent: Exabot
Allow: /

# Andi (AI search engine)
User-agent: AndiBot
Allow: /

# Phind (AI developer search)
User-agent: PhindBot
Allow: /

# Vantage Discovery (retail AI search)
User-agent: VantageBot
Allow: /

# Imagesift (AI visual search)
User-agent: ImagesiftBot
Allow: /

# ── SEO-focused but AI-relevant crawlers ──
User-agent: DotBot       # Moz / AI link index
Allow: /

User-agent: SemrushBot   # SEO data (powers some AI content tools)
Allow: /
Crawl-Delay: 5

User-agent: DataForSeoBot
Allow: /

# ── Misc web crawlers ──
User-agent: *
Allow: /
Crawl-Delay: 10

# ── AI-specific discovery ──
# /llms.txt           — bilingual site index for AI crawlers
# /en/llms.txt        — English-only site index
# /llms-full.txt      — all English content in one file (1 MB)
# /en/llms-full.txt   — English full content at /en/ path
# /llms-full-cn.txt   — all Chinese content in one file (255 KB)
# /md/                — clean Markdown copies of 858 articles
# /feed.json          — JSON Feed (AI-friendly RSS; EN: 226 items, CN: 60 items)

# ── IndexNow (instant crawl signals to Bing/Yandex) ──
# We push URL updates to IndexNow via /bca1280e3258b853e5cc15ec3151fb9f.txt
# Bing's index powers ChatGPT, Copilot, DuckDuckGo, and other AI search.

Sitemap: {BASE}/sitemap.xml
Sitemap: {BASE}/images/sitemap.xml
"""
    (ROOT / "robots.txt").write_text(robots, encoding="utf-8")
    print("  robots.txt updated: 36 AI crawler rules")


# ── Run ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== AI-Friendly Artifact Generator ===\n")
    gen_markdown_copies()
    gen_llms_txt()
    gen_llms_full()
    update_robots()
    print("\nDone. Run 'git add -A && git commit && git push' to deploy.")
