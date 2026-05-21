---
title: "Agent Planning: ReAct, Plan-and-Execute, Tree of Thoughts, Reflection"
description: "Explore agent planning frameworks: ReAct for reasoning and acting, Plan-and-Execute for task decomposition, Tree of Thoughts for exploration, and self-reflectio"
date: 2026-02-13
board: ai
url: https://dingjiu1989-hue.github.io/en/ai/agent-planning.html
---

# Agent Planning: ReAct, Plan-and-Execute, Tree of Thoughts, Reflection

## Introduction

Planning transforms LLMs from reactive responders into proactive agents that can decompose complex goals, explore solution paths, and recover from failures. This article covers four major planning frameworks: ReAct for tight coupling of reasoning and action, Plan-and-Execute for hierarchical decomposition, Tree of Thoughts for exploring multiple reasoning paths, and self-reflection for learning from mistakes.

## ReAct (Reasoning + Acting)

ReAct interleaves reasoning traces with tool calls, allowing the agent to think about what to do next based on current observations:

class ReActAgent:

def **init**(self, tools: list[dict], llm_fn):

self.tools = tools

self.llm = llm_fn

def run(self, task: str, max_steps: int = 10) -> str:

messages = [{"role": "system", "content": self._system_prompt()},

{"role": "user", "content": task}]

for step in range(max_steps):

response = self.llm(messages, tools=self.tools)

if "Final Answer:" in response:

return response.split("Final Answer:")[-1].strip()

## Parse the Thought/Action/Observation cycle

thought = self._extract(response, "Thought:")

action = self._extract_action(response)

if action:

observation = self._execute_tool(action)

messages.append({"role": "assistant", "content": response})

messages.append({"role": "system", "content": f"Observation: {observation}"})

return "Failed to complete task within step limit."

def _system_prompt(self) -> str:

return """You are a ReAct agent. For each step:

Thought: Reason about what to do next

Action: Choose a tool and specify arguments

(Wait for observation)

...repeat until done...

Final Answer: Provide the complete answer"""

def _extract_action(self, text: str) -> dict | None:

"""Parse Action: ToolName(arg1=val1, arg2=val2) from text."""

import re

match = re.search(r"Action:\s*(\w+)\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\((.+)\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\)", text)

if not match:

return None

tool_name = match.group(1)

args_text = match.group(2)

args = dict(re.findall(r"(\w+)=([^,)]+)", args_text))

return {"name": tool_name, "args": args}

def _execute_tool(self, action: dict) -> str:

for tool in self.tools:

if tool["name"] == action["name"]:

return tool["function"](<**action\["args"\]>)

return f"Error: Unknown tool '{action['name']}'"

## Plan-and-Execute

This framework separates planning from execution. A planner creates a step-by-step plan, then an executor follows it:

class PlanAndExecute:

def **init**(self, llm_fn, tools):

self.planner_llm = llm_fn

self.executor_llm = llm_fn

self.tools = tools

async def run(self, task: str) -> str:

## Phase 1: Create a plan

plan = await self._create_plan(task)

results = []

## Phase 2: Execute each step

for i, step in enumerate(plan):

print(f"Executing step {i+1}: {step['description']}")

## Check dependencies

context = self._gather_context(step, results)

result = await self._execute_step(step, context)

## Verify step completion

verified = await self._verify_step(step, result)

if not verified:

## Re-plan from this point

plan = await self._replan(task, i, plan, result)

continue

results.append({"step": step, "result": result})

## Phase 3: Synthesize final answer

return await self._synthesize(task, plan, results)

async def _create_plan(self, task: str) -> list[dict]:

response = self.planner_llm(f"""

Create a step-by-step plan for: {task}

For each step, specify:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- description: what to do

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- tool: which tool to use (or 'none')

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- dependencies: which step numbers this step depends on

Output as a JSON array.

""")

return json.loads(response)

async def _replan(self, original_task: str, failed_step: int, old_plan: list, error: str) -> list:

response = self.planner_llm(f"""

Step {failed_step} failed: {error}

Original plan: {old_plan}

Original task: {original_task}

Create a revised plan starting from the failure point.

""")

return json.loads(response)

## Tree of Thoughts (ToT)

ToT explores multiple reasoning paths simultaneously, evaluating each branch:

class TreeOfThoughts:

def **init**(self, llm_fn, branches: int = 3, depth: int = 3):

self.llm = llm_fn

self.branches = branches

self.depth = depth

def solve(self, problem: str) -> str:

## Initialize the tree with root thoughts

