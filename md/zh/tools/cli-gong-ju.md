---
title: "命令行效率工具：bat、htop、duf、ncdu等现代化替代品"
description: "介绍一系列现代化命令行工具的替代方案，用bat替代cat、htop替代top、duf替代df、ncdu替代du等，提升终端操作体验和效率。"
date: 2026-05-12
board: tools
url: https://dingjiu1989-hue.github.io/zh/tools/cli-gong-ju.html
---

## 为什么使用现代化替代

经典的Unix命令行工具功能强大，但界面和交互方式相对原始。近年来涌现出一批现代化替代品，它们在保持兼容性的同时，提供了更友好的界面和更丰富的功能。

## bat：cat的现代化替代

bat是带有语法高亮和行号的cat增强版。

### 核心特性
- 自动语法高亮（支持数百种语言）
- 行号显示
- Git变更标记
- 非打印字符显示
- 支持分页器

```bash
# 基本使用
bat file.py

# 显示非打印字符
bat -A file.txt

# 与管道结合使用
bat file.json | jq .
```

### 配置建议

```bash
# 别名设置
alias cat='bat'

# 设置主题
export BAT_THEME='Dracula'
```

## htop：top的现代替代

htop提供更直观的进程管理和系统监控界面。

### 核心功能
- 彩色显示，直观易读
- 可滚动进程列表
- 树形视图查看进程关系
- 鼠标支持
- 快捷键操作（F键菜单）

**替代品：** btop（更美观，支持GPU和磁盘监控）

## duf：df的现代替代

duf以表格形式展示磁盘使用情况，比df的输出更加直观。

```bash
# 基本使用
duf

# 只显示本地文件系统
duf --only local

# 按使用率排序
duf --sort usage
```

输出包含：文件系统、类型、大小、已用、可用、使用率和挂载点，一目了然。

## ncdu：du的现代替代

ncdu提供交互式的磁盘空间分析界面。

```bash
# 扫描当前目录
ncdu

# 扫描并导出结果
ncdu -o scan.json /home
ncdu -f scan.json  # 导入查看
```

使用方向键导航，可以快速找出占用空间最大的目录和文件。

## 更多现代化工具

### fd：find的替代
```bash
# 查找文件
fd "pattern"       # 比 find . -name "pattern" 快得多

# 正则搜索
fd '\.py$'

# 排除特定目录
fd "config" --exclude node_modules
```

### sd：sed的替代
```bash
# 更直观的替换语法
sd "old_text" "new_text" file.txt
sd "foo" "bar" **/*.rs  # 递归替换
```

### delta：diff的替代
提供语法高亮和行号的diff输出，与Git深度集成。

```bash
# Git配置
[core]
    pager = delta
[delta]
    navigate = true
```

### procs：ps的替代
```bash
# 更可读的进程信息
procs
procs --tree   # 树形视图
procs docker   # 按关键词过滤
```

## 安装方式

```bash
# macOS
brew install bat htop duf ncdu fd sd delta procs

# Linux
# 各自项目的Release页面下载
```

这些现代化工具可以让终端工作变得更加高效和愉悦，值得逐步替换到日常工具箱中。
