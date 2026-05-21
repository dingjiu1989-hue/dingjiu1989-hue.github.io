---
title: "Running LLMs Locally"
description: "Step-by-step guide to running LLMs locally using Ollama and LM Studio with setup instructions, model selection, and performance tips."
date: 2025-12-12
board: ai
url: https://dingjiu1989-hue.github.io/en/ai/local-llm-setup.html
---

# Running LLMs Locally

## Introduction

Running large language models locally has become practical thanks to quantization techniques, efficient inference engines, and a thriving open-source ecosystem. Whether for privacy, cost savings, or offline availability, local LLMs offer a compelling alternative to cloud APIs for many workloads. This guide covers the two most popular local LLM platforms — Ollama and LM Studio.

## Ollama

[Ollama](<https://ollama.ai>) is the most popular tool for running LLMs locally, known for its simplicity and command-line focus.

## Installation

## macOS

brew install ollama

## Linux

curl -fsSL https://ollama.ai/install.sh | sh

## Windows

## Download from https://ollama.ai/download

## Getting Started

Ollama makes running a model a single command:

## Pull and run a model

ollama run llama3.2:3b

## List available models

ollama list

## Pull a specific model without running

ollama pull mistral:7b

## Popular Models for Ollama

| Model | Size | RAM Required | Best For |

|-------|------|-------------|----------|

| Llama 3.2 3B | 2.0 GB | 4 GB | Fast responses, simple tasks |

| Llama 3.1 8B | 4.7 GB | 8 GB | General purpose Q&A; |

| Mistral 7B | 4.1 GB | 8 GB | Code, reasoning, instruction following |

| Qwen2.5 7B | 4.8 GB | 8 GB | Strong multilingual, coding |

| Mixtral 8x7B | 26 GB | 48 GB | High quality, close to GPT-3.5 |

| DeepSeek-R1 7B | 4.5 GB | 8 GB | Strong reasoning, step-by-step |

## Using Ollama Programmatically

Ollama provides a REST API at `http://localhost:11434`:

import requests

response = requests.post("http://localhost:11434/api/generate", json={

"model": "llama3.2:3b",

"prompt": "Explain quantum computing in three sentences.",

"stream": False

})

print(response.json()["response"])

Or use the official Python library:

import ollama

response = ollama.chat(model="llama3.2:3b", messages=[

{"role": "user", "content": "What is the capital of France?"}

])

print(response["message"]["content"])

## Custom Modelfiles

Create custom models with system prompts and parameters:

FROM llama3.1:8b

## Set system prompt

SYSTEM "You are a helpful coding assistant. Provide concise code examples."

## Configure parameters

PARAMETER temperature 0.3

PARAMETER top_p 0.9

Build and run:

ollama create my-coding-assistant -f Modelfile

ollama run my-coding-assistant

## LM Studio

[LM Studio](<https://lmstudio.ai>) is a GUI-focused alternative that excels for users who prefer visual interfaces and easy model browsing.

## Key Features

  * **Built-in model browser** : Search and download models from Hugging Face

  * **GUI chat interface** : Familiar ChatGPT-like experience

  * **Local API server** : OpenAI-compatible API endpoint

  * **Model configuration** : Easy sliders for context length, GPU offloading, and temperature

  * **Multi-model support** : Load multiple models and switch between them




## Setup

  * Download from [lmstudio.ai](<https://lmstudio.ai>)



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Open the app and browse the model catalog

3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Download a model (start with Llama 3.2 3B or Mistral 7B)

4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Load the model and start chatting

## API Server

LM Studio can serve models via an OpenAI-compatible API:

http://localhost:1234/v1/chat/completions

This means any tool that works with OpenAI's API can use your local model by changing the base URL:

from openai import OpenAI

client = OpenAI(

base_url="http://localhost:1234/v1",

api_key="not-needed"

)

response = client.chat.completions.create(

model="local-model",

messages=[{"role": "user", "content": "Hello!"}]

)

## Performance Optimization

## Quantization Levels

Quantization reduces model size at the cost of some accuracy:

  * **Q4_K_M** : Best balance of quality and size (4-bit, recommended)

  * **Q5_K_M** : Higher quality, larger (5-bit, use if you have RAM headroom)

  * **Q8_0** : Near-full quality, 2x RAM requirement

  * **Q2_K** : Minimal RAM, noticeable quality loss




Rule of thumb: each quantization step roughly doubles model size but improves quality marginally. Q4_K_M is the sweet spot.

## GPU Acceleration

Both Ollama and LM Studio support GPU acceleration via CUDA (NVIDIA), Metal (Apple Silicon), or Vulkan (AMD):

## Ollama uses Metal automatically on Apple Silicon

## For NVIDIA, install CUDA and Ollama detects it

## Check which device is being used

ollama run llama3.2:3b --verbose

## Context Window

Larger context windows consume more memory. A 128K context with Q4_K_M requires approximately:

  * 7B model: ~8 GB total

  * 13B model: ~14 GB total

  * 70B model: ~48 GB total




## Use Cases for Local LLMs

  * **Privacy-sensitive data** : Medical records, legal documents, personal information

  * **Offline environments** : Air-gapped systems, travel, remote locations

  * **Cost-sensitive workloads** : High-volume batch processing

  * **Experimentation** : Rapid testing of different models without API costs

  * **Latency-critical applications** : No network calls for inference




## Conclusion

Running LLMs locally is easier than ever with Ollama and LM Studio. Ollama offers command-line simplicity and a rich set of pre-built models. LM Studio provides a polished GUI and OpenAI-compatible API. Start with a 7B model at Q4_K_M quantization on a machine with 8-16 GB of RAM, and scale up as your needs grow. Local LLMs won't replace cloud APIs for every use case, but they are an essential tool in the AI practitioner's toolkit.

**See also:** [LLM Fine-Tuning Guide](</en/ai/llm-fine-tuning.html>), [AI API Cost Optimization](</en/ai/ai-api-cost-optimization.html>), [Natural Language to SQL with LLMs](</en/ai/ai-database-query.html>).

**See also:** [LLM Fine-Tuning Guide](</en/ai/llm-fine-tuning.html>), [Natural Language to SQL with LLMs](</en/ai/ai-database-query.html>), [Testing Strategies for AI Applications](</en/ai/ai-testing-strategies.html>)

**See also:** [LLM Fine-Tuning Guide](</en/ai/llm-fine-tuning.html>), [Natural Language to SQL with LLMs](</en/ai/ai-database-query.html>), [Testing Strategies for AI Applications](</en/ai/ai-testing-strategies.html>)

**See also:** [LLM Fine-Tuning Guide](</en/ai/llm-fine-tuning.html>), [Natural Language to SQL with LLMs](</en/ai/ai-database-query.html>), [Testing Strategies for AI Applications](</en/ai/ai-testing-strategies.html>)

**See also:** [LLM Fine-Tuning Guide](</en/ai/llm-fine-tuning.html>), [Natural Language to SQL with LLMs](</en/ai/ai-database-query.html>), [Testing Strategies for AI Applications](</en/ai/ai-testing-strategies.html>)

**See also:** [LLM Fine-Tuning Guide](</en/ai/llm-fine-tuning.html>), [Natural Language to SQL with LLMs](</en/ai/ai-database-query.html>), [Testing Strategies for AI Applications](</en/ai/ai-testing-strategies.html>)

**See also:** [AI Embeddings Explained](</en/ai/ai-embeddings-explained.html>), [AI Image Generation Guide](</en/ai/ai-image-generation.html>), [RAG Architecture Guide](</en/ai/rag-architecture-guide.html>)

**See also:** [AI Embeddings Explained](</en/ai/ai-embeddings-explained.html>), [AI Image Generation Guide](</en/ai/ai-image-generation.html>), [RAG Architecture Guide](</en/ai/rag-architecture-guide.html>)

**See also:** [AI Embeddings Explained](</en/ai/ai-embeddings-explained.html>), [AI Image Generation Guide](</en/ai/ai-image-generation.html>), [RAG Architecture Guide](</en/ai/rag-architecture-guide.html>)

**See also:** [AI Embeddings Explained](</en/ai/ai-embeddings-explained.html>), [AI Image Generation Guide](</en/ai/ai-image-generation.html>), [RAG Architecture Guide](</en/ai/rag-architecture-guide.html>)

**See also:** [AI Embeddings Explained](</en/ai/ai-embeddings-explained.html>), [AI Image Generation Guide](</en/ai/ai-image-generation.html>), [RAG Architecture Guide](</en/ai/rag-architecture-guide.html>)

**See also:** [AI Embeddings Explained](</en/ai/ai-embeddings-explained.html>), [AI Image Generation Guide](</en/ai/ai-image-generation.html>), [RAG Architecture Guide](</en/ai/rag-architecture-guide.html>)

**See also:** [AI Embeddings Explained](</en/ai/ai-embeddings-explained.html>), [AI Image Generation Guide](</en/ai/ai-image-generation.html>), [RAG Architecture Guide](</en/ai/rag-architecture-guide.html>)

**See also:** [AI Embeddings Explained](</en/ai/ai-embeddings-explained.html>), [AI Image Generation Guide](</en/ai/ai-image-generation.html>), [RAG Architecture Guide](</en/ai/rag-architecture-guide.html>)

**See also:** [AI Embeddings Explained](</en/ai/ai-embeddings-explained.html>), [AI Image Generation Guide](</en/ai/ai-image-generation.html>), [RAG Architecture Guide](</en/ai/rag-architecture-guide.html>)

**See also:** [AI Embeddings Explained](</en/ai/ai-embeddings-explained.html>), [AI Image Generation Guide](</en/ai/ai-image-generation.html>), [RAG Architecture Guide](</en/ai/rag-architecture-guide.html>)

**See also:** [AI Embeddings Explained](</en/ai/ai-embeddings-explained.html>), [AI Image Generation Guide](</en/ai/ai-image-generation.html>), [RAG Architecture Guide](</en/ai/rag-architecture-guide.html>)

**See also:** [AI Embeddings Explained](</en/ai/ai-embeddings-explained.html>), [AI Image Generation Guide](</en/ai/ai-image-generation.html>), [RAG Architecture Guide](</en/ai/rag-architecture-guide.html>)
