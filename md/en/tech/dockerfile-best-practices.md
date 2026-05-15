---
title: "Dockerfile Best Practices for Production"
description: "Optimize Dockerfiles for production: multi-stage builds, layer caching, security scanning, and minimal images."
date: 2026-05-12
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/dockerfile-best-practices.html
---

# Dockerfile Best Practices for Production

# Dockerfile Best Practices for Production

# Dockerfile Best Practices for Production

# Dockerfile Best Practices for Production

# Dockerfile Best Practices for Production

# Dockerfile Best Practices for Production

# Dockerfile Best Practices for Production

# Dockerfile Best Practices for Production

# Dockerfile Best Practices for Production

# Dockerfile Best Practices for Production

# Dockerfile Best Practices for Production

# Dockerfile Best Practices for Production

# Dockerfile Best Practices for Production

# Dockerfile Best Practices for Production

Writing efficient Dockerfiles reduces image size, improves build speed, and enhances security. These best practices apply to production container builds.

## Multi-Stage Builds

Multi-stage builds separate build and runtime environments. Use one stage with all build tools (compilers, package managers) and a second minimal stage for the runtime. The resulting image contains only the application binary and its runtime dependencies.

Multi-stage builds dramatically reduce image size. A Go application might go from 1GB (with golang:1.21) to 20MB (with scratch). Python applications benefit from using slim base images in final stages.

## Layer Caching

Each Dockerfile instruction creates a cacheable layer. Order instructions from least to most frequently changing. Install system packages first, copy dependency manifests (package.json, requirements.txt), run package install, then copy application code.

This ordering means rebuilding after code changes only invalidates layers from the COPY instruction onward. Dependency installation (the slowest step) uses the cache.

## Security Best Practices

Run containers as non-root users. Create a user in the Dockerfile and switch with USER directive. Never run containers as root—container escape vulnerabilities grant root access to the host.

Use specific base image tags, not latest. Pin versions like python:3.12-slim instead of python:latest. Scan images for vulnerabilities with Docker Scout, Trivy, or Snyk. Remove package manager cache files in the same RUN instruction.

## Minimal Images

Use distroless or Alpine base images. Distroless images contain only the application and runtime libraries—no shell, package manager, or utilities. This reduces attack surface and image size.

Alpine-based images are small (5MB base) but use musl libc instead of glibc. Test thoroughly—some Python packages have musl compatibility issues.

## Dockerignore

Use .dockerignore to exclude unnecessary files from the build context. Exclude .git, node_modules, tests, documentation, and CI configuration. Smaller build contexts mean faster builds, especially in CI environments.

**See also:** [Nginx Configuration: Performance and Security](</en/tech/nginx-configuration.html>), [Build Optimization](</en/tech/build-optimization.html>), [GitHub Actions Workflows: Advanced Patterns](</en/tech/github-actions-workflows.html>).

**See also:** [Nginx Configuration: Performance and Security](</en/tech/nginx-configuration.html>), [Azure Networking: VNets, Peering, Azure Firewall, and Load Balancing](</en/tech/azure-networking.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>)
