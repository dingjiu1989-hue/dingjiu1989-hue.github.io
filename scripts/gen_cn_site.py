#!/usr/bin/env python3
"""Generate all Chinese site HTML files from /articles.json in one pass."""
import json, re, html as html_mod, urllib.parse
from pathlib import Path
from datetime import date
from scripts.site_config import BASE_URL

ROOT = Path(__file__).resolve().parent.parent
ARTICLES_JSON = ROOT / 'articles.json'
TODAY = date.today().isoformat()
BASE = BASE_URL

CN_SITE_NAME = "AI自习室"
CN_BOARD_NAMES = {
    'daily': 'AI每日资讯',
    'tech': '技术教程',
    'sidehustle': '副业资源',
    'tools': '工具推荐',
    'ai': 'AI 教程',
    'ai-analyst': 'AI分析师',
}
CN_BOARD_DESCS = {
    'daily': '每日精选AI领域十大新闻，中英双语，附原文来源链接。',
    'tech': '编程教程、开发者工具与效率提升指南。',
    'sidehustle': '自由职业、远程工作与开发者副业收入策略。',
    'tools': '精选开发者工具、效率软件与技术栈推荐。',
    'ai': 'AI工具、提示工程与LLM实用指南。',
    'ai-analyst': 'AI驱动的深度研究报告，涵盖半导体、科技、行业分析与投资洞察。',
}
CN_BOARD_KEYWORDS = {
    'daily': 'AI新闻, 人工智能, 科技新闻, AI每日资讯',
    'tech': '编程教程, 开发者工具, 软件工程, 编程指南',
    'sidehustle': '自由职业, 远程工作, 副业收入, 开发者创业',
    'tools': '开发者工具, 效率工具, 软件推荐, 技术栈',
    'ai': 'AI工具, LLM, 提示工程, 机器学习, 人工智能教程',
    'ai-analyst': 'AI分析, 深度研究, 行业报告, 半导体, 投资分析, 科技研究',
}
CN_BOARD_ICONS = {
    'daily': '📰',
    'tech': '💻',
    'sidehustle': '💼',
    'tools': '🛠️',
    'ai': '🤖',
    'ai-analyst': '🔬',
}
# Boards with standalone HTML pages — skip auto-generation to preserve rich content
STANDALONE_BOARDS = {'ai-analyst'}


def md_to_html(md_text):
    try:
        import markdown as md_lib
        html = md_lib.markdown(md_text, extensions=['fenced_code', 'codehilite', 'tables'])
        html = re.sub(r'<h1>.*?</h1>\s*', '', html, count=1)
        return html
    except ImportError:
        lines = md_text.split('\n')
        html_parts = []
        in_code = False
        for line in lines:
            if line.startswith('```'):
                if in_code:
                    html_parts.append('</code></pre>')
                    in_code = False
                else:
                    html_parts.append('<pre><code>')
                    in_code = True
            elif in_code:
                html_parts.append(html_mod.escape(line) + '\n')
            elif line.startswith('### '):
                html_parts.append(f'<h4>{line[4:]}</h4>')
            elif line.startswith('## '):
                html_parts.append(f'<h3>{line[3:]}</h3>')
            elif line.startswith('# '):
                html_parts.append(f'<h2>{line[2:]}</h2>')
            elif line.startswith('- '):
                html_parts.append(f'<li>{line[2:]}</li>')
            elif line.startswith('1. '):
                html_parts.append(f'<li>{line[3:]}</li>')
            elif line.strip() == '':
                html_parts.append('<br>')
            elif line.startswith('|'):
                html_parts.append(f'<p>{line}</p>')
            else:
                html_parts.append(f'<p>{line}</p>')
        return '\n'.join(html_parts)


def _strip_title_headings(md_text, title):
    lines = md_text.split('\n')
    result = []
    in_code = False
    for line in lines:
        if line.strip().startswith('```'):
            in_code = not in_code
            result.append(line)
            continue
        if in_code:
            result.append(line)
            continue
        m = re.match(r'^(#{1,6})\s+(.+)$', line)
        if m and m.group(2).strip() == title:
            continue
        result.append(line)
    return '\n'.join(result)


def get_body(slug, board_id, title=None):
    """Get article body from md/zh/ markdown files."""
    md_path = ROOT / 'md' / 'zh' / board_id / f'{slug}.md'
    if md_path.exists():
        content = md_path.read_text(encoding='utf-8')
        if content.startswith('---'):
            end = content.find('---', 3)
            if end > 0:
                content = content[end + 3:].strip()
        if title:
            content = _strip_title_headings(content, title)
        html = md_to_html(content)
        if html.strip():
            return html
    return f'<p>内容即将上线。</p>'


def _js(s):
    """Escape a string for JSON-LD embedding."""
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ').replace('\r', '')


