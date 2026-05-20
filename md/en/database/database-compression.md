---
title: "Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST"
description: "Explore database compression techniques including page-level, tuple-level, and columnar compression. Learn about PostgreSQL TOAST and real-world storage savings."
date: 2026-03-31
board: database
url: https://dingjiu1989-hue.github.io/en/database/database-compression.html
---

# Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST

Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST 

Database compression reduces storage footprint and, more importantly, improves query performance by reducing the amount of data read from disk. This article covers compression techniques across PostgreSQL, MySQL, and columnar databases. 

Why Compression Matters 

Compression provides three benefits: 

  * **Storage savings** : Reduce disk costs by 2x-10x depending on data characteristics.

  * **I/O reduction** : Fewer pages read per query means faster scans.

  * **Cache efficiency** : More data fits in shared_buffers or the OS page cache.




The trade-off is CPU usage for compression and decompression. Modern hardware makes this trade-off favorable for most workloads. 

PostgreSQL Compression Layers 

Page-Level Compression 

PostgreSQL stores data in 8 KB pages. Page-level compression compresses the entire page as a unit. The `page_compression` feature (available since PostgreSQL 15 with `zstd`) reduces page size on disk: 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Enable page compression on a table

CREATE TABLE logs_compressed (

id BIGSERIAL,

payload TEXT,

created_at TIMESTAMPTZ

) WITH (compression = 'zstd');

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Or alter existing table

ALTER TABLE logs SET (compression = 'pglz');

Page compression works transparently: the database decompresses pages when reading and compresses when writing. The overhead is minimal for sequential scans. 

TOAST (The Oversized-Attribute Storage Technique) 

TOAST is PostgreSQL's built-in mechanism for handling large field values. When a row exceeds the 8 KB page size, PostgreSQL moves oversized values to a secondary TOAST table: 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Check TOAST compression settings

SELECT attname,

CASE attstorage

WHEN 'p' THEN 'plain'

WHEN 'm' THEN 'main'

WHEN 'x' THEN 'extended'

WHEN 'e' THEN 'external'

END AS storage_type

FROM pg_attribute

WHERE attrelid = 'documents'::regclass

AND attnum > 0;

Storage types: 

  * `PLAIN`: No compression, no TOAST. For fixed-width types like `INTEGER`.

  * `EXTENDED` (default for `TEXT`, `BYTEA`): Try compression first; if still too large, move to TOAST.

  * `EXTERNAL`: Move to TOAST without compression. Useful for data that is already compressed (e.g., JPEG, JSON).

  * `MAIN`: Try compression but keep in main table if possible.




\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Change storage type for a column

ALTER TABLE documents ALTER COLUMN image SET STORAGE EXTERNAL;

TOAST compression uses a fast, lightweight algorithm (pglz or zstd). It is invisible to queries: SELECT statements decompress transparently. 

Tuple-Level Compression 

Tuple-level compression compresses individual row values. PostgreSQL's built-in `COMPRESSION` clause (PostgreSQL 14+) allows per-column compression: 

CREATE TABLE events (

id BIGSERIAL,

event_type TEXT COMPRESSION lz4,

payload JSONB COMPRESSION zstd,

created_at TIMESTAMPTZ

);

Supported algorithms: `pglz`, `lz4`, `zstd` (with `--with-zstd` build flag). LZ4 is fastest with moderate compression; Zstd offers the best ratio. 

External Compression with pgstattuple 

Measure your current compression benefits: 

CREATE EXTENSION pgstattuple;

SELECT * FROM pgstattuple('large_table');

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- free_space, tuple_count, tuple_len, dead_tuple_count, dead_tuple_len

Columnar Compression 

Columnar databases like ClickHouse, Redshift, and Parquet-format files compress extremely well because same-typed values repeat within a column: 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- ClickHouse example: columnar compression is automatic

CREATE TABLE events (

event_type LowCardinality(String),

user_id UInt32,

timestamp DateTime,

payload String

) ENGINE = MergeTree()

ORDER BY timestamp;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Each column is compressed independently

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- event_type: run-length encoding after dictionary compression

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- user_id: delta encoding + zstd

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- payload: zstd

