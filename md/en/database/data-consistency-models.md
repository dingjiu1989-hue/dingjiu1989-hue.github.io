---
title: "Data Consistency Models Explained"
description: "Learn about strong, eventual, causal, read-your-writes, and monotonic read consistency models plus CAP theorem trade-offs in practice."
date: 2026-05-12
board: database
url: https://dingjiu1989-hue.github.io/en/database/data-consistency-models.html
---

Data consistency models define the guarantees a distributed data system makes about when and in what order updates become visible to readers. Choosing the right consistency model is one of the most important decisions in distributed system design. This article explains the major consistency models and their practical implications.

## Strong Consistency (Linearizability)

Strong consistency guarantees that once a write completes, all subsequent reads (from any node) return that write's value. The system behaves as if there is a single copy of the data.

### How It Works

Strong consistency requires coordination between replicas before acknowledging a write. All replicas must agree on the order of operations.

```python
# Strong consistency write path
def write(key, value):
    # 1. Acquire a distributed lock or lease
    lock = acquire_distributed_lock(key)
    
    # 2. Write to all replicas
    replicas = write_to_all_replicas(key, value)
    
    # 3. Wait for acknowledgment from majority
    if len(replicas) >= len(all_replicas) // 2 + 1:
        release_lock(lock)
        return SUCCESS
    else:
        # Failed to reach quorum
        release_lock(lock)
        return ERROR

def read(key):
    # 1. Read from any replica (all return same value)
    return read_from_any_replica(key)
```

### When to Use Strong Consistency

- Financial transactions (account balances, payments).
- Inventory management (preventing overselling).
- Distributed locking and leader election.
- Any system where stale reads cause real harm.

### Trade-offs

Strong consistency requires coordination, which adds latency. Writes can only be acknowledged after reaching consensus (typically a majority quorum). During network partitions, the system must choose between availability and consistency — the C and A in CAP theorem.

## Eventual Consistency

Eventual consistency guarantees that if no new writes are made to an object, eventually all reads will return the last updated value. There is no bound on how long "eventually" takes.

### How It Works

Replicas accept writes independently and propagate changes asynchronously. Reads may return stale data.

```python
# Eventual consistency
def write(key, value):
    # Accept the write immediately
    local_store[key] = value
    # Propagate to other replicas asynchronously
    background_replicate(key, value)
    return SUCCESS

def read(key):
    # May return stale data
    return local_store.get(key)
```

### When to Use Eventual Consistency

- Social media feeds (slightly stale posts are acceptable).
- DNS records (propagation can take minutes).
- Product catalogs (price updates can propagate slowly).
- Analytics and logging (exact order does not matter).

### Convergence Mechanisms

Eventually consistent systems use conflict resolution to converge on a consistent state:

- **Last-writer-wins (LWW)**: Use timestamps to pick the latest write.
- **Conflict-free replicated data types (CRDTs)**: Data structures that merge automatically without conflicts.
- **Vector clocks**: Track causality to resolve conflicting updates deterministically.

```python
# Last-writer-wins conflict resolution
def resolve(key, value_1, timestamp_1, value_2, timestamp_2):
    if timestamp_1 > timestamp_2:
        return value_1
    return value_2
```

### Trade-offs

Eventual consistency provides high availability and low latency. Writes succeed even if some replicas are unavailable. However, applications must tolerate stale reads and handle conflicts.

## Causal Consistency

Causal consistency preserves the cause-and-effect relationships between operations. If operation A influences operation B (A causes B), then all observers see A before B. Operations that are causally unrelated can be seen in any order.

### How It Works

The system tracks causal dependencies using vector clocks or similar mechanisms.

```python
# Causal consistency with vector clocks
class VectorClock:
    def __init__(self):
        self.clock = defaultdict(int)
    
    def increment(self, node_id):
        self.clock[node_id] += 1
    
    def merge(self, other):
        for node, ts in other.clock.items():
            self.clock[node] = max(self.clock[node], ts)

def write_with_causality(key, value, vector_clock):
    # Track causal dependencies
    local_clock = vector_clock.copy()
    local_clock.increment(my_node_id)
    # Store with vector clock
    store(key, value, local_clock)
    return local_clock
```

### When to Use Causal Consistency

Causal consistency is useful when users interact with a system and expect their own actions to be reflected in order. For example, a user posts a comment (causally related to reading the post). Another user should see the post first, then the comment.

