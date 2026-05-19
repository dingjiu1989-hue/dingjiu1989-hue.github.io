---
title: "Materialized Views"
description: "Using materialized views for performance optimization with refresh strategies, use cases, and SQL examples."
date: 2026-04-10
board: database
url: https://dingjiu1989-hue.github.io/en/database/materialized-views.html
---

# Materialized Views

What are Materialized Views? 

Materialized views pre-compute and store query results. Unlike regular views, they persist data on disk, trading storage for query speed. 

Creating Materialized Views 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- PostgreSQL: materialized view for daily sales

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

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Add index for faster queries

CREATE INDEX idx_daily_sales_date ON daily_sales_summary(date);

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Query is much faster than the original

SELECT * FROM daily_sales_summary

WHERE date >= '2026-01-01';

Refresh Strategies 

Complete Refresh 

Rebuilds the entire view: 

REFRESH MATERIALIZED VIEW daily_sales_summary;

Simple but locks the view during refresh. Best for small datasets or low-frequency refreshes. 

Concurrent Refresh 

Creates a new version and swaps atomically. No lock but requires a unique index: 

CREATE UNIQUE INDEX idx_daily_sales_pk ON daily_sales_summary(date, category);

REFRESH MATERIALIZED VIEW CONCURRENTLY daily_sales_summary;

Incremental Refresh 

Only processes changed data. Not natively supported in PostgreSQL but available in specialized databases. 

Use Cases 

| Use Case | Refresh Frequency | Benefit | |----------|------------------|---------| | Dashboards | Hourly | Sub-second queries | | Aggregations | Daily | Avoid full table scans | | Pre-joined data | On-demand | Eliminate expensive joins | | Reporting | Nightly | Consistent snapshot | 

Performance Considerations 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Compare query performance

EXPLAIN ANALYZE

SELECT date, SUM(total_sales)

FROM daily_sales_summary

WHERE date >= '2026-01-01'

GROUP BY date;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- vs the base query (much slower)

EXPLAIN ANALYZE

SELECT d.date, SUM(s.amount)

FROM fact_sales s

JOIN dim_date d ON s.date_id = d.date_id

WHERE d.date >= '2026-01-01'

GROUP BY d.date;

Conclusion 

Materialized views are essential for dashboard and reporting performance. Use concurrent refresh to avoid locks. Add indexes on frequently filtered columns. Choose refresh strategy based on freshness requirements. Monitor storage overhead for large views.

**See also:** [SQL vs NoSQL in 2026](</en/database/sql-vs-nosql-2026.html>), [Database Views: Simple, Materialized, and Updateable Views](</en/database/database-views.html>), [Database Triggers: Use Cases, Performance Costs, and Alternatives](</en/database/triggers-patterns.html>).

**See also:** [Database Triggers: Use Cases, Performance Costs, and Alternatives](</en/database/triggers-patterns.html>), [SQL vs NoSQL in 2026](</en/database/sql-vs-nosql-2026.html>), [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>)

**See also:** [Database Triggers: Use Cases, Performance Costs, and Alternatives](</en/database/triggers-patterns.html>), [SQL vs NoSQL in 2026](</en/database/sql-vs-nosql-2026.html>), [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>)

**See also:** [Database Triggers: Use Cases, Performance Costs, and Alternatives](</en/database/triggers-patterns.html>), [SQL vs NoSQL in 2026](</en/database/sql-vs-nosql-2026.html>), [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>)

**See also:** [Database Triggers: Use Cases, Performance Costs, and Alternatives](</en/database/triggers-patterns.html>), [SQL vs NoSQL in 2026](</en/database/sql-vs-nosql-2026.html>), [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>)

**See also:** [Database Triggers: Use Cases, Performance Costs, and Alternatives](</en/database/triggers-patterns.html>), [SQL vs NoSQL in 2026](</en/database/sql-vs-nosql-2026.html>), [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>)

**See also:** [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>)

**See also:** [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>)

**See also:** [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>)

**See also:** [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>)

**See also:** [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>)
