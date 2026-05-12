---
title: "API安全：速率限制、输入验证、认证鉴权最佳实践"
description: "全面讲解API安全的核心实践，涵盖速率限制策略、输入验证方法、认证鉴权机制和API网关安全配置的工程方案。"
date: 2026-05-12
board: security
url: https://dingjiu1989-hue.github.io/zh/security/api-anquan.html
---

## API安全威胁

API已成为应用攻击的主要入口。常见的API安全威胁包括：滥用调用、注入攻击、身份伪造和数据泄露。

## 速率限制

### 限流策略

**基于IP的限流：**
```nginx
# Nginx限流配置
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

server {
    location /api/ {
        limit_req zone=api_limit burst=20 nodelay;
    }
}
```

**基于用户的限流：**
```python
from flask_limiter import Limiter

limiter = Limiter(key_func=lambda: current_user.id)

@app.route("/api/endpoint")
@limiter.limit("100/hour")
def endpoint():
    return jsonify({"data": "success"})
```

**分层限流策略：**
- 全局：1000请求/秒
- 每用户：100请求/分钟
- 每IP：50请求/分钟
- 敏感API（登录）：5请求/分钟

### 限流响应

当请求被限流时，返回429状态码和明确的错误信息：

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 60
Content-Type: application/json

{
    "error": "rate_limit_exceeded",
    "message": "请求过于频繁，请60秒后再试",
    "retry_after": 60
}
```

## 输入验证

### 验证层次

输入验证应在多个层次实施：

**传输层：**
- 最大请求体大小限制
- 请求超时设置
- HTTPS强制

**应用层：**
- 参数类型验证
- 长度限制
- 格式校验

```python
from pydantic import BaseModel, EmailStr, Field

class CreateUserRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_]+$")
    email: EmailStr
    age: int = Field(..., ge=0, le=150)
```

### 常见防御

- **SQL注入**：参数化查询
- **XSS**：输出编码
- **命令注入**：禁止使用`exec`、`system`等函数
- **路径遍历**：白名单验证路径

### 内容类型验证

严格验证`Content-Type`头：
```python
@app.before_request
def validate_content_type():
    if request.method in ["POST", "PUT", "PATCH"]:
        if request.content_type != "application/json":
            return {"error": "不支持的Content-Type"}, 415
```

## 认证鉴权

### 认证方案

**OAuth 2.0 + OpenID Connect：**
```http
# 获取Token
POST /oauth/token
Content-Type: application/json

{
    "grant_type": "authorization_code",
    "code": "auth_code_xxx",
    "client_id": "client_xxx",
    "client_secret": "secret_xxx",
    "redirect_uri": "https://app.example.com/callback"
}
```

**API Key方案（适用于服务间调用）：**
- 为每个调用方生成唯一API Key
- API Key定期轮换
- 在请求头中传递：`X-API-Key: your-api-key`

### 鉴权粒度

**RBAC（基于角色的访问控制）：**
```
/admin/* → 需要admin角色
/api/users/{id} → 只能访问自己的数据
/api/orders → 商户可查看自己的订单
```

**ABAC（基于属性的访问控制）：**
根据用户属性、资源属性和环境条件动态判定权限，比RBAC更灵活。

### 敏感操作确认

对于删除、批量操作等敏感API，实施二次确认：
- 发送验证码到注册邮箱/手机
- 要求重新输入密码
- 需要管理员审批

## API网关配置

API网关是实施安全策略的理想位置：

```yaml
# Kong API Gateway 安全配置
plugins:
  - name: rate-limiting
    config:
      minute: 100
      policy: local

  - name: key-auth
    config:
      key_names: ["X-API-Key"]

  - name: cors
    config:
      origins: ["https://app.example.com"]
      methods: ["GET", "POST", "PUT", "DELETE"]
```

## 审计日志

记录所有API调用的审计日志：
- 请求者和请求来源IP
- 请求时间和耗时
- 请求的API和方法
- 响应状态码
- 失败原因

API安全是一个系统工程，需要从传输层到应用层建立多层防御体系。
