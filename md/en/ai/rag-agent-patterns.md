---
title: "RAG Agent Patterns: Self-Query, Corrective, Adaptive Retrieval"
description: "Explore RAG agent patterns that go beyond simple retrieval: self-querying agents, corrective RAG with verification, and adaptive retrieval strategies for comple"
date: 2026-02-18
board: ai
url: https://dingjiu1989-hue.github.io/en/ai/rag-agent-patterns.html
---

# RAG Agent Patterns: Self-Query, Corrective, Adaptive Retrieval

## Introduction

Basic RAG retrieves documents once and generates an answer. RAG agents take this further: they decide when to retrieve, formulate their own queries, verify retrieved information, and adapt their strategy based on the question complexity. This article covers three agentic RAG patterns that dramatically improve retrieval quality.

## Self-Query RAG

Instead of using the raw user question as the search query, the agent generates an optimized query:

def self_query_rag(question: str) -> str:

## Step 1: Generate search query

search_query = call_llm(f"""

Generate an optimal search query for a vector database.

Extract key terms, rephrase questions as search statements.

Output ONLY the search query, nothing else.

User question: {question}

""")

## Step 2: Retrieve using optimized query

chunks = vector_search(search_query, k=5)

## Step 3: Generate answer from retrieved chunks

context = "\n\n".join(chunks)

answer = call_llm(f"""

Answer the question based on the context below.

If the context does not contain enough information, say so.

Context: {context}

Question: {question}

""")

return answer

The self-query pattern resolves the fundamental mismatch between natural language questions and keyword-optimized search indices. A question like "How do I handle rate limiting?" becomes the search query "rate limiting strategies implementation patterns error handling."

## Corrective RAG (CRAG)

Corrective RAG adds a verification step between retrieval and generation. If retrieved documents are irrelevant, the agent takes corrective action:

def corrective_rag(question: str, max_attempts: int = 3) -> str:

for attempt in range(max_attempts):

## Retrieve

chunks = vector_search(question, k=5)

## Score relevance

relevance_scores = []

for chunk in chunks:

score = call_llm(f"""

On a scale of 0-10, how relevant is this document to:

'{question}'

Respond with only a number.

""", chunk)

relevance_scores.append(float(score.strip()))

avg_relevance = sum(relevance_scores) / len(relevance_scores)

if avg_relevance >= 7:

## High confidence: generate answer

context = "\n\n".join(chunks[:3])

return generate_answer(question, context)

elif avg_relevance >= 4:

## Medium confidence: try query decomposition

sub_questions = decompose_question(question)

sub_answers = [corrective_rag(sq) for sq in sub_questions]

return synthesize_answers(question, sub_answers)

else:

## Low confidence: reformulate query

question = reformulate_query(question, chunks)

return "Unable to find sufficient information to answer this question."

CRAG prevents the "hallucinate confidently from irrelevant context" failure mode common in naive RAG. Each attempt either improves the query or escalates to a more sophisticated strategy.

## Adaptive Retrieval

Adaptive retrieval dynamically selects the retrieval strategy based on question characteristics:

class AdaptiveRetriever:

def **init**(self):

self.strategies = {

"factoid": self.factoid_retrieval,

"comparison": self.comparison_retrieval,

"procedural": self.procedural_retrieval,

"analytical": self.analytical_retrieval,

}

def retrieve(self, question: str) -> list[str]:

## Classify the question type

q_type = call_llm(f"""

Classify this question as one of: factoid, comparison, procedural, analytical

Respond with only the type name.

Question: {question}

""")

strategy = self.strategies.get(q_type.strip(), self.factoid_retrieval)

return strategy(question)

def factoid_retrieval(self, question: str) -> list[str]:

## Simple direct retrieval

return vector_search(question, k=3)

def comparison_retrieval(self, question: str) -> list[str]:

## Retrieve documents for each side of the comparison

entities = extract_comparison_entities(question)

docs = []

for entity in entities:

docs.extend(vector_search(entity, k=3))

return docs[:6]

def procedural_retrieval(self, question: str) -> list[str]:

## Step-by-step retrieval

steps = decompose_steps(question)

docs = []

for step in steps:

docs.extend(vector_search(step, k=2))

return docs[:8]

def analytical_retrieval(self, question: str) -> list[str]:

## Retrieve broadly then narrow

broad = vector_search(question, k=20)

reranked = rerank(question, broad)

