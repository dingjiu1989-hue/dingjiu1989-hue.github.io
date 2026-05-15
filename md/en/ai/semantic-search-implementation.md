---
title: "Semantic Search Implementation Guide: Embeddings, Vector Databases, and Reranking"
description: "Step-by-step guide to building semantic search — embedding models comparison, chunking strategies, pgvector setup, and production architecture."
date: 2026-05-08
board: ai
url: https://dingjiu1989-hue.github.io/en/ai/semantic-search-implementation.html
---

# Semantic Search Implementation Guide: Embeddings, Vector Databases, and Reranking

## Beyond Keyword Search

Keyword search (TF-IDF, BM25) matches exact words — great when users type the right keywords, terrible when they don't. Semantic search understands meaning: "how to deploy a Next.js app" matches "deploy a React application" even without shared keywords. In 2026, implementing semantic search is practical with open-source tools and embedding APIs. Here's how to actually build it.

## The Architecture
    
    
    ┌──────────┐    ┌──────────────┐    ┌───────────────┐    ┌──────────┐
    │  Query   │───▶│ Embedding    │───▶│ Vector Search  │───▶│ Results  │
    │  String  │    │ Model/API    │    │ (pgvector, etc)│    │ (ranked) │
    └──────────┘    └──────────────┘    └───────────────┘    └──────────┘
                          │                      │
                          ▼                      ▼
                  float32[] array        cosine similarity
                  (1536 dims typical)    or approximate (ANN)
    

## Embedding Model Comparison

Model| Dimensions| Max Tokens| Cost| MTEB Score (Retrieval)| Self-Hostable  
---|---|---|---|---|---  
OpenAI text-embedding-3-small| 512/1536| 8,191| $0.02/1M tokens| 62.3 (1536d)| No  
OpenAI text-embedding-3-large| 256/1024/3072| 8,191| $0.13/1M tokens| 64.6 (3072d)| No  
Cohere Embed v4| 1024/2048| 8,192| $0.10/1M tokens| 63.8| No  
BGE-M3 (BAAI)| 1024| 8,192| Free (self-host)| 62.0| Yes (MIT)  
jina-embeddings-v3| 1024| 8,192| $0.02/1M tokens| 62.5| No (API only)  
gte-Qwen2-7B-instruct| 3584| 32,768| Free (self-host)| 66.3 (leading)| Yes (Apache 2.0)  
  
_MTEB = Massive Text Embedding Benchmark. Higher is better. Scores from MTEB leaderboard as of early 2026._

## Vector Database Options

Database| Type| Index Types| Filtering| Best For| Pricing  
---|---|---|---|---|---  
pgvector (PostgreSQL)| Postgres extension| IVFFlat, HNSW| Full SQL WHERE + joins| Apps already on Postgres, metadata-rich filtering| Free (OSS, Postgres license)  
Qdrant| Dedicated vector DB| HNSW, quantization (binary, scalar, product)| Payload filtering| High performance, advanced quantization, filtering| Free (OSS) / Cloud from $25/mo  
Pinecone| Managed vector DB| Proprietary (serverless)| Metadata filtering| Zero-ops, serverless scaling, no tuning needed| Free tier (2GB) → $0.33/GB/mo  
Weaviate| Vector + hybrid DB| HNSW, flat, dynamic| GraphQL filtering, BM25 + vector hybrid| Hybrid search (keyword + semantic), built-in modules| Free (OSS) / Cloud from $25/mo  
Milvus| Distributed vector DB| 12+ index types| Scalar filtering, boolean expressions| Billion-scale vectors, distributed, GPU acceleration| Free (OSS) / Cloud from $0.55/hr  
  
## Implementation Steps

**Step 1: Chunk your documents.** The quality of your chunks determines the quality of your search. Strategies: fixed-size (simple, 256-512 tokens with overlap), sentence-based (split on sentence boundaries), recursive character splitting (LangChain's default — splits on separators: , , ., space), semantic chunking (use a smaller model to detect topic boundaries — most accurate, more expensive). For most applications, recursive splitting with 512-token chunks and 50-token overlap works well. For code search, split on function/class boundaries.

**Step 2: Generate and store embeddings.** For a collection of 10,000 documents with 512-token chunks: ~15,000 chunks × 1,536 dimensions × 4 bytes = ~92 MB of vectors. This fits easily in pgvector on a small Postgres instance. Batch embedding generation: 15,000 chunks via OpenAI text-embedding-3-small = ~$0.20. Cache embeddings — don't re-embed unchanged documents.

**Step 3: Implement search with reranking.** Two-stage retrieval is the standard architecture for production: Stage 1 — Vector search returns top 20-50 candidates (fast, approximate). Stage 2 — Reranker model (Cross-encoder like Cohere Rerank v3 or BGE-Reranker-v2) scores the candidates more precisely and returns top 5-10. Stage 2 adds ~50ms latency but dramatically improves relevance. Without reranking, vector search alone returns "in the ballpark" results; with reranking, you get precisely relevant results.

## Hybrid Search: The Best of Both Worlds

Pure semantic search fails for exact match queries (searching for "error code ERR_SSL_PROTOCOL" should match the exact string, not semantically similar concepts). Pure keyword search fails for conceptual queries ("how to deploy" won't match "deployment guide"). Hybrid search combines both: run BM25 + vector search in parallel, merge results via Reciprocal Rank Fusion (RRF). Weaviate and Elasticsearch have hybrid search built in; with pgvector, you implement the combination yourself.

## When Semantic Search Is Worth It

Use Case| Semantic Search?| Why  
---|---|---  
Documentation search (user-facing)| Yes| Users don't know your terminology; they describe problems  
Internal knowledge base| Yes| Employees search differently; semantic bridges the gap  
E-commerce product search| Yes (hybrid)| "running shoes" should match "trainers" — but exact product codes need keyword  
Legal/contract search| No (or hybrid)| Exact terminology matters; "shall" vs "may" is legally significant  
Code search| Maybe (hybrid)| Function names need exact match; bug descriptions need semantic  
  
**Bottom line:** For most applications in 2026, the pragmatic choice is **pgvector + OpenAI embeddings + a reranker**. You already have Postgres, pgvector is a single extension, embeddings cost pennies per thousand documents, and the two-stage retrieval gives production-quality results. If you're doing this at scale (1M+ documents), add Qdrant or Pinecone. See also: [Vector Database Comparison](</en/ai/vector-database-comparison.html>) and [RAG Best Practices](</en/ai/rag-best-practices.html>).

**See also:** [Vector Database Comparison 2026: Pinecone vs Weaviate vs Qdrant vs Milvus vs pgvector](</en/ai/vector-database-comparison.html>), [Embedding Models Comparison 2026: OpenAI vs Cohere vs BGE vs Jina for Semantic Search](</en/ai/embedding-models-comparison.html>), [Vector Databases in 2026: Pinecone vs Chroma vs Weaviate vs Qdrant — Complete Guide](</en/compare/vector-databases-2026-complete-guide.html>)
