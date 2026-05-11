---
title: "ACID vs BASE Transactions"
description: "Compare ACID and BASE transaction models, when to use each, and how modern databases balance consistency, availability, and partition tolerance."
date: 2026-05-11
board: database
url: https://dingjiu1989-hue.github.io/en/database/acid-vs-base.html
---

## The CAP Theorem

Before understanding ACID and BASE, you must understand the CAP theorem. A distributed system can guarantee at most two of three properties:

| Property | Meaning |
|----------|---------|
| Consistency (C) | Every read receives the most recent write |
| Availability (A) | Every request receives a non-error response |
| Partition Tolerance (P) | System continues operating despite network failures |

Since network partitions are inevitable, distributed systems must choose between CP (consistency) and AP (availability).

## ACID Transactions

ACID is the traditional database transaction model used by relational databases.

### Atomicity

A transaction is all-or-nothing. If any part fails, the entire transaction is rolled back.

```sql
BEGIN;

UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- If the server crashes after the first UPDATE but before the second,
-- the database rolls back automatically.
-- Both updates succeed or neither does.

COMMIT;
```

### Consistency

A transaction brings the database from one valid state to another. Constraints, triggers, and cascades ensure data integrity.

```sql
ALTER TABLE orders ADD CONSTRAINT chk_positive_amount
    CHECK (amount > 0);

-- This will fail:
INSERT INTO orders (amount) VALUES (-50);  -- Constraint violation
```

### Isolation

Concurrent transactions do not interfere with each other. SQL defines four isolation levels:

| Isolation Level | Dirty Read | Non-Repeatable Read | Phantom Read |
|-----------------|------------|--------------------|--------------|
| Read Uncommitted | Possible | Possible | Possible |
| Read Committed | Prevented | Possible | Possible |
| Repeatable Read | Prevented | Prevented | Possible |
| Serializable | Prevented | Prevented | Prevented |

```sql
-- Serializable isolation prevents all anomalies
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
BEGIN;
SELECT * FROM products WHERE stock > 0;
-- Other transactions cannot modify products until this one commits
COMMIT;
```

### Durability

Once a transaction is committed, it survives system failures. WAL (Write-Ahead Logging) ensures durability:

```sql
-- PostgreSQL's WAL ensures durability
-- Even if power fails, committed transactions are recovered
SHOW wal_level;  -- replica or logical
```

## BASE Transactions

BASE is the transaction model used by many NoSQL databases. It stands for:

- **Basically Available**: The system guarantees availability (per CAP).
- **Soft State**: The system state may change over time without input.
- **Eventual Consistency**: Given enough time, all replicas will converge.

### Eventual Consistency in Practice

```javascript
// DynamoDB: eventually consistent reads (default)
const { Item } = await docClient.get({
    TableName: 'users',
    Key: { id: '123' },
    ConsistentRead: false  // Eventual consistency
});

// Strongly consistent read (higher latency, lower availability)
const { Item } = await docClient.get({
    TableName: 'users',
    Key: { id: '123' },
    ConsistentRead: true  // Strong consistency
});
```

### Handling Eventual Consistency

```python
def create_order(user_id, product_id):
    """Handle eventual consistency in application code."""

    # Write the order (eventually consistent)
    orders.insert_one({
        "user_id": user_id,
        "product_id": product_id,
        "status": "pending",
        "created_at": datetime.utcnow()
    })

    # For immediate read-after-write, query by timestamp
    def get_recent_order():
        return orders.find_one({
            "user_id": user_id,
            "product_id": product_id,
            "created_at": {"$gte": datetime.utcnow() - timedelta(seconds=1)}
        })
```

## ACID vs BASE Comparison

| Property | ACID | BASE |
|----------|------|------|
| Consistency model | Strong | Eventual |
| Transaction scope | Single node | Distributed |
| Write availability | Lower | Higher |
| Read performance | Consistent reads | Faster eventual reads |
| Schema flexibility | Rigid | Flexible |
| Use case | Financial, inventory | Social, analytics, IoT |

## When to Use Each

### Choose ACID When

```sql
-- Financial transactions: every cent must be accounted for
BEGIN;
UPDATE accounts SET balance = balance - 500 WHERE account_id = 'A';
UPDATE accounts SET balance = balance + 500 WHERE account_id = 'B';
-- If this fails, no money is lost
COMMIT;
```

- Banking and payments
- Inventory management (avoid overselling)
- Booking systems (double-booking prevention)
- Any system where data integrity is critical

### Choose BASE When

```javascript
// Social media: eventual consistency is acceptable
// A like that takes 1 second to propagate is fine
async function likePost(postId, userId) {
    await redis.incr(`post:${postId}:likes`);  // Fast, eventual
    await kafka.produce('like-events', { postId, userId });  // Async processing
}
```

- Social media feeds
- Analytics and logging
- IoT sensor data
- Content delivery networks
- Shopping carts (session data)

## Hybrid Approaches

Modern databases increasingly support both models:

| Database | Default | ACID Available |
|----------|---------|----------------|
| MongoDB | BASE | ACID (multi-document transactions since 4.0) |
| PostgreSQL | ACID | ACID |
| Cassandra | BASE | Lightweight transactions (linearizable) |
| CockroachDB | ACID (serializable) | ACID |
| DynamoDB | BASE | ACID (transactions since 2018) |

```javascript
// MongoDB multi-document ACID transaction
const session = mongoose.startSession();
session.startTransaction();

try {
    await Order.create([orderData], { session });
    await Product.updateOne(
        { _id: productId },
        { $inc: { stock: -1 } },
        { session }
    );
    await session.commitTransaction();
} catch (error) {
    await session.abortTransaction();
} finally {
    session.endSession();
}
```

## Summary

ACID provides strong consistency guarantees at the cost of availability under partition, making it essential for financial transactions and inventory systems. BASE prioritizes availability and performance with eventual consistency, suitable for social media, analytics, and IoT. Modern databases are blurring the lines: use ACID for critical data paths and BASE for high-throughput, non-critical operations, or choose a database that supports both modes for different use cases.
