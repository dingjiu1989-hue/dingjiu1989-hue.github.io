---
title: "Connection Pooling Guide"
description: "Master database connection pooling with PgBouncer, HikariCP, and application-level pools to optimize performance and resource usage."
date: 2025-12-22
board: database
url: https://dingjiu1989-hue.github.io/en/database/connection-pooling.html
---

# Connection Pooling Guide

Why Connection Pooling Matters 

Creating database connections is expensive: TCP handshake, SSL negotiation, and authentication add 7-35ms per connection. Connection pooling reuses established connections. 

How Pools Work 

A pool maintains a set of open connections. When a thread requests one, an idle connection is returned immediately. If all are busy, the thread waits. 

Pool Configuration 

| Parameter | Recommended | |-----------|-------------| | maxSize | 10-20 per CPU core | | connectionTimeout | 30000ms | | maxLifetime | 1800000ms (30min) | 

HikariCP (Java) 

spring.datasource.hikari:

maximum-pool-size: 20

minimum-idle: 5

connection-timeout: 30000

max-lifetime: 1800000

PgBouncer (PostgreSQL) 

[pgbouncer]

pool_mode = transaction

default_pool_size = 25

max_client_conn = 100

Pgbouncer sits between application and database. Transaction mode returns connections to pool after each transaction. 

Sizing Formula 

pool_size = (core_count * 2) + effective_spindle_count

For 8 CPU cores with SSD: 17 connections. More connections causes context switching overhead. 

Monitoring 

SELECT state, count(*) FROM pg_stat_activity

WHERE backend_type = 'client backend' GROUP BY state;

Monitor for idle-in-transaction connections and pool exhaustion. 

Conclusion 

Size pools based on CPU cores, not concurrent users. Use PgBouncer for high-scale PostgreSQL deployments. Set timeouts and max lifetimes. Monitor pool usage and connection leaks.

**See also:** [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>), [Query Performance Tuning Tools](</en/database/query-performance-tuning.html>), [Database Security Hardening Guide](</en/database/database-security-best-practices.html>).

**See also:** [PostgreSQL Query Optimization: From 2 Seconds to 2 Milliseconds](</en/tech/postgresql-query-optimization.html>), [Query Performance Tuning Tools](</en/database/query-performance-tuning.html>), [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>)

**See also:** [PostgreSQL Query Optimization: From 2 Seconds to 2 Milliseconds](</en/tech/postgresql-query-optimization.html>), [Query Performance Tuning Tools](</en/database/query-performance-tuning.html>), [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>)

**See also:** [PostgreSQL Query Optimization: From 2 Seconds to 2 Milliseconds](</en/tech/postgresql-query-optimization.html>), [Query Performance Tuning Tools](</en/database/query-performance-tuning.html>), [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>)

**See also:** [PostgreSQL Query Optimization: From 2 Seconds to 2 Milliseconds](</en/tech/postgresql-query-optimization.html>), [Query Performance Tuning Tools](</en/database/query-performance-tuning.html>), [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>)

**See also:** [PostgreSQL Query Optimization: From 2 Seconds to 2 Milliseconds](</en/tech/postgresql-query-optimization.html>), [Query Performance Tuning Tools](</en/database/query-performance-tuning.html>), [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>)

**See also:** [PostgreSQL vs MySQL vs SQLite in 2026: A Complete Database Guide for Developers](</en/database/postgresql-vs-mysql-2026.html>), [SQL Query Optimization](</en/database/sql-query-optimization.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>)

**See also:** [PostgreSQL vs MySQL vs SQLite in 2026: A Complete Database Guide for Developers](</en/database/postgresql-vs-mysql-2026.html>), [SQL Query Optimization](</en/database/sql-query-optimization.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>)

**See also:** [PostgreSQL vs MySQL vs SQLite in 2026: A Complete Database Guide for Developers](</en/database/postgresql-vs-mysql-2026.html>), [SQL Query Optimization](</en/database/sql-query-optimization.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>)

**See also:** [PostgreSQL vs MySQL vs SQLite in 2026: A Complete Database Guide for Developers](</en/database/postgresql-vs-mysql-2026.html>), [SQL Query Optimization](</en/database/sql-query-optimization.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>)

**See also:** [PostgreSQL vs MySQL vs SQLite in 2026: A Complete Database Guide for Developers](</en/database/postgresql-vs-mysql-2026.html>), [SQL Query Optimization](</en/database/sql-query-optimization.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>)

**See also:** [PostgreSQL vs MySQL vs SQLite in 2026: A Complete Database Guide for Developers](</en/database/postgresql-vs-mysql-2026.html>), [SQL Query Optimization](</en/database/sql-query-optimization.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>)

**See also:** [PostgreSQL vs MySQL vs SQLite in 2026: A Complete Database Guide for Developers](</en/database/postgresql-vs-mysql-2026.html>), [SQL Query Optimization](</en/database/sql-query-optimization.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>)

**See also:** [PostgreSQL vs MySQL vs SQLite in 2026: A Complete Database Guide for Developers](</en/database/postgresql-vs-mysql-2026.html>), [SQL Query Optimization](</en/database/sql-query-optimization.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>)

**See also:** [PostgreSQL vs MySQL vs SQLite in 2026: A Complete Database Guide for Developers](</en/database/postgresql-vs-mysql-2026.html>), [SQL Query Optimization](</en/database/sql-query-optimization.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>)
