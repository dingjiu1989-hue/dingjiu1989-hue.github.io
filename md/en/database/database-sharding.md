---
title: "Database Sharding: Strategies and Trade-offs"
description: "Explore key-based, range-based, and directory-based sharding strategies with rebalancing challenges and tools like Vitess and Citus."
date: 2026-05-12
board: database
url: https://dingjiu1989-hue.github.io/en/database/database-sharding.html
---

Database sharding is the practice of horizontally partitioning a database across multiple servers. Each shard holds a subset of the data, and together they form the complete dataset. Sharding is essential for applications that outgrow a single database instance. This article covers sharding strategies, rebalancing challenges, and available tools.

## Why Shard?

A single database instance has limits. CPU, memory, disk I/O, and network bandwidth all cap out eventually. Before resorting to sharding, consider these alternatives:

- **Read replicas**: Offload read traffic to replicas. Effective for read-heavy workloads but does not help with write scaling.
- **Vertical scaling**: Upgrade to a larger instance. Works up to a point but has a cost ceiling and a hardware limit.
- **Caching**: Add Redis or Memcached. Reduces database load but does not reduce data volume.
- **Connection pooling**: Limited by the database's ability to handle concurrent connections.

When these options are exhausted, sharding becomes necessary. Sharding distributes both read and write load across multiple nodes.

## Sharding Strategies

### Key-Based Sharding (Hash Sharding)

Key-based sharding uses a hash function on the shard key to determine which shard stores a record.

```
shard_id = hash(shard_key) % number_of_shards
```

```python
def get_shard(user_id, num_shards=8):
    return hash(user_id) % num_shards
```

**Advantages**:
- Even data distribution if the hash function is good.
- Simple to implement.
- No need for a lookup service.

**Disadvantages**:
- Adding or removing shards changes the hash modulus, requiring most data to be remapped (resharding).
- Range queries across shards are expensive.
- The shard key must be chosen carefully. A poor choice leads to hotspots.

### Range-Based Sharding

Range-based sharding divides data by ranges of the shard key.

```
Shard 1: user_id 0001-1000
Shard 2: user_id 1001-2000
Shard 3: user_id 2001-3000
```

**Advantages**:
- Efficient range queries within a shard.
- Easy to add new shards for new data ranges without moving existing data.
- Intuitive to understand and administer.

**Disadvantages**:
- Prone to hotspots if the key space is not uniformly accessed. A shard holding active users gets more traffic than a shard holding inactive users.
- Uneven data distribution is common (time-series data concentrates writes on the latest shard).
- Manual planning of range boundaries is required.

### Directory-Based Sharding

Directory-based sharding uses a lookup table that maps keys to shards.

```
Lookup table:
  user_1 -> shard_3
  user_2 -> shard_1
  user_3 -> shard_3
```

```python
# Directory-based routing
class ShardDirectory:
    def __init__(self):
        self.mapping = {}  # key -> shard_id
    
    def get_shard(self, key):
        return self.mapping.get(key)
    
    def assign_shard(self, key, shard_id):
        self.mapping[key] = shard_id
```

**Advantages**:
- Maximum flexibility. Any key can be assigned to any shard.
- Easy resharding. Move a key by updating the directory.
- Supports weighted assignments (larger shards get more data).

**Disadvantages**:
- The lookup directory is a single point of failure and a performance bottleneck.
- Every write operation requires a directory lookup.
- The directory must be replicated and kept consistent.

## Choosing a Shard Key

The shard key is the most important decision in sharding. A good shard key:

- **Distributes data evenly**: No single shard should hold a disproportionate amount of data.
- **Distributes load evenly**: Writes and reads should be spread across all shards.
- **Supports common query patterns**: Ideally, most queries target a single shard.
- **Avoids monotonic or time-series patterns**: Time-based keys concentrate writes on one shard.

