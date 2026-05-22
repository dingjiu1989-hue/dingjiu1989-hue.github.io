---
title: "API Gateway vs Service Mesh"
description: "Responsibilities, overlap, and deployment patterns for API Gateway and Service Mesh with Istio and Kong examples"
date: 2026-04-24
board: architecture
url: https://aidev.fit/en/architecture/gateway-vs-mesh.html
---

# API Gateway vs Service Mesh

API Gateway and Service Mesh solve different problems but operate in overlapping territory, creating confusion about where each belongs. The API Gateway manages north-south traffic (client to service), while the Service Mesh manages east-west traffic (service to service). Understanding their distinct responsibilities, overlap, and coexistence patterns is essential for a well-architected system. 

The API Gateway is the single entry point for external clients. It handles cross-cutting concerns that belong at the edge of the system: authentication, TLS termination, rate limiting, request validation, response transformation, and API versioning. Kong, Apigee, and AWS API Gateway are common implementations. The gateway may also implement routing, load balancing, and caching for external traffic. It is explicitly part of your application architecture — it knows about your services, routes, and business-level concerns like rate limits per customer plan. 

The Service Mesh operates transparently within the service mesh. It injects sidecar proxies (typically Envoy) alongside each service instance. The sidecar intercepts all network traffic and handles service-level concerns: mTLS between services, fine-grained traffic routing (canary, blue-green), circuit breaking, retries, telemetry collection, and access policies. Istio, Linkerd, and Consul Connect are leading implementations. The mesh is infrastructure-level — services are generally unaware of its existence. 

Overlap occurs in several areas. Both can perform load balancing, traffic routing, retry logic, and telemetry. The key distinction is scope: the gateway manages external traffic with business-aware policies, while the mesh manages internal traffic with infrastructure-level policies. When both are present, decisions about where to place a given function must consider whether it applies to all traffic or only external traffic. 

Practical coexistence patterns have emerged. In the most common deployment, the API Gateway sits at the edge and forwards requests to an ingress gateway (part of the mesh), which then routes to the appropriate service through sidecar proxies. The gateway handles authentication, rate limiting, and request validation. The mesh handles service-to-service mTLS, traffic splitting, and telemetry. This separation of concerns avoids duplicating logic while ensuring each layer handles its appropriate responsibilities. 

A common mistake is treating the Service Mesh as a replacement for the API Gateway. The mesh lacks business-context awareness — it cannot apply rate limits per API key or transform request formats for different client versions. Conversely, using the gateway for internal service-to-service communication creates a central bottleneck that defeats the purpose of microservice autonomy. 

Observability benefits significantly from using both. The gateway provides client-facing metrics: request rates per endpoint, error rates per API key, latency percentiles by client type. The mesh provides service-level metrics: dependency call graphs, error rates per service pair, detailed latency breakdowns including time spent in the proxy. Combined, these give complete visibility from client to database. 

Operational complexity is the primary cost. Operating both systems requires expertise in each. Many teams start with just an API Gateway and add a Service Mesh only when they need advanced traffic management patterns or organization-wide security policies. The decision should be driven by concrete needs — canary deployments across services, zero-trust security requirements, or observability gaps — rather than architectural fashion.
