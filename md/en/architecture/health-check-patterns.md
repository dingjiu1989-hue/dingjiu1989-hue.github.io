---
title: "Health Check Patterns"
description: "Liveness vs readiness probes, custom health checks, dependency health, graceful degradation, and production practices"
date: 2026-04-27
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/health-check-patterns.html
---

# Health Check Patterns

## Health Check Patterns

### Health Check Patterns

#### Health Check Patterns

#### Health Check Patterns

#### Health Check Patterns

#### Health Check Patterns

#### Health Check Patterns

#### Health Check Patterns

#### Health Check Patterns

#### Health Check Patterns

#### Health Check Patterns

#### Health Check Patterns

#### Health Check Patterns

#### Health Check Patterns

#### Health Check Patterns

Health checks are the mechanism by which orchestration platforms and load balancers determine whether an application instance is capable of serving requests. Two distinct check types serve different purposes: liveness and readiness. Understanding the difference and implementing them correctly is essential for reliable deployments, self-healing infrastructure, and graceful degradation. 

Liveness probes determine whether the application process is alive. If a liveness probe fails, the application is stuck or deadlocked — unable to recover without restart. The orchestrator will terminate and restart the container or process. Liveness probes should check only whether the process can operate at all. Common checks include: reading a health file written by the application, checking that the main event loop is running, or verifying that internal goroutine counts are within bounds. 

The danger of aggressive liveness probes is the "restart loop of death." If the application becomes slow due to a dependency outage, and the liveness probe times out, the orchestrator restarts the process. The new process immediately encounters the same dependency outage, fails again, and gets restarted in a loop. This not only fails to solve the problem but compounds it by adding startup overhead. Liveness probes should be conservative — use a longer interval (30 seconds) with high failure thresholds. 

Readiness probes determine whether the application is ready to accept traffic. If a readiness probe fails, the instance is removed from service but not restarted. Readiness probes should check that dependencies — databases, message brokers, upstream services — are accessible and that the application has sufficient capacity. A failing readiness probe means the instance should stop accepting new traffic but can recover once dependencies become available. 

Custom health checks beyond basic TCP/HTTP probes provide richer information. A good practice is to implement a health check endpoint that returns structured information about each dependency. The endpoint might return HTTP 200 when all dependencies are healthy, 503 when critical dependencies are unavailable, and include details about which dependencies are degraded. This allows operators and automation to understand the system's health state precisely. 

Dependency health assessment requires careful categorization. Critical dependencies are those without which the instance cannot serve requests — the primary database, the session store. Non-critical dependencies are those whose failure degrades but does not prevent service — a recommendation engine, an analytics pipeline. Readiness probes should only consider critical dependencies. A failing recommendation engine should not cause the entire instance to be removed from traffic. 

Graceful degradation is the architectural counterpart to health checks. When a dependency fails, the application should degrade functionality rather than fail entirely. For example, when the product recommendation service is down, the product page should still serve basic product information and reviews, with the recommendation section showing a fallback or being hidden. Health check endpoints should report degraded status when such fallback modes are active. 

Deployment health checks follow a specific sequence. During startup, the liveness probe should be delayed to allow the application to initialize. The readiness probe should become active only after initialization is complete. During shutdown, the readiness probe should immediately fail to remove the instance from service, then the application drains connections, and finally the liveness probe should reflect termination signal reception. 

Observability integration enriches health checks. Log each health state transition. Expose health check results as metrics (up/down per dependency). Alert on health state changes, not just complete failures. A dependency that is flapping between healthy and unhealthy indicates a more subtle problem than a dependency that is simply up or down — it suggests degraded performance or intermittent connectivity issues. 

Platform-specific implementations vary. Kubernetes supports HTTP, TCP, and command-based probes with configurable initial delay, period, timeout, success threshold, and failure threshold. AWS ALB health checks are simpler but support custom paths and codes. The application should implement a consistent health check endpoint regardless of platform, allowing platform-agnostic health assessment and easier migration between orchestration systems.

**See also:** [Graceful Shutdown Patterns](</en/architecture/graceful-shutdown.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>), [Timeout and Retry Patterns](</en/architecture/timeout-retry-patterns.html>).

**See also:** [Graceful Shutdown Patterns](</en/architecture/graceful-shutdown.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [Zero-Downtime Database Migrations](</en/architecture/database-migration-zero-downtime.html>)

**See also:** [Graceful Shutdown Patterns](</en/architecture/graceful-shutdown.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [Zero-Downtime Database Migrations](</en/architecture/database-migration-zero-downtime.html>)

**See also:** [Graceful Shutdown Patterns](</en/architecture/graceful-shutdown.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [Zero-Downtime Database Migrations](</en/architecture/database-migration-zero-downtime.html>)

**See also:** [Graceful Shutdown Patterns](</en/architecture/graceful-shutdown.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [Zero-Downtime Database Migrations](</en/architecture/database-migration-zero-downtime.html>)

**See also:** [Graceful Shutdown Patterns](</en/architecture/graceful-shutdown.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [Zero-Downtime Database Migrations](</en/architecture/database-migration-zero-downtime.html>)
