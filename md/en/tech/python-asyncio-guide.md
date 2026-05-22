---
title: "Python asyncio Complete Guide: Coroutines, Tasks, and Event Loops"
description: "Master Python async programming: coroutines with async/await, Task groups in Python 3.11+, asyncio.gather vs as_completed, error handling in async code, and integrating async with sync libraries."
date: 2025-10-15
board: tech
url: https://aidev.fit/en/tech/python-asyncio-guide.html
---

# Python asyncio Complete Guide: Coroutines, Tasks, and Event Loops

Python's asyncio has matured into the standard way to write concurrent I/O-bound code, but the learning curve remains steep. The introduction of Task Groups in Python 3.11 and improved exception handling make async Python more ergonomic than ever. This guide covers the patterns that work — and the ones that bite you — with production-ready examples.

## Core Concepts

Concept| What It Is| When to Use  
---|---|---  
Coroutine| A function defined with async def — can be suspended and resumed| Any I/O-bound operation: HTTP requests, DB queries, file I/O  
Task| A coroutine wrapped and scheduled to run on the event loop| Run multiple coroutines concurrently  
Event Loop| The scheduler that runs async code (one thread, cooperative multitasking)| You rarely touch this directly — asyncio.run() handles it  
Awaitable| Anything you can await: coroutine, Task, Future| Use await to pause until the result is ready  
  
## Task Groups (Python 3.11+): The Modern Way

**Best for:** Running multiple async tasks concurrently with proper error handling. Replaces asyncio.gather() with structured concurrency — if one task fails, all sibling tasks are cancelled.
    
    
    import asyncio
    import aiohttp
    
    async def fetch_url(url: str) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return await resp.json()
    
    async def main():
        urls = ['https://api1.example.com', 'https://api2.example.com']
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(fetch_url(url)) for url in urls]
        # All tasks completed (or exception propagated) after exiting TaskGroup
        return [t.result() for t in tasks]
    
    results = asyncio.run(main())

## asyncio.gather vs as_completed

Function| Behavior| Use Case  
---|---|---  
asyncio.gather()| Run all tasks, return results in order. If one raises, it propagates. Prefer TaskGroup in 3.11+.| When you need all results and order matters  
asyncio.as_completed()| Yield results as each task finishes (fastest first)| When you want to process results as they arrive  
asyncio.wait()| Low-level: wait for FIRST_COMPLETED or ALL_COMPLETED| Timeouts, race conditions, advanced patterns  
  
## Common Pitfalls and Solutions

### 1\. Running Blocking Code in Async Functions

**Problem:** Calling a sync function (e.g., time.sleep, requests.get, heavy CPU work) inside an async function blocks the entire event loop. **Solution:** Use asyncio.to_thread() for I/O-bound blocking code, or run_in_executor() for CPU-bound work.
    
    
    # Bad: blocks the event loop
    result = requests.get('https://api.example.com')
    
    # Good: offload to a thread
    result = await asyncio.to_thread(requests.get, 'https://api.example.com')

### 2\. Unhandled Exceptions in Background Tasks

**Problem:** If a Task raises an exception and you never await it, the exception is silently lost until garbage collection. **Solution:** Always use TaskGroup — it ensures exceptions are propagated. For fire-and-forget tasks, add a done callback that logs exceptions.

### 3\. Creating Too Many Concurrent Connections

**Solution:** Use asyncio.Semaphore to limit concurrency:
    
    
    sem = asyncio.Semaphore(20)  # Max 20 concurrent requests
    async def rate_limited_fetch(url):
        async with sem:
            return await fetch_url(url)

**Bottom line:** Use TaskGroup for structured concurrency — it replaces the error-prone gather() pattern. Keep async code purely async (offload blocking code to threads). Always limit concurrency with Semaphore when making external requests. See also: [Node.js Streams Guide](</en/tech/nodejs-streams-guide.html>) and [Error Handling Best Practices](</en/tech/error-handling-best-practices.html>).

**See also:** [Python Tutorial: From Zero to Your First Program](</en/tech/python-tutorial.html>), [Error Handling Best Practices: From Try/Catch to Structured Errors](</en/tech/error-handling-best-practices.html>), [GraphQL API Design: Schema Best Practices, Federation, and Performance](</en/tech/graphql-api-design.html>)
