---
title: "Web Security Fundamentals 2026: A Developer's Complete Guide"
description: "Everything developers need to know about web security in 2026 — OWASP Top 10, authentication, encryption, CSP, and production security patterns."
date: 2026-05-11
board: security
url: https://dingjiu1989-hue.github.io/en/security/web-security-fundamentals-2026.html
---

## Introduction

Web security is not a feature — it is a discipline. Every developer shipping code to the internet in 2026 must understand the threat landscape, the tools to defend against it, and the patterns that turn fragile applications into hardened systems. This guide covers the topics that matter most: from OWASP Top 10 vulnerabilities to production-grade security headers, from JWT best practices to dependency scanning with SBOMs.

Whether you are building a Next.js dashboard, a FastAPI backend, or a static Jamstack site, the principles here apply directly to your stack.

---

## 1. OWASP Top 10 (2025 Edition) Overview

The OWASP Top 10 is the industry-standard awareness document for web application security. Here is the 2025 list with practical examples and mitigations.

| Rank | Category | Example |
|------|----------|---------|
| 1 | Broken Access Control | User A reads User B's private data by changing an ID in the URL |
| 2 | Cryptographic Failures | Storing passwords in plaintext or using MD5 |
| 3 | Injection | SQL injection via unsanitized search input |
| 4 | Insecure Design | No rate limiting on password reset endpoints |
| 5 | Security Misconfiguration | Default credentials left in production |
| 6 | Vulnerable Components | Using a library with a known CVE |
| 7 | Auth & Session Failures | JWT secrets leaked in client-side code |
| 8 | Data Integrity Failures | Accepting unsigned serialized objects (e.g., Pickle) |
| 9 | Logging & Monitoring Failures | No alerting on repeated 403s |
| 10 | SSRF | Server fetches attacker-controlled URL internally |

