---
title: "Agent Memory Systems: Short-Term, Long-Term, Episodic, Semantic Memory"
description: "Design memory systems for AI agents inspired by cognitive architecture: short-term working memory, long-term storage, episodic experiences, and semantic knowled"
date: 2026-02-13
board: ai
url: https://aidev.fit/en/ai/agent-memory-systems.html
---

# Agent Memory Systems: Short-Term, Long-Term, Episodic, Semantic Memory

## Introduction

Memory is what separates stateless LLM calls from true autonomous agents. Without memory, an agent cannot learn from past interactions, maintain context across sessions, or build a model of the world. Drawing from cognitive science, agent memory can be structured into four types: short-term (working memory), long-term (persistent storage), episodic (specific experiences), and semantic (general knowledge).

## Short-Term Memory (Working Memory)

Short-term memory holds the current conversation context and immediate state:

from collections import deque

from typing import Any

class ShortTermMemory:

def **init**(self, max_tokens: int = 4096, max_messages: int = 50):

self.messages: deque[dict] = deque(maxlen=max_messages)

self.max_tokens = max_tokens

self.current_tokens = 0

def add(self, role: str, content: str):

message = {"role": role, "content": content}

estimated_tokens = len(content.split()) * 1.3

## Evict oldest messages when over token limit

while self.current_tokens + estimated_tokens > self.max_tokens:

removed = self.messages.popleft()

self.current_tokens -= len(removed["content"].split()) * 1.3

self.messages.append(message)

self.current_tokens += estimated_tokens

def get_context(self) -> list[dict]:

return list(self.messages)

def summarize_and_compress(self, llm_fn) -> str:

"""When context is full, summarize old messages to make room."""

if len(self.messages) > 30:

old_messages = list(self.messages)[:-20]

summary = llm_fn(f"Summarize these conversation messages: {old_messages}")

self.messages = deque(list(self.messages)[-20:], maxlen=50)

return summary

return ""

## Long-Term Memory

Long-term memory persists across sessions and is typically backed by a vector store:

import uuid

from datetime import datetime

import numpy as np

class LongTermMemory:

def **init**(self, vector_store, embedding_fn):

self.vector_store = vector_store

self.embedding_fn = embedding_fn

self.collection = "agent_memory"

def remember(self, content: str, importance: float = 0.5, metadata: dict = None):

"""Store a memory with importance score for selective recall."""

memory_id = str(uuid.uuid4())

embedding = self.embedding_fn(content)

self.vector_store.add(

ids=[memory_id],

embeddings=[embedding],

metadatas=[{

"content": content,

"importance": importance,

"timestamp": datetime.now().isoformat(),

**(metadata or {}),

}],

)

return memory_id

def recall(self, query: str, k: int = 5, min_importance: float = 0.0) -> list[dict]:

"""Retrieve the most relevant memories."""

query_emb = self.embedding_fn(query)

results = self.vector_store.query(

query_embeddings=[query_emb],

n_results=k,

where={"importance": {"$gte": min_importance}},

)

memories = []

for i, mem_id in enumerate(results["ids"][0]):

metadata = results["metadatas"][0][i]

memories.append({

"id": mem_id,

"content": metadata["content"],

"importance": metadata["importance"],

"timestamp": metadata["timestamp"],

"distance": results["distances"][0][i],

})

return memories

def forget(self, memory_id: str):

"""Delete a specific memory."""

self.vector_store.delete(ids=[memory_id])

def consolidate(self, llm_fn):

"""Periodically merge similar memories."""

all_memories = self.vector_store.get()

## Group similar memories and create consolidated summaries

## This runs as a background task

## Episodic Memory

Episodic memory stores specific experiences: what happened, when, and what the outcome was:

@dataclass

class Episode:

id: str

timestamp: datetime

task: str

action_sequence: list[dict]

outcome: str

reward: float

context: dict

class EpisodicMemory:

def **init**(self, storage_backend):

self.storage = storage_backend

def record_episode(self, task: str, actions: list, outcome: str, reward: float):

episode = Episode(

id=str(uuid.uuid4()),

timestamp=datetime.now(),

task=task,

action_sequence=actions,

outcome=outcome,

reward=reward,

context={},

)

