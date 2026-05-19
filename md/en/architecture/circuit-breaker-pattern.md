---
title: "Circuit Breaker Pattern: Building Resilient Systems"
description: "Circuit breaker state machine (closed/open/half-open), implementation with Resilience4j, monitoring, and recovery strategies."
date: 2026-04-20
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/circuit-breaker-pattern.html
---

# Circuit Breaker Pattern: Building Resilient Systems

The circuit breaker pattern prevents cascading failures in distributed systems. When a service depends on another service that is failing, the circuit breaker detects the failures and stops sending requests to the failing service, allowing it time to recover. This article covers the circuit breaker state machine, implementation with Resilience4j, monitoring, and recovery strategies. 

The Circuit Breaker State Machine 

A circuit breaker has three states: Closed, Open, and Half-Open. 

+-----------+

+--------->| CLOSED |<\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\---------+

| | (正常) | |

| +-----+-----+ |

| | |

[Recovery] [Failure [Success]

complete] threshold] threshold]

| | |

| +-----v-----+ |

+----------| OPEN |----------+

| (断开) |

+-----+-----+

|

[Timeout]

|

+-----v-----+

| HALF-OPEN |

| (半开) |

+-----------+

Closed State 

In the closed state, the circuit breaker allows requests to pass through to the remote service. It tracks the failure rate. When the failure rate exceeds a threshold, the circuit breaker trips to the open state. 

  * All calls pass through.

  * Metrics are tracked (failure count, failure rate, slow call rate).

  * When the failure threshold is exceeded, the breaker opens.




Open State 

In the open state, the circuit breaker immediately rejects requests without calling the remote service. This prevents overwhelming a failing service and allows it time to recover. 

  * All calls fail fast with a `CircuitBreakerOpenException`.

  * A timer starts. When it expires, the breaker transitions to half-open.

  * The open duration should be long enough for the service to recover but short enough to minimize downtime.




Half-Open State 

In the half-open state, the circuit breaker allows a limited number of trial requests. If these requests succeed, the breaker closes. If they fail, the breaker reopens. 

  * A configurable number of trial calls are allowed.

  * Success threshold reached: transition to closed.

  * Any failure: transition back to open.




Implementation with Resilience4j 

Resilience4j is a lightweight, easy-to-use fault tolerance library for Java. It provides circuit breaker, rate limiter, retry, bulkhead, and time limiter modules. 

Basic Circuit Breaker Configuration 

import io.github.resilience4j.circuitbreaker.CircuitBreaker;

import io.github.resilience4j.circuitbreaker.CircuitBreakerConfig;

import io.github.resilience4j.circuitbreaker.CircuitBreakerRegistry;

import java.time.Duration;

// Create a circuit breaker configuration

CircuitBreakerConfig config = CircuitBreakerConfig.custom()

.failureRateThreshold(50) // Open when 50% of calls fail

.slowCallRateThreshold(50) // Open when 50% are slow

.slowCallDurationThreshold(Duration.ofSeconds(2)) // Call > 2s is slow

.waitDurationInOpenState(Duration.ofSeconds(30)) // Time in open before half-open

.permittedNumberOfCallsInHalfOpenState(3) // Trial calls in half-open

.minimumNumberOfCalls(10) // Min calls before evaluating

.slidingWindowSize(20) // Window for metrics

.slidingWindowType(CircuitBreakerConfig.SlidingWindowType.COUNT_BASED)

.recordExceptions(IOException.class, TimeoutException.class)

.ignoreExceptions(BusinessException.class) // Don't count business errors

.build();

// Create the circuit breaker

CircuitBreakerRegistry registry = CircuitBreakerRegistry.of(config);

CircuitBreaker circuitBreaker = registry.circuitBreaker("paymentService");

Decorating Calls 

// Decorate a function with circuit breaker

Supplier decoratedSupplier = CircuitBreaker

.decorateSupplier(circuitBreaker, () -> paymentService.processPayment(request));

// Call with circuit breaker protection

try {

String result = decoratedSupplier.get();

} catch (CircuitBreakerOpenException e) {

// Circuit is open, handle gracefully

return fallbackResponse();

}

Spring Boot Integration 

import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;

import org.springframework.stereotype.Service;

@Service

public class PaymentService {

@CircuitBreaker(name = "paymentService", fallbackMethod = "paymentFallback")

public PaymentResponse processPayment(PaymentRequest request) {

return paymentGateway.charge(request);

}

public PaymentResponse paymentFallback(PaymentRequest request, Throwable t) {

log.warn("Payment service unavailable, using fallback. Error: {}", t.getMessage());

return PaymentResponse.failed("Payment temporarily unavailable, please retry");

}

}

## application.yml

resilience4j.circuitbreaker:

configs:

default:

failureRateThreshold: 50

