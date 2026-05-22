---
title: "Multi-Agent Systems: Coordination, Communication, Consensus"
description: "Design multi-agent systems with LLM-powered agents: coordination patterns, inter-agent communication protocols, consensus mechanisms, and conflict resolution st"
date: 2026-02-17
board: ai
url: https://aidev.fit/en/ai/multi-agent-systems.html
---

# Multi-Agent Systems: Coordination, Communication, Consensus

## Introduction

A single LLM agent has limitations: finite context windows, single perspective bias, and vulnerability to cascading errors. Multi-agent systems address these by distributing work across specialized agents that communicate, coordinate, and reach consensus. This article covers the architectural patterns for building effective multi-agent systems.

## Agent Roles and Specialization

Each agent should have a narrow, defined role:

@dataclass

class AgentSpec:

name: str

role: str

system_prompt: str

tools: list[dict]

model: str

class Agent:

def **init**(self, spec: AgentSpec, llm_fn):

self.spec = spec

self.llm = llm_fn

self.message_history = [{"role": "system", "content": spec.system_prompt}]

async def process(self, task: str, context: str = "") -> str:

messages = self.message_history + [{"role": "user", "content": f"{context}\n\nTask: {task}"}]

response = self.llm(messages, tools=self.spec.tools)

self.message_history.append({"role": "assistant", "content": response})

return response

## Define specialized agents

researcher = Agent(AgentSpec(

name="Researcher",

role="Information retrieval and fact-checking",

system_prompt="You are a research specialist. Find accurate information and verify facts. Cite all sources.",

tools=[search_tool, web_scrape_tool],

model="claude-sonnet-4-20260512",

))

writer = Agent(AgentSpec(

name="Writer",

role="Content creation and editing",

system_prompt="You are a technical writer. Produce clear, well-structured content. Adapt tone to the audience.",

tools=[grammar_check_tool, style_guide_tool],

model="claude-sonnet-4-20260512",

))

critic = Agent(AgentSpec(

name="Critic",

role="Quality assurance and review",

system_prompt="You are a critical reviewer. Find errors, inconsistencies, and areas for improvement. Be thorough.",

tools=[],

model="claude-opus-4-20260512", # Stronger model for evaluation

))

## Communication Protocols

Agents communicate through structured messages:

from enum import Enum

from datetime import datetime

class MessageType(Enum):

TASK = "task"

RESULT = "result"

QUERY = "query"

RESPONSE = "response"

FEEDBACK = "feedback"

COORDINATION = "coordination"

@dataclass

class AgentMessage:

id: str

sender: str

recipients: list[str]

type: MessageType

content: str

metadata: dict = None

timestamp: str = None

def **post_init**(self):

if self.timestamp is None:

self.timestamp = datetime.now().isoformat()

class MessageBus:

def **init**(self):

self.queues: dict[str, list[AgentMessage]] = {}

self.broadcast_log: list[AgentMessage] = []

def send(self, message: AgentMessage):

for recipient in message.recipients:

if recipient not in self.queues:

self.queues[recipient] = []

self.queues[recipient].append(message)

if not message.recipients:

self.broadcast_log.append(message)

def receive(self, agent_name: str) -> list[AgentMessage]:

return self.queues.pop(agent_name, [])

def broadcast(self, message: AgentMessage):

for agent in self.queues:

self.queues[agent].append(message)

self.broadcast_log.append(message)

## Orchestration Patterns

## Sequential Handoff

One agent passes results to the next in a pipeline:

class SequentialOrchestrator:

def **init**(self, agents: list[Agent], bus: MessageBus):

self.agents = agents

self.bus = bus

async def run(self, initial_task: str) -> str:

current_output = initial_task

for i, agent in enumerate(self.agents):

result = await agent.process(current_output)

current_output = result

if i < len(self.agents) - 1:

self.bus.send(AgentMessage(

id=f"handoff_{i}",

sender=agent.spec.name,

recipients=[self.agents[i+1].spec.name],

type=MessageType.TASK,

content=result,

))

return current_output

## Debate and Consensus