self.storage.save(f"episode_{episode.id}", episode.**dict**)

return episode.id

def retrieve_similar_episodes(self, task: str, k: int = 3) -> list[Episode]:

"""Find past episodes similar to the current task."""

all_episodes = self.storage.load_all("episode_*")

scored = []

for ep in all_episodes:

similarity = self._task_similarity(task, ep["task"])

scored.append((ep, similarity))

scored.sort(key=lambda x: x[1], reverse=True)

return [Episode(**ep) for ep, _ in scored[:k]]

def _task_similarity(self, task_a: str, task_b: str) -> float:

"""Compute similarity between two task descriptions."""

emb_a = embedding_fn(task_a)

emb_b = embedding_fn(task_b)

return cosine_similarity(emb_a, emb_b)

## Semantic Memory

Semantic memory stores factual knowledge extracted from experiences:

class SemanticMemory:

def **init**(self):

self.facts: dict[str, list[dict]] = {}

self.confidence_threshold = 0.7

def add_fact(self, subject: str, predicate: str, object_: str, confidence: float):

if subject not in self.facts:

self.facts[subject] = []

self.facts[subject].append({

"predicate": predicate,

"object": object_,

"confidence": confidence,

"timestamp": datetime.now(),

})

def query_fact(self, subject: str, predicate: str = None) -> list[str]:

if subject not in self.facts:

return []

results = []

for fact in self.facts[subject]:

if predicate is None or fact["predicate"] == predicate:

if fact["confidence"] >= self.confidence_threshold:

results.append(fact["object"])

return results

def extract_facts_from_experience(self, episode: Episode, llm_fn):

"""Extract general knowledge from a specific experience."""

extraction = llm_fn(f"""

Extract factual statements from this experience.

Output as JSON array of {{"subject", "predicate", "object"}}.

Task: {episode.task}

Outcome: {episode.outcome}

""")

facts = json.loads(extraction)

for fact in facts:

self.add_fact(fact["subject"], fact["predicate"], fact["object"], confidence=0.5)

## Integrated Agent Memory

Bring all four types together in a unified memory system:

class AgentMemory:

def **init**(self, short_term_capacity=4096, long_term_store=None):

self.short_term = ShortTermMemory(max_tokens=short_term_capacity)

self.long_term = LongTermMemory(long_term_store["vector_db"], long_term_store["embed_fn"])

self.episodic = EpisodicMemory(long_term_store["kv_store"])

self.semantic = SemanticMemory()

def build_prompt_context(self, query: str) -> str:

context_parts = []

## Recent conversation

context_parts.append("=== Recent Context ===\n")

context_parts.extend(self.short_term.get_context())

## Relevant long-term memories

memories = self.long_term.recall(query, k=3)

if memories:

context_parts.append("\n=== Related Memories ===\n")

context_parts.extend([m["content"] for m in memories])

## Similar past episodes

episodes = self.episodic.retrieve_similar_episodes(query, k=2)

if episodes:

context_parts.append("\n=== Similar Past Experiences ===\n")

for ep in episodes:

context_parts.append(f"Task: {ep.task}, Outcome: {ep.outcome}")

## Relevant semantic facts

entities = extract_entities(query)

for entity in entities:

facts = self.semantic.query_fact(entity)

if facts:

context_parts.append(f"\n=== Facts about {entity} ===\n")

context_parts.extend(facts)

return "\n".join(context_parts)

## Conclusion

Agent memory systems mirror human cognitive architecture. Short-term memory maintains immediate conversation context with token-aware eviction. Long-term memory persistently stores important information with vector-based retrieval. Episodic memory records specific experiences for future reference. Semantic memory extracts and stores general knowledge from experiences. An integrated memory system combines all four types, giving agents both the immediate context and the accumulated wisdom needed for complex, long-running tasks.

**See also:** [AI Agents: Architecture and Implementation](</en/ai/ai-agents-overview.html>), [Multi-Agent Systems: Coordination, Communication, Consensus](</en/ai/multi-agent-systems.html>), [RAG Agent Patterns: Self-Query, Corrective, Adaptive Retrieval](</en/ai/rag-agent-patterns.html>).

