---
title: "CSS Grid and Flexbox: Modern Layout Guide"
description: "Master CSS Grid and Flexbox for responsive layouts, component design, and complex page structures."
date: 2026-01-13
board: tech
url: https://aidev.fit/en/tech/css-grid-flexbox.html
---

# CSS Grid and Flexbox: Modern Layout Guide

CSS Grid and Flexbox are the two modern layout systems that replaced float-based layouts. They work best when used together—Grid for page-level layout, Flexbox for component-level alignment.

## Flexbox

Flexbox distributes space along a single axis (row or column). Use display: flex on the container and flex properties on children. Main axis properties (justify-content) control distribution. Cross axis properties (align-items) control alignment.

Flexbox excels at one-dimensional layouts: navigation bars, card rows, centered content, and form layouts. The flex property (flex-grow, flex-shrink, flex-basis) controls how items grow and shrink. gap property adds spacing without margin hacks. Order property rearranges visual order without changing HTML.

## CSS Grid

Grid creates two-dimensional layouts with rows and columns. Define the grid with grid-template-columns and grid-template-rows. Place items with grid-column and grid-row or using named grid areas.

Grid excels at page layouts and component layouts requiring two-dimensional alignment. The fr unit distributes available space proportionally. minmax() creates responsive tracks. auto-fill and auto-fit create responsive layouts without media queries. Grid areas (grid-template-areas) provide visual mapping of layout regions.

## Responsive Design

Both Grid and Flexbox are inherently responsive. Flexbox wraps items with flex-wrap. Grid adjusts tracks with auto-fill/auto-fit and minmax(). Combine with media queries for breakpoint-specific layouts.

Use clamp() for fluid typography and spacing: clamp(1rem, 2.5vw, 2rem). Container queries (@container) enable component-level responsiveness independent of the viewport. Subgrid passes grid tracks to nested grids for aligned layouts.

## Common Patterns

Holy grail layout: Grid for header, footer, main content, and sidebars. Card grid: Grid with auto-fill for responsive card columns. Centered content: Flexbox with justify-content and align-items center. Sticky footer: Flexbox with min-height: 100vh and margin-top: auto on footer. Equal height columns: Grid automatically creates equal height rows.

**See also:** [CI/CD Best Practices](</en/tech/ci-cd-best-practices.html>), [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Advanced Git Techniques for Developers](</en/tech/git-advanced-techniques.html>).

**See also:** [Advanced Git Techniques for Developers](</en/tech/git-advanced-techniques.html>), [AWS VPC Design: Subnets, NAT, Peering, Transit Gateway, and Security Groups](</en/tech/aws-vpc-design.html>), [Docker Networking: Bridge, Overlay, Host, Macvlan, and Troubleshooting](</en/tech/docker-networking.html>)

**See also:** [Advanced Git Techniques for Developers](</en/tech/git-advanced-techniques.html>), [AWS VPC Design: Subnets, NAT, Peering, Transit Gateway, and Security Groups](</en/tech/aws-vpc-design.html>), [Docker Networking: Bridge, Overlay, Host, Macvlan, and Troubleshooting](</en/tech/docker-networking.html>)

**See also:** [Advanced Git Techniques for Developers](</en/tech/git-advanced-techniques.html>), [AWS VPC Design: Subnets, NAT, Peering, Transit Gateway, and Security Groups](</en/tech/aws-vpc-design.html>), [Docker Networking: Bridge, Overlay, Host, Macvlan, and Troubleshooting](</en/tech/docker-networking.html>)

**See also:** [Advanced Git Techniques for Developers](</en/tech/git-advanced-techniques.html>), [AWS VPC Design: Subnets, NAT, Peering, Transit Gateway, and Security Groups](</en/tech/aws-vpc-design.html>), [Docker Networking: Bridge, Overlay, Host, Macvlan, and Troubleshooting](</en/tech/docker-networking.html>)

**See also:** [Advanced Git Techniques for Developers](</en/tech/git-advanced-techniques.html>), [AWS VPC Design: Subnets, NAT, Peering, Transit Gateway, and Security Groups](</en/tech/aws-vpc-design.html>), [Docker Networking: Bridge, Overlay, Host, Macvlan, and Troubleshooting](</en/tech/docker-networking.html>)

**See also:** [Configuration Management](</en/tech/configuration-management.html>), [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Webpack vs Vite](</en/tech/webpack-vs-vite.html>)

**See also:** [Configuration Management](</en/tech/configuration-management.html>), [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Webpack vs Vite](</en/tech/webpack-vs-vite.html>)

**See also:** [Configuration Management](</en/tech/configuration-management.html>), [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Webpack vs Vite](</en/tech/webpack-vs-vite.html>)

**See also:** [Configuration Management](</en/tech/configuration-management.html>), [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Webpack vs Vite](</en/tech/webpack-vs-vite.html>)

**See also:** [Configuration Management](</en/tech/configuration-management.html>), [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Webpack vs Vite](</en/tech/webpack-vs-vite.html>)

**See also:** [Configuration Management](</en/tech/configuration-management.html>), [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Webpack vs Vite](</en/tech/webpack-vs-vite.html>)

**See also:** [Configuration Management](</en/tech/configuration-management.html>), [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Webpack vs Vite](</en/tech/webpack-vs-vite.html>)

**See also:** [Configuration Management](</en/tech/configuration-management.html>), [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Webpack vs Vite](</en/tech/webpack-vs-vite.html>)

**See also:** [Configuration Management](</en/tech/configuration-management.html>), [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Webpack vs Vite](</en/tech/webpack-vs-vite.html>)

**See also:** [Configuration Management](</en/tech/configuration-management.html>), [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Webpack vs Vite](</en/tech/webpack-vs-vite.html>)

**See also:** [Configuration Management](</en/tech/configuration-management.html>), [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Webpack vs Vite](</en/tech/webpack-vs-vite.html>)

**See also:** [Configuration Management](</en/tech/configuration-management.html>), [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Webpack vs Vite](</en/tech/webpack-vs-vite.html>)

**See also:** [Configuration Management](</en/tech/configuration-management.html>), [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Webpack vs Vite](</en/tech/webpack-vs-vite.html>)

**See also:** [Configuration Management](</en/tech/configuration-management.html>), [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Webpack vs Vite](</en/tech/webpack-vs-vite.html>)

**See also:** [Configuration Management](</en/tech/configuration-management.html>), [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Webpack vs Vite](</en/tech/webpack-vs-vite.html>)

**See also:** [Configuration Management](</en/tech/configuration-management.html>), [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Webpack vs Vite](</en/tech/webpack-vs-vite.html>)

**See also:** [Configuration Management](</en/tech/configuration-management.html>), [Infrastructure Composability](</en/tech/infrastructure-composability.html>), [Webpack vs Vite](</en/tech/webpack-vs-vite.html>)
