---
title: "EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types"
description: "Master PostgreSQL EXPLAIN ANALYZE: read query plans, understand cost estimation, compare scan types, and analyze join strategies for query optimization."
date: 2026-05-12
board: database
url: https://dingjiu1989-hue.github.io/en/database/query-optimization-explain.html
---

# EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types

EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types   
The `EXPLAIN` command is the single most important tool for understanding query performance. This article teaches you to read execution plans, interpret cost estimates, and identify optimization opportunities in PostgreSQL.   
EXPLAIN Basics   

    
    
    EXPLAIN SELECT * FROM users WHERE email = 'alice@example.com';
    
    

  
Output:   

    
    
    Seq Scan on users  (cost=0.00..1243.12 rows=1 width=84)
    
      Filter: (email = 'alice@example.com'::text)
    
    

  
This shows a sequential scan (Seq Scan) scanning the entire table at an estimated cost of 0.00 to 1243.12, producing 1 row.   
EXPLAIN ANALYZE   
`EXPLAIN ANALYZE` actually executes the query and shows real metrics:   

    
    
    EXPLAIN (ANALYZE, BUFFERS, TIMING) 
    
    SELECT * FROM users WHERE email = 'alice@example.com';
    
    

  
Output:   

    
    
    Seq Scan on users  (cost=0.00..1243.12 rows=1 width=84) (actual time=0.532..12.843 rows=1 loops=1)
    
      Filter: (email = 'alice@example.com'::text)
    
      Rows Removed by Filter: 99999
    
      Buffers: shared hit=840
    
    Planning Time: 0.083 ms
    
    Execution Time: 12.912 ms
    
    

  
Key differences from the estimated plan:   

* **actual time**: The real time (startup..total) for this node.
* **rows=1**: The actual number of rows returned.
* **Rows Removed by Filter**: 99,999 rows were scanned and discarded, a huge waste.
* **Buffers: shared hit=840**: 840 pages were found in shared buffers.
* **Planning Time vs Execution Time**: Total overhead.
  
Scan Types   
Sequential Scan   
The database reads every page of the table. Efficient for tables that fit in memory or when most rows are returned:   

    
    
    EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE total > 0;
    
    -- Seq Scan on orders  (cost=0.00..5432.10 rows=500000 width=42)
    
    

  
**Ideal when**: The query returns more than ~10% of the table. Sequential reads are faster than random reads for large fractions.   
Index Scan   
The database traverses a B-tree index and fetches matching rows from the heap:   

    
    
    EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE id = 42;
    
    -- Index Scan using orders_pkey on orders  (cost=0.29..8.31 rows=1 width=42)
    
    --   Index Cond: (id = 42)
    
    

  
**Ideal when**: Highly selective queries returning a small fraction of rows. Each row fetch requires a random I/O to the heap.   
Index Only Scan   
PostgreSQL fetches the result entirely from the index, avoiding heap access:   

    
    
    EXPLAIN (ANALYZE, BUFFERS) SELECT id, status FROM orders WHERE status = 'paid';
    
    -- Index Only Scan using idx_orders_status on orders  (cost=0.29..123.43 rows=5000 width=36)
    
    

  
The `Heap Fetches: 0` line confirms no heap visits. Visibility map checks ensure rows are visible without visiting the heap.   
Bitmap Scan   
Combines multiple index lookups and sorts pages before fetching:   

    
    
    EXPLAIN (ANALYZE, BUFFERS)
    
    SELECT * FROM orders WHERE status = 'pending' AND total > 1000;
    
    -- Bitmap Heap Scan on orders  (cost=12.34..567.89 rows=200 width=42)
    
    --   Recheck Cond: ((status = 'pending'::text) AND (total > 1000))
    
    --   -> BitmapAnd
    
    --         -> Bitmap Index Scan on idx_orders_status  (cost=0.00..5.12 rows=10000 width=0)
    
    --         -> Bitmap Index Scan on idx_orders_total  (cost=0.00..4.56 rows=5000 width=0)
    
    

  
