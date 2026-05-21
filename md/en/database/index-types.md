---
title: "Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN"
description: "Comprehensive guide to PostgreSQL index types: B-tree, Hash, GiST, GIN, SP-GiST, and BRIN. Learn when and why to use each index type for optimal performance."
date: 2026-04-07
board: database
url: https://dingjiu1989-hue.github.io/en/database/index-types.html
---

# Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN

Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN 

PostgreSQL offers six index types, each designed for different data distributions and query patterns. Choosing the wrong index type wastes storage and degrades performance. This article explains each type, its strengths, and when to use it. 

B-tree (Default) 

B-tree is PostgreSQL's default and most versatile index type. It supports equality, range, sorting, and pattern matching. 

CREATE INDEX idx_users_email ON users USING BTREE (email);

CREATE INDEX idx_orders_date ON orders USING BTREE (order_date);

**Supported operators** : `<`, `<=`, `=`, `>=`, `>`, `BETWEEN`, `IN`, `LIKE` (non-wildcard prefix), `IS NULL`

B-tree indexes are balanced trees with fan-out on the order of hundreds. Height grows logarithmically with table size. A B-tree on a table with 10 million rows has a height of approximately 4. 

**When to use** : Default choice for primary keys, foreign keys, columns used in equality and range queries, and `ORDER BY` clauses. Use B-tree unless you have a specific reason to choose another type. 

**Performance characteristics** :

  * Point lookups: O(log n)

  * Range scans: O(log n + k) where k is the number of matching rows

  * Insert/Update/Delete: O(log n)




Hash 

Hash indexes support only equality comparisons (`=`). They are typically smaller than B-tree for the same data: 

CREATE INDEX idx_sessions_token ON sessions USING HASH (token);

**When to use** : Columns with many distinct values that are only queried with equality conditions. Before PostgreSQL 10, hash indexes were not WAL-logged and could not be replicated. Since PostgreSQL 10, they are fully transaction-safe. 

**Considerations** : Hash indexes do not support ordering or range queries. For most workloads, btree is a better choice even for equality-only queries because B-tree indexes can also support sort operations and are more robust. 

GiST (Generalized Search Tree) 

GiST is a balanced tree structure that supports custom data types and operators. It is an "indexing framework" rather than a specific algorithm: 

CREATE INDEX idx_locations ON places USING GIST (location);

CREATE INDEX idx_daterange ON bookings USING GIST (booking_period);

**Supported operators** :

  * Geometries: `<<`, `&<`, `&>`, `>>`, `<<|`, `&<|`, `|&>`, `|>>`, `@>`, `<@`, `~=`, `&&`

  * Ranges: `&&`, `@>`, `<@`, `-|-`, `<<`, `>>`, `&<`, `&>`

  * Full-text search: `@@`

  * `inet`: `>>`, `<<`, etc.




**When to use** :

  * Geospatial data (PostGIS points, polygons)

  * Range types and exclusive constraints

  * Full-text search with `tsvector` (though GIN is often better)

  * Custom data types with GiST operator classes




**Performance** : Variable insertion/query performance depending on the operator class. Typically O(log n) for search. 

GIN (Generalized Inverted Index) 

GIN indexes map each distinct value (element) to a list of rows containing that value. They excel at indexing composite values like arrays, JSONB, and full-text documents: 

CREATE INDEX idx_articles_fts ON articles USING GIN (search_vector);

CREATE INDEX idx_products_tags ON products USING GIN (tags);

CREATE INDEX idx_products_attrs ON products USING GIN (attributes jsonb_path_ops);

**Supported operators** :

  * Arrays: `&&`, `@>`, `<@`, `=`

  * JSONB: `@>`, `?`, `?|`, `?&`

  * Full-text search: `@@`




**When to use** :

  * Full-text search (tsvector)

  * JSONB containment queries

  * Array columns (tags, categories)

  * Any column where you need to find rows containing specific elements




**Performance** : GIN indexes are larger than B-tree (typically 2-3x the data size) and slower to build. Reads are fast; writes are slower due to pending list management. Use `gin_pending_list_limit` to tune write performance. 

SP-GiST (Space-Partitioned GiST) 

SP-GiST supports partitioned search trees like quad-trees, k-d trees, and radix trees. It divides the search space into non-overlapping partitions: 

CREATE INDEX idx_points ON locations USING SPGIST (point);

CREATE INDEX idx_text_prefix ON texts USING SPGIST (text);

**When to use** :

  * Point data with natural clustering

  * Text with common prefixes (autocomplete)

  * Geographic data with non-uniform distribution

  * KD-tree semantics for multi-dimensional data




SP-GiST is most effective when the data distribution allows efficient space partitioning. It is faster than GiST for certain point queries but less general. 

BRIN (Block Range INdex) 

BRIN indexes aggregate summary information about physical page ranges (typically 32-128 pages per range). They are orders of magnitude smaller than B-tree: 

CREATE INDEX idx_orders_date_brin ON orders USING BRIN (order_date)

WITH (pages_per_range = 32);

CREATE INDEX idx_logs_brin ON access_logs USING BRIN (logged_at, severity)

WITH (pages_per_range = 64);

**When to use** :

  * Very large tables (100GB+) where B-tree index size is prohibitive

  * Columns with natural physical correlation (time-ordered inserts, monotonic sequences)

  * Data warehousing and analytics workloads

  * Append-only tables (logs, events, time-series)




**Storage comparison** : 

| Table Size | B-tree Size | BRIN Size | BRIN Ratio | |------------|-------------|-----------|------------| | 10 GB | 2.2 GB | 4 MB | 0.2% | | 100 GB | 22 GB | 40 MB | 0.04% | | 1 TB | 220 GB | 400 MB | 0.04% | 

Choosing the Right Index 

| Query Pattern | Recommended Index | |---------------|-------------------| | Equality + range | B-tree | | Equality only (high cardinality) | B-tree (or Hash) | | Full-text search | GIN | | JSONB queries | GIN (jsonb_path_ops) | | Geospatial (points) | GiST or SP-GiST | | Geospatial (polygons) | GiST | | Range types | GiST | | Arrays | GIN | | Time-ordered data, huge tables | BRIN | | Text prefix search (autocomplete) | SP-GiST | 

The best index is the one that matches your query patterns exactly. A B-tree index on a column never used in WHERE or ORDER BY is wasted storage. Conversely, a BRIN index on a randomly-ordered column may be useless because it does not exclude any blocks. Measure before and after creating indexes using `EXPLAIN (ANALYZE, BUFFERS)` to confirm the performance benefit.

**See also:** [B-Tree, Hash, GiST, GIN: Index Type Selection Guide](</en/database/database-index-types.html>), [Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes](</en/database/full-text-search-postgresql.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>).

**See also:** [B-Tree, Hash, GiST, GIN: Index Type Selection Guide](</en/database/database-index-types.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes](</en/database/full-text-search-postgresql.html>)

**See also:** [B-Tree, Hash, GiST, GIN: Index Type Selection Guide](</en/database/database-index-types.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes](</en/database/full-text-search-postgresql.html>)

**See also:** [B-Tree, Hash, GiST, GIN: Index Type Selection Guide](</en/database/database-index-types.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes](</en/database/full-text-search-postgresql.html>)

**See also:** [B-Tree, Hash, GiST, GIN: Index Type Selection Guide](</en/database/database-index-types.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes](</en/database/full-text-search-postgresql.html>)

**See also:** [B-Tree, Hash, GiST, GIN: Index Type Selection Guide](</en/database/database-index-types.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes](</en/database/full-text-search-postgresql.html>)

**See also:** [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)
