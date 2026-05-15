---
title: "Nginx Configuration: Performance and Security"
description: "Configure Nginx for production: reverse proxy, load balancing, caching, SSL termination, and security hardening."
date: 2026-05-12
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/nginx-configuration.html
---

# Nginx Configuration: Performance and Security

## Nginx Configuration: Performance and Security

## Nginx Configuration: Performance and Security

## Nginx Configuration: Performance and Security

## Nginx Configuration: Performance and Security

## Nginx Configuration: Performance and Security

## Nginx Configuration: Performance and Security

## Nginx Configuration: Performance and Security

## Nginx Configuration: Performance and Security

## Nginx Configuration: Performance and Security

## Nginx Configuration: Performance and Security

## Nginx Configuration: Performance and Security

## Nginx Configuration: Performance and Security

## Nginx Configuration: Performance and Security

Nginx is the most popular web server and reverse proxy. Proper configuration balances performance, security, and resource usage.

### Reverse Proxy Configuration

Configure Nginx as a reverse proxy to backend applications. Use proxy_pass to forward requests. Set proxy_set_header to forward client connection details. Configure proxy_buffering for streaming applications.

WebSocket proxying requires specific headers: Upgrade and Connection. FastCGI proxying (for PHP) uses fastcgi_pass. gRPC proxying requires http2 and grpc_pass. Each protocol has specific requirements for reliable proxying.

### Load Balancing

Nginx distributes traffic across backend servers. Load balancing methods include round-robin (default), least_conn (least connections), ip_hash (session persistence), and random. upstream blocks define server groups with optional weights.

Health checks monitor backend availability. Active checks (nginx plus) test endpoints periodically. Passive checks mark servers as failed after connection or timeout errors. max_fails and fail_timeout control failure detection.

### Caching

Nginx caching reduces backend load. proxy_cache_path defines the cache location and parameters. proxy_cache enables caching for specific locations. Cache keys based on request URI, query string, and headers.

Cache bypass headers (Cache-Control: no-cache) from the backend prevent caching of dynamic content. Cache purging removes stale entries. Microcaching (1-5 second cache for all responses) protects backends from traffic spikes.

### SSL/TLS

Configure HTTPS with strong ciphers and protocols. Use TLS 1.2 and 1.3 only. Modern cipher suites prioritize ChaCha20 and AES-GCM. Enable HSTS (Strict-Transport-Security) to enforce HTTPS.

OCSP stapling improves TLS performance. SSL session cache reduces handshake overhead. Use Let's Encrypt with Certbot for automated certificate management. Redirect HTTP to HTTPS in the server block.

### Security Headers

Add security headers: X-Content-Type-Options: nosniff, X-Frame-Options: DENY, X-XSS-Protection: 0 (modern browsers handle XSS), Referrer-Policy: strict-origin-when-cross-origin, Permissions-Policy for feature control. Content-Security-Policy headers mitigate XSS and data injection attacks.

Rate limiting protects against abuse. limit_req_zone defines rate zones. limit_req applies rate limiting per location. Burst and nodelay parameters allow short traffic spikes while maintaining average limits.

**See also:** [Reverse Proxy Guide](</en/tech/reverse-proxy-guide.html>), [Nginx Configuration Guide](</en/tech/nginx-configuration-guide.html>), [Dockerfile Best Practices for Production](</en/tech/dockerfile-best-practices.html>).

**See also:** [Nginx Configuration Guide](</en/tech/nginx-configuration-guide.html>), [Reverse Proxy Guide](</en/tech/reverse-proxy-guide.html>), [Dockerfile Best Practices for Production](</en/tech/dockerfile-best-practices.html>)

**See also:** [Nginx Configuration Guide](</en/tech/nginx-configuration-guide.html>), [Reverse Proxy Guide](</en/tech/reverse-proxy-guide.html>), [Dockerfile Best Practices for Production](</en/tech/dockerfile-best-practices.html>)
