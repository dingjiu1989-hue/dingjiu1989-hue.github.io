---
title: "Database Design Fundamentals: Normalization, Indexing, and Schema Design"
description: "Design databases that don't haunt you later. Covers normalization (1NF to 3NF), indexing strategies, relationship types, and common schema design mistakes."
date: 2025-10-08
board: tech
url: https://aidev.fit/en/tech/database-design-fundamentals.html
---

# Database Design Fundamentals: Normalization, Indexing, and Schema Design

A well-designed database makes every query simpler and faster. A poorly-designed one creates bugs, slow queries, and painful migrations forever. Here are the fundamentals every developer should know before creating tables.

## 1\. Normalization — Reduce Redundancy

Normalization eliminates duplicate data and prevents update anomalies. You need at least 3NF (Third Normal Form) for most applications.

### 1NF: Atomic Values, No Repeating Groups
    
    
    -- ❌ Denormalized: multiple phone numbers in one field
    | id | name  | phones              |
    | 1  | Alice | "555-0001, 555-0002"|
    
    -- ✅ 1NF: each value is atomic, or use a separate table
    | id | name  |
    | 1  | Alice |
    | id | user_id | phone     |
    | 1  | 1       | 555-0001  |
    | 2  | 1       | 555-0002  |

### 2NF: No Partial Dependencies

Every non-key column must depend on the WHOLE primary key, not part of it. This only applies to tables with composite keys.
    
    
    -- ❌ 2NF violation: course_name depends only on course_id, not the full key
    | student_id | course_id | course_name | grade |
    | 1          | CS101     | Intro CS    | A     |
    
    -- ✅ 2NF: split into two tables
    Students: student_id → course_id → grade
    Courses: course_id → course_name

### 3NF: No Transitive Dependencies

Non-key columns must not depend on other non-key columns.
    
    
    -- ❌ 3NF violation: city_population depends on city, not directly on the key
    | student_id | city    | city_population |
    | 1          | Boston  | 675000          |
    
    -- ✅ 3NF: city_population in a cities table
    Students: student_id → city_id
    Cities: city_id → name, population

## 2\. Indexing — Speed Up Queries

Index Type| Best For| Example  
---|---|---  
B-Tree (default)| Equality, range, sorting| WHERE email = ?, ORDER BY created_at  
Composite| Multi-column queries| WHERE user_id = ? AND status = ?  
Partial| Filtering by condition| WHERE deleted_at IS NULL  
Full-text (GIN/GiST)| Text search| WHERE body @@ to_tsquery('typescript')  
Unique| Enforce uniqueness| UNIQUE(email)  
  
### Index Rules of Thumb

  * **Index WHERE and JOIN columns.** Every foreign key gets an index.
  * **Composite index column order matters.** Put the most selective column first.
  * **Don't over-index.** Each index slows down INSERT/UPDATE/DELETE.
  * **Use EXPLAIN ANALYZE.** Verify the index is actually being used.

## 3\. Relationship Types
    
    
    -- One-to-Many (most common):
    CREATE TABLE posts (
      id SERIAL PRIMARY KEY,
      user_id INT REFERENCES users(id),  -- FK to users
      title TEXT NOT NULL
    );  -- One user → many posts
    
    -- Many-to-Many (use junction table):
    CREATE TABLE post_tags (
      post_id INT REFERENCES posts(id),
      tag_id INT REFERENCES tags(id),
      PRIMARY KEY (post_id, tag_id)
    );  -- One post → many tags, one tag → many posts
    
    -- One-to-One (rare, use for optional extension):
    CREATE TABLE user_profiles (
      user_id INT PRIMARY KEY REFERENCES users(id),
      bio TEXT
    );  -- One user → one profile

## 4\. Common Schema Design Mistakes

Mistake| Why It's Bad| Fix  
---|---|---  
Using VARCHAR for everything| No constraints, wasted space| Use appropriate types (UUID, INT, TIMESTAMPTZ, TEXT)  
Storing JSON blobs instead of columns| Can't index, can't query efficiently| Relational columns first, JSONB only for truly dynamic data  
No TIMESTAMPTZ| Timezone bugs are a nightmare| Always use TIMESTAMPTZ, store UTC  
Missing foreign key constraints| Orphaned data, referential chaos| Always add FK constraints (ON DELETE CASCADE or SET NULL)  
EAV (Entity-Attribute-Value)| Unqueriable soup| Use JSONB for dynamic fields per row, or normal columns  
  
## 5\. Choosing Your Primary Key

Strategy| Pros| Cons  
---|---|---  
**UUID v4**|  No collisions, client-generated, no sequence contention| Larger (16 bytes), fragmented index, slower joins  
**UUID v7**|  Time-ordered, all UUID benefits| Slightly more complex generation  
**Auto-increment INT**|  Small index, fast joins, ordered| Predictable, can't merge across servers, exposes count  
**Auto-increment BIGINT**|  Same as INT, won't overflow| Same cons. Use this over INT for new projects.  
**Nano ID / CUID2**|  URL-safe, collision-resistant| String-based (slower than UUID in Postgres)  
  
**Recommendation:** UUID v7 for distributed systems and public-facing IDs. BIGINT for internal tables. Avoid exposing auto-increment IDs in URLs.

**Bottom line:** Normalize to 3NF, index every FK and query column, use appropriate data types, and always have foreign key constraints. A well-designed schema is cheaper to fix now than later. See also: [database comparison](</en/compare/postgresql-vs-mysql-vs-sqlite.html>) and [ORM comparison](</en/compare/prisma-vs-drizzle-vs-typeorm.html>).
