---
title: "Query Parameterization: Bind Parameters, Prepared Statements, and SQL Injection"
description: "Learn query parameterization in PostgreSQL: bind parameters, prepared statements, plan caching, and protection against SQL injection attacks."
date: 2026-04-08
board: database
url: https://dingjiu1989-hue.github.io/en/database/query-parameters.html
---

# Query Parameterization: Bind Parameters, Prepared Statements, and SQL Injection

Query Parameterization: Bind Parameters, Prepared Statements, and SQL Injection 

Parameterized queries are simultaneously the most important security practice and a significant performance optimization. This article explains how bind parameters work, how PostgreSQL caches query plans, and why parameterization is non-negotiable. 

SQL Injection: The Problem 

Without parameterization, user input is concatenated into SQL strings: 

## DANGEROUS: Never do this

user_id = request.args.get("id")

cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

An attacker provides `1; DROP TABLE users;` as the `id` parameter, and the query becomes: 

SELECT * FROM users WHERE id = 1; DROP TABLE users;

Parameterization prevents this by separating SQL code from data: 

## SAFE: Use parameterized query

cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

The database receives the SQL structure and the parameter values separately. The parameter value `1; DROP TABLE users;` is treated as a literal string, not executable SQL. 

Bind Parameters 

PostgreSQL supports two parameter syntaxes depending on the driver: 

**psycopg2** (`%s`): 

cursor.execute(

"INSERT INTO users (email, name, age) VALUES (%s, %s, %s)",

("alice@example.com", "Alice", 30)

)

**asyncpg** (`$1`, `$2`): 

await conn.execute(

"INSERT INTO users (email, name, age) VALUES ($1, $2, $3)",

"alice@example.com", "Alice", 30

)

**JDBC** (`?`): 

PreparedStatement stmt = conn.prepareStatement(

"SELECT * FROM users WHERE email = ?"

);

stmt.setString(1, "alice@example.com");

ResultSet rs = stmt.executeQuery();

Prepared Statements 

PostgreSQL separates prepared statements into two phases: 

  * **PREPARE** : The database parses, analyzes, and plans the query.



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **EXECUTE** : The database runs the plan with specific parameter values. 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Explicit prepared statement

PREPARE find_user(INTEGER) AS

SELECT * FROM users WHERE id = $1;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Execute with parameter

EXECUTE find_user(42);

EXECUTE find_user(99);

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Deallocate when done

DEALLOCATE find_user;

Automatic Prepared Statements in Drivers 

Most PostgreSQL drivers implement automatic prepared statement caching: 

import psycopg2

from psycopg2 import pool

## psycopg2 automatically caches prepared statements per connection

conn = psycopg2.connect("dbname=mydb")

cursor = conn.cursor()

## First call: prepares and executes

cursor.execute("SELECT * FROM users WHERE id = %s", (42,))

## Second call: reuses cached prepared statement

cursor.execute("SELECT * FROM users WHERE id = %s", (99,))

Generic Query Plans 

For prepared statements with bind parameters, PostgreSQL generates a **generic plan** after the fifth execution. The generic plan assumes average parameter values rather than specific ones: 

PREPARE search_orders(INTEGER, TEXT) AS

SELECT * FROM orders WHERE user_id = $1 AND status = $2;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- First 5 executions: custom plans

EXECUTE search_orders(42, 'paid');

EXECUTE search_orders(99, 'pending');

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- After 5: switches to generic plan

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- The generic plan might use a hash join where the custom plan used nested loops

Generic plans are more stable but can be suboptimal for skewed data distributions. Use `PLAN_CACHE_MODE` in some drivers or disable generic plans via `SET plan_cache_mode = force_custom_plan`: 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Force custom plans for this prepared statement

SET plan_cache_mode = force_custom_plan;

PREPARE find_vip(INTEGER) AS

SELECT * FROM orders WHERE user_id = $1 AND total > 1000;

Plan Caching 

How prepared statements interact with connection pooling: 

Application → Connection Pool → PostgreSQL

