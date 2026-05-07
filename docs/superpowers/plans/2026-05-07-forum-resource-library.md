# 论坛风格AI自习室 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把现有 GitHub Pages 单页改造成三层论坛风格AI自习室（首页+分类页+详情页），3 个版块各 2 篇填充文章

**Architecture:** 纯静态 HTML/CSS，共享 CSS 文件，每个页面自包含导航和页脚（inline 保证 SEO）。面包屑和文章结构化数据用 Schema.org JSON-LD

**Tech Stack:** 纯 HTML + CSS，无 JS 框架，无构建工具

---

## 文件结构（完成后）

```
/
├── index.html                    # 首页（版块卡片+最新帖子）
├── css/style.css                 # 全局样式
├── robots.txt
├── sitemap.xml
├── article-template.html         # 新文章模板（供后续复制用）
├── tech/
│   ├── index.html                # 技术教程版块列表
│   ├── git-cheatsheet.html       # 文章
│   └── macos-tools.html          # 文章
├── sidehustle/
│   ├── index.html                # 副业资源版块列表
│   ├── free-images.html          # 文章
│   └── remote-work.html          # 文章
└── tools/
    ├── index.html                # 工具推荐版块列表
    ├── chrome-plugins.html       # 文章
    └── note-apps.html            # 文章
```

---

### Task 1: 共享 CSS 样式表

**Files:**
- Create: `css/style.css`
- Modify: `index.html`（移除内联 `<style>`，改为 `<link>` 引用）

