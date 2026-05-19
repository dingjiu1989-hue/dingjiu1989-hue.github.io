---
title: "Data Modeling Best Practices"
description: "Learn data modeling best practices including entity-relationship diagrams, normalization, patterns for SQL and NoSQL, and schema design."
date: 2025-12-22
board: database
url: https://dingjiu1989-hue.github.io/en/database/data-modeling.html
---

# Data Modeling Best Practices

Data Modeling Fundamentals 

Data modeling defines and organizes data structures to represent real-world entities and their relationships. 

Entity-Relationship Diagrams 

ER diagrams map entities (nouns) and relationships (verbs). Key cardinalities: one-to-one, one-to-many, many-to-many. 

Customer:

attributes: id, email, name, created_at

relationships: has_many Order

Order:

attributes: id, customer_id, status, total, created_at

relationships: belongs_to Customer, has_many OrderItem

Normalization 

Aim for third normal form (3NF) in transactional systems: 

  * 1NF: Atomic columns, unique rows

  * 2NF: Full PK dependency

  * 3NF: No transitive dependencies




\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- 3NF design

CREATE TABLE customers (id SERIAL PRIMARY KEY, name TEXT);

CREATE TABLE orders (id SERIAL PRIMARY KEY, customer_id INT REFERENCES customers(id));

CREATE TABLE order_items (id SERIAL PRIMARY KEY, order_id INT REFERENCES orders(id), product_id INT, quantity INT);

Denormalization 

Denormalize selectively for read performance. Common cases: reporting tables, cached aggregates, distributed databases avoiding joins. 

NoSQL Modeling 

Model for access patterns first: 

// Embed for co-accessed data

{

_id: "...",

customer: { id: "c123", name: "Alice" },

items: [{ product_id: "p1", qty: 2 }]

}

Conclusion 

Start with 3NF for data integrity. Denormalize for performance when needed. For NoSQL, design your schema around your query patterns. Document all denormalization decisions with rationale.

**See also:** [Database Normalization Explained](</en/database/database-normalization.html>), [Database Migration Tools and Strategies](</en/database/database-migration.html>), [Data Warehousing Concepts and Modern Tools](</en/database/data-warehousing.html>).

**See also:** [Database Normalization Explained](</en/database/database-normalization.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Data Warehousing Concepts and Modern Tools](</en/database/data-warehousing.html>)

**See also:** [Database Normalization Explained](</en/database/database-normalization.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Data Warehousing Concepts and Modern Tools](</en/database/data-warehousing.html>)

**See also:** [Database Normalization Explained](</en/database/database-normalization.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Data Warehousing Concepts and Modern Tools](</en/database/data-warehousing.html>)

**See also:** [Database Normalization Explained](</en/database/database-normalization.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Data Warehousing Concepts and Modern Tools](</en/database/data-warehousing.html>)

**See also:** [Database Normalization Explained](</en/database/database-normalization.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Data Warehousing Concepts and Modern Tools](</en/database/data-warehousing.html>)

**See also:** [Time Series Databases (InfluxDB, TimescaleDB, ClickHouse)](</en/database/time-series-databases.html>), [Data Consistency Models Explained](</en/database/data-consistency-models.html>), [Database Security Hardening Guide](</en/database/database-security-best-practices.html>)

**See also:** [Time Series Databases (InfluxDB, TimescaleDB, ClickHouse)](</en/database/time-series-databases.html>), [Data Consistency Models Explained](</en/database/data-consistency-models.html>), [Database Security Hardening Guide](</en/database/database-security-best-practices.html>)

**See also:** [Time Series Databases (InfluxDB, TimescaleDB, ClickHouse)](</en/database/time-series-databases.html>), [Data Consistency Models Explained](</en/database/data-consistency-models.html>), [Database Security Hardening Guide](</en/database/database-security-best-practices.html>)

**See also:** [Time Series Databases (InfluxDB, TimescaleDB, ClickHouse)](</en/database/time-series-databases.html>), [Data Consistency Models Explained](</en/database/data-consistency-models.html>), [Database Security Hardening Guide](</en/database/database-security-best-practices.html>)

**See also:** [Time Series Databases (InfluxDB, TimescaleDB, ClickHouse)](</en/database/time-series-databases.html>), [Data Consistency Models Explained](</en/database/data-consistency-models.html>), [Database Security Hardening Guide](</en/database/database-security-best-practices.html>)
