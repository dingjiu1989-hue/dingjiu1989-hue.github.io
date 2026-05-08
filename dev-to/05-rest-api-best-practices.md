---
title: "REST API Best Practices: The Complete Guide for 2026"
published: true
description: "Design production-ready REST APIs with proper naming, versioning, pagination, error handling, and security. Includes OpenAPI 3.1 standards."
tags: api, webdev, programming, beginners, backend
canonical_url: https://dingjiu1989-hue.github.io/en/tech/rest-api-best-practices.html
---

REST APIs power the modern web, but most are designed with subtle flaws that cause pain months later. Here are the conventions that separate production APIs from weekend projects.

## 1. Use Nouns, Not Verbs

```bash
# Good
GET    /users/42
POST   /users

# Bad
GET    /getUsers
POST   /createUser
```

## 2. Version Your API from Day One

Use URL prefix versioning (`/v1/users`). Choose one strategy and stick with it everywhere.

## 3. Consistent Naming

- **JSON:** camelCase (`createdAt`)
- **URL paths:** kebab-case (`/user-orders`)
- **Query params:** snake_case (`?sort_by=name`)

## 4. Use the Right HTTP Status Codes

| Code | When |
|---|---|
| 200 | Successful GET, PUT, PATCH |
| 201 | Successful POST — include Location header |
| 204 | Successful DELETE |
| 400 | Validation failure |
| 401 | Missing/expired token |
| 403 | Authenticated but not permitted |
| 404 | Resource doesn't exist |
| 409 | Duplicate or state conflict |
| 422 | Valid syntax but semantic error |
| 429 | Rate limit — include Retry-After header |

## 5. Consistent Error Responses

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is required",
    "details": [
      {"field": "email", "reason": "must not be empty"}
    ],
    "requestId": "req_abc123"
  }
}
```

## 6. Pagination

```bash
# Cursor-based (preferred for large datasets)
GET /users?cursor=eyJpZCI6NDJ9&limit=20
Response: {"data": [...], "nextCursor": "...", "hasMore": true}
```

## 7. Security Checklist

- **Always HTTPS.** No exceptions.
- **Rate limit.** 60 req/min per IP for unauthenticated users minimum.
- **Validate Content-Type.** Reject requests with wrong Content-Type.
- **Never use `Access-Control-Allow-Origin: *`** with credentials.
- **Use OAuth2 or API keys.** Never roll your own auth.
- **Keep secrets out of responses.** Password hashes, internal IDs, stack traces, server versions.

## 8. Always Have an OpenAPI Spec

Use OpenAPI 3.1 (Swagger). Stoplight, Redoc, and Swagger UI generate beautiful interactive docs from a single spec file. If your API doesn't have an OpenAPI spec, it's not production-ready.

---

*Originally published at [AI Study Room](https://dingjiu1989-hue.github.io/en/tech/rest-api-best-practices.html) — 70+ curated articles for developers.*
