---
title: "Connection Pooling Guide"
description: "Master database connection pooling with PgBouncer, HikariCP, and application-level pools to optimize performance and resource usage."
date: 2026-05-11
board: database
url: https://dingjiu1989-hue.github.io/en/database/connection-pooling.html
---

## Why Connection Pooling Matters

Opening a database connection is expensive. Each new connection requires TCP handshake, SSL negotiation, authentication, and memory allocation on both the client and server. Connection pooling reuses a set of established connections, eliminating this overhead and preventing resource exhaustion.

## The Cost of Connection Creation

| Operation | Typical Latency |
|-----------|-----------------|
| TCP handshake | 1-5ms |
| SSL/TLS negotiation | 5-20ms |
| Authentication | 1-10ms |
| Total per new connection | 7-35ms |
| Pooled connection reuse | < 1ms |

With a pool of 10 connections handling 100 requests per second, connection reuse saves approximately 700-3500ms of latency per second.

## How Connection Pooling Works

```
Application Threads                  Connection Pool                    Database
┌─────────────────────┐         ┌─────────────────────┐          ┌──────────────┐
│ Thread 1 ───────────┼────────>│   ┌─ Connection 1   │          │              │
│ Thread 2 ───────────┼────────>│   ├─ Connection 2   │<────────>│  PostgreSQL  │
│ Thread 3 ───────────┼────────>│   ├─ Connection 3   │          │  Server      │
│ Thread 4 ───────────┼────────>│   └─ Connection 4   │          │              │
│ Thread 5 (waiting) ─┼────────>│                     │          │              │
└─────────────────────┘         └─────────────────────┘          └──────────────┘
```

When a thread requests a connection: if an idle connection exists, it is returned immediately. If all connections are busy, the thread waits until one becomes available or the timeout expires.

## Pool Configuration Parameters

| Parameter | Description | Recommended Value |
|-----------|-------------|-------------------|
| `maxSize` | Maximum connections in pool | 10-20 per CPU core |
| `minIdle` | Minimum idle connections | 2-5 |
| `connectionTimeout` | Wait timeout for connection | 30000ms (30s) |
| `idleTimeout` | Max idle time before closing | 600000ms (10min) |
| `maxLifetime` | Max connection lifetime | 1800000ms (30min) |
| `validationQuery` | Connection health check | `SELECT 1` |

## Implementation Examples

### HikariCP (Java / Spring Boot)

```yaml
# application.yml
spring:
  datasource:
    url: jdbc:postgresql://database:5432/mydb
    username: app_user
    password: ${DB_PASSWORD}
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
      connection-timeout: 30000
      idle-timeout: 600000
      max-lifetime: 1800000
      pool-name: AppPool
      connection-test-query: SELECT 1
```

```java
@Configuration
public class DatabaseConfig {
    @Bean
    public DataSource dataSource() {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl("jdbc:postgresql://database:5432/mydb");
        config.setUsername("app_user");
        config.setPassword(System.getenv("DB_PASSWORD"));
        config.setMaximumPoolSize(20);
        config.setMinimumIdle(5);
        config.setConnectionTimeout(30000);
        config.setIdleTimeout(600000);
        config.setMaxLifetime(1800000);
        config.setPoolName("AppPool");
        return new HikariDataSource(config);
    }
}
```

### SQLAlchemy (Python)

```python
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://app_user:password@database:5432/mydb",
    pool_size=10,           # Number of connections to maintain
    max_overflow=10,         # Additional connections allowed beyond pool_size
    pool_timeout=30,         # Seconds to wait for a connection
    pool_recycle=1800,       # Recycle connections after 30 minutes
    pool_pre_ping=True,      # Test connections before using
    echo=False
)

# Usage
with engine.connect() as conn:
    result = conn.execute("SELECT * FROM users")
```

### Node.js (pg-pool)

```javascript
const { Pool } = require('pg');

const pool = new Pool({
    host: 'database',
    port: 5432,
    database: 'mydb',
    user: 'app_user',
    password: process.env.DB_PASSWORD,
    max: 20,
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 5000,
    maxUses: 7500,  // Recycle connection after 7500 queries
});

// Query using pool
async function getUsers() {
    const result = await pool.query('SELECT * FROM users');
    return result.rows;
}
```

## Connection Poolers

### PgBouncer (PostgreSQL)

A dedicated lightweight connection pooler that sits between your application and PostgreSQL:

```ini
# pgbouncer.ini
[databases]
mydb = host=127.0.0.1 port=5432 dbname=mydb

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 6432
auth_type = scram-sha-256
auth_file = /etc/pgbouncer/userlist.txt

# Pool modes
pool_mode = transaction  # Most common: return connection to pool after transaction

# Pool sizing
default_pool_size = 25
max_client_conn = 100
reserve_pool_size = 5
reserve_pool_timeout = 5
```

**Pool Modes**:

| Mode | Connection Returned | Best For |
|------|-------------------|----------|
| Session | After client disconnects | Long-lived connections |
| Transaction | After each transaction | Web applications |
| Statement | After each statement | Batch processing |

### ProxySQL (MySQL)

```ini
# proxysql.cnf
datadir=/var/lib/proxysql

mysql_servers =
(
    { address="mysql-master", port=3306, hostgroup=10 },
    { address="mysql-replica1", port=3306, hostgroup=20 },
    { address="mysql-replica2", port=3306, hostgroup=20 }
)

mysql_users =
(
    { username="app_user", password="secret", default_hostgroup=10 }
)

mysql_query_rules =
(
    { rule_id=1, active=1, match_pattern="^SELECT", destination_hostgroup=20 },
    { rule_id=2, active=1, match_pattern=".*", destination_hostgroup=10 }
)
```

## Connection Pool Sizing

The common misconception is "more connections = better performance." In reality, too many connections degrades performance due to context switching and database contention.

### Formula for Optimal Pool Size

```
pool_size = (core_count * 2) + effective_spindle_count
```

For a database server with 8 CPU cores and SSD storage:
```python
pool_size = (8 * 2) + 1  # = 17 connections
```

This is far fewer than the default of 100+ that many applications use.

## Monitoring Connection Pools

```sql
-- PostgreSQL: Check active connections
SELECT
    state,
    count(*) as count,
    wait_event_type,
    wait_event
FROM pg_stat_activity
WHERE backend_type = 'client backend'
GROUP BY state, wait_event_type, wait_event;

-- Identify idle connections
SELECT count(*) FROM pg_stat_activity WHERE state = 'idle';

-- Connection pool hit rate (PgBouncer)
SHOW STATS;
-- avg_recv, avg_sent, total_query_time, avg_query_time
```

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Too many connections | Database overload, slow queries | Use 2x CPU cores + disk spindles |
| No connection timeout | Threads hang forever | Set connectionTimeout |
| No max lifetime | Stale connections, memory leak | Set maxLifetime (30 min) |
| No health check | Broken connections in pool | Enable pool_pre_ping |
| Pool per microservice | Connection exhaustion | Use PgBouncer for unified pooling |
| Leaking connections | Pool exhaustion | Always close connections in finally blocks |

## Summary

Connection pooling is essential for production database applications. Use application-level pools (HikariCP, SQLAlchemy) for basic needs and dedicated poolers (PgBouncer) for high-scale deployments. Size pools based on CPU cores rather than connection demand, set appropriate timeouts and max lifetimes, and always return connections to the pool. Monitor pool usage and database connection counts to detect leaks and sizing issues before they cause outages.
