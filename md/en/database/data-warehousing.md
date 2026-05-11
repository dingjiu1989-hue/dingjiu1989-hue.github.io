---
title: "Data Warehousing Concepts and Modern Tools"
description: "Understand star schema vs snowflake, ETL/ELT, and modern data warehouses including Snowflake, BigQuery, Redshift, and materialized views."
date: 2026-05-12
board: database
url: https://dingjiu1989-hue.github.io/en/database/data-warehousing.html
---

A data warehouse is a central repository for integrated data from multiple sources, optimized for analytical queries and reporting. Unlike operational databases that handle transactions, data warehouses are designed for read-heavy, complex queries across large datasets.

## Schema Design: Star vs Snowflake

### Star Schema

The star schema is the simplest and most common data warehouse schema. It has one or more fact tables referencing multiple dimension tables.

- **Fact tables**: Contain quantitative data (sales amounts, quantities, counts). They grow rapidly and are typically the largest tables in the warehouse.
- **Dimension tables**: Contain descriptive attributes (customer names, product categories, dates). They are smaller and change slowly.

```
Fact_Sales
  |-- sale_id (PK)
  |-- date_id (FK -> Dim_Date)
  |-- product_id (FK -> Dim_Product)
  |-- customer_id (FK -> Dim_Customer)
  |-- store_id (FK -> Dim_Store)
  |-- quantity
  |-- amount

Dim_Date
  |-- date_id (PK)
  |-- date
  |-- year
  |-- quarter
  |-- month
  |-- day

Dim_Product
  |-- product_id (PK)
  |-- product_name
  |-- category
  |-- price
```

Star schemas are easy to understand, perform well with simple joins, and are the preferred schema for most OLAP tools.

### Snowflake Schema

The snowflake schema normalizes dimension tables into multiple related tables. A product dimension might split into product, category, and department tables.

```
Fact_Sales
  |-- product_id (FK -> Dim_Product)

Dim_Product
  |-- product_id (PK)
  |-- product_name
  |-- category_id (FK -> Dim_Category)

Dim_Category
  |-- category_id (PK)
  |-- category_name
  |-- department_id (FK -> Dim_Department)
```

Snowflake schemas save storage by eliminating redundancy in dimensions. However, they require more joins for queries, which can impact performance. In practice, most modern data warehouses use star schemas or heavily denormalized designs.

### Star vs Snowflake: When to Use

| Aspect | Star | Snowflake |
|--------|------|-----------|
| Query simplicity | Simple joins | Complex joins |
| Query performance | Faster | Slightly slower |
| Storage | More (denormalized) | Less (normalized) |
| ETL complexity | Simple | Moderate |
| Dimensional updates | Requires updates in place | Easier partial updates |

Most modern data warehouses use star schemas with some denormalization for performance-critical dimensions.

## ETL vs ELT

### ETL (Extract, Transform, Load)

ETL transforms data before loading it into the warehouse. Transformations happen on a dedicated staging server.

```
Extract -> Transform -> Load
```

**When ETL makes sense**:
- Legacy systems with limited compute power.
- Data requires significant cleaning before loading.
- Compliance requirements mandate data masking before storage.

### ELT (Extract, Load, Transform)

ELT loads raw data into the warehouse first, then transforms it using the warehouse's compute power.

```
Extract -> Load -> Transform
```

**When ELT makes sense**:
- Modern cloud data warehouses with elastic compute (Snowflake, BigQuery).
- Raw data is needed for future analysis (data lakehouse pattern).
- Transformations are exploratory and iterative.
- You want to decouple data ingestion from transformation.

ELT is the dominant pattern for modern data warehouses because cloud warehouses compute separately from storage, making transformation compute essentially unlimited.

## Modern Data Warehouse Platforms

### Snowflake

Snowflake is a cloud-native data warehouse with unique architecture separating storage and compute.

