---
title: "Graph RAG: Knowledge Graphs, Entity Extraction, Relationship Traversal"
description: "Implement Graph RAG using knowledge graphs: extract entities and relationships from documents, traverse graph connections, and combine graph retrieval with vect"
date: 2026-02-16
board: ai
url: https://dingjiu1989-hue.github.io/en/ai/graph-rag.html
---

# Graph RAG: Knowledge Graphs, Entity Extraction, Relationship Traversal

## Introduction

Traditional RAG retrieves documents based on semantic similarity. Graph RAG goes further by modeling the relationships between entities: people, companies, concepts, and their connections. This enables queries like "Which employees worked on projects managed by Alice?" that require traversing relationships rather than matching text. This article covers building knowledge graphs from documents and using them for retrieval.

## Entity Extraction

The first step is extracting entities and their relationships from documents:

from pydantic import BaseModel

class Entity(BaseModel):

name: str

type: str

description: str

class Relationship(BaseModel):

source: str

target: str

relationship: str

description: str

class ExtractionResult(BaseModel):

entities: list[Entity]

relationships: list[Relationship]

def extract_graph(documents: list[str]) -> ExtractionResult:

combined_text = "\n\n".join(documents)

response = call_llm_with_structured_output(f"""

Extract all entities and their relationships from the text below.

Entity types to consider: Person, Organization, Technology, Product, Location, Concept, Event

For each entity, provide: name, type, description

For each relationship, provide: source, target, relationship type, description

Text: {combined_text[:8000]}

""", ExtractionResult)

return response

## Building the Knowledge Graph

Use a graph database like Neo4j to store and query the extracted structure:

from neo4j import GraphDatabase

class KnowledgeGraph:

def **init**(self, uri: str, user: str, password: str):

self.driver = GraphDatabase.driver(uri, auth=(user, password))

def insert_entities_and_relations(self, extraction: ExtractionResult):

with self.driver.session() as session:

## Create entities

for entity in extraction.entities:

session.run(

"MERGE (e:Entity {name: $name}) "

"SET e.type = $type, e.description = $description",

name=entity.name,

type=entity.type,

description=entity.description,

)

## Create relationships

for rel in extraction.relationships:

session.run(

"MATCH (s:Entity {name: $source}) "

"MATCH (t:Entity {name: $target}) "

"MERGE (s)-[r:RELATES {type: $relationship}]->(t) "

"SET r.description = $description",

source=rel.source,

target=rel.target,

relationship=rel.relationship,

description=rel.description,

)

def traverse(self, start_entity: str, max_depth: int = 2) -> list[dict]:

with self.driver.session() as session:

result = session.run(

"""

MATCH path = (start:Entity {name: $start_entity})-[:RELATES*1..$max_depth]->(related)

RETURN [node in nodes(path) | node.name] AS path_nodes,

[rel in relationships(path) | rel.type] AS path_rels

LIMIT 50

""",

start_entity=start_entity,

max_depth=max_depth,

)

return [record.data() for record in result]

## Graph + Vector Hybrid Retrieval

The most powerful pattern combines graph traversal with vector similarity:

class GraphVectorRetriever:

def **init**(self, graph: KnowledgeGraph, vector_store):

self.graph = graph

self.vector_store = vector_store

def retrieve(self, query: str, k: int = 5) -> list[str]:

## Step 1: Identify starting entities from the query

query_entities = self.extract_query_entities(query)

## Step 2: Vector search for broader context

vector_results = self.vector_store.similarity_search(query, k=k)

## Step 3: Graph traversal from identified entities

graph_context = []

for entity in query_entities:

paths = self.graph.traverse(entity, max_depth=2)

for path in paths:

context = " -> ".join(

f"{path['path_nodes'][i]} ({path['path_rels'][i]})"

if i < len(path['path_rels'])

else path['path_nodes'][i]

for i in range(len(path['path_nodes']))

)

graph_context.append(context)

## Step 4: Combine and rank results

combined = graph_context + [doc.page_content for doc in vector_results]

return combined[:k]

def extract_query_entities(self, query: str) -> list[str]:

response = call_llm(f"""

Extract entity names from this query that exist in our knowledge graph.

Return ONLY the entity names, one per line.

Query: {query}

""")

return [line.strip() for line in response.strip().split("\n") if line.strip()]

