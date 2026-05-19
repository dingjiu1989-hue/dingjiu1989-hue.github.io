---
title: "API Rate Limiting Implementation"
description: "A comprehensive guide to implementing API rate limiting with token bucket, leaky bucket, and sliding window algorithms."
date: 2025-12-17
board: security
url: https://dingjiu1989-hue.github.io/en/security/api-rate-limiting.html
---

# API Rate Limiting Implementation

Why Rate Limiting Matters 

Rate limiting protects APIs from abuse, DoS attacks, and unintentional overload. It ensures fair usage and maintains service quality for all consumers. 

Rate Limiting Algorithms 

Token Bucket 

The most popular algorithm, allowing bursts while maintaining average limits: 

import time

import threading

class TokenBucket:

def **init**(self, rate, capacity):

self.rate = rate # Tokens per second

self.capacity = capacity

self.tokens = capacity

self.last_refill = time.monotonic()

self.lock = threading.Lock()

def consume(self, tokens=1):

with self.lock:

self._refill()

if self.tokens >= tokens:

self.tokens -= tokens

return True

return False

def _refill(self):

now = time.monotonic()

elapsed = now - self.last_refill

self.tokens = min(self.capacity, 

self.tokens + elapsed * self.rate)

self.last_refill = now

## Usage

bucket = TokenBucket(rate=10, capacity=20) # 10 req/s, burst 20

if bucket.consume():

process_request()

else:

return "429 Too Many Requests"

Sliding Window Log 

More precise but memory-intensive: 

from collections import deque

import time

class SlidingWindowLog:

def **init**(self, window_size=60, max_requests=100):

self.window_size = window_size

self.max_requests = max_requests

self.log = deque()

def allow_request(self):

now = time.time()

## Remove expired entries

while self.log and self.log[0] <= now - self.window_size:

self.log.popleft()

if len(self.log) < self.max_requests:

self.log.append(now)

return True

return False

Rate Limiting Headers 

Return standard headers for client feedback: 

def rate_limit_response(allowed, limit, remaining, reset):

if allowed:

return {

"X-RateLimit-Limit": str(limit),

"X-RateLimit-Remaining": str(remaining),

"X-RateLimit-Reset": str(reset)

}

else:

return {

"X-RateLimit-Limit": str(limit),

"X-RateLimit-Remaining": "0",

"Retry-After": str(reset - int(time.time()))

}, 429

Distributed Redis Implementation 

For multi-server deployments: 

import redis

import time

class RedisSlidingWindow:

def **init**(self, redis_client):

self.redis = redis_client

def is_allowed(self, key, max_requests=100, window_seconds=60):

now = int(time.time() * 1000)

window_start = now - (window_seconds * 1000)

pipeline = self.redis.pipeline()

pipeline.zremrangebyscore(key, 0, window_start)

pipeline.zcard(key)

pipeline.zadd(key, {str(now): now})

pipeline.expire(key, window_seconds * 2)

_, count,_ , _ = pipeline.execute()

return count < max_requests

Middleware Implementation 

const rateLimit = require("express-rate-limit");

const apiLimiter = rateLimit({

windowMs: 15 * 60 * 1000,

max: 100,

standardHeaders: true,

legacyHeaders: false,

message: { error: "Too many requests, please try again later." },

keyGenerator: (req) => req.user?.id || req.ip,

skip: (req) => req.headers["x-internal"] === process.env.INTERNAL_TOKEN

});

app.use("/api/", apiLimiter);

Conclusion 

Choose the right rate limiting algorithm for your use case. Token bucket works well for most APIs. Use Redis for distributed rate limiting across multiple servers. Always return clear rate limit headers so clients can self-regulate. Monitor rate limit hit rates to tune thresholds over time.

**See also:** [Encryption at Rest Guide](</en/security/encryption-at-rest.html>), [Two-Factor Authentication Guide](</en/security/two-factor-authentication.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>).

**See also:** [RBAC Authorization Implementation](</en/security/rbac-authorization.html>), [Two-Factor Authentication Guide](</en/security/two-factor-authentication.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>)

**See also:** [RBAC Authorization Implementation](</en/security/rbac-authorization.html>), [Two-Factor Authentication Guide](</en/security/two-factor-authentication.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>)

**See also:** [RBAC Authorization Implementation](</en/security/rbac-authorization.html>), [Two-Factor Authentication Guide](</en/security/two-factor-authentication.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>)

**See also:** [RBAC Authorization Implementation](</en/security/rbac-authorization.html>), [Two-Factor Authentication Guide](</en/security/two-factor-authentication.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>)

**See also:** [RBAC Authorization Implementation](</en/security/rbac-authorization.html>), [Two-Factor Authentication Guide](</en/security/two-factor-authentication.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>)

**See also:** [Identity and Access Management (IAM) Guide](</en/security/identity-management.html>), [JWT Authentication Best Practices](</en/security/jwt-authentication-guide.html>), [Password Hashing Algorithms Compared](</en/security/password-hashing.html>)

**See also:** [Identity and Access Management (IAM) Guide](</en/security/identity-management.html>), [JWT Authentication Best Practices](</en/security/jwt-authentication-guide.html>), [Password Hashing Algorithms Compared](</en/security/password-hashing.html>)

**See also:** [Identity and Access Management (IAM) Guide](</en/security/identity-management.html>), [JWT Authentication Best Practices](</en/security/jwt-authentication-guide.html>), [Password Hashing Algorithms Compared](</en/security/password-hashing.html>)

**See also:** [Identity and Access Management (IAM) Guide](</en/security/identity-management.html>), [JWT Authentication Best Practices](</en/security/jwt-authentication-guide.html>), [Password Hashing Algorithms Compared](</en/security/password-hashing.html>)
