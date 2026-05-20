---
title: "Model Quantization: Making LLMs Smaller and Faster"
description: "Quantize LLMs for efficient deployment: GPTQ, AWQ, bitsandbytes, and GGUF for running models on consumer hardware."
date: 2026-02-20
board: ai
url: https://dingjiu1989-hue.github.io/en/ai/model-quantization.html
---

# Model Quantization: Making LLMs Smaller and Faster

Model quantization reduces the precision of neural network weights, making models smaller and faster with minimal accuracy loss. This enables running large language models on consumer hardware, edge devices, and cost-effective inference servers.

## Quantization Fundamentals

Models are typically trained in FP32 (32-bit floating point) or BF16 (16-bit bfloat). Quantization converts weights to lower precision: INT8 (8-bit), INT4 (4-bit), or even 2-bit. Weight size decreases proportionally—INT4 uses 1/8 the memory of FP32.

Quantization introduces quantization error. The trade-off is between compression ratio and accuracy. Most models retain 95-99% of their accuracy at INT4. Some models handle quantization better than others—larger models tend to quantize better.

## Post-Training Quantization

GPTQ (Generative Pre-Trained Quantizer) uses one-shot weight quantization based on approximate second-order information. It calibrates on a small dataset (128 samples) and produces INT4 weights. GPTQ-quantized models maintain high accuracy while reducing size by 4x.

AWQ (Activation-aware Weight Quantization) protects important weights based on activation magnitudes. It identifies 1% of "salient" weights and keeps them at higher precision. AWQ typically outperforms GPTQ on small models and multilingual tasks.

Bitsandbytes integrates with Hugging Face Transformers for easy quantization. Load any model in 4-bit or 8-bit with load_in_4bit=True. QLoRA uses NF4 (NormalFloat4) format for fine-tuning with 4-bit base models.

## GGUF and llama.cpp

GGUF is the quantization format for llama.cpp, enabling local LLM inference on CPU and consumer GPUs. GGUF supports multiple quantization levels (q2_k to q8_0) with different quality-size trade-offs. Choose Q4_K_M for balanced quality and size.

llama.cpp runs quantized models efficiently on CPU, Apple Silicon, and GPU. It supports metal acceleration on Mac, CUDA on NVIDIA, and Vulkan on AMD. GGUF models are widely available on Hugging Face.

## Quantization-Aware Training

QAT (Quantization-Aware Training) simulates quantization during training, producing models that maintain higher accuracy after quantization. The training process inserts fake quantization operations that model the quantization error.

QAT requires full training infrastructure and access to the original training data. It is more effective than PTQ for very low-bit quantization (2-bit, 3-bit) and for quantizing specific layers that are sensitive to precision loss.

## Deployment Decisions

Use INT4 quantization for memory-constrained environments (consumer GPUs with 8-16GB VRAM, mobile devices). Use INT8 for latency-sensitive serving (faster than FP16 with similar quality). Use FP16/BF16 when accuracy is critical and hardware supports it (A100, H100). Always evaluate accuracy on your specific task before deploying quantized models.

**See also:** [Model Deployment: vLLM, TGI, ONNX, Quantization, GPU Optimization](</en/ai/model-deployment.html>), [AI Model Deployment: Strategies for Production LLM Serving](</en/ai/ai-model-deployment-strategies.html>), [Model Evaluation: Benchmarks, Human Evaluation, LLM-as-Judge, and A/B Testing in Production](</en/ai/model-evaluation-harness.html>).

**See also:** [Model Deployment: vLLM, TGI, ONNX, Quantization, GPU Optimization](</en/ai/model-deployment.html>), [AI Model Deployment: Strategies for Production LLM Serving](</en/ai/ai-model-deployment-strategies.html>), [AI Gateway: API Routing, Rate Limiting, Fallback Models, Cost Management, and Logging](</en/ai/ai-gateway.html>)

**See also:** [Model Deployment: vLLM, TGI, ONNX, Quantization, GPU Optimization](</en/ai/model-deployment.html>), [AI Model Deployment: Strategies for Production LLM Serving](</en/ai/ai-model-deployment-strategies.html>), [AI Gateway: API Routing, Rate Limiting, Fallback Models, Cost Management, and Logging](</en/ai/ai-gateway.html>)

