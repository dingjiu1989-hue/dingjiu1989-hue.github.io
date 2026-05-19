---
title: "React Server Components Guide: Architecture, Patterns, and When to Use RSC in 2026"
description: "Deep dive into React Server Components — server vs client components, streaming patterns, Server Actions, boundary rules, and when RSC is worth the complexity."
date: 2025-10-20
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/react-server-components-guide.html
---

# React Server Components Guide: Architecture, Patterns, and When to Use RSC in 2026

## React's Biggest Architectural Shift

React Server Components (RSC) represent the most significant change to React's programming model since hooks. They let you render components on the server, stream them to the client, and never send the JavaScript for those components to the browser. The result: smaller bundles, faster page loads, and direct database access from your components. But RSC also introduces a new mental model that confuses even experienced React developers. Here's what you actually need to understand.

## The Core Idea: Two Component Types

| Server Components (default)| Client Components ('use client')  
---|---|---  
Where they run| Server only (at build time or request time)| Server (SSR) + Client (hydration + interaction)  
JavaScript sent to browser| Zero (only the rendered output)| Full component code + dependencies  
Can use| async/await, fs, DB queries, secrets, any Node API| useState, useEffect, onClick, browser APIs, context  
Cannot use| useState, useEffect, event handlers, browser APIs| Direct database access, filesystem, secrets  
Bundles size impact| Zero (rendered on server, streamed as HTML/RSC payload)| Adds to client bundle  
  
**The mental model shift:** In traditional React, every component ships JavaScript to the browser. In RSC, server components are the default — you opt IN to client-side interactivity with 'use client'. This inverts the traditional model where you opt OUT of client-side code with SSR. The result: most of your components (the ones that just render data) send zero JavaScript.

## When a Component Should Be Server vs Client
    
    
    // Server Component (default) — no 'use client' directive
    // ✅ Direct database access
    // ✅ Async data fetching
    // ✅ Keep secrets (API keys, tokens)
    // ✅ Large dependencies (stay on server)
    // ✅ Render non-interactive content
    
    async function ArticleList() {
        const articles = await db.query('SELECT * FROM articles ORDER BY date DESC');
        return (
            <div>
                {articles.map(a => <ArticleCard key={a.id} article={a} />)}
            </div>
        );
    }
    
    
    // Client Component — must have 'use client' directive
    // ✅ Event listeners (onClick, onChange)
    // ✅ useState, useReducer, useEffect
    // ✅ Browser APIs (localStorage, geolocation, canvas)
    // ✅ Custom hooks that use state/effects
    // ❌ Direct database access
    // ❌ Server-side secrets
    
    'use client';
    function LikeButton({ articleId }) {
        const [liked, setLiked] = useState(false);
        return <button onClick={() => setLiked(!liked)}>{liked ? '♥' : '♡'}</button>;
    }

## The Composition Pattern: Server Shell, Client Islands

The most common RSC pattern: a server component fetches data and wraps client-interactive islands:
    
    
    // ArticlePage.server.tsx — Server Component
    async function ArticlePage({ slug }) {
        const article = await db.article.findUnique({ where: { slug } }); // runs on server
        return (
            <article>
                <h1>{article.title}</h1>
                <div>{article.content}</div>
                <LikeButton articleId={article.id} />      {/* Client Component */}
                <CommentSection articleId={article.id} />   {/* Client Component */}
            </article>
        );
    }

Server component (ArticlePage) sends ZERO JavaScript. LikeButton and CommentSection ship their JS. The non-interactive parts (title, content) are rendered on the server and streamed as HTML. This pattern — "server shell, client islands" — is the mental model for RSC architecture.

## Streaming and Suspense

RSC works with React Suspense to stream content as it becomes available. The server sends the page shell immediately, then streams in content as data loads:
    
    
    function ArticlePage({ slug }) {
        return (
            <div>
                <ArticleHeader slug={slug} />              {/* Renders immediately */}
                <Suspense fallback={<Spinner />}>
                    <ArticleBody slug={slug} />           {/* Streams when DB query completes */}
                </Suspense>
                <Suspense fallback={<Spinner />}>
                    <RelatedArticles slug={slug} />       {/* Streams independently */}
                </Suspense>
            </div>
        );
    }

The user sees the header immediately, then the article body streams in, then related articles — all without waiting for the slowest query.

## Server Actions: Mutations Without an API Route

RSC also introduces Server Actions — functions that run on the server but can be called directly from client components without creating an API endpoint:
    
    
    // actions.ts — server file
    'use server';
    import { revalidatePath } from 'next/cache';
    
    export async function updateArticle(slug: string, data: FormData) {
        const title = data.get('title');
        await db.article.update({ where: { slug }, data: { title } });
        revalidatePath(`/articles/${slug}`);
    }
    
    // Client component:
    'use client';
    import { updateArticle } from './actions';
    function EditForm({ slug }) {
        return (
            <form action={updateArticle.bind(null, slug)}>
                <input name="title" />
                <button type="submit">Save</button>
            </form>
        );
    }

No REST endpoint. No GraphQL mutation. No tRPC procedure. Just a function call across the client-server boundary. React serializes the form data, sends it to the server, runs the function, and returns the result.

## The Boundary Rules (Most Common Mistakes)

Rule| Why  
---|---  
Server components can import Client components ✅| A server component can render a client component as a child  
Client components CANNOT import Server components ❌| If a client component could import a server component, the server code would leak to the client  
You CAN pass server components as children to client components ✅| <ClientWrapper><ServerComponent /></ClientWrapper> — the server component renders first, then is passed as a React node to the client component  
'use client' marks the boundary — everything below is client| All components imported (directly or transitively) by a client component become client components too  
  
## Is RSC Worth the Complexity in 2026?

**Yes, if:** your app has significant non-interactive content (blog, e-commerce listing, documentation), your bundle size is a performance bottleneck (users on slow connections/devices), you want to eliminate the API layer for data fetching (direct DB queries from components), or you're building a new Next.js App Router project (RSC is the default and best-supported path).

**Stick with traditional React (Pages Router, Vite SPA) if:** your app is highly interactive (dashboard, design tool, real-time app — most components will be client components anyway), your team is still learning React (RSC adds complexity), your backend is already a separate service (you're not using Next.js as a full-stack framework), or you need to support older build tooling that doesn't support RSC.

**Bottom line:** RSC is not hype — it's a genuine architectural improvement that reduces JavaScript shipped to the browser by 30-70% for content-heavy apps. But it's not free: the mental model takes time to internalize, debugging is different (server errors vs client errors), and the ecosystem is still maturing (not all libraries support RSC yet). For new Next.js projects in 2026, start with RSC — you can always add 'use client' where you need interactivity, but you can't easily convert a all-client app to RSC later. See also: [Next.js vs Nuxt vs SvelteKit](</en/compare/nextjs-vs-nuxt-vs-sveltekit.html>) and [React Hooks Complete Guide](</en/tech/react-hooks-complete-guide.html>).

**See also:** [Microservices vs Monolith (2026): Making the Right Architectural Choice](</en/tech/microservices-vs-monolith.html>), [How to Deploy a Next.js App for Free: Step-by-Step Guide (2026)](</en/tech/deploy-nextjs-free.html>), [Responsive CSS in 2026: Container Queries, Grid, and Modern Layout Patterns](</en/tech/css-responsive-design-guide.html>)
