---
title: "Couchbase Guide: N1QL, Document Model, Clustering, and Caching"
description: "Comprehensive guide to Couchbase: N1QL query language, document data model, clustering architecture, integrated caching, and real-world use cases."
date: 2026-05-12
board: database
url: https://dingjiu1989-hue.github.io/en/database/couchbase-guide.html
---

# Couchbase Guide: N1QL, Document Model, Clustering, and Caching

# Couchbase Guide: N1QL, Document Model, Clustering, and Caching

# Couchbase Guide: N1QL, Document Model, Clustering, and Caching

# Couchbase Guide: N1QL, Document Model, Clustering, and Caching

# Couchbase Guide: N1QL, Document Model, Clustering, and Caching

# Couchbase Guide: N1QL, Document Model, Clustering, and Caching

# Couchbase Guide: N1QL, Document Model, Clustering, and Caching

# Couchbase Guide: N1QL, Document Model, Clustering, and Caching

# Couchbase Guide: N1QL, Document Model, Clustering, and Caching

# Couchbase Guide: N1QL, Document Model, Clustering, and Caching

# Couchbase Guide: N1QL, Document Model, Clustering, and Caching

# Couchbase Guide: N1QL, Document Model, Clustering, and Caching

Couchbase Guide: N1QL, Document Model, Clustering, and Caching 

Couchbase is a distributed NoSQL document database that combines the flexibility of JSON documents with the query power of SQL. Its key differentiator is the integrated caching layer that automatically keeps frequently accessed data in memory. 

Document Data Model 

Couchbase stores data as JSON documents, organized into buckets (analogous to databases). Each document has a unique key and can contain arbitrarily nested JSON: 

{

"type": "user",

"user_id": "alice_42",

"email": "alice@example.com",

"name": "Alice Smith",

"addresses": [

{"type": "home", "city": "New York", "zip": "10001"},

{"type": "work", "city": "San Francisco", "zip": "94105"}

],

"preferences": {

"theme": "dark",

"notifications": true

},

"created_at": "2026-05-12T10:00:00Z"

}

Key Operations 

from couchbase.cluster import Cluster

from couchbase.options import ClusterOptions

from couchbase.auth import PasswordAuthenticator

cluster = Cluster('couchbase://localhost', ClusterOptions(

PasswordAuthenticator('admin', 'password')

))

bucket = cluster.bucket('myapp')

collection = bucket.default_collection()

# Create/Update

collection.upsert('user_alice_42', {

'type': 'user',

'email': 'alice@example.com',

'name': 'Alice Smith'

})

# Read

result = collection.get('user_alice_42')

user = result.content_as[dict]

# CAS (Compare-And-Swap) for optimistic locking

result = collection.get('user_alice_42')

cas = result.cas

user = result.content_as[dict]

user['name'] = 'Alice Jones'

collection.replace('user_alice_42', user, cas=cas)

N1QL (SQL for JSON) 

N1QL (pronounced "nickel") brings SQL semantics to JSON documents. It is Couchbase's most powerful feature: you get the flexibility of a document database with the query power of SQL. 

Basic Queries 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- SELECT with WHERE

SELECT name, email

FROM `myapp`

WHERE type = 'user' AND email LIKE '%@example.com'

ORDER BY name

LIMIT 10;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- JOIN across document types

SELECT u.name, o.total, o.created_at

FROM `myapp` u

JOIN `myapp` o ON KEYS ARRAY s.order_id FOR s IN u.orders END

WHERE u.type = 'user' AND u.user_id = 'alice_42';

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- UNNEST (flatten arrays)

SELECT u.name, addr.city, addr.zip

FROM `myapp` u

UNNEST u.addresses addr

WHERE u.type = 'user' AND addr.type = 'home';

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Aggregation

SELECT addr.city, COUNT(*) AS user_count

FROM `myapp` u

UNNEST u.addresses addr

WHERE u.type = 'user'

GROUP BY addr.city

ORDER BY user_count DESC;

Secondary Indexes 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Create primary index (required for N1QL queries on a bucket)

CREATE PRIMARY INDEX idx_primary ON `myapp`;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Create secondary index on specific fields

CREATE INDEX idx_users_email ON `myapp`(email)

WHERE type = 'user';

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Composite index

CREATE INDEX idx_users_city_created ON `myapp`(addresses[*].city, created_at)

WHERE type = 'user';

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Covering index (all needed fields)

CREATE INDEX idx_users_cover ON `myapp`(email, name, created_at)

