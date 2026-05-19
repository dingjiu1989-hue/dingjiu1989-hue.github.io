---
title: "Event-Driven Architecture"
description: "Explore event-driven architecture: event bus, event schema management, versioning, and production patterns"
date: 2026-05-03
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/event-driven-arch.html
---

# Event-Driven Architecture

Event-driven architecture (EDA) is an architectural style in which services communicate through the production, detection, and consumption of events. Unlike request-driven architectures where a service explicitly calls another, EDA enables services to react to state changes throughout the system. This decoupling provides scalability, flexibility, and resilience that are difficult to achieve with synchronous communication. 

Core Concepts 

An event is a record of something that happened in the system: "Order Placed", "Payment Received", "Inventory Updated". Events are immutable facts—they describe what occurred, not what to do. Services produce events when their state changes, and other services consume events they are interested in. 

The event bus (or event broker) is the infrastructure that transports events from producers to consumers. Kafka, EventBridge, RabbitMQ, and Pulsar are common event bus implementations. The event bus provides durability, ordering guarantees, and delivery semantics that determine how events travel from producers to consumers. 

Event Schema 

Every event has a schema that defines its structure: the event type, version, timestamp, producer identity, and payload fields. Event schemas must evolve over time as business requirements change. Schema management is critical because producers and consumers may be on different versions. 

A schema registry centralizes schema storage and enforces compatibility rules. When a producer publishes an event, the registry validates the schema against the registered version. Consumers can discover available schemas and understand the event structure. Schema registries support Avro, Protobuf, and JSON Schema, each with different compatibility modes. 

Event Versioning 

Events are long-lived data. An event published today may be consumed by a service deployed months later. Event versioning strategies ensure that old events remain interpretable. 

Backward compatibility ensures that newer consumers can read events produced with older schemas. Forward compatibility ensures that older consumers can read events produced with newer schemas. Full compatibility requires both. The schema registry's compatibility mode determines which changes are allowed. 

Common versioning practices include adding new fields as optional, never removing fields, using default values for new fields, and creating new event types for fundamentally different schemas. Upcasting transforms old event versions to the current version during consumption. 

Event Processing Patterns 

Events can be processed in several ways: stream processing processes each event individually, complex event processing identifies patterns across multiple events, and event sourcing uses events as the primary data store. 

Stream processing frameworks like Kafka Streams, Apache Flink, and Spark Streaming process events in real-time. They support stateful operations like aggregations, joins, and windowed computations. These frameworks are used for real-time analytics, monitoring, and automated reactions. 

Complex event processing detects patterns across multiple events: "If a customer places three orders in one hour and then requests a refund, flag for review." CEP engines like Esper and Flink CEP evaluate event patterns against temporal and logical conditions. 

Challenges 

Event-driven architecture introduces challenges. Eventual consistency means that services may have slightly outdated views of the system state. Monitoring becomes more complex because there is no single request to trace—events flow asynchronously across services. Schema evolution requires coordination even with schema registries. 

Event ordering across partitions is not guaranteed without careful design. Event duplication is possible with at-least-once delivery. Idempotent event handlers are essential to handle duplicates safely. 

When to Use EDA 

Event-driven architecture excels in systems with many loosely coupled services, complex workflows spanning multiple services, real-time processing requirements, and polyglot persistence. It is less suitable for simple CRUD applications, systems requiring strict consistency guarantees, or scenarios where request-response semantics are natural. 

The decision to adopt EDA should be driven by concrete requirements for decoupling, scalability, or real-time processing. For many systems, a hybrid approach—using events for specific workflows while keeping request-response for others—provides the right balance of decoupling and simplicity.

**See also:** [Choreography Patterns](</en/architecture/choreography-patterns.html>), [Polling Consumer vs Event-Driven Consumer](</en/architecture/polling-consumer.html>), [Event Collaboration: Choreography vs Orchestration](</en/architecture/event-collaboration.html>).

**See also:** [Choreography Patterns](</en/architecture/choreography-patterns.html>), [Polling Consumer vs Event-Driven Consumer](</en/architecture/polling-consumer.html>), [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>)

**See also:** [Choreography Patterns](</en/architecture/choreography-patterns.html>), [Polling Consumer vs Event-Driven Consumer](</en/architecture/polling-consumer.html>), [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>)

**See also:** [Choreography Patterns](</en/architecture/choreography-patterns.html>), [Polling Consumer vs Event-Driven Consumer](</en/architecture/polling-consumer.html>), [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>)

**See also:** [Choreography Patterns](</en/architecture/choreography-patterns.html>), [Polling Consumer vs Event-Driven Consumer](</en/architecture/polling-consumer.html>), [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>)

**See also:** [Choreography Patterns](</en/architecture/choreography-patterns.html>), [Polling Consumer vs Event-Driven Consumer](</en/architecture/polling-consumer.html>), [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>)

**See also:** [Health Check Patterns](</en/architecture/health-check-patterns.html>), [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [Saga Choreography Pattern](</en/architecture/saga-choreography.html>)

**See also:** [Health Check Patterns](</en/architecture/health-check-patterns.html>), [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [Saga Choreography Pattern](</en/architecture/saga-choreography.html>)

**See also:** [Health Check Patterns](</en/architecture/health-check-patterns.html>), [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [Saga Choreography Pattern](</en/architecture/saga-choreography.html>)

**See also:** [Health Check Patterns](</en/architecture/health-check-patterns.html>), [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [Saga Choreography Pattern](</en/architecture/saga-choreography.html>)
