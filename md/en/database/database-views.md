---
title: "Database Views: Simple, Materialized, and Updateable Views"
description: "Learn about database views including simple views, materialized views, updateable views, and the performance trade-offs between them in PostgreSQL."
date: 2026-04-05
board: database
url: https://aidev.fit/en/database/database-views.html
---

# Database Views: Simple, Materialized, and Updateable Views

Database Views: Simple, Materialized, and Updateable Views 

A database view is a stored query that behaves like a virtual table. Views abstract complexity, enforce security, and provide a stable API over changing schemas. PostgreSQL supports three categories: simple views, materialized views, and updateable views. 

Simple (Virtual) Views 

A simple view does not store data; it runs the underlying query each time it is referenced. Think of it as a saved `SELECT` statement. 

CREATE VIEW active_users AS

SELECT u.id, u.email, u.created_at,

COUNT(o.id) AS order_count,

COALESCE(SUM(o.total), 0) AS lifetime_value

FROM users u

LEFT JOIN orders o ON o.user_id = u.id

WHERE u.deleted_at IS NULL

GROUP BY u.id, u.email, u.created_at;

Querying the view is identical to querying a table: 

SELECT * FROM active_users WHERE lifetime_value > 1000 ORDER BY lifetime_value DESC;

The planner inlines the view definition into the outer query, so the optimizer can push filters and joins into the underlying scans. A simple view adds almost zero overhead. 

Use cases for simple views: 

  * **Row-level security** : Expose only specific columns or filtered rows to certain roles.

  * **Schema abstraction** : Rename or restructure columns without breaking client applications.

  * **Reusable joins** : Encapsulate multi-table aggregations that are queried frequently.




Materialized Views 

A materialized view physically stores the result set. Queries against it are fast because they read pre-computed data rather than executing the full query. 

CREATE MATERIALIZED VIEW daily_sales_summary AS

SELECT DATE(o.order_date) AS day,

p.category,

COUNT(*) AS order_count,

SUM(oi.quantity * oi.unit_price) AS revenue

FROM orders o

JOIN order_items oi ON oi.order_id = o.id

JOIN products p ON p.id = oi.product_id

GROUP BY DATE(o.order_date), p.category

WITH DATA;

The materialized view must be refreshed to reflect new data: 

REFRESH MATERIALIZED VIEW daily_sales_summary;

In PostgreSQL, `REFRESH MATERIALIZED VIEW` takes an `ACCESS EXCLUSIVE` lock, blocking concurrent reads. The `CONCURRENTLY` option avoids this but requires a unique index: 

CREATE UNIQUE INDEX ON daily_sales_summary (day, category);

REFRESH MATERIALIZED VIEW CONCURRENTLY daily_sales_summary;

Materialized views shine when: 

  * The underlying query aggregates millions of rows and runs for seconds or minutes.

  * Slightly stale data (minutes or hours) is acceptable.

  * The result set is small enough to be stored efficiently.




The trade-off is staleness. Between refreshes, queries see snapshots that may differ from the base tables. Design your refresh schedule around business tolerance for latency. 

Updateable Views 

PostgreSQL automatically makes simple views updateable if they meet certain conditions. The view must reference exactly one table (or a single-table `UNION ALL` in some cases), include the primary key, and exclude aggregates, window functions, and `DISTINCT`. 

CREATE VIEW active_orders AS

SELECT id, user_id, total, status, order_date

FROM orders

WHERE deleted_at IS NULL;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- This INSERT works because the view is updateable

INSERT INTO active_orders (user_id, total, status, order_date)

VALUES (42, 99.99, 'pending', CURRENT_DATE);

For complex views that are not automatically updateable, you can use `INSTEAD OF` triggers: 

CREATE VIEW order_summary AS

SELECT o.id, o.user_id, o.total,

COALESCE(AVG(oi.unit_price), 0) AS avg_item_price

FROM orders o

JOIN order_items oi ON oi.order_id = o.id

GROUP BY o.id, o.user_id, o.total;

CREATE OR REPLACE FUNCTION insert_order_summary()

RETURNS TRIGGER AS $$

BEGIN

INSERT INTO orders (id, user_id, total)

VALUES (NEW.id, NEW.user_id, NEW.total);

RETURN NEW;

END;

$$ LANGUAGE plpgsql;

CREATE TRIGGER instead_of_insert

INSTEAD OF INSERT ON order_summary

FOR EACH ROW EXECUTE FUNCTION insert_order_summary();

Performance Trade-offs 

| Aspect | Simple View | Materialized View | |--------|-------------|-------------------| | Storage | None | Full result set | | Query speed | Depends on base query | Fast (pre-computed) | | Data freshness | Real-time | Stale until refresh | | Write overhead | None | Refresh cost | | Indexed columns | Base table indexes | Materialized view indexes | 

View Security 

Views are a powerful security tool. You can grant `SELECT` on a view without granting access to the underlying tables: 

REVOKE ALL ON users FROM app_readonly;

GRANT SELECT ON active_users TO app_readonly;

With `security_barrier` views, PostgreSQL prevents leaky predicate pushdowns that could expose hidden rows: 

CREATE VIEW secure_employees WITH (security_barrier) AS

SELECT * FROM employees WHERE active = true;

Choose wisely between simple and materialized views. Simple views suit OLTP workloads where freshness matters. Materialized views fit analytical dashboards, reporting, and any query where millisecond latency justifies a few minutes of staleness.