**CSS 设计要点：**
- GitHub 配色基础 (#24292f 深色, #f6f8fa 浅灰, #0969da 链接蓝)
- 论坛风格版块卡片、帖子表格、面包屑、导航栏、页脚
- 响应式：`max-width` 容器 + 手机端断点 `@media (max-width: 768px)`
- 文章正文排版：`max-width: 700px`, `line-height: 1.8`, `font-size: 1rem`

- [ ] **Step 1: 创建 css/style.css**

```css
/* === Reset & Base === */
*,
*::before,
*::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  line-height: 1.6;
  color: #24292f;
  background: #f6f8fa;
}

a { color: #0969da; text-decoration: none; }
a:hover { text-decoration: underline; }

.container { max-width: 900px; margin: 0 auto; padding: 0 1rem; }

/* === Top Nav === */
.navbar {
  background: #24292f;
  padding: 0;
  position: sticky; top: 0; z-index: 100;
}
.navbar .container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 48px;
}
.nav-logo {
  color: #fff;
  font-weight: 700;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}
.nav-logo:hover { text-decoration: none; color: #e6edf3; }
.nav-links { display: flex; gap: 1.25rem; }
.nav-links a { color: #8b949e; font-size: 0.85rem; }
.nav-links a:hover { color: #e6edf3; text-decoration: none; }
.nav-search {
  background: #484f58;
  border: none;
  color: #e6edf3;
  padding: 0.25rem 0.6rem;
  border-radius: 4px;
  font-size: 0.8rem;
  width: 140px;
}
.nav-search::placeholder { color: #8b949e; }

/* === Hero === */
.hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2.5rem 1rem;
  color: #fff;
  margin-bottom: 1.5rem;
}
.hero .container { max-width: 900px; }
.hero h1 { font-size: 1.5rem; margin-bottom: 0.4rem; }
.hero p { opacity: 0.9; font-size: 0.95rem; margin-bottom: 1rem; }
.hero-stats { display: flex; gap: 1rem; }
.hero-stat {
  background: rgba(255,255,255,0.2);
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
}

/* === Stats Bar === */
.stats-bar {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  font-size: 0.8rem;
  color: #656d76;
}

/* === Board Card === */
.board {
  border: 1px solid #d0d7de;
  border-radius: 8px;
  margin-bottom: 1.25rem;
  overflow: hidden;
  background: #fff;
}
.board-header {
  background: #f6f8fa;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #d0d7de;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.board-header .board-icon { font-size: 1.1rem; }
.board-header .board-name { font-weight: 700; font-size: 0.95rem; }
.board-header .board-desc { color: #656d76; font-size: 0.8rem; margin-left: 0.25rem; }
.board-header .board-count {
  margin-left: auto;
  color: #656d76;
  font-size: 0.75rem;
  white-space: nowrap;
}

/* === Post Row === */
.post-row {
  display: flex;
  align-items: center;
  padding: 0.65rem 1rem;
  border-bottom: 1px solid #f0f0f0;
  font-size: 0.88rem;
}
.post-row:last-child { border-bottom: none; }
.post-pin { width: 2rem; font-size: 0.75rem; flex-shrink: 0; }
.post-pin.pinned { color: #d73a49; }
.post-pin.hot { color: #d73a49; }
.post-title { flex: 1; }
.post-title a { color: #0969da; }
.post-replies { width: 4rem; text-align: center; color: #656d76; font-size: 0.8rem; flex-shrink: 0; }
.post-date { width: 3.5rem; text-align: right; color: #656d76; font-size: 0.75rem; flex-shrink: 0; }

/* === Category Page === */
.breadcrumb {
  font-size: 0.8rem;
  color: #656d76;
  margin-bottom: 1rem;
  padding-top: 1rem;
}
.breadcrumb a { color: #0969da; }

.page-header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 1.25rem;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.page-header h2 { font-size: 1.3rem; display: flex; align-items: center; gap: 0.5rem; }
.page-header .post-count { color: #656d76; font-size: 0.85rem; }

.sort-select {
  background: #f6f8fa;
  border: 1px solid #d0d7de;
  padding: 0.35rem 0.6rem;
  border-radius: 6px;
  font-size: 0.8rem;
  color: #24292f;
}

/* === Post Table (Category Page) === */
.post-table {
  border: 1px solid #d0d7de;
  border-radius: 8px;
  overflow: hidden;
  background: #fff;
}
.post-table-header {
  background: #f6f8fa;
  padding: 0.5rem 1rem;
  border-bottom: 1px solid #d0d7de;
  display: flex;
  font-size: 0.75rem;
  color: #656d76;
  font-weight: 600;
}
.post-table-header .col-pin { width: 3rem; flex-shrink: 0; }
.post-table-header .col-title { flex: 1; }
.post-table-header .col-replies { width: 5rem; text-align: center; flex-shrink: 0; }
.post-table-header .col-date { width: 5rem; text-align: right; flex-shrink: 0; }
.post-table .post-row .col-pin { width: 3rem; font-size: 0.75rem; flex-shrink: 0; }
.post-table .post-row .col-title { flex: 1; }
.post-table .post-row .col-replies { width: 5rem; text-align: center; color: #656d76; font-size: 0.8rem; flex-shrink: 0; }
.post-table .post-row .col-date { width: 5rem; text-align: right; color: #656d76; font-size: 0.75rem; flex-shrink: 0; }

/* === Article Detail === */
.article-container { max-width: 750px; }

.article-tags { margin-bottom: 0.75rem; display: flex; gap: 0.4rem; flex-wrap: wrap; }
.tag-pin {
  background: #ddf4ff;
  color: #0969da;
  padding: 0.15rem 0.6rem;
  border-radius: 12px;
  font-size: 0.75rem;
}
.tag-cat {
  background: #f6f8fa;
  color: #656d76;
  padding: 0.15rem 0.6rem;
  border-radius: 12px;
  font-size: 0.75rem;
}

.article-title { font-size: 1.5rem; margin: 0.75rem 0 0.4rem; }
.article-meta { color: #656d76; font-size: 0.8rem; margin-bottom: 2rem; }

.article-body {
  line-height: 1.8;
  font-size: 1rem;
}
.article-body h2 { font-size: 1.2rem; margin: 2rem 0 0.75rem; }
.article-body h3 { font-size: 1.05rem; margin: 1.5rem 0 0.5rem; }
.article-body p { margin-bottom: 1rem; }
.article-body ul, .article-body ol { margin-bottom: 1rem; padding-left: 1.5rem; }
.article-body li { margin-bottom: 0.4rem; }
.article-body code {
  background: #f6f8fa;
  padding: 0.15em 0.4em;
  border-radius: 3px;
  font-size: 0.9em;
}
.article-body pre {
  background: #1b1f23;
  color: #e6edf3;
  padding: 1rem;
  border-radius: 6px;
  overflow-x: auto;
  font-size: 0.85rem;
  margin-bottom: 1rem;
}
.article-body table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1rem;
}
.article-body th, .article-body td {
  border: 1px solid #d0d7de;
  padding: 0.5rem 0.75rem;
  text-align: left;
  font-size: 0.9rem;
}
.article-body th { background: #f6f8fa; font-weight: 600; }

/* === Related Posts === */
.related {
  margin-top: 2.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #d0d7de;
}
.related h3 { font-size: 1rem; margin-bottom: 0.75rem; }
.related-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}
.related-card {
  display: block;
  padding: 0.75rem 1rem;
  border: 1px solid #d0d7de;
  border-radius: 6px;
  color: #0969da;
  font-size: 0.88rem;
}
.related-card:hover { background: #f6f8fa; text-decoration: none; }

/* === Footer === */
.footer {
  text-align: center;
  padding: 2.5rem 1rem;
  color: #656d76;
  font-size: 0.8rem;
  margin-top: 2rem;
  border-top: 1px solid #d0d7de;
}
.footer p { margin-bottom: 0.3rem; }

/* === Responsive === */
@media (max-width: 768px) {
  .hero { padding: 1.5rem 1rem; }
  .hero h1 { font-size: 1.2rem; }
  .nav-links { display: none; }
  .nav-search { width: 100px; }
  .post-row { font-size: 0.82rem; }
  .post-replies, .post-date { width: auto; }
  .related-grid { grid-template-columns: 1fr; }
  .article-title { font-size: 1.2rem; }
  .board-header { flex-wrap: wrap; }
  .board-header .board-desc { display: none; }
}
```

- [ ] **Step 2: 更新 index.html 的样式引用**

把 `index.html` 中 `<style>...</style>` 块替换为 `<link rel="stylesheet" href="css/style.css">`，移除内联样式块。

修改 `<head>` 部分（删除 `<style>` 到 `</style>` 即当前第 5-70 行，替换为）:

```html
    <link rel="stylesheet" href="css/style.css">
```

- [ ] **Step 3: 提交**

```bash
git add css/style.css index.html
git commit -m "feat: extract shared CSS, add forum-style base styles"
```

---

### Task 2: robots.txt 和 sitemap.xml

**Files:**
- Create: `robots.txt`
- Create: `sitemap.xml`

- [ ] **Step 1: 创建 robots.txt**

```txt
User-agent: *
Allow: /
Sitemap: https://dingjiu1989-hue.github.io/sitemap.xml
```

- [ ] **Step 2: 创建 sitemap.xml**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://dingjiu1989-hue.github.io/</loc>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://dingjiu1989-hue.github.io/tech/</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://dingjiu1989-hue.github.io/sidehustle/</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://dingjiu1989-hue.github.io/tools/</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://dingjiu1989-hue.github.io/tech/git-cheatsheet.html</loc>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
  <url>
    <loc>https://dingjiu1989-hue.github.io/tech/macos-tools.html</loc>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
  <url>
    <loc>https://dingjiu1989-hue.github.io/sidehustle/free-images.html</loc>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
  <url>
    <loc>https://dingjiu1989-hue.github.io/sidehustle/remote-work.html</loc>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
  <url>
    <loc>https://dingjiu1989-hue.github.io/tools/chrome-plugins.html</loc>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
  <url>
    <loc>https://dingjiu1989-hue.github.io/tools/note-apps.html</loc>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
</urlset>
```

- [ ] **Step 3: 提交**

```bash
git add robots.txt sitemap.xml
git commit -m "feat: add robots.txt and sitemap.xml for SEO"
```

---

### Task 3: 首页 — 论坛式版块列表

**Files:**
- Rewrite: `index.html`

首页结构：
1. 顶部导航栏（logo + 链接 + 搜索框）
2. Hero 区域（站名 + 简介 + 统计徽章）
3. 统计条（今日/昨日/总帖数 — 手写静态数字）
4. 3 个版块卡片，每个卡片内含 2-3 条最新帖子
5. 页脚

- [ ] **Step 1: 重写 index.html**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI自习室 — 聚合优质资源，分享实用知识</title>
    <meta name="description" content="论坛风格AI自习室，聚合技术教程、副业资源、工具推荐等优质内容。">
    <link rel="stylesheet" href="css/style.css">
    <!-- Schema.org WebSite -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "AI自习室",
      "url": "https://dingjiu1989-hue.github.io/",
      "description": "聚合优质资源，分享实用知识"
    }
    </script>
</head>
<body>

<!-- Top Nav -->
<nav class="navbar">
  <div class="container">
    <a href="/" class="nav-logo">📚 AI自习室</a>
    <div class="nav-links">
      <a href="/">首页</a>
      <a href="/tech/">技术教程</a>
      <a href="/sidehustle/">副业资源</a>
      <a href="/tools/">工具推荐</a>
    </div>
    <input class="nav-search" type="search" placeholder="搜索..." disabled title="搜索功能开发中">
  </div>
</nav>

<main>
  <!-- Hero -->
  <section class="hero">
    <div class="container">
      <h1>📚 欢迎来到AI自习室</h1>
      <p>聚合优质资源，分享实用知识</p>
      <div class="hero-stats">
        <span class="hero-stat">📂 3 个版块</span>
        <span class="hero-stat">📝 6 篇文章</span>
      </div>
    </div>
  </section>

  <div class="container">
    <!-- Stats Bar -->
    <div class="stats-bar">
      <span>🔥 今日: 3 篇新帖</span>
      <span>📅 昨日: 12 篇</span>
      <span>📊 总帖数: 6</span>
    </div>

    <!-- 版块 1: 技术教程 -->
    <div class="board">
      <div class="board-header">
        <span class="board-icon">💻</span>
        <span class="board-name">技术教程</span>
        <span class="board-desc">编程 · 工具 · 效率</span>
        <span class="board-count">共 2 帖</span>
      </div>
      <a href="/tech/git-cheatsheet.html" class="post-row">
        <span class="post-pin pinned">📌</span>
        <span class="post-title">Git 常用命令速查表</span>
        <span class="post-replies">4 回复</span>
        <span class="post-date">05-07</span>
      </a>
      <a href="/tech/macos-tools.html" class="post-row">
        <span class="post-pin"></span>
        <span class="post-title">macOS 效率工具推荐合集</span>
        <span class="post-replies">12 回复</span>
        <span class="post-date">05-06</span>
      </a>
    </div>

    <!-- 版块 2: 副业资源 -->
    <div class="board">
      <div class="board-header">
        <span class="board-icon">💰</span>
        <span class="board-name">副业资源</span>
        <span class="board-desc">工具 · 平台 · 经验</span>
        <span class="board-count">共 2 帖</span>
      </div>
      <a href="/sidehustle/free-images.html" class="post-row">
        <span class="post-pin pinned">📌</span>
        <span class="post-title">免费可商用图片资源汇总</span>
        <span class="post-replies">8 回复</span>
        <span class="post-date">05-03</span>
      </a>
      <a href="/sidehustle/remote-work.html" class="post-row">
        <span class="post-pin"></span>
        <span class="post-title">远程工作平台大盘点</span>
        <span class="post-replies">6 回复</span>
        <span class="post-date">04-28</span>
      </a>
    </div>

    <!-- 版块 3: 工具推荐 -->
    <div class="board">
      <div class="board-header">
        <span class="board-icon">🛠️</span>
        <span class="board-name">工具推荐</span>
        <span class="board-desc">效率 · 设计 · 开发</span>
        <span class="board-count">共 2 帖</span>
      </div>
      <a href="/tools/chrome-plugins.html" class="post-row">
        <span class="post-pin hot">🔥</span>
        <span class="post-title">2025 年度必备 Chrome 插件推荐</span>
        <span class="post-replies">35 回复</span>
        <span class="post-date">04-15</span>
      </a>
      <a href="/tools/note-apps.html" class="post-row">
        <span class="post-pin"></span>
        <span class="post-title">白板/笔记/思维导图工具对比</span>
        <span class="post-replies">9 回复</span>
        <span class="post-date">04-10</span>
      </a>
    </div>
  </div>
</main>

<footer class="footer">
  <p>📚 AI自习室 &copy; 2026</p>
  <p>纯静态 · GitHub Pages 托管 · 内容仅供学习交流</p>
  <p style="margin-top:0.5rem;">
    <a href="/sitemap.xml">站点地图</a> ·
    <a href="https://github.com/dingjiu1989-hue/dingjiu1989-hue.github.io">GitHub</a>
  </p>
</footer>

</body>
</html>
```

- [ ] **Step 2: 在浏览器预览**

```bash
open /Users/daniel/gh-pages-demo/index.html
```

检查：导航栏、Hero、3 个版块卡片、帖子行、页脚均正确显示

- [ ] **Step 3: 提交**

```bash
git add index.html
git commit -m "feat: forum-style homepage with board cards and post lists"
```

---

### Task 4: 分类页 — 技术教程版块

**Files:**
- Create: `tech/index.html`

分类页结构：
1. 导航栏（同首页）
2. 面包屑: 首页 > 技术教程
3. 版块标题 + 描述 + 总帖数 + 排序下拉框
4. 帖子表格（置顶 | 标题 | 回复 | 最后更新）
5. 页脚

- [ ] **Step 1: 创建 tech/index.html**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>技术教程 — AI自习室</title>
    <meta name="description" content="技术教程版块，汇集编程、开发工具、效率提升等实用教程和参考资料。">
    <link rel="stylesheet" href="/css/style.css">
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "CollectionPage",
      "name": "技术教程",
      "url": "https://dingjiu1989-hue.github.io/tech/",
      "description": "编程 · 工具 · 效率"
    }
    </script>
