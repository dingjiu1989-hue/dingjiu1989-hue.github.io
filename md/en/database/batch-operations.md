---
title: "Batch Operations: Bulk Insert, COPY, and Batch Size Tuning"
description: "Master batch operations in PostgreSQL: bulk insert patterns, the COPY command, batch updates, optimal batch sizes, and error handling for large datasets."
date: 2026-03-30
board: database
url: https://aidev.fit/en/database/batch-operations.html
---

# Batch Operations: Bulk Insert, COPY, and Batch Size Tuning

Batch Operations: Bulk Insert, COPY, and Batch Size Tuning 

Loading or updating large volumes of data row-by-row is prohibitively slow. Batch operations reduce overhead by orders of magnitude. This article covers bulk insert techniques, PostgreSQL's COPY command, batch updates, and the art of choosing the right batch size. 

Row-by-Row is Slow 

Inserting one row at a time incurs overhead for each statement: 

  * Parse SQL

  * Plan query

  * Execute plan

  * Commit (if auto-commit)

  * Network round trip




## SLOW: one round trip per row

for row in dataset:

cursor.execute("INSERT INTO users (email, name) VALUES (%s, %s)", row)

For 100,000 rows, that is 100,000 round trips. Batch operations reduce this to one. 

Bulk Insert with Multi-Row VALUES 

The simplest batch insert sends multiple rows in a single statement: 

INSERT INTO users (email, name) VALUES

('alice@example.com', 'Alice'),

('bob@example.com', 'Bob'),

('carol@example.com', 'Carol');

Using psycopg2 execute_values 

from psycopg2.extras import execute_values

data = [

("alice@example.com", "Alice"),

("bob@example.com", "Bob"),

## ... 1000 rows

]

execute_values(

cursor,

"INSERT INTO users (email, name) VALUES %s",

data,

template="(%s, %s)",

page_size=1000

)

Using asyncpg 

import asyncpg

## executemany with prepared statement reuse

await conn.executemany(

"INSERT INTO users (email, name) VALUES ($1, $2)",

[("alice@example.com", "Alice"), ("bob@example.com", "Bob")]

)

The COPY Command 

COPY is PostgreSQL's most efficient data loading mechanism. It streams data in a binary or text format directly into a table, bypassing the SQL layer: 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- From file

COPY users (email, name) FROM '/path/to/users.csv' WITH (FORMAT CSV, HEADER true);

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- From standard input (via driver)

COPY users (email, name) FROM STDIN WITH (FORMAT CSV);

Python with COPY 

import io

import csv

buffer = io.StringIO()

writer = csv.writer(buffer)

writer.writerows([

("alice@example.com", "Alice"),

("bob@example.com", "Bob"),

])

buffer.seek(0)

cursor.copy_expert(

"COPY users (email, name) FROM STDIN WITH CSV",

buffer

)

Performance Comparison 

| Method | Time for 1M rows | Network Rounds | |--------|-----------------|-----------------| | Row-by-row INSERT | ~120 seconds | 1,000,000 | | Batch INSERT (1000 rows) | ~8 seconds | 1,000 | | COPY (binary) | ~1.5 seconds | 1 | | COPY (CSV) | ~2 seconds | 1 | 

Batch Updates 

Updating rows in bulk follows a different pattern. Use a temporary table or unnest: 

Using UNNEST 

UPDATE users SET email = data.email

FROM (SELECT UNNEST(%s) AS id, UNNEST(%s) AS email) AS data

WHERE users.id = data.id;

user_ids = [1, 2, 3, 4, 5]

emails = ["alice@new.com", "bob@new.com", "carol@new.com", "dave@new.com", "eve@new.com"]

cursor.execute("""

UPDATE users SET email = data.email

FROM (SELECT UNNEST(%s::int[]) AS id, UNNEST(%s::text[]) AS email) AS data

WHERE users.id = data.id

""", (user_ids, emails))

Using a Temporary Table 

## Create temp table

cursor.execute("""

CREATE TEMP TABLE tmp_updates (

id INTEGER PRIMARY KEY,

email TEXT,

name TEXT

) ON COMMIT DROP

""")

## COPY into temp table

buffer = io.StringIO()

writer = csv.writer(buffer)

writer.writerows(update_data)

buffer.seek(0)

cursor.copy_expert("COPY tmp_updates FROM STDIN WITH CSV", buffer)

## Join update

cursor.execute("""

UPDATE users u

SET email = t.email, name = t.name

FROM tmp_updates t

WHERE u.id = t.id

""")

Batch Size Tuning 

The optimal batch size depends on row width, network latency, and available memory. 

General Guidelines 

| Row Width | Recommended Batch Size | |-----------|----------------------| | Narrow (few columns) | 1000-5000 | | Medium (10-20 columns) | 500-2000 | | Wide (JSONB, TEXT, many columns) | 100-500 | 

Finding the Sweet Spot 

import time

def benchmark_batch_size(cursor, data, batch_sizes):

for batch_size in batch_sizes:

start = time.time()

for i in range(0, len(data), batch_size):

batch = data[i:i+batch_size]

execute_values(

cursor,

"INSERT INTO users (email, name) VALUES %s",

batch,

page_size=batch_size

)

elapsed = time.time() - start

print(f"Batch size {batch_size}: {elapsed:.2f}s")

Typical results for narrow rows: 

Batch size 100: 3.2s

Batch size 500: 1.8s

