---
title: "JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations"
description: "Comprehensive guide to using JSON in PostgreSQL. Compare JSONB and JSON types, indexing strategies, query operators, and when to choose PostgreSQL over MongoDB."
date: 2026-04-08
board: database
url: https://dingjiu1989-hue.github.io/en/database/json-in-postgresql.html
---

# JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations

JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations 

PostgreSQL's JSON support has matured into a powerful feature set. The `jsonb` type combined with GIN indexes makes PostgreSQL a competitive document database while retaining all relational capabilities. This article covers the types, operators, indexes, and when JSON in PostgreSQL is the right choice. 

JSON vs JSONB 

PostgreSQL offers two JSON data types: 

| Aspect | `json` | `jsonb` | |--------|--------|---------| | Storage | Exact copy of input text | Decomposed binary format | | Duplicate keys | Preserved | Last key wins | | Whitespace | Preserved | Removed | | Key ordering | Preserved | Not preserved | | Indexing | Function-based only | GIN indexes supported | | Parsing overhead | On each access | On insert only | 

**Always use`jsonb`** for new projects unless you have a specific need for `json` (such as preserving duplicate keys exactly as input). 

CREATE TABLE products (

id BIGSERIAL PRIMARY KEY,

name TEXT NOT NULL,

attributes JSONB NOT NULL DEFAULT '{}'

);

INSERT INTO products (name, attributes) VALUES

('Widget', '{"color": "red", "weight": 1.5, "tags": ["sale", "new"]}'),

('Gadget', '{"color": "blue", "dimensions": {"width": 10, "height": 5}}');

Query Operators 

PostgreSQL provides a rich set of JSONB operators: 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- -> returns JSONB (preserves types)

SELECT attributes -> 'color' FROM products; -- "red" (jsonb)

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- ->> returns TEXT

SELECT attributes ->> 'color' FROM products; -- red (text)

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Path access

SELECT attributes #> '{dimensions, width}' FROM products;

SELECT attributes #>> '{dimensions, width}' FROM products;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Containment check

SELECT * FROM products WHERE attributes @> '{"color": "red"}';

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Key existence

SELECT * FROM products WHERE attributes ? 'dimensions';

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Multiple key existence

SELECT * FROM products WHERE attributes ?| ARRAY['color', 'size'];

SELECT * FROM products WHERE attributes ?& ARRAY['color', 'weight'];

Indexing JSONB 

GIN Index 

The default GIN index supports containment (`@>`), key existence (`?`), and key/element existence (`?|`, `?&`): 

CREATE INDEX idx_products_attributes ON products USING GIN (attributes);

GIN with jsonb_path_ops 

The `jsonb_path_ops` operator class creates a more focused index that is faster for containment queries: 

CREATE INDEX idx_products_attributes_path ON products

USING GIN (attributes jsonb_path_ops);

The `jsonb_path_ops` index is typically 1/3 the size of the default GIN index and 2-3x faster for `@>` queries. However, it does not support `?`, `?|`, or `?&` operators. 

B-tree Index for JSONB Fields 

For equality and range queries on specific JSONB fields, use a B-tree index on an expression: 

CREATE INDEX idx_products_color ON products ((attributes ->> 'color'));

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Now this query uses the index:

SELECT * FROM products WHERE attributes ->> 'color' = 'red';

Partial Index for Specific JSON Structures 

CREATE INDEX idx_products_sale ON products ((attributes ->> 'price'))

WHERE attributes @> '{"sale": true}';

JSONB Modification Functions 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Add or update a key

UPDATE products

SET attributes = jsonb_set(attributes, '{stock}', '42')

WHERE id = 1;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Remove a key

UPDATE products

SET attributes = attributes - 'temporary_flag'

WHERE id = 1;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Concatenate (merge) JSONB

UPDATE products

SET attributes = attributes || '{"on_sale": true, "discount_pct": 15}'

