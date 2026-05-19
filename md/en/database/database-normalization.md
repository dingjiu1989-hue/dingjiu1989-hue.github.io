---
title: "Database Normalization Explained"
description: "Learn database normalization from 1NF to 5NF with practical examples, denormalization trade-offs, and real-world schema design."
date: 2025-12-23
board: database
url: https://dingjiu1989-hue.github.io/en/database/database-normalization.html
---

# Database Normalization Explained

What is Normalization? 

Normalization organizes data to reduce redundancy and improve integrity. Each piece of data is stored in exactly one place. 

Normal Forms 

First Normal Form (1NF) 

Each column contains atomic values. Each row is unique. 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Violates 1NF

CREATE TABLE orders (id SERIAL, products TEXT); -- "Laptop,Mouse"

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- 1NF compliant

CREATE TABLE order_items (

order_id INT REFERENCES orders(id),

product_name TEXT,

PRIMARY KEY (order_id, product_name)

);

Second Normal Form (2NF) 

Must be in 1NF. All non-key columns depend on the entire primary key. 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Violates 2NF: product_name depends only on product_id, not order_id

CREATE TABLE order_details (

order_id INT, product_id INT,

product_name TEXT, quantity INT,

PRIMARY KEY (order_id, product_id)

);

Third Normal Form (3NF) 

Must be in 2NF. No transitive dependencies (non-key depends on non-key). 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Violates 3NF: customer_name depends on customer_id

CREATE TABLE orders (id SERIAL, customer_id INT, customer_name TEXT);

BCNF through 5NF 

BCNF: Every determinant is a candidate key. 4NF: No multi-valued dependencies. 5NF: Join dependencies only from candidate keys. 

Practical Guidance 

Most production databases aim for 3NF: 

  * Design in 3NF



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Profile performance 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Denormalize selectively for performance 4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Document all denormalization decisions 

Denormalization 

Denormalize for: reporting, high-read/low-write workloads, distributed databases, cached aggregates. 

Conclusion 

Normalize to 3NF for transactional integrity. Denormalize selectively for performance. Document your decisions. The key is "the key, the whole key, and nothing but the key."

**See also:** [Data Modeling Best Practices](</en/database/data-modeling.html>), [Data Consistency Models Explained](</en/database/data-consistency-models.html>), [Schema Design Patterns: Normalization, Denormalization, Naming Conventions](</en/database/schema-design.html>).

**See also:** [Data Consistency Models Explained](</en/database/data-consistency-models.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>), [Data Modeling Best Practices](</en/database/data-modeling.html>)

**See also:** [Data Consistency Models Explained](</en/database/data-consistency-models.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>), [Data Modeling Best Practices](</en/database/data-modeling.html>)

**See also:** [Data Consistency Models Explained](</en/database/data-consistency-models.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>), [Data Modeling Best Practices](</en/database/data-modeling.html>)

**See also:** [Data Consistency Models Explained](</en/database/data-consistency-models.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>), [Data Modeling Best Practices](</en/database/data-modeling.html>)

**See also:** [Data Consistency Models Explained](</en/database/data-consistency-models.html>), [Database Sharding: Strategies and Trade-offs](</en/database/database-sharding.html>), [Data Modeling Best Practices](</en/database/data-modeling.html>)

**See also:** [Database Monitoring and Performance Alerting](</en/database/database-monitoring.html>), [Database Testing Strategies for Developers](</en/database/database-testing.html>), [Connection Pooling Guide](</en/database/connection-pooling.html>)

**See also:** [Database Monitoring and Performance Alerting](</en/database/database-monitoring.html>), [Database Testing Strategies for Developers](</en/database/database-testing.html>), [Connection Pooling Guide](</en/database/connection-pooling.html>)

**See also:** [Database Monitoring and Performance Alerting](</en/database/database-monitoring.html>), [Database Testing Strategies for Developers](</en/database/database-testing.html>), [Connection Pooling Guide](</en/database/connection-pooling.html>)

**See also:** [Database Monitoring and Performance Alerting](</en/database/database-monitoring.html>), [Database Testing Strategies for Developers](</en/database/database-testing.html>), [Connection Pooling Guide](</en/database/connection-pooling.html>)

**See also:** [Database Monitoring and Performance Alerting](</en/database/database-monitoring.html>), [Database Testing Strategies for Developers](</en/database/database-testing.html>), [Connection Pooling Guide](</en/database/connection-pooling.html>)
