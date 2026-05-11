---
title: "Microservices vs Monolith: Decision Guide"
description: "Guide to choosing between microservices and monoliths, including when to start with a monolith, Conway's Law, module boundaries, and testing."
date: 2026-05-12
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/microservices-vs-monolith.html
---

The debate between microservices and monoliths is one of the most persistent in software architecture. The answer is not "always use microservices" or "never use microservices." The right choice depends on your team size, organizational structure, product maturity, and specific technical requirements. This article provides a framework for making this decision.

## The Spectrum of Architectures

Architecture exists on a spectrum, not a binary choice:

```
Monolith                  Modular Monolith             Microservices
   |                            |                            |
   | Single deployable         | Single deployable          | Multiple deployable
   | Shared database           | Shared database            | Database per service
   | Tight coupling            | Well-defined modules       | Network communication
   | Simple deployment         | Simple deployment          | Complex deployment
```

A monolith can be well-structured internally. Microservices can become a distributed monolith if boundaries are wrong. The Modular Monolith is an often-overlooked middle ground.

## When to Start with a Monolith

Most successful microservice architectures started as monoliths and were extracted later. Starting with microservices is usually premature.

### Reasons to Start Monolithic

1. **Unknown domain boundaries**: In a new product, you do not yet know where the natural service boundaries are. Premature microservices force arbitrary boundaries that need rework later.

2. **Team size**: A small team (under 10 people) cannot justify the overhead of multiple services. The cost of deploying, monitoring, and debugging distributed systems outweighs the benefits.

3. **Rapid iteration**: Early-stage products need fast feature development. Microservices add coordination overhead that slows iteration.

4. **Strong consistency requirements**: If your application requires transactional guarantees across aggregates, a monolith with a single database is simpler and more reliable.

5. **No independent scaling needs**: If all features have similar scaling requirements, there is no benefit to independent scaling.

### Starting Monolithic but Thinking Modular

Start with a monolith, but organize code into well-defined modules with clear interfaces:

```python
# Modular monolith structure
myapp/
  modules/
    billing/
      interfaces/
        PaymentProcessor.py
        InvoiceService.py
      internal/
        PaymentGateway.py
        InvoiceGenerator.py
      models/
        Payment.py
        Invoice.py
    orders/
      interfaces/
        OrderService.py
        OrderRepository.py
      internal/
        Fulfillment.py
        ShipmentTracker.py
      models/
        Order.py
        OrderItem.py
    notifications/
      interfaces/
        NotificationService.py
      internal/
        EmailSender.py
        SMSSender.py
      models/
        Notification.py
```

Each module communicates through well-defined interfaces. Modules should only call each other's interfaces, not internal classes. This makes extraction into separate services easier when the time comes.

## Conway's Law

Conway's Law states that organizations design systems that mirror their communication structures. If your team is organized to build a monolith, trying to build microservices creates friction. Conversely, if your teams are organized by business capability, microservices align naturally.

```
Organization Structure:
  Team A (Billing) | Team B (Orders) | Team C (Notifications)
  
Resulting Architecture:
  [Billing Service] <-> [Orders Service] <-> [Notifications Service]
```

### Applying Conway's Law

- **Two-pizza teams**: If you have two or more autonomous teams, each owning a business capability, microservices may be appropriate.
- **Single team**: One team should not deploy multiple services unless they have a clear reason to do so.
- **Cross-cutting teams**: Teams organized by technology (frontend, backend, database) produce layered monoliths, not microservices.

## Module Boundaries

Whether you choose monolith or microservices, getting module boundaries right is critical.

### Finding Good Boundaries

Good module boundaries follow the principle of high cohesion and low coupling.

**High cohesion**: Related functionality lives together. An order module contains order creation, order validation, order status tracking, and order history.

**Low coupling**: Modules depend on each other minimally. The billing module depends on the order module's balance check interface but does not need to know about order item details.

### Bounded Contexts

Use Domain-Driven Design bounded contexts to identify boundaries:

```python
# Bounded Context: Ordering
class OrderContext:
    def submit_order(self, items):
        # Validates inventory, calculates tax, applies discounts
        pass

# Bounded Context: Inventory
class InventoryContext:
    def check_availability(self, product_ids):
        # Checks warehouse stock
        pass
    def reserve_inventory(self, product_ids):
        # Reserves items for a pending order
        pass
```

The Ordering context references Inventory through its public interface. Each context owns its data and logic.

### Signs of Wrong Boundaries

- **Chatty communication**: Services or modules that call each other hundreds of times per operation.
- **Shared database tables**: Services that read each other's database tables instead of going through APIs.
- **Feature envy**: One module keeps requesting data from another to make decisions.
- **Distributed transactions**: A single user operation requires transactions across three services.

## Integration Testing Strategies

### Monolith Testing

Testing a monolith is straightforward. You run the entire application in a test environment and test end-to-end.

```python
# Monolith integration test
def test_order_workflow():
    # Set up
    app = create_test_app()
    customer = app.create_customer("alice@example.com")
    
    # Execute user workflow
    order_id = app.place_order(customer.id, [{"product_id": 100, "qty": 2}])
    
    # Verify
    order = app.get_order(order_id)
    assert order.status == "confirmed"
    assert order.total == 39.98
    
    # Check side effects
    notification = app.get_notifications(customer.id)[0]
    assert "order confirmed" in notification.message
```

### Microservices Testing

Microservices require a different approach. Each service tests in isolation with mocked dependencies. Integration tests verify the real interactions.

```python
# Microservice contract test (Pact framework style)
{
  "provider": {
    "name": "OrderService"
  },
  "consumer": {
    "name": "BillingService"
  },
  "interactions": [
    {
      "description": "request order totals",
      "request": {
        "method": "GET",
        "path": "/api/orders/customer/42/totals",
        "query": {"from": "2026-01-01", "to": "2026-03-31"}
      },
      "response": {
        "status": 200,
        "headers": {"Content-Type": "application/json"},
        "body": {
          "customer_id": 42,
          "total_spent": 1299.50,
          "order_count": 15
        }
      }
    }
  ]
}
```

```python
# Consumer-driven contract test
import pact

@pytest.fixture
def order_service_mock():
    # Mock OrderService for BillingService tests
    with pact.Consumer('BillingService').has_pact_with('OrderService') as pact:
        pact.given('customer has orders').upon_receiving(
            'request order totals'
        ).with_request('GET', '/api/orders/customer/42/totals',
                       query={'from': '2026-01-01', 'to': '2026-03-31'}
        ).will_respond_with(200, body={
            'customer_id': 42,
            'total_spent': 1299.50
        })
        yield pact

def test_customer_balance_calculation(order_service_mock):
    with order_service_mock:
        billing = BillingService()
        balance = billing.calculate_balance(42)
        assert balance == 1299.50 + 50.00  # spent + monthly fee
```

## Migration Strategy

If you have a monolith and want to migrate to microservices:

1. **Identify bounded contexts**: Use DDD workshop to find natural boundaries.
2. **Extract the simplest service first**: Start with a well-understood, low-coupling domain like notifications.
3. **Use the strangler fig pattern**: Route new functionality to the new service. Route existing functionality to the monolith. Gradually expand the new service's scope.
4. **Implement anti-corruption layers**: Translate between the new service's domain model and the monolith's legacy model.
5. **Do not share databases**: Each service gets its own database. Data synchronization happens via events or APIs.

## Decision Matrix

| Factor | Monolith | Modular Monolith | Microservices |
|--------|----------|------------------|---------------|
| Team size | 1-10 | 5-15 | 10+ per service |
| Product stage | Early | Growth | Mature |
| Domain clarity | Low | Medium | High |
| Scalability needs | Low | Medium | High |
| Consistency needs | High | Medium | Low |
| Deployment frequency | Weekly | Daily | Multiple times/day |
| Operational maturity | Low | Medium | High |

## Conclusion

Start with a monolith. Organize it modularly with well-defined interfaces and bounded contexts. Extract microservices only when a specific boundary has demonstrated independent scaling needs, different failure requirements, or team ownership boundaries. The modular monolith is the right choice for most teams. Microservices are an optimization for specific organizational and technical constraints, not a default architecture.
