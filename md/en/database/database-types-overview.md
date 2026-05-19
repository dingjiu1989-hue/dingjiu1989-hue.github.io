---
title: "Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector"
description: "Comprehensive overview of database types: relational, document, key-value, graph, time-series, and vector databases. Compare use cases and trade-offs."
date: 2026-04-03
board: database
url: https://dingjiu1989-hue.github.io/en/database/database-types-overview.html
---

# Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector

## Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector

### Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector

#### Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector

#### Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector

#### Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector

#### Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector

#### Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector

#### Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector

#### Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector

#### Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector

#### Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector

#### Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector

#### Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector

#### Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector

#### Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector

Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector 

Choosing the right database type is one of the most consequential architectural decisions. Each type optimizes for different access patterns, consistency guarantees, and scalability requirements. This article surveys the major database types and their ideal use cases. 

Relational Databases (PostgreSQL, MySQL, SQL Server) 

Relational databases organize data into tables with predefined schemas, linked by foreign keys. They provide ACID transactions and powerful querying via SQL. 

**Strengths** : 

  * ACID transactions with strong consistency guarantees.

  * Complex joins and aggregations across multiple tables.

  * Rich constraint system (foreign keys, unique, check).

  * Mature ecosystem and tooling.




**Weaknesses** : 

  * Schema changes require migrations.

  * Horizontal scaling is complex (sharding).

  * Rigid for highly varied, sparse data.




\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Typical relational model

CREATE TABLE users (

id BIGSERIAL PRIMARY KEY,

email TEXT UNIQUE NOT NULL,

created_at TIMESTAMPTZ DEFAULT NOW()

);

CREATE TABLE orders (

id BIGSERIAL PRIMARY KEY,

user_id BIGINT REFERENCES users(id),

total NUMERIC(10,2),

created_at TIMESTAMPTZ DEFAULT NOW()

);

SELECT u.email, COUNT(o.id) AS order_count

FROM users u

LEFT JOIN orders o ON o.user_id = u.id

GROUP BY u.email;

**Best for** : Financial systems, ERP, CRM, any application where data integrity is paramount. 

Document Databases (MongoDB, Couchbase) 

Document databases store semi-structured data in JSON-like documents. Schemas are flexible, and documents can have varying structures. 

**Strengths** : 

  * Schema flexibility: documents in the same collection can have different fields.

  * Native JSON support with rich query operations.

  * Horizontal scaling with native sharding.

  * Developer productivity for rapidly evolving models.




**Weaknesses** : 

  * Limited join capabilities (`$lookup` is less performant than SQL JOINs).

  * Multi-document transactions are newer and slower than ACID RDBMS.

  * No enforced schema means application-level validation is essential.




// MongoDB document model

db.users.insertOne({

_id: ObjectId(),

email: "alice@example.com",

profile: { name: "Alice", avatar: "avatar.jpg" },

orders: [

{ order_id: 1, total: 99.99, items: ["Widget"] }

]

});

**Best for** : Content management, catalogs, rapid prototyping, applications with evolving schemas. 

Key-Value Stores (Redis, DynamoDB, Riak) 

Key-value stores are the simplest database type. They store values accessed by a unique key, optimized for high-throughput, low-latency lookups. 

**Strengths** : 

  * Extremely fast reads and writes (sub-millisecond).

  * Simple data model with no schema.

  * Easy to scale horizontally.

  * Ideal for caching and session storage.




**Weaknesses** : 

  * No query capabilities beyond key lookups (in pure KV stores).

  * Limited to simple data structures (without secondary indexes).

  * Application must manage data relationships.




SET user:42 '{"email": "alice@example.com", "name": "Alice"}'

GET user:42

LPUSH recent_views:42 "product:100"

ZADD leaderboard 1000 "player_alice"

**Best for** : Caching, session management, real-time counters, pub/sub, rate limiting. 

Graph Databases (Neo4j, Amazon Neptune) 

Graph databases model data as nodes and edges, optimized for traversing relationships. 

**Strengths** : 

  * Relationship traversal is extremely fast, independent of graph size.

  * Natural modeling of highly connected data.

  * Pattern matching queries for complex relationships.




**Weaknesses** : 

  * Less efficient for non-graph workloads (simple aggregations).

  * Smaller ecosystem and fewer hosting options.

  * Requires learning specialized query languages (Cypher, SPARQL).




// Neo4j Cypher query

MATCH (u:User {email: "alice@example.com"})-[:FRIENDS_WITH]->(f:User)

