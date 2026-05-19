---
title: "Redis Caching Patterns"
description: "Explore Redis caching patterns including cache-aside, write-through, lazy loading, distributed locking, session storage, and rate limiting."
date: 2025-12-24
board: database
url: https://dingjiu1989-hue.github.io/en/database/redis-caching.html
---

# Redis Caching Patterns

## Redis Caching Patterns

### Redis Caching Patterns

#### Redis Caching Patterns

#### Redis Caching Patterns

#### Redis Caching Patterns

#### Redis Caching Patterns

#### Redis Caching Patterns

#### Redis Caching Patterns

#### Redis Caching Patterns

#### Redis Caching Patterns

#### Redis Caching Patterns

#### Redis Caching Patterns

#### Redis Caching Patterns

#### Redis Caching Patterns

#### Redis Caching Patterns

Redis as a Cache 

Redis is an in-memory data structure store that excels as a cache due to its sub-millisecond latency, rich data types, and built-in expiration. When used correctly, Redis can reduce database load by 90% or more while dramatically improving application response times. 

Data Structures Overview 

| Structure | Use Case | Example | |-----------|----------|---------| | String | Simple values, counters | User session, page views | | Hash | Object fields | User profile fields | | List | Ordered collection | Message queue, timeline | | Set | Unique values | Tags, followers | | Sorted Set | Ranked data | Leaderboard, rate limiting | | HyperLogLog | Cardinality estimation | Unique visitors | | Bitmap | Boolean flags | Daily active users | 

Caching Patterns 

Cache-Aside (Lazy Loading) 

The most common caching pattern. The application checks the cache first; on a miss, it loads data from the database and populates the cache. 

import redis

import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def get_user(user_id):

cache_key = f"user:{user_id}"

#### Try cache first

cached = r.get(cache_key)

if cached:

return json.loads(cached)

#### Cache miss: load from database

user = db.query("SELECT * FROM users WHERE id = %s", [user_id])

if user:

#### Populate cache with TTL

r.setex(cache_key, 3600, json.dumps(user))

return user

**Pros** : Only caches data that is requested, resilient to cache failures. **Cons** : Cache miss penalty (three round trips), stale data until TTL expires. 

Write-Through 

Data is written to the cache first, then to the database. Reads always hit the cache. 

def update_user(user_id, data):

cache_key = f"user:{user_id}"

#### Write to cache first

r.setex(cache_key, 3600, json.dumps(data))

#### Then write to database

db.execute(

"UPDATE users SET name = %s, email = %s WHERE id = %s",

[data['name'], data['email'], user_id]

)

**Pros** : Cache is always consistent with database writes. **Cons** : Write latency increases, cache stores data that may never be read. 

Write-Behind (Write-Back) 

Data is written to cache and asynchronously written to the database later. 

def write_behind(user_id, data):

cache_key = f"user:{user_id}"

#### Write to cache immediately

r.setex(cache_key, 3600, json.dumps(data))

#### Queue database write for batch processing

r.lpush("db:write:queue", json.dumps({

"table": "users",

"id": user_id,

"data": data

}))

**Pros** : Very fast writes, can batch database operations. **Cons** : Risk of data loss if cache fails before database write. 

Cache Invalidation Strategies 

| Strategy | How It Works | Best For | |----------|-------------|----------| | TTL expiration | Automatic expiry after set time | Most applications | | Key deletion | Delete cache key on data update | Write-through | | Versioned keys | Include version in key name | Schema changes | | Pub/sub invalidation | Notify all instances to invalidate | Distributed caches | 

Advanced Patterns 

Distributed Locking 

def acquire_lock(lock_name, acquire_timeout=10):

identifier = str(uuid.uuid4())

end = time.time() + acquire_timeout

while time.time() < end:

if r.setnx(f"lock:{lock_name}", identifier):

r.expire(f"lock:{lock_name}", 10)

return identifier

time.sleep(0.001)

return None

def release_lock(lock_name, identifier):

#### Use Lua script for atomic release

script = """

if redis.call("get", KEYS[1]) == ARGV[1] then

return redis.call("del", KEYS[1])

else

return 0

end

"""

