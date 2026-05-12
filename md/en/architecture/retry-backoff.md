---
title: "Retry and Backoff Strategies"
description: "Learn retry and backoff strategies for building resilient distributed systems."
date: 2026-05-11
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/retry-backoff.html
---

# Retry and Backoff Strategies

In distributed systems, failures are inevitable. Networks drop packets, services restart, databases time out. Retry and backoff strategies are essential for building systems that gracefully handle transient failures without overwhelming downstream services.   
When to Retry   
Not all failures deserve a retry. Distinguish between transient and permanent failures:   
**Transient failures** (retry): Network timeouts, connection resets, 503 Service Unavailable, 429 Too Many Requests. These indicate temporary conditions that may resolve on their own.   
**Permanent failures** (do not retry): 400 Bad Request, 401 Unauthorized, 404 Not Found, 403 Forbidden. Retrying these will never succeed and wastes resources.   
Always inspect the error type or status code before deciding to retry.   
Idempotency Is Required   
Never retry an operation unless it is idempotent. If a request succeeds on the server but the response is lost, a retry will create a duplicate. This is catastrophic for operations like charging a credit card or creating an order.   
The solution is idempotency keys. Clients generate a unique key for each operation and include it in the request header:   

    POST /payments

    Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000

    {

      "amount": 1000,

      "currency": "USD"

    }

The server stores the result keyed by the idempotency key. If the same key is received again, the server returns the stored result instead of executing the operation again. Stripe's API is a canonical example of this pattern.   
Fixed Retry   
The simplest strategy: wait N seconds between each retry, up to a maximum number of attempts.   

    max_retries = 3

    delay = 1  # second

    for attempt in range(max_retries):

        try:

            return make_request()

        except TransientError:

            if attempt == max_retries - 1:

                raise

            time.sleep(delay)

**Pros:** Simple to implement and understand. **Cons:** If the service is still recovering, all clients retry simultaneously, potentially causing a thundering herd.   
Exponential Backoff   
Increase the delay exponentially between each retry. If the first retry waits 1 second, the second waits 2, the third waits 4, then 8, 16, and so on.   

    max_retries = 5

    base_delay = 1

    for attempt in range(max_retries):

        try:

            return make_request()

        except TransientError:

            if attempt == max_retries - 1:

                raise

            delay = base_delay * (2 ** attempt)

            time.sleep(delay)

**Pros:** Reduces load on the recovering service. Quickly retries when the failure might be brief, but backs off aggressively for longer outages.   
**Cons:** The delays compound quickly. After 6 attempts with base 1, the delay is 64 seconds. This may be too slow for latency-sensitive applications.   
Exponential Backoff with Jitter   
Jitter adds randomness to the delay, preventing the thundering herd problem when many clients retry simultaneously. Without jitter, all clients retry at exactly the same time, recreating the original load spike.   
There are several jitter strategies:   
**Full jitter:**

    delay = random.uniform(0, base_delay * (2 ** attempt))

**Equal jitter:**

    half = base_delay * (2 ** attempt) / 2

    delay = half + random.uniform(0, half)

**Decorrelated jitter:** (recommended for production)

    delay = min(cap, random.uniform(base_delay, delay * 3))

Full jitter is the most common and works well for most scenarios. The randomness spreads retries across a window, giving the recovering service breathing room. AWS and Google Cloud use exponential backoff with jitter in their SDKs.   
Circuit Breaker Integration   
Retry and circuit breaker patterns are complementary. The circuit breaker prevents retries when the downstream service is known to be failing. Use retry for transient, short-lived failures. Use the circuit breaker for persistent failures.   
A typical integration:
* First failure -> Retry with exponential backoff.
2\. Multiple failures -> Circuit breaker opens, all requests fail fast. 3\. After cooldown -> Circuit breaker half-opens, allows a probe request. 4\. Probe succeeds -> Circuit breaker closes, normal operation resumes.   
Maximum Retries and Timeouts   
Set a maximum number of retries and a maximum total time budget. A request that has been retried for 5 minutes should probably fail fast and return an error to the user.   

    max_retries = 3

    timeout = 30  # seconds total

    start = time.now()

    for attempt in range(max_retries):

        try:

            if time.now() - start > timeout:

                raise TimeoutError()

            return make_request(timeout=5)

        except TransientError:

            if attempt == max_retries - 1:

                raise

Retry-After Header   
When a server returns `429 Too Many Requests` or `503 Service Unavailable`, it should include a `Retry-After` header. The client should respect this header and wait the specified duration before retrying. This allows the server to communicate its preferred retry timing.   

    delay = response.headers.get('Retry-After', default_delay)

Summary   
Effective retry strategies are essential for distributed system resilience. Always combine retries with idempotency keys to prevent duplicate operations. Use exponential backoff with jitter to spread retries and prevent thundering herds. Integrate with circuit breakers for long-term failure handling. Set strict retry limits and time budgets to fail fast when recovery is not imminent.
