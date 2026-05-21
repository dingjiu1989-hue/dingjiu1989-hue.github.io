---
title: "Database Pagination: Offset, Cursor, Keyset, and Seek Methods"
description: "Database pagination strategies compared: OFFSET/LIMIT vs cursor-based pagination for performance and consistency."
date: 2026-04-15
board: database
url: https://dingjiu1989-hue.github.io/en/database/database-pagination-techniques.html
---

# Database Pagination: Offset, Cursor, Keyset, and Seek Methods

Pagination divides large result sets into manageable pages. The choice of pagination method affects query performance, data consistency, and user experience. Different approaches suit different use cases.

## Offset Pagination

OFFSET/LIMIT pagination is the simplest approach. SELECT * FROM orders ORDER BY id LIMIT 20 OFFSET 40 returns page 3 with 20 items per page. It is intuitive and easy to implement.

Problems: OFFSET scans and discards skipped rows—OFFSET 100000 on a query scanning 100k rows still reads all of them. Performance degrades as page number increases. New rows inserted before the current page cause row shifts, and users may see duplicate or missing items.

Offset pagination is acceptable for small datasets (under 10,000 rows) and admin interfaces where exact consistency does not matter. It is not suitable for infinite scroll or real-time feeds.

## Keyset Pagination

Keyset pagination (also called seek method) uses WHERE clauses on the last item's values. SELECT * FROM orders WHERE (created_at, id) > ('2026-01-15T10:30:00', 5000) ORDER BY created_at, id LIMIT 20. It uses a regular index seek.

Advantages: consistent performance regardless of page number. Index scan reads exactly the requested rows. New insertions do not affect previous pages. Fast and stable.

Requirements: the WHERE clause must use a unique combination of columns for unambiguous ordering. Composite index must exist on the pagination columns. Clients must track the last item's sort values.

Keyset pagination is ideal for infinite scroll, real-time feeds, and APIs with stable ordering. Facebook, Twitter, and most modern APIs use cursor-based (keyset) pagination.

## Cursor-Based Pagination

Cursor-based pagination encodes the sort position as an opaque token. The API returns a cursor with each response. Clients pass the cursor for the next request. The server decodes the cursor into WHERE clause values.

Implementation: encode the last row's sort values (base64 JSON or binary). ORM libraries often support cursor pagination natively. GraphQL connections use cursor-based pagination as standard.

Cursor pagination hides pagination details from clients. The cursor can contain not just sort values but also filters, ordering, and version information. Cursor values are opaque—clients cannot manipulate them to access arbitrary pages.

## Comparison

Offset is easiest but breaks at scale. Keyset is fast but requires exposing sort columns to client logic. Cursor offers the best API experience but requires more server-side encoding. Offset suits admin UIs and page-number navigation. Keyset and cursor suit API endpoints and infinite scroll.

## Hybrid Approach

Some applications combine methods: cursor for forward pagination (infinite scroll), offset for backward pagination (page number jumps). The API returns both next_cursor and page_number in responses, letting the client choose.

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Database Migration Strategies](</en/database/database-migration-strategies.html>), [Database Scalability](</en/database/database-scalability.html>).

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance](</en/database/database-design-patterns.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance](</en/database/database-design-patterns.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance](</en/database/database-design-patterns.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance](</en/database/database-design-patterns.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance](</en/database/database-design-patterns.html>)

**See also:** [Database Triggers: Use Cases, Performance Costs, and Alternatives](</en/database/triggers-patterns.html>), [Database Scalability](</en/database/database-scalability.html>), [Materialized Views](</en/database/materialized-views.html>)

**See also:** [Database Triggers: Use Cases, Performance Costs, and Alternatives](</en/database/triggers-patterns.html>), [Database Scalability](</en/database/database-scalability.html>), [Materialized Views](</en/database/materialized-views.html>)

**See also:** [Database Triggers: Use Cases, Performance Costs, and Alternatives](</en/database/triggers-patterns.html>), [Database Scalability](</en/database/database-scalability.html>), [Materialized Views](</en/database/materialized-views.html>)

**See also:** [Database Triggers: Use Cases, Performance Costs, and Alternatives](</en/database/triggers-patterns.html>), [Database Scalability](</en/database/database-scalability.html>), [Materialized Views](</en/database/materialized-views.html>)

**See also:** [Database Triggers: Use Cases, Performance Costs, and Alternatives](</en/database/triggers-patterns.html>), [Database Scalability](</en/database/database-scalability.html>), [Materialized Views](</en/database/materialized-views.html>)

**See also:** [Database Triggers: Use Cases, Performance Costs, and Alternatives](</en/database/triggers-patterns.html>), [Database Scalability](</en/database/database-scalability.html>), [Materialized Views](</en/database/materialized-views.html>)

**See also:** [Database Triggers: Use Cases, Performance Costs, and Alternatives](</en/database/triggers-patterns.html>), [Database Scalability](</en/database/database-scalability.html>), [Materialized Views](</en/database/materialized-views.html>)

**See also:** [Database Triggers: Use Cases, Performance Costs, and Alternatives](</en/database/triggers-patterns.html>), [Database Scalability](</en/database/database-scalability.html>), [Materialized Views](</en/database/materialized-views.html>)

**See also:** [Database Triggers: Use Cases, Performance Costs, and Alternatives](</en/database/triggers-patterns.html>), [Database Scalability](</en/database/database-scalability.html>), [Materialized Views](</en/database/materialized-views.html>)

**See also:** [Database Triggers: Use Cases, Performance Costs, and Alternatives](</en/database/triggers-patterns.html>), [Database Scalability](</en/database/database-scalability.html>), [Materialized Views](</en/database/materialized-views.html>)

**See also:** [Database Triggers: Use Cases, Performance Costs, and Alternatives](</en/database/triggers-patterns.html>), [Database Scalability](</en/database/database-scalability.html>), [Materialized Views](</en/database/materialized-views.html>)

**See also:** [Database Triggers: Use Cases, Performance Costs, and Alternatives](</en/database/triggers-patterns.html>), [Database Scalability](</en/database/database-scalability.html>), [Materialized Views](</en/database/materialized-views.html>)

**See also:** [Database Triggers: Use Cases, Performance Costs, and Alternatives](</en/database/triggers-patterns.html>), [Database Scalability](</en/database/database-scalability.html>), [Materialized Views](</en/database/materialized-views.html>)
