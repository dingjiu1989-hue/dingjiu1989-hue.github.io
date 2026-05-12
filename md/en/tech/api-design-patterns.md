---
title: "API Design Patterns: Rate Limiting, Pagination, Idempotency, and More"
description: "Production-proven API patterns every backend developer needs. Rate limiting strategies, cursor vs offset pagination, idempotency keys, bulk operations, and webhook design."
date: 2026-05-08
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/api-design-patterns.html
---

# API Design Patterns: Rate Limiting, Pagination, Idempotency, and More

Every production API eventually needs the same set of patterns: rate limiting, pagination, idempotency, batching, and webhooks. Here's how to implement each one correctly — with the edge cases that bite you 6 months later.

## 1\. Rate Limiting

Rate limiting protects your API from abuse and ensures fair usage. The three common algorithms:

Algorithm| How It Works| Best For  
---|---|---  
**Token Bucket**|  Tokens refill at a fixed rate. Each request consumes a token. Allows bursts.| Most APIs (best default)  
**Sliding Window**|  Count requests in the last N seconds. Smooth, no burst allowance.| Precise rate enforcement  
**Fixed Window**|  Reset count every N seconds. Simple but allows 2x bursts at boundaries.| Simple use cases (avoid)  

**Response headers:** Always include `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, and `Retry-After` on 429 responses.

## 2\. Pagination — Cursor vs Offset

| Cursor-Based| Offset-Based  
---|---|---  
**Implementation**| `?cursor=abc123&limit;=20`| `?offset=40&limit;=20`  
**Stability**|  Stable (new rows don't shift)| Unstable (page shifts with inserts)  
**Performance**|  Fast (uses index directly)| Slow on large offsets (scans then discards)  
**Random access**|  No (must traverse sequentially)| Yes (jump to page 42)  
**Use case**|  Feeds, timelines, infinite scroll| Search results, admin UIs  

**Rule:** Use cursor-based pagination by default. Only use offset when you need random page access.

## 3\. Idempotency Keys

Network is unreliable. Clients retry. Without idempotency, a retried payment request = double charge. The fix: idempotency keys.

    // Client sends a unique key:
    POST /api/charges
    Idempotency-Key: 8f7d3a2c-9e4b-4a1d-8c6f-3b5e7d9a0f2c

    // Server logic:
    // 1. Check if key exists in idempotency store (e.g., Redis with 24h TTL)
    // 2. If NOT found: process request, store response with key
    // 3. If found: return stored response (same status code, same body)

**Where to use:** Payment endpoints, order creation, any mutation where duplicates are harmful. Stripe's API is the gold standard for idempotency.

## 4\. Bulk Operations

Single-resource endpoints don't scale when users need to operate on 100 items. Add bulk endpoints for common batch operations.

    // ❌ 100 individual requests:
    DELETE /api/tags/1
    DELETE /api/tags/2
    // ... x98

    // ✅ Bulk endpoint:
    POST /api/tags/bulk-delete
    { "ids": [1, 2, 3, ..., 100] }

    // Response is partial-success aware:
    {
      "results": [
        { "id": 1, "status": "deleted" },
        { "id": 2, "status": "not_found" },
        { "id": 3, "status": "forbidden" }  // not owned by user
      ]
    }

## 5\. Webhooks — Reliable Event Delivery

Webhooks let your API push events to external systems. The key is reliable delivery.

    // Webhook delivery pattern:
    // 1. Sign payloads (HMAC-SHA256) so receivers verify authenticity
    // 2. Retry with exponential backoff (1min, 5min, 25min, 2h, 24h)
    // 3. Mark as failed after 24h of retries
    // 4. Provide a dashboard for manual retry of failed deliveries
    // 5. Set reasonable timeouts (10s connect, 30s read)
    // 6. Log all delivery attempts for debugging

Stripe's webhook system is the implementation to study — signatures, retries, and a dashboard for debugging.

## Quick Checklist

  * Rate limit with token bucket. Include headers. Return 429 with Retry-After.
  * Cursor paginate by default. Offset only for search/ADMIN UIs.
  * Idempotency keys on all mutation endpoints that involve money or creation.
  * Bulk operations for batch create/update/delete when users operate on many items.
  * Webhooks with signatures + retries + dashboard for any event-driven integration.

**Bottom line:** These five patterns separate a prototype API from a production API. Implement them before you need them — retrofitting idempotency is much harder than building it in from day one. See also: [REST API Best Practices](</en/tech/rest-api-best-practices.html>) and [API architecture comparison](</en/compare/trpc-vs-graphql-vs-rest.html>).
