---
title: "Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR"
description: "Explore multi-master replication strategies including conflict resolution techniques, CRDTs, Galera Cluster for MySQL, and PostgreSQL BDR."
date: 2026-04-08
board: database
url: https://dingjiu1989-hue.github.io/en/database/multi-master-replication.html
---

# Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR

Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR 

Multi-master replication allows writes to multiple database nodes simultaneously. Unlike primary-replica setups, there is no single point for writes. The trade-off is complexity, particularly around conflict resolution. 

Why Multi-Master? 

The primary reasons to consider multi-master replication are: 

  * **Multi-region writes** : Users in the US and Europe both write with local latency.

  * **Zero downtime upgrades** : Any node can be taken offline without losing write availability.

  * **Read scalability with local writes** : Each node can serve both reads and writes with low latency.




Conflict Resolution Strategies 

When two nodes concurrently modify the same row, a conflict occurs. Resolution strategies vary by system: 

Last-Write-Wins (LWW) 

Each row carries a timestamp. The write with the latest timestamp wins. Simple but lossy: 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Cassandra default

UPDATE users SET email = 'new@example.com', updated_at = now() WHERE id = 1;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- The LWW with the highest timestamp wins

**Pros** : Simple, always converges. **Cons** : Loses data silently. 

Application-Mediated Conflict Resolution 

The database detects conflicts and presents them to the application for resolution. BDR (Bi-Directional Replication) for PostgreSQL supports this: 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Create a conflict handler function

CREATE OR REPLACE FUNCTION resolve_conflict()

RETURNS trigger AS $$

BEGIN

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Custom logic: keep the row with the higher version

IF NEW.version >= OLD.version THEN

RETURN NEW;

END IF;

RETURN OLD;

END;

$$ LANGUAGE plpgsql;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Apply to the replication set

SELECT bdr.conflict_handler('orders', 'resolve_conflict');

CRDT-Based Reconciliation 

Conflict-free Replicated Data Types (CRDTs) mathematically guarantee convergence without coordination. Instead of storing a scalar value, you store a data structure where concurrent operations commute or combine: 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Counter CRDT table

CREATE TABLE page_views (

page_id INTEGER PRIMARY KEY,

counter INTEGER DEFAULT 0

);

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Each replica increments independently

UPDATE page_views SET counter = counter + 1 WHERE page_id = 42;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- The final value after reconciliation: MAX of all replicas' counters (for grow-only counters)

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- or SUM (for counters implemented as PN-Counters)

More sophisticated CRDTs include: 

  * **G-Set** (grow-only set): Elements can only be added. Union merges converge.

  * **LWW-Register** : Last-write-wins register (if using wall clocks) or compare-and-swap.

  * **OR-Set** (observed-remove set): Supports both add and remove without losing concurrent adds.




Galera Cluster (MySQL / MariaDB) 

Galera Cluster implements synchronous multi-master replication for MySQL. All nodes coordinate before committing: 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- All nodes are writable

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- On each node:

CREATE TABLE users (

id INT PRIMARY KEY AUTO_INCREMENT,

email VARCHAR(255) NOT NULL

);

INSERT INTO users (email) VALUES ('alice@example.com');

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- This INSERT is certified on all nodes before returning

Galera Key Properties 

  * **Synchronous replication** : All nodes apply changes simultaneously.

  * **Certification-based** : Transactions are certified on every node before commit.

  * **Automatic node provisioning** : New nodes join via State Snapshot Transfer (SST) or Incremental State Transfer (IST).

  * **No replication lag** : All nodes are consistent at commit time.




Galera Limitations 

  * Cluster size penalty: 2-3 nodes is optimal. More nodes increase certification overhead.

  * Full table writes locks must be avoided; `SELECT ... FOR UPDATE` on uncached workloads causes deadlocks.

  * Network latency between nodes directly impacts write latency (the "slowest node" problem).

  * `REPEATABLE READ` is the default; `SERIALIZABLE` causes high conflict rates.




PostgreSQL BDR (Bi-Directional Replication) 

BDR extends PostgreSQL's logical replication for multi-master scenarios. It operates at row level with conflict resolution: 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Configure BDR group

SELECT bdr.create_node(

node_name := 'node1',

dsn := 'host=node1.example.com port=5432 dbname=appdb'

);

SELECT bdr.create_node(

node_name := 'node2',

dsn := 'host=node2.example.com port=5432 dbname=appdb'

);

SELECT bdr.create_group(

group_name := 'global_app',

nodes := ARRAY['node1', 'node2']

);

BDR supports multiple conflict resolution modes: 

  * `latest_timestamp_wins`

  * `latest_version_wins`

  * `apply_remote`

  * `apply_local`




CAP Theorem Implications 

Multi-master systems live in the CAP trade-off space: 

  * **Galera** : CP (Consistency + Partition tolerance). Sacrifices availability during network partitions because writes must certify on all nodes.

  * **Cassandra-style LWW** : AP (Availability + Partition tolerance). Sacrifices immediate consistency but always accepts writes.

  * **BDR with custom handlers** : Tunable. Configure per-table conflict strategies.




When to Avoid Multi-Master 

Multi-master replication is not the default for good reasons: 

  * **Single-region apps** : A single PostgreSQL primary with streaming replicas handles the vast majority of workloads.

  * **Apps with hot rows** : If 90% of writes target 10 rows (e.g., a counter), conflicts are guaranteed.

  * **Teams without operational maturity** : Multi-master requires monitoring replication lag, conflict rates, and node health.




Monitoring Conflicts 

Whichever system you choose, monitor conflict rates: 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- BDR conflict stats

SELECT * FROM bdr.conflict_history;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Galeria cluster status

SHOW STATUS LIKE 'wsrep_cluster_size';

SHOW STATUS LIKE 'wsrep_local_cert_failures';

A rising conflict rate indicates application-level contention that might be better solved by sharding the data model rather than relying on replication to resolve conflicts. 

Multi-master replication is a powerful but complex tool. Start with single-master and add multi-master only when your availability or latency requirements genuinely demand it.

**See also:** [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>), [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>).

**See also:** [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>), [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>)

**See also:** [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>), [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>)

**See also:** [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>), [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>)

**See also:** [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>), [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>)

**See also:** [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>), [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>)

**See also:** [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance](</en/database/database-design-patterns.html>)

**See also:** [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance](</en/database/database-design-patterns.html>)

**See also:** [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance](</en/database/database-design-patterns.html>)

**See also:** [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance](</en/database/database-design-patterns.html>)

**See also:** [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance](</en/database/database-design-patterns.html>)

**See also:** [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance](</en/database/database-design-patterns.html>)

**See also:** [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance](</en/database/database-design-patterns.html>)

**See also:** [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance](</en/database/database-design-patterns.html>)

**See also:** [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance](</en/database/database-design-patterns.html>)

**See also:** [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance](</en/database/database-design-patterns.html>)