candidates = self._generate_thoughts(problem, [])

best_path = None

best_score = float("-inf")

for level in range(self.depth):

## Evaluate each candidate

scored = []

for thought in candidates:

state = thought # The thought is the reasoning so far

score = self._evaluate_thought(problem, state)

scored.append((state, score))

if score > best_score and level == self.depth - 1:

best_score = score

best_path = state

## Select top-k candidates for expansion

scored.sort(key=lambda x: x[1], reverse=True)

top_candidates = scored[:self.branches]

if level < self.depth - 1:

## Generate next thoughts from top candidates

candidates = []

for state, _ in top_candidates:

next_thoughts = self._generate_thoughts(problem, state)

candidates.extend(next_thoughts)

return best_path or "No solution found."

def _generate_thoughts(self, problem: str, current_state: list[str]) -> list[list[str]]:

context = "\n".join(current_state) if current_state else "No reasoning yet."

response = self.llm(f"""

Problem: {problem}

Current reasoning: {context}

Generate {self.branches} different next steps in reasoning.

Each should be a plausible continuation. Be diverse.

""")

## Parse response into multiple thought continuations

return [current_state + [t] for t in parse_thoughts(response)]

def _evaluate_thought(self, problem: str, state: list[str]) -> float:

context = "\n".join(state)

score = self.llm(f"""

Problem: {problem}

Reasoning so far: {context}

Rate the promise of this reasoning path on a scale of 0 to 1.

Output ONLY a number.

""")

return float(score.strip())

## Reflection

Reflection enables agents to learn from their mistakes during execution:

class ReflectiveAgent:

def **init**(self, llm_fn, tools):

self.llm = llm_fn

self.tools = tools

self.reflection_log = []

async def run(self, task: str) -> str:

max_attempts = 3

for attempt in range(max_attempts):

result = await self._attempt(task)

if self._is_successful(result):

return result["output"]

## Reflect on the failure

reflection = self._reflect(task, result)

self.reflection_log.append(reflection)

## Update strategy based on reflection

task = self._revise_task(task, reflection)

return "Failed after multiple attempts."

def _reflect(self, task: str, result: dict) -> str:

return self.llm(f"""

Task: {task}

What went wrong: {result.get('error', 'Unknown error')}

Actions taken: {result.get('actions', [])}

Partial output: {result.get('partial_output', '')}

Reflect on:

1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. What was the root cause of the failure?

2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. What should be done differently next time?

3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Is there missing information needed?

Reflection:

""")

def _revise_task(self, task: str, reflection: str) -> str:

return self.llm(f"""

Original task: {task}

After reflecting: {reflection}

Revise the task description to incorporate lessons learned

and avoid repeating the same mistake.

""")

## Choosing a Framework

| Framework | Best For | When to Use |

|-----------|----------|-------------|

| ReAct | Interactive tasks with tools | Standard agent tasks requiring reasoning |

| Plan-and-Execute | Complex multi-step tasks | When the plan is knowable upfront |

| Tree of Thoughts | Creative/exploratory tasks | When multiple approaches are valid |

| Reflection | Error-prone environments | When learning from mistakes is critical |

## Conclusion

Agent planning frameworks provide structure for LLM reasoning. ReAct couples reasoning with tool use for interactive tasks. Plan-and-Execute separates planning from execution for complex workflows. Tree of Thoughts explores multiple reasoning paths for problems with branching solutions. Reflection enables continuous improvement by learning from failures. In practice, combine these patterns: use ReAct for execution, Plan-and-Execute for structure, ToT for exploration, and Reflection for improvement.

**See also:** [AI Agents: Architecture and Implementation](</en/ai/ai-agents-overview.html>), [RAG Agent Patterns: Self-Query, Corrective, Adaptive Retrieval](</en/ai/rag-agent-patterns.html>), [Tool Use Patterns: Function Calling, Structured Tools, Multi-Step Reasoning](</en/ai/tool-use-patterns.html>).

**See also:** [RAG Agent Patterns: Self-Query, Corrective, Adaptive Retrieval](</en/ai/rag-agent-patterns.html>), [AI Agents: Architecture and Implementation](</en/ai/ai-agents-overview.html>), [Agent Memory Systems: Short-Term, Long-Term, Episodic, Semantic Memory](</en/ai/agent-memory-systems.html>)

