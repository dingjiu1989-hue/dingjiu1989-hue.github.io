---
title: "Multi-Modal RAG: Images, Tables, Documents — Chunking and Retrieval"
description: "Build multi-modal RAG systems that handle images, tables, and documents. Learn chunking strategies, embedding approaches, and retrieval fusion for different dat"
date: 2026-02-17
board: ai
url: https://dingjiu1989-hue.github.io/en/ai/multi-modal-rag.html
---

# Multi-Modal RAG: Images, Tables, Documents — Chunking and Retrieval

## Introduction

Real-world documents contain more than text: images, charts, tables, and diagrams carry critical information that text-only RAG systems cannot access. Multi-modal RAG extends retrieval to include visual content, enabling questions like "What does the Q3 revenue chart show?" or "What values are in the configuration table?" This article covers the architectures and techniques for building multi-modal RAG.

## Strategies for Multi-Modal RAG

There are three main approaches to handling non-text content:

## Strategy 1: Convert everything to text (simplest)

## Strategy 2: Embed images alongside text (moderate)

## Strategy 3: Multi-modal retrieval with specialized models (most powerful)

## Strategy 1: Text Conversion

Convert images and tables to text using vision models or OCR:

from openai import OpenAI

import base64

client = OpenAI()

def describe_image(image_path: str) -> str:

with open(image_path, "rb") as f:

image_data = base64.b64encode(f.read()).decode("utf-8")

response = client.chat.completions.create(

model="gpt-4o",

messages=[

{

"role": "user",

"content": [

{"type": "text", "text": "Describe this image in detail, including all text, data points, and visual elements."},

{"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_data}"}},

],

}

],

max_tokens=1024,

)

return response.choices[0].message.content

def convert_table_to_text(table_data: list[list[str]]) -> str:

"""Convert a parsed table to searchable text."""

headers = table_data[0]

rows = table_data[1:]

text_parts = []

for row in rows:

row_desc = ", ".join(f"{headers[i]}: {cell}" for i, cell in enumerate(row))

text_parts.append(row_desc)

return "\n".join(text_parts)

## Strategy 2: Multi-Vector Retriever

Store both text representations and visual embeddings:

from langchain.retrievers.multi_vector import MultiVectorRetriever

from langchain.storage import InMemoryStore

from langchain.vectorstores import Chroma

from langchain.embeddings import OpenAIEmbeddings

from langchain.schema.document import Document

## Store text summaries alongside raw elements

vectorstore = Chroma(

collection_name="multi_modal_docs",

embedding_function=OpenAIEmbeddings(),

)

store = InMemoryStore()

retriever = MultiVectorRetriever(

vectorstore=vectorstore,

docstore=store,

id_key="doc_id",

)

## For each document element (text, image, table):

## 1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Generate a text summary

## 2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Store the summary in the vector store

## 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Store the original element in the doc store

## 4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Link them with a shared doc_id

doc_id = "doc_001_image_03"

summary = "Revenue chart showing Q1-Q4 2025: Q1=$1.2M, Q2=$1.5M, Q3=$1.8M, Q4=$2.1M"

original = Document(

page_content="[IMAGE: revenue_chart_2025.png]",

metadata={"type": "image", "path": "revenue_chart_2025.png", "doc_id": doc_id},

)

retriever.vectorstore.add_documents([Document(page_content=summary, metadata={"doc_id": doc_id})])

retriever.docstore.mset([(doc_id, original)])

## Strategy 3: Multi-Modal Embeddings

Use embedding models that handle both text and images in a shared space:

from sentence_transformers import SentenceTransformer

import torch

from PIL import Image

class MultiModalEmbedder:

def **init**(self, model_name="clip-ViT-B-32"):

self.model = SentenceTransformer(model_name)

def embed_text(self, text: str) -> list[float]:

return self.model.encode(text).tolist()

def embed_image(self, image_path: str) -> list[float]:

image = Image.open(image_path)

return self.model.encode(image).tolist()

def search_by_text(self, query: str, image_embeddings: list, top_k: int = 5):

query_emb = self.embed_text(query)

scores = torch.cosine_similarity(

torch.tensor(query_emb).unsqueeze(0),

torch.tensor(image_embeddings),

)

top_indices = scores.topk(top_k).indices.tolist()

return top_indices, scores[top_indices].tolist()

## Chunking Strategies for Multi-Modal Data

Each content type needs a different chunking approach:

class MultiModalChunker:

def chunk_pdf(self, pdf_path: str) -> list[dict]:

"""Extract and chunk text, images, and tables from a PDF."""

import fitz # PyMuPDF

doc = fitz.open(pdf_path)

chunks = []

for page_num, page in enumerate(doc):

## Extract text blocks

blocks = page.get_text("dict")["blocks"]

for block in blocks:

if block["type"] == 0: # Text

text = block["lines"][0]["spans"][0]["text"]

chunks.append({

"type": "text",

"content": text,

"page": page_num,

"bbox": block["bbox"],

})

elif block["type"] == 1: # Image

image = block["image"]

chunks.append({

"type": "image",

"content": f"[IMAGE: page_{page_num}_block_{block['number']}]",

"page": page_num,

"image_data": image,

"bbox": block["bbox"],

})

return chunks

def chunk_table(self, table_df) -> dict:

"""Convert table to searchable format."""

summary = f"Table with {len(table_df)} rows and {len(table_df.columns)} columns: {', '.join(table_df.columns)}"

text_representation = table_df.to_markdown()

return {

"type": "table",

"summary": summary,

"content": text_representation,

"metadata": {"columns": list(table_df.columns), "rows": len(table_df)},

}

## Retrieval and Fusion

Query across all content types and fuse the results:

def multi_modal_retrieve(query: str, text_index, image_index, table_index, top_k: int = 3):

text_results = text_index.similarity_search(query, k=top_k)

image_results = search_images(query, image_index, top_k)

table_results = search_tables(query, table_index, top_k)

## Fuse results with type-aware scoring

all_results = []

for doc in text_results:

all_results.append({"content": doc.page_content, "type": "text", "score": 1.0})

for img in image_results:

all_results.append({"content": img["description"], "type": "image", "path": img["path"], "score": 0.9})

for tbl in table_results:

all_results.append({"content": tbl["summary"], "type": "table", "data": tbl["content"], "score": 0.9})

all_results.sort(key=lambda x: x["score"], reverse=True)

return all_results[:top_k * 2]

## Conclusion

Multi-modal RAG extends retrieval to images, tables, and other visual content. The simplest approach converts non-text content to text descriptions using vision models. More sophisticated approaches use multi-vector retrievers or shared embedding spaces like CLIP. Choose your strategy based on the complexity of your visual content and the precision required for retrieval. Always evaluate retrieval quality separately for each modality.

**See also:** [RAG Pipeline Optimization: Production Best Practices](</en/ai/rag-pipeline-optimization.html>), [RAG Chunking Strategies: Semantic Chunking, Overlapping, Recursive Splitting](</en/ai/rag-chunking-strategies.html>), [RAG Evaluation: Retrieval Metrics, Generation Quality, End-to-End Testing, and Datasets](</en/ai/rag-evaluation.html>).

**See also:** [RAG Agent Patterns: Self-Query, Corrective, Adaptive Retrieval](</en/ai/rag-agent-patterns.html>), [RAG Pipeline Optimization: Production Best Practices](</en/ai/rag-pipeline-optimization.html>), [Fine-Tuning vs RAG: When to Use Each, Hybrid Approaches, Cost Comparison](</en/ai/fine-tuning-vs-rag.html>)

**See also:** [RAG Agent Patterns: Self-Query, Corrective, Adaptive Retrieval](</en/ai/rag-agent-patterns.html>), [RAG Pipeline Optimization: Production Best Practices](</en/ai/rag-pipeline-optimization.html>), [Fine-Tuning vs RAG: When to Use Each, Hybrid Approaches, Cost Comparison](</en/ai/fine-tuning-vs-rag.html>)

**See also:** [RAG Agent Patterns: Self-Query, Corrective, Adaptive Retrieval](</en/ai/rag-agent-patterns.html>), [RAG Pipeline Optimization: Production Best Practices](</en/ai/rag-pipeline-optimization.html>), [Fine-Tuning vs RAG: When to Use Each, Hybrid Approaches, Cost Comparison](</en/ai/fine-tuning-vs-rag.html>)

**See also:** [RAG Agent Patterns: Self-Query, Corrective, Adaptive Retrieval](</en/ai/rag-agent-patterns.html>), [RAG Pipeline Optimization: Production Best Practices](</en/ai/rag-pipeline-optimization.html>), [Fine-Tuning vs RAG: When to Use Each, Hybrid Approaches, Cost Comparison](</en/ai/fine-tuning-vs-rag.html>)