Key features:
- **Storage**: Compressed columnar format in cloud object storage (S3, Azure Blob).
- **Compute**: Virtual warehouses (clusters) that can scale independently and can be paused.
- **Concurrency**: Multiple virtual warehouses can access the same data without contention.
- **Time travel**: Query data as it existed at any point in the past 90 days.
- **Zero-copy cloning**: Instantly clone databases or schemas without copying data.

```sql
-- Snowflake: Create a virtual warehouse
CREATE WAREHOUSE analytics_wh
  WITH WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 300
  AUTO_RESUME = TRUE;

-- Snowflake: Clone a table with time travel
CREATE TABLE sales_restore CLONE sales
  AT (TIMESTAMP => '2026-05-01 12:00:00'::TIMESTAMP);
```

### Google BigQuery

BigQuery is Google's serverless data warehouse. There is no infrastructure to manage — storage and compute are fully managed.

Key features:
- **Automatic scaling**: No clusters or nodes to configure.
- **Columnar storage**: Capacitor columnar storage format with automatic compression.
- **BigQuery Omni**: Query data across AWS, Azure, and GCP.
- **BI Engine**: In-memory analysis for sub-second query responses.
- **Machine learning**: Run ML models directly in SQL with BigQuery ML.

```sql
-- BigQuery: Partitioned table for efficient queries
CREATE TABLE mydataset.sales_partitioned
  (order_id INT64, amount FLOAT64, order_date DATE)
  PARTITION BY order_date
  OPTIONS(require_partition_filter = TRUE);

-- BigQuery ML: Create a linear regression model
CREATE MODEL mydataset.sales_forecast
  OPTIONS(model_type='linear_reg') AS
  SELECT amount, order_date
  FROM mydataset.sales;
```

### Amazon Redshift

Redshift is AWS's petabyte-scale data warehouse. It is based on a modified PostgreSQL and uses a leader-node/follower-node architecture.

Key features:
- **Massively Parallel Processing (MPP)**: Data is distributed across compute nodes.
- **Distribution styles**: KEY, EVEN, and ALL distribution control how data is distributed across slices.
- **Sort keys**: Compound and interleaved sort keys improve query performance for filtered queries.
- **Redshift Spectrum**: Query data directly in S3 without loading it into Redshift.
- **Concurrency Scaling**: Automatically adds capacity for spikes in concurrent queries.

```sql
-- Redshift: Create table with distribution and sort key
CREATE TABLE sales (
    sale_id BIGINT DISTKEY,
    customer_id INT,
    sale_date DATE SORTKEY,
    amount DECIMAL(10,2)
);

-- Redshift Spectrum: Query external data in S3
CREATE EXTERNAL TABLE spectrum.sales (
    sale_id BIGINT,
    amount DECIMAL(10,2)
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
LOCATION 's3://my-bucket/sales-parquet/';
```

## Materialized Views

Materialized views pre-compute and store query results. They trade storage for query performance and are essential for dashboards and recurring reports.

```sql
-- Create a materialized view for daily sales aggregations
CREATE MATERIALIZED VIEW daily_sales_summary AS
SELECT
    d.date,
    p.category,
    COUNT(*) as sale_count,
    SUM(s.amount) as total_sales
FROM fact_sales s
JOIN dim_date d ON s.date_id = d.date_id
JOIN dim_product p ON s.product_id = p.product_id
GROUP BY d.date, p.category;

-- Refresh the materialized view
REFRESH MATERIALIZED VIEW daily_sales_summary;

-- Query the materialized view (much faster than the base query)
SELECT * FROM daily_sales_summary
WHERE date >= '2026-01-01';
```

Materialized views are most useful for:
- Aggregations over large fact tables (monthly totals, category summaries).
- Pre-joined tables that are expensive to join each time.
- Data that does not need real-time freshness.

## Conclusion

Modern data warehousing has evolved from on-premise appliances to cloud-native platforms with elastic scaling, columnar storage, and separated compute and storage. Star schemas remain the standard for analytical modeling. ELT has largely replaced ETL for cloud warehouses. Snowflake, BigQuery, and Redshift each offer different trade-offs in terms of management overhead, scaling, and query performance. Choose based on your team's expertise and specific workload requirements.
