---
title: "API Security: Protecting Your REST and GraphQL APIs"
description: "API security best practices: authentication, authorization, rate limiting, input validation, and OWASP API Top 10."
date: 2026-03-20
board: security
url: https://dingjiu1989-hue.github.io/en/security/api-security-guide.html
---

# API Security: Protecting Your REST and GraphQL APIs

APIs are the primary attack surface for modern applications. API security must address authentication, authorization, input validation, and abuse prevention.

## Authentication

API keys identify API consumers. Generate unique keys per customer. Allow key rotation. Support multiple keys per account for staged transitions. Store keys as hashed values in your database—never store plaintext keys.

OAuth 2.0 provides delegated authorization. Authorization code flow (with PKCE) is the most secure for client-side applications. Client credentials flow works for server-to-server communication. Token expiration limits breach impact. Refresh tokens extend sessions without re-authentication.

## Authorization

Implement authorization at the API gateway level, not just in application code. Validate that the authenticated user has permission for the requested resource. Use scopes (OAuth) or permissions to define what each token can do.

Object-level authorization verifies the user can access the specific resource. A user should not access another user's documents by changing an ID parameter. Implement authorization checks in every endpoint, not just those that seem sensitive. Test authorization thoroughly with negative test cases.

## Rate Limiting

Rate limiting prevents API abuse. Authenticated limits per user or API key. Unauthenticated limits per IP address. Endpoint-specific limits for expensive operations. Graduated responses: warn at 70%, limit at 100%, block at 120%.

Return rate limit headers (X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset) so consumers can adapt. Use token bucket or sliding window algorithms. Consider cost-based rate limiting—bill customers for heavy API usage rathe than hard-blocking.

## Input Validation

Validate all input: request parameters, headers, body, and query strings. Validate types, lengths, formats, and ranges. Reject unexpected input. Use allowlists over blocklists—define what is allowed rather than what is rejected.

SQL injection: use parameterized queries, never string concatenation. NoSQL injection: validate query operators and sanitize input. Command injection: avoid passing user input to system commands. SSRF: restrict outbound URL fetching to approved domains.

## OWASP API Top 10

The OWASP API Security Top 10 lists the most critical API risks: broken object-level authorization, broken authentication, broken property-level authorization, unrestricted resource consumption, broken function-level authorization, mass assignment, security misconfiguration, injection, improper asset management, and excessive data exposure.

Address each risk systematically. Start with authorization testing—this is the most common and most damaging API vulnerability. Use API security testing tools (Postman, OWASP ZAP, Burp Suite) to automate security testing.

**See also:** [Secure API Design Principles](</en/security/secure-api-design.html>), [OWASP Top 10 2026](</en/security/owasp-top-10-2026.html>), [OAuth2 Implementation](</en/security/oauth2-implementation.html>).

**See also:** [Secure API Design Principles](</en/security/secure-api-design.html>), [Helm Security](</en/security/helm-security.html>), [OAuth2 Implementation](</en/security/oauth2-implementation.html>)

**See also:** [Secure API Design Principles](</en/security/secure-api-design.html>), [Helm Security](</en/security/helm-security.html>), [OAuth2 Implementation](</en/security/oauth2-implementation.html>)

**See also:** [Secure API Design Principles](</en/security/secure-api-design.html>), [Helm Security](</en/security/helm-security.html>), [OAuth2 Implementation](</en/security/oauth2-implementation.html>)

**See also:** [Secure API Design Principles](</en/security/secure-api-design.html>), [Helm Security](</en/security/helm-security.html>), [OAuth2 Implementation](</en/security/oauth2-implementation.html>)

**See also:** [Secure API Design Principles](</en/security/secure-api-design.html>), [Helm Security](</en/security/helm-security.html>), [OAuth2 Implementation](</en/security/oauth2-implementation.html>)

**See also:** [Input Validation Deep Dive](</en/security/input-validation.html>), [Microservice Security](</en/security/microservice-security.html>), [Serverless Security](</en/security/serverless-security.html>)

**See also:** [Input Validation Deep Dive](</en/security/input-validation.html>), [Microservice Security](</en/security/microservice-security.html>), [Serverless Security](</en/security/serverless-security.html>)

**See also:** [Input Validation Deep Dive](</en/security/input-validation.html>), [Microservice Security](</en/security/microservice-security.html>), [Serverless Security](</en/security/serverless-security.html>)

**See also:** [Input Validation Deep Dive](</en/security/input-validation.html>), [Microservice Security](</en/security/microservice-security.html>), [Serverless Security](</en/security/serverless-security.html>)

**See also:** [Input Validation Deep Dive](</en/security/input-validation.html>), [Microservice Security](</en/security/microservice-security.html>), [Serverless Security](</en/security/serverless-security.html>)

**See also:** [Input Validation Deep Dive](</en/security/input-validation.html>), [Microservice Security](</en/security/microservice-security.html>), [Serverless Security](</en/security/serverless-security.html>)

**See also:** [Input Validation Deep Dive](</en/security/input-validation.html>), [Microservice Security](</en/security/microservice-security.html>), [Serverless Security](</en/security/serverless-security.html>)

**See also:** [Input Validation Deep Dive](</en/security/input-validation.html>), [Microservice Security](</en/security/microservice-security.html>), [Serverless Security](</en/security/serverless-security.html>)

**See also:** [Input Validation Deep Dive](</en/security/input-validation.html>), [Microservice Security](</en/security/microservice-security.html>), [Serverless Security](</en/security/serverless-security.html>)

**See also:** [Input Validation Deep Dive](</en/security/input-validation.html>), [Microservice Security](</en/security/microservice-security.html>), [Serverless Security](</en/security/serverless-security.html>)

**See also:** [Input Validation Deep Dive](</en/security/input-validation.html>), [Microservice Security](</en/security/microservice-security.html>), [Serverless Security](</en/security/serverless-security.html>)

**See also:** [Input Validation Deep Dive](</en/security/input-validation.html>), [Microservice Security](</en/security/microservice-security.html>), [Serverless Security](</en/security/serverless-security.html>)
