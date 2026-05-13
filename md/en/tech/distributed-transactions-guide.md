---
title: "Distributed Transactions: Sagas, Two-Phase Commit, Outbox Pattern, and Idempotency"
description: "Master distributed transaction patterns for microservices — choreographed sagas, orchestrated sagas, 2PC, transactional outbox, and CDC."
date: 2026-05-08
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/distributed-transactions-guide.html
---

# Distributed Transactions: Sagas, Two-Phase Commit, Outbox Pattern, and Idempotency

Once you split a monolith into microservices, database transactions that used to be a simple BEGIN/COMMIT suddenly span multiple services and databases. Distributed transactions are the hardest problem in microservices — and getting them wrong corrupts data. This guide covers the production patterns: sagas, two-phase commit, the outbox pattern, and idempotency.

## Distributed Transaction Patterns Compared

Pattern| How It Works| Consistency| Complexity| Best For  
---|---|---|---|---  
Saga (Choreographed)| Each service listens for events and performs its step; emits next event on success| Eventually consistent| Medium| Simple workflows, 2-5 steps, independent services  
Saga (Orchestrated)| Central orchestrator coordinates each step, handles compensations on failure| Eventually consistent| Medium-High| Complex workflows, 5+ steps, sequential dependencies  
Two-Phase Commit (2PC)| Coordinator asks all participants "ready?" → all say yes → coordinator says "commit!"| Strong (ACID across services)| High| When strong consistency is required (banking, accounting)  
Transactional Outbox| Write events to an outbox table in the same DB transaction as the data change| Eventually consistent| Medium| Reliable event publishing (guaranteed delivery)  
Reservation Pattern| Reserve resources first (hold inventory), confirm or release after payment| Eventually consistent| Low-Medium| Booking systems (flights, hotels, tickets)  
  
## The Outbox Pattern: Guaranteed Event Publishing
    
    
    -- The problem: you update a database row AND publish an event.
    -- If the DB write succeeds but the event publish fails → data inconsistency.
    -- If the event publish succeeds but the DB write fails → ghost events.
    
    -- The solution: write BOTH in a single DB transaction using an outbox table.
    
    -- Step 1: Update business data + insert into outbox in ONE transaction
    BEGIN;
      UPDATE orders SET status = 'confirmed' WHERE id = 123;
      INSERT INTO outbox (aggregate_id, event_type, payload)
        VALUES (123, 'OrderConfirmed', '{"order_id": 123, "user_id": 456}');
    COMMIT;
    
    -- Step 2: Outbox poller reads events, publishes to message broker, deletes
    -- Debezium (CDC): reads the outbox changes from WAL, publishes to Kafka
    -- Simpler approach: poll the outbox table every 100ms, publish, mark as sent
    
    -- This guarantees: either BOTH the data change and event happen, or NEITHER.
    -- It eliminates the dual-write problem entirely.

## Idempotency: The Foundation of Reliable Distributed Systems

Mechanism| How It Works| Best For  
---|---|---  
Idempotency Key| Client generates a unique key; server stores (key, result); replay returns cached result| Payment APIs, order creation — any operation that must not duplicate  
Database Unique Constraint| INSERT ... ON CONFLICT DO NOTHING — duplicate key = safe skip| Event deduplication, exactly-once processing  
State Machine| Check current state: "if order.status == 'pending' → confirm; else skip"| Workflow steps that should only advance, never replay  
Request Deduplication (at-least-once → exactly-once)| Store processed message IDs; skip duplicates| Message queue consumers  
  
## Implementing a Simple Orchestrated Saga
    
    
    # Order fulfillment saga: orchestrator coordinates 3 services
    # Each step has a compensating action for rollback
    
    async def fulfill_order(order_id, user_id, amount):
        saga_id = generate_saga_id()
    
        # Step 1: Reserve inventory
        try:
            inventory.reserve(order_id, saga_id)
        except Exception:
            return failed("Inventory unavailable")
    
        # Step 2: Charge payment
        try:
            payment_id = payment.charge(user_id, amount, saga_id)
        except Exception:
            inventory.release(order_id, saga_id)  # COMPENSATE step 1
            return failed("Payment failed")
    
        # Step 3: Schedule shipping
        try:
            shipping.schedule(order_id, saga_id)
        except Exception:
            payment.refund(payment_id, saga_id)   # COMPENSATE step 2
            inventory.release(order_id, saga_id)  # COMPENSATE step 1
            return failed("Shipping failed")
    
        return success(order_id)
    
    # Key principle: each compensating action must be IDEMPOTENT
    # (calling refund twice on the same payment should not double-refund)

**Bottom line:** Sagas + the outbox pattern + idempotency keys solve 95% of distributed transaction problems. Start with choreographed sagas for simple workflows (2-3 steps, independent services). Switch to orchestrated sagas when the workflow becomes complex (5+ steps, sequential dependencies). Use the outbox pattern for every event published from a database transaction. And always, always make compensating actions idempotent. See also: [Event-Driven Architecture Guide](</en/tech/event-driven-architecture-guide.html>) and [Microservices vs Monolith](</en/tech/microservices-vs-monolith.html>).