</head>
<body>

<nav class="navbar">
  <div class="container">
    <a href="/" class="nav-logo">📚 AI自习室</a>
    <div class="nav-links">
      <a href="/">首页</a>
      <a href="/tech/">技术教程</a>
      <a href="/sidehustle/">副业资源</a>
      <a href="/tools/">工具推荐</a>
    </div>
    <input class="nav-search" type="search" placeholder="搜索..." disabled title="搜索功能开发中">
  </div>
</nav>

<main>
  <div class="container">
    <!-- 面包屑 Schema.org -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "首页", "item": "https://dingjiu1989-hue.github.io/"},
        {"@type": "ListItem", "position": 2, "name": "技术教程", "item": "https://dingjiu1989-hue.github.io/tech/"}
      ]
    }
    </script>
    <div class="breadcrumb">
      <a href="/">首页</a> › 技术教程
    </div>

    <div class="page-header">
      <div>
        <h2>💻 技术教程</h2>
        <span class="post-count">编程 · 工具 · 效率（共 2 篇）</span>
      </div>
      <select class="sort-select" disabled>
        <option>排序：最新 ↓</option>
      </select>
    </div>

    <div class="post-table">
      <div class="post-table-header">
        <span class="col-pin">置顶</span>
        <span class="col-title">标题</span>
        <span class="col-replies">回复</span>
        <span class="col-date">更新</span>
      </div>
      <a href="/tech/git-cheatsheet.html" class="post-row">
        <span class="col-pin" style="color:#d73a49;">📌</span>
        <span class="col-title" style="font-weight:600;">Git 常用命令速查表</span>
        <span class="col-replies">4</span>
        <span class="col-date">05-07</span>
      </a>
      <a href="/tech/macos-tools.html" class="post-row">
        <span class="col-pin"></span>
        <span class="col-title">macOS 效率工具推荐合集</span>
        <span class="col-replies">12</span>
        <span class="col-date">05-06</span>
      </a>
    </div>
  </div>
</main>

<footer class="footer">
  <p>📚 AI自习室 &copy; 2026</p>
  <p>纯静态 · GitHub Pages 托管</p>
  <p style="margin-top:0.5rem;"><a href="/">返回首页</a></p>
</footer>

</body>
</html>
```

- [ ] **Step 2: 提交**

```bash
git add tech/index.html
git commit -m "feat: tech category page with post table"
```

---

### Task 5: 分类页 — 副业资源版块

**Files:**
- Create: `sidehustle/index.html`

与 Task 4 结构相同，换数据。创建 sidehustle/index.html:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>副业资源 — AI自习室</title>
    <meta name="description" content="副业资源版块，汇集免费商用资源、远程工作平台、副业经验分享等实用信息。">
    <link rel="stylesheet" href="/css/style.css">
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "CollectionPage",
      "name": "副业资源",
      "url": "https://dingjiu1989-hue.github.io/sidehustle/",
      "description": "工具 · 平台 · 经验"
    }
    </script>
</head>
<body>

<nav class="navbar">
  <div class="container">
    <a href="/" class="nav-logo">📚 AI自习室</a>
    <div class="nav-links">
      <a href="/">首页</a>
      <a href="/tech/">技术教程</a>
      <a href="/sidehustle/">副业资源</a>
      <a href="/tools/">工具推荐</a>
    </div>
    <input class="nav-search" type="search" placeholder="搜索..." disabled title="搜索功能开发中">
  </div>
</nav>

<main>
  <div class="container">
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "首页", "item": "https://dingjiu1989-hue.github.io/"},
        {"@type": "ListItem", "position": 2, "name": "副业资源", "item": "https://dingjiu1989-hue.github.io/sidehustle/"}
      ]
    }
    </script>
    <div class="breadcrumb"><a href="/">首页</a> › 副业资源</div>

    <div class="page-header">
      <div>
        <h2>💰 副业资源</h2>
        <span class="post-count">工具 · 平台 · 经验（共 2 篇）</span>
      </div>
      <select class="sort-select" disabled><option>排序：最新 ↓</option></select>
    </div>

    <div class="post-table">
      <div class="post-table-header">
        <span class="col-pin">置顶</span>
        <span class="col-title">标题</span>
        <span class="col-replies">回复</span>
        <span class="col-date">更新</span>
      </div>
      <a href="/sidehustle/free-images.html" class="post-row">
        <span class="col-pin" style="color:#d73a49;">📌</span>
        <span class="col-title" style="font-weight:600;">免费可商用图片资源汇总</span>
        <span class="col-replies">8</span>
        <span class="col-date">05-03</span>
      </a>
      <a href="/sidehustle/remote-work.html" class="post-row">
        <span class="col-pin"></span>
        <span class="col-title">远程工作平台大盘点</span>
        <span class="col-replies">6</span>
        <span class="col-date">04-28</span>
      </a>
    </div>
  </div>
</main>

<footer class="footer">
  <p>📚 AI自习室 &copy; 2026</p>
  <p>纯静态 · GitHub Pages 托管</p>
  <p style="margin-top:0.5rem;"><a href="/">返回首页</a></p>
</footer>

</body>
</html>
```

- [ ] **Step 1: 提交**

```bash
git add sidehustle/index.html
git commit -m "feat: sidehustle category page"
```

---

### Task 6: 分类页 — 工具推荐版块

**Files:**
- Create: `tools/index.html`

