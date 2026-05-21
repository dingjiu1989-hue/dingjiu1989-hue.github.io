---
title: "Retry Patterns"
description: "Learn retry strategies: exponential backoff, jitter, retry budgets, and circuit breaker integration for resilient systems"
date: 2026-05-04
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/retry-patterns.html
---

# Retry Patterns

Retry patterns are fundamental to building resilient distributed systems. Network failures, transient service unavailability, and resource contention are inevitable in any distributed architecture. A well-designed retry mechanism can gracefully handle these failures without overwhelming downstream services or degrading user experience. This article covers exponential backoff, jitter, retry budgets, and integration with circuit breakers. 

Exponential Backoff 

Exponential backoff is the most basic retry strategy. After a failure, the system waits an increasing amount of time before each subsequent retry. The wait time typically doubles with each attempt: 100ms, 200ms, 400ms, 800ms, and so on, up to a maximum delay. This prevents the retry storm problem, where many clients retry simultaneously and overwhelm an already-stressed service. 

The formula is straightforward: `delay = base_delay * (2 ^ attempt)`. Most implementations also cap the maximum delay to prevent excessively long waits. Common base delays range from 50ms to 500ms, with maximum delays typically between 10 and 60 seconds. 

The Importance of Jitter 

Pure exponential backoff can cause a phenomenon called thundering herd. When a service recovers after an outage, all clients may retry at exactly the same interval, creating a synchronous wave of requests that can overwhelm the service again. Jitter adds randomness to the delay calculation, spreading retry attempts across time. 

The most effective jitter strategy is "full jitter": `delay = random_between(0, min(cap, base * 2 ^ attempt))`. This spreads retries evenly across the interval window. Amazon's AWS SDKs and Google's client libraries use variants of this approach. Full jitter dramatically reduces the probability of synchronized retries. 

Retry Budgets 

Not all failures justify retries. A retry budget limits the total number of retries a service will attempt within a time window. When the budget is exhausted, further retries are rejected immediately, and the error propagates to the caller. Retry budgets prevent a cascade of retries from amplifying an outage. 

A common implementation tracks retry attempts as a fraction of total requests. If retries exceed, say, 20% of requests in a one-minute window, additional retries are blocked. This protects both the calling service (from wasting resources on likely-to-fail requests) and the downstream service (from receiving excessive retry traffic). 

Circuit Breaker Integration 

Retries and circuit breakers are complementary patterns with a critical interaction. A circuit breaker should open when retries consistently fail, preventing further retries until the downstream service has time to recover. Without this integration, retries can prevent a circuit breaker from opening by absorbing failures that would otherwise trigger the breaker. 

The typical pattern is: retry within the circuit breaker's closed state. If retries continue to fail, the circuit breaker opens and subsequent requests fail fast without attempting retries. After the circuit breaker's timeout period, it transitions to half-open, allowing limited retries to test recovery. 

Idempotency and Retries 

A fundamental requirement for safe retries is idempotency. If the first request succeeded but the response was lost, a retry will execute the operation again. Idempotent operations are essential. Idempotency keys, idempotent PUT operations, and database upserts are common techniques. 

Configuration Best Practices 

Retry policies should be configurable per dependency. A critical database query might justify more aggressive retries than a non-essential analytics call. Monitor retry rates, success rates, and latency impact. If retries account for a significant portion of traffic, investigate the root cause rather than tuning retry parameters. 

Modern resilience libraries like Resilience4j, Polly (.NET), and Tenacity (Python) provide composable retry, circuit breaker, and bulkhead decorators with built-in metrics. Using these libraries standardizes retry behavior across services and provides consistent observability. 

Retries are a powerful tool, but they are not a substitute for addressing underlying reliability issues. Used judiciously with backoff, jitter, budgets, and circuit breakers, they make distributed systems gracefully resilient to transient failures.

**See also:** [Timeout and Retry Patterns](</en/architecture/timeout-retry-patterns.html>), [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Circuit Breaker vs Bulkhead Pattern](</en/architecture/circuit-breaker-vs-bulkhead.html>).

**See also:** [Timeout and Retry Patterns](</en/architecture/timeout-retry-patterns.html>), [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>)

**See also:** [Timeout and Retry Patterns](</en/architecture/timeout-retry-patterns.html>), [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>)

**See also:** [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Timeout and Retry Patterns](</en/architecture/timeout-retry-patterns.html>), [Bulkhead Pattern for Resilience](</en/architecture/bulkhead-pattern.html>)

**See also:** [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Timeout and Retry Patterns](</en/architecture/timeout-retry-patterns.html>), [Bulkhead Pattern for Resilience](</en/architecture/bulkhead-pattern.html>)

**See also:** [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Timeout and Retry Patterns](</en/architecture/timeout-retry-patterns.html>), [Bulkhead Pattern for Resilience](</en/architecture/bulkhead-pattern.html>)

**See also:** [Chaos Engineering: Building Resilient Systems](</en/architecture/chaos-engineering.html>), [Circuit Breaker Pattern: Building Resilient Systems](</en/architecture/circuit-breaker-pattern.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [Chaos Engineering: Building Resilient Systems](</en/architecture/chaos-engineering.html>), [Circuit Breaker Pattern: Building Resilient Systems](</en/architecture/circuit-breaker-pattern.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [Chaos Engineering: Building Resilient Systems](</en/architecture/chaos-engineering.html>), [Circuit Breaker Pattern: Building Resilient Systems](</en/architecture/circuit-breaker-pattern.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [Chaos Engineering: Building Resilient Systems](</en/architecture/chaos-engineering.html>), [Circuit Breaker Pattern: Building Resilient Systems](</en/architecture/circuit-breaker-pattern.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [Chaos Engineering: Building Resilient Systems](</en/architecture/chaos-engineering.html>), [Circuit Breaker Pattern: Building Resilient Systems](</en/architecture/circuit-breaker-pattern.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [Chaos Engineering: Building Resilient Systems](</en/architecture/chaos-engineering.html>), [Circuit Breaker Pattern: Building Resilient Systems](</en/architecture/circuit-breaker-pattern.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [Chaos Engineering: Building Resilient Systems](</en/architecture/chaos-engineering.html>), [Circuit Breaker Pattern: Building Resilient Systems](</en/architecture/circuit-breaker-pattern.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [Chaos Engineering: Building Resilient Systems](</en/architecture/chaos-engineering.html>), [Circuit Breaker Pattern: Building Resilient Systems](</en/architecture/circuit-breaker-pattern.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [Chaos Engineering: Building Resilient Systems](</en/architecture/chaos-engineering.html>), [Circuit Breaker Pattern: Building Resilient Systems](</en/architecture/circuit-breaker-pattern.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [Chaos Engineering: Building Resilient Systems](</en/architecture/chaos-engineering.html>), [Circuit Breaker Pattern: Building Resilient Systems](</en/architecture/circuit-breaker-pattern.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [Chaos Engineering: Building Resilient Systems](</en/architecture/chaos-engineering.html>), [Circuit Breaker Pattern: Building Resilient Systems](</en/architecture/circuit-breaker-pattern.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [Chaos Engineering: Building Resilient Systems](</en/architecture/chaos-engineering.html>), [Circuit Breaker Pattern: Building Resilient Systems](</en/architecture/circuit-breaker-pattern.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [Chaos Engineering: Building Resilient Systems](</en/architecture/chaos-engineering.html>), [Circuit Breaker Pattern: Building Resilient Systems](</en/architecture/circuit-breaker-pattern.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)
