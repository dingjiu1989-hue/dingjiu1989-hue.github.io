---
title: "Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance"
description: "Explore database design patterns for application development: Repository pattern, Unit of Work, Query Objects, and table inheritance strategies."
date: 2026-04-02
board: database
url: https://dingjiu1989-hue.github.io/en/database/database-design-patterns.html
---

# Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance

Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance 

Design patterns provide reusable solutions to common database access problems. This article covers patterns that help decouple business logic from database access, manage transactions, and model inheritance. 

Repository Pattern 

The Repository pattern mediates between the domain model and the database, providing a collection-like interface for accessing domain objects. 

Interface 

from abc import ABC, abstractmethod

from typing import Optional, List

class UserRepository(ABC):

@abstractmethod

def find_by_id(self, user_id: int) -> Optional[dict]:

pass

@abstractmethod

def find_by_email(self, email: str) -> Optional[dict]:

pass

@abstractmethod

def save(self, user: dict) -> int:

pass

@abstractmethod

def delete(self, user_id: int) -> bool:

pass

Implementation 

import psycopg2

from psycopg2.extras import RealDictCursor

class PostgresUserRepository(UserRepository):

def **init**(self, conn):

self.conn = conn

def find_by_id(self, user_id: int) -> Optional[dict]:

with self.conn.cursor(cursor_factory=RealDictCursor) as cur:

cur.execute(

"SELECT * FROM users WHERE id = %s",

(user_id,)

)

return cur.fetchone()

def find_by_email(self, email: str) -> Optional[dict]:

with self.conn.cursor(cursor_factory=RealDictCursor) as cur:

cur.execute(

"SELECT * FROM users WHERE email = %s",

(email,)

)

return cur.fetchone()

def save(self, user: dict) -> int:

with self.conn.cursor() as cur:

if 'id' in user:

cur.execute("""

UPDATE users SET email = %s, name = %s

WHERE id = %s RETURNING id

""", (user['email'], user['name'], user['id']))

else:

cur.execute("""

INSERT INTO users (email, name)

VALUES (%s, %s) RETURNING id

""", (user['email'], user['name']))

return cur.fetchone()[0]

def delete(self, user_id: int) -> bool:

with self.conn.cursor() as cur:

cur.execute(

"DELETE FROM users WHERE id = %s", (user_id,)

)

return cur.rowcount > 0

Benefits 

  * **Testability** : Mock the repository interface for unit tests.

  * **Encapsulation** : SQL is contained within the repository.

  * **Swappable** : Change database implementation without changing business logic.

  * **Query optimization** : Changes are isolated to the repository.




Unit of Work Pattern 

Unit of Work tracks changes to objects during a business transaction and writes them as a single unit: 

class UnitOfWork:

def **init**(self, conn):

self.conn = conn

self.new_objects = []

self.dirty_objects = []

self.deleted_objects = []

self.repositories = {}

def register_new(self, obj):

self.new_objects.append(obj)

def register_dirty(self, obj):

if obj not in self.dirty_objects:

self.dirty_objects.append(obj)

def register_deleted(self, obj):

self.deleted_objects.append(obj)

def commit(self):

if not self.new_objects and not self.dirty_objects and not self.deleted_objects:

return

with self.conn:

for obj in self.deleted_objects:

self._delete(obj)

for obj in self.dirty_objects:

self._update(obj)

for obj in self.new_objects:

self._insert(obj)

self.new_objects.clear()

self.dirty_objects.clear()

self.deleted_objects.clear()

def _insert(self, obj):

repo = self._get_repo(type(obj))

repo.save(obj)

def _update(self, obj):

repo = self._get_repo(type(obj))

repo.save(obj)

def _delete(self, obj):

repo = self._get_repo(type(obj))

repo.delete(obj.id)

def _get_repo(self, obj_type):

## Repository registry determines which repository maps to which type

pass

Usage 

def create_order(user_id, items):

uow = UnitOfWork(connection)

user_repo = UserRepository(uow)

order_repo = OrderRepository(uow)

user = user_repo.find_by_id(user_id)

user['last_order_date'] = datetime.utcnow()

uow.register_dirty(user)

order = {'user_id': user_id, 'items': items, 'total': calculate_total(items)}

uow.register_new(order)

uow.commit() # All changes in one transaction

Query Object Pattern 

Query Objects encapsulate database queries as reusable objects: 

from dataclasses import dataclass

from typing import Optional, List

@dataclass

class OrderQuery:

user_id: Optional[int] = None

status: Optional[str] = None

min_total: Optional[float] = None

max_total: Optional[float] = None

created_after: Optional[str] = None

created_before: Optional[str] = None

sort_by: str = 'created_at'

sort_order: str = 'DESC'

limit: int = 100

offset: int = 0

def to_sql(self) -> tuple:

conditions = []

params = []

param_index = 1

if self.user_id is not None:

conditions.append(f"user_id = ${param_index}")

params.append(self.user_id)

param_index += 1

if self.status is not None:

conditions.append(f"status = ${param_index}")

params.append(self.status)

param_index += 1

if self.min_total is not None:

conditions.append(f"total >= ${param_index}")

params.append(self.min_total)

param_index += 1

if self.max_total is not None:

conditions.append(f"total <= ${param_index}")

params.append(self.max_total)

param_index += 1

if self.created_after is not None:

conditions.append(f"created_at >= ${param_index}")

params.append(self.created_after)

param_index += 1

if self.created_before is not None:

