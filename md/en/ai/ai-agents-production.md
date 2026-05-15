---
title: "Deploying AI Agents to Production"
description: "Learn agent orchestration, error handling, human-in-the-loop patterns, monitoring agent behavior, cost tracking, rate limiting, and observability strategies."
date: 2026-05-12
board: ai
url: https://dingjiu1989-hue.github.io/en/ai/ai-agents-production.html
---

# Deploying AI Agents to Production

## Deploying AI Agents to Production

## Deploying AI Agents to Production

## Deploying AI Agents to Production

## Deploying AI Agents to Production

## Deploying AI Agents to Production

## Deploying AI Agents to Production

## Deploying AI Agents to Production

## Deploying AI Agents to Production

## Deploying AI Agents to Production

## Deploying AI Agents to Production

## Deploying AI Agents to Production

## Deploying AI Agents to Production

## Deploying AI Agents to Production

### Introduction

AI agents that autonomously execute multi-step tasks are transitioning from experimental prototypes to production systems. Unlike traditional API calls, agents make decisions, use tools, and interact with external systems--introducing new challenges around reliability, cost, safety, and observability. This article covers the patterns and practices needed to deploy AI agents safely and efficiently.

### Agent Orchestration

Production agents typically follow a structured execution loop:

import asyncio

from typing import List, Optional

from dataclasses import dataclass, field

@dataclass

class AgentContext:

task: str

max_steps: int = 20

current_step: int = 0

history: List[dict] = field(default_factory=list)

tools_used: List[str] = field(default_factory=list)

total_cost: float = 0.0

class AgentOrchestrator:

def **init**(self, model: str = "claude-sonnet-4-20260512"):

self.model = model

self.max_retries = 3

self.cost_per_token = {"input": 0.000003, "output": 0.000015}

async def run(self, task: str) -> dict:

ctx = AgentContext(task=task)

while ctx.current_step < ctx.max_steps:

ctx.current_step += 1

try:

## 1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Think: decide next action

action = await self.think(ctx)

## 2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Act: execute tool or respond

if action["type"] == "tool_call":

result = await self.execute_tool(action["tool"], action["args"])

ctx.tools_used.append(action["tool"]["name"])

elif action["type"] == "final_answer":

return {

"status": "success",

"answer": action["content"],

"steps": ctx.current_step,

"tools_used": ctx.tools_used,

"total_cost": ctx.total_cost,

}

## 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Observe: store result

ctx.history.append({

"step": ctx.current_step,

"action": action,

"observation": result,

})

## 4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Cost tracking

ctx.total_cost += self._calculate_cost(action)

except ToolError as e:

## Handle tool failures with retry

await self.handle_tool_error(ctx, e)

except Exception as e:

## Catch-all for unexpected errors

await self.handle_unexpected_error(ctx, e)

return {"status": "max_steps_exceeded", "steps": ctx.max_steps}

### Error Handling and Retry Logic

Agents must gracefully handle failures across multiple dimensions:

class AgentErrorHandler:

def **init**(self):

self.retry_policies = {

"rate_limit": RetryPolicy(max_retries=5, backoff="exponential"),

"timeout": RetryPolicy(max_retries=3, backoff="linear"),

"auth_error": RetryPolicy(max_retries=1, backoff="none"),

"tool_crash": RetryPolicy(max_retries=2, backoff="constant"),

}

async def execute_with_retry(self, tool_call: dict) -> dict:

policy = self._get_policy(tool_call["tool"]["name"])

for attempt in range(policy.max_retries):

try:

return await self._execute_tool(tool_call)

except RateLimitError as e:

wait = self._calculate_backoff(attempt, policy.backoff, e.reset_at)

await self._log_retry(tool_call, attempt, wait)

await asyncio.sleep(wait)

except TimeoutError:

if attempt == policy.max_retries - 1:

return self._graceful_degradation(tool_call)

await asyncio.sleep(policy.backoff_delay * (attempt + 1))

except AuthError:

await self._refresh_credentials(tool_call["tool"]["name"])

continue

return {"error": "max_retries_exceeded", "tool": tool_call["tool"]["name"]}

def _graceful_degradation(self, tool_call: dict) -> dict:

"""Return a safe default when a tool is unavailable."""

return {

"status": "unavailable",

"message": f"{tool_call['tool']['name']} is temporarily unavailable",

"suggestion": "Try again later or use an alternative approach",

}

### Human-in-the-Loop

Critical agent actions require human approval before execution:

class HumanInTheLoop:

def **init**(self, approval_thresholds: dict):

self.thresholds = approval_thresholds

self.pending_approvals = {}

async def request_approval(

self, action: dict, context: AgentContext

) -> bool:

## Determine if approval is needed

if not self._requires_approval(action):

return True

approval_id = str(uuid.uuid4())

