---
title: "模型部署方案：vLLM vs TGI vs Ollama，推理优化技巧"
description: "深入对比vLLM、TGI和Ollama三大模型部署框架，涵盖推理优化技术、吞吐量提升、延迟优化和成本控制等生产级部署实践经验。"
date: 2026-05-12
board: ai
url: https://dingjiu1989-hue.github.io/zh/ai/model-bushu.html
---

## 模型部署挑战

将LLM部署到生产环境面临三大挑战：推理延迟、吞吐量和成本。不同的部署框架以不同方式解决这些问题。

## vLLM

vLLM是目前最流行的开源LLM推理引擎，由加州大学伯克利分校开发。

**核心技术：**
1. **PagedAttention**：类操作系统的分页内存管理，KV Cache利用率提升至95%以上
2. **连续批处理**：动态将请求组合为batch，大幅提升吞吐量
3. **量化支持**：AWQ、GPTQ、FP8等多种量化格式
4. **前缀缓存**：共享前缀的请求复用KV Cache

**优势：** 吞吐量业界领先，API兼容OpenAI格式。
**劣势：** 对HuggingFace模型格式支持最为完善，其他格式支持有限。

## TGI（Text Generation Inference）

TGI由HuggingFace开发，与HuggingFace生态深度集成。

**核心技术：**
1. **张量并行**：跨多GPU的分片推理
2. **Flash Attention**：优化的注意力计算内核
3. **Speculative Decoding**：投机解码加速生成
4. **水印生成**：内置AI文本水印功能

**优势：** 与HuggingFace模型和生态无缝集成，支持模型热加载。
**劣势：** 自定义扩展性不如vLLM灵活。

## Ollama

Ollama专注于本地部署和开发者体验。

**核心技术：**
1. **一键部署**：极简的模型管理和启动流程
2. **Modelfile**：类似Dockerfile的模型配置方式
3. **多平台支持**：macOS、Linux、Windows全覆盖
4. **GPU加速**：自动检测并使用GPU

**优势：** 安装和使用最简单，适合个人开发环境。
**劣势：** 生产级功能不足，不适合高并发场景。

## 推理优化技巧

### KV Cache优化
- 使用PagedAttention减少显存碎片
- 启用前缀缓存减少重复计算

### 量化策略
- INT8量化：无损或接近无损，推理速度提升2倍
- INT4量化：可接受的质量损失，推理速度提升3-4倍
- FP8量化：Hopper架构GPU支持，质量和速度的平衡

### 批处理策略
- 使用连续批处理提高GPU利用率
- 根据延迟SLA动态调整批处理大小
- 长请求和短请求混合批处理

### 部署架构建议
- **单机单卡**：7B以下模型，使用Ollama或vLLM
- **单机多卡**：13B-70B模型，vLLM + 张量并行
- **多机多卡**：70B+模型，vLLM + 流水线并行

选择合适的部署框架需要综合考虑模型大小、并发需求、延迟要求和运维能力。
