---
title: "Graph Databases (Neo4j, Dgraph, ArangoDB)"
description: "Compare Neo4j, Dgraph, and ArangoDB graph databases for connected data, recommendation engines, social networks, and knowledge graphs."
date: 2025-12-23
board: database
url: https://dingjiu1989-hue.github.io/en/database/graph-databases.html
---

# Graph Databases (Neo4j, Dgraph, ArangoDB)

Graph Database Fundamentals 

Graph databases store data as nodes (entities) and edges (relationships). They excel at traversing connected data. 

Neo4j 

The most popular graph database with Cypher query language: 

CREATE (alice:Person {name: 'Alice', age: 30})

CREATE (bob:Person {name: 'Bob', age: 25})

CREATE (alice)-[:FOLLOWS]->(bob)

MATCH (alice:Person {name: 'Alice'})-[:FOLLOWS*2]->(friend)

RETURN friend.name

ArangoDB 

Multi-model database supporting graph, document, and key-value: 

db._query(`

FOR v IN 1..3 OUTBOUND 'users/alice' GRAPH 'social'

RETURN v.name

`);

Property Graph vs RDF 

| Aspect | Property Graph | RDF (SPARQL) | |--------|---------------|--------------| | Model | Labeled nodes/edges | Triple stores | | Schema | Schema-optional | Formal ontology | | Query | Cypher, Gremlin | SPARQL | | Best for | Applications | Linked data, semantics | 

Use Cases 

Graph databases excel in social networks, recommendation engines, fraud detection, knowledge graphs, and identity resolution. Avoid them for simple CRUD or aggregation-heavy analytics. 

Conclusion 

Choose Neo4j for mature graph capabilities and Cypher. Choose ArangoDB for multi-model flexibility. Use property graphs for applications and RDF for semantic web workloads.

**See also:** [Time Series Databases (InfluxDB, TimescaleDB, ClickHouse)](</en/database/time-series-databases.html>), [Data Lake vs Data Warehouse vs Lakehouse](</en/database/data-lake-vs-warehouse.html>), [Full-Text Search Engines (Elasticsearch, Meilisearch, Typesense)](</en/database/full-text-search.html>).

**See also:** [Time Series Databases (InfluxDB, TimescaleDB, ClickHouse)](</en/database/time-series-databases.html>), [Full-Text Search Engines (Elasticsearch, Meilisearch, Typesense)](</en/database/full-text-search.html>), [Best Database GUI Tools 2026: TablePlus vs DBeaver vs Beekeeper vs DataGrip](</en/tools/best-database-gui-tools.html>)

**See also:** [Time Series Databases (InfluxDB, TimescaleDB, ClickHouse)](</en/database/time-series-databases.html>), [Full-Text Search Engines (Elasticsearch, Meilisearch, Typesense)](</en/database/full-text-search.html>), [Best Database GUI Tools 2026: TablePlus vs DBeaver vs Beekeeper vs DataGrip](</en/tools/best-database-gui-tools.html>)

**See also:** [Time Series Databases (InfluxDB, TimescaleDB, ClickHouse)](</en/database/time-series-databases.html>), [Full-Text Search Engines (Elasticsearch, Meilisearch, Typesense)](</en/database/full-text-search.html>), [Best Database GUI Tools 2026: TablePlus vs DBeaver vs Beekeeper vs DataGrip](</en/tools/best-database-gui-tools.html>)

**See also:** [Time Series Databases (InfluxDB, TimescaleDB, ClickHouse)](</en/database/time-series-databases.html>), [Full-Text Search Engines (Elasticsearch, Meilisearch, Typesense)](</en/database/full-text-search.html>), [Best Database GUI Tools 2026: TablePlus vs DBeaver vs Beekeeper vs DataGrip](</en/tools/best-database-gui-tools.html>)

**See also:** [Time Series Databases (InfluxDB, TimescaleDB, ClickHouse)](</en/database/time-series-databases.html>), [Full-Text Search Engines (Elasticsearch, Meilisearch, Typesense)](</en/database/full-text-search.html>), [Best Database GUI Tools 2026: TablePlus vs DBeaver vs Beekeeper vs DataGrip](</en/tools/best-database-gui-tools.html>)

**See also:** [Data Modeling Best Practices](</en/database/data-modeling.html>), [NoSQL Databases Guide (MongoDB, DynamoDB, Firestore)](</en/database/nosql-databases-guide.html>), [SQL vs NoSQL Decision Guide](</en/database/sql-vs-nosql.html>)

**See also:** [Data Modeling Best Practices](</en/database/data-modeling.html>), [NoSQL Databases Guide (MongoDB, DynamoDB, Firestore)](</en/database/nosql-databases-guide.html>), [SQL vs NoSQL Decision Guide](</en/database/sql-vs-nosql.html>)

**See also:** [Data Modeling Best Practices](</en/database/data-modeling.html>), [NoSQL Databases Guide (MongoDB, DynamoDB, Firestore)](</en/database/nosql-databases-guide.html>), [SQL vs NoSQL Decision Guide](</en/database/sql-vs-nosql.html>)

**See also:** [Data Modeling Best Practices](</en/database/data-modeling.html>), [NoSQL Databases Guide (MongoDB, DynamoDB, Firestore)](</en/database/nosql-databases-guide.html>), [SQL vs NoSQL Decision Guide](</en/database/sql-vs-nosql.html>)

**See also:** [Data Modeling Best Practices](</en/database/data-modeling.html>), [NoSQL Databases Guide (MongoDB, DynamoDB, Firestore)](</en/database/nosql-databases-guide.html>), [SQL vs NoSQL Decision Guide](</en/database/sql-vs-nosql.html>)

**See also:** [Data Modeling Best Practices](</en/database/data-modeling.html>), [NoSQL Databases Guide (MongoDB, DynamoDB, Firestore)](</en/database/nosql-databases-guide.html>), [SQL vs NoSQL Decision Guide](</en/database/sql-vs-nosql.html>)

**See also:** [Data Modeling Best Practices](</en/database/data-modeling.html>), [NoSQL Databases Guide (MongoDB, DynamoDB, Firestore)](</en/database/nosql-databases-guide.html>), [SQL vs NoSQL Decision Guide](</en/database/sql-vs-nosql.html>)

**See also:** [Data Modeling Best Practices](</en/database/data-modeling.html>), [NoSQL Databases Guide (MongoDB, DynamoDB, Firestore)](</en/database/nosql-databases-guide.html>), [SQL vs NoSQL Decision Guide](</en/database/sql-vs-nosql.html>)

**See also:** [Data Modeling Best Practices](</en/database/data-modeling.html>), [NoSQL Databases Guide (MongoDB, DynamoDB, Firestore)](</en/database/nosql-databases-guide.html>), [SQL vs NoSQL Decision Guide](</en/database/sql-vs-nosql.html>)

**See also:** [Data Modeling Best Practices](</en/database/data-modeling.html>), [NoSQL Databases Guide (MongoDB, DynamoDB, Firestore)](</en/database/nosql-databases-guide.html>), [SQL vs NoSQL Decision Guide](</en/database/sql-vs-nosql.html>)
