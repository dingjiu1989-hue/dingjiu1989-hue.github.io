---
title: "Two-Phase Commit (2PC) for Distributed Transactions"
description: "Two-phase commit protocol: coordinator, prepare/commit phases, failure scenarios, XA protocol, and when to use sagas instead."
date: 2026-05-12
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/two-phase-commit.html
---

Two-Phase Commit (2PC) is a distributed consensus protocol that ensures all participants in a transaction either commit or abort together. It provides atomicity across multiple databases, message queues, or other resources. This article explains the 2PC protocol, failure scenarios, the XA standard, and when to use sagas instead.

## How 2PC Works

Two-Phase Commit has two phases: Prepare and Commit (or Abort).

### Phase 1: Prepare

The coordinator sends a "prepare" request to all participants. Each participant:

1. Checks if it can commit the transaction.
2. If yes: writes the transaction to a stable log, acquires necessary locks, and responds "ready" (or "yes").
3. If no: responds "abort" (or "no").

```python
class TransactionCoordinator:
    def __init__(self, participants):
        self.participants = participants
        self.state = "INIT"
        self.transaction_id = generate_tx_id()
    
    def execute_transaction(self, operations):
        """Execute a distributed transaction using 2PC."""
        
        # Phase 1: Prepare
        self.state = "PREPARING"
        votes = []
        
        for participant in self.participants:
            try:
                response = participant.prepare(self.transaction_id, operations)
                votes.append(response)
            except Exception as e:
                votes.append({"status": "abort", "reason": str(e)})
        
        # Phase 2: Commit or Abort
        if all(v["status"] == "ready" for v in votes):
            self._commit()
            return "COMMITTED"
        else:
            self._abort()
            return "ABORTED"
    
    def _commit(self):
        self.state = "COMMITTING"
        for participant in self.participants:
            participant.commit(self.transaction_id)
        self.state = "COMMITTED"
    
    def _abort(self):
        self.state = "ABORTING"
        for participant in self.participants:
            participant.rollback(self.transaction_id)
        self.state = "ABORTED"
```

### Phase 2: Commit

If all participants responded "ready," the coordinator sends a "commit" message. Each participant applies the transaction and releases locks.

```python
class DatabaseParticipant:
    def __init__(self, db_connection):
        self.db = db_connection
        self.prepared_transactions = {}
    
    def prepare(self, transaction_id, operations):
        """Prepare phase: validate and lock, but don't apply."""
        try:
            # Begin a local transaction
            self.db.begin()
            
            # Validate all operations
            for op in operations:
                if not self._validate(op):
                    self.db.rollback()
                    return {"status": "abort", "reason": f"Validation failed: {op}"}
            
            # Execute operations within local transaction
            for op in operations:
                self.db.execute(op["sql"], op["params"])
            
            # Don't commit yet — just prepare
            self.prepared_transactions[transaction_id] = self.db.savepoint()
            return {"status": "ready"}
            
        except Exception as e:
            self.db.rollback()
            return {"status": "abort", "reason": str(e)}
    
    def commit(self, transaction_id):
        """Commit phase: apply the prepared transaction."""
        if transaction_id in self.prepared_transactions:
            self.db.commit()
            del self.prepared_transactions[transaction_id]
    
    def rollback(self, transaction_id):
        """Rollback the prepared transaction."""
        if transaction_id in self.prepared_transactions:
            self.db.rollback()
            del self.prepared_transactions[transaction_id]
```

### Flow Diagram

```
Coordinator          Participant A        Participant B
     |                     |                    |
     |--- Prepare -------->|                    |
     |--- Prepare ----------------------------->|
     |                     |                    |
     |<--- Ready ----------|                    |
     |<--- Ready ------------------------------|
     |                     |                    |
     |--- Commit --------->|                    |
     |--- Commit ----------------------------->|
     |                     |                    |
     |<--- Acked ----------|                    |
     |<--- Acked ------------------------------|
     |                     |                    |
```

## Failure Scenarios

