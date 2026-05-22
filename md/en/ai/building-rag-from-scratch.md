---
title: "Building RAG From Scratch: A 200-Line Implementation Without Frameworks"
description: "Build Retrieval-Augmented Generation from scratch with raw OpenAI API, pgvector, and Python — understand every line before using LangChain or LlamaIndex."
date: 2025-11-14
board: ai
url: https://aidev.fit/en/ai/building-rag-from-scratch.html
---

# Building RAG From Scratch: A 200-Line Implementation Without Frameworks

## RAG Without Frameworks

Retrieval-Augmented Generation (RAG) is the most practical AI pattern of the decade: give an LLM access to your documents so it can answer questions grounded in your data. While LangChain and LlamaIndex make RAG easy to prototype, they add abstractions that hide what's actually happening. Building RAG from scratch — with raw API calls, a vector database, and ~200 lines of code — gives you complete control and a deeper understanding. Here's how.

## The RAG Pipeline (Five Steps)
    
    
    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │ 1. Load  │───▶│ 2. Chunk │───▶│ 3. Embed │───▶│ 4. Store  │───▶│ 5. Query │
    │Documents │    │Documents │    │ Chunks   │    │ Vectors   │    │ & Generate│
    └──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
    

## Step 1: Load Documents
    
    
    # Minimal document loader — supports .txt, .md, .pdf
    import pathlib
    import pypdf  # for PDF support
    
    def load_documents(path: str) -> list[dict]:
        docs = []
        for file in pathlib.Path(path).rglob("*"):
            if file.suffix == ".txt":
                docs.append({"text": file.read_text(), "source": str(file)})
            elif file.suffix == ".md":
                docs.append({"text": file.read_text(), "source": str(file)})
            elif file.suffix == ".pdf":
                reader = pypdf.PdfReader(file)
                text = "
    ".join(page.extract_text() for page in reader.pages)
                docs.append({"text": text, "source": str(file)})
        return docs

