---
title: "Database Sharding Strategies: Partitioning, Consistent Hashing, and Real-World Patterns"
description: "Complete guide to database sharding — choosing a shard key, consistent hashing, resharding strategies, and common pitfalls."
date: 2026-05-08
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/database-sharding-strategies.html
---

# Database Sharding Strategies: Partitioning, Consistent Hashing, and Real-World Patterns

Database sharding is how you scale a database beyond what a single server can handle — splitting data across multiple independent database instances. While managed databases have made sharding less common for new projects, understanding sharding is critical for system design interviews, working at scale, and architecting systems that will eventually need it. This guide covers the theory and practice of database sharding.

## Sharding Strategies Compared

Strategy| How It Works| Pros| Cons| Best For  
---|---|---|---|---  
Key-Based (Hash) Sharding| Hash(shard_key) % N → shard number| Even distribution, simple routing| Adding shards rehashes ALL data; cross-shard queries are hard| Even data distribution, simple lookup patterns  
Range-Based Sharding| Shard 1: A-M, Shard 2: N-Z| Intuitive, range queries work within a shard| Hotspots (shard with most popular range gets overloaded)| Time-series data, alphabetical/sequential data  
Directory-Based Sharding| Lookup table maps key → shard| Flexible (move data between shards easily)| Lookup service is a single point of failure/ bottleneck| Complex sharding needs, frequent rebalancing  
Geo-Based Sharding| Shard by geographic region (US, EU, APAC)| Low latency per region, GDPR compliance| Uneven distribution; cross-region queries are slow| Multi-region apps, data locality requirements  
Entity/Functional Sharding| Shard by entity type (users, orders, products)| Independent scaling per entity| Joins across entities are impossible in SQL| Microservices, domain-driven design  
  
## Consistent Hashing: The Key to Dynamic Sharding
    
    
    # Consistent hashing minimizes data movement when adding/removing shards
    # Traditional hash: hash(key) % N → changing N remaps ALL keys
    # Consistent hash: hash(key) and hash(shard) both mapped to a ring
    #   Adding a shard: only ~1/N keys need to move
    #   Removing a shard: only that shard's keys need to move
    
    # Simplified consistent hashing implementation
    import hashlib, bisect
    
    class ConsistentHash:
        def __init__(self, virtual_nodes_per_shard=150):
            self.ring = {}  # hash → shard_id
            self.sorted_hashes = []  # sorted list of hash positions
            self.vnodes = virtual_nodes_per_shard
    
        def add_shard(self, shard_id):
            for i in range(self.vnodes):
                h = self._hash(f"{shard_id}:{i}")
                self.ring[h] = shard_id
                bisect.insort(self.sorted_hashes, h)
    
        def get_shard(self, key):
            h = self._hash(key)
            # Find first shard hash >= key hash (clockwise on ring)
            idx = bisect.bisect_left(self.sorted_hashes, h)
            if idx == len(self.sorted_hashes):
                idx = 0  # Wrap around the ring
            return self.ring[self.sorted_hashes[idx]]
    
        def _hash(self, s):
            return int(hashlib.md5(s.encode()).hexdigest(), 16)

## When to Shard (and When Not To)

Scenario| Should You Shard?| Alternative  
---|---|---  
Single DB < 100GB, < 1K QPS| No — single instance is fine| Add read replicas for read scaling  
100GB-1TB, read-heavy| No — read replicas first| Read replicas + caching (Redis)  
100GB-1TB, write-heavy (>5K write QPS)| Maybe — consider sharding| Also consider: better hardware, connection pooling, queue writes  
>1TB, any workload| Yes — single server can't hold it| Sharding is necessary at this scale  
Multi-tenant SaaS (tenant isolation needed)| Maybe — tenant-based sharding| Also consider: row-level security, separate schemas  
Startup with <1K users| No — premature optimization| Single DB with good indexing  
  
## Common Sharding Pitfalls

Pitfall| Problem| Solution  
---|---|---  
Choosing the wrong shard key| Uneven data distribution, hotspots| Analyze access patterns, pick high-cardinality key  
Cross-shard queries| JOINs, aggregations across shards are application-level| Denormalize data, use materialized views, or avoid cross-shard queries  
Resharding without downtime| Moving data between shards blocks the application| Consistent hashing + live migration tools (Vitess, Citus)  
Auto-increment IDs collide| Each shard's auto-increment starts at 1| Use UUIDs, Snowflake IDs, or globally unique ID service  
Transactions across shards| ACID transactions don't span shards| Use distributed transactions (2PC) or design around it (sagas)  
  
**Bottom line:** Sharding is a last-resort scaling strategy — exhaust all other options first (indexing, caching, read replicas, connection pooling, query optimization). When you do need sharding, use key-based sharding with consistent hashing for the most flexibility. For PostgreSQL, consider Citus (distributed PostgreSQL) or Vitess (MySQL) as battle-tested sharding solutions before building your own. See also: [PostgreSQL Query Optimization](</en/tech/postgresql-query-optimization.html>) and [System Design Interview Guide](</en/tech/system-design-interview-guide.html>).
