---
title: "How to Run AI Models Locally: Ollama, LM Studio, and llama.cpp Guide"
description: "Run powerful AI models on your own machine — private, free, and offline. Complete setup guide for Ollama, LM Studio, and llama.cpp with model recommendations."
date: 2025-11-06
board: ai
url: https://aidev.fit/en/ai/run-local-ai-models.html
---

# How to Run AI Models Locally: Ollama, LM Studio, and llama.cpp Guide

Running AI models on your own machine means privacy, zero cost after setup, and offline access. With tools like Ollama, LM Studio, and llama.cpp, it's surprisingly easy. Here's how to get started and which models to run.

## Why Run AI Locally?

Reason| Detail  
---|---  
**Privacy**|  Code/data never leaves your machine. Essential for proprietary work.  
**Cost**|  Free after hardware. No API bills. No $20/mo subscription.  
**Offline**|  Work on a plane, in a coffee shop, or during API outages.  
**No limits**|  No rate limiting, no message caps, no content filters.  
**Experimentation**|  Try different models, fine-tune, experiment without paying per token.  
  
## The Three Tools Compared

| Ollama| LM Studio| llama.cpp  
---|---|---|---  
**Type**|  CLI + REST API| Desktop GUI| C++ library + CLI  
**Best for**|  Developers, automation| Non-technical users, chat| Maximum performance, servers  
**Setup**|  One command: brew install ollama| Download DMG, install| Compile or brew install  
**Model library**|  Built-in (ollama pull)| HuggingFace integration| GGUF files from HuggingFace  
**API**|  OpenAI-compatible REST| Local OpenAI-compatible| Server mode available  
**GPU support**|  Automatic (Metal/CUDA)| Automatic (Metal/CUDA)| Manual config  
  
## Getting Started with Ollama (Recommended for Developers)
    
    
    # 1. Install
    brew install ollama          # macOS
    # Linux: curl -fsSL https://ollama.com/install.sh | sh
    
    # 2. Pull and run a model
    ollama pull llama3.3:70b     # Meta's latest (70B parameters)
    ollama pull deepseek-coder-v2  # Best coding model
    ollama pull phi-4            # Microsoft's small but mighty model
    
    # 3. Chat in terminal
    ollama run deepseek-coder-v2
    
    # 4. Use as API (OpenAI-compatible)
    # POST http://localhost:11434/v1/chat/completions

## Recommended Models for Coding

Model| Size| RAM Needed| Best For  
---|---|---|---  
**DeepSeek Coder V2**|  16B| 16GB| Best coding quality for size. Runs on most laptops.  
**Llama 3.3 70B**|  70B| 48GB (q4: 40GB)| Best overall quality. Needs a powerful machine.  
**CodeLlama 70B**|  70B| 48GB (q4: 40GB)| Code-specialized. Good for autocomplete.  
**Phi-4**|  14B| 16GB| Best small model. Runs on any M-series Mac.  
**CodeQwen 2.5**|  7B| 8GB| Fastest. Runs on older hardware. Good for simple tasks.  
  
## Hardware Requirements

Machine| What You Can Run  
---|---  
M1/M2/M3 Mac (16GB)| 7B-16B models comfortably. 34B with some swap.  
M3 Max Mac (48GB+)| 70B models with q4 quantization. All coding models.  
PC with RTX 4090 (24GB)| 7B-34B models in VRAM. 70B split across GPU+RAM.  
PC with RTX 3060 (12GB)| 7B-13B models in VRAM.  
  
## When NOT to Use Local Models

  * You need the absolute best code quality (API models are still ahead).
  * You need image generation (local diffusion models are a different setup).
  * You need web search or real-time data.
  * You're on a low-RAM machine and can afford API costs.



**Bottom line:** Ollama + DeepSeek Coder V2 gives you excellent local coding on any M-series Mac. For maximum quality, use API models (Claude/GPT-4o). For privacy, off-grid, or cost reasons, local models are now genuinely useful for daily development. See also: [Best LLMs for Coding comparison](</en/ai/best-llms-for-coding-2026.html>) and [AI-Assisted Programming Guide](</en/ai/ai-coding.html>).
