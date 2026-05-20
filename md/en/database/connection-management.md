---
title: "Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning"
description: "Comprehensive guide to database connection management. Learn connection pooling with PgBouncer and HikariCP, max connections tuning, and best practices."
date: 2026-03-31
board: database
url: https://dingjiu1989-hue.github.io/en/database/connection-management.html
---

# Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning

Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning 

Every database connection consumes memory, file descriptors, and CPU. Connection management directly impacts database performance and application scalability. This article covers pooling strategies, popular poolers, and tuning guidelines. 

Why Connection Pooling Matters 

Each PostgreSQL backend process consumes approximately 5-10 MB of RAM, even when idle. A server with 500 connections uses 2.5-5 GB just for connection overhead. Beyond memory, connection creation is expensive: a new connection requires a TCP handshake, SSL negotiation, authentication, and backend forking. 

The "Too Many Connections" Problem 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Check current connections

SELECT count(*), state FROM pg_stat_activity GROUP BY state;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Find connections by application

SELECT application_name, count(*), sum(waiting) as waiting

FROM pg_stat_activity

GROUP BY application_name;

Connection pooling maintains a persistent set of database connections that applications borrow and return, avoiding the overhead of establishing connections on every request. 

PgBouncer (Server-Side Pooling) 

PgBouncer is a lightweight connection pooler for PostgreSQL. It runs as a separate process and proxies connections to the database. 

Installation and Configuration 

## pgbouncer.ini

[databases]

mydb = host=127.0.0.1 port=5432 dbname=mydb

[pgbouncer]

listen_addr = 0.0.0.0

listen_port = 6432

auth_type = md5

auth_file = /etc/pgbouncer/userlist.txt

pool_mode = transaction

max_client_conn = 500

default_pool_size = 25

reserve_pool_size = 5

reserve_pool_timeout = 3

server_idle_timeout = 300

query_timeout = 30

Pooling Modes 

| Mode | Description | Use Case | |------|-------------|----------| | `session` | Connection assigned for entire client session | Legacy apps, long-lived transactions | | `transaction` | Connection assigned per transaction | Default for web applications | | `statement` | Connection assigned per statement | Rare; only when no session state needed | 

User List 

echo '"app_user"' '"secure_password_hash"' > /etc/pgbouncer/userlist.txt

Connecting Through PgBouncer 

import psycopg2

## Connect to PgBouncer port, not PostgreSQL directly

conn = psycopg2.connect(

host="localhost",

port=6432,

dbname="mydb",

user="app_user",

password="secure_password"

)

Monitoring PgBouncer 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Connect to PgBouncer's admin database

psql -p 6432 -U admin pgbouncer

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Show pool statistics

SHOW POOLS;

SHOW STATS;

SHOW CLIENTS;

SHOW SERVERS;

Key metrics: `clients_active`, `clients_waiting`, `servers_active`, `servers_idle`, `maxwait`. 

HikariCP (Client-Side Pooling) 

HikariCP is the most popular connection pool for Java applications. It manages connections from within the application process. 

Spring Boot Configuration 

## application.yml

spring:

datasource:

url: jdbc:postgresql://localhost:5432/mydb

username: app_user

password: secure_password

hikari:

maximum-pool-size: 20

minimum-idle: 5

idle-timeout: 300000

connection-timeout: 10000

max-lifetime: 1800000

pool-name: MyPool

connection-test-query: SELECT 1

HikariCP Validation 

// Programmatic configuration

HikariConfig config = new HikariConfig();

config.setJdbcUrl("jdbc:postgresql://localhost:5432/mydb");

config.setUsername("app_user");

config.setPassword("secure_password");

config.setMaximumPoolSize(20);

config.setMinimumIdle(5);

config.setConnectionTimeout(10000);

config.setIdleTimeout(300000);

config.setMaxLifetime(1800000);

config.setConnectionTestQuery("SELECT 1");

config.addDataSourceProperty("cachePrepStmts", "true");

config.addDataSourceProperty("prepStmtCacheSize", "250");

config.addDataSourceProperty("prepStmtCacheSqlLimit", "2048");

HikariDataSource ds = new HikariDataSource(config);

Pool Sizing Formula 

The conventional formula for `max_connections` in PostgreSQL: 

max_connections = (max_client_conn / default_pool_size) * 2 + superuser_reserved_connections

But the **Formula rule of thumb** for optimal throughput is: 

