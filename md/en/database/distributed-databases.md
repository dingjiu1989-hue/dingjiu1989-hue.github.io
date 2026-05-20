---
title: "Distributed Databases: Concepts and Implementation"
description: "Explore Raft/Paxos consensus, gossip protocols, CRDTs, and the architectures behind Amazon Dynamo and Google Spanner."
date: 2026-03-28
board: database
url: https://dingjiu1989-hue.github.io/en/database/distributed-databases.html
---

# Distributed Databases: Concepts and Implementation

Distributed Database Architecture 

Distributed databases store data across multiple nodes, presenting a unified interface. They provide scalability and fault tolerance. 

CAP Theorem 

A distributed system can provide at most two of: Consistency, Availability, Partition Tolerance. Since partitions are inevitable, systems choose CP or AP. 

Consensus Algorithms 

Raft 

Raft is a consensus algorithm designed for understandability: 

class RaftNode:

def **init**(self):

self.state = "FOLLOWER"

self.current_term = 0

def start_election(self):

self.state = "CANDIDATE"

votes = 1

for peer in self.peers:

if peer.request_vote(self.current_term):

votes += 1

if votes > len(self.peers) // 2:

self.state = "LEADER"

Raft powers etcd, Consul, and MongoDB replication. 

Paxos 

Paxos is the original consensus algorithm. It is correct but difficult to understand. Used in Google Spanner and Chubby. 

Gossip Protocol 

Nodes periodically exchange state with random peers. Information spreads in O(log N) rounds. Used in Cassandra for membership detection and failure detection. 

Dynamo-Style Architecture 

Amazon DynamoDB and Cassandra prioritize availability: 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Cassandra: tunable consistency

INSERT INTO users (user_id, name) VALUES ('u1', 'Alice')

USING CONSISTENCY QUORUM;

SELECT * FROM users WHERE user_id = 'u1'

USING CONSISTENCY ONE;

Spanner-Style Architecture 

Google Spanner provides strong consistency globally using TrueTime (GPS + atomic clocks) for external consistency. 

Conclusion 

Choose Dynamo-style (Cassandra, DynamoDB) for availability and tunable consistency. Choose Spanner-style (Spanner, CockroachDB) for strong consistency. Choose Raft-based systems (etcd) for coordination. Consider your consistency requirements carefully.

**See also:** [Redis Caching Patterns](</en/database/redis-caching.html>), [Data Lake vs Data Warehouse vs Lakehouse](</en/database/data-lake-vs-warehouse.html>), [NoSQL Databases Guide (MongoDB, DynamoDB, Firestore)](</en/database/nosql-databases-guide.html>).

**See also:** [Data Lake vs Data Warehouse vs Lakehouse](</en/database/data-lake-vs-warehouse.html>), [Redis Caching Patterns](</en/database/redis-caching.html>), [SQL vs NoSQL Decision Guide](</en/database/sql-vs-nosql.html>)

**See also:** [Data Lake vs Data Warehouse vs Lakehouse](</en/database/data-lake-vs-warehouse.html>), [Redis Caching Patterns](</en/database/redis-caching.html>), [SQL vs NoSQL Decision Guide](</en/database/sql-vs-nosql.html>)

**See also:** [Data Lake vs Data Warehouse vs Lakehouse](</en/database/data-lake-vs-warehouse.html>), [Redis Caching Patterns](</en/database/redis-caching.html>), [SQL vs NoSQL Decision Guide](</en/database/sql-vs-nosql.html>)

**See also:** [Data Lake vs Data Warehouse vs Lakehouse](</en/database/data-lake-vs-warehouse.html>), [Redis Caching Patterns](</en/database/redis-caching.html>), [SQL vs NoSQL Decision Guide](</en/database/sql-vs-nosql.html>)

**See also:** [Data Lake vs Data Warehouse vs Lakehouse](</en/database/data-lake-vs-warehouse.html>), [Redis Caching Patterns](</en/database/redis-caching.html>), [SQL vs NoSQL Decision Guide](</en/database/sql-vs-nosql.html>)

**See also:** [OLTP vs OLAP: Workload Optimization](</en/database/oltp-vs-olap.html>), [ACID vs BASE Transactions](</en/database/acid-vs-base.html>), [Database Replication Patterns](</en/database/database-replication.html>)

**See also:** [OLTP vs OLAP: Workload Optimization](</en/database/oltp-vs-olap.html>), [ACID vs BASE Transactions](</en/database/acid-vs-base.html>), [Database Replication Patterns](</en/database/database-replication.html>)

**See also:** [OLTP vs OLAP: Workload Optimization](</en/database/oltp-vs-olap.html>), [ACID vs BASE Transactions](</en/database/acid-vs-base.html>), [Database Replication Patterns](</en/database/database-replication.html>)

**See also:** [OLTP vs OLAP: Workload Optimization](</en/database/oltp-vs-olap.html>), [ACID vs BASE Transactions](</en/database/acid-vs-base.html>), [Database Replication Patterns](</en/database/database-replication.html>)

**See also:** [OLTP vs OLAP: Workload Optimization](</en/database/oltp-vs-olap.html>), [ACID vs BASE Transactions](</en/database/acid-vs-base.html>), [Database Replication Patterns](</en/database/database-replication.html>)

**See also:** [OLTP vs OLAP: Workload Optimization](</en/database/oltp-vs-olap.html>), [ACID vs BASE Transactions](</en/database/acid-vs-base.html>), [Database Replication Patterns](</en/database/database-replication.html>)

**See also:** [OLTP vs OLAP: Workload Optimization](</en/database/oltp-vs-olap.html>), [ACID vs BASE Transactions](</en/database/acid-vs-base.html>), [Database Replication Patterns](</en/database/database-replication.html>)

**See also:** [OLTP vs OLAP: Workload Optimization](</en/database/oltp-vs-olap.html>), [ACID vs BASE Transactions](</en/database/acid-vs-base.html>), [Database Replication Patterns](</en/database/database-replication.html>)

**See also:** [OLTP vs OLAP: Workload Optimization](</en/database/oltp-vs-olap.html>), [ACID vs BASE Transactions](</en/database/acid-vs-base.html>), [Database Replication Patterns](</en/database/database-replication.html>)
