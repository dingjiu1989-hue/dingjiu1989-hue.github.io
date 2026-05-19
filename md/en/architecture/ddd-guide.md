---
title: "Domain-Driven Design Fundamentals"
description: "A practical guide to Domain-Driven Design concepts and implementation strategies."
date: 2025-12-26
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/ddd-guide.html
---

# Domain-Driven Design Fundamentals

## Domain-Driven Design Fundamentals

### Domain-Driven Design Fundamentals

#### Domain-Driven Design Fundamentals

#### Domain-Driven Design Fundamentals

#### Domain-Driven Design Fundamentals

#### Domain-Driven Design Fundamentals

#### Domain-Driven Design Fundamentals

#### Domain-Driven Design Fundamentals

#### Domain-Driven Design Fundamentals

#### Domain-Driven Design Fundamentals

#### Domain-Driven Design Fundamentals

#### Domain-Driven Design Fundamentals

#### Domain-Driven Design Fundamentals

#### Domain-Driven Design Fundamentals

#### Domain-Driven Design Fundamentals

Domain-Driven Design (DDD) is a software development approach introduced by Eric Evans in his seminal 2003 book. It emphasizes building software that reflects a deep understanding of the business domain, using a shared language between developers and domain experts. This article covers the fundamental concepts of DDD and how to apply them in practice. 

Ubiquitous Language 

The cornerstone of DDD is the ubiquitous language -- a common vocabulary shared by developers, domain experts, product managers, and other stakeholders. This language is used in code, documentation, conversations, and specifications. 

If the business calls it "Order Cancellation," then your code should have a `OrderCancellation` class, not `DeleteOrderRequest`. The ubiquitous language eliminates translation layers between business concepts and technical implementation. 

To build a ubiquitous language:

  * Listen to how domain experts describe their work.

  * Use those same terms in your code.

  * When a term causes confusion, refine it together with the domain experts.

  * Keep a glossary of terms and their definitions.




Bounded Contexts 

A bounded context is a boundary within which a particular domain model applies. Different contexts may use the same term to mean different things. 

In an e-commerce system:

  * The **Sales** context has a `Product` with pricing and availability.

  * The **Shipping** context has a `Product` with weight and dimensions.

  * The **Inventory** context has a `Product` with stock levels and warehouse locations.




Each bounded context has its own domain model, its own database, and potentially its own team. The boundaries are explicit, and communication between contexts happens through well-defined integration points. 

Identifying bounded contexts is one of the hardest parts of DDD. Look for:

  * Different teams responsible for different parts of the system.

  * Different lifecycle or persistence requirements.

  * Different ubiquitous language terms.




Entities and Value Objects 

**Entities** are objects with a distinct identity that persists over time. Two entities with the same attributes are still different if they have different identities. A `User` is an entity because user 123 is different from user 456. 

public class User {

private UserId id; // Identity matters

private String name;

private Email email;

}

**Value Objects** are objects defined by their attributes. Two value objects with the same attributes are interchangeable. An `Address` is a value object because two identical addresses are the same address. 

public class Address {

private String street;

private String city;

private String zipCode;

// No identity field -- equality is based on all attributes

}

Value objects should be immutable. Prefer value objects over primitives. A `Email` value object is better than a `String` because it encapsulates validation, formatting, and behavior. 

Aggregates 

An aggregate is a cluster of domain objects treated as a single unit. Each aggregate has a root entity (the aggregate root) that is the only entry point for external access. 

Consider an `Order` aggregate:

  * Aggregate root: `Order`

  * Contained entities: `OrderLineItem`, `ShippingAddress`

  * Contained value objects: `Money`, `OrderStatus`




External objects can only reference the aggregate root. All operations on the aggregate go through the root, which enforces invariants: 

public class Order {

private List items;

public void addItem(Product product, int quantity) {

if (items.size() >= MAX_ITEMS) {

throw new DomainException("Order cannot have more than " + MAX_ITEMS + " items");

}

items.add(new OrderLineItem(product, quantity));

}

}

Domain Events 

Domain events capture something important that happened in the domain. They are named in the past tense and represent facts: 

public class OrderPlacedEvent {

private OrderId orderId;

private CustomerId customerId;

private Money total;

private Instant occurredAt;

}

Domain events are published from aggregates when something significant occurs. Other parts of the system react to these events, potentially in different bounded contexts. 

Repositories and Services 

**Repositories** provide a collection-like interface for retrieving and storing aggregates. Each aggregate root typically has a repository: 

public interface OrderRepository {

Order findById(OrderId id);

void save(Order order);

void delete(OrderId id);

}

**Domain services** hold domain logic that does not naturally fit within an entity or value object. They operate on multiple aggregates or coordinate complex business rules. Domain services are named after business activities: `PricingService`, `FraudDetectionService`. 

Strategic Design 

Beyond tactical patterns, DDD includes strategic design tools: 

  * **Context Mapping** : Documenting relationships between bounded contexts (partnership, customer-supplier, conformist, etc.).

  * **Core Domain** : Identifying which part of the system provides competitive advantage and investing most effort there.

  * **Generic Subdomains** : Using off-the-shelf solutions for non-core functionality (authentication, payments).

  * **Supporting Subdomains** : Building custom but straightforward solutions for areas that support the core domain.




Getting Started with DDD 

Start small. Pick one bounded context and implement it using DDD tactical patterns (entities, value objects, aggregates, repositories). Work closely with domain experts to develop the ubiquitous language. Use event storming workshops to discover domain events and aggregates. 

Avoid over-engineering. Not every class needs to be a domain entity, not every concept needs an aggregate. DDD is a tool for managing complexity, not for adding it. 

Summary 

DDD provides a powerful toolkit for building software that deeply models the business domain. Use bounded contexts to manage complexity, entities and value objects to model domain concepts, and aggregates to enforce invariants. The ubiquitous language bridges the gap between business and technology, creating software that is easier to understand, maintain, and evolve.

**See also:** [System Design Fundamentals 2026: A Developer Guide to Scalable Applications](</en/architecture/system-design-fundamentals-2026.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>).

**See also:** [System Design Fundamentals 2026: A Developer Guide to Scalable Applications](</en/architecture/system-design-fundamentals-2026.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>)

**See also:** [System Design Fundamentals 2026: A Developer Guide to Scalable Applications](</en/architecture/system-design-fundamentals-2026.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>)

**See also:** [System Design Fundamentals 2026: A Developer Guide to Scalable Applications](</en/architecture/system-design-fundamentals-2026.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>)

**See also:** [System Design Fundamentals 2026: A Developer Guide to Scalable Applications](</en/architecture/system-design-fundamentals-2026.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>)

**See also:** [System Design Fundamentals 2026: A Developer Guide to Scalable Applications](</en/architecture/system-design-fundamentals-2026.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>)
