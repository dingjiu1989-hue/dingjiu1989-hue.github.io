---
title: "Feature Flags Architecture"
description: "Flag evaluation, targeting rules, SDK design, flag management platforms, and best practices for feature flags"
date: 2026-04-24
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/feature-flags-architecture.html
---

# Feature Flags Architecture

Feature flags (also called feature toggles) provide runtime control over application behavior without deploying new code. They decouple deployment from release, enabling patterns like canary releases, A/B testing, trunk-based development, and instant rollbacks. The architecture of a feature flag system — how flags are evaluated, stored, distributed, and managed — is critical to both developer experience and system reliability. 

Flag evaluation must be fast and reliable. Every request potentially evaluates multiple flags, so evaluation latency directly impacts overall request latency. The two primary evaluation models are client-side SDK evaluation and server-side evaluation. In client-side evaluation, the SDK holds a copy of all flag configurations and evaluates locally — this provides sub-millisecond evaluation but requires flag configuration synchronization. In server-side evaluation, the client sends user context to a server that evaluates flags and returns results — this adds a network hop but provides centralized control and audit. 

SDK design follows a consistent pattern. The SDK initializes with a connection to the flag management service, downloads flag configurations, and stores them in memory. When the application requests a flag value, the SDK evaluates the flag locally using the targeting rules. The SDK periodically polls or receives real-time updates (WebSocket, Server-Sent Events) for configuration changes. This ensures that flag changes take effect quickly without redeployment. 

Targeting rules determine which users see which flag variations. Rules can be based on user attributes (ID, email, plan tier), request properties (device type, geographic region), or random percentage splits. Rules are typically evaluated in priority order — the first matching rule determines the variant. Rule engines must be deterministic: the same user context must always produce the same result, which is essential for testing and debugging. 

Percentage-based rollouts require consistent bucketing to maintain user experience. If a user is assigned to the 5% cohort for a feature, they should remain in that cohort across requests and sessions. This is achieved through hash-based bucketing: the user ID is hashed with the flag key to produce a consistent bucket assignment. The percentage threshold can be gradually increased as confidence in the feature grows. 

Flag management platforms provide the service-side infrastructure. LaunchDarkly is the market leader, providing a managed platform with sophisticated targeting, approval workflows, and analytics. Flagsmith, Split, and Unleash are alternatives with different tradeoffs in features, pricing, and deployment models. Self-hosted options like Unleash provide data sovereignty for compliance-sensitive industries. 

Flag lifecycle management is a practical challenge that grows with flag count. Dead flags — flags that have been rolled out to 100% or removed — must be cleaned up. The cleanup process involves: confirming the flag is stable at 100%, removing the flag evaluation code from the application, removing the flag from the management platform, and updating any dependent tests. Automated flag lifecycle tools can surface flags that have been at a constant value beyond a configurable threshold. 

Testing with feature flags requires special consideration. Tests should verify behavior for each flag variant. Parameterized tests that run the same test with each flag configuration catch regressions that only manifest under specific flag states. More importantly, tests should verify that removing the flag (when it is eventually retired) produces the expected behavior — the code should assume the flag-enabled state is the final state. 

Security implications of feature flags are significant. Flags that control security-sensitive behavior — authentication flows, authorization rules, payment processing — must be protected from unauthorized modification. Approval workflows, audit logs, and access controls on flag changes are essential. The flag management platform should enforce separation of duties: the developer who creates a flag should not be the one who approves its production rollout. 

Operational concerns include flag evaluation metrics. Track flag evaluation counts, cache hit rates, and evaluation latency. Monitor for unexpected flag evaluation errors — incorrectly cached or missing flag configurations can cause widespread failures. Implement a kill switch flag that disables all non-critical flags simultaneously in emergency scenarios, providing a circuit breaker for flag-induced issues.

**See also:** [Event-Driven Architecture](</en/architecture/event-driven-arch.html>), [Modular Monolith Architecture](</en/architecture/modular-monolith.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>).

