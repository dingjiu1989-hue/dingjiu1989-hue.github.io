---
title: "高级Prompt Engineering技巧"
description: "深入探讨高级提示工程方法，包括思维链、Few-Shot学习、结构化输出等关键技术，助你充分发挥大语言模型的能力。"
date: 2026-05-11
board: zh/ai
url: https://dingjiu1989-hue.github.io/zh/ai/prompt-engineering-advanced.html
---

## 从基础到进阶

Prompt Engineering已从简单的"请用中文回答"进化为一门系统化的工程学科。掌握高级技巧能够显著提升LLM输出的质量和可靠性。

## 思维链（Chain-of-Thought）

思维链提示是让模型展示推理过程的核心技术。与其直接问答案，不如引导模型逐步思考。Few-Shot CoT通过在示例中展示推理步骤来引导模型。Zero-Shot CoT则更简洁——只需在提示末尾加上"让我们逐步思考"即可触发推理链。

进阶用法包括自洽性（Self-Consistency）：多次运行CoT并投票选择最一致的答案，可显著提高数学和逻辑推理任务的准确率。

## 结构化输出控制

控制LLM输出格式是生产环境的关键需求。XML标签法是最直观的方式，在提示中定义`<output><answer></answer><reasoning></reasoning></output>`结构。JSON模式配合System Message中的格式说明，能让模型稳定输出可解析的结构化数据。

更可靠的做法是使用函数调用（Function Calling）功能。通过定义函数的参数Schema，模型会自动输出符合规范的JSON，无需在Prompt中反复强调格式。

## 系统提示词设计

高质量的System Prompt应当包含以下要素：角色定义（你是谁）、任务说明（你要做什么）、输出规范（格式要求）、约束条件（不能做什么）以及上下文信息（当前环境数据）。

## 高级技巧实战

**分而治之**：复杂任务拆分为多个子Prompt，每个Prompt聚焦单一职责。例如代码审查任务可拆分为"检查安全漏洞""检查性能问题""检查代码风格"三个独立步骤。

**动态Few-Shot**：根据用户输入从样本库中检索最相似的示例，而非使用固定示例。利用向量相似度搜索，每次动态选择3-5个最相关示例，效果远超随机选择。

**对抗性Prompt测试**：主动测试Prompt的鲁棒性，包括角色扮演攻击、越狱尝试和边界条件测试，确保生产环境的提示词安全可靠。

掌握这些技巧后，你将能够构建更可靠、更高效的LLM应用系统。
