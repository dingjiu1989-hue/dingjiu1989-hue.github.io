---
title: "Global Traffic Routing"
description: "DNS-based routing, Anycast, global load balancers, latency-based routing, and multi-region traffic management"
date: 2026-04-24
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/global-traffic-routing.html
---

# Global Traffic Routing

Global traffic routing directs user requests to the optimal backend location based on geography, latency, capacity, and availability. As applications scale to serve users worldwide, the routing infrastructure becomes a critical architectural component that determines latency, reliability, and operational flexibility. Multiple routing techniques — DNS-based, Anycast-based, and application-level — combine to provide comprehensive global traffic management. 

DNS-based routing is the most common approach for directing traffic to the nearest data center. The authoritative DNS server for the domain returns different IP addresses based on the requesting resolver's geographic location or network latency. AWS Route 53, Google Cloud DNS, and Azure Traffic Manager implement latency-based routing by maintaining latency tables between DNS resolvers and application endpoints. When a user in Europe requests the domain, the DNS returns the IP of the European data center. 

Latency-based routing uses real-time measurements to direct users to the fastest endpoint. The DNS service continuously probes each endpoint from multiple vantage points and builds a latency map. When a DNS query arrives, the resolver's approximate location is determined (from its IP address or EDNS Client Subnet), and the lowest-latency endpoint is returned. The latency map updates as network conditions change — an endpoint that becomes degraded will gradually receive less traffic as its measured latency increases. 

Geo-proximity routing directs users based on physical distance rather than network latency. The DNS service calculates the distance between the user's resolver and each endpoint using geographic coordinates. The closest endpoint receives the traffic. Geo-proximity is simpler than latency-based routing but less accurate — physical proximity does not always correlate with network performance, especially in regions with circuitous internet routes. 

Anycast routing advertises the same IP address from multiple locations. The internet's Border Gateway Protocol (BGP) naturally routes each user to the nearest advertising location. Anycast provides automatic failover — if one location goes offline, BGP withdraws the route, and traffic automatically shifts to the next nearest location. Anycast is used by CDNs, DNS root servers, and global load balancers. The trade-off is that BGP routing is based on AS-path length, which approximates but does not guarantee optimal latency. 

Global load balancers (GLBs) sit above regional load balancers and provide cross-region traffic distribution. The GLB monitors the health and capacity of each regional deployment. It can implement weighted distribution for gradual traffic shifting (e.g., 90% us-east-1, 10% us-west-2 during a regional migration), failover (all traffic to us-west-2 if us-east-1 is unhealthy), and load-based distribution (direct traffic away from overloaded regions). 

Health-based routing removes unhealthy endpoints from the traffic pool. Each backend region is probed with health checks. If a region returns errors or is unresponsive, the routing system stops directing traffic to it. DNS-based health routing relies on DNS TTL — when a region fails, the DNS records are updated to remove or deprioritize the unhealthy endpoint. Clients with cached DNS records may continue hitting the failed region until the TTL expires, which is why short TTLs (60-120 seconds) are used for health-based routing. 

Active-active vs active-passive configurations determine capacity utilization. Active-active distributes traffic across all available regions, maximizing capacity and providing immediate failover capacity. Active-passive keeps one region in standby, accepting no traffic until the primary fails. Active-active requires application-level support — data must be replicated with conflict resolution, sessions must be shareable across regions, and deployments must be synchronized. Active-passive is simpler but wastes standby capacity. 

Sticky sessions complicate global routing. If user sessions are stored locally in one region, routing that user to another region breaks their session. Solutions include: centralized session stores (Redis global, database-backed sessions), client-side sessions (JWT tokens with all session data), or session migration (transfer session state between regions on routing change). The simplest approach is to avoid session locality — design services as stateless with all state in shared data stores. 

Regional failover testing should be regular and automated. Chaos engineering exercises should verify that global routing correctly detects regional failures and shifts traffic. The failover should be tested in both directions and at different times of day to verify capacity assumptions. DNS propagation delays (due to TTL and resolver caching) should be measured and accounted for in recovery time objectives. Automated failover with manual approval provides a balance between speed and safety. 

Multi-cloud routing adds another dimension of complexity. Traffic must be routed not just to the nearest data center but to the nearest data center in the optimal cloud provider. This introduces cloud provider selection based on pricing, available services, and contractual commitments. Multi-cloud routing typically uses DNS-based steering with cloud-specific health checks and capacity tracking. The routing policy should account for data transfer costs between clouds and regions, which can be significant.

**See also:** [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [A/B Testing Infrastructure](</en/architecture/a-b-testing-infrastructure.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>).

**See also:** [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [A/B Testing Infrastructure](</en/architecture/a-b-testing-infrastructure.html>), [Distributed Locking Mechanisms](</en/architecture/distributed-locking.html>)

**See also:** [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [A/B Testing Infrastructure](</en/architecture/a-b-testing-infrastructure.html>), [Distributed Locking Mechanisms](</en/architecture/distributed-locking.html>)

**See also:** [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [A/B Testing Infrastructure](</en/architecture/a-b-testing-infrastructure.html>), [Distributed Locking Mechanisms](</en/architecture/distributed-locking.html>)

**See also:** [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [A/B Testing Infrastructure](</en/architecture/a-b-testing-infrastructure.html>), [Distributed Locking Mechanisms](</en/architecture/distributed-locking.html>)

**See also:** [Multi-Tenancy Architecture](</en/architecture/multi-tenancy.html>), [A/B Testing Infrastructure](</en/architecture/a-b-testing-infrastructure.html>), [Distributed Locking Mechanisms](</en/architecture/distributed-locking.html>)

**See also:** [Choreography Patterns](</en/architecture/choreography-patterns.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)

**See also:** [Choreography Patterns](</en/architecture/choreography-patterns.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)

**See also:** [Choreography Patterns](</en/architecture/choreography-patterns.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)

**See also:** [Choreography Patterns](</en/architecture/choreography-patterns.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)

**See also:** [Choreography Patterns](</en/architecture/choreography-patterns.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)

**See also:** [Choreography Patterns](</en/architecture/choreography-patterns.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)

**See also:** [Choreography Patterns](</en/architecture/choreography-patterns.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)

**See also:** [Choreography Patterns](</en/architecture/choreography-patterns.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)

**See also:** [Choreography Patterns](</en/architecture/choreography-patterns.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)

**See also:** [Choreography Patterns](</en/architecture/choreography-patterns.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)

**See also:** [Choreography Patterns](</en/architecture/choreography-patterns.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)

**See also:** [Choreography Patterns](</en/architecture/choreography-patterns.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)

**See also:** [Choreography Patterns](</en/architecture/choreography-patterns.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)

**See also:** [Choreography Patterns](</en/architecture/choreography-patterns.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>)