**Example: Broken Access Control (the #1 risk)**

```python
# BAD — no ownership check
@app.get("/api/orders/{order_id}")
def get_order(order_id: int):
    order = db.query(Order).get(order_id)
    return order

# GOOD — enforce ownership
@app.get("/api/orders/{order_id}")
def get_order(order_id: int, user=Depends(get_current_user)):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == user.id
    ).first()
    if not order:
        raise HTTPException(status_code=404)
    return order
```

**Key takeaway:** Never trust user-supplied identifiers. Always verify ownership server-side.

---

## 2. Authentication Security

Authentication is the most attacked surface area on any web application. Here are the patterns that hold up in production.

### JWT Best Practices

JSON Web Tokens are everywhere, but they are easy to misuse.

```javascript
// GOOD: JWT configuration for production
const jwt = require('jsonwebtoken');

const token = jwt.sign(
  { 
    sub: user.id,
    role: user.role,
    session_id: session.uuid   // allow server-side revocation
  },
  process.env.JWT_SECRET,      // never hardcode
  { 
    algorithm: 'RS256',        // asymmetric — never 'none' or 'HS256' in distributed systems
    expiresIn: '15m',          // short-lived access tokens
    issuer: 'myapp.example.com',
    audience: 'myapp-api'
  }
);
```

**JWT checklist:**
- Use `RS256` or `ES256` (asymmetric) for multi-service architectures
- Never store secrets in client-side JavaScript bundles
- Set short expiration (15 minutes for access tokens)
- Implement refresh token rotation
- Blacklist compromised tokens server-side using a session store

### Session Management Comparison

| Approach | Best For | Weakness |
|----------|----------|----------|
| HTTP-only cookies + session ID | Server-rendered apps | Requires server-side store |
| JWT access + refresh tokens | SPAs, mobile apps | Revocation is harder |
| OAuth2 + PKCE | Third-party auth | Complexity |
| WebAuthn / Passkeys | High-security apps | Browser support gaps |

### OAuth2 with PKCE (Recommended Flow)

```javascript
// Authorization code flow with PKCE (Proof Key for Code Exchange)
const crypto = require('crypto');

function generatePKCE() {
  const verifier = crypto.randomBytes(32).toString('base64url');
  const challenge = crypto
    .createHash('sha256')
    .update(verifier)
    .digest('base64url');
  return { verifier, challenge };
}

// Step 1: Redirect user with code_challenge
// GET https://provider.com/auth?response_type=code&code_challenge=<challenge>&code_challenge_method=S256

// Step 2: Exchange code for token (verifier must match)
// POST https://provider.com/token
// Body: { code, code_verifier: verifier, client_id, redirect_uri }
```

**Never use the implicit grant (deprecated).** Always use the authorization code flow with PKCE, even for first-party apps.

---

## 3. Content Security Policy (CSP)

CSP is your last line of defense against XSS. It tells the browser what sources are allowed to load scripts, styles, fonts, and other resources.

### Baseline CSP Header

```
Content-Security-Policy: 
  default-src 'self';
  script-src 'self' https://cdn.example.com;
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https://images.example.com;
  connect-src 'self' https://api.example.com;
  font-src 'self' https://fonts.gstatic.com;
  frame-ancestors 'none';
  base-uri 'self';
  form-action 'self';
  object-src 'none'
```

### How to Set CSP in Popular Frameworks

```javascript
// Express.js
app.use((req, res, next) => {
  res.setHeader(
    'Content-Security-Policy',
    "default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'"
  );
  next();
});
```

```python
# FastAPI middleware
from starlette.middleware.base import BaseHTTPMiddleware

class CSPSecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self'; "
            "object-src 'none'; "
            "frame-ancestors 'none'"
        )
        return response
```

### CSP Pitfalls to Avoid

| Anti-Pattern | Why It Hurts |
|---|---|
| `script-src 'unsafe-inline'` | Defeats CSP — any inline script runs |
| `script-src 'unsafe-eval'` | Allows `eval()` and similar |
| Using `https:` as a whitelist | Too broad — allows any HTTPS-hosted script |
| Missing `object-src 'none'` | Flash/Silverlight plugins bypass CSP |
| Not using `report-uri` / `report-to` | You never know when CSP blocks something legitimate |

**Pro tip:** Deploy CSP in report-only mode first (`Content-Security-Policy-Report-Only`), monitor violations, then enforce. This prevents breaking your production site.

---

## 4. CORS Configuration Best Practices

CORS is not a security boundary — it is a browser-enforced access control mechanism. It does not protect your API from direct requests (curl, Postman), only from cross-origin browser requests.

### Correct CORS Configuration

```javascript
// Express.js — production CORS setup
const cors = require('cors');

const corsOptions = {
  origin: process.env.ALLOWED_ORIGINS.split(','),  // explicit, not '*'
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Authorization', 'Content-Type'],
  exposedHeaders: ['X-Request-ID'],
  credentials: true,           // only if you need cookies
  maxAge: 86400                // preflight cache — 24 hours
};

app.use(cors(corsOptions));
```

```python
# FastAPI
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
    allow_credentials=False,
    max_age=86400,
)
```

### CORS Rules of Thumb

- Never use `Access-Control-Allow-Origin: *` with credentials
- Never reflect the `Origin` header back blindly (this enables attacks on intranet apps)
- Whitelist specific origins, not wildcard patterns like `*.example.com` (DNS rebinding attacks)
- If your API does not use cookies, keep `credentials: false`
- Use `Vary: Origin` so CDNs cache per-origin responses correctly

---

## 5. SQL Injection Prevention

SQL injection is the oldest trick in the book, and it still works because developers concatenate user input into SQL strings.

### Never Do This

```python
# VULNERABLE — never concatenate user input
username = request.form["username"]
query = f"SELECT * FROM users WHERE username = '{username}'"
cursor.execute(query)
```

An attacker sends `' OR '1'='1` and the WHERE clause becomes `WHERE username = '' OR '1'='1'` — every row in the table is returned.

### Always Do This

```python
# SAFE — parameterized queries
cursor.execute(
    "SELECT * FROM users WHERE username = %s",
    (username,)
)
```

```javascript
// SAFE — parameterized queries with node-postgres
const result = await db.query(
  'SELECT * FROM users WHERE username = $1',
  [username]
);
```

### ORMs Are Not Magic Bullets

ORMs protect against basic SQLi but can still leak data through:

- **Raw queries** — `Model.raw('SELECT ...')` must use bind parameters
- **Dynamic column/table names** — cannot be parameterized; whitelist them
- **`$where` in MongoDB** — injection via `$gt`, `$ne`, `$where` operators

```javascript
// VULNERABLE — NoSQL injection
app.get('/api/users', async (req, res) => {
  const { username } = req.query;
  // If username is { "$ne": "" }, this returns ALL users
  const users = await User.find({ username });
  res.json(users);
});
```

**Fix:** Validate that the input is a string, not an object or operator expression.

---

## 6. XSS Types and Prevention

Cross-Site Scripting (XSS) remains pervasive. There are three distinct types.

### Reflected XSS

The payload is part of the request (e.g., URL query parameter) and reflected in the response immediately.

```
Example: https://example.com/search?q=<script>alert('xss')</script>
```

### Stored XSS

The payload is persisted on the server (e.g., in a comment, user bio) and served to every visitor.

```
Example: A comment containing <script>fetch('/api/steal').then(...)</script>
```

### DOM-Based XSS

The vulnerability lives entirely in client-side JavaScript. The server response is clean, but the browser executes attacker-controlled input via `innerHTML`, `document.write`, or `eval`.

```javascript
// VULNERABLE — DOM XSS
const name = new URLSearchParams(window.location.search).get('name');
document.getElementById('greeting').innerHTML = `Hello, ${name}`;

// SAFE — use textContent, not innerHTML
document.getElementById('greeting').textContent = `Hello, ${name}`;
```

### XSS Prevention Table

| Context | Safe Approach | Dangerous Approach |
|---------|--------------|-------------------|
| HTML body | `textContent`, template escaping | `innerHTML`, `outerHTML` |
| HTML attribute | `setAttribute()` with safe values | String concatenation into `onclick` or `href` |
| JavaScript string | JSON.stringify + proper encoding | Direct concatenation into `eval` or `setTimeout` string |
| CSS | Use CSS custom properties | Dynamic `url()` or `expression()` |
| URL | Validate against allowlist | `javascript:` URLs in `<a href>` |

**Defense in depth:** CSP + output encoding + input validation. No single layer is enough.

---

## 7. HTTPS/TLS Fundamentals

HTTPS is non-negotiable in 2026. Every site should be HTTPS-only with HSTS.

### What Every Developer Needs to Know

| Concept | What It Means |
|---------|---------------|
| TLS 1.3 | Current standard. Faster handshake, removed insecure ciphers. |
| Certificate validation | The client verifies the cert chain against trusted CAs |
| SNI | Server Name Indication — lets one server host multiple TLS certs |
| HSTS | HTTP Strict Transport Security — tells browsers to always use HTTPS |
| OCSP Stapling | Server sends proof of cert validity during handshake |

### Setting Up HSTS

```
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
```

- `max-age` in seconds (2 years = 63072000)
- `includeSubDomains` — covers all subdomains
- `preload` — submit your domain to browser preload lists

### Redirect HTTP to HTTPS

```javascript
// Express.js
app.use((req, res, next) => {
  if (!req.secure && req.headers['x-forwarded-proto'] !== 'https') {
    return res.redirect(301, `https://${req.headers.host}${req.url}`);
  }
  next();
});
```

### TLS Configuration Check (2026 Minimum)

```nginx
# nginx TLS config — modern profile
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
ssl_prefer_server_ciphers off;
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 1d;
ssl_session_tickets off;
ssl_stapling on;
ssl_stapling_verify on;
```

Test your TLS setup with: `openssl s_client -connect example.com:443 -tls1_3`

---

## 8. Dependency Scanning and SBOM

Supply chain attacks are the fastest-growing threat vector. In 2026, the US Executive Order on cybersecurity and global regulations require Software Bills of Materials (SBOM) for production software.

### Dependency Scanning Tools

| Tool | Scope | Integration |
|------|-------|-------------|
| `npm audit` / `yarn audit` | Node.js packages | CI/CD pipeline gate |
| `pip-audit` | Python packages | pre-commit hooks |
| `trivy` | Containers, OS packages, IaC | GitHub Actions, GitLab CI |
| `snyk` | Multi-language, container | PR checks |
| `dependabot` | GitHub-hosted repos | Auto-PRs for vulnerable deps |
| `grype` | Containers, filesystem | Fast, free, OSS |

### Running a Scan in CI

```yaml
# .github/workflows/security-scan.yml
name: Security Scan
on: [push, pull_request]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'
      - name: Generate SBOM
        uses: anchore/sbom-action@v0
        with:
          format: 'spdx-json'
          output-file: 'sbom.spdx.json'
