---
title: "MCP 协议入门：让 AI 模型安全访问你的工具和数据"
description: "Model Context Protocol (MCP) 是 Anthropic 推出的开放协议，让 AI 助手通过标准化接口连接外部工具和数据源。本文从零讲解 MCP 的核心概念、服务端开发、客户端集成。"
date: 2026-05-09
board: ai
url: https://dingjiu1989-hue.github.io/ai/mcp-protocol-guide.html
---

# MCP 协议入门：让 AI 模型安全访问你的工具和数据

如果你用过 Claude Code 或者 Cursor，你可能注意到这些工具能**直接读取你的文件系统、执行终端命令、查询数据库** 。这背后是一套标准化的协议在起作用——这就是 **MCP（Model Context Protocol，模型上下文协议）** 。 MCP 由 Anthropic 在 2024 年底推出，2025-2026 年迅速成为 AI 工具生态的主流标准。它的核心思想很简单：**让 AI 模型通过统一的接口，安全地访问外部工具和数据源** ，就像 USB-C 接口统一了硬件连接一样。 为什么需要 MCP？ 在 MCP 出现之前，每个 AI 应用都要自己实现工具调用（Function Calling）。如果你想接 GitHub API，写一套；接数据库，又写一套；接文件系统，再写一套。这带来三个问题：

  * **重复造轮子** ：每个应用都要实现自己的工具集成层
  * **安全风险** ：各做各的权限控制，容易出漏洞
  * **生态割裂** ：为 Claude 写的工具不能在 Cursor 里用

MCP 解决了这三个问题。它定义了一套**客户端-服务器** 架构：

  * **MCP Server** ：暴露工具和数据的服务端。比如一个 GitHub Server 提供"列出仓库""创建 Issue"等工具
  * **MCP Client** ：AI 应用（Claude Desktop、Cursor、VS Code 插件等）作为客户端，发现并调用 Server 提供的工具
  * **MCP 协议** ：客户端和服务器之间通过 JSON-RPC 2.0 通信

MCP 的核心概念 MCP 定义了三种核心原语（Primitives）： 1\. Tools（工具） 让 AI 模型执行具体操作。比如：搜索网页、发送邮件、创建文件、查询数据库。每个 Tool 有名称、描述和参数 Schema（JSON Schema 格式）。AI 模型通过 Function Calling 选择调用哪个 Tool。 2\. Resources（资源） 暴露数据给 AI 模型读取。比如：文件内容、数据库记录、API 响应。Resources 是只读的，模型可以读取但不能修改——这比直接给文件系统权限安全得多。 3\. Prompts（提示模板） 预定义的提示词模板。Server 可以提供特定领域的 Prompt 模板，Client 可以直接使用。比如一个 SQL Server 可以提供"分析这张表的结构"的 Prompt 模板。 动手：构建一个 MCP Server 以 Python 为例，用官方 SDK 创建一个天气查询 Server：
    
    
    # weather_server.py
    from mcp.server import Server, NotificationOptions
    from mcp.server.models import InitializationCapabilities
    import mcp.server.stdio
    import mcp.types as types
    import httpx
    
    server = Server("weather-server")
    
    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name="get_weather",
                description="查询指定城市的当前天气",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "城市名称，如 Beijing"
                        }
                    },
                    "required": ["city"]
                }
            )
        ]
    
    @server.call_tool()
    async def handle_call_tool(
        name: str,
        arguments: dict
    ) -> list[types.TextContent]:
        if name == "get_weather":
            city = arguments["city"]
            # 调用真实天气 API
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"https://api.weather.com/v1/{city}"
                )
                data = resp.json()
            return [types.TextContent(
                type="text",
                text=f"{city} 当前温度 {data['temp']}°C，{data['desc']}"
            )]
        raise ValueError(f"Unknown tool: {name}")
    
    async def main():
        async with mcp.server.stdio.stdio_server() as streams:
            await server.run(
                streams[0], streams[1],
                InitializationCapabilities(
                    sampling={},
                ),
            )
    
    if __name__ == "__main__":
        import asyncio
        asyncio.run(main())