WHERE (f)-[:PURCHASED]->(:Product {category: "Electronics"})

RETURN f.name

**Best for** : Social networks, recommendation engines, fraud detection, knowledge graphs. 

Time-Series Databases (TimescaleDB, InfluxDB, ClickHouse) 

Time-series databases optimize for append-heavy, time-ordered data with automatic retention and downsampling. 

**Strengths** : 

  * High ingestion throughput (millions of data points per second).

  * Automatic data retention and compaction.

  * Time-bucket aggregations and downsampling.

  * Compression ratios of 90%+.




**Weaknesses** : 

  * Less suitable for transactional workloads.

  * Joins and complex relationships are not a focus.

  * Query language varies widely (Flux vs SQL vs custom).




\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- TimescaleDB (SQL-based time-series)

SELECT time_bucket('1 hour', time) AS bucket,

AVG(temperature) AS avg_temp,

MAX(temperature) AS max_temp

FROM sensor_readings

WHERE sensor_id = 42

AND time > now() - INTERVAL '7 days'

GROUP BY bucket

ORDER BY bucket;

**Best for** : IoT, monitoring, observability, financial tick data, analytics. 

Vector Databases (pgvector, Pinecone, Milvus, Qdrant) 

Vector databases store and search high-dimensional vectors (embeddings) using similarity metrics. 

**Strengths** : 

  * Efficient approximate nearest neighbor (ANN) search.

  * Support for multiple distance metrics (cosine, Euclidean, dot product).

  * CRUD operations on vector embeddings.




**Weaknesses** : 

  * Orthogonal use case to traditional databases (complement, not replace).

  * Index build times can be significant for large datasets.

  * Requires vector embeddings from ML models.




\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- pgvector (PostgreSQL extension)

CREATE TABLE documents (

id BIGSERIAL PRIMARY KEY,

content TEXT,

embedding VECTOR(1536) -- OpenAI embedding dimension

);

CREATE INDEX ON documents USING IVFFLAT (embedding vector_cosine_ops);

SELECT content, 1 - (embedding <=> $1) AS similarity

FROM documents

ORDER BY embedding <=> $1

LIMIT 10;

**Best for** : Semantic search, RAG (retrieval-augmented generation), recommendation systems, image similarity. 

Multi-Model Databases 

Many modern databases support multiple models. PostgreSQL is the best example: with JSONB, PostGIS, pgvector, and extensions, it handles relational, document, geospatial, and vector workloads in a single system. 

Choosing the Right Database 

| If you need... | Consider... | |----------------|-------------| | Strong consistency, complex joins | PostgreSQL, MySQL | | Flexible schemas, rapid development | MongoDB | | Sub-millisecond lookups, caching | Redis | | Relationship-heavy traversal | Neo4j | | High-volume time-series | TimescaleDB, InfluxDB | | Semantic similarity search | pgvector, Pinecone, Milvus | | All of the above | PostgreSQL with extensions | 

The polyglot persistence approach uses multiple databases for different workloads. Start with a general-purpose database for most needs, and add specialized databases only when your requirements exceed what your primary database can provide.

**See also:** [NoSQL Databases Guide](</en/database/nosql-guide.html>), [SQL vs NoSQL in 2026](</en/database/sql-vs-nosql-2026.html>), [Couchbase Guide: N1QL, Document Model, Clustering, and Caching](</en/database/couchbase-guide.html>).

**See also:** [NoSQL Databases Guide](</en/database/nosql-guide.html>), [Couchbase Guide: N1QL, Document Model, Clustering, and Caching](</en/database/couchbase-guide.html>), [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>)

**See also:** [NoSQL Databases Guide](</en/database/nosql-guide.html>), [Couchbase Guide: N1QL, Document Model, Clustering, and Caching](</en/database/couchbase-guide.html>), [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>)

**See also:** [NoSQL Databases Guide](</en/database/nosql-guide.html>), [Couchbase Guide: N1QL, Document Model, Clustering, and Caching](</en/database/couchbase-guide.html>), [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>)

**See also:** [NoSQL Databases Guide](</en/database/nosql-guide.html>), [Couchbase Guide: N1QL, Document Model, Clustering, and Caching](</en/database/couchbase-guide.html>), [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>)

**See also:** [NoSQL Databases Guide](</en/database/nosql-guide.html>), [Couchbase Guide: N1QL, Document Model, Clustering, and Caching](</en/database/couchbase-guide.html>), [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>)
