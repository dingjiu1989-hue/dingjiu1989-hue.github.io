---
title: "Prompt Chaining: Decomposition, Parallel Execution, State Management"
description: "Master prompt chaining techniques: decompose complex tasks into steps, execute chains in parallel, manage state across calls, and handle errors gracefully."
date: 2026-02-17
board: ai
url: https://dingjiu1989-hue.github.io/en/ai/prompt-chaining.html
---

# Prompt Chaining: Decomposition, Parallel Execution, State Management

## Introduction

Prompt chaining connects multiple LLM calls into pipelines where each step refines, validates, or transforms the output of the previous one. This pattern is essential for tasks too complex for a single prompt: multi-page document generation, multi-step analysis, and workflows requiring both creativity and precision. This article covers decomposition strategies, parallel execution, and state management across chain steps.

## Task Decomposition

The first step in prompt chaining is breaking a complex task into discrete, independently verifiable steps:

def decompose_task(complex_request: str) -> list[dict]:

"""Use an LLM to plan the decomposition."""

plan = call_llm("""

Break this request into sequential steps. For each step, specify:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- step_name: short description

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- input_description: what this step needs

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- output_format: what this step produces

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- validation_criteria: how to verify correctness

Request: """ + complex_request)

return parse_steps(plan)

## Example decomposition for "write a product page"

steps = [

{"name": "extract_keywords", "input": "product_brief", "output": "keyword_list"},

{"name": "write_headline", "input": "keyword_list", "output": "headline"},

{"name": "write_description", "input": "keyword_list+headline", "output": "description"},

{"name": "write_cta", "input": "description", "output": "cta_text"},

{"name": "validate_tone", "input": "all_outputs", "output": "tone_feedback"},

]

Each step has a narrow focus. Narrow prompts produce more reliable outputs than monolithic ones because the model can concentrate its attention on one objective at a time.

## Sequential Chain Execution

Once decomposed, execute steps in order, passing outputs as inputs:

class ChainStep:

def **init**(self, name: str, prompt_template: str, inputs: list[str]):

self.name = name

self.prompt_template = prompt_template

self.inputs = inputs

class SequentialChain:

def **init**(self, steps: list[ChainStep]):

self.steps = steps

async def execute(self, initial_inputs: dict) -> dict:

state = dict(initial_inputs)

for step in self.steps:

resolved = {name: state[name] for name in step.inputs}

prompt = step.prompt_template.format(**resolved)

output = await call_llm_async(prompt)

state[step.name] = output

await self.validate_step(step, output)

return state

async def validate_step(self, step: ChainStep, output: str):

validation = call_llm(f"Validate this {step.name} output: {output}")

if "FAIL" in validation:

raise ChainValidationError(f"Step {step.name} failed validation: {validation}")

## Parallel Execution

When steps are independent, execute them concurrently to reduce wall-clock time:

import asyncio

async def parallel_chain(initial_inputs: dict, parallel_groups: list[list[ChainStep]]):

state = dict(initial_inputs)

for group in parallel_groups:

results = await asyncio.gather(

*[execute_single_step(step, state) for step in group],

return_exceptions=True,

)

for step, result in zip(group, results):

if isinstance(result, Exception):

raise ChainError(f"Step {step.name} failed: {result}")

state[step.name] = result

return state

## Example: generate three sections of a report simultaneously

parallel_groups = [

[

ChainStep("market_analysis", market_template, ["industry"]),

ChainStep("financial_analysis", financial_template, ["industry"]),

ChainStep("competitive_analysis", competitive_template, ["industry"]),

],

[

ChainStep("executive_summary", summary_template, ["market_analysis", "financial_analysis", "competitive_analysis"]),

],

]

## State Management

Chains accumulate state as they execute. A formal state machine approach prevents data loss and enables error recovery:

from dataclasses import dataclass, field

from typing import Any, Optional

@dataclass

class ChainState:

inputs: dict[str, Any] = field(default_factory=dict)

outputs: dict[str, Any] = field(default_factory=dict)

errors: dict[str, str] = field(default_factory=dict)

metadata: dict[str, Any] = field(default_factory=dict)

def set_output(self, step: str, value: Any):

self.outputs[step] = value

self.metadata[f"{step}_completed_at"] = time.time()

def get(self, key: str) -> Optional[Any]:

return self.outputs.get(key) or self.inputs.get(key)

def snapshot(self) -> dict:

return {"outputs": self.outputs, "errors": self.errors}

def restore(self, snapshot: dict):

self.outputs.update(snapshot.get("outputs", {}))

self.errors.update(snapshot.get("errors", {}))

## Error Recovery Chains

When a step fails, the chain should attempt recovery rather than aborting entirely:

async def execute_with_recovery(step: ChainStep, state: ChainState, max_retries=2):

for attempt in range(max_retries + 1):

try:

result = await execute_single_step(step, state.outputs)

state.set_output(step.name, result)

return result

except ValidationError as e:

if attempt == max_retries:

## Fallback: try a simpler version

fallback = await execute_fallback(step, state)

state.set_output(step.name, fallback)

state.errors[step.name] = f"Used fallback after {attempt} retries"

return fallback

state.metadata[f"{step.name}_retry_{attempt}"] = str(e)

## Conclusion

