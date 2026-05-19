---
title: "DDD Strategic Design"
description: "Explore DDD strategic design: bounded context, context map, ubiquitous language, and domain integration patterns"
date: 2026-05-02
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/ddd-strategic.html
---

# DDD Strategic Design

Strategic Domain-Driven Design addresses the high-level organization of a software system around domain boundaries. While tactical patterns guide implementation within a single domain, strategic patterns define how domains relate to each other and how teams collaborate. This article covers bounded contexts, context maps, ubiquitous language, and integration patterns. 

Bounded Context 

A bounded context is a explicit boundary within which a particular domain model applies. Within the boundary, all terms have specific meanings, and the model is internally consistent. Outside the boundary, different terms or different meanings may apply. 

For example, in an e-commerce system, the concept of "Customer" may be different in the Sales context (someone who buys) than in the Support context (someone who needs help). Each bounded context has its own version of Customer with attributes relevant to that context. 

Identifying bounded contexts is the most critical strategic design activity. Contexts should be aligned with business capabilities and team structures. The general principle is that one team should own one bounded context, and the context boundary should align with the team's scope of responsibility. 

Context Map 

A context map documents the relationships between bounded contexts. It shows how different contexts integrate and where translations occur. Common relationship patterns include partnership (two teams collaborate on integration), shared kernel (shared subset of the model), customer-supplier (one context serves another), and conformist (one context conforms to another's model). 

The context map is both a design artifact and a communication tool. It helps teams understand their dependencies and negotiate integration contracts. A well-maintained context map reveals the system's architectural landscape at a glance. 

Ubiquitous Language 

Ubiquitous language is a shared language structured around the domain model. It is used by developers, domain experts, product managers, and all team members in conversations, documentation, code, and tests. The language is precise and unambiguous within each bounded context. 

Developing ubiquitous language requires continuous refinement. When a team discovers that a term has different meanings for different members, they investigate and resolve the ambiguity. The domain model evolves with the language, and the language evolves with the model. Code names should match spoken language terms. 

Integration Patterns 

Strategic DDD defines several patterns for integrating bounded contexts. Anti-corruption layers protect a context from being polluted by another context's model. Separate ways allow contexts to operate completely independently. Open-host service publishes a formal API for other contexts to consume. 

Published language defines a shared vocabulary used for integration, often taking the form of a data interchange format or API specification. Event-driven communication between contexts uses domain events to notify other contexts of state changes without tight coupling. 

When to Use Strategic DDD 

Strategic DDD is most valuable in complex domains with multiple teams and evolving requirements. It provides the tools to decompose a large system into manageable pieces, define clear ownership, and manage integrations. For simple systems with a single team, strategic DDD may add unnecessary overhead. 

The key insight of strategic DDD is that a single, unified model for an entire enterprise is neither achievable nor desirable. Different contexts need different models, and the boundaries between them should be consciously designed rather than accidental. Strategic thinking about boundaries, language, and relationships is what elevates DDD from a collection of patterns to a coherent design methodology.

**See also:** [DDD Tactical Patterns](</en/architecture/ddd-tactical.html>), [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>), [Event-Driven Architecture](</en/architecture/event-driven-arch.html>).

**See also:** [DDD Tactical Patterns](</en/architecture/ddd-tactical.html>), [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>)

**See also:** [DDD Tactical Patterns](</en/architecture/ddd-tactical.html>), [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>)

**See also:** [DDD Tactical Patterns](</en/architecture/ddd-tactical.html>), [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>)

**See also:** [DDD Tactical Patterns](</en/architecture/ddd-tactical.html>), [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>)

**See also:** [DDD Tactical Patterns](</en/architecture/ddd-tactical.html>), [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>)

**See also:** [Event Storming](</en/architecture/event-storming.html>), [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Orchestration Patterns](</en/architecture/orchestration-patterns.html>)

**See also:** [Event Storming](</en/architecture/event-storming.html>), [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Orchestration Patterns](</en/architecture/orchestration-patterns.html>)

**See also:** [Event Storming](</en/architecture/event-storming.html>), [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Orchestration Patterns](</en/architecture/orchestration-patterns.html>)

**See also:** [Event Storming](</en/architecture/event-storming.html>), [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Orchestration Patterns](</en/architecture/orchestration-patterns.html>)

**See also:** [Event Storming](</en/architecture/event-storming.html>), [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Orchestration Patterns](</en/architecture/orchestration-patterns.html>)

**See also:** [Event Storming](</en/architecture/event-storming.html>), [Materialized View Pattern](</en/architecture/materialized-view-pattern.html>), [Orchestration Patterns](</en/architecture/orchestration-patterns.html>)
