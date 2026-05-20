---
title: "SQL Query Optimization"
description: "Master SQL query optimization with EXPLAIN plans, indexing strategies, JOIN optimization, and common performance anti-patterns."
date: 2025-12-24
board: database
url: https://dingjiu1989-hue.github.io/en/database/sql-query-optimization.html
---

# SQL Query Optimization

Why Query Optimization Matters 

A poorly written query can take seconds or minutes instead of milliseconds, consuming database resources and degrading the experience for all users. Optimizing queries is often the highest-ROI performance improvement you can make because it requires no infrastructure changes. 

Understanding EXPLAIN 

Every database has a query planner that decides how to execute your SQL. EXPLAIN shows you the plan. 

EXPLAIN ANALYZE

SELECT u.name, COUNT(o.id) AS order_count

FROM users u

LEFT JOIN orders o ON u.id = o.user_id

WHERE u.created_at > '2026-01-01'

GROUP BY u.id, u.name

HAVING COUNT(o.id) > 5;

Output analysis: 

Hash Join (cost=125.4..892.1 rows=342 width=72)

Hash Cond: (u.id = o.user_id)

-> Seq Scan on users u (cost=0.0..423.1 rows=1250 width=36)

Filter: (created_at > '2026-01-01')

-> Hash (cost=89.2..89.2 rows=2892 width=8)

-> Seq Scan on orders o (cost=0.0..89.2 rows=2892 width=8)

Key metrics to watch: 

| Metric | What It Means | Good | Bad | |--------|---------------|------|-----| | `cost` | Estimated cost (arbitrary units) | Low | High | | `rows` | Estimated rows returned | Accurate | Off by 10x+ | | `actual time` | Actual execution time | ms | seconds | | `Seq Scan` | Full table scan | Small tables | Large tables | | `Sort` | Explicit sort operation | Sorted data | Large sorts to disk | 

Indexing for Query Performance 

Covering Indexes 

An index that contains all columns needed by a query, enabling index-only scans: 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Query needs: id, email, status, created_at

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Instead of:

CREATE INDEX idx_users_status ON users(status);

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Create a covering index:

CREATE INDEX idx_users_status_covering

ON users(status) INCLUDE (email, created_at);

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Now this query uses an index-only scan:

SELECT email, created_at

FROM users

WHERE status = 'active'

ORDER BY created_at DESC;

JOIN Optimization 

Nested Loop vs Hash Join vs Merge Join 

| Join Type | When It Is Used | Best For | |-----------|-----------------|----------| | Nested Loop | One table is small, other is indexed | Small result sets | | Hash Join | No useful index, medium tables | Unindexed joins | | Merge Join | Both tables sorted on join key | Large sorted datasets | 

Optimizing JOINs 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- INEFFICIENT: Joining without indexes

SELECT *

FROM orders o

JOIN customers c ON o.customer_id = c.id

WHERE c.country = 'US';

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Add index on the join column

CREATE INDEX idx_orders_customer ON orders(customer_id);

CREATE INDEX idx_customers_country ON customers(country);

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Now the planner can use indexes effectively

Subquery vs CTE vs JOIN 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Option 1: Subquery

SELECT name, (SELECT COUNT(*) FROM orders WHERE user_id = users.id) AS order_count

FROM users;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Option 2: Lateral join (often fastest)

SELECT u.name, sq.order_count

FROM users u

LEFT JOIN LATERAL (

SELECT COUNT(*) AS order_count

FROM orders

WHERE user_id = u.id

) sq ON true;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Option 3: Regular JOIN + GROUP BY

SELECT u.name, COUNT(o.id) AS order_count

FROM users u

LEFT JOIN orders o ON u.id = o.user_id

GROUP BY u.id, u.name;

For correlated subqueries, LATERAL joins are often the best choice because they can use indexes efficiently. 

Avoiding Common Anti-Patterns 

SELECT * (Especially with JOINs) 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- BAD: Selects all columns, may force heap lookups

SELECT * FROM users

JOIN orders ON users.id = orders.user_id;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- GOOD: Select only needed columns

SELECT users.name, orders.total

FROM users

JOIN orders ON users.id = orders.user_id;

Functions on Indexed Columns 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- BAD: Function prevents index use

SELECT * FROM users

WHERE LOWER(email) = 'alice@example.com';

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- GOOD: Use a proper case-insensitive index or column

CREATE INDEX idx_users_email_lower ON users(LOWER(email));

SELECT * FROM users WHERE LOWER(email) = 'alice@example.com';

Implicit Type Conversion 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- BAD: Type conversion prevents index use

SELECT * FROM orders

WHERE order_date = '2026-05-11'; -- text vs date

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- GOOD: Explicit cast

SELECT * FROM orders

WHERE order_date = DATE '2026-05-11';

Pagination with OFFSET 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- BAD: OFFSET re-scans skipped rows

SELECT * FROM orders ORDER BY id LIMIT 20 OFFSET 10000;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- GOOD: Keyset pagination (seek method)

SELECT * FROM orders

WHERE id > 10000

ORDER BY id

LIMIT 20;

Query Rewriting Examples 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- BEFORE (Slow - 12s)

SELECT p.*,

(SELECT COUNT(*) FROM reviews r WHERE r.product_id = p.id AND r.rating >= 4) AS good_reviews

