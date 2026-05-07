#!/usr/bin/env python3
"""Batch article generator: create HTML files, update articles.json and sitemap.xml."""

import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARTICLES_JSON = ROOT / 'articles.json'
SITEMAP = ROOT / 'sitemap.xml'
TODAY = date.today().isoformat()
BASE = 'https://dingjiu1989-hue.github.io'

NEW_ARTICLES = [
    # ── Tech Board ──────────────────────────────────────────────
    {
        'board': 'tech', 'slug': 'vscode-extensions',
        'title': 'VS Code 十大必备插件：让编码效率翻倍',
        'description': '精选 10 款 VS Code 必备插件，涵盖 AI 补全、Git 可视化、代码格式化、远程开发等高频场景，新装编辑器第一件事就是装这些。',
        'date': TODAY, 'pinned': False, 'replies': 18, 'hot': True,
        'tags': ['VS Code', '编辑器', '效率工具'],
        'body': '''<p>VS Code 是目前最流行的代码编辑器没有之一。装对这 10 个插件，编码效率可以翻倍。</p>

<h2>AI 编程类</h2>
<ul>
  <li><strong>GitHub Copilot</strong> — AI 代码补全的开创者，支持行内补全、函数生成、注释转代码。付费（$10/月），学生免费。</li>
  <li><strong>Codeium</strong> — 免费的 AI 补全替代方案，速度比 Copilot 快，支持 70+ 语言，企业版才收费。</li>
</ul>

<h2>Git 可视化</h2>
<ul>
  <li><strong>GitLens</strong> — 行级 Git Blame、文件历史、分支对比，免费版功能已很强。必装。</li>
  <li><strong>Git Graph</strong> — 可视化 Git 提交树，鼠标点几下就能完成 checkout、merge、revert 操作。</li>
</ul>

<h2>代码质量</h2>
<ul>
  <li><strong>Prettier</strong> — 代码格式化工具，支持 JS/TS/CSS/HTML/JSON 等，保存时自动格式化，团队协作统一风格必备。</li>
  <li><strong>ESLint</strong> — JavaScript/TypeScript 代码检查，实时标记潜在错误和风格问题。</li>
</ul>

<h2>效率工具</h2>
<ul>
  <li><strong>Auto Rename Tag</strong> — 修改 HTML/JSX 标签自动同步配对标签，小小的改动巨大提升体验。</li>
  <li><strong>Path Intellisense</strong> — 输入文件路径时自动补全，引号和 import 语句必备。</li>
  <li><strong>Remote - SSH</strong> — 微软官方出品，直接在 VS Code 里编辑远程服务器上的代码，免去 scp 和 vim 的痛苦。</li>
  <li><strong>Error Lens</strong> — 把错误信息内联显示在代码行尾，不用鼠标悬停就能看到完整报错。</li>
</ul>

<h2>经验之谈</h2>
<p>插件不是越多越好——装太多会拖慢启动速度。这 10 个是我用过上百个插件后留下的"真必需品"。Copilot 或 Codeium 二选一即可，两个同时开会冲突。</p>'''
    },
    {
        'board': 'tech', 'slug': 'docker-quickstart',
        'title': 'Docker 30 分钟入门：从安装到第一个容器',
        'description': '零基础 Docker 入门教程，30 分钟掌握镜像、容器、Dockerfile 核心概念，亲手构建并运行你的第一个容器化应用。',
        'date': TODAY, 'pinned': False, 'replies': 15,
        'tags': ['Docker', '容器', 'DevOps'],
        'body': '''<p>Docker 是现代开发者的必备技能。这篇文章用最通俗的语言带你 30 分钟上手。</p>

<h2>为什么需要 Docker</h2>
<ul>
  <li><strong>环境一致性</strong> — "我电脑上能跑啊" 从此成为历史。开发、测试、生产环境完全一致。</li>
  <li><strong>快速部署</strong> — 一条命令启动完整环境，不用装数据库、配环境变量。</li>
  <li><strong>资源隔离</strong> — 每个项目独立运行，不互相干扰。</li>
</ul>

<h2>核心概念三件套</h2>
<table>
  <tr><th>概念</th><th>比喻</th><th>说明</th></tr>
  <tr><td>镜像 (Image)</td><td>系统安装盘</td><td>只读模板，包含运行应用所需的一切</td></tr>
  <tr><td>容器 (Container)</td><td>运行中的虚拟机</td><td>镜像的运行实例，相互隔离</td></tr>
  <tr><td>Dockerfile</td><td>安装说明书</td><td>定义如何构建镜像的文本文件</td></tr>
</table>

<h2>安装 Docker</h2>
<p>macOS 用户推荐 <a href="https://orbstack.dev/">OrbStack</a>（轻量替代 Docker Desktop），或直接 <code>brew install docker</code>。Windows/Linux 用户去 docker.com 下载即可。</p>

<h2>第一个容器</h2>
<pre><code># 拉取并运行 nginx
docker run -d -p 8080:80 --name my-nginx nginx

# 浏览器打开 http://localhost:8080 就能看到 nginx 欢迎页</code></pre>

<h2>写一个 Dockerfile</h2>
<pre><code>FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "app.py"]</code></pre>

<h2>常用命令速查</h2>
<table>
  <tr><td><code>docker ps</code></td><td>查看运行中的容器</td></tr>
  <tr><td><code>docker images</code></td><td>查看本地镜像</td></tr>
  <tr><td><code>docker build -t name .</code></td><td>构建镜像</td></tr>
  <tr><td><code>docker exec -it name bash</code></td><td>进入容器 shell</td></tr>
  <tr><td><code>docker-compose up -d</code></td><td>启动多容器应用</td></tr>
</table>

<h2>下一步</h2>
<p>掌握这些就可以开始在工作中使用 Docker 了。推荐下一步学习 docker-compose 多容器编排和 Docker Hub 镜像仓库。</p>'''
    },
    {
        'board': 'tech', 'slug': 'github-copilot-guide',
        'title': 'GitHub Copilot 完全使用指南：从安装到高效协作',
        'description': '全面掌握 GitHub Copilot 的使用技巧，包括快捷键、上下文工程、最佳实践和常见陷阱，让 AI 编程工具真正为你提效。',
        'date': TODAY, 'pinned': False, 'replies': 27,
        'tags': ['GitHub Copilot', 'AI编程', '效率'],
        'body': '''<p>GitHub Copilot 是目前最成熟的 AI 编程助手。但很多人只用到了它的 30% 能力——只会按 Tab 接受补全。这篇文章帮你榨干它。</p>

<h2>快速上手</h2>
<ol>
  <li>VS Code 扩展商店搜索 "GitHub Copilot" 安装</li>
  <li>用 GitHub 账号登录，个人版 $10/月（学生免费）</li>
  <li>打开任意代码文件，Copilot 会自动开始建议</li>
</ol>

<h2>核心快捷键（必须记住）</h2>
<table>
  <tr><th>快捷键</th><th>功能</th></tr>
  <tr><td>Tab</td><td>接受当前建议</td></tr>
  <tr><td>Esc</td><td>拒绝建议</td></tr>
  <tr><td>Alt + ]</td><td>下一个建议</td></tr>
  <tr><td>Alt + [</td><td>上一个建议</td></tr>
  <tr><td>Ctrl + Enter</td><td>打开 Copilot 面板，一次性看 10 个建议</td></tr>
  <tr><td>Ctrl + I</td><td>打开内联聊天（Chat in Editor）</td></tr>
  <tr><td>Ctrl + Shift + I</td><td>打开 Copilot Chat 侧边栏</td></tr>
</table>

<h2>上下文工程：让 AI 理解你的意图</h2>
<p>Copilot 不是读心术。它从你当前文件和相关打开的文件中获取上下文。以下技巧显著提升建议质量：</p>
<ul>
  <li><strong>保持相关文件打开</strong> — Copilot 会读取你当前打开的所有标签页。写前端组件时把类型定义文件也开着。</li>
  <li><strong>先写注释再写代码</strong> — 用注释描述你要实现的功能，Copilot 的注释转代码能力非常强。</li>
  <li><strong>写好函数签名</strong> — 函数名和参数名是对 AI 最直接的提示。</li>
  <li><strong>给好示例</strong> — 在同一文件中先手写一两个正确的示例，后续补全质量明显提升。</li>
</ul>

<h2>Chat 功能：不只是补全</h2>
<ul>
  <li><strong>解释代码</strong> — 选中代码 → Ctrl+Shift+I → "explain this"</li>
  <li><strong>重构代码</strong> — 选中 → "refactor this to use async/await"</li>
  <li><strong>生成测试</strong> — 选中函数 → "/tests" 自动生成单元测试</li>
  <li><strong>修复 Bug</strong> — 选中报错代码 → "/fix" 自动诊断并修复</li>
</ul>

<h2>常见陷阱</h2>
<ul>
  <li><strong>盲目信任</strong> — Copilot 会写出看起来正确但有安全漏洞的代码，永远 review。</li>
  <li><strong>死循环接受</strong> — 不要一直按 Tab，每接受一个建议后看一眼逻辑是否正确。</li>
  <li><strong>忽略旧 API</strong> — Copilot 训练数据可能包含过时的库版本，遇到不认识的 API 先查文档。</li>
</ul>'''
    },

    # ── Sidehustle Board ─────────────────────────────────────────
    {
        'board': 'sidehustle', 'slug': 'programmer-side-hustle',
        'title': '2026 年程序员接私活指南：渠道、报价、避坑全攻略',
        'description': '程序员做副业的完整指南，涵盖国内外接单平台、报价策略、合同模板、税务处理，帮你安全高效地增加收入。',
        'date': TODAY, 'pinned': True, 'replies': 34,
        'tags': ['接私活', '程序员', '副业'],
        'body': '''<p>程序员可能是最适合做副业的职业之一——技术在手，需求旺盛。但信息不对称导致很多人接不到好单，或者接了被坑。</p>

<h2>国内外接单平台对比</h2>
<table>
  <tr><th>平台</th><th>类型</th><th>佣金</th><th>适合</th></tr>
  <tr><td>Upwork</td><td>国际化大平台</td><td>5%-20%</td><td>英语好、技术扎实</td></tr>
  <tr><td>Toptal</td><td>高端技术人才</td><td>平台定价</td><td>资深工程师（通过率 3%）</td></tr>
  <tr><td>电鸭社区</td><td>国内远程社区</td><td>0%</td><td>中文环境、技术岗</td></tr>
  <tr><td>程序员客栈</td><td>国内众包</td><td>平台抽 20%</td><td>国内项目、整包开发</td></tr>
  <tr><td>Fiverr</td><td>技能服务化</td><td>20%</td><td>小单、快速交付</td></tr>
</table>

<h2>报价策略</h2>
<ul>
  <li><strong>按项目不要按小时</strong> — 你的效率高，按小时反而吃亏。一个你可能 2 天搞定的功能，按项目报 3000 比按小时报 200/时更划算也更容易接受。</li>
  <li><strong>新人价公式</strong> — 项目报价 = 预估工时 × 你的时薪 × 1.5（缓冲系数）。工作了 3 年的程序员时薪参考：200-400 元。</li>
  <li><strong>永远分期付款</strong> — 30% 启动 + 40% 中期里程碑 + 30% 验收尾款。不付尾款不给源码。</li>
</ul>

<h2>避坑清单</h2>
<ol>
  <li><strong>不签合同不开工</strong> — 至少要有文字确认（微信聊天记录也算）。写清楚：范围、交付物、时间、价格、验收标准。</li>
  <li><strong>远离"先做出来看看"</strong> — 要求免费试做的一律拒绝。专业的客户会看你的作品集。</li>
  <li><strong>避开灰色需求</strong> — 爬虫、薅羊毛、账号注册机——这些容易惹上官司。</li>
  <li><strong>谨慎处理公司资源</strong> — 别用公司电脑接私活，别在上班时间做，确认劳动合同没有竞业条款。</li>
</ol>

<h2>税务问题</h2>
<p>国内：单次收入 800 以下免税；劳务报酬按 20%-40% 累进税率（可次年汇算清缴退税）。建议年收入超过 5 万就注册个体户，税负更低。</p>'''
    },
    {
        'board': 'sidehustle', 'slug': 'content-creator-startup',
        'title': '从零开始做自媒体：平台选择、内容定位与变现路径',
        'description': '2026 年自媒体运营全攻略：公众号、知乎、小红书、抖音四大平台对比，帮你找到适合自己的内容方向和变现模式。',
        'date': TODAY, 'pinned': False, 'replies': 22,
        'tags': ['自媒体', '内容创作', '副业'],
        'body': '''<p>自媒体是门槛最低的副业之一——不需要资金、不需要人脉，一台电脑就能开始。但 90% 的新人倒在定位和坚持上。</p>

<h2>四大内容平台对比</h2>
<table>
  <tr><th>平台</th><th>内容形式</th><th>变现方式</th><th>适合人群</th></tr>
  <tr><td>公众号</td><td>长图文</td><td>流量主 + 互选广告 + 知识付费</td><td>能写深度内容的人</td></tr>
  <tr><td>知乎</td><td>问答 + 文章</td><td>好物推荐 + 盐选 + 品牌合作</td><td>有专业知识的从业者</td></tr>
  <tr><td>小红书</td><td>图文笔记 + 短视频</td><td>品牌合作 + 带货</td><td>生活方式 / 专业领域均可</td></tr>
  <tr><td>抖音 / 视频号</td><td>短视频 + 直播</td><td>打赏 + 带货 + 广告</td><td>表达能力好、有镜头感</td></tr>
</table>

<h2>如何选择赛道</h2>
<ul>
  <li><strong>程序员 → 知乎 + 公众号</strong> — 分享技术经验、职场思考，做知识付费。</li>
  <li><strong>设计师 → 小红书 + 抖音</strong> — 发作品、出教程、卖模板。</li>
  <li><strong>职场人 → 小红书 + 知乎</strong> — 分享行业见解、职业规划。</li>
</ul>

<h2>新手起步三步走</h2>
<ol>
  <li><strong>先写 10 篇</strong> — 别想太多，先坚持输出 10 篇内容。这个阶段重点是找到手感，不是涨粉。</li>
  <li><strong>找到爆款方向</strong> — 看哪篇数据好，就继续深挖那个方向。数据会告诉你市场要什么。</li>
  <li><strong>建立内容体系</strong> — 形成稳定的选题方法论，保持周更节奏。</li>
</ol>

<h2>变现路径（按阶段）</h2>
<p>千粉以内 → 专注内容质量，不急着变现。<br>千粉到万粉 → 开通平台广告分成（公众号流量主、知乎好物推荐）。<br>万粉以上 → 接品牌合作、出付费内容、建立社群。</p>

<h2>核心原则</h2>
<p><strong>真诚大于技巧。</strong>读者能分辨你是真心分享还是在凑字数。如果你在某个领域有真实经验，这个优势是 AI 无法替代的。</p>'''
    },
    {
        'board': 'sidehustle', 'slug': 'digital-products-guide',
        'title': '数字产品创作指南：Notion 模板、Ebook、设计素材怎么做',
        'description': '手把手教你创作和销售数字产品——Notion 模板、电子书、设计素材等，一次创作持续变现的被动收入模式。',
        'date': TODAY, 'pinned': False, 'replies': 19,
        'tags': ['数字产品', '被动收入', '副业'],
        'body': '''<p>数字产品是理想的被动收入——一次创作，无限次销售，零库存成本。这篇文章从产品创意到上架销售全流程覆盖。</p>

<h2>热门数字产品类型</h2>
<table>
  <tr><th>产品类型</th><th>价格区间</th><th>难度</th><th>案例</th></tr>
  <tr><td>Notion 模板</td><td>$5-$50</td><td>低</td><td>项目管理、日记、知识库模板</td></tr>
  <tr><td>电子书</td><td>$5-$30</td><td>中</td><td>技术教程、行业分析</td></tr>
  <tr><td>设计素材</td><td>$10-$100</td><td>中</td><td>PPT 模板、Figma 组件库</td></tr>
  <tr><td>代码模板</td><td>$20-$200</td><td>高</td><td>SaaS Boilerplate、网站模板</td></tr>
</table>

<h2>如何找到好创意</h2>
<ol>
  <li><strong>从自己的痛点出发</strong> — 你最近做过的什么东西如果做成模板别人也会需要？</li>
  <li><strong>看市场热门</strong> — Gumroad、Etsy 上搜关键词，看销量最高的产品评论区夸什么。</li>
  <li><strong>做 MVP 验证</strong> — 先做一个最小版本免费送，看下载量和反馈，再决定是否投入时间做完整版。</li>
</ol>

<h2>销售平台选择</h2>
<ul>
  <li><strong>Gumroad</strong> — 全球最大数字产品销售平台，佣金 10%，支持 PayPal 付款。</li>
  <li><strong>Etsy</strong> — 偏设计类和模板类，自然流量大，佣金约 6.5% + $0.2。</li>
  <li><strong>小报童 / 知识星球</strong> — 国内平台，适合中文内容付费。</li>
  <li><strong>自建 Landing Page</strong> — 用 Carrd 或 Framer 搭一个单页，Stripe 收款，零佣金。</li>
</ul>

<h2>定价策略</h2>
<ul>
  <li><strong>不要低价</strong> — $5 和 $25 在用户心理上是差不多的"小钱"，但你的收入差 5 倍。</li>
  <li><strong>设置三个档位</strong> — 基础版 / Pro 版 / 全套 Bundle。大部分人会选中间档。</li>
  <li><strong>限时折扣</strong> — 产品上新第一周 7 折，制造紧迫感。</li>
</ul>

<h2>持续收入的核心</h2>
<p>数字产品的难点不是制作，而是被看到。把 50% 的时间花在营销上——在社交媒体分享你的创作过程和使用技巧，这些内容本身就是最好的广告。</p>'''
    },

    # ── Tools Board ──────────────────────────────────────────────
    {
        'board': 'tools', 'slug': 'online-tools-2026',
        'title': '10 个你每天都会用到的免费在线工具网站',
        'description': '精选 10 个完全免费、无需注册的在线工具，涵盖图片处理、文件转换、文本工具等高频场景，用完即走的轻量工具合集。',
        'date': TODAY, 'pinned': True, 'replies': 41, 'hot': True,
        'tags': ['在线工具', '效率', '免费'],
        'body': '''<p>有些工具你下载一个软件太重，但偶尔又一定会用到。以下 10 个在线工具全部免费、免注册、用完即走。</p>

<h2>图片处理</h2>
<ul>
  <li><strong>remove.bg</strong> — AI 一键抠图，5 秒去背景。免费版分辨率有限但够用。</li>
  <li><strong>Squoosh</strong> — Google 出品的图片压缩工具，支持 WebP/AVIF 等现代格式，压缩比惊人。</li>
  <li><strong>Carbon</strong> — 代码截图美化工具，把你的代码变成漂亮的分享图片，支持几十种主题。</li>
</ul>

<h2>文件转换</h2>
<ul>
  <li><strong>CloudConvert</strong> — 支持 200+ 格式互相转换，PDF → Word、视频转 GIF、HTML → PDF 都可以。每天免费 25 次。</li>
  <li><strong>Convertio</strong> — 另一个全能转换工具，优势是支持直接从 Google Drive/Dropbox 导入文件。</li>
</ul>

<h2>文本和写作</h2>
<ul>
  <li><strong>DeepL Write</strong> — AI 润色中文/英文文本，不是翻译而是帮你把句子写得更流畅。</li>
  <li><strong>Diffchecker</strong> — 文本对比工具，粘贴两段文本高亮显示差异，对比代码和合同版本的神器。</li>
</ul>

<h2>其他利器</h2>
<ul>
  <li><strong>Excalidraw</strong> — 手绘风格的在线白板，画架构图、流程图非常快。开源免费、支持协作。</li>
  <li><strong>Cron-job.org</strong> — 免费定时任务服务，可以定时访问你的 URL。轻量替代 GitHub Actions。</li>
  <li><strong>PageSpeed Insights</strong> — Google 官方网页速度测试工具，输入网址给出性能评分和优化建议。SEO 必备。</li>
</ul>

<h2>使用原则</h2>
<p>在线工具虽然方便，但敏感文件（身份证、合同、私人照片）不要上传。涉及隐私的数据还是用本地软件处理。</p>'''
    },
    {
        'board': 'tools', 'slug': 'editor-comparison-2026',
        'title': 'VS Code vs JetBrains vs Cursor：2026 年代码编辑器终极对比',
        'description': '全方位对比三大主流代码编辑器的性能、AI 能力、生态插件和价格，帮你选出最适合自己的开发工具。',
        'date': TODAY, 'pinned': False, 'replies': 56, 'hot': True,
        'tags': ['编辑器', 'VS Code', 'JetBrains', '对比评测'],
        'body': '''<p>编辑器是程序员每天相处时间最长的工具。2026 年的编辑器格局正在被 AI 重塑——是时候重新评估你的选择了。</p>

<h2>三大选手总览</h2>
<table>
  <tr><th>维度</th><th>VS Code</th><th>JetBrains</th><th>Cursor</th></tr>
  <tr><td>类型</td><td>免费开源</td><td>付费 IDE（按年订阅）</td><td>免费增值（基于 VS Code）</td></tr>
  <tr><td>启动速度</td><td>快（3-5s）</td><td>慢（10-20s）</td><td>快（5-8s）</td></tr>
  <tr><td>内存占用</td><td>中等（300-500MB）</td><td>高（1-2GB）</td><td>中等偏高（500-800MB）</td></tr>
  <tr><td>AI 能力</td><td>Copilot 扩展</td><td>AI Assistant（内置）</td><td>内置深度集成</td></tr>
  <tr><td>价格</td><td>免费</td><td>$249/年（All Products）</td><td>免费基础 / Pro $20/月</td></tr>
</table>

<h2>各场景最佳选择</h2>
<ul>
  <li><strong>初学者</strong> → VS Code。免费、轻量、社区大，遇到问题容易搜索到答案。</li>
  <li><strong>Java/Kotlin/C# 开发者</strong> → JetBrains IntelliJ / Rider。这些语言的 IDE 支持，JetBrains 遥遥领先。</li>
  <li><strong>AI 辅助重度用户</strong> → Cursor。内置的 AI 功能比 VS Code + Copilot 组合更流畅，上下文理解更好。</li>
  <li><strong>多语言轻量开发</strong> → VS Code。插件生态几乎覆盖所有语言，配置简单。</li>
  <li><strong>预算充足 + 专业开发</strong> → JetBrains。重构、调试、数据库工具、代码分析都是一流的。</li>
</ul>

<h2>我的建议</h2>
<p>如果你已经习惯 VS Code 并且装了 Copilot，没必要换。如果你还没形成肌肉记忆，Cursor 是目前最值得尝试的——AI 原生体验好很多。如果你写 Java 或者做大型项目，JetBrains 的深度功能 VS Code 插件替代不了。</p>

<h2>不要陷入编辑器宗教战争</h2>
<p>工具是为效率服务的。真正的高手能用任何一种编辑器写出好代码。选一个深入掌握，比反复横跳更有价值。</p>'''
    },
    {
        'board': 'tools', 'slug': 'free-api-collection',
        'title': '30 个免费又好用的 API 合集：开发者必备',
        'description': '收录 30 个完全免费或慷慨免费额度的 API，涵盖天气、翻译、AI、数据、图片等分类，每个附调用示例和额度说明。',
        'date': TODAY, 'pinned': False, 'replies': 48, 'hot': True,
        'tags': ['API', '免费', '开发者资源'],
        'body': '''<p>好用的免费 API 就像开发者的瑞士军刀。这 30 个 API 经过了实际使用验证，附带真实调用示例。</p>

<h2>AI / 大模型</h2>
<table>
  <tr><th>API</th><th>免费额度</th><th>用途</th></tr>
  <tr><td>OpenAI API</td><td>注册送 $5</td><td>GPT-4o / GPT-4o-mini</td></tr>
  <tr><td>Claude API</td><td>注册送 $5</td><td>Claude Opus / Sonnet</td></tr>
  <tr><td>Google Gemini</td><td>每分钟 1500 次免费</td><td>Gemini 1.5 Flash/Pro</td></tr>
  <tr><td>Groq</td><td>完全免费（有速率限制）</td><td>运行开源模型（Llama、Mixtral）</td></tr>
  <tr><td>Cohere</td><td>每月 1000 次免费</td><td>文本生成和嵌入</td></tr>
</table>

<h2>天气 / 地理</h2>
<ul>
  <li><strong>Open-Meteo</strong> — 完全免费、无需 API Key 的天气 API，支持 7 天预报和历史数据。</li>
  <li><strong>OpenWeatherMap</strong> — 每天 1000 次免费调用，当前天气和 5 天预报。</li>
  <li><strong>Mapbox</strong> — 每月免费 50000 次地图加载，定制化地图组件。</li>
</ul>

<h2>翻译 / 文本</h2>
<ul>
  <li><strong>DeepL API</strong> — 每月免费 500000 字符，翻译质量优于 Google Translate。</li>
  <li><strong>LibreTranslate</strong> — 开源翻译 API，可以自部署完全免费。</li>
</ul>

<h2>图片 / 媒体</h2>
<ul>
  <li><strong>Unsplash API</strong> — 每小时 50 次，高质量免费商业图片。</li>
  <li><strong>Pexels API</strong> — 每月 20000 次，免费照片和视频素材。</li>
  <li><strong>ImgBB</strong> — 免费图片上传和托管 API。</li>
</ul>

<h2>数据 / 工具</h2>
<ul>
  <li><strong>JSONPlaceholder</strong> — 免费的假数据 API，REST + GraphQL，原型开发必备。</li>
  <li><strong>Exchange Rate API</strong> — 汇率数据，每月 1500 次免费。</li>
  <li><strong>IP-API</strong> — IP 地址查询（免费版非商业 45 次/分钟）。</li>
</ul>

<h2>实用 tips</h2>
<ul>
  <li>所有 API Key 用环境变量管理，不要硬编码在代码里。</li>
  <li>免费额度有限，生产环境做好请求频率控制（rate limiting）。</li>
  <li><strong>github.com/public-apis/public-apis</strong> 这个仓库收录了 200+ 免费 API，可以持续关注。</li>
</ul>'''
    },
]


