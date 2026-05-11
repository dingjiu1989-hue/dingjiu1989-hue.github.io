---
title: "MongoDB vs PostgreSQL"
description: "An in-depth comparison of MongoDB and PostgreSQL covering performance, features, use cases, and migration strategies."
date: 2026-05-11
board: database
url: https://dingjiu1989-hue.github.io/en/database/mongodb-vs-postgresql.html
---

## The Two Giants

PostgreSQL and MongoDB are the most popular open-source databases in their respective categories. PostgreSQL is the most advanced open-source relational database, while MongoDB is the leading document database. Both are mature, well-supported, and capable of handling production workloads.

## Architecture Comparison

| Feature | PostgreSQL | MongoDB |
|---------|-----------|---------|
| Data model | Relational (tables, rows) | Document (JSON-like BSON) |
| Schema | Fixed with constraints | Flexible, schema-less |
| Query language | SQL | MQL (MongoDB Query Language) |
| Storage engine | Custom (multiple options) | WiredTiger |
| Index types | B-tree, Hash, GiST, GIN, BRIN | B-tree, Text, Geospatial, TTL |
| Replication | Streaming (WAL) | Replica set (oplog) |
| Sharding | No (3rd party Citus) | Native (config servers + mongos) |

## Performance Comparison

### Read Performance

```sql
-- PostgreSQL: indexed read
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'alice@example.com';
-- Index Only Scan: ~0.3ms (with index)
```

```javascript
// MongoDB: indexed read
db.users.find({ email: "alice@example.com" }).explain("executionStats");
// IXSCAN: ~0.3ms (with index)
```

For simple point lookups, both databases perform similarly. For complex analytical queries, PostgreSQL's query optimizer generally outperforms MongoDB's aggregation pipeline.

### Write Performance

MongoDB typically has a write throughput advantage due to its document model and eventual consistency options:

```javascript
// MongoDB: high-throughput writes
const bulkOps = [];
for (const event of eventBatch) {
    bulkOps.push({ insertOne: { document: event } });
}
db.events.bulkWrite(bulkOps, { ordered: false });
// ~100,000 inserts/second on modest hardware
```

```sql
-- PostgreSQL: batched inserts
INSERT INTO events (type, data, created_at)
SELECT * FROM unnest($1::text[], $2::jsonb[], $3::timestamptz[]);
-- ~20,000 inserts/second (with WAL)
```

## Feature Comparison

### PostgreSQL Advantages

**Advanced Indexing**:

```sql
-- Partial index: only index active users
CREATE INDEX idx_active_users ON users(email) WHERE status = 'active';

-- Expression index: index a function result
CREATE INDEX idx_users_name_lower ON users(LOWER(name));

-- Covering index: index-only scans
CREATE INDEX idx_users_email ON users(email) INCLUDE (name, avatar_url);
```

**Full-Text Search**:

```sql
-- Built-in full-text search (no Elasticsearch needed for basic cases)
SELECT title, ts_rank(to_tsvector('english', body), query) AS rank
FROM articles, to_tsquery('english', 'database & optimization') query
WHERE to_tsvector('english', body) @@ query
ORDER BY rank DESC
LIMIT 10;
```

**JSON Support**:

```sql
-- PostgreSQL has excellent JSON support
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    data JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index JSON fields
CREATE INDEX idx_events_type ON events((data->>'type'));
CREATE INDEX idx_events_gin ON events USING GIN(data jsonb_path_ops);

-- Query JSON
SELECT * FROM events WHERE data @> '{"type": "page_view", "user_id": "123"}';
```

### MongoDB Advantages

**Native Document Model**:

```javascript
// Read an entire document tree in one query
const order = db.orders.findOne({ _id: "order_123" });
// order contains customer info, items, shipping, payment — all in one document
// No JOINs needed

// Update nested fields
db.orders.updateOne(
    { _id: "order_123" },
    { $set: { "shipping_address.city": "New York" } }
);
```

**Aggregation Pipeline**:

```javascript
// Powerful data processing pipeline
db.orders.aggregate([
    { $match: { status: "completed", created_at: { $gte: startDate } } },
    { $unwind: "$items" },
    { $group: {
        _id: "$items.category",
        total_revenue: { $sum: { $multiply: ["$items.price", "$items.quantity"] } },
        total_orders: { $addToSet: "$_id" }
    }},
    { $project: {
        category: "$_id",
        revenue: "$total_revenue",
        order_count: { $size: "$total_orders" }
    }},
    { $sort: { revenue: -1 } }
]);
```

**Geo Queries**:

```javascript
// Find nearby places
db.places.createIndex({ location: "2dsphere" });
db.places.find({
    location: {
        $near: {
            $geometry: { type: "Point", coordinates: [-73.97, 40.77] },
            $maxDistance: 1000  // meters
        }
    }
});
```

## Operational Considerations

| Aspect | PostgreSQL | MongoDB |
|--------|-----------|---------|
| Setup complexity | Simple | Moderate (sharding) |
| Monitoring | pg_stat_statements, pgBadger | Ops Manager, Atlas |
| Backup | pg_dump, pgBackRest | mongodump, Ops Manager |
| High availability | Patroni, repmgr | Replica set (automatic failover) |
| Cloud managed | RDS, Cloud SQL, Supabase | Atlas, Cosmos DB, MongoDB on AWS |

## Migration Between Them

### PostgreSQL to MongoDB

```javascript
// Denormalize relational data into documents
// Source (PostgreSQL):
//   users: id, name, email
//   addresses: id, user_id, street, city
//
// Target (MongoDB):
{
    _id: ObjectId(),
    name: "Alice",
    email: "alice@example.com",
    addresses: [
        { street: "123 Main St", city: "San Francisco" }
    ]
}
```

### MongoDB to PostgreSQL

```python
# Extract nested documents to relational tables
for doc in mongo_collection.find():
    pg_cursor.execute(
        "INSERT INTO users (id, name, email) VALUES (%s, %s, %s)",
        [doc['_id'], doc['name'], doc['email']]
    )
    for addr in doc.get('addresses', []):
        pg_cursor.execute(
            "INSERT INTO addresses (user_id, street, city) VALUES (%s, %s, %s)",
            [doc['_id'], addr['street'], addr['city']]
        )
```

## When to Choose Each

| Scenario | Choose |
|----------|--------|
| Complex queries and reporting | PostgreSQL |
| Strict data integrity | PostgreSQL |
| Flexible schema | MongoDB |
| Hierarchical data | MongoDB |
| ACID transactions across tables | PostgreSQL |
| High-volume writes | MongoDB |
| Full-text search | PostgreSQL (basic), Elasticsearch (advanced) |
| Geospatial queries | Both (good in both) |
| Polyglot data types | PostgreSQL |

## Summary

PostgreSQL is the better default choice for most applications due to its superior query optimizer, data integrity features, and advanced indexing. MongoDB excels when you need flexible schemas, high write throughput, and naturally hierarchical data. PostgreSQL has narrowed the gap considerably with its JSONB support, while MongoDB has added ACID transactions. Choose based on your specific data model and query patterns rather than generic popularity.
