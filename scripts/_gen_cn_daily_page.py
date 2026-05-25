#!/usr/bin/env python3
"""Quick script to generate CN daily HTML page (until a proper CN site generator exists)."""
import json, re, urllib.parse
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parent.parent
TODAY = date.today().isoformat()
SLUG = f"ai-daily-news-{TODAY}"
BASE = "https://aidev.fit"

# Read CN md
md_path = ROOT / "md" / "zh" / "daily" / f"{SLUG}.md"
if not md_path.exists():
    print(f"MD file not found: {md_path}")
    exit(1)
md_content = md_path.read_text(encoding="utf-8")

# Read CN article entry
arts = json.loads((ROOT / "articles.json").read_text(encoding="utf-8"))
art = None
for b in arts["boards"]:
    for p in b["posts"]:
        if p["slug"] == SLUG:
            art = dict(p)
            art["board_id"] = b["id"]
            break

if not art:
    print(f"Article {SLUG} not found in articles.json")
    exit(1)

title = art["title"]
desc = art["description"]
tags = art.get("tags", [])


def md_body_to_html(text):
    """Minimal markdown-to-HTML for daily news pages."""
    lines = text.split("\n")
    result = []
    in_fm = False
    for line in lines:
        stripped = line.strip()
        if stripped == "---":
            in_fm = not in_fm
            continue
        if in_fm:
            continue
        # Headings
        if stripped.startswith("### "):
            result.append(f"<h4>{stripped[4:]}</h4>")
        elif stripped.startswith("## "):
            result.append(f"<h3>{stripped[3:]}</h3>")
        elif stripped.startswith("# "):
            result.append(f"<h2>{stripped[2:]}</h2>")
        elif stripped.startswith("---"):
            result.append("<hr />")
        elif stripped == "":
            result.append("")
        elif stripped.startswith("**") and ("**" in stripped[2:]):
            # Bold text like **Source:** or **来源：**
            inner = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line)
            # Convert markdown links
            inner = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', inner)
            result.append(f"<p>{inner}</p>")
        elif stripped.startswith("*") and not stripped.startswith("**"):
            # Em text
            inner = stripped[1:].strip()
            if inner.endswith("*"):
                inner = inner[:-1]
            inner = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', inner)
            result.append(f"<p><em>{inner}</em></p>")
        else:
            inner = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', line)
            result.append(f"<p>{inner}</p>")
    return "\n".join(result)


body_html = md_body_to_html(md_content)

# Generate TOC from ## headings
toc_items = []
for line in md_content.split("\n"):
    if line.startswith("## "):
        h_text = line[3:].strip()
        h_id = re.sub(r"[^\w\s一-鿿-]", "", h_text.lower())
        h_id = re.sub(r"\s+", "-", h_id)
        toc_items.append(f'<li><a href="#{h_id}">{h_text}</a></li>')

toc_html = "<ol>" + "".join(toc_items) + "</ol>" if toc_items else ""

cn_url = f"{BASE}/daily/{SLUG}.html"
en_url = f"{BASE}/en/daily/{SLUG}.html"
tags_html = "\n".join(f'        <span class="tag-cat">{t}</span>' for t in tags)
title_for_meta = title[:120]

# Escape values for safe embedding in HTML/JSON
def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


