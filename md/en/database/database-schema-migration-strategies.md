---
title: "Database Schema Migration: Version Control, Rollback, and Zero-Downtime"
description: "Database migration strategies for production: version-controlled schemas, rollback planning, and zero-downtime deploys."
date: 2026-05-12
board: database
url: https://dingjiu1989-hue.github.io/en/database/database-schema-migration-strategies.html
---

# Database Schema Migration: Version Control, Rollback, and Zero-Downtime

## Database Schema Migration: Version Control, Rollback, and Zero-Downtime

## Database Schema Migration: Version Control, Rollback, and Zero-Downtime

## Database Schema Migration: Version Control, Rollback, and Zero-Downtime

## Database Schema Migration: Version Control, Rollback, and Zero-Downtime

## Database Schema Migration: Version Control, Rollback, and Zero-Downtime

## Database Schema Migration: Version Control, Rollback, and Zero-Downtime

## Database Schema Migration: Version Control, Rollback, and Zero-Downtime

## Database Schema Migration: Version Control, Rollback, and Zero-Downtime

## Database Schema Migration: Version Control, Rollback, and Zero-Downtime

## Database Schema Migration: Version Control, Rollback, and Zero-Downtime

## Database Schema Migration: Version Control, Rollback, and Zero-Downtime

## Database Schema Migration: Version Control, Rollback, and Zero-Downtime

Database schema changes in production require careful planning. Unlike application code, database changes are stateful—they modify existing data and structures. A bad migration can cause downtime, data loss, or performance degradation.

### Version Control for Schema

Treat database schemas as code. Every migration is a file in version control. Use a migration tool (Flyway, Liquibase, Alembic, Prisma Migrate) that tracks which migrations have been applied. The migration tool maintains a tracking table in the database.

Migration naming convention: use timestamps or sequential numbers: 20260512_create_orders_table.sql. Each migration should be additive when possible—adding tables, columns, and indexes is easier to reverse than removing them.

### Migration Patterns

Expand-migrate-contract is the standard pattern for zero-downtime migrations. Phase 1 (expand): add new columns, tables, and indexes without removing old ones. Deploy application code that writes to both old and new structures. Phase 2 (migrate): backfill new columns with data from old columns. Run data validation. Phase 3 (contract): remove old columns and tables after verifying new structures work.

Backward-compatible migrations are safe to deploy at any time. Adding a nullable column is backward-compatible. Adding a column with NOT NULL requires a default value. Renaming a column requires a multi-phase migration—add the new name, dual-write, backfill, then remove the old name.

### Rollback Planning

Every migration needs a rollback script. Test rollbacks before production deployment—they are harder to get right than forward migrations. Rollback of data migrations (backfilling, transformation) requires extra care because data may have changed since the forward migration.

Flyway supports undo migrations with naming convention. Liquibase supports rollback commands. Alembic can generate downgrade scripts. Test the complete forward-and-rollback cycle in a staging environment.

### Performance Considerations

Large migrations lock tables. Adding a column with a default value locks the table in PostgreSQL—it rewrites the table. Adding a CHECK or NOT NULL constraint requires a full table scan. Use pg_repack or pt-online-schema-change for zero-downtime schema changes on large tables.

Batch data migrations: backfill 1000-10000 rows per transaction. Monitor replication lag. Pause if lag exceeds threshold. Set statement_timeout to prevent runaway queries. Run during low-traffic periods.

### Production Checklist

Review migration SQL for locking behavior. Check disk space—ALTER TABLE can double table size temporarily. Run migration on a replica first. Have a rollback plan documented. Test on a staging database with production-scale data. Monitor query performance after migration. Set up rollback alerting.

**See also:** [Database Migration Strategies](</en/database/database-migration-strategies.html>), [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>).

**See also:** [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>), [Database Migration Strategies](</en/database/database-migration-strategies.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>)

**See also:** [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>), [Database Migration Strategies](</en/database/database-migration-strategies.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>)
