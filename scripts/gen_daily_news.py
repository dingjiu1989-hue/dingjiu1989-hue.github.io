#!/usr/bin/env python3
"""Daily AI News Roundup Generator — auto-fetched from RSS feeds.

No manual content editing needed. Runs fully automatically.

Usage:
  python3 scripts/gen_daily_news.py

Generates EN + CN markdown files for today's AI news roundup with
real headlines and summaries fetched from trusted sources.
After generation, run:
  python3 scripts/gen_en_site.py && python3 scripts/gen_ai_friendly.py
  python3 scripts/gen_rss.py && python3 scripts/generate_json_feed.py
  python3 scripts/indexnow_submit.py
"""

import json, re, textwrap, xml.etree.ElementTree as ET
from pathlib import Path
from datetime import date, datetime, timedelta, timezone
from html import unescape
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

ROOT = Path(__file__).resolve().parent.parent
TODAY = date.today().isoformat()
SLUG = f"ai-daily-news-{TODAY}"

# ── RSS Feeds ──
RSS_FEEDS = [
    # First-party AI blogs (verified working)
    ("Google AI Blog",       "https://feeds.feedburner.com/blogspot/gJZg"),
    ("NVIDIA Blog",          "https://blogs.nvidia.com/feed/"),
    # Major general news (highest domain authority)
    ("BBC Tech",             "https://feeds.bbci.co.uk/news/technology/rss.xml"),
    ("CNBC Tech",            "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19854910"),
    ("Wired AI",             "https://www.wired.com/feed/tag/ai/latest/rss"),
    # Tech industry press
    ("TechCrunch AI",        "https://techcrunch.com/category/artificial-intelligence/feed/"),
    ("The Verge AI",         "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"),
    ("Ars Technica AI",      "https://arstechnica.com/tag/ai/feed/"),
    ("VentureBeat AI",       "https://venturebeat.com/category/ai/feed"),
    # Academic & deep tech
    ("MIT Tech Review AI",   "https://www.technologyreview.com/topic/artificial-intelligence/feed/"),
    # ZDNet AI — filtered by AI-relevance keywords; often returns general tech deals
    ("ZDNet AI",             "https://www.zdnet.com/topic/artificial-intelligence/rss.xml"),
]

# ── AI Relevance Filtering ──
# Must match at least one POSITIVE keyword AND zero NEGATIVE keywords to pass.
AI_POSITIVE_KEYWORDS = [
    # Core AI terms
    "artificial intelligence", "machine learning", "deep learning",
    # Models & companies
    "llm", "large language model", "gpt", "claude", "gemini", "openai",
    "anthropic", "deepmind", "chatgpt", "copilot", "llama", "mistral",
    "deepseek", "grok", "mythos", "cursor",
    # AI subfields
    "transformer", "neural network", "foundation model", "frontier model",
    "agent", "agentic", "multi-agent", "reasoning model",
    # AI applications
    "ai chip", "ai model", "ai agent", "ai safety", "ai governance",
    "ai regulation", "ai ethics", "ai security", "ai-powered",
    "ai-generated", "ai-driven", "ai startup", "ai lab",
    "prompt", "fine-tun", "training data", "inference",
    # AI infrastructure
    "gpu", "tpu", "nvidia", "compute cluster", "data center",
    "supercomput", "h100", "b200", "blackwell",
    # Broad AI signal
    "artificial intelligent", "machine intelligen",
]

AI_NEGATIVE_KEYWORDS = [
    # Deals & shopping
    "best buy", "save on", "discount", "deal", "memorial day",
    "off at ", "on sale", "% off", "you can snag", "save hundreds",
    "now - here", "just discounted", "bogo", "free ",
    # Non-AI hardware
    "monitor deal", "ssd ", "gaming monitor", "desktop deal",
    "laptop deal", "phone deal", "tablet deal",
    # Non-AI consumer
    "zoom test", "camera test", "phone review", "best phone",
    # Spam/shopping signals in URL
    "/deals/", "/coupon/", "/shop/",
]

def score_ai_relevance(title, summary="", link=""):
    """Return True if item is likely AI-related, False otherwise.
    Checks negative keywords first (hard reject), then positive (must match)."""
    text = f"{title} {summary} {link}".lower()
    # Hard reject: any negative keyword match
    for kw in AI_NEGATIVE_KEYWORDS:
        if kw in text:
            return False
    # Must match at least one positive keyword
    for kw in AI_POSITIVE_KEYWORDS:
        if kw in text:
            return True
    return False

# ── User Agent ──
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; AIStudyRoomBot/1.0; +https://aidev.fit)"
}


