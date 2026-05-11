---
title: "Backend for Frontend (BFF) Pattern"
description: "Learn the Backend for Frontend pattern for building client-specific APIs."
date: 2026-05-11
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/backend-for-frontend.html
---

The Backend for Frontend (BFF) pattern, introduced by Phil Calçado at SoundCloud, is an architectural approach where each client application (web, mobile, desktop) has its own dedicated backend. This pattern addresses the fundamental challenge of serving multiple client types from a single general-purpose API.

## The Problem

A single general-purpose API tries to serve all clients equally. This leads to several problems:

- **Over-fetching**: A web client needs user profile data plus recent orders, but the API returns only profile data. The web client must make additional requests.
- **Under-fetching**: A mobile client needs only a summary, but the API returns the full detailed object, wasting bandwidth and battery.
- **Different interaction patterns**: Web clients expect rich, chatty APIs. Mobile clients prefer fewer, larger responses to minimize network round trips.
- **Different data formats**: Desktop browsers can handle complex JSON. IoT devices may need compressed binary formats.

Developers end up building workarounds: adding query parameters for field selection, creating composite endpoints, or making multiple round trips. The BFF pattern solves this by providing a dedicated backend for each client.

## How BFF Works

Each client type has its own backend service:

```
[Mobile App] <-> [Mobile BFF] <-> [Shared Services]
                                            |
[Web App]    <-> [Web BFF]    <-> [Shared Services]
                                            |
[IoT Device] <-> [IoT BFF]   <-> [Shared Services]
```

Each BFF:
- Is owned by the same team that owns the client application.
- Understands the specific needs of its client.
- Aggregates data from multiple downstream services.
- Transforms data into the format most convenient for the client.
- Handles client-specific concerns like authentication, session management, and caching.

## Benefits

**Optimized client experience.** Each BFF returns exactly the data the client needs, in the format it prefers. Mobile APIs minimize data transfer. Web APIs support rich interactions. No more over-fetching or under-fetching.

**Simplified client code.** Complex logic moves from the client to the BFF. Data aggregation, transformation, and filtering happen on the server. The client becomes simpler and more focused on presentation.

**Independent evolution.** The web BFF can evolve independently from the mobile BFF. The web team can add endpoints for new browser features without affecting mobile users.

**Security isolation.** Each BFF can implement client-specific security policies. Mobile authentication might use device tokens. Web authentication might use cookie-based sessions.

**Team autonomy.** The web team owns the web BFF. The mobile team owns the mobile BFF. Teams can deploy independently without coordinating API changes.

## Real-World Example

Consider an e-commerce platform. A general-purpose API might return:

```json
{
  "product": {
    "id": "123",
    "name": "Wireless Mouse",
    "description": "...",
    "specifications": { ... },
    "reviews": [ ... ],
    "related_products": [ ... ],
    "inventory": { ... },
    "shipping_options": [ ... ],
    "price_history": [ ... ]
  }
}
```

The **Mobile BFF** tailors this for a phone:

```json
{
  "id": "123",
  "name": "Wireless Mouse",
  "price": "$29.99",
  "image_url": "thumb.jpg",
  "in_stock": true
}
```

The **Web BFF** provides richer data for a desktop browser:

```json
{
  "product": {
    "id": "123",
    "name": "Wireless Mouse",
    "price": "$29.99",
    "description": "...",
    "images": ["img1.jpg", "img2.jpg"],
    "reviews": {
      "summary": { "average": 4.5, "count": 128 },
      "top_reviews": [ ... ]
    }
  }
}
```

Each BFF is between 30-40 lines of server-side code, orchestrating calls to downstream services and shaping the response for its specific client.

## BFF vs. API Gateway

BFF and API Gateway are complementary patterns, not alternatives:

- **API Gateway** is a single entry point for all services, handling cross-cutting concerns like authentication, rate limiting, and routing.
- **BFF** is a specialized backend per client type, handling client-specific logic and data shaping.

In practice, a BFF often sits behind an API Gateway. The gateway handles shared infrastructure, and the BFF handles client-specific logic.

## When to Use BFF

Use BFF when:
- You have multiple client applications with significantly different needs.
- You want to minimize data transfer to mobile or low-bandwidth clients.
- Different teams own different client applications.
- Each client needs different authentication or session management.

Do not overuse BFF when:
- You have a single client application (e.g., web only). A general-purpose API is sufficient.
- Your API is already well-optimized for all clients through field selection and filtering.
- The overhead of running multiple backends outweighs the benefits.

## Potential Drawbacks

**Increased operational complexity.** More services to deploy, monitor, and maintain. Each BFF adds infrastructure overhead.

**Code duplication.** Common logic may be duplicated across BFFs. Be disciplined about extracting shared services.

**Larger team responsibility.** The team must maintain both the client application and its BFF.

## Summary

The BFF pattern provides dedicated backends for each client application, optimizing data delivery and simplifying client code. Use BFFs when you have multiple distinct clients with different needs. Combine with an API Gateway for cross-cutting concerns. Avoid premature adoption -- for single-client applications, a well-designed general-purpose API is sufficient.
