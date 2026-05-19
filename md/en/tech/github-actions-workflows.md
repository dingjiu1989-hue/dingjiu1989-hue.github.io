---
title: "GitHub Actions Workflows: Advanced Patterns"
description: "Advanced GitHub Actions patterns: matrix builds, reusable workflows, caching, environment protection, and custom actions."
date: 2026-01-13
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/github-actions-workflows.html
---

# GitHub Actions Workflows: Advanced Patterns

GitHub Actions powers CI/CD for millions of repositories. Beyond basic workflows, advanced patterns improve reliability, speed, and maintainability.

## Matrix Builds

Matrix builds run the same workflow across multiple configurations. Define a matrix strategy with OS versions, language versions, or dependency configurations. GitHub Actions runs each combination as a separate job in parallel.

Use include and exclude to fine-tune the matrix. Add specific combinations while excluding incompatible ones. Dynamic matrices use JSON output from a previous job to determine the matrix at runtime.

## Reusable Workflows

Reusable workflows (.github/workflows/ with workflow_call trigger) encapsulate common CI patterns. Call them with uses: owner/repo/.github/workflows/ci.yml@v1. Pass inputs and secrets. Reusable workflows standardize CI across an organization.

Composite actions combine multiple steps into a single action. Unlike reusable workflows, composite actions run in the calling workflow's context. Use composites for step-level reuse within a single workflow.

## Caching Dependencies

Cache dependencies with actions/cache. Hash lockfiles (package-lock.json, requirements.txt) to create unique cache keys. Use restore-keys for partial cache matches. Cache npm, pip, Maven, Gradle, and Go module caches for faster builds.

For large monorepos, cache individual package manager caches separately. Monitor cache hit rates—low hit rates indicate ineffective caching strategies.

## Environment Protection

Environments add protection gates. Require reviewers for production deployments. Use environment secrets that are only available to approved deployments. Wait timer delays deployments for a configurable period.

Deployment branches restrict which branches can deploy to an environment. Combined with branch protection rules, this creates a secure deployment pipeline. Audit logs track every deployment.

## Custom Actions

Write custom actions in JavaScript, Docker, or composite. JavaScript actions run directly (fastest). Docker actions support any language. Composite actions compose multiple steps. Publish actions to the Marketplace for organization-wide use.

Inputs, outputs, and pre/post cleanup hooks make actions professional-grade. Test actions with act (local runner) before committing.

**See also:** [Advanced GitHub Actions Workflows](</en/tech/github-actions-advanced.html>), [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Build Optimization](</en/tech/build-optimization.html>).

**See also:** [Advanced GitHub Actions Workflows](</en/tech/github-actions-advanced.html>), [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>)

**See also:** [Advanced GitHub Actions Workflows](</en/tech/github-actions-advanced.html>), [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>)

**See also:** [Advanced GitHub Actions Workflows](</en/tech/github-actions-advanced.html>), [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>)

**See also:** [Advanced GitHub Actions Workflows](</en/tech/github-actions-advanced.html>), [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>)

**See also:** [Advanced GitHub Actions Workflows](</en/tech/github-actions-advanced.html>), [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>)

**See also:** [Dockerfile Best Practices for Production](</en/tech/dockerfile-best-practices.html>), [Advanced Git Techniques for Developers](</en/tech/git-advanced-techniques.html>), [Ansible Automation: Playbooks, Roles, Inventory, and Vault](</en/tech/ansible-automation.html>)

**See also:** [Dockerfile Best Practices for Production](</en/tech/dockerfile-best-practices.html>), [Advanced Git Techniques for Developers](</en/tech/git-advanced-techniques.html>), [Ansible Automation: Playbooks, Roles, Inventory, and Vault](</en/tech/ansible-automation.html>)

**See also:** [Dockerfile Best Practices for Production](</en/tech/dockerfile-best-practices.html>), [Advanced Git Techniques for Developers](</en/tech/git-advanced-techniques.html>), [Ansible Automation: Playbooks, Roles, Inventory, and Vault](</en/tech/ansible-automation.html>)

**See also:** [Dockerfile Best Practices for Production](</en/tech/dockerfile-best-practices.html>), [Advanced Git Techniques for Developers](</en/tech/git-advanced-techniques.html>), [Ansible Automation: Playbooks, Roles, Inventory, and Vault](</en/tech/ansible-automation.html>)

**See also:** [Dockerfile Best Practices for Production](</en/tech/dockerfile-best-practices.html>), [Advanced Git Techniques for Developers](</en/tech/git-advanced-techniques.html>), [Ansible Automation: Playbooks, Roles, Inventory, and Vault](</en/tech/ansible-automation.html>)

**See also:** [Dockerfile Best Practices for Production](</en/tech/dockerfile-best-practices.html>), [Advanced Git Techniques for Developers](</en/tech/git-advanced-techniques.html>), [Ansible Automation: Playbooks, Roles, Inventory, and Vault](</en/tech/ansible-automation.html>)
