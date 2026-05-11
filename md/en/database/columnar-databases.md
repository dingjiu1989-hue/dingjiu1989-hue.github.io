---
title: "Columnar Databases: When and How to Use Them"
description: "Columnar databases like ClickHouse, Redshift, and BigQuery, their compression techniques, query performance advantages, and use cases."
date: 2026-05-12
board: database
url: https://dingjiu1989-hue.github.io/en/database/columnar-databases.html
---

Columnar databases store data by column rather than by row. This seemingly simple difference has profound implications for analytical query performance, compression, and storage efficiency. This article explains how columnar databases work, when to use them, and how they compare to traditional row-oriented databases.

## Row-Oriented vs Columnar Storage

### Row-Oriented Storage

Row-oriented databases (PostgreSQL, MySQL, SQL Server) store all columns of a row together on disk.

```
Row 1: [id=1, name=Alice, age=30, city=NYC]
Row 2: [id=2, name=Bob, age=25, city=SFO]
Row 3: [id=3, name=Charlie, age=35, city=NYC]
```

**Best for**: Transactions (OLTP). When you need to read or write entire rows (SELECT * WHERE id = N), row-oriented is optimal.

### Columnar Storage

Columnar databases store each column's values together on disk.

```
Column id:     [1, 2, 3]
Column name:   [Alice, Bob, Charlie]
Column age:    [30, 25, 35]
Column city:   [NYC, SFO, NYC]
```

**Best for**: Analytics (OLAP). When you need to scan many rows but only a few columns (SELECT SUM(amount) WHERE date > ...), columnar is dramatically faster.

## Compression Techniques

Columnar storage enables compression techniques that are not effective on row-oriented data, because values in a single column tend to be similar.

### Run-Length Encoding (RLE)

RLE replaces consecutive identical values with a count. It is highly effective on sorted columns with low cardinality.

```
City column before RLE: [NYC, NYC, NYC, SFO, SFO, NYC, NYC, NYC, NYC]
City column after RLE:  [NYC:3, SFO:2, NYC:4]
```

If the city column is sorted, compression improves further:

```
Sorted city column:     [NYC, NYC, NYC, NYC, NYC, NYC, NYC, SFO, SFO]
RLE after sorting:      [NYC:7, SFO:2]
```

### Dictionary Encoding

Dictionary encoding replaces repeated values with smaller integer codes.

```
Dictionary:
  0: NYC
  1: SFO
  2: CHI

Column stored as integers: [0, 0, 1, 0, 2, 2, 1]
Integer array can be further compressed with RLE or bit-packing.
```

### Delta Encoding

Delta encoding stores the difference between consecutive values rather than the values themselves. It is effective for monotonically increasing values like timestamps or sequential IDs.

```
Original: [1000, 1005, 1010, 1020, 1030]
Deltas:   [1000, 5, 5, 10, 10]
```

### Bitmap Indexing

For low-cardinality columns, columnar databases create bitmap indexes. Each distinct value has a bitmap where each bit represents whether a row has that value.

```
City:    [NYC, SFO, NYC, CHI, SFO, NYC]
NYC:     [1, 0, 1, 0, 0, 1]
SFO:     [0, 1, 0, 0, 1, 0]
CHI:     [0, 0, 0, 1, 0, 0]
```

Bitmap operations (AND, OR, NOT) are extremely fast using CPU bitwise instructions.

### Compression Ratios

Columnar databases typically achieve 5-10x compression compared to row-oriented storage on analytical workloads. This means more data fits in memory, further improving performance.

## Query Performance

Columnar databases excel at queries that scan many rows but access few columns.

### The Advantage

```sql
-- Analytical query: Poor performance on row-oriented DB
-- Needs to scan all rows but only reads one column
SELECT region, SUM(revenue)
FROM sales
WHERE year = 2026
GROUP BY region;
```

In a row-oriented database, this query reads all columns for every matching row, wasting I/O and memory on unused data.

In a columnar database:
1. Only the `year` column is scanned to find matching rows.
2. Only the `region` and `revenue` columns are read for matching rows.
3. Columnar compression reduces the data volume.
4. The database can use vectorized processing (SIMD instructions) on compressed column data.

### Vectorized Query Execution

Columnar databases use vectorized execution: instead of processing one row at a time, they process batches of rows (typically 1024 or 4096) using CPU SIMD instructions.

