---
title: "Clean Architecture Explained"
description: "Understand Clean Architecture principles for building maintainable, testable software systems."
date: 2026-05-11
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/clean-architecture.html
---

Clean Architecture, popularized by Robert C. Martin (Uncle Bob), is a software design philosophy that emphasizes separation of concerns through concentric layers. Building on concepts from hexagonal architecture, onion architecture, and DCI, it provides a set of rules for organizing code that stands the test of time.

## The Layers

Clean Architecture is typically drawn as a set of concentric circles:

1. **Enterprise Business Rules** (innermost)
2. **Application Business Rules**
3. **Interface Adapters**
4. **Frameworks and Drivers** (outermost)

## The Dependency Rule

The single most important rule: **source code dependencies can only point inward**. Nothing in an inner circle can know about anything in an outer circle. This means:

- The domain layer has no dependencies on frameworks, databases, or UI.
- The application layer depends only on the domain layer.
- The infrastructure layer depends on both inner layers but implements their interfaces.

This is enforced programmatically through dependency injection. The outer layers provide implementations that are injected into inner layers through interfaces.

## Entities (Enterprise Business Rules)

Entities are the innermost layer. They represent enterprise-wide business concepts:

```java
public class Order {
    private String id;
    private List<OrderLineItem> items;
    private OrderStatus status;

    public void addItem(Product product, int quantity) {
        // Business rule: validate quantity limits
        items.add(new OrderLineItem(product, quantity));
    }

    public Money calculateTotal() {
        return items.stream()
            .map(OrderLineItem::getSubtotal)
            .reduce(Money::add)
            .orElse(Money.zero());
    }
}
```

Entities should be pure business objects with no reference to databases, frameworks, or external systems. They encapsulate the most general and high-level business rules.

## Use Cases (Application Business Rules)

The use case layer contains application-specific business rules. It orchestrates the flow of data to and from the entities:

```java
public class CreateOrderUseCase {
    private final OrderRepository repository;
    private final PaymentGateway paymentGateway;
    private final NotificationService notificationService;

    public Order execute(CreateOrderRequest request) {
        Order order = new Order(request.getCustomerId());
        request.getItems().forEach(item ->
            order.addItem(item.getProduct(), item.getQuantity())
        );
        repository.save(order);
        paymentGateway.charge(order.getTotal());
        notificationService.sendOrderConfirmation(order);
        return order;
    }
}
```

Use cases are specific to the application. A web shop and a mobile app might share the same entities but have different use cases.

## Interface Adapters

This layer converts data between the format most convenient for the use cases and entities, and the format most convenient for external agencies like databases and web servers:

- **Controllers** convert HTTP requests into use case inputs.
- **Presenters** convert use case outputs into HTTP responses or view models.
- **Repository implementations** convert between entity objects and database records.

This is where you find DTOs, request/response objects, ORM mappings, and serialization logic. This layer depends on both inner circles and outer frameworks.

## Frameworks and Drivers

The outermost layer consists of frameworks and tools: the database, web framework, UI toolkit, message queue, etc. This layer is kept at the perimeter. You should treat frameworks as tools to be used, not architectures to be conformed to.

A corollary: delay framework decisions. Write your use cases and entities first, then plug in the web framework and database later. This is possible because these outer layers implement interfaces defined by inner layers.

## Crossing Layer Boundaries

When data crosses a layer boundary, it typically takes the form of a simple data structure. Use case request and response objects are passed across boundaries. Inner layers should not leak implementation details like database cursors or HTTP session objects.

## Benefits

**Framework Independence.** The architecture does not depend on any particular framework. You can swap Spring for Quarkus, or Express for Fastify, without touching business logic.

**Testability.** Business rules can be tested without a database, web server, or any external dependency. Tests run fast and are highly reliable.

**UI Independence.** The UI can change without affecting the rest of the system. You can replace a web UI with a CLI or REST API without modifying use cases or entities.

**Database Independence.** You can swap out databases by implementing repository interfaces differently. The business rules do not know which database is in use.

## Common Pitfalls

**Pragmatic shortcuts are okay.** Strict adherence to Clean Architecture can feel verbose for small applications. Start with a simplified version and add layers as complexity grows.

**Don't create unnecessary abstractions.** If an interface has exactly one implementation and you don't foresee a second one, wait before extracting it. Clean Architecture does not require interfaces for everything, just the boundaries that matter.

**Packages vs. layers.** Physical separation (separate modules or packages) is more important than naming conventions. Enforce the dependency rule at the build level to prevent accidental violations.

## Summary

Clean Architecture is about protecting your business logic from the frameworks and infrastructure around it. The dependency rule ensures that inner layers remain pure and testable. While the pattern requires discipline and forethought, it pays significant dividends as the application grows and evolves over time.
