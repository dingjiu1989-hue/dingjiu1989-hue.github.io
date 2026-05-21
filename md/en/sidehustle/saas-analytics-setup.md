---
title: "SaaS Analytics Setup: PostHog, Plausible, and Umami"
description: "Set up SaaS analytics with self-hosted PostHog, Plausible, and Umami for product insights and user behavior tracking."
date: 2026-01-22
board: sidehustle
url: https://dingjiu1989-hue.github.io/en/sidehustle/saas-analytics-setup.html
---

# SaaS Analytics Setup: PostHog, Plausible, and Umami

## SaaS Analytics Setup: Privacy-Focused Tools

Analytics are essential for SaaS decision-making, but traditional tools like Google Analytics are increasingly problematic — slow, privacy-invasive, and providing limited product insights. Modern privacy-focused alternatives offer better performance, data ownership, and actionable product metrics.

## PostHog: Product Analytics Platform

PostHog is the most comprehensive open-source product analytics platform. It provides event tracking, session recording, feature flags, heatmaps, and experimentation tools in a single platform. Self-hosted on your infrastructure or use PostHog Cloud.

**Event tracking** captures user actions: page views, button clicks, feature usage, and custom events. Instrument PostHog with their JavaScript snippet or SDK (Python, Node.js, React, iOS, Android). Events include automatic properties (browser, OS, device) and custom properties you define.

**Session recording** captures real user sessions as video replays. This reveals usability issues impossible to detect in aggregate metrics — dead clicks, rage clicks, confusing navigation, and form abandonment. PostHog's session recording is self-hosted, keeping sensitive data on your infrastructure.

**Feature flags** enable gradual rollouts and A/B testing without additional tools. Target flags by user properties (beta users, enterprise customers, geographic regions) or random percentage. Full-stack experimentation measures the impact of feature changes on conversion metrics.

Pricing: self-hosted is free (unlimited events, users, and team members). PostHog Cloud has a generous free tier (1 million events/month, 5,000 session recordings). Paid plans start at $399/month for additional capabilities.

## Plausible: Lightweight Web Analytics

Plausible is a lightweight, privacy-first web analytics tool. It provides essential metrics (page views, visitors, bounce rate, visit duration) in a clean dashboard. Plausible does not use cookies or collect personal data, making it GDPR-compliant by default.

Installation is simple: add a JavaScript snippet or use the proxy integration for WordPress/Cloudflare. The dashboard loads instantly — no waiting for data aggregation. Break down metrics by source, browser, OS, country, and device.

**Goals and funnels** track conversions. Define goals (signup completions, newsletter subscriptions, purchase events) and see how visitors convert across sources. Funnel analysis reveals drop-off points in multi-step flows.

Plausible Cloud starts at $9/month for 10,000 monthly page views. Self-hosted (Docker) is free but requires infrastructure management. For early-stage SaaS, Plausible's simplicity is an advantage over more complex tools.

## Umami: Self-Hosted Alternative

Umami is a simple, fast, self-hosted analytics alternative. Deploy via Docker on a $5/month VPS. Umami tracks page views, visitors, events, and custom data without cookies or personal data collection.

Key features: real-time analytics, website tracking (unlimited sites), custom events, UTM tracking, and shareable dashboards. Umami's data is stored in your own MySQL or PostgreSQL database, providing full data ownership.

The interface is clean and fast. Umami provides the essential metrics without complexity. It integrates with Vercel (one-click deploy) or any Docker-compatible platform. Umami is completely free and open source.

## Choosing the Right Tool

Use PostHog when you need deep product analytics: event tracking across user journeys, session recordings for UX research, feature flags, and experimentation. PostHog replaces multiple tools (Google Analytics, Hotjar, LaunchDarkly, Optimizely) in one platform.

Use Plausible for simple, privacy-compliant web analytics. Plausible is sufficient for content sites, landing pages, and early-stage SaaS where page views and basic conversion tracking are sufficient.

Use Umami when you want full data ownership with a self-hosted solution and minimal maintenance. Umami bridges the gap between Plausible's simplicity and PostHog's complexity.

## Implementation Guide

Set up tracking infrastructure in three phases. Phase 1: deploy your analytics tool and instrument basic page views. Phase 2: add custom event tracking for key actions (signup, feature usage, upgrade). Phase 3: set up dashboards for the metrics that matter: activation rate, retention, and revenue.

