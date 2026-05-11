---
title: "Database Monitoring and Performance Alerting"
description: "Monitor QPS, latency, connections, and cache hit ratio with Prometheus exporters, Grafana dashboards, and intelligent alert thresholds."
date: 2026-05-12
board: database
url: https://dingjiu1989-hue.github.io/en/database/database-monitoring.html
---

Database monitoring tracks the health, performance, and availability of database systems. Effective monitoring catches problems before they become incidents. This article covers the key metrics to track, tools for collection and visualization, and strategies for setting meaningful alert thresholds.

## Key Database Metrics

### Queries Per Second (QPS)

QPS measures the throughput of your database. Monitoring QPS helps you understand traffic patterns and capacity requirements.

- **Spike detection**: Sudden QPS increases may indicate a traffic surge or a runaway query.
- **Capacity planning**: If QPS consistently approaches your database's limit, it is time to scale.
- **Baseline shifts**: A permanent QPS increase suggests organic growth that may require infrastructure changes.

```sql
-- MySQL: Current QPS
SHOW GLOBAL STATUS LIKE 'Questions';

-- PostgreSQL: Queries per second
SELECT queries_per_second()
FROM pg_stat_database
WHERE datname = 'your_database';
```

### Query Latency

Latency measures how long queries take to execute. Latency spikes degrade user experience and indicate problems.

**Percentile metrics matter more than averages**: p50 (median) shows typical performance. p99 shows the worst-performing queries. A 10ms p50 with a 30-second p99 means 1% of users have a terrible experience.

```sql
-- PostgreSQL: Query latency by query
SELECT
    queryid,
    query,
    mean_exec_time as avg_ms,
    p99_exec_time as p99_ms,
    calls
FROM pg_stat_statements
ORDER BY p99_exec_time DESC
LIMIT 10;
```

### Active Connections

Connection count indicates how many clients are simultaneously connected. Running out of connections causes application failures.

- **Connection pool saturation**: When connection count reaches the max_pool limit, new connections wait or fail.
- **Active vs idle**: High idle connections with low active connections indicates inefficient connection pool configuration.
- **Connection churn**: Rapid connect/disconnect cycles add overhead.

```sql
-- PostgreSQL: Active connection count
SELECT
    state,
    count(*) as connections
FROM pg_stat_activity
WHERE backend_type = 'client backend'
GROUP BY state;

-- Check for idle in transaction (potential blocking)
SELECT count(*) FROM pg_stat_activity
WHERE state = 'idle in transaction'
AND xact_start < now() - interval '5 minutes';
```

### Cache Hit Ratio

Cache hit ratio measures how often the database finds data in memory versus reading from disk. Higher is better.

- **Buffer cache hit ratio**: 99%+ is healthy for most workloads. Below 95% indicates the working set does not fit in memory.
- **Index cache hit ratio**: Especially important for databases with large indexes.

```sql
-- PostgreSQL: Buffer cache hit ratio
SELECT
    sum(blks_hit) / nullif(sum(blks_hit + blks_read), 0) * 100 as hit_ratio
FROM pg_stat_database
WHERE datname = 'your_database';

-- MySQL: InnoDB buffer pool hit ratio
SHOW STATUS LIKE 'InnoDB_buffer_pool_read_%';
```

### Disk I/O

Disk I/O metrics reveal storage performance issues.

- **IOPS**: Input/output operations per second. Cloud databases have IOPS limits based on volume size.
- **Throughput**: Data read/written per second.
- **Latency**: Time per I/O operation. Under 10ms is healthy. Over 50ms indicates problems.
- **Queue depth**: Number of I/O operations waiting. High queue depth suggests the disk subsystem is overwhelmed.

### Replication Lag

For databases with read replicas, replication lag measures how far behind replicas are from the primary.

```sql
-- PostgreSQL: Replication lag
SELECT
    application_name,
    pg_size_pretty(pg_wal_lsn_diff(
        pg_current_wal_lsn(),
        flush_lsn
    )) as lag_bytes,
    now() - pg_last_xact_replay_timestamp() as lag_time
FROM pg_stat_replication;

-- MySQL: Replication lag
SHOW SLAVE STATUS\G
-- Look at Seconds_Behind_Master
```

## Prometheus Exporters

Prometheus is the dominant metrics collection system for infrastructure monitoring. Database exporters translate database metrics into Prometheus format.

### PostgreSQL Exporter

```yaml
# docker-compose.yml for PostgreSQL monitoring
version: '3'
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: myapp
    ports:
      - "5432:5432"

  postgres_exporter:
    image: prometheuscommunity/postgres-exporter:v0.15.0
    environment:
      DATA_SOURCE_NAME: "postgresql://user:password@postgres:5432/myapp?sslmode=disable"
    ports:
      - "9187:9187"

  prometheus:
    image: prom/prometheus:v2.53.0
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
```

