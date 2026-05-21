---
title: "Data Lake vs Data Warehouse vs Lakehouse"
description: "Compare data lake, data warehouse, and lakehouse architectures with Delta Lake, Iceberg, Hudi, and the medallion architecture."
date: 2026-03-26
board: database
url: https://dingjiu1989-hue.github.io/en/database/data-lake-vs-warehouse.html
---

# Data Lake vs Data Warehouse vs Lakehouse

The data landscape has evolved from simple databases to complex architectures spanning data lakes, data warehouses, and the emerging lakehouse paradigm. Understanding the differences between these architectures is essential for building a modern data platform. 

Data Warehouse 

A data warehouse is a centralized repository optimized for structured, processed data used in reporting and analytics. 

Characteristics 

  * **Schema-on-write** : Data must conform to a schema before loading. This ensures quality but adds friction at ingestion time.

  * **Optimized for reads** : Columnar storage, pre-computed aggregations, materialized views, and indexing for fast analytical queries.

  * **Clean, transformed data** : Data goes through ETL/ELT pipelines before it is available for querying.

  * **ACID transactions** : Warehouses support transactions, making them suitable for reliable reporting.




When to Use a Data Warehouse 

  * Business intelligence dashboards.

  * Financial reporting requiring accuracy.

  * Any use case requiring SQL on clean, structured data.

  * Scenarios where query performance is critical (sub-second response).




Limitations 

  * Expensive storage for raw data. Storing terabytes of raw logs in a data warehouse is cost-prohibitive.

  * Rigid schema changes require careful migration.

  * Not designed for unstructured data (images, videos, documents).

  * Data must be transformed before it is useful, adding latency.




Data Lake 

A data lake stores data in its raw, native format. It is a single repository for all data, regardless of structure. 

Characteristics 

  * **Schema-on-read** : Data is stored as-is. Schemas are applied when the data is read, not when it is ingested.

  * **Cheap storage** : Object storage (S3, ADLS, GCS) is an order of magnitude cheaper than warehouse storage.

  * **Any data type** : Structured, semi-structured (JSON, Parquet), unstructured (images, audio, video).

  * **ELT friendly** : Data lands raw, transformations happen later in the lake.




When to Use a Data Lake 

  * Data science and machine learning (access raw data for feature engineering).

  * Log and event data storage at petabyte scale.

  * Archival and data retention.

  * Exploratory analytics where the schema is unknown upfront.




Limitations 

  * **Performance** : Querying raw data directly is slow compared to a warehouse.

  * **No ACID transactions** : Multiple concurrent writers can corrupt data.

  * **Data quality** : Without schema enforcement, data lakes often become "data swamps" with unreliable data.

  * **Governance** : Cataloging and discovering data in a lake requires additional tooling (AWS Glue, Hive Metastore).




Lakehouse Architecture 

The lakehouse combines the flexibility of a data lake with the reliability and performance of a data warehouse. It stores data in object storage with a metadata layer that provides ACID transactions, schema enforcement, and performance optimization. 

Key Innovations 

  * **ACID transactions on object storage** : Atomic commits, rollbacks, and concurrent reader/writer isolation.



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Schema enforcement and evolution** : Enforce schemas on write while allowing controlled evolution. 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Performance optimization** : File layout statistics, compaction, indexing, and caching. 4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Unified batch and streaming** : Same storage for both batch and streaming workloads. 5\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Open formats** : Data stored in Apache Parquet with metadata tracked by open table formats. 

Table Format Comparison 

The lakehouse is enabled by three major open-source table formats. 

Delta Lake 

Delta Lake, developed by Databricks, adds ACID transactions to Parquet files. 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Delta Lake: Create a table

CREATE TABLE sales (

order_id LONG,

customer_id STRING,

amount DOUBLE,

order_date DATE

) USING DELTA;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Delta Lake: Time travel query

SELECT * FROM sales TIMESTAMP AS OF '2026-05-01';

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Delta Lake: Vacuum old versions

VACUUM sales RETAIN 168 HOURS;

Best for: Databricks environments, general purpose lakehouse, Spark workloads. 

Apache Iceberg 

Iceberg was developed at Netflix and is now an Apache top-level project. It is designed for high-performance table management at scale. 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Iceberg: Create a partitioned table

