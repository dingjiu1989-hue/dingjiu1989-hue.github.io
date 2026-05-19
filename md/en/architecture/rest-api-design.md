---
title: "REST API Design Best Practices"
description: "Learn REST API design best practices for building scalable, maintainable web APIs."
date: 2025-12-29
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/rest-api-design.html
---

# REST API Design Best Practices

REST (Representational State Transfer) remains the dominant architectural style for web APIs. A well-designed REST API is intuitive, consistent, and easy to maintain. This article covers the core principles and practical guidelines for designing REST APIs that developers love to use. 

Use Consistent Resource Naming 

Your API endpoints represent resources. Use nouns, not verbs, and stick to a consistent naming convention. 

GET /users # Good

GET /getUsers # Bad

POST /createUser # Bad

Use plural nouns for collections (`/users`, `/orders`) and nest resources to express relationships (`/users/123/orders`). Avoid deep nesting beyond two or three levels. If you find yourself nesting four levels deep, consider flattening the structure or using query parameters. 

Leverage HTTP Methods Correctly 

Each HTTP method has a specific semantic meaning. Use them correctly: 

  * `GET` — Retrieve a resource or collection. Idempotent and safe.

  * `POST` — Create a new resource. Not idempotent.

  * `PUT` — Replace an entire resource. Idempotent.

  * `PATCH` — Partially update a resource. Idempotent when used with merge-style patches.

  * `DELETE` — Remove a resource. Idempotent.




A common mistake is using POST for everything. Proper method usage makes your API self-documenting and allows HTTP clients to make intelligent caching and retry decisions. 

Use Proper HTTP Status Codes 

Your API should return meaningful status codes. Group them logically: 

  * **2xx Success** : `200 OK` for successful GET/PUT/PATCH, `201 Created` for POST, `204 No Content` for DELETE.

  * **3xx Redirection** : `301 Moved Permanently`, `303 See Other` for redirecting after a POST.

  * **4xx Client Error** : `400 Bad Request` for malformed input, `401 Unauthorized` when authentication is missing, `403 Forbidden` when the user lacks permission, `404 Not Found`, `409 Conflict` for duplicate resources, `422 Unprocessable Entity` for validation errors.

  * **5xx Server Error** : `500 Internal Server Error`, `502 Bad Gateway`, `503 Service Unavailable`.




Returning `200 OK` for everything forces API consumers to inspect the response body to determine success or failure. This defeats the purpose of HTTP status codes. 

Pagination, Filtering, and Sorting 

Collections should always support pagination, filtering, and sorting. 

GET /users?page=2&per;_page=20

GET /users?sort=created_atℴ=desc

GET /users?filter[status]=active

Return pagination metadata in the response: 

{

"data": [...],

"pagination": {

"page": 2,

"per_page": 20,

"total": 153,

"total_pages": 8

}

}

Using cursor-based pagination is recommended for large, frequently updated datasets, as it is more performant than offset-based pagination. 

Consistent Error Responses 

Design a standard error response format and use it everywhere: 

{

"error": {

"code": "VALIDATION_ERROR",

"message": "Validation failed",

"details": [

{ "field": "email", "message": "Must be a valid email address" }

]

}

}

Include a machine-readable error code, a human-readable message, and detailed validation errors when appropriate. This allows clients to handle errors programmatically. 

Versioning 

APIs evolve. Plan for it from day one. The simplest approach is URL-based versioning: 

/api/v1/users

/api/v2/users

Header-based versioning (e.g., `Accept: application/vnd.myapi.v1+json`) is more RESTful but harder for clients to discover. Choose whichever approach your consumers will find more intuitive. 

Use HATEOAS for Discoverability 

HATEOAS (Hypermedia as the Engine of Application State) includes links in responses to guide clients: 

{

"id": 123,

"name": "John Doe",

"_links": {

"self": { "href": "/users/123" },

"orders": { "href": "/users/123/orders" }

}

}

