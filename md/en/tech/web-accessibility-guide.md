---
title: "Web Accessibility (a11y) Guide for Developers: WCAG 2.2 in Practice"
description: "Practical accessibility guide for developers: semantic HTML, ARIA labels (when and when not to use), keyboard navigation, screen reader testing, color contrast, and automated a11y testing in CI/CD."
date: 2026-05-08
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/web-accessibility-guide.html
---

# Web Accessibility (a11y) Guide for Developers: WCAG 2.2 in Practice

Web accessibility (a11y) is not just about compliance — accessible websites work better for everyone, including keyboard users, screen reader users, and people with temporary disabilities. The business case is strong: the EU Accessibility Act (2025) mandates accessibility for many digital products, and inaccessible websites lose an estimated 15-20% of potential users. This guide covers practical accessibility patterns that developers actually need.

## Accessibility Basics: The 4 Principles (POUR)

Principle| What It Means| Developer Checklist  
---|---|---  
Perceivable| Users can perceive the content| Alt text for images, captions for video, sufficient color contrast  
Operable| Users can operate the interface| Keyboard navigation, no keyboard traps, enough time to read  
Understandable| Users can understand the content| Readable text, predictable navigation, input assistance (error messages)  
Robust| Content works with assistive technologies| Semantic HTML, valid ARIA (when needed), works across browsers  
  
## Semantic HTML: Your Best Accessibility Tool

**The most important rule:** Use semantic HTML elements. They are accessible by default — no ARIA needed.

Instead of| Use| Why  
---|---|---  
`<div onclick="...">`| `<button>`| Buttons are focusable, keyboard-activatable, and announced as "button" by screen readers  
`<div class="nav">`| `<nav>`| Screen readers have a "skip to navigation" shortcut  
`<div class="main">`| `<main>`| Screen readers have a "skip to main content" shortcut  
`<span class="heading">`| `<h1>-<h6>`| Screen readers navigate by heading hierarchy  
`<div> + CSS grid`| `<table>` for tabular data| Screen readers have table navigation (row/column headers)  
  
## ARIA: When HTML Is Not Enough

**Critical rule:** No ARIA is better than bad ARIA. Only use ARIA when native HTML cannot express the semantics you need.

ARIA Attribute| When to Use| Example  
---|---|---  
aria-label| Provide an accessible name when no visible label exists| `<button aria-label="Close dialog">X</button>`  
aria-describedby| Link an element to its description| `<input aria-describedby="password-hint"> <span id="password-hint">Min 8 characters</span>`  
aria-expanded| Indicate if a collapsible element is open| `<button aria-expanded="true">Section 1</button>`  
aria-live| Announce dynamic content changes| `<div aria-live="polite">5 results found</div>`  
role="alert"| Important, time-sensitive notification| `<div role="alert">Your session will expire in 2 minutes</div>`  
  
## Automated Testing in CI/CD
    
    
    // axe-core: The accessibility testing standard
    // Integrate into Jest, Playwright, or Cypress tests
    import { axe, toHaveNoViolations } from 'jest-axe';
    expect.extend(toHaveNoViolations);
    
    it('homepage should have no accessibility violations', async () => {
      const { container } = render();
      const results = await axe(container);
      expect(results).toHaveNoViolations();
    });
    
    // Playwright test
    import { injectAxe, checkA11y } from 'axe-playwright';
    await injectAxe(page);
    await checkA11y(page); // Runs axe-core against the rendered page

**Bottom line:** Start with semantic HTML — it solves 80% of accessibility issues for free. Add automated a11y testing to CI/CD (axe-core) to catch regressions. Test manually with a keyboard (Tab through your entire app) at least once per feature. Accessibility is not a feature to add later — it is a property of good HTML. See also: [CSS Framework Comparison](</en/compare/tailwind-vs-bootstrap-vs-mui.html>) and [Responsive CSS in 2026](</en/tech/css-responsive-design-guide.html>).

**See also:** [Testing Strategies for Web Apps: Unit, Integration, E2E, and When to Use Each](</en/tech/testing-strategies-web-apps.html>), [Load Testing Guide 2026: k6 vs Artillery vs Locust vs wrk2 for Performance Testing](</en/tech/load-testing-guide.html>), [CSS Container Queries Guide: Component-Based Responsive Design Without Media Queries](</en/tech/css-container-queries-guide.html>)