waitDurationInOpenState: 30s

permittedNumberOfCallsInHalfOpenState: 3

slidingWindowSize: 20

minimumNumberOfCalls: 10

instances:

paymentService:

baseConfig: default

inventoryService:

failureRateThreshold: 30

waitDurationInOpenState: 60s

Python Implementation (Simple) 

import time

import threading

from enum import Enum

class CircuitState(Enum):

CLOSED = "closed"

OPEN = "open"

HALF_OPEN = "half_open"

class CircuitBreaker:

def **init**(self, failure_threshold=5, recovery_timeout=30, half_open_max_calls=3):

self.failure_threshold = failure_threshold

self.recovery_timeout = recovery_timeout

self.half_open_max_calls = half_open_max_calls

self.state = CircuitState.CLOSED

self.failure_count = 0

self.last_failure_time = None

self.half_open_calls = 0

self.lock = threading.Lock()

def call(self, func, fallback_func=None, _args,_ *kwargs):

with self.lock:

if self.state == CircuitState.OPEN:

if time.time() - self.last_failure_time >= self.recovery_timeout:

self.state = CircuitState.HALF_OPEN

self.half_open_calls = 0

else:

return self._handle_open(fallback_func)

if self.state == CircuitState.HALF_OPEN:

if self.half_open_calls >= self.half_open_max_calls:

return self._handle_open(fallback_func)

self.half_open_calls += 1

try:

result = func(_args,_ *kwargs)

self._on_success()

return result

except Exception as e:

self._on_failure()

return self._handle_open(fallback_func)

def _on_success(self):

with self.lock:

if self.state == CircuitState.HALF_OPEN:

self.state = CircuitState.CLOSED

self.failure_count = 0

elif self.state == CircuitState.CLOSED:

self.failure_count = max(0, self.failure_count - 1)

def _on_failure(self):

with self.lock:

self.failure_count += 1

self.last_failure_time = time.time()

if self.failure_count >= self.failure_threshold:

self.state = CircuitState.OPEN

def _handle_open(self, fallback_func):

if fallback_func:

return fallback_func()

raise CircuitBreakerOpenException("Circuit breaker is open")

Monitoring Circuit Breakers 

Exposing Metrics 

Resilience4j integrates with Micrometer for metrics export: 

// Register circuit breaker metrics with Micrometer

MeterRegistry meterRegistry = new SimpleMeterRegistry();

CircuitBreakerMetrics circuitBreakerMetrics = 

circuitBreaker.getMetrics();

// Record state changes

circuitBreaker.getEventPublisher()

.onStateTransition(event -> {

log.info("Circuit breaker state changed: {} -> {}", 

event.getStateTransition().getFromState(),

event.getStateTransition().getToState());

})

.onFailureRateExceeded(event -> {

log.warn("Failure rate exceeded threshold: {}", 

event.getFailureRate());

});

Key Metrics to Monitor 

  * **State** : Is the circuit closed, open, or half-open?

  * **Failure rate** : Current failure rate within the sliding window.

  * **Call count** : Total calls, successful calls, failed calls, and ignored calls.

  * **Not permitted calls** : Number of calls rejected while the breaker is open.

  * **Buffered calls** : Number of buffered calls in the current sliding window.




## Prometheus metric format (from Resilience4j exporter)

resilience4j_circuitbreaker_state{name="paymentService",state="closed"} 1

resilience4j_circuitbreaker_calls{name="paymentService",kind="successful"} 142

resilience4j_circuitbreaker_calls{name="paymentService",kind="failed"} 8

resilience4j_circuitbreaker_not_permitted_calls{name="paymentService"} 34

Grafana Alert Rules 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- alert: CircuitBreakerOpen

expr: resilience4j_circuitbreaker_state{state="open"} == 1

for: 5m

annotations:

summary: "Circuit breaker {{ $labels.name }} is open"

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- alert: HighFailureRate

expr: resilience4j_circuitbreaker_failure_rate > 40

for: 2m

annotations:

summary: "Circuit breaker {{ $labels.name }} failure rate is {{ $value }}%"

Recovery Strategies 

Gradual Recovery 

When a circuit breaker closes after recovery, the previously failing service may be overwhelmed by the sudden return of all traffic. Use gradual recovery: 

// Gradual recovery: allow 50% of usual traffic initially, ramp up

CircuitBreakerConfig config = CircuitBreakerConfig.custom()

.waitDurationInOpenState(Duration.ofSeconds(30))

.permittedNumberOfCallsInHalfOpenState(10) // Allow 10 trial calls

.slidingWindowSize(20)

.build();

Fallback Strategies 

  * **Cache** : Return cached response from the last successful call.

  * **Default value** : Return a safe default (empty list, zero).

  * **Degraded functionality** : Return partial results (e.g., show product page without recommendations).

  * **Queue for retry** : Store the request and retry later.




