---
title: "Docker Compose for Production: Multi-Service Deployments Done Right"
description: "Beyond docker-compose up: production-ready Compose files with health checks, resource limits, secrets management, logging drivers, and zero-downtime rolling updates. Compare with Swarm and Kubernetes."
date: 2025-10-15
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/docker-compose-production.html
---

# Docker Compose for Production: Multi-Service Deployments Done Right

Docker Compose is widely used for local development, but it is also a viable — and often simpler — production deployment tool for small-to-medium applications. With careful configuration (health checks, resource limits, secrets management, and logging), Compose can run production workloads reliably. It is not Kubernetes, but not every app needs Kubernetes.

## Docker Compose vs Swarm vs Kubernetes for Production

Scale| Best Tool| Why  
---|---|---  
1-3 services, single host| Docker Compose| Simplest setup, single docker-compose.yml, no orchestration overhead  
3-10 services, 2-5 hosts| Docker Swarm| Compose-compatible syntax, built-in load balancing, secrets  
10+ services, multi-region, auto-scaling| Kubernetes| Full orchestration, service mesh, auto-scaling, ecosystem  
  
## Production-Ready Compose File
    
    
    # docker-compose.prod.yml
    services:
      app:
        image: myapp:latest
        deploy:
          resources:
            limits:
              cpus: '1.0'
              memory: '512M'
            reservations:
              cpus: '0.5'
              memory: '256M'
        healthcheck:
          test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
          interval: 30s
          timeout: 10s
          retries: 3
          start_period: 40s
        logging:
          driver: "json-file"
          options:
            max-size: "10m"
            max-file: "3"
        restart: unless-stopped
        env_file:
          - .env.production
        secrets:
          - db_password
          - jwt_secret
        volumes:
          - app_uploads:/app/uploads
    
      postgres:
        image: postgres:16-alpine
        healthcheck:
          test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER}"]
          interval: 10s
          timeout: 5s
          retries: 5
        volumes:
          - pgdata:/var/lib/postgresql/data
        secrets:
          - db_password
    
    secrets:
      db_password:
        file: ./secrets/db_password.txt
      jwt_secret:
        file: ./secrets/jwt_secret.txt
    
    volumes:
      pgdata:
      app_uploads:

## Key Production Settings Explained

Setting| What It Does| Recommended Value  
---|---|---  
healthcheck| Docker checks if container is healthy; Compose can wait for healthy before starting dependents| HTTP endpoint at /health, max 3 retries, 30s interval  
deploy.resources.limits| Hard cap on CPU and memory — prevents one container from starving others| Set based on your app's profile; always set a memory limit  
deploy.resources.reservations| Soft minimum — Docker scheduler guarantees this much| 50-75% of limits for production critical services  
restart| Policy for when a container exits| unless-stopped (production), no for one-off jobs  
logging| Log driver + rotation — prevents disk from filling with logs| json-file with 10MB max per file, 3 files max (~30MB per service)  
secrets| In Swarm mode: encrypted at rest, tmpfs-mounted. In Compose: file-based| Use Docker secrets in Swarm; use env_file + vault in Compose  
  
## Zero-Downtime Rolling Updates (Swarm Mode)

With Swarm mode, Compose files gain rolling update support — update your containers without dropping requests:
    
    
    services:
      app:
        image: myapp:latest
        deploy:
          replicas: 3
          update_config:
            parallelism: 1       # Update 1 replica at a time
            delay: 10s           # Wait 10s between updates
            order: start-first   # Start new before stopping old
            failure_action: rollback
          rollback_config:
            parallelism: 1
            delay: 5s
    

**Bottom line:** Docker Compose in production is underrated. If you have fewer than 10 services and do not need auto-scaling or multi-region, Compose (or Compose + Swarm for multi-host) is simpler and more maintainable than Kubernetes. The production checklist: health checks, resource limits, log rotation, secrets management, and a restart policy. See also: [Kubernetes vs Docker Swarm vs Nomad](</en/compare/kubernetes-vs-docker-swarm-vs-nomad.html>) and [Deploy Next.js for Free](</en/tech/deploy-nextjs-free.html>).

**See also:** [Self-Hosted PaaS Comparison 2026: Coolify vs Dokploy vs CapRover vs Kamal vs Dokku](</en/compare/self-hosted-paas-comparison.html>), [Docker vs Podman (2026): Best Container Tool for Developers?](</en/compare/docker-vs-podman.html>), [Docker in 30 Minutes: From Install to First Container](</en/tech/docker-quickstart.html>)
