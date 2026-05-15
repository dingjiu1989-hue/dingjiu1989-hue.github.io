---
title: "Saga Orchestration Pattern"
description: "Coordinator pattern for distributed transactions, compensation strategies, state machines, and Temporal workflows"
date: 2026-05-12
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/saga-orchestration.html
---

# Saga Orchestration Pattern

## Saga Orchestration Pattern

## Saga Orchestration Pattern

## Saga Orchestration Pattern

## Saga Orchestration Pattern

## Saga Orchestration Pattern

## Saga Orchestration Pattern

## Saga Orchestration Pattern

## Saga Orchestration Pattern

## Saga Orchestration Pattern

## Saga Orchestration Pattern

## Saga Orchestration Pattern

## Saga Orchestration Pattern

Saga orchestration manages distributed transactions through a central coordinator that directs participating services through a sequence of local transactions. Unlike two-phase commit, sagas embrace eventual consistency — each step commits independently, and failures trigger compensating transactions to undo completed steps. The orchestrator provides clear workflow visibility, centralized error handling, and explicit state management. 

The orchestrator is a dedicated service responsible for executing the saga. It maintains the workflow state, sends commands to participants, receives results, and decides the next action. The state must be persisted durably — if the orchestrator crashes, it must resume precisely where it left off. This typically involves storing the saga instance state (current step, completed steps, accumulated data) in a database or workflow engine. 

Compensation is the mechanism for undoing completed steps. For each step that makes a forward change, the saga designer defines a compensating action that reverses that change. If step 3 fails, the orchestrator invokes the compensations for steps 2 and 1 in reverse order. Compensations must be idempotent — they may be called multiple times if the orchestrator fails during compensation execution. 

State machines provide a natural model for saga orchestration. The saga exists in one of several states: Pending, Active, Compensating, Completed, or Failed. Each step transition moves the saga to a new state. The orchestrator uses a state machine library or workflow engine to define available transitions, guard conditions, and timeout handling. This makes the saga logic explicit and testable. 

Temporal is a leading platform for saga orchestration. It provides durable execution of workflow functions — the workflow code is executed on a Temporal worker, and its state is persisted to the Temporal server. If the worker crashes, the workflow resumes from the last completed activity. Temporal handles retries, timeouts, and compensation automatically. The workflow developer writes straightforward sequential code, and Temporal ensures reliable execution. 

Concrete implementation requires careful step design. Each step should be a distinct activity with well-defined inputs, outputs, and failure modes. The orchestrator invokes activities through a command message or RPC call. Activities must be idempotent — the orchestrator may retry them on timeout or failure. Activity results are stored in the saga state for use by subsequent steps. 

Timeout management is critical. Each step has a timeout — if the activity does not complete within the window, the orchestrator determines the appropriate action. Idempotent activities can be retried. Non-idempotent activities may require human intervention or automatic compensation. The orchestrator should implement exponential backoff with jitter for transient failures and escalation policies for persistent failures. 

Data accumulation across saga steps requires careful modeling. The orchestrator accumulates data as it progresses through steps. The order creation saga collects the order ID from step 1, payment authorization from step 2, and shipping details from step 3. The saga state contract defines what data each step produces and what subsequent steps consume. This accumulated data may need to be persisted for auditing and recovery. 

Testing orchestrated sagas benefits from the explicit workflow definition. Unit tests verify state transitions and compensation logic. Integration tests verify end-to-end saga execution with actual service instances. Resilience tests verify recovery from orchestrator crashes, participant failures, and network partitions. The explicitness of orchestration makes these tests more comprehensive than testing equivalent choreographed sagas. 

Saga orchestration is the preferred pattern when workflows involve many participants, require strict compensation guarantees, or need auditable execution records. The trade-off is coupling to the orchestrator — but for complex business flows, this coupling provides the visibility and control that production systems require.

**See also:** [Orchestration Patterns](</en/architecture/orchestration-patterns.html>), [Event Collaboration: Choreography vs Orchestration](</en/architecture/event-collaboration.html>), [Saga vs Process Manager: Orchestration Patterns Compared](</en/architecture/saga-process-manager.html>).

**See also:** [Orchestration Patterns](</en/architecture/orchestration-patterns.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>), [Event Collaboration: Choreography vs Orchestration](</en/architecture/event-collaboration.html>)

**See also:** [Orchestration Patterns](</en/architecture/orchestration-patterns.html>), [API Composition and Aggregation](</en/architecture/api-composition.html>), [Event Collaboration: Choreography vs Orchestration](</en/architecture/event-collaboration.html>)
