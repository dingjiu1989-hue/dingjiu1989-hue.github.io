---
title: "Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing"
description: "Learn Change Data Capture patterns with Debezium, PostgreSQL logical replication, and stream processing integration. Real-time data pipelines without performance overhead."
date: 2026-03-30
board: database
url: https://dingjiu1989-hue.github.io/en/database/change-data-capture.html
---

# Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing

Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing 

Change Data Capture (CDC) is a pattern that captures row-level changes in a database and streams them to downstream consumers in real time. Unlike triggers or application-level dual-writes, CDC reads the database's transaction log, adding negligible overhead to production workloads. 

Why CDC? 

Traditional approaches to synchronizing databases have downsides: 

  * **Triggers** : Add per-row overhead and operate within the transaction, slowing writes.

  * **Dual-writes** : Writing to two systems (database and cache, or database and search index) from the application is non-atomic; partial failures cause drift.

  * **Batch ETL** : Hourly or daily jobs introduce latency that many systems cannot tolerate.




CDC solves these problems by making the database transaction log the source of truth and streaming changes as they occur. 

PostgreSQL Logical Replication 

PostgreSQL's built-in logical replication is the foundation for CDC. Unlike physical replication (which copies entire WAL segments and requires identical servers), logical replication streams decoded changes as row-level operations. 

Publisher Setup 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- wal_level must be logical

SHOW wal_level; -- must be 'logical'

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Create a publication

CREATE PUBLICATION cdc_pub FOR TABLE orders, order_items, payments;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Optionally filter rows

CREATE PUBLICATION cdc_pub_usa FOR TABLE orders WHERE (country = 'US');

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Specify publish operations

CREATE PUBLICATION cdc_pub_inserts FOR TABLE orders

WITH (publish = 'insert');

Subscriber Setup 

The subscriber can be another PostgreSQL database or any consumer that speaks the `pgoutput` protocol: 

CREATE SUBSCRIPTION cdc_sub

CONNECTION 'host=primary-db port=5432 dbname=proddb'

PUBLICATION cdc_pub;

Each logical replication slot tracks the WAL position, ensuring no data loss even if the consumer is offline for extended periods. 

Debezium 

Debezium is an open-source CDC platform built on Apache Kafka. It uses PostgreSQL's logical decoding plugin (`pgoutput` or `decoderbufs`) to capture changes and publishes each row change as a Kafka message. 

Debezium Connector Configuration 

{

"name": "postgres-connector",

"config": {

"connector.class": "io.debezium.connector.postgresql.PostgresConnector",

"database.hostname": "primary-db",

"database.port": "5432",

"database.user": "debezium",

"database.password": "debezium",

"database.dbname": "proddb",

"database.server.name": "my-app",

"plugin.name": "pgoutput",

"slot.name": "debezium_slot",

"table.include.list": "public.orders,public.order_items",

"transforms": "unwrap",

"transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",

"decimal.handling.mode": "string"

}

}

Each change event has a standard envelope: 

{

"op": "c",

"before": null,

"after": {

"id": 1001,

"user_id": 42,

"total": "299.99",

"status": "pending"

},

"source": {

"db": "proddb",

"table": "orders",

"lsn": 123456789,

"ts_ms": 1717000000000

}

}

Operation codes: `c` (create), `u` (update), `d` (delete), `r` (snapshot). 

Schema Evolution 

Debezium publishes schema information to a separate Kafka topic. When your database schema evolves (column added, type changed), the schema registry tracks versions. Consumers can adapt dynamically. 

Stream Processing Integration 

CDC naturally feeds into stream processors like Apache Flink, Kafka Streams, or ksqlDB: 

// Kafka Streams CDC consumer example

KStream orders = builder.stream(

"my-app.public.orders",

Consumed.with(Serdes.String(), orderSerde)

);

orders

.filter((key, order) -> order.status.equals("paid"))

.mapValues(order -> {

order.status = "processing";

return order;

})

.to("my-app.public.orders-processing",

Produced.with(Serdes.String(), orderSerde));

Materialized Cache 

CDC can keep a Redis cache or Elasticsearch index in sync with the database: 

