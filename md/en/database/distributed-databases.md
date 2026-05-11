---
title: "Distributed Databases: Concepts and Implementation"
description: "Explore Raft/Paxos consensus, gossip protocols, CRDTs, and the architectures behind Amazon Dynamo and Google Spanner."
date: 2026-05-12
board: database
url: https://dingjiu1989-hue.github.io/en/database/distributed-databases.html
---

Distributed databases store data across multiple nodes while presenting a unified interface to applications. This article covers the fundamental concepts: consensus algorithms (Raft and Paxos), gossip protocols, conflict-free replicated data types (CRDTs), and the architectures behind two landmark distributed databases: Amazon Dynamo and Google Spanner.

## Consensus Algorithms: Paxos and Raft

Consensus algorithms enable a group of nodes to agree on a value despite failures. They are the foundation of replicated state machines in distributed databases.

### Paxos

Paxos was the first practical consensus algorithm, published by Leslie Lamport in 1998. It defines three roles:

- **Proposer**: Proposes a value.
- **Acceptor**: Votes on proposals.
- **Learner**: Learns the agreed value.

Paxos operates in two phases:

1. **Prepare phase**: The proposer sends a prepare request with a proposal number N to a majority of acceptors. Acceptors promise not to accept proposals numbered less than N and respond with the highest-numbered proposal they have accepted.

2. **Accept phase**: If the proposer receives responses from a majority, it sends an accept request with value V (the value from the highest-numbered previous proposal, or its own if none) to the acceptors. Acceptors accept the proposal unless they have promised to a higher number.

```python
# Simplified Paxos implementation
class PaxosNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.promised_n = 0
        self.accepted_n = 0
        self.accepted_value = None
    
    def handle_prepare(self, proposal_n, sender_id):
        if proposal_n > self.promised_n:
            self.promised_n = proposal_n
            return ("PROMISE", self.accepted_n, self.accepted_value)
        return ("REJECT",)
    
    def handle_accept(self, proposal_n, value):
        if proposal_n >= self.promised_n:
            self.promised_n = proposal_n
            self.accepted_n = proposal_n
            self.accepted_value = value
            return ("ACCEPTED",)
        return ("REJECT",)
```

Paxos is correct but notoriously difficult to understand and implement correctly. Most practical systems use variants or alternatives.

### Raft

Raft is a consensus algorithm designed for understandability. It was published by Diego Ongaro in 2014. Raft divides consensus into three subproblems:

1. **Leader election**: One node is elected leader. The leader handles all client requests.
2. **Log replication**: The leader replicates log entries to followers.
3. **Safety**: If a leader has applied a log entry at a given index, no other leader can apply a different entry at that index.

Raft uses random timeouts to elect leaders. Each node has a timer. When the timer expires on a follower, it becomes a candidate and starts an election.

```python
# Simplified Raft leader election
class RaftNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.state = "FOLLOWER"
        self.current_term = 0
        self.voted_for = None
        self.election_timeout = random.uniform(150, 300)  # milliseconds
    
    def start_election(self):
        self.state = "CANDIDATE"
        self.current_term += 1
        self.voted_for = self.node_id
        votes = 1  # Vote for self
        for peer in self.peers:
            response = peer.request_vote(self.current_term, self.node_id)
            if response["vote_granted"]:
                votes += 1
        if votes > len(self.peers) // 2:
            self.state = "LEADER"
            self.start_heartbeat()
```

Raft implementations power etcd, Consul, TiKV, and MongoDB's replication.

### Paxos vs Raft

| Aspect | Paxos | Raft |
|--------|-------|------|
| Understandability | Hard | Accessible |
| Leader-based | Implicit leader | Explicit leader election |
| Performance | Similar | Similar |
| Practical implementations | Google Chubby, Spanner | etcd, Consul, TiKV |

## Gossip Protocol

Gossip (epidemic) protocols spread information through a cluster by having each node periodically exchange state with a small set of random peers. Information spreads exponentially.

### How Gossip Works

```
Round 1: Node A infects nodes B and C
Round 2: B infects D and E, C infects F and G
Round 3: All 7 nodes have the information
```

```python
# Gossip protocol implementation
import random
import time

class GossipNode:
    def __init__(self, node_id, peers):
        self.node_id = node_id
        self.peers = peers
        self.state = {}
        self.version = {}
    
    def gossip_round(self):
        # Select N random peers to gossip with
        targets = random.sample(
            self.peers, 
            min(3, len(self.peers))
        )
        for target in targets:
            self.exchange_state(target)
    
    def exchange_state(self, target):
        # Send our state, receive theirs
        my_state = self.get_state_to_share()
        their_state = target.receive_state(my_state)
        # Merge: keep the higher version for each key
        for key, (value, version) in their_state.items():
            if key not in self.version or version > self.version[key]:
                self.state[key] = value
                self.version[key] = version
```

### Properties of Gossip

- **Scalability**: Information reaches all N nodes in O(log N) rounds.
- **Fault tolerance**: Nodes can join, leave, or fail without disrupting propagation.
- **Decentralization**: No central coordinator needed.
- **Eventual consistency**: All nodes eventually converge on the same state.

