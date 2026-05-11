---
title: "Data Modeling Best Practices"
description: "Learn data modeling best practices including entity-relationship diagrams, normalization, patterns for SQL and NoSQL, and schema design."
date: 2026-05-11
board: database
url: https://dingjiu1989-hue.github.io/en/database/data-modeling.html
---

## What Is Data Modeling?

Data modeling is the process of defining and organizing data structures to represent real-world entities and their relationships. A good data model ensures data integrity, enables efficient queries, and adapts to changing requirements without breaking existing functionality.

## The Three Levels of Data Modeling

| Level | Description | Audience |
|-------|-------------|----------|
| Conceptual | Business entities and relationships | Stakeholders, product managers |
| Logical | Entities, attributes, and relationships in detail | Architects, analysts |
| Physical | Actual database implementation | Developers, DBAs |

## Conceptual Modeling

Identify the core entities and their high-level relationships:

```
Customer ───< Order ───< OrderItem >─── Product
   │
   └─── Address
```

Entities typically represent nouns in your domain: Customer, Order, Product, Payment, Shipment.

## Logical Modeling

Define attributes, data types, and relationships precisely.

### Entity-Relationship Attributes

```yaml
Customer:
  attributes:
    - id (UUID, PK)
    - email (string, unique, not null)
    - name (string, not null)
    - created_at (timestamp)
  relationships:
    - has_many: Order
    - has_many: Address

Order:
  attributes:
    - id (UUID, PK)
    - customer_id (UUID, FK -> Customer)
    - status (enum: pending, paid, shipped, cancelled)
    - total (decimal, not null)
    - created_at (timestamp)
  relationships:
    - belongs_to: Customer
    - has_many: OrderItem

OrderItem:
  attributes:
    - order_id (UUID, FK -> Order)
    - product_id (UUID, FK -> Product)
    - quantity (integer, > 0)
    - unit_price (decimal, not null)
```

### Relationship Cardinality

| Cardinality | Symbol | Example |
|-------------|--------|---------|
| One-to-one (1:1) | | | User <-> Profile |
| One-to-many (1:N) | |< | Customer <-> Order |
| Many-to-many (M:N) | >< | Student <-> Course |

## Physical Modeling

### SQL Schema Design

```sql
-- Complete physical model for an e-commerce system

CREATE TABLE customers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE addresses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
    label VARCHAR(50),  -- 'home', 'work', 'shipping'
    street VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50),
    zip VARCHAR(20),
    country VARCHAR(2) NOT NULL,
    is_default BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    category_id UUID REFERENCES categories(id),
    sku VARCHAR(50) UNIQUE,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID NOT NULL REFERENCES customers(id),
    address_id UUID REFERENCES addresses(id),
    status VARCHAR(20) DEFAULT 'pending',
    subtotal DECIMAL(10,2) NOT NULL,
    tax DECIMAL(10,2),
    total DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    paid_at TIMESTAMPTZ
);

CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id UUID NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) GENERATED ALWAYS AS (quantity * unit_price) STORED
);

-- Indexes for query performance
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created ON orders(created_at DESC);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_active ON products(is_active) WHERE is_active = true;
```

## NoSQL Data Modeling Patterns

### Embedding vs Referencing

```javascript
// EMBED: Use when data is always accessed together (one-to-few)
// Good for: addresses on an order, items in a cart
{
    _id: ObjectId("..."),
    customer: {
        id: "c123",
        name: "Alice"
    },
    items: [
        { product_id: "p1", name: "Laptop", price: 1200, qty: 1 },
        { product_id: "p2", name: "Mouse", price: 25, qty: 2 }
    ],
    total: 1250
}

// REFERENCE: Use when data is accessed independently (one-to-many/many)
// Good for: products in a catalog, user profiles
// orders collection
{
    _id: ObjectId("..."),
    customer_id: "c123",
    product_ids: ["p1", "p2"]
}
// products collection (accessed independently)
{
    _id: "p1",
    name: "Laptop",
    price: 1200,
    stock: 50
}
```

### Single Table Design (DynamoDB)

```
Table: MyApp

PK               SK                         Data
USER#alice       PROFILE                   name, email, created_at
USER#alice       ORDER#2026-05-01#O1       amount, status
USER#alice       ORDER#2026-05-15#O2       amount, status
PROD#P1          META                      name, price, category
PROD#P2          META                      name, price, category
CAT#electronics  PRODUCT#P1                reference to product
CAT#electronics  PRODUCT#P2                reference to product
```

## Common Modeling Patterns

### Inheritance Mapping (SQL)

```sql
-- Table Per Type (TPT)
CREATE TABLE content (
    id SERIAL PRIMARY KEY,
    type VARCHAR(20) NOT NULL,  -- 'article', 'video', 'podcast'
    title VARCHAR(255) NOT NULL,
    published_at TIMESTAMPTZ
);

CREATE TABLE articles (
    id INTEGER PRIMARY KEY REFERENCES content(id),
    body TEXT,
    word_count INTEGER
);

CREATE TABLE videos (
    id INTEGER PRIMARY KEY REFERENCES content(id),
    url VARCHAR(500),
    duration_seconds INTEGER
);
```

### Soft Delete Pattern

```sql
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMPTZ;
CREATE INDEX idx_users_active ON users(id) WHERE deleted_at IS NULL;

-- Queries automatically exclude deleted records
SELECT * FROM users WHERE deleted_at IS NULL;
```

## Data Modeling Process

1. **Understand the domain**: Talk to stakeholders, identify entities and workflows.
2. **Start conceptual**: Map major entities and their relationships.
3. **Identify access patterns**: List every query your application will make.
4. **Design for queries**: Optimize the model for your most frequent and critical queries.
5. **Normalize for integrity**: Apply normalization rules up to 3NF.
6. **Denormalize for performance**: Selectively denormalize where queries demand it.
7. **Document the model**: Maintain an up-to-date schema diagram and data dictionary.

## Summary

Good data modeling starts with understanding the domain and access patterns. Design entities and relationships at the conceptual level, refine them logically, then implement with the appropriate physical model for your database. For SQL databases, normalize to 3NF and create strategic indexes. For NoSQL databases, model for your access patterns first, using embedding for co-accessed data and references for independently accessed entities. Document your model and keep it synchronized with your code.
