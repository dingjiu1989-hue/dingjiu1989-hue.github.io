---
title: "System Design Fundamentals 2026: A Developer Guide to Scalable Applications"
description: "System design concepts every developer should know — microservices vs monolith, CQRS, event-driven architecture, database scaling, caching, and real-world trade-offs."
date: 2025-12-25
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/system-design-fundamentals-2026.html
---

# System Design Fundamentals 2026: A Developer Guide to Scalable Applications

System Design Fundamentals 2026: A Developer's Guide to Scalable Applications 

System design interviews get all the attention, but the real value is in day-to-day decisions: should you extract that service? Add a cache? Reach for a message queue? This guide covers the fundamental patterns, their trade-offs, and the concrete decisions you'll face building production systems in 2026. 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--- 

1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Microservices vs Monolith vs Modular Monolith 

The "monolith vs microservices" debate has matured. In 2026, the winner is often somewhere in between. 

| Architecture | Team Size | Deploy Frequency | Best For | |---|---|---|---| | **Monolith** | 1–5 | Low | Prototypes, internal tools, MVPs | | **Modular Monolith** | 3–15 | Medium | Most business apps, teams that aren't Spotify-sized | | **Microservices** | 10+ per service | High | Large orgs with clear domain boundaries | 

The Modular Monolith Sweet Spot 

A modular monolith is a single deployable unit with **strict module boundaries**. Modules communicate through well-defined interfaces but share the same process and database. 

┌─────────────────────────────────────┐

│ Modular Monolith │

│ ┌──────────┐ ┌──────────┐ │

│ │ Orders │ │ Billing │ │

│ │ Module │──│ Module │ │

│ └────┬─────┘ └────┬─────┘ │

│ │ │ │

│ ┌────▼──────────────▼─────┐ │

│ │ Shared Kernel │ │

│ │ (DB, messaging, auth) │ │

│ └─────────────────────────┘ │

└─────────────────────────────────────┘

**When to extract a service** : When two conditions are met — the module has a clear bounded context (DDD), and you need independent scaling or deploy velocity that the monolith can't provide. 

**Rule of thumb** : Don't break your monolith until it hurts. Premature microservices add distributed transaction complexity, network latency, and operational overhead. Start modular, extract surgically. 

Real-World Decision Tree 

Monolith → Modular Monolith → Selective Extraction → Full Microservices

MVP Phase: Monolith

10k users/5 devs: Modular monolith

100k users: Extract payments (PCI scope)

1M users: Extract search (separate scale)

10M users: Extract recommendations (different stack)

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--- 

2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. CQRS: Command Query Responsibility Segregation 

CQRS separates **reads** from **writes** — different models, sometimes different databases. 

When CQRS Makes Sense 

  * Your read queries are complex and don't map well to your write model (e.g., reporting dashboards)

  * Your read and write workloads have different scaling requirements (10:1 read-to-write ratio)

  * You need different data shapes for reading vs writing (e.g., write normalized, read denormalized)




A Simple CQRS Implementation 

## \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--- Command Side (Writes) ---

class CreateOrderCommand:

def **init**(self, user_id: str, items: list):

self.user_id = user_id

self.items = items

class OrderCommandHandler:

def handle(self, cmd: CreateOrderCommand) -> str:

## Validate business rules

order = Order.create(cmd.user_id, cmd.items)

order.save() # Write to transactional DB (PostgreSQL)

event_bus.publish("order.created", {"order_id": order.id})

return order.id

## \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--- Query Side (Reads) ---

class OrderQueryHandler:

def get_order_summary(self, user_id: str) -> dict:

## Read from denormalized read model (could be a different DB)

return read_db.query(

"SELECT * FROM order_summaries WHERE user_id = :uid",

{"uid": user_id}

)

CQRS Without Event Sourcing 

You don't need event sourcing to use CQRS. The most common pattern is: 

  * **Write** to a normalized PostgreSQL table



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Sync** (or async via CDC) to a read-optimized table 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Read** from the read table 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Write model: normalized

CREATE TABLE orders (

id UUID PRIMARY KEY,

user_id UUID NOT NULL,

status VARCHAR(20) NOT NULL,

total_cents BIGINT NOT NULL,

created_at TIMESTAMP DEFAULT NOW()

);

CREATE TABLE order_items (

id UUID PRIMARY KEY,

order_id UUID REFERENCES orders(id),

product_id UUID NOT NULL,

quantity INT NOT NULL,

unit_price_cents BIGINT NOT NULL

);

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Read model: denormalized for fast queries

