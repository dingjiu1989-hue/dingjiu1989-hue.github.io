---
title: "Developer Environment Setup Guide"
description: "Comprehensive guide to setting up a productive developer environment with tools, configuration, and automation."
date: 2025-12-02
board: tech
url: https://aidev.fit/en/tech/dev-environment-setup.html
---

# Developer Environment Setup Guide

A well-configured developer environment is the foundation of productivity. Investing time in setting up your shell, editor, and tooling pays dividends every single day. This guide covers a complete development environment setup that works across platforms.

## Operating System Choice

Choose an operating system that supports the tools you need:

  * **macOS** : Excellent developer experience, Unix-based terminal, Homebrew package manager. Preferred for iOS/macOS development.

  * **Linux (Ubuntu/Debian/Fedora)** : Native Docker performance, full control over the system. Preferred for server-side and Linux-targeted development.

  * **Windows with WSL2** : Windows Subsystem for Linux 2 provides a Linux kernel inside Windows. Run Linux tools natively while using Windows applications.




For most developers, macOS or WSL2 on Windows provides the best balance of tooling and usability.

## Shell Configuration

Modern shells improve daily productivity. Zsh with Oh My Zsh is the standard:

## Install Zsh and Oh My Zsh

sudo apt install zsh -y

sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

Essential Zsh plugins:

## ~/.zshrc

plugins=(

git

docker

docker-compose

npm

node

history

colored-man-pages

zsh-autosuggestions

zsh-syntax-highlighting

command-not-found

)

For power users, consider Fish shell for autosuggestions out of the box, or Nushell for structured data pipelines.

## Git Configuration

Set up a robust Git configuration:

git config --global user.name "Your Name"

git config --global user.email "your@email.com"

git config --global init.defaultBranch main

git config --global pull.rebase true

git config --global fetch.prune true

git config --global diff.colorMoved zebra

git config --global alias.co checkout

git config --global alias.br branch

git config --global alias.ci commit

git config --global alias.st status

git config --global alias.lg "log --oneline --graph --decorate --all"

git config --global core.excludesfile ~/.gitignore_global

A global `.gitignore` prevents committing common OS and editor files:

## ~/.gitignore_global

.DS_Store

Thumbs.db

*.swp

*.swo

*~

.vscode/

.idea/

*.log

.env.local

## Package Managers

Install language-specific package managers:

## Node.js (via nvm for version management)

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash

nvm install --lts

nvm use --lts

## Python

sudo apt install python3 python3-pip python3-venv

## Rust

curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

## Go

wget https://go.dev/dl/go1.22.linux-amd64.tar.gz

sudo tar -C /usr/local -xzf go1.22.linux-amd64.tar.gz

Use version managers (`nvm`, `pyenv`, `rbenv`, `sdkman`) to manage multiple language versions.

## Editor Setup

VS Code is the most popular editor for good reason. Essential extensions:

## Install via CLI

code --install-extension ms-python.python

code --install-extension dbaeumer.vscode-eslint

code --install-extension esbenp.prettier-vscode

code --install-extension github.copilot

code --install-extension bierner.markdown-mermaid

code --install-extension eamodio.gitlens

code --install-extension ms-azuretools.vscode-docker

code --install-extension streetsidesoftware.code-spell-checker

Settings to consider:

{

"editor.formatOnSave": true,

"editor.defaultFormatter": "esbenp.prettier-vscode",

"editor.minimap.enabled": false,

"editor.fontSize": 14,

"editor.fontFamily": "'JetBrains Mono', 'Fira Code', monospace",

"editor.fontLigatures": true,

"editor.cursorBlinking": "smooth",

"files.autoSave": "onFocusChange",

"workbench.colorTheme": "One Dark Pro",

"terminal.integrated.fontFamily": "JetBrains Mono",

"git.autofetch": true

}

## Docker Setup

Docker is essential for local development consistency:

## Ubuntu

sudo apt install docker.io docker-compose-v2

sudo usermod -aG docker $USER # Log out and back in

## macOS

brew install --cask docker

Create a development Docker Compose file for your project's dependencies:

## dev-dependencies.yml

services:

postgres:

image: postgres:16-alpine

ports: ["5432:5432"]

environment:

POSTGRES_DB: myapp_dev

POSTGRES_PASSWORD: devpassword

volumes:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- pgdata:/var/lib/postgresql/data

redis:

image: redis:7-alpine

ports: ["6379:6379"]

volumes:

pgdata:

## Local HTTPS with mkcert

Test HTTPS locally:

brew install mkcert # or sudo apt install mkcert

mkcert -install

mkcert localhost 127.0.0.1 ::1

This creates locally trusted TLS certificates for development.

## Dotfiles Management

Store your configuration in a Git repository:

git init --bare $HOME/.dotfiles

alias config='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'

config remote add origin https://github.com/you/dotfiles.git

config add ~/.zshrc ~/.gitconfig ~/.vimrc

config commit -m "Initial dotfiles"

config push

Restore on a new machine:

git clone --bare https://github.com/you/dotfiles.git $HOME/.dotfiles

alias config='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'

config checkout

## Containerized Development with Dev Containers

VS Code Dev Containers package the entire development environment:

// .devcontainer/devcontainer.json

{

"name": "My Project",

"image": "mcr.microsoft.com/devcontainers/typescript-node:22",

"features": {

"ghcr.io/devcontainers/features/docker-in-docker:2": {}

},

"postCreateCommand": "npm install",

"forwardPorts": [3000],

"customizations": {

"vscode": {

"extensions": ["dbaeumer.vscode-eslint"]

}

}

}

Every developer gets identical tools regardless of their host OS.

## Summary

A productive developer environment is personal, but some investments benefit everyone: a modern shell with autosuggestions, a well-configured editor with formatting on save, Docker for reproducible dependencies, and dotfiles versioned in Git. The initial setup takes an afternoon, but the time saved over a career is immense. Start with the basics -- shell, Git, editor, and Docker -- then add specialized tools as your workflow requires them.
