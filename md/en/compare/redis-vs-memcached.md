---
title: "Redis vs Memcached: Caching Solution Comparison"
description: "Compare Redis and Memcached across data structures, persistence, clustering, memory efficiency, and use cases for caching, sessions, and message queuing."
date: 2026-05-12
board: compare
url: https://dingjiu1989-hue.github.io/en/compare/redis-vs-memcached.html
---

# Redis vs Memcached: Caching Solution Comparison

## Redis vs Memcached: Caching Solution Comparison

## Redis vs Memcached: Caching Solution Comparison

## Redis vs Memcached: Caching Solution Comparison

## Redis vs Memcached: Caching Solution Comparison

## Redis vs Memcached: Caching Solution Comparison

## Redis vs Memcached: Caching Solution Comparison

## Redis vs Memcached: Caching Solution Comparison

## Redis vs Memcached: Caching Solution Comparison

## Redis vs Memcached: Caching Solution Comparison

## Redis vs Memcached: Caching Solution Comparison

## Redis vs Memcached: Caching Solution Comparison

## Redis vs Memcached: Caching Solution Comparison

## Redis vs Memcached: Caching Solution Comparison

### Introduction

Redis and Memcached are the two most widely used in-memory data stores, but they serve different purposes despite overlapping use cases. Memcached is a purpose-built cache; Redis is a versatile data structure server that happens to excel at caching. Choosing between them requires understanding their architectural differences and the specific requirements of your application.

### Data Structure Support

#### Redis: Rich Data Types

Redis supports a wide range of data structures beyond simple key-value pairs:

import redis.asyncio as redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

## Strings (basic key-value)

await r.set('user:1000:name', 'Alice')

name = await r.get('user:1000:name')

## Lists (ordered collection, great for queues)

await r.lpush('notifications:queue', 'email_1', 'email_2')

notification = await r.brpop('notifications:queue', timeout=5)

## Sets (unique members, set operations)

await r.sadd('user:1000:roles', 'admin', 'editor', 'viewer')

await r.sadd('user:1001:roles', 'editor', 'viewer')

common_roles = await r.sinter('user:1000:roles', 'user:1001:roles')

## Returns: {'editor', 'viewer'}

## Sorted Sets (leaderboards, rate limiting)

await r.zadd('leaderboard:weekly', {'user:1000': 1500, 'user:1001': 2300})

top_players = await r.zrevrange('leaderboard:weekly', 0, 9, withscores=True)

## Hashes (objects)

await r.hset('product:500', mapping={

'name': 'Widget',

'price': 29.99,

'stock': 100,

})

product = await r.hgetall('product:500')

## Bitmaps (analytics, feature flags)

await r.setbit('active:users:2026-05-12', user_id=1000, value=1)

daily_active = await r.bitcount('active:users:2026-05-12')

## Streams (event log, message queue)

await r.xadd('order:events', {'order_id': '123', 'status': 'created'})

events = await r.xread({'order:events': '0'}, count=10)

#### Memcached: Simple Key-Value

Memcached provides a minimal key-value API:

import pymemcache

client = pymemcache.Client(('localhost', 11211))

## Basic get/set

client.set('user:1000:profile', profile_data, expire=3600)

profile = client.get('user:1000:profile')

## Multi-get for batch operations

users = client.get_multi([

'user:1000:profile',

'user:1001:profile',

'user:1002:profile',

])

## Atomic operations

client.add('lock:payment:123', 'locked', expire=30) # Only if not exists

client.replace('user:1000:profile', updated_profile) # Only if exists

client.append('log:buffer', 'new entry\n') # Append to existing value

client.prepend('log:buffer', 'header\n') # Prepend

## Increment/Decrement

client.set('counter:api:day', '0')

client.incr('counter:api:day', 1)

### Persistence and Durability

| Feature | Redis | Memcached |

|---|---|---|

| Persistence | RDB snapshots, AOF logs | None (ephemeral) |

| Recovery | Automatic on restart | All data lost |

| Replication | Master-replica, sentinel, cluster | No replication |

| Durability modes | fsync policies (always, every sec, no) | N/A |

Redis persistence configuration:

## redis.conf

## RDB snapshot (point-in-time)

save 900 1 # Save if 1 key changed in 900 seconds

save 300 10 # Save if 10 keys changed in 300 seconds

save 60 10000 # Save if 10000 keys changed in 60 seconds

## AOF (append-only log)

appendonly yes

appendfsync everysec # fsync every second

auto-aof-rewrite-percentage 100

auto-aof-rewrite-min-size 64mb

## Hybrid persistence (Redis 7+)

aof-use-rdb-preamble yes # RDB prefix for faster loading

### Memory Efficiency and Eviction

#### Memcached: Slab Allocation

Memcached uses slab allocation to minimize fragmentation:

## Memcached slab configuration

## Memory is divided into slabs of various chunk sizes

## Items are stored in the smallest slab that fits

stats = client.stats()

## STAT slab_reassign_rescues 0

