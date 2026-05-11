---
title: "Hexagonal Architecture (Ports and Adapters)"
description: "Learn hexagonal architecture for building maintainable, testable applications."
date: 2026-05-11
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/hexagonal-architecture.html
---

Hexagonal architecture, also known as ports and adapters, is a software design pattern introduced by Alistair Cockburn in 2005. It creates a separation between the core business logic and the external systems it interacts with, making applications more maintainable, testable, and adaptable to change.

## The Core Idea

The pattern gets its name from the hexagonal shape used in diagrams, though the number of sides has no particular significance. The key insight is that the application core should not depend on the details of external systems -- databases, web frameworks, message queues, or user interfaces.

The architecture has three layers:

1. **Core (Domain)**: The pure business logic with no external dependencies.
2. **Ports**: Interfaces that define how the core interacts with the outside world.
3. **Adapters**: Implementations of those interfaces that connect to specific technologies.

## Ports: The Contracts

Ports are interfaces defined within the domain layer. There are two types:

**Inbound ports** (driving ports) define how the outside world can interact with the application. These are typically use-case interfaces:

```java
public interface OrderService {
    Order createOrder(CreateOrderRequest request);
    Order getOrder(String orderId);
    void cancelOrder(String orderId);
}
```

**Outbound ports** (driven ports) define how the application accesses external systems:

```java
public interface OrderRepository {
    void save(Order order);
    Order findById(String orderId);
    List<Order> findByCustomerId(String customerId);
}
```

## Adapters: The Implementations

Adapters implement the port interfaces and handle the details of communicating with specific technologies.

**Inbound adapters** handle incoming requests. A REST controller is an inbound adapter:

```java
@RestController
public class OrderController {
    private final OrderService orderService;

    @PostMapping("/orders")
    public ResponseEntity<OrderResponse> createOrder(@RequestBody CreateOrderRequest request) {
        Order order = orderService.createOrder(request);
        return ResponseEntity.status(201).map(OrderResponse::from);
    }
}
```

**Outbound adapters** handle outgoing calls. A JPA repository implementation is an outbound adapter:

```java
public class JpaOrderRepository implements OrderRepository {
    private final SpringDataJpaOrderRepository repo;

    @Override
    public void save(Order order) {
        repo.save(OrderEntity.from(order));
    }
}
```

## Dependency Rule

The critical rule: **dependencies point inward**. The domain core knows nothing about HTTP, databases, or message queues. The adapters depend on the ports (interfaces), not the other way around. This is achieved through dependency injection at the application's entry point.

```
[External] -> [Inbound Adapter] -> [Port Interface] -> [Domain Core] -> [Port Interface] -> [Outbound Adapter] -> [External]
```

## Benefits

**Testability.** You can test the domain core by mocking adapters at the port boundaries. No database, no HTTP server, no message broker needed. This results in fast, reliable unit tests.

**Technology Independence.** You can swap a SQL database for MongoDB by writing a new adapter. You can change from REST to GraphQL by swapping the inbound adapter. The core business logic remains untouched.

**Isolation of Changes.** When your ORM or web framework releases a breaking change, only the adapter code needs updating. The core business logic is completely isolated.

**Clear Boundaries.** The explicit separation between ports and adapters makes the architecture visible in the code structure. New team members can quickly understand where different concerns live.

## Common Mistakes

**Leaking adapter concerns into the domain.** Your domain objects should not have JPA annotations, JSON serialization attributes, or framework-specific base classes. Use separate data transfer objects and mapping logic in the adapters.

**Over-abstracting.** Not every external dependency needs a port-adapter pair. If you are writing an interface with a single implementation and no foreseeable alternative, you might be over-engineering. The testability argument still holds, but be pragmatic.

**Fat ports.** Keep port interfaces focused. A repository interface with 30 methods suggests the abstraction is too broad or the domain model is not well-defined.

## Summary

Hexagonal architecture is a practical pattern for building maintainable applications. By defining clear boundaries between business logic and infrastructure, you gain testability, technology independence, and protection against external changes. Start by identifying the ports in your domain and implementing adapters for each external system. The investment pays off quickly as the application grows and evolves.
