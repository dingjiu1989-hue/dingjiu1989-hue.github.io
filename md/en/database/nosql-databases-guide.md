---
title: "NoSQL Databases Guide (MongoDB, DynamoDB, Firestore)"
description: "A practical guide to NoSQL databases comparing MongoDB, DynamoDB, and Firestore for document storage, scalability, and query patterns."
date: 2025-12-23
board: database
url: https://dingjiu1989-hue.github.io/en/database/nosql-databases-guide.html
---

# NoSQL Databases Guide (MongoDB, DynamoDB, Firestore)

What Are NoSQL Databases? 

NoSQL databases are non-relational data stores designed for specific data models and access patterns that do not fit well in the relational paradigm. They trade strict ACID guarantees for scalability, flexibility, and performance at scale. 

NoSQL Database Types 

| Type | Examples | Best For | Avoid For | |------|----------|----------|-----------| | Document | MongoDB, Firestore | JSON-like data, flexible schemas | Complex joins | | Key-Value | Redis, DynamoDB | Simple lookups, caching | Multi-key queries | | Wide-Column | Cassandra, Bigtable | Time-series, write-heavy | Ad-hoc queries | | Graph | Neo4j, Dgraph | Relationships, recommendations | Simple CRUD | 

MongoDB 

MongoDB stores data as flexible JSON-like documents in collections. It is schema-less by design. 

Data Modeling 

// MongoDB document (embedded)

{

"_id": ObjectId("5f8c..."),

"username": "alice",

"email": "alice@example.com",

"profile": {

"display_name": "Alice",

"avatar_url": "https://...",

"bio": "Software engineer"

},

"addresses": [

{

"type": "home",

"street": "123 Main St",

"city": "San Francisco"

}

],

"created_at": ISODate("2026-01-15T10:30:00Z")

}

Query Examples 

// Basic queries

db.users.find({ email: "alice@example.com" })

db.users.find({ "addresses.city": "San Francisco" })

db.users.find({ created_at: { $gte: ISODate("2026-01-01") } })

// Aggregation pipeline

db.orders.aggregate([

{ $match: { status: "completed" } },

{ $group: { _id: "$customer_id", total: { $sum: "$amount" } } },

{ $sort: { total: -1 } },

{ $limit: 10 }

])

// Index creation

db.users.createIndex({ email: 1 }, { unique: true })

db.orders.createIndex({ customer_id: 1, created_at: -1 })

When to Use MongoDB 

  * Flexible or evolving schemas

  * Embedded data relationships (one-to-few)

  * Rapid prototyping

  * Document-oriented data (catalogs, content management)




DynamoDB 

DynamoDB is AWS's managed key-value and document database. It requires careful up-front schema design. 

Table Design 

// DynamoDB table with single-table design

// Partition Key: PK (string)

// Sort Key: SK (string)

// User entity

{ PK: "USER#alice", SK: "PROFILE", email: "alice@example.com", name: "Alice" }

// Order entity (access pattern: all orders for a user)

{ PK: "USER#alice", SK: "ORDER#2026-05-01#ORD001", amount: 100, status: "completed" }

{ PK: "USER#alice", SK: "ORDER#2026-05-15#ORD002", amount: 250, status: "pending" }

// Product entity (access pattern: get product by ID)

{ PK: "PROD#001", SK: "META", name: "Laptop", price: 1200 }

Query Patterns 

// AWS SDK v3

import { DynamoDBClient } from "@aws-sdk/client-dynamodb";

import { QueryCommand } from "@aws-sdk/lib-dynamodb";

const client = new DynamoDBClient({ region: "us-east-1" });

// Get user with all related data (single query)

const result = await client.send(new QueryCommand({

TableName: "AppTable",

KeyConditionExpression: "PK = :pk",

ExpressionAttributeValues: {

":pk": "USER#alice"

}

}));

// Query specific entity type

const orders = await client.send(new QueryCommand({

TableName: "AppTable",

KeyConditionExpression: "PK = :pk AND begins_with(SK, :sk)",

ExpressionAttributeValues: {

":pk": "USER#alice",

":sk": "ORDER#"

}

}));

When to Use DynamoDB 

  * Serverless applications

  * Predictable access patterns

  * High-scale workloads (millions of requests/second)

  * AWS-native architectures




Firestore 

Firestore is Google Cloud's NoSQL document database with real-time synchronization. 

Data Model 

import firebase_admin

from firebase_admin import firestore

db = firestore.client()

## Document reference

user_ref = db.collection('users').document('alice')

user_ref.set({

'email': 'alice@example.com',

'name': 'Alice',

'roles': ['admin', 'editor'],

'created_at': firestore.SERVER_TIMESTAMP

})

## Subcollection for hierarchical data

orders_ref = user_ref.collection('orders')

orders_ref.add({

'product': 'Laptop',

'amount': 1200,

'status': 'completed'

})

## Real-time listener

def on_snapshot(doc_snapshot, changes, read_time):

for change in changes:

print(f"Order changed: {change.document.id}")

user_ref.collection('orders').on_snapshot(on_snapshot)

When to Use Firestore 

  * Real-time applications (chat, live updates)

  * Mobile backends (offline support)

  * Google Cloud ecosystem




Decision Matrix 

| Factor | MongoDB | DynamoDB | Firestore | |--------|---------|----------|-----------| | Query flexibility | Excellent | Limited to key/GSI | Moderate | | Scalability | Manual sharding | Automatic | Automatic | | Consistency | Configurable | Eventual (default) | Strong | | Hosting | Self-managed or Atlas | AWS-managed | GCP-managed | | Real-time | Change streams | DynamoDB Streams | Native real-time | | Offline support | Limited | Limited | Excellent | | Pricing | Instance-based | Pay per request | Pay per read/write | 