## Microsoft's GraphRAG Pattern

Microsoft's GraphRAG uses a global-to-local search approach:

def graphrag_search(query: str, graph: KnowledgeGraph, vector_store, llm) -> str:

## Step 1: Local search - find directly relevant entities

local_entities = extract_query_entities(query)

## Step 2: Global search - find related communities

community_context = []

for entity in local_entities:

community = graph.traverse(entity, max_depth=3)

community_context.extend(community)

## Step 3: Vector search for text chunks

text_chunks = vector_store.similarity_search(query, k=10)

## Step 4: Synthesize answer

context_parts = []

for ctx in community_context:

context_parts.append(format_graph_path(ctx))

for doc in text_chunks:

context_parts.append(doc.page_content)

answer = call_llm(f"""

Answer the query using the provided context.

The context includes both graph relationships and document excerpts.

Context: {' '.join(context_parts[:20])}

Query: {query}

""")

return answer

## When to Use Graph RAG

Graph RAG excels over vector-only RAG when:

  * Questions involve multi-hop reasoning ("What projects did people who worked under X manage?")

  * Your data has a rich relational structure (org charts, product hierarchies, dependency maps)

  * You need to answer "how are these related?" questions frequently

  * Entities appear across many documents and you need to aggregate information about them




## Conclusion

Graph RAG extends vector-based retrieval with relationship traversal. Extract entities and relationships from documents to build a knowledge graph. Combine graph traversal with vector search for queries that require understanding connections. The hybrid approach handles both semantic similarity questions ("find documents about topic X") and relational questions ("how is entity A connected to entity B"). Start with vector-only RAG and add graph capabilities when your users ask questions that require understanding relationships.

**See also:** [Multi-Modal RAG: Images, Tables, Documents — Chunking and Retrieval](</en/ai/multi-modal-rag.html>), [RAG Evaluation: Retrieval Metrics, Generation Quality, End-to-End Testing, and Datasets](</en/ai/rag-evaluation.html>), [RAG Agent Patterns: Self-Query, Corrective, Adaptive Retrieval](</en/ai/rag-agent-patterns.html>).

**See also:** [Multi-Modal RAG: Images, Tables, Documents — Chunking and Retrieval](</en/ai/multi-modal-rag.html>), [RAG Agent Patterns: Self-Query, Corrective, Adaptive Retrieval](</en/ai/rag-agent-patterns.html>), [RAG Retrieval Optimization: Hybrid Search, Re-Ranking, Query Transformation](</en/ai/rag-retrieval-optimization.html>)

**See also:** [Multi-Modal RAG: Images, Tables, Documents — Chunking and Retrieval](</en/ai/multi-modal-rag.html>), [RAG Agent Patterns: Self-Query, Corrective, Adaptive Retrieval](</en/ai/rag-agent-patterns.html>), [RAG Retrieval Optimization: Hybrid Search, Re-Ranking, Query Transformation](</en/ai/rag-retrieval-optimization.html>)

**See also:** [Multi-Modal RAG: Images, Tables, Documents — Chunking and Retrieval](</en/ai/multi-modal-rag.html>), [RAG Agent Patterns: Self-Query, Corrective, Adaptive Retrieval](</en/ai/rag-agent-patterns.html>), [RAG Retrieval Optimization: Hybrid Search, Re-Ranking, Query Transformation](</en/ai/rag-retrieval-optimization.html>)

**See also:** [Multi-Modal RAG: Images, Tables, Documents — Chunking and Retrieval](</en/ai/multi-modal-rag.html>), [RAG Agent Patterns: Self-Query, Corrective, Adaptive Retrieval](</en/ai/rag-agent-patterns.html>), [RAG Retrieval Optimization: Hybrid Search, Re-Ranking, Query Transformation](</en/ai/rag-retrieval-optimization.html>)

**See also:** [Multi-Modal RAG: Images, Tables, Documents — Chunking and Retrieval](</en/ai/multi-modal-rag.html>), [RAG Agent Patterns: Self-Query, Corrective, Adaptive Retrieval](</en/ai/rag-agent-patterns.html>), [RAG Retrieval Optimization: Hybrid Search, Re-Ranking, Query Transformation](</en/ai/rag-retrieval-optimization.html>)

