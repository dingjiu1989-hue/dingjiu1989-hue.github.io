---
title: "RAG Architecture Guide"
description: "A comprehensive guide to Retrieval-Augmented Generation architecture, covering indexing, retrieval, generation, and production deployment."
date: 2025-12-13
board: ai
url: https://dingjiu1989-hue.github.io/en/ai/rag-architecture-guide.html
---

# RAG Architecture Guide

## Introduction

Retrieval-Augmented Generation (RAG) has become the dominant architecture for production LLM applications. By combining a retrieval system with a generative model, RAG overcomes the limitations of static model knowledge — providing access to up-to-date information, reducing hallucinations, and grounding responses in verifiable sources. This guide explores RAG architecture from the ground up.

## Core Components

A RAG system consists of three primary stages: indexing, retrieval, and generation.

## Indexing Pipeline

The indexing pipeline transforms raw documents into a searchable format:

  * **Document ingestion** : Load documents from PDFs, web pages, databases, or APIs



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Text splitting** : Chunk documents into manageable pieces using semantic or fixed-size splitting

3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Embedding generation** : Convert each chunk into a dense vector using an embedding model

4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Vector storage** : Store embeddings in a vector database with metadata

Chunking strategy significantly impacts retrieval quality. Fixed-size chunks of 512 tokens with 128-token overlap work well for general-purpose RAG. For code documentation, smaller chunks of 256 tokens are preferable. Semantic chunking, which splits at natural boundaries like paragraphs or sections, often produces the best results.

## Retrieval Stage

The retrieval stage finds relevant documents for a given query:

**Query transformation** is often the first step. Raw user queries are rarely optimal for retrieval. Common transformations include:

  * Query rewriting: Rephrase the user's question to match document language

  * Query expansion: Generate multiple related queries and retrieve for each

  * HyDE (Hypothetical Document Embedding): Generate a hypothetical answer, then use its embedding for retrieval




**Retrieval methods** range from simple to sophisticated:

  * **Dense retrieval** : Cosine similarity search against embedding vectors using ANN indexes (HNSW, IVF)

  * **Sparse retrieval** : Traditional keyword matching using BM25 or TF-IDF

  * **Hybrid retrieval** : Combine dense and sparse results with reciprocal rank fusion




Hybrid retrieval consistently outperforms either method alone. A typical fusion formula is:

RRF(d) = Σ 1/(k + rank_i(d))

Where k is a constant (typically 60) and rank_i(d) is the rank of document d in method i.

## Generation Stage

The generation stage constructs prompts combining retrieved context with the user's query:

**Context windowing** strategies include:

  * **Stuff** : Insert all retrieved documents into the prompt (simple but token-heavy)

  * **Map-reduce** : Process each document separately, then combine results

  * **Refine** : Iteratively update an answer as each document is processed




**Re-ranking** is a critical step between retrieval and generation. A cross-encoder model scores each retrieved document for relevance to the query, filtering out low-quality matches before they reach the LLM.

## Advanced RAG Patterns

## Agentic RAG

Agentic RAG systems give the LLM control over retrieval decisions. Instead of retrieving once and generating, the model can:

  * Request additional documents when information is insufficient

  * Choose between different data sources (vector DB, web search, SQL database)

  * Iteratively refine search queries based on partial results




This pattern dramatically improves answer quality for complex, multi-step questions.

## Multi-Hop RAG

Some questions require information from multiple documents. Multi-hop RAG breaks the question into sub-questions, retrieves for each, and synthesizes the results. For example, "Which company founded by Person A acquired Company B?" requires finding Person A's company, then checking acquisition records.

## Self-RAG

Self-RAG introduces reflection steps where the model evaluates its own retrieval and generation:

  * Retrieve relevant passages



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Generate an answer based on retrieved passages

3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Evaluate whether the answer is supported by the passages

4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. If not, either retrieve more information or revise the answer

## Production Considerations

**Latency optimization** : Embedding generation and vector search both add latency. Strategies include caching frequent queries, using smaller embedding models for initial retrieval, and parallelizing retrieval across multiple data sources.

**Evaluation** : RAG systems need evaluation at both the retrieval and generation stages. Retrieval metrics include recall@k and MRR. Generation metrics include answer relevance, faithfulness (whether the answer is supported by retrieved documents), and answer completeness.

**Monitoring** : Track embedding drift (when the distribution of queries changes), retrieval success rate, and end-user feedback to continuously improve the system.

## Conclusion

RAG architecture provides a powerful framework for building LLM applications grounded in real data. The key to success is understanding the interaction between indexing quality, retrieval strategy, and generation prompts. Start with a simple pipeline, measure performance, and add sophistication — hybrid retrieval, re-ranking, agentic patterns — only where data shows they improve outcomes.

**See also:** [AI Image Generation Guide](</en/ai/ai-image-generation.html>), [AI Code Generation Best Practices](</en/ai/ai-code-generation.html>), [AI Content Generation Workflows](</en/ai/ai-content-generation.html>).

**See also:** [AI Image Generation Guide](</en/ai/ai-image-generation.html>), [AI Content Generation Workflows](</en/ai/ai-content-generation.html>), [RAG Pipeline Optimization: Production Best Practices](</en/ai/rag-pipeline-optimization.html>)

**See also:** [AI Image Generation Guide](</en/ai/ai-image-generation.html>), [AI Content Generation Workflows](</en/ai/ai-content-generation.html>), [RAG Pipeline Optimization: Production Best Practices](</en/ai/rag-pipeline-optimization.html>)

**See also:** [AI Image Generation Guide](</en/ai/ai-image-generation.html>), [AI Content Generation Workflows](</en/ai/ai-content-generation.html>), [RAG Pipeline Optimization: Production Best Practices](</en/ai/rag-pipeline-optimization.html>)

**See also:** [AI Image Generation Guide](</en/ai/ai-image-generation.html>), [AI Content Generation Workflows](</en/ai/ai-content-generation.html>), [RAG Pipeline Optimization: Production Best Practices](</en/ai/rag-pipeline-optimization.html>)

**See also:** [AI Image Generation Guide](</en/ai/ai-image-generation.html>), [AI Content Generation Workflows](</en/ai/ai-content-generation.html>), [RAG Pipeline Optimization: Production Best Practices](</en/ai/rag-pipeline-optimization.html>)

**See also:** [AI Embeddings Explained](</en/ai/ai-embeddings-explained.html>), [LLM Context Window Management](</en/ai/llm-context-window.html>), [LLM Evaluation Metrics](</en/ai/llm-evaluation-metrics.html>)

**See also:** [AI Embeddings Explained](</en/ai/ai-embeddings-explained.html>), [LLM Context Window Management](</en/ai/llm-context-window.html>), [LLM Evaluation Metrics](</en/ai/llm-evaluation-metrics.html>)

**See also:** [AI Embeddings Explained](</en/ai/ai-embeddings-explained.html>), [LLM Context Window Management](</en/ai/llm-context-window.html>), [LLM Evaluation Metrics](</en/ai/llm-evaluation-metrics.html>)