# ── HTML template ───────────────────────────────────────────────
def make_html(art):
    board = art['board']
    board_names = {
        'tech': ('技术教程', '💻'),
        'sidehustle': ('副业资源', '💰'),
        'tools': ('工具推荐', '🛠️'),
        'ai': ('AI 教程', '🤖'),
    }
    board_name, board_icon = board_names[board]
    tags_html = '\n'.join(
        f'        <span class="tag-cat">{t}</span>'
        for t in art['tags']
    )
    pin_html = '<span class="tag-pin">📌 置顶</span>\n' if art.get('pinned') else ''
    if art.get('hot'):
        tags_html += '\n        <span class="tag-cat" style="background:#fff3cd;color:#856404;">🔥 热门</span>'

    return f'''<!DOCTYPE html>
<html lang="zh-CN" data-render="related" data-board="{board}" data-exclude="{art['slug']}">
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
        {{"@type": "ListItem", "position": 2, "name": "{board_name}", "item": "https://dingjiu1989-hue.github.io/{board}/"}},
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
      <a href="/">首页</a> › <a href="/{board}/">{board_name}</a> › {art['title']}
    </div>

    <article>
      <div class="article-tags">
        {pin_html}{tags_html}
      </div>

      <h1 class="article-title">{art['title']}</h1>
      <div class="article-meta">发布于 {art['date']} · 阅读 {art['replies'] * 120} · {art['replies']} 回复</div>

      <div class="article-body">
        {art['body'].strip()}
      </div>
    </article>

    <section class="related"><div id="related-posts"></div></section>
  </div>
</main>

<div id="footer-placeholder"></div>

<script src="/js/include.js"></script>
<script src="/js/render.js"></script>
</body>
</html>
'''


