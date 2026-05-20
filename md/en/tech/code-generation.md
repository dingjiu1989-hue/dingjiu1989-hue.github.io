---
title: "Code Generation"
description: "Learn code generation: scaffolding tools, OpenAPI codegen, GraphQL codegen, template engines, and productivity patterns"
date: 2026-01-06
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/code-generation.html
---

# Code Generation

Code generation automates the creation of repetitive, boilerplate code. It enforces consistency, reduces human error, and accelerates development. This article explores the major code generation approaches: scaffolding tools, API client generation, GraphQL code generation, and custom template engines.

## Scaffolding Tools

Scaffolding tools generate initial project structures with pre-configured build systems, directory layouts, and common dependencies. They eliminate the repetitive setup that every project requires and ensure consistent project structures across the organization.

Popular scaffolding tools include Yeoman (JavaScript), Cookiecutter (Python), and `create-react-app`/`create-next-app` (React/Next.js). These tools ask a few questions and generate a complete project foundation. The generated code follows best practices and is production-ready from day one.

Organizations should invest in custom scaffolding templates that encode their specific conventions, preferred libraries, security policies, and CI/CD configurations. A standardized scaffold reduces onboarding time and ensures every project follows the same patterns.

## OpenAPI Code Generation

OpenAPI specifications enable automatic generation of both server and client code. Tools like OpenAPI Generator and Swagger Codegen read an OpenAPI spec and generate type definitions, API client libraries, server stubs, and documentation.

Server-side code generation produces controllers and service interfaces. The developer implements the business logic within the generated structure. This ensures the implementation matches the specification exactly—any deviation is immediately visible.

Client-side code generation produces type-safe API clients. Generated clients include request/response types, endpoint methods, and serialization logic. This eliminates manual HTTP client code that is error-prone and tedious to maintain. When the API changes, regenerating the client highlights all affected code.

## GraphQL Code Generation

GraphQL's typed schema makes it an ideal candidate for code generation. Tools like GraphQL Code Generator read a GraphQL schema and generate TypeScript types, React hooks, and resolver types.

Generated TypeScript types provide compile-time safety for GraphQL operations. When a field is removed from the schema, the generated types update, and the TypeScript compiler reports every usage that needs attention. This catches breaking changes at compile time rather than runtime.

For React applications, GraphQL Code Generator generates typed hooks for each query and mutation. The generated hooks include response types, variable types, and loading state types. This eliminates manual type annotation and ensures the frontend types always match the schema.

## Template Engines

Custom code generation uses template engines to generate files from templates and data. A template is a text file with placeholders that the engine fills with generated content. Mustache, Handlebars, and EJS are popular template engines.

Templates can generate any text-based file: source code, configuration files, documentation, SQL migrations, or test fixtures. The template approach is flexible and can be adapted to any codebase's specific patterns.

Custom templates are most valuable for generating repetitive code within a project. Common examples include creating new components following a consistent pattern, generating CRUD endpoints for each database table, and creating test files that mirror source file structure.

## Best Practices

Generated code should be clearly marked as generated. Include a comment at the top of generated files indicating they are auto-generated and the source command used. This prevents developers from manually editing generated files—changes would be lost on regeneration.

Version control for generated code depends on the context. API client libraries that are consumed across services should be versioned as packages. Scaffolding-generated projects should start with the generated structure and evolve independently. Template-generated code within a project should be regenerated when the source changes.

Regeneration should be automated and part of the build process. When an API specification changes, a CI pipeline regenerates the client code and runs tests. Any compilation errors from the regeneration are caught immediately.

Code generation is a powerful productivity tool, but it should be used thoughtfully. Generate code where it eliminates significant manual work or enforces consistency. Avoid generating code that adds complexity without proportional benefit—simple tasks may not need generation.

**See also:** [API Documentation](</en/tech/api-documentation.html>), [Task Queues](</en/tech/task-queues.html>), [Testing Strategies](</en/tech/testing-strategies.html>).

**See also:** [Grafana Dashboards: Panels, Variables, Annotations, and Alerting](</en/tech/grafana-dashboards.html>), [API Documentation](</en/tech/api-documentation.html>), [Task Queues](</en/tech/task-queues.html>)

**See also:** [Grafana Dashboards: Panels, Variables, Annotations, and Alerting](</en/tech/grafana-dashboards.html>), [API Documentation](</en/tech/api-documentation.html>), [Task Queues](</en/tech/task-queues.html>)

**See also:** [Grafana Dashboards: Panels, Variables, Annotations, and Alerting](</en/tech/grafana-dashboards.html>), [API Documentation](</en/tech/api-documentation.html>), [Task Queues](</en/tech/task-queues.html>)

**See also:** [Grafana Dashboards: Panels, Variables, Annotations, and Alerting](</en/tech/grafana-dashboards.html>), [API Documentation](</en/tech/api-documentation.html>), [Task Queues](</en/tech/task-queues.html>)

**See also:** [Grafana Dashboards: Panels, Variables, Annotations, and Alerting](</en/tech/grafana-dashboards.html>), [API Documentation](</en/tech/api-documentation.html>), [Task Queues](</en/tech/task-queues.html>)

**See also:** [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>), [Artifact Management](</en/tech/artifact-management.html>)

**See also:** [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>), [Artifact Management](</en/tech/artifact-management.html>)

**See also:** [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>), [Artifact Management](</en/tech/artifact-management.html>)

**See also:** [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>), [Artifact Management](</en/tech/artifact-management.html>)

**See also:** [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>), [Artifact Management](</en/tech/artifact-management.html>)

**See also:** [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>), [Artifact Management](</en/tech/artifact-management.html>)

**See also:** [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>), [Artifact Management](</en/tech/artifact-management.html>)

**See also:** [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>), [Artifact Management](</en/tech/artifact-management.html>)

**See also:** [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>), [Artifact Management](</en/tech/artifact-management.html>)

**See also:** [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>), [Artifact Management](</en/tech/artifact-management.html>)