```sql
-- Bad shard key example: monotonically increasing ID
CREATE TABLE orders (
    order_id BIGSERIAL PRIMARY KEY,  -- monotonically increasing
    user_id INT,
    created_at TIMESTAMP,
    -- ...
);

-- Good shard key for order data
-- Use a hash of user_id or customer_id so orders stay with the customer
```

## Resharding Challenges

Adding or removing shards is one of the hardest operations in database administration.

### The Resharding Problem

With hash-based sharding using `hash(key) % N`, changing N from 8 to 9 means almost every key maps to a different shard. Moving terabytes of live data without downtime is complex.

### Resharding Approaches

1. **Double writes**: Write new data to both old and new shards during migration. Backfill historical data in batches. Switch reads when backfill completes. This requires application-level write amplification.

2. **Virtual shards (consistent hashing)**: Use many virtual shards (e.g., 4096) mapped to fewer physical shards. Adding a physical shard involves reassigning some virtual shards, not all data.

3. **Pre-splitting**: Start with more shards than you need. As data grows, redistribute shards. This delays resharding but does not eliminate it.

4. **Read repair / write behind**: During resharding, route reads to the old shard and writes to both. A background process moves data and reconciles differences.

## Sharding Tools and Platforms

### MySQL Fabric

MySQL Fabric provides sharding management for MySQL. It handles shard creation, data distribution, and routing. It is an Oracle-supported solution but has limited adoption compared to alternatives.

### Vitess

Vitess is a database clustering system for horizontal scaling of MySQL. It powers YouTube's MySQL deployment and is now a CNCF project.

Key features:
- Automatic sharding and resharding.
- Connection pooling and query rewriting.
- Online schema migration (VReplication).
- Transparent routing via Vitess gateway (vtgate).

```sql
-- Vitess schema with sharding key annotation
CREATE TABLE users (
    user_id BIGINT,
    name VARCHAR(255),
    email VARCHAR(255),
    PRIMARY KEY (user_id)
) VITESS_SHARD_BY HASH(user_id);
```

### Citus

Citus is a PostgreSQL extension that transforms PostgreSQL into a distributed database. It distributes tables across a cluster while maintaining PostgreSQL compatibility.

```sql
-- Create a distributed table in Citus
SELECT create_distributed_table('orders', 'customer_id');

-- Citus automatically routes queries to the correct shard
SELECT COUNT(*) FROM orders WHERE customer_id = 42;
-- Runs on one shard (fast)

SELECT COUNT(*) FROM orders WHERE created_at > now() - interval '1 day';
-- Runs on all shards (coordinator aggregates)
```

### MongoDB Sharding

MongoDB has built-in sharding with a config server replica set and mongos routers.

```javascript
// Enable sharding on a database
sh.enableSharding("my_database")

// Shard a collection with range-based hashed key
sh.shardCollection("my_database.orders", { "order_id": "hashed" })
```

## Query Patterns with Sharding

Sharding works well when queries target a single shard. Cross-shard queries are expensive.

- **Single-shard queries**: `SELECT * FROM orders WHERE shard_key = ?` — fast, hits one shard.
- **Multi-shard queries**: `SELECT * FROM orders WHERE status = 'pending'` — hits all shards, coordinator aggregates results.
- **Joins across shards**: Avoid. Denormalize or pre-join data within each shard.
- **Transactions across shards**: Use distributed transaction protocols (2PC) or avoid them entirely.

## When Not to Shard

Sharding adds complexity. Do not shard unless you need to:

- Your dataset exceeds a single server's storage capacity.
- Write throughput exceeds a single server's capacity.
- You cannot scale vertically further.
- Query latency is unacceptable even with caching and replicas.

For many applications, a well-tuned single database with replicas and caching is sufficient.

## Conclusion

Sharding is a powerful but complex scaling technique. Choose hash-based sharding for even distribution, range-based for ordered data with predictable access patterns, or directory-based for maximum flexibility. Design your shard key carefully, plan for resharding from the start, and choose tools like Vitess or Citus that handle the complexity. Most importantly, exhaust simpler scaling options before adopting sharding.