return reranked[:5]

## Multi-Hop Retrieval

Some questions require retrieving information about entities discovered during retrieval:

def multi_hop_rag(question: str, max_hops=3):

context_chunks = []

current_query = question

for hop in range(max_hops):

chunks = vector_search(current_query, k=3)

context_chunks.extend(chunks)

## Check if we need another hop

needs_more = call_llm(f"""

Can you answer '{question}' with the information retrieved so far?

Answer YES or NO. If NO, specify what additional information is needed.

Context so far: {' '.join(context_chunks[:5])}

""")

if needs_more.startswith("YES"):

break

## Extract the next search target

current_query = call_llm(f"""

What additional information do we need to answer '{question}'?

Output a single search query.

Context: {' '.join(context_chunks[-3:])}

""")

return generate_answer(question, context_chunks)

## Conclusion

RAG agents extend basic retrieval with reasoning. Self-query RAG optimizes the search query for better retrieval. Corrective RAG verifies retrieved content and adapts when relevance is low. Adaptive retrieval selects the strategy that fits the question type. Multi-hop retrieval follows information chains across documents. These patterns transform RAG from a single-pass lookup into an intelligent research process.

**See also:** [Multi-Agent Systems: Coordination, Communication, Consensus](</en/ai/multi-agent-systems.html>), [RAG Pipeline Optimization: Production Best Practices](</en/ai/rag-pipeline-optimization.html>), [Agent Planning: ReAct, Plan-and-Execute, Tree of Thoughts, Reflection](</en/ai/agent-planning.html>).

**See also:** [AI Workflow Automation: LangChain, Temporal, Event-Driven Agents](</en/ai/ai-workflow-automation.html>), [Multi-Modal RAG: Images, Tables, Documents — Chunking and Retrieval](</en/ai/multi-modal-rag.html>), [RAG Retrieval Optimization: Hybrid Search, Re-Ranking, Query Transformation](</en/ai/rag-retrieval-optimization.html>)

**See also:** [AI Workflow Automation: LangChain, Temporal, Event-Driven Agents](</en/ai/ai-workflow-automation.html>), [Multi-Modal RAG: Images, Tables, Documents — Chunking and Retrieval](</en/ai/multi-modal-rag.html>), [RAG Retrieval Optimization: Hybrid Search, Re-Ranking, Query Transformation](</en/ai/rag-retrieval-optimization.html>)

**See also:** [AI Workflow Automation: LangChain, Temporal, Event-Driven Agents](</en/ai/ai-workflow-automation.html>), [Multi-Modal RAG: Images, Tables, Documents — Chunking and Retrieval](</en/ai/multi-modal-rag.html>), [RAG Retrieval Optimization: Hybrid Search, Re-Ranking, Query Transformation](</en/ai/rag-retrieval-optimization.html>)

**See also:** [AI Workflow Automation: LangChain, Temporal, Event-Driven Agents](</en/ai/ai-workflow-automation.html>), [Multi-Modal RAG: Images, Tables, Documents — Chunking and Retrieval](</en/ai/multi-modal-rag.html>), [RAG Retrieval Optimization: Hybrid Search, Re-Ranking, Query Transformation](</en/ai/rag-retrieval-optimization.html>)

**See also:** [AI Workflow Automation: LangChain, Temporal, Event-Driven Agents](</en/ai/ai-workflow-automation.html>), [Multi-Modal RAG: Images, Tables, Documents — Chunking and Retrieval](</en/ai/multi-modal-rag.html>), [RAG Retrieval Optimization: Hybrid Search, Re-Ranking, Query Transformation](</en/ai/rag-retrieval-optimization.html>)

**See also:** [RAG Chunking Strategies: Semantic Chunking, Overlapping, Recursive Splitting](</en/ai/rag-chunking-strategies.html>), [Tool Use Patterns: Function Calling, Structured Tools, Multi-Step Reasoning](</en/ai/tool-use-patterns.html>), [Agent Memory Systems: Short-Term, Long-Term, Episodic, Semantic Memory](</en/ai/agent-memory-systems.html>)

**See also:** [RAG Chunking Strategies: Semantic Chunking, Overlapping, Recursive Splitting](</en/ai/rag-chunking-strategies.html>), [Tool Use Patterns: Function Calling, Structured Tools, Multi-Step Reasoning](</en/ai/tool-use-patterns.html>), [Agent Memory Systems: Short-Term, Long-Term, Episodic, Semantic Memory](</en/ai/agent-memory-systems.html>)

