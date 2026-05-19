---
title: "XSRF/CSRF Protection Guide"
description: "A practical guide to preventing Cross-Site Request Forgery attacks using CSRF tokens, SameSite cookies, and custom headers."
date: 2025-12-20
board: security
url: https://dingjiu1989-hue.github.io/en/security/xsrf-csrf-protection.html
---

# XSRF/CSRF Protection Guide

What Is CSRF? 

Cross-Site Request Forgery (CSRF or XSRF) is an attack that forces an authenticated user to execute unwanted actions on a web application. The attacker crafts a malicious page that, when visited by the victim, automatically submits a request to the target application using the victim's existing session cookies. 

Attack Scenario 

  * Alice logs into `bank.example.com` and has a valid session cookie.



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Alice visits `evil.com`, which contains an auto-submitting form targeting `bank.example.com/transfer`. 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. The browser automatically includes Alice's session cookie with the request. 4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. The bank processes the transfer, believing Alice authorized it. 

Defense 1: CSRF Tokens (Synchronizer Token Pattern) 

The server embeds a unique, unpredictable token in each form or request. The server validates the token on state-changing requests. 

Server-Side Implementation (Express) 

const crypto = require('crypto');

function generateCSRFToken(req) {

const token = crypto.randomBytes(32).toString('hex');

req.session.csrfToken = token;

return token;

}

function csrfMiddleware(req, res, next) {

if (['POST', 'PUT', 'DELETE', 'PATCH'].includes(req.method)) {

const token = req.headers['x-csrf-token']

|| req.body._csrfToken;

if (!token || token !== req.session.csrfToken) {

return res.status(403).json({

error: 'CSRF validation failed'

});

}

}

next();

}

HTML Form Usage 

Transfer

Framework Built-In Support 

Most modern frameworks include CSRF protection: 

## Django

{% csrf_token %} 

## Rails

<%= csrf_meta_tags %>

<%= hidden_field_tag :authenticity_token, form_authenticity_token %>

// Spring Security

@EnableWebSecurity

public class SecurityConfig {

@Bean

public SecurityFilterChain filterChain(HttpSecurity http) {

http.csrf(Customizer.withDefaults());

return http.build();

}

}

Defense 2: SameSite Cookies 

The `SameSite` cookie attribute tells the browser when to send cookies with cross-origin requests. 

| Attribute | Behavior | Security | |-----------|----------|----------| | `Strict` | Cookie sent only for same-site requests | Most secure, breaks some legitimate cross-site flows | | `Lax` | Cookie sent for top-level GET navigations | Good balance for most apps | | `None` | Cookie sent for all requests (requires Secure) | Insecure, use only when necessary | 

## Django settings

SESSION_COOKIE_SAMESITE = 'Lax'

CSRF_COOKIE_SAMESITE = 'Lax'

// Express with cookie-session

app.use(session({

cookie: {

sameSite: 'lax', // or 'strict'

secure: true,

httpOnly: true

}

}));

For most applications, `SameSite=Lax` provides strong CSRF protection without breaking user experience. Use `SameSite=Strict` for sensitive operations like password changes or money transfers. 

Defense 3: Custom Request Headers 

Single-page applications that use JavaScript for API calls can leverage custom headers as a CSRF defense. Browsers enforce the same-origin policy, preventing custom headers from being set by cross-origin requests without CORS preflight. 

// Client-side

fetch('/api/transfer', {

method: 'POST',

headers: {

'X-Requested-By': 'XMLHttpRequest',

'Content-Type': 'application/json'

},

body: JSON.stringify({ toAccount, amount }),

credentials: 'include'

});

// Server-side validation

app.post('/api/transfer', (req, res) => {

if (req.get('X-Requested-By') !== 'XMLHttpRequest') {

return res.status(403).json({ error: 'Invalid request origin' });

}

// Process transfer...

});

Defense 4: Origin and Referer Validation 

Check the `Origin` or `Referer` header on incoming requests: 

