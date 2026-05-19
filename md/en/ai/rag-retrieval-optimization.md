---
title: "RAG Retrieval Optimization: Hybrid Search, Re-Ranking, Query Transformation"
description: "Optimize RAG retrieval with hybrid search combining dense and sparse methods, cross-encoder re-ranking, and query transformation techniques for better results."
date: 2026-02-19
board: ai
url: https://dingjiu1989-hue.github.io/en/ai/rag-retrieval-optimization.html
---

# RAG Retrieval Optimization: Hybrid Search, Re-Ranking, Query Transformation

## Introduction

Retrieval quality is the single biggest factor in RAG system performance. Even the best LLM cannot produce accurate answers from irrelevant context. This article covers three optimization layers: hybrid search that combines embedding similarity with keyword matching, re-ranking that refines initial results, and query transformation that bridges the gap between user questions and searchable terms.

## Hybrid Search

Pure vector search excels at semantic similarity but misses exact keyword matches. Pure keyword search finds exact terms but misses conceptually related content. Hybrid search combines both:

from qdrant_client import QdrantClient

from qdrant_client.models import Filter, HybridFusion

client = QdrantClient(host="localhost", port=6333)

def hybrid_search(

query: str, collection: str = "documents", limit: int = 10

) -> list[dict]:

## Generate dense vector

dense_vector = embedding_model.encode(query).tolist()

## Sparse vector (BM25-style)

sparse_vector = sparse_encoder.encode(query)

results = client.search_batch(

collection_name=collection,

requests=[

## Dense search

{

"vector": dense_vector,

"limit": limit * 2,

"with_payload": True,

},

## Sparse search

{

"vector": sparse_vector,

"limit": limit * 2,

"with_payload": True,

},

],

)

## Fusion: Reciprocal Rank Fusion

return rrf_fusion(results[0], results[1], k=60)

## Reciprocal Rank Fusion

RRF combines ranked lists from multiple retrieval methods:

def rrf_fusion(dense_results: list, sparse_results: list, k: int = 60) -> list[dict]:

scores = {}

for rank, result in enumerate(dense_results):

scores[result.id] = scores.get(result.id, 0) + 1 / (k + rank + 1)

for rank, result in enumerate(sparse_results):

scores[result.id] = scores.get(result.id, 0) + 1 / (k + rank + 1)

reranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

return [{"id": id_, "score": score} for id_, score in reranked[:limit]]

RRF is simple, effective, and requires no training. The constant `k` (typically 60) prevents a single high rank from dominating.

## Cross-Encoder Re-Ranking

After initial retrieval, a cross-encoder model re-scores candidates with higher accuracy:

from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def retrieve_and_rerank(query: str, top_k: int = 50, rerank_top: int = 5) -> list[dict]:

## First stage: fast bi-encoder retrieval

candidates = hybrid_search(query, limit=top_k)

## Second stage: cross-encoder re-ranking

pairs = [(query, cand["text"]) for cand in candidates]

scores = reranker.predict(pairs)

for cand, score in zip(candidates, scores):

cand["rerank_score"] = float(score)

candidates.sort(key=lambda x: x["rerank_score"], reverse=True)

return candidates[:rerank_top]

Cross-encoders are 10-100x slower than bi-encoders but significantly more accurate. The two-stage pattern (wide bi-encoder retrieval, narrow cross-encoder re-ranking) balances speed and quality.

## Query Transformation

User queries are rarely optimal for retrieval. Transform them before searching:

def transform_query(user_query: str, technique: str = "expansion") -> str:

if technique == "expansion":

return expand_query(user_query)

elif technique == "decomposition":

return decompose_query(user_query)

elif technique == "hypothetical":

return hyde_query(user_query)

def expand_query(query: str) -> str:

"""Generate search-friendly expansions of the original query."""

expansions = call_llm(f"""

Generate 3 alternative phrasings of this query for better search retrieval.

Keep the core meaning but vary terminology.

Original: {query}

""")

return f"{query}\n{expansions}"

def hyde_query(query: str) -> str:

"""Hypothetical Document Embeddings: generate a hypothetical ideal document,

then use its embedding for retrieval."""

hypothetical = call_llm(f"Write a short passage that perfectly answers: {query}")

return hypothetical

## Query Decomposition

Complex questions should be split into sub-queries, each searched independently:

def decompose_and_retrieve(question: str) -> list[dict]:

sub_queries = call_llm(f"""

Break this question into 2-4 independent sub-questions:

{question}

""")

sub_queries = parse_list(sub_queries)

all_results = []

for sq in sub_queries:

results = hybrid_search(sq, limit=5)

all_results.extend(results)

