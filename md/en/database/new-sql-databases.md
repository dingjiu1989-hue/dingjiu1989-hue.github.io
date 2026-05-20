---
title: "NewSQL Databases: Combining SQL with Horizontal Scaling"
description: "NewSQL databases offer ACID transactions and SQL queries with horizontal scalability. Compare CockroachDB, YugabyteDB, and Spanner."
date: 2026-04-17
board: database
url: https://dingjiu1989-hue.github.io/en/database/new-sql-databases.html
---

# NewSQL Databases: Combining SQL with Horizontal Scaling

NewSQL databases combine the ACID guarantees and SQL query capabilities of traditional relational databases with the horizontal scalability of NoSQL systems. They address a fundamental limitation of traditional databases: scaling beyond a single node without sacrificing consistency.

## CockroachDB

CockroachDB is a distributed SQL database designed for cloud-native applications. It automatically replicates and distributes data across nodes, handles node failures transparently, and supports standard PostgreSQL-compatible SQL.

CockroachDB uses a consensus protocol (Raft) to maintain consistency across replicas. Each range of data is replicated to at least 3 nodes. Reads and writes go through the leaseholder node for that range, providing linearizable consistency.

Its geo-partitioning feature allows data to be stored in specific geographic locations for latency optimization and data residency compliance. A table can specify that EU customer data is stored only on EU nodes.

## YugabyteDB

YugabyteDB is an open-source distributed SQL database that supports both PostgreSQL and Cassandra-compatible APIs. It uses a document store at its core with a distributed transaction layer on top.

YugabyteDB's architecture separates compute from storage. The query layer handles SQL parsing and optimization. The storage layer handles replication and persistence. This separation allows independent scaling of compute and storage resources.

## Google Spanner

Google Spanner is the original NewSQL database, running on Google's global infrastructure. It provides external consistency (global serializability) across data centers through TrueTime, a globally synchronized clock service.

Spanner combines automatic sharding, synchronous replication, and atomic clocks for consistency. It handles automatic failover, data rebalancing, and geo-distribution transparently. The trade-off is vendor lock-in and higher cost.

## When to Use NewSQL

Use NewSQL when you need ACID transactions across multiple nodes, when your application requires standard SQL, and when you anticipate scaling beyond a single database node. NewSQL is ideal for financial systems, multi-tenant SaaS platforms, and globally distributed applications.

Avoid NewSQL for simple key-value workloads (Redis is simpler), write-heavy time series (Cassandra is more cost-effective), or when eventual consistency is acceptable. NewSQL's distributed transaction overhead adds latency compared to NoSQL alternatives.

## Operational Considerations

NewSQL databases require more operational expertise than traditional databases. Plan for cluster management, node replacement, and version upgrades. Most NewSQL databases offer managed cloud services that reduce operational burden.

**See also:** [Graph Queries in SQL: Recursive CTEs, Adjacency Lists, and WITH RECURSIVE](</en/database/graph-queries.html>), [Database Scalability](</en/database/database-scalability.html>), [SQL vs NoSQL in 2026](</en/database/sql-vs-nosql-2026.html>).

**See also:** [Graph Queries in SQL: Recursive CTEs, Adjacency Lists, and WITH RECURSIVE](</en/database/graph-queries.html>), [SQL vs NoSQL in 2026](</en/database/sql-vs-nosql-2026.html>), [Database Transactions Deep Dive: ACID, Isolation Levels, Savepoints](</en/database/database-transactions.html>)

**See also:** [Graph Queries in SQL: Recursive CTEs, Adjacency Lists, and WITH RECURSIVE](</en/database/graph-queries.html>), [SQL vs NoSQL in 2026](</en/database/sql-vs-nosql-2026.html>), [Database Transactions Deep Dive: ACID, Isolation Levels, Savepoints](</en/database/database-transactions.html>)

**See also:** [Graph Queries in SQL: Recursive CTEs, Adjacency Lists, and WITH RECURSIVE](</en/database/graph-queries.html>), [SQL vs NoSQL in 2026](</en/database/sql-vs-nosql-2026.html>), [Database Transactions Deep Dive: ACID, Isolation Levels, Savepoints](</en/database/database-transactions.html>)

**See also:** [Graph Queries in SQL: Recursive CTEs, Adjacency Lists, and WITH RECURSIVE](</en/database/graph-queries.html>), [SQL vs NoSQL in 2026](</en/database/sql-vs-nosql-2026.html>), [Database Transactions Deep Dive: ACID, Isolation Levels, Savepoints](</en/database/database-transactions.html>)

**See also:** [Graph Queries in SQL: Recursive CTEs, Adjacency Lists, and WITH RECURSIVE](</en/database/graph-queries.html>), [SQL vs NoSQL in 2026](</en/database/sql-vs-nosql-2026.html>), [Database Transactions Deep Dive: ACID, Isolation Levels, Savepoints](</en/database/database-transactions.html>)

**See also:** [Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector](</en/database/database-types-overview.html>), [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>)

**See also:** [Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector](</en/database/database-types-overview.html>), [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>)

**See also:** [Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector](</en/database/database-types-overview.html>), [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>)

**See also:** [Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector](</en/database/database-types-overview.html>), [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>)

**See also:** [Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector](</en/database/database-types-overview.html>), [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>)

**See also:** [Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector](</en/database/database-types-overview.html>), [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>)

**See also:** [Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector](</en/database/database-types-overview.html>), [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>)

**See also:** [Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector](</en/database/database-types-overview.html>), [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>)

**See also:** [Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector](</en/database/database-types-overview.html>), [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>)
