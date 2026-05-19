---
title: "AI API Gateway: Load Balancing, Fallback, Cost Tracking, Observability"
description: "Design an AI API gateway for multi-provider LLM access: load balancing across models, automatic fallback on failures, cost tracking per user, and observability."
date: 2026-02-13
board: ai
url: https://dingjiu1989-hue.github.io/en/ai/ai-api-gateway.html
---

# AI API Gateway: Load Balancing, Fallback, Cost Tracking, Observability

## Introduction

As organizations adopt multiple LLM providers (Anthropic, OpenAI, Google, open-source self-hosted), managing each directly from application code becomes unsustainable. An AI API gateway provides a unified interface for routing requests across providers, handling failures, tracking costs, and monitoring usage. This article covers the design of a production-grade AI gateway.

## Unified API Layer

The gateway presents a single API that abstracts provider differences:

from abc import ABC, abstractmethod

from dataclasses import dataclass

from typing import Optional

import time

@dataclass

class LLMRequest:

model: str

messages: list[dict]

max_tokens: int = 1024

temperature: float = 0.7

stream: bool = False

@dataclass

class LLMResponse:

content: str

model: str

provider: str

latency_ms: float

tokens_in: int

tokens_out: int

cost: float

class LLMProvider(ABC):

@abstractmethod

async def complete(self, request: LLMRequest) -> LLMResponse:

pass

@abstractmethod

def get_cost_per_token(self, model: str) -> tuple[float, float]:

pass

class AnthropicProvider(LLMProvider):

def **init**(self, api_key: str):

self.client = Anthropic(api_key=api_key)

async def complete(self, request: LLMRequest) -> LLMResponse:

start = time.time()

response = await self.client.messages.create(

model=request.model,

max_tokens=request.max_tokens,

temperature=request.temperature,

messages=request.messages,

)

latency = (time.time() - start) * 1000

return LLMResponse(

content=response.content[0].text,

model=request.model,

provider="anthropic",

latency_ms=latency,

tokens_in=response.usage.input_tokens,

tokens_out=response.usage.output_tokens,

cost=self._calculate_cost(response.usage),

)

class OpenAIProvider(LLMProvider):

def **init**(self, api_key: str):

self.client = OpenAI(api_key=api_key)

async def complete(self, request: LLMRequest) -> LLMResponse:

start = time.time()

response = await self.client.chat.completions.create(

model=request.model,

max_tokens=request.max_tokens,

temperature=request.temperature,

messages=request.messages,

)

latency = (time.time() - start) * 1000

return LLMResponse(

content=response.choices[0].message.content,

model=request.model,

provider="openai",

latency_ms=latency,

tokens_in=response.usage.prompt_tokens,

tokens_out=response.usage.completion_tokens,

cost=self._calculate_cost(response.usage),

)

## Load Balancing

Distribute requests across providers based on strategy:

class LoadBalancer:

def **init**(self, providers: dict[str, LLMProvider]):

self.providers = providers

self.round_robin_index = 0

async def route(self, request: LLMRequest, strategy: str = "priority") -> LLMResponse:

if strategy == "cheapest":

return await self._route_cheapest(request)

elif strategy == "fastest":

return await self._route_fastest(request)

elif strategy == "round_robin":

return await self._route_round_robin(request)

else:

return await self._route_priority(request)

async def _route_priority(self, request: LLMRequest) -> LLMResponse:

## Try primary provider first, fall back to secondary

for name in ["primary", "secondary", "fallback"]:

if name in self.providers:

try:

return await self.providers[name].complete(request)

except Exception:

continue

raise AllProvidersExhausted("All providers failed")

async def _route_cheapest(self, request: LLMRequest) -> LLMResponse:

## Route to the provider with lowest cost for comparable quality

cheap_providers = sorted(

self.providers.items(),

key=lambda p: p[1].get_cost_per_token(request.model)[0],

)

for name, provider in cheap_providers:

try:

return await provider.complete(request)

except Exception:

continue

raise AllProvidersExhausted("All providers failed")

## Fallback and Retry

When a provider fails, automatically switch to alternatives:

class FallbackHandler:

def **init**(self, load_balancer: LoadBalancer):

self.balancer = load_balancer

async def execute_with_fallback(self, request: LLMRequest, max_retries: int = 3) -> LLMResponse:

last_error = None

for attempt in range(max_retries):

try:

return await self.balancer.route(request)

except RateLimitError:

await asyncio.sleep(2 ** attempt * 2)

## Fallback to different provider

request.model = self._map_to_alternative(request.model)

except ProviderTimeoutError:

await asyncio.sleep(1)

continue

except ProviderError as e:

last_error = e

continue

raise FallbackExhausted(f"All fallbacks failed: {last_error}")

def _map_to_alternative(self, model: str) -> str:

mapping = {

"claude-sonnet-4-20260512": "gpt-4o",

"gpt-4o": "claude-sonnet-4-20260512",

"claude-haiku-20260512": "gpt-4o-mini",

}

return mapping.get(model, model)

## Cost Tracking

Track costs per user, per feature, and per request:

class CostTracker:

def **init**(self, db):

self.db = db

async def record_usage(self, response: LLMResponse, user_id: str, feature: str):