**See also:** [RAG Agent Patterns: Self-Query, Corrective, Adaptive Retrieval](</en/ai/rag-agent-patterns.html>), [AI Agents: Architecture and Implementation](</en/ai/ai-agents-overview.html>), [Agent Memory Systems: Short-Term, Long-Term, Episodic, Semantic Memory](</en/ai/agent-memory-systems.html>)

**See also:** [RAG Agent Patterns: Self-Query, Corrective, Adaptive Retrieval](</en/ai/rag-agent-patterns.html>), [AI Agents: Architecture and Implementation](</en/ai/ai-agents-overview.html>), [Agent Memory Systems: Short-Term, Long-Term, Episodic, Semantic Memory](</en/ai/agent-memory-systems.html>)

**See also:** [RAG Agent Patterns: Self-Query, Corrective, Adaptive Retrieval](</en/ai/rag-agent-patterns.html>), [AI Agents: Architecture and Implementation](</en/ai/ai-agents-overview.html>), [Agent Memory Systems: Short-Term, Long-Term, Episodic, Semantic Memory](</en/ai/agent-memory-systems.html>)

**See also:** [RAG Agent Patterns: Self-Query, Corrective, Adaptive Retrieval](</en/ai/rag-agent-patterns.html>), [AI Agents: Architecture and Implementation](</en/ai/ai-agents-overview.html>), [Agent Memory Systems: Short-Term, Long-Term, Episodic, Semantic Memory](</en/ai/agent-memory-systems.html>)

**See also:** [Tool Use Patterns: Function Calling, Structured Tools, Multi-Step Reasoning](</en/ai/tool-use-patterns.html>), [AI Gateway: API Routing, Rate Limiting, Fallback Models, Cost Management, and Logging](</en/ai/ai-gateway.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>)

**See also:** [Tool Use Patterns: Function Calling, Structured Tools, Multi-Step Reasoning](</en/ai/tool-use-patterns.html>), [AI Gateway: API Routing, Rate Limiting, Fallback Models, Cost Management, and Logging](</en/ai/ai-gateway.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>)

**See also:** [Tool Use Patterns: Function Calling, Structured Tools, Multi-Step Reasoning](</en/ai/tool-use-patterns.html>), [AI Gateway: API Routing, Rate Limiting, Fallback Models, Cost Management, and Logging](</en/ai/ai-gateway.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>)

**See also:** [Tool Use Patterns: Function Calling, Structured Tools, Multi-Step Reasoning](</en/ai/tool-use-patterns.html>), [AI Gateway: API Routing, Rate Limiting, Fallback Models, Cost Management, and Logging](</en/ai/ai-gateway.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>)

**See also:** [Tool Use Patterns: Function Calling, Structured Tools, Multi-Step Reasoning](</en/ai/tool-use-patterns.html>), [AI Gateway: API Routing, Rate Limiting, Fallback Models, Cost Management, and Logging](</en/ai/ai-gateway.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>)

**See also:** [Tool Use Patterns: Function Calling, Structured Tools, Multi-Step Reasoning](</en/ai/tool-use-patterns.html>), [AI Gateway: API Routing, Rate Limiting, Fallback Models, Cost Management, and Logging](</en/ai/ai-gateway.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>)

**See also:** [Tool Use Patterns: Function Calling, Structured Tools, Multi-Step Reasoning](</en/ai/tool-use-patterns.html>), [AI Gateway: API Routing, Rate Limiting, Fallback Models, Cost Management, and Logging](</en/ai/ai-gateway.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>)

**See also:** [Tool Use Patterns: Function Calling, Structured Tools, Multi-Step Reasoning](</en/ai/tool-use-patterns.html>), [AI Gateway: API Routing, Rate Limiting, Fallback Models, Cost Management, and Logging](</en/ai/ai-gateway.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>)

**See also:** [Tool Use Patterns: Function Calling, Structured Tools, Multi-Step Reasoning](</en/ai/tool-use-patterns.html>), [AI Gateway: API Routing, Rate Limiting, Fallback Models, Cost Management, and Logging](</en/ai/ai-gateway.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>)

**See also:** [Tool Use Patterns: Function Calling, Structured Tools, Multi-Step Reasoning](</en/ai/tool-use-patterns.html>), [AI Gateway: API Routing, Rate Limiting, Fallback Models, Cost Management, and Logging](</en/ai/ai-gateway.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>)

**See also:** [Tool Use Patterns: Function Calling, Structured Tools, Multi-Step Reasoning](</en/ai/tool-use-patterns.html>), [AI Gateway: API Routing, Rate Limiting, Fallback Models, Cost Management, and Logging](</en/ai/ai-gateway.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>)