Use a data layer to separate analytics instrumentation from your application code. A single `analytics.track(event, properties)` function routes events to all configured providers. This prevents vendor lock-in and simplifies adding new analytics tools.

## Conclusion

Privacy-focused analytics tools provide better performance, data ownership, and actionable insights than traditional analytics. PostHog serves comprehensive product analytics needs, Plausible provides lightweight web analytics, and Umami offers simple self-hosted analytics. Choose based on your data needs, privacy requirements, and infrastructure preferences.

**See also:** [SaaS Analytics: Mixpanel, Amplitude, PostHog, Event Tracking, and Funnel Analysis](</en/sidehustle/saas-analytics.html>), [Product-Led Growth: Freemium, Free Trials, Self-Serve, and Usage-Based Pricing](</en/sidehustle/product-led-growth.html>), [Indie Hacker Tool Stack: Hosting, Analytics, Email, Payments, and Monitoring](</en/sidehustle/indie-hackers-tools.html>).

**See also:** [SaaS Analytics: Mixpanel, Amplitude, PostHog, Event Tracking, and Funnel Analysis](</en/sidehustle/saas-analytics.html>), [Product-Led Growth: Freemium, Free Trials, Self-Serve, and Usage-Based Pricing](</en/sidehustle/product-led-growth.html>), [SaaS Churn Reduction: Retention Strategies for Growth](</en/sidehustle/churn-reduction.html>)

**See also:** [SaaS Analytics: Mixpanel, Amplitude, PostHog, Event Tracking, and Funnel Analysis](</en/sidehustle/saas-analytics.html>), [Product-Led Growth: Freemium, Free Trials, Self-Serve, and Usage-Based Pricing](</en/sidehustle/product-led-growth.html>), [SaaS Churn Reduction: Retention Strategies for Growth](</en/sidehustle/churn-reduction.html>)

**See also:** [SaaS Analytics: Mixpanel, Amplitude, PostHog, Event Tracking, and Funnel Analysis](</en/sidehustle/saas-analytics.html>), [Product-Led Growth: Freemium, Free Trials, Self-Serve, and Usage-Based Pricing](</en/sidehustle/product-led-growth.html>), [SaaS Churn Reduction: Retention Strategies for Growth](</en/sidehustle/churn-reduction.html>)

**See also:** [SaaS Analytics: Mixpanel, Amplitude, PostHog, Event Tracking, and Funnel Analysis](</en/sidehustle/saas-analytics.html>), [Product-Led Growth: Freemium, Free Trials, Self-Serve, and Usage-Based Pricing](</en/sidehustle/product-led-growth.html>), [SaaS Churn Reduction: Retention Strategies for Growth](</en/sidehustle/churn-reduction.html>)

**See also:** [SaaS Analytics: Mixpanel, Amplitude, PostHog, Event Tracking, and Funnel Analysis](</en/sidehustle/saas-analytics.html>), [Product-Led Growth: Freemium, Free Trials, Self-Serve, and Usage-Based Pricing](</en/sidehustle/product-led-growth.html>), [SaaS Churn Reduction: Retention Strategies for Growth](</en/sidehustle/churn-reduction.html>)

**See also:** [Billing Integration for SaaS: Stripe, Paddle, Chargebee, Subscription Management, and Dunning](</en/sidehustle/billing-integration.html>), [Customer Acquisition Strategies: Content Marketing, SEO, Paid Ads, Partnerships, and PLG](</en/sidehustle/customer-acquisition.html>), [Developer Community Building: Discord, GitHub, Documentation, and Open Source](</en/sidehustle/dev-community-building.html>)

**See also:** [Billing Integration for SaaS: Stripe, Paddle, Chargebee, Subscription Management, and Dunning](</en/sidehustle/billing-integration.html>), [Customer Acquisition Strategies: Content Marketing, SEO, Paid Ads, Partnerships, and PLG](</en/sidehustle/customer-acquisition.html>), [Developer Community Building: Discord, GitHub, Documentation, and Open Source](</en/sidehustle/dev-community-building.html>)

