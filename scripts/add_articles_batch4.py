#!/usr/bin/env python3
"""Batch 4: 5 articles to reach 50 total. Final batch before AdSense application."""
import json, re, sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parent.parent
ARTICLES_JSON = ROOT / 'articles.json'
SITEMAP = ROOT / 'sitemap.xml'
TODAY = date.today()
BASE = 'https://dingjiu1989-hue.github.io'

NEW = [
    # ═══ TOOLS (1) ══════════════════════════════════════════════════
    dict(board='tools', slug='project-management-tools', date=TODAY.isoformat(),
         title='2026 年最佳项目管理工具对比：Jira vs Linear vs Notion vs ClickUp',
         description='四大主流项目管理工具全方位横评，涵盖任务管理、自动化、AI 功能、价格，帮团队选出最佳协作平台。',
         tags=['项目管理', '团队协作', '对比评测'], replies=33, hot=True,
         body='''<p>选错项目管理工具，团队每天浪费 30 分钟在跟工具搏斗上。2026 年的 PM 工具已经全面 AI 化——自动分配任务、智能排期、自然语言生成报表。这篇横评帮你一次选对。</p>
<h2>四大工具核心对比</h2>
<table><tr><th>维度</th><th>Jira</th><th>Linear</th><th>Notion</th><th>ClickUp</th></tr>
<tr><td>定位</td><td>企业级研发管理</td><td>现代软件开发</td><td>全能协作平台</td><td>一站式生产力</td></tr>
<tr><td>适合团队</td><td>50+ 人工程团队</td><td>5-100 人技术团队</td><td>任何规模</td><td>中小企业</td></tr>
<tr><td>学习曲线</td><td>陡峭（需要管理员）</td><td>平缓（分钟级上手）</td><td>中等</td><td>中等偏高</td></tr>
<tr><td>AI 能力</td><td>Atlassian Intelligence</td><td>Linear AI（自动分派、相似问题检测）</td><td>Notion AI（写作、总结、自动建库）</td><td>ClickUp AI（全平台 AI 助手）</td></tr>
<tr><td>免费版</td><td>10 人以下免费</td><td>免费版功能完整</td><td>免费版个人够用</td><td>免费版功能最多</td></tr>
<tr><td>付费起步</td><td>$8.15/人/月</td><td>$8/人/月</td><td>$10/人/月</td><td>$7/人/月</td></tr></table>
<h2>逐个分析</h2>
<h3>Jira — 企业级巨无霸</h3>
<p>功能最多但也最复杂。如果你在 100 人以上的工程团队，Jira 几乎是唯一选择——权限管理、工作流定制、合规审计这些企业需求只有它能满足。但小团队用 Jira 就像用坦克去买菜，杀鸡用牛刀。</p>
<h3>Linear — 开发者的心头好</h3>
<p>快捷键驱动、闪电般流畅、UI 审美在线。Linear 是为软件工程师设计的——Issue 状态流转像 Vim 一样快，Roadmap 视图清晰到可以直接给投资人看。2026 年的 Linear AI 可以自动检测重复 Issue、建议负责人、预估工期。缺点是：非技术团队（市场、运营）用起来不太顺手。</p>
<h3>Notion — 不止是项目管理</h3>
<p>Notion 的灵活性是一把双刃剑。你可以用它做项目管理、知识库、会议记录、招聘 pipeline……但也因为没有固定结构，每个团队都要自己搭一套。Notion AI 现在支持从自然语言描述直接生成数据库——说"创建一个 Sprint 管理模板"就自动建好。</p>
<h3>ClickUp — 功能最全的挑战者</h3>
<p>ClickUp 的策略是"Jira 有的我都有，还更便宜"。确实——甘特图、时间追踪、目标管理、文档协作、白板，一应俱全。但功能太多导致界面有些拥挤，学习成本不低。适合想要 Jira 级功能但预算有限的团队。</p>
<h2>怎么选</h2>
<ul><li><strong>纯技术团队（5-50人）</strong> → Linear。速度快、体验好、工程师爱用。如果工程师讨厌你现在的工具，换 Linear 会让团队士气明显提升。</li><li><strong>大型企业研发团队</strong> → Jira。不是因为它最好用，而是因为它最完整——合规、权限、报表、集成生态没有对手。</li><li><strong>全能型/非技术团队</strong> → Notion。一个工具替代项目管理+知识库+文档协作，减少工具切换成本。</li><li><strong>预算敏感/需要全功能</strong> → ClickUp。性价比最高，免费版就够很多小团队用了。</li></ul>
<h2>避坑指南</h2><p>不要同时用两个项目管理工具——信息分散、更新不同步、最终两个都不用。选定一个，全团队强制使用，三个月后再评估是否要换。</p>'''),

    # ═══ TECH (1) ═══════════════════════════════════════════════════
    dict(board='tech', slug='git-advanced', date=TODAY.isoformat(),
         title='Git 进阶：交互式 rebase、cherry-pick 和 bisect 实战',
         description='进阶 Git 技巧三件套：用交互式 rebase 整理提交历史、用 cherry-pick 精确移植代码、用 bisect 二分法定位 Bug，让你的 Git 段位从熟练进化到精通。',
         tags=['Git', '进阶', '开发工具'], replies=19, hot=True,
         body='''<p>如果你已经会 add/commit/push/pull，是时候学这三个进阶命令了。它们不会让你每天多用 Git，但在关键时刻能省下几个小时。</p>
<h2>交互式 Rebase：整理你的提交历史</h2>
<p>场景：你吭哧吭哧写了一下午，做了 12 个小提交，但提交信息都是 "wip"、"fix"、"fix again"。现在要提交 PR 了——这些乱七八糟的提交历史会让同事鄙视你。</p>
<pre><code>git rebase -i HEAD~12</code></pre>
<p>会打开编辑器，列出最近 12 个提交：</p>
<pre><code>pick a1b2c3d wip
pick e4f5g6h fix typo
pick i7j8k9l fix again
pick m0n1o2p actually works now
...</code></pre>
<p>核心操作：</p>
<ul><li><strong>squash (s)</strong> — 把当前提交合并到上一个，保留所有更改但合并为一个提交</li><li><strong>fixup (f)</strong> — 类似 squash，但丢弃当前提交的信息（适合那些 "wip" 提交）</li><li><strong>reword (r)</strong> — 只改提交信息，不改内容</li><li><strong>drop (d)</strong> — 删除这个提交</li><li><strong>edit (e)</strong> — 停下来让你修改这个提交的内容</li></ul>
<p>把 12 个乱七八糟的提交整理成 3 个逻辑清晰的提交：</p>
<pre><code>pick a1b2c3d feat: 添加用户登录 API
fixup e4f5g6h wip
fixup i7j8k9l fix typo
pick m0n1o2p feat: 添加 JWT Token 验证
fixup n2o3p4q fix again
pick r5s6t7u docs: 更新 API 文档
fixup v8w9x0y wip doc</code></pre>
<p>保存退出，Git 自动完成。提交历史从一团乱麻变成清晰的叙事。<strong>注意：只在还没 push 的分支上做 rebase。已经 push 的提交，rebase 会改写历史，需要 force push——在共享分支上这是灾难。</strong></p>
<h2>Cherry-Pick：精准移植代码</h2>
<p>场景：你在 feature-A 分支上写了一个特别好用的工具函数，feature-B 也需要它。但你不想合并整个 feature-A 分支。</p>
<pre><code># 找到那个提交的 hash
git log feature-A --oneline

# 摘樱桃
git checkout feature-B
git cherry-pick a1b2c3d</code></pre>
<p>Git 会把这个提交的变更单独应用到 feature-B 上，生成一个新的提交（hash 不同，内容相同）。</p>
<p>常见用法：</p>
<ul><li><strong>移植 Bug 修复</strong> — 在 hotfix 分支修了一个 Bug，cherry-pick 到 main 和 dev 分支</li><li><strong>复用工具代码</strong> — 在一个分支写的基础组件，移植到另一个分支</li><li><strong>回滚后重新应用</strong> — revert 了一个提交后又想加回来</li></ul>
<pre><code># 一次 cherry-pick 多个提交
git cherry-pick a1b2c3d e4f5g6h i7j8k9l

# 如果冲突了
git cherry-pick a1b2c3d
# 解决冲突...
git add .
git cherry-pick --continue

# 放弃这次 cherry-pick
git cherry-pick --abort</code></pre>
<h2>Git Bisect：二分法定位 Bug</h2>
<p>场景：两周前一切正常，今天发现一个 Bug，但中间有 200 个提交。是谁引入的？</p>
<p>Bisect 用二分查找自动定位——你只需要告诉 Git 哪个提交是好的、哪个是坏的，然后 Git 切到中间点让你测试。</p>
<pre><code>git bisect start
git bisect bad HEAD          # 当前版本有 Bug
git bisect good v2.0.0       # v2.0.0 是正常的

# Git 自动切到中间某个提交
# 测试这个版本有没有 Bug...

# 如果有 Bug:
git bisect bad

# 如果正常:
git bisect good

# 重复 5-8 次，Git 定位到引入 Bug 的那个提交
# de7f3a2 is the first bad commit

# 结束 bisect
git bisect reset</code></pre>
<p>200 个提交，log2(200) ≈ 8 次测试就能定位。比一个一个找快 25 倍。</p>
<pre><code># 自动化 bisect（如果你的测试可以用脚本跑）
git bisect start
git bisect bad HEAD
git bisect good v2.0.0
git bisect run python test_specific_feature.py
# Git 自动二分查找，输出引入 Bug 的提交</code></pre>
<h2>总结</h2>
<table><tr><th>命令</th><th>用途</th><th>一句话</th></tr>
<tr><td><code>git rebase -i</code></td><td>整理提交历史</td><td>把 12 个 wip 整理成 3 个清晰的 commit</td></tr>
<tr><td><code>git cherry-pick</code></td><td>移植单个提交</td><td>把 A 分支的好代码复制到 B 分支</td></tr>
<tr><td><code>git bisect</code></td><td>二分查找 Bug</td><td>从 200 个提交中快速定位是谁引入的 Bug</td></tr></table>
<p>这三个命令是高级 Git 用户的标志。不需要每天用，但需要的时候知道怎么用——你的同事会以为你是 Git 魔法师。</p>'''),

    # ═══ SIDEHUSTLE (1) ═════════════════════════════════════════════
    dict(board='sidehustle', slug='affiliate-marketing', date=TODAY.isoformat(),
         title='Affiliate Marketing 完全入门指南：从 0 到第一笔佣金',
         description='手把手教你从零开始做联盟营销：选平台、选产品、做内容、引流量，全套实操流程助你拿到第一笔被动收入。',
         tags=['联盟营销', '被动收入', '副业'], replies=28, hot=True,
         body='''<p>联盟营销（Affiliate Marketing）是最经典的被动收入模式之一——你推荐产品，有人通过你的链接购买，你拿佣金。不需要自己囤货、处理售后、跟客户扯皮。这篇文章讲清楚从注册到第一笔佣金的完整流程。</p>
<h2>什么是联盟营销</h2>
<p>简单说：你是一根管道。用户在 Google 搜"最好的机械键盘"→ 看到你的评测文章 → 点你的推荐链接 → 在商家下单 → 你拿 5%-30% 佣金。整个过程你不需要碰产品。</p>
<h2>第一步：选平台（选一个进场）</h2>
<table><tr><th>平台</th><th>佣金率</th><th>适合</th><th>特点</th></tr>
<tr><td><strong>Amazon Associates</strong></td><td>1%-10%</td><td>实物产品推荐</td><td>转化率最高（人人信任亚马逊），但佣金率最低。Cookie 仅 24 小时。</td></tr>
<tr><td><strong>ShareASale</strong></td><td>5%-50%</td><td>SaaS、课程、数字产品</td><td>商家多、品类全。数字产品佣金远高于实物。</td></tr>
<tr><td><strong>CJ Affiliate</strong></td><td>5%-30%</td><td>品牌产品</td><td>大品牌多（Nike、GoDaddy），审核较严。</td></tr>
<tr><td><strong>Impact</strong></td><td>5%-50%</td><td>高佣金 SaaS</td><td>SaaS 公司多（Canva、Shopify），经常有 $50-$200 的固定佣金。</td></tr>
<tr><td><strong>国内：淘宝联盟</strong></td><td>1%-50%</td><td>淘宝/天猫商品</td><td>国内最大，品类最全。高佣金商品佣金率可达 50%。</td></tr>
<tr><td><strong>国内：京东联盟</strong></td><td>1%-30%</td><td>京东商品</td><td>客单价高，3C 数码类佣金可观。</td></tr></table>
<h2>第二步：选产品/利基</h2>
<p>选产品的三个原则：</p>
<ol><li><strong>你用过或懂的产品</strong> — 写出来的内容有说服力，"我用过"三个字价值千金</li><li><strong>客单价适中</strong> — $50-$500 是甜蜜点。太低佣金不够，太高决策周期长</li><li><strong>有搜索量</strong> — 用 Google Keyword Planner 或 Ahrefs 确认有人搜相关关键词</li></ol>
<p>好的利基示例："程序员装备推荐"、"远程办公工具"、"摄影入门器材"、"减肥补剂对比"。</p>
<h2>第三步：做内容（这是核心）</h2>
<p>联盟营销 80% 的工作是做内容。以下是最有效的四种内容类型：</p>
<ul><li><strong>对比评测</strong> — "X vs Y 哪个好？" 这类关键词购买意图最强。搜索结果第一条每天能带来几百个精准流量。</li><li><strong>Best of 列表</strong> — "2026 年最佳 XX Top 10"。人们喜欢列表，搜"best"的人就是在找购买建议。</li><li><strong>单品深度评测</strong> — 完整的使用体验 + 优缺点 + 适合什么人。2000 字起步，有真实照片更佳。</li><li><strong>教程/How-to</strong> — "怎么选机械键盘？" 在教程中自然植入产品推荐，转化率远高于硬广。</li></ul>
<h2>第四步：引流量</h2>
<p>两种主要策略：</p>
<ul><li><strong>SEO（搜索引擎优化）</strong> — 写高质量内容，等 Google 排名。慢（3-6 个月见效）但可持续，文章一旦排上首页就是持续被动收入。</li><li><strong>社交媒体 + 社群</strong> — 在 Reddit/知乎/Twitter/小红书分享有用的内容，自然植入推荐链接。快但需要持续运营。</li></ul>
<p>建议双管齐下：主攻 SEO 做长期资产，同时用社交媒体引流做短期补充。</p>
<h2>第五步：合规和优化</h2>
<ul><li><strong>必须披露</strong> — FTC（美国）和国内法规都要求在明显位置声明"本文包含 affiliate 链接"。既是法律要求，也能建立读者信任。</li><li><strong>追踪转化</strong> — 每个平台用单独的追踪 ID，知道哪篇文章、哪个链接带来了收入。</li><li><strong>优化高转化内容</strong> — 找到带来最多点击的文章，持续更新、加更多产品推荐、改进 CTA。</li></ul>
<h2>真实收益预期</h2>
<p>前 3 个月可能只有 $50-200/月——内容在积累，还没排上名。6-12 个月后，如果你持续输出高质量内容，$500-3000/月是可达的。顶尖的 affiliate 博主月入 $10K-50K+，但这需要 2-3 年的积累和优质内容矩阵。</p>
<p><strong>关键心态：这不是快速致富，是建立内容资产。每一篇好文章都是 24 小时替你赚钱的数字员工。</strong></p>'''),

    # ═══ AI (2) ══════════════════════════════════════════════════
    dict(board='ai', slug='openai-api-intro', date=TODAY.isoformat(),
         title='OpenAI API 入门：用 10 行代码调用 GPT',
         description='零基础入门 OpenAI API，从获取 Key 到发出第一个请求，涵盖 Chat Completion、System Prompt、Temperature 等核心概念，附带可运行的 Python 和 JS 示例。',
         tags=['OpenAI API', 'GPT', '编程入门'], replies=26,
         body='''<p>调用 GPT API 比你想的简单得多——10 行代码就能让 AI 替你写文案、分析数据、回答问题。这篇文章带你从零到发出第一个 API 请求。</p>
<h2>第一步：获取 API Key</h2>
<ol><li>打开 <a href="https://platform.openai.com" target="_blank">platform.openai.com</a> 注册/登录</li><li>点击右上角头像 → "View API keys"</li><li>"Create new secret key" → 复制保存（只显示一次！）</li><li>设置用量限制（建议先设 $10/月，防止意外超支）</li></ol>
<p><strong>API 是按量付费的，不是订阅制。</strong>你可以只充值 $5 开始试用。GPT-4o mini 的价格大约是 $0.15/1M input tokens —— 处理 100 万字的输入只要一毛多。$5 够你做大量实验。</p>
<h2>第二步：安装 SDK</h2>
<pre><code>pip install openai</code></pre>
<h2>第三步：第一个请求</h2>
<pre><code>from openai import OpenAI

client = OpenAI(api_key="sk-your-key-here")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "你是一个简洁的编程助手，回复不超过三句话。"},
        {"role": "user", "content": "Python 中 list 和 tuple 的区别是什么？"}
    ]
)

print(response.choices[0].message.content)</code></pre>
<p>跑一下——AI 用三句话回答了你的问题。</p>
<h2>核心概念拆解</h2>
<table><tr><th>概念</th><th>是什么</th><th>怎么用</th></tr>
<tr><td><strong>Model</strong></td><td>用哪个模型</td><td>gpt-4o（最强）、gpt-4o-mini（便宜快速、日常够用）、o1（深度推理）</td></tr>
<tr><td><strong>Messages</strong></td><td>对话历史</td><td>三中角色：system（设定 AI 行为）、user（你的问题）、assistant（AI 之前的回答）</td></tr>
<tr><td><strong>System Prompt</strong></td><td>给 AI 的"人设"</td><td>最重要的部分。好的 System Prompt 能让 GPT-4o mini 的效果超过乱用的 GPT-4o</td></tr>
<tr><td><strong>Temperature</strong></td><td>控制随机性（0-2）</td><td>0 = 每次回答一样（适合代码/事实）、1 = 有创造性（适合写作）、1.5+ = 天马行空</td></tr>
<tr><td><strong>max_tokens</strong></td><td>限制输出长度</td><td>1 token ≈ 0.75 个英文单词 ≈ 0.5 个中文字。设太低回答会被截断</td></tr></table>
<h2>实用示例：多轮对话</h2>
<pre><code>messages = [
    {"role": "system", "content": "你是一个 Python 编程导师，用 50 字以内回答。"}
]

while True:
    user_input = input("你: ")
    if user_input == "quit":
        break
    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    reply = response.choices[0].message.content
    print(f"AI: {reply}")
    messages.append({"role": "assistant", "content": reply})</code></pre>
<h2>实用示例：用 GPT 做数据分析</h2>
<pre><code># 读取 CSV，让 GPT 写分析代码
import csv

data = []
with open("sales.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append(row)

data_str = str(data[:5])  # 只传前 5 行作为样本

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "你是数据分析师。根据提供的数据样本，写出完整的 Python pandas 分析代码。"},
        {"role": "user", "content": f"分析这个销售数据的前5行，写代码计算每月的销售总额和增长率：{data_str}"}
    ]
)
print(response.choices[0].message.content)
# GPT 会生成可以直接复制运行的 pandas 分析代码</code></pre>
<h2>费用控制</h2>
<ul><li><strong>设 hard limit</strong> — 在 OpenAI Platform → Billing → Usage limits 设每月上限</li><li><strong>用 gpt-4o-mini</strong> — 95% 的场景够用，价格是 GPT-4o 的 1/20</li><li><strong>缓存常见回复</strong> — 同样的 prompt 不要反复调用，存起来复用</li><li><strong>监控用量</strong> — Usage 页面可以实时看到花了多少钱</li></ul>
<h2>下一步</h2>
<p>读完这篇文章你应该能跑起第一个 API 调用了。接下来可以：用 <code>stream=True</code> 实现打字机效果、用 Function Calling 让 GPT 调用你的函数、用 Assistants API 构建带知识库的 AI 助手。OpenAI 的官方文档写得很好——把它当参考书，需要时查。</p>'''),

    dict(board='ai', slug='ai-art-monetization', date=TODAY.isoformat(),
         title='AI 绘画变现指南：从出图到接单的完整路径',
         description='手把手教你将 AI 绘画技能变现：接单平台、素材销售、自媒体涨粉、定制服务四大路径，附定价策略和接单避坑。',
         tags=['AI绘画', '变现', 'Midjourney', '副业'], replies=31, hot=True,
         body='''<p>AI 绘画从"好玩"到"能赚钱"的距离，比大多数人想的短。不需要美术功底，掌握工具 + 懂需求就能变现。这篇文章讲清楚四个主流路径。</p>
<h2>路径一：接单平台接定制需求</h2>
<p>这是最快见到钱的方式。客户需要什么？</p>
<ul><li><strong>头像/Avatar</strong> — AI 生成个人头像、情侣头像、宠物头像。单价 ¥30-100，需求量大</li><li><strong>Logo 设计</strong> — 小企业和个人品牌的低成本 Logo。单价 ¥100-500</li><li><strong>海报/封面</strong> — 公众号封面、小红书封面、播客封面。单价 ¥50-200</li><li><strong>包装设计</strong> — 产品包装、标签、菜单。单价 ¥200-800</li></ul>
<p>在哪接单：</p>
<table><tr><th>平台</th><th>类型</th><th>特点</th></tr>
<tr><td>Fiverr</td><td>海外</td><td>最大市场，英语好有优势。AI头像类Gig竞争激烈但需求大。</td></tr>
<tr><td>Upwork</td><td>海外</td><td>客单价更高，但需要 Pro 级别的作品集。</td></tr>
<tr><td>猪八戒/一品威客</td><td>国内</td><td>设计需求多，但价格竞争激烈。适合练手和积累作品。</td></tr>
<tr><td>小红书/闲鱼</td><td>国内</td><td>发作品 → 有人问 → 私信成交。没有平台抽成，利润全归自己。</td></tr>
<tr><td>淘宝</td><td>国内</td><td>做 AI 头像/AI 修图的店铺，有自然搜索流量。</td></tr></table>
<h2>路径二：素材销售（被动收入）</h2>
<p>把你的 AI 作品上传到素材平台，有人下载就分成。一次创作，持续销售。</p>
<ul><li><strong>Freepik</strong> — 最大素材平台之一，AI 生成内容接受度高。按下载量分成。</li><li><strong>Adobe Stock</strong> — 直接接受 AI 生成内容（需标记为 "Generative AI"）。单价高但审核严。</li><li><strong>Shutterstock</strong> — 有专门的 AI 内容政策，需要明确标注。</li><li><strong>Creative Fabrica</strong> — 专注手工艺和设计素材，AI 内容需要 quality check。</li></ul>
<p><strong>什么素材好卖？</strong> 花纹/图案（pattern）、壁纸/背景、图标套装、字体效果、节日主题素材（圣诞节、春节等季节性内容搜索量暴增）。</p>
<h2>路径三：自媒体涨粉 → 广告/课程变现</h2>
<p>在小红书/抖音/Instagram/YouTube 发布 AI 作品 + 教程，积累粉丝后变现：</p>
<ul><li><strong>广告合作</strong> — 品牌找你推广 AI 工具、设计软件</li><li><strong>付费教程</strong> — 卖 Midjourney/Stable Diffusion 提示词包、教程课程</li><li><strong>Prompt 商店</strong> — PromptBase 等平台可以卖提示词，单价 $1.99-9.99</li></ul>
<p>内容选题方向：AI 作品展示（视觉冲击）、提示词教学（实用价值）、行业趋势评论（思想领导力）。</p>
<h2>路径四：为企业提供 AI 设计服务</h2>
<p>升级版接单——不只出图，而是提供完整的视觉解决方案。客户从个人变成企业，客单价从几百变成几千甚至几万。</p>
<ul><li><strong>电商产品图</strong> — 用 AI 生成产品场景图，替代传统摄影。一个 SKU 可以生成 10 个不同场景的产品图。</li><li><strong>品牌视觉包</strong> — Logo + 配色 + 字体 + 应用模板，一整套。中小企业品牌升级的平价选择。</li><li><strong>游戏/App 素材</strong> — 图标、角色、场景、UI 元素。独立开发者和游戏工作室是优质客户。</li></ul>
<h2>定价策略</h2>
<ul><li><strong>不要按小时定价</strong> — 按交付物的商业价值定价。一个帮客户多卖 $1000 的产品图，收费 $200 是合理的。</li><li><strong>打包卖，不要单卖</strong> — "10 张不同风格头像 ¥299" 比 "1 张 ¥50" 更好卖，客户感觉更值。</li><li><strong>先低后高</strong> — 先做 3-5 个低价单积累作品和好评，然后逐步提价。</li></ul>
<h2>避坑</h2>
<ul><li><strong>明确版权归属</strong> — AI 生成内容的版权在不同平台规则不同。交付前跟客户说清楚：能不能二次修改？能不能商用？</li><li><strong>不要冒充手绘</strong> — 诚实标注 AI 生成。被拆穿对信誉伤害巨大。</li><li><strong>不要接任何涉及真人肖像的定制</strong> — deepfake 的法律风险你承担不起。</li></ul>
<h2>我的建议</h2>
<p>最稳健的起步路径：<strong>小红书发 AI 作品 → 积累作品集和粉丝 → 同时在 Fiverr 开店 → 接单赚到第一笔钱 → 把最好的作品上传素材平台做被动收入。</strong>先用路径一和三赚到正反馈，再逐步扩展到路径二和四。关键是开始行动——先做出 10 张你觉得能卖的作品。</p>'''),
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