Prompt chaining transforms unreliable single-shot generation into reliable multi-step pipelines. Decompose complex tasks into narrow steps, execute independent steps in parallel, maintain state explicitly, and implement recovery logic for each failure mode. The result is LLM-powered workflows that match the reliability of traditional software pipelines.

**See also:** [Prompt Chaining: Building Multi-Step LLM Workflows](</en/ai/ai-prompt-chaining.html>), [Prompt Management: Versioning, Testing, Collaboration, Deployment](</en/ai/prompt-management.html>), [Prompt Engineering Guide for LLMs](</en/ai/prompt-engineering-guide.html>).

**See also:** [Prompt Chaining: Building Multi-Step LLM Workflows](</en/ai/ai-prompt-chaining.html>), [Prompt Management: Versioning, Testing, Collaboration, Deployment](</en/ai/prompt-management.html>), [Agent Planning: ReAct, Plan-and-Execute, Tree of Thoughts, Reflection](</en/ai/agent-planning.html>)

**See also:** [Prompt Chaining: Building Multi-Step LLM Workflows](</en/ai/ai-prompt-chaining.html>), [Prompt Management: Versioning, Testing, Collaboration, Deployment](</en/ai/prompt-management.html>), [Agent Planning: ReAct, Plan-and-Execute, Tree of Thoughts, Reflection](</en/ai/agent-planning.html>)

**See also:** [Prompt Chaining: Building Multi-Step LLM Workflows](</en/ai/ai-prompt-chaining.html>), [Prompt Management: Versioning, Testing, Collaboration, Deployment](</en/ai/prompt-management.html>), [Agent Planning: ReAct, Plan-and-Execute, Tree of Thoughts, Reflection](</en/ai/agent-planning.html>)

**See also:** [Prompt Chaining: Building Multi-Step LLM Workflows](</en/ai/ai-prompt-chaining.html>), [Prompt Management: Versioning, Testing, Collaboration, Deployment](</en/ai/prompt-management.html>), [Agent Planning: ReAct, Plan-and-Execute, Tree of Thoughts, Reflection](</en/ai/agent-planning.html>)

**See also:** [Prompt Chaining: Building Multi-Step LLM Workflows](</en/ai/ai-prompt-chaining.html>), [Prompt Management: Versioning, Testing, Collaboration, Deployment](</en/ai/prompt-management.html>), [Agent Planning: ReAct, Plan-and-Execute, Tree of Thoughts, Reflection](</en/ai/agent-planning.html>)

**See also:** [AI Role Definition: System Prompts, Personas, Tone Guidelines, Constraints, and Examples](</en/ai/ai-role-definition.html>), [Prompt Injection Defense: Input Sanitization, Guardrails, Permissions, and Monitoring](</en/ai/prompt-injection-defense.html>), [AI API Gateway: Load Balancing, Fallback, Cost Tracking, Observability](</en/ai/ai-api-gateway.html>)

**See also:** [AI Role Definition: System Prompts, Personas, Tone Guidelines, Constraints, and Examples](</en/ai/ai-role-definition.html>), [Prompt Injection Defense: Input Sanitization, Guardrails, Permissions, and Monitoring](</en/ai/prompt-injection-defense.html>), [AI API Gateway: Load Balancing, Fallback, Cost Tracking, Observability](</en/ai/ai-api-gateway.html>)

**See also:** [AI Role Definition: System Prompts, Personas, Tone Guidelines, Constraints, and Examples](</en/ai/ai-role-definition.html>), [Prompt Injection Defense: Input Sanitization, Guardrails, Permissions, and Monitoring](</en/ai/prompt-injection-defense.html>), [AI API Gateway: Load Balancing, Fallback, Cost Tracking, Observability](</en/ai/ai-api-gateway.html>)

**See also:** [AI Role Definition: System Prompts, Personas, Tone Guidelines, Constraints, and Examples](</en/ai/ai-role-definition.html>), [Prompt Injection Defense: Input Sanitization, Guardrails, Permissions, and Monitoring](</en/ai/prompt-injection-defense.html>), [AI API Gateway: Load Balancing, Fallback, Cost Tracking, Observability](</en/ai/ai-api-gateway.html>)

**See also:** [AI Role Definition: System Prompts, Personas, Tone Guidelines, Constraints, and Examples](</en/ai/ai-role-definition.html>), [Prompt Injection Defense: Input Sanitization, Guardrails, Permissions, and Monitoring](</en/ai/prompt-injection-defense.html>), [AI API Gateway: Load Balancing, Fallback, Cost Tracking, Observability](</en/ai/ai-api-gateway.html>)

**See also:** [AI Role Definition: System Prompts, Personas, Tone Guidelines, Constraints, and Examples](</en/ai/ai-role-definition.html>), [Prompt Injection Defense: Input Sanitization, Guardrails, Permissions, and Monitoring](</en/ai/prompt-injection-defense.html>), [AI API Gateway: Load Balancing, Fallback, Cost Tracking, Observability](</en/ai/ai-api-gateway.html>)

**See also:** [AI Role Definition: System Prompts, Personas, Tone Guidelines, Constraints, and Examples](</en/ai/ai-role-definition.html>), [Prompt Injection Defense: Input Sanitization, Guardrails, Permissions, and Monitoring](</en/ai/prompt-injection-defense.html>), [AI API Gateway: Load Balancing, Fallback, Cost Tracking, Observability](</en/ai/ai-api-gateway.html>)
