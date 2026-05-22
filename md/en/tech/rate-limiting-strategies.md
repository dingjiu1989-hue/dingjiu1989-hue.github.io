---
title: "Rate Limiting Strategies for APIs: Token Bucket, Sliding Window, and Beyond"
description: "Deep dive into rate limiting algorithms: token bucket, fixed window, sliding window log, sliding window counter, and leaky bucket. Implementation in Redis and comparison of approaches for different API types."
date: 2025-10-16
board: tech
url: https://aidev.fit/en/tech/rate-limiting-strategies.html
---

# Rate Limiting Strategies for APIs: Token Bucket, Sliding Window, and Beyond

Rate limiting is one of the few backend patterns that touches every layer of the stack: it protects your API from abuse, controls costs, ensures fair usage, and prevents cascading failures. But picking the wrong algorithm or implementing it incorrectly leads to inaccurate limits, race conditions, or excessive latency. This guide compares every major rate limiting algorithm and provides production-ready implementations.

## Rate Limiting Algorithms Compared

Algorithm| How It Works| Accuracy| Memory| Best For  
---|---|---|---|---  
Fixed Window| Count requests in fixed time buckets (e.g., per minute)| Poor (burst at boundaries)| Very Low| Simple limits, not recommended for production  
Sliding Window Log| Store timestamp of every request, count in window| Perfect| High| When accuracy matters more than memory  
Sliding Window Counter| Weighted count: current window + previous window| Good (~1% error)| Low| Best balance of accuracy and memory  
Token Bucket| Tokens refill at fixed rate, each request consumes 1 token| Good| Low| Allowing bursts while maintaining average rate  
Leaky Bucket| Requests enter queue, processed at fixed rate| Good| Medium (queue)| Smoothing traffic (networking, traffic shaping)  
  
## Token Bucket — The Default Choice
    
    
    # Redis-based Token Bucket (Lua for atomicity)
    # Allows bursts up to bucket size, refills at steady rate
    
    local key = KEYS[1]        -- rate_limit:user:123
    local capacity = tonumber(ARGV[1])  -- max tokens (burst)
    local rate = tonumber(ARGV[2])      -- tokens per second
    local now = tonumber(ARGV[3])       -- current time in seconds
    
    local bucket = redis.call('HMGET', key, 'tokens', 'last_refill')
    local tokens = tonumber(bucket[1]) or capacity
    local last_refill = tonumber(bucket[2]) or now
    
    -- Refill tokens based on elapsed time
    local elapsed = math.max(0, now - last_refill)
    local refill = elapsed * rate
    tokens = math.min(capacity, tokens + refill)
    
    if tokens >= 1 then
        redis.call('HMSET', key, 'tokens', tokens - 1, 'last_refill', now)
        redis.call('EXPIRE', key, math.ceil(capacity / rate) + 1)
        return {1, tokens - 1}  -- Allowed
    else
        return {0, tokens}  -- Rate limited
    end

## Sliding Window Counter — Better Accuracy
    
    
    # Python: Sliding Window Counter (in-memory)
    # Accuracy: ~1% error, Memory: 2 counters per user
    
    from time import time
    
    class SlidingWindowLimiter:
        def __init__(self, max_req: int, window_sec: int):
            self.max_req = max_req
            self.window = window_sec
            self.current = {}   # user_id -> count in current window
            self.previous = {}  # user_id -> count in previous window
            self.window_start = int(time() / window_sec) * window_sec
    
        def is_allowed(self, user_id: str) -> bool:
            now = int(time())
            window_key = int(now / self.window) * self.window
    
            # Rotate windows if needed
            if window_key > self.window_start:
                self.previous = self.current.copy()
                self.current.clear()
                self.window_start = window_key
    
            # Weighted count
            elapsed = now - self.window_start
            weight = 1 - (elapsed / self.window)
            count = self.current.get(user_id, 0) +                 self.previous.get(user_id, 0) * weight
    
            if count < self.max_req:
                self.current[user_id] = self.current.get(user_id, 0) + 1
                return True
            return False

## Choosing the Right Algorithm

Scenario| Recommended Algorithm| Why  
---|---|---  
General API rate limiting| Token Bucket| Allows short bursts, simple to implement, well-understood  
Strict per-second limits (trading, bidding)| Sliding Window Counter| More accurate than Token Bucket, low overhead  
Hard rate cap with zero burst tolerance| Leaky Bucket| Enforces steady outflow, good for traffic shaping  
Multi-dimensional (per-user + per-endpoint)| Multiple Token Buckets| One bucket per dimension, check all before allowing  
Distributed across API gateway nodes| Redis + Token Bucket| Centralized counter, Lua for atomicity  
  
## Rate Limiting Headers (RFC Standard)

Header| Example| Meaning  
---|---|---  
X-RateLimit-Limit| 100| Maximum requests per window  
X-RateLimit-Remaining| 67| Requests remaining in current window  
X-RateLimit-Reset| 1715818800| Unix timestamp when the window resets  
Retry-After| 30| Seconds until next request will succeed (429 response)  
  
**Bottom line:** Use Token Bucket as your default rate limiting algorithm — it handles bursts gracefully, is simple to explain to API consumers, and has a well-known Redis implementation. Add Sliding Window Counter when you need better accuracy at window boundaries. Always include the standard rate limit headers in your API responses so consumers can self-regulate. See also: [Webhook Implementation Guide](</en/tech/webhook-implementation-guide.html>) and [Web Security Basics](</en/tech/web-security-basics.html>).

**See also:** [Caching Strategies for Web Apps: CDN, Redis, Browser, and API Caching](</en/tech/caching-strategies-web-apps.html>), [Database Indexing Strategies: B-Tree, Hash, GIN, GiST, and BRIN Explained](</en/tech/database-indexing-guide.html>), [REST API Best Practices: The Complete Guide for 2026](</en/tech/rest-api-best-practices.html>)
