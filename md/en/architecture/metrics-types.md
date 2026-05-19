---
title: "Metrics Types and Monitoring Methodologies"
description: "Counters, gauges, histograms, summaries, RED method, USE method, and the four golden signals"
date: 2026-04-27
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/metrics-types.html
---

# Metrics Types and Monitoring Methodologies

Metrics provide the quantitative foundation for understanding system health, detecting anomalies, and driving alerts. The four primary metric types — counters, gauges, histograms, and summaries — each serve distinct purposes. Combined with monitoring methodologies like RED, USE, and the Four Golden Signals, they form a complete picture of system behavior and are essential for effective operations. 

Counters are monotonically increasing values that only go up (or reset to zero on restart). They measure cumulative events: total requests served, total errors, total bytes sent. Counters are useful for computing rates over time — requests per second, error rate — which are the most common observability signals. A counter alone is rarely useful; it is the rate of change that matters. Rate computation requires tracking the counter value over a time window and dividing the delta by the window duration. 

Gauges represent a single numeric value that can go up or down arbitrarily. They measure current state: memory usage, CPU utilization, queue depth, active connections, number of goroutines. Gauges are instantaneous snapshots and should be sampled frequently enough to capture meaningful variation. Unlike counters, gauges are useful as absolute values — a memory gauge at 95% of available memory is actionable on its own. 

Histograms sample observations and count them in configurable buckets. They measure distributions: request latency, response sizes, batch processing times. Histograms estimate quantiles (p50, p99, p999) that show what latency the typical user experiences versus the slowest users. The bucket configuration requires understanding the expected value range. Buckets should be roughly exponentially spaced: 1ms, 5ms, 10ms, 25ms, 50ms, 100ms, 250ms, 500ms, 1s, 2.5s, 5s, 10s. Fine buckets where most values fall and wider buckets at the extremes. 

Summaries are similar to histograms but compute quantiles on the client side before exposing them as metric streams. This reduces storage costs because the aggregation system receives pre-computed quantiles rather than raw bucket counts. The trade-off is that summary quantiles cannot be aggregated across application instances — the p99 of all instances combined is not the average of each instance's p99. For global quantile accuracy, histograms should be used with a metrics system that supports accurate quantile aggregation. 

The RED method monitors services from a user perspective: Rate (requests per second), Errors (failed requests per second), and Duration (request latency distribution). RED applies to every service that users interact with. It answers: how much traffic am I receiving? How many failures? How slow am I? RED is the most intuitive methodology for service-level monitoring and forms the basis of Service Level Objectives (SLOs) and Service Level Indicators (SLIs). 

The USE method monitors resources from an infrastructure perspective: Utilization (percentage of resource capacity), Saturation (amount of work the resource cannot service), and Errors (failure count). USE applies to infrastructure resources: CPU, memory, disk I/O, network bandwidth. A high-utilization CPU is working hard. A saturated CPU has queued work. An erroring CPU is failing instructions. USE is most useful for bottleneck analysis — identifying which resource is constraining performance. 

The Four Golden Signals, popularized by Google's SRE book, combine RED and USE concepts: Latency (time to serve a request), Traffic (demand on the system), Errors (explicit and implicit failures), and Saturation (how "full" the service is). Implicit errors are responses that return successfully but with incorrect content or excessive latency — a 200 OK response that takes 30 seconds is a failure from the user's perspective. 

Metric naming conventions maintain consistency across services. A hierarchical naming scheme is typical: service_name.metric_name.operation.result. For example: orders_service.request_count.create_order.total, orders_service.latency_seconds.create_order.p99. Units should be embedded in the name (seconds, bytes, count). Labels or tags add cardinality dimensions: status code, endpoint, version. Label cardinality must be bounded to prevent metrics system overload. 

Metric retention and aggregation tiers optimize storage. Raw high-resolution metrics (10-second intervals) are retained for short periods (7-30 days). Rolled-up aggregates (5-minute, 1-hour, 1-day resolutions) extend retention to years. Long-term trends use high-level aggregates; incident investigation uses raw metrics. The metrics system (Prometheus, VictoriaMetrics, M3) should transparently handle this downsampling.

**See also:** [Observability: Logs, Metrics, and Traces](</en/architecture/observability-three-pillars.html>), [Choreography Patterns](</en/architecture/choreography-patterns.html>), [Circuit Breaker vs Bulkhead Pattern](</en/architecture/circuit-breaker-vs-bulkhead.html>).

**See also:** [Observability: Logs, Metrics, and Traces](</en/architecture/observability-three-pillars.html>), [Circuit Breaker vs Bulkhead Pattern](</en/architecture/circuit-breaker-vs-bulkhead.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>)

**See also:** [Observability: Logs, Metrics, and Traces](</en/architecture/observability-three-pillars.html>), [Circuit Breaker vs Bulkhead Pattern](</en/architecture/circuit-breaker-vs-bulkhead.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>)

**See also:** [Observability: Logs, Metrics, and Traces](</en/architecture/observability-three-pillars.html>), [Circuit Breaker vs Bulkhead Pattern](</en/architecture/circuit-breaker-vs-bulkhead.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>)

**See also:** [Observability: Logs, Metrics, and Traces](</en/architecture/observability-three-pillars.html>), [Circuit Breaker vs Bulkhead Pattern](</en/architecture/circuit-breaker-vs-bulkhead.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>)

**See also:** [Observability: Logs, Metrics, and Traces](</en/architecture/observability-three-pillars.html>), [Circuit Breaker vs Bulkhead Pattern](</en/architecture/circuit-breaker-vs-bulkhead.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>)

**See also:** [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>), [Transactional Outbox Pattern](</en/architecture/transaction-outbox-reliable.html>)

**See also:** [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>), [Transactional Outbox Pattern](</en/architecture/transaction-outbox-reliable.html>)

**See also:** [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>), [Transactional Outbox Pattern](</en/architecture/transaction-outbox-reliable.html>)
