---
title: "Caching Strategies and Patterns in Distributed Systems"
description: "Caching patterns: cache-aside, write-through, write-behind, eviction policies, distributed caching with Redis, CDN caching, and invalidation."
date: 2026-04-20
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/caching-strategies.html
---

# Caching Strategies and Patterns in Distributed Systems

Caching is the single most effective performance optimization in distributed systems. A well-designed cache reduces database load, decreases response latency, and improves system throughput. This article covers the major caching patterns, eviction policies, distributed caching with Redis, CDN caching, and the hardest problem in computer science: cache invalidation. 

Caching Patterns 

Cache-Aside (Lazy Loading) 

Cache-aside is the most common caching pattern. The application checks the cache first. On a cache miss, it reads from the database and populates the cache. 

class CacheAside:

def **init**(self, cache, database):

self.cache = cache

self.database = database

def get_user(self, user_id):

## 1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Try cache first

cached = self.cache.get(f"user:{user_id}")

if cached is not None:

return cached

## 2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Cache miss: read from database

user = self.database.query("SELECT * FROM users WHERE id = ?", user_id)

if user:

## 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Populate cache for next time

self.cache.set(f"user:{user_id}", user, ttl=3600)

return user

def update_user(self, user_id, data):

## 1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Update database

self.database.execute("UPDATE users SET name = ? WHERE id = ?",

data['name'], user_id)

## 2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Invalidate cache (not update!)

self.cache.delete(f"user:{user_id}")

**Advantages** :

  * Only caches data that is actually requested (no wasted space).

  * Simple to implement and understand.

  * Cache failures are not fatal (system falls back to database).




**Disadvantages** :

  * Cache miss penalty includes both cache check and database read.

  * Stale data until TTL expires (if items are not invalidated on update).

  * Thundering herd problem on cache miss for popular items.




Write-Through 

Write-through caches update the cache synchronously when data is written to the database. 

class WriteThrough:

def **init**(self, cache, database):

self.cache = cache

self.database = database

def update_user(self, user_id, data):

## 1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Update database

self.database.execute("UPDATE users SET name = ? WHERE id = ?",

data['name'], user_id)

## 2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Update cache synchronously

user = self.database.query("SELECT * FROM users WHERE id = ?", user_id)

self.cache.set(f"user:{user_id}", user, ttl=3600)

**Advantages** :

  * Cache is always consistent with the database (no stale data).

  * No cache miss penalty for reads.

  * Read path is simple (always from cache or cache-miss-then-database).




**Disadvantages** :

  * Writes are slower (must update both database and cache).

  * Writes more data to cache than may ever be read (cache pollution).

  * Cache and database updates are not atomic (risk of inconsistency).




Write-Behind (Write-Back) 

Write-behind caches write to the cache immediately and asynchronously update the database. 

import asyncio

class WriteBehind:

def **init**(self, cache, database):

self.cache = cache

self.database = database

self.write_queue = asyncio.Queue()

self._start_flusher()

def _start_flusher(self):

"""Background task that flushes writes to database."""

async def flusher():

while True:

## Batch writes and flush periodically

batch = []

for _ in range(100): # Batch size

try:

item = await asyncio.wait_for(

self.write_queue.get(), timeout=1.0

)

batch.append(item)

except asyncio.TimeoutError:

break

if batch:

self._flush_to_database(batch)

asyncio.create_task(flusher())

def update_user(self, user_id, data):

## 1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Update cache immediately

user = {**self.cache.get(f"user:{user_id}", {}),** data}

self.cache.set(f"user:{user_id}", user)

## 2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Queue database update

self.write_queue.put_nowait({

"type": "update_user",

"user_id": user_id,

"data": data

})

**Advantages** :

  * Very fast writes (no database latency).

  * Can batch database writes for efficiency.

  * Reduces database write load.




**Disadvantages** :

  * Risk of data loss if cache fails before flush completes.

  * Complex to implement correctly.

  * Inconsistency window between cache update and database update.




Refresh-Ahead 

Refresh-ahead proactively refreshes the cache before data expires. 

class RefreshAhead:

def **init**(self, cache, database, refresh_threshold=0.8):

self.cache = cache

self.database = database