**See also:** [AI Caching Strategies: Semantic Caching, Cache Invalidation, Cost Reduction, and Latency Improvement](</en/ai/ai-caching-strategies.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>), [Model Evaluation: Benchmarks, Human Evaluation, LLM-as-Judge, and A/B Testing in Production](</en/ai/model-evaluation-harness.html>)

**See also:** [AI Caching Strategies: Semantic Caching, Cache Invalidation, Cost Reduction, and Latency Improvement](</en/ai/ai-caching-strategies.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>), [Model Evaluation: Benchmarks, Human Evaluation, LLM-as-Judge, and A/B Testing in Production](</en/ai/model-evaluation-harness.html>)

**See also:** [AI Caching Strategies: Semantic Caching, Cache Invalidation, Cost Reduction, and Latency Improvement](</en/ai/ai-caching-strategies.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>), [Model Evaluation: Benchmarks, Human Evaluation, LLM-as-Judge, and A/B Testing in Production](</en/ai/model-evaluation-harness.html>)

**See also:** [AI Caching Strategies: Semantic Caching, Cache Invalidation, Cost Reduction, and Latency Improvement](</en/ai/ai-caching-strategies.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>), [Model Evaluation: Benchmarks, Human Evaluation, LLM-as-Judge, and A/B Testing in Production](</en/ai/model-evaluation-harness.html>)

**See also:** [AI Caching Strategies: Semantic Caching, Cache Invalidation, Cost Reduction, and Latency Improvement](</en/ai/ai-caching-strategies.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>), [Model Evaluation: Benchmarks, Human Evaluation, LLM-as-Judge, and A/B Testing in Production](</en/ai/model-evaluation-harness.html>)

**See also:** [AI Caching Strategies: Semantic Caching, Cache Invalidation, Cost Reduction, and Latency Improvement](</en/ai/ai-caching-strategies.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>), [Model Evaluation: Benchmarks, Human Evaluation, LLM-as-Judge, and A/B Testing in Production](</en/ai/model-evaluation-harness.html>)

**See also:** [AI Caching Strategies: Semantic Caching, Cache Invalidation, Cost Reduction, and Latency Improvement](</en/ai/ai-caching-strategies.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>), [Model Evaluation: Benchmarks, Human Evaluation, LLM-as-Judge, and A/B Testing in Production](</en/ai/model-evaluation-harness.html>)

**See also:** [AI Caching Strategies: Semantic Caching, Cache Invalidation, Cost Reduction, and Latency Improvement](</en/ai/ai-caching-strategies.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>), [Model Evaluation: Benchmarks, Human Evaluation, LLM-as-Judge, and A/B Testing in Production](</en/ai/model-evaluation-harness.html>)

**See also:** [AI Caching Strategies: Semantic Caching, Cache Invalidation, Cost Reduction, and Latency Improvement](</en/ai/ai-caching-strategies.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>), [Model Evaluation: Benchmarks, Human Evaluation, LLM-as-Judge, and A/B Testing in Production](</en/ai/model-evaluation-harness.html>)

**See also:** [AI Caching Strategies: Semantic Caching, Cache Invalidation, Cost Reduction, and Latency Improvement](</en/ai/ai-caching-strategies.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>), [Model Evaluation: Benchmarks, Human Evaluation, LLM-as-Judge, and A/B Testing in Production](</en/ai/model-evaluation-harness.html>)

**See also:** [AI Caching Strategies: Semantic Caching, Cache Invalidation, Cost Reduction, and Latency Improvement](</en/ai/ai-caching-strategies.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>), [Model Evaluation: Benchmarks, Human Evaluation, LLM-as-Judge, and A/B Testing in Production](</en/ai/model-evaluation-harness.html>)

**See also:** [AI Caching Strategies: Semantic Caching, Cache Invalidation, Cost Reduction, and Latency Improvement](</en/ai/ai-caching-strategies.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>), [Model Evaluation: Benchmarks, Human Evaluation, LLM-as-Judge, and A/B Testing in Production](</en/ai/model-evaluation-harness.html>)

**See also:** [AI Caching Strategies: Semantic Caching, Cache Invalidation, Cost Reduction, and Latency Improvement](</en/ai/ai-caching-strategies.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>), [Model Evaluation: Benchmarks, Human Evaluation, LLM-as-Judge, and A/B Testing in Production](</en/ai/model-evaluation-harness.html>)
