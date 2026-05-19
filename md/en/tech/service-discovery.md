---
title: "Service Discovery in Microservices"
description: "Explore client-side and server-side discovery patterns with Consul, etcd, and Kubernetes DNS, including health checking and blue-green deployment strategies."
date: 2025-12-31
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/service-discovery.html
---

# Service Discovery in Microservices

Service discovery enables services to find and communicate with each other in a distributed system. In static environments, service locations could be hardcoded. In dynamic environments like Kubernetes, service instances are ephemeral—they come and go, scale up and down, and move between hosts. Service discovery provides a mechanism for locating available service instances.

## The Service Discovery Problem

Service discovery solves two problems. Registration: when a service instance starts, it must register its location and capabilities so other services can find it. Lookup: when a service needs to call another service, it must discover the location of available instances.

Effective service discovery handles dynamic environments. It reacts to instance registration immediately—new instances become available as soon as they register. It handles instance failures—when an instance crashes or becomes unhealthy, it is removed from the available pool. It distributes load across available instances.

## DNS-Based Discovery

DNS-based service discovery uses DNS records to resolve service names to IP addresses. A service named `orders-service` resolves to one or more IP addresses of healthy instances. The DNS server is updated as instances come and go.

The simplest approach uses round-robin DNS. Multiple A records return IP addresses in rotating order, distributing requests across instances. More sophisticated approaches use DNS with health checking—only healthy instances are included in DNS responses.

DNS-based discovery is simple and ubiquitous. Every system has a DNS resolver. However, DNS caching can cause delays in propagating changes. TTL settings must balance responsiveness against DNS query load. DNS also has limited support for advanced load balancing and port-based routing.

## Consul

HashiCorp Consul provides service discovery with health checking, key-value storage, and multi-datacenter support. Services register with Consul agents running on each node. Consul performs health checks and removes unhealthy instances.

Consul uses DNS for backward compatibility: `orders.service.consul` resolves to available instance IPs. It also provides an HTTP API for richer discovery: querying by service name, tags, and health status. Consul's gossip protocol provides distributed health checking without a central server.

Consul supports service mesh integration through Consul Connect, providing mTLS and intentions alongside service discovery. This makes Consul a comprehensive service networking platform for organizations not using Kubernetes.

## Kubernetes Service Discovery

Kubernetes provides built-in service discovery through Services and DNS. Each Service gets a DNS name (e.g., `my-service.namespace.svc.cluster.local`) that resolves to the Pod IPs backing that Service. The kube-proxy component implements load balancing across Pods.

Kubernetes Services support several types: ClusterIP (internal only), NodePort (accessible on each node's IP), LoadBalancer (cloud load balancer), and ExternalName (DNS alias). ClusterIP Services are the default for internal service-to-service communication.

Kubernetes endpoints track Pod health and readiness. Only ready Pods are included in the Service's endpoint list. Liveness probes determine if a Pod is healthy. Readiness probes determine if a Pod should receive traffic.

## Client-Side vs Server-Side Discovery

In client-side discovery, the client directly queries the service registry and selects an instance. The client implements load balancing logic—typically using a library like Netflix Eureka with Ribbon, or Kubernetes client-go's round-robin.

In server-side discovery, the client sends requests to a load balancer or API gateway, which queries the service registry and forwards the request to an available instance. The client does not know about individual instances—it only knows the load balancer address.

## Health Checking

Health checking is integral to service discovery. Services must differentiate between "running" and "ready." A service may be running but not ready to receive traffic. Readiness checks determine traffic eligibility.

Health checks should test meaningful service functionality. A health endpoint that returns 200 immediately upon startup is less useful than one that verifies database connectivity and internal state. Externally accessible health check endpoints enable monitoring systems and load balancers to validate service health.

## When to Use Each Approach

Kubernetes environments should use Kubernetes-native discovery through Services. Non-Kubernetes environments can use Consul for comprehensive discovery with health checking. Simple environments with few services can use DNS-based discovery with health-checked records.

Service discovery is foundational to distributed system reliability. Combined with health checking and load balancing, it enables resilient, self-healing systems that adapt to changing conditions automatically.

**See also:** [Microservices Communication Patterns](</en/tech/microservices-communication.html>), [API Gateway Implementation Guide](</en/tech/api-gateway-implementation.html>), [Kubernetes Security Best Practices](</en/tech/kubernetes-services-security.html>).

**See also:** [Microservices Communication Patterns](</en/tech/microservices-communication.html>), [API Gateway Implementation Guide](</en/tech/api-gateway-implementation.html>), [Distributed Tracing with OpenTelemetry](</en/tech/distributed-tracing.html>)

**See also:** [Microservices Communication Patterns](</en/tech/microservices-communication.html>), [API Gateway Implementation Guide](</en/tech/api-gateway-implementation.html>), [Distributed Tracing with OpenTelemetry](</en/tech/distributed-tracing.html>)

**See also:** [Microservices Communication Patterns](</en/tech/microservices-communication.html>), [API Gateway Implementation Guide](</en/tech/api-gateway-implementation.html>), [Distributed Tracing with OpenTelemetry](</en/tech/distributed-tracing.html>)

**See also:** [Microservices Communication Patterns](</en/tech/microservices-communication.html>), [API Gateway Implementation Guide](</en/tech/api-gateway-implementation.html>), [Distributed Tracing with OpenTelemetry](</en/tech/distributed-tracing.html>)

**See also:** [Microservices Communication Patterns](</en/tech/microservices-communication.html>), [API Gateway Implementation Guide](</en/tech/api-gateway-implementation.html>), [Distributed Tracing with OpenTelemetry](</en/tech/distributed-tracing.html>)

**See also:** [Helm Charts: Kubernetes Package Management](</en/tech/helm-kubernetes-package-management.html>), [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>), [Cloud Cost Optimization Tips](</en/tech/cloud-cost-optimization.html>)

**See also:** [Helm Charts: Kubernetes Package Management](</en/tech/helm-kubernetes-package-management.html>), [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>), [Cloud Cost Optimization Tips](</en/tech/cloud-cost-optimization.html>)

**See also:** [Helm Charts: Kubernetes Package Management](</en/tech/helm-kubernetes-package-management.html>), [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>), [Cloud Cost Optimization Tips](</en/tech/cloud-cost-optimization.html>)

**See also:** [Helm Charts: Kubernetes Package Management](</en/tech/helm-kubernetes-package-management.html>), [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>), [Cloud Cost Optimization Tips](</en/tech/cloud-cost-optimization.html>)

**See also:** [Helm Charts: Kubernetes Package Management](</en/tech/helm-kubernetes-package-management.html>), [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>), [Cloud Cost Optimization Tips](</en/tech/cloud-cost-optimization.html>)

**See also:** [Helm Charts: Kubernetes Package Management](</en/tech/helm-kubernetes-package-management.html>), [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>), [Cloud Cost Optimization Tips](</en/tech/cloud-cost-optimization.html>)