```yaml
# prometheus.yml scrape configuration
scrape_configs:
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres_exporter:9187']
    metrics_path: /metrics
```

### MySQL Exporter

```yaml
  mysql_exporter:
    image: prom/mysqld-exporter:v0.15.1
    environment:
      DATA_SOURCE_NAME: "exporter:password@(mysql:3306)/"
    ports:
      - "9104:9104"
```

## Grafana Dashboards

Grafana visualizes Prometheus metrics in configurable dashboards. The community provides pre-built dashboards for most databases.

### Dashboard Sections

A good database dashboard includes these panels:

1. **Overview**: QPS, active connections, cache hit ratio, replication lag.
2. **Query Performance**: Top N queries by duration, calls, and rows read.
3. **Resource Usage**: CPU, memory, disk I/O, network throughput.
4. **Slow Queries**: Count of queries exceeding a latency threshold over time.
5. **Error Rate**: Database errors (deadlocks, constraint violations, connection timeouts).

```json
// Grafana panel JSON (simplified)
{
  "title": "Query Latency (p99)",
  "type": "graph",
  "targets": [
    {
      "expr": "pg_stat_statements_p99_ms{datname='myapp'}",
      "legendFormat": "{{queryid}}"
    }
  ],
  "yaxes": [
    { "label": "milliseconds", "format": "ms" }
  ],
  "thresholds": [
    { "value": 100, "op": "gt", "color": "orange" },
    { "value": 1000, "op": "gt", "color": "red" }
  ]
}
```

## Alert Thresholds

Setting the right alert thresholds is harder than it sounds. Too many alerts cause alert fatigue. Too few alerts miss critical issues.

### Threshold Strategy

**Static thresholds**: Fixed values based on capacity. Simple but do not adapt to usage patterns.

```
Alert if:
  - Active connections > 80% of max_connections
  - Replication lag > 60 seconds
  - Disk usage > 85%
  - Cache hit ratio < 97%
```

**Dynamic thresholds**: Alert when metrics deviate from their historical baseline. Better for bursty workloads.

```python
# Dynamic threshold calculation
def calculate_dynamic_threshold(hourly_metric, deviation_factor=2.0):
    """Alert when metric deviates by more than N standard deviations."""
    mean = hourly_metric.mean()
    std = hourly_metric.std()
    upper_threshold = mean + (std * deviation_factor)
    lower_threshold = max(0, mean - (std * deviation_factor))
    return upper_threshold, lower_threshold
```

**Rate-of-change thresholds**: Alert on rapid changes, not absolute values. Useful for detecting anomalies.

```
Alert if:
  - QPS change > 300% compared to same time last week
  - Replication lag increased by 10 seconds in 1 minute
```

### Alert Severity Levels

| Severity | Response Time | Example |
|----------|---------------|---------|
| Critical | Immediate (24x7) | Database down, replication broken |
| High | 1 hour | P99 latency > 1 second, disk > 90% |
| Medium | 1 day | Cache hit ratio trending down |
| Low | 1 week | Database version EOL approaching |

### Reducing Alert Fatigue

1. **Use multi-condition alerts**: Alert only when A and B are both true. Example: latency > 1s AND QPS > baseline.
2. **Implement hysteresis**: Require the condition to persist for N minutes before alerting.
3. **Suppress during maintenance**: Automatically suppress alerts during scheduled windows.
4. **Group related alerts**: A single "database slow" alert is better than 50 individual slow-query alerts.
5. **Auto-resolve**: Clear alerts when the metric returns to normal.

## Database-Specific Monitoring Tools

### pg_stat_statements (PostgreSQL)

The pg_stat_statements extension tracks query execution statistics. It identifies which queries consume the most resources.

```sql
-- Enable the extension
CREATE EXTENSION pg_stat_statements;

-- Find the most expensive queries
SELECT
    query,
    total_exec_time / calls as avg_ms,
    calls,
    rows,
    shared_blks_hit / (shared_blks_hit + shared_blks_read) * 100 as cache_hit_pct
FROM pg_stat_statements
WHERE query NOT LIKE '%pg_%'
ORDER BY total_exec_time DESC
LIMIT 10;
```

### Performance Schema (MySQL)

MySQL Performance Schema provides detailed instrumentation of query execution.

```sql
-- Top queries by total latency
SELECT
    digest_text as query,
    count_star as execution_count,
    round(sum_timer_wait / 1000000000, 2) as total_latency_ms
FROM performance_schema.events_statements_summary_by_digest
ORDER BY sum_timer_wait DESC
LIMIT 10;
```

## Conclusion

Database monitoring is a continuous practice, not a one-time setup. Track QPS, latency, connections, cache hit ratio, and replication lag. Collect these metrics with Prometheus exporters, visualize them in Grafana dashboards, and set intelligent alert thresholds. Start with static thresholds for critical metrics and move to dynamic thresholds as you collect more data. The goal is to detect problems before users do.
