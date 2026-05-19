---
title: "Choreography Patterns"
description: "Learn choreography patterns: event contracts, monitoring, saga coordination, and decentralized workflow management"
date: 2026-05-02
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/choreography-patterns.html
---

# Choreography Patterns

Choreography is an architectural pattern for coordinating distributed workflows without a central coordinator. Unlike orchestration, where a central service directs all participants, choreography uses events to achieve coordination—each service performs its task and emits events that trigger the next steps. This decentralized approach offers scalability and loose coupling but introduces challenges in observability and error handling. 

How Choreography Works 

In a choreographed workflow, there is no central controller. Each service knows its role and reacts to relevant events. When a service completes its work, it emits an event that other services consume to trigger their own work. The workflow emerges from the interaction of independent services. 

Consider an order fulfillment flow. The order service places an order and emits "Order Placed". The payment service receives this event, processes payment, and emits "Payment Received". The inventory service receives "Payment Received", reserves inventory, and emits "Inventory Reserved". The shipping service receives this and creates a shipment. Each service acts independently based on events. 

Event Contracts 

Successful choreography depends on clear event contracts. Each event has a defined schema, producer, and set of expected consumers. Event contracts specify the event name, version, payload structure, and delivery guarantees. These contracts must evolve carefully since multiple services depend on them. 

A schema registry is essential for managing event contracts. It stores event schemas, enforces compatibility, and provides a discovery mechanism for consumers. Without explicit contracts, choreography degrades into unpredictable coupling where services make implicit assumptions about event structure. 

Monitoring Choreography 

Monitoring choreographed workflows is challenging because no single component has a complete view of the workflow. Distributed tracing is essential for understanding how a single request flows through multiple services. Each event should carry a correlation ID that ties it to the originating request. 

Workflow dashboards can reconstruct the state of each workflow instance by consuming the event stream. These dashboards show which events have been emitted, how long each step took, and where failures occurred. Dead letter queue monitoring is critical—events that cannot be processed indicate workflow failures. 

Saga Coordination 

Choreography is one of two approaches to implementing the Saga pattern for distributed transactions. In a choreographed saga, each service that completes a local transaction emits an event that triggers the next service's transaction. If a service fails, it emits a failure event that triggers compensation in earlier services. 

For example, in the order flow, if payment fails, the payment service emits "Payment Failed". The order service consumes this event and cancels the order. The inventory service (if it already reserved inventory) consumes the event and releases the reservation. Each service handles its own compensation logic. 

The advantage of choreographed sagas is minimal coupling. Services do not need to know about saga coordinators or other services. The disadvantage is that the saga logic is distributed across services, making it harder to understand, test, and maintain. 

Error Handling 

Without a central coordinator, error handling in choreography requires careful design. Each event handler should be idempotent—processing the same event multiple times should have the same effect. This handles the at-least-once delivery that event brokers typically provide. 

Compensation events reverse the effects of successful operations. If the payment service emits "Payment Failed", the order service's compensation handler cancels the order. Compensation should consider that the original operation may have been completed long ago and the system state may have changed. 

Timeout handling is another challenge. If a service does not emit its expected event within a time window, the workflow may be stuck. A timeout service or dead letter handling can detect and escalate these cases. Some teams implement a monitoring service that checks for stalled workflow instances without taking control of the coordination. 

When to Use Choreography 

Choreography is appropriate when workflows are relatively stable, events are naturally aligned with service boundaries, and the team has good observability infrastructure. It is less suitable for complex workflows with many conditional paths, strict timing requirements, or where end-to-end visibility is critical. 

Many organizations use a hybrid approach: choreography for simple, stable workflows and orchestration for complex, frequently changing ones. The key is matching the coordination pattern to the workflow's complexity and change rate.

**See also:** [Event Collaboration: Choreography vs Orchestration](</en/architecture/event-collaboration.html>), [Saga Choreography Pattern](</en/architecture/saga-choreography.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>).

**See also:** [Saga Choreography Pattern](</en/architecture/saga-choreography.html>), [Event Collaboration: Choreography vs Orchestration](</en/architecture/event-collaboration.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>)

**See also:** [Saga Choreography Pattern](</en/architecture/saga-choreography.html>), [Event Collaboration: Choreography vs Orchestration](</en/architecture/event-collaboration.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>)

**See also:** [Saga Choreography Pattern](</en/architecture/saga-choreography.html>), [Event Collaboration: Choreography vs Orchestration](</en/architecture/event-collaboration.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>)

**See also:** [Saga Choreography Pattern](</en/architecture/saga-choreography.html>), [Event Collaboration: Choreography vs Orchestration](</en/architecture/event-collaboration.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>)

**See also:** [Saga Choreography Pattern](</en/architecture/saga-choreography.html>), [Event Collaboration: Choreography vs Orchestration](</en/architecture/event-collaboration.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>)

**See also:** [Message Queue Patterns](</en/architecture/message-queue-patterns.html>), [Retry Patterns](</en/architecture/retry-patterns.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)

**See also:** [Message Queue Patterns](</en/architecture/message-queue-patterns.html>), [Retry Patterns](</en/architecture/retry-patterns.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)

**See also:** [Message Queue Patterns](</en/architecture/message-queue-patterns.html>), [Retry Patterns](</en/architecture/retry-patterns.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)

**See also:** [Message Queue Patterns](</en/architecture/message-queue-patterns.html>), [Retry Patterns](</en/architecture/retry-patterns.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)
