---
title: "Graph Databases (Neo4j, Dgraph, ArangoDB)"
description: "Compare Neo4j, Dgraph, and ArangoDB graph databases for connected data, recommendation engines, social networks, and knowledge graphs."
date: 2026-05-11
board: database
url: https://dingjiu1989-hue.github.io/en/database/graph-databases.html
---

## What Are Graph Databases?

Graph databases store data as nodes (entities) and edges (relationships), where both nodes and edges can have properties. This model excels at representing and querying highly connected data, where the relationships between entities are as important as the entities themselves.

## The Graph Model

```
        ┌──────────┐
        │  Alice   │
        │  age: 30 │
        └────┬─────┘
             │
       FOLLOWS│
             │
             ▼
        ┌──────────┐        PURCHASED        ┌──────────┐
        │   Bob    │ ───────────────────────> │ Product  │
        │  age: 25 │                          │ price: 99│
        └──────────┘                          └──────────┘
             │
    REVIEWED  │
             ▼
        ┌──────────┐
        │ Review   │
        │ rating: 5│
        └──────────┘
```

## Graph DB Comparison

| Feature | Neo4j | Dgraph | ArangoDB |
|---------|-------|--------|----------|
| Query language | Cypher | GraphQL+- | AQL |
| Architecture | Native graph | Distributed | Multi-model |
| ACID compliance | Full ACID | Snapshot isolation | Full ACID |
| Sharding | Manual (enterprise) | Automatic | Automatic |
| Performance | Excellent (single node) | Excellent (distributed) | Good |
| Learning curve | Low (Cypher is intuitive) | Medium | Medium |

## Neo4j

Neo4j is the most popular graph database with the Cypher query language.

### Data Model

```cypher
// Create nodes and relationships
CREATE (alice:Person {name: 'Alice', age: 30, city: 'San Francisco'})
CREATE (bob:Person {name: 'Bob', age: 25, city: 'New York'})
CREATE (laptop:Product {name: 'Laptop', price: 1200})
CREATE (mouse:Product {name: 'Mouse', price: 25})

CREATE (alice)-[:FOLLOWS]->(bob)
CREATE (bob)-[:PURCHASED {date: '2026-05-01'}]->(laptop)
CREATE (bob)-[:PURCHASED {date: '2026-05-02'}]->(mouse)
CREATE (bob)-[:REVIEWED {rating: 5, text: 'Great!'}]->(laptop)
```

### Querying

```cypher
// Find products purchased by people Alice follows
MATCH (alice:Person {name: 'Alice'})-[:FOLLOWS]->(friend)-[:PURCHASED]->(product)
RETURN friend.name AS friend, product.name AS product

// Shortest path between two people
MATCH p = shortestPath(
    (alice:Person {name: 'Alice'})-[:FOLLOWS*]-(bob:Person {name: 'Bob'})
)
RETURN length(p) AS degrees_of_separation

// Product recommendations: what did friends of friends buy?
MATCH (me:Person {name: 'Alice'})-[:FOLLOWS*2]-(friend_of_friend)-[:PURCHASED]->(product)
WHERE NOT (me)-[:PURCHASED]->(product)
RETURN product.name, COUNT(*) AS frequency
ORDER BY frequency DESC
LIMIT 10

// Average rating per product category
MATCH (product:Product)<-[review:REVIEWED]-(customer:Person)
RETURN product.name, AVG(review.rating) AS avg_rating, COUNT(review) AS review_count
ORDER BY avg_rating DESC
```

### Neo4j with Python

```python
from neo4j import GraphDatabase

class MovieGraph:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def find_recommendations(self, user_name, limit=10):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (user:Person {name: $name})
                MATCH (user)-[:RATED]->(movie)
                MATCH (movie)<-[:RATED]-(other)-[:RATED]->(rec)
                WHERE rec.rating >= 4 AND NOT (user)-[:RATED]->(rec)
                RETURN rec.title, AVG(rec.rating) AS score
                ORDER BY score DESC
                LIMIT $limit
            """, name=user_name, limit=limit)
            return [record.data() for record in result]

recommender = MovieGraph("bolt://localhost:7687", "neo4j", "password")
recommendations = recommender.find_recommendations("Alice")
```

## Dgraph

Dgraph is a distributed graph database that uses GraphQL+- (a GraphQL variant) and has strong horizontal scaling.

### Schema

```graphql
type Person {
    name: String! @index(exact, term)
    age: Int
    city: String @index(hash)
    follows: [Person] @reverse
    purchased: [Purchase]
}

type Product {
    name: String! @index(term)
    price: Float
}

type Purchase {
    product: Product
    date: DateTime
    review: Review
}

type Review {
    rating: Int
    text: String
}
```

### Data and Queries

```graphql
# Add data
mutation {
  addPerson(input: [
    { name: "Alice", age: 30, city: "San Francisco",
      follows: [{ name: "Bob" }],
      purchased: [{ product: { name: "Laptop" }, date: "2026-05-01" }]
    }
  ]) { person { name } }
}

# Query
{
  queryPerson(filter: { name: { eq: "Alice" } }) {
    follows {
      name
      purchased {
        product { name }
        review { rating }
      }
    }
  }
}
```

### Distributed Query Example

```graphql
# Social graph traversal across distributed nodes
{
  recommendProducts(user: "Alice") {
    productName
    recommendationScore
    purchasedBy
  }
}
```

## ArangoDB

ArangoDB is a multi-model database that supports document, key-value, and graph models with a single query language (AQL).

```javascript
// Create graph
const graph = db.graph('social');
graph.addVertexCollection('users');
graph.addEdgeCollection('follows', 'users', 'users');
graph.addEdgeCollection('purchased', 'users', 'products');

// Add data
db.users.save({ _key: 'alice', name: 'Alice', age: 30 });
db.users.save({ _key: 'bob', name: 'Bob', age: 25 });
db.products.save({ _key: 'laptop', name: 'Laptop', price: 1200 });
db.follows.save({ _from: 'users/alice', _to: 'users/bob' });
db.purchased.save({ _from: 'users/bob', _to: 'products/laptop' });
```

```javascript
// AQL graph traversal
db.query(`
    FOR v, e, p IN 2..3 OUTBOUND 'users/alice'
    GRAPH 'social'
        FILTER e.review.rating >= 4
        RETURN DISTINCT {
            person: v.name,
            product: p.edges[1]._to
        }
`);
```

## Use Cases

| Use Case | Why Graph DB | Example Query |
|----------|--------------|---------------|
| Social network | Friends of friends | "People Alice might know" |
| Recommendation engine | Purchase patterns | "Customers who bought this also bought" |
| Fraud detection | Transaction patterns | "Identify suspicious transaction rings" |
| Knowledge graph | Entity relationships | "What is the relationship between X and Y?" |
| Identity resolution | Entity matching | "Find all accounts belonging to one person" |
| Supply chain | Dependency tracking | "Which suppliers affect product X?" |

## When Not to Use a Graph Database

- Simple CRUD applications with no complex relationships
- Aggregation-heavy analytics (use columnar DB instead)
- Large-scale time-series data
- Applications where relationships are simple and well-understood (relational DB is fine)
- When your team lacks graph database expertise

## Summary

Graph databases are the best choice for highly connected data where relationship traversal is the primary access pattern. Neo4j offers the most mature ecosystem with the intuitive Cypher query language. Dgraph provides excellent horizontal scaling for distributed deployments. ArangoDB's multi-model approach lets you mix graph, document, and key-value patterns in a single database. Choose based on your scalability needs, team expertise, and whether you need multi-model capabilities or a pure graph approach.
