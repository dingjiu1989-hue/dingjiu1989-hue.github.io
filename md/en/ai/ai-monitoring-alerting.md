---
title: "AI Monitoring and Alerting: Latency, Token Usage, Error Rates, Drift Detection"
description: "Monitor LLM applications in production: track latency percentiles, token consumption, error rates by type, and detect response drift with automated alerting."
date: 2026-02-14
board: ai
url: https://dingjiu1989-hue.github.io/en/ai/ai-monitoring-alerting.html
---

# AI Monitoring and Alerting: Latency, Token Usage, Error Rates, Drift Detection

## Introduction

AI applications introduce new monitoring dimensions beyond traditional infrastructure metrics. LLM responses can be slow, expensive, incorrect, or suddenly change behavior when providers update models. This article covers the metrics, tools, and alerting strategies for production AI monitoring, including drift detection that catches quality degradation before users complain.

## Core Metrics

Every AI application should track these foundational metrics:

from prometheus_client import Counter, Histogram, Gauge

import time

class AIMetrics:

def **init**(self):

self.request_count = Counter(

"llm_requests_total", "Total LLM requests",

["provider", "model", "status"],

)

self.latency = Histogram(

"llm_latency_ms", "LLM response latency",

["provider", "model"],

buckets=[100, 250, 500, 1000, 2000, 5000, 10000],

)

self.token_usage = Counter(

"llm_tokens_total", "Token usage",

["provider", "model", "token_type"], # token_type: input/output

)

self.cost_total = Counter(

"llm_cost_usd", "Total cost in USD",

["provider", "model"],

)

self.cache_hit_ratio = Gauge(

"llm_cache_hit_ratio", "Cache hit ratio",

["cache_level"], # cache_level: exact/semantic

)

def record_request(self, provider: str, model: str, duration_ms: float, status: str = "success"):

self.request_count.labels(provider=provider, model=model, status=status).inc()

self.latency.labels(provider=provider, model=model).observe(duration_ms)

def record_tokens(self, provider: str, model: str, input_tokens: int, output_tokens: int, cost: float):

self.token_usage.labels(provider=provider, model=model, token_type="input").inc(input_tokens)

self.token_usage.labels(provider=provider, model=model, token_type="output").inc(output_tokens)

self.cost_total.labels(provider=provider, model=model).inc(cost)

## Token Usage Tracking

Monitor token consumption per user, feature, and time period:

class TokenUsageTracker:

def **init**(self, db):

self.db = db

async def log_usage(self, user_id: str, feature: str, provider: str, model: str,

input_tokens: int, output_tokens: int, latency_ms: float):

await self.db.execute("""

INSERT INTO token_usage

(user_id, feature, provider, model, input_tokens, output_tokens,

latency_ms, cost, timestamp)

VALUES ($1, $2, $3, $4, $5, $6, $7, $8, NOW())

""", user_id, feature, provider, model, input_tokens, output_tokens,

latency_ms, self._calculate_cost(input_tokens, output_tokens, provider, model))

async def get_daily_usage(self, date: str) -> dict:

row = await self.db.fetchrow("""

SELECT SUM(input_tokens) as input, SUM(output_tokens) as output,

SUM(cost) as cost, COUNT(*) as requests

FROM token_usage WHERE DATE(timestamp) = $1

""", date)

return dict(row) if row else {"input": 0, "output": 0, "cost": 0, "requests": 0}

async def check_budget(self, user_id: str, daily_budget: float) -> bool:

row = await self.db.fetchrow("""

SELECT SUM(cost) as today_cost

FROM token_usage

WHERE user_id = $1 AND DATE(timestamp) = CURRENT_DATE

""", user_id)

return (row["today_cost"] or 0) < daily_budget

## Error Rate Monitoring

LLM applications experience distinctive error types:

from enum import Enum

class LLMErrorType(Enum):

RATE_LIMIT = "rate_limit"

CONTEXT_WINDOW = "context_window_exceeded"

CONTENT_FILTER = "content_filter_blocked"

TIMEOUT = "timeout"

INVALID_RESPONSE = "invalid_response"

PROVIDER_DOWN = "provider_down"

class ErrorMonitor:

def **init**(self, alert_threshold: float = 0.05):

self.alert_threshold = alert_threshold

self.error_counts: dict[str, int] = {}

self.total_requests: int = 0

def record_error(self, error_type: LLMErrorType, provider: str):

key = f"{error_type.value}:{provider}"

self.error_counts[key] = self.error_counts.get(key, 0) + 1

self.total_requests += 1

def check_alerts(self) -> list[str]:

alerts = []

for key, count in self.error_counts.items():

rate = count / max(self.total_requests, 1)

if rate > self.alert_threshold:

alerts.append(f"Error rate {rate:.1%} for {key} exceeds threshold {self.alert_threshold:.1%}")

return alerts

## Drift Detection

The most critical AI-specific monitoring: detect when model behavior changes:

import numpy as np

from scipy import stats

class ResponseDriftDetector:

def **init**(self, reference_embeddings: list, drift_threshold: float = 0.1):

self.reference = np.mean(reference_embeddings, axis=0)

self.threshold = drift_threshold

self.recent_embeddings: list = []

def analyze_response(self, query: str, response: str) -> dict:

emb = self._embed(response)

self.recent_embeddings.append(emb)

if len(self.recent_embeddings) >= 100:

drift_score = self._compute_drift()

self.recent_embeddings = []