## Step 2: Chunk Documents
    
    
    def chunk_document(text: str, chunk_size=500, overlap=50) -> list[str]:
        """Split text into overlapping chunks, respecting paragraph boundaries."""
        paragraphs = text.split("
    
    ")
        chunks = []
        current = ""
        for para in paragraphs:
            if len(current) + len(para) <= chunk_size:
                current += para + "
    
    "
            else:
                if current:
                    chunks.append(current.strip())
                # If a single paragraph exceeds chunk_size, split by sentences
                if len(para) > chunk_size:
                    sentences = para.replace(". ", ".|").split("|")
                    sub = ""
                    for s in sentences:
                        if len(sub) + len(s) <= chunk_size:
                            sub += s + ". "
                        else:
                            chunks.append(sub.strip())
                            sub = s + ". "
                    current = sub + "
    
    "
                else:
                    current = para + "
    
    "
        if current.strip():
            chunks.append(current.strip())
        return chunks

## Step 3: Generate Embeddings
    
    
    from openai import OpenAI
    client = OpenAI()
    
    def embed_batch(texts: list[str], model="text-embedding-3-small") -> list[list[float]]:
        """Generate embeddings for a batch of texts."""
        resp = client.embeddings.create(input=texts, model=model)
        return [d.embedding for d in resp.data]
    
    # For self-hosted: use sentence-transformers
    # from sentence_transformers import SentenceTransformer
    # model = SentenceTransformer("BAAI/bge-m3")
    # embeddings = model.encode(texts, normalize_embeddings=True)

## Step 4: Store in Vector Database
    
    
    import psycopg
    import numpy as np
    
    def setup_pgvector():
        conn = psycopg.connect("postgresql://localhost/rag_demo")
        conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                content TEXT,
                source TEXT,
                embedding vector(1536)
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_embedding
            ON documents USING hnsw (embedding vector_cosine_ops)
        """)
        return conn
    
    def insert_documents(conn, chunks, sources, embeddings):
        for chunk, source, emb in zip(chunks, sources, embeddings):
            conn.execute(
                "INSERT INTO documents (content, source, embedding) VALUES (%s, %s, %s)",
                (chunk, source, emb)
            )
        conn.commit()

## Step 5: Query and Generate
    
    
    def retrieve(conn, query: str, k: int = 5) -> list[dict]:
        """Vector search + optional keyword boost."""
        query_embedding = embed_batch([query])[0]
        results = conn.execute("""
            SELECT content, source,
                   1 - (embedding <=> %s::vector) AS similarity
            FROM documents
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        """, (query_embedding, query_embedding, k)).fetchall()
        return [{"content": r[0], "source": r[1], "score": r[2]} for r in results]
    
    def generate_answer(query: str, context_docs: list[dict]) -> str:
        """Generate answer grounded in retrieved context."""
        context = "
    
    ---
    
    ".join(
            f"Source: {d['source']}
    {d['content']}"
            for d in context_docs
        )
        prompt = f"""Answer the question based ONLY on the provided context.
    If the context doesn't contain the answer, say "I don't have enough information."
    
    Context:
    {context}
    
    Question: {query}
    
    Answer (with citations):"""
    
        resp = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1000
        )
        return resp.choices[0].message.content
    
    # Tying it together:
    # docs = load_documents("./my_docs")
    # chunks = []
    # sources = []
    # for doc in docs:
    #     for chunk in chunk_document(doc["text"]):
    #         chunks.append(chunk)
    #         sources.append(doc["source"])
    # embeddings = []
    # for i in range(0, len(chunks), 20):  # batch of 20
    #     embeddings.extend(embed_batch(chunks[i:i+20]))
    # conn = setup_pgvector()
    # insert_documents(conn, chunks, sources, embeddings)
    # answer = generate_answer("How do I deploy?", retrieve(conn, "How do I deploy?"))

## Production Hardening: What the Frameworks Give You

Capability| DIY| LangChain/LlamaIndex  
---|---|---  
Multiple chunking strategies| Write your own| Built-in: recursive, semantic, sentence, agentic  
Metadata filtering| SQL WHERE clauses| Structured query language, auto-metadata extraction  
Async + streaming| asyncio, SSE (manual)| Built-in streaming, async pipeline  
Re-ranking| Call Cohere API, or self-host BGE-Reranker| Pluggable re-rankers (Cohere, BGE, ColBERT)  
Evaluation (faithfulness, relevance)| Write your own tests + RAGAS library| Built-in evaluation harness  
Multi-modal (images, tables)| Manual: extract description, embed separately| LlamaParse, Unstructured.io for PDF parsing  
Agentic RAG (query routing, tool use)| Manual routing logic| Router chains, agent executors  
  
**When to DIY vs use a framework:** Build from scratch when: you're learning RAG, your use case is simple (single document type, straightforward queries), or you need complete control over the pipeline. Use a framework when: you need multi-modal parsing (PDFs with tables/images), you're iterating rapidly on chunking/retrieval strategies, or you need evaluation tooling built in. The right answer for most production projects: build from scratch to understand the fundamentals, then consider LlamaIndex for production when you need its advanced document parsing and evaluation features.

**The key insight:** RAG is not magic — it's document loading + text chunking + embedding generation + vector search + prompt construction. Each step is simple and testable in isolation. The frameworks add convenience, not fundamentally new capabilities. Understanding the raw pipeline will serve you better than memorizing any framework's API. See also: [RAG Best Practices](</en/ai/rag-best-practices.html>) and [Embedding Models Comparison](</en/ai/embedding-models-comparison.html>).

**See also:** [Building Multimodal AI Applications: Vision, Audio, and Text Combined (2026)](</en/ai/multimodal-ai-guide.html>), [RAG Evaluation: Retrieval Metrics, Generation Quality, End-to-End Testing, and Datasets](</en/ai/rag-evaluation.html>), [RAG Pipeline Optimization: Production Best Practices](</en/ai/rag-pipeline-optimization.html>)
