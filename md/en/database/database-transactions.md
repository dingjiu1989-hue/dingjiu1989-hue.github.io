---
title: "Database Transactions Deep Dive: ACID, Isolation Levels, Savepoints"
description: "Master database transactions with a deep dive into ACID properties, isolation levels, nested transactions, savepoints, and PostgreSQL-specific transaction semantics."
date: 2026-04-03
board: database
url: https://dingjiu1989-hue.github.io/en/database/database-transactions.html
---

# Database Transactions Deep Dive: ACID, Isolation Levels, Savepoints

Database Transactions Deep Dive: ACID, Isolation Levels, Savepoints 

A transaction is a unit of work that the database executes atomically. Transactions are the bedrock of data integrity in relational databases. Understanding them deeply separates competent engineers from great ones. 

ACID in Practice 

ACID stands for Atomicity, Consistency, Isolation, Durability. Each property maps to concrete database behavior. 

**Atomicity** : All operations within a transaction succeed or none do. In PostgreSQL, atomicity is guaranteed by the write-ahead log (WAL). If the server crashes mid-transaction, the WAL replay applies only committed transactions and discards partial ones. 

BEGIN;

UPDATE accounts SET balance = balance - 100 WHERE id = 1;

UPDATE accounts SET balance = balance + 100 WHERE id = 2;

COMMIT; -- Both succeed, or neither does

**Consistency** : A transaction brings the database from one valid state to another. Constraints, triggers, and foreign keys enforce consistency rules automatically. 

ALTER TABLE accounts ADD CONSTRAINT positive_balance

CHECK (balance >= 0);

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Any transaction that would violate this constraint is rolled back

**Isolation** : Concurrent transactions should not interfere. PostgreSQL implements four isolation levels to control how much concurrency is allowed. 

**Durability** : Once `COMMIT` returns, the data is safe. PostgreSQL writes transaction commit records to the WAL and forces a `fsync()` before returning success. 

Isolation Levels 

SQL standard defines four isolation levels. PostgreSQL implements three (it does not expose the dirty-read behavior of `READ UNCOMMITTED`; it maps it to `READ COMMITTED`). 

Read Committed (Default) 

Each statement in the transaction sees a snapshot of rows committed before the statement began. Two `SELECT` statements in the same transaction can see different data. 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Session 1

BEGIN;

SELECT balance FROM accounts WHERE id = 1; -- returns 1000

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Session 2 concurrently:

UPDATE accounts SET balance = 500 WHERE id = 1; COMMIT;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Session 1 continues:

SELECT balance FROM accounts WHERE id = 1; -- now returns 500!

COMMIT;

Repeatable Read 

The transaction sees a snapshot taken when the first query or data-modification statement executes. Subsequent reads return the same data, even if concurrent transactions commit changes. 

BEGIN ISOLATION LEVEL REPEATABLE READ;

SELECT balance FROM accounts WHERE id = 1; -- returns 1000

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Session 2 updates and commits

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Session 1:

SELECT balance FROM accounts WHERE id = 1; -- still returns 1000

UPDATE accounts SET balance = balance - 100 WHERE id = 1;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- If Session 2 modified the same row, PostgreSQL raises:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- ERROR: could not serialize access due to concurrent update

COMMIT;

Serializable 

The strictest level. PostgreSQL detects serialization anomalies and enforces true serial execution behavior. Queries may fail with serialization errors that require retries. 

BEGIN ISOLATION LEVEL SERIALIZABLE;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Complex business logic with multiple rows

COMMIT;

Serializable transactions incur overhead from predicate locking. Use it only when correctness requirements truly require it (e.g., financial systems with complex cross-row invariants). 

Nested Transactions and Savepoints 

PostgreSQL does not support true nested transactions (subtransactions that can commit independently of the parent). Instead, it offers **savepoints** : 

BEGIN;

INSERT INTO orders (user_id, total) VALUES (1, 100);

SAVEPOINT order_inserted;

INSERT INTO order_items (order_id, product_id, quantity)

VALUES (currval('orders_id_seq'), 42, 1);

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Something went wrong with the item

ROLLBACK TO SAVEPOINT order_inserted;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Try a different item

INSERT INTO order_items (order_id, product_id, quantity)

VALUES (currval('orders_id_seq'), 99, 2);

COMMIT; -- Only the second order_item is kept