2PC handles various failure scenarios, but some situations require human intervention or complex recovery.

### Participant Failure During Prepare

If a participant crashes during the prepare phase, the coordinator can either retry or abort. Once the participant recovers, it must check whether it had prepared a transaction.

```
Coordinator: Sends prepare
Participant: Crashes (unreachable)
Coordinator: Timeout -> Sends abort to all participants
Participant: Restarts, finds no prepared transaction -> OK
```

### Coordinator Failure During Commit

The most dangerous scenario. The coordinator sends "commit" to some participants but crashes before reaching others. Participants are left in a "prepared but uncertain" state.

```
Coordinator: Sends commit to A, crashes before sending to B
A: Committed
B: Prepared (waiting for coordinator decision)
```

**Resolution**: The prepared transaction on B remains "in doubt" until the coordinator recovers. B holds locks indefinitely. Recovery requires either:
- The coordinator restarts and resends the commit/abort decision.
- An administrator manually inspects and resolves the transaction.

### Network Partition

If the network splits during phase 2, participants that cannot reach the coordinator remain in the prepared state. They hold locks and may block other transactions.

## XA Protocol

XA is the standard specification for distributed transaction processing. It defines the interface between a transaction manager (coordinator) and resource managers (databases, message brokers).

### XA in Practice

```java
// Java: XA transaction with JTA
import javax.transaction.xa.XAResource;
import javax.sql.XAConnection;
import javax.sql.XADataSource;

public class XATransactionExample {
    public void transferMoney(int fromAccount, int toAccount, double amount) {
        // Get XA connections
        XAConnection db1Conn = db1DataSource.getXAConnection();
        XAConnection db2Conn = db2DataSource.getXAConnection();
        
        XAResource db1Res = db1Conn.getXAResource();
        XAResource db2Res = db2Conn.getXAResource();
        
        // Start global transaction
        Xid xid = createXid();
        db1Res.start(xid, XAResource.TMNOFLAGS);
        db2Res.start(xid, XAResource.TMNOFLAGS);
        
        try {
            // Execute operations
            executeUpdate(db1Conn, "UPDATE accounts SET balance = balance - ? WHERE id = ?",
                         amount, fromAccount);
            executeUpdate(db2Conn, "UPDATE accounts SET balance = balance + ? WHERE id = ?",
                         amount, toAccount);
            
            // End the transaction branches
            db1Res.end(xid, XAResource.TMSUCCESS);
            db2Res.end(xid, XAResource.TMSUCCESS);
            
            // Phase 1: Prepare
            int db1Prepare = db1Res.prepare(xid);
            int db2Prepare = db2Res.prepare(xid);
            
            // Phase 2: Commit
            if (db1Prepare == XAResource.XA_OK && db2Prepare == XAResource.XA_OK) {
                db1Res.commit(xid, false);
                db2Res.commit(xid, false);
            } else {
                db1Res.rollback(xid);
                db2Res.rollback(xid);
            }
        } catch (Exception e) {
            // Rollback
            db1Res.rollback(xid);
            db2Res.rollback(xid);
        }
    }
}
```

### XA Support in Databases

| Database | XA Support | Notes |
|----------|------------|-------|
| PostgreSQL | Yes (pg_xact) | Requires max_prepared_transactions > 0 |
| MySQL | Yes (XA syntax) | `XA START`, `XA END`, `XA PREPARE`, `XA COMMIT` |
| Oracle | Yes | Native XA support via Oracle XA |
| SQL Server | Yes | Via .NET System.Transactions |
| MongoDB | No | Multi-document transactions, not XA |
| Cassandra | No | No distributed transaction support |

### MySQL XA Example

```sql
-- MySQL XA transaction across two databases
-- On node 1:
XA START 'xid-123';
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
XA END 'xid-123';
XA PREPARE 'xid-123';

-- On node 2:
XA START 'xid-123';
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
XA END 'xid-123';
XA PREPARE 'xid-123';

-- Coordinator instructs both to commit:
-- On node 1:
XA COMMIT 'xid-123';
-- On node 2:
XA COMMIT 'xid-123';

-- If anything failed:
-- XA ROLLBACK 'xid-123';
```

