---
title: "Strangler Fig Pattern for Legacy Migration"
description: "Learn the strangler fig pattern for incrementally migrating legacy systems."
date: 2026-05-11
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/strangler-fig.html
---

The strangler fig pattern is a strategy for incrementally replacing a legacy system with a new one. Named after the strangler fig plant that grows around a host tree and eventually replaces it, this pattern allows you to migrate functionality piece by piece with minimal risk and zero downtime.

## Why Not a Big Bang Rewrite?

The traditional approach to legacy system replacement is the "big bang" rewrite: build the new system from scratch, then switch over in a single deployment. This approach has a terrible track record. Projects take longer than expected, fail to capture all the legacy system's behavior, and the switchover introduces immense risk.

The strangler fig pattern avoids these problems by replacing the system incrementally, one piece at a time.

## How It Works

The strangler fig pattern typically involves three components:

1. **An intercepting proxy or router** that sits in front of the legacy system.
2. **The legacy system** that continues to run.
3. **The new system** that gradually takes over functionality.

![Diagram: User -> Proxy -> either Legacy or New depending on migrated routes]

When a request arrives:
- If the requested functionality has been migrated, the proxy routes to the new system.
- If not, the proxy forwards to the legacy system.
- Over time, more routes are migrated until the legacy system is no longer needed.

## Implementation Approaches

### URL Routing

Use a reverse proxy (NGINX, HAProxy, API Gateway) to route traffic based on URL patterns:

```
# Initially: all traffic goes to legacy
location / {
    proxy_pass http://legacy-system;
}

# After migrating orders:
location /api/orders {
    proxy_pass http://new-system;
}
location / {
    proxy_pass http://legacy-system;
}
```

This is the simplest approach. New feature development happens on the new system. Legacy routes are progressively migrated.

### Feature Flags

Use feature flags to control migration at a more granular level:

```javascript
if (featureFlags.isEnabled('new-checkout')) {
    return renderNewCheckout(data);
} else {
    return proxyToLegacy(data);
}
```

Feature flags allow you to:
- Migrate at the feature level, not just the URL level.
- A/B test the new implementation against the old one.
- Roll back instantly if the new implementation has issues.
- Enable the new feature for a subset of users first.

### Parallel Run

For high-risk migrations, run both systems simultaneously and compare results:

1. Route the request to both systems.
2. Return the legacy system's response to the user.
3. Compare the new system's response to detect discrepancies.
4. Fix issues until responses match consistently.
5. Switch to the new system.

This is the safest approach and is commonly used for financial systems, inventory management, and other correctness-critical domains.

## Data Migration

Data migration is often the hardest part. Strategies include:

**Lazy migration:** When the new system needs data that exists only in the legacy system, it copies it on demand. The first time a user accesses a migrated feature, their data is migrated.

**Bulk migration:** Copy all data to the new system before cutting over. This requires data transformation and reconciliation.

**Dual writes:** Write to both systems for a period. The new system's data may need to be backfilled from the legacy system.

**Database strangler:** Use database views, triggers, or a change data capture (CDC) pipeline to keep the new system's database in sync with the legacy system.

Choose the approach based on data volume, the cost of inconsistency, and the complexity of data transformation.

## Benefits

**Reduced risk.** Each migration step is small and reversible. If something goes wrong, you roll back one feature, not the entire system.

**Continuous delivery.** The new system can be deployed incrementally. Teams get early feedback and can adjust course.

**Business continuity.** The legacy system remains operational throughout the migration. No downtime is required.

**Knowledge preservation.** Team members learn the legacy system gradually while building the new one. Domain knowledge is transferred naturally.

## Challenges

**Increased complexity.** The system is now running two architectures simultaneously. Developers need to understand both.

**Performance overhead.** Routing through a proxy adds latency. Running both systems in parallel doubles infrastructure costs.

**Coordination.** Multiple teams may be migrating different features. Coordination is needed to avoid conflicts.

**Legacy data dependencies.** Some data is deeply intertwined. Features that share data are harder to migrate independently.

## When to Use

Use the strangler fig pattern when:
- The legacy system is too large or complex to rewrite at once.
- You need to keep the system running during migration.
- The business cannot tolerate a long migration period without new features.

Do not use it when:
- The legacy system is small enough to rewrite quickly.
- The legacy system is being decommissioned entirely (no new features).

## Summary

The strangler fig pattern is the safest and most practical approach to legacy system migration. Use an intercepting proxy or feature flags to gradually route traffic from the legacy system to the new one. Migrate data lazily or in bulk depending on your requirements. Run both systems in parallel for high-risk migrations. The goal is not to replace the system quickly, but to replace it safely.
