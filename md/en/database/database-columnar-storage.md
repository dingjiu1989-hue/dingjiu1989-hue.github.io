---
title: "Columnar Storage: Compression, Encoding, and Analytical Performance"
description: "Understand columnar storage formats: row vs column orientation, encoding techniques, and analytical query optimization."
date: 2026-05-12
board: database
url: https://dingjiu1989-hue.github.io/en/database/database-columnar-storage.html
---

# Columnar Storage: Compression, Encoding, and Analytical Performance

# Columnar Storage: Compression, Encoding, and Analytical Performance

# Columnar Storage: Compression, Encoding, and Analytical Performance

# Columnar Storage: Compression, Encoding, and Analytical Performance

# Columnar Storage: Compression, Encoding, and Analytical Performance

# Columnar Storage: Compression, Encoding, and Analytical Performance

# Columnar Storage: Compression, Encoding, and Analytical Performance

# Columnar Storage: Compression, Encoding, and Analytical Performance

# Columnar Storage: Compression, Encoding, and Analytical Performance

# Columnar Storage: Compression, Encoding, and Analytical Performance

# Columnar Storage: Compression, Encoding, and Analytical Performance

# Columnar Storage: Compression, Encoding, and Analytical Performance

Columnar storage organizes data by column rather than by row. Instead of storing all fields of a row together, columnar databases store each column's values contiguously. This organization dramatically improves analytical query performance and compression.

## Row vs Column Orientation

Row-oriented storage (PostgreSQL, MySQL, SQL Server) stores entire rows together: [id1, name1, price1], [id2, name2, price2]. This is optimal for OLTP workloads that access many columns for a few rows. Row storage excels at point lookups, inserts, and updates.

Column-oriented storage (ClickHouse, Snowflake, BigQuery) stores each column separately: [id1, id2, id3], [name1, name2, name3], [price1, price2, price3]. This is optimal for analytical queries that access few columns for many rows. Column storage reads only the needed columns, reducing I/O.

A query like SELECT SUM(price) FROM orders WHERE year = 2026 reads only the price and year columns. In row storage, it reads the entire row including irrelevant columns. Column storage reads 10-100x less data for typical analytical queries.

## Compression Techniques

Columnar storage enables column-specific compression. Values in a column share the same data type and often have low cardinality or predictable patterns. This yields compression ratios of 5-20x on typical analytical data.

Run-length encoding (RLE) stores repeating values as (value, count) pairs. RLE excels on sorted columns with few distinct values. Status codes, category IDs, and date partitions compress extremely well with RLE.

Delta encoding stores differences between consecutive values. Good for sorted numeric columns like timestamps or sequential IDs. Each value is stored as the difference from the previous value, which is small and compresses well.

Dictionary encoding replaces repeating string values with integer codes. Common with RLE for low-cardinality columns. Dictionary encoding works well on enumeration-like columns: country codes, product categories, status fields.

Zone maps store min/max values per block of rows. Query pruning skips blocks entirely when the WHERE clause cannot match. Zone maps are especially effective for range-partitioned data.

## Columnar Query Optimization

Vectorized execution processes data in batches (typically 1024 values) rather than row-by-row. This maximizes CPU cache utilization and enables SIMD instructions. Columnar databases process 1-10 billion rows per second per core with vectorized execution.

Late materialization defers row assembly until after filtering and aggregation. The query engine processes each column independently, combining results only when needed. This avoids constructing full rows that would be immediately discarded.

Projection pushdown ensures the database reads only columns referenced in the query. Analytical queries typically touch 5-10% of columns. Columnar storage naturally enables this optimization.

## When to Use Columnar

Use columnar storage for data warehousing, business intelligence dashboards, time-series aggregation, and log analytics. Use row storage for transaction processing, user-facing applications, and point queries. Hybrid databases supporting both access patterns are becoming more common.

**See also:** [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>), [Database Query Profiling: Finding and Fixing Performance Bottlenecks](</en/database/database-query-profiling.html>).

**See also:** [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>), [Database Cost Optimization: Instance Sizing, Reserved Instances, Storage Tiering](</en/database/database-cost-optimization.html>)
