---
title: "Database Monitoring and Performance Alerting"
description: "Monitor QPS, latency, connections, and cache hit ratio with Prometheus exporters, Grafana dashboards, and intelligent alert thresholds."
date: 2026-03-26
board: database
url: https://dingjiu1989-hue.github.io/en/database/database-monitoring.html
---

# Database Monitoring and Performance Alerting

## Database Monitoring and Performance Alerting

### Database Monitoring and Performance Alerting

#### Database Monitoring and Performance Alerting

#### Database Monitoring and Performance Alerting

#### Database Monitoring and Performance Alerting

#### Database Monitoring and Performance Alerting

#### Database Monitoring and Performance Alerting

#### Database Monitoring and Performance Alerting

#### Database Monitoring and Performance Alerting

#### Database Monitoring and Performance Alerting

#### Database Monitoring and Performance Alerting

#### Database Monitoring and Performance Alerting

#### Database Monitoring and Performance Alerting

#### Database Monitoring and Performance Alerting

#### Database Monitoring and Performance Alerting

Why Monitor Databases? 

Database monitoring catches problems before they become incidents. Track key metrics and alert on anomalies. 

Key Metrics 

Query Performance 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- PostgreSQL slow queries

SELECT query, mean_exec_time, calls

FROM pg_stat_statements

ORDER BY mean_exec_time DESC LIMIT 10;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Active queries

SELECT pid, state, query_start, query

FROM pg_stat_activity

WHERE state = 'active';

Connection Pools 

Monitor active vs idle connections. Alert when connection count exceeds 80% of max_connections. 

Disk and Memory 

Track cache hit ratio (aim for 99%+), disk usage, and IOPS. Low cache hit ratio indicates the working set does not fit in memory. 

Replication Lag 

SELECT application_name,

pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) AS lag_bytes,

now() - pg_last_xact_replay_timestamp() AS lag_time

FROM pg_stat_replication;

Prometheus Setup 

#### prometheus.yml

scrape_configs:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- job_name: 'postgres'

static_configs:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- targets: ['postgres_exporter:9187']

Alert Thresholds 

| Metric | Warning | Critical | |--------|---------|----------| | Cache hit ratio | < 97% | < 95% | | Connections | > 80% | > 90% | | Replication lag | > 30s | > 300s | | Disk usage | > 80% | > 90% | 

Conclusion 

Track QPS, latency, connections, cache hit ratio, and replication lag. Use Prometheus and Grafana for collection and visualization. Set meaningful alert thresholds and avoid alert fatigue.

**See also:** [Query Performance Tuning Tools](</en/database/query-performance-tuning.html>), [Connection Pooling Guide](</en/database/connection-pooling.html>), [PostgreSQL vs MySQL vs SQLite in 2026: A Complete Database Guide for Developers](</en/database/postgresql-vs-mysql-2026.html>).

**See also:** [Connection Pooling Guide](</en/database/connection-pooling.html>), [Query Performance Tuning Tools](</en/database/query-performance-tuning.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>)

**See also:** [Connection Pooling Guide](</en/database/connection-pooling.html>), [Query Performance Tuning Tools](</en/database/query-performance-tuning.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>)

**See also:** [Connection Pooling Guide](</en/database/connection-pooling.html>), [Query Performance Tuning Tools](</en/database/query-performance-tuning.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>)

**See also:** [Connection Pooling Guide](</en/database/connection-pooling.html>), [Query Performance Tuning Tools](</en/database/query-performance-tuning.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>)

**See also:** [Connection Pooling Guide](</en/database/connection-pooling.html>), [Query Performance Tuning Tools](</en/database/query-performance-tuning.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>)
