---
title: "DDD Tactical Patterns"
description: "Master DDD tactical patterns: aggregate, entity, value object, domain service, and repository implementation"
date: 2026-05-02
board: architecture
url: https://aidev.fit/en/architecture/ddd-tactical.html
---

# DDD Tactical Patterns

Domain-Driven Design (DDD) tactical patterns provide concrete building blocks for implementing domain models. While strategic DDD focuses on boundaries and relationships between domains, tactical patterns guide the implementation of individual domain elements. This article explores the core tactical patterns: entities, value objects, aggregates, domain services, repositories, and domain events. 

Entities 

An entity is an object that has a distinct identity that runs through time and across different states. Two entities with the same attributes but different identities are different objects. The identity is typically represented by a unique identifier—a UUID, a database-generated ID, or a business key. 

Entities are mutable and their state changes over time. An `Order` entity changes from "pending" to "shipped" as the business process progresses. The entity is responsible for maintaining its own invariants—an `Order` should not allow shipping before payment is confirmed. 

Implementing entities requires careful identity management. The identity should be assigned when the entity is created and should never change. Entity equality should be based on identity, not on attribute values. 

Value Objects 

A value object is an immutable object whose equality is based on the values of its attributes rather than on identity. A `Money` object with amount 100 and currency USD is equal to another `Money` object with the same values. Value objects have no identity and should be treated as immutable. 

Value objects are powerful modeling tools. They encapsulate domain concepts with their own behavior. An `EmailAddress` value object can validate format, normalize casing, and provide comparison logic. A `DateRange` value object can check overlap, compute duration, and enforce that start is before end. 

The preference in DDD is to use value objects over entities whenever possible. They are easier to reason about, thread-safe by nature, and reduce complexity. 

Aggregates 

An aggregate is a cluster of domain objects that can be treated as a single unit. An aggregate has a root entity, the aggregate root, which is the only object external clients can reference directly. The aggregate root enforces invariants for all objects within the aggregate boundary. 

For example, an `Order` aggregate might contain `OrderItem` entities and `ShippingAddress`, `Money` value objects. External code only holds references to the `Order` aggregate root. To modify an order item, you go through the `Order`. This ensures that business rules like "order total must match sum of line items" are always enforced. 

Aggregate design is critical for consistency. The general rule is to keep aggregates small—only include objects that must be consistent together. Large aggregates cause performance problems and contention issues. 

Domain Services 

A domain service is a stateless object that implements business logic that does not naturally fit within an entity or value object. Domain services are named after the business activity they perform. 

For example, a `TransferService` handles the logic of transferring money between two accounts—a concept that does not belong to either account entity. Domain services operate on domain objects and their behavior is part of the ubiquitous language. 

Repositories 

A repository provides a collection-like interface for accessing aggregates from persistent storage. Each aggregate root typically has its own repository. The repository mediates between the domain model and the data mapping layer, providing the illusion of an in-memory collection. 

Repositories should be defined as interfaces in the domain layer and implemented in the infrastructure layer. This follows the dependency inversion principle and keeps the domain model independent of persistence technology. 

Tactical patterns provide a shared vocabulary for implementation. When a team uses terms like "aggregate root" or "value object", they have precise, agreed-upon meanings. This shared understanding reduces communication overhead and leads to more consistent implementations.

**See also:** [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>), [DDD Strategic Design](</en/architecture/ddd-strategic.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>).

**See also:** [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>), [DDD Strategic Design](</en/architecture/ddd-strategic.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>)

**See also:** [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>), [DDD Strategic Design](</en/architecture/ddd-strategic.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>)

**See also:** [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>), [DDD Strategic Design](</en/architecture/ddd-strategic.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>)

**See also:** [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>), [DDD Strategic Design](</en/architecture/ddd-strategic.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>)

**See also:** [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>), [DDD Strategic Design](</en/architecture/ddd-strategic.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>)

**See also:** [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>), [Stateful vs Stateless Architecture Patterns](</en/architecture/stateful-vs-stateless.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>), [Stateful vs Stateless Architecture Patterns](</en/architecture/stateful-vs-stateless.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>), [Stateful vs Stateless Architecture Patterns](</en/architecture/stateful-vs-stateless.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>), [Stateful vs Stateless Architecture Patterns](</en/architecture/stateful-vs-stateless.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>), [Stateful vs Stateless Architecture Patterns](</en/architecture/stateful-vs-stateless.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>), [Stateful vs Stateless Architecture Patterns](</en/architecture/stateful-vs-stateless.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>), [Stateful vs Stateless Architecture Patterns](</en/architecture/stateful-vs-stateless.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>), [Stateful vs Stateless Architecture Patterns](</en/architecture/stateful-vs-stateless.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>), [Stateful vs Stateless Architecture Patterns](</en/architecture/stateful-vs-stateless.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>), [Stateful vs Stateless Architecture Patterns](</en/architecture/stateful-vs-stateless.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>), [Stateful vs Stateless Architecture Patterns](</en/architecture/stateful-vs-stateless.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>), [Stateful vs Stateless Architecture Patterns](</en/architecture/stateful-vs-stateless.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>), [Stateful vs Stateless Architecture Patterns](</en/architecture/stateful-vs-stateless.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>), [Stateful vs Stateless Architecture Patterns](</en/architecture/stateful-vs-stateless.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>), [Stateful vs Stateless Architecture Patterns](</en/architecture/stateful-vs-stateless.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>), [Stateful vs Stateless Architecture Patterns](</en/architecture/stateful-vs-stateless.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>), [Stateful vs Stateless Architecture Patterns](</en/architecture/stateful-vs-stateless.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)

**See also:** [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>), [Stateful vs Stateless Architecture Patterns](</en/architecture/stateful-vs-stateless.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>)
