---
title: "PostgreSQL Query Optimization: From 2 Seconds to 2 Milliseconds"
description: "Practical PostgreSQL performance guide: EXPLAIN ANALYZE deep dive, index types (B-tree, GIN, GiST, BRIN), query plan analysis, common anti-patterns, partitioning strategies, and connection pooling with PgBouncer."
date: 2026-05-08
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/postgresql-query-optimization.html
---

# PostgreSQL Query Optimization: From 2 Seconds to 2 Milliseconds

A slow PostgreSQL query is the most common performance bottleneck in web applications — and the most fixable. This guide covers the systematic approach to identifying slow queries, reading EXPLAIN ANALYZE output, and applying the optimizations that have the highest ROI: indexing, query rewriting, and configuration tuning. From 2 seconds to 2 milliseconds.

## The Optimization Workflow

  1. **Identify:** Enable pg_stat_statements, find the top 10 slowest/most frequent queries
  2. **Analyze:** Run EXPLAIN (ANALYZE, BUFFERS) on the slow query
  3. **Diagnose:** Is it a missing index? A bad query plan? Lock contention? Hardware?
  4. **Fix:** Apply the specific optimization, measure the improvement
  5. **Prevent:** Add an index, adjust work_mem, or rewrite the query permanently

## Reading EXPLAIN ANALYZE Output

Node Type| What It Means| Good or Bad?| Action  
---|---|---|---  
Seq Scan| Scanning every row in the table| Bad for large tables (>10K rows)| Add an index  
Index Scan| Using index, reads index + heap| Good for selective queries, bad for large result sets| Usually fine; Index Only Scan is better  
Index Only Scan| Index covers all needed columns| Excellent — no heap access needed| Keep; consider covering indexes  
Bitmap Index Scan → Bitmap Heap Scan| Combines multiple indexes, then reads heap| OK for AND/OR conditions on indexed columns| Fine unless rows are very large  
Nested Loop| For each row in A, look up B| Good if A is small, B is indexed| Bad for large tables without index  
Hash Join| Build hash of one table, probe with other| Good for joining two large tables| Usually fine; ensure work_mem is sufficient  
Merge Join| Both inputs sorted, merge like zipper| Good for pre-sorted inputs (from indexes)| Excellent if both are index scans  

## Index Types and When to Use Them

Index Type| Best For| Example| Size Overhead  
---|---|---|---  
B-Tree (default)| Equality, range, ORDER BY, <, >, BETWEEN| WHERE user_id = 123 / WHERE created_at > now() - interval '7 days'| ~40% of table size  
Partial Index| Queries on a subset of rows| WHERE status = 'active' AND created_at > '2024-01-01' (index WHERE status = 'active')| Small  
Covering Index (INCLUDE)| Index-Only Scans for specific columns| INDEX ON users (email) INCLUDE (name, avatar_url)| Medium  
GIN (Generalized Inverted)| Full-text search, arrays, JSONB| WHERE document @@ to_tsquery('search & query')| Large  
GiST| Geometric data, full-text search| WHERE location <@ ST_MakeEnvelope(...)| Medium-Large  
BRIN (Block Range)| Very large tables, naturally sorted data| WHERE created_at BETWEEN ... (on 1B+ row tables)| Very Small (<0.1%)  

## Common Optimizations by Root Cause

Symptom| Root Cause| Fix| Speedup  
---|---|---|---  
Seq Scan on large table| Missing index| CREATE INDEX ON table (filter_column)| 100-10,000x  
Nested Loop with large inner table| Missing JOIN index| CREATE INDEX ON inner_table (join_key)| 50-500x  
Sort using external merge (disk)| work_mem too low| SET work_mem = '256MB' for this query| 5-20x  
N+1 queries (ORM)| Lazy loading in application| Use eager loading (includes/joins)| 10-100x  
Slow COUNT(*)| MVCC visibility checks| Use estimate: SELECT reltuples FROM pg_class WHERE relname = 'table'| 100-1000x  
Table bloat| Dead tuples from UPDATE/DELETE| VACUUM ANALYZE; adjust autovacuum settings| 2-10x  

## Key PostgreSQL Configuration Tuning

    -- Check current settings
    SHOW shared_buffers;        -- Default: 128MB. Set to 25% of RAM.
    SHOW work_mem;              -- Default: 4MB. Increase to 64-256MB for reporting queries.
    SHOW maintenance_work_mem;  -- Default: 64MB. Set to 10% of RAM for VACUUM/INDEX speed.
    SHOW effective_cache_size;  -- Default: 4GB. Set to 75% of RAM (hint for planner).
    SHOW random_page_cost;      -- Default: 4.0. Set to 1.1 for SSD (encourages index use).

    -- Enable slow query logging
    ALTER SYSTEM SET log_min_duration_statement = 1000;  -- Log queries > 1s
    SELECT pg_reload_conf();

**Bottom line:** 90% of PostgreSQL performance problems are solved by adding the right index and adjusting work_mem. Before adding indexes, run EXPLAIN (ANALYZE, BUFFERS) on the slow query. If you see Seq Scan on a large table, add an index. If you see external merge on disk, increase work_mem. These two fixes alone resolve the vast majority of performance issues. See also: [Full-Text Search Comparison](</en/tech/full-text-search-comparison.html>) and [Database Migrations Guide](</en/tech/database-migration-strategies.html>).