PostgreSQL → Debezium → Kafka → Kafka Connect (Elasticsearch Sink) → Elasticsearch

This architecture eliminates application-level cache-warming code. The cache is always consistent (within the replication lag, typically milliseconds). 

Logical Replication Slots 

Replication slots are the backbone of PostgreSQL CDC. They retain WAL segments until the consumer acknowledges receipt. Monitoring slot state is critical: 

SELECT slot_name, database, active, restart_lsn,

pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)) AS wal_retained

FROM pg_replication_slots;

A stalled consumer causes WAL accumulation, potentially filling disk. Set up alerts on slot lag. 

CDC vs Triggers 

| Aspect | CDC (Logical Replication) | Triggers | |--------|--------------------------|----------| | Overhead | Minimal (WAL reading) | Per-row function execution | | Coupling | Asynchronous | Same transaction | | External consumers | Native via Kafka/Flink | Requires custom solution | | Schema changes | Managed via slot versioning | Manual trigger updates | | Backfill | Snapshot phase included | Requires separate mechanism | 

Anti-Patterns 

  * **Writing CDC events back to the same database** : Creates infinite loops or logical confusion.



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Using CDC as a general-purpose event bus** : CDC captures row changes, not domain events. Use an explicit event store for domain events. 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Ignoring initial snapshots** : Debezium takes a consistent snapshot before streaming changes. Large tables may require tuning of snapshot chunk sizes and lock timeouts. 

CDC is the most robust approach for keeping secondary systems synchronized with a primary database. Combined with Kafka, it enables event-driven architectures where the database is the source of truth and every change is an event.

**See also:** [Change Data Capture: Tracking Database Changes in Real-Time](</en/database/database-change-tracking-cdc.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>), [Foreign Key Constraints: Referential Integrity in Practice](</en/database/database-foreign-key-constraints.html>).

**See also:** [Change Data Capture: Tracking Database Changes in Real-Time](</en/database/database-change-tracking-cdc.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>)

**See also:** [Change Data Capture: Tracking Database Changes in Real-Time](</en/database/database-change-tracking-cdc.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>)

**See also:** [Change Data Capture: Tracking Database Changes in Real-Time](</en/database/database-change-tracking-cdc.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>)

**See also:** [Change Data Capture: Tracking Database Changes in Real-Time](</en/database/database-change-tracking-cdc.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>)

**See also:** [Change Data Capture: Tracking Database Changes in Real-Time](</en/database/database-change-tracking-cdc.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Slow Query Troubleshooting: Identification, Profiling, and Optimization](</en/database/database-slow-query-fix.html>), [Database Views: Simple, Materialized, and Updateable Views](</en/database/database-views.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Slow Query Troubleshooting: Identification, Profiling, and Optimization](</en/database/database-slow-query-fix.html>), [Database Views: Simple, Materialized, and Updateable Views](</en/database/database-views.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Slow Query Troubleshooting: Identification, Profiling, and Optimization](</en/database/database-slow-query-fix.html>), [Database Views: Simple, Materialized, and Updateable Views](</en/database/database-views.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Slow Query Troubleshooting: Identification, Profiling, and Optimization](</en/database/database-slow-query-fix.html>), [Database Views: Simple, Materialized, and Updateable Views](</en/database/database-views.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Slow Query Troubleshooting: Identification, Profiling, and Optimization](</en/database/database-slow-query-fix.html>), [Database Views: Simple, Materialized, and Updateable Views](</en/database/database-views.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Slow Query Troubleshooting: Identification, Profiling, and Optimization](</en/database/database-slow-query-fix.html>), [Database Views: Simple, Materialized, and Updateable Views](</en/database/database-views.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Slow Query Troubleshooting: Identification, Profiling, and Optimization](</en/database/database-slow-query-fix.html>), [Database Views: Simple, Materialized, and Updateable Views](</en/database/database-views.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Slow Query Troubleshooting: Identification, Profiling, and Optimization](</en/database/database-slow-query-fix.html>), [Database Views: Simple, Materialized, and Updateable Views](</en/database/database-views.html>)