FROM products p

WHERE p.category_id = 5;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- AFTER (Fast - 0.3s)

SELECT p.*, COALESCE(gr.count, 0) AS good_reviews

FROM products p

LEFT JOIN (

SELECT product_id, COUNT(*) AS count

FROM reviews

WHERE rating >= 4

GROUP BY product_id

) gr ON p.id = gr.product_id

WHERE p.category_id = 5;

Performance Budgets 

| Query Type | Target Latency | Max Rows Returned | |------------|---------------|-------------------| | Simple lookup (by PK) | < 5ms | 1 | | List with filter | < 50ms | 100 | | Report/aggregation | < 500ms | 10000 | | Dashboard | < 2s | 1000 | | Batch/ETL | < 30min | Unlimited | 

Summary 

SQL query optimization starts with understanding the query plan through EXPLAIN ANALYZE. Ensure appropriate indexes exist for your query patterns, prefer covering indexes for index-only scans, avoid functions on indexed columns, replace OFFSET pagination with keyset pagination, and rewrite correlated subqueries as joins or lateral joins. Measure before and after each optimization to confirm the improvement.

**See also:** [OLTP vs OLAP: Workload Optimization](</en/database/oltp-vs-olap.html>), [Query Performance Tuning Tools](</en/database/query-performance-tuning.html>), [Database Indexing Strategies](</en/database/database-indexing.html>).

**See also:** [PostgreSQL Query Optimization: From 2 Seconds to 2 Milliseconds](</en/tech/postgresql-query-optimization.html>), [OLTP vs OLAP: Workload Optimization](</en/database/oltp-vs-olap.html>), [Query Performance Tuning Tools](</en/database/query-performance-tuning.html>)

**See also:** [PostgreSQL Query Optimization: From 2 Seconds to 2 Milliseconds](</en/tech/postgresql-query-optimization.html>), [OLTP vs OLAP: Workload Optimization](</en/database/oltp-vs-olap.html>), [Query Performance Tuning Tools](</en/database/query-performance-tuning.html>)

**See also:** [PostgreSQL Query Optimization: From 2 Seconds to 2 Milliseconds](</en/tech/postgresql-query-optimization.html>), [OLTP vs OLAP: Workload Optimization](</en/database/oltp-vs-olap.html>), [Query Performance Tuning Tools](</en/database/query-performance-tuning.html>)

**See also:** [PostgreSQL Query Optimization: From 2 Seconds to 2 Milliseconds](</en/tech/postgresql-query-optimization.html>), [OLTP vs OLAP: Workload Optimization](</en/database/oltp-vs-olap.html>), [Query Performance Tuning Tools](</en/database/query-performance-tuning.html>)

**See also:** [PostgreSQL Query Optimization: From 2 Seconds to 2 Milliseconds](</en/tech/postgresql-query-optimization.html>), [OLTP vs OLAP: Workload Optimization](</en/database/oltp-vs-olap.html>), [Query Performance Tuning Tools](</en/database/query-performance-tuning.html>)

**See also:** [Slow Query Optimization: Analysis, Indexing, and Rewriting](</en/database/database-slow-query-optimization.html>), [Connection Pooling Guide](</en/database/connection-pooling.html>), [Columnar Databases: When and How to Use Them](</en/database/columnar-databases.html>)

**See also:** [Slow Query Optimization: Analysis, Indexing, and Rewriting](</en/database/database-slow-query-optimization.html>), [Connection Pooling Guide](</en/database/connection-pooling.html>), [Columnar Databases: When and How to Use Them](</en/database/columnar-databases.html>)

**See also:** [Slow Query Optimization: Analysis, Indexing, and Rewriting](</en/database/database-slow-query-optimization.html>), [Connection Pooling Guide](</en/database/connection-pooling.html>), [Columnar Databases: When and How to Use Them](</en/database/columnar-databases.html>)

**See also:** [Slow Query Optimization: Analysis, Indexing, and Rewriting](</en/database/database-slow-query-optimization.html>), [Connection Pooling Guide](</en/database/connection-pooling.html>), [Columnar Databases: When and How to Use Them](</en/database/columnar-databases.html>)

**See also:** [Slow Query Optimization: Analysis, Indexing, and Rewriting](</en/database/database-slow-query-optimization.html>), [Connection Pooling Guide](</en/database/connection-pooling.html>), [Columnar Databases: When and How to Use Them](</en/database/columnar-databases.html>)

**See also:** [Slow Query Optimization: Analysis, Indexing, and Rewriting](</en/database/database-slow-query-optimization.html>), [Connection Pooling Guide](</en/database/connection-pooling.html>), [Columnar Databases: When and How to Use Them](</en/database/columnar-databases.html>)

**See also:** [Slow Query Optimization: Analysis, Indexing, and Rewriting](</en/database/database-slow-query-optimization.html>), [Connection Pooling Guide](</en/database/connection-pooling.html>), [Columnar Databases: When and How to Use Them](</en/database/columnar-databases.html>)

**See also:** [Slow Query Optimization: Analysis, Indexing, and Rewriting](</en/database/database-slow-query-optimization.html>), [Connection Pooling Guide](</en/database/connection-pooling.html>), [Columnar Databases: When and How to Use Them](</en/database/columnar-databases.html>)
