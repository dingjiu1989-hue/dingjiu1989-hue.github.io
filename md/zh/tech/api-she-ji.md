---
title: "RESTful API设计规范：资源命名、状态码、版本管理、分页"
description: "系统讲解RESTful API的设计规范和最佳实践，涵盖资源命名规则、HTTP状态码使用、版本管理策略和分页方案的设计。"
date: 2026-05-12
board: tech
url: https://dingjiu1989-hue.github.io/zh/tech/api-she-ji.html
---

## RESTful设计原则

RESTful API设计需要遵循几个核心原则：资源导向、无状态、统一接口和HATEOAS。虽然在实际项目中不必严格遵守所有原则，但理解这些原则有助于设计更规范的API。

## 资源命名

### 命名规范

- 使用名词复数表示资源集合：`/users`、`/orders`
- 使用URL路径表示资源层级：`/users/{id}/orders`
- 使用查询参数表示过滤和排序：`?status=active&sort=created_at`
- 使用小写字母和连字符：`/user-profiles`而非`/userProfiles`

### 最佳实践

```http
GET /users                    # 获取用户列表
GET /users/{id}               # 获取单个用户
POST /users                   # 创建用户
PATCH /users/{id}             # 部分更新用户
DELETE /users/{id}            # 删除用户
GET /users/{id}/orders        # 获取用户的订单列表
```

### 常见反模式

- 使用动词：`/getUsers`应为`GET /users`
- 过深的嵌套：超过三级嵌套应考虑展平
- 不一致的命名：混合使用snake_case和camelCase

## HTTP状态码

正确使用HTTP状态码可以让客户端更准确地理解请求结果。

### 常用状态码

- **200 OK**：请求成功
- **201 Created**：资源创建成功
- **204 No Content**：删除成功，无返回内容
- **400 Bad Request**：请求参数错误
- **401 Unauthorized**：未认证
- **403 Forbidden**：无权限
- **404 Not Found**：资源不存在
- **409 Conflict**：资源冲突（如重复创建）
- **422 Unprocessable Entity**：业务逻辑验证失败
- **429 Too Many Requests**：请求频率限制
- **500 Internal Server Error**：服务器内部错误

### 错误响应格式

```json
{
    "error": {
        "code": "USER_NOT_FOUND",
        "message": "用户不存在",
        "details": {
            "userId": "12345"
        }
    }
}
```

## 版本管理

### 版本策略

- **URL路径版本**：`/v1/users`、`/v2/users`，最常用
- **请求头版本**：`Accept: application/vnd.myapp.v1+json`
- **查询参数版本**：`/users?version=1`

URL路径版本策略最为直观，便于缓存和调试。建议在URL中永久保留版本号。

### 版本演进

- 向后兼容的变更：新增字段、新增端点不需要大版本
- 破坏性变更：修改字段类型、删除字段需要大版本
- 每个大版本至少维护6-12个月的过渡期

## 分页设计

### 分页方案

```http
GET /users?page=1&per_page=20
```

响应中包含分页元数据：

```json
{
    "data": [...],
    "pagination": {
        "page": 1,
        "per_page": 20,
        "total": 156,
        "total_pages": 8,
        "links": {
            "first": "/users?page=1",
            "prev": null,
            "next": "/users?page=2",
            "last": "/users?page=8"
        }
    }
}
```

### 游标分页

对于实时数据，游标分页比偏移分页更稳定：

```http
GET /users?cursor=eyJpZCI6MTB9&limit=20
```

游标分页在数据发生增删时不会导致重复或遗漏，适合社交信息流等场景。

## 安全与规范

- 所有API必须使用HTTPS
- 认证使用Bearer Token或OAuth 2.0
- 统一时间格式（ISO 8601）
- 统一错误格式
- 提供API文档（OpenAPI/Swagger）

遵循一致的API设计规范能降低前后端协作成本，提升API的可维护性和开发者体验。
