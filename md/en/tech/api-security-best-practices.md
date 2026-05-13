---
title: "API Security Best Practices 2026: JWT, Rate Limiting, Input Validation, and OWASP for APIs"
description: "Complete API security guide covering JWT authentication, RBAC authorization, rate limiting, input validation, CORS, SQL injection prevention, and secrets management with code examples."
date: 2026-05-09
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/api-security-best-practices.html
---

# API Security Best Practices 2026: JWT, Rate Limiting, Input Validation, and OWASP for APIs

APIs are the front door to your application — and the #1 attack surface in 2026. This guide covers the security practices every API developer must implement, from authentication to rate limiting to input validation, with concrete code examples.

## 1\. Authentication: JWT Done Right

JWTs are ubiquitous, but most implementations are vulnerable. Here are the rules: always set an expiration (`exp`) claim — never issue eternal tokens; always validate the `iss` (issuer) and `aud` (audience) claims — don't accept tokens issued for other services; never accept `alg: none` — explicitly whitelist your signing algorithm; use RS256 or ES256, not HS256 with a weak secret; store refresh tokens in an httpOnly, Secure, SameSite=Strict cookie, never in localStorage.
    
    
    const jwt = require('jsonwebtoken');
    
    function createToken(user) {
      return jwt.sign(
        { sub: user.id, role: user.role },
        process.env.JWT_PRIVATE_KEY,
        { algorithm: 'RS256', expiresIn: '15m', issuer: 'api.example.com', audience: 'app.example.com' }
      );
    }
    
    function verifyToken(token) {
      return jwt.verify(token, process.env.JWT_PUBLIC_KEY, {
        algorithms: ['RS256'],
        issuer: 'api.example.com',
        audience: 'app.example.com'
      });
    }

## 2\. Authorization: RBAC and ABAC

Never trust the client to enforce authorization. Every API endpoint must verify: is this user authenticated? Does this user have permission for this action on this resource? Implement role-based access control (RBAC) for simple cases: admin, editor, viewer. For complex cases, use attribute-based access control (ABAC): "Can this user edit this document if the document is in draft status and the user is in the same department?"
    
    
    function authorize(user, action, resource) {
      if (user.role === 'admin') return true;
      if (action === 'read' && resource.public) return true;
      if (action === 'write' && resource.ownerId === user.id) return true;
      if (action === 'write' && resource.departmentId === user.departmentId && user.role === 'editor') return true;
      return false;
    }

## 3\. Rate Limiting: Stop Abuse Before It Starts

Every public API endpoint needs rate limiting. Without it, a single misconfigured client can take down your service. Use the token bucket or sliding window algorithm — fixed window is too bursty. Rate limit by: IP address (basic), API key (better), user ID + endpoint (best). Return standard headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, and `Retry-After` when throttled. Return HTTP 429 (Too Many Requests), not 200 with an error body.
    
    
    const rateLimit = require('express-rate-limit');
    const RedisStore = require('rate-limit-redis');
    
    const limiter = rateLimit({
      store: new RedisStore({ client: redisClient }),
      windowMs: 60 * 1000,
      max: 100,              // 100 requests per minute
      standardHeaders: true,
      legacyHeaders: false,
      keyGenerator: (req) => req.user?.id || req.ip,
      handler: (req, res) => {
        res.status(429).json({
          error: 'Too many requests. Retry after 60 seconds.',
          retryAfter: 60
        });
      }
    });

## 4\. Input Validation: Never Trust the Client

The #1 cause of API vulnerabilities is trusting user input. Validate everything: type (is this a string? number?), format (is this a valid email? UUID?), length (is this under the max?), range (is this number between 1 and 100?), and business rules (is this status transition allowed?). Use a schema validation library — never write validation by hand. Zod (TypeScript), Pydantic (Python), or Joi (Node.js) — pick one and use it on every endpoint.
    
    
    import { z } from 'zod';
    
    const CreateUserSchema = z.object({
      email: z.string().email().max(255),
      name: z.string().min(1).max(100).regex(/^[a-zA-Z\s-]+$/),
      age: z.number().int().min(13).max(120),
      role: z.enum(['user', 'editor', 'admin']),
      website: z.string().url().optional()
    });
    
    function createUser(req, res) {
      const result = CreateUserSchema.safeParse(req.body);
      if (!result.success) {
        return res.status(400).json({
          error: 'Validation failed',
          details: result.error.flatten().fieldErrors
        });
      }
      // result.data is now guaranteed valid
    }

## 5\. CORS: Be Strict, Not Permissive

Never use `Access-Control-Allow-Origin: *` on an API that uses cookies or tokens. Specify exact origins. Never echo back the `Origin` header without whitelisting. Don't allow `Access-Control-Allow-Credentials: true` with a wildcard origin. For public APIs that legitimately need broad access, use API keys (in headers) rather than cookies, so CORS isn't the security boundary.

## 6\. SQL Injection: Still Relevant in 2026

Parameterized queries eliminate SQL injection. Never concatenate user input into SQL strings. ORMs help but aren't foolproof — raw queries with string interpolation are still common in ORM codebases. Always use parameterized queries or the ORM's safe query builder.
    
    
    // BAD - SQL injection vulnerable
    const query = `SELECT * FROM users WHERE email = '${req.body.email}'`;
    
    // GOOD - Parameterized query
    const query = 'SELECT * FROM users WHERE email = $1';
    const result = await db.query(query, [req.body.email]);
    
    // GOOD - ORM safe query (Prisma)
    const user = await prisma.user.findUnique({ where: { email: req.body.email } });

## 7\. HTTPS and TLS: Non-Negotiable

Serve everything over HTTPS. Redirect HTTP to HTTPS with HSTS (`Strict-Transport-Security: max-age=31536000; includeSubDomains`). Use TLS 1.3 minimum. GitHub Pages handles this automatically, but if you self-host, use Let's Encrypt with auto-renewal. Never disable certificate validation in your API client — even in development.

## 8\. Secrets Management

Never hardcode secrets. Use environment variables for local development, a secrets manager (AWS Secrets Manager, Doppler, Infisical) for production. Rotate secrets regularly. Never log secrets — configure your logger to redact known secret patterns. Never commit secrets to version control — use `.gitignore` and pre-commit hooks (detect-secrets, git-secrets) to catch them before they're pushed.

## 9\. Logging and Monitoring

Log every authentication attempt (success and failure). Log every authorization failure. Log every rate limit hit. Log every input validation failure. These four signals catch 80% of attacks in progress. Ship logs to a centralized system (Datadog, Grafana Loki, Better Stack) and set up alerts for anomaly spikes. A 10x increase in auth failures over 5 minutes is almost certainly a credential-stuffing attack.

## 10\. API Security Checklist

Category| Must Have| Nice to Have  
---|---|---  
Auth| JWT with expiry + RS256| OAuth 2.1, Passkeys  
AuthZ| RBAC per endpoint| ABAC, OPA/Rego policies  
Rate Limit| Per-user/IP, 429 response| Distributed rate limiting  
Validation| Schema validation on every input| OpenAPI spec as validation source  
CORS| Explicit origins, no wildcard| —  
SQL| Parameterized queries only| Read-only DB user for GET  
TLS| HTTPS only, HSTS| mTLS for service-to-service  
Secrets| Never in code, env vars only| Secrets manager with rotation  
Logging| Auth/authZ failures logged| Anomaly detection alerts  
Headers| CSP, X-Content-Type-Options| Permissions-Policy  
  
Security is not a feature you add — it's a property every endpoint must have. Start with the checklist above. Implement one item per sprint until they're all covered. The time to think about API security is before the breach, not after.
