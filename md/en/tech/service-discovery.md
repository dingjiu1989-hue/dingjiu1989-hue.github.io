---
title: "Service Discovery in Microservices"
description: "Explore client-side and server-side discovery patterns with Consul, etcd, and Kubernetes DNS, including health checking and blue-green deployment strategies."
date: 2026-05-12
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/service-discovery.html
---

## Introduction

Service discovery is the mechanism by which microservices locate each other on a network. In dynamic environments where containers come and go, IP addresses and ports cannot be hard-coded. A robust discovery layer is essential for resilient, scalable microservice communication. This article covers the core patterns, tools, and best practices for implementing service discovery in production.

## Client-Side vs Server-Side Discovery

### Client-Side Discovery

The client queries a service registry directly and handles load balancing. This pattern is lightweight but requires service-specific client logic:

```python
import requests
from consul import Consul

class ServiceClient:
    def __init__(self):
        self.consul = Consul(host="consul.service.consul")

    def get_service_url(self, service_name: str) -> str:
        _, services = self.consul.catalog.service(service_name)
        if not services:
            raise Exception(f"Service {service_name} not found")
        # Pick a healthy instance
        instance = services[0]
        return f"http://{instance['ServiceAddress']}:{instance['ServicePort']}"

    def call_user_service(self, user_id: str):
        base_url = self.get_service_url("user-service")
        resp = requests.get(f"{base_url}/users/{user_id}")
        return resp.json()
```

### Server-Side Discovery

A load balancer or gateway handles discovery transparently. Clients only know the gateway address:

```yaml
# Kubernetes: Service handles DNS-based discovery
apiVersion: v1
kind: Service
metadata:
  name: user-service
spec:
  selector:
    app: user-service
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
---
apiVersion: v1
kind: EndpointSlice
metadata:
  labels:
    kubernetes.io/service-name: user-service
addressType: IPv4
endpoints:
  - addresses: ["10.0.1.5"]
    conditions:
      ready: true
  - addresses: ["10.0.1.6"]
    conditions:
      ready: true
ports:
  - name: http
    protocol: TCP
    port: 8080
```

## Consul

HashiCorp Consul provides service registration, health checking, and a distributed key-value store:

```hcl
# service registration configuration
service {
  name = "payment-service"
  id = "payment-service-v1"
  port = 9090
  tags = ["v1", "production", "critical"]

  check {
    id       = "payment-health"
    name     = "Payment Service Health"
    http     = "http://localhost:9090/health"
    method   = "GET"
    interval = "10s"
    timeout  = "2s"
    deregister_critical_service_after = "5m"
  }

  connect {
    sidecar_service {
      proxy {
        upstreams {
          destination_name = "order-service"
          local_bind_port  = 8080
        }
      }
    }
  }
}
```

Programmatic registration via the API:

```go
package main

import (
    "github.com/hashicorp/consul/api"
)

func registerService() {
    client, _ := api.NewClient(api.DefaultConfig())
    registration := &api.AgentServiceRegistration{
        ID:   "order-svc-1",
        Name: "order-service",
        Port: 8080,
        Check: &api.AgentServiceCheck{
            HTTP:     "http://localhost:8080/healthz",
            Interval: "10s",
            DeregisterCriticalServiceAfter: "3m",
        },
    }
    client.Agent().ServiceRegister(registration)
}
```

## etcd

etcd offers a strongly consistent key-value store often used for service discovery in Kubernetes (it powers Kubernetes itself):

```go
package main

import (
    "context"
    "clientv3" "go.etcd.io/etcd/client/v3"
    "time"
)

func registerWithLease() {
    cli, _ := clientv3.New(clientv3.Config{
        Endpoints:   []string{"localhost:2379"},
        DialTimeout: 5 * time.Second,
    })

    lease, _ := cli.Grant(context.Background(), 10) // 10-second TTL
    key := "/services/payment-service/instance-1"
    value := `{"address": "10.0.1.10", "port": 9090}`

    cli.Put(context.Background(), key, value,
        clientv3.WithLease(lease.ID))

    // Keep alive
    ch, _ := cli.KeepAlive(context.Background(), lease.ID)
    go func() {
        for range ch {
            // Lease refreshed
        }
    }()
}

func discoverService(name string) []string {
    cli, _ := clientv3.New(clientv3.Config{
        Endpoints: []string{"localhost:2379"},
    })
    resp, _ := cli.Get(context.Background(),
        "/services/"+name, clientv3.WithPrefix())

    var instances []string
    for _, kv := range resp.Kvs {
        instances = append(instances, string(kv.Value))
    }
    return instances
}
```

## Health Checking Strategies

Effective health checks prevent routing traffic to unhealthy instances:

```yaml
# Kubernetes: multi-probe health checking
apiVersion: v1
kind: Pod
metadata:
  name: web-app
spec:
  containers:
    - name: app
      image: web-app:latest
      livenessProbe:         # Restart if fails
        httpGet:
          path: /healthz
          port: 8080
        initialDelaySeconds: 10
        periodSeconds: 5
        failureThreshold: 3
      readinessProbe:        # Remove from service if fails
        httpGet:
          path: /ready
          port: 8080
        periodSeconds: 2
        failureThreshold: 1
      startupProbe:          # Delay other probes
        httpGet:
          path: /startup
          port: 8080
        initialDelaySeconds: 15
        periodSeconds: 5
        failureThreshold: 30
```

Consul gRPC checks for streaming services:

```hcl
check {
  id       = "grpc-health"
  name     = "gRPC Health Check"
  grpc     = "localhost:50051"
  grpc_use_tls = true
  interval = "15s"
  timeout  = "3s"
  notes    = "Uses gRPC health checking protocol"
}
```

## Blue-Green Deployments with Discovery

Service discovery enables seamless traffic switching during blue-green deployments:

```hcl
# Consul: traffic splitting via service resolver
kind = "service-resolver"
name = "web-service"

subsets = {
  blue = {
    filter = "Service.Meta.version == blue"
  }
  green = {
    filter = "Service.Meta.version == green"
  }
}

default_subset = "blue"
```

Switch traffic atomically:

```bash
# Switch from blue to green
consul config write - <<EOF
kind = "service-resolver"
name = "web-service"
default_subset = "green"
EOF
```

## Registry Patterns

Choose your registration approach based on operational maturity:

**Self-Registration**: Services register themselves on startup and deregister on shutdown. Simplest but requires service frameworks to implement registration logic.

**Third-Party Registration**: An external process (like Kubernetes watchers or Kubernetes itself) monitors instances and updates the registry. More resilient but adds operational complexity.

```yaml
# Kubernetes: third-party via Endpoint Controller
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-v2
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
      version: v2
  template:
    metadata:
      labels:
        app: my-app
        version: v2
    spec:
      containers:
        - name: app
          image: my-app:v2
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
```

Kubernetes DNS-based discovery (`my-svc.namespace.svc.cluster.local`) remains the simplest approach for cloud-native workloads, while Consul offers richer health checking and multi-datacenter support for hybrid or VM-based infrastructure.
