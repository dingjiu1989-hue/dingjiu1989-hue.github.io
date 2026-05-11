---
title: "Event Sourcing Pattern"
description: "Learn the event sourcing pattern for capturing state changes as immutable events."
date: 2026-05-11
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/event-sourcing.html
---

Event sourcing is an architectural pattern where state changes are stored as a sequence of immutable events, rather than overwriting the current state. Instead of storing "what the current balance is," you store every "account credited" and "account debited" event. This article explores the pattern, its benefits, trade-offs, and when to use it.

## How Event Sourcing Works

In a traditional CRUD approach, you store the current state of an entity. When a user updates their profile, you issue an UPDATE statement that overwrites the previous values. The history of changes is lost.

With event sourcing, every change to the application state is captured as an event object:

```
AccountCreated { id: 123, owner: "Alice", initial_balance: 0 }
MoneyDeposited { account_id: 123, amount: 500, timestamp: 2026-01-15T10:00:00Z }
MoneyWithdrawn { account_id: 123, amount: 100, timestamp: 2026-01-16T14:30:00Z }
```

The current state is derived by replaying all events in order. To get Alice's balance, you replay the events: start at 0, add 500, subtract 100, resulting in 400. The event store is the single source of truth.

## The Event Store

The event store is the central component. It is an append-only database that stores events sequentially. Each event has:

- An aggregate ID (which entity does this belong to?)
- A sequence number or timestamp (what order did things happen?)
- Event type (what happened?)
- Event payload (the data associated with the change)

Most implementations use a dedicated event store database (like EventStoreDB) or a regular database used in a special way. PostgreSQL, for example, works well as an event store when combined with proper indexing.

## Benefits of Event Sourcing

**Complete Audit Trail.** Every state change is recorded permanently. This is invaluable for regulated industries like finance, healthcare, and insurance. You can always answer the question "who changed what and when?"

**Temporal Queries.** You can reconstruct the state of the system at any point in time. Need to know what the user's profile looked like on January 1st? Just replay events up to that date.

**Debugging and Analysis.** Events capture intent, not just the resulting state. This makes debugging production issues significantly easier. You can replay events in a development environment to reproduce bugs.

**Flexibility.** Multiple read models can be derived from the same event stream. Your reporting system can consume the same events as your customer-facing UI, each projecting the data differently.

## Challenges and Trade-offs

Event sourcing is not free. The biggest challenges include:

**Complexity.** Event sourcing introduces concepts (events, aggregates, projections, snapshots) that are unfamiliar to many developers. The learning curve is steep.

**Event Schema Evolution.** Events are immutable, but their schemas will change over time. You need strategies for handling events that were created with old schemas. Common approaches include upcasting (transforming old events to new formats on read) or versioned event types.

**Storage Requirements.** Since you never delete data, storage grows continuously. Regular snapshotting helps -- you store the current state at a point in time, then only replay events after the snapshot.

**Eventual Consistency.** Read models (projections) are typically updated asynchronously. Your system must tolerate temporary inconsistencies between the event store and the read views.

## When to Use Event Sourcing

Event sourcing excels in specific scenarios:

- **Auditing and compliance** are critical requirements.
- **Temporal queries** are needed ("show me the state as of last Tuesday").
- **Complex business logic** that benefits from understanding the sequence of events.
- **Multiple read models** consuming the same data in different ways.

Avoid event sourcing for simple CRUD applications where a traditional database works perfectly well. The added complexity is rarely justified without a concrete need for the benefits above.

## CQRS and Event Sourcing

Event sourcing is frequently paired with CQRS (Command Query Responsibility Segregation). Commands write events to the event store, while separate read models (projections) consume those events to build optimized query structures. This combination gives you the best of both worlds: reliable writes through events and fast reads through purpose-built projections.

## Practical Implementation Tips

Start small. Implement event sourcing for one bounded context or aggregate root in your system, not the entire application. Use an existing event store library rather than building your own. Take snapshots regularly (every N events) to keep replay times manageable. And invest in monitoring -- event stores behave differently from traditional databases under load.

## Summary

Event sourcing is powerful but complex. Use it when you need a complete audit trail, temporal queries, or flexible read models. Pair it with CQRS for production systems. Be prepared for the operational complexity, and start with a limited scope to build experience before expanding.
