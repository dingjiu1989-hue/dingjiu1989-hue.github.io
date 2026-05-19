---
title: "AI API Integration Guide: OpenAI, Anthropic, and Google AI for Developers"
description: "Practical guide to integrating AI APIs into your apps. Streaming responses, function calling, embeddings, rate limits, and cost optimization across the big 3 providers."
date: 2025-11-06
board: ai
url: https://dingjiu1989-hue.github.io/en/ai/ai-api-integration-guide.html
---

# AI API Integration Guide: OpenAI, Anthropic, and Google AI for Developers

Adding AI to your app means calling an API. OpenAI, Anthropic, and Google AI each have different SDKs, pricing models, and capabilities. Here's the practical integration guide covering the patterns you'll actually use: streaming, function calling, embeddings, and cost optimization.

## The Big Three AI APIs

| OpenAI| Anthropic| Google AI  
---|---|---|---  
**Models**|  GPT-4o, GPT-4.1, o4-mini| Claude Opus 4, Sonnet 4, Haiku 4| Gemini 2.5 Pro, Flash  
**Max context**|  128K tokens| 200K tokens| 1M tokens  
**SDK**|  openai (Node/Python)| @anthropic-ai/sdk| @google/generative-ai  
**Pricing model**|  Per 1K tokens (in+out)| Per 1M tokens (in+out)| Per 1M chars (in+out)  
**Image input**|  Yes (GPT-4o)| Yes| Yes  
**Image output**|  Yes (DALL-E)| No| Yes (Imagen)  
**Streaming**|  Yes (SSE)| Yes (SSE + streaming text)| Yes  
  
## 1\. Streaming Responses

Streaming shows tokens as they're generated — critical for good UX. All three APIs support it:
    
    
    // Anthropic streaming example
    import Anthropic from "@anthropic-ai/sdk";
    
    const client = new Anthropic();
    
    const stream = client.messages.stream({
      model: "claude-sonnet-4-20250514",
      max_tokens: 4096,
      messages: [{ role: "user", content: "Write a function to..." }],
    });
    
    stream.on("text", (text) => {
      process.stdout.write(text);  // Show tokens as they arrive
    });
    
    const finalMessage = await stream.finalMessage();

## 2\. Function Calling (Tool Use)

Function calling lets the AI call your APIs. Define the tools, and the AI decides when to use them:
    
    
    // Define a tool
    const tools = [{
      name: "search_database",
      description: "Search the product database",
      input_schema: {
        type: "object",
        properties: {
          query: { type: "string", description: "Search query" },
          category: { type: "string", enum: ["electronics", "books", "clothing"] }
        },
        required: ["query"]
      }
    }];
    
    // The AI can now call search_database() when needed
    // Your code executes the function and sends the result back

## 3\. Embeddings for Semantic Search

Embeddings convert text into vectors for semantic search. OpenAI and Google both offer embedding APIs:
    
    
    // OpenAI embeddings
    const embedding = await openai.embeddings.create({
      model: "text-embedding-3-small",  // $0.02/1M tokens — cheapest
      input: "How to deploy Next.js to Vercel",
    });
    
    // Store in vector DB (pgvector, Pinecone, Chroma)
    // Query: find similar docs by cosine similarity

## 4\. Cost Optimization Strategies

Strategy| Savings| How  
---|---|---  
**Model routing**|  50-80%| Route simple tasks to Haiku/Flash, complex to Sonnet/Pro  
**Caching**|  50-90%| Cache common responses. Anthropic has built-in prompt caching.  
**Shorter prompts**|  20-40%| System prompts are charged per request. Keep them tight.  
**Batch processing**|  50%| OpenAI batch API is 50% cheaper (24h turnaround).  
**Token limits**|  Variable| Set max_tokens to prevent runaway costs.  
**Self-host small models**|  90%+| Use local models for classification/summarization tasks.  
  
## 5\. Error Handling Pattern
    
    
    async function callAI(prompt: string): Promise<string> {
      const maxRetries = 3;
      for (let i = 0; i < maxRetries; i++) {
        try {
          const response = await client.messages.create({
            model: "claude-sonnet-4-20250514",
            max_tokens: 4096,
            messages: [{ role: "user", content: prompt }],
          });
          return response.content[0].text;
        } catch (error) {
          if (error.status === 429) {  // Rate limited
            await sleep(Math.pow(2, i) * 1000);  // Exponential backoff
            continue;
          }
          if (error.status === 400) throw error;  // Bad request — don't retry
          throw error;
        }
      }
    }

**Bottom line:** Use streaming for any user-facing feature. Use function calling to extend the AI with your own data. Cache aggressively. Route simple queries to cheaper models. See also: [Prompt Engineering](</en/ai/prompt-engineering.html>) and [Best LLMs for Coding](</en/ai/best-llms-for-coding-2026.html>).

**See also:** [LLM Cost Optimization: Cut Your AI API Bills by 50-80% (2026 Guide)](</en/ai/llm-cost-optimization.html>), [LLM API Design: Streaming, Structured Output, Error Handling, Rate Limits](</en/ai/llm-api-design.html>), [MCP (Model Context Protocol) Complete Guide: The Standard Connecting AI to Your Tools](</en/ai/mcp-complete-guide.html>)