## When 2PC Works

2PC is appropriate when:

1. **Strong consistency is required**: All participants must see the same result.
2. **Transaction duration is short**: Locks are held during the prepare phase. Long transactions block other operations.
3. **Participants are reliable**: Frequent failures lead to in-doubt transactions requiring manual recovery.
4. **The transaction involves few participants**: 2PC with 2-3 participants is manageable. 2PC with 10+ participants is fragile.
5. **Fallback to manual recovery is acceptable**: In-doubt transactions can be resolved manually.

### Use Cases

- **Financial transfers**: Money moves from one account (DB1) to another (DB2).
- **Inventory and order**: Reserve inventory in one system and create an order in another.
- **Account provisioning**: Create a user in the IDP and a billing account simultaneously.

## When to Use Sagas Instead

The saga pattern is an alternative to 2PC for long-running transactions. Instead of locking resources, sagas define compensating actions for each step.

### Saga Pattern

```
Saga: Order Processing

1. Create Order (Service A)
   Compensation: Cancel Order
   
2. Reserve Inventory (Service B)
   Compensation: Release Inventory
   
3. Process Payment (Service C)
   Compensation: Refund Payment
   
4. Ship Order (Service D)
   Compensation: No compensation (can't un-ship)
```

```python
class OrderSaga:
    def __init__(self):
        self.executed_steps = []
        self.compensations = []
    
    def execute(self):
        try:
            # Step 1: Create order
            order = payment_service.create_order(data)
            self.executed_steps.append(("create_order", order.id))
            self.compensations.append(lambda: payment_service.cancel_order(order.id))
            
            # Step 2: Reserve inventory
            inventory = inventory_service.reserve(order.items)
            self.executed_steps.append(("reserve", order.id))
            self.compensations.append(lambda: inventory_service.release(order.items))
            
            # Step 3: Process payment
            payment = payment_service.charge(order.total)
            self.executed_steps.append(("payment", payment.id))
            self.compensations.append(lambda: payment_service.refund(payment.id))
            
            # Step 4: Ship (no compensation)
            shipment = shipping_service.ship(order.id)
            self.executed_steps.append(("ship", shipment.id))
            
        except Exception as e:
            self._compensate()
            raise SagaFailedError(str(e), self.executed_steps)
    
    def _compensate(self):
        # Execute compensations in reverse order
        for compensation in reversed(self.compensations):
            try:
                compensation()
            except Exception as e:
                log.error(f"Compensation failed: {e}")
                # Manual intervention required for this step
```

### 2PC vs Saga

| Aspect | 2PC | Saga |
|--------|-----|------|
| Consistency | Strong (ACID) | Eventual |
| Locking | Holds locks during prepare | No locks |
| Transaction duration | Short | Long-running possible |
| Resilience | Fragile (in-doubt state) | Resilient (compensations) |
| Complexity | Medium | Higher |
| Performance | Lower (sync overhead) | Higher (async) |
| Recovery | Manual for in-doubt | Automatic compensations |

### Decision Guide

Use **2PC** when:
- The transaction completes in milliseconds.
- Strong consistency is non-negotiable.
- All participants are reliable and available.

Use **Saga** when:
- The transaction spans minutes or hours.
- Eventual consistency is acceptable.
- You need high availability and resilience.
- Participants are loosely coupled services.

## Conclusion

Two-Phase Commit provides strong consistency across distributed systems through a prepare/commit protocol. It is appropriate for short transactions requiring atomicity across few participants. However, 2PC has significant drawbacks: it blocks resources during prepare, is fragile to coordinator failure, and requires potentially messy manual recovery for in-doubt transactions. Consider the saga pattern for long-running, loosely coupled, and highly available distributed transactions. In modern microservice architectures, sagas are generally preferred over 2PC.
