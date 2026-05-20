---
title: "Zero-Downtime Deployment Strategies"
description: "Rolling, blue-green, canary deployments, feature flags, database migrations for zero-downtime releases"
date: 2026-05-01
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/zero-downtime-deployment.html
---

# Zero-Downtime Deployment Strategies

Zero-downtime deployment ensures that application updates occur without interrupting user-facing service. As systems grow from hobby projects to business-critical platforms, deployment windows become unacceptable. Modern deployment strategies provide multiple approaches to achieving seamless updates, each with different tradeoffs in complexity, cost, and risk. 

Rolling deployment replaces instances one at a time. The orchestrator spins up a new instance with the new version, health-checks it, and once healthy, terminates an old instance. This continues until all instances are updated. Rolling deployments require no additional infrastructure and work well with horizontal scaling. The disadvantage is backward compatibility issues during the update window — both old and new versions serve traffic simultaneously, so API changes must be backward compatible. 

Blue-green deployment maintains two complete environments: blue (current) and green (next). The new version is deployed to the green environment. Once fully deployed and tested, the router or load balancer switches traffic from blue to green. If issues arise, traffic can be instantly reverted to blue. Blue-green deployment eliminates the mixed-version problem — all traffic goes to one version at a time. The cost is double infrastructure during deployment and the need for environments that can handle full production load. 

Canary deployment releases the new version to a small subset of traffic initially, monitors for issues, and gradually increases the traffic percentage. This provides the safest rollout — issues are detected with minimal user impact. Canary deployments require sophisticated traffic routing (request-based, not connection-based) and monitoring to detect regressions. Service mesh technologies like Istio make canary deployments practical by providing fine-grained traffic splitting based on headers, cookies, or percentages. 

Feature flags provide deployment independence from release. The code for a new feature is deployed to production behind a feature flag that disables it. Later, the flag is enabled gradually or instantly. This decouples deployment (moving code to production) from release (making features available to users). Feature flags enable canary-like testing at the feature level, instant rollbacks (flip the flag off), and environment-specific behavior. LaunchDarkly and Flagsmith provide managed feature flag platforms. 

Database migrations are the hardest part of zero-downtime deployment and are covered separately, but the key principle here is backward compatibility. The old code must work with the new schema, and the new code must work with the old schema (during rolling upgrades). This requires expand-contract migration patterns where columns are added before they are used, old columns remain until all instances are updated, and data transformations happen in steps. 

Readiness and liveness probes must be version-aware. A new instance should not be considered ready until its dependencies are compatible and its data migrations are complete. The probe for the old version should remain healthy even as the migration progresses. Kubernetes lifecycle hooks can coordinate this. 

Health check integration during deployment is critical. Monitor error rates, latency percentiles, and instance health throughout the deployment. Automatically rollback if error rates exceed a threshold. Blue-green and canary deployments benefit from automated smoke tests after each stage before proceeding to the next. 

Session management requires attention during deployments. In-memory sessions are lost when instances restart. Sessions should be stored in a shared session store (Redis, database) that survives instance termination. Alternatively, use stateless sessions with client-side tokens. WebSocket connections must be re-established if their instance is terminated — the client should implement reconnection logic. 

The choice of deployment strategy depends on application architecture, team maturity, and risk tolerance. Rolling deployments suit simple stateless services. Blue-green deployments fit services requiring predictable cutover times. Canary deployments are appropriate for high-risk, high-traffic services where gradual rollout provides the best safety profile. Many organizations combine approaches — using rolling deployments for routine updates and canary for major releases.

**See also:** [Blue-Green Deployment Strategy](</en/architecture/blue-green-deployment.html>), [Canary Deployments for Safe Releases](</en/architecture/canary-deployment.html>), [Zero-Downtime Database Migrations](</en/architecture/database-migration-zero-downtime.html>).

**See also:** [Blue-Green Deployment Strategy](</en/architecture/blue-green-deployment.html>), [Canary Deployments for Safe Releases](</en/architecture/canary-deployment.html>), [Zero-Downtime Database Migrations](</en/architecture/database-migration-zero-downtime.html>)

**See also:** [Blue-Green Deployment Strategy](</en/architecture/blue-green-deployment.html>), [Canary Deployments for Safe Releases](</en/architecture/canary-deployment.html>), [Zero-Downtime Database Migrations](</en/architecture/database-migration-zero-downtime.html>)

**See also:** [Blue-Green Deployment Strategy](</en/architecture/blue-green-deployment.html>), [Canary Deployments for Safe Releases](</en/architecture/canary-deployment.html>), [Zero-Downtime Database Migrations](</en/architecture/database-migration-zero-downtime.html>)

**See also:** [Blue-Green Deployment Strategy](</en/architecture/blue-green-deployment.html>), [Canary Deployments for Safe Releases](</en/architecture/canary-deployment.html>), [Zero-Downtime Database Migrations](</en/architecture/database-migration-zero-downtime.html>)

**See also:** [Blue-Green Deployment Strategy](</en/architecture/blue-green-deployment.html>), [Canary Deployments for Safe Releases](</en/architecture/canary-deployment.html>), [Zero-Downtime Database Migrations](</en/architecture/database-migration-zero-downtime.html>)

**See also:** [CDN Architecture](</en/architecture/cdn-architecture.html>), [Cost Per Request Modeling](</en/architecture/cost-per-request.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>)

**See also:** [CDN Architecture](</en/architecture/cdn-architecture.html>), [Cost Per Request Modeling](</en/architecture/cost-per-request.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>)

**See also:** [CDN Architecture](</en/architecture/cdn-architecture.html>), [Cost Per Request Modeling](</en/architecture/cost-per-request.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>)

**See also:** [CDN Architecture](</en/architecture/cdn-architecture.html>), [Cost Per Request Modeling](</en/architecture/cost-per-request.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>)

**See also:** [CDN Architecture](</en/architecture/cdn-architecture.html>), [Cost Per Request Modeling](</en/architecture/cost-per-request.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>)

**See also:** [CDN Architecture](</en/architecture/cdn-architecture.html>), [Cost Per Request Modeling](</en/architecture/cost-per-request.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>)

**See also:** [CDN Architecture](</en/architecture/cdn-architecture.html>), [Cost Per Request Modeling](</en/architecture/cost-per-request.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>)

**See also:** [CDN Architecture](</en/architecture/cdn-architecture.html>), [Cost Per Request Modeling](</en/architecture/cost-per-request.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>)

**See also:** [CDN Architecture](</en/architecture/cdn-architecture.html>), [Cost Per Request Modeling](</en/architecture/cost-per-request.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>)
