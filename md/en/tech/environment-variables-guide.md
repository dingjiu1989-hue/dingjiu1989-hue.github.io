---
title: "Environment Variables: The Complete Guide for Developers"
description: "How to manage .env files, secrets, and configs across local dev, CI/CD, and production. Covers .env.local, Doppler, Infisical, and production security."
date: 2026-05-08
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/environment-variables-guide.html
---

# Environment Variables: The Complete Guide for Developers

Environment variables connect your code to the outside world — database URLs, API keys, feature flags. Misconfiguring them is one of the most common causes of production incidents and security breaches. Here's the complete guide to managing them correctly.

## The Hierarchy of Config

Layer| Where| Example| Never Commit?  
---|---|---|---  
**Default values**|  Code (as fallback)| `PORT ?? 3000`| Commit (with safe defaults)  
**Local dev overrides**| .env.local| `DATABASE_URL=localhost`| Yes (.gitignore)  
**CI/CD**|  Platform secrets| `DATABASE_URL=staging-db`| Yes (platform-managed)  
**Production**|  Platform secrets / vault| `DATABASE_URL=prod-db`| Yes (platform-managed)  
**Public config**|  NEXT_PUBLIC_* vars| `NEXT_PUBLIC_API_URL`| OK (intentionally public)  

## Rules for Environment Variables

  1. **Never commit secrets to Git.** Use .gitignore for .env.local, .env.*.local. If a secret ever hits Git history, rotate it immediately.
  2. **Prefix public variables.** Next.js uses NEXT_PUBLIC_*. Vite uses VITE_*. This makes it clear what's exposed to the browser.
  3. **Validate at startup, not at runtime.** Use Zod to validate all env vars when the app starts. If a required var is missing, crash immediately — don't fail mysteriously 3 hours later.
  4. **Use different values per environment.** Development, staging, and production should have separate database URLs, API keys, and feature flags.

## Validation Pattern (Prevent Runtime Surprises)

    // env.ts — validate all env vars at startup
    import { z } from "zod";

    const envSchema = z.object({
      DATABASE_URL: z.string().url(),
      AUTH_SECRET: z.string().min(32),
      STRIPE_SECRET_KEY: z.string().startsWith("sk_"),
      NEXT_PUBLIC_APP_URL: z.string().url().default("http://localhost:3000"),
      FEATURE_NEW_CHECKOUT: z.enum(["true", "false"]).default("false"),
    });

    export const env = envSchema.parse(process.env);
    // If any var is missing or invalid, the app crashes immediately

## Managing Secrets Across a Team

Tool| Best For| How It Works  
---|---|---  
**Doppler**|  Teams, automatic sync| Central dashboard → CLI syncs to local .env. Secrets never on disk.  
**Infisical**|  Open source, self-hosted| Self-hosted Doppler alternative. Inject secrets at build/run time.  
**1Password CLI**|  Small teams with 1Password| op run --env-file=.env -- npm run dev. Secret references, not values.  
**Platform-native**|  Simplest, free| Vercel/Render/Railway all have secret management built in.  

## Common Mistakes & Fixes

Mistake| Fix  
---|---  
Hardcoding API keys in source| Move to .env.local immediately. Check git history. Rotate if exposed.  
NEXT_PUBLIC_* for secrets| NEXT_PUBLIC_ vars are bundled into client JS. Anyone can see them. Never put secrets here.  
Same API key for dev + prod| Use separate keys. Stripe has test mode keys. Dev databases are separate.  
.env.example not updated| Add new vars to .env.example with dummy values. Treat it as documentation.  
Secrets in Docker images| Inject at runtime, not at build time. Use docker run -e or Docker secrets.  

**Bottom line:** Validate env vars at startup with Zod. Never put secrets in NEXT_PUBLIC_* or Git. Use Doppler/Infisical for teams, platform-native for side projects. Document every variable in .env.example. See also: [Web Security Basics](</en/tech/web-security-basics.html>) and [Error Handling Best Practices](</en/tech/error-handling-best-practices.html>).
