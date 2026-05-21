---
title: "Database High Availability: Failover, Standby Types, Health Checks"
description: "Learn database high availability patterns: failover strategies, standby types (hot, warm, cold), health checks, automated recovery, and PostgreSQL HA setup."
date: 2026-05-14
board: database
url: https://dingjiu1989-hue.github.io/en/database/database-high-availability.html
---

# Database High Availability: Failover, Standby Types, Health Checks

Database High Availability: Failover, Standby Types, Health Checks 

High availability (HA) ensures your database remains accessible despite hardware failures, network partitions, or software crashes. This article covers failover mechanisms, standby types, health monitoring, and automated recovery. 

Availability Metrics 

Availability is measured in "nines": 

| Uptime | Downtime/Year | Classification | |--------|---------------|----------------| | 99% | 87.6 hours | Basic | | 99.9% (three nines) | 8.76 hours | Standard | | 99.99% (four nines) | 52.56 minutes | Enterprise | | 99.999% (five nines) | 5.26 minutes | Mission-critical | 

Achieving higher availability requires increasingly sophisticated (and expensive) infrastructure. 

Standby Types 

Hot Standby 

A hot standby accepts read queries while replicating from the primary. PostgreSQL's `hot_standby = on` enables this: 

## standby postgresql.conf

hot_standby = on

hot_standby_feedback = on

  * **Failover time** : Seconds (already running, just promote).

  * **Resource usage** : Full database server resources.

  * **Use case** : Production read replicas with fast failover.




Warm Standby 

A warm standby is running but does not accept connections until promoted: 

## warm standby: accept no connections

hot_standby = off

  * **Failover time** : Tens of seconds (start postmaster + recovery).

  * **Resource usage** : Moderate (receives WAL but no query processing).

  * **Use case** : Cost-sensitive environments.




Cold Standby 

A cold standby is an offline copy of the data. It must be started from scratch during failover: 

  * **Failover time** : Minutes to hours (restore from backup, start database).

  * **Resource usage** : Minimal (only storage).

  * **Use case** : Disaster recovery only.




Failover Strategies 

Manual Failover 

The operator promotes a standby and redirects applications: 

## Promote standby

pg_ctl promote -D /var/lib/postgresql/data

## Update application DNS or connection string

## This may take minutes and requires human intervention

**Pros** : Simple, operator has full control. **Cons** : Slow (minutes), error-prone under pressure. 

Automated Failover with Patroni 

Patroni is the most popular HA solution for PostgreSQL. It uses distributed consensus (etcd, Consul, or Zookeeper) to elect a new leader: 

## patroni.yml

scope: myapp-db

namespace: /service/

name: pg-node-1

consul:

host: consul.service.consul:8500

register_service: true

postgresql:

listen: 0.0.0.0:5432

connect_address: pg-node-1:5432

data_dir: /var/lib/postgresql/data

bin_dir: /usr/lib/postgresql/16/bin

authentication:

replication:

username: replicator

password: secure_password

superuser:

username: postgres

password: secure_password

parameters:

max_connections: 200

use_pg_rewind: true

use_slots: true

watchdog:

mode: required

device: /dev/watchdog

Health Checks 

Patroni performs regular health checks: 

  * **pg_isready** : Checks if PostgreSQL is accepting connections.



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Replication lag** : If lag exceeds a threshold, the standby is not eligible for promotion. 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Consensus health** : The node must be reachable to the DCS (etcd/Consul). 

## Manual health check

pg_isready -h localhost -p 5432

## localhost:5432 - accepting connections

## Check replication status

psql -c "SELECT * FROM pg_stat_replication;"

Failover Flow 

  * Patroni detects primary is down (missed health check + no DCS lock).



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Patroni holds a leader election via DCS. 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. The most advanced replica wins (most recent WAL position). 4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. The replica is promoted to primary. 5\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. The old primary, when it recovers, is reconfigured as a replica. 

Connection Draining and Routing 

During failover, in-flight transactions are lost. Applications must handle this: 

from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1))

def execute_with_retry(conn, query, params=None):

try:

with conn.cursor() as cur:

cur.execute(query, params or ())

conn.commit()

except (psycopg2.OperationalError, psycopg2.InterfaceError) as e:

## Reconnect and retry

conn = psycopg2.connect(dsn)

raise

Smart DNS (Route53, CloudDNS) 

import boto3

def failover_to_standby(region, standby_dns):

r53 = boto3.client('route53')

r53.change_resource_record_sets(

HostedZoneId='ZONE_ID',

ChangeBatch={

'Changes': [{

'Action': 'UPSERT',

'ResourceRecordSet': {

'Name': 'db.myapp.com',

'Type': 'CNAME',

'TTL': 30,

'ResourceRecords': [{'Value': standby_dns}]

}

}]

}

)

Low TTL (30 seconds) ensures fast propagation. 

PostgreSQL High Availability Stack 

A production HA setup combines: 

  * **Streaming replication** : 2-3 synchronous standbys.



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Patroni** : Automated failover and cluster management. 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **etcd/Consul** : Distributed consensus for leader election. 4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **HAProxy or PgBouncer** : Connection routing to the current primary. 5\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Watchdog** : Fencing to prevent split-brain. 

## HAProxy configuration

frontend pg_frontend

bind *:5000

default_backend pg_backend

backend pg_backend

option httpchk GET /master

server pg-node-1 pg-node-1:5432 check port 8008 inter 2s

server pg-node-2 pg-node-2:5432 check port 8008 inter 2s

server pg-node-3 pg-node-3:5432 check port 8008 inter 2s

Testing HA 

Regular failover testing is essential: 

## Test: Kill the primary

ssh pg-node-1 "systemctl stop postgresql"

## Expected:

## \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- Patroni promotes pg-node-2 within 30 seconds

## \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- HAProxy routes to pg-node-2

## \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- Applications reconnect and continue

## Verify:

psql -h haproxy -p 5000 -c "SELECT inet_server_addr();"

## Should show pg-node-2's IP

Common Pitfalls 

  * **Split-brain** : Two nodes both think they are primary. Prevented by fencing (STONITH) and watchdog.

  * **Replication lag** : A promoted standby may lose recent transactions if synchronous replication is not configured.

  * **Connection timeouts** : Application connection pools must be configured to detect and recover from failover quickly.

  * **Untested failover** : The first failover should not be a real incident. Test monthly.




High availability is not a product you buy; it is a property of your system's architecture and operations. Invest in automation, test regularly, and accept that no system is 100% available.

**See also:** [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Database Disaster Recovery: RPO, RTO, Cross-Region Replication](</en/database/database-disaster-recovery.html>).

**See also:** [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>)

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>)

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>)

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>)

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>)

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>)

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>)

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>)

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>)

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>)

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>)

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>)
