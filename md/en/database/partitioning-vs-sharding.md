---
title: "Partitioning vs Sharding"
description: "Comparing database partitioning and sharding: differences, use cases, and implementation approaches."
date: 2026-04-12
board: database
url: https://dingjiu1989-hue.github.io/en/database/partitioning-vs-sharding.html
---

# Partitioning vs Sharding

Partitioning vs Sharding 

Partitioning splits a table within a single database. Sharding splits data across multiple database servers. 

Table Partitioning 

Divide a large table into smaller physical pieces within one database: 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Range partitioning

CREATE TABLE orders (

id BIGSERIAL, order_date DATE, total DECIMAL(10,2)

) PARTITION BY RANGE (order_date);

CREATE TABLE orders_2026_01 PARTITION OF orders

FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- List partitioning

CREATE TABLE events (

id BIGSERIAL, event_type TEXT

) PARTITION BY LIST (event_type);

CREATE TABLE events_pageview PARTITION OF events

FOR VALUES IN ('pageview');

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Hash partitioning

CREATE TABLE sessions (

session_id UUID, user_id INT

) PARTITION BY HASH (session_id);

CREATE TABLE sessions_0 PARTITION OF sessions

FOR VALUES WITH (MODULUS 4, REMAINDER 0);

Partitioning benefits: partition pruning (skip irrelevant partitions), faster maintenance, efficient bulk deletes. 

Database Sharding 

Distribute data across multiple database servers: 

class ShardRouter:

def **init**(self, shards):

self.shards = shards

def get_shard(self, key):

shard_id = hash(key) % len(self.shards)

return self.shards[shard_id]

Sharding benefits: horizontal scalability for writes, distributes load across servers. 

Key Differences 

| Aspect | Partitioning | Sharding | |--------|-------------|----------| | Scope | Within one DB | Across servers | | Complexity | Low | High | | Cross-partition queries | Possible | Difficult | | Cross-shard joins | Easy | Very hard | | Scaling | Limited | Near-unlimited | 

When to Use 

  * Partitioning: Tables > 100GB, time-series data, easy data lifecycle management

  * Sharding: Write throughput exceeds single server, dataset too large for one server




Conclusion 

Start with partitioning before considering sharding. Partitioning solves many problems with less complexity. Only shard when a single database is insufficient, and use tools like Vitess or Citus to manage the complexity.

**See also:** [SQL vs NoSQL in 2026](</en/database/sql-vs-nosql-2026.html>), [NoSQL Databases Guide](</en/database/nosql-guide.html>), [Database Triggers: Use Cases, Performance Costs, and Alternatives](</en/database/triggers-patterns.html>).

**See also:** [Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector](</en/database/database-types-overview.html>), [Database Triggers: Use Cases, Performance Costs, and Alternatives](</en/database/triggers-patterns.html>), [NoSQL Databases Guide](</en/database/nosql-guide.html>)

**See also:** [Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector](</en/database/database-types-overview.html>), [Database Triggers: Use Cases, Performance Costs, and Alternatives](</en/database/triggers-patterns.html>), [NoSQL Databases Guide](</en/database/nosql-guide.html>)

**See also:** [Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector](</en/database/database-types-overview.html>), [Database Triggers: Use Cases, Performance Costs, and Alternatives](</en/database/triggers-patterns.html>), [NoSQL Databases Guide](</en/database/nosql-guide.html>)

**See also:** [Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector](</en/database/database-types-overview.html>), [Database Triggers: Use Cases, Performance Costs, and Alternatives](</en/database/triggers-patterns.html>), [NoSQL Databases Guide](</en/database/nosql-guide.html>)

**See also:** [Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector](</en/database/database-types-overview.html>), [Database Triggers: Use Cases, Performance Costs, and Alternatives](</en/database/triggers-patterns.html>), [NoSQL Databases Guide](</en/database/nosql-guide.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Materialized Views](</en/database/materialized-views.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Materialized Views](</en/database/materialized-views.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Materialized Views](</en/database/materialized-views.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Materialized Views](</en/database/materialized-views.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Materialized Views](</en/database/materialized-views.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Materialized Views](</en/database/materialized-views.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Materialized Views](</en/database/materialized-views.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Materialized Views](</en/database/materialized-views.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Materialized Views](</en/database/materialized-views.html>)
