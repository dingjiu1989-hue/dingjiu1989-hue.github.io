---
title: "Developer Portal"
description: "Explore developer portals: Backstage, documentation hubs, API catalogs, service catalogs, and platform engineering"
date: 2026-01-06
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/developer-portal.html
---

# Developer Portal

A developer portal is a centralized platform that provides developers with the tools, documentation, and services they need to build and operate software. In modern platform engineering, the developer portal is the primary interface between the platform team and application teams. This article covers Backstage, API catalogs, service catalogs, and developer portal best practices.

## The Need for Developer Portals

As organizations grow, the number of services, APIs, tools, and internal resources multiplies. Developers struggle to find what they need. Documentation is scattered across wikis and documents. Service ownership is unclear. Onboarding new team members takes weeks.

A developer portal addresses these challenges by providing a single entry point for all developer needs. It aggregates documentation, catalogs services and APIs, provides self-service actions, and gives visibility into the organization's software ecosystem.

## Backstage

Backstage is an open-source developer portal platform created by Spotify and now under the Cloud Native Computing Foundation. It provides a plugin-based architecture where each capability is a plugin. Core features include a service catalog, software templates, tech docs, and API documentation.

The Backstage service catalog is the central feature. It provides a uniform view of all services, their ownership, metadata, and relationships. Each service has a "catalog entity" defined in YAML, typically stored in the service's repository. The catalog is populated through automated ingestion.

Backstage software templates automate service creation. A template defines the project structure, CI/CD pipeline, monitoring configuration, and documentation scaffolding. Developers select a template, answer a few questions, and Backstage creates a new repository with everything set up.

## API Catalog

An API catalog provides a searchable directory of all APIs in the organization. Each API entry includes the OpenAPI specification, documentation, ownership information, usage guidelines, and service level objectives.

The API catalog helps developers discover existing APIs before building new ones. This reduces duplication and promotes reuse. API consumers can find the right API for their needs, understand how to use it, and see its reliability guarantees.

API catalog management should be automated. When an API changes, the catalog should update automatically. Ownership metadata ensures developers know who to contact with questions. Deprecation status prevents new consumers from adopting APIs that will be retired.

## Service Catalog

A service catalog extends beyond APIs to cover all services in the organization. Each service entry includes ownership, dependencies, documentation, runbooks, monitoring dashboards, deployment history, and health status.

The service catalog answers questions like: Who owns this service? What does it depend on? What depends on it? Where is its source code? How do I deploy it? How do I debug it? Having these answers in a central location dramatically reduces onboarding time and incident response time.

Service dependency visualization shows relationships between services. This helps teams understand the impact of changes, identify potential failure cascades, and plan migrations. The dependency graph is a powerful tool for system understanding.

## Developer Self-Service

Developer portals enable self-service actions. Developers can create new services, provision infrastructure, request access, and deploy changes—all without opening a ticket or asking another team. Self-service is a key enabler of developer productivity.

Backstage software templates implement self-service. Each template automates the creation of a new service with standardized tooling, security policies, and observability. The developer provides a few inputs (service name, team, database type) and the template creates everything.

Self-service reduces the platform team's support burden. Developers get what they need faster. Platform teams spend less time on repetitive requests and more time on platform improvements. The key is well-designed templates that produce production-ready results.

## Documentation Hub

A developer portal centralizes all developer documentation. Tech docs (API references, architecture guides, runbooks), process docs (onboarding, deployment, incident response), and reference docs (tool guides, configuration references) are all in one searchable location.

Backstage's TechDocs plugin renders Markdown documentation within the portal. Documentation is stored alongside source code in each service's repository. This keeps docs close to the code and supports documentation-as-code workflows.

The documentation hub should support robust search across all documentation sources. Developers should find the right documentation through a single search, not through Google-like searches across multiple wikis.

## Best Practices

Start with the service catalog as the core feature. Add capabilities incrementally based on developer feedback. Measure adoption and satisfaction. Automate as much as possible—manual metadata updates quickly become stale.

Ensure ownership metadata is accurate and current. Every service should have an identified owner and team. Stale ownership information undermines trust in the portal. Automated ownership verification prevents staleness.

Keep the portal fast and responsive. Developers will not use a slow portal. Search results should return in milliseconds. Page loads should be under a second. A poor user experience defeats the portal's purpose.

A well-designed developer portal transforms the developer experience. It reduces onboarding time, enables self-service, centralizes knowledge, and provides visibility into the software ecosystem. The developer portal is the cornerstone of a successful platform engineering initiative.

**See also:** [API Documentation](</en/tech/api-documentation.html>), [Platform Engineering](</en/tech/platform-engineering.html>), [Node.js Streams](</en/tech/nodejs-streams.html>).

**See also:** [API Documentation](</en/tech/api-documentation.html>), [Platform Engineering](</en/tech/platform-engineering.html>), [SLI/SLO/Error Budgets: Defining SLIs, Setting SLOs, and Burn Rate Alerts](</en/tech/sli-slo-error-budget.html>)

**See also:** [API Documentation](</en/tech/api-documentation.html>), [Platform Engineering](</en/tech/platform-engineering.html>), [SLI/SLO/Error Budgets: Defining SLIs, Setting SLOs, and Burn Rate Alerts](</en/tech/sli-slo-error-budget.html>)

**See also:** [API Documentation](</en/tech/api-documentation.html>), [Platform Engineering](</en/tech/platform-engineering.html>), [SLI/SLO/Error Budgets: Defining SLIs, Setting SLOs, and Burn Rate Alerts](</en/tech/sli-slo-error-budget.html>)

**See also:** [API Documentation](</en/tech/api-documentation.html>), [Platform Engineering](</en/tech/platform-engineering.html>), [SLI/SLO/Error Budgets: Defining SLIs, Setting SLOs, and Burn Rate Alerts](</en/tech/sli-slo-error-budget.html>)

**See also:** [API Documentation](</en/tech/api-documentation.html>), [Platform Engineering](</en/tech/platform-engineering.html>), [SLI/SLO/Error Budgets: Defining SLIs, Setting SLOs, and Burn Rate Alerts](</en/tech/sli-slo-error-budget.html>)

**See also:** [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Load Testing Strategies](</en/tech/load-testing-strategies.html>), [Log Management](</en/tech/log-management.html>)

**See also:** [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Load Testing Strategies](</en/tech/load-testing-strategies.html>), [Log Management](</en/tech/log-management.html>)

**See also:** [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Load Testing Strategies](</en/tech/load-testing-strategies.html>), [Log Management](</en/tech/log-management.html>)

**See also:** [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Load Testing Strategies](</en/tech/load-testing-strategies.html>), [Log Management](</en/tech/log-management.html>)

**See also:** [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Load Testing Strategies](</en/tech/load-testing-strategies.html>), [Log Management](</en/tech/log-management.html>)

**See also:** [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Load Testing Strategies](</en/tech/load-testing-strategies.html>), [Log Management](</en/tech/log-management.html>)

**See also:** [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Load Testing Strategies](</en/tech/load-testing-strategies.html>), [Log Management](</en/tech/log-management.html>)

**See also:** [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Load Testing Strategies](</en/tech/load-testing-strategies.html>), [Log Management](</en/tech/log-management.html>)

**See also:** [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Load Testing Strategies](</en/tech/load-testing-strategies.html>), [Log Management](</en/tech/log-management.html>)

**See also:** [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Load Testing Strategies](</en/tech/load-testing-strategies.html>), [Log Management](</en/tech/log-management.html>)

**See also:** [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Load Testing Strategies](</en/tech/load-testing-strategies.html>), [Log Management](</en/tech/log-management.html>)