### Uses in Distributed Databases

- **Membership detection**: Cassandra and Consul use gossip to track which nodes are alive.
- **Metadata dissemination**: Distribute schema changes and configuration updates.
- **Failure detection**: Nodes that miss gossip rounds are suspected as failed.

## Conflict-Free Replicated Data Types (CRDTs)

CRDTs are data structures that can be updated concurrently on different replicas and automatically merge without conflicts. They provide strong eventual consistency.

### Types of CRDTs

**G-Counter (Grow-only Counter)**: A counter that only increases. Each replica owns one element in a vector. Increments only affect the replica's own element. Merge takes the element-wise maximum.

```python
class GCounter:
    def __init__(self, node_id, num_nodes):
        self.node_id = node_id
        self.counts = [0] * num_nodes
    
    def increment(self):
        self.counts[self.node_id] += 1
    
    def value(self):
        return sum(self.counts)
    
    def merge(self, other):
        for i in range(len(self.counts)):
            self.counts[i] = max(self.counts[i], other.counts[i])
```

**PN-Counter (Positive-Negative Counter)**: Supports both increments and decrements using two G-Counters.

**G-Set (Grow-only Set)**: Elements can only be added, never removed. Merge is set union.

**LWW-Register (Last-Writer-Wins Register)**: Each write is tagged with a timestamp. On conflict, the write with the highest timestamp wins.

```python
class LWWRegister:
    def __init__(self):
        self.value = None
        self.timestamp = 0
    
    def set(self, value, timestamp):
        if timestamp > self.timestamp:
            self.value = value
            self.timestamp = timestamp
    
    def merge(self, other):
        if other.timestamp > self.timestamp:
            self.value = other.value
            self.timestamp = other.timestamp
```

### CRDTs in Production

- **Redis CRDTs**: Redis Enterprise uses CRDTs for active-active geo-distribution.
- **Riak**: Distributed database built on CRDTs for conflict-free replication.
- **Automerge**: JavaScript CRDT library for collaborative applications.

## Amazon Dynamo-Style Architectures

Dynamo-style databases (DynamoDB, Cassandra, Riak) prioritize availability and partition tolerance over strong consistency.

### Key Design Decisions

1. **Consistent hashing**: Data is distributed across nodes using consistent hashing, which minimizes movement when nodes join or leave.
2. **N = 3 replication**: Each data item is replicated to N nodes. The coordinator forwards writes to all replicas.
3. **Tunable consistency**: Each read or write operation specifies its consistency level.

```python
# Dynamo-style write with tunable consistency
def dynamo_write(key, value, consistency_level="QUORUM"):
    # 1. Determine coordinator using consistent hashing
    coordinator = consistent_hash_ring.get_node(key)
    
    # 2. Forward write to all N replicas
    replicas = coordinator.get_preference_list(key, N=3)
    
    responses = []
    for replica in replicas:
        response = replica.write(key, value, version)
        responses.append(response)
    
    # 3. Wait for consistency level
    write_consistency = {
        "ONE": 1,
        "QUORUM": len(replicas) // 2 + 1,
        "ALL": len(replicas)
    }
    
    required = write_consistency[consistency_level]
    if sum(1 for r in responses if r["success"]) >= required:
        return SUCCESS
    return ERROR
```

### Cassandra Example

```sql
-- Cassandra: Tunable consistency on queries
-- Write with strong consistency
INSERT INTO users (user_id, name, email)
VALUES ('u1', 'Alice', 'alice@example.com')
USING CONSISTENCY QUORUM;

-- Read with eventual consistency (fastest)
SELECT * FROM users WHERE user_id = 'u1'
USING CONSISTENCY ONE;

-- Read with strong consistency
SELECT * FROM users WHERE user_id = 'u1'
USING CONSISTENCY ALL;
```

## Google Spanner-Style Architectures

Spanner is Google's globally distributed database that provides external consistency (linearizability) across data centers.

### Key Innovations

1. **TrueTime**: GPS and atomic clocks synchronize time across data centers with bounded clock uncertainty. TrueTime exposes a time interval `[earliest, latest]` for the current time.

2. **2PC + Paxos**: Spanner uses two-phase commit for transactions spanning multiple Paxos groups, with TrueTime timestamps for external consistency.

3. **Commit wait**: Spanner waits until the TrueTime uncertainty interval has passed before acknowledging a write. This ensures linearizability without locks.

```sql
-- Spanner: Globally consistent reads at a timestamp
SELECT * FROM orders
WHERE customer_id = 42
AND order_date >= '2026-01-01';
-- Automatically reads at a globally consistent timestamp
```

Spanner-based solutions include Cloud Spanner (Google Cloud) and CockroachDB (open-source, Spanner-inspired).

## Conclusion

Distributed databases rely on consensus algorithms (Raft/Paxos) for consistent replication, gossip protocols for decentralized communication, CRDTs for conflict-free merging, and careful architecture design that balances consistency, availability, and latency. Dynamo-style systems optimize for availability with tunable consistency. Spanner-style systems optimize for strong consistency with global distribution. Choosing the right approach depends on your workload's consistency requirements and latency tolerance.