```

### What Goes Into an SBOM

```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.5",
  "metadata": {
    "component": {
      "name": "my-app",
      "version": "1.2.3",
      "type": "application"
    }
  },
  "components": [
    {
      "name": "express",
      "version": "4.18.2",
      "type": "library",
      "purl": "pkg:npm/express@4.18.2"
    }
  ]
}
```

**Action item:** Run `pip freeze > requirements.txt` or `npm list --json > deps.json` and pipe it through an SBOM generator in your CI pipeline. Store the SBOM alongside your release artifact.

---

## 9. Security Headers Checklist

Apply these HTTP response headers to every page and every API response.

| Header | Value | Purpose |
|--------|-------|---------|
| `Strict-Transport-Security` | `max-age=63072000; includeSubDomains` | Enforce HTTPS |
| `Content-Security-Policy` | See Section 3 | Prevent XSS and data injection |
| `X-Content-Type-Options` | `nosniff` | Prevent MIME type sniffing |
| `X-Frame-Options` | `DENY` | Prevent clickjacking |
| `X-XSS-Protection` | `0` | Disable legacy XSS filter (does more harm than good) |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Control referrer data leakage |
| `Permissions-Policy` | `camera=(), microphone=(), geolocation=()` | Restrict browser API access |
| `Cache-Control` | `no-store, no-cache, must-revalidate` | Prevent sensitive data caching |

### Apply Them in One Shot

```javascript
// Express.js helmet — sets most security headers automatically
const helmet = require('helmet');
app.use(helmet());

