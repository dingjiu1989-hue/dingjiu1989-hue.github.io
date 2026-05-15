---
title: "Event Collaboration: Choreography vs Orchestration"
description: "Event-driven collaboration patterns, saga execution, choreography vs orchestration, error handling in distributed workflows"
date: 2026-05-12
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/event-collaboration.html
---

# Event Collaboration: Choreography vs Orchestration

## Event Collaboration: Choreography vs Orchestration

## Event Collaboration: Choreography vs Orchestration

## Event Collaboration: Choreography vs Orchestration

## Event Collaboration: Choreography vs Orchestration

## Event Collaboration: Choreography vs Orchestration

## Event Collaboration: Choreography vs Orchestration

## Event Collaboration: Choreography vs Orchestration

## Event Collaboration: Choreography vs Orchestration

## Event Collaboration: Choreography vs Orchestration

## Event Collaboration: Choreography vs Orchestration

## Event Collaboration: Choreography vs Orchestration

## Event Collaboration: Choreography vs Orchestration

Event collaboration is the architectural pattern where services communicate through events rather than direct requests. This shifts the coordination model from asking (request-response) to telling (event notification). Two fundamental patterns govern how these collaborations are structured: choreography, where each service independently responds to events, and orchestration, where a central coordinator directs the workflow. 

In choreography, services are loosely coupled through events. When a service completes an operation, it publishes an event. Other services subscribe to relevant events and react accordingly. There is no central controller — the workflow emerges from the collective behavior of participating services. For example, when the Order Service creates an order, it publishes an OrderCreated event. The Inventory Service subtracts stock, the Payment Service charges the customer, and the Shipping Service schedules delivery — each acting independently. 

Choreography's strength is decoupling. Services have no direct knowledge of each other, only of the events they produce and consume. New services can join the workflow by subscribing to existing events without modifying any existing service. This aligns naturally with domain-driven design and bounded contexts. The trade-off is visibility: the overall workflow is not explicitly defined anywhere, making it difficult to understand, monitor, and debug. 

Orchestration centralizes workflow control in an orchestrator service. The orchestrator tells each service what to do and when. A coordinator pattern, often implemented as a state machine or workflow engine, tracks the progress of each workflow instance. Temporal, Camunda, and AWS Step Functions are common orchestration platforms. The orchestrator sends commands to services, receives results, and decides the next step. 

Orchestration provides clear visibility. The workflow is explicitly defined in code or configuration, making it straightforward to understand, test, and modify. Error handling is centralized — the orchestrator knows the complete workflow state and can execute compensating actions. The trade-off is coupling: the orchestrator becomes a central dependency that all services must interact with, creating a potential bottleneck and a single point of failure. 

Saga patterns apply both choreography and orchestration to manage distributed transactions. A saga is a sequence of local transactions where each step publishes an event or message that triggers the next step. If a step fails, compensating transactions undo the preceding steps. In choreographed sagas, each service knows how to compensate for its own operations. In orchestrated sagas, the coordinator maintains a list of completed steps and their compensations. 

Error handling differs significantly between the two approaches. In choreography, each service handles errors independently. If the Payment Service fails after Inventory Service has already deducted stock, the Inventory Service must subscribe to a PaymentFailed event and restore stock. This requires each service to anticipate and handle failure scenarios for every event it reacts to. Missing a compensation path can leave the system in an inconsistent state. 

In orchestration, the coordinator tracks state and invokes compensations in reverse order. This makes error handling more manageable to implement and verify. However, the coordinator itself must be highly available and its state durable. If the coordinator fails mid-workflow, it must recover precisely where it left off — requiring persistent workflow state and idempotent service operations. 

Many production systems combine both patterns. Orchestration manages core business flows that require strict consistency guarantees. Choreography handles peripheral flows where eventual consistency and loose coupling are more valuable than workflow visibility. The choice depends on the criticality of the flow, the number of participating services, and the organization's tolerance for implicit versus explicit workflow definitions.

**See also:** [Saga Choreography Pattern](</en/architecture/saga-choreography.html>), [Saga vs Process Manager: Orchestration Patterns Compared](</en/architecture/saga-process-manager.html>), [Choreography Patterns](</en/architecture/choreography-patterns.html>).

**See also:** [Saga Choreography Pattern](</en/architecture/saga-choreography.html>), [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>), [Choreography Patterns](</en/architecture/choreography-patterns.html>)

**See also:** [Saga Choreography Pattern](</en/architecture/saga-choreography.html>), [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>), [Choreography Patterns](</en/architecture/choreography-patterns.html>)