## STAT slab_reassign_evictions_nomem 0

## STAT slab_reassign_inline_reclaim 0

## STAT slab_reassign_busy_items 0

## Eviction: LRU only

client.set('key', 'value', expire=0, noreply=False)

#### Redis: Multiple Eviction Policies

## redis.conf eviction policies

maxmemory 2gb

maxmemory-policy allkeys-lru # Evict least recently used keys

## Available policies:

## noeviction: Return errors on writes when memory full

## allkeys-lru: Evict LRU keys (most common)

## allkeys-lfu: Evict least frequently used

## volatile-lru: Evict LRU among keys with TTL

## volatile-lfu: Evict LFU among keys with TTL

## allkeys-random: Evict random keys

## volatile-random: Evict random keys with TTL

## volatile-ttl: Evict keys with shortest TTL

Memory overhead comparison:

## Redis: ~50 bytes overhead per key + value size

## Example: 1M keys with 100-byte values

overhead_redis = 1_000_000 * (50 + 100) # ~150MB

## Memcached: ~56 bytes overhead per key + value size + slab fragmentation

## Example: 1M keys with 100-byte values

overhead_memcached = 1_000_000 * (56 + 100) # ~156MB + ~10% fragmentation

### Clustering and High Availability

#### Redis Cluster

## redis-cluster.conf (per node)

port 7000

cluster-enabled yes

cluster-config-file nodes.conf

cluster-node-timeout 5000

appendonly yes

## 3 master, 3 replica (production minimum)

## Redis Cluster client

from redis.cluster import RedisCluster

rc = RedisCluster(

startup_nodes=[

{"host": "127.0.0.1", "port": "7000"},

{"host": "127.0.0.1", "port": "7001"},

{"host": "127.0.0.1", "port": "7002"},

],

decode_responses=True,

)

## Automatic sharding: keys are distributed across 16384 slots

## slot = CRC16(key) % 16384

await rc.set("user:1000:session", session_data)

await rc.get("user:1000:session")

## Cross-slot operations require tags

await rc.set("{users}:1000", "alice")

await rc.set("{users}:1001", "bob")

users = await rc.mget("{users}:1000", "{users}:1001")

#### Memcached: No Built-in Clustering

Memcached has no built-in clustering. Sharding is implemented at the client level:

from pymemcache.client.hash import HashClient

## Client-side consistent hashing

client = HashClient([

('memcached-1', 11211),

('memcached-2', 11211),

('memcached-3', 11211),

], use_pooling=True)

## Consistent hashing minimizes cache misses when nodes change

client.set("key", "value")

result = client.get("key")

### Use Case Comparison

| Use Case | Redis | Memcached |

|---|---|---|

| Simple key-value cache | Good (with persistence overhead) | Excellent |

| Session store | Excellent (built-in TTL, persistence) | Requires external persistence |

| Rate limiting | Excellent (sorted sets + atomic incr) | Basic (atomic incr only) |

| Message queue | Built-in (lists, streams, pub/sub) | No support |

| Leaderboards | Built-in (sorted sets) | No support |

| Geospatial queries | Yes (GEO commands) | No |

| Full-text search | Yes (RediSearch module) | No |

| Time-series data | Yes (RedisTimeSeries module) | No |

### When to Use Which

  * **Use Memcached** when you need a simple, fast, memory-only cache for database query results or computed data that can be regenerated. Memcached excels at its single purpose.

  * **Use Redis** when you need data structures beyond key-value, persistence, replication, or any advanced caching patterns like rate limiting, session stores, or leaderboards.

  * **Use both** when you want a two-tier caching strategy: Memcached for hot cache (regenerable) and Redis for persistent cache (session, counter) and non-cache workloads.




For most modern applications, Redis is the better default due to its versatility. Reserve Memcached for specific high-throughput caching scenarios where Redis's overhead and feature set are unnecessary.

**See also:** [Redis vs Memcached vs Dragonfly (2026): In-Memory Data Store Comparison](</en/compare/redis-vs-memcached-vs-dragonfly.html>), [Next.js vs Remix vs Astro](</en/compare/nextjs-vs-remix.html>), [Nginx vs Caddy: Web Server Comparison](</en/compare/nginx-vs-caddy.html>).

**See also:** [Redis vs Memcached vs Dragonfly (2026): In-Memory Data Store Comparison](</en/compare/redis-vs-memcached-vs-dragonfly.html>), [Next.js vs Remix vs Astro](</en/compare/nextjs-vs-remix.html>), [gRPC vs WebSocket: Real-Time Communication](</en/compare/grpc-vs-websocket.html>)

**See also:** [Redis vs Memcached vs Dragonfly (2026): In-Memory Data Store Comparison](</en/compare/redis-vs-memcached-vs-dragonfly.html>), [Next.js vs Remix vs Astro](</en/compare/nextjs-vs-remix.html>), [gRPC vs WebSocket: Real-Time Communication](</en/compare/grpc-vs-websocket.html>)
