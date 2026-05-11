---
title: "Saga Pattern for Distributed Transactions"
description: "Learn the saga pattern for managing distributed transactions across microservices."
date: 2026-05-11
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/saga-pattern.html
---

In a monolithic application, a database transaction guarantees atomicity across multiple operations. In a microservices architecture, where each service has its own database, traditional ACID transactions are no longer possible. The saga pattern provides a way to maintain data consistency across services without distributed transactions.

## What Is a Saga?

A saga is a sequence of local transactions, each within a single service. Each local transaction updates the database and publishes a message or event that triggers the next local transaction. If a local transaction fails, the saga executes compensating transactions to undo the changes made by previous transactions.

There are two common implementations: choreography-based and orchestration-based sagas.

## Choreography-Based Saga

In a choreography-based saga, each service knows what to do next and publishes events after completing its local transaction. There is no central coordinator.

Consider an order placement flow:

1. **Order Service** creates an order in `PENDING` status and publishes `OrderCreated`.
2. **Inventory Service** receives the event, reserves inventory, publishes `InventoryReserved`.
3. **Payment Service** receives the event, processes payment, publishes `PaymentProcessed`.
4. **Order Service** receives the event, updates order status to `CONFIRMED`.

If payment fails, the Payment Service publishes `PaymentFailed`. The Inventory Service listens for this event and releases the reserved inventory. The Order Service updates the order to `FAILED`.

**Pros:** Simple, no single point of failure, services are loosely coupled.
**Cons:** The flow is spread across services, making it harder to trace and debug. Services can become tightly coupled to each other's events. Complex workflows are difficult to manage.

## Orchestration-Based Saga

In an orchestration-based saga, a central orchestrator (the saga coordinator) tells each service what to do. The orchestrator sends commands to services and handles their responses.

Using the same order flow:

1. **Order Saga Orchestrator** tells Order Service to create an order.
2. Order Service creates the order and responds with `success`.
3. Orchestrator tells Inventory Service to reserve inventory.
4. Inventory Service responds with `success`.
5. Orchestrator tells Payment Service to process payment.
6. Payment Service responds with `success`.
7. Orchestrator tells Order Service to confirm the order.

If any step fails, the orchestrator executes compensating actions in reverse order. For example, if payment fails, it tells Inventory Service to release inventory and Order Service to reject the order.

**Pros:** Clear workflow definition in one place, easier to monitor and debug, good for complex workflows with conditional logic.
**Cons:** The orchestrator is a single point of failure and can become a bottleneck.

## Compensating Transactions

Sagas rely on compensating transactions for rollback. Unlike ACID rollbacks, compensations are application-level operations that semantically undo a previous action. For example:

- `InventoryReserved` is compensated by `InventoryReleased`.
- `PaymentProcessed` is compensated by `PaymentRefunded`.
- `EmailSent` might not require compensation at all.

Design compensations to be idempotent. A compensation might be executed multiple times if the orchestrator crashes and retries. A good test: if the compensation runs twice, the system should still end up in the correct state.

## Handling Failures and Retries

Failures in sagas fall into two categories:

**Business failures** (insufficient inventory, invalid payment) trigger compensation flows immediately. These are expected and part of normal operation.

**Technical failures** (timeout, network error) are harder to handle. Best practices include:

- Implementing retry with exponential backoff for transient failures.
- Storing saga state in a database so the saga can resume after a crash.
- Using a saga log to track which steps have completed.

## When to Use Sagas

Use sagas when:
- You need to maintain data consistency across multiple services.
- Each service has its own database (database per service pattern).
- You accept eventual consistency -- sagas are not ACID. There is a window of inconsistency between steps.

Do not use sagas when you need strong ACID guarantees across services. In those cases, reconsider your service boundaries or accept that some operations might need to be in the same service.

## Practical Implementation

Start with choreography for simple flows with 2-3 services. Switch to orchestration when the flow becomes complex or you need visibility into saga state. Use a dedicated saga orchestration framework like Axon, Temporal, or Camunda for production systems. Always implement idempotency and retry logic. Log every saga step for debugging and monitoring.

## Summary

The saga pattern is the de facto standard for distributed transactions in microservices. Choose choreography for simple flows and orchestration for complex ones. Design compensating transactions carefully, handle both business and technical failures, and accept that sagas provide eventual consistency, not ACID guarantees.