def _esc(s):
    """Escape a string for HTML attribute embedding."""
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')


def _extract_headings(body_html):
    """Extract h2/h3 headings from HTML body for TOC generation."""
    headings = []
    for m in re.finditer(r'<h([23])[^>]*>(.+?)</h\1>', body_html):
        level = int(m.group(1))
        text = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        hid = re.sub(r'[^\w\s一-鿿㐀-䶿-]', '', text.lower())
        hid = re.sub(r'\s+', '-', hid)
        headings.append({'level': level, 'text': text, 'id': hid})
    return headings


def make_article_html(art, board_id, board_name, all_posts):
    """Generate a single CN article page at /{board}/{slug}.html"""
    slug = art['slug']
    art_url = f'{BASE}/{board_id}/{slug}.html'
    en_url = f'{BASE}/en/{board_id}/{slug}.html'
    cn_hreflang = f'    <link rel="alternate" hreflang="zh-CN" href="{art_url}">\n'

    body_raw = get_body(slug, board_id, art.get('title'))

    # Table of contents from h2/h3
    headings = _extract_headings(body_raw)
    toc_items_html = ''
    if headings:
        items = []
        for h in headings:
            indent = '  ' if h['level'] == 3 else ''
            items.append(f'{indent}<li><a href="#{h["id"]}">{h["text"]}</a></li>')
        toc_items_html = '\n'.join(items)

    toc_inline_html = ''
    toc_sidebar_html = ''
    if headings:
        toc_items = ''.join(f'<li><a href="#{h["id"]}">{h["text"]}</a></li>' for h in headings)
        toc_inline_html = f'<details class="article-toc-inline"><summary>目录（{len(headings)}）</summary><ol>{toc_items}</ol></details>'
        nav_items = ''.join(
            f'<li class="toc-h{h["level"]}"><a href="#{h["id"]}">{h["text"]}</a></li>'
            for h in headings
        )
        toc_sidebar_html = f'<nav class="toc-sidebar" aria-label="目录"><div class="toc-title">本页目录</div><ul>{nav_items}</ul></nav>'

    # Meta
    tags = art.get('tags', []) if isinstance(art.get('tags', []), list) else []
    tags_str = ', '.join(tags)
    meta_desc = art.get('description', '')[:160]
    title_for_meta = art['title'][:120]

    # Cover image
    cover_url = f'{BASE}/images/covers/en/{board_id}/{slug}.png'
    cover_webp = f'{BASE}/images/covers/en/{board_id}/{slug}.webp'

    # Read time & word estimate
    text_only = re.sub(r'<[^>]+>', ' ', body_raw)
    word_count = len(text_only.split())
    word_est = max(word_count, len(body_raw) // 5)
    read_time = max(1, word_est // 200)

    # Views
    views = art.get('views', 0)
    article_views = f'{views:,}' if views else '0'

    # Date
    pub_date = art.get('date', TODAY)
    mod_date = art.get('lastActive', pub_date)

    # OG/Twitter
    og_tags = f'''    <meta property="og:title" content="{_esc(title_for_meta)}">
    <meta property="og:description" content="{_esc(meta_desc)}">
    <meta property="og:url" content="{art_url}">
    <meta property="og:type" content="article">
    <meta property="og:site_name" content="{CN_SITE_NAME}">
    <meta property="og:locale" content="zh_CN">
    <meta property="og:image" content="{cover_url}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="article:published_time" content="{pub_date}">
    <meta property="article:modified_time" content="{mod_date}">
    <meta property="article:section" content="{board_name}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{_esc(title_for_meta)}">
    <meta name="twitter:description" content="{_esc(meta_desc)}">
    <meta name="twitter:image" content="{cover_url}">'''

    tags_h = '\n'.join(f'          <span class="tag-cat">{_esc(t)}</span>' for t in tags)
    pin_h = '          <span class="tag-pin">📌 置顶</span>\n' if art.get('pinned') else ''

    # Prev/next navigation
    board_posts = sorted(
        [p for p in all_posts if p['board_id'] == board_id],
        key=lambda x: x.get('date', '')
    )
    prev_next = ''
    prev_next_buttons = ''
    try:
        idx = next(i for i, p in enumerate(board_posts) if p['slug'] == slug)
        prev_link = ''
        next_link = ''
        if idx > 0:
            p = board_posts[idx - 1]
            prev_link = f'<link rel="prev" href="{BASE}/{board_id}/{p["slug"]}.html">\n'
        if idx < len(board_posts) - 1:
            p = board_posts[idx + 1]
            next_link = f'<link rel="next" href="{BASE}/{board_id}/{p["slug"]}.html">\n'
        prev_next = prev_link + next_link

        prev_btn = ''
        next_btn = ''
        if idx > 0:
            p = board_posts[idx - 1]
            prev_btn = f'<a class="prev" href="/{board_id}/{p["slug"]}.html" title="{_esc(p["title"])}">← 上一篇<br><small>{_esc(p["title"][:60])}</small></a>'
        if idx < len(board_posts) - 1:
            p = board_posts[idx + 1]
            next_btn = f'<a class="next" href="/{board_id}/{p["slug"]}.html" title="{_esc(p["title"])}">下一篇 →<br><small>{_esc(p["title"][:60])}</small></a>'
        if prev_btn or next_btn:
            prev_next_buttons = prev_btn + (next_btn or '')
    except StopIteration:
        pass

    # Related articles — same board, tag overlap scoring
    related_html = ''
    art_tags_lower = [t.lower() for t in tags]
    if all_posts:
        scored = []
        for other in all_posts:
            if other['slug'] == slug:
                continue
            other_tags = [t.lower() for t in other.get('tags', [])] if isinstance(other.get('tags', []), list) else []
            score = 0
            if other.get('board_id') == board_id:
                score += 5
            score += len(set(art_tags_lower) & set(other_tags)) * 3
            if other.get('date', '') > pub_date:
                score += 1
            if score > 0:
                scored.append((score, other))
        scored.sort(key=lambda x: x[0], reverse=True)
        top = scored[:6]
        if top:
            cards = []
            for _, p in top:
                date_str = p.get('date', '')[:10]
                cards.append(
                    f'<a class="related-card" href="/{p["board_id"]}/{p["slug"]}.html">'
                    f'<span class="related-title">{_esc(p["title"])}</span>'
                    f'<span class="related-meta">{CN_BOARD_NAMES.get(p["board_id"], p["board_id"])} · {date_str}</span>'
                    f'</a>'
                )
            related_html = '\n'.join(cards)

    # Share URLs
    share_twitter = f'https://twitter.com/intent/tweet?text={urllib.parse.quote(art["title"])}&url={urllib.parse.quote(art_url)}'
    share_linkedin = f'https://www.linkedin.com/sharing/share-offsite/?url={urllib.parse.quote(art_url)}'
    share_reddit = f'https://www.reddit.com/submit?title={urllib.parse.quote(art["title"])}&url={urllib.parse.quote(art_url)}'
    share_hn = f'https://news.ycombinator.com/submitlink?u={urllib.parse.quote(art_url)}&t={urllib.parse.quote(art["title"])}'
    share_email = f'mailto:?subject={urllib.parse.quote(art["title"])}&body={urllib.parse.quote(art_url)}'

    # Structured data
    if board_id == "daily":
        article_type = "NewsArticle"
    else:
        article_type = "TechArticle"

    art_tags = [t.lower() for t in tags]
    if any(w in art_tags for w in ['advanced', 'expert', 'production', 'optimization', 'scaling', 'performance', '高级', '进阶', '专家', '生产', '优化']):
        proficiency = ',\n      "proficiencyLevel": "Advanced"'
    elif any(w in art_tags for w in ['beginner', 'introduction', 'getting-started', 'guide', 'fundamental', 'basic', 'quickstart', 'overview', '入门', '新手', '基础', '教程', '指南']):
        proficiency = ',\n      "proficiencyLevel": "Beginner"'
    else:
        proficiency = ',\n      "proficiencyLevel": "Intermediate"' if article_type == "TechArticle" else ''

    about_tags = ', '.join(f'{{"@type": "Thing", "name": "{_js(t)}"}}' for t in tags[:8])
    body_json = json.dumps(re.sub(r'<[^>]+>', ' ', body_raw).replace('\n', ' ').strip()[:5000], ensure_ascii=False)

    # Robots meta
    robots_meta = 'index, follow, max-image-preview:large'

    # See also (inline mid-article)
    see_also_html = ''
    if related_html:
        see_also_html = '<section class="see-also"><h3>📖 相关阅读</h3><div class="related-grid">' + related_html + '</div></section>'

    # Mid-content ad
    ad_mid = '''        <div class="ad-container">
          <div class="ad-label">— 广告 —</div>
          <ins class="adsbygoogle"
               style="display:block"
               data-ad-client="ca-pub-3258394111169733"
               data-ad-format="auto"
               data-full-width-responsive="true"></ins>
          <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
        </div>'''

    return f'''<!DOCTYPE html>
<html lang="zh-CN" data-render="related" data-board="{board_id}" data-exclude="{slug}">
<head>
    <meta charset="UTF-8">
    <meta name="google-site-verification" content="XzThATs15kR08VOM-tCxIztKjEGW8ft-T75SmH_Wz38" />
    <meta name="msvalidate.01" content="6D67B742819758DC63A576B495E40ACC" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="base-path" content="">
    <link rel="preconnect" href="https://www.googletagmanager.com" crossorigin>
    <link rel="dns-prefetch" href="https://www.googletagmanager.com">
    <link rel="preconnect" href="https://pagead2.googlesyndication.com" crossorigin>
    <link rel="dns-prefetch" href="https://pagead2.googlesyndication.com">
    <link rel="preconnect" href="https://googleads.g.doubleclick.net" crossorigin>
    <link rel="dns-prefetch" href="https://googleads.g.doubleclick.net">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <link rel="alternate icon" href="/favicon.ico">
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-XGFYGQE9NS"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-XGFYGQE9NS');
    </script>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3258394111169733" crossorigin="anonymous"></script>
{og_tags}
    <link rel="preload" as="image" href="{cover_webp}" type="image/webp" fetchpriority="high">
    <title>{_esc(art['title'])} — {CN_SITE_NAME}</title>
    <meta name="description" content="{_esc(meta_desc)}">
    <meta name="keywords" content="{_esc(tags_str)}">
{cn_hreflang}    <link rel="alternate" hreflang="en" href="{en_url}">
    <link rel="canonical" href="{art_url}">{prev_next}
    <meta name="robots" content="{robots_meta}">
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "{article_type}",
      "headline": "{_js(art['title'])}",
      "description": "{_js(art.get('description', ''))}",
      "image": "{cover_url}",
      "datePublished": "{pub_date}",
      "dateModified": "{mod_date}",
      "wordCount": "{word_est}",
      "keywords": "{_js(tags_str)}",
      "about": [{about_tags}],
      "inLanguage": "zh-CN",
      "isAccessibleForFree": true{proficiency},
      "license": "https://creativecommons.org/licenses/by/4.0/",
      "author": {{"@type": "Person", "name": "{CN_SITE_NAME}"}},
      "publisher": {{
        "@type": "Organization",
        "name": "{CN_SITE_NAME}",
        "url": "{BASE}/",
        "logo": {{"@type": "ImageObject", "url": "{BASE}/images/logo.png"}},
        "sameAs": ["https://github.com/dingjiu1989-hue", "https://dev.to/dingjiu1989"]
      }},
      "mainEntityOfPage": {{"@type": "WebPage", "@id": "{art_url}"}},
      "articleBody": {body_json}
    }}
    </script>
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{"@type": "ListItem", "position": 1, "name": "首页", "item": "{BASE}/"}},
        {{"@type": "ListItem", "position": 2, "name": "{board_name}", "item": "{BASE}/{board_id}/"}},
        {{"@type": "ListItem", "position": 3, "name": "{_js(art['title'])}"}}
      ]
    }}
    </script>
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "WebPage",
      "speakable": {{
        "@type": "SpeakableSpecification",
        "xpath": ["/html/head/title", "/html/head/meta[@name='description']/@content"]
      }}
    }}
    </script>
    <link rel="alternate" type="application/rss+xml" title="{CN_SITE_NAME} (中文)" href="/feed.xml">
</head>
<body>
<div id="reading-progress-container"><div id="reading-progress-bar"></div></div>
<div id="nav-placeholder"></div>
<main>
  <div class="breadcrumb container">
    <a href="/">首页</a> › <a href="/{board_id}/">{board_name}</a>
  </div>
  <div class="article-layout">
    <div class="article-main">
      <article>
        <div class="article-tags">{pin_h}{tags_h}</div>
        <h1 class="article-title">{_esc(art['title'])}</h1>
        <div class="article-meta">
          <span class="author-name">By {CN_SITE_NAME}</span>
          <span class="meta-sep">·</span>
          <time datetime="{pub_date}">{pub_date}</time>
          <span class="meta-sep">·</span>
          <span>{read_time} 分钟阅读</span>
          <span class="meta-sep">·</span>
          <span>{article_views} 次浏览</span>
          <span class="meta-sep">·</span>
          <span>{word_est} 字</span>
        </div>
        <picture><source srcset="{cover_webp}" type="image/webp"><img class="article-cover" src="{cover_url}" alt="{_esc(art['title'])}" width="1200" height="630" fetchpriority="high" decoding="sync"></picture>
        {toc_inline_html}
        <div class="article-body">{body_raw}</div>{see_also_html}
        {ad_mid}
        <div class="share-bar">
          <span>分享</span>
          <a href="{share_twitter}" target="_blank" rel="noopener" aria-label="分享到 X">𝕏</a>
          <a href="{share_linkedin}" target="_blank" rel="noopener" aria-label="分享到 LinkedIn">in</a>
          <a href="{share_reddit}" target="_blank" rel="noopener" aria-label="分享到 Reddit">Reddit</a>
          <a href="{share_hn}" target="_blank" rel="noopener" aria-label="分享到 HN">HN</a>
          <a href="{share_email}" aria-label="通过邮件分享">邮件</a>
          <button class="copy-link-btn" data-url="{art_url}" aria-label="复制链接">复制</button>
        </div>
        <nav class="prev-next-nav" aria-label="文章导航">{prev_next_buttons}</nav>
        <section class="related">
          <div class="related-heading">相关文章</div>
          <div class="related-grid">{related_html}</div>
        </section>
      </article>
      <div class="discussion-cta">
        <p>参与讨论</p>
        <p>有想法或问题？在下方留言 — 你的见解能帮助其他读者。</p>
        <a href="#giscus-section">留下评论</a>
      </div>
      <div id="giscus-section" data-giscus-loaded="false"></div>
    </div>
    <aside class="article-sidebar">
      {toc_sidebar_html}
    </aside>
  </div>
</main>
<button id="back-to-top" aria-label="回到顶部" title="回到顶部">↑</button>
<div id="footer-placeholder"></div>
<script src="/js/include.js"></script>
<script src="/js/render.js"></script>
<div id="cookie-banner" class="cookie-banner">
  <p>本站使用 cookie 进行分析和个性化广告。继续使用即同意我们的 <a href="/privacy.html">隐私政策</a>。</p>
  <button onclick="acceptCookies()">接受</button>
</div>
<script>
function acceptCookies(){{localStorage.setItem('cookies_accepted','1');document.getElementById('cookie-banner').classList.remove('show');}}
if(!localStorage.getItem('cookies_accepted')){{document.addEventListener('DOMContentLoaded',function(){{document.getElementById('cookie-banner').classList.add('show');}});}}
</script>
</body>
</html>'''


def make_homepage(data):
    """Generate /index.html (CN homepage)"""
    boards = data['boards']
    total_boards = len(boards)
    total_posts = sum(len(b['posts']) for b in boards)
    site = data['site']

    noscript_hp = ''
    for b in boards:
        icon = CN_BOARD_ICONS.get(b['id'], b.get('icon', ''))
        links = ''.join(f'<li><a href="/{b["id"]}/{p["slug"]}.html">{p["title"]}</a></li>' for p in b['posts'][:8])
        noscript_hp += f'<section><h3>{icon} {b["name"]}</h3><ul>{links}</ul></section>'

    return f'''<!DOCTYPE html>
<html lang="zh-CN" data-render="homepage">
<head>
    <meta charset="UTF-8">
    <meta name="google-site-verification" content="XzThATs15kR08VOM-tCxIztKjEGW8ft-T75SmH_Wz38" />
    <meta name="msvalidate.01" content="6D67B742819758DC63A576B495E40ACC" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="base-path" content="">
    <link rel="preconnect" href="https://www.googletagmanager.com" crossorigin>
    <link rel="dns-prefetch" href="https://www.googletagmanager.com">
    <link rel="preconnect" href="https://pagead2.googlesyndication.com" crossorigin>
    <link rel="dns-prefetch" href="https://pagead2.googlesyndication.com">
    <link rel="preconnect" href="https://googleads.g.doubleclick.net" crossorigin>
    <link rel="dns-prefetch" href="https://googleads.g.doubleclick.net">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <link rel="alternate icon" href="/favicon.ico">
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-XGFYGQE9NS"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-XGFYGQE9NS');
    </script>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3258394111169733" crossorigin="anonymous"></script>
    <meta property="og:title" content="{CN_SITE_NAME} — {site['tagline']}">
    <meta property="og:description" content="聚合优质AI开发资源，涵盖技术教程、副业策略、工具推荐与AI应用指南。">
    <meta property="og:url" content="{BASE}/">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="{CN_SITE_NAME}">
    <meta property="og:locale" content="zh_CN">
    <meta property="og:image" content="{BASE}/images/logo.png">
    <meta property="og:image:width" content="512">
    <meta property="og:image:height" content="512">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{CN_SITE_NAME} — {site['tagline']}">
    <meta name="twitter:description" content="聚合优质AI开发资源，涵盖技术教程、副业策略、工具推荐与AI应用指南。">
    <meta name="twitter:image" content="{BASE}/images/logo.png">
    <title>{CN_SITE_NAME} — {site['tagline']}</title>
    <meta name="description" content="聚合优质AI开发资源，涵盖技术教程、副业策略、工具推荐与AI应用指南。">
    <link rel="stylesheet" href="/css/style.css">
    <link rel="alternate" type="application/rss+xml" title="{CN_SITE_NAME} RSS" href="/feed.xml">
    <link rel="alternate" hreflang="zh-CN" href="{BASE}/">
    <link rel="alternate" hreflang="en" href="{BASE}/en/">
    <link rel="canonical" href="{BASE}/">
    <meta name="robots" content="index, follow">
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "{CN_SITE_NAME}",
      "url": "{BASE}/",
      "description": "{site['tagline']}",
      "potentialAction": {{
        "@type": "SearchAction",
        "target": {{
          "@type": "EntryPoint",
          "urlTemplate": "{BASE}/?search={{search_term_string}}"
        }},
        "query-input": "required name=search_term_string"
      }}
    }}
    </script>
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Organization",
      "name": "{CN_SITE_NAME}",
      "url": "{BASE}/",
      "logo": "{BASE}/images/logo.png",
      "sameAs": ["https://github.com/dingjiu1989-hue", "https://dev.to/dingjiu1989"],
      "foundingDate": "2025"
    }}
    </script>
    <script>
    (function(){{
      if (window.location.pathname !== '/') return;
      var ua = navigator.userAgent.toLowerCase();
      if (/bot|spider|crawler|googlebot|bingbot/i.test(ua)) return;
      var choice = localStorage.getItem('lang');
      if (!choice) {{
        var lang = navigator.language || '';
        if (!lang.startsWith('zh')) {{
          window.location.replace('/en/');
        }}
      }}
    }})();
    </script>
    <link rel="alternate" type="application/rss+xml" title="{CN_SITE_NAME} (中文)" href="/feed.xml">
</head>
<body>

<div id="nav-placeholder"></div>

<main>
  <section class="hero">
    <div class="container">
      <h1>📚 欢迎来到 AI 自习室</h1>
      <p>{site['tagline']}</p>
      <div class="hero-stats" id="hero-stats">
        <span class="hero-stat">📂 {total_boards} 个板块</span>
        <span class="hero-stat">📝 {total_posts} 篇文章</span>
      </div>
    </div>
  </section>

  <div class="container">
    <div class="search-bar">
      <input type="text" id="search-input" placeholder="搜索文章标题、标签或关键词..." autocomplete="off">
      <div id="search-results" class="search-results"></div>
    </div>

    <div class="stats-bar" id="stats-bar">
      <span>📊 文章总数：{total_posts}</span>
    </div>

    <div id="homepage-boards"><noscript>{noscript_hp}</noscript></div>
  </div>
</main>

<div id="footer-placeholder"></div>

<script src="/js/include.js"></script>
<script src="/js/render.js"></script>
<script src="/js/search.js"></script>
<div id="cookie-banner" class="cookie-banner">
  <p>本站使用 cookie 进行分析和个性化广告。继续使用即同意我们的 <a href="/privacy.html">隐私政策</a>。</p>
  <button onclick="acceptCookies()">接受</button>
</div>
<script>
function acceptCookies(){{localStorage.setItem('cookies_accepted','1');document.getElementById('cookie-banner').classList.remove('show');}}
if(!localStorage.getItem('cookies_accepted')){{document.addEventListener('DOMContentLoaded',function(){{document.getElementById('cookie-banner').classList.add('show');}});}}
</script>
</body>
</html>'''


def make_category(data, board_id):
    """Generate /{board}/index.html"""
    board = next(b for b in data['boards'] if b['id'] == board_id)
    count = len(board['posts'])
    cn_url = f'{BASE}/{board_id}/'
    en_url = f'{BASE}/en/{board_id}/'

    item_list = ', '.join(
        '{{"@type": "ListItem", "position": {i}, "url": "{url}"}}'.format(
            i=i+1,
            url=f'{BASE}/{board_id}/{art["slug"]}.html'
        )
        for i, art in enumerate(board['posts'])
    )

    title = CN_BOARD_NAMES.get(board_id, board['name'])
    desc = CN_BOARD_DESCS.get(board_id, '')
    keywords = CN_BOARD_KEYWORDS.get(board_id, '')
    icon = CN_BOARD_ICONS.get(board_id, board.get('icon', ''))

    noscript_links = ''.join(
        f'<li><a href="/{board_id}/{p["slug"]}.html">{p["title"]}</a> <small>{p["date"]}</small></li>'
        for p in board['posts']
    )

    return f'''<!DOCTYPE html>
<html lang="zh-CN" data-render="category" data-board="{board_id}">
<head>
    <meta charset="UTF-8">
    <meta name="google-site-verification" content="XzThATs15kR08VOM-tCxIztKjEGW8ft-T75SmH_Wz38" />
    <meta name="msvalidate.01" content="6D67B742819758DC63A576B495E40ACC" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="base-path" content="">
    <link rel="preconnect" href="https://www.googletagmanager.com" crossorigin>
    <link rel="dns-prefetch" href="https://www.googletagmanager.com">
    <link rel="preconnect" href="https://pagead2.googlesyndication.com" crossorigin>
    <link rel="dns-prefetch" href="https://pagead2.googlesyndication.com">
    <link rel="preconnect" href="https://googleads.g.doubleclick.net" crossorigin>
    <link rel="dns-prefetch" href="https://googleads.g.doubleclick.net">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <link rel="alternate icon" href="/favicon.ico">
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-XGFYGQE9NS"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-XGFYGQE9NS');
    </script>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3258394111169733" crossorigin="anonymous"></script>
    <meta property="og:title" content="{title} — {CN_SITE_NAME}">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="{cn_url}">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="{CN_SITE_NAME}">
    <meta property="og:locale" content="zh_CN">
    <meta property="og:image" content="{BASE}/images/logo.png">
    <meta property="og:image:width" content="512">
    <meta property="og:image:height" content="512">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title} — {CN_SITE_NAME}">
    <meta name="twitter:description" content="{desc}">
    <meta name="twitter:image" content="{BASE}/images/logo.png">
    <title>{title} — {CN_SITE_NAME}</title>
    <meta name="description" content="{desc}">
    <meta name="keywords" content="{keywords}">
    <link rel="stylesheet" href="/css/style.css">
    <link rel="alternate" hreflang="zh-CN" href="{cn_url}">
    <link rel="alternate" hreflang="en" href="{en_url}">
    <link rel="canonical" href="{cn_url}">
    <meta name="robots" content="index, follow">
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "CollectionPage",
      "name": "{title}",
      "url": "{cn_url}",
      "description": "{desc}",
      "numberOfItems": {count},
      "inLanguage": "zh-CN",
      "isAccessibleForFree": true,
      "about": {{"@type": "Thing", "name": "{title}"}},
      "mainEntity": {{"@type": "ItemList", "itemListElement": [{item_list}]}}
    }}
    </script>
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{"@type": "ListItem", "position": 1, "name": "首页", "item": "{BASE}/"}},
        {{"@type": "ListItem", "position": 2, "name": "{title}", "item": "{cn_url}"}}
      ]
    }}
    </script>
    <link rel="alternate" type="application/rss+xml" title="{CN_SITE_NAME} (中文)" href="/feed.xml">
</head>
<body>

<div id="nav-placeholder"></div>

<main>
  <div class="container">
    <div class="breadcrumb">
      <a href="/">首页</a> › {title}
    </div>

    <div class="page-header">
      <div>
        <h1>{icon} {title}</h1>
        <p class="board-description">{desc}（{count} 篇文章）</p>
      </div>
      <label for="sort-select" class="sr-only">文章排序</label>
      <select id="sort-select" class="sort-select" disabled>
        <option>排序：最新 ↓</option>
      </select>
    </div>

    <div id="category-posts"><noscript><ul>{noscript_links}</ul></noscript></div>
  </div>
</main>

<div id="footer-placeholder"></div>

<script src="/js/include.js"></script>
<script src="/js/render.js"></script>
<div id="cookie-banner" class="cookie-banner">
  <p>本站使用 cookie 进行分析和个性化广告。继续使用即同意我们的 <a href="/privacy.html">隐私政策</a>。</p>
  <button onclick="acceptCookies()">接受</button>
</div>
<script>
function acceptCookies(){{localStorage.setItem('cookies_accepted','1');document.getElementById('cookie-banner').classList.remove('show');}}
if(!localStorage.getItem('cookies_accepted')){{document.addEventListener('DOMContentLoaded',function(){{document.getElementById('cookie-banner').classList.add('show');}});}}
</script>
</body>
</html>'''


def make_all_html(data):
    """Generate /all.html with pre-rendered article links by board."""
    boards_html = ''
    total = 0
    for board in data['boards']:
        posts = board['posts']
        total += len(posts)
        board_name = CN_BOARD_NAMES.get(board['id'], board['name'])
        items = ''
        for p in sorted(posts, key=lambda x: x.get('date', ''), reverse=True):
            items += f'<li><a href="/{board["id"]}/{p["slug"]}.html">{p["title"]}</a></li>'
        boards_html += (
            f'<section class="all-board">'
            f'<h3>{board.get("icon", "")} {board_name} <span class="board-count">{len(posts)}</span></h3>'
            f'<ul>{items}</ul>'
            f'</section>'
        )

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="google-site-verification" content="XzThATs15kR08VOM-tCxIztKjEGW8ft-T75SmH_Wz38" />
    <meta name="msvalidate.01" content="6D67B742819758DC63A576B495E40ACC" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>全部 {total} 篇文章 — {CN_SITE_NAME}</title>
    <meta name="description" content="共 {total} 篇文章，涵盖 {len(data['boards'])} 个板块：技术教程、AI教程、副业资源、工具推荐、AI每日资讯。">
    <link rel="stylesheet" href="/css/style.css">
    <link rel="canonical" href="{BASE}/all.html">
    <link rel="alternate" hreflang="zh-CN" href="{BASE}/all.html">
    <link rel="alternate" hreflang="en" href="{BASE}/en/all.html">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="全部 {total} 篇文章 — {CN_SITE_NAME}">
    <meta property="og:description" content="共 {total} 篇文章，涵盖 {len(data['boards'])} 个板块。">
    <meta property="og:url" content="{BASE}/all.html">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="{CN_SITE_NAME}">
    <meta property="og:image" content="{BASE}/images/og-default.jpg">
    <meta property="og:locale" content="zh_CN">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="全部 {total} 篇文章 — {CN_SITE_NAME}">
    <meta name="twitter:description" content="共 {total} 篇文章，涵盖 {len(data['boards'])} 个板块。">
    <meta name="twitter:image" content="{BASE}/images/og-default.jpg">
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "CollectionPage",
      "name": "全部文章 — {CN_SITE_NAME}",
      "description": "共 {total} 篇文章，涵盖 {len(data['boards'])} 个板块。",
      "url": "{BASE}/all.html",
      "isAccessibleForFree": true,
      "license": "https://creativecommons.org/licenses/by/4.0/",
      "about": {{"@type": "WebSite", "name": "{CN_SITE_NAME}", "url": "{BASE}/"}}
    }}
    </script>
