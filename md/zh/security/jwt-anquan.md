---
title: "JWT安全：签名算法选择、过期策略、刷新令牌最佳实践"
description: "系统讲解JWT认证的安全最佳实践，涵盖签名算法选型、Token过期策略设计、刷新令牌机制和常见安全漏洞的防御措施。"
date: 2026-05-12
board: security
url: https://dingjiu1989-hue.github.io/zh/security/jwt-anquan.html
---

## JWT基础

JSON Web Token（JWT）是目前最流行的令牌格式，由Header、Payload和Signature三部分组成，通过Base64URL编码和签名算法生成。

## 签名算法选择

### HS256 vs RS256

**HS256（对称加密）：**
- 使用同一个密钥签名和验证
- 速度快，Token较短
- 密钥需要妥善管理，泄露后无法区分签名者和验证者

**RS256（非对称加密）：**
- 使用私钥签名，公钥验证
- 适合多服务间验证（一个认证服务签发，多个业务服务验证）
- 公钥可以公开，私钥只有签发服务持有

**推荐：** 微服务架构下始终使用RS256。单体应用可以使用HS256，但要确保密钥强度足够。

### 算法混淆攻击

这是JWT最常见的安全漏洞之一。攻击者修改JWT Header中的`alg`字段为`none`，如果服务端验证不严格，就会接受没有签名的Token。

**防御：**
```python
# 验证算法白名单
jwt.decode(token, public_key, algorithms=["RS256"], options={"require": ["exp", "iat"]})
```

## Token过期策略

### Access Token

**建议过期时间：**
- Web应用：15-30分钟
- 移动应用：30-60分钟
- 需要用户确认的敏感操作：5分钟

**过期后的处理：**
- 前端检测到401错误，自动使用Refresh Token获取新Access Token
- 如果Refresh Token也过期，要求用户重新登录

### 基于风险的动态过期

对于高风险操作（修改密码、支付），使用更短的过期时间。对于低风险操作（浏览内容），使用标准过期时间。

## 刷新令牌机制

Refresh Token是长期令牌，用于获取新的Access Token。

### 安全存储

- **Access Token**：内存变量，不持久化
- **Refresh Token**：HttpOnly Cookie或安全存储

### 轮转策略

每次使用Refresh Token获取新的Access Token时，同时返回一个新的Refresh Token，旧的Refresh Token立即失效。

```python
def refresh_access_token(refresh_token):
    # 验证Refresh Token
    payload = verify_refresh_token(refresh_token)
    user_id = payload["sub"]

    # 检查是否已被使用（轮转检测）
    if is_token_revoked(refresh_token):
        revoke_all_user_tokens(user_id)  # 可能被攻击，清理所有令牌
        raise SecurityException("检测到令牌重用")

    # 吊销旧Refresh Token
    revoke_token(refresh_token)

    # 生成新的Access Token和Refresh Token
    new_access = create_access_token(user_id)
    new_refresh = create_refresh_token(user_id)

    return new_access, new_refresh
```

### 重用检测

如果检测到已使用的Refresh Token被再次提交，说明令牌可能已被盗，应吊销该用户的所有令牌。

## 其他安全措施

### Token召回（撤销）

JWT在签发后无法主动失效（直到过期）。对于需要提前失效的场景：

1. **黑名单**：将需要失效的Token的JTI标识加入黑名单
2. **版本号**：在Token中嵌入用户令牌版本号，版本变更时旧Token失效
3. **短过期+自动刷新**：减少Token被利用的时间窗口

### Claims验证

```python
claims = jwt.decode(token, public_key, algorithms=["RS256"])
# 必验证的字段
assert claims["iss"] == "https://auth.example.com"  # 签发者
assert claims["aud"] == "https://api.example.com"    # 接收者
assert claims["exp"] > time.time()                   # 过期时间
assert claims["nbf"] < time.time()                   # 生效时间
```

### 避免在Payload中存放敏感信息

JWT的Payload只是Base64URL编码（不是加密），任何人解码后都能读取。不要在Payload中存放密码、信用卡号等敏感信息。

## 最佳实践总结

1. 使用RS256非对称签名算法
2. Access Token短过期（15-30分钟）
3. Refresh Token实施轮转和重用检测
4. 验证所有标准Claims（iss、aud、exp）
5. 不使用`alg: none`
6. 不在Payload中存敏感数据
7. 实施令牌黑名单机制

JWT认证的安全关键在于正确地实施每个环节，而不是依赖某个单一机制。
