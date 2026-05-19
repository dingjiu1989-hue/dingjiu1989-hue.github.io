---
title: "LLM API Design: Streaming, Structured Output, Error Handling, Rate Limits"
description: "Practical guide to designing LLM APIs with streaming responses, structured JSON output, error handling patterns, and rate limiting strategies for production sys"
date: 2026-02-16
board: ai
url: https://dingjiu1989-hue.github.io/en/ai/llm-api-design.html
---

# LLM API Design: Streaming, Structured Output, Error Handling, Rate Limits

## Introduction

Designing APIs that wrap large language models requires handling concerns that traditional REST APIs do not face: streaming token-by-token responses, enforcing structured output schemas, managing unpredictable latency, and protecting against runaway costs. This guide covers the four critical pillars of LLM API design with production-ready patterns.

## Streaming Responses

Streaming is the standard way to return LLM outputs. Instead of waiting for the full response, the client receives tokens as they are generated:

from fastapi import FastAPI, Request

from fastapi.responses import StreamingResponse

from anthropic import AsyncAnthropic

import asyncio

app = FastAPI()

client = AsyncAnthropic(api_key="sk-ant-...")

async def generate_stream(prompt: str):

async with client.messages.stream(

model="claude-sonnet-4-20260512",

max_tokens=4096,

messages=[{"role": "user", "content": prompt}],

) as stream:

async for chunk in stream:

if chunk.type == "content_block_delta":

yield f"data: {chunk.delta.text}\n\n"

@app.post("/chat")

async def chat(request: Request):

body = await request.json()

return StreamingResponse(

generate_stream(body["prompt"]),

media_type="text/event-stream",

headers={

"Cache-Control": "no-cache",

"Connection": "keep-alive",

"X-Accel-Buffering": "no",

},

)

The Server-Sent Events protocol is the most compatible streaming format. Each `data:` line is a new token chunk. Clients use `EventSource` or fetch with `ReadableStream` to consume the stream progressively.

## Structured Output

Raw LLM text is unreliable for programmatic consumption. Use structured output modes to enforce JSON schemas:

from pydantic import BaseModel

from openai import OpenAI

client = OpenAI()

class ExtractedEntity(BaseModel):

name: str

type: str

confidence: float

source_text: str

class ExtractionResult(BaseModel):

entities: list[ExtractedEntity]

summary: str

language: str

response = client.beta.chat.completions.parse(

model="gpt-4o",

messages=[

{"role": "system", "content": "Extract entities from the text."},

{"role": "user", "content": user_text},

],

response_format=ExtractionResult,

)

result: ExtractionResult = response.choices[0].message.parsed

When the API does not support native structured output, use a two-step approach: request JSON in the prompt, then validate and re-request on failure:

import json

from pydantic import ValidationError

def safe_structured_generate(prompt: str, schema: type[BaseModel], max_retries=3):

for attempt in range(max_retries):

raw = call_llm(prompt + "\n\nRespond in valid JSON matching this schema: " + str(schema.model_json_schema()))

try:

parsed = json.loads(clean_json(raw))

return schema.model_validate(parsed)

except (json.JSONDecodeError, ValidationError) as e:

if attempt == max_retries - 1:

raise

prompt += f"\n\nPrevious attempt failed: {e}. Please fix the JSON."

return None

## Error Handling

LLM APIs fail in distinctive ways. Build a retry strategy around each failure mode:

import time

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

class RateLimitError(Exception): pass

class ContextWindowExceeded(Exception): pass

class ContentFilterError(Exception): pass

@retry(

stop=stop_after_attempt(3),

wait=wait_exponential(multiplier=1, min=2, max=30),

retry=retry_if_exception_type(RateLimitError),

)

def call_with_retry(prompt: str) -> str:

try:

response = client.messages.create(model="claude-sonnet-4-20260512", max_tokens=1024, messages=[{"role": "user", "content": prompt}])

return response.content[0].text

except APIStatusError as e:

if e.status_code == 429:

retry_after = int(e.response.headers.get("retry-after", 5))

time.sleep(retry_after)

raise RateLimitError from e

elif e.status_code == 400 and "context_length_exceeded" in str(e):

raise ContextWindowExceeded from e

elif e.status_code == 400 and "content_filter" in str(e):

raise ContentFilterError from e

raise

Each error type deserves a different handler: rate limits get exponential backoff, context windows trigger input truncation, and content filter errors should be logged and escalated.

## Rate Limiting

Protect your API from abuse and cost spikes with layered rate limiting:

from fastapi import HTTPException

import time

from collections import defaultdict

class RateLimiter:

def **init**(self):

self.tokens_per_second = 10

self.burst_limit = 20

self.cost_per_token = 0.000003

self.daily_budget = 10.0

self.user_usage = defaultdict(float)

async def check(self, user_id: str, estimated_tokens: int):

cost = estimated_tokens * self.cost_per_token

if self.user_usage[user_id] + cost > self.daily_budget:

raise HTTPException(status_code=429, detail="Daily budget exceeded")

self.user_usage[user_id] += cost

def get_usage(self, user_id: str) -> dict:

return {"cost": self.user_usage[user_id], "budget": self.daily_budget}

rate_limiter = RateLimiter()

@app.post("/chat")

async def chat(request: Request):

user_id = request.headers.get("X-User-Id")

body = await request.json()

estimated = len(body["prompt"].split()) * 2 + int(body.get("max_tokens", 1024))

await rate_limiter.check(user_id, estimated)

return await generate_response(body["prompt"])

