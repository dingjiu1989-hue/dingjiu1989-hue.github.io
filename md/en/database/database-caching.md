---
title: "Database Caching"
description: "Implementing database caching with query cache, result cache, and Redis integration patterns."
date: 2026-04-09
board: database
url: https://dingjiu1989-hue.github.io/en/database/database-caching.html
---

# Database Caching

Why Cache? 

Caching reduces database load and improves response times. A good caching strategy can reduce database queries by 90% or more. 

Caching Strategies 

Cache-Aside 

Application checks cache first, loads from database on miss: 

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

Cache sits between application and database. The cache itself loads from the database on miss. 

Write-Through 

Data is written to cache first, then to database. Ensures cache is always consistent. 

Write-Behind 

Data is written to cache and asynchronously batched to database. Fastest writes but risk of data loss. 

Cache Invalidation 

| Strategy | Description | Best For | |----------|-------------|----------| | TTL | Automatic expiry | Most cases | | Key deletion | Delete on update | Write-through | | Versioned keys | Include version | Schema changes | 

Redis Integration 

import redis

class CacheManager:

def **init**(self):

self.redis = redis.Redis(host='localhost', port=6379, decode_responses=True)

def get_or_compute(self, key, compute_func, ttl=3600):

cached = self.redis.get(key)

if cached:

return json.loads(cached)

value = compute_func()

self.redis.setex(key, ttl, json.dumps(value))

return value

Cache Stampede Prevention 

When a popular key expires, many requests may try to recompute simultaneously: 

def get_with_mutex(key, compute_func, ttl=3600):

value = redis.get(key)

if value:

return json.loads(value)

## Try to acquire lock

lock_key = f"lock:{key}"

if redis.setnx(lock_key, "1"):

redis.expire(lock_key, 10)

value = compute_func()

redis.setex(key, ttl, json.dumps(value))

redis.delete(lock_key)

return value

## Wait for the other thread

import time

time.sleep(0.1)

return json.loads(redis.get(key))

Conclusion 

Use cache-aside as the default pattern. Set appropriate TTLs. Implement mutex locking for cache stampede prevention. Monitor cache hit rates. Always have a fallback when cache is unavailable.

**See also:** [Redis Caching Patterns](</en/database/redis-caching-patterns.html>), [Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance](</en/database/database-design-patterns.html>), [Database Migration Strategies](</en/database/database-migration-strategies.html>).

**See also:** [Redis Caching Patterns](</en/database/redis-caching-patterns.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance](</en/database/database-design-patterns.html>)

**See also:** [Redis Caching Patterns](</en/database/redis-caching-patterns.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance](</en/database/database-design-patterns.html>)

**See also:** [Redis Caching Patterns](</en/database/redis-caching-patterns.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance](</en/database/database-design-patterns.html>)

**See also:** [Redis Caching Patterns](</en/database/redis-caching-patterns.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance](</en/database/database-design-patterns.html>)

**See also:** [Redis Caching Patterns](</en/database/redis-caching-patterns.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance](</en/database/database-design-patterns.html>)

**See also:** [Couchbase Guide: N1QL, Document Model, Clustering, and Caching](</en/database/couchbase-guide.html>), [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>)

**See also:** [Couchbase Guide: N1QL, Document Model, Clustering, and Caching](</en/database/couchbase-guide.html>), [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>)

**See also:** [Couchbase Guide: N1QL, Document Model, Clustering, and Caching](</en/database/couchbase-guide.html>), [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>)

**See also:** [Couchbase Guide: N1QL, Document Model, Clustering, and Caching](</en/database/couchbase-guide.html>), [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>)

**See also:** [Couchbase Guide: N1QL, Document Model, Clustering, and Caching](</en/database/couchbase-guide.html>), [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>)

**See also:** [Couchbase Guide: N1QL, Document Model, Clustering, and Caching](</en/database/couchbase-guide.html>), [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>)

**See also:** [Couchbase Guide: N1QL, Document Model, Clustering, and Caching](</en/database/couchbase-guide.html>), [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>)

**See also:** [Couchbase Guide: N1QL, Document Model, Clustering, and Caching](</en/database/couchbase-guide.html>), [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>)

**See also:** [Couchbase Guide: N1QL, Document Model, Clustering, and Caching](</en/database/couchbase-guide.html>), [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>)

**See also:** [Couchbase Guide: N1QL, Document Model, Clustering, and Caching](</en/database/couchbase-guide.html>), [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>)