**See also:** [AI Agents: Architecture and Implementation](</en/ai/ai-agents-overview.html>), [Multi-Agent Systems: Coordination, Communication, Consensus](</en/ai/multi-agent-systems.html>), [AI Workflow Automation: LangChain, Temporal, Event-Driven Agents](</en/ai/ai-workflow-automation.html>)

**See also:** [AI Agents: Architecture and Implementation](</en/ai/ai-agents-overview.html>), [Multi-Agent Systems: Coordination, Communication, Consensus](</en/ai/multi-agent-systems.html>), [AI Workflow Automation: LangChain, Temporal, Event-Driven Agents](</en/ai/ai-workflow-automation.html>)

**See also:** [AI Agents: Architecture and Implementation](</en/ai/ai-agents-overview.html>), [Multi-Agent Systems: Coordination, Communication, Consensus](</en/ai/multi-agent-systems.html>), [AI Workflow Automation: LangChain, Temporal, Event-Driven Agents](</en/ai/ai-workflow-automation.html>)

**See also:** [AI Agents: Architecture and Implementation](</en/ai/ai-agents-overview.html>), [Multi-Agent Systems: Coordination, Communication, Consensus](</en/ai/multi-agent-systems.html>), [AI Workflow Automation: LangChain, Temporal, Event-Driven Agents](</en/ai/ai-workflow-automation.html>)

**See also:** [AI Agents: Architecture and Implementation](</en/ai/ai-agents-overview.html>), [Multi-Agent Systems: Coordination, Communication, Consensus](</en/ai/multi-agent-systems.html>), [AI Workflow Automation: LangChain, Temporal, Event-Driven Agents](</en/ai/ai-workflow-automation.html>)

**See also:** [LLM API Design: Streaming, Structured Output, Error Handling, Rate Limits](</en/ai/llm-api-design.html>), [LLM Caching: Semantic Cache, Exact Match, TTL, Invalidation Strategies](</en/ai/llm-caching-deep.html>), [Multi-Modal RAG: Images, Tables, Documents — Chunking and Retrieval](</en/ai/multi-modal-rag.html>)

**See also:** [LLM API Design: Streaming, Structured Output, Error Handling, Rate Limits](</en/ai/llm-api-design.html>), [LLM Caching: Semantic Cache, Exact Match, TTL, Invalidation Strategies](</en/ai/llm-caching-deep.html>), [Multi-Modal RAG: Images, Tables, Documents — Chunking and Retrieval](</en/ai/multi-modal-rag.html>)

**See also:** [LLM API Design: Streaming, Structured Output, Error Handling, Rate Limits](</en/ai/llm-api-design.html>), [LLM Caching: Semantic Cache, Exact Match, TTL, Invalidation Strategies](</en/ai/llm-caching-deep.html>), [Multi-Modal RAG: Images, Tables, Documents — Chunking and Retrieval](</en/ai/multi-modal-rag.html>)

**See also:** [LLM API Design: Streaming, Structured Output, Error Handling, Rate Limits](</en/ai/llm-api-design.html>), [LLM Caching: Semantic Cache, Exact Match, TTL, Invalidation Strategies](</en/ai/llm-caching-deep.html>), [Multi-Modal RAG: Images, Tables, Documents — Chunking and Retrieval](</en/ai/multi-modal-rag.html>)

**See also:** [LLM API Design: Streaming, Structured Output, Error Handling, Rate Limits](</en/ai/llm-api-design.html>), [LLM Caching: Semantic Cache, Exact Match, TTL, Invalidation Strategies](</en/ai/llm-caching-deep.html>), [Multi-Modal RAG: Images, Tables, Documents — Chunking and Retrieval](</en/ai/multi-modal-rag.html>)

**See also:** [LLM API Design: Streaming, Structured Output, Error Handling, Rate Limits](</en/ai/llm-api-design.html>), [LLM Caching: Semantic Cache, Exact Match, TTL, Invalidation Strategies](</en/ai/llm-caching-deep.html>), [Multi-Modal RAG: Images, Tables, Documents — Chunking and Retrieval](</en/ai/multi-modal-rag.html>)

**See also:** [LLM API Design: Streaming, Structured Output, Error Handling, Rate Limits](</en/ai/llm-api-design.html>), [LLM Caching: Semantic Cache, Exact Match, TTL, Invalidation Strategies](</en/ai/llm-caching-deep.html>), [Multi-Modal RAG: Images, Tables, Documents — Chunking and Retrieval](</en/ai/multi-modal-rag.html>)

