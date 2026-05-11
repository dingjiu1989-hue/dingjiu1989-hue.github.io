---
title: "Database Replication Patterns"
description: "Explore database replication patterns including leader-follower, multi-leader, peer-to-peer, and strategies for high availability and read scaling."
date: 2026-05-11
board: database
url: https://dingjiu1989-hue.github.io/en/database/database-replication.html
---

## What Is Database Replication?

Database replication is the process of copying data from one database server to another. Replication serves three primary purposes: high availability (failover if the primary fails), read scaling (distribute read queries across replicas), and disaster recovery (geographically distributed copies).

## Replication Topologies

### Leader-Follower (Single-Leader)

The most common replication pattern. One node accepts writes (leader), and one or more nodes replicate data asynchronously or synchronously (followers).

```
                                         Read Queries
                                            |
Client Writes ───> Leader ────> Follower 1 ───> Results
                          |         |
                          |    Follower 2 ───> Results
                          |
                     Follower 3 ───> Results
```

```sql
-- PostgreSQL: Configure streaming replication
-- On leader (postgresql.conf)
wal_level = replica
max_wal_senders = 5
wal_keep_size = 1024  -- MB

-- On follower (recovery.conf)
primary_conninfo = 'host=leader-ip port=5432 user=replicator'
primary_slot_name = 'follower_1'
```

```yaml
# Application connection pooling (read/write splitting)
spring:
  datasource:
    write:
      url: jdbc:postgresql://leader:5432/db
    read:
      url: jdbc:postgresql://follower:5432/db
      # Or multiple read replicas:
      # - jdbc:postgresql://follower1:5432/db
      # - jdbc:postgresql://follower2:5432/db
```

### Multi-Leader

Multiple nodes accept writes, each propagating changes to other leaders. Common in geo-distributed deployments.

```
          US East Leader <───> EU West Leader
              │                       │
              │                       │
          US East Follower        EU West Follower
```

```python
# Conflict resolution in multi-leader replication
# Last-Writer-Wins (LWW) approach
def resolve_conflict(existing, incoming):
    """Resolve by most recent timestamp."""
    if incoming.timestamp > existing.timestamp:
        return incoming
    elif incoming.timestamp < existing.timestamp:
        return existing
    else:
        # Same timestamp: merge values
        return merge_values(existing, incoming)
```

### Peer-to-Peer (Multi-Leader All-to-All)

Every node can accept reads and writes. Changes propagate to all other nodes.

```
    Node 1 <───> Node 2
       ↑            ↑
       ↓            ↓
    Node 3 <───> Node 4
```

## Replication Methods

### Statement-Based Replication

SQL statements are sent from leader to followers.

```
Leader executes: UPDATE users SET name = 'Bob' WHERE id = 1
Follower receives: UPDATE users SET name = 'Bob' WHERE id = 1
```

**Problem**: Non-deterministic functions (`NOW()`, `RANDOM()`) may produce different results on followers.

### Write-Ahead Log (WAL) Shipping

The leader's transaction log is shipped to followers, which replay it.

```bash
# PostgreSQL WAL shipping
# Followers continuously apply WAL segments
# This is the most common PostgreSQL replication method
```

### Logical Replication

A higher-level replication that streams changes by row rather than by disk block:

```sql
-- PostgreSQL logical replication
-- Publisher (leader)
CREATE PUBLICATION my_pub FOR TABLE users, orders;

-- Subscriber (follower)
CREATE SUBSCRIPTION my_sub
CONNECTION 'host=leader port=5432 dbname=mydb'
PUBLICATION my_pub;
```

## Synchronous vs Asynchronous

| Aspect | Synchronous | Asynchronous |
|--------|-------------|--------------|
| Data loss on failover | None (committed on all nodes) | Possible (unsynced writes lost) |
| Write latency | Higher (wait for all nodes) | Lower (ack immediately) |
| Availability | Lower (replica failure blocks writes) | Higher (replica failure ignored) |
| Use case | Financial systems | Most web applications |

```sql
-- PostgreSQL: Configure synchronous replication
synchronous_standby_names = 'FIRST 2 (*)'
-- Write commits only after at least 2 replicas confirm
```

## Automatic Failover

```yaml
# Patroni configuration for PostgreSQL HA
scope: mydb
namespace: /service/
name: pg_leader

consul:
  host: consul.service.consul

postgresql:
  listen: 0.0.0.0:5432
  data_dir: /data/postgresql
  bin_dir: /usr/lib/postgresql/16/bin
  parameters:
    max_connections: 200

  authentication:
    replication:
      username: replicator
      password: secure_password
    superuser:
      username: postgres
      password: secure_password

  callbacks:
    on_role_change: /scripts/notify_role_change.sh
```

## Read Replica Lag

Asynchronous replication introduces lag. Applications must handle stale reads:

```python
class DatabaseRouter:
    """Route reads to replicas with staleness awareness."""

    def __init__(self, primary, replicas):
        self.primary = primary
        self.replicas = replicas

    def get_connection(self, need_freshness=False):
        """Get a database connection for reading."""
        if need_freshness:
            # Query must see the latest write
            return self.primary

        # Round-robin through replicas
        replica = random.choice(self.replicas)
        return replica

# Usage
def get_order(order_id, user_id):
    # If user just placed this order, read from primary
    if order_just_placed(user_id):
        conn = router.get_connection(need_freshness=True)
    else:
        conn = router.get_connection()

    return conn.query("SELECT * FROM orders WHERE id = %s", [order_id])
```

## Monitoring Replication

```sql
-- PostgreSQL: Check replication status
SELECT
    application_name,
    state,
    sync_state,
    pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) AS lag_bytes,
    (EXTRACT(EPOCH FROM NOW() - replay_lag) * 1000)::bigint AS lag_ms
FROM pg_stat_replication;

-- Check last WAL receive/replay time
SELECT
    now() - pg_last_xact_replay_timestamp() AS replication_delay;
```

## Common Pitfalls

| Pitfall | Consequence | Mitigation |
|---------|-------------|------------|
| Replication lag | Stale reads | Route freshness-sensitive queries to primary |
| Auto-increment conflicts | Duplicate keys | Use UUIDs or sequence ranges in multi-leader |
| Schema drift | Replication breaks | Apply migrations to followers first, then leader |
| Network latency | Replication delay | Keep replicas in same region for sync replication |
| Cascading failures | Overloaded replicas | Add connection pooling and query limits |

## Summary

Leader-follower replication is the standard pattern for most applications, providing read scaling and failover capabilities. Use synchronous replication for zero data loss in critical systems and asynchronous replication for lower write latency. Implement automatic failover with tools like Patroni, handle read replicas with staleness-aware routing, and monitor replication lag as a key operational metric. For global deployments, consider multi-leader replication with conflict resolution strategies.
