---
title: "Python Package Management: pip, Poetry, uv, Conda"
description: "Compare Python package management tools: pip, Poetry, uv, and Conda for dependency resolution and project management."
date: 2026-01-15
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/python-package-management.html
---

# Python Package Management: pip, Poetry, uv, Conda

Python package management has evolved significantly. The ecosystem now offers multiple tools competing for the role of standard package and project manager.

## pip and requirements.txt

pip is Python's default package installer. requirements.txt lists dependencies with optional version constraints. pip installs packages from PyPI into the current environment. It is simple and universal—every Python environment has pip.

pip's limitations include no dependency resolution (it installs the latest compatible version rather than deterministic resolution) and no environment management. pip freeze outputs the current environment's packages but includes dependencies, not just direct requirements. pip-tools (pip-compile) addresses this by generating pinned requirements from loose requirements.

## Poetry

Poetry is a modern dependency manager with deterministic resolution. pyproject.toml replaces setup.py, setup.cfg, and requirements.txt. Poetry.lock pins exact versions for reproducibility.

Poetry manages virtual environments automatically—poetry install creates and activates environments. poetry add installs and adds dependencies in one step. Poetry builds and publishes packages to PyPI with poetry build and poetry publish.

## uv

uv is a Rust-based pip and Poetry replacement that is 10-100x faster than pip. It supports pip-compatible commands (uv pip install) and Poetry-compatible project management (uv sync, uv add). uv resolves dependencies in milliseconds.

uv's speed advantage comes from Rust implementation, aggressive caching, and parallel downloads. It supports Python version management (uv python install) and works in CI where installation speed matters. uv is production-ready for most workflows.

## Conda

Conda is a cross-platform package manager for Python and non-Python dependencies. It excels at scientific computing where native library dependencies (NumPy, SciPy, PyTorch) are complex. Conda channels (conda-forge, defaults) provide pre-compiled binaries.

Miniconda is the minimal installer. Mamba is a faster Conda alternative with the same commands. Conda-lock provides reproducible environments. Conda environments are heavy—each environment is a full directory of packages.

## Recommendation

Use pip for simple projects and containers. Use Poetry for library development and projects needing deterministic resolution. Use uv for speed-sensitive workflows and CI. Use Conda for data science and machine learning projects with complex native dependencies.

**See also:** [Artifact Management](</en/tech/artifact-management.html>), [Dependency Management](</en/tech/dependency-management.html>), [Python Performance Optimization](</en/tech/python-performance.html>).

**See also:** [Rust vs Go: A Practical Comparison](</en/tech/rust-vs-go-practical.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>)

**See also:** [Rust vs Go: A Practical Comparison](</en/tech/rust-vs-go-practical.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>)

**See also:** [Rust vs Go: A Practical Comparison](</en/tech/rust-vs-go-practical.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>)

**See also:** [Rust vs Go: A Practical Comparison](</en/tech/rust-vs-go-practical.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>)

**See also:** [Rust vs Go: A Practical Comparison](</en/tech/rust-vs-go-practical.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>)

**See also:** [Git Workflows](</en/tech/git-workflows.html>), [Log Management](</en/tech/log-management.html>), [Python Performance Optimization](</en/tech/python-performance.html>)

**See also:** [Git Workflows](</en/tech/git-workflows.html>), [Log Management](</en/tech/log-management.html>), [Python Performance Optimization](</en/tech/python-performance.html>)

**See also:** [Git Workflows](</en/tech/git-workflows.html>), [Log Management](</en/tech/log-management.html>), [Python Performance Optimization](</en/tech/python-performance.html>)

**See also:** [Git Workflows](</en/tech/git-workflows.html>), [Log Management](</en/tech/log-management.html>), [Python Performance Optimization](</en/tech/python-performance.html>)

**See also:** [Git Workflows](</en/tech/git-workflows.html>), [Log Management](</en/tech/log-management.html>), [Python Performance Optimization](</en/tech/python-performance.html>)

**See also:** [Git Workflows](</en/tech/git-workflows.html>), [Log Management](</en/tech/log-management.html>), [Python Performance Optimization](</en/tech/python-performance.html>)

**See also:** [Git Workflows](</en/tech/git-workflows.html>), [Log Management](</en/tech/log-management.html>), [Python Performance Optimization](</en/tech/python-performance.html>)

**See also:** [Git Workflows](</en/tech/git-workflows.html>), [Log Management](</en/tech/log-management.html>), [Python Performance Optimization](</en/tech/python-performance.html>)

**See also:** [Git Workflows](</en/tech/git-workflows.html>), [Log Management](</en/tech/log-management.html>), [Python Performance Optimization](</en/tech/python-performance.html>)
