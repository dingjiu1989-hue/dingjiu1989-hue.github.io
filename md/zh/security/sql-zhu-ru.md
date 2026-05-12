---
title: "SQL注入防御：参数化查询、ORM安全、WAF配置"
description: "深入讲解SQL注入攻击的原理和防御措施，涵盖参数化查询的正确使用、ORM框架的安全配置和Web应用防火墙的策略设置。"
date: 2026-05-12
board: security
url: https://dingjiu1989-hue.github.io/zh/security/sql-zhu-ru.html
---

## SQL注入原理

SQL注入是最经典的Web安全漏洞之一，攻击者通过在输入中嵌入恶意SQL语句，操纵后端数据库执行非预期的查询。

## 参数化查询

参数化查询是防御SQL注入最有效的手段。

### Python示例

```python
# 不安全：字符串拼接
cursor.execute(f"SELECT * FROM users WHERE name = '{name}'")

# 安全：参数化查询
cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
```

### Node.js示例

```javascript
// 不安全
const sql = `SELECT * FROM users WHERE name = '${name}'`;

// 安全（使用mysql2）
const sql = 'SELECT * FROM users WHERE name = ?';
connection.execute(sql, [name]);
```

### Java示例

```java
// 安全：PreparedStatement
String sql = "SELECT * FROM users WHERE name = ?";
PreparedStatement ps = connection.prepareStatement(sql);
ps.setString(1, name);
ResultSet rs = ps.executeQuery();
```

### 原理说明

参数化查询将SQL语句和数据分离，数据库预编译SQL语句的语法结构，后续传入的参数只作为数据处理，不会改变SQL的语义。因此即使用户输入包含SQL关键字，也不会被执行。

## ORM安全

现代ORM框架（SQLAlchemy、Prisma、TypeORM、Hibernate）默认使用参数化查询，大大降低了SQL注入风险。

### 安全使用原则

**使用ORM的查询构建器：**

```python
# SQLAlchemy 安全示例
user = session.query(User).filter(User.name == name).first()
```

**避免原生SQL：**
- ORM框架的原生SQL方法（如`session.execute(raw_sql)`）绕过了参数化保护
- 不得已使用原生SQL时，确保使用参数化方式

### 常见ORM风险

1. **动态查询拼接**：根据条件动态拼接查询字符串
2. **排序参数**：`ORDER BY`后的字段名不能参数化，需要白名单校验
3. **批量操作**：批量删除或更新时的条件拼接

## WAF配置

Web应用防火墙（WAF）作为第二道防线，可以在请求到达应用之前拦截恶意输入。

### WAF规则配置

```nginx
# Nginx + ModSecurity 规则示例
SecRule REQUEST_FILENAME "\.(php|asp)" "id:1000"
SecRule ARGS "@detectSQLi" "id:1001,deny,msg:'SQL注入检测'"
```

### 云WAF

- **Cloudflare WAF**：预置SQL注入规则集
- **AWS WAF**：可与ALB和CloudFront集成
- **阿里云WAF**：中文场景最佳支持

### WAF的局限性

- 无法防御所有SQL注入变种
- 可能产生误报（阻断正常请求）
- 二次编码和分块传输可能绕过WAF

因此，WAF应作为补充防御，而非主要依赖。

## 其他防御措施

### 最小权限数据库账户

应用使用的数据库账户应遵循最小权限原则：
- 只读操作使用只读账户
- 仅授权必要的表
- 禁止使用`GRANT ALL`

### 输入验证

- 白名单验证：只接受预期格式的输入
- 类型检查：数字字段确保是数字类型
- 长度限制：防止缓冲区溢出攻击

### 错误信息处理

- 不要在生产环境中显示数据库错误信息
- 使用自定义错误页面
- 记录完整错误到日志便于排查

SQL注入虽然历史悠久，但至今仍是常见的安全漏洞。通过参数化查询、ORM安全和WAF的多层防御，可以有效消除SQL注入风险。