CREATE TABLE order_summaries (

order_id UUID PRIMARY KEY,

user_id UUID NOT NULL,

status VARCHAR(20) NOT NULL,

item_count INT NOT NULL,

total_cents BIGINT NOT NULL,

product_names TEXT[] NOT NULL,

created_at TIMESTAMP DEFAULT NOW()

);

When NOT to Use CQRS 

  * Your app is a simple CRUD interface with no complex queries

  * You don't need separate read/write scaling

  * Your team is small and you can't justify the infrastructure overhead




\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--- 

3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Event-Driven Architecture 

Event-driven systems decouple producers from consumers. When an event happens, interested services react. 

Core Concepts 

┌──────────┐ Event Bus ┌──────────────┐

│ Producer │─────(Kafka/RMQ)────▶│ Consumer 1 │

│ (Orders) │ │ (Analytics) │

└──────────┘ └──────────────┘

───────────────▶┌──────────────┐

│ Consumer 2 │

│ (Email) │

└──────────────┘

Message Queue Comparison 

| Feature | Kafka | RabbitMQ | SQS | |---|---|---|---| | **Delivery** | At-least-once, exactly-once (idempotent) | At-most-once, at-least-once | At-least-once | | **Ordering** | Per-partition guaranteed | Not guaranteed (unless single queue) | FIFO queue (limited throughput) | | **Persistence** | Disk-based, configurable retention | Memory + disk (lazy queues) | Automatic (up to 14 days) | | **Throughput** | Millions/sec | Thousands/sec | Unlimited (soft limit 300/s for FIFO) | | **Consumer model** | Pull-based (offset tracking) | Push or pull | Pull-based (long polling) | | **Use case** | Event sourcing, stream processing, logs | Task queues, RPC, work queues | Serverless workloads, simple decoupling | | **Operational cost** | High (requires Zookeeper/KRaft) | Medium | Zero (fully managed) | 

Kafka in Practice: The Url Shortener Click Stream 

## Producer — emit click events

def record_click(short_code: str, ip: str, user_agent: str):

producer.send(

topic="url_clicks",

key=short_code.encode(), # Same key → same partition → ordered

value={

"short_code": short_code,

"ip": ip,

"user_agent": user_agent,

"timestamp": int(time.time()),

}

)

## Consumer 1 — real-time analytics (e.g., update Redis counters)

def consume_clicks_for_analytics():

for message in consumer:

click = message.value

redis.zincrby("popular_urls:today", 1, click["short_code"])

redis.incr(f"url:{click['short_code']}:clicks")

## Consumer 2 — store raw clicks in data warehouse

def consume_clicks_for_storage():

for message in consumer:

warehouse.insert_one(message.value)

Event Sourcing: Storing State as Events 

Instead of storing the current state, event sourcing stores a sequence of state-changing events. The current state is derived by replaying them. 

## Events (immutable facts)

events = [

{"type": "AccountCreated", "data": {"user_id": "u1", "email": "a@b.com"}},

{"type": "EmailVerified", "data": {"user_id": "u1", "verified_at": "2026-05-01"}},

{"type": "PasswordChanged", "data": {"user_id": "u1", "changed_at": "2026-05-10"}},

]

## Derive current state by replaying events

def get_account_state(events):

state = {"email": None, "email_verified": False, "password_hash": None}

for event in events:

if event["type"] == "AccountCreated":

state["email"] = event["data"]["email"]

elif event["type"] == "EmailVerified":

state["email_verified"] = True

return state

**Trade-offs** : Event sourcing gives you a complete audit trail and time travel, but makes querying awkward (you need projections) and schema evolution painful. 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--- 

4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Database Scaling Strategies 

Read Replicas 

The simplest scaling strategy: one primary handles writes, replicas handle reads. 

┌─────────────┐

│ Primary DB │◀── Writes

└──────┬──────┘

│

┌────────────────┼────────────────┐

│ │ │

┌────▼─────┐ ┌─────▼────┐ ┌───────▼──┐

│ Replica 1│ │ Replica 2│ │ Replica 3│

│ (Reads) │ │ (Reads) │ │ (Reads) │

└──────────┘ └──────────┘ └──────────┘

## Using read/write separation in code

class DatabaseRouter:

def **init**(self):

self.primary = create_engine(PRIMARY_URL)

self.replicas = [create_engine(url) for url in REPLICA_URLS]

self.replica_index = 0

