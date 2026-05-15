---
title: "DevOps for Developers: CI/CD, Docker, IaC, and Monitoring — A Practical Guide"
description: "The DevOps skills every developer needs in 2026. CI/CD pipelines, Docker containers, Infrastructure as Code (Terraform), and monitoring. Hands-on, not theoretical."
date: 2026-05-08
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/devops-for-developers.html
---

# DevOps for Developers: CI/CD, Docker, IaC, and Monitoring — A Practical Guide

You don't need to be a DevOps engineer to deploy and operate software in 2026. The tools have gotten so good that every developer can own their full pipeline. Here's the practical DevOps toolkit — CI/CD, containers, IaC, and monitoring — explained for developers.

## The Developer DevOps Stack (2026)

Layer| Tool| Why It's Worth Learning  
---|---|---  
**CI/CD**|  GitHub Actions| Free 2000 min/mo. 20K+ marketplace actions. The default.  
**Containers**|  Docker| Works everywhere. Compose for local dev.  
**Orchestration**|  Kubernetes (or skip it)| Overkill for 90% of projects. Use managed containers instead.  
**Infrastructure as Code**|  Terraform / OpenTofu| Declare infra in HCL. Version-controlled, repeatable, auditable.  
**Monitoring**|  Grafana + Prometheus| Dashboard metrics from any source. Prometheus scrapes and stores.  
**Logging**|  Pino (structured) → Loki/Grafana| Structured JSON logs. Centralized querying.  
**Secrets**|  Infisical / Doppler| Sync .env across devs, CI, and production. Encrypted, audited.  
**Deploy**|  Coolify / Railway| Self-hosted Vercel or managed PaaS. Dockerfile → URL.  
  
## 1\. CI/CD with GitHub Actions

A good CI/CD pipeline tests, builds, and deploys on every push. Here's a minimal but complete workflow:
    
    
    # .github/workflows/ci.yml
    name: CI
    on: [push, pull_request]
    jobs:
      test:
        runs-on: ubuntu-latest
        services:
          postgres:
            image: postgres:16
            env:
              POSTGRES_PASSWORD: test
            options: >-
              --health-cmd pg_isready
              --health-interval 10s
        steps:
          - uses: actions/checkout@v4
          - uses: actions/setup-node@v4
            with: { node-version: "22" }
          - run: npm ci
          - run: npx vitest --coverage
            env:
              DATABASE_URL: postgresql://postgres:test@localhost:5432/test
          - run: npx playwright test  # E2E
          - name: Deploy (if main)
            if: github.ref == 'refs/heads/main'
            run: curl -X POST $DEPLOY_WEBHOOK

## 2\. Docker for Containers
    
    
    # Multi-stage Dockerfile for a Node.js app
    FROM node:22-alpine AS builder
    WORKDIR /app
    COPY package*.json ./
    RUN npm ci
    COPY . .
    RUN npm run build
    
    FROM node:22-alpine AS runner
    WORKDIR /app
    COPY --from=builder /app/dist ./dist
    COPY --from=builder /app/node_modules ./node_modules
    EXPOSE 3000
    CMD ["node", "dist/server.js"]

## 3\. Infrastructure as Code (Terraform)

Terraform lets you declare infrastructure in code. No more clicking in cloud consoles — your infra is version-controlled and repeatable.
    
    
    # main.tf — Deploy a Next.js app to Vercel
    resource "vercel_project" "web" {
      name      = "my-app"
      framework = "nextjs"
      git_repository = {
        type = "github"
        repo = "my-org/my-app"
      }
    }
    
    resource "vercel_project_environment_variable" "db_url" {
      project_id = vercel_project.web.id
      key        = "DATABASE_URL"
      value      = var.database_url
    }

## 4\. Monitoring with Grafana + Prometheus

Prometheus scrapes metrics from your app (CPU, memory, request latency, error rate). Grafana visualizes them in dashboards. For Node.js apps, use prom-client to expose custom metrics:
    
    
    import client from "prom-client";
    import express from "express";
    
    const app = express();
    const collectDefaultMetrics = client.collectDefaultMetrics;
    collectDefaultMetrics();
    
    const httpRequestDuration = new client.Histogram({
      name: "http_request_duration_seconds",
      help: "Duration of HTTP requests in seconds",
      labelNames: ["method", "route", "status"],
    });
    
    app.use((req, res, next) => {
      const end = httpRequestDuration.startTimer();
      res.on("finish", () => {
        end({ method: req.method, route: req.route?.path, status: res.statusCode });
      });
      next();
    });
    
    app.get("/metrics", async (req, res) => {
      res.set("Content-Type", client.register.contentType);
      res.end(await client.register.metrics());
    });

## When to Skip Complexity

Not every project needs the full DevOps stack:

  * **Side project / MVP:** GitHub Actions → Coolify on a $20 VPS. Skip K8s, skip Terraform.
  * **Growing startup:** GitHub Actions → Railway or Render. Add Sentry for errors.
  * **Scaling product:** GitHub Actions → K8s (or ECS). Terraform for infra. Full monitoring stack.



**Bottom line:** Learn CI/CD and Docker first — they're universally useful. Add Terraform when your infra has 5+ resources. Add K8s only when you have 10+ containers and need orchestration. The best operations is the one you don't have to think about. See also: [CI/CD tools comparison](</en/tools/best-cicd-tools-2026.html>) and [Docker vs Podman](</en/compare/docker-vs-podman.html>).

**See also:** [Docker in 30 Minutes: From Install to First Container](</en/tech/docker-quickstart.html>), [AI for DevOps in 2026: Best Tools and Practical Use Cases](</en/ai/ai-devops-tools.html>), [Docker Compose for Production: Multi-Service Deployments Done Right](</en/tech/docker-compose-production.html>)