self.pending_approvals[approval_id] = {

"action": action,

"context": context,

"status": "pending",

"created_at": datetime.utcnow(),

}

## Notify human reviewer

await self._notify_reviewer(

approval_id=approval_id,

action_description=action["description"],

risk_level=action.get("risk", "low"),

current_state=context.history[-3:],

)

## Wait for approval (with timeout)

try:

approved = await self._wait_for_approval(approval_id, timeout=300)

self.pending_approvals[approval_id]["status"] = (

"approved" if approved else "rejected"

)

return approved

except TimeoutError:

self.pending_approvals[approval_id]["status"] = "timed_out"

return False

def _requires_approval(self, action: dict) -> bool:

return any([

action.get("risk") in self.thresholds.get("high_risk_actions", []),

action["tool"].get("name") in self.thresholds.get("protected_tools", []),

action.get("amount", 0) > self.thresholds.get("max_amount", 1000),

action.get("destructive", False),

])

### Monitoring Agent Behavior

Track agent decisions and outcomes with structured telemetry:

class AgentTelemetry:

def **init**(self):

self.metrics = MetricsClient()

self.tracer = Tracer()

def record_step(self, ctx: AgentContext, action: dict, observation: dict):

span = self.tracer.start_span("agent_step")

span.set_attributes({

"agent.step": ctx.current_step,

"agent.task_hash": hash(ctx.task),

"action.type": action["type"],

"action.tool": action.get("tool", {}).get("name", "none"),

"action.duration_ms": action.get("duration_ms", 0),

"observation.status": observation.get("status", "unknown"),

})

self.metrics.histogram(

"agent.step.duration",

value=action.get("duration_ms", 0),

tags={

"tool": action.get("tool", {}).get("name", "none"),

"status": observation.get("status", "unknown"),

},

)

span.end()

def detect_anomalies(self, ctx: AgentContext) -> List[str]:

warnings = []

## Looping detection

recent_actions = [h["action"]["tool"]["name"]

for h in ctx.history[-10:]]

if len(set(recent_actions)) < 3 and len(recent_actions) >= 5:

warnings.append("POSSIBLE_LOOP")

## Cost anomaly

if ctx.total_cost > 0.50:

warnings.append("HIGH_COST")

## Token usage

total_tokens = sum(

h["action"].get("tokens", 0) for h in ctx.history

)

if total_tokens > 50000:

warnings.append("HIGH_TOKEN_USAGE")

return warnings

### Cost Tracking and Rate Limiting

class AgentCostManager:

def **init**(self, daily_budget: float = 10.0):

self.daily_budget = daily_budget

self.daily_spend = 0.0

self.token_buckets = {}

async def check_budget(self, estimated_cost: float) -> bool:

## Reset daily counter

if self._is_new_day():

self.daily_spend = 0.0

if self.daily_spend + estimated_cost > self.daily_budget:

return False # Budget exceeded

self.daily_spend += estimated_cost

return True

async def rate_limit_check(self, tool: str) -> bool:

bucket = self.token_buckets.get(tool, TokenBucket(

capacity=10,

refill_rate=1,

refill_interval=60

))

return bucket.consume()

### Observability

Log agent decision traces for debugging and audit:

{

"timestamp": "2026-05-12T10:30:00Z",

"agent_id": "agent-payment-v3",

"session_id": "sess_abc123",

"step": 4,

"action": {

"type": "tool_call",

"tool": "stripe_charge",

"args": {"amount": 49.99, "currency": "usd"},

"reasoning": "Customer requested payment for order ord-789"

},

"observation": {

"status": "success",

"charge_id": "ch_xyz456",

"duration_ms": 234

},

"cost": {

"input_tokens": 1245,

"output_tokens": 89,

"estimated_cost": 0.005

},

"warnings": []

}

Deploy agents incrementally: start with read-only tools, add human-in-the-loop for destructive actions, and only move to fully autonomous mode after extensive monitoring and failure mode analysis.

**See also:** [AI Content Generation Workflows](</en/ai/ai-content-generation.html>), [AI Agent Frameworks Compared](</en/ai/ai-agents-frameworks.html>), [LLM API Design: Streaming, Structured Output, Error Handling, Rate Limits](</en/ai/llm-api-design.html>).

**See also:** [AI Content Generation Workflows](</en/ai/ai-content-generation.html>), [LLM API Design: Streaming, Structured Output, Error Handling, Rate Limits](</en/ai/llm-api-design.html>), [AI Agent Frameworks Compared](</en/ai/ai-agents-frameworks.html>)

**See also:** [AI Content Generation Workflows](</en/ai/ai-content-generation.html>), [LLM API Design: Streaming, Structured Output, Error Handling, Rate Limits](</en/ai/llm-api-design.html>), [AI Agent Frameworks Compared](</en/ai/ai-agents-frameworks.html>)
