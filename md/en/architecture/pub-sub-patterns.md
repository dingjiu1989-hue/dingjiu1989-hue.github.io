---
title: "Pub-Sub Patterns: Event-Driven Communication"
description: "A deep dive into publish-subscribe patterns for decoupled service communication in distributed systems."
date: 2026-05-14
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/pub-sub-patterns.html
---

# Pub-Sub Patterns: Event-Driven Communication

The publish-subscribe (pub-sub) pattern enables one-to-many communication between services without direct coupling. Publishers emit events without knowing which subscribers will receive them. Subscribers express interest in certain events and receive them asynchronously.

## Core Concepts

A pub-sub system has three components: publishers that produce events, a message broker that routes events, and subscribers that consume events. Events are categorized into topics or channels. Subscribers register interest in specific topics and receive all events published to those topics.

## Message Brokers

Apache Kafka is the most popular pub-sub system for high-throughput event streaming. Topics are partitioned for parallelism, and consumers organize into consumer groups for load-balanced consumption. Kafka retains events even after consumption, enabling replay and reprocessing.

Redis Pub-Sub is lightweight but does not persist messages. If a subscriber is offline, messages are lost. This is suitable for real-time notifications where message loss is acceptable.

Google Pub-Sub and AWS SNS provide managed pub-sub services with automatic scaling, dead letter queues, and exactly-once delivery guarantees.

## At-Least-Once vs Exactly-Once

Most pub-sub systems provide at-least-once delivery. Subscribers must handle duplicate events through idempotent processing. Exactly-once delivery requires coordination between the broker, producer, and consumer—achievable with Kafka exactly-once semantics but with performance overhead.

## Pattern Variations

Topic-based pub-sub routes events by topic name. Content-based pub-sub routes events based on message content evaluation. Hybrid systems combine both approaches for flexible routing.

## Best Practices

Design event schemas for backward compatibility. Use schema registries to manage schema evolution. Monitor subscription lag to detect consumer issues. Implement circuit breakers to handle slow consumers gracefully. Test subscriber failure scenarios to ensure system resilience.

**See also:** [Messaging Patterns: Pub/Sub and Request/Reply](</en/architecture/messaging-patterns.html>), [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [Event Collaboration: Choreography vs Orchestration](</en/architecture/event-collaboration.html>).

**See also:** [Messaging Patterns: Pub/Sub and Request/Reply](</en/architecture/messaging-patterns.html>), [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [Event Collaboration: Choreography vs Orchestration](</en/architecture/event-collaboration.html>)

**See also:** [Messaging Patterns: Pub/Sub and Request/Reply](</en/architecture/messaging-patterns.html>), [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [Event Collaboration: Choreography vs Orchestration](</en/architecture/event-collaboration.html>)

**See also:** [Messaging Patterns: Pub/Sub and Request/Reply](</en/architecture/messaging-patterns.html>), [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [Event Collaboration: Choreography vs Orchestration](</en/architecture/event-collaboration.html>)

**See also:** [Messaging Patterns: Pub/Sub and Request/Reply](</en/architecture/messaging-patterns.html>), [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [Event Collaboration: Choreography vs Orchestration](</en/architecture/event-collaboration.html>)

**See also:** [Messaging Patterns: Pub/Sub and Request/Reply](</en/architecture/messaging-patterns.html>), [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [Event Collaboration: Choreography vs Orchestration](</en/architecture/event-collaboration.html>)

**See also:** [Fanout Pattern for Event Distribution](</en/architecture/fanout-pattern.html>), [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Distributed Tracing: Deep Dive](</en/architecture/distributed-tracing-deep.html>)

**See also:** [Fanout Pattern for Event Distribution](</en/architecture/fanout-pattern.html>), [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Distributed Tracing: Deep Dive](</en/architecture/distributed-tracing-deep.html>)

**See also:** [Fanout Pattern for Event Distribution](</en/architecture/fanout-pattern.html>), [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Distributed Tracing: Deep Dive](</en/architecture/distributed-tracing-deep.html>)