## Conclusion

Designing LLM APIs requires balancing responsiveness with cost control. Stream responses for user experience, enforce structured output for programmatic reliability, implement retry logic calibrated to each error type, and gate access with rate and budget limits. These four patterns form the foundation of any production LLM service.

**See also:** [AI Gateway: API Routing, Rate Limiting, Fallback Models, Cost Management, and Logging](</en/ai/ai-gateway.html>), [Tool Use Patterns: Function Calling, Structured Tools, Multi-Step Reasoning](</en/ai/tool-use-patterns.html>), [Prompt Chaining: Building Multi-Step LLM Workflows](</en/ai/ai-prompt-chaining.html>).

**See also:** [AI Gateway: API Routing, Rate Limiting, Fallback Models, Cost Management, and Logging](</en/ai/ai-gateway.html>), [Tool Use Patterns: Function Calling, Structured Tools, Multi-Step Reasoning](</en/ai/tool-use-patterns.html>), [Prompt Chaining: Building Multi-Step LLM Workflows](</en/ai/ai-prompt-chaining.html>)

**See also:** [AI Gateway: API Routing, Rate Limiting, Fallback Models, Cost Management, and Logging](</en/ai/ai-gateway.html>), [Tool Use Patterns: Function Calling, Structured Tools, Multi-Step Reasoning](</en/ai/tool-use-patterns.html>), [Prompt Chaining: Building Multi-Step LLM Workflows](</en/ai/ai-prompt-chaining.html>)

**See also:** [AI Gateway: API Routing, Rate Limiting, Fallback Models, Cost Management, and Logging](</en/ai/ai-gateway.html>), [Tool Use Patterns: Function Calling, Structured Tools, Multi-Step Reasoning](</en/ai/tool-use-patterns.html>), [Prompt Chaining: Building Multi-Step LLM Workflows](</en/ai/ai-prompt-chaining.html>)

**See also:** [AI Gateway: API Routing, Rate Limiting, Fallback Models, Cost Management, and Logging](</en/ai/ai-gateway.html>), [Tool Use Patterns: Function Calling, Structured Tools, Multi-Step Reasoning](</en/ai/tool-use-patterns.html>), [Prompt Chaining: Building Multi-Step LLM Workflows](</en/ai/ai-prompt-chaining.html>)

**See also:** [AI Gateway: API Routing, Rate Limiting, Fallback Models, Cost Management, and Logging](</en/ai/ai-gateway.html>), [Tool Use Patterns: Function Calling, Structured Tools, Multi-Step Reasoning](</en/ai/tool-use-patterns.html>), [Prompt Chaining: Building Multi-Step LLM Workflows](</en/ai/ai-prompt-chaining.html>)

**See also:** [AI Workflow Automation: LangChain, Temporal, Event-Driven Agents](</en/ai/ai-workflow-automation.html>), [LLM Caching: Semantic Cache, Exact Match, TTL, Invalidation Strategies](</en/ai/llm-caching-deep.html>), [LLM Safety: RLHF, Constitutional AI, Content Filtering, Red Teaming](</en/ai/llm-safety.html>)

**See also:** [AI Workflow Automation: LangChain, Temporal, Event-Driven Agents](</en/ai/ai-workflow-automation.html>), [LLM Caching: Semantic Cache, Exact Match, TTL, Invalidation Strategies](</en/ai/llm-caching-deep.html>), [LLM Safety: RLHF, Constitutional AI, Content Filtering, Red Teaming](</en/ai/llm-safety.html>)

**See also:** [AI Workflow Automation: LangChain, Temporal, Event-Driven Agents](</en/ai/ai-workflow-automation.html>), [LLM Caching: Semantic Cache, Exact Match, TTL, Invalidation Strategies](</en/ai/llm-caching-deep.html>), [LLM Safety: RLHF, Constitutional AI, Content Filtering, Red Teaming](</en/ai/llm-safety.html>)

**See also:** [AI Workflow Automation: LangChain, Temporal, Event-Driven Agents](</en/ai/ai-workflow-automation.html>), [LLM Caching: Semantic Cache, Exact Match, TTL, Invalidation Strategies](</en/ai/llm-caching-deep.html>), [LLM Safety: RLHF, Constitutional AI, Content Filtering, Red Teaming](</en/ai/llm-safety.html>)

**See also:** [AI Workflow Automation: LangChain, Temporal, Event-Driven Agents](</en/ai/ai-workflow-automation.html>), [LLM Caching: Semantic Cache, Exact Match, TTL, Invalidation Strategies](</en/ai/llm-caching-deep.html>), [LLM Safety: RLHF, Constitutional AI, Content Filtering, Red Teaming](</en/ai/llm-safety.html>)

**See also:** [AI Workflow Automation: LangChain, Temporal, Event-Driven Agents](</en/ai/ai-workflow-automation.html>), [LLM Caching: Semantic Cache, Exact Match, TTL, Invalidation Strategies](</en/ai/llm-caching-deep.html>), [LLM Safety: RLHF, Constitutional AI, Content Filtering, Red Teaming](</en/ai/llm-safety.html>)

**See also:** [AI Workflow Automation: LangChain, Temporal, Event-Driven Agents](</en/ai/ai-workflow-automation.html>), [LLM Caching: Semantic Cache, Exact Match, TTL, Invalidation Strategies](</en/ai/llm-caching-deep.html>), [LLM Safety: RLHF, Constitutional AI, Content Filtering, Red Teaming](</en/ai/llm-safety.html>)