</head>
<body>
<div id="nav-placeholder"></div>
<main>
  <div class="container">
    <div class="breadcrumb"><a href="/">首页</a> › 全部文章</div>
    <div class="page-header">
      <h2>全部文章</h2>
      <span class="post-count">{total} 篇文章，涵盖 {len(data['boards'])} 个板块</span>
    </div>
    {boards_html}
  </div>
</main>
<div id="footer-placeholder"></div>
<script src="/js/include.js"></script>
<div id="cookie-banner" class="cookie-banner">
  <p>本站使用 cookie 进行分析和个性化广告。继续使用即同意我们的 <a href="/privacy.html">隐私政策</a>。</p>
  <button onclick="acceptCookies()">接受</button>
</div>
<script>
function acceptCookies(){{localStorage.setItem('cookies_accepted','1');document.getElementById('cookie-banner').classList.remove('show');}}
if(!localStorage.getItem('cookies_accepted')){{document.addEventListener('DOMContentLoaded',function(){{document.getElementById('cookie-banner').classList.add('show');}});}}
</script>
</body>
</html>'''


def main():
    data = json.loads(ARTICLES_JSON.read_text(encoding='utf-8'))
    created = 0

    # Homepage at /index.html
    hp = ROOT / 'index.html'
    hp.write_text(make_homepage(data), encoding='utf-8')
    created += 1
    print(f'  HTML: {hp}')

    # All articles index at /all.html
    all_page = ROOT / 'all.html'
    all_page.write_text(make_all_html(data), encoding='utf-8')
    created += 1
    print(f'  HTML: {all_page}')

    # Category pages at /{board}/index.html
    for board in data['boards']:
        cat_dir = ROOT / board['id']
        cat_dir.mkdir(exist_ok=True)
        idx = cat_dir / 'index.html'
        idx.write_text(make_category(data, board['id']), encoding='utf-8')
        created += 1
        print(f'  HTML: {idx}')

    # Build flat list of all posts for related posts computation
    all_posts = []
    for board in data['boards']:
        board_name = CN_BOARD_NAMES.get(board['id'], board['name'])
        for art in board['posts']:
            all_posts.append({**art, 'board_id': board['id'], 'board_name': board_name})

    # Article pages at /{board}/{slug}.html
    for board in data['boards']:
        board_name = CN_BOARD_NAMES.get(board['id'], board['name'])
        for art in board['posts']:
            slug = art['slug']
            art_dir = ROOT / board['id']
            art_dir.mkdir(exist_ok=True)
            out_html = art_dir / f'{slug}.html'

            # Skip standalone boards — they have hand-crafted HTML with rich content
            if board['id'] in STANDALONE_BOARDS:
                if out_html.exists():
                    print(f'  SKIP (standalone): {out_html}')
                    continue
                else:
                    print(f'  WARNING: Standalone HTML missing for {slug}, using template fallback')

            md_path = ROOT / 'md' / 'zh' / board['id'] / f'{slug}.md'
            if not md_path.exists():
                print(f'  WARNING: No md file for {slug}, skipping')
                continue
            p = art_dir / f'{slug}.html'
            p.write_text(make_article_html(art, board['id'], board_name, all_posts), encoding='utf-8')
            created += 1
            print(f'  HTML: {p}')

    print(f'\nCreated {created} files.')


if __name__ == '__main__':
    main()
