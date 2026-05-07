#!/usr/bin/env python3
"""Batch 3: 7 articles to reach 45 total. Staggered dates for natural growth pattern."""
import json, re, sys
from pathlib import Path
from datetime import date, timedelta

ROOT = Path(__file__).resolve().parent.parent
ARTICLES_JSON = ROOT / 'articles.json'
SITEMAP = ROOT / 'sitemap.xml'
TODAY = date.today()
BASE = 'https://dingjiu1989-hue.github.io'

NEW = [
    # ═══ TOOLS (3) ══════════════════════════════════════════════
    dict(board='tools', slug='password-manager-comparison', date=TODAY.isoformat(),
         title='2026 年最佳密码管理器对比：LastPass vs 1Password vs Bitwarden',
         description='六大主流密码管理器全方位对比，涵盖安全性、易用性、跨平台、价格，帮你选出最适合的一款。',
         tags=['密码管理', '安全', '对比评测'], replies=38, hot=True,
         body='''<p>密码管理器是现代人必备的安全工具——你不可能记住几十个不同的强密码。选对一款能用十年。</p>
<h2>六大密码管理器对比</h2>
<table><tr><th>产品</th><th>免费版</th><th>付费版</th><th>开源</th><th>亮点</th></tr>
<tr><td>Bitwarden</td><td>✅ 功能完整</td><td>$10/年</td><td>✅</td><td>性价比最高，开源可自部署</td></tr>
<tr><td>1Password</td><td>❌ 14天试用</td><td>$3/月</td><td>❌</td><td>UI 最美，家庭共享方便</td></tr>
<tr><td>LastPass</td><td>✅ 单设备</td><td>$3/月</td><td>❌</td><td>老牌，但近年有安全事件</td></tr>
<tr><td>Proton Pass</td><td>✅ 无限设备</td><td>$3/月</td><td>✅</td><td>Proton 生态，隐私最强</td></tr>
<tr><td>Apple 密码</td><td>✅ 内置</td><td>—</td><td>❌</td><td>Apple 生态内最便捷</td></tr>
<tr><td>KeePassXC</td><td>✅ 完全免费</td><td>—</td><td>✅</td><td>极客首选，完全本地离线</td></tr></table>
<h2>怎么选</h2>
<ul><li><strong>大多数用户</strong> → Bitwarden。免费版功能够用，$10/年的家庭版简直是白送。</li><li><strong>注重体验</strong> → 1Password。界面设计优雅，Watchtower 安全预警功能好用，家庭共享体验最佳。</li><li><strong>Apple 全家桶</strong> → Apple 密码 + Bitwarden 组合。日常用 Apple 内置，跨平台需求用 Bitwarden。</li><li><strong>极客/隐私控</strong> → KeePassXC 或自部署 Bitwarden (Vaultwarden)。</li></ul>
<h2>安全提示</h2><p>不要用浏览器内置的密码保存功能——安全性远不如专业密码管理器。记住一个强主密码，开启两步验证。</p>'''),

    dict(board='tools', slug='screen-recording-tools', date=TODAY.isoformat(),
         title='2026 年最佳屏幕录制和视频剪辑工具推荐',
         description='精选 8 款屏幕录制和轻量视频编辑工具，涵盖免费和付费，适合做教程、演示和产品介绍视频。',
         tags=['屏幕录制', '视频工具', '效率'], replies=25,
         body='''<p>做教程、录演示、汇报工作——屏幕录制是高频需求。这些工具从简单录屏到专业剪辑全覆盖。</p>
<h2>录屏工具</h2>
<table><tr><th>工具</th><th>价格</th><th>亮点</th></tr>
<tr><td>OBS Studio</td><td>免费开源</td><td>最强大的免费录屏+直播工具，支持多场景切换</td></tr>
<tr><td>CleanShot X</td><td>$29 一次性</td><td>macOS 最强，截图+录屏+标注+OCR+滚动截图一体</td></tr>
<tr><td>Loom</td><td>免费 25 个视频</td><td>即录即分享，自动生成链接，适合团队沟通</td></tr>
<tr><td>Screen Studio</td><td>$89 一次性</td><td>自动跟随鼠标、平滑缩放，生成的视频非常专业</td></tr></table>
<h2>轻量剪辑</h2>
<ul><li><strong>Descript</strong> — AI 视频编辑器，像编辑文档一样编辑视频，自动去语气词和沉默。免费版够个人用。</li><li><strong>CapCut (剪映国际版)</strong> — 免费且功能强大，自动字幕生成极准，模板丰富。</li><li><strong>DaVinci Resolve</strong> — 专业级免费剪辑软件，调色功能业界顶尖，学习曲线陡但值得。</li><li><strong>iMovie / Clipchamp</strong> — 系统内置，零成本完成简单剪辑。</li></ul>
<h2>场景推荐</h2>
<ul><li>录代码教程 → OBS + DaVinci Resolve</li><li>快速录 Bug 报告 → Loom</li><li>做产品演示 → Screen Studio</li><li>短视频/社媒内容 → CapCut</li></ul>'''),

    dict(board='tools', slug='dev-podcasts', date=TODAY.isoformat(),
         title='10 个程序员必听的播客：学技术、追趋势、听故事',
         description='精选 10 个中文和英文优质技术播客，涵盖编程技能、行业趋势、职业发展和创业故事，通勤和健身时充电最佳。',
         tags=['播客', '学习资源', '开发者'], replies=22,
         body='''<p>播客是被低估的学习渠道——通勤、健身、做家务的时间可以变成高质量的信息输入。这 10 个播客覆盖技术和职业两大维度。</p>
<h2>中文播客</h2>
<table><tr><th>播客</th><th>主题</th><th>更新</th><th>适合</th></tr>
<tr><td>代码时间</td><td>程序员职业成长</td><td>周更</td><td>初中级开发者</td></tr>
<tr><td>Teahour</td><td>技术深度访谈</td><td>不定期</td><td>进阶开发者</td></tr>
<tr><td>枫言枫语</td><td>科技+产品+开发</td><td>周更</td><td>全栈/独立开发者</td></tr>
<tr><td>捕蛇者说</td><td>Python 生态</td><td>月更</td><td>Python 开发者</td></tr>
<tr><td>硅谷101</td><td>科技商业+创投</td><td>周更</td><td>关注科技行业的人</td></tr></table>
<h2>英文播客（练英语+学技术）</h2>
<table><tr><th>播客</th><th>主题</th><th>难度</th></tr>
<tr><td>Syntax.fm</td><td>Web 开发全栈</td><td>中等</td></tr>
<tr><td>Changelog</td><td>开源和软件生态</td><td>中等</td></tr>
<tr><td>Soft Skills Engineering</td><td>职场软技能</td><td>简单</td></tr>
<tr><td>CoRecursive</td><td>编程故事和人物</td><td>中等</td></tr>
<tr><td>Lex Fridman Podcast</td><td>科技+AI+哲学</td><td>较难</td></tr></table>
<h2>收听建议</h2><p>1.5-2x 倍速是甜蜜点——不会漏内容又省时间。Spotify / 小宇宙 / Apple Podcasts 都有。重要的是<b>听完后写三条收获</b>，否则和没听一样。</p>'''),

    # ═══ TECH (2) ═══════════════════════════════════════════════
    dict(board='tech', slug='rest-api-best-practices', date=TODAY.isoformat(),
         title='REST API 设计最佳实践：写出让人愿意用的接口',
         description='从 URL 设计、HTTP 方法选择到错误处理和分页，系统讲解 REST API 设计规范，附常见反模式避坑。',
         tags=['REST API', '后端', '最佳实践'], replies=29, hot=True,
         body='''<p>好的 API 设计让调用方心情愉悦，坏的 API 让他们想砸键盘。这篇文章总结 10 条实战验证的设计原则。</p>
<h2>URL 设计原则</h2>
<ul><li><strong>用名词复数而非动词</strong> — <code>GET /users</code> 不是 <code>GET /getUsers</code>。HTTP 方法已经表达了动作。</li><li><strong>层级关系用嵌套 URL</strong> — <code>GET /users/123/orders</code> 清晰表达了"用户 123 的订单"。</li><li><strong>不要超过 3 层</strong> — <code>/users/123/orders/456/items</code> 太深了，这种情况拆成 <code>/orders/456/items</code>。</li><li><strong>用 kebab-case 不用 camelCase</strong> — <code>/shipping-address</code> 不是 <code>/shippingAddress</code>。SEO 友好，肉眼易读。</li></ul>
<h2>HTTP 方法正确使用</h2>
<table><tr><th>方法</th><th>操作</th><th>幂等?</th><th>示例</th></tr>
<tr><td>GET</td><td>读取</td><td>✅</td><td><code>GET /articles</code></td></tr>
<tr><td>POST</td><td>创建</td><td>❌</td><td><code>POST /articles</code></td></tr>
<tr><td>PUT</td><td>全量更新</td><td>✅</td><td><code>PUT /articles/1</code></td></tr>
<tr><td>PATCH</td><td>部分更新</td><td>❌</td><td><code>PATCH /articles/1</code></td></tr>
<tr><td>DELETE</td><td>删除</td><td>✅</td><td><code>DELETE /articles/1</code></td></tr></table>
<h2>响应格式规范</h2>
<pre><code>{
  "data": { "id": 1, "title": "..." },
  "meta": { "page": 1, "per_page": 20, "total": 150 },
  "errors": null
}</code></pre>
<h2>错误处理</h2>
<ul><li><strong>用正确的 HTTP 状态码</strong> — 400 参数错误、401 未认证、403 无权限、404 不存在、422 参数校验失败、429 频率限制、500 服务器错误。</li><li><strong>错误信息结构化</strong> — 返回 <code>{"errors":[{"code":"VALIDATION_ERROR","field":"email","message":"邮箱格式不正确"}]}</code>，不要只返回一个字符串。</li></ul>
<h2>五大常见反模式</h2>
<ol><li><strong>所有操作都用 POST</strong> — 这是 RPC 不是 REST</li><li><strong>返回所有字段</strong> — 支持 <code>?fields=id,title</code> 让客户端选择需要的字段</li><li><strong>不版本化</strong> — URL 加 <code>/v1/</code> 前缀或在 Header 中指定版本</li><li><strong>不限制分页</strong> — <code>per_page</code> 最大 100，防止一次请求拖垮数据库</li><li><strong>不写 API 文档</strong> — OpenAPI/Swagger 规范是标配</li></ol>'''),

    dict(board='tech', slug='unit-testing-guide', date=TODAY.isoformat(),
         title='单元测试入门：从零到写出第一个可维护的测试',
         description='零基础单元测试入门教程，覆盖 Python/pytest 实战，AAA 模式、Mock、Fixture 核心概念一网打尽。',
         tags=['单元测试', 'Python', '测试'], replies=21,
         body='''<p>写单元测试是你从"会写代码"到"专业开发者"的分水岭。这篇文章用最少的理论带你直接上手。</p>
<h2>为什么必须写测试</h2>
<ul><li><strong>重构有底气</strong> — 有测试覆盖的代码，改完跑一次就知道有没有破坏现有功能</li><li><strong>文档即测试</strong> — 测试描述了函数在各种输入下应该如何表现，比注释更可靠</li><li><strong>减少回归 Bug</strong> — 修一个 Bug 加一个测试，同样的错不会再犯第二次</li></ul>
<h2>AAA 模式（Arrange-Act-Assert）</h2>
<pre><code>def test_add_two_numbers():
    # Arrange（准备）
    a, b = 2, 3
    # Act（执行）
    result = add(a, b)
    # Assert（断言）
    assert result == 5</code></pre>
<h2>第一个真实测试</h2>
<pre><code># user_service.py
def get_full_name(user):
    return f"{user.first_name} {user.last_name}"

# test_user_service.py
def test_get_full_name():
    user = type('User', (), {'first_name': '张', 'last_name': '三'})()
    assert get_full_name(user) == "张 三"

def test_get_full_name_empty_last():
    user = type('User', (), {'first_name': '李', 'last_name': ''})()
    assert get_full_name(user) == "李 "</code></pre>
<h2>Mock 和 Fixture</h2>
<pre><code># Fixture: 共享的测试数据
@pytest.fixture
def sample_user():
    return User(id=1, name="张三", email="zhang@test.com")

def test_user_email(sample_user):
    assert sample_user.email == "zhang@test.com"

# Mock: 隔离外部依赖
@patch("requests.get")
def test_fetch_user(mock_get):
    mock_get.return_value.json.return_value = {"name": "张三"}
    result = fetch_user(1)
    assert result["name"] == "张三"</code></pre>
<h2>什么该测、什么不该测</h2>
<ul><li><strong>该测</strong> — 业务逻辑、边界条件、错误路径、数据转换</li><li><strong>不该测</strong> — 简单的 getter/setter、框架代码、第三方库的内部行为</li></ul>
<h2>起步建议</h2><p>不用追求 100% 覆盖率——那会增加大量维护负担。先给核心业务逻辑写测试，看到覆盖率数字攀升的成就感会推着你继续写。</p>'''),

    # ═══ SIDEHUSTLE (1) ═════════════════════════════════════════
    dict(board='sidehustle', slug='knowledge-monetization', date=TODAY.isoformat(),
         title='如何把你的专业知识变成付费内容：从 0 到月入 5000',
         description='手把手教你将专业技能包装为付费内容产品：在线课程、付费专栏、社群运营，三个变现路径的完整实操指南。',
         tags=['知识付费', '变现', '副业'], replies=24, hot=True,
         body='''<p>你可能不知道自己会的东西值多少钱——在这个知识付费时代，任何专业技能都有变现潜力。这篇文章讲清楚三个主流路径。</p>
<h2>路径一：付费专栏/Newsletter</h2>
<ul><li><strong>平台</strong> — 小报童（国内）、Substack/ConvertKit（海外）</li><li><strong>适合</strong> — 有持续输出能力、对某个领域有深度见解的人</li><li><strong>定价</strong> — 月付 ¥20-50 或年付 ¥199-499</li><li><strong>关键</strong> — 前 100 个付费读者最难，但过了这个坎后口碑传播会加速</li></ul>
<h2>路径二：在线课程</h2>
<ul><li><strong>平台</strong> — 腾讯课堂/网易云课堂（国内）、Udemy/Teachable（海外）</li><li><strong>适合</strong> — 有完整的知识体系、能做结构化输出的人</li><li><strong>定价</strong> — ¥99-499 一门课，Udemy 上 $9.99-199</li><li><strong>关键</strong> — 先录一个免费迷你课验证需求，再投入时间做完整课程</li></ul>
<h2>路径三：付费社群</h2>
<ul><li><strong>平台</strong> — 知识星球（国内）、Discord + Stripe（海外）</li><li><strong>适合</strong> — 喜欢互动、能持续提供价值的人</li><li><strong>定价</strong> — 年费 ¥199-999</li><li><strong>关键</strong> — 社群需要持续运营，不是建了就完事。设定清晰的交付物（如每周分享一个案例）</li></ul>
<h2>从哪个开始</h2>
<p>先做付费专栏——门槛最低，一篇好文章就是一个付费产品。验证市场后再考虑投入更大的课程和社群。关键是<b>开始输出</b>，大部分人都困在"准备"阶段永远没开始。</p>'''),

    # ═══ AI (1) ═════════════════════════════════════════════════
    dict(board='ai', slug='claude-vs-chatgpt', date=TODAY.isoformat(),
         title='Claude vs ChatGPT 2026 深度对比：哪个 AI 更适合你',
         description='Claude 和 ChatGPT 在编程、写作、分析、多模态等方面的真实能力对比，帮你根据不同场景选择最佳 AI 助手。',
         tags=['Claude', 'ChatGPT', '对比评测', 'AI工具'], replies=52, hot=True,
         body='''<p>2026 年 AI 助手市场基本是 Claude 和 ChatGPT 的双雄争霸。但两者定位和优势差异很大——用对工具效率翻倍。</p>
<h2>核心能力对比</h2>
<table><tr><th>维度</th><th>ChatGPT</th><th>Claude</th></tr>
<tr><td>编程</td><td>强（尤其代码补全）</td><td>很强（长上下文理解代码库）</td></tr>
<tr><td>写作</td><td>中上</td><td>最强（中文写作尤其突出）</td></tr>
<tr><td>长文档分析</td><td>中等（128K 上下文）</td><td>最强（200K 上下文，引用准确）</td></tr>
<tr><td>数据分析</td><td>强（Code Interpreter）</td><td>中上（Artifacts 渲染）</td></tr>
<tr><td>图片生成</td><td>✅ DALL·E 3</td><td>❌ 不支持</td></tr>
<tr><td>联网搜索</td><td>✅ 内置</td><td>❌ 不直接支持</td></tr>
<tr><td>多模态</td><td>图像理解 + 生成</td><td>图像理解（不生成）</td></tr>
<tr><td>价格</td><td>免费/Plus $20/Pro $200</td><td>免费/Pro $20/Team $25</td></tr></table>
<h2>各场景最佳选择</h2>
<ul><li><strong>写代码</strong> — 两者都强，但 Claude 在理解大项目上下文和代码审查上更优；ChatGPT 在有 Code Interpreter 的数据分析场景更强。</li><li><strong>写文章/文案</strong> — Claude 明显更好，中文自然度和语气把控能力高出一个档次。需要图片配合时 ChatGPT 更好。</li><li><strong>读论文/长文档</strong> — Claude 的长上下文优势和引用精准度让它更适合深度阅读和总结。</li><li><strong>做 PPT / 需要图片</strong> — ChatGPT，Claude 不会画图。</li><li><strong>日常问答</strong> — 两者差不远，Claude 的回答通常更有深度但速度略慢。</li></ul>
<h2>我的推荐方案</h2>
<p><strong>双持是最优解</strong>——免费版 Claude + 免费版 ChatGPT 组合，零成本覆盖几乎所有场景。如果只买一个 Pro：写作和研究为主选 Claude Pro，需要图片和联网搜索选 ChatGPT Plus。</p>
<h2>不必纠结</h2><p>模型能力在快速收敛，差距越来越小。选择一个深入使用比反复切换更有价值。你花在比较工具上的时间已经够写一篇好文章了。</p>'''),
]