与 Tasks 4-5 结构相同，换数据。创建 tools/index.html:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>工具推荐 — AI自习室</title>
    <meta name="description" content="工具推荐版块，汇集效率工具、设计资源、开发辅助等实用软件和在线服务推荐。">
    <link rel="stylesheet" href="/css/style.css">
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "CollectionPage",
      "name": "工具推荐",
      "url": "https://dingjiu1989-hue.github.io/tools/",
      "description": "效率 · 设计 · 开发"
    }
    </script>
</head>
<body>

<nav class="navbar">
  <div class="container">
    <a href="/" class="nav-logo">📚 AI自习室</a>
    <div class="nav-links">
      <a href="/">首页</a>
      <a href="/tech/">技术教程</a>
      <a href="/sidehustle/">副业资源</a>
      <a href="/tools/">工具推荐</a>
    </div>
    <input class="nav-search" type="search" placeholder="搜索..." disabled title="搜索功能开发中">
  </div>
</nav>

<main>
  <div class="container">
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "首页", "item": "https://dingjiu1989-hue.github.io/"},
        {"@type": "ListItem", "position": 2, "name": "工具推荐", "item": "https://dingjiu1989-hue.github.io/tools/"}
      ]
    }
    </script>
    <div class="breadcrumb"><a href="/">首页</a> › 工具推荐</div>

    <div class="page-header">
      <div>
        <h2>🛠️ 工具推荐</h2>
        <span class="post-count">效率 · 设计 · 开发（共 2 篇）</span>
      </div>
      <select class="sort-select" disabled><option>排序：最新 ↓</option></select>
    </div>

    <div class="post-table">
      <div class="post-table-header">
        <span class="col-pin">置顶</span>
        <span class="col-title">标题</span>
        <span class="col-replies">回复</span>
        <span class="col-date">更新</span>
      </div>
      <a href="/tools/chrome-plugins.html" class="post-row">
        <span class="col-pin" style="color:#d73a49;">🔥</span>
        <span class="col-title" style="font-weight:600;">2025 年度必备 Chrome 插件推荐</span>
        <span class="col-replies">35</span>
        <span class="col-date">04-15</span>
      </a>
      <a href="/tools/note-apps.html" class="post-row">
        <span class="col-pin"></span>
        <span class="col-title">白板/笔记/思维导图工具对比</span>
        <span class="col-replies">9</span>
        <span class="col-date">04-10</span>
      </a>
    </div>
  </div>
</main>

<footer class="footer">
  <p>📚 AI自习室 &copy; 2026</p>
  <p>纯静态 · GitHub Pages 托管</p>
  <p style="margin-top:0.5rem;"><a href="/">返回首页</a></p>
</footer>

</body>
</html>
```

- [ ] **Step 1: 提交**

```bash
git add tools/index.html
git commit -m "feat: tools category page"
```

---

### Task 7: 创建文章模板

**Files:**
- Create: `article-template.html`

一个可供未来复制用的空白文章模板，包含完整的导航、面包屑、结构化数据、相关推荐占位。

- [ ] **Step 1: 创建 article-template.html**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文章标题 — AI自习室</title>
    <meta name="description" content="文章摘要，150字以内，用于搜索引擎结果展示。">
    <link rel="stylesheet" href="/css/style.css">
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "文章标题",
      "description": "文章摘要",
      "datePublished": "2026-05-07",
      "dateModified": "2026-05-07",
      "author": {"@type": "Person", "name": "AI自习室"}
    }
    </script>
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "首页", "item": "https://dingjiu1989-hue.github.io/"},
        {"@type": "ListItem", "position": 2, "name": "分类名", "item": "https://dingjiu1989-hue.github.io/分类目录/"},
        {"@type": "ListItem", "position": 3, "name": "文章标题"}
      ]
    }
    </script>
</head>
<body>

<nav class="navbar">
  <div class="container">
    <a href="/" class="nav-logo">📚 AI自习室</a>
    <div class="nav-links">
      <a href="/">首页</a>
      <a href="/tech/">技术教程</a>
      <a href="/sidehustle/">副业资源</a>
      <a href="/tools/">工具推荐</a>
    </div>
    <input class="nav-search" type="search" placeholder="搜索..." disabled title="搜索功能开发中">
  </div>
</nav>

<main>
  <div class="container article-container">
    <div class="breadcrumb">
      <a href="/">首页</a> › <a href="/分类目录/">分类名</a> › 文章标题
    </div>

    <article>
      <div class="article-tags">
        <span class="tag-pin">📌 置顶</span>
        <span class="tag-cat">分类标签</span>
      </div>

      <h1 class="article-title">文章标题</h1>
      <div class="article-meta">发布于 2026-05-07 · 阅读 100 · 0 回复</div>

      <div class="article-body">
        <!-- 文章正文 -->
      </div>
    </article>

    <section class="related">
      <h3>相关文章</h3>
      <div class="related-grid">
        <a href="#" class="related-card">相关文章 1</a>
        <a href="#" class="related-card">相关文章 2</a>
      </div>
    </section>
  </div>
</main>

<footer class="footer">
  <p>📚 AI自习室 &copy; 2026</p>
  <p>纯静态 · GitHub Pages 托管</p>
  <p style="margin-top:0.5rem;"><a href="/">返回首页</a></p>
</footer>

</body>
</html>
```

- [ ] **Step 2: 提交**

```bash
git add article-template.html
git commit -m "feat: article template for future use"
```

---

### Task 8: 6 篇填充文章（批量）

**Files:**
- Create: `tech/git-cheatsheet.html`
- Create: `tech/macos-tools.html`
- Create: `sidehustle/free-images.html`
- Create: `sidehustle/remote-work.html`
- Create: `tools/chrome-plugins.html`
- Create: `tools/note-apps.html`

每篇文章基于模板，替换标题、简介、面包屑、分类标签、相关推荐链接、正文内容。正文为 300-800 字的实用内容，包含标题、列表、表格等富文本。

- [ ] **Step 1: 创建 tech/git-cheatsheet.html**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Git 常用命令速查表 — AI自习室</title>
    <meta name="description" content="Git 常用命令速查，涵盖分支管理、撤销操作、暂存与提交、远程协作等核心场景，快速查找即用。">
    <link rel="stylesheet" href="/css/style.css">
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "Git 常用命令速查表",
      "description": "Git 常用命令速查，涵盖分支管理、撤销操作、暂存与提交、远程协作等核心场景。",
      "datePublished": "2026-05-07",
      "dateModified": "2026-05-07",
      "author": {"@type": "Person", "name": "AI自习室"}
    }
    </script>
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "首页", "item": "https://dingjiu1989-hue.github.io/"},
        {"@type": "ListItem", "position": 2, "name": "技术教程", "item": "https://dingjiu1989-hue.github.io/tech/"},
        {"@type": "ListItem", "position": 3, "name": "Git 常用命令速查表"}
      ]
    }
    </script>
</head>
<body>

<nav class="navbar">
  <div class="container">
    <a href="/" class="nav-logo">📚 AI自习室</a>
    <div class="nav-links">
      <a href="/">首页</a>
      <a href="/tech/">技术教程</a>
      <a href="/sidehustle/">副业资源</a>
      <a href="/tools/">工具推荐</a>
    </div>
    <input class="nav-search" type="search" placeholder="搜索..." disabled title="搜索功能开发中">
  </div>
</nav>

