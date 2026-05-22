---
title: "Error Handling Patterns"
description: "Master error handling patterns: Result types, exceptions, error boundaries, resilience strategies, and recovery approaches"
date: 2026-01-07
board: tech
url: https://aidev.fit/en/tech/error-handling-patterns.html
---

# Error Handling Patterns

Error handling is a cross-cutting concern that affects system reliability, debuggability, and user experience. Different languages and paradigms offer different error handling approaches: exceptions in Java and Python, Result types in Rust and Swift, and error boundaries in UI frameworks. This article examines these patterns and provides guidance for building resilient error handling.

## Exceptions

Exception-based error handling uses try/catch blocks to handle errors that occur in a different part of the call stack. When an error occurs, the code throws an exception that propagates up the call stack until a matching catch block handles it. Unhandled exceptions typically crash the program.

Exceptions are appropriate for errors that cannot be handled at the point of occurrence and need to propagate to a higher level. A database connection failure, for example, may need to propagate to the request handler rather than being handled in the data access layer.

Exception handling best practices include catching specific exception types rather than generic ones, using finally blocks for cleanup, not using exceptions for control flow, and logging exceptions with full stack traces at the appropriate level. Overly broad catch blocks that swallow exceptions are a common source of hard-to-debug issues.

## Result Types

Result types (also called Either types) represent the possibility of success or failure as a return value. A function returns a Result that is either an Ok value or an Err value. The caller must handle both cases—there is no way to ignore the error.

Rust's `Result` type is the most prominent example. The `?` operator propagates errors to the caller. Pattern matching on Result values ensures all cases are handled at compile time. This explicit error handling makes error paths visible and forces the programmer to consider them.

Result types provide type safety for error handling. The compiler ensures that errors are handled at some level—they cannot be silently ignored. This is a significant advantage over exceptions, where unhandled exceptions crash at runtime.

## Error Boundaries

Error boundaries are a UI pattern, popularized by React, that catch errors in component subtrees and display fallback UI instead of crashing the entire page. An error boundary wraps a section of the UI and catches errors thrown by its children.

In React, class components implement `componentDidCatch` to become error boundaries. React 16 introduced this pattern for recovering from rendering errors. The App Router in Next.js uses `error.tsx` files to define segment-level error boundaries automatically.

Error boundaries allow partial page crashes rather than full page crashes. A broken sidebar does not take down the main content area. This significantly improves user experience in complex applications where some components may fail independently.

## Resilience Patterns

Beyond basic error handling, resilience patterns prevent errors from causing system-wide failures. Circuit breakers stop calling a failing service to give it time to recover. Bulkheads isolate resources so a failure in one component does not exhaust shared resources.

Retry with backoff handles transient failures. Timeouts prevent waiting indefinitely for a response. Fallbacks provide degraded functionality when a dependency fails. Rate limiting prevents a single client from overwhelming the system.

These patterns are composable. A typical resilience pipeline wraps a service call with a timeout, retries with exponential backoff, a circuit breaker, and finally a fallback. Libraries like Resilience4j (Java), Polly (.NET), and resilience4s (Scala) provide these patterns as reusable components.

## Error Propagation

How errors propagate through a system affects debuggability. Errors should include context about what went wrong, where it happened, and what the system was doing at the time. In distributed systems, errors should include correlation IDs that tie them to the originating request.

Errors that cross service boundaries should be translated to appropriate HTTP status codes and structured error responses. Internal error details should not leak to external clients. Consistent error response formats make client-side error handling predictable.

## Error Recovery

Not all errors need to crash the program. Graceful degradation handles errors by providing reduced functionality rather than failing completely. A recommendation service that fails can be degraded to showing popular items. An image loading failure can show a placeholder.

Error recovery follows the principle of graceful degradation: degrade functionality rather than denying service. The key is knowing which errors are recoverable (a failed recommendation call) and which are not (a failed authentication check).

The most robust error handling strategies combine multiple patterns. Use Result types or exceptions for local error handling. Use error boundaries for UI resilience. Use circuit breakers for service resilience. Use structured logging and tracing for diagnosis. The combination of these patterns creates systems that fail gracefully and are debuggable when they do.

**See also:** [CI/CD Best Practices](</en/tech/ci-cd-best-practices.html>), [Node.js Streams](</en/tech/nodejs-streams.html>), [Metric Collection](</en/tech/metric-collection.html>).

**See also:** [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>), [CI/CD Best Practices](</en/tech/ci-cd-best-practices.html>), [Load Testing Strategies](</en/tech/load-testing-strategies.html>)

**See also:** [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>), [CI/CD Best Practices](</en/tech/ci-cd-best-practices.html>), [Load Testing Strategies](</en/tech/load-testing-strategies.html>)

