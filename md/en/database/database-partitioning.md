---
title: "Database Table Partitioning: Range, List, Hash"
description: "Explore PostgreSQL table partitioning methods including range, list, and hash. Learn partition pruning, maintenance strategies, and performance implications."
date: 2026-04-03
board: database
url: https://dingjiu1989-hue.github.io/en/database/database-partitioning.html
---

# Database Table Partitioning: Range, List, Hash

Database Table Partitioning: Range, List, Hash 

Partitioning splits a large logical table into smaller physical pieces called partitions. Each partition holds a subset of rows based on a partition key. PostgreSQL has supported declarative partitioning since version 10, with major improvements in subsequent releases. 

Why Partition? 

Tables exceeding hundreds of gigabytes benefit from partitioning for several reasons: 

  * **Query performance** : The query planner can skip irrelevant partitions (partition pruning), dramatically reducing the amount of data scanned.

  * **Maintenance speed** : Operations like `VACUUM`, `REINDEX`, and `CLUSTER` can target individual partitions instead of the entire table.

  * **Bulk deletes** : Dropping an entire partition is far faster than `DELETE FROM large_table WHERE ...` because it bypasses the need to vacuum dead tuples.

  * **Archival** : Older partitions can be detached and moved to cheaper storage without affecting access to recent data.




Partitioning Methods 

PostgreSQL supports three built-in partitioning methods: range, list, and hash. 

Range Partitioning 

Range partitioning divides data by contiguous ranges of the partition key. It is ideal for time-series data, log tables, and date-range datasets. 

CREATE TABLE orders (

id BIGSERIAL,

order_date DATE NOT NULL,

customer_id INTEGER,

total NUMERIC(10,2)

) PARTITION BY RANGE (order_date);

CREATE TABLE orders_2025_q1 PARTITION OF orders

FOR VALUES FROM ('2025-01-01') TO ('2025-04-01');

CREATE TABLE orders_2025_q2 PARTITION OF orders

FOR VALUES FROM ('2025-04-01') TO ('2025-07-01');

CREATE TABLE orders_2025_q3 PARTITION OF orders

FOR VALUES FROM ('2025-07-01') TO ('2025-10-01');

The planner prunes partitions when the query includes a filter on `order_date`: 

EXPLAIN SELECT * FROM orders WHERE order_date = '2025-05-15';

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Only scans orders_2025_q2

List Partitioning 

List partitioning assigns rows to partitions based on a discrete set of values. This works well for categorical data such as region, status, or department. 

CREATE TABLE events (

id BIGSERIAL,

event_type TEXT NOT NULL,

payload JSONB,

created_at TIMESTAMPTZ DEFAULT NOW()

) PARTITION BY LIST (event_type);

CREATE TABLE events_pageview PARTITION OF events

FOR VALUES IN ('pageview');

CREATE TABLE events_click PARTITION OF events

FOR VALUES IN ('click', 'dblclick');

CREATE TABLE events_custom PARTITION OF events

FOR VALUES IN ('custom');

Queries filtering on `event_type` prune to the matching partition: 

EXPLAIN SELECT * FROM events WHERE event_type = 'click';

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Only scans events_click

Hash Partitioning 

Hash partitioning distributes rows evenly across a fixed number of partitions using a hash function on the partition key. It is useful when there is no natural partitioning column and you want uniform data distribution for parallel I/O. 

CREATE TABLE sessions (

session_id UUID NOT NULL,

user_id INTEGER,

payload JSONB,

started_at TIMESTAMPTZ

) PARTITION BY HASH (session_id);

CREATE TABLE sessions_0 PARTITION OF sessions

FOR VALUES WITH (MODULUS 4, REMAINDER 0);

CREATE TABLE sessions_1 PARTITION OF sessions

FOR VALUES WITH (MODULUS 4, REMAINDER 1);

CREATE TABLE sessions_2 PARTITION OF sessions

FOR VALUES WITH (MODULUS 4, REMAINDER 2);

CREATE TABLE sessions_3 PARTITION OF sessions

FOR VALUES WITH (MODULUS 4, REMAINDER 3);

Hash partitioning ensures roughly equal row counts across partitions. It does not support partition pruning on range queries, but it does prune when the partition key is filtered by equality. 

Partition Pruning 

Partition pruning is the query planner's ability to skip partitions that cannot contain matching rows. This optimization applies at execution time and, since PostgreSQL 11, also at plan time. 

EXPLAIN (ANALYZE, BUFFERS)

SELECT * FROM orders WHERE order_date = '2025-06-20';

The plan should show only one partition being scanned. Without pruning, a query scans every partition in sequence. 

Sub-partitioning 

Partitions can themselves be partitioned, creating a hierarchical design: 

CREATE TABLE logs (

id BIGSERIAL,

severity TEXT,

logged_at TIMESTAMPTZ NOT NULL,

message TEXT

) PARTITION BY RANGE (logged_at);

CREATE TABLE logs_2025 PARTITION OF logs

FOR VALUES FROM ('2025-01-01') TO ('2026-01-01')

PARTITION BY LIST (severity);

CREATE TABLE logs_2025_error PARTITION OF logs_2025

FOR VALUES IN ('ERROR', 'FATAL');

CREATE TABLE logs_2025_info PARTITION OF logs_2025

FOR VALUES IN ('INFO', 'DEBUG');

Maintenance 

Managing partitions over time is a routine task. A typical monthly maintenance workflow includes: 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Detach an old partition for archival

ALTER TABLE orders DETACH PARTITION orders_2025_q1;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Attach a new partition

CREATE TABLE orders_2025_q4 PARTITION OF orders

FOR VALUES FROM ('2025-10-01') TO ('2026-01-01');

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Reindex a specific partition

REINDEX INDEX orders_2025_q2_total_idx;

An automated job (often via `pg_cron` or a scheduled task) handles partition rotation. 

Common Pitfalls 

  * **Primary keys must include the partition key** unless a globally unique index (via constraint exclusion) is used.

  * **Foreign keys cannot reference a partitioned table directly** unless using PostgreSQL 12+ with proper setup.

  * **Row triggers on the parent table** can have unexpected behavior; apply triggers to partitions instead.

  * **Too many partitions** degrade planner performance and increase memory usage. Aim for 50-500 partitions for most workloads.




Partitioning is a powerful technique when applied deliberately. Measure your workload patterns, choose the right method, and automate partition lifecycle management to keep your database performing predictably as it grows.

**See also:** [Database Views: Simple, Materialized, and Updateable Views](</en/database/database-views.html>), [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>), [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>).

**See also:** [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>), [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>), [Database Views: Simple, Materialized, and Updateable Views](</en/database/database-views.html>)

**See also:** [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>), [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>), [Database Views: Simple, Materialized, and Updateable Views](</en/database/database-views.html>)

**See also:** [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>), [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>), [Database Views: Simple, Materialized, and Updateable Views](</en/database/database-views.html>)

**See also:** [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>), [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>), [Database Views: Simple, Materialized, and Updateable Views](</en/database/database-views.html>)

**See also:** [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>), [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>), [Database Views: Simple, Materialized, and Updateable Views](</en/database/database-views.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>)
