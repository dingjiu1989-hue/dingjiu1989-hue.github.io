---
title: "Database Security Hardening"
description: "Hardening database security with encryption, audit logging, access control, and network isolation."
date: 2026-04-10
board: database
url: https://dingjiu1989-hue.github.io/en/database/database-security-hardening.html
---

# Database Security Hardening

Defense in Depth 

Database security requires multiple layers: network isolation, encryption, access control, and auditing. 

Encryption 

Encryption at Rest 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- PostgreSQL TDE

CREATE EXTENSION pg_tde;

SELECT pg_tde_add_database_key_provider('file-vault', '{"type":"file"}');

SELECT pg_tde_set_principal_key('production-db-key', 'file-vault');

Encryption in Transit 

## postgresql.conf

ssl = on

ssl_cert_file = '/etc/ssl/certs/server.crt'

ssl_key_file = '/etc/ssl/private/server.key'

Access Control 

Apply least privilege with separate roles: 

CREATE ROLE read_only;

CREATE ROLE read_write;

GRANT SELECT ON ALL TABLES TO read_only;

GRANT INSERT, UPDATE, DELETE ON ALL TABLES TO read_write;

Row-Level Security 

ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON orders

USING (tenant_id = current_setting('app.tenant_id')::INT);

Audit Logging 

CREATE EXTENSION pgaudit;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- In postgresql.conf

pgaudit.log = 'write,ddl,role'

Network Isolation 

Place databases in private subnets. Use security groups to restrict access to specific application servers only. Never expose databases directly to the internet. 

Conclusion 

Layer encryption, access control, RLS, audit logging, and network isolation. Rotate credentials regularly. Follow least privilege. Test your security controls periodically.

**See also:** [Database Audit Triggers: Automatic Change Tracking](</en/database/database-audit-triggers.html>), [Database Security Hardening Guide](</en/database/database-security-best-practices.html>), [Change Data Capture: Tracking Database Changes in Real-Time](</en/database/database-change-tracking-cdc.html>).

**See also:** [Database Audit Triggers: Automatic Change Tracking](</en/database/database-audit-triggers.html>), [Database Transactions Deep Dive: ACID, Isolation Levels, Savepoints](</en/database/database-transactions.html>), [Database Triggers: Use Cases, Performance Costs, and Alternatives](</en/database/triggers-patterns.html>)

**See also:** [Database Audit Triggers: Automatic Change Tracking](</en/database/database-audit-triggers.html>), [Database Transactions Deep Dive: ACID, Isolation Levels, Savepoints](</en/database/database-transactions.html>), [Database Triggers: Use Cases, Performance Costs, and Alternatives](</en/database/triggers-patterns.html>)

**See also:** [Database Audit Triggers: Automatic Change Tracking](</en/database/database-audit-triggers.html>), [Database Transactions Deep Dive: ACID, Isolation Levels, Savepoints](</en/database/database-transactions.html>), [Database Triggers: Use Cases, Performance Costs, and Alternatives](</en/database/triggers-patterns.html>)

**See also:** [Database Audit Triggers: Automatic Change Tracking](</en/database/database-audit-triggers.html>), [Database Transactions Deep Dive: ACID, Isolation Levels, Savepoints](</en/database/database-transactions.html>), [Database Triggers: Use Cases, Performance Costs, and Alternatives](</en/database/triggers-patterns.html>)

**See also:** [Database Audit Triggers: Automatic Change Tracking](</en/database/database-audit-triggers.html>), [Database Transactions Deep Dive: ACID, Isolation Levels, Savepoints](</en/database/database-transactions.html>), [Database Triggers: Use Cases, Performance Costs, and Alternatives](</en/database/triggers-patterns.html>)

**See also:** [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>), [Database Concurrency Control: MVCC, Locking, and Deadlocks](</en/database/database-concurrency.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>)

**See also:** [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>), [Database Concurrency Control: MVCC, Locking, and Deadlocks](</en/database/database-concurrency.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>)

**See also:** [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>), [Database Concurrency Control: MVCC, Locking, and Deadlocks](</en/database/database-concurrency.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>)

**See also:** [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>), [Database Concurrency Control: MVCC, Locking, and Deadlocks](</en/database/database-concurrency.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>)

**See also:** [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>), [Database Concurrency Control: MVCC, Locking, and Deadlocks](</en/database/database-concurrency.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>)

**See also:** [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>), [Database Concurrency Control: MVCC, Locking, and Deadlocks](</en/database/database-concurrency.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>)