def write(self, query, params=None):

with self.primary.begin() as conn:

return conn.execute(query, params or {})

def read(self, query, params=None):

## Round-robin across replicas

replica = self.replicas[self.replica_index % len(self.replicas)]

self.replica_index += 1

return replica.execute(query, params or {})

**Replication lag** is the #1 problem. If your app reads immediately after a write (e.g., "you just placed an order" page), route that read to the primary. This is called **read-after-write consistency**. 

async def create_order_and_redirect(user_id: str, items: list):

order_id = db.write("INSERT INTO orders ... RETURNING id")

## Read-after-write: force this read to the primary

order = db.read_from_primary(

"SELECT * FROM orders WHERE id = :oid", {"oid": order_id}

)

return redirect(f"/orders/{order_id}")

Sharding (Horizontal Partitioning) 

Split data across databases by a shard key. 

| Strategy | Shard Key | Pros | Cons | |---|---|---|---| | **Hash-based** | hash(user_id) % N | Even distribution | Resharding is painful (need consistent hashing) | | **Range-based** | user_id 1–10000 → shard 1 | Range queries work | Hot spots possible | | **Directory-based** | Lookup table maps key → shard | Flexible, re-shardable | Extra lookup, single point of failure | 

## Consistent hashing — minimizes re-sharding

class ConsistentHashRing:

def **init**(self, nodes: list, replicas: int = 150):

self.ring = {}

for node in nodes:

for i in range(replicas):

key = self._hash(f"{node}:{i}")

self.ring[key] = node

self.sorted_keys = sorted(self.ring.keys())

def get_node(self, key: str) -> str:

if not self.ring:

return None

hash_val = self._hash(key)

for ring_key in self.sorted_keys:

if hash_val <= ring_key:

return self.ring[ring_key]

return self.ring[self.sorted_keys[0]]

def _hash(self, key: str) -> int:

return int(hashlib.md5(key.encode()).hexdigest(), 16)

Partitioning (Within a Database) 

Split a table into smaller physical chunks. PostgreSQL declarative partitioning: 

CREATE TABLE events (

event_id UUID NOT NULL,

occurred_at TIMESTAMP NOT NULL,

payload JSONB

) PARTITION BY RANGE (occurred_at);

CREATE TABLE events_2026_q1

PARTITION OF events

FOR VALUES FROM ('2026-01-01') TO ('2026-04-01');

CREATE TABLE events_2026_q2

PARTITION OF events

FOR VALUES FROM ('2026-04-01') TO ('2026-07-01');

Partition pruning means queries with `WHERE occurred_at >= '2026-04-01'` only scan relevant partitions. 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--- 

5\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Caching Layers 

The Three Cache Levels 

CDN ─── Application Cache (Redis) ─── In-Memory Cache (Local)

│ │ │

│ Expensive to fill Fastest access

│ Shared across servers 1-5μs per get

│ 50-500μs per get Lost on restart

Cache Strategies 

| Strategy | Read Behavior | Write Behavior | Best For | |---|---|---|---| | **Cache Aside** | Check cache → miss → load from DB → populate cache | Write to DB, invalidate cache key | Most general-purpose apps | | **Read Through** | Cache is authoritative; loads from DB on miss | Write through to DB; cache handles loading | When cache handles persistence | | **Write Through** | — | Write to cache first, then DB synchronously | Apps needing strong consistency | | **Write Behind** | — | Write to cache, async flush to DB | High-write-throughput apps | | **Write Around** | — | Write to DB only; cache populated on subsequent read | Write-once, read-rarely data | 

Cache Aside — The Default Choice 

async def get_user_profile(user_id: str) -> dict:

cache_key = f"user:profile:{user_id}"

## 1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Try cache

cached = await redis.get(cache_key)

if cached:

return json.loads(cached)

## 2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Cache miss — load from database

profile = await db.query(

"SELECT * FROM user_profiles WHERE user_id = :uid",

{"uid": user_id}

)

if profile:

## 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Populate cache with TTL

await redis.setex(cache_key, 300, json.dumps(profile))

return profile

async def update_user_profile(user_id: str, data: dict):

## 1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Write to database

await db.execute(

"UPDATE user_profiles SET name = :name WHERE user_id = :uid",

{"uid": user_id, "name": data["name"]}

)

## 2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Invalidate cache (don't update it — let next read re-populate)

await redis.delete(f"user:profile:{user_id}")

Write Behind — For High-Volume Writes 

