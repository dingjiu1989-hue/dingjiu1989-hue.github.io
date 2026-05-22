---
title: "Stored Procedures vs Functions: When to Use, Languages, Security"
description: "An in-depth guide to stored procedures and functions in PostgreSQL and SQL Server. Learn language options, security considerations, testing, and best practices."
date: 2026-04-09
board: database
url: https://aidev.fit/en/database/stored-procedures.html
---

# Stored Procedures vs Functions: When to Use, Languages, Security

Stored Procedures vs Functions: When to Use, Languages, Security 

Stored procedures and user-defined functions (UDFs) let you execute application logic inside the database engine. While they share similarities, their differences determine the right use case for each. 

Functions vs Procedures 

In PostgreSQL, the distinction is clearer since version 11 introduced `CREATE PROCEDURE`: 

| Aspect | Function (`FUNCTION`) | Procedure (`PROCEDURE`) | |--------|----------------------|------------------------| | Return value | Always returns a value | Can return nothing | | Called from SQL | Yes: `SELECT my_func()` | No: `CALL my_proc()` | | Transaction control | Cannot commit/rollback | Can commit/rollback | | Used in expressions | Yes | No | 

A typical function in PL/pgSQL: 

CREATE OR REPLACE FUNCTION calculate_discount(

customer_id INTEGER,

order_total NUMERIC

) RETURNS NUMERIC AS $$

DECLARE

tier TEXT;

discount NUMERIC := 0;

BEGIN

SELECT membership_tier INTO tier FROM customers WHERE id = customer_id;

IF tier = 'gold' THEN

discount := order_total * 0.20;

ELSIF tier = 'silver' THEN

discount := order_total * 0.10;

END IF;

RETURN discount;

END;

$$ LANGUAGE plpgsql IMMUTABLE;

Calling it inline: 

SELECT id, total, calculate_discount(id, total) AS discount

FROM orders WHERE status = 'pending';

A stored procedure for multi-step operations with transaction control: 

CREATE OR REPLACE PROCEDURE process_order_payment(

p_order_id INTEGER,

p_payment_method TEXT

) AS $$

DECLARE

v_total NUMERIC;

v_account_id INTEGER;

BEGIN

SELECT total, account_id INTO v_total, v_account_id

FROM orders WHERE id = p_order_id;

UPDATE accounts SET balance = balance - v_total

WHERE id = v_account_id;

INSERT INTO payments (order_id, method, amount, paid_at)

VALUES (p_order_id, p_payment_method, v_total, NOW());

UPDATE orders SET status = 'paid' WHERE id = p_order_id;

COMMIT;

EXCEPTION WHEN OTHERS THEN

ROLLBACK;

RAISE;

END;

$$ LANGUAGE plpgsql;

CALL process_order_payment(1001, 'credit_card');

Language Options 

PostgreSQL supports multiple procedural languages, each with distinct advantages. 

**PL/pgSQL** is the default. It is designed for PostgreSQL and offers tight integration with SQL, transparent cursor handling, and exception blocks. Use it for data-intensive logic where most work happens inside SQL statements. 

**PL/Python** (via `CREATE EXTENSION plpython3u`) allows Python logic inside the database. It is useful for business rules expressed naturally in Python, but it adds interpreter overhead and runs in a separate process. 

**PL/v8** supports JavaScript via V8. It is fast for compute-heavy functions but less commonly used in production. 

**PL/SQL** in Oracle and **T-SQL** in SQL Server are proprietary equivalents. T-SQL uses a `CREATE PROCEDURE` syntax with `SET` and `SELECT` semantics: 

CREATE OR ALTER PROCEDURE GetCustomerOrders

@CustomerId INT,

@MinTotal DECIMAL(10,2) = 0

AS

BEGIN

SET NOCOUNT ON;

SELECT o.Id, o.OrderDate, o.Total

FROM Orders o

WHERE o.CustomerId = @CustomerId

AND o.Total >= @MinTotal

ORDER BY o.OrderDate DESC;

END;

EXEC GetCustomerOrders @CustomerId = 42, @MinTotal = 100;

Security Considerations 

Procedures and functions can be powerful security tools or vectors. 

**Definer vs invoker permissions** : By default, functions execute with the privileges of their owner (`SECURITY DEFINER`). This allows controlled privilege escalation: 

CREATE OR REPLACE FUNCTION get_user_email(user_id INTEGER)

RETURNS TEXT

SECURITY DEFINER

SET search_path = public

AS $$

SELECT email FROM users WHERE id = user_id;

$$ LANGUAGE sql;

REVOKE ALL ON FUNCTION get_user_email FROM public;

GRANT EXECUTE ON FUNCTION get_user_email TO app_readonly;

Note the `SET search_path = public`. Without this, a `SECURITY DEFINER` function can be hijacked by temporarily altering `search_path` to load a malicious table named `users` in a different schema. 

**SQL injection** inside dynamic SQL within a procedure is a real risk. Always use `EXECUTE ... USING` for parameterized execution: 

CREATE FUNCTION search_products(query TEXT)

RETURNS SETOF products AS $$

BEGIN

RETURN QUERY EXECUTE

'SELECT * FROM products WHERE name ILIKE $1'

USING '%' || query || '%';

END;

$$ LANGUAGE plpgsql;

Testing 

Database code deserves the same testing rigor as application code. The `db-tests` or `pgtap` framework enables unit tests: 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- pgtap example

SELECT plan(3);

SELECT is(calculate_discount(1, 100.00), 20.00,

'Gold member gets 20% discount');

SELECT is(calculate_discount(2, 100.00), 10.00,

'Silver member gets 10% discount');

SELECT is(calculate_discount(3, 100.00), 0.00,

'Regular member gets no discount');

SELECT * FROM finish();

When to Use Stored Procedures 

Favor procedures when: 

  * The operation spans multiple SQL statements requiring transaction control.

  * Data validation rules are best expressed close to the data.

  * You need consistent enforcement of business logic across multiple applications.

  * Network round trips must be minimized.




Favor application code when: 

  * The logic involves complex control flow across external services.

  * You need to version business logic independently of the database.

  * Testing frameworks are more mature in the application language.

  * The database CPU is already a bottleneck.




A balanced architecture puts data-integrity rules in the database and complex orchestration in the application layer, using each environment for what it does best.

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes](</en/database/full-text-search-postgresql.html>), [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>).

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>), [Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes](</en/database/full-text-search-postgresql.html>)

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>), [Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes](</en/database/full-text-search-postgresql.html>)

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>), [Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes](</en/database/full-text-search-postgresql.html>)

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>), [Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes](</en/database/full-text-search-postgresql.html>)

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>), [Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes](</en/database/full-text-search-postgresql.html>)

**See also:** [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>)

**See also:** [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>)

**See also:** [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>)

**See also:** [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>)

**See also:** [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>)

**See also:** [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>)

**See also:** [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>)

**See also:** [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>)

**See also:** [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>)

**See also:** [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>)

**See also:** [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>)

**See also:** [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>)

**See also:** [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>)

**See also:** [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>)

**See also:** [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>)

**See also:** [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>)

**See also:** [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>)

**See also:** [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>)