<main>
  <div class="container article-container">
    <div class="breadcrumb">
      <a href="/">首页</a> › <a href="/tech/">技术教程</a> › Git 常用命令速查表
    </div>

    <article>
      <div class="article-tags">
        <span class="tag-pin">📌 置顶</span>
        <span class="tag-cat">Git</span>
        <span class="tag-cat">命令行</span>
      </div>

      <h1 class="article-title">Git 常用命令速查表</h1>
      <div class="article-meta">发布于 2026-05-07 · 阅读 1.2k · 4 回复</div>

      <div class="article-body">
        <p>日常开发中 Git 是最常用的版本控制工具。这里整理了高频命令，按场景分类，方便速查。</p>

        <h2>分支管理</h2>
        <table>
          <tr><th>命令</th><th>说明</th></tr>
          <tr><td><code>git branch</code></td><td>查看本地分支</td></tr>
          <tr><td><code>git branch -r</code></td><td>查看远程分支</td></tr>
          <tr><td><code>git branch &lt;name&gt;</code></td><td>创建新分支</td></tr>
          <tr><td><code>git checkout &lt;name&gt;</code></td><td>切换分支</td></tr>
          <tr><td><code>git checkout -b &lt;name&gt;</code></td><td>创建并切换到新分支</td></tr>
          <tr><td><code>git merge &lt;branch&gt;</code></td><td>合并指定分支到当前分支</td></tr>
          <tr><td><code>git branch -d &lt;name&gt;</code></td><td>删除本地分支</td></tr>
          <tr><td><code>git push origin --delete &lt;name&gt;</code></td><td>删除远程分支</td></tr>
        </table>

        <h2>暂存与提交</h2>
        <table>
          <tr><th>命令</th><th>说明</th></tr>
          <tr><td><code>git status</code></td><td>查看工作区状态</td></tr>
          <tr><td><code>git add &lt;file&gt;</code></td><td>添加文件到暂存区</td></tr>
          <tr><td><code>git add .</code></td><td>添加所有更改到暂存区</td></tr>
          <tr><td><code>git commit -m "msg"</code></td><td>提交暂存区内容</td></tr>
          <tr><td><code>git commit --amend</code></td><td>修改上一次提交</td></tr>
        </table>

        <h2>撤销操作</h2>
        <table>
          <tr><th>命令</th><th>说明</th></tr>
          <tr><td><code>git restore &lt;file&gt;</code></td><td>撤销工作区修改</td></tr>
          <tr><td><code>git restore --staged &lt;file&gt;</code></td><td>取消暂存</td></tr>
          <tr><td><code>git reset --soft HEAD~1</code></td><td>撤销上次 commit，保留修改</td></tr>
          <tr><td><code>git reset --hard HEAD~1</code></td><td>撤销上次 commit，丢弃修改</td></tr>
          <tr><td><code>git revert &lt;commit&gt;</code></td><td>安全撤销某次提交（生成新 commit）</td></tr>
        </table>

        <h2>远程协作</h2>
        <table>
          <tr><th>命令</th><th>说明</th></tr>
          <tr><td><code>git remote -v</code></td><td>查看远程仓库地址</td></tr>
          <tr><td><code>git push</code></td><td>推送当前分支到远程</td></tr>
          <tr><td><code>git pull</code></td><td>拉取远程更新并合并</td></tr>
          <tr><td><code>git fetch</code></td><td>拉取远程更新但不合并</td></tr>
          <tr><td><code>git clone &lt;url&gt;</code></td><td>克隆远程仓库</td></tr>
        </table>

        <h2>日志与历史</h2>
        <table>
          <tr><th>命令</th><th>说明</th></tr>
          <tr><td><code>git log --oneline</code></td><td>查看简洁提交历史</td></tr>
          <tr><td><code>git log --graph --oneline</code></td><td>查看分支图</td></tr>
          <tr><td><code>git diff</code></td><td>查看未暂存的修改</td></tr>
          <tr><td><code>git diff --staged</code></td><td>查看已暂存的修改</td></tr>
        </table>

        <h2>储藏 (Stash)</h2>
        <table>
          <tr><th>命令</th><th>说明</th></tr>
          <tr><td><code>git stash</code></td><td>暂存当前修改到储藏栈</td></tr>
          <tr><td><code>git stash pop</code></td><td>恢复最近一次储藏并删除</td></tr>
          <tr><td><code>git stash list</code></td><td>查看储藏列表</td></tr>
          <tr><td><code>git stash drop</code></td><td>删除最近一次储藏</td></tr>
        </table>
      </div>
    </article>

    <section class="related">
      <h3>相关文章</h3>
      <div class="related-grid">
        <a href="/tech/macos-tools.html" class="related-card">macOS 效率工具推荐合集</a>
      </div>
    </section>
  </div>
</main>

<footer class="footer">
  <p>📚 AI自习室 &copy; 2026</p>
  <p>纯静态 · GitHub Pages 托管</p>
  <p style="margin-top:0.5rem;"><a href="/">返回首页</a></p>
</footer>

</body>
</html>
```

- [ ] **Step 2: 创建 tech/macos-tools.html**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>macOS 效率工具推荐合集 — AI自习室</title>
    <meta name="description" content="精选 macOS 效率工具推荐，涵盖启动器、窗口管理、剪贴板、截图、终端等必备软件，提升日常工作效率。">
    <link rel="stylesheet" href="/css/style.css">
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "macOS 效率工具推荐合集",
      "description": "精选 macOS 效率工具推荐，涵盖启动器、窗口管理、剪贴板、截图、终端等必备软件。",
      "datePublished": "2026-05-06",
      "dateModified": "2026-05-06",
      "author": {"@type": "Person", "name": "AI自习室"}
    }
    </script>
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "首页", "item": "https://dingjiu1989-hue.github.io/"},
        {"@type": "ListItem", "position": 2, "name": "技术教程", "item": "https://dingjiu1989-hue.github.io/tech/"},
        {"@type": "ListItem", "position": 3, "name": "macOS 效率工具推荐合集"}
      ]
    }
    </script>
</head>
<body>

<nav class="navbar">
  <div class="container">
    <a href="/" class="nav-logo">📚 AI自习室</a>
    <div class="nav-links">
      <a href="/">首页</a>
      <a href="/tech/">技术教程</a>
      <a href="/sidehustle/">副业资源</a>
      <a href="/tools/">工具推荐</a>
    </div>
    <input class="nav-search" type="search" placeholder="搜索..." disabled title="搜索功能开发中">
  </div>
</nav>

<main>
  <div class="container article-container">
    <div class="breadcrumb">
      <a href="/">首页</a> › <a href="/tech/">技术教程</a> › macOS 效率工具推荐合集
    </div>

    <article>
      <div class="article-tags">
        <span class="tag-cat">macOS</span>
        <span class="tag-cat">效率工具</span>
      </div>

      <h1 class="article-title">macOS 效率工具推荐合集</h1>
      <div class="article-meta">发布于 2026-05-06 · 阅读 890 · 12 回复</div>

      <div class="article-body">
        <p>一套好用的工具能让 Mac 工作效率翻倍。这里整理了我长期使用后筛选出的精品工具，涵盖各个高频场景。</p>

        <h2>启动器与搜索</h2>
        <ul>
          <li><strong>Raycast</strong> — 免费且功能强大的启动器，替代 Spotlight。支持剪贴板历史、窗口管理、快捷搜索、插件扩展。比 Alfred 更现代，社区生态活跃。</li>
          <li><strong>Alfred</strong> — 老牌启动器，Powerpack 付费后可自定义 Workflow。功能深度够，但界面略显老旧。</li>
        </ul>

        <h2>窗口管理</h2>
        <ul>
          <li><strong>Rectangle</strong> — 开源免费，快捷键快速分屏。支持左右半屏、四分之一屏、全屏等布局。</li>
          <li><strong>Magnet</strong> — 付费（$8），拖拽窗口到边缘自动吸附分屏，操作直觉化。</li>
        </ul>

        <h2>剪贴板管理</h2>
        <ul>
          <li><strong>Maccy</strong> — 开源免费，轻量级剪贴板管理器。菜单栏快捷访问，支持纯文本粘贴。</li>
          <li><strong>Paste</strong> — 付费订阅，可视化剪贴板界面华丽，适合设计类工作。</li>
        </ul>

        <h2>截图与录屏</h2>
        <ul>
          <li><strong>CleanShot X</strong> — 付费（$29 一次性），截图标注、滚动截图、录屏、OCR 文字识别。功能最全。</li>
          <li><strong>Shottr</strong> — 免费（基础功能），轻量截图工具，支持像素级放大镜和取色器。</li>
        </ul>

        <h2>终端工具</h2>
        <ul>
          <li><strong>iTerm2</strong> — 老牌终端增强，分屏、热键窗口、Shell Integration。</li>
          <li><strong>Warp</strong> — 现代化的 Rust 终端，AI 辅助命令，团队协作功能。</li>
          <li><strong>Homebrew</strong> — macOS 必不可少的包管理器。<code>brew install &lt;package&gt;</code> 搞定一切。</li>
        </ul>

        <h2>其他精品</h2>
        <ul>
          <li><strong>IINA</strong> — 开源视频播放器，界面优雅，支持所有格式。</li>
          <li><strong>Keka</strong> — 免费解压工具，支持 7z、RAR、ZIP 等格式。</li>
          <li><strong>AppCleaner</strong> — 彻底卸载应用并清理残留文件。</li>
        </ul>
      </div>
    </article>

    <section class="related">
      <h3>相关文章</h3>
      <div class="related-grid">
        <a href="/tech/git-cheatsheet.html" class="related-card">Git 常用命令速查表</a>
      </div>
    </section>
  </div>
</main>

<footer class="footer">
  <p>📚 AI自习室 &copy; 2026</p>
  <p>纯静态 · GitHub Pages 托管</p>
  <p style="margin-top:0.5rem;"><a href="/">返回首页</a></p>
</footer>

</body>
</html>
```

