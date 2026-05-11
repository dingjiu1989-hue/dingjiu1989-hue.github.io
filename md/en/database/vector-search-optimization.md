---
title: "Vector Search Optimization Techniques"
description: "Optimize vector search with HNSW tuning, quantization (PQ, scalar), IVF parameters, filtered search performance, and multi-vector indexing."
date: 2026-05-12
board: database
url: https://dingjiu1989-hue.github.io/en/database/vector-search-optimization.html
---

Vector search is the foundation of modern retrieval-augmented generation (RAG), semantic search, and recommendation systems. As vector databases become production workloads, optimizing search performance, recall, and memory usage becomes critical. This article covers practical optimization techniques for HNSW, quantization, IVF, filtered search, and multi-vector indexing.

## HNSW Tuning

HNSW (Hierarchical Navigable Small World) is the most popular approximate nearest neighbor (ANN) algorithm. It builds a multi-layer graph where higher layers have fewer nodes (long-range connections) and lower layers have more nodes (short-range connections).

### Key Parameters

**M (Maximum number of connections per node)**:
Controls how many neighbors each node connects to. Higher M improves recall and search quality at the cost of more memory and slower indexing.

- M = 8: Lower memory, lower recall. Good for filtering-heavy workloads.
- M = 16: Balanced. Recommended default for most cases.
- M = 32: Higher recall, higher memory. Good for high-accuracy requirements.

```python
# HNSW with different M values
from pymilvus import CollectionSchema, FieldSchema, DataType

schema = CollectionSchema([
    FieldSchema("id", DataType.INT64, is_primary=True),
    FieldSchema("embedding", DataType.FLOAT_VECTOR, dim=768),
])

# Milvus: Create collection with HNSW index
collection.create_index("embedding", {
    "metric_type": "IP",          # Inner product
    "index_type": "HNSW",
    "params": {
        "M": 16,                  # Connections per node
        "efConstruction": 200     # Build-time search width
    }
})
```

**efConstruction (Build-time search width)**:
Controls how many candidate neighbors are evaluated during index construction. Higher values improve index quality but increase build time.

- efConstruction = 100: Fast building. Good for frequent rebuilds.
- efConstruction = 200: Balanced quality and speed.
- efConstruction = 400: Highest quality. For static datasets built once.

**ef (Search-time search width)**:
Controls the trade-off between search speed and recall. Unlike M and efConstruction, ef is set at query time, not build time.

```python
# Search with different ef values
def search_with_ef(collection, query_vector, ef, top_k=10):
    search_params = {
        "metric_type": "IP",
        "params": {
            "ef": ef  # Higher = better recall, slower
        }
    }
    results = collection.search(
        data=[query_vector],
        anns_field="embedding",
        param=search_params,
        limit=top_k
    )
    return results

# Tuning strategy: Start with ef=top_k*2, increase until recall is acceptable
```

### HNSW Tuning Process

1. Set M = 16, efConstruction = 200 as baseline.
2. Build the index and measure recall at ef = 100.
3. If recall is below target, increase M to 24 or 32.
4. If still below, increase efConstruction to 300-400.
5. For production queries, set ef based on latency budget: higher ef for offline, lower for real-time.

## Quantization

Quantization reduces the memory footprint of vectors by reducing the precision of each dimension. It enables larger datasets to fit in memory or reduces search latency by shrinking the data that must be scanned.

### Scalar Quantization (SQ)

Scalar quantization converts 32-bit float vectors to 8-bit (or 4-bit) integers. Each dimension is compressed by 4x (or 8x for 4-bit).

```python
# Scalar quantization: float32 to int8
import numpy as np

def quantize_scalar_8bit(vectors):
    """Convert float32 vectors to int8."""
    # Calculate min/max per dimension
    mins = vectors.min(axis=0)
    maxs = vectors.max(axis=0)
    ranges = maxs - mins
    
    # Quantize to int8
    quantized = ((vectors - mins) / (ranges + 1e-10) * 255 - 128).astype(np.int8)
    return quantized, mins, ranges

def dequantize_scalar_8bit(quantized, mins, ranges):
    """Restore approximate float32 from int8."""
    return ((quantized.astype(np.float32) + 128) / 255 * ranges + mins)
```