CREATE TABLE sales (

order_id BIGINT,

customer_id STRING,

amount DECIMAL(10,2),

order_date DATE

) USING ICEBERG

PARTITIONED BY (month(order_date));

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Iceberg: Incremental read (only new data)

SELECT * FROM sales

WHERE order_date BETWEEN '2026-05-01' AND '2026-05-12';

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Iceberg: Schema evolution (add column)

ALTER TABLE sales ADD COLUMN discount DECIMAL(5,2);

Best for: Multi-engine environments (Spark, Flink, Trino, Hive), cloud-agnostic deployments. 

Apache Hudi 

Hudi (Hadoop Upserts Deletes and Incrementals) was developed at Uber for real-time data ingestion. 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Hudi: Create a Copy-on-Write table

CREATE TABLE uber_trips (

trip_id BIGINT,

driver_id STRING,

fare DOUBLE,

trip_date DATE

) USING HUDI

TBLPROPERTIES (

primaryKey = 'trip_id',

preCombineField = 'trip_date'

);

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Hudi: Upsert new records

MERGE INTO uber_trips AS target

USING new_trips AS source

ON target.trip_id = source.trip_id

WHEN MATCHED THEN UPDATE SET *

WHEN NOT MATCHED THEN INSERT *;

Best for: Real-time ingestion, upsert-heavy workloads, incremental processing pipelines. 

Medallion Architecture 

The medallion architecture organizes data lakehouse data into layers of increasing quality. 

Bronze Layer (Raw) 

Raw data ingested from source systems. No transformations. Schema-on-read. Data is append-only. 

bronze/orders/

order_date=2026-05-01/

file1.parquet

file2.parquet

order_date=2026-05-02/

file3.parquet

Silver Layer (Cleaned) 

Data is deduplicated, validated, and lightly transformed. Null handling, type casting, and simple joins. This layer serves as the source of truth for analysts. 

## Bronze to Silver transformation

def bronze_to_silver(spark):

bronze_df = spark.read.format("delta").load("/data/bronze/orders")

silver_df = bronze_df \

.dropDuplicates(["order_id"]) \

.filter(col("amount").isNotNull()) \

.withColumn("order_date", to_date(col("order_raw_date"))) \

.withColumn("amount", col("amount").cast("decimal(10,2)"))

silver_df.write \

.format("delta") \

.mode("overwrite") \

.save("/data/silver/orders")

Gold Layer (Aggregated) 

Business-level aggregations and metrics. Data marts for specific teams or use cases. 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Gold layer: Daily sales by region

CREATE TABLE gold.daily_sales_by_region

USING DELTA

AS

SELECT

order_date,

region,

COUNT(DISTINCT customer_id) as unique_customers,

COUNT(*) as order_count,

SUM(amount) as total_revenue

FROM silver.orders

GROUP BY order_date, region;

Architecture Decision Matrix 

| Factor | Warehouse | Data Lake | Lakehouse | |--------|-----------|-----------|-----------| | Data freshness | Hours to days | Minutes to hours | Minutes | | Query performance | Sub-second | Seconds to minutes | Sub-second to seconds | | Storage cost | High | Low | Low | | Schema flexibility | Rigid | Flexible | Schema on write with evolution | | ACID transactions | Yes | No | Yes | | ML/AI support | Limited | Good | Good | | BI tool support | Excellent | Poor | Good to excellent | | Complexity | Low | Medium | Medium-high | 

Migration Path 

Moving from warehouse-only or lake-only architectures to a lakehouse: 

  * **Start with S3/ADLS as a data lake** for raw data ingestion.



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Continue using the warehouse** for BI and reporting. 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Introduce an open table format** (Delta, Iceberg, Hudi) on the lake for ACID properties. 4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Move bronze/silver layers to the lake** while keeping gold aggregations in the warehouse. 5\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Adopt a lakehouse query engine** (Trino, Athena, Databricks SQL) for direct lake queries. 6\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Migrate gold layer to the lakehouse** once performance is acceptable. 

Conclusion 

Data warehouses remain essential for BI and reporting. Data lakes are ideal for raw storage and ML workloads. The lakehouse architecture bridges both worlds by bringing ACID transactions, schema enforcement, and performance optimization to object storage. Choose the medallion architecture (bronze, silver, gold) to organize lakehouse data. Start with a data warehouse, add a lake for raw data, and converge on a lakehouse as your platform matures.