## Batch writer process — runs every 5 seconds

write_buffer = []

async def write_to_cache(key: str, value: dict):

write_buffer.append((key, value))

if len(write_buffer) >= 100:

await flush_buffer()

async def flush_buffer():

async with db.transaction():

for key, value in write_buffer:

await db.execute(

"UPSERT INTO ... VALUES (:k, :v)",

{"k": key, "v": json.dumps(value)}

)

write_buffer.clear()

## Start background flusher

async def periodic_flush():

while True:

await asyncio.sleep(5)

if write_buffer:

await flush_buffer()

**Write behind risk** : if the process crashes before the flush, data is lost. Use a persistent queue (Kafka) for critical writes. 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--- 

6\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. CAP Theorem Explained Practically 

CAP says a distributed data store can provide at most two of three guarantees: **Consistency** , **Availability** , and **Partition Tolerance**. 

What CAP Actually Means 

  * **C (Consistency)** : Every read sees the most recent write (or an error)

  * **A (Availability)** : Every request gets a non-error response (not necessarily the latest data)

  * **P (Partition Tolerance)** : System continues working despite network failures




The Key Insight 

You **must** choose CP or AP. Partition tolerance is non-negotiable in distributed systems — networks WILL fail. 

| System | Choice | Real-World | |---|---|---| | PostgreSQL (single node) | CA | No distribution, no partition | | PostgreSQL + synchronous replication | CP | Writes wait for replicas | | Cassandra | AP | Writes always succeed, reads may be stale | | DynamoDB (eventual consistency) | AP | Default read is eventually consistent | | DynamoDB (strongly consistent) | CP | Higher latency, lower availability | | MongoDB (replica set) | CP | Writes acknowledged by majority | 

Practical CAP Decisions 

## AP choice — accept stale reads for availability

async def get_product_stock(product_id: str) -> int:

## Read from nearest replica, may be stale

return await replica.query(

"SELECT stock FROM products WHERE id = :pid",

{"pid": product_id}

)

## CP choice — accept slower reads for consistency

async def get_product_stock_cp(product_id: str) -> int:

## Read from primary, always latest

return await primary.query(

"SELECT stock FROM products WHERE id = :pid",

{"pid": product_id}

)

**Rule of thumb** : Use eventual consistency for read-heavy, non-critical data (product descriptions, view counts). Use strong consistency for financial data, inventory, and auth tokens. 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--- 

7\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Load Balancing Strategies 

Layer 4 vs Layer 7 

| Aspect | Layer 4 (TCP) | Layer 7 (HTTP) | |---|---|---| | **Routing based on** | IP + port | URL, headers, cookies, body | | **Performance** | Very fast | Slower (inspects payload) | | **Features** | Simple forwarding | Content-based routing, rate limiting | | **Examples** | HAProxy (TCP mode), AWS NLB | NGINX, Envoy, AWS ALB | 

Algorithms 

## Round Robin — predictable, but doesn't handle different load sizes

servers = ["app-01", "app-02", "app-03"]

next_server = current_index % len(servers)

current_index += 1

## Least Connections — better for variable request durations

def least_connections(servers: list) -> str:

return min(servers, key=lambda s: s.active_connections)

## IP Hash — session persistence without cookies

def ip_hash(client_ip: str, servers: list) -> str:

hash_val = int(hashlib.md5(client_ip.encode()).hexdigest(), 16)

return servers[hash_val % len(servers)]

Health Checks: The Bare Minimum 

┌──────────┐ /healthz ┌──────────┐

│ LB │───────────────▶│ App-01 │──▶ Returns 200

│ │ ├──────────┤

│ │───────────────▶│ App-02 │──▶ Returns 500 (removed from pool)

│ │ ├──────────┤

│ │───────────────▶│ App-03 │──▶ Returns 200

└──────────┘ └──────────┘

## /healthz endpoint

@app.get("/healthz")

async def health_check():

## Check critical dependencies

db_ok = await check_database()

cache_ok = await check_redis()

if db_ok and cache_ok:

return {"status": "ok"}

return {"status": "degraded"}, 503

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--- 

8\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. API Gateway Patterns 

An API gateway sits between clients and your services, handling cross-cutting concerns. 

┌─────────────────┐

│ API Gateway │

│ ┌─────────────┐ │

Client ──────────┼─▶ Auth │ │

│ └─────────────┘ │

│ ┌─────────────┐ │

│─▶ Rate Limit │ │──▶ Service A

│ └─────────────┘ │

