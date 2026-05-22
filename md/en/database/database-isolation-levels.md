---
title: "Database Isolation Levels and Anomalies"
description: "Learn SQL isolation levels: read uncommitted, read committed, repeatable read, and serializable, and the anomalies they prevent."
date: 2026-05-12
board: database
url: https://aidev.fit/en/database/database-isolation-levels.html
---

# Database Isolation Levels and Anomalies

Isolation levels define how transaction concurrency is managed in a database. Higher isolation levels prevent more anomalies but reduce concurrency. Lower isolation levels increase performance at the cost of data consistency.

## Read Uncommitted

Read uncommitted is the lowest isolation level. A transaction can read data written by another uncommitted transaction. This exposes dirty reads—reading data that may be rolled back.

This level is rarely used in production. It is appropriate only when reading approximate data where precision does not matter, such as rough count queries.

## Read Committed

Read committed prevents dirty reads. A transaction only sees data that was committed before the statement began. This is the default isolation level in PostgreSQL, SQL Server, and Oracle.

Read committed does not prevent non-repeatable reads. If a transaction reads the same row twice, it may see different values if another transaction committed an update between the reads. This level also does not prevent phantom reads.

## Repeatable Read

Repeatable read ensures that if a transaction reads a row multiple times, it sees the same data. The database locks read rows or uses multi-version concurrency control to provide consistent snapshots.

Repeatable read is the default in MySQL/InnoDB. It prevents dirty reads and non-repeatable reads but may allow phantom reads—new rows inserted by other transactions appearing in subsequent range queries.

## Serializable

Serializable is the highest isolation level. Transactions execute as if they ran sequentially, one after another. No anomalies are possible. Serializable is the default isolation level in CockroachDB and YugabyteDB.

Serializable achieves this through either pessimistic locking (transactions block) or optimistic concurrency control (transactions abort and retry on conflicts). The trade-off is throughput—serializable isolation reduces concurrent transaction throughput.

## Common Anomalies

Dirty read: reading uncommitted data that may be rolled back. Non-repeatable read: reading the same row twice and getting different values. Phantom read: a range query returns different rows when re-executed. Lost update: two transactions read the same value, modify it independently, and the second overwrites the first. Write skew: two transactions read overlapping data and make conflicting writes based on stale reads.

## Choosing an Isolation Level

Use read committed for most applications—good balance of correctness and performance. Use repeatable read when reports or calculations require consistent snapshots. Use serializable for financial transactions and inventory management where correctness is critical. Use read uncommitted only for approximate aggregate queries.
