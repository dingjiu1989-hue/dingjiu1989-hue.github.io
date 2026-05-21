---
title: "NoSQL Databases Guide"
description: "A guide to NoSQL database types: document, key-value, wide-column, graph, and time-series with use cases."
date: 2026-04-10
board: database
url: https://dingjiu1989-hue.github.io/en/database/nosql-guide.html
---

# NoSQL Databases Guide

NoSQL Database Types 

NoSQL databases are non-relational stores designed for specific data models. Four major types exist. 

Document Databases (MongoDB) 

Store data as JSON-like documents. Flexible schema, nested data: 

db.users.insertOne({

name: "Alice",

email: "alice@example.com",

addresses: [{ city: "San Francisco" }]

});

Best for: flexible schemas, embedded data, rapid prototyping. 

Key-Value Stores (Redis, DynamoDB) 

Simple key-value pairs for fast lookups: 

cache.set("user:123", json.dumps(user_data))

user = json.loads(cache.get("user:123"))

Best for: caching, session storage, simple lookups. 

Wide-Column Stores (Cassandra, Bigtable) 

Column-oriented with flexible schema per row key: 

CREATE TABLE users (user_id UUID PRIMARY KEY, name TEXT, email TEXT);

Best for: time-series, write-heavy workloads, high scalability. 

Graph Databases (Neo4j) 

Nodes and edges representing entities and relationships: 

MATCH (alice:Person)-[:FOLLOWS]->(friend)-[:PURCHASED]->(product)

RETURN product.name

Best for: social networks, recommendations, fraud detection. 

Choosing a NoSQL Database 

| Type | When to Use | Avoid For | |------|-------------|-----------| | Document | Flexible schemas | Complex joins | | Key-Value | Simple lookups | Multi-key queries | | Wide-Column | High-scale writes | Ad-hoc queries | | Graph | Connected data | Simple CRUD | 

Conclusion 

Match the NoSQL type to your data model. Document for nested data, key-value for caching, wide-column for scale, graph for relationships. Consider using multiple databases for different workloads.

**See also:** [Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector](</en/database/database-types-overview.html>), [SQL vs NoSQL in 2026](</en/database/sql-vs-nosql-2026.html>), [Couchbase Guide: N1QL, Document Model, Clustering, and Caching](</en/database/couchbase-guide.html>).

**See also:** [Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector](</en/database/database-types-overview.html>), [SQL vs NoSQL in 2026](</en/database/sql-vs-nosql-2026.html>), [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>)

**See also:** [Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector](</en/database/database-types-overview.html>), [SQL vs NoSQL in 2026](</en/database/sql-vs-nosql-2026.html>), [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>)

**See also:** [Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector](</en/database/database-types-overview.html>), [SQL vs NoSQL in 2026](</en/database/sql-vs-nosql-2026.html>), [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>)

**See also:** [Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector](</en/database/database-types-overview.html>), [SQL vs NoSQL in 2026](</en/database/sql-vs-nosql-2026.html>), [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>)

**See also:** [Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector](</en/database/database-types-overview.html>), [SQL vs NoSQL in 2026](</en/database/sql-vs-nosql-2026.html>), [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>)

**See also:** [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>), [Graph Queries in SQL: Recursive CTEs, Adjacency Lists, and WITH RECURSIVE](</en/database/graph-queries.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>)

**See also:** [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>), [Graph Queries in SQL: Recursive CTEs, Adjacency Lists, and WITH RECURSIVE](</en/database/graph-queries.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>)

**See also:** [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>), [Graph Queries in SQL: Recursive CTEs, Adjacency Lists, and WITH RECURSIVE](</en/database/graph-queries.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>)

**See also:** [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>), [Graph Queries in SQL: Recursive CTEs, Adjacency Lists, and WITH RECURSIVE](</en/database/graph-queries.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>)

**See also:** [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>), [Graph Queries in SQL: Recursive CTEs, Adjacency Lists, and WITH RECURSIVE](</en/database/graph-queries.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>)

**See also:** [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>), [Graph Queries in SQL: Recursive CTEs, Adjacency Lists, and WITH RECURSIVE](</en/database/graph-queries.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>)

**See also:** [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>), [Graph Queries in SQL: Recursive CTEs, Adjacency Lists, and WITH RECURSIVE](</en/database/graph-queries.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>)

**See also:** [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>), [Graph Queries in SQL: Recursive CTEs, Adjacency Lists, and WITH RECURSIVE](</en/database/graph-queries.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>)

**See also:** [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>), [Graph Queries in SQL: Recursive CTEs, Adjacency Lists, and WITH RECURSIVE](</en/database/graph-queries.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>)

**See also:** [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>), [Graph Queries in SQL: Recursive CTEs, Adjacency Lists, and WITH RECURSIVE](</en/database/graph-queries.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>)

**See also:** [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>), [Graph Queries in SQL: Recursive CTEs, Adjacency Lists, and WITH RECURSIVE](</en/database/graph-queries.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>)

**See also:** [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>), [Graph Queries in SQL: Recursive CTEs, Adjacency Lists, and WITH RECURSIVE](</en/database/graph-queries.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>)

**See also:** [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>), [Graph Queries in SQL: Recursive CTEs, Adjacency Lists, and WITH RECURSIVE](</en/database/graph-queries.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>)