**See also:** [Billing Integration for SaaS: Stripe, Paddle, Chargebee, Subscription Management, and Dunning](</en/sidehustle/billing-integration.html>), [Customer Acquisition Strategies: Content Marketing, SEO, Paid Ads, Partnerships, and PLG](</en/sidehustle/customer-acquisition.html>), [Developer Community Building: Discord, GitHub, Documentation, and Open Source](</en/sidehustle/dev-community-building.html>)

**See also:** [Billing Integration for SaaS: Stripe, Paddle, Chargebee, Subscription Management, and Dunning](</en/sidehustle/billing-integration.html>), [Customer Acquisition Strategies: Content Marketing, SEO, Paid Ads, Partnerships, and PLG](</en/sidehustle/customer-acquisition.html>), [Developer Community Building: Discord, GitHub, Documentation, and Open Source](</en/sidehustle/dev-community-building.html>)

**See also:** [Billing Integration for SaaS: Stripe, Paddle, Chargebee, Subscription Management, and Dunning](</en/sidehustle/billing-integration.html>), [Customer Acquisition Strategies: Content Marketing, SEO, Paid Ads, Partnerships, and PLG](</en/sidehustle/customer-acquisition.html>), [Developer Community Building: Discord, GitHub, Documentation, and Open Source](</en/sidehustle/dev-community-building.html>)

**See also:** [Billing Integration for SaaS: Stripe, Paddle, Chargebee, Subscription Management, and Dunning](</en/sidehustle/billing-integration.html>), [Customer Acquisition Strategies: Content Marketing, SEO, Paid Ads, Partnerships, and PLG](</en/sidehustle/customer-acquisition.html>), [Developer Community Building: Discord, GitHub, Documentation, and Open Source](</en/sidehustle/dev-community-building.html>)

**See also:** [Billing Integration for SaaS: Stripe, Paddle, Chargebee, Subscription Management, and Dunning](</en/sidehustle/billing-integration.html>), [Customer Acquisition Strategies: Content Marketing, SEO, Paid Ads, Partnerships, and PLG](</en/sidehustle/customer-acquisition.html>), [Developer Community Building: Discord, GitHub, Documentation, and Open Source](</en/sidehustle/dev-community-building.html>)

**See also:** [Billing Integration for SaaS: Stripe, Paddle, Chargebee, Subscription Management, and Dunning](</en/sidehustle/billing-integration.html>), [Customer Acquisition Strategies: Content Marketing, SEO, Paid Ads, Partnerships, and PLG](</en/sidehustle/customer-acquisition.html>), [Developer Community Building: Discord, GitHub, Documentation, and Open Source](</en/sidehustle/dev-community-building.html>)

**See also:** [Billing Integration for SaaS: Stripe, Paddle, Chargebee, Subscription Management, and Dunning](</en/sidehustle/billing-integration.html>), [Customer Acquisition Strategies: Content Marketing, SEO, Paid Ads, Partnerships, and PLG](</en/sidehustle/customer-acquisition.html>), [Developer Community Building: Discord, GitHub, Documentation, and Open Source](</en/sidehustle/dev-community-building.html>)

**See also:** [Billing Integration for SaaS: Stripe, Paddle, Chargebee, Subscription Management, and Dunning](</en/sidehustle/billing-integration.html>), [Customer Acquisition Strategies: Content Marketing, SEO, Paid Ads, Partnerships, and PLG](</en/sidehustle/customer-acquisition.html>), [Developer Community Building: Discord, GitHub, Documentation, and Open Source](</en/sidehustle/dev-community-building.html>)

**See also:** [Billing Integration for SaaS: Stripe, Paddle, Chargebee, Subscription Management, and Dunning](</en/sidehustle/billing-integration.html>), [Customer Acquisition Strategies: Content Marketing, SEO, Paid Ads, Partnerships, and PLG](</en/sidehustle/customer-acquisition.html>), [Developer Community Building: Discord, GitHub, Documentation, and Open Source](</en/sidehustle/dev-community-building.html>)

**See also:** [Billing Integration for SaaS: Stripe, Paddle, Chargebee, Subscription Management, and Dunning](</en/sidehustle/billing-integration.html>), [Customer Acquisition Strategies: Content Marketing, SEO, Paid Ads, Partnerships, and PLG](</en/sidehustle/customer-acquisition.html>), [Developer Community Building: Discord, GitHub, Documentation, and Open Source](</en/sidehustle/dev-community-building.html>)
