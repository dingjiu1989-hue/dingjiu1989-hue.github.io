---
title: "PostgreSQL Vacuuming: Maintenance, Tuning, and Automation"
description: "Master PostgreSQL VACUUM: autovacuum tuning, bloat prevention, and maintenance best practices."
date: 2026-05-12
board: database
url: https://dingjiu1989-hue.github.io/en/database/database-vacuuming-maintenance.html
---

# PostgreSQL Vacuuming: Maintenance, Tuning, and Automation

# PostgreSQL Vacuuming: Maintenance, Tuning, and Automation

# PostgreSQL Vacuuming: Maintenance, Tuning, and Automation

# PostgreSQL Vacuuming: Maintenance, Tuning, and Automation

# PostgreSQL Vacuuming: Maintenance, Tuning, and Automation

# PostgreSQL Vacuuming: Maintenance, Tuning, and Automation

# PostgreSQL Vacuuming: Maintenance, Tuning, and Automation

# PostgreSQL Vacuuming: Maintenance, Tuning, and Automation

# PostgreSQL Vacuuming: Maintenance, Tuning, and Automation

# PostgreSQL Vacuuming: Maintenance, Tuning, and Automation

# PostgreSQL Vacuuming: Maintenance, Tuning, and Automation

# PostgreSQL Vacuuming: Maintenance, Tuning, and Automation

PostgreSQL uses Multi-Version Concurrency Control (MVCC) to handle concurrent transactions. Every UPDATE and DELETE creates a new row version while keeping the old one. Dead rows accumulate over time, consuming storage and degrading query performance. VACUUM reclaims this space and updates statistics.

## Understanding Bloat

Table bloat occurs when dead row versions accumulate faster than VACUUM reclaims them. Causes include long-running transactions that prevent dead row removal, high update frequency tables, and insufficient VACUUM frequency.

Measure bloat using the pg_stat_user_tables view. High n_dead_tup relative to n_live_tup indicates bloat. A ratio over 20% needs investigation. The pgstattuple extension provides accurate bloat measurement per table.

## Autovacuum Tuning

Autovacuum runs automatically based on thresholds. The default settings work for small databases but need tuning for large ones. Key parameters: autovacuum_vacuum_threshold (50) plus autovacuum_vacuum_scale_factor (0.2) means VACUUM triggers when 20% of rows plus 50 are dead. For large tables, reduce scale_factor or use per-table settings.

autovacuum_vacuum_cost_limit and autovacuum_vacuum_cost_delay control autovacuum's I/O impact. Default settings are conservative (cost_limit=200, cost_delay=20ms). Increase cost_limit for faster VACUUM on systems with I/O headroom. Decrease cost_delay for aggressive cleanup.

Set per-table autovacuum settings for busy tables:

ALTER TABLE orders SET (autovacuum_vacuum_scale_factor = 0.05, autovacuum_vacuum_threshold = 1000);

## Manual Vacuum Operations

Standard VACUUM reclaims space but does not return it to the operating system. It makes space available for reuse within the table. Run standard VACUUM during low-traffic periods for tables with heavy updates.

VACUUM FULL reclaims space to the OS but requires an ACCESS EXCLUSIVE lock. It rewrites the entire table, blocking all operations. Use during maintenance windows only. Consider pg_repack instead—it rebuilds tables without blocking reads or writes.

## Monitoring

Track vacuum activity through pg_stat_progress_vacuum. Monitor last_autovacuum and last_analyze timestamps. Tables not vacuumed in 24 hours need attention. Set up alerts for tables approaching the autovacuum threshold without being vacuumed.

**See also:** [Connection Pooling: Tuning, Best Practices, and Pitfalls](</en/database/database-connection-pooling.html>), [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [Batch Operations: Bulk Insert, COPY, and Batch Size Tuning](</en/database/batch-operations.html>).

**See also:** [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [Connection Pooling: Tuning, Best Practices, and Pitfalls](</en/database/database-connection-pooling.html>), [Batch Operations: Bulk Insert, COPY, and Batch Size Tuning](</en/database/batch-operations.html>)
