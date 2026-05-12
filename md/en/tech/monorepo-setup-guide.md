---
title: "Monorepo Setup Guide: Turborepo + pnpm + TypeScript in 30 Minutes"
description: "Set up a production-ready monorepo with shared packages, TypeScript configs, and parallel builds. Step-by-step from scratch with Turborepo best practices."
date: 2026-05-08
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/monorepo-setup-guide.html
---

# Monorepo Setup Guide: Turborepo + pnpm + TypeScript in 30 Minutes

A monorepo lets you share code between apps (web, mobile, docs) and packages (shared utils, configs, UI components) in a single repository. Turborepo + pnpm + TypeScript is the modern stack. Here's how to set it up in 30 minutes.

## Why a Monorepo?

Problem| Monorepo Solution  
---|---  
Duplicate tsconfig, ESLint config, etc. in 5 repos| One shared config package. Update once, all apps get it.  
Copy-pasting UI components between apps| Shared UI package. One component, used everywhere.  
Can't refactor across apps safely| TypeScript validates ALL consumers when you change a shared package.  
CI runs unrelated changes on every commit| Turborepo caches tasks. Only changed packages rebuild.  

## Step-by-Step Setup

    # 1. Create the monorepo structure
    mkdir my-monorepo && cd my-monorepo
    pnpm init

    # 2. Create pnpm-workspace.yaml
    cat > pnpm-workspace.yaml << 'EOF'
    packages:
      - "apps/*"
      - "packages/*"
    EOF

    # 3. Create directory structure
    mkdir -p apps/web apps/docs packages/ui packages/config

    # 4. Create root package.json with Turborepo
    cat > package.json << 'EOF'
    {
      "private": true,
      "scripts": {
        "dev": "turbo dev",
        "build": "turbo build",
        "lint": "turbo lint",
        "test": "turbo test"
      },
      "devDependencies": {
        "turbo": "^2.0.0",
        "typescript": "^5.5.0"
      }
    }
    EOF

    # 5. Install Turborepo
    pnpm install

    # 6. Create turbo.json
    cat > turbo.json << 'EOF'
    {
      "$schema": "https://turbo.build/schema.json",
      "tasks": {
        "build": {
          "dependsOn": ["^build"],
          "outputs": [".next/**", "dist/**"]
        },
        "dev": { "cache": false, "persistent": true },
        "lint": { "dependsOn": ["^build"] },
        "test": { "dependsOn": ["^build"] }
      }
    }
    EOF

## Shared Config Package

    # packages/config/package.json
    {
      "name": "@repo/config",
      "version": "0.0.0",
      "private": true,
      "exports": {
        "./typescript": "./tsconfig.base.json",
        "./eslint": "./eslint.base.js"
      }
    }

    # packages/config/tsconfig.base.json
    {
      "compilerOptions": {
        "target": "ES2022",
        "module": "ESNext",
        "moduleResolution": "bundler",
        "strict": true,
        "esModuleInterop": true,
        "skipLibCheck": true,
        "forceConsistentCasingInFileNames": true
      }
    }

## App Configuration

    # apps/web/tsconfig.json — each app extends the shared base
    {
      "extends": "@repo/config/typescript",
      "compilerOptions": {
        "baseUrl": ".",
        "paths": {
          "@/*": ["./src/*"],
          "@repo/ui/*": ["../../packages/ui/src/*"]
        }
      },
      "include": ["src", "next-env.d.ts"]
    }

## Best Practices

  * **One package = one purpose.** @repo/ui for components, @repo/config for shared configs, @repo/utils for shared utilities. Don't create a "misc" package.
  * **Use workspace protocol:** In package.json dependencies, use `"@repo/ui": "workspace:*"` instead of version numbers.
  * **Parallel builds:** Turborepo runs independent tasks in parallel. A build across 5 packages finishes in the time of the slowest one, not the sum.
  * **Remote caching:** Turborepo can cache builds remotely (Vercel). CI builds reuse cache from previous CI runs.
  * **Don't go monorepo for <3 packages.** The overhead isn't worth it for tiny projects. Start with a single repo, extract when you have sharing pain.

**Bottom line:** Monorepos shine when you have 3+ apps/packages that share code. pnpm workspaces + Turborepo is the best stack in 2026. The shared config package alone saves hours of boilerplate setup per new project. See also: [Package Manager Comparison](</en/compare/pnpm-vs-npm-vs-yarn.html>) and [Build Tools Comparison](</en/compare/vite-vs-webpack-vs-turbopack.html>).
