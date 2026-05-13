---
title: "CI/CD Pipeline Complete Guide 2026: From Git Push to Production"
description: "End-to-end CI/CD guide: linting, testing, building, security scanning, and deploying. GitHub Actions vs GitLab CI vs CircleCI comparison. Includes monorepo strategies, cache optimization, and deployment patterns (blue-green, canary)."
date: 2026-05-08
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/ci-cd-pipeline-guide.html
---

# CI/CD Pipeline Complete Guide 2026: From Git Push to Production

A well-designed CI/CD pipeline is the difference between deploying with confidence and deploying with prayer. In 2026, modern CI/CD goes beyond "run tests and deploy" — it includes automated canary analysis, security scanning, and instant rollbacks. This guide covers the complete pipeline architecture, tool comparison, and the practices that ship code faster with fewer incidents.

## The Modern CI/CD Pipeline Stages
    
    
    Git Push
      → 1. Lint & Format (Biome, ESLint)           [<30s]
      → 2. Type Check (TypeScript, mypy)           [<60s]
      → 3. Unit Tests                              [<2 min]
      → 4. Build (Docker, artifact)                [<3 min]
      → 5. Security Scan (SAST, dependency audit)  [<2 min]
      → 6. Integration Tests                       [<5 min]
      → 7. Deploy to Staging                       [<2 min]
      → 8. Smoke Tests (staging)                   [<3 min]
      → 9. Deploy to Canary (1% traffic)           [<2 min]
      → 10. Canary Analysis (metrics, errors)      [5-60 min]
      → 11. Full Production Deploy                 [<5 min]
      → 12. Post-Deploy Monitoring                 [ongoing]

## CI/CD Platform Comparison

Platform| Best For| Pricing| Key Strengths| Weaknesses  
---|---|---|---|---  
GitHub Actions| Most teams, GitHub-native| Free (2,000 min/mo), $0.008/min after| Largest marketplace (20K+ actions), matrix builds, OIDC| Slow on large monorepos, 6h max job time  
GitLab CI| GitLab users, self-hosted| Free (400 min/mo), $19/user/mo| Integrated container registry, auto-DevOps, best for self-hosted| Steeper YAML learning curve, smaller marketplace  
CircleCI| Large monorepos, high concurrency| $15/mo (6,000 min)| Fast caching, dynamic config, parallelism| More expensive at scale, less integrated than GitHub Actions  
Buildkite| Enterprise, hybrid cloud/on-prem| $20/user/mo| Hybrid runners (your infra), unlimited concurrency| Requires managing your own build infrastructure  
ArgoCD + Tekton| Kubernetes-native teams| Free (OSS)| GitOps native, declarative, Kubernetes-native| Complex setup, K8s expertise required  
  
## Pipeline Optimization: The 10-Minute Rule

Strategy| Time Saved| Implementation  
---|---|---  
Parallel jobs| 50-70%| Split tests into shards, run in parallel across multiple runners  
Dependency caching| 30-60%| Cache node_modules, pip packages, Docker layers  
Incremental builds| 40-70%| Only build/test what changed (Nx, Turborepo, Bazel)  
Skip unnecessary runs| 20-50%| Skip CI on docs-only changes, skip deploy on non-main branches  
Optimized Docker builds| 30-50%| Multi-stage builds, layer caching, minimal base images (distroless)  
  
## Deployment Strategies Compared

Strategy| Risk| Rollback Time| Infra Cost| Best For  
---|---|---|---|---  
Rolling Update| Medium| 1-5 min| No extra| Stateless services, most web apps  
Blue-Green| Low| <1 min (instant switch)| 2x (two full environments)| Critical services, zero-downtime required  
Canary| Very Low| <1 min| 1.1-1.5x| High-traffic services with good observability  
Feature Flags| Very Low| Instant| Flag management system| Decoupling deploy from release  
  
## GitHub Actions Pipeline Example
    
    
    # .github/workflows/ci.yml
    name: CI/CD Pipeline
    on:
      push:
        branches: [main, staging]
      pull_request:
        branches: [main]
    
    jobs:
      lint-and-test:
        runs-on: ubuntu-latest
        timeout-minutes: 10
        steps:
          - uses: actions/checkout@v4
          - uses: actions/setup-node@v4
            with: { node-version: '22', cache: 'npm' }
          - run: npm ci
          - run: npx biome ci .               # Lint + format
          - run: npx tsc --noEmit             # Type check
          - run: npm test -- --coverage       # Tests
          - run: npx vitest --shard=${{ matrix.shard }}/4  # Parallel
    
      security:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - run: npm ci
          - run: npm audit --audit-level=high  # Dependency scan
          - uses: aquasecurity/trivy-action@master  # Container scan
            with: { scan-type: 'fs', scanners: 'vuln,secret' }
    
      deploy-staging:
        needs: [lint-and-test, security]
        if: github.ref == 'refs/heads/staging'
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - run: npm run build
          - uses: cloudflare/wrangler-action@v3
            with: { environment: 'staging' }
    
      deploy-production:
        needs: [lint-and-test, security]
        if: github.ref == 'refs/heads/main'
        runs-on: ubuntu-latest
        environment: production  # Requires approval
        steps:
          - uses: actions/checkout@v4
          - run: npm run build
          - run: npm run deploy:canary  # Deploy to 5% first
          - run: npm run smoke-test
          - run: npm run deploy:full    # Full production after canary passes

**Bottom line:** A good CI/CD pipeline should give you confidence to deploy on Friday at 5pm. Key principles: the pipeline should complete in under 10 minutes (optimize ruthlessly), every failure should have a clear error message (not "Exit code 1"), and deploys should be one-click reversible. Start with GitHub Actions (free for most teams), implement parallel test sharding first (biggest speed win), and adopt canary deploys as your traffic and risk grow. See also: [Webhook Implementation Guide](</en/tech/webhook-implementation-guide.html>) and [Kubernetes vs Docker Swarm vs Nomad](</en/compare/kubernetes-vs-docker-swarm-vs-nomad.html>).