│ ┌─────────────┐ │──▶ Service B

│─▶ Routing │ │

│ └─────────────┘ │──▶ Service C

│ ┌─────────────┐ │

│─▶ Logging │ │

│ └─────────────┘ │

└─────────────────┘

What the Gateway Handles 

## Before gateway — each service handles auth

@app.route("/api/orders")

class OrdersResource:

def get(self):

token = request.headers["Authorization"]

user = verify_token(token) # Duplicated in EVERY service

## After gateway — auth is centralized

## Service code is simpler:

@app.route("/api/orders")

class OrdersResource:

def get(self):

user = request.environ["X-Authenticated-User"] # Set by gateway

return get_orders(user["id"])

Gateway vs Service Mesh 

| Concern | API Gateway | Service Mesh (e.g., Istio) | |---|---|---| | **Client-facing** | Yes (edge) | No (internal) | | **Auth** | Token verification, API keys | mTLS between services | | **Rate limiting** | Per-client, per-endpoint | Per-service | | **Routing** | URL-based | Traffic splitting, canary | | **Location** | Edge proxy | Sidecar per pod | 

**Recommendation** : Start with an API gateway. Add a service mesh only when you have dozens of services and need advanced traffic management. 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--- 

9\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Circuit Breaker and Resilience Patterns 

The Circuit Breaker Pattern 

class CircuitBreaker:

STATES = ["CLOSED", "OPEN", "HALF_OPEN"]

def **init**(self, failure_threshold=5, recovery_timeout=30):

self.failure_count = 0

self.failure_threshold = failure_threshold

self.recovery_timeout = recovery_timeout # seconds

self.state = "CLOSED"

self.last_failure_time = None

async def call(self, func, fallback=None):

if self.state == "OPEN":

if time.time() - self.last_failure_time > self.recovery_timeout:

self.state = "HALF_OPEN"

else:

return await fallback() if fallback else None

try:

result = await func()

if self.state == "HALF_OPEN":

self.state = "CLOSED"

self.failure_count = 0

return result

except Exception as e:

self.failure_count += 1

self.last_failure_time = time.time()

if self.failure_count >= self.failure_threshold:

self.state = "OPEN"

return await fallback() if fallback else None

## Usage

cb = CircuitBreaker(failure_threshold=3, recovery_timeout=60)

async def get_recommendations(user_id: str):

return await cb.call(

func=lambda: recommendations_service.fetch(user_id),

fallback=lambda: {"recommendations": [], "source": "fallback"}

)

Other Resilience Patterns 

| Pattern | What It Does | |---|---| | **Retry with backoff** | Exponential backoff + jitter to avoid thundering herd | | **Timeout** | Hard timeout per request (e.g., 5s) to prevent cascading | | **Bulkhead** | Isolate resources — limit connections per service | | **Rate limiting** | Token bucket or leaky bucket per client | | **Dead letter queue** | Failed messages go to a DLQ for manual inspection | 

## Retry with exponential backoff and jitter

async def retry_with_backoff(func, max_retries=3):

for attempt in range(max_retries):

try:

return await func()

except (ConnectionError, TimeoutError) as e:

if attempt == max_retries - 1:

raise

sleep_time = (2 ** attempt) + random.random() # exp + jitter

await asyncio.sleep(sleep_time)

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--- 

10\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Real Example: Design a URL Shortener 

Let's design bit.ly/tinyurl step by step. 

Requirements 

  * Generate a short, unique code for any URL

  * Redirect to the original URL when the short code is accessed

  * Track click analytics (count, referrer, timestamp)

  * Handle 10M URLs, 100M redirects/day




Step 1: URL Encoding 

BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def encode_base62(num: int) -> str:

if num == 0:

return BASE62[0]

result = []

while num > 0:

result.append(BASE62[num % 62])

num //= 62

return ''.join(reversed(result))

def decode_base62(code: str) -> int:

result = 0

for char in code:

result = result * 62 + BASE62.index(char)

return result

## Example: 7 chars of base62 = 62^7 ≈ 3.5 trillion unique URLs

encode_base62(123456789) # "8m0Kx"

Step 2: Architecture 

┌────────────┐

│ Analytics │

│ (Kafka → │

│ ClickHouse)│

└─────────────┘

▲

│ (async)

┌──────────┐ POST /shorten ┌──────────────────────────┐

│ Client │────────────────────▶│ API Gateway │

│ │ │ ┌────────────────────┐ │