Summary 

NoSQL databases excel at scale and flexibility but require different design thinking than relational databases. MongoDB offers the most flexible querying with embedded documents, DynamoDB provides unparalleled scalability with single-table design, and Firestore offers the best real-time and offline support. Choose based on your access patterns, scalability needs, and cloud ecosystem rather than treating NoSQL as a one-size-fits-all solution.

**See also:** [SQL vs NoSQL Decision Guide](</en/database/sql-vs-nosql.html>), [Document Databases: MongoDB, CouchDB, Firestore](</en/database/document-databases.html>), [OLTP vs OLAP: Workload Optimization](</en/database/oltp-vs-olap.html>).

**See also:** [SQL vs NoSQL Decision Guide](</en/database/sql-vs-nosql.html>), [OLTP vs OLAP: Workload Optimization](</en/database/oltp-vs-olap.html>), [Data Modeling Best Practices](</en/database/data-modeling.html>)

**See also:** [SQL vs NoSQL Decision Guide](</en/database/sql-vs-nosql.html>), [OLTP vs OLAP: Workload Optimization](</en/database/oltp-vs-olap.html>), [Data Modeling Best Practices](</en/database/data-modeling.html>)

**See also:** [SQL vs NoSQL Decision Guide](</en/database/sql-vs-nosql.html>), [OLTP vs OLAP: Workload Optimization](</en/database/oltp-vs-olap.html>), [Data Modeling Best Practices](</en/database/data-modeling.html>)

**See also:** [SQL vs NoSQL Decision Guide](</en/database/sql-vs-nosql.html>), [OLTP vs OLAP: Workload Optimization](</en/database/oltp-vs-olap.html>), [Data Modeling Best Practices](</en/database/data-modeling.html>)

**See also:** [SQL vs NoSQL Decision Guide](</en/database/sql-vs-nosql.html>), [OLTP vs OLAP: Workload Optimization](</en/database/oltp-vs-olap.html>), [Data Modeling Best Practices](</en/database/data-modeling.html>)

**See also:** [Building ETL Pipelines: A Practical Guide](</en/database/etl-pipelines.html>), [PostgreSQL vs MySQL vs SQLite in 2026: A Complete Database Guide for Developers](</en/database/postgresql-vs-mysql-2026.html>), [Database Indexing Strategies](</en/database/database-indexing.html>)

**See also:** [Building ETL Pipelines: A Practical Guide](</en/database/etl-pipelines.html>), [PostgreSQL vs MySQL vs SQLite in 2026: A Complete Database Guide for Developers](</en/database/postgresql-vs-mysql-2026.html>), [Database Indexing Strategies](</en/database/database-indexing.html>)

**See also:** [Building ETL Pipelines: A Practical Guide](</en/database/etl-pipelines.html>), [PostgreSQL vs MySQL vs SQLite in 2026: A Complete Database Guide for Developers](</en/database/postgresql-vs-mysql-2026.html>), [Database Indexing Strategies](</en/database/database-indexing.html>)

**See also:** [Building ETL Pipelines: A Practical Guide](</en/database/etl-pipelines.html>), [PostgreSQL vs MySQL vs SQLite in 2026: A Complete Database Guide for Developers](</en/database/postgresql-vs-mysql-2026.html>), [Database Indexing Strategies](</en/database/database-indexing.html>)

**See also:** [Building ETL Pipelines: A Practical Guide](</en/database/etl-pipelines.html>), [PostgreSQL vs MySQL vs SQLite in 2026: A Complete Database Guide for Developers](</en/database/postgresql-vs-mysql-2026.html>), [Database Indexing Strategies](</en/database/database-indexing.html>)

**See also:** [Building ETL Pipelines: A Practical Guide](</en/database/etl-pipelines.html>), [PostgreSQL vs MySQL vs SQLite in 2026: A Complete Database Guide for Developers](</en/database/postgresql-vs-mysql-2026.html>), [Database Indexing Strategies](</en/database/database-indexing.html>)

**See also:** [Building ETL Pipelines: A Practical Guide](</en/database/etl-pipelines.html>), [PostgreSQL vs MySQL vs SQLite in 2026: A Complete Database Guide for Developers](</en/database/postgresql-vs-mysql-2026.html>), [Database Indexing Strategies](</en/database/database-indexing.html>)

**See also:** [Building ETL Pipelines: A Practical Guide](</en/database/etl-pipelines.html>), [PostgreSQL vs MySQL vs SQLite in 2026: A Complete Database Guide for Developers](</en/database/postgresql-vs-mysql-2026.html>), [Database Indexing Strategies](</en/database/database-indexing.html>)

**See also:** [Building ETL Pipelines: A Practical Guide](</en/database/etl-pipelines.html>), [PostgreSQL vs MySQL vs SQLite in 2026: A Complete Database Guide for Developers](</en/database/postgresql-vs-mysql-2026.html>), [Database Indexing Strategies](</en/database/database-indexing.html>)

**See also:** [Building ETL Pipelines: A Practical Guide](</en/database/etl-pipelines.html>), [PostgreSQL vs MySQL vs SQLite in 2026: A Complete Database Guide for Developers](</en/database/postgresql-vs-mysql-2026.html>), [Database Indexing Strategies](</en/database/database-indexing.html>)

**See also:** [Building ETL Pipelines: A Practical Guide](</en/database/etl-pipelines.html>), [PostgreSQL vs MySQL vs SQLite in 2026: A Complete Database Guide for Developers](</en/database/postgresql-vs-mysql-2026.html>), [Database Indexing Strategies](</en/database/database-indexing.html>)
