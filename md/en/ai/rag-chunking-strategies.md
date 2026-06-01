---
title: "RAG Chunking Strategies: Semantic Chunking, Overlapping, Recursive Splitting"
description: "Master document chunking for RAG pipelines: semantic chunking with embeddings, overlapping strategies for context preservation, and recursive splitting for hete"
date: 2026-02-18
board: ai
url: https://aidev.fit/en/ai/rag-chunking-strategies.html
---

# RAG Chunking Strategies: Semantic Chunking, Overlapping, Recursive Splitting

## Introduction

Document chunking is the foundation of any RAG system. How you split documents into chunks directly determines retrieval quality: chunks that are too small lose context, chunks that are too large dilute relevance, and naive splits break semantic units mid-thought. This article covers the major chunking strategies and when to use each.

## Naive Fixed-Size Chunking

The simplest approach splits text every N characters or tokens:

def fixed_size_chunks(text: str, chunk_size: int = 512, overlap: int = 64) -> list[str]:

chunks = []

start = 0

while start < len(text):

end = start + chunk_size

chunk = text[start:end]

chunks.append(chunk)

start = end - overlap

return chunks

Fixed-size chunking is fast and predictable. However, it frequently splits in the middle of sentences, paragraphs, or code blocks, producing chunks that are semantically incomplete. Use it only for homogeneous text where content quality is not critical.

## Recursive Character Text Splitter

LangChain's RecursiveCharacterTextSplitter tries to split on natural boundaries first, falling back to smaller separators:

from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(

chunk_size=512,

chunk_overlap=64,

separators=["

", " ", ".", " ", ""],

keep_separator=True,

)

chunks = splitter.split_text(long_document)

The algorithm tries each separator in order. It first attempts to split on paragraph boundaries (`

`). If a paragraph exceeds the chunk size, it splits on line breaks, then sentences, then spaces. This preserves as much natural structure as possible.

## Semantic Chunking

Semantic chunking uses embedding similarity to detect natural boundaries:

import numpy as np

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_chunk(text: str, threshold: float = 0.7) -> list[str]:

sentences = split_into_sentences(text)

chunks = []

current_chunk = [sentences[0]]

for i in range(1, len(sentences)):

## Encode as we go

emb_current = model.encode(" ".join(current_chunk[-3:]))

emb_next = model.encode(sentences[i])

similarity = cosine_similarity(emb_current, emb_next)

if similarity < threshold or len(" ".join(current_chunk)) > 1000:

chunks.append(" ".join(current_chunk))

current_chunk = [sentences[i]]

else:

current_chunk.append(sentences[i])

if current_chunk:

chunks.append(" ".join(current_chunk))

return chunks

Semantic chunking produces chunks that are internally coherent: each chunk discusses a single topic. The threshold controls chunk granularity. Lower values create larger chunks with more context; higher values create smaller, tighter chunks.

## Chunking by Document Structure

When documents have known structures (headings, sections), use the structure to define chunks:

import re

def structure_aware_chunk(markdown_text: str) -> list[dict]:

chunks = []

current_section = {"heading": "Introduction", "content": []}

for line in markdown_text.split(" "):

heading_match = re.match(r"^(#{1,3})\s+(.+)$", line)

if heading_match:

if current_section["content"]:

chunks.append(current_section)

current_section = {

"heading": heading_match.group(2),

"level": len(heading_match.group(1)),

"content": [],

}

else:

current_section["content"].append(line)

if current_section["content"]:

chunks.append(current_section)

return chunks

Structure-aware chunking preserves document hierarchy. Each chunk retains a heading reference, enabling richer retrieval context and more accurate citation.

## Sliding Window with Overlap

Overlap between adjacent chunks prevents information loss at boundaries:

def sliding_window_chunks(text: str, window: int = 512, stride: int = 384) -> list[str]:

chunks = []

for i in range(0, len(text) - window + 1, stride):

chunks.append(text[i:i + window])

return chunks

A 512-token window with 384-token stride means each adjacent pair overlaps by 128 tokens. This ensures that no query misses context that spans a chunk boundary. The trade-off is increased storage and more chunks to search.

## Choosing the Right Strategy

| Strategy | Best For | Pros | Cons |

|----------|----------|------|------|

| Fixed-size | Simple docs, testing | Fast, predictable | Breaks sentences |

| Recursive | General purpose | Natural boundaries | May still break context |

| Semantic | Narrative text | Topic coherence | Slower, model-dependent |

| Structure-aware | Markdown, HTML, code | Preserves hierarchy | Requires structured input |

| Sliding window | Dense technical docs | No information loss | More chunks, overlap |

## Conclusion

Chunking strategy is one of the highest-leverage decisions in RAG system design. Start with recursive character splitting for general use, add structure-aware splitting for documents with clear hierarchy, and adopt semantic chunking when topic coherence is critical. Always include overlap to prevent boundary information loss, and measure retrieval recall on your specific document types to validate your choice.
