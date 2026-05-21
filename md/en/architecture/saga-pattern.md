---
title: "Saga Pattern for Distributed Transactions"
description: "Learn the saga pattern for managing distributed transactions across microservices."
date: 2025-12-30
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/saga-pattern.html
---

# Saga Pattern for Distributed Transactions

The Saga pattern manages distributed transactions across multiple services without requiring two-phase commit. Instead of a single, atomic distributed transaction, a saga breaks the operation into a series of local transactions, each with a compensating action that can undo its effects if a subsequent step fails. This article examines the two saga implementation approaches, compensation design, and monitoring strategies. 

The Need for Sagas 

In a microservice architecture, a single business operation often spans multiple services. An order placement might involve the order service, payment service, inventory service, and shipping service. Each service has its own database, so traditional database transactions cannot span all of them. 

Without distributed transaction coordination, a partial failure leaves the system in an inconsistent state. If payment succeeds but inventory reservation fails, the system has paid for an order that cannot be fulfilled. The Saga pattern ensures that either all steps complete successfully or compensating actions reverse the completed steps. 

Choreography-Based Saga 

In choreography-based sagas, each service performs its local transaction and emits an event. The event triggers the next service's transaction. If a service fails, it emits a failure event that triggers compensating actions in earlier services. 

Choreography sagas are loosely coupled. Services do not need to know about a saga coordinator. However, the saga logic is distributed across services, making it harder to understand the complete workflow. Monitoring requires reconstructing the saga state from multiple event streams. 

Choreography works best for simple sagas with few participants and straightforward compensation logic. As sagas grow in complexity, orchestration becomes more manageable. 

Orchestration-Based Saga 

In orchestration-based sagas, a saga orchestrator (or coordinator) controls the workflow. The orchestrator tells each service what to do, tracks which steps have completed, and calls compensating actions when failures occur. The orchestrator is the single source of truth for saga state. 

Orchestration provides better visibility and control. The orchestrator's state explicitly shows where each saga instance is in the workflow. Error handling and compensation are centralized, making the saga easier to reason about and test. Temporal, AWS Step Functions, and Camunda are common orchestration platforms. 

The trade-off is coupling. The orchestrator must know about all participants and their APIs. Changes to participant interfaces may require changes to the orchestrator. 

Compensation Design 

Compensation is the heart of the Saga pattern. Each step in a saga must have a compensating action that semantically undoes its effects. The compensation should be written assuming the original operation may have partially completed—it should be idempotent and handle cases where the original data may have changed. 

Compensation differs from rollback in traditional transactions. A rollback restores the exact prior state. A compensation applies a new business transaction to reverse the effect. For example, if the payment step debited $50, the compensation credits $50 back. If interest has accrued, the compensation amount may differ. 

Compensations may themselves fail. Saga implementations should have retry logic for compensation failures and an escalation path for compensations that cannot be completed automatically. 

Monitoring Sagas 

Monitoring sagas requires tracking each saga instance's current step, the time spent in each step, and the outcome. Distributed tracing with correlation IDs ties saga events across services. Metrics should track saga duration, success rate, failure rate by step, and compensation rate. 

Alerting should fire when sagas remain in a non-terminal state beyond a threshold, when compensation rates exceed normal levels, or when specific steps consistently fail. Operational dashboards show the current state of all in-flight sagas and recent failures. 

Implementation Best Practices 

Each saga step should be idempotent—processing the same command twice should have the same effect. This allows safe retries when responses are lost. Commands should include an idempotency key that the participant uses to detect duplicates. 

Saga orchestrators should persist their state to survive failures. If the orchestrator restarts, it should recover the state of all in-flight sagas and continue from where it left off. Workflow engines like Temporal handle this automatically. 

Saga timeouts should prevent steps from waiting indefinitely. Each step should have a timeout, and the orchestrator should handle timeout failures by initiating compensation. The overall saga should have a maximum duration to detect stalled instances. 

The Saga pattern is essential for maintaining data consistency in distributed systems without sacrificing the autonomy and scalability of individual services. When designed with careful compensation logic and robust monitoring, sagas provide reliable distributed transaction semantics with manageable complexity.

**See also:** [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>), [Bulkhead Pattern for Resilience](</en/architecture/bulkhead-pattern.html>), [Database per Service Pattern](</en/architecture/database-per-service.html>).

**See also:** [Bulkhead Pattern for Resilience](</en/architecture/bulkhead-pattern.html>), [Database per Service Pattern](</en/architecture/database-per-service.html>), [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>)

**See also:** [Bulkhead Pattern for Resilience](</en/architecture/bulkhead-pattern.html>), [Database per Service Pattern](</en/architecture/database-per-service.html>), [Saga Orchestration Pattern](</en/architecture/saga-orchestration.html>)

**See also:** [Database per Service Pattern](</en/architecture/database-per-service.html>), [Backend for Frontend (BFF) Pattern](</en/architecture/backend-for-frontend.html>), [Bulkhead Pattern for Resilience](</en/architecture/bulkhead-pattern.html>)

**See also:** [Database per Service Pattern](</en/architecture/database-per-service.html>), [Backend for Frontend (BFF) Pattern](</en/architecture/backend-for-frontend.html>), [Bulkhead Pattern for Resilience](</en/architecture/bulkhead-pattern.html>)

**See also:** [Database per Service Pattern](</en/architecture/database-per-service.html>), [Backend for Frontend (BFF) Pattern](</en/architecture/backend-for-frontend.html>), [Bulkhead Pattern for Resilience](</en/architecture/bulkhead-pattern.html>)

**See also:** [Strangler Fig Pattern for Legacy Migration](</en/architecture/strangler-fig.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>), [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>)

**See also:** [Strangler Fig Pattern for Legacy Migration](</en/architecture/strangler-fig.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>), [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>)

**See also:** [Strangler Fig Pattern for Legacy Migration](</en/architecture/strangler-fig.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>), [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>)

**See also:** [Strangler Fig Pattern for Legacy Migration](</en/architecture/strangler-fig.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>), [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>)

**See also:** [Strangler Fig Pattern for Legacy Migration](</en/architecture/strangler-fig.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>), [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>)

**See also:** [Strangler Fig Pattern for Legacy Migration](</en/architecture/strangler-fig.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>), [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>)

**See also:** [Strangler Fig Pattern for Legacy Migration](</en/architecture/strangler-fig.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>), [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>)

**See also:** [Strangler Fig Pattern for Legacy Migration](</en/architecture/strangler-fig.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>), [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>)

**See also:** [Strangler Fig Pattern for Legacy Migration](</en/architecture/strangler-fig.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>), [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>)

**See also:** [Strangler Fig Pattern for Legacy Migration](</en/architecture/strangler-fig.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>), [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>)

**See also:** [Strangler Fig Pattern for Legacy Migration](</en/architecture/strangler-fig.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>), [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>)

**See also:** [Strangler Fig Pattern for Legacy Migration](</en/architecture/strangler-fig.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>), [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>)
