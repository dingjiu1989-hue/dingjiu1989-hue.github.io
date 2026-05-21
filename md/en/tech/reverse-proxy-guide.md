---
title: "Reverse Proxy Guide"
description: "Complete guide to reverse proxy configuration with Nginx and Caddy, covering SSL, caching, and load balancing."
date: 2025-12-03
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/reverse-proxy-guide.html
---

# Reverse Proxy Guide

A reverse proxy sits in front of your application servers, handling incoming requests and distributing them to backend services. It is essential for TLS termination, load balancing, caching, and security. This guide covers two of the most popular options: Nginx and Caddy.

## Why Use a Reverse Proxy

  * **TLS termination** : Handle HTTPS once at the proxy layer.

  * **Load balancing** : Distribute traffic across multiple backend instances.

  * **Caching** : Cache responses to reduce backend load.

  * **Security** : Filter malicious requests, rate limiting, IP blocking.

  * **Multiple services** : Route different paths to different backends from one domain.




## Nginx Reverse Proxy

Nginx is the industry standard for reverse proxying. It is mature, highly performant, and extremely configurable.

## Basic Reverse Proxy Configuration

server {

listen 80;

server_name app.example.com;

location / {

proxy_pass http://127.0.0.1:3000;

proxy_set_header Host $host;

proxy_set_header X-Real-IP $remote_addr;

proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

proxy_set_header X-Forwarded-Proto $scheme;

}

}

The `proxy_pass` directive sends requests to the backend. Always forward the original host and client IP headers so your application has accurate client information.

## WebSocket Support

location /ws/ {

proxy_pass http://127.0.0.1:3001;

proxy_http_version 1.1;

proxy_set_header Upgrade $http_upgrade;

proxy_set_header Connection "upgrade";

proxy_set_header Host $host;

proxy_read_timeout 86400s;

}

The `Upgrade` and `Connection` headers are required for WebSocket connections. Set `proxy_read_timeout` to a long duration since WebSocket connections remain open.

## Load Balancing

Distribute traffic across multiple backends:

upstream app_cluster {

least_conn;

server 10.0.0.1:3000 weight=3;

server 10.0.0.2:3000;

server 10.0.0.3:3000 backup;

}

server {

location / {

proxy_pass http://app_cluster;

}

}

Load balancing methods: `round-robin` (default), `least_conn` (fewest active connections), `ip_hash` (session persistence). Assign higher `weight` to more powerful servers.

## Caching

Cache responses from the backend:

proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=appcache:10m max_size=1g;

server {

location / {

proxy_cache appcache;

proxy_cache_valid 200 30m;

proxy_cache_valid 404 1m;

proxy_cache_use_stale error timeout updating;

add_header X-Cache-Status $upstream_cache_status;

}

}

The `$upstream_cache_status` header helps debug caching (HIT, MISS, STALE, etc.). `proxy_cache_use_stale` serves stale content when the backend is down.

## Caddy Reverse Proxy

Caddy is a modern web server with automatic HTTPS, simpler configuration, and Go-based performance. It is ideal for teams that want a zero-fuss reverse proxy.

## Basic Reverse Proxy

## Caddyfile

app.example.com {

reverse_proxy localhost:3000

}

That is the entire configuration. Caddy automatically obtains and renews Let's Encrypt TLS certificates.

## Multiple Backends with Load Balancing

app.example.com {

reverse_proxy 10.0.0.1:3000 10.0.0.2:3000 10.0.0.3:3000 {

lb_policy least_conn

health_uri /health

health_interval 30s

}

}

Caddy supports multiple load balancing policies: `random`, `least_conn`, `round_robin`, `first`, `ip_hash`.

## Path-Based Routing

Route different paths to different services:

api.example.com {

reverse_proxy /api/* localhost:3000

reverse_proxy /auth/* localhost:3001

reverse_proxy localhost:3002 # default

}

## Request Manipulation

app.example.com {

reverse_proxy localhost:3000 {

header_up Host {host}

header_up X-Real-IP {remote_host}

}

## Add security headers

header {

X-Frame-Options "SAMEORIGIN"

X-Content-Type-Options "nosniff"

}

}

Caddy's `header` directive works for both request and response headers.

## Nginx vs Caddy: Comparison

| Feature | Nginx | Caddy |

|---------|-------|-------|

| Configuration | Complex, powerful | Simple, opinionated |

| TLS | Manual cert management | Automatic Let's Encrypt |

| Performance | Excellent | Very good |

| Ecosystem | Vast (modules, guides) | Growing but smaller |

| Docker support | Official image | Official image |

| Learning curve | Steep | Gentle |

| Dynamic configuration | Limited | REST API available |

| HTTP/3 | Supported | Supported |

## Security Headers

Regardless of which reverse proxy you choose, add these security headers:

For Nginx:

add_header X-Frame-Options "SAMEORIGIN" always;

add_header X-Content-Type-Options "nosniff" always;

add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

add_header Content-Security-Policy "default-src 'self';" always;

For Caddy:

header {

X-Frame-Options "SAMEORIGIN"

X-Content-Type-Options "nosniff"

Strict-Transport-Security "max-age=31536000; includeSubDomains"

}

## Rate Limiting

Nginx:

limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

location /api/ {

limit_req zone=api burst=20 nodelay;

proxy_pass http://backend;

}

Caddy:

app.example.com {

rate_limit {

zone api {

key {remote_host}

events 10

window 1s

}

}

reverse_proxy localhost:3000

}

## Health Checks

Nginx health checks require the Plus version or are handled externally (e.g., via Docker health checks). Caddy includes built-in active health checks that mark unhealthy backends as down and stop routing traffic to them.

## Summary

Nginx and Caddy are both excellent reverse proxies. Nginx offers unmatched flexibility and performance for complex deployments. Caddy provides automatic TLS and simpler configuration, making it ideal for smaller teams or simpler setups. For TLS-heavy deployments, Caddy's automatic certificates save significant operational overhead. For high-traffic scenarios requiring fine-grained control, Nginx remains the standard. Both can route traffic, terminate TLS, add security headers, and cache responses -- choose based on your team's expertise and operational complexity tolerance.

**See also:** [Nginx Configuration Guide](</en/tech/nginx-configuration-guide.html>), [Nginx Configuration: Performance and Security](</en/tech/nginx-configuration.html>), [Developer Environment Setup Guide](</en/tech/dev-environment-setup.html>).

**See also:** [Nginx Configuration Guide](</en/tech/nginx-configuration-guide.html>), [Nginx Configuration: Performance and Security](</en/tech/nginx-configuration.html>), [Developer Environment Setup Guide](</en/tech/dev-environment-setup.html>)

**See also:** [Nginx Configuration Guide](</en/tech/nginx-configuration-guide.html>), [Nginx Configuration: Performance and Security](</en/tech/nginx-configuration.html>), [Developer Environment Setup Guide](</en/tech/dev-environment-setup.html>)

**See also:** [Nginx Configuration Guide](</en/tech/nginx-configuration-guide.html>), [Nginx Configuration: Performance and Security](</en/tech/nginx-configuration.html>), [Developer Environment Setup Guide](</en/tech/dev-environment-setup.html>)

**See also:** [Nginx Configuration Guide](</en/tech/nginx-configuration-guide.html>), [Nginx Configuration: Performance and Security](</en/tech/nginx-configuration.html>), [Developer Environment Setup Guide](</en/tech/dev-environment-setup.html>)

**See also:** [Nginx Configuration Guide](</en/tech/nginx-configuration-guide.html>), [Nginx Configuration: Performance and Security](</en/tech/nginx-configuration.html>), [Developer Environment Setup Guide](</en/tech/dev-environment-setup.html>)

**See also:** [Advanced GitHub Actions Workflows](</en/tech/github-actions-advanced.html>), [Helm Charts: Kubernetes Package Management](</en/tech/helm-kubernetes-package-management.html>), [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>)

**See also:** [Advanced GitHub Actions Workflows](</en/tech/github-actions-advanced.html>), [Helm Charts: Kubernetes Package Management](</en/tech/helm-kubernetes-package-management.html>), [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>)

**See also:** [Advanced GitHub Actions Workflows](</en/tech/github-actions-advanced.html>), [Helm Charts: Kubernetes Package Management](</en/tech/helm-kubernetes-package-management.html>), [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>)

**See also:** [Advanced GitHub Actions Workflows](</en/tech/github-actions-advanced.html>), [Helm Charts: Kubernetes Package Management](</en/tech/helm-kubernetes-package-management.html>), [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>)

**See also:** [Advanced GitHub Actions Workflows](</en/tech/github-actions-advanced.html>), [Helm Charts: Kubernetes Package Management](</en/tech/helm-kubernetes-package-management.html>), [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>)

**See also:** [Advanced GitHub Actions Workflows](</en/tech/github-actions-advanced.html>), [Helm Charts: Kubernetes Package Management](</en/tech/helm-kubernetes-package-management.html>), [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>)

**See also:** [Advanced GitHub Actions Workflows](</en/tech/github-actions-advanced.html>), [Helm Charts: Kubernetes Package Management](</en/tech/helm-kubernetes-package-management.html>), [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>)

**See also:** [Advanced GitHub Actions Workflows](</en/tech/github-actions-advanced.html>), [Helm Charts: Kubernetes Package Management](</en/tech/helm-kubernetes-package-management.html>), [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>)

**See also:** [Advanced GitHub Actions Workflows](</en/tech/github-actions-advanced.html>), [Helm Charts: Kubernetes Package Management](</en/tech/helm-kubernetes-package-management.html>), [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>)

**See also:** [Advanced GitHub Actions Workflows](</en/tech/github-actions-advanced.html>), [Helm Charts: Kubernetes Package Management](</en/tech/helm-kubernetes-package-management.html>), [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>)

**See also:** [Advanced GitHub Actions Workflows](</en/tech/github-actions-advanced.html>), [Helm Charts: Kubernetes Package Management](</en/tech/helm-kubernetes-package-management.html>), [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>)

**See also:** [Advanced GitHub Actions Workflows](</en/tech/github-actions-advanced.html>), [Helm Charts: Kubernetes Package Management](</en/tech/helm-kubernetes-package-management.html>), [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>)

**See also:** [Advanced GitHub Actions Workflows](</en/tech/github-actions-advanced.html>), [Helm Charts: Kubernetes Package Management](</en/tech/helm-kubernetes-package-management.html>), [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>)

**See also:** [Advanced GitHub Actions Workflows](</en/tech/github-actions-advanced.html>), [Helm Charts: Kubernetes Package Management](</en/tech/helm-kubernetes-package-management.html>), [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>)
