---
title: "REST API 设计最佳实践：写出让人愿意用的接口"
description: "从 URL 设计、HTTP 方法选择到错误处理和分页，系统讲解 REST API 设计规范，附常见反模式避坑。"
date: 2026-05-07
board: tech
url: https://dingjiu1989-hue.github.io/zh/tech/rest-api-best-practices.html
---

# REST API 设计最佳实践：写出让人愿意用的接口

好的 API 设计让调用方心情愉悦，坏的 API 让他们想砸键盘。这篇文章总结 10 条实战验证的设计原则。 URL 设计原则

  * **用名词复数而非动词** — `GET /users` 不是 `GET /getUsers`。HTTP 方法已经表达了动作。
  * **层级关系用嵌套 URL** — `GET /users/123/orders` 清晰表达了"用户 123 的订单"。
  * **不要超过 3 层** — `/users/123/orders/456/items` 太深了，这种情况拆成 `/orders/456/items`。
  * **用 kebab-case 不用 camelCase** — `/shipping-address` 不是 `/shippingAddress`。SEO 友好，肉眼易读。

HTTP 方法正确使用 方法| 操作| 幂等?| 示例  
---|---|---|---  
GET| 读取| ✅| `GET /articles`  
POST| 创建| ❌| `POST /articles`  
PUT| 全量更新| ✅| `PUT /articles/1`  
PATCH| 部分更新| ❌| `PATCH /articles/1`  
DELETE| 删除| ✅| `DELETE /articles/1`  
响应格式规范

    {
      "data": { "id": 1, "title": "..." },
      "meta": { "page": 1, "per_page": 20, "total": 150 },
      "errors": null
    }

错误处理

  * **用正确的 HTTP 状态码** — 400 参数错误、401 未认证、403 无权限、404 不存在、422 参数校验失败、429 频率限制、500 服务器错误。
  * **错误信息结构化** — 返回 `{"errors":[{"code":"VALIDATION_ERROR","field":"email","message":"邮箱格式不正确"}]}`，不要只返回一个字符串。

五大常见反模式

  1. **所有操作都用 POST** — 这是 RPC 不是 REST
  2. **返回所有字段** — 支持 `?fields=id,title` 让客户端选择需要的字段
  3. **不版本化** — URL 加 `/v1/` 前缀或在 Header 中指定版本
  4. **不限制分页** — `per_page` 最大 100，防止一次请求拖垮数据库
  5. **不写 API 文档** — OpenAPI/Swagger 规范是标配

📖 相关推荐

  * [Git 进阶：交互式 rebase、cherry-pick 和 bisect 实战](<https://dingjiu1989-hue.github.io/zh/tech/git-advanced.html>)
  * [单元测试入门：从零到写出第一个可维护的测试](<https://dingjiu1989-hue.github.io/zh/tech/unit-testing-guide.html>)
  * [正则表达式 30 分钟入门指南](<https://dingjiu1989-hue.github.io/zh/tech/regex-guide.html>)

**See also:** [30 个免费又好用的 API 合集：开发者必备](</zh/tools/free-api-collection.html>), [OpenAI API 入门：用 10 行代码调用 GPT](</zh/ai/openai-api-intro.html>), [AI 自动化工作流实战：让 AI 替你干重复活](</zh/ai/ai-automation-workflow.html>).
