---
title: "Dependency Management"
description: "Learn dependency management: lock files, vulnerability scanning, semantic versioning, update strategies, and governance"
date: 2026-01-06
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/dependency-management.html
---

# Dependency Management

Dependency management is a critical but often neglected aspect of software engineering. Every dependency introduces risk: security vulnerabilities, breaking changes, licensing issues, and maintenance burden. This article covers the key practices for managing dependencies effectively, from lock files to vulnerability scanning.

## Lock Files

Lock files pin exact versions of every dependency and its transitive dependencies. They ensure that every build uses the same dependency versions, regardless of when the build runs. This is essential for reproducible builds and consistent behavior across environments.

Package managers generate lock files automatically. npm's `package-lock.json`, Yarn's `yarn.lock`, Python's `poetry.lock` or `Pipfile.lock`, and Go's `go.sum` all serve this purpose. Lock files should be committed to version control. Without committed lock files, a build may install different dependency versions today than it did yesterday, potentially introducing unexpected behavior changes.

Lock files also enable security auditing. When a vulnerability is discovered in a specific dependency version, the lock file shows whether your project is affected. Security scanning tools analyze lock files to identify vulnerable dependencies.

## Semantic Versioning

Semantic versioning (semver) provides a contract for dependency compatibility. MAJOR.MINOR.PATCH versions communicate the scope of changes: MAJOR for breaking changes, MINOR for backward-compatible new features, PATCH for backward-compatible bug fixes.

Understanding semver allows appropriate version ranges in dependency specifications. A caret range (`^1.2.3`) accepts any compatible version (1.x.x). A tilde range (`~1.2.3`) accepts only patch versions (1.2.x). Exact versions specify a single version.

In practice, not all packages follow semver strictly. Minor version releases may include breaking changes. Testing dependency upgrades before deploying to production is essential, regardless of the advertised version number.

## Vulnerability Scanning

Dependency vulnerabilities are a common attack vector. Automated scanning tools detect known vulnerabilities in dependencies by comparing installed versions against vulnerability databases. Dependabot, Snyk, Renovate, and OWASP Dependency-Check are popular scanning tools.

Scanning should be integrated into CI/CD pipelines. A build should fail if critical vulnerabilities are present. The team should have a policy for addressing vulnerabilities: critical vulnerabilities are patched within days, moderate within weeks, and low within the next release cycle.

Beyond known vulnerabilities, scanning should also detect deprecated packages, packages with incompatible licenses, and packages with poor maintenance indicators (no recent releases, unaddressed issues).

## Update Strategies

Dependencies should be updated regularly to receive bug fixes, performance improvements, and security patches. The update strategy balances stability against staying current. A well-defined strategy prevents both stagnation (outdated dependencies with known vulnerabilities) and churn (constantly upgrading for minor improvements).

A common approach uses automated dependency update tools like Renovate or Dependabot. These tools create pull requests when new versions are available. The CI pipeline runs tests against each update PR. If tests pass and the change is minor, it is merged automatically. Major version updates require manual review.

Dependency updates should be small and frequent. A weekly update cycle with automated PRs keeps the dependency tree current without overwhelming the team. Larger, less frequent updates create risk as multiple changes compound.

## Governance

Dependency governance establishes rules for which dependencies can be used and how they are managed. An approved dependency list specifies trusted packages. New dependencies require review, assessing necessity, maintenance quality, license compatibility, and security track record.

Governance prevents dependency sprawl. Each new dependency is an addition to the attack surface, a maintenance commitment, and a potential source of breakage. The question "do we really need this dependency?" should be asked for every new addition.

Unused dependencies should be removed. Dead code elimination is well understood, but unused dependencies are harder to detect. Tools like `depcheck` (JavaScript) and `pip-check-reqs` (Python) identify dependencies that are no longer imported.

## Best Practices

