---
title: "Domain Event Implementation: Publishing, Handling, and Testing"
description: "Implement domain events in DDD: event definitions, publishing patterns, handlers, and testing strategies."
date: 2026-05-07
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/domain-event-implementation.html
---

# Domain Event Implementation: Publishing, Handling, and Testing

Domain events capture significant business occurrences within a domain-driven system. When a domain expert says "when the order is shipped, send an invoice," the "order shipped" is a domain event. Events are named in the past tense: OrderShipped, PaymentReceived, InvoiceGenerated.

## Event Definition

Each event is an immutable object containing the data relevant to the occurrence. Events include a unique identifier, a timestamp, and the business data. Event names come from the ubiquitous language. The structure should be kept stable—consumers depend on it.

## Publishing

Events are published from the domain layer when an aggregate changes state. The aggregate returns events after command execution. The application layer collects and publishes these events to a message bus or event store.

Transactional outbox ensures events are published reliably. The outbox stores events in the same database transaction as the state change. A separate process reads the outbox and publishes events to the message broker.

**See also:** [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [DDD Tactical Patterns](</en/architecture/ddd-tactical.html>), [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>).

**See also:** [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [DDD Tactical Patterns](</en/architecture/ddd-tactical.html>), [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>)

**See also:** [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [DDD Tactical Patterns](</en/architecture/ddd-tactical.html>), [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>)

**See also:** [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [DDD Tactical Patterns](</en/architecture/ddd-tactical.html>), [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>)

**See also:** [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [DDD Tactical Patterns](</en/architecture/ddd-tactical.html>), [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>)

**See also:** [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [DDD Tactical Patterns](</en/architecture/ddd-tactical.html>), [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>)

**See also:** [Event Collaboration: Choreography vs Orchestration](</en/architecture/event-collaboration.html>), [Graceful Shutdown Patterns](</en/architecture/graceful-shutdown.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>)

**See also:** [Event Collaboration: Choreography vs Orchestration](</en/architecture/event-collaboration.html>), [Graceful Shutdown Patterns](</en/architecture/graceful-shutdown.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>)

**See also:** [Event Collaboration: Choreography vs Orchestration](</en/architecture/event-collaboration.html>), [Graceful Shutdown Patterns](</en/architecture/graceful-shutdown.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>)

**See also:** [Event Collaboration: Choreography vs Orchestration](</en/architecture/event-collaboration.html>), [Graceful Shutdown Patterns](</en/architecture/graceful-shutdown.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>)

**See also:** [Event Collaboration: Choreography vs Orchestration](</en/architecture/event-collaboration.html>), [Graceful Shutdown Patterns](</en/architecture/graceful-shutdown.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>)