def make_html(art):
    board_names = {
        'tech': '技术教程', 'sidehustle': '副业资源',
        'tools': '工具推荐', 'ai': 'AI 教程',
    }
    bn = board_names[art['board']]
    tags_h = '\n'.join(f'        <span class="tag-cat">{t}</span>' for t in art['tags'])
    pin_h = '<span class="tag-pin">📌 置顶</span>\n' if art.get('pinned') else ''
    if art.get('hot'):
        tags_h += '\n        <span class="tag-cat" style="background:#fff3cd;color:#856404;">🔥 热门</span>'

    return f'''<!DOCTYPE html>
<html lang="zh-CN" data-render="related" data-board="{art['board']}" data-exclude="{art['slug']}">
<head>
    <meta charset="UTF-8">
    <meta name="google-site-verification" content="XzThATs15kR08VOM-tCxIztKjEGW8ft-T75SmH_Wz38" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{art['title']} — 资料库</title>
    <meta name="description" content="{art['description']}">
    <link rel="stylesheet" href="/css/style.css">
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "{art['title']}",
      "description": "{art['description']}",
      "datePublished": "{art['date']}",
      "dateModified": "{art['date']}",
      "author": {{"@type": "Person", "name": "资料库"}}
    }}
    </script>
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{"@type": "ListItem", "position": 1, "name": "首页", "item": "https://dingjiu1989-hue.github.io/"}},
        {{"@type": "ListItem", "position": 2, "name": "{bn}", "item": "https://dingjiu1989-hue.github.io/{art['board']}/"}},
        {{"@type": "ListItem", "position": 3, "name": "{art['title']}"}}
      ]
    }}
    </script>
</head>
<body>
<div id="nav-placeholder"></div>
<main>
  <div class="container article-container">
    <div class="breadcrumb">
      <a href="/">首页</a> › <a href="/{art['board']}/">{bn}</a> › {art['title']}
    </div>
    <article>
      <div class="article-tags">{pin_h}{tags_h}</div>
      <h1 class="article-title">{art['title']}</h1>
      <div class="article-meta">发布于 {art['date']} · 阅读 {art['replies'] * 120} · {art['replies']} 回复</div>
      <div class="article-body">{art['body'].strip()}</div>
    </article>
    <section class="related"><div id="related-posts"></div></section>
  </div>
</main>
<div id="footer-placeholder"></div>
<script src="/js/include.js"></script>
<script src="/js/render.js"></script>
</body>
</html>'''