**See also:** [Model Deployment: vLLM, TGI, ONNX, Quantization, GPU Optimization](</en/ai/model-deployment.html>), [AI Model Deployment: Strategies for Production LLM Serving](</en/ai/ai-model-deployment-strategies.html>), [AI Gateway: API Routing, Rate Limiting, Fallback Models, Cost Management, and Logging](</en/ai/ai-gateway.html>)

**See also:** [Model Deployment: vLLM, TGI, ONNX, Quantization, GPU Optimization](</en/ai/model-deployment.html>), [AI Model Deployment: Strategies for Production LLM Serving](</en/ai/ai-model-deployment-strategies.html>), [AI Gateway: API Routing, Rate Limiting, Fallback Models, Cost Management, and Logging](</en/ai/ai-gateway.html>)

**See also:** [Model Deployment: vLLM, TGI, ONNX, Quantization, GPU Optimization](</en/ai/model-deployment.html>), [AI Model Deployment: Strategies for Production LLM Serving](</en/ai/ai-model-deployment-strategies.html>), [AI Gateway: API Routing, Rate Limiting, Fallback Models, Cost Management, and Logging](</en/ai/ai-gateway.html>)

**See also:** [Prompt Management: Versioning, Testing, Collaboration, Deployment](</en/ai/prompt-management.html>), [AI Safety: Responsible Development and Deployment](</en/ai/ai-safety.html>), [Prompt Engineering Guide for LLMs](</en/ai/prompt-engineering-guide.html>)

**See also:** [Prompt Management: Versioning, Testing, Collaboration, Deployment](</en/ai/prompt-management.html>), [AI Safety: Responsible Development and Deployment](</en/ai/ai-safety.html>), [Prompt Engineering Guide for LLMs](</en/ai/prompt-engineering-guide.html>)

**See also:** [Prompt Management: Versioning, Testing, Collaboration, Deployment](</en/ai/prompt-management.html>), [AI Safety: Responsible Development and Deployment](</en/ai/ai-safety.html>), [Prompt Engineering Guide for LLMs](</en/ai/prompt-engineering-guide.html>)

**See also:** [Prompt Management: Versioning, Testing, Collaboration, Deployment](</en/ai/prompt-management.html>), [AI Safety: Responsible Development and Deployment](</en/ai/ai-safety.html>), [Prompt Engineering Guide for LLMs](</en/ai/prompt-engineering-guide.html>)

**See also:** [Prompt Management: Versioning, Testing, Collaboration, Deployment](</en/ai/prompt-management.html>), [AI Safety: Responsible Development and Deployment](</en/ai/ai-safety.html>), [Prompt Engineering Guide for LLMs](</en/ai/prompt-engineering-guide.html>)

**See also:** [Prompt Management: Versioning, Testing, Collaboration, Deployment](</en/ai/prompt-management.html>), [AI Safety: Responsible Development and Deployment](</en/ai/ai-safety.html>), [Prompt Engineering Guide for LLMs](</en/ai/prompt-engineering-guide.html>)

**See also:** [Prompt Management: Versioning, Testing, Collaboration, Deployment](</en/ai/prompt-management.html>), [AI Safety: Responsible Development and Deployment](</en/ai/ai-safety.html>), [Prompt Engineering Guide for LLMs](</en/ai/prompt-engineering-guide.html>)

**See also:** [Prompt Management: Versioning, Testing, Collaboration, Deployment](</en/ai/prompt-management.html>), [AI Safety: Responsible Development and Deployment](</en/ai/ai-safety.html>), [Prompt Engineering Guide for LLMs](</en/ai/prompt-engineering-guide.html>)

**See also:** [Prompt Management: Versioning, Testing, Collaboration, Deployment](</en/ai/prompt-management.html>), [AI Safety: Responsible Development and Deployment](</en/ai/ai-safety.html>), [Prompt Engineering Guide for LLMs](</en/ai/prompt-engineering-guide.html>)

**See also:** [Prompt Management: Versioning, Testing, Collaboration, Deployment](</en/ai/prompt-management.html>), [AI Safety: Responsible Development and Deployment](</en/ai/ai-safety.html>), [Prompt Engineering Guide for LLMs](</en/ai/prompt-engineering-guide.html>)