- [ ] **Step 3: 创建 sidehustle/free-images.html**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>免费可商用图片资源汇总 — AI自习室</title>
    <meta name="description" content="盘点 10+ 免费可商用的高质量图片资源网站，包括 Unsplash、Pexels、Pixabay 等，设计师和运营必备。">
    <link rel="stylesheet" href="/css/style.css">
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "免费可商用图片资源汇总",
      "description": "盘点 10+ 免费可商用的高质量图片资源网站，设计师和运营必备。",
      "datePublished": "2026-05-03",
      "dateModified": "2026-05-03",
      "author": {"@type": "Person", "name": "AI自习室"}
    }
    </script>
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "首页", "item": "https://dingjiu1989-hue.github.io/"},
        {"@type": "ListItem", "position": 2, "name": "副业资源", "item": "https://dingjiu1989-hue.github.io/sidehustle/"},
        {"@type": "ListItem", "position": 3, "name": "免费可商用图片资源汇总"}
      ]
    }
    </script>
</head>
<body>

<nav class="navbar">
  <div class="container">
    <a href="/" class="nav-logo">📚 AI自习室</a>
    <div class="nav-links">
      <a href="/">首页</a>
      <a href="/tech/">技术教程</a>
      <a href="/sidehustle/">副业资源</a>
      <a href="/tools/">工具推荐</a>
    </div>
    <input class="nav-search" type="search" placeholder="搜索..." disabled title="搜索功能开发中">
  </div>
</nav>

<main>
  <div class="container article-container">
    <div class="breadcrumb">
      <a href="/">首页</a> › <a href="/sidehustle/">副业资源</a> › 免费可商用图片资源汇总
    </div>

    <article>
      <div class="article-tags">
        <span class="tag-pin">📌 置顶</span>
        <span class="tag-cat">图片资源</span>
        <span class="tag-cat">免费</span>
      </div>

      <h1 class="article-title">免费可商用图片资源汇总</h1>
      <div class="article-meta">发布于 2026-05-03 · 阅读 2.1k · 8 回复</div>

      <div class="article-body">
        <p>做设计、写文章、做视频都需要配图。付费图库太贵，版权问题又麻烦。以下都是真正免费可商用的图片资源。</p>

        <h2>综合图库（Free + CC0）</h2>
        <table>
          <tr><th>网站</th><th>特点</th><th>是否需要署名</th></tr>
          <tr><td>Unsplash</td><td>高质量摄影，审美在线，量大</td><td>不需要</td></tr>
          <tr><td>Pexels</td><td>照片+视频，中文搜索还行</td><td>不需要</td></tr>
          <tr><td>Pixabay</td><td>照片+插画+矢量图+视频</td><td>不需要</td></tr>
          <tr><td>Freepik</td><td>大量矢量图和 PSD，部分免费</td><td>需要（免费版）</td></tr>
        </table>

        <h2>特定风格</h2>
        <ul>
          <li><strong>Illustrations (unDraw)</strong> — 开源 SVG 插画，可自定义颜色，适合产品页和 PPT。</li>
          <li><strong>Humaaans</strong> — 人物插画组件，可自由组合场景。</li>
          <li><strong>Nappy</strong> — 专注黑人/棕色人种的高质量照片，多元文化素材。</li>
          <li><strong>The Gender Spectrum Collection</strong> — LGBTQ+ 主题的免费图库。</li>
        </ul>

        <h2>纹理与背景</h2>
        <ul>
          <li><strong>Subtle Patterns</strong> — 细腻的平铺纹理背景，适合网站背景。</li>
          <li><strong>Gradienta</strong> — CSS 渐变背景，可直接复制代码。</li>
          <li><strong>SVG Backgrounds</strong> — 可定制的 SVG 背景图案生成器。</li>
        </ul>

        <h2>Icon 图标</h2>
        <ul>
          <li><strong>Flaticon</strong> — 海量矢量图标，部分免费需署名。</li>
          <li><strong>Feather Icons</strong> — 开源极简图标集，React/Vue 都有封装。</li>
          <li><strong>Heroicons</strong> — Tailwind CSS 团队出品，MIT 协议。</li>
        </ul>
      </div>
    </article>

    <section class="related">
      <h3>相关文章</h3>
      <div class="related-grid">
        <a href="/sidehustle/remote-work.html" class="related-card">远程工作平台大盘点</a>
      </div>
    </section>
  </div>
</main>

<footer class="footer">
  <p>📚 AI自习室 &copy; 2026</p>
  <p>纯静态 · GitHub Pages 托管</p>
  <p style="margin-top:0.5rem;"><a href="/">返回首页</a></p>
</footer>

