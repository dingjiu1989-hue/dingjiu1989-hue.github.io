---
title: "CDN Architecture"
description: "Edge caching, origin shielding, dynamic content acceleration, and purge strategies for content delivery networks"
date: 2026-04-22
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/cdn-architecture.html
---

# CDN Architecture

Content Delivery Networks (CDNs) distribute content across geographically dispersed servers to reduce latency, offload origin infrastructure, and absorb large-scale traffic spikes. Modern CDNs have evolved from simple static asset caches into sophisticated application delivery platforms that cache dynamic content, execute edge compute, and provide security functions. Understanding CDN architecture is essential for architects designing global-scale systems. 

Edge caching is the foundational CDN capability. Edge servers cache responses from the origin server and serve them directly to users. Cache placement is determined by the user's geographic proximity to the edge node. The CDN's global DNS resolves the domain to the nearest edge server IP based on latency measurements. When a request arrives, the edge server checks its cache — on hit, it serves the cached response instantly; on miss, it fetches from the origin, caches the response, and serves it. 

Origin shielding reduces load on the origin server by consolidating cache misses. Without shielding, every edge node that experiences a cache miss sends a request to the origin simultaneously during a cache fill event. With shielding, edge nodes forward cache misses to a shield or parent layer, which makes a single request to the origin and distributes the response to all requesting edges. This dramatically reduces origin request volume during cache warmup periods. 

Dynamic content acceleration optimizes requests that cannot be cached. The CDN uses optimized routing and TCP optimizations to accelerate uncacheable requests. Route optimization selects the best path from the edge node to the origin, avoiding internet congestion. TCP optimizations include: connection reuse (keep-alive), TLS session resumption, and optimized TCP window sizes. For users far from the origin, dynamic acceleration often provides a 2-5x improvement in connection setup time. 

Edge compute (CDN workers, Lambda@Edge, Cloudflare Workers) extends CDN functionality beyond caching. Code executes at the edge server on each request, enabling: request transformation (header modification, URL rewriting), authentication and authorization checks, A/B testing assignment, and response composition from multiple origins. Edge compute eliminates round trips to the origin for these operations, significantly reducing latency. The compute model is stateless with limited execution time (typically 10-50ms CPU, 30-second wall clock). 

SSL/TLS termination at the edge provides security benefits. The CDN terminates the user's TLS connection, decrypts the request, and can inspect and modify the content. The CDN then creates a new TLS connection to the origin server. This enables the CDN to inspect traffic for threats, inject headers for origin identification, and compress responses. Custom certificates can be uploaded for branded TLS presentation. Automatic certificate provisioning (Let's Encrypt integration) simplifies certificate management. 

Web Application Firewall (WAF) integration at the CDN layer blocks malicious traffic before it reaches the origin. The WAF inspects requests for SQL injection, cross-site scripting, and other attack patterns. Rate limiting at the CDN layer distributes the limiting infrastructure across edge nodes, handling DDoS attacks at the network edge rather than at the origin. Geo-blocking and IP reputation filtering further reduce malicious traffic. The CDN effectively becomes the first line of defense. 

Cache purge strategies determine how quickly updated content reaches users. Hard purge immediately removes cached content — the next request fetches from origin. Soft purge marks content as stale but serves it until fresh content is fetched. Instant purge is essential for breaking news, live events, and security incidents. Purge APIs support URL-precise, directory-pattern, and tag-based invalidation. Most CDNs achieve global purge within seconds, though full propagation can take minutes across thousands of edge nodes. 

Content pre-warming prepares the CDN cache before expected traffic spikes. For product launches, live events, or marketing campaigns, warming the cache ensures the first users receive cached responses rather than origin-cold responses. Pre-warming involves programmatically requesting the relevant URLs from CDN edge nodes in the expected traffic regions. The CDN fetches and caches the responses before user traffic arrives. Pre-warming scripts should simulate the actual user request headers to ensure correct cache behavior. 

Multi-CDN architectures provide redundancy and geographic optimization. Different CDNs may excel in different regions (Asia, South America, Africa). A multi-CDN strategy uses DNS-based traffic steering or client-side load balancing to direct users to the best-performing CDN for their location. Failover between CDNs ensures availability if one provider experiences an outage. The cost is increased operational complexity — managing multiple CDN configurations and monitoring requires mature tooling. 

Performance monitoring includes cache hit ratio, time to first byte (TTFB), and availability per edge region. Cache hit ratio should be monitored per URL pattern — a sudden drop indicates a configuration change or origin issue. TTFB from different regions reveals geographic performance disparities. Availability alerts should trigger when the CDN returns elevated error rates from any region. Real User Monitoring (RUM) provides client-side performance data that complements server-side CDN metrics.

**See also:** [HTTP Caching Architecture](</en/architecture/caching-http.html>), [Caching Strategies](</en/architecture/cache-strategies.html>), [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>).

**See also:** [HTTP Caching Architecture](</en/architecture/caching-http.html>), [Caching Strategies](</en/architecture/cache-strategies.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>)

**See also:** [HTTP Caching Architecture](</en/architecture/caching-http.html>), [Caching Strategies](</en/architecture/cache-strategies.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>)

**See also:** [HTTP Caching Architecture](</en/architecture/caching-http.html>), [Caching Strategies](</en/architecture/cache-strategies.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>)

**See also:** [HTTP Caching Architecture](</en/architecture/caching-http.html>), [Caching Strategies](</en/architecture/cache-strategies.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>)

**See also:** [HTTP Caching Architecture](</en/architecture/caching-http.html>), [Caching Strategies](</en/architecture/cache-strategies.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>)

**See also:** [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>), [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Retry Patterns](</en/architecture/retry-patterns.html>)

**See also:** [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>), [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Retry Patterns](</en/architecture/retry-patterns.html>)

**See also:** [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>), [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Retry Patterns](</en/architecture/retry-patterns.html>)

**See also:** [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>), [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Retry Patterns](</en/architecture/retry-patterns.html>)

**See also:** [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>), [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Retry Patterns](</en/architecture/retry-patterns.html>)

**See also:** [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>), [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Retry Patterns](</en/architecture/retry-patterns.html>)

**See also:** [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>), [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Retry Patterns](</en/architecture/retry-patterns.html>)

**See also:** [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>), [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Retry Patterns](</en/architecture/retry-patterns.html>)

**See also:** [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>), [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Retry Patterns](</en/architecture/retry-patterns.html>)

**See also:** [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>), [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Retry Patterns](</en/architecture/retry-patterns.html>)

**See also:** [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>), [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Retry Patterns](</en/architecture/retry-patterns.html>)