```python
# Pseudocode: Vectorized processing vs row-by-row
# Row-by-row (slow)
total = 0
for row in rows:
    if row['region'] == target_region:
        total += row['revenue']

# Vectorized (fast)
region_column = load_column('region')
revenue_column = load_column('revenue')
mask = region_column == target_region  # SIMD comparison
filtered_revenue = revenue_column[mask]  # SIMD gather
total = sum(filtered_revenue)  # SIMD reduction
```

## Columnar Database Platforms

### ClickHouse

ClickHouse is an open-source columnar database designed for real-time analytics. It is known for exceptional query speed on large datasets.

```sql
-- ClickHouse: Create a MergeTree table
CREATE TABLE sales (
    order_id UInt64,
    order_date Date,
    customer_id UInt32,
    amount Float64,
    region String
) ENGINE = MergeTree()
ORDER BY (order_date, region)
PARTITION BY toYYYYMM(order_date);

-- ClickHouse: Aggregation query
SELECT
    region,
    toMonth(order_date) as month,
    count() as order_count,
    sum(amount) as total_revenue
FROM sales
WHERE order_date >= '2026-01-01'
GROUP BY region, month
ORDER BY total_revenue DESC;
```

**Best for**: Real-time analytics, time-series data, event logging, monitoring dashboards.

### Amazon Redshift

Redshift uses columnar storage with automatic compression encoding selection.

```sql
-- Redshift: Create a columnar table with sort key
CREATE TABLE sales (
    order_id BIGINT ENCODE ZSTD,
    order_date DATE ENCODE DELTA,
    region VARCHAR(50) ENCODE BYTEDICT,
    amount DECIMAL(10,2) ENCODE ZSTD
)
DISTKEY(region)
SORTKEY(order_date, region);
```

Redshift automatically selects the best compression encoding based on sample data.

### Google BigQuery

BigQuery uses the Capacitor columnar storage format, which is proprietary and automatically optimized.

```sql
-- BigQuery: Partitioned and clustered table
CREATE TABLE mydataset.sales
PARTITION BY DATE(order_date)
CLUSTER BY region, customer_id
AS SELECT * FROM source_table;
```

BigQuery charges by bytes processed, not storage. Columnar storage and clustering minimize bytes scanned.

## Columnar vs Row-Oriented Comparison

| Aspect | Row-Oriented | Columnar |
|--------|--------------|----------|
| Read pattern | Full rows | Few columns, many rows |
| Write pattern | Single rows | Batches preferred |
| Compression | 1-2x | 5-10x |
| Range scan | Efficient | Very efficient |
| Point query | Very efficient | Less efficient |
| Inserts/updates | Efficient | Expensive |
| Concurrency | High | Lower |
| Use case | OLTP | OLAP / Analytics |

### When to Use Columnar

- Reporting and dashboards.
- Time-series analysis.
- Log analytics.
- Business intelligence workloads.
- Data warehousing.
- Any query that aggregates large datasets.

### When NOT to Use Columnar

- Transactional workloads with frequent single-row inserts and updates.
- Applications requiring high concurrency with many small queries.
- Systems needing real-time point lookups by primary key.
- Write-heavy workloads (columnar compresses data in batches, individual inserts are expensive).

## Hybrid Approaches

Some databases use hybrid storage to handle both OLTP and OLAP workloads.

### PostgreSQL + Columnar Extensions

```sql
-- PostgreSQL with pg_analytics extension for columnar execution
CREATE EXTENSION pg_analytics;

-- Set a table to use columnar storage
ALTER TABLE large_analytics_table SET ACCESS METHOD columnar;
```

### HTAP (Hybrid Transactional/Analytical Processing)

HTAP databases handle both workloads in a single system:

- **SingleStore**: Row-oriented for transactions, columnar for analytics, automatically routed.
- **Amazon Aurora**: Row-oriented MySQL/PostgreSQL compatible with parallel query for analytical workloads.
- **MySQL HeatWave**: In-memory columnar engine for MySQL with automatic query offloading.

## Conclusion

Columnar databases are essential for modern analytical workloads. Their storage format enables aggressive compression (5-10x), vectorized query execution, and dramatically faster queries when scanning many rows but few columns. Choose ClickHouse for real-time analytics, Redshift for cloud data warehousing, BigQuery for serverless analytics, and columnar extensions or HTAP databases when you need hybrid capabilities. Use row-oriented databases for transactional workloads and switch to columnar for analytics.
