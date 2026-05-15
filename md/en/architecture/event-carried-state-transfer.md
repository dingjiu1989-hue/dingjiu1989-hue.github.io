---
title: "Event-Carried State Transfer Pattern"
description: "Learn the event-carried state transfer pattern for reducing service dependencies in event-driven architectures."
date: 2026-05-12
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/event-carried-state-transfer.html
---

# Event-Carried State Transfer Pattern

## Event-Carried State Transfer Pattern

## Event-Carried State Transfer Pattern

## Event-Carried State Transfer Pattern

## Event-Carried State Transfer Pattern

## Event-Carried State Transfer Pattern

## Event-Carried State Transfer Pattern

## Event-Carried State Transfer Pattern

## Event-Carried State Transfer Pattern

## Event-Carried State Transfer Pattern

## Event-Carried State Transfer Pattern

## Event-Carried State Transfer Pattern

## Event-Carried State Transfer Pattern

Event-carried state transfer is a messaging pattern where events include the full state needed by consumers, eliminating the need for consumers to query the producer for additional data. This reduces synchronous dependencies and improves system resilience.

### How It Works

When a service publishes an event about a domain entity, it includes all relevant state in the event payload. A UserCreated event contains the user's name, email, role, and other attributes. The consumer that needs this information has it immediately without making an additional API call.

This is a departure from traditional event design, where events contain only identifiers and consumers query the producer for details. That approach creates synchronous coupling and single points of failure.

### Benefits

Event-carried state transfer eliminates synchronous dependencies. If the producer is down, consumers can still process events using the embedded state. It also reduces latency—consumers save the round-trip time of querying the producer.

System resilience improves because consumers are self-sufficient. A consumer can rebuild its state entirely from the event stream without accessing the producer's API.

### Drawbacks

Events become larger, increasing message broker storage and network bandwidth. Schema evolution is more complex because event payloads now contain more fields. Event producers must anticipate what consumers need, which requires coordination.

Stale data is a concern. If the producer updates its internal state after publishing the event, consumers have the old state. This is acceptable in eventually consistent systems but requires careful design.

### When to Use

Use event-carried state transfer when consumer independence is a priority, when the producer is likely to experience high load from consumer queries, and when eventual consistency is acceptable. Avoid it when event payload size is constrained or when consumers need absolutely current data.

### Best Practices

Include only the state that consumers need, not the producer's entire internal model. Version event schemas to manage payload evolution. Document which fields each consumer uses so producers understand the impact of changes.

**See also:** [Event Notification vs Event-Carried State Transfer](</en/architecture/event-notification-vs-event-carrying.html>), [Saga Choreography Pattern](</en/architecture/saga-choreography.html>), [Fanout Pattern for Event Distribution](</en/architecture/fanout-pattern.html>).

**See also:** [Event Notification vs Event-Carried State Transfer](</en/architecture/event-notification-vs-event-carrying.html>), [Fanout Pattern for Event Distribution](</en/architecture/fanout-pattern.html>), [Sidecar Pattern in Microservices Architecture](</en/architecture/sidecar-pattern.html>)

**See also:** [Event Notification vs Event-Carried State Transfer](</en/architecture/event-notification-vs-event-carrying.html>), [Fanout Pattern for Event Distribution](</en/architecture/fanout-pattern.html>), [Sidecar Pattern in Microservices Architecture](</en/architecture/sidecar-pattern.html>)
