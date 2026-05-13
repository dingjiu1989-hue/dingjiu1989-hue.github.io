---
title: "Throttling Pattern for System Protection"
description: "Implement throttling to protect backend systems from overload and ensure fair resource allocation."
date: 2026-05-12
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/throttling-pattern.html
---

# Throttling Pattern for System Protection

# Throttling Pattern for System Protection

  


# Throttling Pattern for System Protection

  
  
  
  


# Throttling Pattern for System Protection

  
  
  
  
  
  
  


# Throttling Pattern for System Protection

  
  
  
  
  
  
  


Throttling controls the rate at which requests are processed to protect backend systems from overload. When request volume exceeds capacity, throttling rejects or delays excess requests instead of allowing the system to fail under load.

  
  
  
  
  
  
  
  
  
  


##  Throttling vs Rate Limiting

  
  
  
  
  
  
  
  
  
  


Rate limiting controls how many requests a client can make within a time window. Throttling controls the overall processing rate of the system, regardless of client distribution. Rate limiting is typically client-specific. Throttling is system-wide.

  
  
  
  
  
  
  
  
  
  


Both patterns protect systems, but they operate at different levels. Rate limiting prevents abusive clients from monopolizing resources. Throttling prevents the system from exceeding its processing capacity.

  
  
  
  
  
  
  
  
  
  


##  Implementation Approaches

  
  
  
  
  
  
  
  
  
  


Token bucket is the most common throttling algorithm. Tokens are added to a bucket at a fixed rate. Each request consumes a token. If the bucket is empty, the request is throttled. The bucket size allows burst handling.

  
  
  
  
  
  
  
  
  
  


Leaky bucket queues requests at a fixed processing rate. Burst requests are buffered and processed at the controlled rate. Excess requests beyond the buffer capacity are rejected.

  
  
  
  
  
  
  
  
  
  


Concurrency limiter controls the number of in-flight requests. New requests are queued or rejected when the concurrency limit is reached. This is effective for protecting thread pools and database connections.

  
  
  
  
  
  
  
  
  
  


##  Throttling Responses

  
  
  
  
  
  
  
  
  
  


Throttled requests should return appropriate HTTP status codes. 429 Too Many Requests is standard with a Retry-After header indicating when the client should retry. Include rate limit headers (X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset) so clients can adjust their behavior.

  
  
  
  
  
  
  
  
  
  


##  Distributed Throttling

  
  
  
  
  
  
  
  
  
  


In distributed systems, throttling requires shared state. Redis is commonly used for distributed rate counters. Use atomic operations (INCR, EXPIRE) for correctness. Consider performance impact of cross-network throttling calls.

  
  
  
  
  
  
  
  
  
  


##  When to Throttle

  
  
  
  
  
  
  
  
  
  


Throttle when protecting external API dependencies with rate limits, when the system has hard capacity limits (database connections, thread pools), and during traffic spikes to maintain system stability. Monitor throttled request rates—sustained throttling indicates capacity issues.