Multiple agents work on the same problem and then converge:

class DebateOrchestrator:

def **init**(self, agents: list[Agent], rounds: int = 3):

self.agents = agents

self.rounds = rounds

async def debate(self, problem: str) -> str:

positions = {a.spec.name: await a.process(problem) for a in self.agents}

for round_num in range(self.rounds):

## Share positions

summary = "\n".join(f"{name}: {pos}" for name, pos in positions.items())

## Each agent critiques and refines

new_positions = {}

for agent in self.agents:

critique = await agent.process(

f"Round {round_num + 1}. Review these positions and refine your own:\n{summary}",

context=f"Your previous position: {positions[agent.spec.name]}"

)

new_positions[agent.spec.name] = critique

positions = new_positions

## Final consensus

consensus_agent = self.agents[0]

summary = "\n".join(f"{name}: {pos}" for name, pos in positions.items())

consensus = await consensus_agent.process(

f"Based on all perspectives, produce a final consensus answer:\n{summary}"

)

return consensus

## Manager-Worker Pattern

A manager agent decomposes tasks and delegates to workers:

class ManagerWorkerOrchestrator:

def **init**(self, manager: Agent, workers: list[Agent], bus: MessageBus):

self.manager = manager

self.workers = workers

self.bus = bus

async def run(self, task: str) -> str:

## Manager creates a plan

plan = await self.manager.process(f"Decompose this task into sub-tasks and assign to workers: {task}")

sub_tasks = self._parse_plan(plan)

## Distribute to workers

worker_futures = []

for sub_task in sub_tasks:

worker = self._select_worker(sub_task)

future = worker.process(sub_task["description"])

worker_futures.append(future)

## Collect results

results = await asyncio.gather(*worker_futures)

## Manager synthesizes final output

results_text = "\n".join(f"{st['id']}: {r}" for st, r in zip(sub_tasks, results))

final = await self.manager.process(

f"Synthesize these results into a coherent output:\n{results_text}",

context=f"Original task: {task}"

)

return final

def _select_worker(self, sub_task: dict) -> Agent:

skill = sub_task.get("required_skill", "general")

for worker in self.workers:

if skill in worker.spec.role.lower():

return worker

return self.workers[0]

## Consensus with Voting

When agents disagree, a voting mechanism resolves conflicts:

def weighted_vote(proposals: list[dict], agent_weights: dict[str, float]) -> dict:

"""Weighted voting: each agent's vote is weighted by its reliability."""

vote_counts = {}

for proposal in proposals:

key = proposal["solution"]

weight = agent_weights.get(proposal["agent"], 1.0)

vote_counts[key] = vote_counts.get(key, 0) + weight

winner = max(vote_counts, key=vote_counts.get)

return {"winner": winner, "confidence": vote_counts[winner] / sum(vote_counts.values())}

## Conclusion

Multi-agent systems distribute intelligence across specialized agents. Sequential handoff is suitable for linear pipelines. Debate and consensus produces higher-quality answers by challenging assumptions. Manager-worker scales to complex tasks by decomposing and delegating. Choose your coordination pattern based on the task: sequential for well-defined steps, debate for decisions requiring multiple perspectives, and manager-worker for complex projects with parallelizable sub-tasks.

**See also:** [AI Agents: Architecture and Implementation](</en/ai/ai-agents-overview.html>), [Agent Memory Systems: Short-Term, Long-Term, Episodic, Semantic Memory](</en/ai/agent-memory-systems.html>), [AI Workflow Automation: LangChain, Temporal, Event-Driven Agents](</en/ai/ai-workflow-automation.html>).

**See also:** [AI Workflow Automation: LangChain, Temporal, Event-Driven Agents](</en/ai/ai-workflow-automation.html>), [AI Agents: Architecture and Implementation](</en/ai/ai-agents-overview.html>), [Agent Memory Systems: Short-Term, Long-Term, Episodic, Semantic Memory](</en/ai/agent-memory-systems.html>)

