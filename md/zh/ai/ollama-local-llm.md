---
title: "本地运行大模型：Ollama 完全入门指南"
description: "从安装到实战，手把手教你用 Ollama 在个人电脑上运行 Llama、Mistral、Qwen 等开源大模型，实现隐私安全的本地 AI 助手。"
date: 2026-05-02
board: ai
url: https://dingjiu1989-hue.github.io/ai/ollama-local-llm.html
---

# 本地运行大模型：Ollama 完全入门指南

2025 年，调用 GPT-4 或 Claude API 依然是大多数人的首选，但越来越多开发者和隐私敏感用户开始把目光转向本地大模型。原因很简单：数据不出本机、无需按 Token 付费、可离线使用、完全可控。Ollama 正是这一切的入口——它是目前最简单易用的本地大模型运行工具。

## 什么是 Ollama？为什么选它？

Ollama 是一个开源的本地大模型运行框架，它将模型下载、环境配置、API 服务封装成一个极简的命令行工具。你不需要理解 CUDA、Python 虚拟环境或模型格式转换——装好 Ollama，一条命令就能跑起一个 7B 参数的 Llama 3 模型。

选择本地 LLM 的核心理由有三：**隐私** ——你的对话数据永远不会离开本机，适合处理敏感文档；**成本** ——一次性的硬件投入，没有按 Token 计费的后顾之忧；**离线** ——没有网络也能用，飞机上、偏远地区不受影响。当然，本地模型的能力目前还无法完全媲美 GPT-4，但在代码辅助、文档分析、翻译等场景中已经足够好用。

## 安装 Ollama

Ollama 支持三大操作系统，安装过程都非常简单：

  * **macOS：** 从 [ollama.com](<https://ollama.com>) 下载 DMG 安装包，拖入 Applications 文件夹即可。首次运行会要求授予权限。
  * **Windows：** 下载官方安装程序（.exe），一路下一步。安装完成后 Ollama 会在后台运行，托盘图标可管理。
  * **Linux：** 一行命令 `curl -fsSL https://ollama.com/install.sh | sh`，脚本会自动配置 systemd 服务和 NVIDIA 驱动检测。



安装完成后在终端运行 `ollama --version` 验证是否成功。

## 下载并运行模型

Ollama 的核心操作只有一条命令。以下载并运行 Meta 最新开源的 Llama 3.1 8B 为例：
    
    
    ollama run llama3.1

这条命令会自动下载模型（约 4.7GB 的量化版本），然后进入交互式对话模式。你可以直接打字提问，就像在跟 ChatGPT 聊天一样。

以下是几个推荐入门的模型：

模型 | 参数规模 | 磁盘占用 | 推荐内存 | 特点  
---|---|---|---|---  
**Llama 3.1 8B** | 8B | ~4.7GB | 8GB+ | 通用对话，综合能力均衡  
**Mistral 7B** | 7B | ~4.1GB | 8GB+ | 英文能力强，代码能力出色  
**Qwen2.5 7B** | 7B | ~4.3GB | 8GB+ | 中文能力最强，数学推理好  
**Codestral 22B** | 22B | ~12GB | 16GB+ | 代码专用，Mistral 出品  
  
## Ollama CLI 常用命令

除了 `ollama run`，还有几个命令非常常用：

  * `ollama pull <模型名>` — 仅下载模型不运行，适合提前准备好需要的模型。
  * `ollama list` — 查看本地已下载的所有模型及其大小。
  * `ollama rm <模型名>` — 删除不再需要的模型，释放磁盘空间。
  * `ollama serve` — 启动 Ollama 的 REST API 服务（默认端口 11434），供其他应用调用。
  * `ollama ps` — 查看当前正在运行的模型进程。



Ollama 还内置了 REST API。启动服务后，你可以用 curl 或者其他 HTTP 客户端调用模型：
    
    
    curl http://localhost:11434/api/generate -d '{
      "model": "llama3.1",
      "prompt": "用 Python 写一个快速排序",
      "stream": false
    }'

## 搭配 Open WebUI：获得 ChatGPT 般的体验

命令行虽然够用，但大多数人还是喜欢图形界面。Open WebUI（原 Ollama WebUI）是一个开源的 Web 前端，界面设计向 ChatGPT 致敬，功能却更丰富。

安装方式也极其简单：
    
    
    docker run -d -p 3000:8080 \
      -v open-webui:/app/backend/data \
      --name open-webui \
      ghcr.io/open-webui/open-webui:main

启动后访问 `http://localhost:3000`，注册一个本地账号即可。Open WebUI 自动发现本机的 Ollama 实例，你可以直接在浏览器中切换不同模型、管理对话历史、上传文件做 RAG、甚至设置系统提示词。对于想要把本地模型当成主力助手的人来说，这是必备组件。

## 硬件要求与性能调优

这是最受关注的问题。简单来说：

  * **7B 模型（Q4 量化）：** 最低 8GB 内存即可运行，CPU 模式能用但较慢。M1/M2/M3 Mac 的 8GB 版本足够流畅运行。
  * **13B 模型（Q4 量化）：** 推荐 16GB 内存。Apple Silicon 统一内存架构表现最好。
  * **33B-70B 模型（Q4 量化）：** 需要 32GB-48GB 内存。除非有专用 GPU（24GB+ VRAM），否则 CPU 推理会很慢。



如果你的 Mac 有 16GB 以上统一内存，Ollama + Qwen2.5 7B 的组合可以稳定输出每秒 30-50 个 Token，日常使用完全够用。Windows 用户如果有 NVIDIA 显卡（6GB+ VRAM），开启 CUDA 加速后速度会快很多。

## 实战：本地编码助手

我的日常使用场景是 Ollama + Continue（VS Code 插件）。Continue 是一款开源的 AI 编码插件，支持接入本地 Ollama 模型。配置完成后，在 VS Code 中选中代码按 Cmd+I 就能让本地模型帮你解释、重构或生成代码。数据全程不离开电脑，公司敏感项目也能放心使用。

本地大模型的时代已经到来。Ollama 极大地降低了门槛，让每个人都能在自己的电脑上拥有一个私有 AI。试试看吧——从 `ollama run llama3.1` 开始。

### 📖 相关推荐

  * [AI 编程助手对比 2026：Cursor vs Copilot vs Claude Code 怎么选](<https://dingjiu1989-hue.github.io/ai/ai-coding-tools-comparison-2026.html>)
  * [MCP 协议入门：让 AI 模型安全访问你的工具和数据](<https://dingjiu1989-hue.github.io/ai/mcp-protocol-guide.html>)
  * [AI 绘画变现指南：从出图到接单的完整路径](<https://dingjiu1989-hue.github.io/ai/ai-art-monetization.html>)
