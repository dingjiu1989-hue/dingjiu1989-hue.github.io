---
title: "Read Replicas: Scaling Reads, Replication Lag, and Failover"
description: "Learn how to scale database reads with read replicas. Understand replication lag, load balancing strategies, failover, and best practices for PostgreSQL and MySQL."
date: 2026-04-08
board: database
url: https://aidev.fit/en/database/read-replicas.html
---

# Read Replicas: Scaling Reads, Replication Lag, and Failover

Read Replicas: Scaling Reads, Replication Lag, and Failover 

Read replicas are copies of your primary database that serve read queries. They are the most common and cost-effective way to scale database read throughput. This article covers setup, load balancing, lag monitoring, and failover strategies. 

How Read Replicas Work 

The primary database streams changes to replicas via the write-ahead log (WAL). In PostgreSQL, this is called streaming replication. The replica continuously applies WAL records to stay current. 

PostgreSQL Streaming Replication Setup 

On the primary: 

## postgresql.conf

wal_level = replica

max_wal_senders = 5

wal_keep_size = 1024

Create a replication user: 

CREATE ROLE replicator WITH LOGIN REPLICATION PASSWORD 'secure_password';

Allow replication in `pg_hba.conf`: 

host replication replicator replica-host/32 md5

On the replica: 

pg_basebackup -h primary-host -D /var/lib/postgresql/data \

-U replicator -P -v --wal-method=stream

Create a `standby.signal` file and start PostgreSQL. The replica streams continuously. 

MySQL Replica Setup 

## my.cnf on primary

server_id = 1

log_bin = /var/log/mysql/mysql-bin.log

binlog_format = ROW

CREATE USER 'replicator'@'%' IDENTIFIED BY 'secure_password';

GRANT REPLICATION SLAVE ON _._ TO 'replicator'@'%';

On the replica: 

CHANGE MASTER TO

MASTER_HOST='primary-host',

MASTER_USER='replicator',

MASTER_PASSWORD='secure_password',

MASTER_LOG_FILE='mysql-bin.000001',

MASTER_LOG_POS=0;

START SLAVE;

SHOW SLAVE STATUS\G;

Load Balancing Strategies 

Application-level read/write splitting is the most common pattern: 

import psycopg2

class DatabaseRouter:

def **init**(self, primary_dsn, replica_dsns):

self.primary = psycopg2.connect(primary_dsn)

self.replicas = [psycopg2.connect(dsn) for dsn in replica_dsns]

self.round_robin = 0

def get_connection(self, read_only=False):

if read_only and self.replicas:

conn = self.replicas[self.round_robin % len(self.replicas)]

self.round_robin += 1

return conn

return self.primary

def execute_read(self, query, params=None):

conn = self.get_connection(read_only=True)

with conn.cursor() as cur:

cur.execute(query, params or ())

return cur.fetchall()

def execute_write(self, query, params=None):

conn = self.get_connection(read_only=False)

with conn.cursor() as cur:

cur.execute(query, params or ())

conn.commit()

A **proxy layer** like PgBouncer, ProxySQL, or HAProxy handles routing transparently: 

## ProxySQL query rules

mysql_query_rules:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- rule_id: 1

active: 1

match: "^SELECT .*"

destination_hostgroup: 1 # replicas

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- rule_id: 2

active: 1

match: "^(INSERT|UPDATE|DELETE|CREATE|DROP|ALTER) .*"

destination_hostgroup: 0 # primary

Replication Lag 

Replication lag is the time between a commit on the primary and its visibility on a replica. Causes include: 

  * Large transactions on the primary that must be applied in full on replicas.

  * Replica hardware that is slower than the primary.

  * Network latency between primary and replica.

  * Long-running queries on the replica competing for I/O.




Monitoring Lag 

PostgreSQL offers precise lag metrics: 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- On the replica

SELECT pg_last_wal_receive_lsn(),

pg_last_wal_replay_lsn(),

pg_wal_lsn_diff(pg_last_wal_receive_lsn(),

pg_last_wal_replay_lsn()) AS replay_lag_bytes;

In MySQL: 

SHOW SLAVE STATUS\G

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Focus on: Seconds_Behind_Master, Relay_Log_Space

Set up alerts. A lag of more than a few seconds (or minutes for analytics workloads) indicates a problem. 

Handling Stale Reads 

Applications that route reads of recently written data back to the primary avoid inconsistent behavior. One pattern is to mark rows with a timestamp and route queries for recent rows accordingly: 

def get_order(order_id):

## Orders updated within the last 30 seconds route to primary

order = router.execute_read(

"SELECT created_at FROM orders WHERE id = %s", (order_id,)

)

if order and (datetime.utcnow() - order[0]) < timedelta(seconds=30):

conn = router.get_connection(read_only=False)

## Query primary

else:

conn = router.get_connection(read_only=True)

Failover Strategies 

When the primary fails, one replica must become the new primary: 

PostgreSQL 

## Promote a replica to primary

pg_ctl promote -D /var/lib/postgresql/data

Or via `pg_rewind` for a clean re-sync: 

## After promotion, rewind old primary to follow new primary

pg_rewind --target-pgdata=/var/lib/postgresql/data \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--source-server='host=new-primary-db ...'

Managed Failover 

Tools like Patroni automate failover: 

## patroni.yml

scope: myapp

consul:

host: consul.service.consul:8500

postgresql:

use_pg_rewind: true

use_slots: true

parameters:

max_connections: 200

Patroni uses a distributed consensus store (etcd, Consul, Zookeeper) to elect a new leader when the current leader fails. The election typically completes in under 30 seconds. 

Best Practices 

  * **Use at least two replicas** for redundancy.

  * **Test failover** regularly in staging environments.

  * **Align replica hardware** to the primary to avoid replay stalls.

  * **Monitor replication slots** to prevent WAL accumulation on the primary.

  * **Use`hot_standby_feedback`** in PostgreSQL to prevent query cancellations on replicas due to vacuum conflicts.

  * **Consider cascading replication** for multi-region setups: primary in us-east-1 streams to a regional replica in us-west-2, which then feeds application replicas in the same region.




Read replicas are a proven, low-risk approach to scaling reads. Combined with proper monitoring and automated failover, they form the foundation of a highly available database architecture.

**See also:** [Database Horizontal Scaling Strategies](</en/database/database-horizontal-scaling.html>), [Database Scalability](</en/database/database-scalability.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>).

**See also:** [Database Horizontal Scaling Strategies](</en/database/database-horizontal-scaling.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>)

**See also:** [Database Horizontal Scaling Strategies](</en/database/database-horizontal-scaling.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>)

**See also:** [Database Horizontal Scaling Strategies](</en/database/database-horizontal-scaling.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>)

**See also:** [Database Horizontal Scaling Strategies](</en/database/database-horizontal-scaling.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>)

**See also:** [Database Horizontal Scaling Strategies](</en/database/database-horizontal-scaling.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>)

**See also:** [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>)

**See also:** [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>)

**See also:** [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>)

**See also:** [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>)

**See also:** [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>)

**See also:** [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>)

**See also:** [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>)

**See also:** [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>)

**See also:** [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>)

**See also:** [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>)

**See also:** [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>)

**See also:** [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>)

**See also:** [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>)

**See also:** [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>)

**See also:** [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>)

**See also:** [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>)