r.eval(script, 1, f"lock:{lock_name}", identifier)

Rate Limiting with Sorted Sets 

def is_rate_limited(user_id, max_requests=100, window_seconds=60):

key = f"ratelimit:{user_id}"

now = time.time()

#### Remove old entries

r.zremrangebyscore(key, 0, now - window_seconds)

#### Count current requests

if r.zcard(key) >= max_requests:

return True

#### Add current request

r.zadd(key, {now: now})

r.expire(key, window_seconds)

return False

Session Storage 

#### Store session with hash

def create_session(session_id, user_data, ttl=86400):

key = f"session:{session_id}"

r.hset(key, mapping={

'user_id': user_data['id'],

'username': user_data['username'],

'roles': json.dumps(user_data['roles']),

'ip': user_data['ip'],

'created_at': time.time()

})

r.expire(key, ttl)

def get_session(session_id):

key = f"session:{session_id}"

data = r.hgetall(key)

if data:

data['roles'] = json.loads(data['roles'])

return data

Performance Optimization 

Connection Pooling 

from redis.connection import ConnectionPool

#### Reuse connections across requests

pool = ConnectionPool(

host='localhost',

port=6379,

max_connections=50,

socket_timeout=5

)

r = redis.Redis(connection_pool=pool)

Pipeline / Batching 

#### Batch operations to reduce round trips

pipe = r.pipeline()

for user_id in user_ids:

pipe.get(f"user:{user_id}")

results = pipe.execute()

Monitoring 

#### Redis CLI monitoring

redis-cli info stats

#### Key metrics to watch

#### \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- hit_rate: keyspace_hits / (keyspace_hits + keyspace_misses)

#### \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- evicted_keys: keys evicted due to maxmemory

#### \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- maxmemory: configured memory limit

#### \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- connected_clients: active connections

Common Pitfalls 

| Pitfall | Consequence | Fix | |---------|-------------|-----| | No TTL | Memory exhaustion | Always set TTL | | Cache stampede | Overload database on miss | Use mutex locking | | Too-large values | Memory waste, slow serialization | Compress or split | | Hot keys | Single key becomes bottleneck | Shard or replicate | | Cache-aside without TTL | Stale data lives forever | Always set TTL | 

Summary 

Redis caching can dramatically improve application performance when the right pattern is applied. Use cache-aside as the default pattern with appropriate TTLs, implement write-through for consistency-critical data, use distributed locking for race conditions, and sorted sets for rate limiting. Monitor hit rates and eviction counts, and always set TTLs to prevent memory exhaustion.

**See also:** [Redis Caching Patterns](</en/database/redis-caching-patterns.html>), [Database Replication Patterns](</en/database/database-replication.html>), [NoSQL Databases Guide (MongoDB, DynamoDB, Firestore)](</en/database/nosql-databases-guide.html>).

**See also:** [Redis Caching Patterns](</en/database/redis-caching-patterns.html>), [Database Replication Patterns](</en/database/database-replication.html>), [Distributed Databases: Concepts and Implementation](</en/database/distributed-databases.html>)

**See also:** [Redis Caching Patterns](</en/database/redis-caching-patterns.html>), [Database Replication Patterns](</en/database/database-replication.html>), [Distributed Databases: Concepts and Implementation](</en/database/distributed-databases.html>)

**See also:** [Redis Caching Patterns](</en/database/redis-caching-patterns.html>), [Database Replication Patterns](</en/database/database-replication.html>), [Distributed Databases: Concepts and Implementation](</en/database/distributed-databases.html>)

**See also:** [Redis Caching Patterns](</en/database/redis-caching-patterns.html>), [Database Replication Patterns](</en/database/database-replication.html>), [Distributed Databases: Concepts and Implementation](</en/database/distributed-databases.html>)

**See also:** [Redis Caching Patterns](</en/database/redis-caching-patterns.html>), [Database Replication Patterns](</en/database/database-replication.html>), [Distributed Databases: Concepts and Implementation](</en/database/distributed-databases.html>)