## Deduplicate by ID

seen = set()

unique_results = []

for r in all_results:

if r["id"] not in seen:

seen.add(r["id"])

unique_results.append(r)

return unique_results[:10]

## Measuring Retrieval Quality

Track these metrics to validate improvements:

def evaluate_retrieval(test_queries: list[dict], retriever_fn) -> dict:

"""test_queries: [{query, relevant_doc_ids}]"""

metrics = {"recall@k": {}, "mrr": 0}

for k in [1, 3, 5, 10]:

recalls = []

for tq in test_queries:

results = retriever_fn(tq["query"], limit=k)

retrieved_ids = {r["id"] for r in results}

relevant = set(tq["relevant_doc_ids"])

recall = len(retrieved_ids & relevant) / len(relevant) if relevant else 0

recalls.append(recall)

metrics["recall@k"] = np.mean(recalls)

return metrics

## Conclusion

Optimize RAG retrieval in three layers. First, implement hybrid search combining dense and sparse vectors with RRF fusion. Second, add cross-encoder re-ranking for precision on early-stage results. Third, transform user queries through expansion, decomposition, or HyDE techniques. Measure recall@k after each change to validate improvements before deploying.

**See also:** [RAG Pipeline Optimization: Production Best Practices](</en/ai/rag-pipeline-optimization.html>), [Vector Database Tuning: Index Parameters, Search Configuration, and Hybrid Search](</en/ai/vector-database-tuning.html>), [RAG Agent Patterns: Self-Query, Corrective, Adaptive Retrieval](</en/ai/rag-agent-patterns.html>).

**See also:** [RAG Agent Patterns: Self-Query, Corrective, Adaptive Retrieval](</en/ai/rag-agent-patterns.html>), [Vector Database Tuning: Index Parameters, Search Configuration, and Hybrid Search](</en/ai/vector-database-tuning.html>), [Embeddings: Techniques and Best Practices](</en/ai/embeddings-techniques.html>)

**See also:** [RAG Agent Patterns: Self-Query, Corrective, Adaptive Retrieval](</en/ai/rag-agent-patterns.html>), [Vector Database Tuning: Index Parameters, Search Configuration, and Hybrid Search](</en/ai/vector-database-tuning.html>), [Embeddings: Techniques and Best Practices](</en/ai/embeddings-techniques.html>)

**See also:** [RAG Agent Patterns: Self-Query, Corrective, Adaptive Retrieval](</en/ai/rag-agent-patterns.html>), [Vector Database Tuning: Index Parameters, Search Configuration, and Hybrid Search](</en/ai/vector-database-tuning.html>), [Embeddings: Techniques and Best Practices](</en/ai/embeddings-techniques.html>)

**See also:** [RAG Agent Patterns: Self-Query, Corrective, Adaptive Retrieval](</en/ai/rag-agent-patterns.html>), [Vector Database Tuning: Index Parameters, Search Configuration, and Hybrid Search](</en/ai/vector-database-tuning.html>), [Embeddings: Techniques and Best Practices](</en/ai/embeddings-techniques.html>)

**See also:** [RAG Agent Patterns: Self-Query, Corrective, Adaptive Retrieval](</en/ai/rag-agent-patterns.html>), [Vector Database Tuning: Index Parameters, Search Configuration, and Hybrid Search](</en/ai/vector-database-tuning.html>), [Embeddings: Techniques and Best Practices](</en/ai/embeddings-techniques.html>)

**See also:** [Graph RAG: Knowledge Graphs, Entity Extraction, Relationship Traversal](</en/ai/graph-rag.html>), [Model Deployment: vLLM, TGI, ONNX, Quantization, GPU Optimization](</en/ai/model-deployment.html>), [Multi-Modal RAG: Images, Tables, Documents — Chunking and Retrieval](</en/ai/multi-modal-rag.html>)

**See also:** [Graph RAG: Knowledge Graphs, Entity Extraction, Relationship Traversal](</en/ai/graph-rag.html>), [Model Deployment: vLLM, TGI, ONNX, Quantization, GPU Optimization](</en/ai/model-deployment.html>), [Multi-Modal RAG: Images, Tables, Documents — Chunking and Retrieval](</en/ai/multi-modal-rag.html>)

**See also:** [Graph RAG: Knowledge Graphs, Entity Extraction, Relationship Traversal](</en/ai/graph-rag.html>), [Model Deployment: vLLM, TGI, ONNX, Quantization, GPU Optimization](</en/ai/model-deployment.html>), [Multi-Modal RAG: Images, Tables, Documents — Chunking and Retrieval](</en/ai/multi-modal-rag.html>)