**See also:** [Graph Databases (Neo4j, Dgraph, ArangoDB)](</en/database/graph-databases.html>), [Time Series Databases (InfluxDB, TimescaleDB, ClickHouse)](</en/database/time-series-databases.html>), [Data Modeling Best Practices](</en/database/data-modeling.html>).

**See also:** [Distributed Databases: Concepts and Implementation](</en/database/distributed-databases.html>), [Graph Databases (Neo4j, Dgraph, ArangoDB)](</en/database/graph-databases.html>), [SQL vs NoSQL Decision Guide](</en/database/sql-vs-nosql.html>)

**See also:** [Distributed Databases: Concepts and Implementation](</en/database/distributed-databases.html>), [Graph Databases (Neo4j, Dgraph, ArangoDB)](</en/database/graph-databases.html>), [SQL vs NoSQL Decision Guide](</en/database/sql-vs-nosql.html>)

**See also:** [Distributed Databases: Concepts and Implementation](</en/database/distributed-databases.html>), [Graph Databases (Neo4j, Dgraph, ArangoDB)](</en/database/graph-databases.html>), [SQL vs NoSQL Decision Guide](</en/database/sql-vs-nosql.html>)

**See also:** [Distributed Databases: Concepts and Implementation](</en/database/distributed-databases.html>), [Graph Databases (Neo4j, Dgraph, ArangoDB)](</en/database/graph-databases.html>), [SQL vs NoSQL Decision Guide](</en/database/sql-vs-nosql.html>)

**See also:** [Distributed Databases: Concepts and Implementation](</en/database/distributed-databases.html>), [Graph Databases (Neo4j, Dgraph, ArangoDB)](</en/database/graph-databases.html>), [SQL vs NoSQL Decision Guide](</en/database/sql-vs-nosql.html>)

**See also:** [Data Warehousing Concepts and Modern Tools](</en/database/data-warehousing.html>), [Database Monitoring and Performance Alerting](</en/database/database-monitoring.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>)

**See also:** [Data Warehousing Concepts and Modern Tools](</en/database/data-warehousing.html>), [Database Monitoring and Performance Alerting](</en/database/database-monitoring.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>)

**See also:** [Data Warehousing Concepts and Modern Tools](</en/database/data-warehousing.html>), [Database Monitoring and Performance Alerting](</en/database/database-monitoring.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>)

**See also:** [Data Warehousing Concepts and Modern Tools](</en/database/data-warehousing.html>), [Database Monitoring and Performance Alerting](</en/database/database-monitoring.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>)

**See also:** [Data Warehousing Concepts and Modern Tools](</en/database/data-warehousing.html>), [Database Monitoring and Performance Alerting](</en/database/database-monitoring.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>)

**See also:** [Data Warehousing Concepts and Modern Tools](</en/database/data-warehousing.html>), [Database Monitoring and Performance Alerting](</en/database/database-monitoring.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>)

**See also:** [Data Warehousing Concepts and Modern Tools](</en/database/data-warehousing.html>), [Database Monitoring and Performance Alerting](</en/database/database-monitoring.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>)

**See also:** [Data Warehousing Concepts and Modern Tools](</en/database/data-warehousing.html>), [Database Monitoring and Performance Alerting](</en/database/database-monitoring.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>)

**See also:** [Data Warehousing Concepts and Modern Tools](</en/database/data-warehousing.html>), [Database Monitoring and Performance Alerting](</en/database/database-monitoring.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>)

**See also:** [Data Warehousing Concepts and Modern Tools](</en/database/data-warehousing.html>), [Database Monitoring and Performance Alerting](</en/database/database-monitoring.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>)

**See also:** [Data Warehousing Concepts and Modern Tools](</en/database/data-warehousing.html>), [Database Monitoring and Performance Alerting](</en/database/database-monitoring.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>)

**See also:** [Data Warehousing Concepts and Modern Tools](</en/database/data-warehousing.html>), [Database Monitoring and Performance Alerting](</en/database/database-monitoring.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>)

**See also:** [Data Warehousing Concepts and Modern Tools](</en/database/data-warehousing.html>), [Database Monitoring and Performance Alerting](</en/database/database-monitoring.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>)