**See also:** [AI Workflow Automation: LangChain, Temporal, Event-Driven Agents](</en/ai/ai-workflow-automation.html>), [AI Agents: Architecture and Implementation](</en/ai/ai-agents-overview.html>), [Agent Memory Systems: Short-Term, Long-Term, Episodic, Semantic Memory](</en/ai/agent-memory-systems.html>)

**See also:** [AI Workflow Automation: LangChain, Temporal, Event-Driven Agents](</en/ai/ai-workflow-automation.html>), [AI Agents: Architecture and Implementation](</en/ai/ai-agents-overview.html>), [Agent Memory Systems: Short-Term, Long-Term, Episodic, Semantic Memory](</en/ai/agent-memory-systems.html>)

**See also:** [AI Workflow Automation: LangChain, Temporal, Event-Driven Agents](</en/ai/ai-workflow-automation.html>), [AI Agents: Architecture and Implementation](</en/ai/ai-agents-overview.html>), [Agent Memory Systems: Short-Term, Long-Term, Episodic, Semantic Memory](</en/ai/agent-memory-systems.html>)

**See also:** [AI Workflow Automation: LangChain, Temporal, Event-Driven Agents](</en/ai/ai-workflow-automation.html>), [AI Agents: Architecture and Implementation](</en/ai/ai-agents-overview.html>), [Agent Memory Systems: Short-Term, Long-Term, Episodic, Semantic Memory](</en/ai/agent-memory-systems.html>)

**See also:** [AI API Gateway: Load Balancing, Fallback, Cost Tracking, Observability](</en/ai/ai-api-gateway.html>), [Prompt Chaining: Building Multi-Step LLM Workflows](</en/ai/ai-prompt-chaining.html>), [AI Caching Strategies: Semantic Caching, Cache Invalidation, Cost Reduction, and Latency Improvement](</en/ai/ai-caching-strategies.html>)

**See also:** [AI API Gateway: Load Balancing, Fallback, Cost Tracking, Observability](</en/ai/ai-api-gateway.html>), [Prompt Chaining: Building Multi-Step LLM Workflows](</en/ai/ai-prompt-chaining.html>), [AI Caching Strategies: Semantic Caching, Cache Invalidation, Cost Reduction, and Latency Improvement](</en/ai/ai-caching-strategies.html>)

**See also:** [AI API Gateway: Load Balancing, Fallback, Cost Tracking, Observability](</en/ai/ai-api-gateway.html>), [Prompt Chaining: Building Multi-Step LLM Workflows](</en/ai/ai-prompt-chaining.html>), [AI Caching Strategies: Semantic Caching, Cache Invalidation, Cost Reduction, and Latency Improvement](</en/ai/ai-caching-strategies.html>)

**See also:** [AI API Gateway: Load Balancing, Fallback, Cost Tracking, Observability](</en/ai/ai-api-gateway.html>), [Prompt Chaining: Building Multi-Step LLM Workflows](</en/ai/ai-prompt-chaining.html>), [AI Caching Strategies: Semantic Caching, Cache Invalidation, Cost Reduction, and Latency Improvement](</en/ai/ai-caching-strategies.html>)

**See also:** [AI API Gateway: Load Balancing, Fallback, Cost Tracking, Observability](</en/ai/ai-api-gateway.html>), [Prompt Chaining: Building Multi-Step LLM Workflows](</en/ai/ai-prompt-chaining.html>), [AI Caching Strategies: Semantic Caching, Cache Invalidation, Cost Reduction, and Latency Improvement](</en/ai/ai-caching-strategies.html>)

**See also:** [AI API Gateway: Load Balancing, Fallback, Cost Tracking, Observability](</en/ai/ai-api-gateway.html>), [Prompt Chaining: Building Multi-Step LLM Workflows](</en/ai/ai-prompt-chaining.html>), [AI Caching Strategies: Semantic Caching, Cache Invalidation, Cost Reduction, and Latency Improvement](</en/ai/ai-caching-strategies.html>)

