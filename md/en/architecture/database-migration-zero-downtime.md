---
title: "Zero-Downtime Database Migrations"
description: "Expand-contract pattern, backward-compatible schema changes, safe migration strategies, and production practices"
date: 2026-04-23
board: architecture
url: https://aidev.fit/en/architecture/database-migration-zero-downtime.html
---

# Zero-Downtime Database Migrations

Database migrations are the highest-risk operation in zero-downtime deployments. Schema changes can lock tables, break queries, or silently corrupt data. In a distributed system where multiple service instances run different versions simultaneously, every migration must be backward compatible with both old and new code. The expand-contract pattern is the canonical approach to achieving this. 

The expand phase adds new schema elements without modifying or removing existing ones. New columns are added as nullable (or with default values), new tables are created alongside existing ones, and new indexes are built in the background. During this phase, old code continues to work unchanged — it reads and writes the old schema elements. New code can begin writing to both old and new elements to populate them for the eventual switchover. 

The migration phase transitions from old to new schema elements. This is typically done through a data migration script that backfills new columns or tables from old data. The migration should run in batches with progress tracking, allowing pausing and resuming. Locks should be minimized — use techniques like batch processing with sleep intervals, or use database-specific online DDL features (PostgreSQL pg_repack, MySQL pt-online-schema-change, or gh-ost). 

The contract phase removes old schema elements that are no longer needed. This only occurs after all running instances have been updated to use the new schema exclusively — verified through code audit and monitoring. Dropping a column requires confirming that no query references it. Dropping an index requires confirming that the query planner no longer uses it. Dropping a table requires confirming that no foreign key or application code references it. 

Column additions are the simplest case. Adding a nullable column with a default value is generally safe in modern databases. However, adding a NOT NULL column requires caution — either provide a default value (which locks the table in some databases) or add the column as nullable, backfill data, and then add the NOT NULL constraint. PostgreSQL can add a NOT NULL column with a default without table rewrite in recent versions. 

Index changes require careful timing. Adding an index can be done concurrently in PostgreSQL (CREATE INDEX CONCURRENTLY) without locking writes, but this takes longer and consumes resources. MySQL 8+ supports online DDL for most index operations. The index addition should be verified with EXPLAIN plans before and after to ensure the query planner actually uses the new index. Dropping an index should only happen after confirming that all query patterns that depended on it have been updated. 

Table changes are more complex. Renaming a table requires a two-phase approach: add a view or synonym with the old name, rename the table, and update code to use the new name. Splitting a table requires creating the new tables, writing dual-write code to keep both old and new tables in sync while backfilling historical data, then switching reads to the new tables. 

Foreign key additions risk deadlocks and performance degradation. In high-traffic systems, adding foreign keys should be done with NOT VALID constraints that are later validated. The validation runs as a background operation without locking. This approach ensures new data respects the constraint while existing data is validated asynchronously. 

The expand-contract pattern naturally handles rollbacks. If the deployment fails during the expand phase, simply roll back the application code — the empty new columns and tables are harmless. If the deployment fails during the migration phase (data backfill), the migration can be paused or reversed. Only the contract phase (removing old elements) is non-reversible — which is why it must be executed as a separate, confirmed step. 

Orchestration and automation are essential for production migrations. Tools like Flyway, Liquibase, and Alembic manage migration versions and ordering. They should be integrated with CI/CD so that migrations are tested against a staging database before production. Migration scripts should be idempotent — running them multiple times should be safe. 

Monitoring during migration is critical. Track migration progress, database CPU, replication lag, lock contention, and query latency. Set up automated alerts for any metrics that deviate from baseline. If a migration causes performance degradation, have a plan to pause or rollback. In high-traffic environments, run migrations during low-traffic periods even with zero-downtime techniques, to provide maximum safety margin. 

Testing migrations against production data volume is essential. Synthetic migrations against staging databases with small data volumes miss performance problems that emerge at scale. Use anonymized production data snapshots or automated data generation that matches production distribution to validate migration performance before deployment.

**See also:** [Zero-Downtime Deployment Strategies](</en/architecture/zero-downtime-deployment.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [Blue-Green Deployment Strategy](</en/architecture/blue-green-deployment.html>).

**See also:** [Zero-Downtime Deployment Strategies](</en/architecture/zero-downtime-deployment.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [Blue-Green Deployment Strategy](</en/architecture/blue-green-deployment.html>)

**See also:** [Zero-Downtime Deployment Strategies](</en/architecture/zero-downtime-deployment.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [Blue-Green Deployment Strategy](</en/architecture/blue-green-deployment.html>)

**See also:** [Zero-Downtime Deployment Strategies](</en/architecture/zero-downtime-deployment.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [Blue-Green Deployment Strategy](</en/architecture/blue-green-deployment.html>)

**See also:** [Zero-Downtime Deployment Strategies](</en/architecture/zero-downtime-deployment.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [Blue-Green Deployment Strategy](</en/architecture/blue-green-deployment.html>)

**See also:** [Zero-Downtime Deployment Strategies](</en/architecture/zero-downtime-deployment.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [Blue-Green Deployment Strategy](</en/architecture/blue-green-deployment.html>)

**See also:** [Monolith-First Strategy](</en/architecture/monolith-first-strategy.html>), [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>)

**See also:** [Monolith-First Strategy](</en/architecture/monolith-first-strategy.html>), [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>)

**See also:** [Monolith-First Strategy](</en/architecture/monolith-first-strategy.html>), [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>)

**See also:** [Monolith-First Strategy](</en/architecture/monolith-first-strategy.html>), [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>)

**See also:** [Monolith-First Strategy](</en/architecture/monolith-first-strategy.html>), [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>)

**See also:** [Monolith-First Strategy](</en/architecture/monolith-first-strategy.html>), [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>)

**See also:** [Monolith-First Strategy](</en/architecture/monolith-first-strategy.html>), [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>)

**See also:** [Monolith-First Strategy](</en/architecture/monolith-first-strategy.html>), [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>)

**See also:** [Monolith-First Strategy](</en/architecture/monolith-first-strategy.html>), [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>)

**See also:** [Monolith-First Strategy](</en/architecture/monolith-first-strategy.html>), [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>)

**See also:** [Monolith-First Strategy](</en/architecture/monolith-first-strategy.html>), [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>)

**See also:** [Monolith-First Strategy](</en/architecture/monolith-first-strategy.html>), [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>)

**See also:** [Monolith-First Strategy](</en/architecture/monolith-first-strategy.html>), [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>)

**See also:** [Monolith-First Strategy](</en/architecture/monolith-first-strategy.html>), [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>)

**See also:** [Monolith-First Strategy](</en/architecture/monolith-first-strategy.html>), [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>)

**See also:** [Monolith-First Strategy](</en/architecture/monolith-first-strategy.html>), [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>)

**See also:** [Monolith-First Strategy](</en/architecture/monolith-first-strategy.html>), [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>)

**See also:** [Monolith-First Strategy](</en/architecture/monolith-first-strategy.html>), [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>)