conditions.append(f"created_at <= ${param_index}")

params.append(self.created_before)

param_index += 1

where_clause = " AND ".join(conditions) if conditions else "TRUE"

sql = f"""

SELECT * FROM orders

WHERE {where_clause}

ORDER BY {self.sort_by} {self.sort_order}

LIMIT ${param_index} OFFSET ${param_index + 1}

"""

params.extend([self.limit, self.offset])

return sql, params

class OrderRepository:

def **init**(self, conn):

self.conn = conn

def find_by_query(self, query: OrderQuery) -> List[dict]:

sql, params = query.to_sql()

with self.conn.cursor(cursor_factory=RealDictCursor) as cur:

cur.execute(sql, params)

return cur.fetchall()

Table Inheritance Patterns 

Single Table Inheritance (STI) 

All types in one table with a type discriminator column: 

CREATE TABLE content_items (

id BIGSERIAL PRIMARY KEY,

type TEXT NOT NULL, -- 'article', 'video', 'podcast'

title TEXT NOT NULL,

body TEXT, -- articles only

video_url TEXT, -- videos only

audio_url TEXT, -- podcasts only

duration_seconds INTEGER, -- videos and podcasts only

created_at TIMESTAMPTZ DEFAULT NOW()

);

CREATE INDEX idx_content_type ON content_items (type);

**Pros** : Simple queries, no joins. **Cons** : Many nullable columns, wasted space. 

Class Table Inheritance (CTI) 

One table for base type, separate tables for subtypes: 

CREATE TABLE content_items (

id BIGSERIAL PRIMARY KEY,

title TEXT NOT NULL,

created_at TIMESTAMPTZ DEFAULT NOW()

);

CREATE TABLE articles (

id BIGINT PRIMARY KEY REFERENCES content_items(id),

body TEXT NOT NULL

);

CREATE TABLE videos (

id BIGINT PRIMARY KEY REFERENCES content_items(id),

video_url TEXT NOT NULL,

duration_seconds INTEGER

);

**Pros** : No wasted space, clean schema. **Cons** : Requires JOIN to read full object. 

class ContentRepository:

def find_article(self, article_id: int):

cur.execute("""

SELECT c.*, a.body

FROM content_items c

JOIN articles a ON a.id = c.id

WHERE c.id = %s

""", (article_id,))

Concrete Table Inheritance 

Each subtype has its own complete table: 

CREATE TABLE articles (

id BIGSERIAL PRIMARY KEY,

title TEXT NOT NULL,

body TEXT NOT NULL,

created_at TIMESTAMPTZ DEFAULT NOW()

);

CREATE TABLE videos (

id BIGSERIAL PRIMARY KEY,

title TEXT NOT NULL,

video_url TEXT NOT NULL,

duration_seconds INTEGER,

created_at TIMESTAMPTZ DEFAULT NOW()

);

**Pros** : No joins, no nullable columns. **Cons** : Duplicated columns, hard to query across types. 

When to Use Each 

| Pattern | Use Case | |---------|----------| | Single Table | Few subtypes, similar columns, simple queries | | Class Table | Many shared columns, many different columns | | Concrete Table | Completely different behavior per type, no cross-type queries | 

Choosing the Right Pattern 

  * Use **Repository** for most CRUD-heavy applications (standard web apps).

  * Use **Unit of Work** when transactions span multiple objects (order processing, accounting).

  * Use **Query Objects** when queries have many optional parameters (reports, search APIs).

  * Use **Table Inheritance** based on how your domain model maps to data.




These patterns are not prescriptive rules but tools. Use them when they simplify your code; do not force them into a simple application that would be better served by direct SQL or a lightweight ORM.

**See also:** [Schema Design Patterns: Normalization, Denormalization, Naming Conventions](</en/database/schema-design.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [Database Caching](</en/database/database-caching.html>).

**See also:** [Schema Design Patterns: Normalization, Denormalization, Naming Conventions](</en/database/schema-design.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>)

**See also:** [Schema Design Patterns: Normalization, Denormalization, Naming Conventions](</en/database/schema-design.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>)

**See also:** [Schema Design Patterns: Normalization, Denormalization, Naming Conventions](</en/database/schema-design.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>)

**See also:** [Schema Design Patterns: Normalization, Denormalization, Naming Conventions](</en/database/schema-design.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>)

**See also:** [Schema Design Patterns: Normalization, Denormalization, Naming Conventions](</en/database/schema-design.html>), [Database Migration Tools: Alembic, Flyway, Liquibase, Versioning](</en/database/database-migration-tools.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [DynamoDB vs Cassandra: Data Model, Consistency, Scaling, and Cost](</en/database/dynamodb-vs-cassandra.html>), [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [DynamoDB vs Cassandra: Data Model, Consistency, Scaling, and Cost](</en/database/dynamodb-vs-cassandra.html>), [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [DynamoDB vs Cassandra: Data Model, Consistency, Scaling, and Cost](</en/database/dynamodb-vs-cassandra.html>), [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [DynamoDB vs Cassandra: Data Model, Consistency, Scaling, and Cost](</en/database/dynamodb-vs-cassandra.html>), [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [DynamoDB vs Cassandra: Data Model, Consistency, Scaling, and Cost](</en/database/dynamodb-vs-cassandra.html>), [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>)

**See also:** [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>), [DynamoDB vs Cassandra: Data Model, Consistency, Scaling, and Cost](</en/database/dynamodb-vs-cassandra.html>), [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>)
