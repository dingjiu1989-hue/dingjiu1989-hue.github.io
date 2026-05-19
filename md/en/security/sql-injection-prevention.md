---
title: "SQL Injection Prevention Guide"
description: "Comprehensive guide to preventing SQL injection attacks with parameterized queries, ORM protections, input validation, and WAF rules."
date: 2025-12-19
board: security
url: https://dingjiu1989-hue.github.io/en/security/sql-injection-prevention.html
---

# SQL Injection Prevention Guide

Understanding SQL Injection 

SQL injection is a code injection technique where an attacker inserts malicious SQL statements into application queries. It has been the top vulnerability in the OWASP Top 10 for years and remains one of the most damaging attack vectors despite being well-understood. 

How It Works 

Consider a vulnerable login query built by string concatenation: 

String query = "SELECT * FROM users WHERE email = '" + email + "' AND password = '" + password + "'";

An attacker providing `email = admin@example.com' --` comments out the password check, logging in as admin without knowing the password. Worse, providing `email = '; DROP TABLE users; --` could destroy the database entirely. 

Defense Layer 1: Parameterized Queries 

Parameterized queries (also called prepared statements) separate SQL logic from data. User input is always treated as data, never as executable code. 

Node.js (mysql2) 

const mysql = require('mysql2/promise');

const connection = await mysql.createConnection({ /_config_ / });

const [rows] = await connection.execute(

'SELECT * FROM users WHERE email = ? AND password_hash = ?',

[email, passwordHash]

);

Python (psycopg2) 

import psycopg2

conn = psycopg2.connect("dbname=test user=postgres")

cur = conn.cursor()

cur.execute(

"SELECT * FROM users WHERE email = %s AND status = %s",

(user_email, 'active')

)

Java (JDBC) 

String sql = "SELECT * FROM products WHERE category = ? AND price < ?";

PreparedStatement stmt = connection.prepareStatement(sql);

stmt.setString(1, category);

stmt.setBigDecimal(2, maxPrice);

ResultSet rs = stmt.executeQuery();

Go (database/sql) 

rows, err := db.Query(

"SELECT * FROM users WHERE email = $1 AND active = $2",

email, true,

)

Defense Layer 2: ORM Protections 

Modern ORMs provide built-in protection against SQL injection when used correctly. 

Django ORM 

## Safe: ORM parameterizes automatically

users = User.objects.filter(email=user_input, is_active=True)

## Safe: Raw queries with parameters

users = User.objects.raw(

'SELECT * FROM auth_user WHERE email = %s', [user_input]

)

## UNSAFE: String interpolation bypasses protections

users = User.objects.raw(f'SELECT * FROM auth_user WHERE email = "{user_input}"')

SQLAlchemy 

## Safe

result = session.execute(

text("SELECT * FROM users WHERE email = :email"),

{"email": user_input}

)

## UNSAFE

result = session.execute(

text(f"SELECT * FROM users WHERE email = '{user_input}'")

)

Defense Layer 3: Input Validation 

Parameterized queries prevent SQL injection in most cases, but input validation provides defense in depth. 

import re

def validate_username(username):

"""Allow only alphanumeric and underscore."""

if not re.match(r'^[a-zA-Z0-9_]{3,30}$', username):

raise ValueError("Invalid username format")

return username

Defense Layer 4: Stored Procedures 

Stored procedures can add an abstraction layer between queries and user input. 

CREATE PROCEDURE GetUserByEmail(IN user_email VARCHAR(255))

BEGIN

SELECT id, username, email

FROM users

WHERE email = user_email AND deleted_at IS NULL;

END

cursor.callproc('GetUserByEmail', [email])

Note that stored procedures must still use parameterized calls internally. A stored procedure that concatenates strings is still vulnerable. 

Defense Layer 5: Least Privilege 

Limit database account permissions so that a successful injection causes minimal damage: 

| Account | Permissions | Purpose | |---------|-------------|---------| | app_read | SELECT only | Read-only queries | | app_write | SELECT, INSERT, UPDATE | Write operations | | app_admin | SELECT, INSERT, UPDATE, DELETE | Admin functions | | migration | DDL (CREATE, ALTER, DROP) | Schema migrations only | 

Never use the database root or admin account for application connections. 

Advanced Threats 

Second-Order SQL Injection 

Data stored in the database can later be used unsafely in a different query. Parameterized queries on all queries mitigate this. 

Blind SQL Injection 

Attackers infer information through boolean or time-based responses. Use uniform error messages and prevent timing-based inference by adding random delays. 

Detection Tools 

| Tool | Type | Coverage | |------|------|----------| | SQLMap | Automated exploitation testing | Dynamic analysis | | OWASP ZAP | DAST scanner | Runtime detection | | SonarQube | SAST | Static code analysis | | Semgrep | SAST | Custom rule patterns | 

## Scan Go code for string concatenation in SQL queries

semgrep --config "p/sql-injection" .

Summary 

SQL injection is entirely preventable. Parameterized queries are the single most effective defense and should be the default pattern for every database interaction. Layer in ORM protections, input validation, least-privilege database accounts, and static analysis tools to create defense-in-depth. Never concatenate user input directly into SQL strings, and train every developer on these principles from day one.

**See also:** [XSRF/CSRF Protection Guide](</en/security/xsrf-csrf-protection.html>), [Encryption at Rest Guide](</en/security/encryption-at-rest.html>), [Two-Factor Authentication Guide](</en/security/two-factor-authentication.html>).

**See also:** [API Rate Limiting Implementation](</en/security/api-rate-limiting.html>), [Two-Factor Authentication Guide](</en/security/two-factor-authentication.html>), [XSRF/CSRF Protection Guide](</en/security/xsrf-csrf-protection.html>)

**See also:** [API Rate Limiting Implementation](</en/security/api-rate-limiting.html>), [Two-Factor Authentication Guide](</en/security/two-factor-authentication.html>), [XSRF/CSRF Protection Guide](</en/security/xsrf-csrf-protection.html>)

**See also:** [API Rate Limiting Implementation](</en/security/api-rate-limiting.html>), [Two-Factor Authentication Guide](</en/security/two-factor-authentication.html>), [XSRF/CSRF Protection Guide](</en/security/xsrf-csrf-protection.html>)

**See also:** [API Rate Limiting Implementation](</en/security/api-rate-limiting.html>), [Two-Factor Authentication Guide](</en/security/two-factor-authentication.html>), [XSRF/CSRF Protection Guide](</en/security/xsrf-csrf-protection.html>)

**See also:** [API Rate Limiting Implementation](</en/security/api-rate-limiting.html>), [Two-Factor Authentication Guide](</en/security/two-factor-authentication.html>), [XSRF/CSRF Protection Guide](</en/security/xsrf-csrf-protection.html>)

**See also:** [RBAC Authorization Implementation](</en/security/rbac-authorization.html>), [Webhook Security Best Practices](</en/security/webhook-security.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)

**See also:** [RBAC Authorization Implementation](</en/security/rbac-authorization.html>), [Webhook Security Best Practices](</en/security/webhook-security.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)

**See also:** [RBAC Authorization Implementation](</en/security/rbac-authorization.html>), [Webhook Security Best Practices](</en/security/webhook-security.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)

**See also:** [RBAC Authorization Implementation](</en/security/rbac-authorization.html>), [Webhook Security Best Practices](</en/security/webhook-security.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)

**See also:** [RBAC Authorization Implementation](</en/security/rbac-authorization.html>), [Webhook Security Best Practices](</en/security/webhook-security.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)
