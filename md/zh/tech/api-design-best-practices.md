---
title: "API设计最佳实践"
description: "系统化讲解RESTful API设计原则，包括资源命名、版本管理、错误处理、认证授权以及文档规范等关键实践方法。"
date: 2026-05-11
board: tech
url: https://dingjiu1989-hue.github.io/zh/tech/api-design-best-practices.html
---

## 资源命名规范

RESTful API的核心是资源导向设计。资源使用名词复数形式：`/users`、`/orders`、`/articles`。子资源通过嵌套表达层级关系：`/users/{id}/orders`。查询参数用于过滤和排序：`/users?status=active&sort=-created_at`。

避免在URL中使用动词。操作通过HTTP方法表达：GET查询、POST创建、PUT全量更新、PATCH部分更新、DELETE删除。如果确实需要表达动作，可以将其作为子资源：`/orders/{id}/cancel`。

## API版本管理

版本管理有三种主流策略：URL路径版本（`/v1/users`）、请求头版本（`Accept: application/vnd.api.v1+json`）和查询参数版本（`/users?version=1`）。URL路径版本最为直观，推荐使用。

版本迭代时遵循向后兼容原则。新增字段不影响旧版本客户端，修改字段需同时维护新旧版本。废弃端点时使用Sunset响应头通知客户端，保留至少6个月的迁移窗口。

## 错误处理规范

统一的错误响应格式对客户端友好。定义标准错误结构：`{"error": {"code": "USER_NOT_FOUND", "message": "用户不存在", "details": {}}}`。HTTP状态码准确反映错误类型：400参数错误、401未认证、403无权限、404资源不存在、422验证失败、429请求过频、500服务器错误。

**错误信息**应足够详细帮助调试，但避免暴露敏感信息如数据库查询语句或堆栈信息。开发环境与生产环境的错误详情通过配置区分。

## 认证与授权

API认证推荐使用JWT（JSON Web Token）。访问令牌（Access Token）设置较短有效期（15分钟），刷新令牌（Refresh Token）设置较长有效期（7天）。令牌在请求头中传递：`Authorization: Bearer <token>`。

OAuth 2.0适合第三方应用授权场景。授权码流程是最安全的方式，适用于有后端的应用。客户端凭证流程适合机器对机器通信。

## 文档与规范

使用OpenAPI（Swagger）规范定义API文档，让文档与代码保持一致。推荐使用API First开发模式：先编写OpenAPI规范，再根据规范生成服务端和客户端代码。

**限流策略**：在响应头中返回限流信息：`X-RateLimit-Limit`请求上限、`X-RateLimit-Remaining`剩余次数、`X-RateLimit-Reset`重置时间。配合429状态码和Retry-After头告知客户端等待时间。

分页是所有列表接口的必备功能。游标分页比传统偏移分页性能更好，适合大数据集。始终返回total_count方便客户端展示分页组件。