│ │ GET /abc123 │ │ Write Service │──┼──▶ PostgreSQL (URLs)

│ │────────────────────▶│ │ (generate code) │ │

│ │ │ └────────────────────┘ │

│ │ 301 Redirect │ ┌────────────────────┐ │

│ │◀────────────────────│ │ Read Service │ │

│ │ │ │ (resolve + cache) │──┼──▶ Redis (cache)

│ │ │ └────────────────────┘ │

│ │ │ ┌────────────────────┐ │

│ │ │ │ Click Logger │──┼──▶ Kafka

│ │ │ └────────────────────┘ │

└──────────┘ └──────────────────────────┘

Step 3: Data Model 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- PostgreSQL

CREATE TABLE urls (

id BIGSERIAL PRIMARY KEY,

short_code VARCHAR(10) UNIQUE NOT NULL,

original_url TEXT NOT NULL,

user_id UUID, -- nullable for anonymous users

created_at TIMESTAMP DEFAULT NOW(),

expires_at TIMESTAMP -- nullable

);

CREATE INDEX idx_short_code ON urls(short_code);

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Redis cache

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Key: "url:abc123" → Value: "https://example.com/long-url"

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- TTL: 24 hours

Step 4: Write Path 

@app.post("/shorten")

async def shorten_url(url: str, user_id: str = None):

## 1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Check if URL already shortened (optimization)

existing = await db.query(

"SELECT short_code FROM urls WHERE original_url = :url AND user_id = :uid",

{"url": url, "uid": user_id}

)

if existing:

return {"short_url": f"https://short.domain/{existing['short_code']}"}

## 2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Generate unique code

short_code = await generate_unique_code()

## 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Store in DB

await db.execute(

"INSERT INTO urls (short_code, original_url, user_id) VALUES (:c, :u, :uid)",

{"c": short_code, "u": url, "uid": user_id}

)

## 4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Warm the cache

await redis.setex(f"url:{short_code}", 86400, url)

return {"short_url": f"https://short.domain/{short_code}"}

async def generate_unique_code() -> str:

for _ in range(3): # Retry on collision

code = encode_base62(random.randint(0, 62**7 - 1))

exists = await db.query(

"SELECT 1 FROM urls WHERE short_code = :c", {"c": code}

)

if not exists:

return code

raise Exception("Collision rate too high — increase code length")

Step 5: Read Path (The Hot Path — Handles 100M req/day) 

@app.get("/{short_code}")

async def redirect(short_code: str, request: Request):

## 1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Try cache (99% hit rate with 24h TTL)

original_url = await redis.get(f"url:{short_code}")

if not original_url:

## 2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Cache miss — hit DB

row = await db.query(

"SELECT original_url FROM urls WHERE short_code = :c",

{"c": short_code}

)

if not row:

raise HTTPException(status_code=404)

original_url = row["original_url"]

## 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Populate cache with TTL

await redis.setex(f"url:{short_code}", 86400, original_url)

## 4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Log click asynchronously (don't block the redirect)

click_event = {

"short_code": short_code,

"ip": request.client.host,

"user_agent": request.headers.get("user-agent"),

"referer": request.headers.get("referer"),

"timestamp": int(time.time()),

}

## Fire and forget — queue to Kafka

await click_producer.send("url_clicks", click_event)

## 5\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Redirect (301 for permanent, 302 for analytics)

return RedirectResponse(url=original_url, status_code=301)

Step 6: Scale Considerations 

  * **Read replicas** for URL resolution (read-heavy: 10:1 read-to-write ratio)

  * **Redis cluster** for cache (with consistent hashing)

  * **Kafka partitions** by short_code for ordered click logs

  * **Batch write** click analytics to ClickHouse every 30 seconds

  * **CDN** for the redirect page itself (not the API — API calls are cheap)




\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--- 

11\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Async Processing Patterns 

The Problem: Synchronous Chains 

Client ──▶ Service A ──▶ Service B ──▶ Service C ──▶ Response

500ms 800ms 200ms = 1.5s total

The client waits 1.5 seconds for something that doesn't need a response. 

Solution: Decouple with Async 

Client ──▶ Service A ──▶ Response (immediate: "Accepted")

│

▼

Queue (Kafka/SQS)

│

┌──────┴──────┐

▼ ▼

Service B Service C

(email) (generate PDF)

Pattern 1: Fire and Forget 

@app.post("/api/send-email")

async def send_email(request: EmailRequest):

## Validate request

if not request.valid:

raise HTTPException(400)

