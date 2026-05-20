---
title: "Data Consistency Models Explained"
description: "Learn about strong, eventual, causal, read-your-writes, and monotonic read consistency models plus CAP theorem trade-offs in practice."
date: 2026-03-26
board: database
url: https://dingjiu1989-hue.github.io/en/database/data-consistency-models.html
---

# Data Consistency Models Explained

Consistency in Distributed Systems 

Data consistency models define guarantees about when updates become visible to readers. Choosing the right model is critical. 

Strong Consistency 

All reads return the latest write. Behaves like a single copy: 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Strong: reads always see latest write

SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

SELECT balance FROM accounts WHERE id = 1;

Strong consistency requires coordination, adding latency and reducing availability during partitions. 

Eventual Consistency 

Replicas converge over time. Reads may return stale data: 

def read(key):

return any_replica.get(key) # May be stale

def write(key, value):

local.set(key, value)

background_replicate(key, value) # Async

Causal Consistency 

Preserves cause-and-effect relationships. If A causes B, all observers see A before B. Unrelated operations can be seen in any order. 

Read-After-Write (Read-Your-Writes) 

After a client writes, subsequent reads by the same client return that value. Other clients may still see the old value. 

Choosing a Model 

| Model | Guarantee | Latency | Use Case | |-------|-----------|---------|----------| | Strong | All reads current | High | Banking, inventory | | Eventual | Converges | Low | Feeds, analytics | | Causal | Causality preserved | Medium | Social apps | | Read-your-writes | Own writes visible | Low | User profiles | 

Conclusion 

Use strong consistency where correctness is critical. Use eventual consistency for scale. Session-level guarantees (read-your-writes, monotonic reads) cover most real-world use cases without the cost of global strong consistency.

**See also:** [Database Normalization Explained](</en/database/database-normalization.html>), [Data Modeling Best Practices](</en/database/data-modeling.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>).

**See also:** [Database Normalization Explained](</en/database/database-normalization.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>), [ACID vs BASE Transactions](</en/database/acid-vs-base.html>)

**See also:** [Database Normalization Explained](</en/database/database-normalization.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>), [ACID vs BASE Transactions](</en/database/acid-vs-base.html>)

**See also:** [Database Normalization Explained](</en/database/database-normalization.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>), [ACID vs BASE Transactions](</en/database/acid-vs-base.html>)

**See also:** [Database Normalization Explained](</en/database/database-normalization.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>), [ACID vs BASE Transactions](</en/database/acid-vs-base.html>)

**See also:** [Database Normalization Explained](</en/database/database-normalization.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>), [ACID vs BASE Transactions](</en/database/acid-vs-base.html>)

**See also:** [Building ETL Pipelines: A Practical Guide](</en/database/etl-pipelines.html>), [Database Backup and Recovery Strategies](</en/database/database-backup-strategies.html>), [Database Migration Tools and Strategies](</en/database/database-migration.html>)

**See also:** [Building ETL Pipelines: A Practical Guide](</en/database/etl-pipelines.html>), [Database Backup and Recovery Strategies](</en/database/database-backup-strategies.html>), [Database Migration Tools and Strategies](</en/database/database-migration.html>)

**See also:** [Building ETL Pipelines: A Practical Guide](</en/database/etl-pipelines.html>), [Database Backup and Recovery Strategies](</en/database/database-backup-strategies.html>), [Database Migration Tools and Strategies](</en/database/database-migration.html>)

**See also:** [Building ETL Pipelines: A Practical Guide](</en/database/etl-pipelines.html>), [Database Backup and Recovery Strategies](</en/database/database-backup-strategies.html>), [Database Migration Tools and Strategies](</en/database/database-migration.html>)

**See also:** [Building ETL Pipelines: A Practical Guide](</en/database/etl-pipelines.html>), [Database Backup and Recovery Strategies](</en/database/database-backup-strategies.html>), [Database Migration Tools and Strategies](</en/database/database-migration.html>)

**See also:** [Building ETL Pipelines: A Practical Guide](</en/database/etl-pipelines.html>), [Database Backup and Recovery Strategies](</en/database/database-backup-strategies.html>), [Database Migration Tools and Strategies](</en/database/database-migration.html>)

**See also:** [Building ETL Pipelines: A Practical Guide](</en/database/etl-pipelines.html>), [Database Backup and Recovery Strategies](</en/database/database-backup-strategies.html>), [Database Migration Tools and Strategies](</en/database/database-migration.html>)

**See also:** [Building ETL Pipelines: A Practical Guide](</en/database/etl-pipelines.html>), [Database Backup and Recovery Strategies](</en/database/database-backup-strategies.html>), [Database Migration Tools and Strategies](</en/database/database-migration.html>)

**See also:** [Building ETL Pipelines: A Practical Guide](</en/database/etl-pipelines.html>), [Database Backup and Recovery Strategies](</en/database/database-backup-strategies.html>), [Database Migration Tools and Strategies](</en/database/database-migration.html>)
