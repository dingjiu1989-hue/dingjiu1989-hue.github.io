---
title: "Database Scalability"
description: "Strategies for database scalability: vertical scaling, horizontal scaling, read replicas, and caching."
date: 2026-04-09
board: database
url: https://aidev.fit/en/database/database-scalability.html
---

# Database Scalability

Scalability Options 

Database scalability options range from simple to complex. Start with the simplest approach and evolve. 

Vertical Scaling 

Upgrade to a larger server with more CPU, RAM, and storage. 

## AWS RDS instance upgrade

resource "aws_db_instance" "main" {

instance_class = "db.r6g.8xlarge" # 32 vCPU, 256GB RAM

allocated_storage = 5000 # 5TB SSD

}

Simple but has a cost ceiling and hardware limits. 

Read Replicas 

Offload read traffic to replicas: 

class DatabaseRouter:

def **init**(self, primary, replicas):

self.primary = primary

self.replicas = replicas

def get_conn(self, write=False):

if write:

return self.primary

return random.choice(self.replicas)

## Route reads to replicas, writes to primary

db_router.get_conn(write=True).execute("INSERT INTO ...")

results = db_router.get_conn(write=False).execute("SELECT ...")

Effective for read-heavy workloads. Does not help with write scaling. 

Caching 

Reduce database load with in-memory caching: 

def get_user(user_id):

user = cache.get(f"user:{user_id}")

if not user:

user = db.query("SELECT * FROM users WHERE id = %s", user_id)

cache.setex(f"user:{user_id}", 3600, json.dumps(user))

return user

Horizontal Scaling (Sharding) 

Distribute data across multiple database servers: 

class ShardManager:

def **init**(self, shards):

self.shards = shards

def get_shard(self, customer_id):

return self.shards[hash(customer_id) % len(self.shards)]

Most complex. Use tools like Vitess, Citus, or CockroachDB. 

Scaling Decision Tree 

Is DB overloaded?

├── Read-heavy? → Add read replicas

├── Write-heavy?

│ ├── Can you cache? → Add Redis/memcached

│ └── Cache insufficient? → Shard

└── Both? → Scale vertically first, then shard

Conclusion 

Scale vertically first (simple). Add read replicas for read loads. Add caching for repeated queries. Shard only when necessary. Monitor your bottleneck before choosing a strategy. Most applications never need sharding.

**See also:** [Database Horizontal Scaling Strategies](</en/database/database-horizontal-scaling.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Redis Caching Patterns](</en/database/redis-caching-patterns.html>).

**See also:** [Database Horizontal Scaling Strategies](</en/database/database-horizontal-scaling.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [Database Horizontal Scaling Strategies](</en/database/database-horizontal-scaling.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [Database Horizontal Scaling Strategies](</en/database/database-horizontal-scaling.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [Database Horizontal Scaling Strategies](</en/database/database-horizontal-scaling.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [Database Horizontal Scaling Strategies](</en/database/database-horizontal-scaling.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [Redis Caching Patterns](</en/database/redis-caching-patterns.html>), [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>), [Database Pagination: Offset, Cursor, Keyset, and Seek Methods](</en/database/database-pagination-techniques.html>)

**See also:** [Redis Caching Patterns](</en/database/redis-caching-patterns.html>), [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>), [Database Pagination: Offset, Cursor, Keyset, and Seek Methods](</en/database/database-pagination-techniques.html>)

**See also:** [Redis Caching Patterns](</en/database/redis-caching-patterns.html>), [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>), [Database Pagination: Offset, Cursor, Keyset, and Seek Methods](</en/database/database-pagination-techniques.html>)

**See also:** [Redis Caching Patterns](</en/database/redis-caching-patterns.html>), [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>), [Database Pagination: Offset, Cursor, Keyset, and Seek Methods](</en/database/database-pagination-techniques.html>)

**See also:** [Redis Caching Patterns](</en/database/redis-caching-patterns.html>), [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>), [Database Pagination: Offset, Cursor, Keyset, and Seek Methods](</en/database/database-pagination-techniques.html>)

**See also:** [Redis Caching Patterns](</en/database/redis-caching-patterns.html>), [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>), [Database Pagination: Offset, Cursor, Keyset, and Seek Methods](</en/database/database-pagination-techniques.html>)

**See also:** [Redis Caching Patterns](</en/database/redis-caching-patterns.html>), [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>), [Database Pagination: Offset, Cursor, Keyset, and Seek Methods](</en/database/database-pagination-techniques.html>)

**See also:** [Redis Caching Patterns](</en/database/redis-caching-patterns.html>), [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>), [Database Pagination: Offset, Cursor, Keyset, and Seek Methods](</en/database/database-pagination-techniques.html>)

**See also:** [Redis Caching Patterns](</en/database/redis-caching-patterns.html>), [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>), [Database Pagination: Offset, Cursor, Keyset, and Seek Methods](</en/database/database-pagination-techniques.html>)

**See also:** [Redis Caching Patterns](</en/database/redis-caching-patterns.html>), [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>), [Database Pagination: Offset, Cursor, Keyset, and Seek Methods](</en/database/database-pagination-techniques.html>)

**See also:** [Redis Caching Patterns](</en/database/redis-caching-patterns.html>), [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>), [Database Pagination: Offset, Cursor, Keyset, and Seek Methods](</en/database/database-pagination-techniques.html>)

**See also:** [Redis Caching Patterns](</en/database/redis-caching-patterns.html>), [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>), [Database Pagination: Offset, Cursor, Keyset, and Seek Methods](</en/database/database-pagination-techniques.html>)

**See also:** [Redis Caching Patterns](</en/database/redis-caching-patterns.html>), [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>), [Database Pagination: Offset, Cursor, Keyset, and Seek Methods](</en/database/database-pagination-techniques.html>)

**See also:** [Redis Caching Patterns](</en/database/redis-caching-patterns.html>), [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>), [Database Pagination: Offset, Cursor, Keyset, and Seek Methods](</en/database/database-pagination-techniques.html>)

**See also:** [Redis Caching Patterns](</en/database/redis-caching-patterns.html>), [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>), [Database Pagination: Offset, Cursor, Keyset, and Seek Methods](</en/database/database-pagination-techniques.html>)

**See also:** [Redis Caching Patterns](</en/database/redis-caching-patterns.html>), [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>), [Database Pagination: Offset, Cursor, Keyset, and Seek Methods](</en/database/database-pagination-techniques.html>)
