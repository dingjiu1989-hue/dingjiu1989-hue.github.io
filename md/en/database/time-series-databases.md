---
title: "Time Series Databases (InfluxDB, TimescaleDB, ClickHouse)"
description: "Compare InfluxDB, TimescaleDB, and ClickHouse for time-series data workloads including monitoring, IoT, and real-time analytics."
date: 2026-05-11
board: database
url: https://dingjiu1989-hue.github.io/en/database/time-series-databases.html
---

## What Is Time-Series Data?

Time-series data is a sequence of data points indexed by time. Examples include server metrics (CPU, memory), IoT sensor readings, financial tick data, application logs, and user behavior events. Time-series databases are optimized for high write throughput, efficient storage, and fast range queries over time intervals.

## Characteristics of Time-Series Workloads

| Characteristic | Typical Requirement |
|----------------|---------------------|
| Write throughput | Millions of data points per second |
| Data immutability | Appends only, rarely updated |
| Time-ordered queries | "Last 24 hours," "Average per minute this week" |
| Retention policies | Automatic data expiration |
| Downsampling | Roll up old data to lower resolution |

## Time-Series DB Comparison

| Feature | InfluxDB | TimescaleDB | ClickHouse |
|---------|----------|-------------|------------|
| Architecture | Custom TS engine | PostgreSQL extension | Columnar OLAP |
| Query language | Flux / SQL | SQL (full) | SQL (custom dialect) |
| Write throughput | Very high | High | Very high |
| Compression | Excellent | Good (native) | Excellent |
| SQL compatibility | Partial | Full PostgreSQL | ClickHouse SQL |
| Joins | Limited | Full SQL joins | Limited |
| Deployment | Standalone | PostgreSQL-based | Standalone |

## InfluxDB

InfluxDB is a purpose-built time-series database with automatic downsampling and retention policies.

### Data Model

```javascript
// Measurement: cpu
// Tags (indexed): host, region
// Fields (values): usage_user, usage_system, usage_idle
// Timestamp: automatic or explicit

cpu,host=server01,region=us-east1 usage_user=45.2,usage_system=12.1 1715385600
cpu,host=server01,region=us-east1 usage_user=47.8,usage_system=13.4 1715385601
cpu,host=server02,region=us-west1 usage_user=32.1,usage_system=8.9  1715385600
```

### Writing Data

```python
from influxdb_client import InfluxDBClient

client = InfluxDBClient(url="http://localhost:8086", token="my-token")
write_api = client.write_api()

# Write a single point
from influxdb_client.client.write_api import SYNCHRONOUS
p = Point("cpu") \
    .tag("host", "server01") \
    .tag("region", "us-east1") \
    .field("usage_user", 45.2) \
    .field("usage_system", 12.1) \
    .time(datetime.utcnow())

write_api.write(bucket="metrics", record=p)

# Batch write for performance
points = []
for metric in metrics_batch:
    points.append(
        Point("sensor") \
            .tag("device_id", metric.device_id) \
            .field("temperature", metric.temp) \
            .field("humidity", metric.humidity) \
            .time(metric.timestamp)
    )
write_api.write(bucket="iot", record=points)
```

### Querying

```sql
-- InfluxDB SQL (v3+)
SELECT
    time,
    mean(usage_user) AS avg_cpu
FROM cpu
WHERE
    host = 'server01'
    AND time >= now() - interval '1 hour'
GROUP BY time(1m)
ORDER BY time;

-- Downsampling with continuous query
CREATE CONTINUOUS QUERY cpu_1h ON mydb
BEGIN
    SELECT mean(usage_user) AS usage_user
    INTO cpu_1h
    FROM cpu
    GROUP BY time(1h), host
END;
```

## TimescaleDB

TimescaleDB extends PostgreSQL with hypertables that transparently partition data by time.

### Setup

```sql
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Create a regular table
CREATE TABLE sensor_data (
    time TIMESTAMPTZ NOT NULL,
    device_id INTEGER NOT NULL,
    temperature DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    pressure DOUBLE PRECISION
);

-- Convert to hypertable
SELECT create_hypertable('sensor_data', 'time');

-- Add compression policy
ALTER TABLE sensor_data SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'device_id'
);
SELECT add_compression_policy('sensor_data', INTERVAL '7 days');
```

