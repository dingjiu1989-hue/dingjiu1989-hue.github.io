---
title: "Web Security Basics: CORS, CSP, XSS, CSRF — What Every Developer Must Know"
description: "Practical web security guide covering Cross-Site Scripting, CORS headers, Content Security Policy, SQL injection, and CSRF attacks. Includes code examples and prevention strategies."
date: 2025-10-08
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/web-security-basics.html
---

# Web Security Basics: CORS, CSP, XSS, CSRF — What Every Developer Must Know

Security isn't optional — it's part of your job as a developer. Most breaches exploit well-known vulnerabilities that have been understood for years. Here are the five web security threats every developer must understand, with prevention strategies and code examples.

## The Threat Landscape

Attack| Severity| OWASP Rank| What It Does  
---|---|---|---  
XSS (Cross-Site Scripting)| Critical| #2| Injects malicious scripts into your pages  
SQL Injection| Critical| #3| Executes arbitrary SQL on your database  
CSRF (Cross-Site Request Forgery)| High| Dropped| Tricks users into performing unwanted actions  
CORS Misconfiguration| High| #5| Allows unauthorized cross-origin access  
Insecure Authentication| Critical| #1| Weak auth allows account takeover  
  
## 1\. Cross-Site Scripting (XSS)

XSS happens when user input is rendered as HTML without sanitization. An attacker who can inject <script> tags can steal cookies, session tokens, and sensitive data.
    
    
    // ❌ Vulnerable:
    div.innerHTML = userComment;  // Attacker: <img src=x onerror="stealCookies()">
    
    // ✅ Safe:
    div.textContent = userComment;      // Escapes HTML automatically
    // Or sanitize:
    import DOMPurify from 'dompurify';
    div.innerHTML = DOMPurify.sanitize(userComment);

**React note:** JSX auto-escapes by default — you're safe from XSS in standard rendering. The danger is dangerouslySetInnerHTML and direct DOM manipulation.

## 2\. SQL Injection

Concatenating user input into SQL queries gives attackers full database access. Parameterized queries are the fix — use them 100% of the time.
    
    
    // ❌ Vulnerable — attacker input: "1; DROP TABLE users;"
    const query = `SELECT * FROM users WHERE id = ${userId}`;
    
    // ✅ Safe — parameterized query
    const query = "SELECT * FROM users WHERE id = $1";
    const result = await db.query(query, [userId]);
    // ORM users: Prisma/Drizzle parameterize automatically

## 3\. Cross-Site Request Forgery (CSRF)

An attacker's site makes a request to your API using the victim's cookies. CSRF tokens ensure the request originated from your own frontend.
    
    
    // Mitigation strategies:
    // 1. SameSite cookies (simplest, best):
    Set-Cookie: session=abc123; SameSite=Strict; HttpOnly; Secure
    
    // 2. CSRF token (additional layer):
    // Server sends a unique token; client includes it in requests
    // Modern frameworks (Next.js, Remix) handle this automatically
    
    // 3. Custom header requirement:
    // Browsers don't allow custom headers cross-origin
    // Require X-Requested-With or similar

## 4\. CORS Misconfiguration

CORS (Cross-Origin Resource Sharing) controls which origins can access your API. The most common mistake: using a wildcard or reflecting the Origin header blindly.
    
    
    // ❌ Vulnerable — allows any origin:
    Access-Control-Allow-Origin: *
    Access-Control-Allow-Credentials: true  // Can't use with *
    
    // ❌ Vulnerable — reflects origin blindly:
    // If your server echoes back the request's Origin header, any domain can access
    
    // ✅ Safe — explicit allowlist:
    const allowedOrigins = ["https://myapp.com", "https://admin.myapp.com"];
    const origin = req.headers.origin;
    if (allowedOrigins.includes(origin)) {
      res.setHeader("Access-Control-Allow-Origin", origin);
    }

## 5\. Content Security Policy (CSP)

CSP is your last line of defense. It tells the browser what sources of scripts, styles, and other resources are allowed. A well-configured CSP makes XSS exploitation nearly impossible.
    
    
    // Recommended CSP header:
    Content-Security-Policy:
      default-src 'self';
      script-src 'self' 'unsafe-inline' 'unsafe-eval' https://js.stripe.com;
      style-src 'self' 'unsafe-inline';
      img-src 'self' data: https:;
      font-src 'self';
      connect-src 'self' https://api.myapp.com;
      frame-src https://js.stripe.com;
      // NO 'unsafe-inline' for scripts in production (use nonce/hash)

## Security Checklist

  * **Authentication:** Use OAuth 2.0 / OIDC. Never roll your own crypto.
  * **Passwords:** bcrypt with cost factor 12+. Never store plaintext.
  * **HTTPS:** Everywhere. Redirect HTTP. HSTS header.
  * **Dependencies:** npm audit / snyk weekly. Auto-update minor patches.
  * **Environment variables:** Never commit .env files. Inject at runtime.
  * **Rate limiting:** Protect login and API endpoints from brute force.
  * **Logging:** Log auth events. Never log passwords or tokens.



**Bottom line:** Use parameterized queries, auto-escaping frameworks, SameSite cookies, CSP headers, and explicit CORS allowlists. Security is layers — implement them all, and a single failure won't compromise you. See also: [REST API Best Practices](</en/tech/rest-api-best-practices.html>) and [API Design Patterns](</en/tech/api-design-patterns.html>).

**See also:** [Testing Strategies for Web Apps: Unit, Integration, E2E, and When to Use Each](</en/tech/testing-strategies-web-apps.html>), [Web Authentication Best Practices 2026: JWT, OAuth 2.1, Passkeys](</en/tech/authentication-best-practices-2026.html>), [API Security Best Practices 2026: JWT, Rate Limiting, Input Validation, and OWASP for APIs](</en/tech/api-security-best-practices.html>)
