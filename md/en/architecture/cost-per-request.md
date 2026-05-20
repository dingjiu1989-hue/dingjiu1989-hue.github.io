---
title: "Cost Per Request Modeling"
description: "Compute, storage, network, database per-request cost modeling, and optimization strategies"
date: 2026-04-22
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/cost-per-request.html
---

# Cost Per Request Modeling

Cost per request modeling decomposes infrastructure costs into the cost of serving a single request. This metric enables data-driven optimization: if a request costs \$0.001 and you serve 100 million requests per month, a 20% reduction saves \$20,000 monthly. More importantly, understanding per-request costs reveals which features, endpoints, or user segments are profitable and which may need rethinking. 

Compute cost is calculated from the resources consumed during request processing. For a containerized service with 500 millicores of CPU and 512 MB of memory allocation, running on instances costing \$50/month with 100 requests per second capacity, the per-request compute cost is approximately \$0.0000058 (50 / 30 / 86400 / 100 * 500/1000). This minimal per-request cost compounds through the chain of services involved — the API gateway, multiple backend services, and background job processors all contribute. 

Storage cost includes database capacity, object storage, and caching layers. A request that reads 10 KB of product data, writes 2 KB of order data, and caches the result for 60 seconds has a direct storage cost plus the amortized cost of the storage infrastructure. Database IOPS and provisioned throughput costs are usually larger than raw storage costs. For relational databases, each request's storage cost must account for the total database cost divided across all served requests, not just the marginal cost. 

Network cost is often the easiest to quantify. Cloud providers charge for inter-zone, inter-region, and egress traffic. A request that enters through the load balancer, hits three services across two availability zones, and returns a 50 KB response incurs network costs at each hop. Network costs scale linearly with response size and service depth. Optimizing network cost involves reducing response sizes (compression, partial responses), collocating services in the same availability zone, and using internal load balancers. 

Database per-request cost depends on query complexity and data volume. A simple primary key lookup costs less than a full-text search or a join across multiple tables. Write operations generally cost more than reads — they require transaction log writes, index updates, and replication. The database cost per request should include: query CPU time, IOPS consumed, data transfer, and a proportional share of the database instance cost. For serverless databases (Aurora Serverless, DynamoDB on-demand), per-request costs are directly observable. 

Optimization strategies target the highest-cost components first. Instrument every request with cost attribution tags: feature, user segment, endpoint, service. Aggregate costs by these dimensions. Pareto principle applies — 20% of features typically drive 80% of infrastructure cost. Common high-cost patterns include: expensive database queries in hot paths, excessive logging for high-traffic endpoints, unnecessary API calls in critical request flows, and large response payloads with unused fields. 

Caching reduces all cost dimensions simultaneously. A cached response eliminates compute, storage, and network costs for the downstream services. Cache hit ratio directly multiplies cost savings. A 99% cache hit ratio means the full request cost is paid for only 1% of requests. The cache layer itself has a cost (Redis nodes, CDN bandwidth), but this is typically far smaller than the cost of serving requests from origin. 

Request batching reduces per-request overhead. Instead of making 20 individual requests to fetch related data, a single batch request reduces network round trips, database queries, and serialization overhead. The per-unit cost decreases as batch size increases, subject to diminishing returns at very large batch sizes. Batch endpoints should have reasonable maximum sizes to prevent memory and latency issues. 

Cost attribution requires distributed tracing metadata. Each trace span should carry cost-related attributes: service name, instance type, data size processed, cache hit status, and database query cost. The tracing system can then sum costs across spans to compute end-to-end per-request cost. This correlation enables architects to identify the most expensive path for any request and target optimization efforts effectively. 

Right-sizing infrastructure is the fundamental cost optimization. Over-provisioned services waste money on idle capacity. Under-provisioned services waste money on performance-related customer churn. Autoscaling policies should target 60-70% utilization during peak — low enough to handle traffic spikes, high enough to avoid waste. For services with predictable traffic patterns, scheduled scaling reduces costs further by matching capacity to expected load.

**See also:** [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [Zero-Downtime Deployment Strategies](</en/architecture/zero-downtime-deployment.html>), [Zero-Downtime Database Migrations](</en/architecture/database-migration-zero-downtime.html>).

**See also:** [Zero-Downtime Database Migrations](</en/architecture/database-migration-zero-downtime.html>), [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>)

**See also:** [Zero-Downtime Database Migrations](</en/architecture/database-migration-zero-downtime.html>), [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>)

**See also:** [Zero-Downtime Database Migrations](</en/architecture/database-migration-zero-downtime.html>), [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>)

**See also:** [Zero-Downtime Database Migrations](</en/architecture/database-migration-zero-downtime.html>), [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>)

**See also:** [Zero-Downtime Database Migrations](</en/architecture/database-migration-zero-downtime.html>), [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>)

**See also:** [Distributed ID Generation](</en/architecture/distributed-id.html>), [Distributed Tracing: Deep Dive](</en/architecture/distributed-tracing-deep.html>), [Monolith-First Strategy](</en/architecture/monolith-first-strategy.html>)

**See also:** [Distributed ID Generation](</en/architecture/distributed-id.html>), [Distributed Tracing: Deep Dive](</en/architecture/distributed-tracing-deep.html>), [Monolith-First Strategy](</en/architecture/monolith-first-strategy.html>)

**See also:** [Distributed ID Generation](</en/architecture/distributed-id.html>), [Distributed Tracing: Deep Dive](</en/architecture/distributed-tracing-deep.html>), [Monolith-First Strategy](</en/architecture/monolith-first-strategy.html>)

**See also:** [Distributed ID Generation](</en/architecture/distributed-id.html>), [Distributed Tracing: Deep Dive](</en/architecture/distributed-tracing-deep.html>), [Monolith-First Strategy](</en/architecture/monolith-first-strategy.html>)

**See also:** [Distributed ID Generation](</en/architecture/distributed-id.html>), [Distributed Tracing: Deep Dive](</en/architecture/distributed-tracing-deep.html>), [Monolith-First Strategy](</en/architecture/monolith-first-strategy.html>)

**See also:** [Distributed ID Generation](</en/architecture/distributed-id.html>), [Distributed Tracing: Deep Dive](</en/architecture/distributed-tracing-deep.html>), [Monolith-First Strategy](</en/architecture/monolith-first-strategy.html>)

**See also:** [Distributed ID Generation](</en/architecture/distributed-id.html>), [Distributed Tracing: Deep Dive](</en/architecture/distributed-tracing-deep.html>), [Monolith-First Strategy](</en/architecture/monolith-first-strategy.html>)

**See also:** [Distributed ID Generation](</en/architecture/distributed-id.html>), [Distributed Tracing: Deep Dive](</en/architecture/distributed-tracing-deep.html>), [Monolith-First Strategy](</en/architecture/monolith-first-strategy.html>)

**See also:** [Distributed ID Generation](</en/architecture/distributed-id.html>), [Distributed Tracing: Deep Dive](</en/architecture/distributed-tracing-deep.html>), [Monolith-First Strategy](</en/architecture/monolith-first-strategy.html>)