If each application request gets a different pooled connection, prepared statements are not reused across requests. Solutions: 

  * **Application-side caching** : Cache prepared statement text and let the driver prepare on each connection.



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Server-side prepared statements** : Use `PREPARE`/`EXECUTE` explicitly, but manage lifecycle. 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Statement pooling** : PgBouncer with `pool_mode = session` shares the same connection for the same client. 

pg_stat_statements Insights 

CREATE EXTENSION pg_stat_statements;

SELECT query, calls, total_exec_time, rows,

mean_exec_time, stddev_exec_time

FROM pg_stat_statements

WHERE query LIKE '%users%'

ORDER BY total_exec_time DESC

LIMIT 10;

High `stddev_exec_time` on parameterized queries suggests plan instability: the same query performs very differently depending on parameter values. 

Parameterization Beyond SQL Injection 

Parameterization also handles type conversion automatically: 

## Without parameterization: type conversion issues

## f-string produces: ... WHERE created_at = 2026-05-12 (subtraction!)

cursor.execute(f"SELECT * FROM orders WHERE created_at = '{date_string}'")

## With parameterization: driver handles quoting

cursor.execute("SELECT * FROM orders WHERE created_at = %s", (date_obj,))

Best Practices 

Always Parameterize 

## Good

cursor.execute("UPDATE users SET email = %s WHERE id = %s", (new_email, uid))

## Bad: f-string or string concatenation

cursor.execute(f"UPDATE users SET email = '{new_email}' WHERE id = {uid}")

Dynamic IN Clauses 

For variable-length IN clauses, use `ANY(ARRAY[...])`: 

user_ids = [1, 2, 3, 4, 5]

cursor.execute(

"SELECT * FROM users WHERE id = ANY(%s)",

(user_ids,)

)

Or generate positional parameters: 

placeholders = ','.join(['%s'] * len(user_ids))

cursor.execute(

f"SELECT * FROM users WHERE id IN ({placeholders})",

user_ids

)

Batch Execution 

data = [

("alice@example.com", "Alice"),

("bob@example.com", "Bob"),

("carol@example.com", "Carol"),

]

## Uses server-side prepared statement for all rows

psycopg2.extras.execute_values(

cursor,

"INSERT INTO users (email, name) VALUES %s",

data,

template="(%s, %s)"

)

Stored Procedures 

CREATE FUNCTION get_user(p_id INTEGER)

RETURNS users AS $$

SELECT * FROM users WHERE id = p_id;

$$ LANGUAGE sql STABLE;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Call with parameter

SELECT * FROM get_user(42);

Common Mistakes 

  * **Escaping is not parameterization** : `escape_string()` or `quote_ident()` are error-prone. Use bind parameters.



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Dynamic identifiers cannot be parameterized** : Table/column names must be validated separately: `python # Column name cannot be a bind parameter! cursor.execute("SELECT %s FROM users", ("email",)) # Always validate dynamic identifiers against a whitelist allowed_columns = {'email', 'name', 'age'} if column not in allowed_columns: raise ValueError(f"Invalid column: {column}")` 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Stored procedures still need parameterization** : Do not concatenate input inside procedures. 

Parameterization is the single most impactful practice for database security and performance. It is supported by every modern database driver and should be used for every query that includes any data from outside the SQL text.

**See also:** [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>), [Stored Procedures vs Functions: When to Use, Languages, Security](</en/database/stored-procedures.html>), [Database Caching](</en/database/database-caching.html>).

**See also:** [Stored Procedures vs Functions: When to Use, Languages, Security](</en/database/stored-procedures.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>)

**See also:** [Stored Procedures vs Functions: When to Use, Languages, Security](</en/database/stored-procedures.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>)

**See also:** [Stored Procedures vs Functions: When to Use, Languages, Security](</en/database/stored-procedures.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>)

**See also:** [Stored Procedures vs Functions: When to Use, Languages, Security](</en/database/stored-procedures.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>)

**See also:** [Stored Procedures vs Functions: When to Use, Languages, Security](</en/database/stored-procedures.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>)

**See also:** [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>), [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>)

**See also:** [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>), [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>)

**See also:** [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>), [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>)

**See also:** [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>), [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>)

**See also:** [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>), [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>)

**See also:** [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>), [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>)

**See also:** [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>), [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>)