While many APIs skip HATEOAS, it significantly improves discoverability and reduces the need for external documentation for navigating resource relationships. 

Authentication and Authorization 

Use industry-standard authentication mechanisms. Token-based auth (JWT) is the most common choice for REST APIs. Include tokens in the `Authorization` header: 

Authorization: Bearer 

Use scopes or claims within the token to implement fine-grained authorization. Always use HTTPS in production to protect tokens and data in transit. 

Rate Limiting 

Protect your API from abuse by implementing rate limiting. Return rate limit information in response headers: 

X-RateLimit-Limit: 100

X-RateLimit-Remaining: 42

X-RateLimit-Reset: 1640995200

When a client exceeds the limit, return `429 Too Many Requests` with a `Retry-After` header. 

Documentation 

An API is only as good as its documentation. Use OpenAPI/Swagger to document your API. Generate interactive documentation that allows developers to test endpoints directly from the browser. Keep your documentation in sync with your implementation by using a code-first approach where the OpenAPI spec is generated from annotations in your code. 

Summary 

Great REST API design comes down to consistency and following conventions. Use proper HTTP methods and status codes, name resources with plural nouns, version your API, and document it thoroughly. When in doubt, follow the principle of least surprise -- your API should work the way developers expect it to.

**See also:** [Backend for Frontend (BFF) Pattern](</en/architecture/backend-for-frontend.html>), [Hexagonal Architecture (Ports and Adapters)](</en/architecture/hexagonal-architecture.html>), [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>).

**See also:** [Backend for Frontend (BFF) Pattern](</en/architecture/backend-for-frontend.html>), [Hexagonal Architecture (Ports and Adapters)](</en/architecture/hexagonal-architecture.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>)

**See also:** [Backend for Frontend (BFF) Pattern](</en/architecture/backend-for-frontend.html>), [Hexagonal Architecture (Ports and Adapters)](</en/architecture/hexagonal-architecture.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>)

**See also:** [Backend for Frontend (BFF) Pattern](</en/architecture/backend-for-frontend.html>), [Hexagonal Architecture (Ports and Adapters)](</en/architecture/hexagonal-architecture.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>)

**See also:** [Backend for Frontend (BFF) Pattern](</en/architecture/backend-for-frontend.html>), [Hexagonal Architecture (Ports and Adapters)](</en/architecture/hexagonal-architecture.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>)

**See also:** [Backend for Frontend (BFF) Pattern](</en/architecture/backend-for-frontend.html>), [Hexagonal Architecture (Ports and Adapters)](</en/architecture/hexagonal-architecture.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>)

**See also:** [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Serverless Architecture Patterns](</en/architecture/serverless-architecture.html>), [Graceful Shutdown Patterns](</en/architecture/graceful-shutdown.html>)

**See also:** [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Serverless Architecture Patterns](</en/architecture/serverless-architecture.html>), [Graceful Shutdown Patterns](</en/architecture/graceful-shutdown.html>)

**See also:** [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Serverless Architecture Patterns](</en/architecture/serverless-architecture.html>), [Graceful Shutdown Patterns](</en/architecture/graceful-shutdown.html>)

**See also:** [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Serverless Architecture Patterns](</en/architecture/serverless-architecture.html>), [Graceful Shutdown Patterns](</en/architecture/graceful-shutdown.html>)

**See also:** [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Serverless Architecture Patterns](</en/architecture/serverless-architecture.html>), [Graceful Shutdown Patterns](</en/architecture/graceful-shutdown.html>)

**See also:** [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Serverless Architecture Patterns](</en/architecture/serverless-architecture.html>), [Graceful Shutdown Patterns](</en/architecture/graceful-shutdown.html>)

**See also:** [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Serverless Architecture Patterns](</en/architecture/serverless-architecture.html>), [Graceful Shutdown Patterns](</en/architecture/graceful-shutdown.html>)
