---
title: "Timeout and Retry Patterns"
description: "Deadline propagation, exponential backoff, jitter, circuit breaker integration, and retry best practices"
date: 2026-04-30
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/timeout-retry-patterns.html
---

# Timeout and Retry Patterns

Timeouts and retries are the most basic building blocks of resilient distributed systems, yet they are among the most commonly misconfigured. A timeout that is too short causes unnecessary failures under normal load spikes. A timeout that is too long causes cascading resource exhaustion. Retries without backpressure amplify failure. Getting these patterns right requires understanding the tradeoffs and the interactions between them. 

Timeouts define the maximum time a caller waits for a response. Every remote call must have a timeout — without one, a hung dependency can hold open resources indefinitely, eventually exhausting connection pools and thread pools. The timeout should be set per operation type: a simple key-value lookup may have a 100ms timeout, while a complex report generation may have 30 seconds. The timeout should be based on the operation's p99.9 latency plus a safety margin. 

Deadline propagation extends timeout semantics across the call graph. Instead of each service independently timing out, the remaining deadline is propagated from caller to callee. If Service A has 2 seconds to respond and spends 1 second processing, it passes a 1-second deadline to Service B. This prevents the thundering herd problem where all downstream services receive requests that are already expired from the caller's perspective. gRPC supports deadline propagation natively through the context. 

Exponential backoff spaces retries with progressively longer delays. After the first failure, wait 100ms. After the second, 200ms. After the third, 400ms, and so on. The exponential growth prevents synchronized retries from overwhelming the recovering service. The base delay should be long enough to allow transient failures to resolve — typically 50-200ms for network-level retries, 1-10 seconds for service-level retries. 

Jitter adds randomness to the backoff to prevent the thundering herd problem. Without jitter, when a service recovers, all clients retry simultaneously, creating a new spike that re-overwhelms the service. Full jitter randomizes the delay between 0 and the current backoff value. Equal jitter randomizes the delay between half and the full backoff value. Full jitter is generally preferred for distributed systems — it provides the best distribution of retry attempts. 

The maximum retry count prevents indefinite retries. Three retries is a common starting point. More than five retries risks creating unacceptable latency spikes — three retries with 100ms, 200ms, 400ms backoff add a maximum of 700ms. Five retries add 3100ms. The retry budget should be negotiated with the caller's total timeout — if the caller has a 5-second timeout, the service should not consume 4 seconds of that on retries before the callee even processes the request. 

Retry amplification is the hidden danger of retries in distributed systems. When Service A retries a call to Service B, which itself calls Service C and Service D, a single failed request can generate multiple retries at each level. In the worst case, retries are multiplicative — a 3-level call graph with 3 retries at each level can generate 27 total calls for one original request. The solution is to retry only at the outermost layer or use exponential backoff with jitter at each level. 

Retry with circuit breaker integration prevents retrying a failing service. Once the circuit breaker opens, retries should stop. The retry logic should check the circuit breaker state before each attempt. If the circuit is open, the retry should fail fast rather than attempt the call. When the circuit is half-open, a single retry is allowed as a probe. This integration is built into most resilience frameworks (Resilience4j, Polly) but requires explicit configuration. 

Selective retry categorizes failures into retriable and non-retriable. Network timeouts, 503 Service Unavailable, and 429 Too Many Requests are retriable — they indicate transient issues that may resolve. 400 Bad Request and 404 Not Found are not retriable — they will always fail. 500 Internal Server Error may or may not be retriable depending on whether the error is idempotent. The retry logic must distinguish these cases to avoid wasting effort on certain-failure retries. 

Retry budgets limit total retry volume over time. A budget of 5% means that at most 5% of calls to a dependency are retries. If the normal call rate is 1000/s, the retry budget is 50/s. This prevents retries from dominating traffic during extended failures. Retry budgets are adaptive — as failures increase, the budget limits the system's self-inflicted load. Google's gRPC retry implementation supports retry budgets natively. 

Consistent configuration across services is essential but elusive. Timeout and retry policies should be documented, standardized, and enforced through shared infrastructure libraries rather than reimplemented in each service. A platform team should own the shared resilience library and maintain it across languages as the organization grows. The configuration should be visible as metrics — track retry counts, backoff durations, and timeout rates to identify misconfigured services.

**See also:** [Retry Patterns](</en/architecture/retry-patterns.html>), [Circuit Breaker vs Bulkhead Pattern](</en/architecture/circuit-breaker-vs-bulkhead.html>), [Graceful Shutdown Patterns](</en/architecture/graceful-shutdown.html>).

**See also:** [Retry Patterns](</en/architecture/retry-patterns.html>), [Circuit Breaker vs Bulkhead Pattern](</en/architecture/circuit-breaker-vs-bulkhead.html>), [Graceful Shutdown Patterns](</en/architecture/graceful-shutdown.html>)

**See also:** [Retry Patterns](</en/architecture/retry-patterns.html>), [Circuit Breaker vs Bulkhead Pattern](</en/architecture/circuit-breaker-vs-bulkhead.html>), [Graceful Shutdown Patterns](</en/architecture/graceful-shutdown.html>)

**See also:** [Retry Patterns](</en/architecture/retry-patterns.html>), [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Circuit Breaker vs Bulkhead Pattern](</en/architecture/circuit-breaker-vs-bulkhead.html>)

**See also:** [Retry Patterns](</en/architecture/retry-patterns.html>), [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Circuit Breaker vs Bulkhead Pattern](</en/architecture/circuit-breaker-vs-bulkhead.html>)

**See also:** [Retry Patterns](</en/architecture/retry-patterns.html>), [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Circuit Breaker vs Bulkhead Pattern](</en/architecture/circuit-breaker-vs-bulkhead.html>)

**See also:** [Health Check Patterns](</en/architecture/health-check-patterns.html>), [Leader Election in Distributed Systems](</en/architecture/leader-election.html>), [Structured Logging](</en/architecture/structured-logging.html>)

**See also:** [Health Check Patterns](</en/architecture/health-check-patterns.html>), [Leader Election in Distributed Systems](</en/architecture/leader-election.html>), [Structured Logging](</en/architecture/structured-logging.html>)

**See also:** [Health Check Patterns](</en/architecture/health-check-patterns.html>), [Leader Election in Distributed Systems](</en/architecture/leader-election.html>), [Structured Logging](</en/architecture/structured-logging.html>)

**See also:** [Health Check Patterns](</en/architecture/health-check-patterns.html>), [Leader Election in Distributed Systems](</en/architecture/leader-election.html>), [Structured Logging](</en/architecture/structured-logging.html>)

**See also:** [Health Check Patterns](</en/architecture/health-check-patterns.html>), [Leader Election in Distributed Systems](</en/architecture/leader-election.html>), [Structured Logging](</en/architecture/structured-logging.html>)

**See also:** [Health Check Patterns](</en/architecture/health-check-patterns.html>), [Leader Election in Distributed Systems](</en/architecture/leader-election.html>), [Structured Logging](</en/architecture/structured-logging.html>)

**See also:** [Health Check Patterns](</en/architecture/health-check-patterns.html>), [Leader Election in Distributed Systems](</en/architecture/leader-election.html>), [Structured Logging](</en/architecture/structured-logging.html>)