**See also:** [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>), [CI/CD Best Practices](</en/tech/ci-cd-best-practices.html>), [Load Testing Strategies](</en/tech/load-testing-strategies.html>)

**See also:** [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>), [CI/CD Best Practices](</en/tech/ci-cd-best-practices.html>), [Load Testing Strategies](</en/tech/load-testing-strategies.html>)

**See also:** [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>), [CI/CD Best Practices](</en/tech/ci-cd-best-practices.html>), [Load Testing Strategies](</en/tech/load-testing-strategies.html>)

**See also:** [React Server Components](</en/tech/react-server-components.html>), [Testing Strategies](</en/tech/testing-strategies.html>), [API Versioning Strategies: REST vs GraphQL Approaches](</en/tech/api-versioning-rest-graphql.html>)

**See also:** [React Server Components](</en/tech/react-server-components.html>), [Testing Strategies](</en/tech/testing-strategies.html>), [API Versioning Strategies: REST vs GraphQL Approaches](</en/tech/api-versioning-rest-graphql.html>)

**See also:** [React Server Components](</en/tech/react-server-components.html>), [Testing Strategies](</en/tech/testing-strategies.html>), [API Versioning Strategies: REST vs GraphQL Approaches](</en/tech/api-versioning-rest-graphql.html>)

**See also:** [React Server Components](</en/tech/react-server-components.html>), [Testing Strategies](</en/tech/testing-strategies.html>), [API Versioning Strategies: REST vs GraphQL Approaches](</en/tech/api-versioning-rest-graphql.html>)

**See also:** [React Server Components](</en/tech/react-server-components.html>), [Testing Strategies](</en/tech/testing-strategies.html>), [API Versioning Strategies: REST vs GraphQL Approaches](</en/tech/api-versioning-rest-graphql.html>)

**See also:** [React Server Components](</en/tech/react-server-components.html>), [Testing Strategies](</en/tech/testing-strategies.html>), [API Versioning Strategies: REST vs GraphQL Approaches](</en/tech/api-versioning-rest-graphql.html>)

**See also:** [React Server Components](</en/tech/react-server-components.html>), [Testing Strategies](</en/tech/testing-strategies.html>), [API Versioning Strategies: REST vs GraphQL Approaches](</en/tech/api-versioning-rest-graphql.html>)

**See also:** [React Server Components](</en/tech/react-server-components.html>), [Testing Strategies](</en/tech/testing-strategies.html>), [API Versioning Strategies: REST vs GraphQL Approaches](</en/tech/api-versioning-rest-graphql.html>)

**See also:** [React Server Components](</en/tech/react-server-components.html>), [Testing Strategies](</en/tech/testing-strategies.html>), [API Versioning Strategies: REST vs GraphQL Approaches](</en/tech/api-versioning-rest-graphql.html>)

**See also:** [React Server Components](</en/tech/react-server-components.html>), [Testing Strategies](</en/tech/testing-strategies.html>), [API Versioning Strategies: REST vs GraphQL Approaches](</en/tech/api-versioning-rest-graphql.html>)

**See also:** [React Server Components](</en/tech/react-server-components.html>), [Testing Strategies](</en/tech/testing-strategies.html>), [API Versioning Strategies: REST vs GraphQL Approaches](</en/tech/api-versioning-rest-graphql.html>)

**See also:** [React Server Components](</en/tech/react-server-components.html>), [Testing Strategies](</en/tech/testing-strategies.html>), [API Versioning Strategies: REST vs GraphQL Approaches](</en/tech/api-versioning-rest-graphql.html>)

**See also:** [React Server Components](</en/tech/react-server-components.html>), [Testing Strategies](</en/tech/testing-strategies.html>), [API Versioning Strategies: REST vs GraphQL Approaches](</en/tech/api-versioning-rest-graphql.html>)

**See also:** [React Server Components](</en/tech/react-server-components.html>), [Testing Strategies](</en/tech/testing-strategies.html>), [API Versioning Strategies: REST vs GraphQL Approaches](</en/tech/api-versioning-rest-graphql.html>)

**See also:** [React Server Components](</en/tech/react-server-components.html>), [Testing Strategies](</en/tech/testing-strategies.html>), [API Versioning Strategies: REST vs GraphQL Approaches](</en/tech/api-versioning-rest-graphql.html>)

**See also:** [React Server Components](</en/tech/react-server-components.html>), [Testing Strategies](</en/tech/testing-strategies.html>), [API Versioning Strategies: REST vs GraphQL Approaches](</en/tech/api-versioning-rest-graphql.html>)
