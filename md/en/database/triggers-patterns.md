---
title: "Database Triggers: Use Cases, Performance Costs, and Alternatives"
description: "Explore database triggers for audit logging, validation, and synchronization. Understand performance costs, debugging challenges, and CDC alternatives."
date: 2026-04-09
board: database
url: https://dingjiu1989-hue.github.io/en/database/triggers-patterns.html
---

# Database Triggers: Use Cases, Performance Costs, and Alternatives

Database Triggers: Use Cases, Performance Costs, and Alternatives 

A trigger is a named database object that executes a function automatically in response to `INSERT`, `UPDATE`, `DELETE`, or `TRUNCATE` events on a table. Triggers run inside the same transaction and offer powerful guarantees, but they carry real costs. 

Anatomy of a Trigger 

A trigger consists of two parts: the trigger definition and the trigger function. PostgreSQL separates them, allowing one function to serve multiple triggers. 

CREATE OR REPLACE FUNCTION log_changes()

RETURNS TRIGGER AS $$

BEGIN

IF TG_OP = 'UPDATE' THEN

INSERT INTO audit_log (table_name, row_id, old_data, new_data, changed_at)

VALUES (TG_TABLE_NAME, OLD.id, row_to_json(OLD), row_to_json(NEW), NOW());

RETURN NEW;

ELSIF TG_OP = 'DELETE' THEN

INSERT INTO audit_log (table_name, row_id, old_data, changed_at)

VALUES (TG_TABLE_NAME, OLD.id, row_to_json(OLD), NOW());

RETURN OLD;

END IF;

RETURN NULL; -- for INSERT, do nothing

END;

$$ LANGUAGE plpgsql;

CREATE TRIGGER audit_users

AFTER UPDATE OR DELETE ON users

FOR EACH ROW EXECUTE FUNCTION log_changes();

Trigger timing options: 

  * `BEFORE`: Runs before the operation. Useful for validation or default-value injection.

  * `AFTER`: Runs after the operation. Used for audit logs, cascade updates, or synchronization.

  * `INSTEAD OF`: Replaces the operation entirely. Only valid on views.




Common Use Cases 

Audit Logging 

Recording every change to sensitive tables is the most common trigger use case: 

CREATE TABLE audit_log (

id BIGSERIAL PRIMARY KEY,

table_name TEXT NOT NULL,

operation TEXT NOT NULL,

row_id INTEGER,

old_values JSONB,

new_values JSONB,

changed_by TEXT DEFAULT current_user,

changed_at TIMESTAMPTZ DEFAULT NOW()

);

CREATE OR REPLACE FUNCTION audit_employee_changes()

RETURNS TRIGGER AS $$

BEGIN

INSERT INTO audit_log (table_name, operation, row_id, old_values, new_values)

VALUES ('employees', TG_OP, COALESCE(NEW.id, OLD.id),

CASE WHEN TG_OP IN ('UPDATE', 'DELETE') THEN row_to_json(OLD)::jsonb END,

CASE WHEN TG_OP IN ('INSERT', 'UPDATE') THEN row_to_json(NEW)::jsonb END);

RETURN COALESCE(NEW, OLD);

END;

$$ LANGUAGE plpgsql SECURITY DEFINER;

Business Rule Validation 

BEFORE triggers enforce invariants that cannot be expressed as `CHECK` constraints: 

CREATE OR REPLACE FUNCTION validate_order()

RETURNS TRIGGER AS $$

BEGIN

IF NEW.total < 0 THEN

RAISE EXCEPTION 'Order total cannot be negative: %', NEW.total;

END IF;

IF NEW.status = 'shipped' AND OLD.status != 'paid' THEN

RAISE EXCEPTION 'Cannot ship unpaid order %', NEW.id;

END IF;

RETURN NEW;

END;

$$ LANGUAGE plpgsql;

Cross-Table Synchronization 

Keep denormalized counters or summary tables in sync: 

CREATE OR REPLACE FUNCTION update_user_order_count()

RETURNS TRIGGER AS $$

BEGIN

IF TG_OP = 'INSERT' THEN

UPDATE users SET order_count = order_count + 1 WHERE id = NEW.user_id;

ELSIF TG_OP = 'DELETE' THEN

UPDATE users SET order_count = order_count - 1 WHERE id = OLD.user_id;

END IF;

RETURN COALESCE(NEW, OLD);

END;

$$ LANGUAGE plpgsql;

Performance Costs 