**When to use SQ**:
- Memory is constrained (you cannot fit float32 vectors in RAM).
- Dataset has 100M+ vectors and you are using disk-based indexes.
- Recall loss of 1-2 percentage points is acceptable.

### Product Quantization (PQ)

Product quantization splits vectors into sub-vectors and quantizes each sub-vector independently using a codebook. It is more aggressive than scalar quantization.

```python
# Product quantization with 8 sub-quantizers
def train_pq(vectors, m=8, k=256):
    """Train product quantization codebooks.
    
    Args:
        vectors: (n, d) float32 array
        m: Number of sub-vector partitions
        k: Number of centroids per partition
    """
    d = vectors.shape[1]
    assert d % m == 0, "Dimension must be divisible by m"
    
    sub_dim = d // m
    codebooks = []
    codes = np.zeros((vectors.shape[0], m), dtype=np.uint8)
    
    for i in range(m):
        sub_vectors = vectors[:, i*sub_dim:(i+1)*sub_dim]
        # Train k-means with k centroids
        centroids = train_kmeans(sub_vectors, k)
        codebooks.append(centroids)
        # Assign each sub-vector to nearest centroid
        codes[:, i] = assign_to_centroids(sub_vectors, centroids)
    
    return codebooks, codes
```

**PQ compression ratios**:
- PQ 4x8: 4 bytes per sub-vector, 8 sub-vectors = 32 bytes per vector (96% reduction from 768-dim float32).
- PQ 8x8: 8 bytes per sub-vector, 8 sub-vectors = 64 bytes per vector (92% reduction).
- PQ 16x8: 16 bytes per sub-vector, 8 sub-vectors = 128 bytes per vector (83% reduction).

**When to use PQ**:
- Extremely large datasets (billions of vectors).
- Memory is the primary constraint.
- Some recall loss (5-10%) is acceptable.

### Quantization Trade-offs

```yaml
quantization_methods:
  none:
    memory: 3072 bytes (768-dim float32)
    recall: ~100%
    use_case: "Highest accuracy, small datasets"
  
  scalar_8bit:
    memory: 768 bytes
    recall: ~98-99%
    use_case: "General optimization"
  
  pq_8x8:
    memory: 64 bytes
    recall: ~90-95%
    use_case: "Large-scale, memory-constrained"
  
  pq_4x8:
    memory: 32 bytes
    recall: ~85-90%
    use_case: "Billions of vectors"
```

## IVF (Inverted File Index) Parameters

IVF clusters vectors and only searches the nearest clusters during query. It is fast and memory-efficient but requires careful parameter tuning.

### Key Parameters

**nlist (Number of clusters)**:
Controls the granularity of the inverted file index.

- nlist = sqrt(N): Recommended baseline (N = dataset size).
- Higher nlist: Smaller clusters, faster search (fewer vectors to scan) but increased indexing time.
- Lower nlist: Larger clusters, slower search but better recall.

```python
import faiss

# Create IVF index with HNSW for cluster assignment
d = 768
nlist = 4096  # For 10M vectors: sqrt(10M) ~ 3162

quantizer = faiss.IndexHNSWFlat(d, 32)  # HNSW for cluster assignment
index = faiss.IndexIVFFlat(quantizer, d, nlist, faiss.METRIC_INNER_PRODUCT)
index.train(vectors)
index.add(vectors)

# Set nprobe at query time
index.nprobe = 100  # Number of clusters to probe
```

**nprobe (Number of clusters to probe)**:
Set at query time. Higher values improve recall but increase latency.

- Start with nprobe = nlist / 10.
- Increase until recall target is met.
- Each doubling of nprobe roughly doubles search time but improves recall by diminishing amounts.

## Filtered Search Performance

Searching with metadata filters (e.g., "find similar to X where category = books") is one of the hardest problems in vector search.

### Pre-Filtering vs Post-Filtering

**Post-filtering**: Run the vector search, then apply metadata filters to results. Simple but can miss results if the top-k vectors are all filtered out.

```python
# Post-filtering (may return fewer than k results)
unfiltered = collection.search(query, limit=5000)
filtered = [r for r in unfiltered if r.metadata["category"] == "books"]
final = filtered[:10]
# Problem: What if none of the top 5000 are in "books"?
```

