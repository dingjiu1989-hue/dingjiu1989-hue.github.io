---
title: "HTTP Caching Architecture"
description: "Cache-Control, ETags, CDN caching, stale-while-revalidate, and cache invalidation strategies"
date: 2026-04-21
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/caching-http.html
---

# HTTP Caching Architecture

HTTP caching is the most cost-effective performance optimization available. A single cache hit eliminates an entire request path through the network, load balancers, application servers, and databases. The HTTP specification provides a comprehensive caching framework through headers, validation mechanisms, and extension directives. Understanding and applying these correctly is essential for building performant web systems. 

Cache-Control headers are the primary mechanism for controlling HTTP caching behavior. The max-age directive specifies the maximum time in seconds that a response can be cached. The s-maxage directive overrides max-age for shared caches (CDNs, reverse proxies). The private directive limits caching to the browser (no shared caching). The public directive allows any cache, including shared ones. The no-cache directive requires revalidation with the origin server before serving from cache. The no-store directive prevents any caching. 

ETags provide cache validation. An ETag is a unique identifier for a specific version of a resource. When a client has a cached response with an ETag, it sends If-None-Match with that ETag on subsequent requests. If the resource has not changed, the server returns 304 Not Modified with an empty body. This saves bandwidth even when the cached response needs revalidation. Strong ETags change when the content changes. Weak ETags (prefixed with W/) change when the semantic meaning changes but not necessarily the byte representation. 

Conditional requests with If-Modified-Since and If-None-Match provide similar validation. Last-Modified headers provide a timestamp that the client can use with If-Modified-Since. However, timestamps are less reliable than ETags — they have second-level granularity, can be inconsistent across servers, and do not detect changes that occur within the same second. ETags are preferred for accuracy; Last-Modified serves as a fallback. 

The stale-while-revalidate directive enables serving stale content while asynchronously fetching fresh content. When a cache has a response with max-age=3600 and stale-while-revalidate=86400, for the first hour the fresh content is served. For the next 24 hours, stale content is served while the cache fetches fresh content in the background. This dramatically improves perceived latency — users never wait for cache misses. The stale-if-error extension provides stale content when the origin server is unavailable. 

CDN caching adds a distributed layer between users and the origin server. CDNs cache responses at edge locations geographically close to users. Cache-Control headers control what the CDN caches and for how long. The CDN respects Cache-Control directives but may override them with CDN-specific settings. CDN cache behavior should be tested — some CDNs ignore private headers on authenticated responses, accidentally caching user-specific content. 

Cache invalidation strategies must handle dynamic content. Purge-based invalidation explicitly removes cached content by URL or tag. The CDN API provides purge endpoints for targeted invalidation. Tag-based invalidation associates cache entries with tags and purges all entries with a given tag. For example, all product page entries carry a "product:123" tag, and updating product 123 triggers a tag-based purge. Pattern-based invalidation uses URL patterns — /api/products/* purges all product API responses. 

Surrogate keys (cache tags) extend cache invalidation for dynamic content. The origin server includes a Surrogate-Key header with space-separated tags. The CDN associates each cached response with these tags. When the origin sends a PURGE request with a tag, all responses with that tag are invalidated. This enables fine-grained invalidation — updating a product's price invalidates only the affected product pages, not the entire product catalog cache. 

Cache hierarchies combine browser cache, CDN cache, and origin cache. Browser cache serves the fastest response (zero network latency) but has limited capacity and no sharing. CDN cache serves regional users with low latency and shares across users. Origin cache (Redis, Memcached) serves as the application-level cache, reducing database load. Each layer is a potential cache hit that eliminates the need to go deeper. The Cache-Control headers should account for the full hierarchy. 

Versioned URLs eliminate the need for cache invalidation for static assets. By including a content hash in the URL (styles.a3b4c5.css, app.6d7e8f.js), each version of the asset has a unique URL. These assets can be cached with max-age=31536000 (one year) because the URL changes when the content changes. This is the most reliable caching strategy — CDN cost is minimized, and cache invalidation is automatic. 

Cache hit ratio is the primary metric. Monitor cache hit ratio at each layer: browser cache, CDN cache, origin cache. A low CDN cache hit ratio indicates responses that are not cacheable or have short TTLs. A low origin cache hit ratio indicates application-level caching issues. The aggregate cache hit ratio across all layers represents the fraction of requests that never reach the origin server, directly translating to infrastructure cost savings and latency reduction.

**See also:** [CDN Architecture](</en/architecture/cdn-architecture.html>), [Caching Strategies](</en/architecture/cache-strategies.html>), [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>).

**See also:** [CDN Architecture](</en/architecture/cdn-architecture.html>), [Caching Strategies](</en/architecture/cache-strategies.html>), [Caching Strategies and Patterns in Distributed Systems](</en/architecture/caching-strategies.html>)

**See also:** [CDN Architecture](</en/architecture/cdn-architecture.html>), [Caching Strategies](</en/architecture/cache-strategies.html>), [Caching Strategies and Patterns in Distributed Systems](</en/architecture/caching-strategies.html>)

**See also:** [CDN Architecture](</en/architecture/cdn-architecture.html>), [Caching Strategies](</en/architecture/cache-strategies.html>), [Caching Strategies and Patterns in Distributed Systems](</en/architecture/caching-strategies.html>)

**See also:** [CDN Architecture](</en/architecture/cdn-architecture.html>), [Caching Strategies](</en/architecture/cache-strategies.html>), [Caching Strategies and Patterns in Distributed Systems](</en/architecture/caching-strategies.html>)

**See also:** [CDN Architecture](</en/architecture/cdn-architecture.html>), [Caching Strategies](</en/architecture/cache-strategies.html>), [Caching Strategies and Patterns in Distributed Systems](</en/architecture/caching-strategies.html>)

**See also:** [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>), [Cost Per Request Modeling](</en/architecture/cost-per-request.html>)

**See also:** [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>), [Cost Per Request Modeling](</en/architecture/cost-per-request.html>)

**See also:** [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>), [Cost Per Request Modeling](</en/architecture/cost-per-request.html>)