@CircuitBreaker(name = "recommendationService", fallbackMethod = "recommendationFallback")

public List getRecommendations(String userId) {

return recommendationClient.fetch(userId);

}

public List recommendationFallback(String userId, Throwable t) {

if (t instanceof CircuitBreakerOpenException) {

log.info("Recommendations unavailable, returning popular products instead");

return popularProductsCache.get("global");

}

return Collections.emptyList();

}

Bulkhead Pattern 

Combine circuit breakers with bulkheads to isolate failure domains: 

import io.github.resilience4j.bulkhead.Bulkhead;

import io.github.resilience4j.bulkhead.BulkheadConfig;

BulkheadConfig bulkheadConfig = BulkheadConfig.custom()

.maxConcurrentCalls(10)

.maxWaitDuration(Duration.ofMillis(500))

.build();

Bulkhead bulkhead = Bulkhead.of("paymentService", bulkheadConfig);

// Combined: circuit breaker wraps bulkhead wraps function

Supplier decorated = Decorators

.ofSupplier(() -> paymentService.processPayment(request))

.withCircuitBreaker(circuitBreaker)

.withBulkhead(bulkhead)

.decorate();

Common Pitfalls 

  * **Too short timeout** : Circuit opens too frequently due to normal latency spikes. Set thresholds based on observed p99 latency.

  * **Too long open duration** : Service recovers quickly but the circuit stays open. Monitor recovery patterns and tune accordingly.

  * **No fallback** : An open circuit breaker still needs to return something useful to the caller.

  * **All-or-nothing thinking** : Not all dependencies need circuit breakers. Use them for external APIs, databases, and critical services.

  * **Ignoring half-open** : The half-open state is critical for recovery. Do not skip it.




Conclusion 

The circuit breaker pattern prevents cascading failures by detecting when a remote service is failing and stopping calls to it. Implement the three-state state machine (closed, open, half-open) with libraries like Resilience4j. Monitor circuit breaker state in production dashboards. Combine with fallbacks, bulkheads, and gradual recovery for a comprehensive resilience strategy. Circuit breakers are not a silver bullet, but they are an essential tool in building systems that degrade gracefully instead of failing catastrophically.

**See also:** [Retry Patterns](</en/architecture/retry-patterns.html>), [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Circuit Breaker vs Bulkhead Pattern](</en/architecture/circuit-breaker-vs-bulkhead.html>).

**See also:** [Retry Patterns](</en/architecture/retry-patterns.html>), [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Circuit Breaker vs Bulkhead Pattern](</en/architecture/circuit-breaker-vs-bulkhead.html>)

**See also:** [Retry Patterns](</en/architecture/retry-patterns.html>), [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Circuit Breaker vs Bulkhead Pattern](</en/architecture/circuit-breaker-vs-bulkhead.html>)

**See also:** [Bulkhead Pattern for Resilience](</en/architecture/bulkhead-pattern.html>), [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Retry Patterns](</en/architecture/retry-patterns.html>)

**See also:** [Bulkhead Pattern for Resilience](</en/architecture/bulkhead-pattern.html>), [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Retry Patterns](</en/architecture/retry-patterns.html>)

**See also:** [Bulkhead Pattern for Resilience](</en/architecture/bulkhead-pattern.html>), [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Retry Patterns](</en/architecture/retry-patterns.html>)

**See also:** [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>), [CQRS Pattern: Command Query Responsibility Segregation](</en/architecture/cqrs-pattern.html>), [Backend for Frontend (BFF) Pattern](</en/architecture/backend-for-frontend.html>)

**See also:** [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>), [CQRS Pattern: Command Query Responsibility Segregation](</en/architecture/cqrs-pattern.html>), [Backend for Frontend (BFF) Pattern](</en/architecture/backend-for-frontend.html>)

**See also:** [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>), [CQRS Pattern: Command Query Responsibility Segregation](</en/architecture/cqrs-pattern.html>), [Backend for Frontend (BFF) Pattern](</en/architecture/backend-for-frontend.html>)

**See also:** [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>), [CQRS Pattern: Command Query Responsibility Segregation](</en/architecture/cqrs-pattern.html>), [Backend for Frontend (BFF) Pattern](</en/architecture/backend-for-frontend.html>)

**See also:** [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>), [CQRS Pattern: Command Query Responsibility Segregation](</en/architecture/cqrs-pattern.html>), [Backend for Frontend (BFF) Pattern](</en/architecture/backend-for-frontend.html>)

**See also:** [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>), [CQRS Pattern: Command Query Responsibility Segregation](</en/architecture/cqrs-pattern.html>), [Backend for Frontend (BFF) Pattern](</en/architecture/backend-for-frontend.html>)