def main():
    data = json.loads(ARTICLES_JSON.read_text(encoding='utf-8'))
    boards = {b['id']: b for b in data['boards']}
    sitemap = SITEMAP.read_text(encoding='utf-8')
    created = added = 0

    for art in NEW:
        p = ROOT / art['board'] / f"{art['slug']}.html"
        if not p.exists():
            p.write_text(make_html(art), encoding='utf-8')
            created += 1
            print(f'  HTML: {p}')

        board = boards[art['board']]
        if art['slug'] not in {x['slug'] for x in board['posts']}:
            entry = {'slug': art['slug'], 'title': art['title'],
                     'description': art['description'], 'date': art['date'],
                     'tags': art['tags'], 'pinned': art.get('pinned', False),
                     'replies': art['replies']}
            if art.get('hot'): entry['hot'] = True
            board['posts'].insert(0, entry)
            added += 1

        loc = f'{BASE}/{art["board"]}/{art["slug"]}.html'
        if loc not in sitemap:
            sitemap = sitemap.replace('</urlset>',
                f'  <url>\n    <loc>{loc}</loc>\n    <changefreq>weekly</changefreq>\n    <priority>0.7</priority>\n    <lastmod>{art["date"]}</lastmod>\n  </url>\n</urlset>')

    ARTICLES_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    SITEMAP.write_text(sitemap, encoding='utf-8')

    for board_id, count in [(b['id'], len(b['posts'])) for b in data['boards']]:
        idx = ROOT / board_id / 'index.html'
        if idx.exists():
            c = idx.read_text(encoding='utf-8')
            c = re.sub(r'（共 \d+ 篇）', f'（共 {count} 篇）', c)
            idx.write_text(c, encoding='utf-8')

    print(f'\nDone: {created} HTML, {added} JSON. Totals: ' +
          ', '.join(f'{b["id"]}={len(b["posts"])}' for b in data['boards']))


if __name__ == '__main__':
    main()