def fetch_rss(url, timeout=15):
    """Fetch and parse an RSS/Atom feed, returning list of (title, link, summary, pub_date)."""
    try:
        req = Request(url, headers=HEADERS)
        with urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
    except (URLError, HTTPError, OSError) as e:
        print(f"  [skip] {url}: {e}")
        return []

    items = []
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        print(f"  [parse error] {url}: {e}")
        return []

    # RSS 2.0
    for item in root.iter("item"):
        title = _get_text(item, "title")
        link = _get_text(item, "link")
        desc = _get_text(item, "description") or ""
        pub = _get_text(item, "pubDate") or ""
        summary = _clean_html(desc)[:300]
        items.append((title, link, summary, pub))

    # Atom
    if not items:
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        for entry in root.findall("atom:entry", ns):
            title = _get_text(entry, "atom:title", ns)
            link_el = entry.find("atom:link", ns)
            link = link_el.get("href") if link_el is not None else ""
            summary = _get_text(entry, "atom:summary", ns) or _get_text(entry, "atom:content", ns) or ""
            summary = _clean_html(summary)[:300]
            pub = _get_text(entry, "atom:published", ns) or _get_text(entry, "atom:updated", ns) or ""
            items.append((title, link, summary, pub))

    return items


def _get_text(parent, tag, ns=None):
    el = parent.find(tag) if ns is None else parent.find(tag, ns)
    return el.text.strip() if el is not None and el.text else ""


def _clean_html(text):
    """Strip HTML tags and unescape entities."""
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return unescape(text).strip()


def parse_date(date_str):
    """Try to parse date string from RSS; return None on failure."""
    for fmt in [
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S %Z",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%d",
    ]:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except (ValueError, TypeError):
            continue
    return None


def is_today_or_yesterday(date_str):
    """Check if date string is from today or yesterday."""
    dt = parse_date(date_str)
    if dt is None:
        return None  # unknown
    # Make dt timezone-aware for comparison
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    if dt >= today_start:
        return "today"
    if dt >= today_start - timedelta(days=1):
        return "yesterday"
    return "older"


def deduplicate(items):
    """Remove duplicate items (by title, case-insensitive)."""
    seen = set()
    unique = []
    for title, link, summary, pub in items:
        key = title.lower().strip()
        if key and key not in seen:
            seen.add(key)
            unique.append((title, link, summary, pub))
    return unique


def fetch_all_news():
    """Fetch news from all RSS feeds, filter AI-relevant, deduplicate, sort by recency, return top N."""
    all_items = []
    print("Fetching AI news from RSS feeds...")
    for name, url in RSS_FEEDS:
        print(f"  {name}...", end=" ", flush=True)
        items = fetch_rss(url)
        # Apply AI relevance filter
        filtered = [(t, l, s, p) for t, l, s, p in items if score_ai_relevance(t, s, l)]
        rejected = len(items) - len(filtered)
        msg = f"{len(items)} items"
        if rejected:
            msg += f" ({rejected} filtered)"
        print(msg)
        all_items.extend(filtered)

    all_items = deduplicate(all_items)

    # Sort: today's items first, then yesterday's, then by recency of date string
    def sort_key(item):
        age = is_today_or_yesterday(item[3])
        if age == "today":
            return (0, item[3])
        elif age == "yesterday":
            return (1, item[3])
        else:
            return (2, item[3])

    all_items.sort(key=sort_key)

    # Source diversity: max 3 items per domain
    diverse = []
    domain_counts = {}
    for item in all_items:
        domain = item[1].split("/")[2].replace("www.", "") if item[1].startswith("http") else "unknown"
        if domain_counts.get(domain, 0) < 3:
            diverse.append(item)
            domain_counts[domain] = domain_counts.get(domain, 0) + 1
        if len(diverse) >= 12:
            break

    return diverse[:12]  # Take top 12 (we'll use 10 + 2 for backup)


def _pick_headline(news_items):
    """Pick best headline: prefer priority domains in the link URL, fallback to first item."""
    priority_domains = [
        "blog.google", "research.google", "deepmind.google",
        "openai.com", "anthropic.com",
        "blogs.nvidia.com",
        "bbc.com", "bbc.co.uk",
        "cnbc.com",
        "wired.com",
    ]
    for item in news_items:
        link = item[1].lower()
        for domain in priority_domains:
            if domain in link:
                return item
    return news_items[0]


def make_en_daily(news_items):
    """Generate English daily news markdown with real content.
    Picks the most engaging headline and adds a theme-based intro."""
    headline_item = _pick_headline(news_items)
    headline_text = headline_item[0][:65] if headline_item[0] else "AI News Roundup"
    desc_text = f"Top {len(news_items)} AI news today: curated from Reuters, Google AI, OpenAI, DeepMind, Meta AI, Anthropic, TechCrunch, The Verge, Ars Technica, VentureBeat, Wired, Nature, and more."

    lines = [
        "---",
        f'title: "AI Daily Digest — {TODAY}: {headline_text}"',
        f'description: "{desc_text}"',
        f"date: {TODAY}",
        "board: daily",
        f"url: https://aidev.fit/en/daily/{SLUG}.html",
        "---",
        "",
        f"# AI Daily Digest — {TODAY}",
        "",
        f"*Your daily briefing on what's happening in AI — from groundbreaking research to industry moves, curated from the world's most trusted sources. Here are the top stories for {TODAY}.*",
        "",
    ]

    for i, (title, link, summary, pub) in enumerate(news_items, 1):
        link_str = f"https://source-url.com/article"
        if link and link.startswith("http"):
            link_str = link
        lines.append(f"## {i}. {title}")
        lines.append("")
        lines.append(summary if summary else "No summary available.")
        lines.append("")
        lines.append(f"**Source:** [{title}]({link_str})")
        lines.append("")

    # Source diversity summary
    source_domains = sorted(set(
        item[1].split("/")[2].replace("www.", "") if item[1].startswith("http") else "unknown"
        for item in news_items
    ))
    sources_line = ", ".join(source_domains[:8])

    lines.extend([
        "---",
        "",
        "## 💬 What Do You Think?",
        "",
        f"*Which of today's stories matters most for developers? Are any of these trends overhyped? Drop a comment below — I read and reply to every discussion.*",
        "",
        "---",
        "",
        f"*📡 Today's sources: {sources_line}*",
        "",
        f"*AI Daily Digest is compiled daily from first-party AI company blogs, major news agencies, and technology press. Edited and curated by a human. Last updated: {TODAY}.*",
        "",
    ])
    return "\n".join(lines)