function validateOrigin(req) {

const origin = req.get('Origin');

const referer = req.get('Referer');

const allowed = ['https://example.com', 'https://app.example.com'];

if (origin && !allowed.includes(origin)) {

return false;

}

if (!origin && referer) {

const url = new URL(referer);

if (!allowed.includes(url.origin)) {

return false;

}

}

return true;

}

Defense Comparison 

| Method | Complexity | Browser Support | Protection Level | |--------|-----------|-----------------|------------------| | CSRF Token | Medium | Universal | Strong | | SameSite Cookie (Lax) | Low | 95%+ | Strong | | Custom Header | Low | Universal | Strong (CORS protected) | | Origin/Referer Check | Low | Universal | Moderate | 

For maximum protection, use CSRF tokens plus SameSite cookies. This covers both legacy browsers (no SameSite support) and modern browsers with the additional layer of SameSite protection. 

Summary 

CSRF attacks exploit the browser's automatic inclusion of credentials in cross-origin requests. Defend using synchronizer token patterns for traditional server-rendered apps, SameSite cookies for modern browsers, and custom headers for API-driven SPAs. The most robust approach combines CSRF tokens with SameSite cookies to protect users across all browser versions.

**See also:** [SQL Injection Prevention Guide](</en/security/sql-injection-prevention.html>), [HTTP Security Headers Checklist](</en/security/http-security-headers.html>), [Incident Response Playbook for Developers](</en/security/incident-response.html>).

**See also:** [SQL Injection Prevention Guide](</en/security/sql-injection-prevention.html>), [Web Security Basics: CORS, CSP, XSS, CSRF — What Every Developer Must Know](</en/tech/web-security-basics.html>), [Incident Response Playbook for Developers](</en/security/incident-response.html>)

**See also:** [SQL Injection Prevention Guide](</en/security/sql-injection-prevention.html>), [Web Security Basics: CORS, CSP, XSS, CSRF — What Every Developer Must Know](</en/tech/web-security-basics.html>), [Incident Response Playbook for Developers](</en/security/incident-response.html>)

**See also:** [SQL Injection Prevention Guide](</en/security/sql-injection-prevention.html>), [Web Security Basics: CORS, CSP, XSS, CSRF — What Every Developer Must Know](</en/tech/web-security-basics.html>), [Incident Response Playbook for Developers](</en/security/incident-response.html>)

**See also:** [SQL Injection Prevention Guide](</en/security/sql-injection-prevention.html>), [Web Security Basics: CORS, CSP, XSS, CSRF — What Every Developer Must Know](</en/tech/web-security-basics.html>), [Incident Response Playbook for Developers](</en/security/incident-response.html>)

**See also:** [SQL Injection Prevention Guide](</en/security/sql-injection-prevention.html>), [Web Security Basics: CORS, CSP, XSS, CSRF — What Every Developer Must Know](</en/tech/web-security-basics.html>), [Incident Response Playbook for Developers](</en/security/incident-response.html>)

**See also:** [RBAC Authorization Implementation](</en/security/rbac-authorization.html>), [Identity and Access Management (IAM) Guide](</en/security/identity-management.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>)

**See also:** [RBAC Authorization Implementation](</en/security/rbac-authorization.html>), [Identity and Access Management (IAM) Guide](</en/security/identity-management.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>)

**See also:** [RBAC Authorization Implementation](</en/security/rbac-authorization.html>), [Identity and Access Management (IAM) Guide](</en/security/identity-management.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>)

**See also:** [RBAC Authorization Implementation](</en/security/rbac-authorization.html>), [Identity and Access Management (IAM) Guide](</en/security/identity-management.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>)

**See also:** [RBAC Authorization Implementation](</en/security/rbac-authorization.html>), [Identity and Access Management (IAM) Guide](</en/security/identity-management.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>)

**See also:** [RBAC Authorization Implementation](</en/security/rbac-authorization.html>), [Identity and Access Management (IAM) Guide](</en/security/identity-management.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>)
