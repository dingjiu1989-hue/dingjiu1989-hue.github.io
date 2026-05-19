---
title: "Database Indexing Strategies"
description: "A comprehensive guide to database indexing covering B-tree, hash, GiST, GIN indexes, composite indexes, and query optimization."
date: 2025-12-22
board: database
url: https://dingjiu1989-hue.github.io/en/database/database-indexing.html
---

# Database Indexing Strategies

What Is Database Indexing? 

A database index is a data structure that improves the speed of data retrieval operations on a table at the cost of additional writes and storage space. Think of it like a book's index: instead of flipping through every page to find a topic, you look up the topic in the index and go directly to the right page. 

How Indexes Work 

Without an index, the database performs a sequential scan, reading every row until it finds matches. With an index, the database navigates a balanced tree structure to locate data in O(log n) time instead of O(n). 

Sequential Scan: [Row1] [Row2] [Row3] ... [Row1M] = 1,000,000 reads

B-Tree Index: [Root] -> [Branch] -> [Leaf] -> [Row] = 3-4 reads

Index Types 

B-Tree Index 

The default and most common index type. Works well for equality and range queries. 

CREATE INDEX idx_users_email ON users(email);

CREATE INDEX idx_users_created ON users(created_at);

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Used for:

SELECT * FROM users WHERE email = 'alice@example.com';

SELECT * FROM users WHERE created_at > '2026-01-01';

SELECT * FROM users WHERE email LIKE 'alice%';

Hash Index 

Optimized for equality comparisons. Not suitable for range queries or sorting. 

CREATE INDEX idx_sessions_token ON sessions USING HASH(session_token);

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Good for:

SELECT * FROM sessions WHERE session_token = 'abc123';

GiST Index 

Generalized Search Tree, useful for full-text search and geometric data. 

CREATE INDEX idx_posts_content ON posts USING GIST(to_tsvector('english', content));

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Used for:

SELECT * FROM posts

WHERE to_tsvector('english', content) @@ to_tsquery('database & indexing');

GIN Index 

Generalized Inverted Index, optimized for composite types and arrays. 

CREATE INDEX idx_article_tags ON articles USING GIN(tags);

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Used for:

SELECT * FROM articles WHERE tags @> ARRAY['postgresql'];

SELECT * FROM articles WHERE tags && ARRAY['database', 'sql'];

BRIN Index 

Block Range INdex, efficient for very large tables with naturally ordered data. 

CREATE INDEX idx_logs_created ON logs USING BRIN(created_at)

WITH (pages_per_range = 32);

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Best for:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Time-series data where rows are inserted in order

Composite Indexes 

Indexes on multiple columns. Column order matters significantly. 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Composite index

CREATE INDEX idx_users_status_created

ON users(status, created_at);

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- This index can serve:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- 1. WHERE status = 'active'

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- 2. WHERE status = 'active' AND created_at > '2026-01-01'

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- 3. WHERE status IN ('active', 'pending') ORDER BY created_at

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- But NOT:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- WHERE created_at > '2026-01-01' (status is leading column)

Column Order Rules 

| Rule | Example | |------|---------| | Equality conditions first | `WHERE status = 'active' AND created_at > '2026-01-01'` -> index on `(status, created_at)` | | High cardinality columns first for range | `WHERE type = 'user' AND email LIKE 'a%'` -> index on `(type, email)` | | Most selective column first | `WHERE country = 'US' AND status = 'active'` — US is 10% of data, active is 90% -> index on `(country, status)` | 

Index Scan Types 

| Scan Type | When Used | Performance | |-----------|-----------|-------------| | Sequential Scan | No index, or query returns large percentage of table | Full table read | | Index Scan | Index lookup + heap access | Fast for selective queries | | Index Only Scan | All needed columns are in the index | Fastest, no heap access | | Bitmap Scan | Combines multiple indexes, returns moderate row count | Good for multi-condition queries | 

Monitoring Index Usage 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- PostgreSQL: Find unused indexes

SELECT

schemaname || '.' || relname AS table,

indexrelname AS index,

idx_scan AS index_scans

FROM pg_stat_user_indexes

WHERE idx_scan < 100

AND indexrelname NOT LIKE '%_pkey'

ORDER BY idx_scan ASC;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Find missing indexes

