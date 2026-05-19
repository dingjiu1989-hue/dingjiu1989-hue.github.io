---
title: "Contract Testing"
description: "Master contract testing: Pact, consumer-driven contracts, provider verification, and CI/CD integration"
date: 2026-01-06
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/contract-testing.html
---

# Contract Testing

Contract testing is a testing methodology that validates the interactions between services against a shared agreement. Unlike integration tests that run both services together, contract tests verify each service independently against a contract that defines their interaction. This approach catches integration issues early and enables independent deployment of services.

## Consumer-Driven Contracts

Consumer-driven contracts (CDC) follow the principle that consumers define their expectations from a provider. The consumer writes a contract specifying how it intends to use the provider's API—which endpoints it calls, what data it sends, and what responses it expects. The provider verifies that it meets all consumer contracts.

This approach ensures that providers do not break existing consumers when they change their API. Before deploying a change, the provider runs all consumer contracts and confirms compatibility. If a change would break a consumer, the provider knows before deployment.

## How Pact Works

Pact is the leading contract testing framework. The consumer writes a Pact test that describes its expectations. The test defines the request it will make and the response it expects. Pact records these interactions in a contract file (a pact file).

The consumer runs its Pact test against a mock provider. This verifies that the consumer code correctly handles the expected responses. The pact file is then shared with the provider team, typically as an artifact in a CI/CD pipeline.

The provider runs the pact file against its actual implementation. Pact replays each consumer request, verifies that the provider returns the expected response, and reports any mismatches. This "provider verification" step catches breaking changes before they reach production.

## Pact Flow

The typical Pact workflow follows these steps. The consumer writes a Pact test defining its expectations. The consumer test runs against a mock provider and generates a pact file. The pact file is published to a Pact Broker (a shared repository for contracts).

The provider retrieves consumer contracts from the Pact Broker. The provider verification tests run each consumer interaction against the actual provider. Results are published back to the Pact Broker. The broker shows which provider versions are compatible with which consumer versions, enabling safe deployment decisions.

## Provider Verification

Provider verification is the core of Pact's value. The provider test suite loads each pact file and replays each consumer request against the running provider. If the response matches, the contract is verified. If not, the test reports which consumer would be broken.

Provider verification can be integrated into CI/CD pipelines. Before deploying a provider change, the CI pipeline runs verification against all consumer pacts. If any verification fails, deployment is blocked. This prevents breaking changes from reaching production.

## Contract Testing vs Integration Testing

Contract testing differs from integration testing in important ways. Integration tests run both services together, which requires both to be available and configured correctly. This makes integration tests slow, fragile, and expensive to maintain.

Contract tests run each service independently. The consumer test uses a mock provider. The provider test uses the real provider but the consumer's requests are replayed from the pact file. Neither test requires both services to be running. Contract tests are faster, more reliable, and more focused than integration tests.

Contract testing is not a replacement for all integration testing. It validates API contracts but does not verify end-to-end behavior. A complete testing strategy uses both: contract tests for service interactions and a smaller number of end-to-end tests for critical workflows.

## When to Use Contract Testing

Contract testing is most valuable in microservice architectures where services are owned by different teams. It provides a formal mechanism for managing API dependencies without requiring constant coordination. Each team can evolve their service independently as long as contracts remain compatible.

For monoliths or services owned by the same team, contract testing may add unnecessary overhead. The same team can manage API changes through refactoring and shared test suites. However, even within a team, contract testing can provide clear API documentation and prevent accidental breakage.

## Best Practices

Contracts should focus on the interactions that consumers actually use, not all possible interactions of the provider API. This keeps contracts small and relevant. Contracts should use realistic data that reflects production usage patterns. Matchers (like Pact's `like()`) make contracts flexible enough to handle variations in non-essential fields.

Publish contract verification results to a Pact Broker to enable safe deployment decisions. The broker's "can-i-deploy" tool checks whether a given service version is compatible with its consumers before allowing deployment. This automated safety check is central to the Pact workflow.

Contract testing provides a practical mechanism for managing service dependencies in distributed systems. By validating API interactions independently, it enables faster, safer deployments in microservice architectures with multiple teams.

**See also:** [Testing Strategies](</en/tech/testing-strategies.html>), [API Documentation](</en/tech/api-documentation.html>), [CI/CD Best Practices](</en/tech/ci-cd-best-practices.html>).

**See also:** [Testing Strategies](</en/tech/testing-strategies.html>), [API Documentation](</en/tech/api-documentation.html>), [CI/CD Best Practices](</en/tech/ci-cd-best-practices.html>)

**See also:** [Testing Strategies](</en/tech/testing-strategies.html>), [API Documentation](</en/tech/api-documentation.html>), [CI/CD Best Practices](</en/tech/ci-cd-best-practices.html>)

**See also:** [Testing Strategies](</en/tech/testing-strategies.html>), [API Documentation](</en/tech/api-documentation.html>), [CI/CD Best Practices](</en/tech/ci-cd-best-practices.html>)

**See also:** [Testing Strategies](</en/tech/testing-strategies.html>), [API Documentation](</en/tech/api-documentation.html>), [CI/CD Best Practices](</en/tech/ci-cd-best-practices.html>)

**See also:** [Testing Strategies](</en/tech/testing-strategies.html>), [API Documentation](</en/tech/api-documentation.html>), [CI/CD Best Practices](</en/tech/ci-cd-best-practices.html>)

**See also:** [Load Testing Strategies](</en/tech/load-testing-strategies.html>), [Metric Collection](</en/tech/metric-collection.html>), [Node.js Streams](</en/tech/nodejs-streams.html>)

**See also:** [Load Testing Strategies](</en/tech/load-testing-strategies.html>), [Metric Collection](</en/tech/metric-collection.html>), [Node.js Streams](</en/tech/nodejs-streams.html>)

**See also:** [Load Testing Strategies](</en/tech/load-testing-strategies.html>), [Metric Collection](</en/tech/metric-collection.html>), [Node.js Streams](</en/tech/nodejs-streams.html>)

**See also:** [Load Testing Strategies](</en/tech/load-testing-strategies.html>), [Metric Collection](</en/tech/metric-collection.html>), [Node.js Streams](</en/tech/nodejs-streams.html>)

**See also:** [Load Testing Strategies](</en/tech/load-testing-strategies.html>), [Metric Collection](</en/tech/metric-collection.html>), [Node.js Streams](</en/tech/nodejs-streams.html>)

**See also:** [Load Testing Strategies](</en/tech/load-testing-strategies.html>), [Metric Collection](</en/tech/metric-collection.html>), [Node.js Streams](</en/tech/nodejs-streams.html>)
