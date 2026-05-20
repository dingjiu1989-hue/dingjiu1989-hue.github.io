---
title: "Event Sourcing Pattern"
description: "Learn the event sourcing pattern for capturing state changes as immutable events."
date: 2025-12-26
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/event-sourcing.html
---

# Event Sourcing Pattern

Event sourcing is an architectural pattern that stores the state of a system as a sequence of immutable events rather than as the current state. Instead of updating a database row to reflect a new state, the system appends an event describing what happened. The current state is derived by replaying all events for a given entity. This fundamental shift in data management provides powerful capabilities for audit, debugging, and system evolution. 

The Event Store 

The event store is the centerpiece of an event-sourced system. It is an append-only database that stores events in the order they occurred. Each event represents a fact about the system: "OrderPlaced", "PaymentReceived", "ItemShipped". Events are immutable once written—they cannot be changed or deleted. New events can only be appended. 

Event stores typically provide two key operations: append an event to a stream, and read all events from a stream. Many event stores also support subscription mechanisms that notify consumers when new events are appended. Popular event store implementations include EventStoreDB, Kafka (when used as an event store), and specialized databases like Axon Server. 

Projections and Read Models 

Events alone are not sufficient for efficient querying. To reconstruct the current state or answer queries, the system builds projections. A projection reads events from the event store and produces a read model—a data structure optimized for a specific query pattern. 

For example, an `OrderSummary` projection might listen for `OrderPlaced`, `PaymentReceived`, and `ItemShipped` events and maintain a denormalized table showing order status, amounts, and shipping details. Different projections can produce different read models from the same event stream, enabling diverse query capabilities without impacting the write path. 

Snapshots 

Replaying the entire event stream for an entity with thousands of events is inefficient. Snapshots solve this problem by periodically capturing the state of an entity at a point in time. When the system needs to reconstruct the current state, it loads the most recent snapshot and replays only the events that occurred after it. 

Snapshots are a performance optimization and do not affect the correctness of event sourcing. They can be generated asynchronously and stored alongside the event stream. The snapshot frequency depends on the event volume and the cost of replaying events. A common approach is to take a snapshot every N events or when the event stream exceeds a threshold size. 

Event Versioning 

Events are data structures, and data structures evolve over time. When an event schema changes, older stored events may no longer match the current code. Event versioning strategies address this. Common approaches include using a schema registry (Avro, Protobuf), applying upcasting (transforming old events to the current version during replay), or maintaining backward compatibility through optional fields. 

The principle is that old events must always be readable. Deleting or destructively modifying events violates the immutability guarantee central to event sourcing. Instead, new versions are introduced through new event types or versioned fields, and old events are migrated via upcasting during projection. 

Event sourcing is a powerful pattern that provides unmatched auditability and temporal querying, but it requires careful design of event schemas, projection infrastructure, and operational tooling. When applied appropriately, it creates systems that are remarkably resilient to change.

**See also:** [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>), [CQRS Pattern: Command Query Responsibility Segregation](</en/architecture/cqrs-pattern.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>).

**See also:** [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [Fanout Pattern for Event Distribution](</en/architecture/fanout-pattern.html>)

**See also:** [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [Fanout Pattern for Event Distribution](</en/architecture/fanout-pattern.html>)

**See also:** [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [Fanout Pattern for Event Distribution](</en/architecture/fanout-pattern.html>)

**See also:** [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [Fanout Pattern for Event Distribution](</en/architecture/fanout-pattern.html>)

**See also:** [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [Fanout Pattern for Event Distribution](</en/architecture/fanout-pattern.html>)

**See also:** [Database per Service Pattern](</en/architecture/database-per-service.html>), [Saga Pattern for Distributed Transactions](</en/architecture/saga-pattern.html>), [Strangler Fig Pattern for Legacy Migration](</en/architecture/strangler-fig.html>)

**See also:** [Database per Service Pattern](</en/architecture/database-per-service.html>), [Saga Pattern for Distributed Transactions](</en/architecture/saga-pattern.html>), [Strangler Fig Pattern for Legacy Migration](</en/architecture/strangler-fig.html>)

**See also:** [Database per Service Pattern](</en/architecture/database-per-service.html>), [Saga Pattern for Distributed Transactions](</en/architecture/saga-pattern.html>), [Strangler Fig Pattern for Legacy Migration](</en/architecture/strangler-fig.html>)

**See also:** [Database per Service Pattern](</en/architecture/database-per-service.html>), [Saga Pattern for Distributed Transactions](</en/architecture/saga-pattern.html>), [Strangler Fig Pattern for Legacy Migration](</en/architecture/strangler-fig.html>)

**See also:** [Database per Service Pattern](</en/architecture/database-per-service.html>), [Saga Pattern for Distributed Transactions](</en/architecture/saga-pattern.html>), [Strangler Fig Pattern for Legacy Migration](</en/architecture/strangler-fig.html>)

**See also:** [Database per Service Pattern](</en/architecture/database-per-service.html>), [Saga Pattern for Distributed Transactions](</en/architecture/saga-pattern.html>), [Strangler Fig Pattern for Legacy Migration](</en/architecture/strangler-fig.html>)

**See also:** [Database per Service Pattern](</en/architecture/database-per-service.html>), [Saga Pattern for Distributed Transactions](</en/architecture/saga-pattern.html>), [Strangler Fig Pattern for Legacy Migration](</en/architecture/strangler-fig.html>)

**See also:** [Database per Service Pattern](</en/architecture/database-per-service.html>), [Saga Pattern for Distributed Transactions](</en/architecture/saga-pattern.html>), [Strangler Fig Pattern for Legacy Migration](</en/architecture/strangler-fig.html>)
