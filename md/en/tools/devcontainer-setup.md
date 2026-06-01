---
title: "Dev Containers: devcontainer.json, Features, Dotfiles, and GitHub Codespaces"
description: "Technical guide to development containers covering devcontainer.json configuration, features, dotfiles integration, remote development workflows, and GitHub Codespaces."
date: 2026-01-29
board: tools
url: https://aidev.fit/en/tools/devcontainer-setup.html
---

# Dev Containers: devcontainer.json, Features, Dotfiles, and GitHub Codespaces

## Introduction

Development containers (dev containers) provide consistent, reproducible development environments defined as code. Instead of developers manually installing language runtimes, databases, and tools on their local machines, dev containers package the entire development environment into a Docker container. This eliminates "works on my machine" problems, reduces onboarding time from days to minutes, and ensures consistency across team environments.

This article covers devcontainer.json configuration, features, dotfiles integration, remote development workflows, and GitHub Codespaces.

## Dev Container Specification

The dev container specification, maintained by the Community Specification Contributor Agreement, defines a standard format for configuring development containers. The primary configuration file is `.devcontainer/devcontainer.json` at the repository root.

{

"name": "Node.js & PostgreSQL",

"image": "mcr.microsoft.com/devcontainers/javascript-node:20",

"forwardPorts": [3000, 5432],

"postCreateCommand": "npm install",

"customizations": {

"vscode": {

"extensions": [

"dbaeumer.vscode-eslint",

"esbenp.prettier-vscode",

"ms-vscode.vscode-typescript-next"

],

"settings": {

"editor.formatOnSave": true

}

}

}

}

The `image` property specifies the base container image. Alternatively, `build` references a Dockerfile for custom images. The Dockerfile approach provides complete control over the environment but requires more maintenance.

## Base Images and Features

Microsoft maintains a library of pre-built dev container base images: `javascript-node`, `python`, `go`, `rust`, `java`, `dotnet`, and more. These images include the runtime, common development tools (git, curl, zsh, Oh My Zsh), and non-root user configuration.

Features are self-contained, shareable units of configuration that install additional tools into a dev container. The features repository includes CLI tools (Azure CLI, AWS CLI, Docker-in-Docker), language runtimes (Ruby, PHP, Elixir), and databases (PostgreSQL, SQLite, Redis).

{

"image": "mcr.microsoft.com/devcontainers/base:ubuntu",

"features": {

"ghcr.io/devcontainers/features/node:1": {

"version": "20"

},

"ghcr.io/devcontainers/features/docker-in-docker:2": {},

"ghcr.io/devcontainers/features/aws-cli:1": {}

}

}

Features are versioned and published as OCI artifacts. The community contributes features to the shared registry, providing a growing catalog of ready-to-use environment components.

## Dotfiles Integration

Dotfiles — configuration files for shell, editors, and tools — can be automatically applied when creating a dev container. The devcontainer.json specifies a dotfiles repository:

{

"dotfilesRepository": "github.com/username/dotfiles",

"dotfilesInstallCommand": "./install.sh",

"dotfilesTargetPath": "~/dotfiles"

}

The dotfiles repository typically contains shell configuration (.zshrc, .bashrc), git configuration (.gitconfig), editor settings, and tool configuration. The install script links or copies files to the appropriate locations inside the container.

This feature enables personalized development environments within the standardized container, balancing consistency with individual preferences.

## Remote Development Workflows

Dev containers support four connection modes:

Docker (local): The container runs on the local Docker daemon. VS Code's Remote - Containers extension attaches to the container. This is the simplest mode for individual development.

Docker (remote SSH): The container runs on a remote Docker host accessed via SSH. Useful for development on powerful remote machines without transferring local setup.

Dev Tunnel: VS Code tunnels through firewalls to connect to a dev container on any machine. Enabled by the `devcontainer up` CLI command.

Codespaces: GitHub managed remote dev containers in the cloud.

## Build and open a dev container

devcontainer open .

## Rebuild from scratch

devcontainer build --workspace-folder . --image-name my-devcontainer

## GitHub Codespaces

GitHub Codespaces provides cloud-hosted dev containers integrated directly with GitHub repositories. When `devcontainer.json` exists in a repository, Codespaces automatically provisions a container with the specified configuration.

Codespaces supports:

  * Prebuilds: Pre-build containers on push to reduce startup time.

  * Multi-machine configuration: Different container specs for different branches or PRs.

  * Core hours billing: Consumption-based pricing for compute resources.

  * VS Code and browser-based editors.

{

"image": "mcr.microsoft.com/devcontainers/universal:2",

"hostRequirements": {

"cpus": 4,

"memory": "8gb",

"storage": "32gb"

},

"forwardPorts": [8080],

"portsAttributes": {

"8080": {

"label": "Application",

"onAutoForward": "notify"

}

}

}

Prebuilds significantly improve the Codespaces experience. A GitHub Actions workflow builds the container on each push, caching layers for instant startup. Without prebuilds, Codespaces builds the container on first launch, which can take several minutes.

## Best Practices

Keep devcontainer.json in the repository root for broadest tool compatibility. Pin feature versions for reproducibility. Use postCreateCommand for setup scripts, not for tools that should be permanently installed. Configure lifecycle hooks for different timing phases:

  * `onCreateCommand`: Runs when container is first created.

  * `updateContentCommand`: Runs when source code changes.

  * `postCreateCommand`: Runs after container creation completes.

  * `postStartCommand`: Runs each time container starts.

Minimize image size by using specific base images rather than the universal image unless diverse tooling is needed. Test dev container configuration in CI to catch configuration drift.

## Conclusion

Dev containers transform development environment management. devcontainer.json defines environments as code. Features provide composable tool installation. Dotfiles integration preserves personal preferences. Remote development workflows support diverse connectivity modes. GitHub Codespaces extends the model to cloud-hosted environments. Organizations adopting dev containers reduce onboarding friction, eliminate environment inconsistencies, and enable developers to contribute to any repository with zero local configuration.
