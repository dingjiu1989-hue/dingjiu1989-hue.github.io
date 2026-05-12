---
title: "Metric Collection"
description: "Master metric collection: agent-based, pull-based, and push-based approaches, cardinality management, and observability"
date: 2026-05-12
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/metric-collection.html
---

# Metric Collection

# Metric Collection

  


Metric collection is the practice of gathering numerical measurements from applications and infrastructure. Metrics provide insight into system health, performance, and usage patterns. This article covers the three main collection approaches—agent-based, pull-based, and push-based—along with cardinality management and best practices.

  
  
  
  


##  Metric Types

  
  
  
  


Metrics fall into several categories. System metrics measure infrastructure: CPU usage, memory consumption, disk I/O, network traffic. Application metrics measure software behavior: request rate, error rate, response time, queue depth. Business metrics measure business outcomes: orders per minute, active users, revenue.

  
  
  
  


Each metric has a name, value, timestamp, and optional dimensions (labels or tags). Dimensions provide context: `http_requests_total{method="GET", path="/api/users", status="200"}`. Dimensions enable slicing and filtering of metric data.

  
  
  
  


##  Agent-Based Collection

  
  
  
  


Agent-based collection runs a monitoring agent on each node. The agent collects system metrics (CPU, memory, disk, network) and forwards them to a central monitoring system. Examples include collectd, Telegraf, and Datadog Agent.

  
  
  
  


Agents handle local aggregation and buffering, reducing the load on the central system. They can collect metrics that are only available locally (detailed process information, log file sizes). The agent's configuration controls which metrics are collected and at what frequency.

  
  
  
  


Agent-based collection is reliable—the agent continues collecting even if the central system is unavailable. When connectivity is restored, buffered metrics are forwarded. The trade-off is the operational cost of managing agents on every node.

  
  
  
  


##  Pull-Based Collection

  
  
  
  


Pull-based collection (also called scrape-based) has the monitoring system periodically fetch metrics from instrumented targets. Prometheus is the most prominent pull-based system. Each service exposes a metrics endpoint (`/metrics`) that Prometheus scrapes at configured intervals.

  
  
  
  


Pull-based collection simplifies discovery. Prometheus queries a service discovery mechanism (Kubernetes, Consul) to find targets. New targets are automatically discovered and scraped. Scaling is straightforward: add scrapers to handle more targets.

  
  
  
  


The pull model works well for batch workloads and scheduled jobs that are not always running. The Prometheus pushgateway bridges this gap by accepting pushed metrics from short-lived jobs for later scraping.

  
  
  
  


##  Push-Based Collection

  
  
  
  


Push-based collection has services actively send metrics to a central collector. Graphite, StatsD, and InfluxDB use push-based models. The service sends metrics at regular intervals or on specific events.

  
  
  
  


Push-based collection is simpler to implement in application code—just send metrics to a known address. It works well for ephemeral services and serverless functions that may not be running when a pull-based system tries to scrape them.

  
  
  
  


The trade-off is reliability. If the central collector is unavailable, metrics may be lost unless the client buffers them. Authorization needs to be handled differently since the collector receives connections from many sources.

  
  
  
  


##  Cardinality Management

  
  
  
  


Metric cardinality refers to the number of unique dimension combinations. Each dimension value combination creates a unique metric time series. If you have a metric with dimensions `user_id` (10,000 values) and `action` (10 values), you have 100,000 time series.

  
  
  
  


High cardinality causes performance problems. Monitoring systems struggle with millions of time series. Storage costs increase. Query performance degrades. The monitoring system may reject high-cardinality metrics entirely.

  
  
  
  


Cardinality management limits uncontrolled dimension explosion. Avoid putting high-cardinality values (user IDs, session IDs, request IDs) as metric dimensions. Use logging or tracing for high-cardinality data instead. Aggregate metrics before sending to reduce unique series counts.

  
  
  
  


##  Collection Frequency

  
  
  
  


Collection frequency balances granularity against cost. High-frequency collection (every 10 seconds) provides detailed data but increases storage and network costs. Low-frequency collection (every minute) reduces costs but may miss brief spikes.

  
  
  
  


The appropriate frequency depends on the metric type. System metrics benefit from high frequency to detect brief CPU or memory spikes. Business metrics are typically fine with lower frequency. Different metrics can have different collection intervals.

  
  
  
  


##  Best Practices

  
  
  
  


Use consistent metric naming conventions. Follow a hierarchical naming structure: `service.layer.operation.unit` (e.g., `orders.api.create.latency_seconds`). Include meaningful dimensions while avoiding cardinality explosion.

  
  
  
  


Define metric types clearly. Counters increase monotonically (total requests). Gauges represent current values (active connections). Histograms track distributions (request latency). Summaries provide quantile estimates.

  
  
  
  


Instrument all services from the start. Adding metrics after deployment is harder than building them in. Establish SLIs (Service Level Indicators) for each service and monitor them consistently. Correlate metrics with deployment events to identify performance regressions.

  
  
  
  


Metric collection is the foundation of observability. Well-designed metrics enable rapid diagnosis, capacity planning, and performance optimization. Combined with structured logging and distributed tracing, metrics provide the visibility needed to operate complex distributed systems reliably.
