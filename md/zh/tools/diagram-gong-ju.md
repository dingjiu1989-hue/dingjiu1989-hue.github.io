---
title: "架构图工具：Draw.io vs Excalidraw vs Mermaid vs Diagrams"
description: "对比四款主流的架构图和流程图工具——Draw.io、Excalidraw、Mermaid和Diagrams，从绘图方式、协作功能和适用场景进行深入分析。"
date: 2026-05-12
board: tools
url: https://dingjiu1989-hue.github.io/zh/tools/diagram-gong-ju.html
---

## 架构图工具的选择

技术文档中的架构图、流程图和时序图是沟通设计思路的重要载体。Draw.io、Excalidraw、Mermaid和Diagrams代表了不同的绘图范式。

## Draw.io

Draw.io（现更名为diagrams.net）是最经典的在线绘图工具。

### 核心特性
- 图形化拖拽绘图
- 丰富的模板库（架构图、流程图、UML、网络拓扑等）
- 支持本地存储（Google Drive、OneDrive、GitHub、本地文件）
- 导出格式多样（PNG、SVG、PDF、HTML）
- VS Code插件支持

### 优劣势

- **优势**：功能最全面，上手简单，与VS Code集成
- **劣势**：界面略显过时，不适合描述复杂架构的细节

### 适用场景

流程图、UML图、网络拓扑图、架构概览图。

## Excalidraw

Excalidraw以手绘风格著称，适合快速绘制概念图。

### 核心特性
- 独特的手绘风格
- 实时协作
- 丰富的图形库（Libraries）
- 端到端加密
- 导出为SVG/PNG

### 优劣势

- **优势**：视觉风格独特美观，协作体验好，氛围轻松
- **劣势**：不适合精确的架构图，功能相对简单

### 适用场景

白板讨论、概念设计、用户流程图、非正式的技术交流。

## Mermaid

Mermaid是基于文本的图表生成工具，使用类似Markdown的语法定义图表。

### 核心特性
- 文本即图表，支持版本控制
- 集成在Markdown中
- 支持流程图、时序图、类图、甘特图、Git图等
- CI/CD可以自动生成图表

### 语法示例

```
graph TD
    A[用户请求] --> B[API网关]
    B --> C{认证}
    C -->|通过| D[业务服务]
    C -->|失败| E[返回401]
    D --> F[数据库]
    F --> G[返回数据]
```

### 优劣势

- **优势**：Git友好，文档即代码，适合集成到文档流程
- **劣势**：复杂图表表达受限，样式定制不够灵活

### 适用场景

技术文档中的图表、自动生成的架构图、README中的流程图。

## Diagrams

Diagrams（前称Diagrams as Code）是Python库，用代码定义云架构图。

### 核心特性
- 用Python代码定义架构图
- 支持AWS、Azure、GCP、K8s等云资源图标
- 自动布局
- CI/CD友好

### 示例

```python
from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS

with Diagram("Web Service", show=False):
    EC2("Web") >> RDS("Database")
```

### 优劣势

- **优势**：代码版本管理，云资源图标丰富，适合基础设施即代码团队
- **劣势**：灵活性有限，不支持手绘风格

### 适用场景

云架构图、基础设施即代码团队的自动化图表生成。

## 对比总结

| 工具 | 操作方式 | 版本控制 | 协作 | 美观度 | 学习曲线 |
|------|---------|---------|------|--------|---------|
| Draw.io | 拖拽 | 文件存储 | 一般 | 中 | 低 |
| Excalidraw | 拖拽 | 文件/云端 | 优秀 | 高 | 极低 |
| Mermaid | 代码 | 原生 | 一般 | 中 | 中 |
| Diagrams | 代码 | 原生 | 一般 | 中 | 中高 |

## 选型建议

- **团队白板讨论** → Excalidraw
- **文档中的图表** → Mermaid
- **云架构图** → Diagrams或Draw.io
- **正式技术文档** → Draw.io

多种工具可以组合使用，在不同场景选择最合适的工具。
