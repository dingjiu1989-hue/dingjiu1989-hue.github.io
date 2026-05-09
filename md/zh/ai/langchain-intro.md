---
title: "LangChain 入门：构建你的第一个 AI 应用"
description: "深入浅出讲解 LangChain 核心概念（Chain、Agent、Tool、Memory），用可运行的 RAG 问答代码示例带你写出第一个 LLM 应用。"
date: 2026-05-01
board: ai
url: https://dingjiu1989-hue.github.io/ai/langchain-intro.html
---

# LangChain 入门：构建你的第一个 AI 应用

LangChain 是当前 AI 应用开发领域最热门的框架之一。但坦白说，很多人用了 LangChain 只是因为它"大家都在用"，实际项目中可能一条 OpenAI SDK 调用就能解决问题。本文不讲空洞的概念，而是给出一个清晰的判断标准：什么时候该用 LangChain，什么时候不该用，以及如何用 LangChain 快速搭建一个真正有用的 RAG 问答应用。

## LangChain 解决了什么问题？

LangChain 的核心理念是"LLM 应用开发的通用框架"。它把与大模型交互中大量重复的工作——提示词模板、输出解析、多步调用、外部工具集成——抽象成可复用的组件。具体来说，LangChain 提供了以下能力：

  * **统一接口：** 无论你用的是 OpenAI、Claude、Llama 还是本地 Ollama，LangChain 提供一套统一的调用接口，切换模型只需改一行配置。
  * **链式调用（Chain）：** 将多个 LLM 调用串联起来，前一个调用的输出作为后一个的输入，组合成复杂的工作流。
  * **智能体（Agent）：** 让 LLM 自主决定调用哪些工具（搜索引擎、计算器、数据库），实现更复杂的推理-行动循环。
  * **记忆（Memory）：** 维护对话历史，让多轮对话有上下文连贯性。



## 核心概念快速理解

LangChain 的五个核心组件你需要了解：

  * **LLM / ChatModel：** 对底层模型 API 的封装。示例：`ChatOpenAI(model="gpt-4")` 或 `ChatOllama(model="llama3.1")`，两者接口一致。
  * **Prompt Template：** 提示词模板。把用户输入动态填入固定的提示词结构，避免每次手写完整提示词。
  * **Chain：** 将 LLM + Prompt + 输出解析器组合成一个可执行的单元。最常用的是 `LLMChain`。
  * **Tool：** 一个函数或 API 的包装，Agent 可以调用它来获取外部信息或执行操作。比如搜索、计算、数据库查询。
  * **Agent：** 一个"大脑"，它接收自然语言指令，决定用哪些 Tools 来完成任务，并解析工具返回的结果继续推理。



## 实战：RAG 问答应用

我们做一个实际的 RAG（检索增强生成）应用，让用户上传一份 PDF，然后对 PDF 内容提问。完整代码不到 60 行：
    
    
    from langchain_community.document_loaders import PyPDFLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import Chroma
    from langchain_openai import OpenAIEmbeddings, ChatOpenAI
    from langchain.chains import RetrievalQA
    from langchain.prompts import PromptTemplate
    
    # 1. 加载 PDF 文档
    loader = PyPDFLoader("report.pdf")
    documents = loader.load()
    
    # 2. 将长文档切分成小段
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50
    )
    chunks = text_splitter.split_documents(documents)
    
    # 3. 向量化并存储
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=OpenAIEmbeddings()
    )
    
    # 4. 构建检索问答链
    prompt_template = """根据以下上下文回答问题。如果你无法从上下文中找到答案，请直接说不知道。
    
    上下文：
    {context}
    
    问题：{question}
    """
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model="gpt-4o-mini"),
        retriever=vectorstore.as_retriever(search_k=3),
        chain_type="stuff",
        return_source_documents=True
    )
    
    # 5. 提问
    result = qa_chain.invoke({
        "query": "报告中提到的核心指标是什么？"
    })
    print(result["result"])

这个例子展示了 LangChain 的核心价值：5 个步骤对应 5 个概念（Document Loaders、Text Splitters、Vector Stores、RetrievalQA Chain、Prompt Templates），每个步骤都可以独立替换或定制。比如把 Chroma 换为 Pinecone，把 OpenAI 换为本地 Ollama，只需改一两行代码。

## 从 LangChain 到 LangGraph

需要说明的是：LangChain 团队在 2025 年已经将重心从传统的 Chain/Agent 转向了 **LangGraph** 。LangGraph 把应用定义为一个有向图（Graph），节点是 LLM 调用或工具执行，边是状态流转。相比 Chain 的线性执行，Graph 支持循环、分支和并行，更适合复杂的 Agent 应用。

对于简单场景（如本文的 RAG 示例），传统 LangChain 依然完全够用。但如果你在构建自主 Agent 或多步骤决策流程，建议直接学习 LangGraph。

## 什么时候不该用 LangChain

技术选型最重要的是知道什么时候说不。以下场景建议放弃 LangChain：

  * **只是调 API：** 如果你只需要一个简单的 Chat Completion 调用，`openai.ChatCompletion.create()` 一行代码就够了，LangChain 反而增加了依赖和抽象复杂度。
  * **纯 RAG 无需复杂链：** 用 LlamaIndex 更轻量、更容易 Debug，文档质量和检索体验也更好。
  * **生产环境要求高可控：** LangChain 的抽象层在你需要精细控制 prompt 和输出格式时可能会成为负担。很多生产团队最终把 LangChain 换成了手写 Pipeline。



一句话总结：LangChain 最适合快速原型验证和中等复杂度的 LLM 应用。它降低了组合 LLM + 外部数据的门槛，但当你需要精细控制或追求极致性能时，不妨考虑更轻量的替代方案。

### 📖 相关推荐

  * [MCP 协议入门：让 AI 模型安全访问你的工具和数据](<https://dingjiu1989-hue.github.io/ai/mcp-protocol-guide.html>)
  * [AI 编程助手对比 2026：Cursor vs Copilot vs Claude Code 怎么选](<https://dingjiu1989-hue.github.io/ai/ai-coding-tools-comparison-2026.html>)
  * [AI 绘画变现指南：从出图到接单的完整路径](<https://dingjiu1989-hue.github.io/ai/ai-art-monetization.html>)



**See also:** [AI Agent 开发入门 2026：从原理到第一个智能体](</ai/ai-agent-development-2026.html>), [零代码搭建 AI 聊天机器人：客服、知识库、个人助手](</ai/no-code-ai-chatbot.html>), [AI 编程助手对比 2026：Cursor vs Copilot vs Claude Code 怎么选](</ai/ai-coding-tools-comparison-2026.html>).