Triggers add overhead that is easy to underestimate: 

  * **Per-row execution** : `FOR EACH ROW` triggers execute the function once per affected row. An `UPDATE` that modifies 100,000 rows runs the trigger 100,000 times.

  * **Transaction scope** : Trigger failures roll back the entire operation, not just the trigger action.

  * **Nested triggers** : A trigger that updates another table can fire triggers on that table, creating a cascade that is difficult to debug.

  * **Lock duration** : Triggers extend the time a row or page lock is held, increasing contention in high-concurrency workloads.




The `pg_stat_user_functions` view helps identify trigger overhead: 

SELECT total_time / calls AS avg_time_per_call,

calls,

funcname

FROM pg_stat_user_functions

WHERE funcname LIKE '%trigger%'

ORDER BY total_time DESC;

Debugging Challenges 

Triggers execute transparently. Developers new to a codebase often discover triggers only when an `UPDATE` suddenly fails with an unexpected error. Mitigation strategies: 

  * **Naming conventions** : Prefix trigger functions with `trg_` and trigger names with the table name.



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Document dependencies** : Maintain a trigger dependency map. 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Session-level disable** (requires superuser or explicit privilege): 

SET session_replication_role = replica;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Perform bulk operation

SET session_replication_role = origin;

Alternatives: Change Data Capture (CDC) 

When triggers become too expensive or complex, Change Data Capture offers a streaming alternative: 

  * **Logical replication** (PostgreSQL native): Streams changes to a consumer without triggers.

  * **Debezium** : Captures row changes via the write-ahead log and publishes them to Kafka.

  * **pgoutput + pg_recvlogical** : Custom CDC implementations.




CDC avoids trigger overhead, does not slow the original transaction, and supports real-time streaming to external systems. 

Best Practices 

  * Prefer `CONSTRAINT` triggers for deferred validation when possible.

  * Keep trigger functions fast: avoid network calls, file I/O, and expensive computations.

  * Use `FOR EACH STATEMENT` when row-level granularity is unnecessary.

  * Add comments explaining _why_ the trigger exists, not just what it does.

  * Test trigger behavior with rollback test cases.




Triggers are a legitimate tool for data integrity, but they should be your last resort, not your first instinct. When a `CHECK` constraint, `UNIQUE` index, or `FOREIGN KEY` can enforce the rule, use that instead.

**See also:** [Change Data Capture: Tracking Database Changes in Real-Time](</en/database/database-change-tracking-cdc.html>), [Database Audit Triggers: Automatic Change Tracking](</en/database/database-audit-triggers.html>), [Partitioning vs Sharding](</en/database/partitioning-vs-sharding.html>).

**See also:** [Change Data Capture: Tracking Database Changes in Real-Time](</en/database/database-change-tracking-cdc.html>), [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Materialized Views](</en/database/materialized-views.html>)

**See also:** [Change Data Capture: Tracking Database Changes in Real-Time](</en/database/database-change-tracking-cdc.html>), [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Materialized Views](</en/database/materialized-views.html>)

**See also:** [Change Data Capture: Tracking Database Changes in Real-Time](</en/database/database-change-tracking-cdc.html>), [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Materialized Views](</en/database/materialized-views.html>)

**See also:** [Change Data Capture: Tracking Database Changes in Real-Time](</en/database/database-change-tracking-cdc.html>), [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Materialized Views](</en/database/materialized-views.html>)

**See also:** [Change Data Capture: Tracking Database Changes in Real-Time](</en/database/database-change-tracking-cdc.html>), [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Materialized Views](</en/database/materialized-views.html>)

**See also:** [Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector](</en/database/database-types-overview.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Schema Design Patterns: Normalization, Denormalization, Naming Conventions](</en/database/schema-design.html>)

**See also:** [Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector](</en/database/database-types-overview.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Schema Design Patterns: Normalization, Denormalization, Naming Conventions](</en/database/schema-design.html>)

**See also:** [Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector](</en/database/database-types-overview.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Schema Design Patterns: Normalization, Denormalization, Naming Conventions](</en/database/schema-design.html>)

**See also:** [Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector](</en/database/database-types-overview.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Schema Design Patterns: Normalization, Denormalization, Naming Conventions](</en/database/schema-design.html>)

**See also:** [Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector](</en/database/database-types-overview.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Schema Design Patterns: Normalization, Denormalization, Naming Conventions](</en/database/schema-design.html>)

**See also:** [Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector](</en/database/database-types-overview.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Schema Design Patterns: Normalization, Denormalization, Naming Conventions](</en/database/schema-design.html>)

**See also:** [Database Types Overview: Relational, Document, Key-Value, Graph, Time-Series, Vector](</en/database/database-types-overview.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Schema Design Patterns: Normalization, Denormalization, Naming Conventions](</en/database/schema-design.html>)
