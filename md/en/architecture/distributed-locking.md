---
title: "Distributed Locking Mechanisms"
description: "Redis Redlock, ZooKeeper locks, lease mechanisms, fencing tokens, and consensus-based distributed locking patterns"
date: 2026-04-23
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/distributed-locking.html
---

# Distributed Locking Mechanisms

Distributed locking coordinates access to shared resources across multiple processes or machines. While single-node locking is well-understood, distributed environments introduce unique challenges: network partitions, process pauses, clock drift, and partial failures. Different locking approaches offer distinct tradeoffs between consistency, availability, and performance. 

Lease-based locking is the most common pattern. The lock has a time-to-live (TTL). The holder must periodically renew the lease before it expires. If the holder crashes or is partitioned, the lease expires and another process can acquire the lock. This prevents permanent lock holder failures. The critical implementation detail is choosing an appropriate lease duration — too short causes unnecessary lock releases, too long extends recovery time after holder failure. 

Redis-based locking is popular for its simplicity and performance. SET NX EX implements a basic distributed lock atomically — set the key only if it does not exist, with an expiration. The Redlock algorithm extends this to multiple Redis nodes for fault tolerance. However, Redlock has been subject to debate. Martin Kleppmann's analysis identified scenarios where clock drift or process pauses (garbage collection) can violate mutual exclusion guarantees. 

ZooKeeper provides a stronger consistency model through its ZAB consensus protocol. Locks are implemented using ephemeral sequential znodes. Each process creates an ephemeral znode under a lock path. The process with the lowest sequence number holds the lock. Others watch the previous znode and get notified when it disappears. This provides strict mutual exclusion without expiration timing issues — the lock is released when the session ends, which ZooKeeper detects through heartbeats. 

The ZooKeeper approach handles process pauses correctly. If a lock holder experiences a long garbage collection pause, ZooKeeper will detect the heartbeat timeout and release the lock. Other processes can then acquire it. The original holder, upon resuming, will discover its lock is gone and can react accordingly. This eliminates the clock drift vulnerability inherent in Redis-based approaches. 

Etcd locks follow a similar pattern to ZooKeeper. Etcd offers the concurrency package with mutexes that use lease-based mechanisms. The lock is associated with a lease, and the lease TTL is refreshed by the holder. Session expiry handles holder failures. Etcd's Raft-based consensus ensures strong consistency. For Kubernetes-native environments, etcd locks are the natural choice. 

Fencing tokens address the fundamental problem with distributed locks: preventing stale lock holders from accessing the shared resource. A fencing token is a monotonically increasing number issued to the lock holder. The holder presents this token with each write request to the resource. The resource rejects writes with outdated tokens. Without fencing, a process that holds a stale lock (due to pause or partition) could corrupt data when it resumes and writes to the resource. 

Implementing fencing requires the resource to check the token. For example, a database table could have a lock_token column. Each write includes the token, and the database rejects writes where the stored token is higher than the provided one. This ensures that even if a stale lock holder attempts to write, the write is rejected. 

The choice between locking mechanisms depends on consistency requirements. ZooKeeper and etcd provide strong consistency and proper fencing but require operating a consensus cluster. Redis provides high performance and availability but with weaker guarantees under failure scenarios. For idempotent operations where the cost of duplicate execution is acceptable, Redis locks suffice. For strictly exclusive access to shared resources, ZooKeeper or etcd with fencing tokens is necessary. 

Optimistic concurrency is an alternative worth considering. Rather than acquiring a distributed lock, the application performs its operation and checks for conflicts. If a conflict is detected (row version, etag), it retries. This avoids distributed locking entirely for workloads where contention is low. Many distributed systems find that optimistic approaches with appropriate retry logic outperform pessimistic locking at scale.

**See also:** [Rate Limiting Architecture](</en/architecture/rate-limiting-architecture.html>), [Saga vs Process Manager: Orchestration Patterns Compared](</en/architecture/saga-process-manager.html>), [Leader Election in Distributed Systems](</en/architecture/leader-election.html>).

**See also:** [Rate Limiting Architecture](</en/architecture/rate-limiting-architecture.html>), [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>)

**See also:** [Rate Limiting Architecture](</en/architecture/rate-limiting-architecture.html>), [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>)

**See also:** [Rate Limiting Architecture](</en/architecture/rate-limiting-architecture.html>), [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>)

**See also:** [Rate Limiting Architecture](</en/architecture/rate-limiting-architecture.html>), [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>)

**See also:** [Rate Limiting Architecture](</en/architecture/rate-limiting-architecture.html>), [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>)

**See also:** [Distributed ID Generation](</en/architecture/distributed-id.html>), [Distributed Tracing: Deep Dive](</en/architecture/distributed-tracing-deep.html>), [Event Collaboration: Choreography vs Orchestration](</en/architecture/event-collaboration.html>)

**See also:** [Distributed ID Generation](</en/architecture/distributed-id.html>), [Distributed Tracing: Deep Dive](</en/architecture/distributed-tracing-deep.html>), [Event Collaboration: Choreography vs Orchestration](</en/architecture/event-collaboration.html>)

**See also:** [Distributed ID Generation](</en/architecture/distributed-id.html>), [Distributed Tracing: Deep Dive](</en/architecture/distributed-tracing-deep.html>), [Event Collaboration: Choreography vs Orchestration](</en/architecture/event-collaboration.html>)

**See also:** [Distributed ID Generation](</en/architecture/distributed-id.html>), [Distributed Tracing: Deep Dive](</en/architecture/distributed-tracing-deep.html>), [Event Collaboration: Choreography vs Orchestration](</en/architecture/event-collaboration.html>)

**See also:** [Distributed ID Generation](</en/architecture/distributed-id.html>), [Distributed Tracing: Deep Dive](</en/architecture/distributed-tracing-deep.html>), [Event Collaboration: Choreography vs Orchestration](</en/architecture/event-collaboration.html>)

**See also:** [Distributed ID Generation](</en/architecture/distributed-id.html>), [Distributed Tracing: Deep Dive](</en/architecture/distributed-tracing-deep.html>), [Event Collaboration: Choreography vs Orchestration](</en/architecture/event-collaboration.html>)
