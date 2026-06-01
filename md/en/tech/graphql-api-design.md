---
title: "GraphQL API Design: Schema Best Practices, Federation, and Performance"
description: "Design production GraphQL APIs: schema-first design, N+1 query solutions (DataLoader), federation for microservices, error handling patterns, and caching strategies. Real examples from GitHub and Shopify APIs."
date: 2025-10-14
board: tech
url: https://aidev.fit/en/tech/graphql-api-design.html
---

# GraphQL API Design: Schema Best Practices, Federation, and Performance

GraphQL API design involves tradeoffs that REST does not — N+1 queries, over-fetching is replaced with potential under-fetching, and the flexibility of client-driven queries creates new security and performance challenges. This guide covers schema design, federation, performance optimization, and patterns learned from production GraphQL APIs at GitHub, Shopify, and Stripe.

## Schema Design Principles

Principle| Good Practice| Anti-Pattern  
---|---|---  
Naming| Use descriptive names: `article(id: ID!): Article`| Generic names: `node(id: ID!): Node` for everything  
Nullability| Mark fields as nullable unless always present: `email: String`| Making everything Non-Null: `email: String!` — breaks clients on partial data  
Pagination| Cursor-based (Relay spec): `articles(first: Int, after: String): ArticleConnection!`| Offset-based: `articles(page: Int): [Article]` — breaks under concurrent writes  
Mutations| Specific input types per mutation: `createArticle(input: CreateArticleInput!): Article!`| Reusing types between queries and mutations (they diverge)  
Errors| Union type for success/error: `CreateArticlePayload = Article | ValidationError | PermissionError`| Using HTTP status codes or top-level errors for business logic errors  
Versioning| Add fields, deprecate with @deprecated, never remove| Breaking changes without deprecation period  
  
## Solving the N+1 Problem with DataLoader

**Best for:** Batching and caching database queries during a single GraphQL request. Without DataLoader, each user in a list would trigger a separate database query for their posts.
    
    
    // Without DataLoader: N+1 queries
    // Query: { users { name posts { title } } }
    // Result: 1 query for users + N queries for each user's posts
    
    // With DataLoader: 2 queries total
    const userLoader = new DataLoader(async (userIds) => {
      const posts = await db.posts.findMany({
        where: { authorId: { in: userIds } }
      });
      // Group posts by userId and return in same order as userIds
      return userIds.map(id => posts.filter(p => p.authorId === id));
    });

## Federation for Microservices

**Best for:** Large organizations where different teams own different parts of the graph. Each team owns their subgraph, and a gateway (Apollo Router or GraphOS) composes them into one unified graph.

Component| Responsibility| Example  
---|---|---  
Subgraph| One team's slice of the schema| Users subgraph, Products subgraph, Orders subgraph  
Entity| Type shared across subgraphs via @key directive| User type: @key(fields: "id") in both subgraphs  
Gateway| Routes queries to the right subgraph(s), stitches responses| Apollo Router (Rust, fast), GraphOS  
  
## Performance Checklist

  * **Persisted queries:** Register queries at build time, clients send a hash instead of the full query — reduces bandwidth and blocks arbitrary queries
  * **Query depth limiting:** Reject queries deeper than 7-10 levels to prevent recursive denial-of-service attacks
  * **Query cost analysis:** Assign costs to fields (scalar=1, connection=10) and reject queries exceeding a total cost threshold
  * **Response caching:** Cache resolver results with cache-control headers or Redis; use schema-level caching hints (@cacheControl)
  * **Batched HTTP requests:** Use @apollo/client's batchHttpLink to combine multiple queries into a single HTTP request

**Bottom line:** GraphQL's flexibility is also its biggest risk — without guardrails (depth limiting, cost analysis, persisted queries), a single malicious query can take down your server. Invest in the DataLoader pattern from day one. If you are a single team, start with a monolith schema before reaching for federation. See also: [tRPC vs GraphQL vs REST](</en/compare/trpc-vs-graphql-vs-rest.html>) and [API Design Patterns](</en/tech/api-design-patterns.html>).
