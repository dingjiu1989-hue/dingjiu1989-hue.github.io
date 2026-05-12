#!/usr/bin/env python3
"""Generate final 27 EN articles to reach 1000 total."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_DIR = ROOT / 'md' / 'en'

ARTICLES = {
    'architecture': [
        {
            'slug': 'architecture-decision-records',
            'title': 'Architecture Decision Records: Documenting Technical Decisions',
            'desc': 'Capture and manage architecture decisions with ADRs: templates, workflows, and team adoption strategies.',
            'content': '''
Architecture Decision Records (ADRs) document significant architectural decisions and their context. An ADR captures the decision, the alternatives considered, the rationale, and the consequences. This creates an organizational memory that persists beyond team changes.

## ADR Structure

Each ADR follows a consistent format. Title includes a short description and a unique number. Status indicates whether the decision is proposed, accepted, deprecated, or superseded. Context describes the problem and constraints that led to the decision.

Decision states the chosen approach explicitly. Consequences document the trade-offs, both positive and negative. Alternatives list approaches that were considered and why they were rejected.

## Storage and Discovery

Store ADRs in version control alongside the code they describe. A \_docs/adr directory is conventional. Use sequential numbers or ISO dates as prefixes: 001-use-postgresql.md or 2026-05-use-postgresql.md. ADRs in version control are linked to commits and code changes.

## Adoption

Start documenting decisions during design discussions. Write the ADR when the decision is made, not after. Review ADRs during architecture reviews. Link ADRs in pull requests that implement the decision. Keep ADRs short—one page is ideal.
''',
        },
        {
            'slug': 'domain-event-implementation',
            'title': 'Domain Event Implementation: Publishing, Handling, and Testing',
            'desc': 'Implement domain events in DDD: event definitions, publishing patterns, handlers, and testing strategies.',
            'content': '''
Domain events capture significant business occurrences within a domain-driven system. When a domain expert says "when the order is shipped, send an invoice," the "order shipped" is a domain event. Events are named in the past tense: OrderShipped, PaymentReceived, InvoiceGenerated.

## Event Definition

Each event is an immutable object containing the data relevant to the occurrence. Events include a unique identifier, a timestamp, and the business data. Event names come from the ubiquitous language. The structure should be kept stable—consumers depend on it.

## Publishing

Events are published from the domain layer when an aggregate changes state. The aggregate returns events after command execution. The application layer collects and publishes these events to a message bus or event store.

Transactional outbox ensures events are published reliably. The outbox stores events in the same database transaction as the state change. A separate process reads the outbox and publishes events to the message broker.
''',
        },
        {
            'slug': 'event-notification-vs-event-carrying',
            'title': 'Event Notification vs Event-Carried State Transfer',
            'desc': 'Compare event notification and event-carried state transfer patterns for microservices communication.',
            'content': '''
Event notification and event-carried state transfer are two patterns for communicating state changes between microservices. The choice affects coupling, data consistency, and service autonomy.

## Event Notification

The publisher sends only a reference to the changed entity. Consumers must query the publisher's API for details. This minimizes coupling—consumers know only that something changed. The publisher's API remains the source of truth.

Drawbacks: each consumer must make additional API calls. This increases latency and reduces availability. If the publisher is down during event processing, consumers cannot get the full picture.

## Event-Carried State Transfer

The publisher includes all relevant data in the event. Consumers can process events without querying the publisher. This reduces latency and increases resilience—consumers have the data they need even if the publisher is unavailable.

Trade-offs: data duplication increases storage requirements. Consumers may have stale data if the publisher changes its data model. The event schema becomes a public contract between publisher and consumers.

## Choosing

Use event notification when the consumer always needs fresh data or the event's context is minimal. Use event-carried state transfer when consumers need data immediately or the publisher's API availability cannot be guaranteed.
''',
        },
        {
            'slug': 'saga-process-manager',
            'title': 'Saga vs Process Manager: Orchestration Patterns Compared',
            'desc': 'Compare saga orchestration with process manager patterns for distributed transaction management.',
            'content': '''
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
''',
        },
    ],
    'database': [
        {
            'slug': 'database-audit-triggers',
            'title': 'Database Audit Triggers: Automatic Change Tracking',
            'desc': 'Implement database audit logging with triggers: audit tables, trigger functions, and compliance reporting.',
            'content': '''
Database triggers can automatically capture changes to sensitive data for audit purposes. An audit trigger logs who changed what, when, and the old and new values. This provides a reliable audit trail that cannot be bypassed.

## Audit Table Design

The audit table captures the table name, operation type (INSERT, UPDATE, DELETE), the old row values, the new row values, the user who made the change, and a timestamp. For compliance, include the application context—the session ID, IP address, and transaction ID.

## Trigger Implementation

Each audited table gets a trigger that fires on INSERT, UPDATE, DELETE. The trigger function captures the OLD and NEW row values and inserts into the audit table. Row-level triggers capture individual row changes with full context.

## Performance Considerations

Audit triggers add overhead to every DML operation. Batch the audit writes when possible. Consider asynchronous audit logging for high-traffic tables. Archive audit data regularly. Index the audit table on timestamp and table name for efficient queries.

## Compliance

Audit logs support SOX, HIPAA, PCI-DSS, and SOC 2 compliance. They provide evidence of data access and modification. Keep audit logs immutable—restrict write access and set retention policies. Test audit coverage regularly.
''',
        },
        {
            'slug': 'database-change-tracking-cdc',
            'title': 'Change Data Capture: Tracking Database Changes in Real-Time',
            'desc': 'Implement change data capture (CDC) for real-time data synchronization, event streaming, and audit logging.',
            'content': '''
Change Data Capture (CDC) tracks row-level changes in a database and streams them to other systems. CDC captures inserts, updates, and deletes without application-level instrumentation. It is the foundation for event-driven architectures and real-time data pipelines.

## CDC Methods

Log-based CDC reads the database transaction log (WAL in PostgreSQL, binlog in MySQL). It captures all changes with minimal database impact. Log-based CDC is the preferred method because it does not require schema changes and has low overhead.

Trigger-based CDC uses database triggers to capture changes. It provides more control over what is captured but adds overhead to every write. Trigger-based CDC is suitable when log-based capture is not available.

Polling-based CDC periodically queries tables for changes using timestamp or version columns. It is the simplest to implement but has higher latency and database impact. Polling is suitable for low-frequency synchronization.

## Tools

Debezium is the most popular CDC platform. It connects to database transaction logs and streams changes to Apache Kafka. Debezium supports PostgreSQL, MySQL, MongoDB, SQL Server, and Oracle.

## Use Cases

CDC supports data warehouse synchronization, cache invalidation, search index updates, event streams for microservices, and real-time analytics. It reduces coupling between operational and analytical systems.
''',
        },
        {
            'slug': 'database-foreign-key-constraints',
            'title': 'Foreign Key Constraints: Referential Integrity in Practice',
            'desc': 'Master foreign key constraints: referential actions, performance impact, and real-world integrity patterns.',
            'content': '''
Foreign key constraints enforce referential integrity between related tables. They guarantee that a value in one table has a corresponding value in another. Without foreign keys, applications must enforce relationships, which is error-prone.

## Referential Actions

ON DELETE CASCADE automatically deletes related rows when the parent row is deleted. Use when child rows have no meaning without the parent. Be careful with cascading deletes in deep relationship chains.

ON DELETE SET NULL sets the foreign key column to NULL when the parent is deleted. Use when the relationship is optional and child rows should survive parent deletion.

ON DELETE RESTRICT prevents deletion of the parent if child rows exist. This is the safest default—it prevents accidental data loss.

## Performance

Foreign keys add overhead to INSERT, UPDATE, and DELETE operations. Each write validates that referenced rows exist. The overhead is typically small but matters for bulk operations.

Indexes on foreign key columns are essential. Without indexes, each write to the parent table triggers a full table scan on the child table. PostgreSQL does not automatically index foreign keys; MySQL InnoDB does.

## Practical Guidelines

Use foreign keys to enforce relationships that are business rules. Skip them for high-volume logging tables where referential integrity is not critical. Always index foreign key columns. Consider deferrable constraints for bulk load operations.
''',
        },
        {
            'slug': 'database-query-profiling',
            'title': 'Database Query Profiling: Finding and Fixing Performance Bottlenecks',
            'desc': 'Profile database queries to identify bottlenecks: execution plans, wait events, and systematic optimization.',
            'content': '''
Query profiling identifies why a query is slow. Rather than guessing, profiling measures where time is spent: CPU, I/O, locks, or network. This data guides targeted optimization.

## Profiling Tools

PostgreSQL: EXPLAIN ANALYZE BUFFERS shows execution plan with actual timing and buffer access. pg_stat_statements tracks query statistics. auto_explain logs slow queries automatically. pgBadger analyzes PostgreSQL logs for query performance patterns.

MySQL: EXPLAIN ANALYZE (MySQL 8.0.18+) shows execution plan. performance_schema tracks query execution statistics. sys schema provides query performance summaries. pt-query-digest analyzes slow query logs.

## Key Metrics

Execution time: total time and time per execution. Buffer usage: shared hit reveals cache efficiency. Rows examined vs returned: high examined-to-returned ratio suggests missing indexes. Wait events: what the query is waiting for (I/O, locks, CPU).

## Optimization Workflow

Identify slow queries via monitoring. Profile with EXPLAIN ANALYZE. Check for sequential scans on large tables. Verify index usage. Examine join strategies. Review sort operations. Test the fix. Profile again to confirm improvement. Monitor in production.
''',
        },
    ],
    'compare': [
        {
            'slug': 'nginx-vs-apache',
            'title': 'Nginx vs Apache: Web Server Comparison 2026',
            'desc': 'Compare Nginx and Apache web servers: architecture, performance, configuration, and ecosystem.',
            'content': '''
Nginx and Apache are the two dominant web servers. Nginx uses an event-driven, asynchronous architecture. Apache uses a process-driven architecture with MPM (Multi-Processing Modules).

## Architecture

Nginx handles thousands of concurrent connections with a single thread. Each connection is handled as an event in an event loop. This makes Nginx memory-efficient under high concurrency. Nginx cannot embed interpreters—it proxies requests to application servers.

Apache uses one thread or process per connection. Prefork MPM creates separate processes. Worker MPM uses threads. Event MPM keeps connections alive without consuming threads. Apache supports embedded interpreters via mod_php, mod_perl, and mod_python.

## Performance

Nginx excels at static file serving and high-concurrency connections. It handles 10,000+ concurrent connections with minimal memory. Apache performs well for dynamic content when using embedded interpreters.

## Configuration

Nginx configuration is clean and hierarchical. Apache configuration uses per-directory .htaccess files, which add flexibility but require directory traversal on every request. Nginx does not support .htaccess.

## Ecosystem

Apache has more modules and longer history. Nginx has a growing module ecosystem and better integration with modern architectures. Nginx is the default in most container images.

## Choosing

Use Nginx for high-concurrency static serving, reverse proxy, and microservices. Use Apache for shared hosting environments requiring .htaccess compatibility and embedded interpreters.
''',
        },
        {
            'slug': 'flask-vs-fastapi',
            'title': 'Flask vs FastAPI: Python Web Framework Comparison 2026',
            'desc': 'Compare Flask and FastAPI Python web frameworks: async support, performance, ecosystem, and use cases.',
            'content': '''
Flask and FastAPI are the two most popular Python web frameworks. Flask is mature and minimalist. FastAPI is modern with async support and automatic OpenAPI documentation.

## Async Support

FastAPI is built on Starlette and Pydantic with native async support. It handles concurrent requests efficiently without threading complexities. FastAPI supports async routes, dependencies, and database sessions.

Flask is synchronous by design. Async support exists via Quart (a Flask-like async framework) but is not native. Flask sync works well for I/O-bound tasks when combined with thread pools.

## Performance

FastAPI performs 3-5x better than Flask on typical web workloads. The async request handling reduces overhead. FastAPI matches Node.js and Go performance for many workloads.

## Developer Experience

FastAPI provides automatic OpenAPI documentation, request validation via Pydantic models, and dependency injection. This reduces boilerplate and catches errors at request time.

Flask has a larger ecosystem with more extensions and tutorials. It is simpler to start with but requires more manual setup for type validation and documentation.

## Choosing

Use FastAPI for new projects requiring async performance and automatic API documentation. Use Flask for existing Flask projects, simple APIs, and teams familiar with its patterns.
''',
        },
    ],
    'tech': [
        {
            'slug': 'monorepo-vs-multirepo',
            'title': 'Monorepo vs Multirepo: Repository Strategy Comparison',
            'desc': 'Compare monorepo and multirepo strategies: tooling, scaling, CI/CD, and team workflow implications.',
            'content': '''
The monorepo vs multirepo decision affects developer workflow, CI/CD efficiency, and team autonomy. Both approaches have strong advocates and proven implementations.

## Monorepo

A monorepo stores all projects, libraries, and services in a single repository. Google, Meta, and Microsoft use monorepos. Single versioning eliminates dependency version conflicts. Shared tooling and standards reduce configuration overhead. Cross-project refactoring is easier. CI/CD requires selective execution to avoid running all tests for every change.

Tools: Bazel, Nx, Turborepo, Rush, Lerna. These tools enable incremental builds, affected project detection, and dependency graph management.

## Multirepo

Each project or service has its own repository. Teams have autonomy over their tooling and release cycles. Repository size stays manageable. CI/CD is simpler per repository. Cross-project changes require coordination across repos.

## CI/CD Considerations

Monorepos need smart CI/CD to only build changed projects. Multirepos need cross-repo coordination for shared changes. Monorepo CI/CD is harder to configure but more efficient for cross-cutting changes.

## Choosing

Start with a monorepo for small to medium teams (under 50 developers). Move to multirepos when team autonomy becomes a bottleneck. Many organizations use a hybrid approach: monorepo for related projects, separate repos for independent teams.
''',
        },
        {
            'slug': 'api-versioning-rest-graphql',
            'title': 'API Versioning Strategies: REST vs GraphQL Approaches',
            'desc': 'Compare API versioning strategies for REST and GraphQL: URL versioning, header versioning, schema evolution.',
            'content': '''
API versioning manages changes to public interfaces without breaking existing clients. REST and GraphQL handle versioning differently due to their architectural differences.

## REST Versioning

URL versioning embeds the version in the path: /v1/users, /v2/users. It is the most common approach. Simple to implement and discoverable. It encourages maintaining multiple API versions simultaneously.

Header versioning uses custom headers: Accept: application/vnd.api+json;version=2. Keeps URLs clean. Version negotiation is handled by the client. More complex to implement but follows REST principles more closely.

Query parameter versioning uses ?version=2. Simple but easily overlooked. Not recommended for production APIs.

## GraphQL Versioning

GraphQL avoids traditional versioning. The schema evolves by adding new fields and deprecating old ones. Clients request only the fields they need, so new fields do not break existing queries.

Deprecated fields remain in the schema but are marked @deprecated. Clients receive deprecation warnings in responses. After sufficient migration time, deprecated fields can be removed.

## Choosing

For REST, use URL versioning for simple APIs and header versioning for API-first products. For GraphQL, use schema evolution with deprecation rather than versioned endpoints. Always document breaking changes and provide migration guides.
''',
        },
    ],
    'ai': [
        {
            'slug': 'ai-code-generation-tools',
            'title': 'AI Code Generation: Tools, Workflows, and Best Practices',
            'desc': 'Compare AI code generation tools: GitHub Copilot, Cursor, Claude Code. Best practices for AI-assisted development.',
            'content': '''
AI code generation tools have transformed software development. These tools suggest code, explain existing code, and automate repetitive tasks. Choosing the right tool depends on workflow integration, language support, and team needs.

## Tools Overview

GitHub Copilot integrates with VS Code, JetBrains, and Neovim. It provides inline code suggestions based on context. Copilot Chat enables interactive code generation and explanation. It supports all major languages.

Cursor is an AI-first IDE built on VS Code. It provides deep codebase understanding, multi-file editing, and agentic code generation. Cursor excels at larger refactoring tasks that span multiple files.

Claude Code operates in the terminal and supports complex multi-step tasks. It can plan implementations, write code, run tests, and debug issues autonomously.

## Workflow Integration

AI tools work best with clear context. Provide relevant files, documentation, and requirements. Review AI-generated code before committing—treat AI suggestions as a first draft, not a final product.

## Best Practices

Use AI for boilerplate, tests, documentation, and simple functions. Review AI code for correctness, security, and style. Test AI-generated code as thoroughly as hand-written code. Understand what AI generates—do not accept code you cannot explain.

## Limitations

AI tools may produce incorrect, insecure, or inefficient code. They lack business context and architectural awareness. AI code requires human review and testing. Never use AI-generated code without understanding its implications.
''',
        },
        {
            'slug': 'ai-prompt-chaining',
            'title': 'Prompt Chaining: Building Multi-Step LLM Workflows',
            'desc': 'Design prompt chains for complex LLM tasks: chain types, state management, error handling, and performance optimization.',
            'content': '''
Prompt chaining connects multiple LLM calls to accomplish complex tasks. Instead of solving everything in one prompt, chains break the task into manageable steps. Each step builds on the previous output.

## Chain Types

Sequential chains pass output from one step to the next. Example: extract text → summarize → translate. Each step depends on the previous one. Sequential chains are simple but accumulate latency.

Parallel chains execute independent steps concurrently. Example: research a topic from multiple sources simultaneously. Parallel chains reduce total execution time for independent sub-tasks.

Conditional chains use the output of one step to decide what to do next. Example: classify the user intent, then route to the appropriate handler. Conditional chains enable flexible, adaptive workflows.

## State Management

Chain state accumulates across steps. Store intermediate results in a structured format (JSON). Pass relevant context to each step. Clean up unnecessary state to reduce token consumption.

## Error Handling

Each chain step can fail. Implement retry logic for transient failures. Use fallback prompts for repeated failures. Validate outputs between steps. Log chain execution for debugging.

## Performance

Minimize chain length. Each step adds latency and cost. Combine related tasks into fewer, larger prompts. Cache identical prompt results. Monitor token usage per chain execution.
''',
        },
        {
            'slug': 'ai-model-deployment-strategies',
            'title': 'AI Model Deployment: Strategies for Production LLM Serving',
            'desc': 'Deploy LLMs to production: serving infrastructure, batching, caching, load balancing, and cost optimization.',
            'content': '''
Deploying AI models to production requires infrastructure for serving, scaling, and monitoring. LLM deployment differs from traditional ML deployment due to high compute requirements, variable latency, and unique cost models.

## Serving Options

Managed APIs (OpenAI, Anthropic, Google) provide the simplest deployment. No infrastructure management. Pay per token. Best for most applications. Limited customization and data control.

Self-hosted (vLLM, TGI, Triton) provide full control. Lower per-token cost at scale. Data stays within your infrastructure. Requires GPU infrastructure and operational expertise.

Hybrid: use managed APIs for production and self-hosted for high-volume or sensitive workloads. This balances cost, latency, and control.

## Infrastructure

LLM serving requires GPU instances (A100, H100). Use autoscaling to handle traffic variability. Load balance across instances. Implement request queuing and retry logic. Monitor GPU utilization and memory.

## Optimization Techniques

Continuous batching: combine multiple requests into a single batch for efficient GPU utilization. Speculative decoding: use a small model to generate tokens that a large model validates. KV-cache optimization: reuse cached attention computations across requests.

Prompt caching: store processed prompt outputs for identical or similar requests. Semantic caching: cache responses for semantically similar inputs. These techniques reduce both latency and cost.

## Monitoring

Track latency (TTFT and TPOT), throughput (tokens/second), error rates, and cost per request. Monitor GPU memory, utilization, and temperature. Set up alerts for latency spikes and error rate increases.
''',
        },
    ],
    'tools': [
        {
            'slug': 'cloud-cost-tools',
            'title': 'Cloud Cost Management Tools: Saving Money on AWS, Azure, GCP',
            'desc': 'Compare cloud cost management tools: native tools, third-party platforms, and cost optimization strategies.',
            'content': '''
Cloud cost management tools help organizations understand and optimize cloud spending. Without proper tooling, cloud costs grow faster than infrastructure usage.

## Native Tools

AWS Cost Explorer provides cost visualization, usage reports, and budget alerts. AWS Compute Optimizer suggests right-sizing recommendations. Trusted Advisor identifies cost optimization opportunities.

Azure Cost Management offers budgeting, cost allocation, and recommendations. Azure Advisor provides optimization suggestions. Azure Reservations provide significant discounts for committed usage.

GCP Cost Table reports spending and provides recommendations. GCP Committed Use Discounts reduce costs for consistent usage.

## Third-Party Tools

Vantage: user-friendly interface, real-time cost tracking, and multi-cloud support. Supports AWS, Azure, GCP, and Kubernetes cost allocation.

CloudHealth: comprehensive multi-cloud management. Cost optimization, security, and compliance in one platform. Best for enterprise environments.

## Optimization Strategies

Right-size instances, use reserved instances, implement auto-scaling, clean up unused resources, use spot instances for non-critical workloads, implement tagging for cost allocation, set budgets and alerts, and review costs weekly.
''',
        },
        {
            'slug': 'issue-tracking-tools',
            'title': 'Issue Tracking Tools: Jira, Linear, GitHub Issues, and More',
            'desc': 'Compare issue tracking and project management tools for software teams of all sizes.',
            'content': '''
Issue tracking tools manage bugs, feature requests, tasks, and project progress. The right tool depends on team size, workflow complexity, and integration needs.

## Jira

Jira is the most powerful and customizable issue tracker. Supports Scrum, Kanban, and custom workflows. Rich plugin ecosystem. Best for enterprise teams with complex workflows. Can be overwhelming for small teams due to complexity.

## Linear

Linear is a modern issue tracker focused on speed and developer experience. Fast keyboard navigation, clean interface, and GitHub integration. Best for startups and product teams. Simpler than Jira but less customizable.

## GitHub Issues

GitHub Issues is integrated with GitHub repositories. Supports labels, milestones, projects, and issue templates. Best for open-source projects and small teams already using GitHub. Limited compared to dedicated tools.

## Choosing

Use Jira for enterprise teams with complex workflows. Use Linear for fast-moving product teams. Use GitHub Issues for open-source projects. Use Trello for simple task boards. Use Asana for cross-team project management.
''',
        },
        {
            'slug': 'productivity-tools',
            'title': 'Developer Productivity Tools: Essential Toolkit for 2026',
            'desc': 'Essential developer productivity tools: time tracking, knowledge management, focus tools, and workflow automation.',
            'content': '''
Developer productivity goes beyond code editors and compilers. The right supporting tools reduce context switching, improve focus, and streamline workflows.

## Time Management

Toggl Track and RescueTime track how time is spent across applications and websites. Focusmate provides virtual coworking sessions for deep work. Pomodoro timers (Focus Booster, Pomofocus) structure work into focused intervals.

## Knowledge Management

Notion, Obsidian, and Logseq are the three leading knowledge management tools. Notion excels at team wikis and documentation. Obsidian provides local-first markdown notes with graph view. Logseq is an open-source outliner for personal knowledge management.

## Focus Tools

Cold Turkey and Freedom block distracting websites during focus sessions. Brain.fm provides focus-enhancing music. Noisli provides ambient sounds for concentration.

## Workflow Automation

Alfred (macOS) and PowerToys (Windows) provide launcher shortcuts. Keyboard Maestro automates repetitive tasks. TextExpander handles snippet expansion. Hazel automates file organization on macOS.
''',
        },
        {
            'slug': 'text-editor-comparison',
            'title': 'Code Editors Compared: VS Code, Neovim, JetBrains, Zed 2026',
            'desc': 'Compare VS Code, Neovim, JetBrains IDEs, and Zed for developer productivity and workflow.',
            'content': '''
The choice of code editor affects developer productivity daily. Modern editors offer powerful features but differ in philosophy, extensibility, and workflow.

## VS Code

Most popular editor with the largest extension ecosystem. Excellent language support via Language Server Protocol. Integrated terminal, debugger, and Git. Built-in AI features with Copilot integration. Runs everywhere. Extensions can impact performance.

## Neovim

Modal editor optimized for keyboard-driven workflows. Highly configurable via Lua. Lightweight and fast. Lua-based plugin ecosystem (Lazy.nvim). Steep learning curve but highly efficient once mastered. Excellent for terminal-based development and remote editing.

## JetBrains IDEs

Language-specific IDEs (IntelliJ IDEA, PyCharm, GoLand, WebStorm). Deep code analysis, refactoring, and debugging. Excellent for complex codebases. Heavy memory usage. Slower startup. Best for professional development in specific languages.

## Zed

Next-generation editor written in Rust. GPU-accelerated rendering. Fast startup and editing. Built-in AI features. Limited extension ecosystem. Newer with fewer integrations. Promising for performance-conscious developers.

## Choosing

Start with VS Code. Move to Neovim for keyboard efficiency. Use JetBrains for complex projects in a single language. Try Zed for a fast, modern experience.
''',
        },
    ],
    'sidehustle': [
        {
            'slug': 'bootstrapping-essentials',
            'title': 'Bootstrapping Essentials: Building a Startup Without VC Funding',
            'desc': 'Practical guide to bootstrapping a SaaS startup: lean operations, revenue-first growth, and sustainable scaling.',
            'content': '''
Bootstrapping means building a business with personal resources and revenue rather than investor funding. It forces discipline, focus, and revenue-first thinking. Bootstrapped companies often have higher survival rates than VC-backed ones.

## Lean Operations

Keep fixed costs minimal. Use serverless and managed services instead of dedicated infrastructure. Start with a single product. Hire slowly—consider contractors and part-time help before full-time employees. Use no-code and low-code tools for non-core operations.

## Revenue First

Charge from day one. Validate pricing early. Focus on customers who will pay. Avoid free tiers that attract non-paying users. Raise prices gradually. Revenue is the only sustainable growth engine for bootstrapped businesses.

## Growth Without Budget

Content marketing and SEO provide the highest ROI for bootstrapped companies. Write about problems your target customers face. Build in public on Twitter and LinkedIn. Participate in relevant communities. Referral programs incentivize word-of-mouth growth.

## Sustainable Scaling

Grow within your revenue constraints. Avoid premature scaling. Invest in automation before hiring. Maintain profitability as the primary metric. Build cash reserves for slow periods.
''',
        },
        {
            'slug': 'remote-freelancing-guide',
            'title': 'Remote Freelancing Guide: Finding Clients and Scaling Income',
            'desc': 'Build a successful remote freelancing career: platforms, pricing, client management, and income scaling.',
            'content': '''
Remote freelancing offers location independence, income potential, and career flexibility. Success requires client acquisition, effective pricing, and scalable operations.

## Finding Clients

Upwork and Toptal provide access to global clients. Build a professional profile with relevant experience and portfolio. Start with smaller projects to build ratings. Gradually increase rates. Niche expertise commands premium rates.

Direct outreach to companies in your niche is more effective than platform applications. Build a professional website. Write case studies of past work. Network in industry communities. Offer value before asking for work.

## Pricing Strategies

Hourly billing is simple but limits income. Value-based pricing aligns fees with client outcomes. Retainer arrangements provide predictable income. Project pricing is best for defined scopes.

## Scaling

Automate administrative tasks: invoicing, proposals, contracts. Use tools like HoneyBook or Bonsai. Build a referral network with other freelancers. Raise rates 10-20% annually. Hire subcontractors for overflow work. Transition to a micro-agency model.
''',
        },
    ],
    'security': [
        {
            'slug': 'container-scanning-tools',
            'title': 'Container Scanning Tools: Securing Images in CI/CD',
            'desc': 'Compare container image scanning tools: Trivy, Snyk, Clair, Docker Scout for vulnerability detection.',
            'content': '''
Container image scanning identifies vulnerabilities in container images before deployment. Scanning integrates into CI/CD pipelines to prevent vulnerable images from reaching production.

## Tools

Trivy is open-source and covers OS packages and language dependencies. Fast scanning with comprehensive vulnerability database. Integrates with CI/CD and Kubernetes. Free for all use cases.

Snyk provides developer-friendly scanning with fix suggestions. Supports container images and IaC scanning. Commercial product with per-developer pricing. Good reporting and policy management.

Clair is CoreOS's open-source scanner. Static analysis of container layers. Good for self-hosted scanning infrastructure. Limited language-specific scanning.

Docker Scout integrates with Docker Desktop and Hub. Provides contextual vulnerability analysis based on usage. Good for teams already using Docker ecosystem.

## CI/CD Integration

Scan images after build, before push to registry. Gate deployments on scan results. Fail builds on critical vulnerabilities. Allowlist known acceptable vulnerabilities. Schedule regular scanning for deployed images.

## Best Practices

Scan early and often. Use minimal base images (distroless, Alpine). Pin base image versions. Subscribe to vulnerability notifications. Maintain a vulnerability management policy. Regularly update base images.
''',
        },
        {
            'slug': 'security-compliance-tools',
            'title': 'Security Compliance Automation: SOC 2, ISO 27001, HIPAA Tools',
            'desc': 'Automate security compliance: compliance frameworks, evidence collection, monitoring, and audit preparation tools.',
            'content': '''
Security compliance tools automate the collection, monitoring, and reporting required for compliance frameworks. They reduce the manual effort of audit preparation and continuous compliance.

## Tools by Framework

SOC 2: Vanta, Drata, and Secureframe automate evidence collection, policy management, and continuous monitoring. They integrate with AWS, GCP, Azure, GitHub, and common SaaS tools. Automated control testing runs daily.

ISO 27001: StandardFusion and ISMS.online manage the ISMS, risk register, and audit evidence. They support document control, internal audits, and management review processes.

HIPAA: Compliancy Group and Hipaa Secure Now provide gap analysis, policy templates, and audit support. They focus on the administrative, physical, and technical safeguards required by HIPAA.

## Automation Patterns

Automated evidence collection gathers logs, configurations, and access reviews without manual effort. Continuous monitoring detects compliance drift in real-time. Policy management distributes and tracks acceptance of security policies.

## Implementation

Map controls to framework requirements. Configure integrations with infrastructure and SaaS tools. Define evidence collection schedules. Set up alerts for control failures. Run mock audits before the real one.
''',
        },
        {
            'slug': 'security-testing-tools',
            'title': 'Security Testing Tools: SAST, DAST, IAST, and RASP Compared',
            'desc': 'Compare application security testing approaches: SAST, DAST, IAST, RASP tools and integration strategies.',
            'content': '''
Application security testing identifies vulnerabilities in software. Different testing approaches find different types of issues and operate at different stages of the SDLC. A comprehensive security testing program uses multiple approaches.

## SAST (Static Analysis)

SAST analyzes source code without executing it. It finds vulnerabilities early in development. SAST tools scan for injection flaws, buffer overflows, insecure cryptographic practices, and other code-level issues.

Tools: SonarQube, Checkmarx, Fortify, Semgrep. SonarQube is the most popular open-source option. Semgrep provides custom rule writing for team-specific patterns.

## DAST (Dynamic Analysis)

DAST tests running applications by sending malicious inputs and observing responses. It finds runtime vulnerabilities that SAST cannot detect: authentication bypass, session management flaws, and business logic errors.

Tools: OWASP ZAP (open-source), Burp Suite (professional), Acunetix (commercial). OWASP ZAP provides automated scanning with CI/CD integration.

## IAST (Interactive Analysis)

IAST instruments the application and analyzes code execution during testing. It combines SAST's code analysis with DAST's runtime context. IAST provides fewer false positives than SAST and deeper coverage than DAST.

## RASP (Runtime Protection)

RASP monitors application behavior at runtime and blocks attacks. It provides real-time protection without requiring code changes. RASP complements other testing approaches by protecting against unknown vulnerabilities.

## Integration

Use SAST in the IDE for early feedback. Run SAST in CI/CD for every commit. Schedule DAST scans weekly or before releases. Use IAST during QA testing. Deploy RASP in production for defense-in-depth.
''',
        },
        {
            'slug': 'zero-trust-networking',
            'title': 'Zero Trust Networking: Architecture and Implementation Guide',
            'desc': 'Implement zero trust networking: micro-segmentation, identity-based access, and encrypted communication.',
            'content': '''
Zero Trust Networking (ZTN) assumes no network is trusted. Every request must be authenticated, authorized, and encrypted regardless of origin. ZTN replaces the traditional castle-and-moat security model with identity-based perimeter defense.

## Core Principles

Never trust, always verify: every request is authenticated and authorized. Assume breach: design for containment if an attacker gains access. Least privilege: grant the minimum access needed. Micro-segmentation: isolate workloads to limit lateral movement.

## Architecture Components

Identity-aware proxy: authenticates users and devices before granting network access. Micro-segmentation: divides the network into isolated zones with granular firewall rules. Encrypted tunnels: all communication is encrypted using mTLS or WireGuard.

## Implementation

Start with identity-based access for critical services. Implement mTLS for service-to-service communication. Deploy network micro-segmentation. Implement continuous monitoring and logging. Roll out gradually—start with non-critical workloads.

## Tools

Cloudflare Zero Trust, Zscaler, and Tailscale provide ZTN solutions. Istio and Cilium provide service mesh with mTLS and micro-segmentation for Kubernetes. OpenZiti provides open-source zero trust networking.
''',
        },
        {
            'slug': 'identity-provider-comparison',
            'title': 'Identity Providers Compared: Auth0, Okta, Keycloak, Firebase Auth',
            'desc': 'Compare identity providers: Auth0, Okta, Keycloak, Firebase Auth for authentication and user management.',
            'content': '''
Identity providers (IdPs) handle user authentication, authorization, and identity management. Choosing the right IdP affects security, developer experience, and operational costs.

## Auth0

Auth0 is the most popular identity platform. It supports social login, multi-factor authentication, passwordless, and enterprise SSO. Extensive SDK library for web and mobile. Customizable login pages. Generous free tier.

## Okta

Okta targets enterprise identity management. It excels at workforce identity, single sign-on, and lifecycle management. Strong compliance and audit capabilities. Higher pricing. Best for organizations with complex enterprise identity requirements.

## Keycloak

Keycloak is an open-source identity and access management solution. It supports OAuth 2.0, OIDC, and SAML. Self-hosted. Flexible and customizable. Requires operational expertise to deploy and maintain.

## Firebase Auth

Firebase Auth provides authentication for mobile and web apps. Supports email/password, social login, phone auth, and anonymous auth. Free with Firebase project. Limited customization. Tight integration with Firebase ecosystem.

## Choosing

Use Auth0 for general-purpose web and mobile apps. Use Okta for enterprise SSO and workforce identity. Use Keycloak for self-hosted, customizable solutions. Use Firebase Auth for Firebase-based projects. Use Cognito for AWS-native applications.
''',
        },
        {
            'slug': 'waf-comparison',
            'title': 'WAF Solutions Compared: Cloudflare, AWS WAF, ModSecurity, Akamai',
            'desc': 'Compare Web Application Firewall solutions: Cloudflare, AWS WAF, ModSecurity, Akamai for application protection.',
            'content': '''
Web Application Firewalls (WAF) protect web applications from common attacks including SQL injection, XSS, and DDoS. WAFs analyze HTTP traffic and block malicious requests before they reach the application.

## Cloudflare WAF

Cloudflare offers the most accessible WAF. Integrated with CDN and DDoS protection. Managed rule sets for OWASP Top 10. Rate limiting and bot management. Free tier includes basic WAF rules. Pay-as-you-go pricing.

## AWS WAF

AWS WAF integrates with CloudFront, ALB, API Gateway, and AppSync. Managed rule groups from AWS and third parties. Custom rules using JSON. Web ACLs for fine-grained access control. Pricing per rule and per request.

## ModSecurity

ModSecurity is the leading open-source WAF engine. It works with Apache, Nginx, and IIS. Core Rule Set (CRS) provides OWASP Top 10 protection. Highly customizable. Requires manual configuration and tuning.

## Akamai WAF

Akamai App & API Protector provides enterprise WAF with edge delivery. Advanced bot management and API protection. Machine learning-based attack detection. High cost. Best for large enterprises with global traffic.

## Choosing

Use Cloudflare for most web applications. Use AWS WAF for AWS-native architectures. Use ModSecurity for self-hosted, cost-sensitive deployments. Use Akamai for large enterprises with global traffic and compliance requirements.
''',
        },
    ],
}

def write_md(filepath, title, desc, content, board):
    frontmatter = f'''---
title: "{title}"
description: "{desc}"
date: 2026-05-12
board: {board}
url: https://dingjiu1989-hue.github.io/en/{board}/{filepath.stem}.html
---
'''
    with open(filepath, 'w') as f:
        f.write(frontmatter)
        f.write(f'\n# {title}\n')
        f.write(content.strip())
        f.write('\n')

def main():
    total = 0
    for board, articles in ARTICLES.items():
        board_dir = EN_DIR / board
        board_dir.mkdir(parents=True, exist_ok=True)

        for art in articles:
            slug = art['slug']
            fp = board_dir / f'{slug}.md'
            if fp.exists():
                print(f"  SKIP (exists): {board}/{slug}")
                continue
            write_md(fp, art['title'], art['desc'], art['content'], board)
            total += 1
            print(f"  WROTE: {board}/{slug}")

    print(f"\n=== Total articles written: {total} ===")

if __name__ == '__main__':
    main()