self.refresh_threshold = refresh_threshold # Refresh when 80% of TTL elapsed

def get_user(self, user_id):

cached = self.cache.get(f"user:{user_id}")

if cached is None:

user = self.database.query("SELECT * FROM users WHERE id = ?", user_id)

self.cache.set(f"user:{user_id}", user, ttl=3600)

return user

## Check if we should refresh

ttl = self.cache.ttl(f"user:{user_id}")

if ttl < 3600 * (1 - self.refresh_threshold):

## Asynchronously refresh in background

self._async_refresh(f"user:{user_id}", user_id)

return cached

def _async_refresh(self, cache_key, user_id):

"""Background refresh task."""

import threading

def refresh():

user = self.database.query("SELECT * FROM users WHERE id = ?", user_id)

if user:

self.cache.set(cache_key, user, ttl=3600)

threading.Thread(target=refresh, daemon=True).start()

Cache Eviction Policies 

Least Recently Used (LRU) 

Evicts the item that was accessed least recently. Good for workloads with temporal locality. 

Cache: [A(1min ago), B(30s ago), C(5s ago), D(now)]

A is accessed least recently -> evict A

Redis implements LRU approximation with `maxmemory-policy allkeys-lru`. 

Least Frequently Used (LFU) 

Evicts the item accessed least frequently. Good for workloads with skewed popularity. 

Cache: [A(100x), B(50x), C(30x), D(5x)]

D is least frequently accessed -> evict D

Redis supports LFU with `maxmemory-policy allkeys-lfu`. 

Time-To-Live (TTL) 

Evicts items based on their TTL. Items expire regardless of access pattern. Essential for all caching systems. 

First In, First Out (FIFO) 

Evicts the oldest item regardless of access frequency. Simple but less effective than LRU. 

Choosing an Eviction Policy 

| Workload | Best Policy | |----------|-------------| | Uniform access (all items equally likely) | FIFO or TTL | | Temporal locality (recent items more likely) | LRU | | Skewed access (some items much more popular) | LFU | | Time-sensitive data (session, expiring offers) | TTL | | Unknown | LRU + TTL | 

Distributed Caching with Redis 

Redis is the dominant distributed cache. It provides in-memory data structures, replication, persistence, and high availability. 

Redis Cluster Setup 

## docker-compose.yml for Redis Cluster

version: '3'

services:

redis-cluster:

image: redis:7-alpine

command: redis-cli --cluster create

127.0.0.1:7000 127.0.0.1:7001 127.0.0.1:7002

127.0.0.1:7003 127.0.0.1:7004 127.0.0.1:7005

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--cluster-replicas 1

ports:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- "7000-7005:7000-7005"

Redis Caching Best Practices 

import redis

import json

class RedisCache:

def **init**(self, redis_url):

self.client = redis.from_url(redis_url)

def get_or_compute(self, key, compute_func, ttl=300):

"""Cache-aside with compute function."""

cached = self.client.get(key)

if cached is not None:

return json.loads(cached)

value = compute_func()

self.client.setex(key, ttl, json.dumps(value))

return value

def get_batch(self, keys):

"""Batch cache get using pipeline."""

pipeline = self.client.pipeline()

for key in keys:

pipeline.get(key)

results = pipeline.execute()

return {

key: json.loads(val) if val else None

for key, val in zip(keys, results)

}

Cache Sharding 

For very large caches, shard across multiple Redis nodes. 

import hashlib

class ShardedRedis:

def **init**(self, nodes):

self.nodes = nodes # List of Redis clients

def _get_node(self, key):

"""Determine which node holds this key."""

hash_val = int(hashlib.md5(key.encode()).hexdigest(), 16)

return self.nodes[hash_val % len(self.nodes)]

def get(self, key):

node = self._get_node(key)

return node.get(key)

def set(self, key, value, ttl=300):

node = self._get_node(key)

node.setex(key, ttl, value)

CDN Caching 

Content Delivery Networks (CDNs) cache static and dynamic content at edge locations close to users. 

Cache Control Headers 

## Nginx: Static asset caching headers

location /static/ {

expires 365d;

add_header Cache-Control "public, immutable";

}

location /api/content/ {

## Dynamic content: shorter cache

expires 5m;

add_header Cache-Control "public, must-revalidate";

}

