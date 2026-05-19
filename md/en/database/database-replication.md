---
title: "Database Replication Patterns"
description: "Explore database replication patterns including leader-follower, multi-leader, peer-to-peer, and strategies for high availability and read scaling."
date: 2025-12-23
board: database
url: https://dingjiu1989-hue.github.io/en/database/database-replication.html
---

# Database Replication Patterns

Replication Fundamentals 

Database replication copies data from one server to another for redundancy, read scaling, and disaster recovery. 

Synchronous Replication 

The primary waits for replicas to acknowledge writes: 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- PostgreSQL synchronous replication

synchronous_commit = on

synchronous_standby_names = '2 (standby1, standby2, standby3)'

SELECT application_name, state, sync_state, sync_priority

FROM pg_stat_replication;

Synchronous replication guarantees no data loss but increases latency. 

Asynchronous Replication 

The primary does not wait for replicas: 

def check_replication_lag():

cur.execute("""

SELECT client_addr, application_name,

pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) AS lag_bytes,

EXTRACT(EPOCH FROM (now() - pg_last_xact_replay_timestamp())) AS lag_seconds

FROM pg_stat_replication;

""")

for row in cur.fetchall():

if row[3] > 60:

alert(f"Replication lag critical on {row[1]}")

Conflict Resolution 

Multi-primary replication requires conflict resolution: 

class ConflictResolver:

strategies = {

"last_write_wins": lambda a, b: a if a["timestamp"] > b["timestamp"] else b,

"majority_wins": lambda versions: Counter(versions).most_common(1)[0][0]

}

Replication Topologies 

| Topology | Pros | Cons | |----------|------|------| | Primary-replica | Simple | Single point of failure | | Multi-primary | HA writes | Conflict resolution needed | | Cascading | Reduced primary load | Increased lag | 

Conclusion 

Choose synchronous for zero data loss, asynchronous for performance. Monitor replication lag closely. Test failover procedures regularly.

**See also:** [Database Backup and Recovery Strategies](</en/database/database-backup-strategies.html>), [Database Migration Tools and Strategies](</en/database/database-migration.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>).

**See also:** [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>), [Database Testing Strategies for Developers](</en/database/database-testing.html>), [Data Modeling Best Practices](</en/database/data-modeling.html>)

**See also:** [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>), [Database Testing Strategies for Developers](</en/database/database-testing.html>), [Data Modeling Best Practices](</en/database/data-modeling.html>)

**See also:** [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>), [Database Testing Strategies for Developers](</en/database/database-testing.html>), [Data Modeling Best Practices](</en/database/data-modeling.html>)

**See also:** [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>), [Database Testing Strategies for Developers](</en/database/database-testing.html>), [Data Modeling Best Practices](</en/database/data-modeling.html>)

**See also:** [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>), [Database Testing Strategies for Developers](</en/database/database-testing.html>), [Data Modeling Best Practices](</en/database/data-modeling.html>)

**See also:** [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Database Horizontal Scaling Strategies](</en/database/database-horizontal-scaling.html>)

**See also:** [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Database Horizontal Scaling Strategies](</en/database/database-horizontal-scaling.html>)

**See also:** [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Database Horizontal Scaling Strategies](</en/database/database-horizontal-scaling.html>)