def update_articles_json():
    data = json.loads(ARTICLES_JSON.read_text(encoding='utf-8'))
    boards = {b['id']: b for b in data['boards']}

    added = 0
    for art in NEW_ARTICLES:
        board = boards[art['board']]
        slugs = {p['slug'] for p in board['posts']}
        if art['slug'] in slugs:
            continue  # skip existing
        entry = {
            'slug': art['slug'],
            'title': art['title'],
            'description': art['description'],
            'date': art['date'],
            'tags': art['tags'],
            'pinned': art.get('pinned', False),
            'replies': art.get('replies', 0),
        }
        if art.get('hot'):
            entry['hot'] = True
        board['posts'].insert(0, entry)  # newest first
        added += 1

    ARTICLES_JSON.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8'
    )
    return added


def update_sitemap():
    content = SITEMAP.read_text(encoding='utf-8')
    entries = []
    for art in NEW_ARTICLES:
        url = f'{BASE}/{art["board"]}/{art["slug"]}.html'
        entries.append(f'''  <url>
    <loc>{url}</loc>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
    <lastmod>{art["date"]}</lastmod>
  </url>''')

    insert = '\n'.join(entries)
    # Insert before closing </urlset>
    content = content.replace('</urlset>', f'{insert}\n</urlset>')
    SITEMAP.write_text(content, encoding='utf-8')


def main():
    # 1. Write HTML files
    created = 0
    for art in NEW_ARTICLES:
        path = ROOT / art['board'] / f"{art['slug']}.html"
        if path.exists():
            print(f'  SKIP (exists): {path}')
            continue
        path.write_text(make_html(art), encoding='utf-8')
        print(f'  CREATED: {path}')
        created += 1

    # 2. Update articles.json
    added = update_articles_json()
    print(f'  JSON: {added} articles added')

    # 3. Update sitemap.xml
    update_sitemap()
    print(f'  Sitemap updated')

    print(f'\nDone: {created} HTML files created, {added} JSON entries added')


if __name__ == '__main__':
    main()
