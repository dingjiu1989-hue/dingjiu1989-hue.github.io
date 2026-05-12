---
title: "Saga vs Process Manager: Orchestration Patterns Compared"
description: "Compare saga orchestration with process manager patterns for distributed transaction management."
date: 2026-05-12
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/saga-process-manager.html
---

# Saga vs Process Manager: Orchestration Patterns Compared
Both sagas and process managers coordinate multi-step workflows in distributed systems. The key difference: sagas handle failure through compensating actions, while process managers maintain explicit workflow state.

## Saga Pattern

Sagas break long-running transactions into a sequence of local transactions with compensating actions. If a step fails, the saga executes compensating transactions for previous steps. Each service participating in the saga provides both a forward action and a compensating action.

Saga choreography uses events for coordination. Services listen for events and respond with their actions. Compensations are triggered by failure events. Choreography works well for simple workflows with few participants.

Saga orchestration uses a central coordinator. The orchestrator tells each service what to do and handles compensation logic. Orchestration provides better visibility and error handling for complex workflows.

## Process Manager

A process manager maintains explicit workflow state, including what has happened and what should happen next. It sends commands to services and waits for responses. The process manager persists state and survives failures.

Process managers are state machines. Each event transitions the workflow to a new state. Timeout handling triggers retries and escalations. Process managers handle both happy path and error states explicitly.

## Choosing

Use sagas for compensating transactions where eventual consistency is acceptable. Use process managers for workflows requiring explicit state tracking, human-in-the-loop approvals, or complex timeout handling.
