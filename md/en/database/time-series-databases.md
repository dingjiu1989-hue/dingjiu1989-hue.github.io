---
title: "Time Series Databases (InfluxDB, TimescaleDB, ClickHouse)"
description: "Compare InfluxDB, TimescaleDB, and ClickHouse for time-series data workloads including monitoring, IoT, and real-time analytics."
date: 2025-12-24
board: database
url: https://dingjiu1989-hue.github.io/en/database/time-series-databases.html
---

# Time Series Databases (InfluxDB, TimescaleDB, ClickHouse)

Time-Series Data 

Time-series data is a sequence of data points indexed by time. Examples include server metrics, IoT sensor readings, and financial tick data. 

Database Comparison 

| Feature | InfluxDB | TimescaleDB | QuestDB | |---------|----------|-------------|---------| | Architecture | Custom TS engine | PostgreSQL extension | Columnar | | SQL | Flux / SQL | Full SQL | SQL | | Write throughput | Very high | High | Very high | | Compression | Excellent | Good | Excellent | 

InfluxDB 

Purpose-built time-series with automatic downsampling: 

from influxdb_client import InfluxDBClient

client = InfluxDBClient(url="http://localhost:8086", token="my-token")

write_api = client.write_api()

p = Point("cpu").tag("host", "server01").field("usage_user", 45.2)

write_api.write(bucket="metrics", record=p)

TimescaleDB 

PostgreSQL extension with hypertables: 

CREATE TABLE sensor_data (

time TIMESTAMPTZ NOT NULL,

device_id INTEGER,

temperature DOUBLE PRECISION

);

SELECT create_hypertable('sensor_data', 'time');

SELECT time_bucket('5m', time) AS bucket,

AVG(temperature) FROM sensor_data

WHERE time > NOW() - INTERVAL '24h'

GROUP BY bucket;

Performance 

For 1 billion rows, QuestDB and InfluxDB lead on write throughput. TimescaleDB wins on SQL compatibility. Choose based on your query patterns and ecosystem requirements. 

Conclusion 

Choose InfluxDB for purpose-built time-series, TimescaleDB for SQL compatibility, and QuestDB for maximum performance. All support downsampling and retention policies.

**See also:** [Graph Databases (Neo4j, Dgraph, ArangoDB)](</en/database/graph-databases.html>), [OLTP vs OLAP: Workload Optimization](</en/database/oltp-vs-olap.html>), [Data Lake vs Data Warehouse vs Lakehouse](</en/database/data-lake-vs-warehouse.html>).

**See also:** [Graph Databases (Neo4j, Dgraph, ArangoDB)](</en/database/graph-databases.html>), [OLTP vs OLAP: Workload Optimization](</en/database/oltp-vs-olap.html>), [Data Modeling Best Practices](</en/database/data-modeling.html>)

**See also:** [Graph Databases (Neo4j, Dgraph, ArangoDB)](</en/database/graph-databases.html>), [OLTP vs OLAP: Workload Optimization](</en/database/oltp-vs-olap.html>), [Data Modeling Best Practices](</en/database/data-modeling.html>)

**See also:** [Graph Databases (Neo4j, Dgraph, ArangoDB)](</en/database/graph-databases.html>), [OLTP vs OLAP: Workload Optimization](</en/database/oltp-vs-olap.html>), [Data Modeling Best Practices](</en/database/data-modeling.html>)

**See also:** [Graph Databases (Neo4j, Dgraph, ArangoDB)](</en/database/graph-databases.html>), [OLTP vs OLAP: Workload Optimization](</en/database/oltp-vs-olap.html>), [Data Modeling Best Practices](</en/database/data-modeling.html>)

**See also:** [Graph Databases (Neo4j, Dgraph, ArangoDB)](</en/database/graph-databases.html>), [OLTP vs OLAP: Workload Optimization](</en/database/oltp-vs-olap.html>), [Data Modeling Best Practices](</en/database/data-modeling.html>)

**See also:** [Data Lake vs Data Warehouse vs Lakehouse](</en/database/data-lake-vs-warehouse.html>), [Data Warehousing Concepts and Modern Tools](</en/database/data-warehousing.html>), [ACID vs BASE Transactions](</en/database/acid-vs-base.html>)

**See also:** [Data Lake vs Data Warehouse vs Lakehouse](</en/database/data-lake-vs-warehouse.html>), [Data Warehousing Concepts and Modern Tools](</en/database/data-warehousing.html>), [ACID vs BASE Transactions](</en/database/acid-vs-base.html>)

**See also:** [Data Lake vs Data Warehouse vs Lakehouse](</en/database/data-lake-vs-warehouse.html>), [Data Warehousing Concepts and Modern Tools](</en/database/data-warehousing.html>), [ACID vs BASE Transactions](</en/database/acid-vs-base.html>)

**See also:** [Data Lake vs Data Warehouse vs Lakehouse](</en/database/data-lake-vs-warehouse.html>), [Data Warehousing Concepts and Modern Tools](</en/database/data-warehousing.html>), [ACID vs BASE Transactions](</en/database/acid-vs-base.html>)

**See also:** [Data Lake vs Data Warehouse vs Lakehouse](</en/database/data-lake-vs-warehouse.html>), [Data Warehousing Concepts and Modern Tools](</en/database/data-warehousing.html>), [ACID vs BASE Transactions](</en/database/acid-vs-base.html>)

**See also:** [Data Lake vs Data Warehouse vs Lakehouse](</en/database/data-lake-vs-warehouse.html>), [Data Warehousing Concepts and Modern Tools](</en/database/data-warehousing.html>), [ACID vs BASE Transactions](</en/database/acid-vs-base.html>)

**See also:** [Data Lake vs Data Warehouse vs Lakehouse](</en/database/data-lake-vs-warehouse.html>), [Data Warehousing Concepts and Modern Tools](</en/database/data-warehousing.html>), [ACID vs BASE Transactions](</en/database/acid-vs-base.html>)

**See also:** [Data Lake vs Data Warehouse vs Lakehouse](</en/database/data-lake-vs-warehouse.html>), [Data Warehousing Concepts and Modern Tools](</en/database/data-warehousing.html>), [ACID vs BASE Transactions](</en/database/acid-vs-base.html>)

**See also:** [Data Lake vs Data Warehouse vs Lakehouse](</en/database/data-lake-vs-warehouse.html>), [Data Warehousing Concepts and Modern Tools](</en/database/data-warehousing.html>), [ACID vs BASE Transactions](</en/database/acid-vs-base.html>)
