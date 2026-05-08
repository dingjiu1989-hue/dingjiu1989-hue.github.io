---
title: "Caching Strategies for Web Apps: CDN, Redis, Browser, and API Caching"
description: "Where, when, and how to cache in a modern web app. CDN caching, Redis, HTTP cache headers, stale-while-revalidate, and cache invalidation strategies."
date: 2026-05-08
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/caching-strategies-web-apps.html
---

# Caching Strategies for Web Apps: CDN, Redis, Browser, and API Caching

Caching is the difference between a 50ms response and a 5-second timeout. But cache invalidation is famously one of the hardest problems in computer science. Here's a practical guide to caching at every layer — and when NOT to cache.

## The Caching Layers

Layer| What to Cache| TTL| Invalidation  
---|---|---|---  
**Browser (HTTP Cache)**|  Static assets (JS, CSS, images, fonts)| 1 year (with hash in filename)| Change filename → new URL → cache miss  
**CDN**|  HTML, API responses, images| 1 min to 1 hour| Purge by URL or tag. Stale-while-revalidate.  
**Application (Redis/Memcached)**|  DB query results, computed values, sessions| 1 second to 1 hour| Delete on write. TTL-based. Cache-aside pattern.  
**Database query cache**|  Query results (PostgreSQL/MySQL built-in)| Automatic| Invalidated on table writes.  
**Next.js data cache**|  fetch() results in Server Components| Configurable| revalidateTag(), revalidatePath()  
  
## 1\. Browser & CDN: Cache-Control Headers
    
    
    # Static assets with content hash (1 year)
    # /_next/static/chunks/main-abc123.js
    Cache-Control: public, max-age=31536000, immutable
    
    # HTML pages (revalidate at CDN, serve stale if origin is down)
    # /blog/my-post
    Cache-Control: public, s-maxage=60, stale-while-revalidate=300
    
    # API responses that don't change often
    # /api/posts/trending
    Cache-Control: public, max-age=300, s-maxage=300
    
    # Never cache (user-specific data)
    # /api/user/profile
    Cache-Control: private, no-cache, no-store, must-revalidate

## 2\. Application Cache: Redis
    
    
    // Cache-aside pattern — the most common approach
    async function getUserPosts(userId: string): Promise<Post[]> {
      const cacheKey = `user:${userId}:posts`;
    
      // 1. Try cache
      const cached = await redis.get(cacheKey);
      if (cached) return JSON.parse(cached);
    
      // 2. Cache miss — fetch from DB
      const posts = await db.posts.findMany({ where: { userId } });
    
      // 3. Store in cache (5 minutes)
      await redis.set(cacheKey, JSON.stringify(posts), "EX", 300);
    
      return posts;
    }
    
    // Delete cache on write — prevent stale data
    async function createPost(userId: string, data: CreatePostInput) {
      const post = await db.posts.create({ data: { userId, ...data } });
      await redis.del(`user:${userId}:posts`); // Invalidate
      return post;
    }

## 3\. Next.js Caching (App Router)
    
    
    // Static data — cached permanently
    async function getNavigation() {
      const res = await fetch("https://cms.example.com/navigation");
      return res.json(); // Cached forever (build-time)
    }
    
    // Revalidated data — cached, then refreshed
    async function getBlogPosts() {
      const res = await fetch("https://cms.example.com/posts", {
        next: { revalidate: 3600 }, // Revalidate every hour
      });
      return res.json();
    }
    
    // On-demand revalidation (webhook from CMS)
    import { revalidateTag } from "next/cache";
    
    export async function POST(request: Request) {
      const { tag } = await request.json();
      revalidateTag(tag); // Revalidate everything with this tag
      return Response.json({ revalidated: true });
    }

## When NOT to Cache

  * **User-specific data that changes frequently:** Shopping cart, notifications, real-time dashboards.
  * **Write-heavy data:** If the data changes every second, caching just adds complexity.
  * **Data that must be accurate:** Bank balances, inventory counts during flash sales. Use the database directly or use a cache with write-through.
  * **Before you have a performance problem:** Caching prematurely adds complexity. Wait until you measure a bottleneck.



## Cache Invalidation Strategies

Strategy| How| When  
---|---|---  
**TTL (Time to Live)**|  Set expiry. Data is stale for up to TTL.| When staleness is acceptable (analytics, trending, recommendations)  
**Write-through**|  Write to cache AND DB simultaneously.| When you need consistency and read latency matters  
**Cache-aside (lazy)**|  Read from cache, fall back to DB. Delete on write.| Most common. Good balance of simplicity and freshness.  
**Stale-while-revalidate**|  Serve stale, refresh in background.| CDN. Tolerates staleness for a few seconds for massive latency wins.  
  
**Bottom line:** Cache at the CDN first (biggest win, simplest). Add Redis when you have specific slow queries. Use Next.js built-in caching for data fetching. Invalidate on write, not on a timer, for user-facing data. See also: [Web Performance Tools](</en/tools/best-web-performance-tools.html>) and [Database Comparison](</en/compare/postgresql-vs-mysql-vs-sqlite.html>).
