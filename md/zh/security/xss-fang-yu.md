---
title: "XSS跨站脚本攻击防御：CSP策略、输出编码、框架安全"
description: "全面讲解跨站脚本攻击（XSS）的防御体系，涵盖内容安全策略配置、输出编码方法和前端框架的安全使用实践。"
date: 2026-05-12
board: security
url: https://dingjiu1989-hue.github.io/zh/security/xss-fang-yu.html
---

## XSS攻击类型

跨站脚本攻击（XSS）是Web应用最常见的漏洞之一，攻击者将恶意脚本注入到页面中，在用户浏览器中执行。

### 存储型XSS

恶意脚本存储在服务器端（如数据库），当用户访问受影响页面时被触发。

**场景：** 评论区、用户资料、博客文章。

### 反射型XSS

恶意脚本通过URL参数或表单提交传入，服务器将未经过滤的输入直接返回给用户。

**场景：** 搜索功能、错误页面。

### DOM型XSS

恶意脚本通过修改客户端JavaScript运行时环境触发，不需要服务端参与。

**场景：** 使用`innerHTML`、`document.write`等方法不安全地渲染用户输入。

## CSP策略

内容安全策略（CSP）是防御XSS最强大的机制，通过HTTP头告诉浏览器哪些来源是可信任的。

### CSP配置

```http
Content-Security-Policy: default-src 'self'; script-src 'self' https://cdn.example.com; style-src 'self' 'unsafe-inline'
```

### 常用指令

- `default-src`：所有资源的默认策略
- `script-src`：可执行脚本的允许来源
- `style-src`：样式表的允许来源
- `img-src`：图片的允许来源
- `connect-src`：API请求的允许来源
- `report-uri`：违规上报地址

### 推荐策略

```http
# 严格CSP（推荐）
Content-Security-Policy: default-src 'self'; script-src 'nonce-{random}'; report-uri /csp-report

# 宽松CSP（迁移期）
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; report-uri /csp-report
```

### 实施步骤

1. 先使用`Content-Security-Policy-Report-Only`模式收集违规报告
2. 分析报告，调整策略以兼容现有功能
3. 切换到强制模式

## 输出编码

### 上下文相关的编码

在不同的HTML上下文中，需要使用不同的编码方式：

**HTML标签内：**
```html
&lt;script&gt;alert(1)&lt;/script&gt;
```

**HTML属性中：**
```html
<input value="John &amp; Doe">
```

**JavaScript字符串中：**
```javascript
var name = 'John\x20Doe';
```

**URL参数中：**
```javascript
encodeURIComponent(userInput)
```

### 框架内置编码

现代前端框架默认对输出进行编码：

- **React**：JSX默认转义所有输出
- **Vue**：模板插值`{{ }}`自动进行HTML转义
- **Angular**：默认使用安全上下文

```jsx
// React 安全输出
<div>{userInput}</div>  // 自动转义

// 危险：故意渲染HTML
<div dangerouslySetInnerHTML={{__html: userInput}} />
```

## 框架安全实践

### React安全指南

- 不要在`dangerouslySetInnerHTML`中使用用户输入
- 使用`sanitize-html`或`DOMPurify`净化HTML内容
- 避免使用`eval()`和`new Function()`

### Vue安全指南

- 使用`v-text`替代`v-html`显示用户内容
- 使用`xss`库对`v-html`内容进行过滤
- 避免使用`$el.innerHTML`直接操作

### 通用安全措施

- **Cookie设置HttpOnly和Secure标记**：防止JavaScript访问Cookie
- **输入过滤**：使用白名单方式过滤用户输入
- **CSP报告**：开启CSP报告，及时发现绕过方式

## XSS测试

- 使用自动化扫描工具（XSStrike、Burp Suite）
- 手动测试常见Payload
- 在CI/CD中集成安全扫描

XSS防御需要从多个层面入手，没有单一措施能提供完全保护。采用纵深防御策略才是最佳实践。