### Querying

```sql
-- Full SQL compatibility
SELECT
    time_bucket('5 minutes', time) AS bucket,
    device_id,
    AVG(temperature) AS avg_temp,
    MAX(temperature) AS max_temp,
    MIN(temperature) AS min_temp
FROM sensor_data
WHERE
    time > NOW() - INTERVAL '24 hours'
    AND device_id = 42
GROUP BY bucket, device_id
ORDER BY bucket DESC;

-- Continuous aggregate (pre-computed rollup)
CREATE MATERIALIZED VIEW sensor_hourly
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', time) AS bucket,
    device_id,
    AVG(temperature) AS avg_temperature
FROM sensor_data
GROUP BY bucket, device_id;

-- Real-time aggregation (includes recent un-materialized data)
SELECT * FROM sensor_hourly
WHERE bucket > NOW() - INTERVAL '7 days'
ORDER BY bucket DESC
LIMIT 100;
```

### When to Use TimescaleDB

- You already use PostgreSQL and need time-series capabilities
- You need SQL JOINs between time-series and relational data
- You value full SQL compatibility for reporting
- Your time-series data has relational context (e.g., sensors belong to locations)

## ClickHouse

ClickHouse is a columnar OLAP database optimized for real-time analytics on large datasets.

### Schema Design

```sql
CREATE TABLE sensor_data (
    timestamp DateTime64(3),
    device_id UInt32,
    temperature Float32,
    humidity Float32,
    pressure Float32,
    location String
) ENGINE = MergeTree()
ORDER BY (device_id, timestamp)
TTL timestamp + INTERVAL 90 DAY DELETE;

-- Distributed version
CREATE TABLE sensor_data_distributed AS sensor_data
ENGINE = Distributed('cluster', 'default', 'sensor_data', rand());
```

### Querying

```sql
-- ClickHouse's strength: fast aggregations on massive datasets
SELECT
    toStartOfMinute(timestamp) AS minute,
    device_id,
    avg(temperature) AS avg_temp,
    quantile(0.95)(temperature) AS p95_temp,
    quantile(0.99)(temperature) AS p99_temp
FROM sensor_data
WHERE timestamp > now() - INTERVAL 7 DAY
GROUP BY minute, device_id
ORDER BY minute DESC
LIMIT 100;

-- Using materialized views for pre-aggregation
CREATE MATERIALIZED VIEW sensor_stats_hourly
ENGINE = AggregatingMergeTree()
ORDER BY (device_id, hour)
AS SELECT
    device_id,
    toStartOfHour(timestamp) AS hour,
    avgState(temperature) AS avg_temp,
    maxState(temperature) AS max_temp
FROM sensor_data
GROUP BY device_id, hour;
```

## Performance Comparison (1B rows)

| Benchmark | InfluxDB | TimescaleDB | ClickHouse |
|-----------|----------|-------------|------------|
| Write speed (rows/s) | 1.2M | 850K | 1.5M |
| Storage (compressed) | 35 GB | 65 GB | 22 GB |
| Last 24h range query | 210ms | 380ms | 120ms |
| Aggregation (1 week) | 1.2s | 2.1s | 0.4s |
| Memory usage | 2 GB | 4 GB | 6 GB |

## Choosing the Right Database

| Use Case | Recommended |
|----------|-------------|
| Infrastructure monitoring (Prometheus compatible) | InfluxDB |
| IoT sensor data with relational context | TimescaleDB |
| Real-time analytics on billions of rows | ClickHouse |
| Simple metrics and events | InfluxDB |
| Full SQL + time-series hybrid | TimescaleDB |
| Log analytics and observability | ClickHouse |

## Summary

Time-series databases optimize for append-heavy, time-ordered data with high compression and fast range queries. Choose InfluxDB for purpose-built time-series with minimal operational overhead, TimescaleDB when you need full SQL compatibility and relational joins with your time-series data, and ClickHouse for real-time analytics on massive datasets. All three support automatic downsampling, retention policies, and continuous aggregates to manage data at scale.
