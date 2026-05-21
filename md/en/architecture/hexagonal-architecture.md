---
title: "Hexagonal Architecture (Ports and Adapters)"
description: "Learn hexagonal architecture for building maintainable, testable applications — ports and adapters, dependency inversion, domain isolation, and migrating legacy code to hexagonal structure."
date: 2025-12-27
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/hexagonal-architecture.html
---

# Hexagonal Architecture (Ports and Adapters)

Hexagonal Architecture, also known as the Ports and Adapters pattern, was introduced by Alistair Cockburn to create applications that are isolated from their technical infrastructure. The core idea is that the application's business logic is at the center, communicating with the outside world through well-defined ports and adapters. This separation makes the application testable, maintainable, and adaptable to changing infrastructure. 

Core Concept 

In Hexagonal Architecture, the application core contains the domain logic and business rules. It defines ports—interfaces that express what the application needs from the outside world (driven ports) and what the outside world can do with the application (driving ports). Adapters implement these ports to connect the core to specific technologies. 

A driving adapter (like a web controller) triggers the application by calling a driving port. A driven adapter (like a database repository) implements a driven port that the application core calls. The core has no knowledge of which adapter is connected—it only knows the port interface. 

Domain Isolation 

The greatest benefit of Hexagonal Architecture is domain isolation. The business logic never imports or depends on frameworks, databases, or external services. It is pure code focused on the problem domain. This means you can unit test business logic without infrastructure, and you can swap technologies without changing business code. 

For example, if you replace PostgreSQL with MongoDB, you write a new repository adapter that implements the same port interface. The core remains completely unchanged. This isolation also makes it feasible to run the same application on different infrastructure configurations for different environments. 

Ports 

A port is an interface that defines a boundary interaction. Driving ports are use case interfaces that expose application capabilities to the outside world. They are called "inbound ports" and typically correspond to service methods or command handlers. 

Driven ports are interfaces for capabilities the application needs from infrastructure. They are called "outbound ports" and typically include repository interfaces, message publisher interfaces, and external API interfaces. The key constraint is that ports are defined by the application core, not by the infrastructure layer. 

Adapters 

Adapters implement ports to connect the core to specific technologies. A web controller adapter listens for HTTP requests, deserializes them, calls the appropriate driving port, and serializes the response. A JPA repository adapter implements a repository port using JPA and a relational database. A Kafka adapter implements a message publisher port using Kafka. 

Adapters can contain significant complexity related to their technology, but this complexity is contained and does not leak into the core. Adapters can also be replaced or configured differently per environment. 

Testing Benefits 

Hexagonal Architecture enables a testing strategy where the core is tested with unit tests using mock adapters, and adapters are tested with integration tests. Domain logic tests run in milliseconds with no infrastructure setup. Adapter tests verify that the implementation correctly interacts with the actual technology. 

This testing approach gives high confidence with fast feedback. The core tests verify business correctness. The adapter tests verify infrastructure integration. Combined, they provide comprehensive coverage without the fragility of end-to-end tests. 

Practical Implementation 

In practice, Hexagonal Architecture requires careful project structure. A common layout separates the project into `domain` (core), `application` (ports and use cases), and `infrastructure` (adapters) modules. Dependency injection frameworks wire the adapters to ports at application startup. 

The key to success is discipline about dependency direction. The core must never import infrastructure code. Tools like ArchUnit (Java) or custom linting rules can enforce this constraint automatically. 

Hexagonal Architecture pairs well with Domain-Driven Design, where the core contains the domain model and the ports express the domain's requirements from infrastructure. It also integrates naturally with Clean Architecture—the hexagonal core is the inner layer, and the adapters are the outer layers. For any long-lived application with significant business logic, the investment in hexagonal isolation pays substantial dividends.

**See also:** [Clean Architecture Explained](</en/architecture/clean-architecture.html>), [Serverless Architecture Patterns](</en/architecture/serverless-architecture.html>), [REST API Design Best Practices](</en/architecture/rest-api-design.html>).

**See also:** [Clean Architecture Explained](</en/architecture/clean-architecture.html>), [REST API Design Best Practices](</en/architecture/rest-api-design.html>), [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>)

**See also:** [Clean Architecture Explained](</en/architecture/clean-architecture.html>), [REST API Design Best Practices](</en/architecture/rest-api-design.html>), [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>)

**See also:** [Clean Architecture Explained](</en/architecture/clean-architecture.html>), [Strangler Fig Pattern for Legacy Migration](</en/architecture/strangler-fig.html>), [Backend for Frontend (BFF) Pattern](</en/architecture/backend-for-frontend.html>)

**See also:** [Clean Architecture Explained](</en/architecture/clean-architecture.html>), [Strangler Fig Pattern for Legacy Migration](</en/architecture/strangler-fig.html>), [Backend for Frontend (BFF) Pattern](</en/architecture/backend-for-frontend.html>)

**See also:** [Clean Architecture Explained](</en/architecture/clean-architecture.html>), [Strangler Fig Pattern for Legacy Migration](</en/architecture/strangler-fig.html>), [Backend for Frontend (BFF) Pattern](</en/architecture/backend-for-frontend.html>)

**See also:** [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Serverless Architecture Patterns](</en/architecture/serverless-architecture.html>), [Event Storming](</en/architecture/event-storming.html>)

**See also:** [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Serverless Architecture Patterns](</en/architecture/serverless-architecture.html>), [Event Storming](</en/architecture/event-storming.html>)

**See also:** [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Serverless Architecture Patterns](</en/architecture/serverless-architecture.html>), [Event Storming](</en/architecture/event-storming.html>)

**See also:** [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Serverless Architecture Patterns](</en/architecture/serverless-architecture.html>), [Event Storming](</en/architecture/event-storming.html>)

**See also:** [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Serverless Architecture Patterns](</en/architecture/serverless-architecture.html>), [Event Storming](</en/architecture/event-storming.html>)

**See also:** [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Serverless Architecture Patterns](</en/architecture/serverless-architecture.html>), [Event Storming](</en/architecture/event-storming.html>)

**See also:** [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Serverless Architecture Patterns](</en/architecture/serverless-architecture.html>), [Event Storming](</en/architecture/event-storming.html>)

**See also:** [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Serverless Architecture Patterns](</en/architecture/serverless-architecture.html>), [Event Storming](</en/architecture/event-storming.html>)

**See also:** [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Serverless Architecture Patterns](</en/architecture/serverless-architecture.html>), [Event Storming](</en/architecture/event-storming.html>)

**See also:** [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Serverless Architecture Patterns](</en/architecture/serverless-architecture.html>), [Event Storming](</en/architecture/event-storming.html>)

**See also:** [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Serverless Architecture Patterns](</en/architecture/serverless-architecture.html>), [Event Storming](</en/architecture/event-storming.html>)

**See also:** [Retry and Backoff Strategies](</en/architecture/retry-backoff.html>), [Serverless Architecture Patterns](</en/architecture/serverless-architecture.html>), [Event Storming](</en/architecture/event-storming.html>)
