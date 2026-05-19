---
title: "Slow Query Troubleshooting: Identification, Profiling, and Optimization"
description: "Learn systematic slow query troubleshooting: identifying problematic queries, profiling with EXPLAIN ANALYZE, optimization workflow, and performance regression prevention."
date: 2026-04-03
board: database
url: https://dingjiu1989-hue.github.io/en/database/database-slow-query-fix.html
---

# Slow Query Troubleshooting: Identification, Profiling, and Optimization

## Slow Query Troubleshooting: Identification, Profiling, and Optimization

### Slow Query Troubleshooting: Identification, Profiling, and Optimization

#### Slow Query Troubleshooting: Identification, Profiling, and Optimization

#### Slow Query Troubleshooting: Identification, Profiling, and Optimization

#### Slow Query Troubleshooting: Identification, Profiling, and Optimization

#### Slow Query Troubleshooting: Identification, Profiling, and Optimization

#### Slow Query Troubleshooting: Identification, Profiling, and Optimization

#### Slow Query Troubleshooting: Identification, Profiling, and Optimization

#### Slow Query Troubleshooting: Identification, Profiling, and Optimization

#### Slow Query Troubleshooting: Identification, Profiling, and Optimization

#### Slow Query Troubleshooting: Identification, Profiling, and Optimization

#### Slow Query Troubleshooting: Identification, Profiling, and Optimization

#### Slow Query Troubleshooting: Identification, Profiling, and Optimization

#### Slow Query Troubleshooting: Identification, Profiling, and Optimization

#### Slow Query Troubleshooting: Identification, Profiling, and Optimization

Slow Query Troubleshooting: Identification, Profiling, and Optimization 

Slow queries are the most common database performance problem. This article presents a systematic workflow: from identifying the slowest queries through profiling to implementing and verifying optimizations. 

Step 1: Identify Slow Queries 

Using pg_stat_statements 

Enable the extension and query for the worst performers: 

CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Top 10 queries by total execution time

SELECT queryid,

LEFT(query, 100) AS query_preview,

calls,

ROUND(total_exec_time::numeric, 2) AS total_ms,

ROUND(mean_exec_time::numeric, 2) AS avg_ms,

ROUND(min_exec_time::numeric, 2) AS min_ms,

ROUND(max_exec_time::numeric, 2) AS max_ms,

ROUND(stddev_exec_time::numeric, 2) AS stddev_ms,

rows,

shared_blks_hit,

shared_blks_read,

shared_blks_dirtied,

shared_blks_written

FROM pg_stat_statements

WHERE query NOT LIKE '%pg_stat%'

ORDER BY total_exec_time DESC

LIMIT 20;

Focus on queries with: 

  * High `total_exec_time`: Consuming the most database time overall.

  * High `mean_exec_time`: Individually slow queries.

  * High `stddev_exec_time`: Performance varies wildly (plan instability).

  * Low cache hit ratio: `(shared_blks_hit / NULLIF(shared_blks_hit + shared_blks_read, 0)) < 0.99`.




Using pg_stat_activity 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Current running queries

SELECT pid, now() - query_start AS duration, state, query

FROM pg_stat_activity

WHERE state = 'active'

AND query_start < now() - interval '5 seconds'

ORDER BY duration DESC;

External Tools 

#### pgBadger: parse PostgreSQL logs for slow queries

pgbadger /var/log/postgresql/postgresql.log -o report.html

#### pgFincore: analyze cache hit rates

#### pgbouncer logs for pool-level insights

Step 2: Profile the Problem Query 

Once identified, profile the slow query: 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Reset statistics for this specific query

SELECT pg_stat_statements_reset();

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Run the query once

EXPLAIN (ANALYZE, BUFFERS, TIMING) 

SELECT u.email, COUNT(o.id) AS order_count

FROM users u

LEFT JOIN orders o ON o.user_id = u.id

WHERE u.created_at > '2026-01-01'

GROUP BY u.email

ORDER BY order_count DESC

LIMIT 100;

What to Look For in the Plan 

  * **Seq Scan on a large table** when only a few rows are needed → Add an index.



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Large discrepancy between estimated rows and actual rows** → Run `ANALYZE`. 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Sort node with high memory or disk** → Increase `work_mem` or add an index. 4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Nested Loop with many iterations** → May need a different join strategy. 5\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **"Rows Removed by Filter" is much larger than returned rows** → Add partial or better index. 

Plan Analysis Example 

Sort (cost=1234.56..1289.01 rows=21780 width=42)

Sort Key: (count(o.id)) DESC

Sort Method: external merge Disk: 1234kB

-> HashAggregate (cost=456.78..789.01 rows=21780 width=42)

-> Hash Join (cost=123.45..345.67 rows=22000 width=34)

Hash Cond: (u.id = o.user_id)

-> Seq Scan on users u (cost=0.00..123.45 rows=3000 width=26)

Filter: (created_at > '2026-01-01')

-> Hash (cost=67.89..67.89 rows=4567 width=16)

-> Seq Scan on orders o (cost=0.00..67.89 rows=4567 width=16)

Problems identified: 

  * `Sort Method: external merge Disk`: Sort spilled to disk, `work_mem` too low.

  * `Seq Scan on orders`: No index on `orders.user_id`.

  * The hash join will work well after the orders index is added.




