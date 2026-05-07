#!/usr/bin/env python3
"""Batch 2: 10 new high-search-volume articles."""
import json, re, sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parent.parent
ARTICLES_JSON = ROOT / 'articles.json'
SITEMAP = ROOT / 'sitemap.xml'
TODAY = date.today().isoformat()
BASE = 'https://dingjiu1989-hue.github.io'

NEW = [
    # ═══ TECH (3) ═══════════════════════════════════════════════
    dict(board='tech', slug='python-tutorial', pinned=True,
         title='Python 入门教程：从零到写出第一个程序',
         description='零基础 Python 编程入门，30 分钟掌握变量、条件、循环、函数等核心语法，手写第一个可运行程序。',
         tags=['Python', '编程入门', '教程'], replies=31,
         body='''<p>Python 是最适合初学者的编程语言——语法接近自然语言，生态强大到几乎无所不能。这篇教程带你 30 分钟入门。</p>
<h2>安装 Python</h2>
<p>macOS 自带 Python 3，终端输入 <code>python3 --version</code> 检查。Windows 去 python.org 下载安装包，安装时勾选 "Add Python to PATH"。</p>
<h2>第一个程序</h2>
<pre><code>print("Hello, World!")</code></pre>
<p>保存为 <code>hello.py</code>，终端运行 <code>python3 hello.py</code>，看到输出就成功了。</p>
<h2>变量和数据类型</h2>
<pre><code>name = "小明"        # 字符串
age = 25             # 整数
height = 1.75        # 浮点数
is_student = True    # 布尔值

print(f"{name}今年{age}岁")</code></pre>
<h2>条件判断</h2>
<pre><code>score = 85
if score >= 90:
    print("优秀")
elif score >= 60:
    print("及格")
else:
    print("不及格")</code></pre>
<h2>循环</h2>
<pre><code># for 循环
for i in range(5):
    print(f"第{i+1}次")

# while 循环
count = 0
while count < 3:
    print(f"count = {count}")
    count += 1</code></pre>
<h2>列表和字典</h2>
<pre><code># 列表 — 有序集合
fruits = ["苹果", "香蕉", "橘子"]
fruits.append("葡萄")
print(fruits[0])  # 苹果

# 字典 — 键值对
user = {"name": "小明", "age": 25, "city": "北京"}
print(user["name"])  # 小明</code></pre>
<h2>函数</h2>
<pre><code>def greet(name):
    return f"你好，{name}！"

print(greet("小明"))  # 你好，小明！</code></pre>
<h2>下一步学什么</h2>
<ol><li><strong>pip 包管理</strong> — 安装第三方库</li><li><strong>文件读写</strong> — 处理文本和 CSV</li><li><strong>requests 库</strong> — 爬取网页和调用 API</li><li><strong>Flask</strong> — 写一个简单的 Web 应用</li></ol>'''),

    dict(board='tech', slug='linux-commands', pinned=False,
         title='Linux 命令行入门：30 个最常用的命令',
         description='Linux 新手必学的 30 个命令，从文件操作、权限管理到进程查看，每个带示例，收藏这一篇就够了。',
         tags=['Linux', '命令行', '教程'], replies=24, hot=True,
         body='''<p>不管你做不做运维，Linux 命令行都是程序员的必修课。这 30 个命令覆盖 80% 日常场景。</p>
<h2>文件操作（10 个）</h2>
<table><tr><th>命令</th><th>用途</th><th>示例</th></tr>
<tr><td>ls</td><td>列出目录</td><td><code>ls -la</code></td></tr>
<tr><td>cd</td><td>切换目录</td><td><code>cd /var/log</code></td></tr>
<tr><td>pwd</td><td>显示当前路径</td><td><code>pwd</code></td></tr>
<tr><td>mkdir</td><td>创建目录</td><td><code>mkdir -p a/b/c</code></td></tr>
<tr><td>cp</td><td>复制文件</td><td><code>cp -r src dst</code></td></tr>
<tr><td>mv</td><td>移动/重命名</td><td><code>mv old.txt new.txt</code></td></tr>
<tr><td>rm</td><td>删除</td><td><code>rm -rf dir/</code></td></tr>
<tr><td>cat</td><td>查看文件内容</td><td><code>cat file.txt</code></td></tr>
<tr><td>head/tail</td><td>查看头/尾行</td><td><code>tail -f log.txt</code></td></tr>
<tr><td>find</td><td>搜索文件</td><td><code>find . -name "*.py"</code></td></tr></table>
<h2>文本处理（6 个）</h2>
<table><tr><th>命令</th><th>用途</th><th>示例</th></tr>
<tr><td>grep</td><td>文本搜索</td><td><code>grep "error" log.txt</code></td></tr>
<tr><td>wc</td><td>统计行/字数</td><td><code>wc -l file.txt</code></td></tr>
<tr><td>sort</td><td>排序</td><td><code>sort -n data.txt</code></td></tr>
<tr><td>uniq</td><td>去重</td><td><code>sort file.txt | uniq -c</code></td></tr>
<tr><td>sed</td><td>流编辑器</td><td><code>sed \'s/old/new/g\' file.txt</code></td></tr>
<tr><td>awk</td><td>列处理</td><td><code>awk \'{print $1}\' data.txt</code></td></tr></table>
<h2>权限管理（3 个）</h2>
<table><tr><th>命令</th><th>用途</th><th>示例</th></tr>
<tr><td>chmod</td><td>修改权限</td><td><code>chmod +x script.sh</code></td></tr>
<tr><td>chown</td><td>修改所有者</td><td><code>chown user:group file</code></td></tr>
<tr><td>sudo</td><td>超级用户权限</td><td><code>sudo systemctl restart nginx</code></td></tr></table>
<h2>系统信息（5 个）</h2>
<table><tr><th>命令</th><th>用途</th></tr>
<tr><td>ps aux</td><td>查看进程</td></tr>
<tr><td>top/htop</td><td>实时资源监控</td></tr>
<tr><td>df -h</td><td>磁盘空间</td></tr>
<tr><td>free -h</td><td>内存使用</td></tr>
<tr><td>uname -a</td><td>系统信息</td></tr></table>
<h2>网络（3 个）</h2>
<table><tr><th>命令</th><th>用途</th></tr>
<tr><td>curl</td><td>发送 HTTP 请求</td></tr>
<tr><td>ping</td><td>测试连通性</td></tr>
<tr><td>netstat</td><td>网络连接状态</td></tr></table>
<h2>管道和重定向（3 个）</h2>
<table><tr><th>符号</th><th>用途</th><th>示例</th></tr>
<tr><td>|</td><td>管道</td><td><code>cat log.txt | grep error | wc -l</code></td></tr>
<tr><td>></td><td>输出重定向</td><td><code>echo "hello" > file.txt</code></td></tr>
<tr><td>>></td><td>追加输出</td><td><code>echo "world" >> file.txt</code></td></tr></table>
<h2>推荐学习路径</h2>
<p>先掌握文件操作 → 文本处理 → 管道重定向（这是 Linux 的精髓）→ 权限管理 → Shell 脚本编写。</p>'''),

    dict(board='tech', slug='regex-guide', pinned=False,
         title='正则表达式 30 分钟入门指南',
         description='从完全不懂到能写出实用的正则表达式，涵盖元字符、量词、分组、断言和 Python/JS 实战示例。',
         tags=['正则表达式', '编程', '教程'], replies=18,
         body='''<p>正则表达式是文本处理的瑞士军刀——验证表单、提取数据、搜索替换，没有比它更强的工具。学会它，一辈子受益。</p>
<h2>基础元字符</h2>
<table><tr><th>符号</th><th>含义</th><th>示例匹配</th></tr>
<tr><td>.</td><td>任意单个字符</td><td>a.c → abc, a1c</td></tr>
<tr><td>\\d</td><td>数字</td><td>\\d\\d\\d → 123, 456</td></tr>
<tr><td>\\w</td><td>字母数字下划线</td><td>\\w+ → hello_world</td></tr>
<tr><td>\\s</td><td>空白字符</td><td>a\\sb → "a b"</td></tr>
<tr><td>[abc]</td><td>字符组，匹配 a/b/c</td><td>[aeiou] → 元音字母</td></tr>
<tr><td>[^abc]</td><td>取反，不匹配 a/b/c</td><td>[^0-9] → 非数字</td></tr></table>
<h2>量词</h2>
<table><tr><th>符号</th><th>含义</th></tr>
<tr><td>*</td><td>0 次或多次</td></tr>
<tr><td>+</td><td>1 次或多次</td></tr>
<tr><td>?</td><td>0 次或 1 次</td></tr>
<tr><td>{n}</td><td>恰好 n 次</td></tr>
<tr><td>{n,m}</td><td>n 到 m 次</td></tr></table>
<h2>实战 5 例</h2>
<pre><code># 1. 验证手机号（中国大陆）
^1[3-9]\\d{9}$

# 2. 提取邮箱地址
[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}

# 3. 匹配 URL
https?://[\\w.-]+(:\\d+)?(/[\\w./-]*)?

# 4. 提取 HTML 标签内容
>([^<]+)<

# 5. 验证日期格式 YYYY-MM-DD
^\\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\\d|3[01])$</code></pre>
<h2>分组和捕获</h2>
<pre><code># 匹配 "2026-05-07"，分别捕获年月日
(\\d{4})-(\\d{2})-(\\d{2})

# Python 中可以用 group(1) group(2) group(3) 获取
# 等价于 \\1 \\2 \\3 在替换中引用</code></pre>
<h2>零宽断言（进阶）</h2>
<table><tr><th>符号</th><th>含义</th><th>示例</th></tr>
<tr><td>(?=...)</td><td>正向前瞻</td><td>\\d+(?=元) 匹配"50元"中的50</td></tr>
<tr><td>(?<=...)</td><td>正向后顾</td><td>(?<=¥)\\d+ 匹配"¥50"中的50</td></tr>
<tr><td>(?!...)</td><td>负向前瞻</td><td>\\d+(?!元) 匹配后不跟"元"的数字</td></tr></table>
<h2>练习是关键</h2>
<p>推荐在 <strong>regex101.com</strong> 上实操练习，它有交互式解释器、多语言支持和测试用例功能。每天练 2 个正则，一周后你就能随手写出匹配规则了。</p>'''),

    # ═══ SIDEHUSTLE (3) ══════════════════════════════════════════
    dict(board='sidehustle', slug='indie-dev-guide', pinned=False,
         title='独立开发者出海指南：从产品 Idea 到稳定变现',
         description='面向程序员的独立开发者完整指南：产品创意验证、技术选型、海外支付接入、推广引流和变现策略。',
         tags=['独立开发者', '出海', '变现'], replies=26, hot=True,
         body='''<p>一个人写代码 + AI 辅助 + 全球化分发 = 独立开发者的黄金时代。这篇文章讲清楚从 0 到 1 的全流程。</p>
<h2>为什么选择出海</h2>
<ul><li><strong>付费意愿高</strong> — 美国和欧洲用户习惯了为软件付费，SaaS 订阅模式成熟</li><li><strong>汇率红利</strong> — 收美金/欧元，生活在中国/东南亚，成本优势巨大</li><li><strong>平台完善</strong> — Stripe 支付、Vercel 部署、Supabase 后端，技术栈零门槛</li></ul>
<h2>产品 Idea 怎么找</h2>
<ol><li><strong>从自己的痛点出发</strong> — 你最近缺少什么工具？哪怕很小的工具也可能有市场</li><li><strong>看 Product Hunt 评论</strong> — 找差评，看用户在抱怨什么，那就是机会</li><li><strong>看 Indie Hackers</strong> — 看其他独立开发者在做什么、赚多少、怎么做的</li><li><strong>做小不做大</strong> — 不要做"下一个 Notion"，做一个 Notion 没有的小功能</li></ol>
<h2>技术选型建议</h2>
<table><tr><th>组件</th><th>推荐</th><th>免费额度</th></tr>
<tr><td>前端</td><td>Next.js / Astro</td><td>Vercel 免费</td></tr>
<tr><td>后端</td><td>Supabase</td><td>50K 月活免费</td></tr>
<tr><td>数据库</td><td>Supabase (PostgreSQL)</td><td>500MB 免费</td></tr>
<tr><td>支付</td><td>Stripe / Lemonsqueezy</td><td>按交易抽成</td></tr>
<tr><td>认证</td><td>Clerk / Supabase Auth</td><td>5K 用户免费</td></tr>
<tr><td>域名</td><td>Namecheap / Cloudflare</td><td>$10/年</td></tr>
<tr><td>邮件</td><td>Resend</td><td>100 封/天免费</td></tr></table>
<h2>推广路径</h2>
<ol><li><strong>Product Hunt 发布</strong> — 独立开发者最重要的曝光渠道，认真准备素材</li><li><strong>Twitter/X 建号发帖</strong> — 分享开发过程和收入，透明吸引关注</li><li><strong>Reddit / Hacker News</strong> — 在相关子版块分享你的产品故事</li><li><strong>写博客做 SEO</strong> — 围绕你的产品写教程和使用案例，长期引流</li></ol>
<h2>定价和变现</h2><ul><li><strong>免费 + Pro 双档位</strong> — 门槛最低，先用免费版积累用户</li><li><strong>订阅制（月费/年费）</strong> — 稳定现金流，7-15$/月是 sweet spot</li><li><strong>终身版（Lifetime Deal）</strong> — 产品初期快速回笼资金，但长期看可能亏</li></ul>
<h2>关键心态</h2><p>90% 的独立产品不赚钱，但不代表你不该试。<strong>失败的产品也是经验</strong>。用最小成本验证 Idea，不行就快速换方向。</p>'''),

    dict(board='sidehustle', slug='tech-blog-monetization', pinned=False,
         title='如何通过写技术博客赚钱：从 0 到月入 1000 美元',
         description='技术博客的完整变现路径：广告、联盟营销、付费内容、咨询转化，附带真实案例和收入拆解。',
         tags=['技术博客', '博客变现', '副业'], replies=22,
         body='''<p>写技术博客是程序员最自然的副业——你本来就在学习和解决问题，记录下来分享出去就能产生收入。这篇文章拆解整个变现路径。</p>
<h2>先搞清楚：博客怎么赚钱</h2>
<table><tr><th>变现方式</th><th>收入潜力</th><th>门槛</th><th>适合阶段</th></tr>
<tr><td>展示广告 (AdSense)</td><td>低（$2-10/千次PV）</td><td>需要流量</td><td>月 PV > 1 万</td></tr>
<tr><td>联盟营销</td><td>中（佣金 $10-200/单）</td><td>需要信任</td><td>月 PV > 5000</td></tr>
<tr><td>付费内容/课程</td><td>高（$50-500/单）</td><td>需要专业度</td><td>有忠实读者</td></tr>
<tr><td>咨询/接单</td><td>最高（$100-300/时）</td><td>需要口碑</td><td>有案例展示</td></tr>
<tr><td>赞助内容</td><td>中（$500-5000/篇）</td><td>需要影响力</td><td>月 PV > 5 万</td></tr></table>
<h2>起步三步走</h2>
<ol><li><strong>选一个细分方向</strong> — 不要写泛技术，选一个你擅长的细分领域（比如"Python 数据分析"而不是"编程"）</li><li><strong>坚持周更 3 个月</strong> — 前 12 篇是为搜索引擎写的，不是流量，是积累</li><li><strong>每篇解决一个具体问题</strong> — "Python Pandas 如何合并两个 CSV 文件"比"Python 数据分析入门"更容易获取搜索流量</li></ol>
<h2>联盟营销实战</h2><ul><li><strong>DigitalOcean / Vultr</strong> — 推荐链接用户注册消费后你拿 $25-100</li><li><strong>各类 SaaS 工具</strong> — Notion、Airtable、Figma 等都有联盟计划</li><li><strong>Amazon Associates</strong> — 推荐技术书籍和设备</li><li><strong>Coursera / Udemy</strong> — 推荐在线课程</li></ul>
<h2>真实收入拆解（博客月 PV 3 万）</h2>
<p>AdSense 广告：$150-300/月<br>联盟营销：$200-500/月<br>付费电子书：$100-300/月<br><strong>合计约 $500-1000/月</strong></p>
<h2>核心建议</h2><p>前 6 个月不要想赚钱，专注写出对读者有用的内容。博客是慢生意，但从第 7 个月开始，之前的积累会开始产生复利效应。</p>'''),

    dict(board='sidehustle', slug='cross-border-ecommerce', pinned=False,
         title='跨境电商入门指南：从 0 到第一单的全流程',
         description='新手友好的跨境电商入门教程，Shopee/Lazada/Tokopedia 三大平台对比，选品、运营、物流全链路讲解。',
         tags=['跨境电商', '电商', 'Shopee'], replies=20,
         body='''<p>跨境电商是门槛相对较低的收入来源之一——国内供应链优势 + 东南亚市场增长红利 = 机会窗口还在。这篇指南帮你快速上手。</p>
<h2>为什么选东南亚市场</h2>
<ul><li><strong>增长快</strong> — 东南亚电商年增长率 15-20%，远高于成熟市场</li><li><strong>竞争低</strong> — 比欧美市场内卷程度低，新卖家还有机会</li><li><strong>距离近</strong> — 物流时效和成本可控，深圳到新加坡 3-5 天</li><li><strong>华裔多</strong> — 沟通和选品理解门槛低</li></ul>
<h2>三大平台对比</h2>
<table><tr><th>平台</th><th>主市场</th><th>费用</th><th>特点</th></tr>
<tr><td>Shopee</td><td>印尼/马来/泰国/菲律宾/越南/新加坡</td><td>佣金 3-5%</td><td>移动端第一，玩法简单</td></tr>
<tr><td>Lazada</td><td>印尼/马来/泰国/菲律宾/越南/新加坡</td><td>佣金 4-6%</td><td>阿里系，品牌化运营</td></tr>
<tr><td>Tokopedia</td><td>印尼（人口 2.7 亿）</td><td>佣金 2-4%</td><td>印尼最大电商平台</td></tr></table>
<h2>新手选品策略</h2>
<ol><li><strong>轻小件优先</strong> — 重量 < 500g，体积小，运费低</li><li><strong>高毛利（> 50%）</strong> — 售价是成本 3 倍以上才有利可图</li><li><strong>非标品</strong> — 避开手机壳之类的标品红海，做有差异化的小众品类</li><li><strong>看平台热卖榜</strong> — 各平台都有 Bestseller 榜单，研究热卖品的特点</li></ol>
<h2>物流方案</h2>
<ul><li><strong>Shopee/Lazada 官方物流</strong> — 新手首选，把货发到国内转运仓就行，平台负责跨境配送</li><li><strong>第三方海外仓</strong> — 适合稳定出单后，时效更快但需要备货</li></ul>
<h2>启动成本估算</h2>
<p>首月总投入约 ¥5000-10000：平台保证金 ¥0-3000 + 首批货 ¥2000-5000 + 工具/软件 ¥500-1000。Shopee 新手卖家基本零门槛。</p>
<h2>避坑提醒</h2>
<ul><li>先了解目标国的禁售品清单（印尼对化妆品、食品限制多）</li><li>注意回款周期（通常 15-45 天），现金流要能周转</li><li>别一上来就砸钱投广告，先拿自然流量验证产品</li></ul>'''),

    # ═══ TOOLS (2) ═══════════════════════════════════════════════
    dict(board='tools', slug='notion-complete-guide', pinned=True,
         title='Notion 完全使用指南：从入门到精通',
         description='最完整的 Notion 中文教程，覆盖数据库、公式、模板、自动化等核心功能，附 10 个可以直接用的模板。',
         tags=['Notion', '效率工具', '教程'], replies=42, hot=True,
         body='''<p>Notion 是现在最流行的全能型笔记和协作工具。但它功能太深，很多人用了半年还在当备忘录用。这篇文章带你挖掘它真正的威力。</p>
<h2>Notion 到底能做什么</h2>
<ul><li>个人知识库 — 读书笔记、学习计划、日记</li><li>项目管理 — 任务看板、甘特图、Sprint 计划</li><li>团队 Wiki — 流程文档、新人入职手册</li><li>数据库应用 — CRM、内容日历、预算跟踪</li></ul>
<h2>核心概念：Block 和 Database</h2>
<p><strong>Block（块）</strong> 是 Notion 的最小单位——每个段落、标题、图片、列表都是 Block。输入 <code>/</code> 就能插入任何类型的 Block。</p>
<p><strong>Database（数据库）</strong> 是 Notion 的灵魂——不只是表格，而是可以关联、筛选、多视图展示的关系型数据。</p>
<h2>数据库六大视图</h2>
<table><tr><th>视图</th><th>适合场景</th></tr>
<tr><td>Table（表格）</td><td>数据密集，需要看到所有字段</td></tr>
<tr><td>Board（看板）</td><td>按状态分列的看板，项目管理</td></tr>
<tr><td>Calendar（日历）</td><td>按日期展示，适合内容日历</td></tr>
<tr><td>Gallery（画廊）</td><td>图文卡片，适合设计灵感墙</td></tr>
<tr><td>List（列表）</td><td>极简视图，适合快速浏览</td></tr>
<tr><td>Timeline（时间线）</td><td>甘特图，适合项目排期</td></tr></table>
<h2>Formula 公式入门</h2>
<pre><code># 计算两个日期之间的天数
dateBetween(prop("截止日期"), prop("开始日期"), "days")

# 根据进度显示状态
if(prop("进度") == 100, "✅ 完成",
  prop("进度") >= 50, "🟡 进行中", "🔴 未开始")</code></pre>
<h2>10 个必备模板</h2>
<ol><li>读书清单（Gallery 视图 + 评分 + 笔记）</li><li>项目看板（Board 视图 + 任务关联）</li><li>周报/日报模板</li><li>目标追踪（OKR 模板）</li><li>内容日历（Calendar + 状态管理）</li><li>预算追踪（Table + 公式计算）</li><li>会议笔记（模板按钮一键创建）</li><li>个人 CRM（人脉管理）</li><li>旅行规划（Gallery + Checklist）</li><li>学习路线图（Timeline 视图）</li></ol>
<h2>进阶技巧</h2>
<ul><li><strong>关联数据库（Relation）</strong> — 比如"项目"关联"任务"，一个项目下能看到所有关联任务</li><li><strong>汇总（Rollup）</strong> — 聚合关联数据，如显示项目的总任务数和完成率</li><li><strong>同步区块（Synced Block）</strong> — 同一内容在多个页面同步更新</li></ul>'''),

    dict(board='tools', slug='cli-tools-collection', pinned=False,
         title='10 款开发者必备的命令行工具（2026 版）',
         description='精选 10 款提升终端效率的命令行工具，涵盖文件管理、JSON 处理、Git 增强、系统监控等场景。',
         tags=['命令行', '开发工具', '效率'], replies=35, hot=True,
         body='''<p>终端是开发者的主战场。这些 CLI 工具能让你的命令行效率提升 10 倍。</p>
<h2>文件与导航</h2>
<ul><li><strong>fd</strong> — 比 <code>find</code> 快 5 倍的搜索工具，语法直观。例：<code>fd "test.*py" src/</code></li><li><strong>ripgrep (rg)</strong> — 比 <code>grep</code> 快 10 倍的文本搜索。例：<code>rg "TODO" --type py</code></li><li><strong>fzf</strong> — 模糊搜索交互工具。Ctrl+T 模糊搜文件，Ctrl+R 模糊搜历史命令，安装即生效。</li><li><strong>zoxide</strong> — 智能 <code>cd</code> 替代。不记全路径，只记文件夹名，自动跳转到你最常去的目录。例：<code>z proj</code></li></ul>
<h2>文件内容查看</h2>
<ul><li><strong>bat</strong> — <code>cat</code> 替代品，语法高亮、行号、分页。例：<code>bat main.py</code></li><li><strong>jq</strong> — JSON 处理的瑞士军刀。提取、筛选、转换 JSON 数据：<code>curl api.com | jq \'.items[] | {name, price}\'</code></li><li><strong>fx</strong> — 交互式 JSON 查看器，支持鼠标点击折叠/展开，比 <code>jq</code> 更直观。</li></ul>
<h2>Git 增强</h2>
<ul><li><strong>lazygit</strong> — Git 的终端 GUI。在终端内用键盘快捷键完成 commit、push、merge、rebase 等所有操作，不用记命令。</li><li><strong>delta</strong> — 增强 <code>git diff</code> 显示效果，语法高亮、行号、侧边对比。</li></ul>
<h2>系统监控</h2>
<ul><li><strong>btm (bottom)</strong> — Rust 写的系统资源监控，比 <code>top</code> 和 <code>htop</code> 更现代的 UI，CPU/内存/磁盘/网络/温度一屏显示。</li></ul>
<h2>一行安装（macOS）</h2>
<pre><code>brew install fd ripgrep fzf zoxide bat jq lazygit git-delta bottom</code></pre>
<h2>组合使用的威力</h2>
<pre><code># 在所有 Python 文件中搜索 "user"，模糊筛选后用 bat 查看
rg -l "user" --type py | fzf --preview "bat --color=always {}"</code></pre>
<p>把这些工具加到你的工作流里，两周后你会奇怪之前没有它们是怎么活下来的。</p>'''),

    # ═══ AI (2) ══════════════════════════════════════════════════
    dict(board='ai', slug='ai-automation-workflow', pinned=False,
         title='AI 自动化工作流实战：让 AI 替你干重复活',
         description='手把手搭建 AI 自动化工作流：Zapier/Make + ChatGPT/Claude API 联动，自动处理邮件、生成报表、监控舆情。',
         tags=['AI自动化', 'Zapier', '效率提升'], replies=28, hot=True,
         body='''<p>AI 不只是聊天——它还可以在后台自动帮你处理重复性工作。这篇文章教你搭建第一个 AI 自动化工作流。</p>
<h2>什么是 AI 自动化</h2>
<p>简单公式：<strong>触发器（Trigger）+ AI 处理 + 动作（Action）= 自动化工作流</strong>。</p>
<p>举例：收到新邮件 → AI 判断重要程度并生成摘要 → 高优先级的自动发送通知到 Slack。</p>
<h2>工具选型</h2>
<table><tr><th>工具</th><th>定位</th><th>免费额度</th><th>适合</th></tr>
<tr><td>Zapier</td><td>最全的自动化平台</td><td>100 次/月</td><td>非技术用户，应用多</td></tr>
<tr><td>Make (Integromat)</td><td>可视化更强</td><td>1000 次/月</td><td>复杂逻辑，条件分支</td></tr>
<tr><td>n8n</td><td>开源自部署</td><td>无限（自托管）</td><td>开发者，需要定制</td></tr>
</table>
<h2>实战案例 1：AI 邮件分类和摘要</h2>
<pre><code>触发器：Gmail 收到新邮件
↓
AI 步骤 (OpenAI API)：分析邮件内容
  提示词："判断邮件紧急度（高/中/低），用一句话总结内容"
↓
条件分支：
  - 高优先级 → Slack 通知 + 添加到 Todoist
  - 中优先级 → 添加到 Notion "待处理" 数据库
  - 低优先级 → 存档，每周汇总一次</code></pre>
<h2>实战案例 2：AI 日报自动生成</h2>
<pre><code>触发器：每天 18:00
↓
数据收集：
  - 从 Todoist 获取今日完成任务
  - 从 RescueTime 获取工作时长
  - 从 GitHub 获取今日 commits
↓
AI 步骤 (Claude API)：根据数据生成日报
↓
动作：保存到 Notion + 发送到企业微信/飞书</code></pre>
<h2>实战案例 3：AI 客服预处理</h2>
<pre><code>触发器：网站表单提交
↓
AI 步骤：根据知识库判断能否直接回答
  - 能 → AI 直接回复邮件
  - 不能 → 转发给人工客服，附带 AI 整理的上下文</code></pre>
<h2>新手建议</h2>
<ol><li>从最简单的自动化开始（2 步）</li><li>AI 步骤的提示词要反复调试，结果要验证</li><li>所有 AI 自动化留人工检查点，100% 自动化有风险</li></ol>'''),

    dict(board='ai', slug='chatgpt-plus-worth', pinned=False,
         title='ChatGPT Plus 值得买吗？免费版 vs Plus vs Pro 深度对比',
         description='2026 年 ChatGPT 三档价格方案深度对比：免费版、Plus($20/月)、Pro($200/月) 各自适合什么人？帮你做出不后悔的选择。',
         tags=['ChatGPT', '评测对比', 'AI工具'], replies=45, hot=True,
         body='''<p>$20/月看起来不多，一年就是 $240。这笔钱到底值不值？这篇文章从实际使用场景出发，帮你做决策。</p>
<h2>三档方案对比</h2>
<table><tr><th>维度</th><th>免费版</th><th>Plus ($20/月)</th><th>Pro ($200/月)</th></tr>
<tr><td>模型</td><td>GPT-4o mini</td><td>GPT-4o + o3-mini</td><td>GPT-4o + o3 + o3-pro</td></tr>
<tr><td>消息限制</td><td>有限</td><td>GPT-4o 80条/3h</td><td>近乎无限</td></tr>
<tr><td>联网搜索</td><td>有限</td><td>✅</td><td>✅</td></tr>
<tr><td>文件上传</td><td>有限</td><td>✅ 图片/PDF/文档</td><td>✅ 所有格式 + API</td></tr>
<tr><td>图片生成</td><td>有限（DALL·E）</td><td>✅ DALL·E 3</td><td>✅ DALL·E 3 + Sora</td></tr>
<tr><td>语音对话</td><td>有限</td><td>✅ 高级语音模式</td><td>✅ 无限制</td></tr>
<tr><td>深度研究</td><td>❌</td><td>10次/月</td><td>120次/月</td></tr>
<tr><td>Operator (AI Agent)</td><td>❌</td><td>有限</td><td>✅ 完整</td></tr>
</table>
<h2>什么人该买 Plus</h2>
<ul><li><strong>内容创作者</strong> — 每天和 AI 协作写文章、改文案、生成图片</li><li><strong>程序员</strong> — 用 GPT-4o 调试代码、解释复杂逻辑、写文档</li><li><strong>学生和研究者</strong> — Deep Research 做文献综述效率提升极大</li><li><strong>产品经理 / 创业者</strong> — 用 AI 做竞品分析、用户调研、数据分析</li></ul>
<h2>什么人不该买</h2>
<ul><li><strong>偶尔用用</strong> — 如果一周只用 2-3 次，免费版或按量付费的 API 更划算</li><li><strong>只用基础问答</strong> — GPT-4o mini 对简单问题够用了</li><li><strong>已经用 Claude 的</strong> — Claude 免费版在写作和编程方面的表现也可圈可点</li></ul>
<h2>省钱技巧</h2>
<ol><li><strong>API 按量付费更便宜</strong> — 如果不常用，用 OpenAI API 按量计费比 $20/月省多了</li><li><strong>学生可申请折扣</strong> — 部分学校有教育优惠</li><li><strong>用 Claude + ChatGPT 免费版组合</strong> — 两者互补，不花一分钱</li></ol>
<h2>我的建议</h2>
<p>如果你每天用 AI 超过 30 分钟，Plus 的 $20 是物有所值的——GPT-4o 比 GPT-4o mini 在复杂任务上强一个档次，文件上传和联网搜索也很实用。但如果只是偶尔问几个问题，免费版足够。</p>'''),
]