connections = 2 * CPU_cores + effective_spindle_count

A 4-core machine with SSDs: `2 * 4 + 1 = 9` concurrent connections for optimal throughput. Beyond this, context switching and lock contention degrade performance. 

Max Connections Tuning 

## postgresql.conf

max_connections = 200

superuser_reserved_connections = 5

Application Statement Timeout 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Prevent runaway queries from holding connections

ALTER DATABASE mydb SET statement_timeout = '30s';

ALTER DATABASE mydb SET idle_in_transaction_session_timeout = '5min';

Common Pitfalls 

Connection Leaks 

## Bad: connection not returned to pool

def get_user(user_id):

conn = pool.getconn()

cursor = conn.cursor()

cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

result = cursor.fetchone()

## Missing: pool.putconn(conn)

return result

## Good: always use try/finally or context manager

def get_user(user_id):

conn = pool.getconn()

try:

cursor = conn.cursor()

cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

return cursor.fetchone()

finally:

pool.putconn(conn)

Long-Running Queries in Pool 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Set statement timeout at database level

ALTER DATABASE mydb SET statement_timeout = '30000'; -- 30 seconds

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Kill queries exceeding threshold

SELECT pg_terminate_backend(pid)

FROM pg_stat_activity

WHERE state = 'active'

AND now() - query_start > interval '5 minutes';

Connection Starvation 

When all pool connections are busy and requests queue: 

spring.datasource.hikari:

maximum-pool-size: 20

connection-timeout: 5000 # 5 seconds max wait

## After 5 seconds, throw SQLException instead of hanging forever

Monitoring Connection Health 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Connection utilization

SELECT

count(*) AS total_connections,

count(*) FILTER (WHERE state = 'active') AS active,

count(*) FILTER (WHERE state = 'idle') AS idle,

count(*) FILTER (WHERE state = 'idle in transaction') AS idle_in_txn

FROM pg_stat_activity;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Waiting queries

SELECT count(*) AS waiting_count

FROM pg_stat_activity

WHERE wait_event IS NOT NULL AND state = 'active';

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Connection age

SELECT pid, now() - backend_start AS connection_age, state, query

FROM pg_stat_activity

ORDER BY connection_age DESC

LIMIT 10;

Best Practices 

  * **Always use a pooler** : Direct connections from every application instance are not sustainable.



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Set pool size to CPU*2+disk** : More connections than that add latency, not throughput. 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Use PgBouncer in transaction mode** : Best balance for web applications. 4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Set connection timeouts** : Prevent applications from hanging indefinitely. 5\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Monitor and alert** on connection utilization trends. 6\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Use prepared statement caching** : Reduces query planning overhead. 7\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Separate pools for OLTP and analytics** : Different pool sizes and timeout values for different workloads. 

Connection management is invisible when done correctly and catastrophic when done poorly. A well-tuned pool keeps your database responsive under load and your applications free from connection-related failures.

**See also:** [Connection Pooling: Tuning, Best Practices, and Pitfalls](</en/database/database-connection-pooling.html>), [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>).

**See also:** [Connection Pooling: Tuning, Best Practices, and Pitfalls](</en/database/database-connection-pooling.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>)

**See also:** [Connection Pooling: Tuning, Best Practices, and Pitfalls](</en/database/database-connection-pooling.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>)

**See also:** [Connection Pooling: Tuning, Best Practices, and Pitfalls](</en/database/database-connection-pooling.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>)

**See also:** [Connection Pooling: Tuning, Best Practices, and Pitfalls](</en/database/database-connection-pooling.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>)

**See also:** [Connection Pooling: Tuning, Best Practices, and Pitfalls](</en/database/database-connection-pooling.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>)

**See also:** [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>), [NoSQL Databases Guide](</en/database/nosql-guide.html>)

**See also:** [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>), [NoSQL Databases Guide](</en/database/nosql-guide.html>)

**See also:** [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>), [NoSQL Databases Guide](</en/database/nosql-guide.html>)

**See also:** [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>), [NoSQL Databases Guide](</en/database/nosql-guide.html>)

**See also:** [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>), [NoSQL Databases Guide](</en/database/nosql-guide.html>)

**See also:** [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>), [NoSQL Databases Guide](</en/database/nosql-guide.html>)

**See also:** [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>), [NoSQL Databases Guide](</en/database/nosql-guide.html>)

**See also:** [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>), [NoSQL Databases Guide](</en/database/nosql-guide.html>)