WHERE id = 1;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Delete from array

UPDATE products

SET attributes = attributes #- '{tags, 0}'

WHERE id = 1;

JSONB in Queries with Relational Data 

The real power of JSONB in PostgreSQL is combining document flexibility with relational integrity: 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Join JSONB data with relational tables

SELECT p.name,

p.attributes ->> 'color' AS color,

o.order_date,

o.quantity

FROM products p

JOIN orders o ON o.product_id = p.id

WHERE p.attributes @> '{"color": "red"}'

AND o.order_date > '2026-01-01';

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Aggregate JSONB data per category

SELECT category,

jsonb_agg(attributes ORDER BY name) AS product_attrs

FROM products

GROUP BY category;

PostgreSQL vs MongoDB 

When does PostgreSQL's JSONB make sense as a MongoDB alternative? 

| Capability | PostgreSQL JSONB | MongoDB | |------------|-----------------|---------| | Schema enforcement | Optional (CHECK constraints) | Optional (schema validation) | | Joins | Full SQL JOIN support | $lookup (limited) | | Transactions | ACID, multi-document | Multi-document (since 4.0) | | Index types | B-tree, GIN, GiST, BRIN | B-tree, compound, text, geospatial | | Aggregation | SQL + JSONB functions | Aggregation pipeline | | Horizontal scaling | Read replicas, sharding (Citus) | Native sharding | | Geospatial | PostGIS (very mature) | Built-in 2dsphere | 

Choose PostgreSQL with JSONB when you need: 

  * A mix of relational and document data with referential integrity.

  * Complex joins and aggregations across structured and semi-structured data.

  * ACID guarantees with JSON document consistency.

  * Familiar SQL tooling and ORM integration.




Choose MongoDB when you need: 

  * Native horizontal sharding out of the box.

  * Deeply nested, varied document structures across collections.

  * A document-first data model without relational baggage.




Best Practices 

  * **Always use`jsonb`**, not `json`, unless you have a specific reason.

  * **Add CHECK constraints** to validate JSON structure when possible:




ALTER TABLE products ADD CONSTRAINT valid_attributes

CHECK (jsonb_typeof(attributes -> 'price') = 'number');

  * **Combine JSONB with regular columns** : Use relational columns for primary keys, timestamps, and foreign keys. Use JSONB for variable or extensible attributes.

  * **Benchmark GIN indexes** : The default GIN index covers more operators. The `jsonb_path_ops` variant is faster for containment but less flexible.

  * **Avoid JSONB for everything** : If your "attributes" are always queried with equality or range conditions, use regular columns with proper types. JSONB is best for truly variable schemas.




PostgreSQL's JSONB support bridges the gap between relational and document databases. Used wisely, it eliminates the need for a separate document store in many applications.

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Document Databases: MongoDB, CouchDB, Firestore](</en/database/document-databases.html>).

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>)

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>)

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>)

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>)

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>)

**See also:** [Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes](</en/database/full-text-search-postgresql.html>), [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>), [Stored Procedures vs Functions: When to Use, Languages, Security](</en/database/stored-procedures.html>)

**See also:** [Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes](</en/database/full-text-search-postgresql.html>), [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>), [Stored Procedures vs Functions: When to Use, Languages, Security](</en/database/stored-procedures.html>)

**See also:** [Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes](</en/database/full-text-search-postgresql.html>), [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>), [Stored Procedures vs Functions: When to Use, Languages, Security](</en/database/stored-procedures.html>)

**See also:** [Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes](</en/database/full-text-search-postgresql.html>), [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>), [Stored Procedures vs Functions: When to Use, Languages, Security](</en/database/stored-procedures.html>)

**See also:** [Full-Text Search in PostgreSQL: tsvector, tsquery, GIN Indexes](</en/database/full-text-search-postgresql.html>), [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>), [Stored Procedures vs Functions: When to Use, Languages, Security](</en/database/stored-procedures.html>)
