---
title: "CQRS Pattern: Command Query Responsibility Segregation"
description: "Learn CQRS pattern with read/write separation, event sourcing integration, materialized views, and guidance on when to use it."
date: 2026-05-12
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/cqrs-pattern.html
---

Command Query Responsibility Segregation (CQRS) is a pattern that separates read and write operations into different models. Instead of using a single model for both commands that change state and queries that read state, CQRS uses separate models optimized for each purpose. This article explains the pattern, its integration with event sourcing, materialized views, and when CQRS adds value versus when it overcomplicates.

## Core Concept

In a traditional CRUD architecture, the same entity model handles both reads and writes:

```python
class UserModel:
    def get_user(self, user_id): ...    # Query
    def update_user(self, user_id, data): ...  # Command
    def create_user(self, data): ...    # Command
```

In CQRS, these are split:

```python
# Command side (writes)
class UserCommand:
    def create_user(self, data): ...
    def update_email(self, user_id, new_email): ...
    def deactivate_user(self, user_id): ...

# Query side (reads)
class UserQuery:
    def get_user_by_id(self, user_id): ...
    def search_users(self, criteria): ...
    def get_user_profile(self, user_id): ...
```

### Why Separate?

The read and write paths have different requirements:

| Aspect | Command Side | Query Side |
|--------|-------------|------------|
| Focus | Business logic, validation, consistency | Performance, flexibility, denormalization |
| Data model | Normalized, domain-driven | Denormalized, view-optimized |
| Operations | Create, Update, Delete | Queries, aggregations |
| Consistency | ACID required | Eventual often acceptable |
| Scalability | Scale by domain partitioning | Scale by read replicas |

## Implementation Patterns

### Simple CQRS (Separate Models, Single Database)

The simplest CQRS implementation uses separate command and query models but a single database.

```python
# Simple CQRS with separate models
from dataclasses import dataclass

# Command model
@dataclass
class OrderCommand:
    db_connection: Database
    
    def place_order(self, customer_id, items):
        total = sum(item.price * item.quantity for item in items)
        order_id = self.db_connection.execute(
            "INSERT INTO orders (customer_id, total, status) VALUES (?, ?, 'pending')",
            (customer_id, total)
        )
        for item in items:
            self.db_connection.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)",
                (order_id, item.product_id, item.quantity, item.price)
            )
        return order_id

# Query model
@dataclass
class OrderQuery:
    db_connection: Database
    
    def get_order_summary(self, customer_id, page=1, page_size=20):
        return self.db_connection.query(
            """SELECT o.id, o.created_at, o.total, o.status,
                      COUNT(oi.id) as item_count
               FROM orders o
               LEFT JOIN order_items oi ON o.id = oi.order_id
               WHERE o.customer_id = ?
               GROUP BY o.id
               ORDER BY o.created_at DESC
               LIMIT ? OFFSET ?""",
            (customer_id, page_size, (page - 1) * page_size)
        )
```

### CQRS with Separate Databases

For full separation, use different databases for commands and queries.

```
[Client] -> [Command Handler] -> [Write DB (PostgreSQL)]
[Client] -> [Query Handler]   -> [Read DB (Elasticsearch / Redis)]
                     ^
                     | [Sync mechanism: CDC, event bus, batch]
```

```python
# Write side: PostgreSQL (normalized)
class OrderWriteRepository:
    def save(self, order):
        with self.conn.transaction():
            self.conn.execute("INSERT INTO orders ...", order.data())
            
# Read side: Elasticsearch (denormalized for search)
class OrderReadRepository:
    def save_projection(self, order):
        self.es.index(index="orders", id=order.id, body=order.search_data())
    
    def search(self, query):
        return self.es.search(index="orders", body=query)
```

The sync mechanism keeps the read databases updated. This can use change data capture, domain events, or batch jobs.

## Event Sourcing Integration

CQRS pairs naturally with event sourcing. Instead of storing the current state, event sourcing stores a sequence of events that led to the current state.

### How It Works