Step 3: Implement the Fix 

Add Missing Index 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- The most common fix

CREATE INDEX CONCURRENTLY idx_orders_user_id ON orders (user_id);

Optimize the Query 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Before (commented for reference)

SELECT u.email, COUNT(o.id) AS order_count

FROM users u LEFT JOIN orders o ON o.user_id = u.id

WHERE u.created_at > '2026-01-01'

GROUP BY u.email

ORDER BY order_count DESC;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- After: use EXISTS if you just need to check existence

SELECT u.email,

(SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) AS order_count

FROM users u

WHERE u.created_at > '2026-01-01'

ORDER BY order_count DESC;

Rewrite Complex Joins 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Before: slow correlated subquery

SELECT p.*,

(SELECT AVG(rating) FROM reviews WHERE product_id = p.id) AS avg_rating,

(SELECT COUNT(*) FROM orders WHERE product_id = p.id) AS order_count

FROM products p

WHERE p.category = 'electronics';

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- After: use LATERAL JOIN

SELECT p.*, r.avg_rating, o.order_count

FROM products p

LEFT JOIN LATERAL (

SELECT AVG(rating) AS avg_rating

FROM reviews WHERE product_id = p.id

) r ON true

LEFT JOIN LATERAL (

SELECT COUNT(*) AS order_count

FROM orders WHERE product_id = p.id

) o ON true

WHERE p.category = 'electronics';

Step 4: Verify the Improvement 

EXPLAIN (ANALYZE, BUFFERS)

SELECT u.email, COUNT(o.id) AS order_count

FROM users u

LEFT JOIN orders o ON o.user_id = u.id

WHERE u.created_at > '2026-01-01'

GROUP BY u.email

ORDER BY order_count DESC

LIMIT 100;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Compare: total cost, actual time, buffers, sort method

Before and After Comparison 

| Metric | Before | After | Improvement | |--------|--------|-------|-------------| | Execution time | 12.4 seconds | 0.3 seconds | 97% | | Buffers | 84,000 shared hit | 2,500 shared hit | 97% | | Sort method | external merge Disk | quicksort memory | In-memory | | Scan type | Seq Scan on orders | Index Scan | Added index | 

Step 5: Prevent Regression 

Capture Baseline 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Create a baseline from pg_stat_statements

SELECT queryid, query, mean_exec_time, calls, rows

FROM pg_stat_statements

ORDER BY queryid;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Store in a monitoring table for trend analysis

CREATE TABLE query_performance_baseline AS

SELECT now() AS captured_at, *

FROM pg_stat_statements;

Set Up Alerts 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Create a function to check for regressions

CREATE OR REPLACE FUNCTION check_query_regression()

RETURNS TABLE(query TEXT, avg_time_ms NUMERIC, calls BIGINT) AS $$

SELECT left(query, 200), mean_exec_time, calls

FROM pg_stat_statements

WHERE mean_exec_time > (

SELECT mean_exec_time * 2

FROM query_performance_baseline qpb

WHERE qpb.queryid = pg_stat_statements.queryid

)

AND calls > 100

ORDER BY mean_exec_time DESC

LIMIT 10;

$$ LANGUAGE sql;

Optimization Workflow Summary 

  * **Identify** : Find the top slow queries (pg_stat_statements).



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Profile** : Run EXPLAIN (ANALYZE, BUFFERS, TIMING). 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Diagnose** : Identify the bottleneck node in the plan. 4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Fix** : Add index, rewrite query, update statistics, or tune parameters. 5\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Verify** : Re-run EXPLAIN ANALYZE to confirm improvement. 6\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Monitor** : Track query performance over time for regression. 

Most slow queries are fixed by adding the right index. When that is not enough, analyze the plan for unexpected join strategies, inefficient scans, or plan instability. A systematic approach prevents guessing and ensures each optimization has a measurable impact.

**See also:** [Database Query Profiling: Finding and Fixing Performance Bottlenecks](</en/database/database-query-profiling.html>), [Slow Query Optimization: Analysis, Indexing, and Rewriting](</en/database/database-slow-query-optimization.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>).

**See also:** [Database Query Profiling: Finding and Fixing Performance Bottlenecks](</en/database/database-query-profiling.html>), [Slow Query Optimization: Analysis, Indexing, and Rewriting](</en/database/database-slow-query-optimization.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>)

**See also:** [Database Query Profiling: Finding and Fixing Performance Bottlenecks](</en/database/database-query-profiling.html>), [Slow Query Optimization: Analysis, Indexing, and Rewriting](</en/database/database-slow-query-optimization.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>)

**See also:** [Database Query Profiling: Finding and Fixing Performance Bottlenecks](</en/database/database-query-profiling.html>), [Slow Query Optimization: Analysis, Indexing, and Rewriting](</en/database/database-slow-query-optimization.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>)

**See also:** [Database Query Profiling: Finding and Fixing Performance Bottlenecks](</en/database/database-query-profiling.html>), [Slow Query Optimization: Analysis, Indexing, and Rewriting](</en/database/database-slow-query-optimization.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>)

**See also:** [Database Query Profiling: Finding and Fixing Performance Bottlenecks](</en/database/database-query-profiling.html>), [Slow Query Optimization: Analysis, Indexing, and Rewriting](</en/database/database-slow-query-optimization.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>)