Columnar compression ratios are often 5x-10x higher than row-oriented compression because similar values cluster together. 

Compression Algorithm Comparison 

| Algorithm | Speed | Ratio | CPU Use | PostgreSQL Support | |-----------|-------|-------|---------|-------------------| | pglz | Fast | Low | Low | Built-in (default) | | LZ4 | Very fast | Low-Medium | Very low | PG 14+ | | Zstd | Moderate | High | Moderate | PG 15+ | | zlib | Slow | High | High | Extension | 

Benchmarks show LZ4 compresses at 2-3 GB/s per core, while Zstd achieves 15-30% better ratios at 500 MB/s. 

Real-World Storage Savings 

| Data Type | Raw Size | pglz | zstd | Notes | |-----------|----------|------|------|-------| | Log text | 100 GB | 35 GB | 22 GB | Highly compressible | | JSON payloads | 50 GB | 42 GB | 30 GB | Semi-structured | | UUIDs | 10 GB | 10 GB | 10 GB | Incompressible | | Numeric arrays | 20 GB | 8 GB | 5 GB | Delta encoding helps | 

Monitoring Compression 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Table size breakdown

SELECT schemaname, tablename,

pg_size_pretty(pg_table_size(relid)) AS table_size,

pg_size_pretty(pg_indexes_size(relid)) AS index_size,

pg_size_pretty(pg_total_relation_size(relid)) AS total_size

FROM pg_catalog.pg_statio_user_tables

ORDER BY pg_total_relation_size(relid) DESC;

For TOAST-specific sizes: 

SELECT relname,

pg_size_pretty(relpages::bigint * 8192) AS toast_size

FROM pg_class

WHERE oid = (

SELECT reltoastrelid FROM pg_class WHERE relname = 'large_table'

);

Best Practices 

  * **Use Zstd for new tables** with large TEXT/JSONB columns. It offers the best compression ratio in PostgreSQL.



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Use EXTERNAL storage** for columns that are already compressed (images, compressed archives). 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Benchmark your workload** : Compression benefits vary. Run `pgstattuple` before and after. 4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Consider BRIN indexes** on compressed, naturally ordered columns (timestamps, sequence IDs) for additional space savings. 5\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Balance CPU and I/O** : If your database is CPU-bound, avoid heavy compression. If I/O-bound, compress aggressively. 

Compression is a rare optimization that reduces cost and improves performance simultaneously. Measure your data's compressibility and choose the right algorithm for each column type.

**See also:** [Database Views: Simple, Materialized, and Updateable Views](</en/database/database-views.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Columnar Storage: Compression, Encoding, and Analytical Performance](</en/database/database-columnar-storage.html>).

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Database Views: Simple, Materialized, and Updateable Views](</en/database/database-views.html>), [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Database Views: Simple, Materialized, and Updateable Views](</en/database/database-views.html>), [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Database Views: Simple, Materialized, and Updateable Views](</en/database/database-views.html>), [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Database Views: Simple, Materialized, and Updateable Views](</en/database/database-views.html>), [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Database Views: Simple, Materialized, and Updateable Views](</en/database/database-views.html>), [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>)

**See also:** [Columnar Storage: Compression, Encoding, and Analytical Performance](</en/database/database-columnar-storage.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>)

**See also:** [Columnar Storage: Compression, Encoding, and Analytical Performance](</en/database/database-columnar-storage.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>)

**See also:** [Columnar Storage: Compression, Encoding, and Analytical Performance](</en/database/database-columnar-storage.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>)

**See also:** [Columnar Storage: Compression, Encoding, and Analytical Performance](</en/database/database-columnar-storage.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>)

**See also:** [Columnar Storage: Compression, Encoding, and Analytical Performance](</en/database/database-columnar-storage.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>)

**See also:** [Columnar Storage: Compression, Encoding, and Analytical Performance](</en/database/database-columnar-storage.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>)

**See also:** [Columnar Storage: Compression, Encoding, and Analytical Performance](</en/database/database-columnar-storage.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>)

**See also:** [Columnar Storage: Compression, Encoding, and Analytical Performance](</en/database/database-columnar-storage.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>)