Batch size 1000: 1.2s

Batch size 5000: 1.5s # Diminishing returns begin

Batch size 10000: 2.1s # Worse: memory pressure

Error Handling 

All-or-Nothing (Transactional) 

try:

conn = psycopg2.connect(dsn)

cursor = conn.cursor()

execute_values(cursor, "INSERT INTO users (email) VALUES %s", data)

conn.commit()

except Exception as e:

conn.rollback()

print(f"Batch failed: {e}")

Savepoint per Batch 

for i, batch in enumerate(batches):

try:

cursor.execute("SAVEPOINT batch_sp")

execute_values(cursor, "INSERT INTO users (email) VALUES %s", batch)

cursor.execute("RELEASE SAVEPOINT batch_sp")

except Exception as e:

cursor.execute("ROLLBACK TO SAVEPOINT batch_sp")

print(f"Batch {i} failed, skipping: {e}")

ON CONFLICT for Idempotent Loads 

INSERT INTO users (id, email, name) VALUES %s

ON CONFLICT (id) DO UPDATE SET

email = EXCLUDED.email,

name = EXCLUDED.name;

Best Practices 

  * **Use COPY for initial loads** and bulk inserts where latency is acceptable.



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Use batch INSERTs (execute_values)** for operational bulk operations. 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Disable triggers and indexes** temporarily for very large loads, then re-enable: 

ALTER TABLE users SET (autovacuum_enabled = false);

ALTER TABLE users DISABLE TRIGGER ALL;

DROP INDEX idx_users_email;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Perform batch load

CREATE INDEX CONCURRENTLY idx_users_email ON users (email);

ALTER TABLE users ENABLE TRIGGER ALL;

ALTER TABLE users SET (autovacuum_enabled = true);

4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Increase max_wal_size** for large batch operations to avoid excessive checkpoints. 5\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Use UNLOGGED tables** for staging (data lost on crash but much faster): 

CREATE UNLOGGED TABLE staging_users (LIKE users INCLUDING ALL);

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Load into staging, then INSERT INTO users SELECT FROM staging

Batch operations are essential for ETL pipelines, data migrations, and any workflow that moves large volumes of data. Measure your batch sizes, use COPY when possible, and always handle errors gracefully.

**See also:** [PostgreSQL Vacuuming: Maintenance, Tuning, and Automation](</en/database/database-vacuuming-maintenance.html>), [Connection Pooling: Tuning, Best Practices, and Pitfalls](</en/database/database-connection-pooling.html>), [Foreign Key Constraints: Referential Integrity in Practice](</en/database/database-foreign-key-constraints.html>).

**See also:** [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>)

**See also:** [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>)

**See also:** [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>)

**See also:** [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>)

**See also:** [Composite Indexes: Column Order, Covering Indexes, and Partial Indexes](</en/database/composite-indexes.html>), [Index Maintenance: Bloat, Rebuild, Reindex, and Fillfactor Tuning](</en/database/index-maintenance.html>), [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>)

**See also:** [PostgreSQL Vacuuming: Maintenance, Tuning, and Automation](</en/database/database-vacuuming-maintenance.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [PostgreSQL Vacuuming: Maintenance, Tuning, and Automation](</en/database/database-vacuuming-maintenance.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [PostgreSQL Vacuuming: Maintenance, Tuning, and Automation](</en/database/database-vacuuming-maintenance.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [PostgreSQL Vacuuming: Maintenance, Tuning, and Automation](</en/database/database-vacuuming-maintenance.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [PostgreSQL Vacuuming: Maintenance, Tuning, and Automation](</en/database/database-vacuuming-maintenance.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [PostgreSQL Vacuuming: Maintenance, Tuning, and Automation](</en/database/database-vacuuming-maintenance.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [PostgreSQL Vacuuming: Maintenance, Tuning, and Automation](</en/database/database-vacuuming-maintenance.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [PostgreSQL Vacuuming: Maintenance, Tuning, and Automation](</en/database/database-vacuuming-maintenance.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [PostgreSQL Vacuuming: Maintenance, Tuning, and Automation](</en/database/database-vacuuming-maintenance.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [PostgreSQL Vacuuming: Maintenance, Tuning, and Automation](</en/database/database-vacuuming-maintenance.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [PostgreSQL Vacuuming: Maintenance, Tuning, and Automation](</en/database/database-vacuuming-maintenance.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [PostgreSQL Vacuuming: Maintenance, Tuning, and Automation](</en/database/database-vacuuming-maintenance.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [PostgreSQL Vacuuming: Maintenance, Tuning, and Automation](</en/database/database-vacuuming-maintenance.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [PostgreSQL Vacuuming: Maintenance, Tuning, and Automation](</en/database/database-vacuuming-maintenance.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [PostgreSQL Vacuuming: Maintenance, Tuning, and Automation](</en/database/database-vacuuming-maintenance.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [PostgreSQL Vacuuming: Maintenance, Tuning, and Automation](</en/database/database-vacuuming-maintenance.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [PostgreSQL Vacuuming: Maintenance, Tuning, and Automation](</en/database/database-vacuuming-maintenance.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)

**See also:** [PostgreSQL Vacuuming: Maintenance, Tuning, and Automation](</en/database/database-vacuuming-maintenance.html>), [Change Data Capture (CDC): Debezium, Logical Replication, and Stream Processing](</en/database/change-data-capture.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>)