html = f"""<!DOCTYPE html>
<html lang="zh-CN" data-render="related" data-board="daily" data-exclude="{SLUG}">
<head>
    <meta charset="UTF-8">
    <meta name="google-site-verification" content="XzThATs15kR08VOM-tCxIztKjEGW8ft-T75SmH_Wz38" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="base-path" content="">
    <link rel="preconnect" href="https://www.googletagmanager.com" crossorigin>
    <link rel="dns-prefetch" href="https://www.googletagmanager.com">
    <link rel="preconnect" href="https://pagead2.googlesyndication.com" crossorigin>
    <link rel="dns-prefetch" href="https://pagead2.googlesyndication.com">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <link rel="alternate icon" href="/favicon.ico">
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-XGFYGQE9NS"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-XGFYGQE9NS');
    </script>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3258394111169733" crossorigin="anonymous"></script>
    <meta property="og:title" content="{esc(title_for_meta)}">
    <meta property="og:description" content="{esc(desc[:160])}">
    <meta property="og:url" content="{cn_url}">
    <meta property="og:type" content="article">
    <meta property="og:site_name" content="AI自习室">
    <meta property="og:locale" content="zh_CN">
    <meta property="og:image" content="{BASE}/images/og-default.jpg">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{esc(title_for_meta)}">
    <meta name="twitter:description" content="{esc(desc[:160])}">
    <meta name="twitter:image" content="{BASE}/images/og-default.jpg">
    <meta property="article:published_time" content="{TODAY}">
    <meta property="article:modified_time" content="{TODAY}">
    <meta property="article:section" content="AI每日资讯">
    <meta property="article:tag" content="{tags[0] if tags else 'Technology'}">
    <title>{esc(title)} — AI自习室</title>
    <meta name="description" content="{esc(desc[:160])}">
    <meta name="keywords" content="{', '.join(tags[:5])}">
    <link rel="alternate" hreflang="zh-CN" href="{cn_url}">
    <link rel="alternate" hreflang="en" href="{en_url}">
    <link rel="canonical" href="{cn_url}">
    <meta name="robots" content="index, follow">
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "NewsArticle",
      "headline": "{esc(title)}",
      "description": "{esc(desc[:160])}",
      "image": "{BASE}/images/og-default.jpg",
      "datePublished": "{TODAY}",
      "dateModified": "{TODAY}",
      "inLanguage": "zh-CN",
      "isAccessibleForFree": true,
      "author": {{"@type": "Person", "name": "AI自习室"}},
      "publisher": {{
        "@type": "Organization",
        "name": "AI自习室",
        "url": "{BASE}/",
        "logo": {{"@type": "ImageObject", "url": "{BASE}/images/logo.png"}}
      }},
      "mainEntityOfPage": {{"@type": "WebPage", "@id": "{cn_url}"}}
    }}
    </script>
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{"@type": "ListItem", "position": 1, "name": "首页", "item": "{BASE}/"}},
        {{"@type": "ListItem", "position": 2, "name": "AI每日资讯", "item": "{BASE}/daily/"}},
        {{"@type": "ListItem", "position": 3, "name": "{esc(title)}"}}
      ]
    }}
    </script>
    <link rel="alternate" type="application/rss+xml" title="AI自习室 (中文)" href="/feed.xml">
</head>
<body>
<div id="reading-progress-container"><div id="reading-progress-bar"></div></div>
<div id="nav-placeholder"></div>
<main>
  <div class="breadcrumb container">
    <a href="/">首页</a> › <a href="/daily/">AI每日资讯</a>
  </div>
  <div class="article-layout">
    <div class="article-main">
      <article>
        <div class="article-tags">{tags_html}</div>
        <h1 class="article-title">{esc(title)}</h1>
        <div class="article-meta">
          <span class="author-name">By AI自习室</span>
          <span class="meta-sep">·</span>
          <time datetime="{TODAY}">{TODAY}</time>
          <span class="meta-sep">·</span>
          <span>{len(md_content.split()) // 200 + 1} min read</span>
        </div>
        <details class="article-toc-inline"><summary>目录 ({len(toc_items)})</summary>{toc_html}</details>
        <div class="article-body">{body_html}</div>
        <div class="ad-container">
    <div class="ad-label">— 广告 —</div>
    <ins class="adsbygoogle"
         style="display:block"
         data-ad-client="ca-pub-3258394111169733"
         data-ad-format="auto"
         data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
    </div>
        <div class="share-bar">
          <span>分享</span>
          <a href="https://twitter.com/intent/tweet?text={urllib.parse.quote(title)}&url={urllib.parse.quote(cn_url)}" target="_blank" rel="noopener" aria-label="分享到 X">𝕏</a>
          <a href="https://www.linkedin.com/sharing/share-offsite/?url={urllib.parse.quote(cn_url)}" target="_blank" rel="noopener" aria-label="分享到 LinkedIn">in</a>
          <a href="https://www.reddit.com/submit?title={urllib.parse.quote(title)}&url={urllib.parse.quote(cn_url)}" target="_blank" rel="noopener" aria-label="分享到 Reddit">Reddit</a>
          <button class="copy-link-btn" data-url="{cn_url}" aria-label="复制链接">复制</button>
        </div>
      </article>
      <div class="discussion-cta">
        <p>参与讨论</p>
        <p>有问题或想法？在下方留言 — 你的见解能帮助其他读者。</p>
        <a href="#giscus-section">留下评论</a>
      </div>
      <div id="giscus-section" data-giscus-loaded="false"></div>
    </div>
    <aside class="article-sidebar">
      <nav class="toc-sidebar" aria-label="目录">
      <div class="toc-title">本页目录</div>
      {toc_html}
    </nav>
    </aside>
  </div>
</main>
<button id="back-to-top" aria-label="回到顶部" title="回到顶部">↑</button>
<div id="footer-placeholder"></div>
<script src="/js/include.js"></script>
<script src="/js/render.js"></script>
<div id="cookie-banner" class="cookie-banner">
  <p>本站使用 cookie 进行分析和个性化广告。继续使用即表示您同意我们的 <a href="/privacy.html">隐私政策</a>。</p>
  <button onclick="acceptCookies()">接受</button>
</div>
<script>
function acceptCookies(){{localStorage.setItem('cookies_accepted','1');document.getElementById('cookie-banner').classList.remove('show');}}
if(!localStorage.getItem('cookies_accepted')){{document.addEventListener('DOMContentLoaded',function(){{document.getElementById('cookie-banner').classList.add('show');}});}}
</script>
</body>
</html>"""

out_path = ROOT / "daily" / f"{SLUG}.html"
out_path.parent.mkdir(exist_ok=True)
out_path.write_text(html, encoding="utf-8")
print(f"CN daily page generated: {out_path}")
print(f"Size: {len(html):,} bytes")