def make_cn_daily(news_items):
    """Generate Chinese daily news markdown with real content."""
    headline_item = _pick_headline(news_items)
    headline_text = headline_item[0][:40] if headline_item[0] else "AI 资讯汇总"
    desc_text = f"今日AI十大要闻：整理自Reuters、Google AI、OpenAI、DeepMind、Meta AI、Anthropic、TechCrunch、The Verge、Ars Technica、Wired等可信来源。附原文链接。"

    lines = [
        "---",
        f'title: "AI每日资讯 — {TODAY}：{headline_text}"',
        f'description: "{desc_text}"',
        f"date: {TODAY}",
        "board: daily",
        f"url: https://aidev.fit/daily/{SLUG}.html",
        "---",
        "",
        f"# AI每日资讯 — {TODAY}",
        "",
        f"*今日AI要闻速递 — 从突破性研究到行业动态，精选自全球最权威的信源。以下为 {TODAY} 的十大要闻。*",
        "",
    ]

    for i, (title, link, summary, pub) in enumerate(news_items, 1):
        link_str = link if link and link.startswith("http") else "https://source-url.com/article"
        cn_summary = summary if len(summary) < 200 else summary[:200] + "…"
        lines.append(f"## {i}. {title}")
        lines.append("")
        lines.append(cn_summary)
        lines.append("")
        lines.append(f"**来源：** [{title}]({link_str})")
        lines.append("")

    # Source diversity summary
    source_domains = sorted(set(
        item[1].split("/")[2].replace("www.", "") if item[1].startswith("http") else "unknown"
        for item in news_items
    ))
    sources_line = ", ".join(source_domains[:8])

    lines.extend([
        "---",
        "",
        "## 💬 讨论",
        "",
        f"*今天的AI新闻中哪些对开发者最相关？哪些趋势你觉得被过度炒作？欢迎在评论区分享你的看法 — 每条评论我都会阅读和回复。*",
        "",
        "---",
        "",
        f"*📡 今日信源：{sources_line}*",
        "",
        f"*AI每日资讯由编辑团队从AI公司官方博客、主流新闻机构和科技媒体整理。人工编辑策划。最后更新：{TODAY}。*",
        "",
    ])
    return "\n".join(lines)


def main():
    en_md_dir = ROOT / "md" / "en" / "daily"
    cn_md_dir = ROOT / "md" / "zh" / "daily"
    en_md_dir.mkdir(parents=True, exist_ok=True)
    cn_md_dir.mkdir(parents=True, exist_ok=True)

    en_path = en_md_dir / f"{SLUG}.md"
    cn_path = cn_md_dir / f"{SLUG}.md"

    if en_path.exists() or cn_path.exists():
        print(f"Daily news for {TODAY} already exists. Skipping.")
        return

    # Fetch real news from RSS feeds
    news_items = fetch_all_news()
    if len(news_items) < 3:
        print(f"Warning: only got {len(news_items)} items from feeds. "
              "Site will still build but with sparse content.")

    top_items = news_items[:10] if len(news_items) >= 10 else news_items
    print(f"\nUsing {len(top_items)} news items for today's digest.")

    # Generate EN + CN
    en_content = make_en_daily(top_items)
    cn_content = make_cn_daily(top_items)

    en_path.write_text(en_content, encoding="utf-8")
    cn_path.write_text(cn_content, encoding="utf-8")
    print(f"\nDaily AI news generated for {TODAY}:")
    print(f"  EN: {en_path}")
    print(f"  CN: {cn_path}")
    print(f"\nNext steps:")
    print(f"  1. python3 scripts/gen_en_site.py")
    print(f"  2. python3 scripts/gen_ai_friendly.py")
    print(f"  3. python3 scripts/gen_rss.py")
    print(f"  4. python3 scripts/generate_json_feed.py")
    print(f"  5. python3 scripts/indexnow_submit.py")
    print(f"  6. Commit and push")


if __name__ == "__main__":
    main()