SELECT

relname AS table,

seq_scan - idx_scan AS too_much_seq,

seq_scan,

idx_scan

FROM pg_stat_user_tables

WHERE seq_scan > idx_scan

AND seq_scan > 1000

ORDER BY seq_scan DESC;

Index Maintenance 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Rebuild indexes to reclaim space (PostgreSQL)

REINDEX INDEX idx_users_email;

REINDEX TABLE users;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Update statistics for query planner

ANALYZE users;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Check index size

SELECT

pg_size_pretty(pg_indexes_size('users')) AS total_index_size,

pg_size_pretty(pg_total_relation_size('users')) AS total_size;

Common Anti-Patterns 

| Anti-Pattern | Why It Hurts | |--------------|--------------| | Indexing every column | Writes become slow, storage bloats | | Forgetting composite indexes | Query uses multiple single-column indexes inefficiently | | Indexing boolean columns | Very low cardinality, rarely useful | | Not indexing foreign keys | JOIN queries perform sequential scans | | Over-indexing small tables | Tables under 1000 rows are faster to scan sequentially | 

Summary 

Indexes are the most impactful performance optimization for database queries. Use B-tree indexes as the default for most workloads, composite indexes with carefully ordered columns for multi-condition queries, and specialized types (GIN, GiST, BRIN) for specific use cases. Monitor index usage and remove unused indexes to keep write performance optimal. Always run queries through EXPLAIN ANALYZE to verify the planner is using your indexes effectively.

**See also:** [SQL Query Optimization](</en/database/sql-query-optimization.html>), [OLTP vs OLAP: Workload Optimization](</en/database/oltp-vs-olap.html>), [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>).

**See also:** [PostgreSQL Query Optimization: From 2 Seconds to 2 Milliseconds](</en/tech/postgresql-query-optimization.html>), [Database Indexing Strategies: B-Tree, Hash, GIN, GiST, and BRIN Explained](</en/tech/database-indexing-guide.html>), [OLTP vs OLAP: Workload Optimization](</en/database/oltp-vs-olap.html>)

**See also:** [PostgreSQL Query Optimization: From 2 Seconds to 2 Milliseconds](</en/tech/postgresql-query-optimization.html>), [Database Indexing Strategies: B-Tree, Hash, GIN, GiST, and BRIN Explained](</en/tech/database-indexing-guide.html>), [OLTP vs OLAP: Workload Optimization](</en/database/oltp-vs-olap.html>)

**See also:** [PostgreSQL Query Optimization: From 2 Seconds to 2 Milliseconds](</en/tech/postgresql-query-optimization.html>), [Database Indexing Strategies: B-Tree, Hash, GIN, GiST, and BRIN Explained](</en/tech/database-indexing-guide.html>), [OLTP vs OLAP: Workload Optimization](</en/database/oltp-vs-olap.html>)

**See also:** [PostgreSQL Query Optimization: From 2 Seconds to 2 Milliseconds](</en/tech/postgresql-query-optimization.html>), [Database Indexing Strategies: B-Tree, Hash, GIN, GiST, and BRIN Explained](</en/tech/database-indexing-guide.html>), [OLTP vs OLAP: Workload Optimization](</en/database/oltp-vs-olap.html>)

**See also:** [PostgreSQL Query Optimization: From 2 Seconds to 2 Milliseconds](</en/tech/postgresql-query-optimization.html>), [Database Indexing Strategies: B-Tree, Hash, GIN, GiST, and BRIN Explained](</en/tech/database-indexing-guide.html>), [OLTP vs OLAP: Workload Optimization](</en/database/oltp-vs-olap.html>)

**See also:** [B-Tree, Hash, GiST, GIN: Index Type Selection Guide](</en/database/database-index-types.html>), [Database Security Hardening Guide](</en/database/database-security-best-practices.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>)

**See also:** [B-Tree, Hash, GiST, GIN: Index Type Selection Guide](</en/database/database-index-types.html>), [Database Security Hardening Guide](</en/database/database-security-best-practices.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>)

**See also:** [B-Tree, Hash, GiST, GIN: Index Type Selection Guide](</en/database/database-index-types.html>), [Database Security Hardening Guide](</en/database/database-security-best-practices.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>)
