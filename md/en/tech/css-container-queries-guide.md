---
title: "CSS Container Queries Guide: Component-Based Responsive Design Without Media Queries"
description: "Complete guide to CSS container queries — syntax, real-world patterns, container query units, style queries, and when to still use media queries."
date: 2025-12-31
board: tech
url: https://aidev.fit/en/tech/css-container-queries-guide.html
---

# CSS Container Queries Guide: Component-Based Responsive Design Without Media Queries

## The Most Important CSS Feature Since Flexbox

For 15 years, responsive design relied on media queries — which only know the viewport size. Container queries let you style based on the size of a parent container. This is transformative for component-based architecture: a card component can adapt its layout based on whether it's in a wide main column or a narrow sidebar, without needing to know about the page layout. Supported in all modern browsers since 2023, container queries are production-ready and underused. Here's how to use them.

## Media Queries vs Container Queries

Media Queries (@media)| Container Queries (@container)  
---|---  
Queries the viewport width/height| Queries a parent container's width/height/inline-size  
Good for: page-level layout (header, sidebar, grid)| Good for: component-level adaptation (cards, forms, lists)  
Component must know about the page structure| Component is self-contained; works in any layout context  
Available since 2012 (IE9+)| Available since 2023 (all modern browsers, 95%+ support)  
  
## The Syntax
    
    
    /* 1. Define a containment context */
    .card-wrapper {
        container-type: inline-size;  /* enables container queries on this element */
        container-name: card;         /* optional: name for targeting specific containers */
    }
    
    /* 2. Query the container */
    @container card (min-width: 400px) {
        .card {
            display: grid;
            grid-template-columns: 200px 1fr;
            gap: 1rem;
        }
    }
    
    @container (max-width: 300px) {
        .card {
            display: block;
        }
        .card-image {
            width: 100%;
        }
    }

## Container Query Units

Unit| Relative To| Use Case  
---|---|---  
cqw| 1% of container width| Font size that scales with card width: font-size: clamp(0.9rem, 3cqw, 1.5rem)  
cqh| 1% of container height| Element height proportional to container  
cqi| 1% of container inline size| Logical property: 1% of width in LTR, height in vertical writing modes  
cqb| 1% of container block size| Logical property: 1% of height in LTR  
cqmin / cqmax| min/max of cqi and cqb| Ensure elements fit in either dimension  
  
## Real-World Patterns

**Pattern 1: Adaptive Card Layout.** The classic container query use case. A card displays vertically in a narrow container (sidebar) and horizontally in a wide container (main content). The card doesn't need to know where it is — it adapts to the space it's given.
    
    
    .card-container {
        container-type: inline-size;
    }
    
    @container (min-width: 350px) {
        .card {
            flex-direction: row;
            align-items: center;
        }
        .card-thumbnail {
            width: 120px;
            flex-shrink: 0;
        }
    }

**Pattern 2: Responsive Typography Inside Components.** Use cqw units to scale text proportionally within a card, so a card in a wide column has larger text than the same card in a narrow sidebar.
    
    
    .widget {
        container-type: inline-size;
    }
    .widget-title {
        font-size: clamp(1rem, 5cqi, 1.75rem);
    }
    .widget-body {
        font-size: clamp(0.875rem, 3cqi, 1.125rem);
    }

**Pattern 3: Grid Columns Based on Container Width.** Change the number of columns based on container width, not viewport width. A grid of items in a 600px sidebar shows 2 columns; the same grid in a 900px main area shows 3 columns.
    
    
    .grid-container {
        container-type: inline-size;
    }
    .grid {
        display: grid;
        grid-template-columns: repeat(1, 1fr);
    }
    @container (min-width: 400px) {
        .grid { grid-template-columns: repeat(2, 1fr); }
    }
    @container (min-width: 700px) {
        .grid { grid-template-columns: repeat(3, 1fr); }
    }

**Pattern 4: Container Queries + CSS Grid for Page Layouts.** Combine container queries with CSS Grid's auto-fit/minmax for truly responsive layouts without media queries. The grid places as many columns as fit; container queries handle the styling inside each grid cell.
    
    
    .page-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
    }
    .page-grid > * {
        container-type: inline-size; /* each grid cell is its own container */
    }

## Style Queries (The Next Frontier)

Beyond container size queries, CSS now supports style queries — querying CSS custom property values:
    
    
    @container style(--theme: dark) {
        .card {
            background: #1a1a2e;
            color: #e0e0e0;
        }
    }

Style queries are newer (Chrome 111+, Safari 18+, Firefox support in progress) but are the logical next step: components that adapt not just to size but to any inherited property or custom property. Combined with design tokens as CSS custom properties, this enables fully context-aware components.

## When to Still Use Media Queries

Container queries don't replace media queries — they complement them. Still use media queries for: overall page layout (header, navigation, footer), user preference queries (prefers-reduced-motion, prefers-color-scheme, prefers-contrast), and device characteristics (pointer: coarse for touch devices, resolution for high-DPI screens). The rule: media queries for page-level concerns, container queries for component-level concerns.

**Bottom line:** Container queries are the missing piece in component-based CSS. If you build with React, Vue, or Svelte components, start using container queries today — every major browser has supported them for over two years. The old approach of passing "variant" props (variant="compact" vs variant="wide") becomes unnecessary when the component can sense its own container width. See also: [CSS Responsive Design Guide](</en/tech/css-responsive-design-guide.html>) and [Tailwind vs Bootstrap vs MUI](</en/compare/tailwind-vs-bootstrap-vs-mui.html>).