entry = {

"user_id": user_id,

"feature": feature,

"provider": response.provider,

"model": response.model,

"tokens_in": response.tokens_in,

"tokens_out": response.tokens_out,

"cost": response.cost,

"latency_ms": response.latency_ms,

"timestamp": time.time(),

}

await self.db.insert("usage_log", entry)

async def get_user_cost(self, user_id: str, period_days: int = 30) -> dict:

costs = await self.db.query(

"SELECT SUM(cost) as total, SUM(tokens_in) as in_tokens, "

"SUM(tokens_out) as out_tokens FROM usage_log "

"WHERE user_id = $1 AND timestamp > $2",

user_id, time.time() - period_days * 86400,

)

return costs[0] if costs else {"total": 0, "in_tokens": 0, "out_tokens": 0}

## Observability

Every request should produce structured telemetry:

class GatewayObservability:

def **init**(self):

self.metrics = {

"requests_total": 0,

"errors_total": 0,

"latency_histogram": [],

"cost_total": 0.0,

}

def instrument(self, handler):

async def wrapped(request: LLMRequest):

self.metrics["requests_total"] += 1

start = time.time()

try:

response = await handler(request)

self.metrics["latency_histogram"].append((time.time() - start) * 1000)

self.metrics["cost_total"] += response.cost

return response

except Exception as e:

self.metrics["errors_total"] += 1

raise

return wrapped

## Conclusion

An AI API gateway provides provider abstraction, load balancing, automatic fallback, cost tracking, and observability in a single layer. Route requests based on cost, latency, or priority. Fail over between providers transparently. Track costs per user and feature to prevent budget surprises. Expose latency, error rate, and cost metrics for dashboards. A gateway is essential for any organization using multiple LLM providers in production.

**See also:** [AI Gateway: API Routing, Rate Limiting, Fallback Models, Cost Management, and Logging](</en/ai/ai-gateway.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>), [AI Model Deployment: Strategies for Production LLM Serving](</en/ai/ai-model-deployment-strategies.html>).

**See also:** [AI Gateway: API Routing, Rate Limiting, Fallback Models, Cost Management, and Logging](</en/ai/ai-gateway.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>), [AI Model Deployment: Strategies for Production LLM Serving](</en/ai/ai-model-deployment-strategies.html>)

**See also:** [AI Gateway: API Routing, Rate Limiting, Fallback Models, Cost Management, and Logging](</en/ai/ai-gateway.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>), [AI Model Deployment: Strategies for Production LLM Serving](</en/ai/ai-model-deployment-strategies.html>)

**See also:** [AI Gateway: API Routing, Rate Limiting, Fallback Models, Cost Management, and Logging](</en/ai/ai-gateway.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>), [AI Model Deployment: Strategies for Production LLM Serving](</en/ai/ai-model-deployment-strategies.html>)

**See also:** [AI Gateway: API Routing, Rate Limiting, Fallback Models, Cost Management, and Logging](</en/ai/ai-gateway.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>), [AI Model Deployment: Strategies for Production LLM Serving](</en/ai/ai-model-deployment-strategies.html>)

**See also:** [AI Gateway: API Routing, Rate Limiting, Fallback Models, Cost Management, and Logging](</en/ai/ai-gateway.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>), [AI Model Deployment: Strategies for Production LLM Serving](</en/ai/ai-model-deployment-strategies.html>)

**See also:** [Fine-Tuning vs RAG: When to Use Each, Hybrid Approaches, Cost Comparison](</en/ai/fine-tuning-vs-rag.html>), [LLM Caching: Semantic Cache, Exact Match, TTL, Invalidation Strategies](</en/ai/llm-caching-deep.html>), [Multi-Agent Systems: Coordination, Communication, Consensus](</en/ai/multi-agent-systems.html>)

**See also:** [Fine-Tuning vs RAG: When to Use Each, Hybrid Approaches, Cost Comparison](</en/ai/fine-tuning-vs-rag.html>), [LLM Caching: Semantic Cache, Exact Match, TTL, Invalidation Strategies](</en/ai/llm-caching-deep.html>), [Multi-Agent Systems: Coordination, Communication, Consensus](</en/ai/multi-agent-systems.html>)

**See also:** [Fine-Tuning vs RAG: When to Use Each, Hybrid Approaches, Cost Comparison](</en/ai/fine-tuning-vs-rag.html>), [LLM Caching: Semantic Cache, Exact Match, TTL, Invalidation Strategies](</en/ai/llm-caching-deep.html>), [Multi-Agent Systems: Coordination, Communication, Consensus](</en/ai/multi-agent-systems.html>)

**See also:** [Fine-Tuning vs RAG: When to Use Each, Hybrid Approaches, Cost Comparison](</en/ai/fine-tuning-vs-rag.html>), [LLM Caching: Semantic Cache, Exact Match, TTL, Invalidation Strategies](</en/ai/llm-caching-deep.html>), [Multi-Agent Systems: Coordination, Communication, Consensus](</en/ai/multi-agent-systems.html>)

**See also:** [Fine-Tuning vs RAG: When to Use Each, Hybrid Approaches, Cost Comparison](</en/ai/fine-tuning-vs-rag.html>), [LLM Caching: Semantic Cache, Exact Match, TTL, Invalidation Strategies](</en/ai/llm-caching-deep.html>), [Multi-Agent Systems: Coordination, Communication, Consensus](</en/ai/multi-agent-systems.html>)