Savepoints let you abort part of a transaction without aborting the whole thing. They are useful in batch processing, ETL pipelines, and complex workflows where partial failures must be isolated. 

The general structure for safe savepoint use: 

BEGIN;

FOR batch IN batch_data LOOP

SAVEPOINT batch_savepoint;

BEGIN TRY

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Process batch

EXCEPTION WHEN OTHERS THEN

ROLLBACK TO batch_savepoint;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Log error, skip batch

END TRY;

END LOOP;

COMMIT;

Transaction IDs and Wraparound 

PostgreSQL assigns a 32-bit transaction ID (XID) to each transaction. With roughly 4 billion IDs available, a busy system could exhaust them. This is called **transaction ID wraparound**. 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Check for wraparound risk

SELECT datname, age(datfrozenxid) AS xid_age,

ROUND(100 * age(datfrozenxid) / 2000000000.0, 2) AS pct_to_wraparound

FROM pg_database

ORDER BY xid_age DESC;

When a table's `age` approaches 2 billion, PostgreSQL runs aggressive autovacuum. If that process falls behind, the database shuts down to prevent data loss. Monitoring XID age is an essential operational task. 

Best Practices 

  * **Keep transactions short** : Hold locks and connections for the minimum possible duration.

  * **Never wait for user input inside a transaction** : This kills concurrency.

  * **Choose the lowest isolation level** that ensures correctness. Read Committed is sufficient for most workloads.

  * **Retry on serialization failures** : Serializable transactions are expected to fail occasionally.

  * **Use`COMMIT AND CHAIN`** to avoid re-declaring isolation level on successive transactions.

  * **Monitor long-running transactions** via `pg_stat_activity`:




SELECT pid, NOW() - xact_start AS duration, state, query

FROM pg_stat_activity

WHERE state IN ('active', 'idle in transaction')

AND xact_start IS NOT NULL

ORDER BY duration DESC;

Transactions are not just a SQL feature; they are a correctness contract between your application and the database. Understanding isolation levels and their performance implications is essential for building reliable, concurrent systems.

**See also:** [Database Concurrency Control: MVCC, Locking, and Deadlocks](</en/database/database-concurrency.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Database Isolation Levels and Anomalies](</en/database/database-isolation-levels.html>).

**See also:** [Database Concurrency Control: MVCC, Locking, and Deadlocks](</en/database/database-concurrency.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>)

**See also:** [Database Concurrency Control: MVCC, Locking, and Deadlocks](</en/database/database-concurrency.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>)

**See also:** [Database Concurrency Control: MVCC, Locking, and Deadlocks](</en/database/database-concurrency.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>)

**See also:** [Database Concurrency Control: MVCC, Locking, and Deadlocks](</en/database/database-concurrency.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>)

**See also:** [Database Concurrency Control: MVCC, Locking, and Deadlocks](</en/database/database-concurrency.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>)

**See also:** [NewSQL Databases: Combining SQL with Horizontal Scaling](</en/database/new-sql-databases.html>), [Batch Operations: Bulk Insert, COPY, and Batch Size Tuning](</en/database/batch-operations.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>)

**See also:** [NewSQL Databases: Combining SQL with Horizontal Scaling](</en/database/new-sql-databases.html>), [Batch Operations: Bulk Insert, COPY, and Batch Size Tuning](</en/database/batch-operations.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>)

**See also:** [NewSQL Databases: Combining SQL with Horizontal Scaling](</en/database/new-sql-databases.html>), [Batch Operations: Bulk Insert, COPY, and Batch Size Tuning](</en/database/batch-operations.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>)

**See also:** [NewSQL Databases: Combining SQL with Horizontal Scaling](</en/database/new-sql-databases.html>), [Batch Operations: Bulk Insert, COPY, and Batch Size Tuning](</en/database/batch-operations.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>)

**See also:** [NewSQL Databases: Combining SQL with Horizontal Scaling](</en/database/new-sql-databases.html>), [Batch Operations: Bulk Insert, COPY, and Batch Size Tuning](</en/database/batch-operations.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>)

**See also:** [NewSQL Databases: Combining SQL with Horizontal Scaling](</en/database/new-sql-databases.html>), [Batch Operations: Bulk Insert, COPY, and Batch Size Tuning](</en/database/batch-operations.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>)
