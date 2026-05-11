---
title: "API Rate Limiting Implementation"
description: "A comprehensive guide to implementing API rate limiting with token bucket, leaky bucket, and sliding window algorithms."
date: 2026-05-11
board: security
url: https://dingjiu1989-hue.github.io/en/security/api-rate-limiting.html
---

## Why Rate Limiting Matters

API rate limiting protects backend services from abuse, ensures fair resource distribution, and prevents cascading failures. Without rate limiting, a single aggressive client can degrade the experience for all other users or even crash the service entirely. For public APIs, rate limiting is a fundamental security control that mitigates DDoS attacks, credential stuffing, and web scraping.

## Rate Limiting Algorithms

### Token Bucket

The token bucket algorithm is the most widely used approach. A bucket holds a fixed number of tokens, and each request consumes one token. Tokens are replenished at a steady rate. If the bucket is empty, the request is denied.

```
class TokenBucket:
    def __init__(self, capacity, refill_rate, refill_interval=1.0):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.refill_interval = refill_interval
        self.last_refill = time.time()

    def allow_request(self):
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity,
            self.tokens + elapsed * self.refill_rate)
        self.last_refill = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
```

The token bucket allows short bursts up to `capacity` while enforcing a long-term average rate. This makes it ideal for APIs where occasional spikes are acceptable.

### Leaky Bucket

The leaky bucket algorithm enforces a strict processing rate. Incoming requests fill a queue, and a worker processes them at a fixed rate. If the queue is full, new requests are dropped.

This approach smooths out traffic perfectly but does not handle bursts well. It is best suited for downstream systems that cannot tolerate spikes, such as legacy databases or third-party APIs with strict rate contracts.

### Sliding Window Log

The sliding window algorithm maintains a timestamped log of recent requests within a time window. When a new request arrives, entries older than the window are pruned. If the count of remaining entries exceeds the limit, the request is denied.

```
class SlidingWindowLog:
    def __init__(self, limit, window_ms=1000):
        self.limit = limit
        self.window_ms = window_ms
        self.log = deque()

    def allow_request(self):
        now = time.time() * 1000
        cutoff = now - self.window_ms
        while self.log and self.log[0] < cutoff:
            self.log.popleft()
        if len(self.log) < self.limit:
            self.log.append(now)
            return True
        return False
```

Sliding window gives precise per-user limits and avoids the boundary spikes of fixed-window counters, at the cost of storing request timestamps in memory.

## Implementation Patterns

### Middleware Pattern (Node.js / Express)

```javascript
const rateLimit = require('express-rate-limit');
const limiter = rateLimit({
    windowMs: 60 * 1000,
    max: 100,
    standardHeaders: true,
    legacyHeaders: false,
    keyGenerator: (req) => req.ip,
    handler: (req, res) => {
        res.status(429).json({
            error: 'Too many requests',
            retryAfter: Math.ceil(req.rateLimit.resetTime / 1000)
        });
    }
});
app.use('/api/', limiter);
```

### Distributed Rate Limiting with Redis

For applications running across multiple instances, in-memory rate limiting is insufficient. Use Redis with atomic operations:

```lua
-- Redis Lua script for sliding window counter
local key = KEYS[1]
local now = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local limit = tonumber(ARGV[3])

redis.call('ZREMRANGEBYSCORE', key, 0, now - window)
local count = redis.call('ZCARD', key)
if count < limit then
    redis.call('ZADD', key, now, now .. ':' .. math.random())
    redis.call('EXPIRE', key, window / 1000)
    return 1
end
return 0
```

## HTTP Response Headers

Always communicate rate limits to clients via standard headers:

| Header | Purpose |
|--------|---------|
| `X-RateLimit-Limit` | Maximum requests per window |
| `X-RateLimit-Remaining` | Requests left in current window |
| `X-RateLimit-Reset` | Unix timestamp when the window resets |
| `Retry-After` | Seconds to wait before retrying (on 429) |

## Tiered Rate Limiting

Apply different limits based on client tiers:

| Tier | Limit | Window |
|------|-------|--------|
| Free | 10 req/s | 1 second |
| Pro | 100 req/s | 1 second |
| Enterprise | 1000 req/s | 1 second |

## Common Pitfalls

- **Using IP alone**: Behind NAT, many legitimate users share an IP. Use API keys or authentication tokens as the primary key, with IP as a fallback.
- **Not rate limiting authentication endpoints**: Login, registration, and password reset endpoints need stricter limits than the rest of the API.
- **Ignoring distributed denial of service**: Application-level rate limiting alone cannot stop layer 3/4 attacks. Combine with a CDN or WAF with DDoS protection.
- **Missing retry-after headers**: Clients cannot implement exponential backoff without knowing when to retry.

## Summary

Choose token bucket for general-purpose APIs, sliding window for precise per-user limits, and leaky bucket for downstream protection. Always distribute limit state via Redis when running multiple service instances, and communicate limits through standard HTTP headers so clients can adapt their behavior.
