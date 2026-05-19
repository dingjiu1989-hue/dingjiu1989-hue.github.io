---
title: "Event Notification vs Event-Carried State Transfer"
description: "Compare event notification and event-carried state transfer patterns for microservices communication."
date: 2026-05-07
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/event-notification-vs-event-carrying.html
---

# Event Notification vs Event-Carried State Transfer

Event notification and event-carried state transfer are two patterns for communicating state changes between microservices. The choice affects coupling, data consistency, and service autonomy.

## Event Notification

The publisher sends only a reference to the changed entity. Consumers must query the publisher's API for details. This minimizes coupling—consumers know only that something changed. The publisher's API remains the source of truth.

Drawbacks: each consumer must make additional API calls. This increases latency and reduces availability. If the publisher is down during event processing, consumers cannot get the full picture.

## Event-Carried State Transfer

The publisher includes all relevant data in the event. Consumers can process events without querying the publisher. This reduces latency and increases resilience—consumers have the data they need even if the publisher is unavailable.

Trade-offs: data duplication increases storage requirements. Consumers may have stale data if the publisher changes its data model. The event schema becomes a public contract between publisher and consumers.

## Choosing

Use event notification when the consumer always needs fresh data or the event's context is minimal. Use event-carried state transfer when consumers need data immediately or the publisher's API availability cannot be guaranteed.

**See also:** [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>), [Polling Consumer vs Event-Driven Consumer](</en/architecture/polling-consumer.html>), [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>).

**See also:** [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>), [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [Polling Consumer vs Event-Driven Consumer](</en/architecture/polling-consumer.html>)

**See also:** [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>), [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [Polling Consumer vs Event-Driven Consumer](</en/architecture/polling-consumer.html>)

**See also:** [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>), [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [Polling Consumer vs Event-Driven Consumer](</en/architecture/polling-consumer.html>)

**See also:** [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>), [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [Polling Consumer vs Event-Driven Consumer](</en/architecture/polling-consumer.html>)

**See also:** [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>), [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [Polling Consumer vs Event-Driven Consumer](</en/architecture/polling-consumer.html>)

**See also:** [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>), [Graceful Shutdown Patterns](</en/architecture/graceful-shutdown.html>), [Monolith-First Strategy](</en/architecture/monolith-first-strategy.html>)

**See also:** [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>), [Graceful Shutdown Patterns](</en/architecture/graceful-shutdown.html>), [Monolith-First Strategy](</en/architecture/monolith-first-strategy.html>)

**See also:** [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>), [Graceful Shutdown Patterns](</en/architecture/graceful-shutdown.html>), [Monolith-First Strategy](</en/architecture/monolith-first-strategy.html>)

**See also:** [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>), [Graceful Shutdown Patterns](</en/architecture/graceful-shutdown.html>), [Monolith-First Strategy](</en/architecture/monolith-first-strategy.html>)
