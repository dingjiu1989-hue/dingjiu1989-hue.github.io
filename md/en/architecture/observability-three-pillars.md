---
title: "Observability: Logs, Metrics, and Traces"
description: "Logs, metrics, traces correlation, cardinality, sampling, storage costs, and the three pillars of observability"
date: 2026-04-29
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/observability-three-pillars.html
---

# Observability: Logs, Metrics, and Traces

Observability is the ability to understand a system's internal state from its external outputs. The three pillars — logs, metrics, and traces — each provide different perspectives. Logs describe discrete events. Metrics provide aggregate measurements. Traces follow requests across service boundaries. Effective observability requires combining all three and correlating them to answer questions about system behavior, especially during incidents. 

Logs are timestamped records of discrete events. They are the most detailed pillar — a log line can contain any amount of structured or unstructured data about what happened, when, and with what context. The challenge is volume. Production systems generate millions of log lines per minute. Without structure and filtering, logs become noise. Structured logging (JSON format) is essential for machine parsing and querying. Log levels (DEBUG, INFO, WARN, ERROR) provide the primary filtering mechanism. 

Metrics are numeric aggregations over time. They are the most efficient storage representation — a single metric stream consumes bytes rather than kilobytes per event. Metrics are ideal for dashboards, alerting, and trend analysis. Common metric types include counters (total requests), gauges (current memory usage), histograms (request latency distribution), and summaries (quantile approximations). Metrics inherently lose individual event detail — you know the 99th percentile latency but not which specific request was slow. 

Traces follow a single request through the distributed system. A trace is composed of spans, where each span represents a unit of work (an HTTP request, a database query, a function call). Spans carry the parent span ID, creating a tree structure that shows the call hierarchy. Traces provide the most information for debugging specific issues but have the highest storage cost. A single trace for a complex request may include hundreds of spans. 

Correlation between pillars is the goal. A trace ID should appear in log entries (structured logging), metric labels, and trace spans. When investigating an issue: a latency spike in metrics triggers an alert, the associated trace ID links to specific traces showing which service caused the delay, and logs at the trace context level reveal the error or slow operation. Without correlation, each pillar is a silo that provides incomplete information. 

Cardinality is the primary scalability challenge. High-cardinality dimensions — customer ID, request ID, session ID — are essential for debugging but explosive for storage. A metric labeled with customer_id across millions of customers creates billions of time series. Metrics systems (Prometheus, M3) struggle with high cardinality. Tracing systems excel here because they naturally capture high-cardinality data within individual traces. Logs fall in between — search indexes can handle high-cardinality fields but at significant storage cost. 

Sampling strategies manage the trace volume problem. Head-based sampling (decide at the root span) is simple but may miss errors that occur rarely. Tail-based sampling (decide after all spans arrive) allows intelligent selection — sample all errors, sample a percentage of successful traces, and ensure critical traces (high-value customers, specific endpoints) are always sampled. Adaptive sampling adjusts the sampling rate based on traffic volume, maintaining a consistent trace storage budget. 

Storage costs drive architectural decisions. Logs are the most expensive per event because they store the full payload. Metrics are the cheapest because they aggregate. Traces are intermediate but explode with request complexity. A cost-effective strategy uses short-term retention for high-cardinality data (7-30 days for traces, 30 days for logs) and long-term retention for aggregated metrics (1-2 years). Tiered storage with warm (fast query) and cold (cheap archive) further optimizes costs. 

The OpenTelemetry project is converging the three pillars. OTel provides a unified API for generating signals, with exporters that send data to any backend. Logs, metrics, and traces share instrumentation context including trace IDs and resource attributes. This unification dramatically improves correlation — with OTel, the three pillars are generated from the same instrumentation and carry the same context, making cross-pillar analysis natural rather than bolted on. 

Choosing an observability backend depends on scale and budget. Self-hosted options (Grafana + Loki for logs, Prometheus for metrics, Tempo for traces) provide cost control but operational overhead. Managed options (Datadog, Honeycomb, New Relic) provide convenience at higher per-event cost. Hybrid approaches (self-hosted for high-volume data, managed for curated dashboards) balance cost and capability.

**See also:** [Cost Per Request Modeling](</en/architecture/cost-per-request.html>), [Structured Logging](</en/architecture/structured-logging.html>), [Distributed Tracing: Deep Dive](</en/architecture/distributed-tracing-deep.html>).

**See also:** [Metrics Types and Monitoring Methodologies](</en/architecture/metrics-types.html>), [Cost Per Request Modeling](</en/architecture/cost-per-request.html>), [Distributed Tracing: Deep Dive](</en/architecture/distributed-tracing-deep.html>)

**See also:** [Metrics Types and Monitoring Methodologies](</en/architecture/metrics-types.html>), [Cost Per Request Modeling](</en/architecture/cost-per-request.html>), [Distributed Tracing: Deep Dive](</en/architecture/distributed-tracing-deep.html>)

**See also:** [Metrics Types and Monitoring Methodologies](</en/architecture/metrics-types.html>), [Cost Per Request Modeling](</en/architecture/cost-per-request.html>), [Distributed Tracing: Deep Dive](</en/architecture/distributed-tracing-deep.html>)

**See also:** [Metrics Types and Monitoring Methodologies](</en/architecture/metrics-types.html>), [Cost Per Request Modeling](</en/architecture/cost-per-request.html>), [Distributed Tracing: Deep Dive](</en/architecture/distributed-tracing-deep.html>)

**See also:** [Metrics Types and Monitoring Methodologies](</en/architecture/metrics-types.html>), [Cost Per Request Modeling](</en/architecture/cost-per-request.html>), [Distributed Tracing: Deep Dive](</en/architecture/distributed-tracing-deep.html>)

**See also:** [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>), [Transactional Outbox Pattern](</en/architecture/transaction-outbox-reliable.html>)

**See also:** [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>), [Transactional Outbox Pattern](</en/architecture/transaction-outbox-reliable.html>)

**See also:** [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>), [Transactional Outbox Pattern](</en/architecture/transaction-outbox-reliable.html>)

**See also:** [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>), [Transactional Outbox Pattern](</en/architecture/transaction-outbox-reliable.html>)

**See also:** [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>), [Transactional Outbox Pattern](</en/architecture/transaction-outbox-reliable.html>)

**See also:** [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>), [Transactional Outbox Pattern](</en/architecture/transaction-outbox-reliable.html>)

**See also:** [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>), [Transactional Outbox Pattern](</en/architecture/transaction-outbox-reliable.html>)

**See also:** [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>), [Transactional Outbox Pattern](</en/architecture/transaction-outbox-reliable.html>)

**See also:** [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>), [Transactional Outbox Pattern](</en/architecture/transaction-outbox-reliable.html>)

**See also:** [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>), [Transactional Outbox Pattern](</en/architecture/transaction-outbox-reliable.html>)

**See also:** [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>), [Transactional Outbox Pattern](</en/architecture/transaction-outbox-reliable.html>)

**See also:** [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>), [Transactional Outbox Pattern](</en/architecture/transaction-outbox-reliable.html>)

**See also:** [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>), [Transactional Outbox Pattern](</en/architecture/transaction-outbox-reliable.html>)
