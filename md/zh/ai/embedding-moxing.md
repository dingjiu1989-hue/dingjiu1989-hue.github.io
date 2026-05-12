---
title: "Embedding模型对比：text-embedding-3 vs BGE vs E5"
description: "全面对比主流文本Embedding模型，包括OpenAI text-embedding-3系列、BGE系列和E5系列，覆盖性能、价格、中文支持和选型建议。"
date: 2026-05-12
board: ai
url: https://dingjiu1989-hue.github.io/zh/ai/embedding-moxing.html
---

## Embedding模型的重要性

文本Embedding模型将自然语言转换为向量表示，是RAG系统、语义搜索和文本分类的基础。选择合适的Embedding模型直接影响下游任务的性能。

## OpenAI text-embedding-3系列

OpenAI目前提供两个版本的Embedding模型：

**text-embedding-3-small：**
- 维度：1536（可通过dimensions参数降低）
- 价格：$0.02/1M tokens
- MTEB基准：62.3
- 特点：性价比极高，适合大多数场景

**text-embedding-3-large：**
- 维度：3072（可通过dimensions参数降低）
- 价格：$0.13/1M tokens
- MTEB基准：64.6
- 特点：效果最佳，适合对精度要求极高的场景

## BGE系列

北京人工智能研究院（BAAI）开发的BGE系列在中文场景表现优异。

**BGE-large-zh-v1.5：**
- 维度：1024
- 特点：中文效果出色，开源可私有部署
- 适用场景：中文文档检索、中文RAG系统

**BGE-M3：**
- 特点：多语言、多粒度（词/句/段）、多功能（稠密/稀疏向量）
- 适用场景：多语言混合内容、需要混合检索的场景

BGE模型的优势在于可以完全本地部署，没有API调用成本和数据隐私风险。

## E5系列

微软开发的E5系列采用对比学习训练。

**E5-mistral-7b-instruct：**
- 维度：4096
- 特点：基于Mistral-7B训练，效果在MTEB上排名靠前
- 局限：需要使用指令前缀，推理资源要求高

**multilingual-e5-large：**
- 维度：1024
- 特点：支持多语言，包括中文
- 适用场景：多语言搜索和检索

## 效果对比

在中文语义相似度任务上的表现：

| 模型 | 维度 | 中文效果 | 推理速度 | 部署成本 |
|------|------|----------|----------|----------|
| text-embedding-3-small | 1536 | 良好 | API | 按量付费 |
| text-embedding-3-large | 3072 | 优秀 | API | 较高 |
| BGE-large-zh-v1.5 | 1024 | 优秀 | 快 | 低 |
| BGE-M3 | 1024 | 优秀 | 中 | 中 |
| multilingual-e5-large | 1024 | 良好 | 中 | 中 |

## 选型建议

1. **中文为主，预算充足** → text-embedding-3-large
2. **中文为主，注重成本** → BGE-large-zh-v1.5
3. **需要本地部署** → BGE系列
4. **多语言混合** → BGE-M3或multilingual-e5-large
5. **英文为主，追求极致** → text-embedding-3-large

选择Embedding模型需平衡效果、成本、延迟和隐私需求，没有放之四海而皆准的最优解。