WHERE type = 'user';

Architecture and Clustering 

Couchbase uses a distributed architecture with several key components: 

Data Service 

Stores and retrieves documents. Data is partitioned into 1024 vBuckets (virtual buckets) that are distributed across nodes. 

Query Service 

Processes N1QL queries. It can run on dedicated query nodes or co-located with data nodes. 

Index Service 

Maintains Global Secondary Indexes (GSI). Indexes can be replicated for high availability. 

Search Service 

Provides full-text search capabilities using FTS (based on Bleve). 

Cluster Management 

# Initialize cluster

couchbase-cli cluster-init -c 127.0.0.1 \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--cluster-username admin \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--cluster-password password \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--cluster-ramsize 2048 \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--cluster-index-ramsize 512 \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--services data,index,query

# Add node

couchbase-cli server-add -c 192.168.1.1 \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--server-add 192.168.1.2 \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--server-add-username admin \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--server-add-password password \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--services data,index,query

# Rebalance

couchbase-cli rebalance -c 192.168.1.1

Integrated Caching Layer 

Couchbase's most distinctive feature is its integrated cache. Every data node includes an in-memory cache (managed by the "couchbase" engine) that stores frequently accessed documents. 

Cache Behavior 

  * **Writes** are written to memory and queued for disk persistence.

  * **Reads** check the cache first (sub-millisecond for cache hits).

  * **Eviction** uses a variant of LRU when memory is full.

  * **Persistence** is asynchronous by default but configurable.




Memory Quotas 

# Set bucket memory quota (important tuning parameter)

couchbase-cli bucket-create -c 127.0.0.1 \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--bucket myapp \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--bucket-type couchbase \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--bucket-ramsize 1024 \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--bucket-priority high \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--bucket-eviction-policy fullEviction

Eviction policies: 

  * `valueOnly`: Evict document value, keep metadata (faster re-fetch on access).

  * `fullEviction`: Evict entire document (more memory savings but slower on cache miss).




Durability Settings 

# Wait for replication to N nodes before acknowledging

collection.upsert('doc_id', doc,

durability= Durability.MAJORITY_AND_PERSIST_TO_ACTIVE)

# Or use observe-based durability

collection.upsert('doc_id', doc,

durability_level= DurabilityLevel.PERSIST_TO_MAJORITY)

Use Cases 

Session Store 

Couchbase's sub-millisecond get/set operations and built-in TTL make it an excellent session store: 

# Set session with TTL (24 hours)

collection.upsert('session_token_xyz', {

'user_id': 'alice_42',

'created_at': '2026-05-12T10:00:00Z'

}, ttl=timedelta(hours=24))

User Profile Service 

JSON flexibility and N1QL queries support user profiles with varying fields: 

SELECT name, email, preferences

FROM `myapp`

WHERE type = 'user_profile' AND META().id IN $user_ids;

Catalog / Product Database 

Couchbase is widely used for e-commerce catalogs where products have varying attributes: 

SELECT name, price, attributes

FROM `myapp`

WHERE type = 'product'

AND category = 'electronics'

AND price BETWEEN 100 AND 500

ORDER BY price

LIMIT 20;

Couchbase vs Alternatives 

| Feature | Couchbase | MongoDB | Redis | |---------|-----------|---------|-------| | Query language | N1QL (SQL-like) | MQL (JSON-based) | Command-based | | Caching | Built-in (cache-first) | WiredTiger cache | Pure in-memory | | Durability | Tunable (async to sync) | Journal + replication | AOF/RDB persistence | | Cross-datacenter | XDCR (bidirectional) | Replica sets | Active-Active | | Full-text search | Built-in (Bleve) | Built-in (Atlas Search) | RediSearch module | 

Couchbase fills a unique niche: a document database with SQL querying and built-in caching. It is a strong choice when you need low-latency document access combined with ad-hoc query capabilities, and when you want to simplify your architecture by avoiding a separate cache layer.

**See also:** [NoSQL Databases Guide](</en/database/nosql-guide.html>), [Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector](</en/database/database-types-overview.html>), [SQL vs NoSQL in 2026](</en/database/sql-vs-nosql-2026.html>).

**See also:** [Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector](</en/database/database-types-overview.html>), [NoSQL Databases Guide](</en/database/nosql-guide.html>), [DynamoDB vs Cassandra: Data Model, Consistency, Scaling, and Cost](</en/database/dynamodb-vs-cassandra.html>)