</body>
</html>
```

- [ ] **Step 4: 创建 sidehustle/remote-work.html**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>远程工作平台大盘点 — AI自习室</title>
    <meta name="description" content="盘点国内外主流远程工作平台，包括 Upwork、Toptal、电鸭社区等，自由职业者和数字游民必看。">
    <link rel="stylesheet" href="/css/style.css">
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "远程工作平台大盘点",
      "description": "盘点国内外主流远程工作平台，包括 Upwork、Toptal、电鸭社区等，自由职业者和数字游民必看。",
      "datePublished": "2026-04-28",
      "dateModified": "2026-04-28",
      "author": {"@type": "Person", "name": "AI自习室"}
    }
    </script>
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "首页", "item": "https://dingjiu1989-hue.github.io/"},
        {"@type": "ListItem", "position": 2, "name": "副业资源", "item": "https://dingjiu1989-hue.github.io/sidehustle/"},
        {"@type": "ListItem", "position": 3, "name": "远程工作平台大盘点"}
      ]
    }
    </script>
</head>
<body>

<nav class="navbar">
  <div class="container">
    <a href="/" class="nav-logo">📚 AI自习室</a>
    <div class="nav-links">
      <a href="/">首页</a>
      <a href="/tech/">技术教程</a>
      <a href="/sidehustle/">副业资源</a>
      <a href="/tools/">工具推荐</a>
    </div>
    <input class="nav-search" type="search" placeholder="搜索..." disabled title="搜索功能开发中">
  </div>
</nav>

<main>
  <div class="container article-container">
    <div class="breadcrumb">
      <a href="/">首页</a> › <a href="/sidehustle/">副业资源</a> › 远程工作平台大盘点
    </div>

    <article>
      <div class="article-tags">
        <span class="tag-cat">远程工作</span>
        <span class="tag-cat">自由职业</span>
      </div>

      <h1 class="article-title">远程工作平台大盘点</h1>
      <div class="article-meta">发布于 2026-04-28 · 阅读 1.5k · 6 回复</div>

      <div class="article-body">
        <p>远程工作不再是少数人的特权。这里整理国内外主流的远程工作平台，从接单到全职，覆盖各个层次。</p>

        <h2>国际平台</h2>
        <table>
          <tr><th>平台</th><th>定位</th><th>佣金</th></tr>
          <tr><td>Upwork</td><td>最大自由职业市场，各类工种</td><td>5%-20%</td></tr>
          <tr><td>Fiverr</td><td>服务化交易，卖家发布"服务套餐"</td><td>20%</td></tr>
          <tr><td>Toptal</td><td>高端技术人才，通过率仅 3%</td><td>平台定价</td></tr>
          <tr><td>Freelancer</td><td>项目竞标模式，价格竞争激烈</td><td>10%</td></tr>
        </table>

        <h2>国内平台</h2>
        <ul>
          <li><strong>电鸭社区 (eleduck.com)</strong> — 国内最大远程工作社区，职位质量高，偏技术岗。</li>
          <li><strong>V2EX 酷工作节点</strong> — 偶有远程岗发布，需常刷新。</li>
          <li><strong>圆领 (yuanling.com)</strong> — 字节系远程工作平台，偏设计/开发。</li>
          <li><strong>甜薪工场</strong> — 偏新媒体、运营、设计类远程兼职。</li>
        </ul>

        <h2>全职远程招聘网站</h2>
        <ul>
          <li><strong>Remote OK</strong> — 全球远程职位聚合，更新频繁。</li>
          <li><strong>We Work Remotely</strong> — 老牌远程招聘站，职位质量稳定。</li>
          <li><strong>Arc.dev</strong> — 面向开发者的远程工作平台，需通过技术面试。</li>
          <li><strong>Remotive</strong> — 主要为欧美公司，技术岗居多。</li>
        </ul>

        <h2>新手建议</h2>
        <ol>
          <li><strong>先完善英文简历和作品集</strong> — 国际平台英语是基本门槛</li>
          <li><strong>从小单做起</strong> — 积累好评后再接大单，不要急着报高价</li>
          <li><strong>选择垂直领域</strong> — 全栈不如一个细分方向深入</li>
          <li><strong>注意时区和税务</strong> — 跨国远程涉及外汇结算和个人报税</li>
        </ol>
      </div>
    </article>

    <section class="related">
      <h3>相关文章</h3>
      <div class="related-grid">
        <a href="/sidehustle/free-images.html" class="related-card">免费可商用图片资源汇总</a>
      </div>
    </section>
  </div>
</main>

<footer class="footer">
  <p>📚 AI自习室 &copy; 2026</p>
  <p>纯静态 · GitHub Pages 托管</p>
  <p style="margin-top:0.5rem;"><a href="/">返回首页</a></p>
</footer>

</body>
</html>
```

- [ ] **Step 5: 创建 tools/chrome-plugins.html**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2025 年度必备 Chrome 插件推荐 — AI自习室</title>
    <meta name="description" content="精选 15 款 2025 年必备的 Chrome 浏览器插件，涵盖效率、安全、开发、设计等场景。">
    <link rel="stylesheet" href="/css/style.css">
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "2025 年度必备 Chrome 插件推荐",
      "description": "精选 15 款 2025 年必备的 Chrome 浏览器插件，涵盖效率、安全、开发、设计等场景。",
      "datePublished": "2026-04-15",
      "dateModified": "2026-04-15",
      "author": {"@type": "Person", "name": "AI自习室"}
    }
    </script>
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "首页", "item": "https://dingjiu1989-hue.github.io/"},
        {"@type": "ListItem", "position": 2, "name": "工具推荐", "item": "https://dingjiu1989-hue.github.io/tools/"},
        {"@type": "ListItem", "position": 3, "name": "2025 年度必备 Chrome 插件推荐"}
      ]
    }
    </script>
</head>
<body>

<nav class="navbar">
  <div class="container">
    <a href="/" class="nav-logo">📚 AI自习室</a>
    <div class="nav-links">
      <a href="/">首页</a>
      <a href="/tech/">技术教程</a>
      <a href="/sidehustle/">副业资源</a>
      <a href="/tools/">工具推荐</a>
    </div>
    <input class="nav-search" type="search" placeholder="搜索..." disabled title="搜索功能开发中">
  </div>
</nav>

<main>
  <div class="container article-container">
    <div class="breadcrumb">
      <a href="/">首页</a> › <a href="/tools/">工具推荐</a> › 2025 年度必备 Chrome 插件推荐
    </div>

    <article>
      <div class="article-tags">
        <span class="tag-cat">Chrome</span>
        <span class="tag-cat">浏览器插件</span>
        <span class="tag-cat" style="background:#fff3cd;color:#856404;">🔥 热门</span>
      </div>

      <h1 class="article-title">2025 年度必备 Chrome 插件推荐</h1>
      <div class="article-meta">发布于 2026-04-15 · 阅读 3.8k · 35 回复</div>

      <div class="article-body">
        <p>浏览器是我们每天使用时间最长的软件之一。装上这些插件，Chrome 的效率和体验直接翻倍。</p>

        <h2>效率类</h2>
        <table>
          <tr><th>插件</th><th>功能</th><th>推荐理由</th></tr>
          <tr><td>uBlock Origin</td><td>广告拦截</td><td>轻量、开源、不卖数据，比 AdBlock 强太多</td></tr>
          <tr><td>Vimium</td><td>键盘浏览网页</td><td>不用鼠标就能滚动、点击、切换标签页</td></tr>
          <tr><td>OneTab</td><td>标签页管理</td><td>一键将大量标签页收纳为列表，释放内存</td></tr>
          <tr><td>GoFullPage</td><td>全页截图</td><td>滚动截取整个网页为 PNG，支持长图</td></tr>
        </table>

        <h2>安全和隐私</h2>
        <ul>
          <li><strong>Bitwarden</strong> — 开源密码管理器，全平台同步，免费版功能够用。</li>
          <li><strong>Privacy Badger</strong> — EFF 出品，自动学习并阻止跟踪器。</li>
          <li><strong>ClearURLs</strong> — 自动移除 URL 中的跟踪参数（utm_source 等）。</li>
        </ul>

        <h2>开发者工具</h2>
        <ul>
          <li><strong>React Developer Tools</strong> — React 组件树调试必备。</li>
          <li><strong>Wappalyzer</strong> — 一键查看任意网站的技术栈。</li>
          <li><strong>JSON Viewer</strong> — 自动格式化 JSON 响应，可折叠可搜索。</li>
        </ul>

        <h2>内容消费</h2>
        <ul>
          <li><strong>DeepL Translate</strong> — 整句翻译质量碾压 Google 翻译。</li>
          <li><strong>Grammarly</strong> — AI 英语写作助手，检查语法和语气。</li>
          <li><strong>Simplify</strong> — 格式化网页内容，去除广告和杂乱元素。</li>
        </ul>
      </div>
    </article>

    <section class="related">
      <h3>相关文章</h3>
      <div class="related-grid">
        <a href="/tools/note-apps.html" class="related-card">白板/笔记/思维导图工具对比</a>
      </div>
    </section>
  </div>
