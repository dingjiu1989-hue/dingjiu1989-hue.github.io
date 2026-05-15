---
title: "Scatter-Gather Pattern for Parallel Processing"
description: "The scatter-gather pattern: broadcast requests to multiple recipients and aggregate responses for comprehensive results."
date: 2026-05-12
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/scatter-gather.html
---

# Scatter-Gather Pattern for Parallel Processing

# Scatter-Gather Pattern for Parallel Processing

# Scatter-Gather Pattern for Parallel Processing

# Scatter-Gather Pattern for Parallel Processing

# Scatter-Gather Pattern for Parallel Processing

# Scatter-Gather Pattern for Parallel Processing

# Scatter-Gather Pattern for Parallel Processing

# Scatter-Gather Pattern for Parallel Processing

# Scatter-Gather Pattern for Parallel Processing

# Scatter-Gather Pattern for Parallel Processing

# Scatter-Gather Pattern for Parallel Processing

# Scatter-Gather Pattern for Parallel Processing

The scatter-gather pattern sends a request to multiple recipients simultaneously, then aggregates their responses into a single result. This is useful when you need information from multiple sources or want to run parallel operations for fault tolerance.

## Architecture

A scatter-gather implementation has three phases. First, the scatter phase broadcasts the request to all recipients. Second, the recipients process the request in parallel. Third, the gather phase collects responses and combines them according to aggregation rules.

## Scatter Mechanisms

Topic-based scatter publishes a request to a pub-sub topic. All subscribers receive the request simultaneously. This is the most common approach and works well when the recipients are known to the broker.

Recipient list scatter maintains a list of recipient addresses and sends the request to each. This is more explicit but requires the scatter component to know all recipients. Dynamic recipient lists can be maintained in a service registry.

## Aggregation Strategies

Wait-for-all aggregation collects responses from all recipients before returning the combined result. This ensures completeness but is limited by the slowest recipient. Timeout-based aggregation waits for responses within a time window, returning partial results. This provides predictable latency but may miss some responses.

Quorum-based aggregation returns results after receiving a configurable number of responses (typically a majority). This is useful for fault tolerance—if some recipients fail, the result is still valid.

## When to Use Scatter-Gather

Use scatter-gather when you need to query multiple data sources for a comprehensive view, when you want fault tolerance through redundant processing, or when you can parallelize independent operations to reduce total response time.

Common applications include search engines querying multiple indexes, credit check systems querying multiple bureaus, and monitoring systems collecting health status from multiple services.

## Performance Considerations

The total latency is determined by the slowest recipient. Set timeouts to bound worst-case latency. Consider caching responses from slower recipients. Use asynchronous processing where possible to avoid blocking on aggregation.

Identify and isolate slow recipients. Implement circuit breakers for recipients that consistently exceed timeouts. Consider removing persistently slow recipients from the recipient list.

**See also:** [Fanout Pattern for Event Distribution](</en/architecture/fanout-pattern.html>), [Graceful Shutdown Patterns](</en/architecture/graceful-shutdown.html>), [Claim Check Pattern](</en/architecture/claim-check.html>).

**See also:** [Fanout Pattern for Event Distribution](</en/architecture/fanout-pattern.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>), [Graceful Shutdown Patterns](</en/architecture/graceful-shutdown.html>)
