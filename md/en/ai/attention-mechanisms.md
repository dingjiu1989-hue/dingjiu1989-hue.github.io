---
title: "Attention Mechanisms in Neural Networks"
description: "A comprehensive guide to attention mechanisms: from additive attention to multi-query attention and FlashAttention."
date: 2026-02-19
board: ai
url: https://dingjiu1989-hue.github.io/en/ai/attention-mechanisms.html
---

# Attention Mechanisms in Neural Networks

Attention mechanisms allow neural networks to focus on relevant parts of input when producing output. Since the original transformer, numerous attention variants have improved efficiency, quality, and scalability.

## From Additive to Dot-Product

Bahdanau attention (additive attention) uses a small feed-forward network to compute attention scores. It introduced attention to neural machine translation but is computationally expensive. Luong attention (multiplicative/dot-product) computes scores as a dot product, enabling efficient matrix multiplication.

Scaled dot-product attention (transformer) divides scores by sqrt(d_k) to prevent softmax saturation at high dimensions. This simple scaling stabilizes training and enables parallel computation. Modern LLMs universally use scaled dot-product attention.

## Causal Attention

Causal (masked) attention prevents tokens from attending to future tokens. The attention mask sets future token scores to -infinity before softmax, ensuring predictions depend only on previous tokens. This is essential for autoregressive language models.

Causal attention introduces a triangular mask. During training, teacher forcing uses the mask to predict each token given only previous tokens. During inference, the mask prevents looking ahead. PrefixLM uses a bidirectional prefix followed by causal attention for the generation part.

## Multi-Query and Grouped-Query Attention

Multi-Query Attention (MQA) shares key-value heads across all query heads, dramatically reducing KV cache memory. MQA reduces memory by 4-8x with minimal quality loss. It is used in PaLM and Falcon.

Grouped-Query Attention (GQA) is a middle ground between MHA and MQA. Query heads are divided into groups sharing key-value heads. GQA with 8 key-value groups for 32 query heads offers better quality than MQA with similar memory savings. GQA is used in Llama 2/3 and Mistral.

## FlashAttention

FlashAttention computes attention without materializing the full N×N attention matrix, reducing memory from O(N²) to O(N). It uses tiling to process attention in blocks that fit in fast on-chip SRAM. IO-aware algorithms minimize slow HBM accesses.

FlashAttention 2 improves parallelism and reduces non-matmul operations. FlashAttention 3 adds FP8 support and asynchronous processing. These optimizations make long-context transformers practical—enabling 128K+ token contexts by reducing attention memory overhead.

## Sparse Attention

Sparse attention patterns reduce computation by only attending to a subset of tokens. Sliding window attention attends to local tokens. Global tokens attend to all tokens. BigBird and Longformer combine local, global, and random attention patterns for linear complexity.

**See also:** [Transformer Mechanisms in Deep Learning](</en/ai/transformer-mechanisms.html>), [AI Testing Frameworks: DeepEval, Ragas, LangSmith, CI Integration](</en/ai/ai-testing-frameworks.html>), [LLM Safety: RLHF, Constitutional AI, Content Filtering, Red Teaming](</en/ai/llm-safety.html>).

**See also:** [Transformer Mechanisms in Deep Learning](</en/ai/transformer-mechanisms.html>), [AI Testing Frameworks: DeepEval, Ragas, LangSmith, CI Integration](</en/ai/ai-testing-frameworks.html>), [LLM Safety: RLHF, Constitutional AI, Content Filtering, Red Teaming](</en/ai/llm-safety.html>)

**See also:** [Transformer Mechanisms in Deep Learning](</en/ai/transformer-mechanisms.html>), [AI Testing Frameworks: DeepEval, Ragas, LangSmith, CI Integration](</en/ai/ai-testing-frameworks.html>), [LLM Safety: RLHF, Constitutional AI, Content Filtering, Red Teaming](</en/ai/llm-safety.html>)

**See also:** [Transformer Mechanisms in Deep Learning](</en/ai/transformer-mechanisms.html>), [AI Testing Frameworks: DeepEval, Ragas, LangSmith, CI Integration](</en/ai/ai-testing-frameworks.html>), [LLM Safety: RLHF, Constitutional AI, Content Filtering, Red Teaming](</en/ai/llm-safety.html>)

**See also:** [Transformer Mechanisms in Deep Learning](</en/ai/transformer-mechanisms.html>), [AI Testing Frameworks: DeepEval, Ragas, LangSmith, CI Integration](</en/ai/ai-testing-frameworks.html>), [LLM Safety: RLHF, Constitutional AI, Content Filtering, Red Teaming](</en/ai/llm-safety.html>)

**See also:** [Transformer Mechanisms in Deep Learning](</en/ai/transformer-mechanisms.html>), [AI Testing Frameworks: DeepEval, Ragas, LangSmith, CI Integration](</en/ai/ai-testing-frameworks.html>), [LLM Safety: RLHF, Constitutional AI, Content Filtering, Red Teaming](</en/ai/llm-safety.html>)

**See also:** [AI API Gateway: Load Balancing, Fallback, Cost Tracking, Observability](</en/ai/ai-api-gateway.html>), [Graph RAG: Knowledge Graphs, Entity Extraction, Relationship Traversal](</en/ai/graph-rag.html>), [LLM API Design: Streaming, Structured Output, Error Handling, Rate Limits](</en/ai/llm-api-design.html>)

**See also:** [AI API Gateway: Load Balancing, Fallback, Cost Tracking, Observability](</en/ai/ai-api-gateway.html>), [Graph RAG: Knowledge Graphs, Entity Extraction, Relationship Traversal](</en/ai/graph-rag.html>), [LLM API Design: Streaming, Structured Output, Error Handling, Rate Limits](</en/ai/llm-api-design.html>)

**See also:** [AI API Gateway: Load Balancing, Fallback, Cost Tracking, Observability](</en/ai/ai-api-gateway.html>), [Graph RAG: Knowledge Graphs, Entity Extraction, Relationship Traversal](</en/ai/graph-rag.html>), [LLM API Design: Streaming, Structured Output, Error Handling, Rate Limits](</en/ai/llm-api-design.html>)

**See also:** [AI API Gateway: Load Balancing, Fallback, Cost Tracking, Observability](</en/ai/ai-api-gateway.html>), [Graph RAG: Knowledge Graphs, Entity Extraction, Relationship Traversal](</en/ai/graph-rag.html>), [LLM API Design: Streaming, Structured Output, Error Handling, Rate Limits](</en/ai/llm-api-design.html>)

**See also:** [AI API Gateway: Load Balancing, Fallback, Cost Tracking, Observability](</en/ai/ai-api-gateway.html>), [Graph RAG: Knowledge Graphs, Entity Extraction, Relationship Traversal](</en/ai/graph-rag.html>), [LLM API Design: Streaming, Structured Output, Error Handling, Rate Limits](</en/ai/llm-api-design.html>)