**See also:** [AI API Gateway: Load Balancing, Fallback, Cost Tracking, Observability](</en/ai/ai-api-gateway.html>), [Prompt Chaining: Building Multi-Step LLM Workflows](</en/ai/ai-prompt-chaining.html>), [AI Caching Strategies: Semantic Caching, Cache Invalidation, Cost Reduction, and Latency Improvement](</en/ai/ai-caching-strategies.html>)

**See also:** [AI API Gateway: Load Balancing, Fallback, Cost Tracking, Observability](</en/ai/ai-api-gateway.html>), [Prompt Chaining: Building Multi-Step LLM Workflows](</en/ai/ai-prompt-chaining.html>), [AI Caching Strategies: Semantic Caching, Cache Invalidation, Cost Reduction, and Latency Improvement](</en/ai/ai-caching-strategies.html>)

**See also:** [AI API Gateway: Load Balancing, Fallback, Cost Tracking, Observability](</en/ai/ai-api-gateway.html>), [Prompt Chaining: Building Multi-Step LLM Workflows](</en/ai/ai-prompt-chaining.html>), [AI Caching Strategies: Semantic Caching, Cache Invalidation, Cost Reduction, and Latency Improvement](</en/ai/ai-caching-strategies.html>)

**See also:** [AI API Gateway: Load Balancing, Fallback, Cost Tracking, Observability](</en/ai/ai-api-gateway.html>), [Prompt Chaining: Building Multi-Step LLM Workflows](</en/ai/ai-prompt-chaining.html>), [AI Caching Strategies: Semantic Caching, Cache Invalidation, Cost Reduction, and Latency Improvement](</en/ai/ai-caching-strategies.html>)

**See also:** [AI API Gateway: Load Balancing, Fallback, Cost Tracking, Observability](</en/ai/ai-api-gateway.html>), [Prompt Chaining: Building Multi-Step LLM Workflows](</en/ai/ai-prompt-chaining.html>), [AI Caching Strategies: Semantic Caching, Cache Invalidation, Cost Reduction, and Latency Improvement](</en/ai/ai-caching-strategies.html>)

**See also:** [AI API Gateway: Load Balancing, Fallback, Cost Tracking, Observability](</en/ai/ai-api-gateway.html>), [Prompt Chaining: Building Multi-Step LLM Workflows](</en/ai/ai-prompt-chaining.html>), [AI Caching Strategies: Semantic Caching, Cache Invalidation, Cost Reduction, and Latency Improvement](</en/ai/ai-caching-strategies.html>)

**See also:** [AI API Gateway: Load Balancing, Fallback, Cost Tracking, Observability](</en/ai/ai-api-gateway.html>), [Prompt Chaining: Building Multi-Step LLM Workflows](</en/ai/ai-prompt-chaining.html>), [AI Caching Strategies: Semantic Caching, Cache Invalidation, Cost Reduction, and Latency Improvement](</en/ai/ai-caching-strategies.html>)

**See also:** [AI API Gateway: Load Balancing, Fallback, Cost Tracking, Observability](</en/ai/ai-api-gateway.html>), [Prompt Chaining: Building Multi-Step LLM Workflows](</en/ai/ai-prompt-chaining.html>), [AI Caching Strategies: Semantic Caching, Cache Invalidation, Cost Reduction, and Latency Improvement](</en/ai/ai-caching-strategies.html>)

**See also:** [AI API Gateway: Load Balancing, Fallback, Cost Tracking, Observability](</en/ai/ai-api-gateway.html>), [Prompt Chaining: Building Multi-Step LLM Workflows](</en/ai/ai-prompt-chaining.html>), [AI Caching Strategies: Semantic Caching, Cache Invalidation, Cost Reduction, and Latency Improvement](</en/ai/ai-caching-strategies.html>)

**See also:** [AI API Gateway: Load Balancing, Fallback, Cost Tracking, Observability](</en/ai/ai-api-gateway.html>), [Prompt Chaining: Building Multi-Step LLM Workflows](</en/ai/ai-prompt-chaining.html>), [AI Caching Strategies: Semantic Caching, Cache Invalidation, Cost Reduction, and Latency Improvement](</en/ai/ai-caching-strategies.html>)