return {"drift_detected": drift_score > self.threshold, "drift_score": drift_score}

return {"drift_detected": False, "drift_score": 0.0}

def _embed(self, text: str) -> np.ndarray:

return embedding_model.encode(text)

def _compute_drift(self) -> float:

recent_mean = np.mean(self.recent_embeddings, axis=0)

return float(np.linalg.norm(recent_mean - self.reference))

def detect_refusal_rate_change(self, recent_responses: list[str], baseline_rate: float) -> dict:

refusal_patterns = ["I cannot", "I'm unable", "I apologize", "cannot assist"]

current_rate = sum(

1 for r in recent_responses

if any(p in r.lower() for p in refusal_patterns)

) / len(recent_responses)

change = abs(current_rate - baseline_rate)

return {"changed": change > 0.05, "baseline": baseline_rate, "current": current_rate, "change": change}

## Alerting Configuration

class AIAlertManager:

def **init**(self, pagerduty_key: str, slack_webhook: str):

self.pagerduty = pagerduty_key

self.slack = slack_webhook

def check_and_alert(self, metrics: dict):

alerts = []

## Latency alerts

if metrics.get("p99_latency_ms", 0) > 10000:

alerts.append(Alert(severity="critical", title="High P99 latency",

message=f"P99 latency is {metrics['p99_latency_ms']}ms"))

## Error rate alerts

if metrics.get("error_rate", 0) > 0.05:

alerts.append(Alert(severity="critical", title="Elevated error rate",

message=f"Error rate is {metrics['error_rate']:.1%}"))

## Cost anomaly alerts

if metrics.get("daily_cost", 0) > metrics.get("daily_budget", float("inf")) * 1.2:

alerts.append(Alert(severity="warning", title="Cost anomaly detected",

message=f"Cost ${metrics['daily_cost']:.2f} exceeds 120% of budget"))

## Drift alerts

if metrics.get("drift_detected", False):

alerts.append(Alert(severity="warning", title="Response drift detected",

message=f"Drift score: {metrics.get('drift_score', 0):.3f}"))

return alerts

## Conclusion

AI monitoring extends traditional observability with LLM-specific metrics. Track latency percentiles (P50, P95, P99) to detect slowdowns. Monitor token usage and cost per user and feature to control spending. Categorize errors by type (rate limit, context window, content filter) to identify provider issues. Most importantly, implement drift detection to catch subtle quality changes when models are updated or system prompts are modified. Alert on all four dimensions and investigate any metric that deviates more than 20% from its baseline.

**See also:** [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>), [AI Testing Frameworks: DeepEval, Ragas, LangSmith, CI Integration](</en/ai/ai-testing-frameworks.html>), [AI Gateway: API Routing, Rate Limiting, Fallback Models, Cost Management, and Logging](</en/ai/ai-gateway.html>).

**See also:** [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>), [LLM API Design: Streaming, Structured Output, Error Handling, Rate Limits](</en/ai/llm-api-design.html>), [LLM Version Management: Model Registry, A/B Testing, Rollback](</en/ai/llm-version-management.html>)

**See also:** [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>), [LLM API Design: Streaming, Structured Output, Error Handling, Rate Limits](</en/ai/llm-api-design.html>), [LLM Version Management: Model Registry, A/B Testing, Rollback](</en/ai/llm-version-management.html>)

**See also:** [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>), [LLM API Design: Streaming, Structured Output, Error Handling, Rate Limits](</en/ai/llm-api-design.html>), [LLM Version Management: Model Registry, A/B Testing, Rollback](</en/ai/llm-version-management.html>)

**See also:** [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>), [LLM API Design: Streaming, Structured Output, Error Handling, Rate Limits](</en/ai/llm-api-design.html>), [LLM Version Management: Model Registry, A/B Testing, Rollback](</en/ai/llm-version-management.html>)

**See also:** [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>), [LLM API Design: Streaming, Structured Output, Error Handling, Rate Limits](</en/ai/llm-api-design.html>), [LLM Version Management: Model Registry, A/B Testing, Rollback](</en/ai/llm-version-management.html>)

**See also:** [AI Testing Frameworks: DeepEval, Ragas, LangSmith, CI Integration](</en/ai/ai-testing-frameworks.html>), [Tool Use Patterns: Function Calling, Structured Tools, Multi-Step Reasoning](</en/ai/tool-use-patterns.html>), [AI Red Teaming: Adversarial Testing, Jailbreak Attempts, Safety Evaluation, and Automated Testing](</en/ai/ai-red-teaming.html>)

**See also:** [AI Testing Frameworks: DeepEval, Ragas, LangSmith, CI Integration](</en/ai/ai-testing-frameworks.html>), [Tool Use Patterns: Function Calling, Structured Tools, Multi-Step Reasoning](</en/ai/tool-use-patterns.html>), [AI Red Teaming: Adversarial Testing, Jailbreak Attempts, Safety Evaluation, and Automated Testing](</en/ai/ai-red-teaming.html>)

**See also:** [AI Testing Frameworks: DeepEval, Ragas, LangSmith, CI Integration](</en/ai/ai-testing-frameworks.html>), [Tool Use Patterns: Function Calling, Structured Tools, Multi-Step Reasoning](</en/ai/tool-use-patterns.html>), [AI Red Teaming: Adversarial Testing, Jailbreak Attempts, Safety Evaluation, and Automated Testing](</en/ai/ai-red-teaming.html>)