**See also:** [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [Graceful Shutdown Patterns](</en/architecture/graceful-shutdown.html>), [Structured Logging](</en/architecture/structured-logging.html>)

**See also:** [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [Graceful Shutdown Patterns](</en/architecture/graceful-shutdown.html>), [Structured Logging](</en/architecture/structured-logging.html>)

**See also:** [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [Graceful Shutdown Patterns](</en/architecture/graceful-shutdown.html>), [Structured Logging](</en/architecture/structured-logging.html>)

**See also:** [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [Graceful Shutdown Patterns](</en/architecture/graceful-shutdown.html>), [Structured Logging](</en/architecture/structured-logging.html>)

**See also:** [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [Graceful Shutdown Patterns](</en/architecture/graceful-shutdown.html>), [Structured Logging](</en/architecture/structured-logging.html>)

**See also:** [Modular Monolith Architecture](</en/architecture/modular-monolith.html>), [Timeout and Retry Patterns](</en/architecture/timeout-retry-patterns.html>), [Zero-Downtime Deployment Strategies](</en/architecture/zero-downtime-deployment.html>)

**See also:** [Modular Monolith Architecture](</en/architecture/modular-monolith.html>), [Timeout and Retry Patterns](</en/architecture/timeout-retry-patterns.html>), [Zero-Downtime Deployment Strategies](</en/architecture/zero-downtime-deployment.html>)

**See also:** [Modular Monolith Architecture](</en/architecture/modular-monolith.html>), [Timeout and Retry Patterns](</en/architecture/timeout-retry-patterns.html>), [Zero-Downtime Deployment Strategies](</en/architecture/zero-downtime-deployment.html>)

**See also:** [Modular Monolith Architecture](</en/architecture/modular-monolith.html>), [Timeout and Retry Patterns](</en/architecture/timeout-retry-patterns.html>), [Zero-Downtime Deployment Strategies](</en/architecture/zero-downtime-deployment.html>)

**See also:** [Modular Monolith Architecture](</en/architecture/modular-monolith.html>), [Timeout and Retry Patterns](</en/architecture/timeout-retry-patterns.html>), [Zero-Downtime Deployment Strategies](</en/architecture/zero-downtime-deployment.html>)

**See also:** [Modular Monolith Architecture](</en/architecture/modular-monolith.html>), [Timeout and Retry Patterns](</en/architecture/timeout-retry-patterns.html>), [Zero-Downtime Deployment Strategies](</en/architecture/zero-downtime-deployment.html>)

**See also:** [Modular Monolith Architecture](</en/architecture/modular-monolith.html>), [Timeout and Retry Patterns](</en/architecture/timeout-retry-patterns.html>), [Zero-Downtime Deployment Strategies](</en/architecture/zero-downtime-deployment.html>)

**See also:** [Modular Monolith Architecture](</en/architecture/modular-monolith.html>), [Timeout and Retry Patterns](</en/architecture/timeout-retry-patterns.html>), [Zero-Downtime Deployment Strategies](</en/architecture/zero-downtime-deployment.html>)

**See also:** [Modular Monolith Architecture](</en/architecture/modular-monolith.html>), [Timeout and Retry Patterns](</en/architecture/timeout-retry-patterns.html>), [Zero-Downtime Deployment Strategies](</en/architecture/zero-downtime-deployment.html>)

**See also:** [Modular Monolith Architecture](</en/architecture/modular-monolith.html>), [Timeout and Retry Patterns](</en/architecture/timeout-retry-patterns.html>), [Zero-Downtime Deployment Strategies](</en/architecture/zero-downtime-deployment.html>)

**See also:** [Modular Monolith Architecture](</en/architecture/modular-monolith.html>), [Timeout and Retry Patterns](</en/architecture/timeout-retry-patterns.html>), [Zero-Downtime Deployment Strategies](</en/architecture/zero-downtime-deployment.html>)
