---
title: "Circuit Breaker vs Bulkhead Pattern"
description: "Differences, when to use each, resilience patterns, and combined application of circuit breaker and bulkhead"
date: 2026-05-19
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/circuit-breaker-vs-bulkhead.html
---

# Circuit Breaker vs Bulkhead Pattern

Circuit breaker and bulkhead are two fundamental resilience patterns from the stability arsenal, but they solve different problems and are most effective when used together. The circuit breaker protects downstream services from cascading failures by failing fast when a dependency is unhealthy. The bulkhead isolates failure by limiting the resources a failing component can consume. Understanding when and how to apply each is essential for building resilient distributed systems. 

The circuit breaker pattern monitors calls to a dependency. When failures exceed a threshold, the circuit breaker trips to the OPEN state, and subsequent calls return immediately with an error without actually invoking the failing dependency. After a timeout, the circuit enters HALF-OPEN state and allows a probe request. If the probe succeeds, the circuit resets to CLOSED. If it fails, it returns to OPEN. This prevents the calling service from wasting resources on a failing dependency and allows the dependency time to recover. 

The three circuit breaker states serve distinct purposes. CLOSED: normal operation, calls proceed with failure counting. OPEN: failures exceed threshold, calls fail fast without invoking the dependency. HALF-OPEN: recovery attempt, limited calls allowed to test if the dependency has recovered. The transition thresholds and timeout durations must be configured per dependency — a critical database may have a higher failure threshold and shorter timeout than a non-critical analytics service. 

The bulkhead pattern isolates failures by partitioning system resources into pools. The name comes from ship design — watertight compartments prevent a hull breach from sinking the entire ship. In software, bulkheads limit the number of concurrent calls to a dependency (semaphore bulkhead) or the size of a thread pool dedicated to a dependency (thread pool bulkhead). When one dependency fails and its calls start queuing, the bulkhead ensures that only the resources allocated to that dependency are consumed. 

Thread pool bulkheads allocate a dedicated thread pool for each dependency. A failing dependency can exhaust its own pool but cannot affect other pools. The trade-off is thread overhead — each dependency pool has its own threads, which increases memory usage and context switching. Semaphore bulkheads are lighter — they just limit the number of concurrent calls without dedicating threads — but provide weaker isolation since blocked threads still share the common thread pool. 

The key difference between the two patterns: circuit breakers actively reject calls during failures (failing fast), while bulkheads passively limit resource consumption (creating backpressure). Circuit breakers protect downstream services from being overwhelmed. Bulkheads protect the calling service from being overwhelmed. A failing database may be behind a circuit breaker to prevent the application from hammering it. A slow buggy downstream service may be behind a bulkhead to prevent it from consuming all application threads. 

When to use each: circuit breakers are the right choice when the downstream service is known to fail or degrade, recovery is expected, and failing fast is better than waiting. Bulkheads are the right choice when resource isolation is critical — when one dependency must not be allowed to consume resources needed by other parts of the system. In practice, both should be used. A bulkhead ensures a failing dependency does not exhaust threads, while a circuit breaker prevents repeated calls to that dependency once failure is confirmed. 

Combined usage provides layered resilience. The bulkhead limits concurrent calls to 10 for a given dependency. The circuit breaker monitors those calls: if 50% fail in a 30-second window, the circuit opens. During the open state, the circuit breaker rejects calls immediately without consuming bulkhead resources. After the timeout, the circuit half-opens and allows a limited number of calls through the bulkhead. The combination prevents both resource exhaustion (bulkhead) and wasted effort (circuit breaker). 

Implementation considerations include metric collection for both patterns. Track circuit breaker state transitions (total, time in each state). Track bulkhead queue depth and rejection counts. Alert on circuit breaker trips (indicates a problem) and bulkhead queue saturation (indicates a load problem). Historical metrics of circuit breaker activity help identify recurring dependency failure patterns and inform threshold tuning. 

