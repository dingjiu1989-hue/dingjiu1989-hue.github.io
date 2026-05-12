---
title: "Orchestration Patterns"
description: "Explore orchestration patterns: workflow engines, Temporal, state machines, and centralized workflow coordination"
date: 2026-05-12
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/orchestration-patterns.html
---

# Orchestration Patterns

Orchestration is an architectural pattern for coordinating distributed workflows using a central controller. Unlike choreography, where services coordinate through events, orchestration uses an explicit workflow engine or orchestrator service that tells each participant what to do and when. This centralized approach provides visibility, control, and error handling that are difficult to achieve with decentralized coordination.   
Centralized Coordination   
In an orchestrated workflow, an orchestrator service manages the entire process. It calls each participant service in sequence, handles responses, manages state, and decides the next step based on results. The orchestrator is the single place where the workflow logic lives.   
For example, an order fulfillment orchestrator would call the payment service, wait for the response, call the inventory service, wait for the response, and finally call the shipping service. Each participant is unaware of the larger workflow—it simply performs its task and returns a result.   
Workflow Engines   
Workflow engines provide a runtime for defining and executing orchestrated workflows. Temporal, AWS Step Functions, Camunda, and Apache Airflow are popular workflow engines. They handle workflow state persistence, automatic retries, timeout management, and error handling.   
Temporal has emerged as a leading workflow engine for microservice orchestration. It supports long-running workflows, automatic retries with configurable policies, and deterministic workflow replay. Workflow code is written in standard programming languages (Java, Go, Python, TypeScript), and Temporal ensures that the workflow logic executes reliably even through failures and restarts.   
State Machines   
State machines are a natural model for orchestration. Each workflow instance starts in an initial state, transitions through states based on completed activities, and ends in a terminal state (success or failure). The state machine approach makes workflow logic explicit, testable, and visualizable.   
AWS Step Functions uses a JSON-based state machine definition. Each state can be a Task (invoke a service), Choice (branch based on input), Wait (delay), Parallel (execute branches in parallel), or Fail/Succeed (terminal states). The state machine definition captures the entire workflow in a single document.   
Compensation Handling   
One of the main advantages of orchestration is straightforward compensation handling. The orchestrator knows exactly which activities have completed and can call compensating actions in reverse order when a failure occurs.   
Temporal provides explicit compensation support through the Saga pattern and its `Workflow` API. When an activity fails, the orchestrator can execute compensating activities for all previously completed steps. The orchestrator also manages the compensation state, ensuring compensations are applied even if the orchestrator itself fails during compensation.   
Visibility and Debugging   
Orchestration provides excellent workflow visibility. The orchestrator or workflow engine exposes the current state of each workflow instance, including which activities have completed, which are in progress, and where failures occurred. This eliminates the need to reconstruct workflow state from distributed event logs.   
Temporal provides a web UI for inspecting workflow instances, viewing execution history, and replaying workflows for debugging. Step Functions offers similar visibility through the AWS Management Console. This centralized visibility dramatically simplifies debugging compared to choreographed workflows.   
When to Use Orchestration   
Orchestration is appropriate for complex workflows with many conditional paths, strict ordering requirements, or where end-to-end visibility is critical. It excels in scenarios where the workflow logic changes frequently—changes are made in one place rather than across multiple services.   
The trade-off is coupling. The orchestrator must know about all participants and their APIs. Changes to participant services may require changes to the orchestrator. This coupling is acceptable when workflow complexity justifies the centralized control.   
In practice, many organizations use a hybrid approach: orchestration for complex business workflows and choreography for simple, stable event flows. Workflow engines like Temporal support both patterns, allowing teams to choose the right level of coordination for each workflow. The key is recognizing that orchestration and choreography are complementary tools, not competing philosophies.
