---
title: "密码安全：哈希算法选择、加盐、密码策略设计"
description: "系统讲解密码安全的最佳实践，涵盖密码哈希算法选型、加盐技术、密码策略设计、防暴力破解机制和安全存储方案。"
date: 2026-05-12
board: security
url: https://dingjiu1989-hue.github.io/zh/security/mi-ma-anquan.html
---

## 密码安全的重要性

密码泄露是企业数据泄露事件中最常见的原因之一。安全存储用户密码是应用安全的基本底线。

## 密码哈希算法

### 为什么不能使用MD5/SHA-1/SHA-256

这些通用哈希算法设计目标是速度快，正是这个特性让它们不适合密码存储。攻击者可以在短时间内计算数十亿次哈希，轻松破解弱密码。

### 专用密码哈希算法

**bcrypt（推荐）：**
- 内置加盐机制
- 可调节的工作因子（cost factor）
- 对GPU/ASIC攻击有天然抵抗力
- 当前推荐cost值为10-12

```python
import bcrypt

# 哈希密码
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))

# 验证密码
bcrypt.checkpw(password.encode(), hashed)
```

**Argon2（更推荐）：**
- 2015年密码哈希竞赛冠军
- 抗GPU、抗ASIC、抗侧信道攻击
- 支持配置内存、时间和并行度参数

```python
from argon2 import PasswordHasher

ph = PasswordHasher(
    time_cost=3,      # 迭代次数
    memory_cost=65536, # 内存使用（KB）
    parallelism=4,    # 并行度
    hash_len=32
)

hashed = ph.hash(password)
ph.verify(hashed, password)
```

**scrypt：**
- 内存密集型算法
- 广泛应用于加密货币领域

### 算法选择建议

1. **首选Argon2id**（最安全）
2. **次选bcrypt**（广泛支持）
3. 不要使用MD5、SHA系列、PBKDF2（除非兼容旧系统）

## 加盐技术

### 盐的作用

盐是随机生成的字符串，与密码拼接后再哈希。即使两个用户设置了相同密码，加盐后得到不同的哈希值。

### 盐的生成

```python
import os

# 生成16字节的随机盐
salt = os.urandom(16)
```

### 盐的存储

盐不需要保密，应存储在哈希值旁边。大多数密码哈希库会自动处理盐的生成和存储。

## 密码策略设计

### 最小长度优先

现代密码安全研究表明：密码长度比复杂度更重要。建议：
- 最短长度：8个字符
- 推荐长度：12个字符以上
- 使用密码短语（passphrase）而非密码

### 不要强制复杂度

强制要求包含大小写、数字和特殊字符的策略会让用户更倾向于使用"Password1!"这样的可预测模式。建议：
- 不强制字符类型多样性
- 使用密码强度指示器引导用户
- 检查密码是否在已知泄露列表中

### 防泄露检查

```python
# 检查密码是否被泄露
import requests

def is_password_pwned(password):
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    resp = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
    return suffix in resp.text
```

## 防暴力破解

### 速率限制

- 同一IP每分钟最多5次登录尝试
- 同一账号每小时最多10次尝试
- 连续失败后增加延迟时间

### 账户锁定

- 5次失败后临时锁定15分钟
- 24小时内累计10次失败后锁定1小时
- 提供解锁流程（邮箱验证）

### 多因素认证

在密码之外增加第二认证因素，是防御密码泄露最有效的方法。包括：TOTP验证码、短信验证码、硬件密钥（WebAuthn/FIDO2）。

## 安全存储实践

1. 绝不明文存储密码
2. 使用专用的密码哈希算法（Argon2/bcrypt）
3. 自动生成和管理盐值
4. 不使用客户端的密码哈希（必须HTTPS传输原文）
5. 密码重置时发送临时链接而非原始密码
6. 密码变更时通知用户

密码安全涉及用户数据的核心安全，每个细节都值得认真对待。
