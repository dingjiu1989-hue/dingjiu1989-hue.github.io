---
title: "Database Locking: Row Locks, Table Locks, and Deadlock Prevention"
description: "Understand database locking mechanisms: shared/exclusive locks, row vs table locks, two-phase locking, and deadlock handling."
date: 2026-04-15
board: database
url: https://aidev.fit/en/database/database-locking-mechanisms.html
---

# Database Locking: Row Locks, Table Locks, and Deadlock Prevention

Locking is how databases maintain data consistency under concurrent access. Without locks, concurrent transactions could read partially-written data or overwrite each other's changes. Different databases implement locking differently, but the core concepts are universal.

## Lock Modes

Shared locks (read locks) allow multiple transactions to read the same data simultaneously. Multiple shared locks can coexist on the same resource. Shared locks prevent exclusive locks from being acquired.

Exclusive locks (write locks) prevent any other transaction from reading or writing the locked resource. Only one transaction can hold an exclusive lock. Exclusive locks block both shared and other exclusive lock requests.

Update locks are a hybrid used to prevent deadlocks during read-then-write operations. An update lock starts as shared but can be promoted to exclusive. Only one transaction can hold an update lock on a resource.

## Lock Granularity

Row locks lock individual rows. They provide maximum concurrency but require more locks for the same operation. Row-level locking is the default in modern databases like PostgreSQL and MySQL (InnoDB).

Page locks lock a group of rows on a database page. They balance concurrency and lock management overhead. Page-level locking is used by SQL Server and older MySQL storage engines. Page locks increase contention compared to row locks.

Table locks lock the entire table. They provide maximum protection but minimum concurrency. Use table locks for DDL operations, bulk data loads, and when row-level locking overhead is unacceptable.

Lock escalation: some databases automatically escalate row locks to table locks when a transaction holds many row locks on the same table. This prevents excessive lock memory usage but reduces concurrency.

## Deadlocks

A deadlock occurs when two transactions each hold locks the other needs: Transaction A locks row 1, Transaction B locks row 2, then A waits for row 2 while B waits for row 1. Neither can proceed.

Databases detect deadlocks through wait-for graph analysis. When detected, one transaction is chosen as the victim and rolled back. The victim is typically the transaction that accumulated the least work.

Prevent deadlocks: access resources in a consistent order across all transactions. Keep transactions short to minimize lock duration. Use lock timeouts to fail fast rather than waiting indefinitely. Consider snapshot isolation to eliminate many locking conflicts.

## Two-Phase Locking

Two-Phase Locking (2PL) is the protocol databases use to ensure serializability. Phase 1 (growing phase): transactions acquire locks but cannot release them. Phase 2 (shrinking phase): transactions release locks but cannot acquire new ones.

Strict 2PL releases all locks at transaction commit time. This is the most common implementation and prevents cascading aborts. If a transaction aborts, other transactions did not read its uncommitted writes.

## Monitoring Locks

Query pg_locks in PostgreSQL or performance_schema.data_locks in MySQL to see current locks. Look for transactions holding locks for extended periods. Long lock waits indicate contention. Long-running transactions are the most common cause of blocking.
