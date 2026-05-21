---
title: "Consumer-Driven Contracts in Microservices"
description: "Learn consumer-driven contract testing to ensure microservice compatibility without brittle integration tests."
date: 2026-05-06
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/consumer-driven-contracts.html
---

# Consumer-Driven Contracts in Microservices

Consumer-driven contracts (CDC) is a pattern where service consumers define the expectations for the API they consume. The provider tests against these contracts to ensure changes do not break consumers. This approach enables independent service evolution while maintaining compatibility.

## How CDC Works

Each consumer creates a contract file specifying exactly how it uses the provider's API—which endpoints, request parameters, and response fields. These contracts are shared with the provider. The provider runs a contract verification suite that tests its API against all consumer contracts before deployment.

If a provider change would break any consumer, the contract test fails. The provider must either revert the change or coordinate with the consumer to update the contract. This feedback loop catches breaking changes before they reach production.

## Pact Framework

Pact is the most widely used CDC framework. It supports multiple languages including Java, Python, JavaScript, and Go. Consumers use Pact to write tests that generate contract files. Providers use Pact to verify these contracts.

Pact supports message-based interactions for asynchronous communication. Consumer tests specify expected messages; provider tests verify actual message format and content.

## Benefits Over Integration Tests

Integration tests require both provider and consumer to be running simultaneously. They are slow, brittle, and require complex test infrastructure. CDC tests run independently on each side. Consumer tests mock the provider; provider tests run against the real API. This separation enables faster feedback and simpler test setup.

## Adoption Strategy

Start with one provider-consumer pair. Choose a critical service with multiple consumers. Write consumer contracts for the most-used endpoints. Add provider verification to the CI pipeline. Expand to additional services as the team gains experience. Maintain a contract repository that all teams can access.

## Common Pitfalls

Contracts can become large and brittle if consumers test too many scenarios. Focus on testing realistic consumer usage, not exhaustive provider behavior. Version contracts and coordinate changes. Treat contract changes as API changes—they require communication and agreement between teams.

**See also:** [Contract Testing for Microservices](</en/architecture/contract-testing.html>), [Sidecar Pattern in Microservices Architecture](</en/architecture/sidecar-pattern.html>), [Choreography Patterns](</en/architecture/choreography-patterns.html>).

**See also:** [Contract Testing for Microservices](</en/architecture/contract-testing.html>), [Sidecar Pattern in Microservices Architecture](</en/architecture/sidecar-pattern.html>), [Microservices vs Monolith: Decision Guide](</en/architecture/microservices-vs-monolith.html>)

**See also:** [Contract Testing for Microservices](</en/architecture/contract-testing.html>), [Sidecar Pattern in Microservices Architecture](</en/architecture/sidecar-pattern.html>), [Microservices vs Monolith: Decision Guide](</en/architecture/microservices-vs-monolith.html>)

**See also:** [Contract Testing for Microservices](</en/architecture/contract-testing.html>), [Sidecar Pattern in Microservices Architecture](</en/architecture/sidecar-pattern.html>), [Microservices vs Monolith: Decision Guide](</en/architecture/microservices-vs-monolith.html>)

**See also:** [Contract Testing for Microservices](</en/architecture/contract-testing.html>), [Sidecar Pattern in Microservices Architecture](</en/architecture/sidecar-pattern.html>), [Microservices vs Monolith: Decision Guide](</en/architecture/microservices-vs-monolith.html>)

**See also:** [Contract Testing for Microservices](</en/architecture/contract-testing.html>), [Sidecar Pattern in Microservices Architecture](</en/architecture/sidecar-pattern.html>), [Microservices vs Monolith: Decision Guide](</en/architecture/microservices-vs-monolith.html>)

**See also:** [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>), [Polling Consumer vs Event-Driven Consumer](</en/architecture/polling-consumer.html>), [A/B Testing Infrastructure](</en/architecture/a-b-testing-infrastructure.html>)

**See also:** [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>), [Polling Consumer vs Event-Driven Consumer](</en/architecture/polling-consumer.html>), [A/B Testing Infrastructure](</en/architecture/a-b-testing-infrastructure.html>)

**See also:** [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>), [Polling Consumer vs Event-Driven Consumer](</en/architecture/polling-consumer.html>), [A/B Testing Infrastructure](</en/architecture/a-b-testing-infrastructure.html>)

**See also:** [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>), [Polling Consumer vs Event-Driven Consumer](</en/architecture/polling-consumer.html>), [A/B Testing Infrastructure](</en/architecture/a-b-testing-infrastructure.html>)

**See also:** [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>), [Polling Consumer vs Event-Driven Consumer](</en/architecture/polling-consumer.html>), [A/B Testing Infrastructure](</en/architecture/a-b-testing-infrastructure.html>)

**See also:** [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>), [Polling Consumer vs Event-Driven Consumer](</en/architecture/polling-consumer.html>), [A/B Testing Infrastructure](</en/architecture/a-b-testing-infrastructure.html>)

**See also:** [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>), [Polling Consumer vs Event-Driven Consumer](</en/architecture/polling-consumer.html>), [A/B Testing Infrastructure](</en/architecture/a-b-testing-infrastructure.html>)

**See also:** [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>), [Polling Consumer vs Event-Driven Consumer](</en/architecture/polling-consumer.html>), [A/B Testing Infrastructure](</en/architecture/a-b-testing-infrastructure.html>)

**See also:** [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>), [Polling Consumer vs Event-Driven Consumer](</en/architecture/polling-consumer.html>), [A/B Testing Infrastructure](</en/architecture/a-b-testing-infrastructure.html>)

**See also:** [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>), [Polling Consumer vs Event-Driven Consumer](</en/architecture/polling-consumer.html>), [A/B Testing Infrastructure](</en/architecture/a-b-testing-infrastructure.html>)

**See also:** [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>), [Polling Consumer vs Event-Driven Consumer](</en/architecture/polling-consumer.html>), [A/B Testing Infrastructure](</en/architecture/a-b-testing-infrastructure.html>)

**See also:** [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>), [Polling Consumer vs Event-Driven Consumer](</en/architecture/polling-consumer.html>), [A/B Testing Infrastructure](</en/architecture/a-b-testing-infrastructure.html>)

**See also:** [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>), [Polling Consumer vs Event-Driven Consumer](</en/architecture/polling-consumer.html>), [A/B Testing Infrastructure](</en/architecture/a-b-testing-infrastructure.html>)
