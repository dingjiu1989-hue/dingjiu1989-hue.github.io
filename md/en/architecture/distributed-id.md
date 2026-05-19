---
title: "Distributed ID Generation"
description: "UUID v7, Snowflake, ULID, database sequences, k-ordered IDs and their tradeoffs in distributed systems"
date: 2026-04-23
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/distributed-id.html
---

# Distributed ID Generation

Distributed ID generation is a foundational infrastructure concern for any system that spans multiple databases or services. IDs must be unique across all nodes, generate quickly without coordination, and often carry useful properties like time-orderedness, compactness, or security. The choice of ID generation strategy affects database performance, sorting behavior, and system complexity. 

UUID v7 is the newest contender, standardized in RFC 9562. It generates time-ordered, random-based UUIDs. The first 48 bits contain a Unix timestamp with millisecond precision. The remaining bits contain random data. UUID v7 combines the ordering benefit of time-based IDs with the distribution properties of random IDs. Database indexes benefit from the time-ordered prefix, which reduces B-tree index fragmentation compared to purely random UUIDs. 

Snowflake IDs, popularized by Twitter (now X), provide compact 64-bit integer IDs. The typical bit layout includes a timestamp (41 bits, giving ~69 years of unique timestamps), a worker ID (10 bits, supporting up to 1024 nodes), and a sequence number (12 bits, allowing 4096 IDs per millisecond per worker). Snowflake IDs are monotonically increasing, sortable, and compact for storage and indexing. The downsides are dependence on clock synchronization — clock skew can produce duplicate or out-of-order IDs. 

ULIDs offer another compact alternative: a 128-bit identifier encoded as a 26-character Crockford Base32 string. The first 10 characters encode a Unix timestamp with millisecond precision. The remaining 16 characters are random. ULIDs are case-insensitive, URL-safe, and lexicographically sortable. They are intended as a drop-in replacement for UUIDs with better sorting properties and more compact string representation. 

Database sequences provide the simplest approach but create a coordination bottleneck. Auto-increment columns in relational databases guarantee uniqueness and ordering within a single database. Distributed sequences require coordination across databases, typically through a centralized sequence service. The HA sequence pattern uses a database table with configurable increments (step sizes) — each application instance reserves a range of IDs and caches them locally, reducing database round trips. 

The HA approach works well: configure N application instances with step = N and different starting offsets. Each instance generates IDs sequentially using its assigned range. When it exhausts its range, it requests a new range from the database. This provides ordering within each instance and uniqueness across the system without requiring coordination for each ID. The trade-off is gaps in sequences when instances restart or scale. 

K-ordered IDs represent a class of IDs that are approximately time-ordered within a bounded window of disorder. Snowflake variants fall into this category. The time component provides a global ordering approximation, while the node and sequence components allow for concurrent generation across nodes. Database indexes perform significantly better with k-ordered IDs than with random IDs because new insertions tend to land near the end of the index rather than at random positions. 

Security considerations apply when IDs are exposed to clients. Sequential numeric IDs reveal the rate at which resources are created. Time-based IDs reveal the creation timestamp. In some contexts, unpredictable IDs are preferred to prevent enumeration attacks. UUID v4 provides randomness but poor index performance. A hybrid approach uses random IDs for external exposure and maps them to internally optimized IDs through a lookup table. 

The choice depends on database technology, ID length constraints, ordering requirements, and security needs. Modern recommendations favor UUID v7 as a default choice: it provides time-orderedness for good index performance, sufficient randomness for moderate security, and standardized format for interoperability. Snowflake variants remain excellent when compact 64-bit integer IDs are required for storage efficiency or legacy system compatibility.

**See also:** [Caching Strategies](</en/architecture/cache-strategies.html>), [Leader Election in Distributed Systems](</en/architecture/leader-election.html>), [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>).

**See also:** [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>)

**See also:** [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>)

**See also:** [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>)

**See also:** [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>)

**See also:** [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>)

**See also:** [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [Cost Per Request Modeling](</en/architecture/cost-per-request.html>), [Zero-Downtime Database Migrations](</en/architecture/database-migration-zero-downtime.html>)

**See also:** [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [Cost Per Request Modeling](</en/architecture/cost-per-request.html>), [Zero-Downtime Database Migrations](</en/architecture/database-migration-zero-downtime.html>)

**See also:** [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [Cost Per Request Modeling](</en/architecture/cost-per-request.html>), [Zero-Downtime Database Migrations](</en/architecture/database-migration-zero-downtime.html>)