## Queue the work — don't wait

await email_queue.send({

"to": request.to,

"template": request.template,

"data": request.data,

})

## Return immediately

return {"status": "queued", "message_id": str(uuid.uuid4())}

Pattern 2: Polling with Status 

@app.post("/api/report/generate")

async def generate_report(params: ReportParams):

report_id = str(uuid.uuid4())

await report_queue.send({"report_id": report_id, "params": params})

return {"report_id": report_id, "status_url": f"/api/report/{report_id}/status"}

@app.get("/api/report/{report_id}/status")

async def check_status(report_id: str):

status = await redis.get(f"report:{report_id}:status")

if status == "ready":

return {"status": "ready", "url": f"/api/report/{report_id}/download"}

return {"status": "processing"}

Pattern 3: Webhook Callback 

Instead of polling, have the worker call a URL when done: 

async def process_report(report_id: str, params: dict, callback_url: str):

## ... generate report ...

await save_report(report_id, result)

## Notify caller

if callback_url:

await httpx.post(callback_url, json={

"report_id": report_id,

"status": "completed",

"download_url": f"/api/report/{report_id}/download",

})

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--- 

12\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Common Anti-Patterns 

1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. The Distributed Monolith 

You split into microservices but deploy them together and fail to maintain boundaries. Every service calls every other service directly. Schema changes ripple across the system. 

**Signs** : A "simple" feature touches 5+ services. You need to coordinate deploys across teams. Services share a database — or god forbid, tables. 

**Fix** : Enforce bounded contexts. Each service owns its data. Communication is via APIs or events, not shared databases. 

2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Over-Engineering from Day One 

"Let's use Kafka, Cassandra, Kubernetes, and event sourcing" — for a blog with 10 visitors/day. 

**Fix** : Start with the simplest thing that works. A monolith with PostgreSQL and Redis will handle 99% of applications. Extract services when there's a proven need. 

3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Synchronous Coupling via HTTP 

Service A ──HTTP──▶ Service B ──HTTP──▶ Service C ──HTTP──▶ Service D

If one service is slow, the whole chain slows. Latency adds up. Failures cascade. 

**Fix** : Use async communication for non-critical paths. Use circuit breakers for critical sync calls. Prefer eventual consistency over synchronous coordination. 

4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. The Shared Database 

Two services reading/writing the same database table. Schema changes require coordination. One service can deadlock the other. 

**Fix** : Each service owns its data. Share via APIs or events, not databases. 

5\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Ignoring Caching 

Every request hits the database. Database CPU is 90%. Response times are 200ms for data that changes hourly. 

**Fix** : Add Redis. Cache the most frequently accessed data. Even a 60-second cache TTL reduces DB load by 95% for read-heavy workloads. 

6\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. The N+1 Query Problem 

## Anti-pattern: N+1 queries

def get_orders_with_items(user_id: str):

orders = db.query("SELECT * FROM orders WHERE user_id = :uid", {"uid": user_id})

for order in orders:

## One query PER order — terrible!

order["items"] = db.query(

"SELECT * FROM order_items WHERE order_id = :oid",

{"oid": order["id"]}

)

return orders

## Fix: single query with JOIN

def get_orders_with_items_fixed(user_id: str):

return db.query("""

SELECT o.id, o.total, oi.product_id, oi.quantity

FROM orders o

LEFT JOIN order_items oi ON oi.order_id = o.id

WHERE o.user_id = :uid

""", {"uid": user_id})

7\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. No Monitoring / No Observability 

"Everything looks fine" — until users complain that the site is slow and you have no idea why. 

**Baseline monitoring** : Request latency (p50, p95, p99), error rate, throughput, CPU/memory per service. Structured logging with correlation IDs. Distributed tracing for async flows. 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--- 

Summary: Key Decisions for 2026 

| Decision | Default Choice | Upgrade When | |---|---|---| | **Architecture** | Modular monolith | Team >15 or clear independent scale need | | **Database** | PostgreSQL | Read replicas at 10k reads/s, sharding at 100k | | **Cache** | Redis (cache aside) | Write-behind for high-throughput writes | | **Queue** | SQS (serverless) → RabbitMQ (control) → Kafka (streaming) | Scale-dependent | | **Async** | Fire and forget for non-critical | Polling → Webhooks as needs grow | | **API Gateway** | NGINX / Traefik | Envoy / Kong for advanced routing | | **Resilience** | Circuit breaker + timeout | Bulkhead + rate limiting at scale | 