**See also:** [RAG Agent Patterns: Self-Query, Corrective, Adaptive Retrieval](</en/ai/rag-agent-patterns.html>), [RAG Pipeline Optimization: Production Best Practices](</en/ai/rag-pipeline-optimization.html>), [Fine-Tuning vs RAG: When to Use Each, Hybrid Approaches, Cost Comparison](</en/ai/fine-tuning-vs-rag.html>)

**See also:** [RAG Retrieval Optimization: Hybrid Search, Re-Ranking, Query Transformation](</en/ai/rag-retrieval-optimization.html>), [AI Agents: Architecture and Implementation](</en/ai/ai-agents-overview.html>), [LLM Fine-Tuning Strategies and Techniques](</en/ai/fine-tuning-strategies.html>)

**See also:** [RAG Retrieval Optimization: Hybrid Search, Re-Ranking, Query Transformation](</en/ai/rag-retrieval-optimization.html>), [AI Agents: Architecture and Implementation](</en/ai/ai-agents-overview.html>), [LLM Fine-Tuning Strategies and Techniques](</en/ai/fine-tuning-strategies.html>)

**See also:** [RAG Retrieval Optimization: Hybrid Search, Re-Ranking, Query Transformation](</en/ai/rag-retrieval-optimization.html>), [AI Agents: Architecture and Implementation](</en/ai/ai-agents-overview.html>), [LLM Fine-Tuning Strategies and Techniques](</en/ai/fine-tuning-strategies.html>)

**See also:** [RAG Retrieval Optimization: Hybrid Search, Re-Ranking, Query Transformation](</en/ai/rag-retrieval-optimization.html>), [AI Agents: Architecture and Implementation](</en/ai/ai-agents-overview.html>), [LLM Fine-Tuning Strategies and Techniques](</en/ai/fine-tuning-strategies.html>)

**See also:** [RAG Retrieval Optimization: Hybrid Search, Re-Ranking, Query Transformation](</en/ai/rag-retrieval-optimization.html>), [AI Agents: Architecture and Implementation](</en/ai/ai-agents-overview.html>), [LLM Fine-Tuning Strategies and Techniques](</en/ai/fine-tuning-strategies.html>)

**See also:** [RAG Retrieval Optimization: Hybrid Search, Re-Ranking, Query Transformation](</en/ai/rag-retrieval-optimization.html>), [AI Agents: Architecture and Implementation](</en/ai/ai-agents-overview.html>), [LLM Fine-Tuning Strategies and Techniques](</en/ai/fine-tuning-strategies.html>)

**See also:** [RAG Retrieval Optimization: Hybrid Search, Re-Ranking, Query Transformation](</en/ai/rag-retrieval-optimization.html>), [AI Agents: Architecture and Implementation](</en/ai/ai-agents-overview.html>), [LLM Fine-Tuning Strategies and Techniques](</en/ai/fine-tuning-strategies.html>)

**See also:** [RAG Retrieval Optimization: Hybrid Search, Re-Ranking, Query Transformation](</en/ai/rag-retrieval-optimization.html>), [AI Agents: Architecture and Implementation](</en/ai/ai-agents-overview.html>), [LLM Fine-Tuning Strategies and Techniques](</en/ai/fine-tuning-strategies.html>)

**See also:** [RAG Retrieval Optimization: Hybrid Search, Re-Ranking, Query Transformation](</en/ai/rag-retrieval-optimization.html>), [AI Agents: Architecture and Implementation](</en/ai/ai-agents-overview.html>), [LLM Fine-Tuning Strategies and Techniques](</en/ai/fine-tuning-strategies.html>)

**See also:** [RAG Retrieval Optimization: Hybrid Search, Re-Ranking, Query Transformation](</en/ai/rag-retrieval-optimization.html>), [AI Agents: Architecture and Implementation](</en/ai/ai-agents-overview.html>), [LLM Fine-Tuning Strategies and Techniques](</en/ai/fine-tuning-strategies.html>)

**See also:** [RAG Retrieval Optimization: Hybrid Search, Re-Ranking, Query Transformation](</en/ai/rag-retrieval-optimization.html>), [AI Agents: Architecture and Implementation](</en/ai/ai-agents-overview.html>), [LLM Fine-Tuning Strategies and Techniques](</en/ai/fine-tuning-strategies.html>)

**See also:** [RAG Retrieval Optimization: Hybrid Search, Re-Ranking, Query Transformation](</en/ai/rag-retrieval-optimization.html>), [AI Agents: Architecture and Implementation](</en/ai/ai-agents-overview.html>), [LLM Fine-Tuning Strategies and Techniques](</en/ai/fine-tuning-strategies.html>)
