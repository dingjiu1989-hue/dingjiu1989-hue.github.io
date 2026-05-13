---
title: "Two-Phase Commit (2PC) for Distributed Transactions"
description: "Two-phase commit protocol: coordinator, prepare/commit phases, failure scenarios, XA protocol, and when to use sagas instead."
date: 2026-05-12
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/two-phase-commit.html
---

# Two-Phase Commit (2PC) for Distributed Transactions

# Two-Phase Commit (2PC) for Distributed Transactions

  


# Two-Phase Commit (2PC) for Distributed Transactions

  
  
  
  


# Two-Phase Commit (2PC) for Distributed Transactions

  
  
  
  
  
  
  


# Two-Phase Commit (2PC) for Distributed Transactions

  
  
  
  
  
  
  
  
  
  


Two-phase commit (2PC) is a distributed transaction protocol that ensures atomic commitment across multiple databases or services. While it provides strong consistency guarantees, 2PC introduces significant complexity, blocking behavior, and failure modes that require careful consideration. This article examines the protocol mechanics, XA standard, coordinator failure scenarios, and modern alternatives. 

  
  
  
  
  
  
  


Protocol Overview 

  
  
  
  
  
  
  


The 2PC protocol involves a coordinator and multiple participants. The protocol proceeds in two phases. In phase one, the prepare phase, the coordinator sends a prepare request to all participants. Each participant checks whether it can commit the transaction, writes enough information to durable storage to guarantee commitability, and responds with either a "ready" or "abort" vote. 

  
  
  
  
  
  
  


In phase two, the commit phase, if all participants voted "ready", the coordinator sends a commit message to all participants. If any participant voted "abort", the coordinator sends an abort message. The critical guarantee is that once a participant votes "ready" in phase one, it must be able to commit until it receives a commit or abort instruction from the coordinator. 

  
  
  
  
  
  
  


XA Standard 

  
  
  
  
  
  
  


The XA standard, part of the X/Open Distributed Transaction Processing model, specifies the interface between a transaction manager and resource managers. It is supported by virtually all relational databases (Oracle, PostgreSQL, MySQL, SQL Server) and many message brokers. 

  
  
  
  
  
  
  


XA provides functions like `xa_start`, `xa_end`, `xa_prepare`, `xa_commit`, and `xa_rollback` that implement the 2PC protocol. Applications use XA through a transaction manager, often integrated into an application server or a distributed transaction coordinator. 

  
  
  
  
  
  
  


Coordinator Failure Scenarios 

  
  
  
  
  
  
  


Coordinator failure is the most dangerous failure mode in 2PC. If the coordinator crashes after sending prepare requests but before sending commit decisions, participants remain in a prepared state indefinitely. They hold locks on resources, preventing other transactions from accessing those resources. This is known as the "blocking" problem. 

  
  
  
  
  
  
  


Recovery requires the coordinator to maintain a transaction log on durable storage. When the coordinator restarts, it reads the log to determine the outcome of in-flight transactions and sends the appropriate commit or abort decisions to participants. If the log is lost or corrupted, the prepared transactions remain blocked until an administrator intervenes. 

  
  
  
  
  
  
  


Heuristic resolutions allow participants to unilaterally decide the outcome of a stuck transaction after a timeout. A heuristic commit or heuristic abort breaks the two-phase protocol's atomicity guarantee but releases blocked resources. 

  
  
  
  
  
  
  


Performance Implications 

  
  
  
  
  
  
  


2PC imposes significant performance costs. The prepare phase requires an additional round trip compared to a local transaction. Each participant must write to disk to ensure durability of the prepare vote. Locks are held across both phases, increasing contention and reducing concurrency. 

  
  
  
  
  
  
  


In practice, 2PC is limited to within a single data center due to latency and reliability constraints. Cross-data-center 2PC is rarely attempted. 

  
  
  
  
  
  
  


Modern Alternatives 

  
  
  
  
  
  
  


Given 2PC's limitations, modern architectures often prefer alternatives. The Saga pattern breaks a distributed transaction into a series of local transactions with compensating actions. Eventual consistency with event sourcing accepts temporary inconsistency in exchange for higher throughput. The Outbox pattern avoids distributed transactions by using a local transaction to write both data and messages to the same database. 

  
  
  
  
  
  
  


Two-phase commit remains useful for specific scenarios, particularly within a single data center where strong consistency across heterogeneous data stores is non-negotiable. For most modern cloud-native applications, however, the trade-offs favor alternatives that embrace eventual consistency and compensate rather than block.
