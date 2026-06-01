---
title: "DynamoDB vs Cassandra: Data Model, Consistency, Scaling, and Cost"
description: "In-depth comparison of DynamoDB vs Cassandra covering data model, consistency levels, scaling strategies, query patterns, and cost considerations."
date: 2026-04-05
board: database
url: https://aidev.fit/en/database/dynamodb-vs-cassandra.html
---

# DynamoDB vs Cassandra: Data Model, Consistency, Scaling, and Cost

DynamoDB vs Cassandra: Data Model, Consistency, Scaling, and Cost 

DynamoDB and Cassandra are both distributed, horizontally scalable NoSQL databases. They share a common heritage (both influenced by Amazon's Dynamo paper), but their implementations and operational models differ significantly. 

Data Model 

DynamoDB 

DynamoDB uses tables with items (rows) and attributes (columns). Each item must have a partition key and optionally a sort key: 

// DynamoDB table: Users

// Partition key: user_id (String)

// Sort key: created_at (Number)

{

"user_id": "user_42",

"created_at": 1717000000,

"email": "alice@example.com",

"name": "Alice",

"address": {

"city": "New York",

"zip": "10001"

}

}

Key design rules: 

  * The partition key determines which partition stores the item.

  * Items with the same partition key are stored together, ordered by sort key.

  * Query operations require the partition key; optional sort key conditions.

  * Secondary indexes can be local (same partition key, different sort key) or global (different partition key).

## DynamoDB query

import boto3

client = boto3.client('dynamodb')

response = client.query(

TableName='Users',

KeyConditionExpression='user_id = :uid',

ExpressionAttributeValues={

':uid': {'S': 'user_42'}

}

)

Cassandra 

Cassandra uses tables with rows and columns, but the data model is designed around query patterns. The PRIMARY KEY defines partitioning and clustering: 

CREATE TABLE users_by_email (

email TEXT PRIMARY KEY,

user_id UUID,

name TEXT,

address TEXT

);

CREATE TABLE orders_by_user (

user_id UUID,

order_id UUID,

total DECIMAL,

created_at TIMESTAMP,

PRIMARY KEY (user_id, created_at, order_id)

) WITH CLUSTERING ORDER BY (created_at DESC);

Key design rules: 

  * The first column in PRIMARY KEY is the partition key.

  * Subsequent columns are clustering columns that define sort order within a partition.

  * You model tables around your access patterns (query-first design).

  * Denormalization is expected and encouraged.

## Cassandra query

from cassandra.cluster import Cluster

cluster = Cluster(['127.0.0.1'])

session = cluster.connect('mykeyspace')

rows = session.execute(

"SELECT * FROM orders_by_user WHERE user_id = %s",

(user_id,)

)

Consistency 

DynamoDB Consistency Levels 

| Level | Description | Cost | |-------|-------------|------| | Eventual | Reads may return stale data | 0.5 RCU per read | | Strong | Returns most up-to-date data | 1 RCU per read | | Transactional | Serial isolation for reads/writes | 2 RCU/WCU per operation | 

DynamoDB offers tunable consistency at the request level: 

## Eventually consistent read (cheaper)

response = client.get_item(

TableName='Users',

Key={'user_id': {'S': 'user_42'}},

ConsistentRead=False

)

## Strongly consistent read

response = client.get_item(

TableName='Users',

Key={'user_id': {'S': 'user_42'}},

ConsistentRead=True

)

Cassandra Consistency Levels 

Cassandra's consistency is tunable per query using the consistency level (CL): 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- QUORUM: majority of replicas must respond

SELECT * FROM users WHERE email = 'alice@example.com'

CONSISTENCY QUORUM;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- ONE: fastest, weakest guarantee

SELECT * FROM users WHERE email = 'alice@example.com'

CONSISTENCY ONE;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- ALL: strongest guarantee, slowest

SELECT * FROM users WHERE email = 'alice@example.com'

CONSISTENCY ALL;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- LOCAL_QUORUM: quorum within local datacenter

SELECT * FROM users WHERE email = 'alice@example.com'

CONSISTENCY LOCAL_QUORUM;

Scaling 

DynamoDB Scaling 

DynamoDB scales vertically by provisioning read and write capacity units (RCUs and WCUs). Auto-scaling adjusts capacity based on traffic: 

## Configure auto-scaling

client.update_table(

TableName='Users',

ProvisionedThroughput={

'ReadCapacityUnits': 100,

'WriteCapacityUnits': 100

}

)

## Or use on-demand mode (pay-per-request)

## No capacity planning needed, but higher per-request cost

DynamoDB partitions are invisible to users. The service automatically splits partitions when they exceed 10 GB or when throughput exceeds 3000 RCU or 1000 WCU per partition. 

Cassandra Scaling 

Cassandra scales horizontally by adding nodes. Data is distributed using consistent hashing: 

## cassandra.yaml

num_tokens: 256

initial_token:

replication_factor: 3

Adding a node: 

## Add node to cluster

nodetool status

nodetool join

## Rebalance data

nodetool rebuild

Scaling is linear: doubling nodes doubles throughput. No partitioning limits; the only constraint is disk space per node. 

Cost Comparison 

| Factor | DynamoDB | Cassandra | |--------|----------|-----------| | Infrastructure | Serverless (pay per request) | Self-managed or managed (AWS Keyspaces) | | Read cost | $0.00013 per RCU-hour | Server/cloud instance cost | | Write cost | $0.00065 per WCU-hour | Server/cloud instance cost | | Storage | $0.25 GB/month | EBS/gp3 cost (~$0.08/GB) | | Complex queries | Additional RCUs for scan | Single query cost | | Minimum cost | Free tier (25 GB, 25 RCU/WCU) | 3-node minimum cluster | 

When to Choose Which 

**Choose DynamoDB when** : 

  * You are already in AWS and want managed, serverless operations.

  * Traffic patterns are unpredictable (on-demand mode).

  * You need single-digit-millisecond latency at any scale.

  * You prioritize operations simplicity over cost optimization.

**Choose Cassandra when** : 

  * You run on-premises or multi-cloud.

  * Traffic is predictable and cost optimization matters at scale.

  * You need custom compaction and repair strategies.

  * You want to avoid vendor lock-in.

  * Your queries require complex clustering and ordering within partitions.

**Avoid both when** : 

  * You need complex joins, aggregations, or ad-hoc queries.

  * ACID transactions across multiple records are critical.

  * Your data model has many-to-many relationships.

DynamoDB and Cassandra are both excellent at what they do: high-throughput, scalable key-value and wide-column workloads. The choice depends on your operational preferences, cloud strategy, and cost sensitivity. For most applications starting out, a relational database with read replicas is the simpler and more flexible choice.
