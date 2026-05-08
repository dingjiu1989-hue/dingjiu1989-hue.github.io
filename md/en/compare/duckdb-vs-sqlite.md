---
title: "DuckDB vs SQLite: Embedded Databases for Analytics and Applications Compared"
description: "Compare embedded databases — DuckDB for analytical queries (OLAP), SQLite for transactional workloads (OLTP), when to use each, and how they complement."
date: 2026-05-08
board: compare
url: https://dingjiu1989-hue.github.io/en/compare/duckdb-vs-sqlite.html
---

# DuckDB vs SQLite: Embedded Databases for Analytics and Applications Compared

SQLite and DuckDB are both embedded databases — they run in-process, require zero configuration, and store data in a single file. But they are optimized for radically different workloads. SQLite is an OLTP database (transactional, row-oriented). DuckDB is an OLAP database (analytical, column-oriented). Understanding when to use which can mean the difference between a query taking 2 seconds versus 2 minutes. This comparison breaks down the trade-offs.

## Quick Comparison

Feature| SQLite| DuckDB  
---|---|---  
Type| OLTP (Online Transaction Processing)| OLAP (Online Analytical Processing)  
Storage Layout| Row-oriented (good for writes, point lookups)| Column-oriented (good for scans, aggregations)  
Concurrency| Single-writer, multiple-readers (WAL mode)| Single-writer (optimistic), multi-reader  
Query Language| Standard SQL (limited extensions)| Extended SQL (window functions, LIST, structs, lambdas)  
Data Types| 5 storage classes (NULL, INTEGER, REAL, TEXT, BLOB)| Rich types: STRUCT, LIST, MAP, UNION, ENUM, UUID, JSON native  
File Formats (read directly)| Only .sqlite/.db files| CSV, Parquet, JSON, Arrow, Excel, SQLite files  
Extensions / Ecosystem| Massive (every language, every OS, 30+ years)| Growing fast (Python, R, Node.js, Java, Rust, Go, Wasm)  
Query Performance (OLTP)| Excellent (microsecond point lookups with index)| Decent but not its strength (columnar overhead on lookups)  
Query Performance (OLAP)| Poor to decent (row scans are slow on wide tables)| Excellent (columnar + vectorized, 10-100x faster on aggregates)  
Memory / Disk| Minimal memory, works on tiny devices| Happier with more memory (in-memory mode for speed)  
Embedded / IoT| Yes — runs on phones, browsers (Wasm), embedded| Yes — but heavier; not for constrained devices  
Pricing| Free (public domain)| Free (MIT, DuckDB Labs for support)  
  
## When Each Database Wins

**SQLite — Best for:** Application databases — the database behind your mobile app, desktop app, or web app backend. SQLite is the most deployed database in the world: every iPhone, Android phone, browser (Wasm), and operating system uses it. It is perfect for configuration storage, caching, application state, and any workload where you do point lookups and small-range queries on indexed data. **Weak spot:** Analytical queries — SELECT AVG(), GROUP BY on large tables with many columns — are slow because SQLite must read entire rows even when you only need 2 columns.

**DuckDB — Best for:** Analytical workloads — data science, BI queries, log analysis, CSV/Parquet processing. DuckDB is the database you reach for when you have a 10GB CSV file and want to run a GROUP BY query on it in under a second. It reads Parquet files directly, can query across multiple files, and integrates deeply with Python (Pandas, Polars, Arrow). **Weak spot:** Transactional workloads — it is not built for thousands of small inserts/updates per second; concurrency is limited; overkill for simple config storage.

## Killer Features

Feature| SQLite| DuckDB  
---|---|---  
Point Lookups (SELECT WHERE id=123)| ★★★★★ (microseconds, B-tree index)| ★★★ (columnar overhead, not its strength)  
Aggregations (SELECT AVG() GROUP BY)| ★★ (row scans, slow on many columns)| ★★★★★ (vectorized, column pruning, 10-100x faster)  
Window Functions| ★★★ (supported but limited)| ★★★★★ (rich support, fast execution)  
CSV / Parquet Import| ★ (manual; .import or external tools)| ★★★★★ (read_csv(), read_parquet() — one function)  
Concurrent Writes| ★★★ (single writer, WAL helps)| ★★ (optimistic, not designed for many writers)  
Python Integration| ★★★★ (sqlite3 standard library)| ★★★★★ (deep Pandas/Polars/Arrow integration)  
Embeddability / Size| ★★★★★ (~600KB library)| ★★★ (~30MB library, richer dependencies)  
  
## Decision Matrix

Scenario| Best Choice| Why  
---|---|---  
Mobile app local storage (iOS, Android)| SQLite| Built into every platform, tiny, transactional  
Analyze 5GB CSV dataset in Python| DuckDB| read_csv() + GROUP BY in under a second  
Web app backend database (low-medium traffic)| SQLite| Litestream for replication, enough for most apps  
Data warehouse queries on Parquet files in S3| DuckDB| Query Parquet directly from S3/HTTP, no ingestion  
Embedded IoT device with 64MB RAM| SQLite| Minimal footprint, runs on anything  
BI dashboard with complex aggregations| DuckDB| Vectorized execution, rich SQL, fast on aggregates  
Both OLTP + OLAP in the same app| Both| SQLite for transactions, DuckDB for analytics queries  
  
**Bottom line:** SQLite and DuckDB are not competitors — they are complementary. SQLite is your application's transactional database; DuckDB is your analytical engine. Use SQLite for writes, point lookups, and application state. Use DuckDB for queries that scan, aggregate, or join large datasets. Many modern data stacks use both: SQLite for the operational database, DuckDB for the analytical queries, and they happily coexist. See also: [Best Database Tools for Developers](</en/tools/best-database-gui-tools.html>) and [Columnar Database Guide](</en/compare/duckdb-vs-sqlite.html>).
