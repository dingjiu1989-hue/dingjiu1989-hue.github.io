---
title: "A/B Testing Infrastructure"
description: "Experiment frameworks, traffic assignment, statistical analysis, and infrastructure for A/B testing at scale"
date: 2026-04-21
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/a-b-testing-infrastructure.html
---

# A/B Testing Infrastructure

A/B testing infrastructure enables organizations to make data-driven decisions by comparing user experiences against a control group. At its core, an A/B testing system must: consistently assign users to experiment groups, reliably track metrics for each group, perform statistical analysis to determine significance, and manage the lifecycle of experiments from creation to analysis. The infrastructure requirements scale with experiment volume, traffic, and statistical rigor. 

Experiment assignment uses deterministic bucketing. A consistent hash of the user identifier and experiment key determines which variant the user sees. This ensures the user remains in the same variant across sessions. The hash function must distribute users uniformly across variants. Common approaches include MD5 or SHA-256 hashed to a modulus, or using the MurmurHash for better distribution characteristics. The assignment function should produce the same result regardless of the order experiments are evaluated. 

The assignment infrastructure must handle overlapping experiments. Users may participate in multiple experiments simultaneously. Each experiment uses a unique salt or namespace in the hash computation, ensuring that participation in one experiment does not correlate with participation in another. This prevents interaction effects where users in variant A of experiment 1 are disproportionately likely to be in variant B of experiment 2. 

Metrics collection is a two-phase process. The first phase captures exposure events — recording which users were assigned to which variant at the moment of assignment. The second phase captures outcome events — purchases, clicks, signups — with their associated experiment context. Both events must carry the experiment ID, variant, and a consistent user identifier. The event pipeline must handle late-arriving events, out-of-order events, and event deduplication. 

Statistical analysis determines whether observed differences are significant. Frequentist approaches use hypothesis testing (t-test, chi-square) with p-values and confidence intervals. Bayesian approaches model the posterior distribution of the metric difference and report the probability that one variant outperforms another. Sequential testing methods allow continuous monitoring without inflating false positive rates — essential for stopping experiments early when results are clear. 

Sample ratio mismatch (SRM) is a critical quality check. The actual assignment ratio should match the expected ratio (e.g., 50/50). SRM indicates that user assignment is biased — perhaps due to caching, client-side logic failures, or network issues. Automated SRM detection using a chi-square test should run on every experiment before any conclusions are drawn. An experiment with SRM should be invalidated until the root cause is identified. 

Novelty effects and carryover effects require attention. Novelty effects cause users to behave differently simply because something is new — the effect diminishes over time. Carryover effects occur when a user's experience in one experiment affects their behavior in a subsequent experiment. Mitigations include: running experiments long enough for novelty to wear off, implementing washout periods between experiments for the same user, and cross-experiment randomization that accounts for history. 

Infrastructure must handle experiment lifecycle. Create: an experiment is defined with its variants, targeting rules, and metrics. Start: traffic begins flowing to the experiment. Analyze: data accumulates and statistical analysis runs. Conclude: the experiment is analyzed and a decision is made. Cleanup: variant-specific code and flag configurations are removed. The platform should automate cleanup reminders for experiments that have been running beyond their intended duration. 

Client-side experimentation introduces additional challenges. The experiment data must be available on the client for assignment, which exposes targeting rules and variant definitions. The assignment must happen before the user sees any content, making synchronous loading critical. Client-side events may be lost due to ad blockers, network failures, or page abandonment. Server-side supplementation provides a fallback for critical metrics. 

The experiment platform should provide self-service capabilities for product managers and data scientists without requiring engineering involvement for every experiment. The self-service interface should support: experiment definition through a UI, automated statistical analysis with guardrail metrics, and rollback of underperforming experiments with a single click. This democratizes experimentation and increases the velocity of data-driven decision-making.

**See also:** [Global Traffic Routing](</en/architecture/global-traffic-routing.html>), [Service Mesh Deep Dive](</en/architecture/service-mesh-deep.html>), [Chaos Engineering: Building Resilient Systems](</en/architecture/chaos-engineering.html>).

**See also:** [Blue-Green Deployment Strategy](</en/architecture/blue-green-deployment.html>), [Chaos Engineering: Building Resilient Systems](</en/architecture/chaos-engineering.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>)

**See also:** [Blue-Green Deployment Strategy](</en/architecture/blue-green-deployment.html>), [Chaos Engineering: Building Resilient Systems](</en/architecture/chaos-engineering.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>)

**See also:** [Blue-Green Deployment Strategy](</en/architecture/blue-green-deployment.html>), [Chaos Engineering: Building Resilient Systems](</en/architecture/chaos-engineering.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>)

**See also:** [Blue-Green Deployment Strategy](</en/architecture/blue-green-deployment.html>), [Chaos Engineering: Building Resilient Systems](</en/architecture/chaos-engineering.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>)

**See also:** [Blue-Green Deployment Strategy](</en/architecture/blue-green-deployment.html>), [Chaos Engineering: Building Resilient Systems](</en/architecture/chaos-engineering.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>)

**See also:** [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [Feature Flags Architecture](</en/architecture/feature-flags-architecture.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>)

**See also:** [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [Feature Flags Architecture](</en/architecture/feature-flags-architecture.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>)

**See also:** [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [Feature Flags Architecture](</en/architecture/feature-flags-architecture.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>)

**See also:** [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [Feature Flags Architecture](</en/architecture/feature-flags-architecture.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>)

**See also:** [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [Feature Flags Architecture](</en/architecture/feature-flags-architecture.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>)

**See also:** [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [Feature Flags Architecture](</en/architecture/feature-flags-architecture.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>)

**See also:** [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [Feature Flags Architecture](</en/architecture/feature-flags-architecture.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>)

**See also:** [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [Feature Flags Architecture](</en/architecture/feature-flags-architecture.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>)

**See also:** [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [Feature Flags Architecture](</en/architecture/feature-flags-architecture.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>)

**See also:** [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [Feature Flags Architecture](</en/architecture/feature-flags-architecture.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>)

**See also:** [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [Feature Flags Architecture](</en/architecture/feature-flags-architecture.html>), [API Gateway vs Service Mesh](</en/architecture/gateway-vs-mesh.html>)