在 Claude Desktop 中配置 MCP Server 创建好 Server 后，在 Claude Desktop 的配置文件中注册即可：
    
    
    // ~/Library/Application Support/Claude/claude_desktop_config.json
    {
      "mcpServers": {
        "weather": {
          "command": "python3",
          "args": ["/path/to/weather_server.py"]
        },
        "filesystem": {
          "command": "npx",
          "args": [
            "-y",
            "@anthropic/mcp-server-filesystem",
            "/Users/me/Documents"
          ]
        }
      }
    }

配置完成后，重启 Claude Desktop，在对话中直接说"帮我查一下北京的天气"，Claude 就会自动调用你的 MCP Server。 主流的 MCP Server 推荐 社区已经有大量现成的 MCP Server，你不需要从零写： Server| 功能| 安装命令  
---|---|---  
Filesystem| 安全的文件系统访问| `npx @anthropic/mcp-server-filesystem`  
GitHub| 仓库管理、Issue、PR| `npx @anthropic/mcp-server-github`  
Postgres| 数据库查询与 Schema 探索| `npx @anthropic/mcp-server-postgres`  
Brave Search| 网页搜索能力| `npx @anthropic/mcp-server-brave-search`  
Puppeteer| 浏览器自动化（截图、爬取）| `npx @anthropic/mcp-server-puppeteer`  
Slack| 消息发送与频道管理| `npx @anthropic/mcp-server-slack`  
MCP 的安全模型 MCP 的设计非常重视安全性：

  * **用户同意原则** ：AI 调用工具前需要用户确认（可以在设置中调整）
  * **最小权限** ：每个 MCP Server 只暴露必要的工具，不是全部系统权限
  * **沙箱隔离** ：Server 运行在独立的进程中，单个 Server 崩溃不影响其他
  * **传输安全** ：支持 stdio（本地进程通信）和 HTTP+SSE（远程通信），远程通信建议走 HTTPS

MCP vs 传统 Function Calling 特性| MCP| 传统 Function Calling  
---|---|---  
标准化| 开放协议，跨模型、跨应用| 各家 API 格式不同  
复用性| 写一次，到处用| 每个应用单独集成  
发现机制| Client 自动发现 Server 的工具列表| 开发者硬编码函数定义  
安全模型| 内置用户确认 + 沙箱| 依赖应用自行实现  
生态| 社区贡献 500+ Server，覆盖主流服务| 各自为战  
适用场景 MCP 已经在这几个场景中证明了价值：

  * **AI 编程助手** ：Claude Code 通过 MCP Server 访问文件系统、Git、包管理器，实现完整开发流程
  * **数据分析** ：AI 通过 MCP 连接数据库，直接写 SQL 查询并返回分析结果
  * **企业内部工具** ：将 Jira、Confluence、Slack 封装为 MCP Server，AI 助手统一接入
  * **个人自动化** ：通过 MCP 让 AI 管理日历、邮件、待办事项

总结 MCP 正在成为 AI 工具生态的"USB-C 接口"。它的价值不在于技术有多复杂，而在于**标准化带来的生态效应** ——一个人写的 MCP Server，所有人都能用。如果你在做 AI 应用开发，MCP 是 2026 年必须了解的基础设施。 下一步建议：安装 Claude Desktop 或支持 MCP 的客户端，从官方 Filesystem Server 开始体验，然后再尝试接入 GitHub 或数据库 Server。 📖 相关推荐

  * [LangChain 入门：构建你的第一个 AI 应用](<https://dingjiu1989-hue.github.io/ai/langchain-intro.html>)
  * [AI 编程助手对比 2026：Cursor vs Copilot vs Claude Code 怎么选](<https://dingjiu1989-hue.github.io/ai/ai-coding-tools-comparison-2026.html>)
  * [AI 绘画变现指南：从出图到接单的完整路径](<https://dingjiu1989-hue.github.io/ai/ai-art-monetization.html>)

**See also:** [AI 编程助手对比 2026：Cursor vs Copilot vs Claude Code 怎么选](</ai/ai-coding-tools-comparison-2026.html>), [AI Agent 开发入门 2026：从原理到第一个智能体](</ai/ai-agent-development-2026.html>), [AI 绘画变现指南：从出图到接单的完整路径](</ai/ai-art-monetization.html>).