location /api/user/ {

## Private content: no CDN caching

add_header Cache-Control "private, no-cache";

}

CDN Cache Invalidation 

## CloudFront: Invalidate specific paths

aws cloudfront create-invalidation \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--distribution-id E123456 \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--paths "/api/content/*" "/index.html"

## Fastly: Purge by key

curl -X POST https://api.fastly.com/service/SERVICE/purge \

-H "Fastly-Key: $API_KEY" \

-H "Surrogate-Key: product:1234" \

-H "Accept: application/json"

Cache Invalidation 

Cache invalidation is notoriously difficult. These strategies help. 

Time-Based Invalidation (TTL) 

The simplest approach. Every cache entry has a TTL. Data is stale until the TTL expires. 

Always safe: stale data is eventually replaced.

Always simple: no complex invalidation logic.

Limitation: data can be arbitrarily stale within the TTL window.

Event-Driven Invalidation 

When data changes, publish an invalidation event. 

## Event-driven invalidation

class EventDrivenCache:

def **init**(self, cache, message_bus):

self.cache = cache

self.message_bus = message_bus

## Subscribe to invalidation events

self.message_bus.subscribe("cache.invalidate", self.handle_invalidation)

def handle_invalidation(self, event):

key = event.data['key']

self.cache.delete(key)

log.info(f"Invalidated cache key: {key} due to {event.data['reason']}")

Write-Through Invalidation 

Invalidate (or update) the cache as part of the write transaction. 

def update_product(product_id, data):

with transaction():

## Update database

db.execute("UPDATE products SET price = ? WHERE id = ?",

data['price'], product_id)

## Invalidate cache in same transaction if possible

cache.delete(f"product:{product_id}")

## Publish invalidation for other cache nodes

message_bus.publish("cache.invalidate", {"key": f"product:{product_id}"})

Conclusion 

Choose cache-aside for most general-purpose caching. Use write-through when read consistency is critical. Use write-behind when write performance is paramount. Use refresh-ahead for predictable access patterns. Set appropriate TTLs as a safety net. Use Redis for distributed caching with proper cluster configuration. Use CDNs for content delivery to global users. Remember that cache invalidation is hard: prefer TTLs over complex invalidation logic, use event-driven invalidation when TTLs are insufficient, and always have a fallback to the original data source.

**See also:** [Caching Strategies](</en/architecture/cache-strategies.html>), [HTTP Caching Architecture](</en/architecture/caching-http.html>), [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>).

**See also:** [Caching Strategies](</en/architecture/cache-strategies.html>), [HTTP Caching Architecture](</en/architecture/caching-http.html>), [Circuit Breaker Pattern: Building Resilient Systems](</en/architecture/circuit-breaker-pattern.html>)

**See also:** [Caching Strategies](</en/architecture/cache-strategies.html>), [HTTP Caching Architecture](</en/architecture/caching-http.html>), [Circuit Breaker Pattern: Building Resilient Systems](</en/architecture/circuit-breaker-pattern.html>)

**See also:** [Caching Strategies](</en/architecture/cache-strategies.html>), [HTTP Caching Architecture](</en/architecture/caching-http.html>), [Bulkhead Pattern for Resilience](</en/architecture/bulkhead-pattern.html>)

**See also:** [Caching Strategies](</en/architecture/cache-strategies.html>), [HTTP Caching Architecture](</en/architecture/caching-http.html>), [Bulkhead Pattern for Resilience](</en/architecture/bulkhead-pattern.html>)

**See also:** [Caching Strategies](</en/architecture/cache-strategies.html>), [HTTP Caching Architecture](</en/architecture/caching-http.html>), [Bulkhead Pattern for Resilience](</en/architecture/bulkhead-pattern.html>)

**See also:** [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [CDN Architecture](</en/architecture/cdn-architecture.html>)

**See also:** [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [CDN Architecture](</en/architecture/cdn-architecture.html>)

**See also:** [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [CDN Architecture](</en/architecture/cdn-architecture.html>)

**See also:** [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [CDN Architecture](</en/architecture/cdn-architecture.html>)

**See also:** [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [CDN Architecture](</en/architecture/cdn-architecture.html>)
