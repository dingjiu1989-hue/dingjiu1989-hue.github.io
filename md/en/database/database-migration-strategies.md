---
title: "Database Migration Strategies"
description: "Zero-downtime database migration strategies with rollback planning, testing, and CI/CD integration."
date: 2026-05-12
board: database
url: https://dingjiu1989-hue.github.io/en/database/database-migration-strategies.html
---

# Database Migration Strategies

Database migrations in production are terrifying — one mistake can corrupt data, cause downtime, or lock a critical table for hours. Yet every application needs them. This guide covers battle-tested strategies for running database migrations with zero downtime, including the expand-contract pattern, handling large tables, and reversible migrations. Migration Strategies Compared Strategy| Downtime| Complexity| Best For  
---|---|---|---  
Expand-Contract| Zero| High| Schema changes on high-traffic tables  
Online Schema Change (gh-ost, pt-online-schema-change)| Zero| Medium| ALTER TABLE on large MySQL tables  
Blue-Green Database| Near-zero| Very High| Major version upgrades, risky operations  
Deploy + Migrate (simultaneous)| Brief (seconds)| Low| Small apps with maintenance windows  
Shadow Table Migration| Zero| Medium| Reshaping or cleaning data with dual writes  
The Expand-Contract Pattern (Zero-Downtime) **Best for:** Adding, renaming, or removing columns without downtime. The key insight: deploy in multiple phases, and each phase must be compatible with the previous version. Example: Renaming a Column (users.name → users.full_name) Phase| What to Do| App Behavior  
---|---|---  
1\. Expand| Add new column full_name (nullable), write to BOTH columns| App writes to both old and new column  
2\. Backfill| COPY name into full_name for existing rows| App reads from new column, falls back to old; writes to both  
3\. Migrate reads| Deploy code that reads only from new column| App reads from full_name only, writes to both  
4\. Contract| Stop writing to old column, eventually DROP it| App reads and writes full_name only  
Handling Large Tables (100M+ Rows) **Critical rule:** Never run a blocking ALTER TABLE on a large production table — it acquires an ACCESS EXCLUSIVE lock for the duration, blocking all reads and writes. Database| Safe Solution| Tool  
---|---|---  
PostgreSQL| Add CHECK constraints as NOT VALID, validate later| Built-in: ADD CONSTRAINT ... NOT VALID; ALTER CONSTRAINT ... VALIDATE  
PostgreSQL| Create index with CONCURRENTLY| CREATE INDEX CONCURRENTLY (no table lock)  
PostgreSQL| Add column with a default (PG 11+)| ALTER TABLE ... ADD COLUMN ... DEFAULT (no rewrite in PG 11+)  
MySQL| Online schema change| gh-ost (GitHub), pt-online-schema-change (Percona)  
SQLite| Batched writes in a transaction| Wrap in BEGIN/COMMIT, limit batch size to ~10,000 rows  
Reversible Migrations Every migration should have a planned rollback. Before running a migration, write (and test) the down migration: Change| Up Migration| Down Migration  
---|---|---  
Add column| ALTER TABLE users ADD COLUMN bio TEXT;| ALTER TABLE users DROP COLUMN bio;  
Add NOT NULL column| Add nullable → backfill → set NOT NULL (3-phase)| ALTER TABLE users ALTER COLUMN bio DROP NOT NULL;  
Rename column| Expand-contract (4 phases, see above)| Reverse the expand-contract phases  
Add index| CREATE INDEX CONCURRENTLY ...;| DROP INDEX CONCURRENTLY ...;  
**Bottom line:** The expand-contract pattern is the gold standard for zero-downtime migrations — deploy changes in small, compatible steps. For any ALTER TABLE on a large production table, use your database's non-blocking equivalent (CONCURRENTLY for PostgreSQL, gh-ost for MySQL). Never run a migration you cannot roll back. See also: [Database Design Fundamentals](</en/tech/database-design-fundamentals.html>) and [PostgreSQL vs MySQL vs SQLite](</en/compare/postgresql-vs-mysql-vs-sqlite.html>).
