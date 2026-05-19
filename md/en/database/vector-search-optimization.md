---
title: "Vector Search Optimization Techniques"
description: "Optimize vector search with HNSW tuning, quantization (PQ, scalar), IVF parameters, filtered search performance, and multi-vector indexing."
date: 2026-03-29
board: database
url: https://dingjiu1989-hue.github.io/en/database/vector-search-optimization.html
---

# Vector Search Optimization Techniques

Vector Search Fundamentals 

Vector search finds similar items using embedding vectors. It powers semantic search, recommendation systems, and RAG applications. 

HNSW Index Parameters 

Hierarchical Navigable Small World (HNSW) is the most popular vector index: 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- pgvector HNSW index

CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops)

WITH (m = 16, ef_construction = 200);

SET hnsw.ef_search = 100;

SELECT id, embedding <=> '[0.1, 0.2, ...]' as distance

FROM documents

ORDER BY embedding <=> '[0.1, 0.2, ...]' LIMIT 10;

Key HNSW parameters: M (connections per node, default 16), ef_construction (build quality, default 200), ef_search (query recall, set per-query). 

Quantization 

Reduce memory footprint: 

def quantize_int8(vectors):

mins = vectors.min(axis=0)

maxs = vectors.max(axis=0)

scale = 255.0 / (maxs - mins + 1e-8)

quantized = ((vectors - mins) * scale - 128).astype(np.int8)

return quantized, mins, scale

FP16 halves memory. INT8 reduces by 4x. Product quantization achieves 10-30x compression. 

Pre-filtering Strategies 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Post-filtering: search then filter

SELECT id, embedding <=> '[0.1, 0.2]' as distance

FROM documents

WHERE category = 'technology'

ORDER BY embedding <=> '[0.1, 0.2]' LIMIT 10;

Prefer pre-filtering with separate indexes per filter category for optimal performance. 

Conclusion 

Tune HNSW parameters for your data distribution. Use quantization to reduce memory. Benchmark with your actual data. Monitor recall in production.

**See also:** [SQL Query Optimization](</en/database/sql-query-optimization.html>), [Query Performance Tuning Tools](</en/database/query-performance-tuning.html>), [Connection Pooling Guide](</en/database/connection-pooling.html>).

**See also:** [SQL Query Optimization](</en/database/sql-query-optimization.html>), [Connection Pooling Guide](</en/database/connection-pooling.html>), [Query Performance Tuning Tools](</en/database/query-performance-tuning.html>)

**See also:** [SQL Query Optimization](</en/database/sql-query-optimization.html>), [Connection Pooling Guide](</en/database/connection-pooling.html>), [Query Performance Tuning Tools](</en/database/query-performance-tuning.html>)

**See also:** [SQL Query Optimization](</en/database/sql-query-optimization.html>), [Connection Pooling Guide](</en/database/connection-pooling.html>), [Query Performance Tuning Tools](</en/database/query-performance-tuning.html>)

**See also:** [SQL Query Optimization](</en/database/sql-query-optimization.html>), [Connection Pooling Guide](</en/database/connection-pooling.html>), [Query Performance Tuning Tools](</en/database/query-performance-tuning.html>)

**See also:** [SQL Query Optimization](</en/database/sql-query-optimization.html>), [Connection Pooling Guide](</en/database/connection-pooling.html>), [Query Performance Tuning Tools](</en/database/query-performance-tuning.html>)

**See also:** [Database Indexing Strategies](</en/database/database-indexing.html>), [Full-Text Search Engines (Elasticsearch, Meilisearch, Typesense)](</en/database/full-text-search.html>), [Data Lake vs Data Warehouse vs Lakehouse](</en/database/data-lake-vs-warehouse.html>)

**See also:** [Database Indexing Strategies](</en/database/database-indexing.html>), [Full-Text Search Engines (Elasticsearch, Meilisearch, Typesense)](</en/database/full-text-search.html>), [Data Lake vs Data Warehouse vs Lakehouse](</en/database/data-lake-vs-warehouse.html>)

**See also:** [Database Indexing Strategies](</en/database/database-indexing.html>), [Full-Text Search Engines (Elasticsearch, Meilisearch, Typesense)](</en/database/full-text-search.html>), [Data Lake vs Data Warehouse vs Lakehouse](</en/database/data-lake-vs-warehouse.html>)
