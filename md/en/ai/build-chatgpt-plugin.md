---
title: "How to Build a Custom GPT Plugin: Complete Developer Guide"
description: "Step-by-step tutorial: setting up the manifest, creating API endpoints, authentication, testing in ChatGPT, and publishing to the GPT Store. Includes working code examples in Python and Node.js."
date: 2025-11-07
board: ai
url: https://dingjiu1989-hue.github.io/en/ai/build-chatgpt-plugin.html
---

# How to Build a Custom GPT Plugin: Complete Developer Guide

Custom GPTs and ChatGPT plugins let you extend ChatGPT with your own data, APIs, and functionality. In 2026, the GPT Store has millions of custom GPTs — but most are thin wrappers without real functionality. For developers, the real opportunity is building GPTs that connect to live APIs, databases, and internal tools. This guide walks through building a production-quality ChatGPT plugin with working code examples in Python and Node.js.

## Custom GPT vs ChatGPT Plugin: What to Build

Feature| Custom GPT| ChatGPT Plugin (Actions)  
---|---|---  
Setup Complexity| Low (configuration-based)| Medium-High (requires API + OpenAPI spec)  
Coding Required| No (prompt + knowledge files)| Yes (backend API required)  
Data Sources| Static files (PDF, CSV, text)| Live APIs, databases, any HTTP endpoint  
Authentication| None| API key, OAuth 2.0, service accounts  
Real-Time Data| No (static at creation time)| Yes (fetches live data on every query)  
Best For| Knowledge bases, style guides, templates| Interactive tools, live dashboards, CRUD operations  
  
## Building a Plugin: Architecture

**Best for:** Integrating live data, external APIs, or business logic. **Weak spot:** You need to run a backend server and maintain an OpenAPI 3.1 specification.

The architecture has three components:

  1. **Your API Backend:** A REST API that ChatGPT calls to perform actions (Node.js, Python, or any backend)
  2. **OpenAPI Specification:** A JSON/YAML file describing your API endpoints (what ChatGPT reads to understand your plugin)
  3. **Plugin Manifest:** A JSON file registered with OpenAI describing your plugin and pointing to your API + OpenAPI spec



## Step-by-Step Implementation (Python/FastAPI)
    
    
    # main.py — FastAPI backend for a "DevTools" GPT plugin
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    import httpx
    
    app = FastAPI(title="DevTools Plugin API", version="1.0.0")
    app.add_middleware(CORSMiddleware, allow_origins=["*"])
    
    # --- Models ---
    class URLInput(BaseModel):
        url: str
    
    class CodeInput(BaseModel):
        code: str
        language: str = "python"
    
    # --- Endpoints ---
    @app.get("/api/health")
    async def health():
        return {"status": "ok"}
    
    @app.post("/api/analyze-website")
    async def analyze_website(input: URLInput):
        """Analyze a website's tech stack and performance."""
        async with httpx.AsyncClient() as client:
            resp = await client.get(input.url, timeout=10.0)
        return {
            "url": input.url,
            "status_code": resp.status_code,
            "headers": dict(resp.headers),
            "size_bytes": len(resp.content),
            "server": resp.headers.get("server", "unknown"),
        }
    
    @app.post("/api/review-code")
    async def review_code(input: CodeInput):
        """Review code for common issues."""
        issues = []
        if "TODO" in input.code:
            issues.append({"severity": "low", "message": "Contains TODO comments"})
        if "print(" in input.code:
            issues.append({"severity": "medium", "message": "Uses print() — consider logging"})
        if "password" in input.code.lower() or "secret" in input.code.lower():
            issues.append({"severity": "high", "message": "Potential hardcoded credentials"})
        return {"language": input.language, "issues": issues, "total_lines": len(input.code.splitlines())}
    

## OpenAPI Spec for Your Plugin

Create an `openapi.json` file that ChatGPT reads to understand your API. This must be hosted at a public URL:
    
    
    {
      "openapi": "3.1.0",
      "info": { "title": "DevTools Plugin", "version": "1.0.0" },
      "servers": [{ "url": "https://your-api.example.com" }],
      "paths": {
        "/api/analyze-website": {
          "post": {
            "summary": "Analyze a website's tech stack",
            "operationId": "analyzeWebsite",
            "requestBody": { "required": true, "content": { "application/json": { "schema": { "type": "object", "properties": { "url": { "type": "string" } } } } } },
            "responses": { "200": { "description": "Analysis results" } }
          }
        },
        "/api/review-code": {
          "post": {
            "summary": "Review code for issues",
            "operationId": "reviewCode",
            "requestBody": { "required": true, "content": { "application/json": { "schema": { "type": "object", "properties": { "code": { "type": "string" }, "language": { "type": "string" } } } } } },
            "responses": { "200": { "description": "Code review results" } }
          }
        }
      }
    }

**Bottom line:** ChatGPT Plugins are most valuable when they connect to live data or systems that change — static knowledge is better served by Custom GPTs with uploaded files. Start simple: one endpoint, deploy on Railway or Fly.io (free tier), test thoroughly, then add more features. The barrier to entry is running a public API — but the reward is a GPT that does real work, not just chatting. See also: [How to Build and Sell APIs](</en/sidehustle/build-and-sell-api.html>) and [AI API Integration Guide](</en/ai/ai-api-integration-guide.html>).

**See also:** [LLM Function Calling: Complete Developer Guide with Code Examples](</en/ai/function-calling-guide.html>), [How to Build and Sell APIs: A Developer's Guide to API-as-a-Service](</en/sidehustle/build-and-sell-api.html>), [Webhook Implementation: Design, Security, and Best Practices (2026)](</en/tech/webhook-implementation-guide.html>)
