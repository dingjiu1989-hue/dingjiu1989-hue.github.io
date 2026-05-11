---
title: "Database per Service Pattern"
description: "Learn the database per service pattern for microservices data management."
date: 2026-05-11
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/database-per-service.html
---

The database per service pattern is a fundamental principle of microservices architecture. Each service owns its data and exposes it only through its API. No other service can access a service's database directly. This article explores the pattern, its benefits, challenges, and practical implementation strategies.

## The Core Principle

In a monolithic application, a single database serves all modules. This creates tight coupling between modules -- changing one module's schema can break another module's queries. The database becomes a bottleneck and a single point of failure.

With database per service:

```
[Order Service]    -> [Order DB]     (private)
[Payment Service]  -> [Payment DB]   (private)
[Inventory Service]-> [Inventory DB] (private)
```

Each service has complete ownership of its database. Other services can only interact with the data through the service's API. This ensures:
- **Encapsulation**: Service internals are hidden.
- **Independent evolution**: Services can change their database schema without coordinating with other teams.
- **Independent scaling**: Each service can choose the database technology that best fits its needs.

## Benefits

**Decentralized data management.** Each team chooses the best database for their service's needs. The order service might use PostgreSQL for ACID compliance. The analytics service might use a columnar store or data warehouse. The product catalog might use Elasticsearch for full-text search.

**Independent scalability.** Services with high data volume can scale independently. The order database can be scaled up without affecting the payment database.

**Fault isolation.** A failure in one service's database does not affect other services. If the inventory database goes down, the order service can still handle requests using cached or default inventory data.

**Team autonomy.** Service teams can change their schema, migrate databases, or switch technologies without coordinating with other teams. This speed is a primary goal of microservices.

**Polyglot persistence.** Different data storage technologies excel at different tasks. SQL, NoSQL, key-value stores, graph databases, and time-series databases each have strengths. The database per service pattern lets you choose the right tool for each job.

## Challenges

### Data Consistency Across Services

In a monolith, a single ACID transaction can update multiple tables atomically. In a microservices architecture with separate databases, cross-service transactions are not possible.

**Solution:** Use the saga pattern. A saga is a sequence of local transactions, each within a single service. If a step fails, compensating transactions undo prior steps. Sagas provide eventual consistency without distributed transactions.

### Queries Across Services

A query like "find all orders containing a product that is currently on sale" spans the order service and the product service. With separate databases, a simple JOIN is impossible.

**Solutions:**
- **API composition**: The calling service queries each service individually and combines results in memory. Simple but can be slow for complex queries.
- **CQRS**: Maintain a read-optimized view that aggregates data from multiple services. Updates are asynchronous. This is the recommended approach for complex queries.
- **Event-driven data synchronization**: Services publish events when their data changes. Other services consume these events and update their own copies of the data.

### Data Duplication

Multiple services might need the same data. The order service needs customer names. The shipping service needs customer addresses. Different pieces of customer data are owned by different services.

**Solution:** Each piece of data has a single source of truth (the service that owns it). Other services store cached or derived copies. Event-driven updates keep copies synchronized. Accept that some data duplication is normal and intentional in distributed systems.

## Polyglot Persistence in Practice

Choosing the right database for each service:

- **Order Service**: PostgreSQL or MySQL for ACID transactions and relational data.
- **Product Catalog**: Elasticsearch for full-text search and faceted filtering.
- **Shopping Cart**: Redis for fast, temporary key-value storage.
- **User Session**: DynamoDB or Cassandra for high-velocity, low-latency access.
- **Analytics**: ClickHouse or BigQuery for columnar storage and aggregation queries.
- **Graph**: Neo4j for relationship-heavy data like recommendations.

The cost of polyglot persistence is operational complexity. Each database type has different management, monitoring, and backup requirements. Evaluate whether the benefits justify the additional operational burden.

## Eventual Consistency and Compensations

Embrace eventual consistency between services. When a user places an order:

1. Order service creates the order (immediate).
2. Order service publishes `OrderCreated` event.
3. Inventory service consumes the event and reserves inventory (may take milliseconds).
4. Payment service consumes the event and processes payment (may take seconds).

Between steps 1 and 4, the order is in a "pending" state. This window of inconsistency is normal. The user sees "Order placed, processing payment" rather than an immediate confirmation.

Design your compensation logic carefully. If payment fails:
- Cancel the reservation (inventory compensation).
- Notify the user.
- Mark the order as failed.

## Transactional Boundaries

Define clear transactional boundaries for each service. A service should encapsulate data that changes together. If two pieces of data are always read and written together, they might belong in the same service.

A common mistake is splitting data too finely. If every order operation needs to query customer data, the order and customer services are tightly coupled by data dependencies. In such cases, reconsider the service boundaries.

## Migration Strategy

Migrating from a shared database to database per service:

1. **Identify bounded contexts** based on domain-driven design.
2. **Extract one service at a time**. Do not attempt a big bang migration.
3. **Use database views or triggers** as temporary bridges during migration.
4. **Implement event-driven synchronization** to keep data in sync during the transition.
5. **Cut over traffic** service by service.

## Summary

The database per service pattern is essential for microservices that need independent scalability, team autonomy, and polyglot persistence. Embrace eventual consistency across services and use the saga pattern for multi-service operations. Accept data duplication as a normal part of distributed systems. Choose database technologies based on each service's specific requirements, but be mindful of the operational complexity that comes with multiple database systems.