Configuration should be dynamic where possible. Circuit breaker thresholds and timeouts may need adjustment during incidents. Bulkhead sizes may need adjustment based on traffic patterns. Feature flags or runtime configuration changes allow tuning without redeployment. The initial configuration should be conservative — circuit breakers trip quickly, bulkheads are sized generously — and tightened based on operational experience.

**See also:** [Timeout and Retry Patterns](</en/architecture/timeout-retry-patterns.html>), [Retry Patterns](</en/architecture/retry-patterns.html>), [Polling Consumer vs Event-Driven Consumer](</en/architecture/polling-consumer.html>).

**See also:** [Timeout and Retry Patterns](</en/architecture/timeout-retry-patterns.html>), [Retry Patterns](</en/architecture/retry-patterns.html>), [Monolith-First Strategy](</en/architecture/monolith-first-strategy.html>)

**See also:** [Timeout and Retry Patterns](</en/architecture/timeout-retry-patterns.html>), [Retry Patterns](</en/architecture/retry-patterns.html>), [Monolith-First Strategy](</en/architecture/monolith-first-strategy.html>)

**See also:** [Bulkhead Pattern for Resilience](</en/architecture/bulkhead-pattern.html>), [Timeout and Retry Patterns](</en/architecture/timeout-retry-patterns.html>), [Retry Patterns](</en/architecture/retry-patterns.html>)

**See also:** [Bulkhead Pattern for Resilience](</en/architecture/bulkhead-pattern.html>), [Timeout and Retry Patterns](</en/architecture/timeout-retry-patterns.html>), [Retry Patterns](</en/architecture/retry-patterns.html>)

**See also:** [Bulkhead Pattern for Resilience](</en/architecture/bulkhead-pattern.html>), [Timeout and Retry Patterns](</en/architecture/timeout-retry-patterns.html>), [Retry Patterns](</en/architecture/retry-patterns.html>)

**See also:** [Stateful vs Stateless Architecture Patterns](</en/architecture/stateful-vs-stateless.html>), [Circuit Breaker Pattern: Building Resilient Systems](</en/architecture/circuit-breaker-pattern.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [Stateful vs Stateless Architecture Patterns](</en/architecture/stateful-vs-stateless.html>), [Circuit Breaker Pattern: Building Resilient Systems](</en/architecture/circuit-breaker-pattern.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [Stateful vs Stateless Architecture Patterns](</en/architecture/stateful-vs-stateless.html>), [Circuit Breaker Pattern: Building Resilient Systems](</en/architecture/circuit-breaker-pattern.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [Stateful vs Stateless Architecture Patterns](</en/architecture/stateful-vs-stateless.html>), [Circuit Breaker Pattern: Building Resilient Systems](</en/architecture/circuit-breaker-pattern.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [Stateful vs Stateless Architecture Patterns](</en/architecture/stateful-vs-stateless.html>), [Circuit Breaker Pattern: Building Resilient Systems](</en/architecture/circuit-breaker-pattern.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [Stateful vs Stateless Architecture Patterns](</en/architecture/stateful-vs-stateless.html>), [Circuit Breaker Pattern: Building Resilient Systems](</en/architecture/circuit-breaker-pattern.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [Stateful vs Stateless Architecture Patterns](</en/architecture/stateful-vs-stateless.html>), [Circuit Breaker Pattern: Building Resilient Systems](</en/architecture/circuit-breaker-pattern.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [Stateful vs Stateless Architecture Patterns](</en/architecture/stateful-vs-stateless.html>), [Circuit Breaker Pattern: Building Resilient Systems](</en/architecture/circuit-breaker-pattern.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [Stateful vs Stateless Architecture Patterns](</en/architecture/stateful-vs-stateless.html>), [Circuit Breaker Pattern: Building Resilient Systems](</en/architecture/circuit-breaker-pattern.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [Stateful vs Stateless Architecture Patterns](</en/architecture/stateful-vs-stateless.html>), [Circuit Breaker Pattern: Building Resilient Systems](</en/architecture/circuit-breaker-pattern.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)