**Pre-filtering**: Apply metadata filters first, then search on the filtered subset. More accurate but slower because the filtered subset may be fragmented.

```python
# Pre-filtering with Milvus
results = collection.search(
    data=[query_vector],
    anns_field="embedding",
    param={"metric_type": "IP", "params": {"nprobe": 100}},
    limit=10,
    expr='category == "books" and year > 2020'
)
```

Pre-filtering is generally preferred for accuracy. Optimization focuses on making it fast.

### Optimization Strategies for Filtered Search

1. **Filter-aware HNSW**: Some databases (Milvus 2.4+, Qdrant) use HNSW variants that store filter metadata in graph nodes, enabling efficient filter-skip during traversal.

2. **Bitmask filtering**: Convert filter conditions to bitmasks that can be evaluated in bulk using SIMD instructions.

```python
# Bitmask-based fast filtering
import numpy as np

def create_bitmask(metadata_df, category):
    """Create a bitmask for fast filtering."""
    mask = np.zeros(len(metadata_df), dtype=bool)
    mask[metadata_df["category"] == category] = True
    return mask

def filtered_search(query, index, mask):
    """Search with bitmask-based filtering."""
    # Step 1: Run approximate search on all vectors
    distances, indices = index.search(query.reshape(1, -1), 1000)
    
    # Step 2: Fast mask-based filter using numpy boolean indexing
    valid = mask[indices[0]]
    filtered_distances = distances[0][valid]
    filtered_indices = indices[0][valid]
    
    return filtered_indices[:10], filtered_distances[:10]
```

3. **Run separate indexes**: For each filter value, maintain a separate HNSW index.

```python
# Per-category indexes
indexes = {}
for category in ["books", "movies", "music"]:
    category_vectors = all_vectors[labels == category]
    idx = faiss.IndexHNSWFlat(d, 16)
    idx.add(category_vectors)
    indexes[category] = idx

# Query using the correct index
idx = indexes["books"]
results = idx.search(query_vector, 10)
```

4. **Sparse-dense hybrid search**: Combine keyword-based BM25 search with vector search. Filters that match many documents (e.g., "year > 2020") are handled by the vector index. Filters that match few documents (e.g., "author = rare_name") are handled by sparse retrieval.

## Multi-Vector Indexing

Some use cases require indexing multiple vectors per document (e.g., several paragraphs from one article, or multi-modal embeddings).

### Multi-Vector Challenges

- Each document has N vectors, requiring N queries for standard search.
- Scoring must aggregate across all vectors per document.

### Optimization Techniques

1. **ColBERT-style late interaction**: Store all vectors but compute similarity between query and each document vector. Aggregate using MaxSim.

2. **Mean pooling**: Average all vectors per document into a single vector. Simple and fast but loses detail.

```python
def mean_pool_vectors(document_vectors):
    """Average all vectors in a document into one."""
    return np.mean(document_vectors, axis=0)
```

3. **Centroid aggregation**: Cluster each document's vectors into K centroids. Search against centroids, then refine with full vectors.

## Production Tuning Checklist

- [ ] Set HNSW M=16 and efConstruction=200 as baseline.
- [ ] Tune ef at query time based on latency/recall requirements.
- [ ] Use scalar quantization (8-bit) if memory is constrained.
- [ ] Use product quantization only for billion-scale datasets.
- [ ] Set IVF nlist to sqrt(N) and tune nprobe empirically.
- [ ] Prefer pre-filtering over post-filtering for filtered search.
- [ ] Consider separate indexes per filter category for high-cardinality filters.
- [ ] Benchmark recall at various ef/nprobe values before production deployment.
- [ ] Monitor index memory usage and set memory limits.

## Conclusion

Vector search optimization requires balancing recall, latency, memory, and indexing speed. Start with HNSW tuned to medium parameters (M=16, efConstruction=200). Add scalar quantization if memory is tight. Use IVF for very large datasets. Handle filtered search with pre-filtering or separate indexes. For multi-vector documents, consider averaging or centroid-based approaches. Always benchmark your specific dataset and query patterns before deploying optimization techniques.
