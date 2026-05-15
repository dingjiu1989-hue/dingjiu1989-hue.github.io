---
title: "Consensus Algorithms: Paxos, Raft, Zab"
description: "Paxos, Raft, Zab consensus algorithms compared, practical considerations, and implementation choices for distributed systems"
date: 2026-05-12
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/consensus-algorithms.html
---

# Consensus Algorithms: Paxos, Raft, Zab

## Consensus Algorithms: Paxos, Raft, Zab

## Consensus Algorithms: Paxos, Raft, Zab

## Consensus Algorithms: Paxos, Raft, Zab

## Consensus Algorithms: Paxos, Raft, Zab

## Consensus Algorithms: Paxos, Raft, Zab

## Consensus Algorithms: Paxos, Raft, Zab

## Consensus Algorithms: Paxos, Raft, Zab

## Consensus Algorithms: Paxos, Raft, Zab

## Consensus Algorithms: Paxos, Raft, Zab

## Consensus Algorithms: Paxos, Raft, Zab

## Consensus Algorithms: Paxos, Raft, Zab

## Consensus Algorithms: Paxos, Raft, Zab

Consensus algorithms enable a group of distributed nodes to agree on a value despite failures. They are the foundation of replicated state machines, which underpin distributed databases, configuration stores, and coordination services. Three algorithms dominate production systems: Paxos, Raft, and Zab. Understanding their mechanics and tradeoffs is essential for architects designing fault-tolerant infrastructure. 

Paxos, published by Leslie Lamport in 1989, was the first practical consensus algorithm. It operates in phases: prepare, promise, accept, and learned. A proposer selects a proposal number and sends prepare requests to acceptors. If a majority of acceptors promise to accept the highest-numbered proposal they have seen, the proposer sends an accept request with its value. Once a majority accepts, the value is chosen. Multi-Paxos extends this to a sequence of values with a distinguished leader for efficiency. 

Paxos is notoriously difficult to understand and implement correctly. The algorithm is correct and proven, but subtle implementation details — handling of persistent state, leader election, log compaction — create many opportunities for bugs. The number of production-grade Paxos implementations is small, and most real systems use Paxos variants (Mencius, Fast Paxos, EPaxos) rather than classic Paxos. 

Raft, published by Diego Ongaro in 2013, was designed specifically to be understandable. It decomposes consensus into three subproblems: leader election, log replication, and safety. Leaders are elected through a randomized timeout mechanism. The leader accepts client requests, appends them to its log, and replicates them to followers. A majority of followers must acknowledge each entry before it is committed. Safety guarantees are clearly described through the leader completeness property and the election safety property. 

The most impactful innovation in Raft is the explicit leader election using randomized election timeouts. Each follower maintains an election timeout (150-300ms typically). If a follower does not receive a heartbeat from the leader within the timeout, it becomes a candidate, increments its term, and requests votes. The term number acts as a logical clock — older leaders cannot disrupt newer ones. Randomized timeouts make split votes rare and resolution fast. 

Zab (ZooKeeper Atomic Broadcast) powers Apache ZooKeeper. Like Raft, it uses a leader-based protocol with epochs (terms) and quorums. The key difference is that Zab focuses on total order broadcast of transactions rather than the replicated state machine abstraction. Zab guarantees that messages are delivered in the order they were proposed, and that the delivery order respects causality. This makes Zab particularly well-suited for coordination services where ordering guarantees matter. 

Algorithmic differences matter in practice. Raft's approach of committing entries through the current term's leader is cleaner than Zab's approach. Raft has a well-defined cluster membership change mechanism (joint consensus). Zab's recovery process during leader election is considered more complex. However, both algorithms provide equivalent safety guarantees under the same failure model. 

Practical considerations dominate implementation choices. Disk I/O for persistent log entries is the primary performance bottleneck. Batching and pipelining of log entries significantly improve throughput. The number of nodes in the consensus group affects performance — three nodes is minimum, five is typical for production, beyond seven rarely provides additional benefits due to communication overhead. 

Witnesses and observers extend consensus clusters without affecting quorum size. A witness node stores the log but does not vote. An observer node provides read-only access. These patterns allow read scaling without reducing write performance. 

Choosing between algorithms is less important than choosing a mature implementation. The differences between Raft, Zab, and Paxos are dwarfed by differences between well-tested and poorly-tested implementations. Production systems should use established implementations (etcd's Raft, ZooKeeper's Zab, CockroachDB's extended Raft) rather than custom implementations, no matter how clean the algorithm appears.

**See also:** [Leader Election in Distributed Systems](</en/architecture/leader-election.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>), [Caching Strategies](</en/architecture/cache-strategies.html>).

**See also:** [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>), [Leader Election in Distributed Systems](</en/architecture/leader-election.html>)

**See also:** [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>), [Leader Election in Distributed Systems](</en/architecture/leader-election.html>)
