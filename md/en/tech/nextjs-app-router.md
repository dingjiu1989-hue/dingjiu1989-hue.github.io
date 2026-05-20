---
title: "Next.js App Router"
description: "Explore Next.js App Router: server components, layouts, loading states, error boundaries, and routing architecture"
date: 2026-01-09
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/nextjs-app-router.html
---

# Next.js App Router

Next.js App Router represents a fundamental shift in how React applications are structured. Introduced in Next.js 13 and refined through subsequent releases, the App Router replaces the Pages Router with a new paradigm built on React Server Components, nested layouts, and file-based routing conventions. This article explores the architecture, patterns, and best practices for the App Router.

## File-Based Routing

The App Router uses a file-system based routing where folders define routes and files define UI components. A `page.tsx` file defines the UI for a route segment. A `layout.tsx` file defines a layout that wraps child routes. This convention creates a clear, predictable project structure.

Special files provide route-level configuration. `loading.tsx` defines loading UI shown during page transitions. `error.tsx` defines error UI for that segment. `not-found.tsx` handles 404 cases. These files automatically create boundaries for loading states, error handling, and fallback UI without additional routing configuration.

## React Server Components

The App Router defaults to React Server Components. Server components render on the server and send only the static HTML to the client. They can directly access databases, file systems, and backend services without exposing them to the client. This eliminates the need for API routes when rendering initial page data.

Server components reduce the JavaScript bundle size because their code never reaches the browser. Libraries for date formatting, markdown parsing, or data access are executed only on the server. The client receives only the rendered output, resulting in smaller bundles and faster page loads.

## Client Components

When you need interactivity, event handlers, state, or browser APIs, you mark a component with `'use client'`. Client components are hydrated on the browser and behave like traditional React components. The boundary between server and client components is explicit—you choose which parts of your UI need interactivity.

Best practice is to push client boundaries as far down the tree as possible. Keep most of your page as server components and only make the interactive parts client components. This minimizes the JavaScript shipped to the browser and maximizes the benefits of server rendering.

## Layouts and Templates

Layouts are UI components that persist across route transitions. A `layout.tsx` file wraps all child routes. When users navigate between pages within the same layout, the layout does not re-render. This makes layouts ideal for navigation bars, sidebars, and persistent UI elements.

Templates are similar to layouts but re-mount on each navigation. They are useful for UI that should reset state on navigation, such as page-level animations or analytics tracking. Templates are defined with `template.tsx` files.

## Loading and Error Boundaries

The App Router automatically creates loading boundaries from `loading.tsx` files. These files define fallback UI shown while the page data loads. Next.js uses streaming Suspense to progressively render page content as data becomes available. The result is a fast initial page load with progressive enhancement as data arrives.

Error boundaries from `error.tsx` files catch errors in the component tree and display fallback UI without breaking the entire page. Error boundaries are scoped to their route segment—an error in one section does not crash other parts of the page.

## Data Fetching Patterns

Server components can directly `await` data fetching functions. Next.js extends the native `fetch` API with automatic caching and revalidation. `fetch(url, { next: { revalidate: 60 } })` caches the response for 60 seconds. `fetch(url, { cache: 'no-store' })` always fetches fresh data.

Parallel data fetching with `Promise.all` reduces load times by fetching independent data simultaneously. Sequential fetching is appropriate when one fetch depends on another's result. The App Router also supports streaming, where the page progressively renders as each piece of data arrives.

The App Router represents the future of React development at scale. Its combination of server components, streaming, and nested routes enables faster, more efficient applications with better developer experience.

**See also:** [React Server Components](</en/tech/react-server-components.html>), [Error Handling Patterns](</en/tech/error-handling-patterns.html>), [Build Optimization](</en/tech/build-optimization.html>).

**See also:** [React Server Components](</en/tech/react-server-components.html>), [Error Handling Patterns](</en/tech/error-handling-patterns.html>), [AWS VPC Design: Subnets, NAT, Peering, Transit Gateway, and Security Groups](</en/tech/aws-vpc-design.html>)

