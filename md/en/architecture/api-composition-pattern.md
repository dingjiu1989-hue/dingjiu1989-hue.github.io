---
title: "API Composition Pattern"
description: "Learn API composition: aggregation, parallel calls, error handling strategies, and cross-service data retrieval"
date: 2026-05-01
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/api-composition-pattern.html
---

# API Composition Pattern

The API composition pattern is a technique for retrieving data that spans multiple services in a microservice architecture. A composer (which could be an API gateway, a dedicated service, or the client itself) calls multiple services and combines their responses into a single, aggregated result. This pattern is the simplest approach to cross-service queries, but it requires careful handling of performance, error, and consistency concerns. 

How API Composition Works 

The composer receives a request that requires data from multiple services. It identifies which services have the needed data, determines whether calls can be parallelized, and makes the necessary requests. As responses arrive, the composer combines them into the requested format and returns the result. 

For example, to display an order detail page, the composer might call the Order service for order data, the Payment service for payment status, the Shipping service for tracking information, and the Product service for product details. It combines these responses into a single view model for the client. 

Parallel vs Sequential Calls 

The composer should make parallel calls whenever possible to minimize latency. Calls that are independent can be issued simultaneously. Calls where one depends on the output of another must be sequential. 

Parallel execution reduces response time to the slowest service call rather than the sum of all calls. However, the composer needs thread or coroutine management for concurrent calls. Async/await patterns, futures, and reactive streams are common implementation techniques. 

Sequential calls are needed when the composer must use the response from one service to construct the request for another. For example, fetching user details to determine which group they belong to, then fetching group-specific permissions. These dependencies should be minimized through service design. 

Error Handling 

Error handling in API composition requires a strategy for partial failures. When one of multiple service calls fails, the composer can fail the entire request, return partial data, or substitute default values. 

Failing fast is often the safest approach for read operations, especially when the client expects complete data. The composer should cancel in-flight requests for services that are no longer needed. 

Returning partial data is appropriate when the missing data is non-critical. The response can indicate which data is missing, allowing the client to display what is available. This approach is common in dashboards where some panels may fail independently. 

Default values or cached data can substitute for service failures when the composer has reasonable defaults. This provides the best user experience but risks showing stale or incorrect data. 

Performance Optimization 

Performance optimization for API composition focuses on reducing the number of calls and minimizing their latency. Batch endpoints that accept multiple IDs reduce N+1 query problems. Instead of calling the Product service once per product ID, the composer calls a batch endpoint with all product IDs. 

Caching is also effective. Frequently accessed data that changes slowly (product details, user profiles) can be cached in the composer. This reduces the number of service calls and improves response times. Cache invalidation must be managed, typically through TTL or event-driven invalidation. 

The composer can also prefetch data it expects to need based on the request. If a request for user data typically also needs group membership data, the composer can fetch both in parallel rather than discovering the need for group data later. 

When to Use Composition 

API composition is appropriate for simple aggregations where the relationships between data sources are straightforward and performance requirements are moderate. It is the simplest cross-service query pattern and the easiest to implement and understand. 

Composition becomes problematic when aggregations are complex, involve large datasets, or require joins that cannot be efficiently performed in memory. For these cases, the CQRS or materialized view patterns are more appropriate. 

Implementation considerations include the location of the composer. API gateways often handle simple composition. Dedicated composition services handle more complex logic. Client-side composition works for simple cases but couples the client to multiple services. 

API composition is a fundamental pattern in microservice architectures. It provides a straightforward way to serve data from multiple services without the complexity of event-driven synchronization or dedicated query services. When performance and error handling are carefully managed, composition is an effective tool for cross-service data retrieval.

**See also:** [API Composition and Aggregation](</en/architecture/api-composition.html>), [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>).

**See also:** [API Composition and Aggregation](</en/architecture/api-composition.html>), [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>)

**See also:** [API Composition and Aggregation](</en/architecture/api-composition.html>), [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [API Gateway Patterns](</en/architecture/api-gateway-patterns.html>)

**See also:** [API Composition and Aggregation](</en/architecture/api-composition.html>), [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Backend for Frontend (BFF) Pattern](</en/architecture/backend-for-frontend.html>)

**See also:** [API Composition and Aggregation](</en/architecture/api-composition.html>), [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Backend for Frontend (BFF) Pattern](</en/architecture/backend-for-frontend.html>)

**See also:** [API Composition and Aggregation](</en/architecture/api-composition.html>), [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Backend for Frontend (BFF) Pattern](</en/architecture/backend-for-frontend.html>)

**See also:** [Zero-Downtime Database Migrations](</en/architecture/database-migration-zero-downtime.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>)

**See also:** [Zero-Downtime Database Migrations](</en/architecture/database-migration-zero-downtime.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>)

**See also:** [Zero-Downtime Database Migrations](</en/architecture/database-migration-zero-downtime.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>)

**See also:** [Zero-Downtime Database Migrations](</en/architecture/database-migration-zero-downtime.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>)

**See also:** [Zero-Downtime Database Migrations](</en/architecture/database-migration-zero-downtime.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>)

**See also:** [Zero-Downtime Database Migrations](</en/architecture/database-migration-zero-downtime.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>)

**See also:** [Zero-Downtime Database Migrations](</en/architecture/database-migration-zero-downtime.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>)

**See also:** [Zero-Downtime Database Migrations](</en/architecture/database-migration-zero-downtime.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>)

**See also:** [Zero-Downtime Database Migrations](</en/architecture/database-migration-zero-downtime.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>)

**See also:** [Zero-Downtime Database Migrations](</en/architecture/database-migration-zero-downtime.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>)
