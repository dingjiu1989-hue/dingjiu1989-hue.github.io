---
title: "Slow Query Optimization: Analysis, Indexing, and Rewriting"
description: "Systematic approach to finding and fixing slow database queries: EXPLAIN plans, index strategies, and SQL rewriting."
date: 2026-04-16
board: database
url: https://aidev.fit/en/database/database-slow-query-optimization.html
---

# Slow Query Optimization: Analysis, Indexing, and Rewriting

Slow queries are the most common cause of database performance problems. A single slow query can consume database resources and degrade performance for all users. Systematic optimization requires measuring, analyzing, and fixing queries methodically.

## Finding Slow Queries

pg_stat_statements in PostgreSQL and performance_schema in MySQL track query execution statistics. Query these views for total execution time, calls, and mean time per query. Sort by total time to find the queries consuming the most database resources.

Set a slow query log threshold. Log queries exceeding 100ms in development, 200ms in production. Review logs regularly. Tools like pgBadger and pt-query-digest analyze log files and produce execution summaries.

## Reading EXPLAIN Plans

EXPLAIN ANALYZE executes the query and shows actual execution times. Key indicators: sequential scans on large tables suggest missing indexes. Nested loop joins on large datasets may need different join strategies. Sort operations on unindexed columns indicate missing sort keys.

Poor plan indicators: actual rows diverging significantly from estimated rows suggests stale statistics. High buffer usage (shared hit vs shared read) indicates inefficient cache usage. Execution time dominated by a single node suggests a bottleneck.

## Index Optimization

Examine query WHERE clauses, JOIN conditions, and ORDER BY columns. Create indexes that match the query access pattern. A B-tree index works best for equality and range conditions. Composite indexes should match query filter order—put equality conditions first, range conditions last.

Covering indexes include all columns needed by a query, eliminating table access entirely. PostgreSQL supports INCLUDE columns. Use them for SELECT columns that are not filter conditions.

Remove unused indexes. Indexes slow writes and consume storage. Use pg_stat_user_indexes to find indexes never used for index scans. Drop them carefully—one at a time—monitoring for query regression.

## SQL Rewriting

Sometimes the query itself needs restructuring. Common optimizations: replace multiple OR conditions with IN or UNION. Replace correlated subqueries with JOINs or window functions. Use EXISTS instead of IN for large subquery result sets.

Avoid functions on indexed columns in WHERE clauses—WHERE DATE(created_at) = '2026-01-01' cannot use an index on created_at. Rewrite as WHERE created_at >= '2026-01-01' AND created_at < '2026-01-02'.

## Maintenance

Regular VACUUM and ANALYZE keep statistics current. Outdated statistics produce bad query plans. Schedule ANALYZE after significant data changes. Consider autovacuum tuning for busy tables.

**See also:** [Database Query Profiling: Finding and Fixing Performance Bottlenecks](</en/database/database-query-profiling.html>), [Slow Query Troubleshooting: Identification, Profiling, and Optimization](</en/database/database-slow-query-fix.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>).

**See also:** [Database Query Profiling: Finding and Fixing Performance Bottlenecks](</en/database/database-query-profiling.html>), [Slow Query Troubleshooting: Identification, Profiling, and Optimization](</en/database/database-slow-query-fix.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>)

**See also:** [Database Query Profiling: Finding and Fixing Performance Bottlenecks](</en/database/database-query-profiling.html>), [Slow Query Troubleshooting: Identification, Profiling, and Optimization](</en/database/database-slow-query-fix.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>)

**See also:** [Database Query Profiling: Finding and Fixing Performance Bottlenecks](</en/database/database-query-profiling.html>), [Slow Query Troubleshooting: Identification, Profiling, and Optimization](</en/database/database-slow-query-fix.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>)

**See also:** [Database Query Profiling: Finding and Fixing Performance Bottlenecks](</en/database/database-query-profiling.html>), [Slow Query Troubleshooting: Identification, Profiling, and Optimization](</en/database/database-slow-query-fix.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>)

**See also:** [Database Query Profiling: Finding and Fixing Performance Bottlenecks](</en/database/database-query-profiling.html>), [Slow Query Troubleshooting: Identification, Profiling, and Optimization](</en/database/database-slow-query-fix.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>)

**See also:** [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>), [Materialized Views](</en/database/materialized-views.html>), [ORM Performance](</en/database/orm-performance.html>)

**See also:** [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>), [Materialized Views](</en/database/materialized-views.html>), [ORM Performance](</en/database/orm-performance.html>)

**See also:** [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>), [Materialized Views](</en/database/materialized-views.html>), [ORM Performance](</en/database/orm-performance.html>)

**See also:** [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>), [Materialized Views](</en/database/materialized-views.html>), [ORM Performance](</en/database/orm-performance.html>)

**See also:** [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>), [Materialized Views](</en/database/materialized-views.html>), [ORM Performance](</en/database/orm-performance.html>)

**See also:** [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>), [Materialized Views](</en/database/materialized-views.html>), [ORM Performance](</en/database/orm-performance.html>)

**See also:** [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>), [Materialized Views](</en/database/materialized-views.html>), [ORM Performance](</en/database/orm-performance.html>)

**See also:** [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>), [Materialized Views](</en/database/materialized-views.html>), [ORM Performance](</en/database/orm-performance.html>)

**See also:** [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>), [Materialized Views](</en/database/materialized-views.html>), [ORM Performance](</en/database/orm-performance.html>)

**See also:** [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>), [Materialized Views](</en/database/materialized-views.html>), [ORM Performance](</en/database/orm-performance.html>)

**See also:** [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>), [Materialized Views](</en/database/materialized-views.html>), [ORM Performance](</en/database/orm-performance.html>)

**See also:** [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>), [Materialized Views](</en/database/materialized-views.html>), [ORM Performance](</en/database/orm-performance.html>)

**See also:** [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>), [Materialized Views](</en/database/materialized-views.html>), [ORM Performance](</en/database/orm-performance.html>)

**See also:** [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>), [Materialized Views](</en/database/materialized-views.html>), [ORM Performance](</en/database/orm-performance.html>)

**See also:** [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>), [Materialized Views](</en/database/materialized-views.html>), [ORM Performance](</en/database/orm-performance.html>)

**See also:** [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>), [Materialized Views](</en/database/materialized-views.html>), [ORM Performance](</en/database/orm-performance.html>)

**See also:** [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>), [Materialized Views](</en/database/materialized-views.html>), [ORM Performance](</en/database/orm-performance.html>)

**See also:** [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>), [Materialized Views](</en/database/materialized-views.html>), [ORM Performance](</en/database/orm-performance.html>)