</main>

<footer class="footer">
  <p>📚 AI自习室 &copy; 2026</p>
  <p>纯静态 · GitHub Pages 托管</p>
  <p style="margin-top:0.5rem;"><a href="/">返回首页</a></p>
</footer>

</body>
</html>
```

- [ ] **Step 6: 创建 tools/note-apps.html**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>白板笔记思维导图工具对比 — AI自习室</title>
    <meta name="description" content="对比 Notion、Obsidian、Miro、Heptabase 等主流笔记和思维导图工具的优缺点，帮你选适合自己的。">
    <link rel="stylesheet" href="/css/style.css">
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "白板笔记思维导图工具对比",
      "description": "对比 Notion、Obsidian、Miro、Heptabase 等主流笔记和思维导图工具的优缺点。",
      "datePublished": "2026-04-10",
      "dateModified": "2026-04-10",
      "author": {"@type": "Person", "name": "AI自习室"}
    }
    </script>
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "首页", "item": "https://dingjiu1989-hue.github.io/"},
        {"@type": "ListItem", "position": 2, "name": "工具推荐", "item": "https://dingjiu1989-hue.github.io/tools/"},
        {"@type": "ListItem", "position": 3, "name": "白板笔记思维导图工具对比"}
      ]
    }
    </script>
</head>
<body>

<nav class="navbar">
  <div class="container">
    <a href="/" class="nav-logo">📚 AI自习室</a>
    <div class="nav-links">
      <a href="/">首页</a>
      <a href="/tech/">技术教程</a>
      <a href="/sidehustle/">副业资源</a>
      <a href="/tools/">工具推荐</a>
    </div>
    <input class="nav-search" type="search" placeholder="搜索..." disabled title="搜索功能开发中">
  </div>
</nav>

<main>
  <div class="container article-container">
    <div class="breadcrumb">
      <a href="/">首页</a> › <a href="/tools/">工具推荐</a> › 白板笔记思维导图工具对比
    </div>

    <article>
      <div class="article-tags">
        <span class="tag-cat">效率工具</span>
        <span class="tag-cat">笔记软件</span>
      </div>

      <h1 class="article-title">白板/笔记/思维导图工具对比</h1>
      <div class="article-meta">发布于 2026-04-10 · 阅读 2.3k · 9 回复</div>

      <div class="article-body">
        <p>市面上的笔记工具有几十款，适合别人的不一定适合你。从功能、平台、价格三个维度帮你选对工具。</p>

        <h2>综合对比</h2>
        <table>
          <tr><th>工具</th><th>定位</th><th>免费版</th><th>离线</th></tr>
          <tr><td>Notion</td><td>全能型笔记+数据库</td><td>个人免费</td><td>不支持</td></tr>
          <tr><td>Obsidian</td><td>本地优先知识库</td><td>个人免费</td><td>原生支持</td></tr>
          <tr><td>Logseq</td><td>大纲式双链笔记</td><td>开源免费</td><td>本地优先</td></tr>
          <tr><td>Heptabase</td><td>可视化知识管理</td><td>$8.99/月</td><td>不支持</td></tr>
          <tr><td>Miro</td><td>在线协作白板</td><td>3 块白板免费</td><td>不支持</td></tr>
          <tr><td>Excalidraw</td><td>手绘风格白板</td><td>开源免费</td><td>支持</td></tr>
          <tr><td>XMind</td><td>专业思维导图</td><td>基础免费</td><td>桌面版支持</td></tr>
        </table>

        <h2>场景推荐</h2>
        <ul>
          <li><strong>个人知识管理</strong> → Obsidian 或 Logseq。本地 Markdown 文件，数据自己掌控，双链功能强大。</li>
          <li><strong>团队文档协作</strong> → Notion。数据库视图、模板系统、权限管理，小团队一站式方案。</li>
          <li><strong>视觉思考和研究</strong> → Heptabase。白板+卡片，适合深度研究和复杂问题的可视化梳理。</li>
          <li><strong>头脑风暴和流程图</strong> → Miro 或 Excalidraw。前者适合团队，后者适合个人快速画草稿。</li>
          <li><strong>考试复习/读书笔记</strong> → XMind。传统思维导图工具中最成熟的，模板丰富。</li>
        </ul>
      </div>
    </article>

    <section class="related">
      <h3>相关文章</h3>
      <div class="related-grid">
        <a href="/tools/chrome-plugins.html" class="related-card">2025 年度必备 Chrome 插件推荐</a>
      </div>
    </section>
  </div>
</main>

<footer class="footer">
  <p>📚 AI自习室 &copy; 2026</p>
  <p>纯静态 · GitHub Pages 托管</p>
  <p style="margin-top:0.5rem;"><a href="/">返回首页</a></p>
</footer>

</body>
</html>
```

- [ ] **Step 7: 提交全部 6 篇文章**

```bash
git add tech/ sidehustle/ tools/ article-template.html
git commit -m "feat: 6 sample articles across 3 categories, plus article template"
```

---

### Task 9: 验证和部署

**Files:** 不改文件，纯验证

- [ ] **Step 1: 本地验证 — 确认所有页面可正常打开**

```bash
open /Users/daniel/gh-pages-demo/index.html && \
open /Users/daniel/gh-pages-demo/tech/index.html && \
open /Users/daniel/gh-pages-demo/sidehustle/index.html && \
open /Users/daniel/gh-pages-demo/tools/index.html && \
open /Users/daniel/gh-pages-demo/tech/git-cheatsheet.html && \
open /Users/daniel/gh-pages-demo/tech/macos-tools.html && \
open /Users/daniel/gh-pages-demo/sidehustle/free-images.html && \
open /Users/daniel/gh-pages-demo/sidehustle/remote-work.html && \
open /Users/daniel/gh-pages-demo/tools/chrome-plugins.html && \
open /Users/daniel/gh-pages-demo/tools/note-apps.html
```

检查：浏览器中逐个打开 10 个页面，确认样式正常、链接可点、导航一致

- [ ] **Step 2: 验证 SEO 要素**

手动检查首页和任意一篇文章页：
- `<title>` 非空且包含关键词
- `<meta name="description">` 含 120-160 字描述
- Schema.org JSON-LD 脚本存在
- 面包屑链接可点击

- [ ] **Step 3: 提交并推送到 GitHub**

```bash
git -C /Users/daniel/gh-pages-demo log --oneline
# 确认所有提交都在

git -C /Users/daniel/gh-pages-demo push origin main
```

- [ ] **Step 4: 验证线上部署**

```bash
# 等 30 秒让 GitHub Pages 构建
sleep 30

# 逐个检查关键页面返回 200
for url in \
  https://dingjiu1989-hue.github.io/ \
  https://dingjiu1989-hue.github.io/tech/ \
  https://dingjiu1989-hue.github.io/sidehustle/ \
  https://dingjiu1989-hue.github.io/tools/ \
  https://dingjiu1989-hue.github.io/tech/git-cheatsheet.html \
  https://dingjiu1989-hue.github.io/tools/chrome-plugins.html \
  https://dingjiu1989-hue.github.io/sitemap.xml \
  https://dingjiu1989-hue.github.io/robots.txt; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "$url")
  echo "$code — $url"
done
```

期望：所有 URL 返回 `200`

- [ ] **Step 5: 打开线上首页**

```bash
open https://dingjiu1989-hue.github.io/
```

---

## 完成标志

- [ ] 首页显示 3 个版块、6 篇文章链接
- [ ] 3 个分类页各有 2 篇文章
- [ ] 每篇文章有完整正文、面包屑、相关推荐
- [ ] SEO 要素齐全（title, description, Schema.org, sitemap, robots）
- [ ] 所有页面内链不出现死链
- [ ] `sitemap.xml` 和 `robots.txt` 可访问
