---
title: "Routing Slip Pattern for Dynamic Message Processing"
description: "Implement the routing slip pattern to process messages through a dynamic sequence of processing steps."
date: 2026-05-09
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/routing-slip.html
---

# Routing Slip Pattern for Dynamic Message Processing

The routing slip pattern processes a message through a predefined sequence of processing steps, where the path is determined at runtime. Think of it as a delivery route for messages—each stop adds value or transformation before sending the message to the next destination.

## How Routing Slips Work

The routing slip is attached to the message as metadata. It contains an ordered list of processing steps. After each step completes, the processing component reads the next destination from the routing slip and forwards the message. When all steps are complete, the message reaches its final destination.

## Implementation

The routing slip is typically implemented as a JSON array or a comma-separated list of endpoint addresses. Each processing step inspects the slip, performs its operation, removes the current step from the list, and forwards the message to the next address.

In Apache Camel, routing slips are a built-in Enterprise Integration Pattern (EIP). Camel reads the slip from a message header and routes dynamically. Spring Integration and Mule also support routing slips natively.

## Dynamic Routing vs Static Pipelines

Static processing pipelines hardcode the sequence of steps. Every message follows the same path. Routing slips allow each message to have a unique path based on its content or type. This flexibility is valuable when different message types require different processing.

For example, a payment message might follow the path: validate → enrich → fraud check → process. A simple status check message might skip enrichment and fraud check entirely.

## Use Cases

Data transformation pipelines where different data sources need different enrichment steps. Document approval workflows where the approval chain depends on document type and value. Multi-step provisioning processes where the required steps depend on the requested resources.

## Error Handling

If a step fails, the message should go to a dead letter queue with its routing slip intact. The failure context includes which step failed and what steps remain. After fixing the issue, operators can resume processing from the failed step by modifying the routing slip.

## Monitoring

Track metrics per step: processing time, success rate, and queue depth. A routing slip dashboard should show the distribution of message paths—which combinations of steps are most common and where bottlenecks occur.

**See also:** [Priority Queue Pattern for Message Processing](</en/architecture/priority-queue.html>), [Transactional Inbox Pattern for Reliable Messaging](</en/architecture/transactional-inbox.html>), [Request-Reply Pattern for Asynchronous Communication](</en/architecture/request-reply-pattern.html>).

**See also:** [Priority Queue Pattern for Message Processing](</en/architecture/priority-queue.html>), [Transactional Inbox Pattern for Reliable Messaging](</en/architecture/transactional-inbox.html>), [Request-Reply Pattern for Asynchronous Communication](</en/architecture/request-reply-pattern.html>)

**See also:** [Priority Queue Pattern for Message Processing](</en/architecture/priority-queue.html>), [Transactional Inbox Pattern for Reliable Messaging](</en/architecture/transactional-inbox.html>), [Request-Reply Pattern for Asynchronous Communication](</en/architecture/request-reply-pattern.html>)

**See also:** [Priority Queue Pattern for Message Processing](</en/architecture/priority-queue.html>), [Transactional Inbox Pattern for Reliable Messaging](</en/architecture/transactional-inbox.html>), [Request-Reply Pattern for Asynchronous Communication](</en/architecture/request-reply-pattern.html>)

**See also:** [Priority Queue Pattern for Message Processing](</en/architecture/priority-queue.html>), [Transactional Inbox Pattern for Reliable Messaging](</en/architecture/transactional-inbox.html>), [Request-Reply Pattern for Asynchronous Communication](</en/architecture/request-reply-pattern.html>)

**See also:** [Priority Queue Pattern for Message Processing](</en/architecture/priority-queue.html>), [Transactional Inbox Pattern for Reliable Messaging](</en/architecture/transactional-inbox.html>), [Request-Reply Pattern for Asynchronous Communication](</en/architecture/request-reply-pattern.html>)

**See also:** [Claim Check Pattern](</en/architecture/claim-check.html>), [Transactional Outbox Pattern](</en/architecture/transaction-outbox-reliable.html>), [Ambassador Pattern for Service Communication](</en/architecture/ambassador-pattern.html>)

**See also:** [Claim Check Pattern](</en/architecture/claim-check.html>), [Transactional Outbox Pattern](</en/architecture/transaction-outbox-reliable.html>), [Ambassador Pattern for Service Communication](</en/architecture/ambassador-pattern.html>)

**See also:** [Claim Check Pattern](</en/architecture/claim-check.html>), [Transactional Outbox Pattern](</en/architecture/transaction-outbox-reliable.html>), [Ambassador Pattern for Service Communication](</en/architecture/ambassador-pattern.html>)

**See also:** [Claim Check Pattern](</en/architecture/claim-check.html>), [Transactional Outbox Pattern](</en/architecture/transaction-outbox-reliable.html>), [Ambassador Pattern for Service Communication](</en/architecture/ambassador-pattern.html>)

**See also:** [Claim Check Pattern](</en/architecture/claim-check.html>), [Transactional Outbox Pattern](</en/architecture/transaction-outbox-reliable.html>), [Ambassador Pattern for Service Communication](</en/architecture/ambassador-pattern.html>)