Amazon DynamoDB supports causal consistency through its "consistent reads" option. Apache Cassandra offers causal consistency through lightweight transactions.

## Read-Your-Writes Consistency

Read-your-writes guarantees that after a client writes a value, subsequent reads by the same client return that value. Other clients may still see the old value.

### How It Works

The system tracks the client's most recent writes. Read requests include a hint about the client's write timestamp.

```python
# Read-your-writes implementation
import threading

class SessionStore:
    def __init__(self):
        self.data = {}
        self.session_writes = threading.local()
    
    def write(self, key, value, user_session):
        self.data[key] = value
        user_session.last_write_ts[key] = time.time()
    
    def read(self, key, user_session):
        value = self.data.get(key)
        # Always route reads to a replica that has seen the latest write
        if key in user_session.last_write_ts:
            # Ensure we read from a replica with data >= write timestamp
            return read_from_replica_with_timestamp(
                key, user_session.last_write_ts[key]
            )
        return value
```

### When to Use Read-Your-Writes

- User profile updates (user edits profile and immediately sees the change).
- Shopping cart additions (user adds an item and sees it in the cart).
- Session management (user logs in and is immediately recognized).

## Monotonic Reads

Monotonic reads guarantee that once a client reads a value at time T, subsequent reads by the same client never return an older value.

### Why It Matters

Without monotonic reads, a user might refresh a page and see data from an earlier state. For example, a user sees a confirmed order, refreshes, and sees the order as pending. This is confusing and erodes trust.

### Implementation

Monotonic reads require the system to remember the timestamp of the most recent read by each client. Subsequent reads must go to a replica that has at least that timestamp.

## CAP Theorem in Practice

The CAP theorem states that a distributed system can provide at most two of three properties: Consistency, Availability, and Partition Tolerance.

### CAP in the Real World

Networks partition. Therefore, every distributed system must choose between consistency and availability when a partition occurs.

```
         Consistency
             |
        CP  |  CA
             |
   AP ------+------ Availability
           
Partition Tolerance (always required)
```

### CAP Configurations

**CP (Consistency + Partition Tolerance)**:
- Sacrifices availability during partitions.
- Systems: etcd, Zookeeper, HBase, MongoDB (default configuration).
- Use when consistency is non-negotiable: distributed locks, configuration management.

**AP (Availability + Partition Tolerance)**:
- Sacrifices consistency during partitions. Returns eventually consistent data.
- Systems: Cassandra, DynamoDB (default), CouchDB.
- Use when availability is paramount: user-facing applications, content delivery.

### PACELC Extension

PACELC extends CAP: during a Partition, choose Availability or Consistency. Else (E), choose Latency or Consistency.

This captures the trade-off even when there is no partition. Many systems trade consistency for lower latency under normal operation, then trade differently during partitions.

## Choosing the Right Model

| Model | Guarantee | Latency | Use Case |
|-------|-----------|---------|----------|
| Strong | All reads see all writes | High | Banking, inventory |
| Eventual | Converges over time | Low | Feeds, analytics |
| Causal | Causally related ops in order | Medium | Social apps, collaboration |
| Read-your-writes | Own writes visible | Low | User profiles |
| Monotonic reads | Never go back in time | Low | Any user-facing app |

### Practical Guidelines

1. **Use strong consistency only where necessary**. Most applications do not need linearizability for every operation. Strong consistency multiplies latency and reduces availability.

2. **Default to strong for critical paths, eventual for everything else**. Financial systems use strong consistency for transactions but may use eventual for historical reporting.

3. **Session-level guarantees cover most cases**. Read-your-writes and monotonic reads prevent the most confusing user-facing inconsistencies without the performance cost of global strong consistency.

4. **Understand your database's defaults**. Cassandra defaults to eventual. DynamoDB defaults to eventual with consistent-reads opt-in. Spanner provides strong consistency globally.

5. **Test with real partition scenarios**. Simulate network partitions in staging environments. Most consistency bugs surface first when replicas cannot communicate.

## Conclusion

Consistency models define the contract between the database and the application. Strong consistency provides familiar semantics at a performance cost. Eventual consistency enables scalability but requires careful application design. Causal and session-level consistency models offer intermediate guarantees that cover many real-world use cases. Understand the CAP theorem and its PACELC extension. Most importantly, choose the weakest consistency model your application can tolerate, and only use strong consistency where correctness demands it.
