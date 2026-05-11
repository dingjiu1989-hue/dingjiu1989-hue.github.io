---
title: "Database Normalization Explained"
description: "Learn database normalization from 1NF to 5NF with practical examples, denormalization trade-offs, and real-world schema design."
date: 2026-05-11
board: database
url: https://dingjiu1989-hue.github.io/en/database/database-normalization.html
---

## What Is Normalization?

Normalization is the process of organizing data in a database to reduce redundancy and improve data integrity. It involves dividing large tables into smaller, related tables and defining relationships between them. The goal is to ensure that each piece of data is stored in exactly one place.

## The Problem Normalization Solves

Consider an unnormalized table:

| OrderID | Customer | Address | Product | Price |
|---------|----------|---------|---------|-------|
| 1 | Alice | 123 Main St | Laptop | 1200 |
| 2 | Alice | 123 Main St | Mouse | 25 |
| 3 | Bob | 456 Oak Ave | Laptop | 1200 |

Problems:
- **Update anomaly**: If Alice moves, you must update multiple rows.
- **Insert anomaly**: Cannot add a new customer without an order.
- **Delete anomaly**: Deleting Bob's order removes all knowledge of Bob.

## Normal Forms

### First Normal Form (1NF)

Each column contains atomic (indivisible) values, and each row is unique.

| Violation | Corrected |
|-----------|-----------|
| Products: "Laptop, Mouse, Keyboard" | One product per row |
| Phone: "555-0100, 555-0200" | Separate rows for each phone |

```sql
-- Violates 1NF
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    product_names TEXT  -- "Laptop,Mouse,Keyboard"
);

-- 1NF compliant
CREATE TABLE order_items (
    order_id INTEGER REFERENCES orders(id),
    product_name TEXT,
    PRIMARY KEY (order_id, product_name)
);
```

### Second Normal Form (2NF)

Must be in 1NF, and all non-key columns must depend on the entire primary key (not just part of it).

```sql
-- Violates 2NF (composite PK: order_id, product_id)
CREATE TABLE order_details (
    order_id INTEGER,
    product_id INTEGER,
    product_name TEXT,     -- Depends only on product_id, not on order_id
    product_price DECIMAL, -- Depends only on product_id, not on order_id
    quantity INTEGER,      -- Depends on full PK
    PRIMARY KEY (order_id, product_id)
);

-- 2NF compliant
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL NOT NULL
);

CREATE TABLE order_items (
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    PRIMARY KEY (order_id, product_id)
);
```

### Third Normal Form (3NF)

Must be in 2NF, and no transitive dependencies (non-key columns must not depend on other non-key columns).

```sql
-- Violates 3NF
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    customer_name TEXT,     -- Depends on customer_id, not on order_id
    customer_email TEXT,    -- Depends on customer_id, not on order_id
    order_date DATE
);

-- 3NF compliant
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    order_date DATE NOT NULL
);
```

### Boyce-Codd Normal Form (BCNF)

A stricter version of 3NF where every determinant must be a candidate key.

```sql
-- Violates BCNF
-- Each student has one major, each professor teaches one course,
-- but a professor can teach different courses in different majors
CREATE TABLE enrollment (
    student_id INTEGER,
    major TEXT,
    professor TEXT,
    course TEXT,
    PRIMARY KEY (student_id, course)
    -- professor -> course (professor determines course, but is not a key)
);

-- BCNF compliant: split into multiple tables
CREATE TABLE student_major (student_id INTEGER, major TEXT);
CREATE TABLE professor_course (professor TEXT, course TEXT);
CREATE TABLE enrollment (student_id INTEGER, professor TEXT, PRIMARY KEY (student_id, professor));
```

## Normal Forms Comparison

| Normal Form | Rule | Violation Example |
|-------------|------|-------------------|
| 1NF | Atomic values | Multiple values in one column |
| 2NF | Full PK dependency | Column depends on part of composite PK |
| 3NF | No transitive dependency | Column depends on non-key column |
| BCNF | Every determinant is a key | Column determines another non-key column |
| 4NF | No multi-valued dependencies | Independent 1:N relationships in same table |
| 5NF | Join dependencies | Cannot reconstruct from smaller tables |

## Denormalization: When to Break the Rules

Normalization is not always the best choice. Denormalization trades storage and update complexity for read performance.

### When to Denormalize

1. **Reporting and analytics**: Pre-joined tables for dashboards.
2. **High-read, low-write workloads**: Blog posts, product catalogs.
3. **Distributed databases**: Avoiding JOINs across shards.
4. **Caching computed values**: Order totals, comment counts.

```sql
-- Denormalized for read performance
CREATE TABLE products_with_category (
    id SERIAL PRIMARY KEY,
    name TEXT,
    price DECIMAL,
    category_name TEXT,         -- Denormalized from categories table
    category_slug TEXT,         -- Denormalized from categories table
    review_count INTEGER,       -- Cached aggregate
    avg_rating DECIMAL          -- Cached aggregate
);
```

## Normalization in Practice

Most production databases aim for 3NF in transactional systems and selectively denormalize for performance. The common approach:

1. Design in 3NF.
2. Profile performance with real queries.
3. Denormalize specific tables or add computed columns when queries are too slow.
4. Document all denormalization decisions and their rationale.

## Summary

Normalization eliminates data redundancy and protects data integrity by enforcing single-truth storage. Aim for 3NF in transactional databases, ensure every non-key column depends on the key, the whole key, and nothing but the key. Denormalize selectively for read-heavy workloads, reporting, and distributed architectures, always documenting the trade-off being made.