**Ideal when**: The query can use multiple indexes. The BitmapAnd/BitmapOr operations combine index results efficiently.   
Join Strategies   
Nested Loop Join   
For each row in the outer relation, scan the inner relation:   

    
    
    EXPLAIN (ANALYZE, BUFFERS)
    
    SELECT * FROM users u JOIN orders o ON o.user_id = u.id WHERE u.id = 42;
    
    -- Nested Loop  (cost=0.29..12.45 rows=5 width=126)
    
    --   -> Index Scan on users u  (cost=0.29..8.31 rows=1 width=84)
    
    --   -> Index Scan on orders o  (cost=0.29..4.14 rows=5 width=42)
    
    --         Index Cond: (user_id = 42)
    
    

  
**Ideal when**: Outer relation produces few rows and inner join column has an index.   
Hash Join   
Hash the inner relation, then probe with rows from the outer:   

    
    
    EXPLAIN (ANALYZE, BUFFERS)
    
    SELECT * FROM users u JOIN orders o ON o.user_id = u.id;
    
    -- Hash Join  (cost=1243.00..5432.10 rows=500000 width=126)
    
    --   Hash Cond: (o.user_id = u.id)
    
    --   -> Seq Scan on orders o  (cost=0.00..3210.00 rows=500000 width=42)
    
    --   -> Hash  (cost=843.00..843.00 rows=32000 width=84)
    
    --         -> Seq Scan on users u  (cost=0.00..843.00 rows=32000 width=84)
    
    

  
**Ideal when**: Joining a large portion of two tables, especially without indexed join columns.   
Merge Join   
Sort both relations and merge them in parallel:   

    
    
    EXPLAIN (ANALYZE, BUFFERS)
    
    SELECT * FROM users u JOIN orders o ON o.user_id = u.id ORDER BY u.id;
    
    -- Merge Join  (cost=3456.78..6789.01 rows=500000 width=126)
    
    --   Merge Cond: (u.id = o.user_id)
    
    --   -> Index Scan using users_pkey on users u  (cost=0.29..843.00 rows=32000 width=84)
    
    --   -> Index Scan using idx_orders_user_id on orders o  (cost=0.29..3210.00 rows=500000 width=42)
    
    

  
**Ideal when**: Inputs are already sorted by the join key (e.g., from index scans).   
Cost Parameters   
PostgreSQL's cost model uses tunable constants:   

    
    
    SELECT name, setting, unit
    
    FROM pg_settings
    
    WHERE name LIKE 'seq_page_cost' OR name LIKE 'random_page_cost'
    
       OR name LIKE 'cpu_%' OR name LIKE 'parallel_%';
    
    

  
Default values assume spinning disks:   

* `seq_page_cost = 1.0`
* `random_page_cost = 4.0`
* `cpu_tuple_cost = 0.01`
* `cpu_operator_cost = 0.0025`
  
For SSD-based systems, set `random_page_cost` to 1.1 to reflect the lower cost of random I/O:   

    
    
    ALTER SYSTEM SET random_page_cost = 1.1;
    
    SELECT pg_reload_conf();
    
    

  
Common Optimization Patterns   

    
    
    -- Always check: is an index being used?
    
    EXPLAIN (ANALYZE, BUFFERS) SELECT ...;
    
    
    
    -- Check for sequential scans on large tables
    
    SELECT relname, seq_scan, seq_tup_read, idx_scan
    
    FROM pg_stat_user_tables
    
    ORDER BY seq_scan DESC;
    
    
    
    -- Look for sorts that spill to disk
    
    EXPLAIN (ANALYZE, BUFFERS) SELECT ... ORDER BY ...;
    
    -- Watch for: Sort Method: external merge  Disk: 1234kB
    
    

  
Summary   
Reading `EXPLAIN ANALYZE` output is the most important skill for query optimization. Focus on:   

* Actual vs estimated rows: Large discrepancies indicate stale statistics (`ANALYZE` needed).
2\. Sequential scans on large tables when only a few rows are needed (missing index). 3\. Sort nodes that spill to disk (increase `work_mem`). 4\. Nested loops with many iterations (consider hash join or index).   
Every query optimization should start and end with `EXPLAIN (ANALYZE, BUFFERS)`. The plan tells you what the database actually did, not what you expected it to do.
