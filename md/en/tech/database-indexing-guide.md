---
title: "Database Indexing Strategies: B-Tree, Hash, GIN, GiST, and BRIN Explained"
description: "Go beyond CREATE INDEX with a deep dive into index types, when each excels, covering indexes, partial indexes, and how the query planner chooses."
date: 2025-10-18
board: tech
url: https://aidev.fit/en/tech/database-indexing-guide.html
---

# Database Indexing Strategies: B-Tree, Hash, GIN, GiST, and BRIN Explained

Adding an index is the highest-ROI database optimization — a well-chosen index can turn a 30-second sequential scan into a sub-millisecond index lookup. But indexing is full of trade-offs: each index slows writes, consumes storage, and requires the query planner to choose it. This guide covers index types, when to use each, and how to verify they are actually working.

## Index Types: Complete Reference

Index Type| How It Works| Best For| Limitations| Database Support  
---|---|---|---|---  
B-Tree| Balanced tree, sorted order| =, <, >, BETWEEN, LIKE 'prefix%', ORDER BY, GROUP BY| Slow on LIKE '%suffix' (no leading wildcard)| All databases (default index type)  
Hash| Hash table, O(1) lookup| = (equality only)| No range queries, no ORDER BY, no partial key matches| PostgreSQL, MySQL (Memory engine)  
GIN (Generalized Inverted)| Inverted index: key → list of row IDs| Arrays, JSONB, full-text search (tsvector)| Slower writes; larger than B-Tree; GIN scans return all matches| PostgreSQL  
GiST (Generalized Search Tree)| Balanced tree, extensible| Geometric/spatial data (PostGIS), full-text search| More complex than GIN; slower reads, faster writes than GIN| PostgreSQL  
BRIN (Block Range INdex)| Summary per block range (min/max)| Very large tables (>100M rows), naturally sorted data (timestamps)| Loose — returns false positives that must be filtered| PostgreSQL  
SP-GiST (Space-Partitioned GiST)| Partitioned search tree| Non-overlapping data, phone numbers, IP addresses| Specialized; narrow use case| PostgreSQL  
Full-Text Index| Tokenized inverted index| MATCH ... AGAINST, CONTAINS, @@ tsquery| Language-specific tokenization; keyword search ≠ semantic search| PostgreSQL (GIN), MySQL (FULLTEXT), MSSQL (Full-Text)  
Bitmap (Columnar)| Bitmap per distinct value| Low-cardinality columns (status, category, boolean)| High-cardinality columns create massive bitmaps| PostgreSQL (via extensions), Oracle, Data Warehouses  
  
## Advanced Index Patterns

Pattern| What It Is| When to Use| Example  
---|---|---|---  
Composite (Multi-Column)| Index on (col1, col2, col3)| Queries filter on col1, then col2, then col3| INDEX ON orders (user_id, status, created_at)  
Covering Index (INCLUDE)| Index contains all columns the query needs| Enable Index-Only Scans; avoid heap lookups| INDEX ON users (email) INCLUDE (name, avatar)  
Partial Index| Index only rows matching WHERE| Index a subset of data, save space| INDEX ON orders (created_at) WHERE status = 'active'  
Expression / Functional Index| Index on expression result| Queries filter on computed values| INDEX ON users (LOWER(email)), INDEX ON orders (date_trunc('day', created_at))  
Descending Index| Index sorted DESC (not default ASC)| ORDER BY col DESC is the primary access pattern| INDEX ON events (created_at DESC)  
  
## How to Verify Your Index Is Working
    
    
    -- PostgreSQL: Check index usage
    SELECT
        schemaname || '.' || relname AS table,
        indexrelname AS index,
        idx_scan AS index_scans,
        idx_tup_read AS rows_returned,
        idx_tup_fetch AS rows_fetched,
        pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
    FROM pg_stat_user_indexes
    WHERE idx_scan = 0  -- Unused indexes! Safe to drop
    ORDER BY pg_relation_size(indexrelid) DESC;
    
    -- Find missing indexes (seq scans on tables > 1MB)
    SELECT
        schemaname || '.' || relname AS table,
        seq_scan, seq_tup_read,
        pg_size_pretty(pg_relation_size(relid)) AS table_size
    FROM pg_stat_user_tables
    WHERE seq_scan > 0
      AND pg_relation_size(relid) > 1024 * 1024  -- > 1MB
    ORDER BY seq_tup_read DESC;

## The 5-Minute Indexing Checklist

  1. **Find the slow query:** pg_stat_statements or slow query log → extract the WHERE/JOIN/ORDER BY
  2. **Check existing indexes:** \d tablename — is there already an index that covers this? Is it being used?
  3. **Match index type to query:** = → B-Tree or Hash; range/LIKE prefix → B-Tree; JSONB/array → GIN; full-text → GIN + tsvector
  4. **Create with purpose:** Partial index for subsets, covering index (INCLUDE) for Index-Only Scans, composite for multi-column filters
  5. **Verify with EXPLAIN:** Did the plan change from Seq Scan → Index Scan / Index Only Scan? Run ANALYZE first.

**Bottom line:** B-Tree indexes solve 90% of indexing needs — they handle =, range, sorting, and prefix matching. GIN is essential for JSONB and full-text search workloads. The most common indexing mistakes: (1) indexing columns that are never queried, (2) missing composite indexes for multi-column WHERE clauses, and (3) not using covering indexes (INCLUDE) to enable Index-Only Scans. Run the unused index query above quarterly — dropping unused indexes speeds up every INSERT/UPDATE. See also: [PostgreSQL Query Optimization](</en/tech/postgresql-query-optimization.html>) and [Database Design Fundamentals](</en/tech/database-design-fundamentals.html>).
