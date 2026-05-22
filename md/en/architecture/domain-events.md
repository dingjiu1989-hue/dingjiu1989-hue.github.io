---
title: "Domain Events: Design and Implementation"
description: "Domain event design, publishing, handling, idempotency considerations, and the outbox pattern for reliable delivery"
date: 2026-04-24
board: architecture
url: https://aidev.fit/en/architecture/domain-events.html
---

# Domain Events: Design and Implementation

Domain events capture significant state changes within a bounded context. They are a tactical pattern from Domain-Driven Design that enables loose coupling between domain aggregates while maintaining consistency boundaries. A domain event represents something that happened in the past and is meaningful to domain experts: OrderSubmitted, PaymentReceived, InventoryDepleted. 

Designing domain events requires careful consideration of what information to include. Each event should contain the aggregate identifier, a timestamp of when the event occurred, the event type, and the data relevant to the change. Crucially, domain events should not contain internal implementation details of the aggregate. The specific fields should represent what happened from the domain perspective, not what data structures changed internally. Event naming follows past-tense convention: OrderShipped rather than ShipOrder, which would be a command. 

The publishing lifecycle has distinct phases. First, the domain event is raised within the aggregate during a command execution. The aggregate appends the event to a collection of unpublished events. When the repository saves the aggregate, it persists both the aggregate state and publishes the events. This atomicity is critical — publishing events must be transactional with the state change to prevent inconsistencies between what the system recorded and what other services learned. 

In-process domain event handling occurs within the same transaction. Event handlers registered in the application layer execute immediately after the aggregate is saved. These handlers are appropriate for side effects that must be consistent with the transaction, such as sending notifications or invalidating caches. They execute synchronously, so they must be fast and reliable. 

Out-of-process handlers receive domain events through a message broker or event bus. These handlers are appropriate for cross-service coordination, long-running workflows, or side effects where eventual consistency is acceptable. The distribution boundary is key — events that cross bounded contexts should be published to a message broker, while events consumed within the same context can be handled in-process. 

Idempotency is non-negotiable for domain event handlers. The same event may be delivered multiple times due to network retries, broker redelivery, or consumer failures. Handlers must detect and ignore duplicate processing. Common strategies include storing processed event IDs in a database with a unique constraint, using idempotent operations (SET x = y rather than x = x + 1), or making handlers check the current state before acting. 

The transactional outbox pattern solves the dual-write problem: updating the database and publishing an event must be atomic. Writing both the aggregate change and the event to the database in a single transaction ensures consistency. A separate process reads unpublished events from the outbox table and publishes them to the message broker. After successful publication, it marks the events as published or deletes them. This guarantees at-least-once delivery without distributed transactions. 

Event versioning addresses schema evolution. Domain events are persistent contracts that may be consumed by services running different versions. Strategies include keeping past event classes in the codebase, using a schema registry with compatibility checks, and designing events with optional fields and sensible defaults. Forward compatibility — where new consumers can read old events and vice versa — requires disciplined schema evolution. 

Testing domain events requires verifying that the correct events are raised for each command, that event data contains the expected information, and that handlers produce the correct side effects. Unit tests validate event raising within aggregates, while integration tests verify the full publish-and-handle pipeline including the outbox pattern.

**See also:** [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>), [Transactional Outbox Pattern](</en/architecture/transaction-outbox.html>), [Transactional Outbox Pattern](</en/architecture/transaction-outbox-reliable.html>).

**See also:** [Transactional Outbox Pattern](</en/architecture/transaction-outbox-reliable.html>), [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>), [Transactional Outbox Pattern](</en/architecture/transaction-outbox.html>)

**See also:** [Transactional Outbox Pattern](</en/architecture/transaction-outbox-reliable.html>), [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>), [Transactional Outbox Pattern](</en/architecture/transaction-outbox.html>)

**See also:** [Transactional Outbox Pattern](</en/architecture/transaction-outbox-reliable.html>), [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>), [Transactional Outbox Pattern](</en/architecture/transaction-outbox.html>)

**See also:** [Transactional Outbox Pattern](</en/architecture/transaction-outbox-reliable.html>), [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>), [Transactional Outbox Pattern](</en/architecture/transaction-outbox.html>)

**See also:** [Transactional Outbox Pattern](</en/architecture/transaction-outbox-reliable.html>), [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>), [Transactional Outbox Pattern](</en/architecture/transaction-outbox.html>)

**See also:** [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)

**See also:** [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)

**See also:** [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)

**See also:** [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)

**See also:** [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)

**See also:** [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)

**See also:** [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)

**See also:** [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)

**See also:** [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)

**See also:** [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)

**See also:** [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)

**See also:** [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)

**See also:** [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)

**See also:** [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)

**See also:** [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)

**See also:** [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)

**See also:** [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)