```python
# Event-sourced command handler
class AccountCommand:
    def __init__(self, event_store):
        self.event_store = event_store
    
    def deposit(self, account_id, amount):
        balance = self._get_current_balance(account_id)
        event = MoneyDeposited(account_id, amount, balance + amount)
        self.event_store.append(event)
    
    def withdraw(self, account_id, amount):
        balance = self._get_current_balance(account_id)
        if balance < amount:
            raise InsufficientFundsError()
        event = MoneyWithdrawn(account_id, amount, balance - amount)
        self.event_store.append(event)
    
    def _get_current_balance(self, account_id):
        events = self.event_store.get_events(account_id)
        balance = 0
        for event in events:
            if isinstance(event, MoneyDeposited):
                balance += event.amount
            elif isinstance(event, MoneyWithdrawn):
                balance -= event.amount
        return balance
```

### Materialized View from Events

Projections build read models by processing events:

```python
# Projection: Building a read model from events
class AccountBalanceProjection:
    def __init__(self, read_db):
        self.read_db = read_db
    
    def handle_deposited(self, event):
        # Update the projection atomically
        self.read_db.execute(
            """INSERT INTO account_summary (account_id, balance, last_updated)
               VALUES (?, ?, ?)
               ON CONFLICT(account_id) DO UPDATE SET
                   balance = balance + ?,
                   last_updated = ?""",
            (event.account_id, event.amount, event.timestamp,
             event.amount, event.timestamp)
        )
    
    def handle_withdrawn(self, event):
        self.read_db.execute(
            "UPDATE account_summary SET balance = ?, last_updated = ? WHERE account_id = ?",
            (event.new_balance, event.timestamp, event.account_id)
        )
```

## Materialized Views

Materialized views are denormalized, pre-computed read models. They make queries fast by storing data in a shape that matches the query.

```sql
-- Materialized view for order dashboards
CREATE MATERIALIZED VIEW monthly_customer_summary AS
SELECT
    c.id as customer_id,
    c.email,
    DATE_TRUNC('month', o.created_at) as month,
    COUNT(DISTINCT o.id) as order_count,
    SUM(oi.quantity * oi.price) as total_spent,
    AVG(oi.quantity * oi.price) as avg_order_value
FROM customers c
JOIN orders o ON c.id = o.customer_id
JOIN order_items oi ON o.id = oi.order_id
GROUP BY c.id, c.email, DATE_TRUNC('month', o.created_at);

-- Queries against the materialized view are fast
SELECT * FROM monthly_customer_summary
WHERE customer_id = 42
ORDER BY month DESC;
```

### Projection Design Principles

1. **Idempotent processing**: Processing the same event twice produces the same result.
2. **Exactly-once semantics**: Track which events have been processed to avoid duplicates.
3. **Rebuildable**: Projections can be rebuilt from scratch by replaying all events.
4. **Versioned**: Schema changes to projections support backward compatibility.

## When CQRS Adds Value

CQRS is not the right choice for every application. It adds significant complexity.

### Use CQRS When

- **Different read and write models**: The data you write differs significantly from the data you read. For example, writing a normalized order, but reading a denormalized customer dashboard with order history, product recommendations, and activity metrics.
- **Different performance requirements**: Reads need to be fast at high concurrency, while writes need transactional guarantees. Separating them allows independent scaling.
- **Multiple read representations**: The same data needs different representations for different consumers (analytics dashboard, customer portal, mobile app).
- **Complex business logic**: The write side has complex validation and business rules that conflict with simple query paths.

### When NOT to Use CQRS

- **Simple CRUD applications**: If your read model looks like your write model, CQRS adds complexity without benefit.
- **Small teams or early-stage products**: The operational complexity of managing multiple models and sync mechanisms is significant.
- **Single-model fits both read and write**: Many applications have a simple enough data model that a single entity handles both.
- **Strong consistency requirements everywhere**: If every read must see every write immediately, the complexity of sync mechanisms outweighs the benefits.

## Common Pitfalls

- **Inconsistent read models**: Read models lag behind writes due to async updates. Design for eventual consistency.
- **Duplicate logic**: Business rules end up in both command handlers and projection handlers. Keep business logic in commands only.
- **Over-normalization**: Projections should be fast and denormalized. Do not replicate the write model schema.
- **Missing error handling**: Projection failures can silently cause stale data. Monitor and alert on projection lag.

## Conclusion

CQRS separates read and write operations into different models, each optimized for its purpose. It pairs well with event sourcing, which stores events rather than state, and materialized views, which pre-compute read-optimized data shapes. CQRS adds substantial complexity, so use it only when your application genuinely benefits from independent read and write models. For most applications, start with a simple CRUD model and extract CQRS patterns when specific performance or modeling needs arise.
