---
title: "API Composition and Aggregation"
description: "API aggregation layer, GraphQL federation, Backend for Frontend pattern, and service aggregation strategies"
date: 2026-04-21
board: architecture
url: https://aidev.fit/en/architecture/api-composition.html
---

# API Composition and Aggregation

API composition addresses a fundamental challenge in distributed architectures: how to aggregate data from multiple backend services into a single, efficient client response. In a monolithic application, the database can join tables across domains with a single query. In a microservice architecture, each service owns its data, and aggregation must happen at the application layer. Three primary patterns address this: the API composition layer, GraphQL federation, and the Backend for Frontend (BFF) pattern. 

The API composition layer is a dedicated service that orchestrates calls to downstream services, aggregates results, and returns a unified response. It is conceptually simple: the composer receives a request, calls the relevant services in parallel where possible, merges the data, and responds. The challenge lies in handling partial failures. If one of five downstream services fails, does the entire request fail, or does the composer return partial data? Strategies include timeout handling with fallback responses, circuit breaker integration, and return of partial results with error indicators. 

The N+1 query problem manifests in API composition when the composer fetches a list from one service, then iterates over each item to fetch details from another. Batch endpoints or GraphQL DataLoader patterns mitigate this by collecting keys and making batched requests. For example, instead of fetching each order's customer details individually, the composer collects all customer IDs and makes a single batch request to the customer service. 

GraphQL federation provides an alternative approach where multiple services expose their own GraphQL schemas, and a federation gateway merges them into a unified graph. Each service contributes types and fields to the global schema. The gateway resolves queries by delegating field resolution to the appropriate service. Apollo Federation and Netflix's DGS framework are popular implementations. Federation eliminates the need for a separate aggregation service while providing typed, flexible queries that clients can tailor to their needs. The trade-off is increased complexity in schema management and the challenge of distributed field resolution performance. 

The Backend for Frontend (BFF) pattern creates dedicated backend services for each client type. A mobile BFF might return a coarser payload optimized for bandwidth, while a web BFF returns a richer payload suitable for desktop browsers. Each BFF owns its aggregation logic, reducing the risk of breaking one client's experience when optimizing for another. The BFF pattern often incorporates API composition as one of its responsibilities, but extends it to include client-specific concerns like data transformation, caching strategy, and authentication. 

Data consistency challenges arise in all composition patterns. When the composer aggregates data from multiple services, the data may be from different points in time. A product name fetched from the catalog service may have been updated milliseconds after the price was fetched from the pricing service. The composer must decide whether eventual consistency is acceptable or whether causal consistency guarantees are needed, which significantly complicates the architecture. 

Caching at the composition layer can dramatically improve performance and reduce downstream load. The composer can cache aggregated responses or its individual downstream calls. Cache invalidation becomes complex when data changes affect multiple cached responses — a product price change may invalidate cache entries in the product detail, search results, and order history compositions. 

The choice between these patterns depends on client diversity, team structure, and performance requirements. API composition suits homogeneous clients and simpler architectures. GraphQL federation excels when clients need flexible data shapes. BFF shines with diverse client platforms and independent team ownership of client experiences.

**See also:** [API Composition Pattern](</en/architecture/api-composition-pattern.html>), [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>), [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>).

**See also:** [API Composition Pattern](</en/architecture/api-composition-pattern.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>), [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>)

**See also:** [API Composition Pattern](</en/architecture/api-composition-pattern.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>), [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>)

**See also:** [API Composition Pattern](</en/architecture/api-composition-pattern.html>), [Backend for Frontend (BFF) Pattern](</en/architecture/backend-for-frontend.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>)

**See also:** [API Composition Pattern](</en/architecture/api-composition-pattern.html>), [Backend for Frontend (BFF) Pattern](</en/architecture/backend-for-frontend.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>)

**See also:** [API Composition Pattern](</en/architecture/api-composition-pattern.html>), [Backend for Frontend (BFF) Pattern](</en/architecture/backend-for-frontend.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>)

**See also:** [Throttling Pattern for System Protection](</en/architecture/throttling-pattern.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [CDN Architecture](</en/architecture/cdn-architecture.html>)

**See also:** [Throttling Pattern for System Protection](</en/architecture/throttling-pattern.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [CDN Architecture](</en/architecture/cdn-architecture.html>)

**See also:** [Throttling Pattern for System Protection](</en/architecture/throttling-pattern.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [CDN Architecture](</en/architecture/cdn-architecture.html>)

**See also:** [Throttling Pattern for System Protection](</en/architecture/throttling-pattern.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [CDN Architecture](</en/architecture/cdn-architecture.html>)

**See also:** [Throttling Pattern for System Protection](</en/architecture/throttling-pattern.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [CDN Architecture](</en/architecture/cdn-architecture.html>)

**See also:** [Throttling Pattern for System Protection](</en/architecture/throttling-pattern.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [CDN Architecture](</en/architecture/cdn-architecture.html>)

**See also:** [Throttling Pattern for System Protection](</en/architecture/throttling-pattern.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [CDN Architecture](</en/architecture/cdn-architecture.html>)

**See also:** [Throttling Pattern for System Protection](</en/architecture/throttling-pattern.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [CDN Architecture](</en/architecture/cdn-architecture.html>)

**See also:** [Throttling Pattern for System Protection](</en/architecture/throttling-pattern.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [CDN Architecture](</en/architecture/cdn-architecture.html>)

**See also:** [Throttling Pattern for System Protection](</en/architecture/throttling-pattern.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [CDN Architecture](</en/architecture/cdn-architecture.html>)

**See also:** [Throttling Pattern for System Protection](</en/architecture/throttling-pattern.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [CDN Architecture](</en/architecture/cdn-architecture.html>)

**See also:** [Throttling Pattern for System Protection](</en/architecture/throttling-pattern.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [CDN Architecture](</en/architecture/cdn-architecture.html>)

**See also:** [Throttling Pattern for System Protection](</en/architecture/throttling-pattern.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [CDN Architecture](</en/architecture/cdn-architecture.html>)

**See also:** [Throttling Pattern for System Protection](</en/architecture/throttling-pattern.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [CDN Architecture](</en/architecture/cdn-architecture.html>)

**See also:** [Throttling Pattern for System Protection](</en/architecture/throttling-pattern.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [CDN Architecture](</en/architecture/cdn-architecture.html>)

**See also:** [Throttling Pattern for System Protection](</en/architecture/throttling-pattern.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [CDN Architecture](</en/architecture/cdn-architecture.html>)

**See also:** [Throttling Pattern for System Protection](</en/architecture/throttling-pattern.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [CDN Architecture](</en/architecture/cdn-architecture.html>)