**See also:** [RAG Chunking Strategies: Semantic Chunking, Overlapping, Recursive Splitting](</en/ai/rag-chunking-strategies.html>), [Tool Use Patterns: Function Calling, Structured Tools, Multi-Step Reasoning](</en/ai/tool-use-patterns.html>), [Agent Memory Systems: Short-Term, Long-Term, Episodic, Semantic Memory](</en/ai/agent-memory-systems.html>)

**See also:** [RAG Chunking Strategies: Semantic Chunking, Overlapping, Recursive Splitting](</en/ai/rag-chunking-strategies.html>), [Tool Use Patterns: Function Calling, Structured Tools, Multi-Step Reasoning](</en/ai/tool-use-patterns.html>), [Agent Memory Systems: Short-Term, Long-Term, Episodic, Semantic Memory](</en/ai/agent-memory-systems.html>)

**See also:** [RAG Chunking Strategies: Semantic Chunking, Overlapping, Recursive Splitting](</en/ai/rag-chunking-strategies.html>), [Tool Use Patterns: Function Calling, Structured Tools, Multi-Step Reasoning](</en/ai/tool-use-patterns.html>), [Agent Memory Systems: Short-Term, Long-Term, Episodic, Semantic Memory](</en/ai/agent-memory-systems.html>)

**See also:** [RAG Chunking Strategies: Semantic Chunking, Overlapping, Recursive Splitting](</en/ai/rag-chunking-strategies.html>), [Tool Use Patterns: Function Calling, Structured Tools, Multi-Step Reasoning](</en/ai/tool-use-patterns.html>), [Agent Memory Systems: Short-Term, Long-Term, Episodic, Semantic Memory](</en/ai/agent-memory-systems.html>)

**See also:** [RAG Chunking Strategies: Semantic Chunking, Overlapping, Recursive Splitting](</en/ai/rag-chunking-strategies.html>), [Tool Use Patterns: Function Calling, Structured Tools, Multi-Step Reasoning](</en/ai/tool-use-patterns.html>), [Agent Memory Systems: Short-Term, Long-Term, Episodic, Semantic Memory](</en/ai/agent-memory-systems.html>)

**See also:** [RAG Chunking Strategies: Semantic Chunking, Overlapping, Recursive Splitting](</en/ai/rag-chunking-strategies.html>), [Tool Use Patterns: Function Calling, Structured Tools, Multi-Step Reasoning](</en/ai/tool-use-patterns.html>), [Agent Memory Systems: Short-Term, Long-Term, Episodic, Semantic Memory](</en/ai/agent-memory-systems.html>)

**See also:** [RAG Chunking Strategies: Semantic Chunking, Overlapping, Recursive Splitting](</en/ai/rag-chunking-strategies.html>), [Tool Use Patterns: Function Calling, Structured Tools, Multi-Step Reasoning](</en/ai/tool-use-patterns.html>), [Agent Memory Systems: Short-Term, Long-Term, Episodic, Semantic Memory](</en/ai/agent-memory-systems.html>)

**See also:** [RAG Chunking Strategies: Semantic Chunking, Overlapping, Recursive Splitting](</en/ai/rag-chunking-strategies.html>), [Tool Use Patterns: Function Calling, Structured Tools, Multi-Step Reasoning](</en/ai/tool-use-patterns.html>), [Agent Memory Systems: Short-Term, Long-Term, Episodic, Semantic Memory](</en/ai/agent-memory-systems.html>)

**See also:** [RAG Chunking Strategies: Semantic Chunking, Overlapping, Recursive Splitting](</en/ai/rag-chunking-strategies.html>), [Tool Use Patterns: Function Calling, Structured Tools, Multi-Step Reasoning](</en/ai/tool-use-patterns.html>), [Agent Memory Systems: Short-Term, Long-Term, Episodic, Semantic Memory](</en/ai/agent-memory-systems.html>)

**See also:** [RAG Chunking Strategies: Semantic Chunking, Overlapping, Recursive Splitting](</en/ai/rag-chunking-strategies.html>), [Tool Use Patterns: Function Calling, Structured Tools, Multi-Step Reasoning](</en/ai/tool-use-patterns.html>), [Agent Memory Systems: Short-Term, Long-Term, Episodic, Semantic Memory](</en/ai/agent-memory-systems.html>)
