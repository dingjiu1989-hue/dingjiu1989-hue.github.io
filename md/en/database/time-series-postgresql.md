---
title: "Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates"
description: "Learn time-series data management with PostgreSQL and TimescaleDB. Hypertables, continuous aggregates, data retention, and query optimization for time-series workloads."
date: 2026-04-09
board: database
url: https://dingjiu1989-hue.github.io/en/database/time-series-postgresql.html
---

# Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates

Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates 

Time-series data powers monitoring systems, IoT applications, financial tick data, and analytics pipelines. PostgreSQL with TimescaleDB offers a robust solution that combines SQL power with time-series optimizations. 

The Time-Series Challenge 

Time-series workloads differ from traditional OLTP: 

  * **Append-heavy** : Most data is inserted, rarely updated.

  * **Time-ordered** : Queries filter on time ranges.

  * **Downsampling** : Old data is aggregated and retained at lower granularity.

  * **Retention** : Data older than a threshold is dropped automatically.




Hypertables 

TimescaleDB's central abstraction is the hypertable, which automatically partitions data by time: 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Enable the extension

CREATE EXTENSION IF NOT EXISTS timescaledb;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Create a regular table

CREATE TABLE sensor_readings (

time TIMESTAMPTZ NOT NULL,

sensor_id INTEGER NOT NULL,

temperature DOUBLE PRECISION,

humidity DOUBLE PRECISION,

pressure DOUBLE PRECISION

);

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Convert to hypertable, partitioned by time

SELECT create_hypertable('sensor_readings', 'time',

chunk_time_interval => INTERVAL '1 day');

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Optional: space partition by sensor_id for parallel I/O

SELECT add_dimension('sensor_readings',

create_hypertable_index('sensor_readings', 'sensor_id', 4));

TimescaleDB automatically creates chunks (internal partitions), each covering one day of data. Queries that filter on `time` prune irrelevant chunks, similar to declarative partitioning. 

Inserting Data 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Inserts work exactly as with regular tables

INSERT INTO sensor_readings (time, sensor_id, temperature, humidity, pressure)

SELECT

generate_series('2026-01-01', '2026-05-12', INTERVAL '1 minute'),

(random() * 100)::INTEGER + 1,

random() * 35 + 5,

random() * 60 + 20,

random() * 50 + 950;

Querying Data 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Time-range queries prune chunks automatically

SELECT time, temperature

FROM sensor_readings

WHERE sensor_id = 42

AND time BETWEEN '2026-05-10' AND '2026-05-11'

ORDER BY time;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Chunk pruning visible in explain plan

EXPLAIN (ANALYZE, BUFFERS)

SELECT avg(temperature) FROM sensor_readings

WHERE time > now() - INTERVAL '1 hour';

Continuous Aggregates 

Continuous aggregates are TimescaleDB's answer to materialized views for time-series. They automatically and incrementally maintain pre-computed aggregations: 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Create a continuous aggregate

CREATE MATERIALIZED VIEW hourly_stats

WITH (timescaledb.continuous) AS

SELECT

time_bucket('1 hour', time) AS bucket,

sensor_id,

COUNT(*) AS readings,

AVG(temperature) AS avg_temp,

MAX(temperature) AS max_temp,

MIN(temperature) AS min_temp,

AVG(humidity) AS avg_humidity

FROM sensor_readings

GROUP BY bucket, sensor_id;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Set refresh policy: refresh every hour, keep 7 days of data

SELECT add_continuous_aggregate_policy('hourly_stats',

start_offset => INTERVAL '3 days',

end_offset => INTERVAL '1 hour',

schedule_interval => INTERVAL '1 hour'

);

Continuous aggregates update incrementally: only the time buckets that have new data are recomputed. This makes them viable for real-time dashboards. 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Query the continuous aggregate

SELECT bucket, avg_temp, max_temp

FROM hourly_stats

WHERE sensor_id = 42

AND bucket >= now() - INTERVAL '7 days'

ORDER BY bucket;

Data Retention 

Time-series data grows indefinitely without a retention policy. TimescaleDB provides native retention policies: 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Drop chunks older than 90 days

SELECT add_retention_policy('sensor_readings',

drop_after => INTERVAL '90 days');

The drop operation is nearly instant because it removes entire chunks rather than individual rows. 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Manual chunk management

SELECT show_chunks('sensor_readings');

SELECT drop_chunks('sensor_readings', older_than => INTERVAL '90 days');

SELECT reorder_chunk('_hyper_1_1_chunk', 'sensor_readings_time_idx');

Compression 

TimescaleDB's native compression is designed for time-series data: 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Enable compression

ALTER TABLE sensor_readings SET (

timescaledb.compress,

timescaledb.compress_segmentby = 'sensor_id',

timescaledb.compress_orderby = 'time DESC'

);

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Set compression policy: compress chunks older than 7 days

SELECT add_compression_policy('sensor_readings',

compress_after => INTERVAL '7 days');

TimescaleDB reports 90-95% compression ratios for typical sensor data because consecutive readings from the same sensor are highly correlated. 

Performance Optimization 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Index for typical queries

CREATE INDEX idx_sensor_time ON sensor_readings (sensor_id, time DESC);

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Use timescaledb toolkit extension for advanced analytics

CREATE EXTENSION timescaledb_toolkit;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Approximate percentile

SELECT

time_bucket('1 hour', time) AS bucket,

approx_percentile(0.95, percentile_agg(temperature)) AS p95_temp

FROM sensor_readings

WHERE sensor_id = 42

GROUP BY bucket;

PostgreSQL vs Dedicated Time-Series Databases 

| Feature | TimescaleDB | InfluxDB | ClickHouse | |---------|------------|----------|------------| | Query language | Full SQL | Flux | SQL-like | | Joins | Full support | Limited | Moderate | | ACID transactions | Yes | No | Limited | | Compression ratio | 90-95% | 90-95% | 90-99% | | Ingestion rate | 1M+ rows/sec | 1M+ rows/sec | 10M+ rows/sec | | Ecosystem | PostgreSQL ecosystem | Grafana mainly | Analytics tools | 

TimescaleDB is the right choice when you need: 

  * Full SQL and JOIN capabilities across time-series and relational data.

  * ACID guarantees for insert patterns.

  * Existing PostgreSQL tooling (PgBouncer, pgBadger, ORMs).

  * A single database for both transactional and time-series workloads.




The combination of hypertables, continuous aggregates, and compression makes PostgreSQL with TimescaleDB a compelling default choice for time-series data that coexists with relational data.

**See also:** [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Query Parameterization: Bind Parameters, Prepared Statements, and SQL Injection](</en/database/query-parameters.html>).

**See also:** [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Slow Query Troubleshooting: Identification, Profiling, and Optimization](</en/database/database-slow-query-fix.html>)

**See also:** [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Slow Query Troubleshooting: Identification, Profiling, and Optimization](</en/database/database-slow-query-fix.html>)

**See also:** [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Slow Query Troubleshooting: Identification, Profiling, and Optimization](</en/database/database-slow-query-fix.html>)

**See also:** [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Slow Query Troubleshooting: Identification, Profiling, and Optimization](</en/database/database-slow-query-fix.html>)

**See also:** [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Slow Query Troubleshooting: Identification, Profiling, and Optimization](</en/database/database-slow-query-fix.html>)

**See also:** [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>), [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>), [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>), [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)