**See also:** [React Server Components](</en/tech/react-server-components.html>), [Error Handling Patterns](</en/tech/error-handling-patterns.html>), [AWS VPC Design: Subnets, NAT, Peering, Transit Gateway, and Security Groups](</en/tech/aws-vpc-design.html>)

**See also:** [React Server Components](</en/tech/react-server-components.html>), [Error Handling Patterns](</en/tech/error-handling-patterns.html>), [AWS VPC Design: Subnets, NAT, Peering, Transit Gateway, and Security Groups](</en/tech/aws-vpc-design.html>)

**See also:** [React Server Components](</en/tech/react-server-components.html>), [Error Handling Patterns](</en/tech/error-handling-patterns.html>), [AWS VPC Design: Subnets, NAT, Peering, Transit Gateway, and Security Groups](</en/tech/aws-vpc-design.html>)

**See also:** [React Server Components](</en/tech/react-server-components.html>), [Error Handling Patterns](</en/tech/error-handling-patterns.html>), [AWS VPC Design: Subnets, NAT, Peering, Transit Gateway, and Security Groups](</en/tech/aws-vpc-design.html>)

**See also:** [SLI/SLO/Error Budgets: Defining SLIs, Setting SLOs, and Burn Rate Alerts](</en/tech/sli-slo-error-budget.html>), [Build Optimization](</en/tech/build-optimization.html>), [Developer Portal](</en/tech/developer-portal.html>)

**See also:** [SLI/SLO/Error Budgets: Defining SLIs, Setting SLOs, and Burn Rate Alerts](</en/tech/sli-slo-error-budget.html>), [Build Optimization](</en/tech/build-optimization.html>), [Developer Portal](</en/tech/developer-portal.html>)

**See also:** [SLI/SLO/Error Budgets: Defining SLIs, Setting SLOs, and Burn Rate Alerts](</en/tech/sli-slo-error-budget.html>), [Build Optimization](</en/tech/build-optimization.html>), [Developer Portal](</en/tech/developer-portal.html>)

**See also:** [SLI/SLO/Error Budgets: Defining SLIs, Setting SLOs, and Burn Rate Alerts](</en/tech/sli-slo-error-budget.html>), [Build Optimization](</en/tech/build-optimization.html>), [Developer Portal](</en/tech/developer-portal.html>)

**See also:** [SLI/SLO/Error Budgets: Defining SLIs, Setting SLOs, and Burn Rate Alerts](</en/tech/sli-slo-error-budget.html>), [Build Optimization](</en/tech/build-optimization.html>), [Developer Portal](</en/tech/developer-portal.html>)

**See also:** [SLI/SLO/Error Budgets: Defining SLIs, Setting SLOs, and Burn Rate Alerts](</en/tech/sli-slo-error-budget.html>), [Build Optimization](</en/tech/build-optimization.html>), [Developer Portal](</en/tech/developer-portal.html>)

**See also:** [SLI/SLO/Error Budgets: Defining SLIs, Setting SLOs, and Burn Rate Alerts](</en/tech/sli-slo-error-budget.html>), [Build Optimization](</en/tech/build-optimization.html>), [Developer Portal](</en/tech/developer-portal.html>)

**See also:** [SLI/SLO/Error Budgets: Defining SLIs, Setting SLOs, and Burn Rate Alerts](</en/tech/sli-slo-error-budget.html>), [Build Optimization](</en/tech/build-optimization.html>), [Developer Portal](</en/tech/developer-portal.html>)

**See also:** [SLI/SLO/Error Budgets: Defining SLIs, Setting SLOs, and Burn Rate Alerts](</en/tech/sli-slo-error-budget.html>), [Build Optimization](</en/tech/build-optimization.html>), [Developer Portal](</en/tech/developer-portal.html>)