def make_html(art):
    board_names = {
        'tech': ('技术教程', '💻'), 'sidehustle': ('副业资源', '💰'),
        'tools': ('工具推荐', '🛠️'), 'ai': ('AI 教程', '🤖'),
    }
    bn, bi = board_names[art['board']]
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
        art.setdefault('date', TODAY)
        # HTML file
        p = ROOT / art['board'] / f"{art['slug']}.html"
        if not p.exists():
            p.write_text(make_html(art), encoding='utf-8')
            created += 1
            print(f'  HTML: {p}')

        # JSON
        board = boards[art['board']]
        if art['slug'] not in {x['slug'] for x in board['posts']}:
            entry = {'slug': art['slug'], 'title': art['title'],
                     'description': art['description'], 'date': art['date'],
                     'tags': art['tags'], 'pinned': art.get('pinned', False),
                     'replies': art['replies']}
            if art.get('hot'): entry['hot'] = True
            board['posts'].insert(0, entry)
            added += 1

        # Sitemap (idempotent: only add if not present)
        loc = f'{BASE}/{art["board"]}/{art["slug"]}.html'
        if loc not in sitemap:
            sitemap = sitemap.replace('</urlset>',
                f'  <url>\n    <loc>{loc}</loc>\n    <changefreq>weekly</changefreq>\n    <priority>0.7</priority>\n    <lastmod>{art["date"]}</lastmod>\n  </url>\n</urlset>')

    ARTICLES_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    SITEMAP.write_text(sitemap, encoding='utf-8')

    # Update category page counts
    for board_id, count in [(b['id'], len(b['posts'])) for b in data['boards']]:
        idx = ROOT / board_id / 'index.html'
        if idx.exists():
            c = idx.read_text(encoding='utf-8')
            c = re.sub(r'（共 \d+ 篇）', f'（共 {count} 篇）', c)
            idx.write_text(c, encoding='utf-8')

    print(f'\nDone: {created} HTML files, {added} JSON entries')
    print(f'Totals: ' + ', '.join(f'{b["id"]}={len(b["posts"])}' for b in data['boards']))


if __name__ == '__main__':
    main()
