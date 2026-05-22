---
title: "How to Deploy a Next.js App for Free: Step-by-Step Guide (2026)"
description: "Get your Next.js app live on the internet in 10 minutes without spending a cent. Covers Vercel, Cloudflare Pages, and environment variable setup."
date: 2025-10-09
board: tech
url: https://aidev.fit/en/tech/deploy-nextjs-free.html
---

# How to Deploy a Next.js App for Free: Step-by-Step Guide (2026)

You built a Next.js app. Now get it on the internet — for free, with a real URL, in 10 minutes. Here's the step-by-step guide covering Vercel (easiest for Next.js), plus Cloudflare Pages as an alternative with unlimited bandwidth.

## Option 1: Vercel (Easiest, Built for Next.js)

Vercel is the company behind Next.js. Deployment is zero-configuration — push to GitHub, and Vercel automatically detects Next.js, builds it, and gives you a URL. The free tier (100GB bandwidth, 6K build minutes/month) is generous enough for most side projects.

### Step-by-Step
    
    
    # 1. Make sure your Next.js app is on GitHub
    git init && git add . && git commit -m "initial"
    git remote add origin https://github.com/your-username/your-repo.git
    git push -u origin main
    
    # 2. Go to vercel.com → Sign Up with GitHub
    # 3. Click "New Project" → Import your repo
    # 4. Vercel auto-detects Next.js. No configuration needed.
    # 5. Click "Deploy"
    
    # 3 minutes later: your app is live at your-app.vercel.app
    # Add a custom domain: Settings → Domains → add your domain

### Environment Variables

If your app uses .env.local, add those variables in Vercel:
    
    
    # Vercel Dashboard → Your Project → Settings → Environment Variables
    DATABASE_URL=postgresql://...
    NEXT_PUBLIC_API_URL=https://api.example.com
    AUTH_SECRET=your-secret-here
    
    # Redeploy after adding variables (Vercel will prompt you)

## Option 2: Cloudflare Pages (Unlimited Bandwidth)

If you expect a lot of traffic or want the largest global edge network (330+ locations), Cloudflare Pages is the better choice. It supports Next.js via the @cloudflare/next-on-pages adapter.
    
    
    # 1. Install adapter
    npm install -D @cloudflare/next-on-pages
    
    # 2. Update next.config.js (if App Router)
    const nextConfig = {
      // Your existing config
    };
    module.exports = nextConfig;
    
    # 3. Update wrangler.toml
    name = "your-app"
    compatibility_date = "2025-01-01"
    pages_build_output_dir = ".vercel/output/static"
    
    # 4. Push to GitHub
    # 5. Go to Cloudflare Dashboard → Pages → Create → Connect Git
    # 6. Set build command: npx @cloudflare/next-on-pages
    # 7. Set output directory: .vercel/output/static
    # 8. Deploy

**Limitation:** Not all Next.js features work on Cloudflare Pages. Server Components, middleware, and ISR require the Vercel runtime. Check compatibility before choosing Cloudflare.

## Option 3: Static Export (Simplest, Most Portable)

If your Next.js app doesn't use server-side features (SSR, middleware, API routes), export it as a static site:
    
    
    # next.config.js
    const nextConfig = {
      output: 'export',  // Static HTML export
    };
    
    # Build: npx next build → output in /out folder
    # Deploy /out to: GitHub Pages, Cloudflare Pages, Netlify, or any static host

## Quick Comparison

| Vercel| Cloudflare Pages| Static Export + GitHub Pages  
---|---|---|---  
**SSR/ISR/Middleware**|  Full support| Limited (adapter)| No (static only)  
**Bandwidth**|  100GB| Unlimited| 100GB  
**Setup time**|  2 minutes| 10 minutes| 5 minutes  
**Edge locations**|  100+| 330+| 1 (GitHub CDN)  
**Best for**|  Full Next.js features| Traffic-heavy static| Simple static sites  
  
**Bottom line:** Vercel is the default for Next.js — simplest deploy, full feature support. Cloudflare Pages for unlimited bandwidth. Static export for maximum portability. After deploying, set up a custom domain (free on both platforms) and you're production-ready. See also: [Free Hosting Guide](</en/tools/best-free-hosting-side-projects.html>) and [Hosting Comparison](</en/compare/vercel-vs-netlify-vs-cloudflare.html>).
