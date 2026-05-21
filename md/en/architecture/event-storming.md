---
title: "Event Storming"
description: "Learn event storming: big picture, process modeling, and design workshop techniques for domain exploration"
date: 2026-05-04
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/event-storming.html
---

# Event Storming

Event Storming is a collaborative workshop technique for exploring complex business domains. Created by Alberto Brandolini, it brings together domain experts, developers, and stakeholders to model business processes using colored sticky notes on a large wall. The technique is remarkably effective at surfacing domain knowledge, discovering inconsistencies, and designing software that aligns with business needs. 

The Basic Format 

Event Storming sessions use a large modeling surface—a physical wall covered in paper or a virtual whiteboard. Participants write domain events on orange sticky notes, using the past tense: "Order Placed", "Payment Received", "Item Shipped". These events represent something that happened in the domain. 

The session starts with domain experts writing events freely. As events accumulate, the group organizes them chronologically, creating a timeline of business activity. The facilitator guides the conversation, asking questions and highlighting areas of uncertainty. 

Big Picture Workshop 

The big picture workshop is the most common Event Storming format. It runs for several hours with a large group including domain experts, business stakeholders, developers, testers, and operations staff. The goal is to understand the entire domain landscape. 

During a big picture session, participants identify domain events, pain points (pink sticky notes), opportunities (green), and questions (yellow). The group also sketches bounded context boundaries around groups of related events. By the end, the team has a shared understanding of the domain's scope, pain points, and organizational boundaries. 

The big picture workshop is particularly valuable at the start of a project or when entering an unfamiliar domain. It quickly surfaces assumptions, reveals knowledge gaps, and builds shared understanding across the team. 

Process Modeling Workshop 

The process modeling workshop focuses on a single bounded context or a specific business process. It goes deeper than the big picture, adding commands (blue sticky notes) that trigger events, actors who issue commands, and policies or business rules (purple) that govern the process. 

This format identifies aggregates—the consistency boundaries around groups of events and commands. The group decides which events belong to which aggregate and how aggregates communicate. The output is a detailed model that can directly inform software design and implementation. 

Process modeling workshops typically run one to two days and include a focused group of domain experts and developers. The result is a shared model that the development team can implement with confidence. 

Design Workshop 

The design workshop is the most technical format. It takes the process model and designs the software architecture. Participants identify aggregate boundaries, repository needs, domain events for integration, and service interfaces. The output includes aggregate designs, event schemas, and bounded context interfaces. 

This format is well-suited for teams using Domain-Driven Design, CQRS, and Event Sourcing. The event storming output directly feeds into aggregate design, command handler definitions, and read model identification. 

Remote Event Storming 

With distributed teams, Event Storming has adapted to virtual formats. Tools like Miro, Mural, and specialized event storming tools provide virtual sticky notes and collaboration features. Remote sessions require more facilitation—clear timekeeping, explicit turn-taking, and regular check-ins. 

The core principles remain the same: start with events, organize chronologically, surface questions and pain points, and let the domain experts lead. Remote Event Storming has proven effective for distributed teams, though it requires more deliberate facilitation than in-person sessions. 

Benefits and Outcomes 

Event Storming produces several valuable outcomes: a shared understanding of the domain, identified bounded contexts, surfaced assumptions and inconsistencies, prioritized questions for further investigation, and a concrete model that translates directly into software design. The process is as valuable as the output—the conversations and discoveries during the workshop build team alignment that persists throughout the project.

**See also:** [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [Modular Monolith Architecture](</en/architecture/modular-monolith.html>), [Choreography Patterns](</en/architecture/choreography-patterns.html>).

**See also:** [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [Feature Flags Architecture](</en/architecture/feature-flags-architecture.html>)

**See also:** [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [Feature Flags Architecture](</en/architecture/feature-flags-architecture.html>)

**See also:** [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [Feature Flags Architecture](</en/architecture/feature-flags-architecture.html>)

**See also:** [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [Feature Flags Architecture](</en/architecture/feature-flags-architecture.html>)

**See also:** [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [Alerting Strategies for Production Systems](</en/architecture/alerting-strategies.html>), [Feature Flags Architecture](</en/architecture/feature-flags-architecture.html>)

**See also:** [Retry Patterns](</en/architecture/retry-patterns.html>), [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>), [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>)

**See also:** [Retry Patterns](</en/architecture/retry-patterns.html>), [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>), [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>)

**See also:** [Retry Patterns](</en/architecture/retry-patterns.html>), [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>), [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>)

**See also:** [Retry Patterns](</en/architecture/retry-patterns.html>), [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>), [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>)

**See also:** [Retry Patterns](</en/architecture/retry-patterns.html>), [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>), [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>)

**See also:** [Retry Patterns](</en/architecture/retry-patterns.html>), [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>), [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>)

**See also:** [Retry Patterns](</en/architecture/retry-patterns.html>), [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>), [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>)

**See also:** [Retry Patterns](</en/architecture/retry-patterns.html>), [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>), [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>)

**See also:** [Retry Patterns](</en/architecture/retry-patterns.html>), [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>), [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>)

**See also:** [Retry Patterns](</en/architecture/retry-patterns.html>), [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>), [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>)

**See also:** [Retry Patterns](</en/architecture/retry-patterns.html>), [Domain Event Implementation: Publishing, Handling, and Testing](</en/architecture/domain-event-implementation.html>), [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>)
