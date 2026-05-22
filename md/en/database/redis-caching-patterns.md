---
title: "Redis Caching Patterns"
description: "Redis caching patterns including cache-aside, read-through, write-through, and cache invalidation strategies."
date: 2026-04-13
board: database
url: https://aidev.fit/en/database/redis-caching-patterns.html
---

# Redis Caching Patterns

Redis as Cache 

Redis is an in-memory data store that excels as a cache due to sub-millisecond latency and rich data types. 

Cache-Aside Pattern 

Application checks cache first, falls back to database: 

def get_user(user_id):

cache_key = f"user:{user_id}"

cached = redis.get(cache_key)

if cached:

return json.loads(cached)

user = db.query("SELECT * FROM users WHERE id = %s", [user_id])

if user:

redis.setex(cache_key, 3600, json.dumps(user))

return user

Read-Through 

Cache sits between app and database, auto-loading on miss. Logic is in the cache layer, not the application. 

Write-Through 

Data written to cache first, then database: 

def update_user(user_id, data):

cache_key = f"user:{user_id}"

redis.setex(cache_key, 3600, json.dumps(data))

db.execute("UPDATE users SET name = %s WHERE id = %s", [data['name'], user_id])

Write-Behind 

Write to cache immediately, batch database writes asynchronously. Fastest writes but risk of data loss if cache fails. 

Invalidation Strategies 

| Strategy | Approach | Best For | |----------|----------|----------| | TTL | Auto-expire | Most cases | | Key deletion | Delete on update | Write-through | | Versioned | Include version in key | Schema changes | | Pub/sub | Notify all instances | Distributed caches | 

Rate Limiting with Sorted Sets 

def is_rate_limited(user_id, max_requests=100, window=60):

key = f"ratelimit:{user_id}"

now = time.time()

redis.zremrangebyscore(key, 0, now - window)

if redis.zcard(key) >= max_requests:

return True

redis.zadd(key, {now: now})

redis.expire(key, window)

return False

Conclusion 

Use cache-aside as the default pattern. Always set TTLs to prevent memory exhaustion. Monitor cache hit rates. Implement mutex locking for stampede prevention. Pipeline batch operations for performance.

**See also:** [Database Caching](</en/database/database-caching.html>), [Database Scalability](</en/database/database-scalability.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>).

**See also:** [Database Caching](</en/database/database-caching.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Database Scalability](</en/database/database-scalability.html>)

**See also:** [Database Caching](</en/database/database-caching.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Database Scalability](</en/database/database-scalability.html>)

**See also:** [Database Caching](</en/database/database-caching.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Database Scalability](</en/database/database-scalability.html>)

**See also:** [Database Caching](</en/database/database-caching.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Database Scalability](</en/database/database-scalability.html>)

**See also:** [Database Caching](</en/database/database-caching.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Database Scalability](</en/database/database-scalability.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [DynamoDB vs Cassandra: Data Model, Consistency, Scaling, and Cost](</en/database/dynamodb-vs-cassandra.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [DynamoDB vs Cassandra: Data Model, Consistency, Scaling, and Cost](</en/database/dynamodb-vs-cassandra.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [DynamoDB vs Cassandra: Data Model, Consistency, Scaling, and Cost](</en/database/dynamodb-vs-cassandra.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [DynamoDB vs Cassandra: Data Model, Consistency, Scaling, and Cost](</en/database/dynamodb-vs-cassandra.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [DynamoDB vs Cassandra: Data Model, Consistency, Scaling, and Cost](</en/database/dynamodb-vs-cassandra.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [DynamoDB vs Cassandra: Data Model, Consistency, Scaling, and Cost](</en/database/dynamodb-vs-cassandra.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [DynamoDB vs Cassandra: Data Model, Consistency, Scaling, and Cost](</en/database/dynamodb-vs-cassandra.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [DynamoDB vs Cassandra: Data Model, Consistency, Scaling, and Cost](</en/database/dynamodb-vs-cassandra.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [DynamoDB vs Cassandra: Data Model, Consistency, Scaling, and Cost](</en/database/dynamodb-vs-cassandra.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [DynamoDB vs Cassandra: Data Model, Consistency, Scaling, and Cost](</en/database/dynamodb-vs-cassandra.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [DynamoDB vs Cassandra: Data Model, Consistency, Scaling, and Cost](</en/database/dynamodb-vs-cassandra.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [DynamoDB vs Cassandra: Data Model, Consistency, Scaling, and Cost](</en/database/dynamodb-vs-cassandra.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [DynamoDB vs Cassandra: Data Model, Consistency, Scaling, and Cost](</en/database/dynamodb-vs-cassandra.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [DynamoDB vs Cassandra: Data Model, Consistency, Scaling, and Cost](</en/database/dynamodb-vs-cassandra.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [DynamoDB vs Cassandra: Data Model, Consistency, Scaling, and Cost](</en/database/dynamodb-vs-cassandra.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [DynamoDB vs Cassandra: Data Model, Consistency, Scaling, and Cost](</en/database/dynamodb-vs-cassandra.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [DynamoDB vs Cassandra: Data Model, Consistency, Scaling, and Cost](</en/database/dynamodb-vs-cassandra.html>)
