---
title: "OpenAI API 入门：用 10 行代码调用 GPT"
description: "零基础入门 OpenAI API，从获取 Key 到发出第一个请求，涵盖 Chat Completion、System Prompt、Temperature 等核心概念，附带可运行的 Python 和 JS 示例。"
date: 2026-05-07
board: ai
url: https://dingjiu1989-hue.github.io/ai/openai-api-intro.html
---

# OpenAI API 入门：用 10 行代码调用 GPT

调用 GPT API 比你想的简单得多——10 行代码就能让 AI 替你写文案、分析数据、回答问题。这篇文章带你从零到发出第一个 API 请求。 第一步：获取 API Key

  1. 打开 [platform.openai.com](<https://platform.openai.com>) 注册/登录
  2. 点击右上角头像 → "View API keys"
  3. "Create new secret key" → 复制保存（只显示一次！）
  4. 设置用量限制（建议先设 $10/月，防止意外超支）

**API 是按量付费的，不是订阅制。** 你可以只充值 $5 开始试用。GPT-4o mini 的价格大约是 $0.15/1M input tokens —— 处理 100 万字的输入只要一毛多。$5 够你做大量实验。 第二步：安装 SDK
    
    
    pip install openai

第三步：第一个请求
    
    
    from openai import OpenAI
    
    client = OpenAI(api_key="sk-your-key-here")
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "你是一个简洁的编程助手，回复不超过三句话。"},
            {"role": "user", "content": "Python 中 list 和 tuple 的区别是什么？"}
        ]
    )
    
    print(response.choices[0].message.content)

跑一下——AI 用三句话回答了你的问题。 核心概念拆解 概念| 是什么| 怎么用  
---|---|---  
**Model**|  用哪个模型| gpt-4o（最强）、gpt-4o-mini（便宜快速、日常够用）、o1（深度推理）  
**Messages**|  对话历史| 三中角色：system（设定 AI 行为）、user（你的问题）、assistant（AI 之前的回答）  
**System Prompt**|  给 AI 的"人设"| 最重要的部分。好的 System Prompt 能让 GPT-4o mini 的效果超过乱用的 GPT-4o  
**Temperature**|  控制随机性（0-2）| 0 = 每次回答一样（适合代码/事实）、1 = 有创造性（适合写作）、1.5+ = 天马行空  
**max_tokens**|  限制输出长度| 1 token ≈ 0.75 个英文单词 ≈ 0.5 个中文字。设太低回答会被截断  
实用示例：多轮对话
    
    
    messages = [
        {"role": "system", "content": "你是一个 Python 编程导师，用 50 字以内回答。"}
    ]
    
    while True:
        user_input = input("你: ")
        if user_input == "quit":
            break
        messages.append({"role": "user", "content": user_input})
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        reply = response.choices[0].message.content
        print(f"AI: {reply}")
        messages.append({"role": "assistant", "content": reply})

实用示例：用 GPT 做数据分析
    
    
    # 读取 CSV，让 GPT 写分析代码
    import csv
    
    data = []
    with open("sales.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    
    data_str = str(data[:5])  # 只传前 5 行作为样本
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "你是数据分析师。根据提供的数据样本，写出完整的 Python pandas 分析代码。"},
            {"role": "user", "content": f"分析这个销售数据的前5行，写代码计算每月的销售总额和增长率：{data_str}"}
        ]
    )
    print(response.choices[0].message.content)
    # GPT 会生成可以直接复制运行的 pandas 分析代码

费用控制

  * **设 hard limit** — 在 OpenAI Platform → Billing → Usage limits 设每月上限
  * **用 gpt-4o-mini** — 95% 的场景够用，价格是 GPT-4o 的 1/20
  * **缓存常见回复** — 同样的 prompt 不要反复调用，存起来复用
  * **监控用量** — Usage 页面可以实时看到花了多少钱

下一步 读完这篇文章你应该能跑起第一个 API 调用了。接下来可以：用 `stream=True` 实现打字机效果、用 Function Calling 让 GPT 调用你的函数、用 Assistants API 构建带知识库的 AI 助手。OpenAI 的官方文档写得很好——把它当参考书，需要时查。 📖 相关推荐

  * [AI 编程助手对比 2026：Cursor vs Copilot vs Claude Code 怎么选](<https://dingjiu1989-hue.github.io/ai/ai-coding-tools-comparison-2026.html>)
  * [MCP 协议入门：让 AI 模型安全访问你的工具和数据](<https://dingjiu1989-hue.github.io/ai/mcp-protocol-guide.html>)
  * [AI 绘画变现指南：从出图到接单的完整路径](<https://dingjiu1989-hue.github.io/ai/ai-art-monetization.html>)

**See also:** [Python 入门教程：从零到写出第一个程序](</tech/python-tutorial.html>), [30 个免费又好用的 API 合集：开发者必备](</tools/free-api-collection.html>), [REST API 设计最佳实践：写出让人愿意用的接口](</tech/rest-api-best-practices.html>).