Commit lock files to version control. Run dependency audits regularly. Use automated update tools for routine updates. Review major version upgrades manually. Remove unused dependencies. Maintain a dependency inventory. Establish governance for new dependency approval.

Dependency management requires ongoing attention. Neglected dependencies accumulate risk: security vulnerabilities, compatibility issues, and maintenance burden. A systematic approach with automated tools and clear policies keeps the dependency tree healthy without imposing excessive overhead.

**See also:** [Artifact Management](</en/tech/artifact-management.html>), [CI/CD Best Practices](</en/tech/ci-cd-best-practices.html>), [Performance Testing](</en/tech/performance-testing.html>).

**See also:** [Artifact Management](</en/tech/artifact-management.html>), [Cloud Capacity Planning: Auto-Scaling, Reserved Instances, Spot Instances, and Demand Forecasting](</en/tech/capacity-planning-cloud.html>), [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>)

**See also:** [Artifact Management](</en/tech/artifact-management.html>), [Cloud Capacity Planning: Auto-Scaling, Reserved Instances, Spot Instances, and Demand Forecasting](</en/tech/capacity-planning-cloud.html>), [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>)

**See also:** [Artifact Management](</en/tech/artifact-management.html>), [Cloud Capacity Planning: Auto-Scaling, Reserved Instances, Spot Instances, and Demand Forecasting](</en/tech/capacity-planning-cloud.html>), [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>)

**See also:** [Artifact Management](</en/tech/artifact-management.html>), [Cloud Capacity Planning: Auto-Scaling, Reserved Instances, Spot Instances, and Demand Forecasting](</en/tech/capacity-planning-cloud.html>), [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>)

**See also:** [Artifact Management](</en/tech/artifact-management.html>), [Cloud Capacity Planning: Auto-Scaling, Reserved Instances, Spot Instances, and Demand Forecasting](</en/tech/capacity-planning-cloud.html>), [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>)

**See also:** [Performance Testing](</en/tech/performance-testing.html>), [Secret Management](</en/tech/secret-management.html>), [Testing Strategies](</en/tech/testing-strategies.html>)

**See also:** [Performance Testing](</en/tech/performance-testing.html>), [Secret Management](</en/tech/secret-management.html>), [Testing Strategies](</en/tech/testing-strategies.html>)

**See also:** [Performance Testing](</en/tech/performance-testing.html>), [Secret Management](</en/tech/secret-management.html>), [Testing Strategies](</en/tech/testing-strategies.html>)

**See also:** [Performance Testing](</en/tech/performance-testing.html>), [Secret Management](</en/tech/secret-management.html>), [Testing Strategies](</en/tech/testing-strategies.html>)

**See also:** [Performance Testing](</en/tech/performance-testing.html>), [Secret Management](</en/tech/secret-management.html>), [Testing Strategies](</en/tech/testing-strategies.html>)

**See also:** [Performance Testing](</en/tech/performance-testing.html>), [Secret Management](</en/tech/secret-management.html>), [Testing Strategies](</en/tech/testing-strategies.html>)

**See also:** [Performance Testing](</en/tech/performance-testing.html>), [Secret Management](</en/tech/secret-management.html>), [Testing Strategies](</en/tech/testing-strategies.html>)

**See also:** [Performance Testing](</en/tech/performance-testing.html>), [Secret Management](</en/tech/secret-management.html>), [Testing Strategies](</en/tech/testing-strategies.html>)

**See also:** [Performance Testing](</en/tech/performance-testing.html>), [Secret Management](</en/tech/secret-management.html>), [Testing Strategies](</en/tech/testing-strategies.html>)

**See also:** [Performance Testing](</en/tech/performance-testing.html>), [Secret Management](</en/tech/secret-management.html>), [Testing Strategies](</en/tech/testing-strategies.html>)

**See also:** [Performance Testing](</en/tech/performance-testing.html>), [Secret Management](</en/tech/secret-management.html>), [Testing Strategies](</en/tech/testing-strategies.html>)
