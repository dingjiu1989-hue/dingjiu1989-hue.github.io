---
title: "Web 安全入门：每个开发者都应知道的 10 个安全实践"
description: "XSS、CSRF、SQL 注入、HTTPS、CORS……这些不是运维的事。本文用通俗语言讲解 10 个每个 Web 开发者都必须掌握的安全实践，附代码示例和检查清单。"
date: 2026-05-09
board: tech
url: https://dingjiu1989-hue.github.io/tech/web-security-basics.html
---

# Web 安全入门：每个开发者都应知道的 10 个安全实践

"安全是运维的事"——这是 Web 开发中最危险的误解。实际上，**大多数安全漏洞都来自应用层代码** ：没有校验的用户输入、硬编码的密钥、错误配置的 CORS。本文用最直白的语言讲清楚 10 个你明天就能用上的安全实践。

## 1\. 永远不要信任用户输入（XSS 防御）

跨站脚本攻击（XSS）的原理很简单：攻击者在输入框里插入 JavaScript 代码，你的网站原封不动地把它显示给其他用户，然后代码就执行了。

**三种 XSS 类型** ：

  * **存储型 XSS** ：恶意脚本被存到数据库，每次有人访问页面都会执行。比如论坛帖子内容里插入了 script 标签。
  * **反射型 XSS** ：恶意脚本通过 URL 参数传入，服务端直接返回到页面。比如搜索结果的"你搜索了：<script>..."
  * **DOM 型 XSS** ：纯前端问题，JS 把不可信数据写入了 innerHTML。



**防御方案** ：
    
    
    // ❌ 危险：直接把用户输入插入 HTML
    element.innerHTML = userInput;
    
    // ✅ 安全：转义 HTML 实体
    function escapeHtml(str) {
      const div = document.createElement('div');
      div.textContent = str;
      return div.innerHTML;
    }
    element.innerHTML = escapeHtml(userInput);
    
    // ✅ 更安全：用 textContent 替代 innerHTML
    element.textContent = userInput;

现代框架（React、Vue）默认会转义变量输出，但 `dangerouslySetInnerHTML` 和 `v-html` 仍然有风险。

## 2\. 参数化查询防 SQL 注入

SQL 注入至今仍是 OWASP Top 10 的常客。原理是将恶意 SQL 片段注入到查询语句中。
    
    
    // ❌ 危险：字符串拼接
    const query = `SELECT * FROM users WHERE name = '${username}'`;
    // 如果 username = "admin' OR '1'='1"
    // 结果：SELECT * FROM users WHERE name = 'admin' OR '1'='1'
    // 直接返回所有用户！
    
    // ✅ 安全：参数化查询
    const query = 'SELECT * FROM users WHERE name = ?';
    db.query(query, [username]);  // username 被当做值，不会被执行为 SQL

使用 ORM（Prisma、TypeORM、SQLAlchemy）能很大程度上避免这个问题，但手写 SQL 时务必用参数化。

## 3\. CSRF Token 防跨站请求伪造

CSRF 利用的是浏览器自动携带 Cookie 的特性。你在 A 网站登录了银行，然后访问了恶意网站 B，B 网站偷偷向 A 银行发了一个转账请求——浏览器自动带上了你的 Cookie，转账成功。

**防御方案** ：

  * **CSRF Token** ：服务端生成随机 token，放在表单隐藏字段中。提交时验证 token 是否匹配。攻击者无法猜到 token。
  * **SameSite Cookie** ：设置 `Set-Cookie: SameSite=Strict`，跨站请求不会携带 Cookie。这是最简单的防线。
  * **自定义 Header** ：Ajax 请求加 `X-Requested-With: XMLHttpRequest`，服务端校验。



## 4\. HTTPS 和 HSTS

HTTP 是明文传输，中间人可以窃听和篡改。HTTPS 是底线——**2026 年了，没有理由不用 HTTPS** 。

更进一步：启用 **HSTS（HTTP Strict Transport Security）** 。它告诉浏览器"以后只通过 HTTPS 访问我"，防止 SSL 剥离攻击。
    
    
    # Nginx 配置
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";

## 5\. 正确配置 CORS

CORS（跨域资源共享）是最容易被误解和误配的安全机制。常见错误：
    
    
    // ❌ 危险：允许所有来源
    Access-Control-Allow-Origin: *
    
    // ❌ 危险：反射式允许（攻击者可以伪造 Origin 头）
    // 不要从请求的 Origin 头反射回 Access-Control-Allow-Origin
    
    // ✅ 安全：白名单验证
    const allowedOrigins = ['https://myapp.com', 'https://admin.myapp.com'];
    if (allowedOrigins.includes(requestOrigin)) {
      res.setHeader('Access-Control-Allow-Origin', requestOrigin);
    }

