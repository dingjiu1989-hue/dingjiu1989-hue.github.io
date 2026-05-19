---
title: "Event-Driven Architecture Patterns: Kafka, RabbitMQ, SQS, and EventBridge Compared"
description: "Design event-driven systems with practical patterns — event sourcing, CQRS, sagas, and choosing the right message broker."
date: 2025-10-17
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/event-driven-architecture-guide.html
---

# Event-Driven Architecture Patterns: Kafka, RabbitMQ, SQS, and EventBridge Compared

Event-driven architecture (EDA) is the pattern behind the most scalable systems — from Netflix's microservices to Stripe's payment processing. Instead of services calling each other directly (request-response), they communicate through events (messages about things that happened). This guide covers the patterns, message brokers, and practical implementation of event-driven systems.

## Core Event-Driven Patterns

Pattern| How It Works| Use Case| Complexity  
---|---|---|---  
Event Notification| "Order #123 was placed" — fire and forget, subscribers react| Send email on signup, update search index on content change| Low  
Event-Carried State Transfer| Events contain all data subscribers need (no callback to source)| Catalog service publishes full product data — search, pricing, and inventory consume it| Low-Medium  
Event Sourcing| State is derived from a sequence of events (not a current snapshot)| Banking transactions, audit logs, undo/redo functionality| High  
CQRS (Command Query Responsibility Segregation)| Separate read and write models — writes go through events, reads from materialized views| High-read, complex-query applications (e-commerce product search)| High  
Saga (Distributed Transaction)| A sequence of local transactions, each compensated if a later step fails| Order fulfillment: reserve inventory → charge payment → schedule shipping| High  
  
## Message Broker Comparison

Broker| Type| Throughput| Latency| Best For  
---|---|---|---|---  
Apache Kafka| Distributed event log| 1M+ msg/s| 2-20ms| High-throughput event streaming, event sourcing, data pipelines  
RabbitMQ| Message queue (AMQP)| 50K msg/s| <1ms| Task distribution, RPC, complex routing patterns  
Amazon SQS| Managed message queue| Unlimited (AWS scaling)| 1-50ms| AWS-native, zero ops, FIFO when ordering matters  
Google Pub/Sub| Managed pub/sub| Unlimited (GCP scaling)| 1-10ms| GCP-native, push subscriptions, global by default  
Redis Streams| In-memory event log| 100K msg/s| <1ms| Lightweight event streaming, already have Redis  
NATS| Lightweight pub/sub| 1M+ msg/s| <1ms| Low-latency, edge, IoT, microservices  
  
## When to Go Event-Driven

Situation| Event-Driven?| Why  
---|---|---  
Monolith → microservices migration| Yes — use events to decouple| Events let services evolve independently  
Multiple services need to react to the same event| Yes — pub/sub is the pattern| One event, many consumers, no coupling  
Simple CRUD app, single database| No — request-response is fine| EDA adds complexity; don't need it yet  
Need audit trail of all state changes| Yes — event sourcing| Events ARE the audit trail  
Data analytics / real-time dashboards| Yes — event streaming| Kafka → stream processing → real-time views  
Two services need a synchronous response| No — use REST/gRPC| Events are async; request-response is simpler for sync needs  
  
## Implementing a Saga: Order Fulfillment Example
    
    
    # Saga pattern: orchestration-based (orchestrator coordinates the steps)
    # Each step is a local transaction; each has a compensating action
    
    # Step 1: Create order (reserve inventory)
    POST /orders {status: PENDING, items: [...]}
      → Event: "OrderCreated" {order_id: 123}
      → Inventory Service reserves stock
    
    # Step 2: Process payment
      → Event: "InventoryReserved" {order_id: 123}
      → Payment Service charges customer
      → Success: "PaymentProcessed" {order_id: 123}
      → Failure: "PaymentFailed" {order_id: 123}
        → Compensate: Inventory Service releases stock
    
    # Step 3: Schedule shipping
      → Event: "PaymentProcessed" {order_id: 123}
      → Shipping Service creates label
      → Success: "OrderFulfilled" {order_id: 123}
      → Failure: "ShippingFailed" {order_id: 123}
        → Compensate: Payment Service refunds
        → Compensate: Inventory Service releases stock
    
    # Key: each compensating action must be idempotent
    # (refunding twice = bad; but idempotent refund = safe to retry)

**Bottom line:** Start with simple event notification (one service emits, others react) before adopting event sourcing or CQRS. For most projects, RabbitMQ or Redis Streams provide enough throughput with simpler operations. Only reach for Kafka when you need replay, long-term retention, or 1M+ msg/s throughput. The biggest mistake is going fully event-driven when simple request-response would suffice — EDA is a powerful tool, not a default architecture. See also: [Microservices vs Monolith](</en/tech/microservices-vs-monolith.html>) and [Webhook Implementation Guide](</en/tech/webhook-implementation-guide.html>).

**See also:** [System Design Fundamentals 2026: A Developer Guide to Scalable Applications](</en/architecture/system-design-fundamentals-2026.html>), [Microservices vs Monolith (2026): Making the Right Architectural Choice](</en/tech/microservices-vs-monolith.html>), [Distributed Transactions: Sagas, Two-Phase Commit, Outbox Pattern, and Idempotency](</en/tech/distributed-transactions-guide.html>)
