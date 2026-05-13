---
title: "B-Tree, Hash, GiST, GIN: Index Type Selection Guide"
description: "Choose the right database index type: B-Tree for general use, Hash for equality, GiST/GIN for full-text and JSON."
date: 2026-05-12
board: database
url: https://dingjiu1989-hue.github.io/en/database/database-index-types.html
---

# B-Tree, Hash, GiST, GIN: Index Type Selection Guide

# B-Tree, Hash, GiST, GIN: Index Type Selection Guide

  


# B-Tree, Hash, GiST, GIN: Index Type Selection Guide

  
  
  
  


# B-Tree, Hash, GiST, GIN: Index Type Selection Guide

  
  
  
  
  
  
  


# B-Tree, Hash, GiST, GIN: Index Type Selection Guide

  
  
  
  
  
  
  


Database indexes accelerate queries by providing fast lookup paths. Different index types optimize for different query patterns. Choosing the wrong index type wastes storage and may not improve query performance.

  
  
  
  
  
  
  
  
  
  


##  B-Tree Indexes

  
  
  
  
  
  
  
  
  
  


B-Tree is the default and most versatile index type. It supports equality, range, sorting, and pattern matching queries. B-Tree indexes organize data in a balanced tree structure where leaf nodes contain sorted data values.

  
  
  
  
  
  
  
  
  
  


Use B-Tree for: primary key lookups, range queries (>, <, BETWEEN), ORDER BY sorting, prefix matching (LIKE 'abc%'). B-Tree is optimal when queries filter by comparison operators or require sorted output.

  
  
  
  
  
  
  
  
  
  


Performance characteristics: O(log n) lookup time. Insert and delete cost O(log n) with page splits. B-Tree is the best general-purpose index and should be your default choice.

  
  
  
  
  
  
  
  
  
  


##  Hash Indexes

  
  
  
  
  
  
  
  
  
  


Hash indexes support only equality lookups (=, IN). They compute a hash of the index key and store the hash value. Hash indexes are smaller than B-Tree for the same data because they store fixed-length hash values.

  
  
  
  
  
  
  
  
  
  


Use Hash indexes for: exact-match lookups where range queries are never needed. Hash indexes perform best when indexed values are large (long strings) where hash comparisons are faster than value comparisons.

  
  
  
  
  
  
  
  
  
  


PostgreSQL's hash indexes are now WAL-logged and crash-safe (since PostgreSQL 10). They were historically discouraged but are production-ready in modern versions. Benchmark B-Tree vs Hash for your specific workload before choosing.

  
  
  
  
  
  
  
  
  
  


##  GiST Indexes

  
  
  
  
  
  
  
  
  
  


GiST (Generalized Search Tree) supports complex data types: geometric data, full-text search, range types, and nearest-neighbor searches. GiST is an extensible index framework—different operators provide different capabilities.

  
  
  
  
  
  
  
  
  
  


Use GiST for: geospatial queries with PostGIS, range type overlap (&& operator), full-text ranking and ordering, nearest-neighbor (ORDER BY val <-> target). GiST indexes handle queries that B-Tree cannot express.

  
  
  
  
  
  
  
  
  
  


Trade-offs: GiST indexes are larger than B-Tree and slower to build. Query performance varies by operator class. GiST has higher write overhead.

  
  
  
  
  
  
  
  
  
  


##  GIN Indexes

  
  
  
  
  
  
  
  
  
  


GIN (Generalized Inverted Index) is designed for composite values: arrays, JSONB, full-text vectors. GIN stores mappings from component values to rows containing them.

  
  
  
  
  
  
  
  
  
  


Use GIN for: JSONB queries (? and @> operators), array containment (array @> value), full-text search (tsvector @@ tsquery), trigram similarity (pg_trgm extension). GIN excels at searching within composite data.

  
  
  
  
  
  
  
  
  
  


GIN indexes have fast query speed but slow writes. Use fastupdate setting for write-heavy workloads—it buffers index entries and bulk-inserts them. GIN indexes are significantly larger than B-Tree.

  
  
  
  
  
  
  
  
  
  


##  Choosing

  
  
  
  
  
  
  
  
  
  


Start with B-Tree. If B-Tree does not support your query type, evaluate GiST or GIN based on your data type. Hash indexes are rarely needed—B-Tree handles equality queries well and supports more operations. Test index types with your actual data and query patterns.
