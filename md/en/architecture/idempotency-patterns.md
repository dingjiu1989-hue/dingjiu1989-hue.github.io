---
title: "Idempotency Patterns in Distributed Systems"
description: "Idempotency keys, deduplication, at-least-once delivery, exactly-once semantics, and implementation patterns"
date: 2026-04-27
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/idempotency-patterns.html
---

# Idempotency Patterns in Distributed Systems

Idempotency is the property that applying an operation multiple times produces the same result as applying it once. In distributed systems, networks are unreliable, services fail and restart, and clients naturally retry. Idempotency turns unreliable infrastructure into reliable semantics — it allows safe retries without data corruption or duplicate side effects. 

The idempotency key pattern is the foundation. The client generates a unique key for each operation and includes it with the request. The server stores the key and its result. If the server receives a duplicate request with the same key, it returns the stored result without re-executing the operation. The idempotency key should be scoped to the client and operation type. UUIDs or ULIDs are typical key formats. 

Implementation requires an idempotency store. This is typically a database table or Redis cache with the key as the primary key. When a request arrives, the server checks the idempotency store. If the key exists and the operation completed, return the cached response. If the key exists and the operation is in progress, wait or return a conflict. If the key does not exist, execute the operation and store the result. The key must be created atomically — a unique constraint prevents two requests with the same key from executing simultaneously. 

The idempotency key lifecycle requires careful management. The key is created at the start of the request and, depending on the implementation, may have a TTL. After the TTL expires, the key is eligible for cleanup. The client should use a new key for each distinct operation. For example, each payment attempt should have a unique idempotency key, even if retrying the same order's payment. This prevents the case where the first attempt times out, the key expires, and a retry with the same key accidentally creates a duplicate payment. 

At-least-once delivery guarantees that a message is delivered one or more times. The consumer handles duplicates through idempotent processing. This is the pragmatic baseline for most messaging systems — achieving exactly-once end-to-end is extremely difficult, so systems layer idempotency on top of at-least-once delivery to provide the same guarantees. 

Exactly-once semantics combine at-least-once delivery with idempotent processing. The system must guarantee: the operation executes at least once, and duplicate executions produce the same result as a single execution. True exactly-once requires end-to-end idempotency spanning the producer, broker, consumer, and downstream systems. This is rarely achieved in practice — systems aim for effectively-once by ensuring idempotent consumers. 

Deduplication is a closely related pattern for event processing. When a consumer receives an event, it checks a deduplication table (event_id processed, timestamp). If the event ID already exists, it skips processing. The deduplication table should have a unique constraint on event_id, and the check-and-insert should be atomic. Deduplication windows must be longer than the maximum expected redelivery interval. A 24-hour deduplication window is common. 

State-based idempotency offers an alternative to key-based deduplication. Instead of tracking operation IDs, the system checks the current state before performing state-changing operations. For example, before processing a payment, check that the invoice is in "unpaid" state. If the invoice is already "paid," skip the payment. This works well when operations map to clear state transitions but requires careful handling of race conditions. 

Uniqueness constraints are the most reliable idempotency mechanism. A database unique constraint on business keys (order ID, payment reference) guarantees that duplicate operations fail atomically at the database level. This is the foundation of idempotent inserts. The constraint handles concurrent requests correctly — only the first insert succeeds, and subsequent attempts fail with a unique constraint violation that the application can handle gracefully. 

Idempotency should be designed into every external-facing API and every event handler from the start. Retrofitting idempotency after data corruption incidents is painful. The upfront cost of adding idempotency keys and deduplication logic is minimal compared to the cost of debugging duplicate processing in production.

**See also:** [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>).

**See also:** [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>)

**See also:** [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>)

**See also:** [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>)

**See also:** [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>)

**See also:** [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>)

**See also:** [Leader Election in Distributed Systems](</en/architecture/leader-election.html>), [Rate Limiting Architecture](</en/architecture/rate-limiting-architecture.html>), [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>)

**See also:** [Leader Election in Distributed Systems](</en/architecture/leader-election.html>), [Rate Limiting Architecture](</en/architecture/rate-limiting-architecture.html>), [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>)

**See also:** [Leader Election in Distributed Systems](</en/architecture/leader-election.html>), [Rate Limiting Architecture](</en/architecture/rate-limiting-architecture.html>), [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>)

**See also:** [Leader Election in Distributed Systems](</en/architecture/leader-election.html>), [Rate Limiting Architecture](</en/architecture/rate-limiting-architecture.html>), [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>)

**See also:** [Leader Election in Distributed Systems](</en/architecture/leader-election.html>), [Rate Limiting Architecture](</en/architecture/rate-limiting-architecture.html>), [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>)

**See also:** [Leader Election in Distributed Systems](</en/architecture/leader-election.html>), [Rate Limiting Architecture](</en/architecture/rate-limiting-architecture.html>), [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>)

**See also:** [Leader Election in Distributed Systems](</en/architecture/leader-election.html>), [Rate Limiting Architecture](</en/architecture/rate-limiting-architecture.html>), [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>)

**See also:** [Leader Election in Distributed Systems](</en/architecture/leader-election.html>), [Rate Limiting Architecture](</en/architecture/rate-limiting-architecture.html>), [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>)

**See also:** [Leader Election in Distributed Systems](</en/architecture/leader-election.html>), [Rate Limiting Architecture](</en/architecture/rate-limiting-architecture.html>), [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>)

**See also:** [Leader Election in Distributed Systems](</en/architecture/leader-election.html>), [Rate Limiting Architecture](</en/architecture/rate-limiting-architecture.html>), [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>)
