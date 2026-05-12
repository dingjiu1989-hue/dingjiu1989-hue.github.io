---
title: "Web安全基础指南"
description: "系统介绍Web安全核心知识，包括XSS、CSRF、SQL注入等常见攻击原理与防御方案，帮助开发者构建安全的Web应用。"
date: 2026-05-11
board: security
url: https://dingjiu1989-hue.github.io/zh/security/web-security-basics.html
---

## 跨站脚本攻击（XSS）

XSS是最常见的Web安全漏洞，攻击者将恶意脚本注入页面。分为三种类型：反射型XSS（恶意脚本在请求中，服务器直接返回执行）、存储型XSS（恶意脚本存储在服务器，每次访问都执行）和DOM型XSS（纯客户端漏洞，通过DOM操作执行）。

**防御方案**：核心原则是"不信任任何用户输入"。对输出进行HTML实体编码，将`<`转义为`&lt;`，`>`转义为`&gt;`。设置CSP（Content Security Policy）响应头限制脚本来源：`Content-Security-Policy: default-src 'self'`。React和Vue等现代框架默认对输出编码，但`dangerouslySetInnerHTML`和`v-html`需谨慎使用。

## 跨站请求伪造（CSRF）

CSRF攻击诱导用户在已登录状态下执行非本意的操作。攻击者构造恶意页面，自动发起跨站请求，因为Cookie会自动携带，服务器误认为是合法操作。

**防御方案**：使用CSRF Token——在表单中嵌入随机Token，服务端验证Token有效性。SameSite Cookie属性设置为Strict或Lax，限制跨站请求携带Cookie。验证请求头中的Origin或Referer字段。

## SQL注入

SQL注入利用未过滤的用户输入构造恶意SQL语句。攻击形式包括基于布尔的盲注、基于时间的盲注和UNION查询注入。即使返回结果不可见，攻击者也能通过布尔或时间延迟逐步提取数据。

**防御方案**：永远使用参数化查询（Prepared Statement），而不是拼接SQL字符串。ORM框架（如Sequelize、Prisma、SQLAlchemy）默认使用参数化查询，但原生查询时仍需警惕。对数据库账户实施最小权限原则，应用层使用只读或特定Schema的访问账户。

## HTTPS与TLS

所有Web应用都应启用HTTPS。使用Let's Encrypt免费获取TLS证书，Certbot自动化续期。配置HSTS头要求浏览器始终使用HTTPS连接：`Strict-Transport-Security: max-age=31536000; includeSubDomains`。

## 安全响应头

除了CSP和HSTS，还应配置：X-Frame-Options防止点击劫持，X-Content-Type-Options防止MIME类型嗅探，Referrer-Policy控制Referer信息泄露。定期使用Security Headers工具检测站点头部配置。
