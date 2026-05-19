---
title: "Database Migration Tools: Alembic, Flyway, Liquibase, Versioning"
description: "Compare database migration tools including Alembic, Flyway, and Liquibase. Learn versioning strategies, rollback patterns, and best practices for schema changes."
date: 2026-04-02
board: database
url: https://dingjiu1989-hue.github.io/en/database/database-migration-tools.html
---

# Database Migration Tools: Alembic, Flyway, Liquibase, Versioning

Database Migration Tools: Alembic, Flyway, Liquibase, Versioning 

Database migrations are the practice of version-controlling schema changes. A good migration tool applies changes in order, handles conflicts, and supports rollback. This article compares the three leading tools and covers migration strategies. 

Why Migrations? 

Without migrations, schema changes are applied manually or through ad-hoc scripts: 

  * "Did we run the `ALTER TABLE` on staging?"

  * "Which servers have the new index?"

  * "The deploy failed because the migration hadn't run yet."




Migrations solve these problems by making schema changes repeatable, versioned, and automated. 

Alembic 

Alembic is the migration tool for SQLAlchemy (Python). It generates migration scripts from model definitions and supports auto-generation. 

Setup 

## alembic.ini

[alembic]

script_location = alembic

sqlalchemy.url = postgresql://user:pass@localhost/mydb

alembic init alembic

Creating a Migration 

## alembic/versions/0001_create_users.py

"""create users table

Revision ID: 0001

Revises: None

Create Date: 2026-05-12

"""

from alembic import op

import sqlalchemy as sa

def upgrade():

op.create_table(

'users',

sa.Column('id', sa.Integer(), primary_key=True),

sa.Column('email', sa.String(255), nullable=False),

sa.Column('name', sa.String(100)),

sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),

)

op.create_index('idx_users_email', 'users', ['email'], unique=True)

def downgrade():

op.drop_index('idx_users_email')

op.drop_table('users')

Auto-Generation 

## Generate migration from model changes

alembic revision --autogenerate -m "add avatar column"

This compares the current database state against SQLAlchemy models and generates `upgrade()` and `downgrade()` functions. 

Running Migrations 

alembic upgrade head # Apply all pending migrations

alembic upgrade +2 # Apply next 2 migrations

alembic downgrade -1 # Rollback 1 migration

alembic history # View migration history

alembic current # Show current revision

Flyway 

Flyway is a Java-based migration tool that works with SQL scripts. It is simple, opinionated, and supports multiple databases. 

Directory Structure 

sql/

V1__create_users.sql

V2__add_avatar_column.sql

V3__create_orders_table.sql

Migration Script 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- V1__create_users.sql

CREATE TABLE users (

id BIGSERIAL PRIMARY KEY,

email VARCHAR(255) NOT NULL UNIQUE,

name VARCHAR(100),

created_at TIMESTAMPTZ DEFAULT NOW()

);

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- V2__add_avatar_column.sql

ALTER TABLE users ADD COLUMN avatar_url VARCHAR(500);

Configuration 

## flyway.conf

flyway.url = jdbc:postgresql://localhost:5432/mydb

flyway.user = app_user

flyway.password = secure_password

flyway.locations = filesystem:sql

flyway.baselineOnMigrate = true

Running 

flyway migrate

flyway undo # Flyway Teams only

flyway info # Show migration status

flyway validate # Check for changes to applied migrations

Checksum Validation 

Flyway stores a checksum of each migration script. If a script is modified after being applied, `flyway validate` detects the change and warns: 

> If a deployed migration is edited, Flyway catches it and refuses to apply further migrations until the discrepancy is resolved. 

Liquibase 

Liquibase supports multiple change formats: SQL, XML, YAML, and JSON. It is the most flexible but most verbose option. 

Changeset (XML) 

xmlns="http://www.liquibase.org/xml/ns/dbchangelog"

xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog

http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-latest.xsd">

Changeset (YAML) 

databaseChangeLog:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- changeSet:

id: 2

author: bob

changes:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- addColumn:

tableName: users

columns:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- column:

name: avatar_url

type: varchar(500)

Rolling Back 

liquibase rollbackCount 1 # Rollback 1 changeset

liquibase rollbackToDate 2026-05-10T12:00:00 # Rollback to specific date

liquibase rollback --tag v1.0 # Rollback to tagged release

Tool Comparison 

| Feature | Alembic | Flyway | Liquibase | |---------|---------|--------|-----------| | Language | Python | Java/SQL | Java | | Auto-generation | Yes (from models) | No | No | | Rollback | Code-defined | Undo migration | Rollback changeset | | CI/CD integration | Pipeline script | Maven/Gradle/CLI | Maven/Gradle/CLI | | Complex logic | Python code | SQL only | SQL + XML/YAML | | Learning curve | Medium | Low | Medium | | Database support | SQLAlchemy-supported | 20+ databases | 15+ databases | 

Migration Strategy Patterns 

Linear Migrations 

The simplest pattern: each migration depends on the previous one. 

V1 → V2 → V3 → V4

Branching with Merges 

For larger teams, branches create divergent migration histories: 

V1 → V2 → V3 → V4 (main branch)

└→ V2a → V2b (feature branch)

When the feature branch merges, use `flyway merge` or adjust `Alembic` revision dependencies. 

Repeatable Migrations 

Views, functions, and stored procedures benefit from repeatable migrations that reapply on every change: 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Flyway: R__update_user_view.sql

CREATE OR REPLACE VIEW active_users AS

SELECT * FROM users WHERE deleted_at IS NULL;

## Alembic: revision_identifiers.py with %(revision)s

## Or mark as "revision_identifiers = False" for repeatable patterns

Best Practices 

  * **One change per migration** : Adding a column and creating a table in the same migration makes rollback harder.



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Test both directions** : Always test `upgrade()` and `downgrade()` before merging. 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Use CI validation** : Run `flyway validate` or `alembic check` in CI to catch mistakes. 4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Avoid long-running locks** : Use `CREATE INDEX CONCURRENTLY` instead of `CREATE INDEX` in migrations. 5\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Never modify applied migrations** : Create a new migration to fix issues. 6\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Database-as-code** : Store migrations in version control alongside application code. 

Database migrations bring schema changes into the software development lifecycle. Choose the tool that fits your language ecosystem, establish clear conventions, and make schema changes as routine as code changes.

**See also:** [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>), [Database Schema Migration: Version Control, Rollback, and Zero-Downtime](</en/database/database-schema-migration-strategies.html>), [Database Migration Strategies](</en/database/database-migration-strategies.html>).

**See also:** [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Database Schema Migration: Version Control, Rollback, and Zero-Downtime](</en/database/database-schema-migration-strategies.html>)

**See also:** [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Database Schema Migration: Version Control, Rollback, and Zero-Downtime](</en/database/database-schema-migration-strategies.html>)

**See also:** [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Database Schema Migration: Version Control, Rollback, and Zero-Downtime](</en/database/database-schema-migration-strategies.html>)

**See also:** [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Database Schema Migration: Version Control, Rollback, and Zero-Downtime](</en/database/database-schema-migration-strategies.html>)

**See also:** [Database Migration Version Control Strategies](</en/database/database-migration-version-control.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Database Schema Migration: Version Control, Rollback, and Zero-Downtime](</en/database/database-schema-migration-strategies.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Schema Design Patterns: Normalization, Denormalization, Naming Conventions](</en/database/schema-design.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Schema Design Patterns: Normalization, Denormalization, Naming Conventions](</en/database/schema-design.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Schema Design Patterns: Normalization, Denormalization, Naming Conventions](</en/database/schema-design.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Schema Design Patterns: Normalization, Denormalization, Naming Conventions](</en/database/schema-design.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Schema Design Patterns: Normalization, Denormalization, Naming Conventions](</en/database/schema-design.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Schema Design Patterns: Normalization, Denormalization, Naming Conventions](</en/database/schema-design.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Schema Design Patterns: Normalization, Denormalization, Naming Conventions](</en/database/schema-design.html>)
