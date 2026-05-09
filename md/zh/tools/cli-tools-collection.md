---
title: "10 款开发者必备的命令行工具（2026 版）"
description: "精选 10 款提升终端效率的命令行工具，涵盖文件管理、JSON 处理、Git 增强、系统监控等场景。"
date: 2026-05-07
board: tools
url: https://dingjiu1989-hue.github.io/tools/cli-tools-collection.html
---

# 10 款开发者必备的命令行工具（2026 版）

终端是开发者的主战场。这些 CLI 工具能让你的命令行效率提升 10 倍。

## 文件与导航

  * **fd** — 比 `find` 快 5 倍的搜索工具，语法直观。例：`fd "test.*py" src/`
  * **ripgrep (rg)** — 比 `grep` 快 10 倍的文本搜索。例：`rg "TODO" --type py`
  * **fzf** — 模糊搜索交互工具。Ctrl+T 模糊搜文件，Ctrl+R 模糊搜历史命令，安装即生效。
  * **zoxide** — 智能 `cd` 替代。不记全路径，只记文件夹名，自动跳转到你最常去的目录。例：`z proj`



## 文件内容查看

  * **bat** — `cat` 替代品，语法高亮、行号、分页。例：`bat main.py`
  * **jq** — JSON 处理的瑞士军刀。提取、筛选、转换 JSON 数据：`curl api.com | jq '.items[] | {name, price}'`
  * **fx** — 交互式 JSON 查看器，支持鼠标点击折叠/展开，比 `jq` 更直观。



## Git 增强

  * **lazygit** — Git 的终端 GUI。在终端内用键盘快捷键完成 commit、push、merge、rebase 等所有操作，不用记命令。
  * **delta** — 增强 `git diff` 显示效果，语法高亮、行号、侧边对比。



## 系统监控

  * **btm (bottom)** — Rust 写的系统资源监控，比 `top` 和 `htop` 更现代的 UI，CPU/内存/磁盘/网络/温度一屏显示。



## 一行安装（macOS）
    
    
    brew install fd ripgrep fzf zoxide bat jq lazygit git-delta bottom

## 组合使用的威力
    
    
    # 在所有 Python 文件中搜索 "user"，模糊筛选后用 bat 查看
    rg -l "user" --type py | fzf --preview "bat --color=always {}"

把这些工具加到你的工作流里，两周后你会奇怪之前没有它们是怎么活下来的。

### 📖 相关推荐

  * [2026 年 10 款必装终端工具：让你的命令行效率翻倍](<https://dingjiu1989-hue.github.io/tools/terminal-tools-2026.html>)
  * [2026 年最佳屏幕录制和视频剪辑工具推荐](<https://dingjiu1989-hue.github.io/tools/screen-recording-tools.html>)
  * [10 个你每天都会用到的免费在线工具网站](<https://dingjiu1989-hue.github.io/tools/online-tools-2026.html>)



**See also:** [Git 常用命令速查表](</tech/git-cheatsheet.html>), [VS Code 十大必备插件：让编码效率翻倍](</tech/vscode-extensions.html>), [Git 进阶：交互式 rebase、cherry-pick 和 bisect 实战](</tech/git-advanced.html>).
