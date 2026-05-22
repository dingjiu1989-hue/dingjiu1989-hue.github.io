---
title: "Rate Limiting Architecture"
description: "Token bucket, sliding window, distributed rate limiting, Redis-based implementation, and algorithm tradeoffs"
date: 2026-04-29
board: architecture
url: https://aidev.fit/en/architecture/rate-limiting-architecture.html
---

# Rate Limiting Architecture

Rate limiting protects system resources by controlling the rate at which clients can make requests. It prevents abuse, ensures fair resource allocation, and maintains system stability under load. The choice of rate limiting algorithm — how limits are tracked and enforced — determines the system's accuracy, memory usage, and ability to handle burst traffic. 

The token bucket algorithm is the most widely used rate limiting approach. A bucket holds tokens that replenish at a fixed rate. Each request consumes one token. If the bucket is empty, the request is rejected. The bucket capacity allows bursts — if the bucket is full, a client can send a burst of requests equal to the bucket size. Token bucket has two parameters: the fill rate (steady-state requests per second) and the bucket size (maximum burst). This combination provides both sustained throughput limits and burst tolerance. 

The sliding window algorithm provides precise rate enforcement over time windows. A sliding window log stores timestamps for each request. When a new request arrives, timestamps outside the window are removed, and the count is checked against the limit. The sliding window counter variant improves memory efficiency by tracking two counters: the current window count and the previous window count, with a weighted estimate for the current position. This provides good accuracy with bounded memory. 

Fixed window counting is simpler but suffers from boundary effects. The window resets at fixed intervals (every minute, every hour). A client can send the full limit at the end of one window and the full limit at the beginning of the next, achieving double the intended rate. Fixed window is acceptable for coarse rate limiting where occasional bursts are tolerable but is inadequate for strict rate enforcement. 

Distributed rate limiting adds the challenge of coordinating across multiple application instances. Each instance must apply consistent rate limits — if the limit is 100 requests per second and there are 3 instances, together they must not allow more than 100 requests. Centralized rate tracking in Redis is the standard approach: each instance increments a counter in Redis with the appropriate TTL. The atomic INCR command with EXPIRE provides correct distributed counting. 

Redis-based implementations must handle consistency and performance. Each request performs a Redis operation, adding latency. Pipelining and Lua scripting reduce round trips — a Lua script can check and increment the counter in a single atomic operation. Local caching with eventual synchronization reduces Redis load at the cost of temporary over-limit tolerance. For high-traffic systems, the Redis instance itself can become a bottleneck, requiring Redis Cluster sharding by client ID. 

Rate limit headers communicate limits to clients. Standard headers include: X-RateLimit-Limit (maximum requests per window), X-RateLimit-Remaining (requests remaining in current window), X-RateLimit-Reset (time until the window resets). When a request is rejected, the 429 Too Many Requests response includes Retry-After header indicating when the client should retry. These headers enable intelligent client-side backoff. 

Rate limiting at different layers serves different purposes. API gateway rate limiting protects the overall infrastructure from abusive traffic. Application-level rate limiting protects specific resources (checkout, search, API endpoints). User-level rate limiting prevents a single user from overwhelming the system. Tiered rate limiting applies different limits based on client type (free tier: 10 req/s, premium tier: 100 req/s, enterprise tier: 1000 req/s). 

Sliding window log vs counter tradeoff: the log approach is memory-intensive (stores a timestamp per request) but perfectly accurate. The counter approach is memory-efficient (stores only two counters) but has approximation error. A practical compromise uses the sliding window counter with a small number of sub-windows (4-10 per window), providing good accuracy with bounded memory — each client rate limit requires 8-20 counters. 

Concurrency limiting complements rate limiting. Rate limiting controls request arrival rate. Concurrency limiting controls the number of in-flight requests. A service with 10 worker threads needs to limit concurrent requests to protect those workers, regardless of arrival rate. Semaphores or circuit breakers provide concurrency limiting. Both should be used together: rate limiting for traffic shaping, concurrency limiting for resource protection. 

Client identification is the prerequisite for rate limiting. Simple identification uses IP address, which is unreliable behind proxies or NAT. API keys or JWT claims provide reliable client identity. Anonymous clients may be identified by a combination of factors (IP + user agent + geolocation). The identification method determines the limit's fairness — IP-based limiting unfairly restricts users behind shared IPs, while API key limiting requires all clients to authenticate.