The best system design is the one that solves today's problem without creating tomorrow's nightmare. Start simple, measure everything, extract with surgical precision, and never optimize for a scale you haven't reached.

**See also:** [Domain-Driven Design Fundamentals](</en/architecture/ddd-guide.html>), [Event-Driven Architecture Patterns: Kafka, RabbitMQ, SQS, and EventBridge Compared](</en/tech/event-driven-architecture-guide.html>), [Serverless Architecture Patterns](</en/architecture/serverless-architecture.html>).

**See also:** [Event-Driven Architecture Patterns: Kafka, RabbitMQ, SQS, and EventBridge Compared](</en/tech/event-driven-architecture-guide.html>), [Domain-Driven Design Fundamentals](</en/architecture/ddd-guide.html>), [System Design Interview Prep: Complete Developer Guide (2026)](</en/tech/system-design-interview-guide.html>)

**See also:** [Event-Driven Architecture Patterns: Kafka, RabbitMQ, SQS, and EventBridge Compared](</en/tech/event-driven-architecture-guide.html>), [Domain-Driven Design Fundamentals](</en/architecture/ddd-guide.html>), [System Design Interview Prep: Complete Developer Guide (2026)](</en/tech/system-design-interview-guide.html>)

**See also:** [Event-Driven Architecture Patterns: Kafka, RabbitMQ, SQS, and EventBridge Compared](</en/tech/event-driven-architecture-guide.html>), [Domain-Driven Design Fundamentals](</en/architecture/ddd-guide.html>), [System Design Interview Prep: Complete Developer Guide (2026)](</en/tech/system-design-interview-guide.html>)

**See also:** [Event-Driven Architecture Patterns: Kafka, RabbitMQ, SQS, and EventBridge Compared](</en/tech/event-driven-architecture-guide.html>), [Domain-Driven Design Fundamentals](</en/architecture/ddd-guide.html>), [System Design Interview Prep: Complete Developer Guide (2026)](</en/tech/system-design-interview-guide.html>)

**See also:** [Event-Driven Architecture Patterns: Kafka, RabbitMQ, SQS, and EventBridge Compared](</en/tech/event-driven-architecture-guide.html>), [Domain-Driven Design Fundamentals](</en/architecture/ddd-guide.html>), [System Design Interview Prep: Complete Developer Guide (2026)](</en/tech/system-design-interview-guide.html>)

**See also:** [Modular Monolith Architecture](</en/architecture/modular-monolith.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>), [Microservices vs Monolith 2026](</en/architecture/microservices-vs-monolith-2026.html>)

**See also:** [Modular Monolith Architecture](</en/architecture/modular-monolith.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>), [Microservices vs Monolith 2026](</en/architecture/microservices-vs-monolith-2026.html>)

**See also:** [Modular Monolith Architecture](</en/architecture/modular-monolith.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>), [Microservices vs Monolith 2026](</en/architecture/microservices-vs-monolith-2026.html>)

**See also:** [Modular Monolith Architecture](</en/architecture/modular-monolith.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>), [Microservices vs Monolith 2026](</en/architecture/microservices-vs-monolith-2026.html>)

**See also:** [Modular Monolith Architecture](</en/architecture/modular-monolith.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>), [Microservices vs Monolith 2026](</en/architecture/microservices-vs-monolith-2026.html>)

**See also:** [Modular Monolith Architecture](</en/architecture/modular-monolith.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>), [Microservices vs Monolith 2026](</en/architecture/microservices-vs-monolith-2026.html>)

**See also:** [Modular Monolith Architecture](</en/architecture/modular-monolith.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>), [Microservices vs Monolith 2026](</en/architecture/microservices-vs-monolith-2026.html>)

**See also:** [Modular Monolith Architecture](</en/architecture/modular-monolith.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>), [Microservices vs Monolith 2026](</en/architecture/microservices-vs-monolith-2026.html>)

**See also:** [Modular Monolith Architecture](</en/architecture/modular-monolith.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>), [Microservices vs Monolith 2026](</en/architecture/microservices-vs-monolith-2026.html>)

**See also:** [Modular Monolith Architecture](</en/architecture/modular-monolith.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>), [Microservices vs Monolith 2026](</en/architecture/microservices-vs-monolith-2026.html>)

**See also:** [Modular Monolith Architecture](</en/architecture/modular-monolith.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>), [Microservices vs Monolith 2026](</en/architecture/microservices-vs-monolith-2026.html>)