// Or set manually for fine control
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
  res.setHeader('Permissions-Policy', 'camera=(), microphone=(), geolocation=()');
  next();
});
```

```python
# FastAPI with SecureHeaders middleware
from secure import SecureHeaders

secure_headers = SecureHeaders()

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    secure_headers.framework.fastapi(response)
    return response
```

---

## 10. API Security Basics

APIs are the backbone of modern web applications and a prime attack target.

### Rate Limiting

```javascript
// Express.js with express-rate-limit
const rateLimit = require('express-rate-limit');

const globalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,      // 15 minutes
  max: 100,                       // limit each IP
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Too many requests' }
});

const authLimiter = rateLimit({
  windowMs: 60 * 1000,            // 1 minute
  max: 5,                         // 5 attempts per minute
  message: { error: 'Too many auth attempts' }
});

app.use('/api/', globalLimiter);
app.use('/api/auth/login', authLimiter);
```

### Input Validation

Use a schema validation library. Never trust incoming data.

```javascript
// Zod validation — reject unexpected fields and bad types
const { z } = require('zod');

const CreateUserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(12).max(128),
  role: z.enum(['user', 'admin']).default('user'),
}).strict();  // strips or rejects extra fields

app.post('/api/users', (req, res) => {
  const parsed = CreateUserSchema.parse(req.body);
  // parsed is now type-safe and validated
});
```

### Proper Error Handling

Never leak stack traces, database schemas, or internal paths to API consumers.

```python
# BAD — leaks internals
@app.exception_handler(Exception)
async def debug_error(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "traceback": traceback.format_exc()}
    )

# GOOD — sanitized errors with logging
import logging
logger = logging.getLogger(__name__)

@app.exception_handler(HTTPException)
async def http_error(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.exception_handler(Exception)
async def generic_error(request, exc):
    logger.error("Internal error", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "An internal error occurred"}
    )
```

### API Security Checklist

- [ ] Rate limiting on all endpoints (stricter on auth)
- [ ] Input validation with schema library (Zod, Pydantic, Marshmallow)
- [ ] Structured error responses — no stack traces
- [ ] Authentication on every endpoint (no unprotected internal routes)
- [ ] Audit logging for sensitive operations
- [ ] Request size limits (`body-parser` `limit` option, nginx `client_max_body_size`)
- [ ] API keys stored server-side only, rotated regularly
- [ ] UUIDs instead of auto-increment IDs in URLs

---

## 11. Production Security Checklist

A practical runbook to harden any web application before launch.

### Infrastructure

- [ ] All traffic is HTTPS (HSTS preloaded)
- [ ] TLS 1.2 minimum, TLS 1.3 preferred
- [ ] No default credentials on any service (database, Redis, admin panels)
- [ ] Database is not publicly accessible (private subnet / VPC)
- [ ] Secrets stored in a vault / secrets manager (not in `.env` files in repos)
- [ ] Container images scanned for CVEs before deployment

### Application

- [ ] All user input is validated and sanitized
- [ ] Parameterized queries everywhere — no SQL string concatenation
- [ ] Authentication uses short-lived tokens with rotation
- [ ] Session tokens stored in HTTP-only, Secure, SameSite cookies
- [ ] CSP header is enforced (not just report-only)
- [ ] CORS origins are explicitly whitelisted
- [ ] File uploads are restricted to allowed types and scanned
- [ ] File uploads stored outside the web root with random filenames
- [ ] IDs are UUIDs not sequential integers
- [ ] Logs contain no PII, tokens, or passwords
- [ ] Rate limiting is active on all endpoints

### Process

- [ ] Dependency scanning runs on every PR
- [ ] SBOM is generated with each release
- [ ] Secrets scanning (e.g., `git secrets`, `truffleHog`) in CI
- [ ] Regular penetration tests (at least annually)
- [ ] Incident response plan documented
- [ ] Dependabot or Renovate configured for auto-updates

---

## Conclusion

Web security in 2026 is about layers. No single header, library, or practice will protect your application. The combination of CSP + parameterized queries + short-lived tokens + dependency scanning + proper CORS configuration + HSTS creates a defense-in-depth posture that raises the bar for attackers.

Start with the production checklist above and work through each item. Automate everything you can — security scanning in CI, dependency updates, SBOM generation. The goal is not perfect security (it does not exist), but rather making your application resilient enough that attackers move on to an easier target.

**Remember:** security is not a one-time audit. It is a continuous practice embedded into your development workflow. Ship safely.

---

*Last updated: May 2026*
