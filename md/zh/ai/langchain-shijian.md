---
title: "LangChain实战：Chain、Agent、Memory、Tool使用详解"
description: "深入讲解LangChain框架的核心组件——Chain、Agent、Memory和Tool的实战用法，结合代码示例展示如何构建复杂的LLM应用工作流。"
date: 2026-05-12
board: ai
url: https://dingjiu1989-hue.github.io/zh/ai/langchain-shijian.html
---

## LangChain框架概览

LangChain是构建LLM应用最流行的框架之一，以模块化设计著称。其核心抽象包括Chain、Agent、Memory、Tool和Callback，理解这些组件的协作方式是掌握LangChain的关键。

## Chain：任务执行的基本单元

Chain是LangChain中最基础的执行单元，代表一个完整的任务处理流程。

### 常见Chain类型

**LLMChain：** 最简单的Chain，组合Prompt模板和LLM调用。

```python
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    template="请用{language}写一首关于{topic}的诗",
    input_variables=["language", "topic"]
)
chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run(language="中文", topic="人工智能")
```

**SequentialChain：** 串联多个Chain，前一个的输出作为后一个的输入。

**RouterChain：** 根据输入内容动态选择执行哪个子Chain，适合多意图处理场景。

## Memory：对话记忆管理

Memory组件用于在多轮对话中维护上下文信息。

### 内置Memory类型

- **ConversationBufferMemory**：完整记录所有历史消息
- **ConversationSummaryMemory**：对历史进行摘要压缩，节省Token
- **ConversationBufferWindowMemory**：只保留最近K轮对话
- **VectorStoreRetrieverMemory**：基于向量检索的长时记忆

选择合适的Memory类型需要权衡记忆完整性和Token消耗。对于长对话，推荐使用摘要记忆或窗口记忆。

## Agent：自主决策的核心

Agent是LangChain中最强大的组件，它能够根据任务目标自主决定调用哪些Tool以及以什么顺序调用。

### Agent类型
- **OpenAI Tools Agent**：使用OpenAI的function calling能力
- **ReAct Agent**：基于Think-Act-Observe循环的推理模式
- **Plan-and-Execute Agent**：先制定计划，再逐步执行

Agent的执行涉及观察环境、推理决策、执行动作和更新记忆的循环过程。

## Tool：Agent的能力扩展

Tool是Agent与外部世界交互的接口。LangChain内置了丰富的Tool集：

- **计算器**：执行数学运算
- **搜索引擎**：获取实时信息
- **数据库查询**：访问结构化数据
- **文件操作**：读写和处理文件
- **API集成**：调用第三方服务

自定义Tool只需继承BaseTool并实现_run方法即可。

## Callback：全流程监控

Callback机制允许开发者监听Chain和Agent执行的各个阶段，用于日志记录、性能监控和调试。

```python
class MyCallbackHandler(BaseCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kwargs):
        print(f"LLM开始处理: {prompts}")
    def on_llm_end(self, response, **kwargs):
        print(f"LLM处理完成: {response}")
```

LangChain的组件化设计让开发者可以灵活组合这些核心抽象，快速构建从简单到复杂的LLM应用。
