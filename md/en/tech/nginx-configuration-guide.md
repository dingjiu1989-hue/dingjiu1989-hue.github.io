---
title: "Nginx Configuration Guide"
description: "Master Nginx configuration with practical examples for reverse proxying, SSL, caching, rate limiting, and load balancing."
date: 2026-05-11
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/nginx-configuration-guide.html
---

# Nginx Configuration Guide

## Nginx Configuration Guide

## Nginx Configuration Guide

## Nginx Configuration Guide

## Nginx Configuration Guide

## Nginx Configuration Guide

## Nginx Configuration Guide

## Nginx Configuration Guide

## Nginx Configuration Guide

## Nginx Configuration Guide

## Nginx Configuration Guide

## Nginx Configuration Guide

## Nginx Configuration Guide

## Nginx Configuration Guide

## Nginx Configuration Guide

Nginx is the most widely used web server and reverse proxy in production. Its event-driven architecture handles thousands of concurrent connections with minimal resource usage. This guide covers essential Nginx configuration patterns for production deployments.

### Core Configuration Structure

Every Nginx configuration follows a hierarchical structure:

/etc/nginx/

nginx.conf # Main configuration

sites-enabled/ # Active site configurations

sites-available/ # All site configurations (symlinked)

conf.d/ # Additional configuration fragments

The main `nginx.conf` sets global settings:

user www-data;

worker_processes auto;

pid /run/nginx.pid;

events {

worker_connections 1024;

multi_accept on;

use epoll;

}

http {

include /etc/nginx/mime.types;

default_type application/octet-stream;

sendfile on;

tcp_nopush on;

tcp_nodelay on;

keepalive_timeout 65;

types_hash_max_size 2048;

include /etc/nginx/conf.d/*.conf;

include /etc/nginx/sites-enabled/*;

}

Set `worker_processes` to `auto` to match the number of CPU cores. `worker_connections` controls how many simultaneous connections each worker handles.

### HTTP Server Block

A basic server block for a static site:

server {

listen 80;

listen [::]:80;

server_name example.com www.example.com;

root /var/www/example.com/public;

index index.html;

location / {

try_files $uri $uri/ /index.html;

}

location ~* \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\.(js|css|png|jpg|jpeg|gif|ico|svg)$ {

expires 30d;

add_header Cache-Control "public, immutable";

}

}

### Reverse Proxy Configuration

Nginx excels as a reverse proxy for application servers:

server {

listen 80;

server_name api.example.com;

location / {

proxy_pass http://127.0.0.1:3000;

proxy_http_version 1.1;

proxy_set_header Upgrade $http_upgrade;

proxy_set_header Connection 'upgrade';

proxy_set_header Host $host;

proxy_set_header X-Real-IP $remote_addr;

proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

proxy_set_header X-Forwarded-Proto $scheme;

proxy_cache_bypass $http_upgrade;

}

}

Always set the `X-Forwarded-*` headers so upstream applications know the client's real IP and protocol. The `proxy_http_version 1.1` and `Upgrade` headers are required for WebSocket support.

### SSL/TLS with Let's Encrypt

Secure your sites with modern TLS configuration:

server {

listen 443 ssl http2;

listen [::]:443 ssl http2;

server_name example.com;

ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;

ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

ssl_protocols TLSv1.2 TLSv1.3;

ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;

ssl_prefer_server_ciphers off;

ssl_session_cache shared:SSL:10m;

ssl_session_timeout 10m;

add_header Strict-Transport-Security "max-age=63072000" always;

}

server {

listen 80;

server_name example.com;

return 301 https://$server_name$request_uri;

}

TLSv1.3 should be preferred when available. The HTTP redirect ensures all traffic uses HTTPS. HSTS headers tell browsers to always use HTTPS for your domain.

### Rate Limiting

Protect your application from abuse:

http {

limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

limit_conn_zone $binary_remote_addr zone=addr:10m;

server {

location /api/ {

limit_req zone=api burst=20 nodelay;

limit_conn addr 10;

proxy_pass http://backend;

}

}

}

The `limit_req_zone` defines a shared memory zone for tracking request rates. A burst of 20 allows short spikes above the 10 requests-per-second limit.

### Load Balancing

Distribute traffic across multiple upstream servers:

upstream backend {

least_conn;

server 10.0.0.1:3000 weight=3;

server 10.0.0.2:3000;

server 10.0.0.3:3000 backup;

}

server {

location / {

proxy_pass http://backend;

}

}

Use `least_conn` for variable-length requests, `ip_hash` for session persistence, or the default round-robin for identical workloads. The `backup` server only receives traffic when all primary servers are down.

### Caching Static Content

Cache proxied responses to reduce backend load:

http {

proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=static:10m max_size=1g inactive=60m;

server {

location /static/ {

proxy_cache static;

proxy_cache_valid 200 302 60m;

proxy_cache_valid 404 1m;

proxy_cache_use_stale error timeout updating;

proxy_pass http://backend;

}

}

}

The `proxy_cache_use_stale` directive serves stale content when the backend is unreachable, preventing error pages during brief outages.

### Security Headers

Add security headers to all responses:

add_header X-Frame-Options "SAMEORIGIN" always;

add_header X-Content-Type-Options "nosniff" always;

add_header X-XSS-Protection "0" always;

add_header Referrer-Policy "strict-origin-when-cross-origin" always;

add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;

### Logging Configuration

Customize log formats for better debugging:

log_format json escape=json '{'

'"time": "$time_local",'

'"remote_addr": "$remote_addr",'

'"request": "$request",'

'"status": $status,'

'"body_bytes": $body_bytes_sent,'

'"request_time": $request_time,'

'"upstream_addr": "$upstream_addr",'

'"upstream_time": "$upstream_response_time"'

'}';

access_log /var/log/nginx/access.log json buffer=32k flush=5s;

JSON-formatted logs are parseable by log aggregation tools like Loki, Elasticsearch, or Datadog.

### Summary

Nginx is a versatile tool that serves as web server, reverse proxy, load balancer, and TLS termination point. Master these configuration patterns -- server blocks, reverse proxying, SSL termination, rate limiting, and caching -- and you can handle the majority of production deployment scenarios. Always test configuration changes with `nginx -t` before reloading.

**See also:** [Reverse Proxy Guide](</en/tech/reverse-proxy-guide.html>), [Nginx Configuration: Performance and Security](</en/tech/nginx-configuration.html>), [API Gateway Implementation Guide](</en/tech/api-gateway-implementation.html>).

**See also:** [Reverse Proxy Guide](</en/tech/reverse-proxy-guide.html>), [Nginx Configuration: Performance and Security](</en/tech/nginx-configuration.html>), [API Gateway Implementation Guide](</en/tech/api-gateway-implementation.html>)

**See also:** [Reverse Proxy Guide](</en/tech/reverse-proxy-guide.html>), [Nginx Configuration: Performance and Security](</en/tech/nginx-configuration.html>), [API Gateway Implementation Guide](</en/tech/api-gateway-implementation.html>)