## 6\. 密码存储：bcrypt 而不是 MD5

密码永远不要明文存储，也不要用快速哈希算法（MD5、SHA-1）。用专为密码设计的慢哈希算法：
    
    
    // Node.js (bcrypt)
    const bcrypt = require('bcrypt');
    const saltRounds = 12;
    
    // 注册时哈希密码
    const hash = await bcrypt.hash(password, saltRounds);
    await db.users.insert({ email, password: hash });
    
    // 登录时验证
    const user = await db.users.findOne({ email });
    const valid = await bcrypt.compare(password, user.password);

**盐值（Salt）是关键** ：即使两个用户用相同的密码，哈希结果也不一样。大部分哈希库会自动处理。

## 7\. 环境变量管理密钥

API Key、数据库密码、JWT Secret 硬编码在代码里——这是教科书级别的安全灾难。一旦代码泄露到 GitHub，攻击者可以用自动化工具在几分钟内扫描到。
    
    
    # ✅ 用 .env 文件 + .gitignore
    DATABASE_URL=postgres://...
    STRIPE_SECRET=sk_live_...
    JWT_SECRET=your-256-bit-secret
    
    # ✅ .gitignore 必须包含
    .env
    .env.local
    *.pem

使用 `dotenv` 或框架内置的环境变量加载。生产环境用平台的环境变量注入（Vercel Env、GitHub Secrets、K8s Secrets）。

## 8\. 限制速率（Rate Limiting）

没有速率限制的 API 就是开放的 DDoS 攻击面和暴力破解入口。
    
    
    // Express 中间件示例 (express-rate-limit)
    const rateLimit = require('express-rate-limit');
    
    const loginLimiter = rateLimit({
      windowMs: 15 * 60 * 1000,  // 15 分钟
      max: 5,                      // 最多 5 次请求
      message: '登录尝试过于频繁，请 15 分钟后再试'
    });
    
    app.post('/login', loginLimiter, loginHandler);

关键端点（登录、注册、密码重置、API）都要加限速。

## 9\. 依赖安全审计

你的应用代码可能没问题，但你引用的 300 个 npm 包中可能隐藏着已知漏洞。
    
    
    # npm 审计
    npm audit          # 列出已知漏洞
    npm audit fix      # 自动修复（安全的补丁版本）
    
    # 定期检查
    npm outdated       # 查看过时的依赖

GitHub Dependabot 会自动扫描你的仓库并提 PR 修复漏洞。打开它，免费的。

## 10\. 安全响应头

几个 HTTP 头可以防御大量常见攻击：
    
    
    # 防点击劫持
    X-Frame-Options: DENY
    
    # 防 MIME 类型嗅探
    X-Content-Type-Options: nosniff
    
    # 内容安全策略（CSP）——最强防线之一
    Content-Security-Policy: default-src 'self'; script-src 'self' https://trusted-cdn.com;
    
    # 禁用浏览器特性探测（生产环境用不到）
    Permissions-Policy: camera=(), microphone=(), geolocation=()

可以用 [securityheaders.com](<https://securityheaders.com>) 检查你的网站得分。

## 安全检查清单

#| 检查项| 状态  
---|---|---  
1| 所有用户输入经过转义/校验| ☐  
2| SQL 查询全部参数化| ☐  
3| 表单有 CSRF Token 或 SameSite Cookie| ☐  
4| 全站 HTTPS + HSTS| ☐  
5| CORS 配置白名单，非通配符| ☐  
6| 密码用 bcrypt/argon2 存储| ☐  
7| 密钥/敏感信息不在代码中| ☐  
8| 关键端点有速率限制| ☐  
9| 依赖漏洞已修复（npm audit 通过）| ☐  
10| 安全响应头已配置| ☐  
  
## 总结

这 10 条不需要你是安全专家。它们大多是"配置一次，受益终生"的实践。如果你只能做三件事：**转义用户输入、参数化查询、HTTPS + HSTS** ——这三条能挡住 80% 的常见攻击。

### 📖 相关推荐

  * [REST API 设计最佳实践：写出让人愿意用的接口](<https://dingjiu1989-hue.github.io/tech/rest-api-best-practices.html>)
  * [Docker 30 分钟入门：从安装到第一个容器](<https://dingjiu1989-hue.github.io/tech/docker-quickstart.html>)
  * [单元测试入门：从零到写出第一个可维护的测试](<https://dingjiu1989-hue.github.io/tech/unit-testing-guide.html>)



**See also:** [Git 进阶：交互式 rebase、cherry-pick 和 bisect 实战](</tech/git-advanced.html>), [单元测试入门：从零到写出第一个可维护的测试](</tech/unit-testing-guide.html>), [REST API 设计最佳实践：写出让人愿意用的接口](</tech/rest-api-best-practices.html>).