**See also:** [LLM API Design: Streaming, Structured Output, Error Handling, Rate Limits](</en/ai/llm-api-design.html>), [LLM Caching: Semantic Cache, Exact Match, TTL, Invalidation Strategies](</en/ai/llm-caching-deep.html>), [Multi-Modal RAG: Images, Tables, Documents — Chunking and Retrieval](</en/ai/multi-modal-rag.html>)

**See also:** [LLM API Design: Streaming, Structured Output, Error Handling, Rate Limits](</en/ai/llm-api-design.html>), [LLM Caching: Semantic Cache, Exact Match, TTL, Invalidation Strategies](</en/ai/llm-caching-deep.html>), [Multi-Modal RAG: Images, Tables, Documents — Chunking and Retrieval](</en/ai/multi-modal-rag.html>)

**See also:** [LLM API Design: Streaming, Structured Output, Error Handling, Rate Limits](</en/ai/llm-api-design.html>), [LLM Caching: Semantic Cache, Exact Match, TTL, Invalidation Strategies](</en/ai/llm-caching-deep.html>), [Multi-Modal RAG: Images, Tables, Documents — Chunking and Retrieval](</en/ai/multi-modal-rag.html>)

**See also:** [LLM API Design: Streaming, Structured Output, Error Handling, Rate Limits](</en/ai/llm-api-design.html>), [LLM Caching: Semantic Cache, Exact Match, TTL, Invalidation Strategies](</en/ai/llm-caching-deep.html>), [Multi-Modal RAG: Images, Tables, Documents — Chunking and Retrieval](</en/ai/multi-modal-rag.html>)

**See also:** [LLM API Design: Streaming, Structured Output, Error Handling, Rate Limits](</en/ai/llm-api-design.html>), [LLM Caching: Semantic Cache, Exact Match, TTL, Invalidation Strategies](</en/ai/llm-caching-deep.html>), [Multi-Modal RAG: Images, Tables, Documents — Chunking and Retrieval](</en/ai/multi-modal-rag.html>)

**See also:** [LLM API Design: Streaming, Structured Output, Error Handling, Rate Limits](</en/ai/llm-api-design.html>), [LLM Caching: Semantic Cache, Exact Match, TTL, Invalidation Strategies](</en/ai/llm-caching-deep.html>), [Multi-Modal RAG: Images, Tables, Documents — Chunking and Retrieval](</en/ai/multi-modal-rag.html>)

**See also:** [LLM API Design: Streaming, Structured Output, Error Handling, Rate Limits](</en/ai/llm-api-design.html>), [LLM Caching: Semantic Cache, Exact Match, TTL, Invalidation Strategies](</en/ai/llm-caching-deep.html>), [Multi-Modal RAG: Images, Tables, Documents — Chunking and Retrieval](</en/ai/multi-modal-rag.html>)

**See also:** [LLM API Design: Streaming, Structured Output, Error Handling, Rate Limits](</en/ai/llm-api-design.html>), [LLM Caching: Semantic Cache, Exact Match, TTL, Invalidation Strategies](</en/ai/llm-caching-deep.html>), [Multi-Modal RAG: Images, Tables, Documents — Chunking and Retrieval](</en/ai/multi-modal-rag.html>)

**See also:** [LLM API Design: Streaming, Structured Output, Error Handling, Rate Limits](</en/ai/llm-api-design.html>), [LLM Caching: Semantic Cache, Exact Match, TTL, Invalidation Strategies](</en/ai/llm-caching-deep.html>), [Multi-Modal RAG: Images, Tables, Documents — Chunking and Retrieval](</en/ai/multi-modal-rag.html>)

**See also:** [LLM API Design: Streaming, Structured Output, Error Handling, Rate Limits](</en/ai/llm-api-design.html>), [LLM Caching: Semantic Cache, Exact Match, TTL, Invalidation Strategies](</en/ai/llm-caching-deep.html>), [Multi-Modal RAG: Images, Tables, Documents — Chunking and Retrieval](</en/ai/multi-modal-rag.html>)
