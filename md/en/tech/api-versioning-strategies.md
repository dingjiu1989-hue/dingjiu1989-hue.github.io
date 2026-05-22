---
title: "API Versioning Strategies: URL, Header, and Query Parameter Approaches Compared"
description: "Compare every API versioning strategy — URI path, Accept header, query parameters, and rolling versioning with real-world trade-offs."
date: 2025-10-17
board: tech
url: https://aidev.fit/en/tech/api-versioning-strategies.html
---

# API Versioning Strategies: URL, Header, and Query Parameter Approaches Compared

API versioning is one of those decisions that seems trivial — "just add /v2/" — until you have 50 clients on v1, 30 on v2, and a breaking change you need to roll out. The versioning strategy you choose affects every client integration, every SDK, and every internal team that depends on your API. This guide compares every major API versioning approach and helps you pick the least painful one.

## API Versioning Strategies Compared

Strategy| Example| Pros| Cons| Best For  
---|---|---|---|---  
URI Path| /api/v2/users| Most visible, easy to test, easy to route, cache-friendly| URL changes; "v2" in URL forever; URL pollution| Public APIs, REST APIs, external consumers  
Accept Header (Content Negotiation)| Accept: application/vnd.api+json;version=2| Clean URLs, no URL versioning, REST purist-friendly| Harder to test (curl -H), harder to cache (CDN), invisible| Internal APIs, REST purists, when URL cleanliness matters  
Query Parameter| /api/users?version=2| Easy default (no version = latest), simple to test| Easy to forget, cache key complexity, pollutes parameters| Simple APIs, internal tools, when path versioning is blocked  
Custom Header| X-API-Version: 2026-05-01| Clean URLs, date-based (intuitive), easy to deprecate| Invisible, hard to discover, hard to test, CDN issues| Stripe-style date-based versioning, API gateways  
Hostname / Subdomain| v2.api.example.com| Complete isolation, can run separate services| DNS management, SSL certificates, infrastructure complexity| Major breaking changes, completely different implementations  
  
## Date-Based vs Semantic Versioning

Approach| Example| Best For| Pioneered By  
---|---|---|---  
Date-Based (Calendar Versioning)| 2026-05-01| APIs that evolve continuously with many small changes| Stripe, Twilio, AWS  
Semantic (Major.Minor)| v1, v2, v3| APIs with clear, infrequent major breaking changes| GitHub, most REST APIs  
Rolling (No Version)| No version identifier| Internal APIs, GraphQL (deprecation instead of versioning)| GraphQL, internal services  
  
## Stripe's Versioning Model (The Gold Standard)
    
    
    # Stripe's approach: date-based versioning via custom header
    # Stripe-Version: 2026-05-01
    
    # Key principles:
    # 1. Every API request is pinned to a specific version date
    # 2. New features are added without breaking existing code
    # 3. Breaking changes: old behavior is maintained for old versions
    # 4. Upgrading is explicit: change the date, test, deploy
    # 5. Old versions are supported for a long time (years)
    
    # Why this works:
    # - No URL changes ever
    # - Clients control when they upgrade
    # - Backward compatibility is the API's responsibility, not the client's
    # - Can ship changes daily without breaking anyone

## How to Deprecate an API Version Without Making Enemies

Step| What to Do| Timeline  
---|---|---  
1\. Announce| Email all users of the old version, add deprecation header (Sunset, Deprecation)| 6-12 months before shutdown  
2\. Monitor| Track who is still on old version, reach out personally to high-usage clients| Ongoing  
3\. Warn| Add deprecation warnings in API responses, documentation banners| 3-6 months before shutdown  
4\. Rate Limit| Slow down old version responses (add 100ms latency, then 500ms)| 1-3 months before shutdown  
5\. Shut Down| Return 410 Gone with clear error message + upgrade link| After announced date  
  
**Bottom line:** For public REST APIs, URI path versioning (/v2/) is the most practical — it is visible, easy to test, and works with all HTTP tooling. For developer-focused APIs, date-based versioning (Stripe model) is more elegant but requires more infrastructure. The key is not the format — it is maintaining backward compatibility and giving clients 6-12 months to migrate when you do break things. See also: [REST API Best Practices](</en/tech/rest-api-best-practices.html>) and [API Design Patterns](</en/tech/api-design-patterns.html>).

**See also:** [Git Workflows: Git Flow vs GitHub Flow vs Trunk-Based Development](</en/tech/git-workflows-team-guide.html>), [Caching Strategies for Web Apps: CDN, Redis, Browser, and API Caching](</en/tech/caching-strategies-web-apps.html>), [Node.js Streams: Complete Guide to Efficient Data Processing](</en/tech/nodejs-streams-guide.html>)
