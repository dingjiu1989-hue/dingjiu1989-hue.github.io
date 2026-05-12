---
title: "Graph Queries in SQL: Recursive CTEs, Adjacency Lists, and WITH RECURSIVE"
description: "Master graph queries in SQL using recursive CTEs, adjacency lists, and the WITH RECURSIVE clause. Compare SQL graph queries vs dedicated graph databases."
date: 2026-05-12
board: database
url: https://dingjiu1989-hue.github.io/en/database/graph-queries.html
---

# Graph Queries in SQL: Recursive CTEs, Adjacency Lists, and WITH RECURSIVE

Graph Queries in SQL: Recursive CTEs, Adjacency Lists, and WITH RECURSIVE   
Relational databases can model and query graph data effectively using recursive Common Table Expressions (CTEs). While not as optimized as dedicated graph databases, SQL-based graph queries handle many real-world use cases without adding infrastructure.   
Modeling Graphs in SQL   
The adjacency list model represents nodes and edges as separate tables:   

    CREATE TABLE nodes (

        id BIGSERIAL PRIMARY KEY,

        label TEXT NOT NULL,

        properties JSONB DEFAULT '{}'

    );

    CREATE TABLE edges (

        id BIGSERIAL PRIMARY KEY,

        source_id BIGINT NOT NULL REFERENCES nodes(id),

        target_id BIGINT NOT NULL REFERENCES nodes(id),

        edge_type TEXT NOT NULL,

        properties JSONB DEFAULT '{}',

        created_at TIMESTAMPTZ DEFAULT NOW()

    );

    -- Indexes for graph traversal

    CREATE INDEX idx_edges_source ON edges (source_id);

    CREATE INDEX idx_edges_target ON edges (target_id);

    CREATE INDEX idx_edges_type ON edges (edge_type);

For an organizational hierarchy, the "manager-employee" relationship:   

    INSERT INTO nodes (id, label) VALUES

        (1, 'Alice CEO'),

        (2, 'Bob CTO'),

        (3, 'Carol CFO'),

        (4, 'Dave Engineering Lead'),

        (5, 'Eve Senior Engineer'),

        (6, 'Frank Junior Engineer');

    INSERT INTO edges (source_id, target_id, edge_type) VALUES

        (1, 2, 'manages'),

        (1, 3, 'manages'),

        (2, 4, 'manages'),

        (4, 5, 'manages'),

        (5, 6, 'manages');

WITH RECURSIVE Basics   
A recursive CTE has two parts: a base term and a recursive term, joined by `UNION ALL`:   

    WITH RECURSIVE org_chart AS (

        -- Base: find the CEO

        SELECT id, label, 0 AS depth, ARRAY[id] AS path

        FROM nodes

        WHERE id = 1

        UNION ALL

        -- Recursive: find direct reports

        SELECT n.id, n.label, oc.depth + 1, oc.path || n.id

        FROM nodes n

        JOIN edges e ON e.target_id = n.id AND e.edge_type = 'manages'

        JOIN org_chart oc ON oc.id = e.source_id

    )

    SELECT repeat('  ', depth) || label AS hierarchy

    FROM org_chart

    ORDER BY path;

Result:   

    Alice CEO

      Bob CTO

        Dave Engineering Lead

          Eve Senior Engineer

            Frank Junior Engineer

      Carol CFO

Graph Traversal Patterns   
Shortest Path (BFS)   

    WITH RECURSIVE bfs AS (

        -- Base: start node

        SELECT id AS node_id, 0 AS distance, ARRAY[id] AS path

        FROM nodes WHERE id = 1

        UNION ALL

        -- Explore neighbors

        SELECT e.target_id, bfs.distance + 1, bfs.path || e.target_id

        FROM bfs

        JOIN edges e ON e.source_id = bfs.node_id

        WHERE NOT e.target_id = ANY(bfs.path)  -- avoid cycles

          AND bfs.distance < 10                -- max depth

    )

    SELECT * FROM bfs

    WHERE node_id = 6  -- target node

    LIMIT 1;

All Paths Between Two Nodes   

    WITH RECURSIVE paths AS (

        SELECT e.source_id, e.target_id, ARRAY[e.source_id, e.target_id] AS path

        FROM edges e

        WHERE e.source_id = 1 AND e.target_id = 6

        UNION ALL

        SELECT p.source_id, e.target_id, p.path || e.target_id

        FROM paths p

        JOIN edges e ON e.source_id = p.target_id

        WHERE NOT e.target_id = ANY(p.path)

          AND array_length(p.path, 1) < 10

    )

    SELECT path FROM paths WHERE target_id = 6;

Cycle Detection   

    WITH RECURSIVE detect_cycles AS (

        SELECT id, ARRAY[id] AS visited, false AS is_cycle

        FROM nodes

        WHERE label = 'Alice CEO'

        UNION ALL

        SELECT n.id, dc.visited || n.id, n.id = ANY(dc.visited)

        FROM detect_cycles dc

        JOIN edges e ON e.source_id = dc.id

        JOIN nodes n ON n.id = e.target_id

        WHERE NOT dc.is_cycle

    )

    SELECT * FROM detect_cycles WHERE is_cycle;

Optimizing Recursive Queries   
Recursive CTEs execute sequentially (each iteration is one plan node). Optimization strategies:   

* **Limit depth early**: Add a depth guard in the `WHERE` clause.
2\. **Use cycle detection**: The `ARRAY[...]` path check can be expensive for deep graphs. Use PostgreSQL 14+'s `CYCLE` clause:   

    WITH RECURSIVE org_chart AS (

        SELECT id, label, 0 AS depth

        FROM nodes WHERE id = 1

        UNION ALL

        SELECT n.id, n.label, oc.depth + 1

        FROM nodes n

        JOIN edges e ON e.target_id = n.id AND e.edge_type = 'manages'

        JOIN org_chart oc ON oc.id = e.source_id

    )

    CYCLE id SET is_cycle USING path

    SELECT * FROM org_chart;

The `CYCLE` clause is more efficient than manual `ARRAY` checks because it uses efficient internal data structures.   
3\. **Create indexes**: The source and target columns must be indexed for good join performance.   
SQL Graphs vs Dedicated Graph Databases   
| Capability | PostgreSQL (Recursive CTEs) | Neo4j (Cypher) | |------------|-----------------------------|-----------------| | Query syntax | WITH RECURSIVE + JOINs | MATCH (n)-[r]->(m) | | Path expressions | Manual construction | Built-in | | Variable-length paths | Recursive CTE depth | [r*1..5] syntax | | Graph algorithms | Custom SQL | Built-in (PageRank, etc.) | | Performance | Table scans, JOINs | Index-free adjacency | | Horizontal scaling | Read replicas, Citus | Native sharding |   
When to Use Recursive CTEs   
Recursive CTEs are the right tool when:   

* The graph is a tree or near-tree hierarchy (org charts, category trees, bill of materials).
* The maximum depth is bounded (typically under 20 levels).
* You already use PostgreSQL and do not want to introduce a separate graph database.
* Graph traversal is a small fraction of overall query volume.

Consider a dedicated graph database when:   

* You need unbounded, many-to-many graph traversal at scale.
* Graph algorithms (shortest path, centrality, PageRank) are the core of your application.
* Path queries traverse millions of nodes and edges.
* You need property graph features (labels on both nodes and edges) as a primary data model.

Recursive CTEs prove that SQL can handle graph queries. For bounded-depth hierarchies, they perform well and keep your architecture simple. When your graph queries become the dominant workload, it is time to evaluate a dedicated graph database.
