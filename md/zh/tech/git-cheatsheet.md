---
title: "Git 常用命令速查表"
description: "Git 常用命令速查，涵盖分支管理、撤销操作、暂存与提交、远程协作等核心场景，快速查找即用。"
date: 2026-05-08
board: tech
url: https://dingjiu1989-hue.github.io/tech/git-cheatsheet.html
---

# Git 常用命令速查表

日常开发中 Git 是最常用的版本控制工具。这里整理了高频命令，按场景分类，方便速查。

## 分支管理

命令| 说明  
---|---  
`git branch`| 查看本地分支  
`git branch -r`| 查看远程分支  
`git branch <name>`| 创建新分支  
`git checkout <name>`| 切换分支  
`git checkout -b <name>`| 创建并切换到新分支  
`git merge <branch>`| 合并指定分支到当前分支  
`git branch -d <name>`| 删除本地分支  
`git push origin --delete <name>`| 删除远程分支  
  
## 暂存与提交

命令| 说明  
---|---  
`git status`| 查看工作区状态  
`git add <file>`| 添加文件到暂存区  
`git add .`| 添加所有更改到暂存区  
`git commit -m "msg"`| 提交暂存区内容  
`git commit --amend`| 修改上一次提交  
  
## 撤销操作

命令| 说明  
---|---  
`git restore <file>`| 撤销工作区修改  
`git restore --staged <file>`| 取消暂存  
`git reset --soft HEAD~1`| 撤销上次 commit，保留修改  
`git reset --hard HEAD~1`| 撤销上次 commit，丢弃修改  
`git revert <commit>`| 安全撤销某次提交（生成新 commit）  
  
## 远程协作

命令| 说明  
---|---  
`git remote -v`| 查看远程仓库地址  
`git push`| 推送当前分支到远程  
`git pull`| 拉取远程更新并合并  
`git fetch`| 拉取远程更新但不合并  
`git clone <url>`| 克隆远程仓库  
  
## 日志与历史

命令| 说明  
---|---  
`git log --oneline`| 查看简洁提交历史  
`git log --graph --oneline`| 查看分支图  
`git diff`| 查看未暂存的修改  
`git diff --staged`| 查看已暂存的修改  
  
## 储藏 (Stash)

命令| 说明  
---|---  
`git stash`| 暂存当前修改到储藏栈  
`git stash pop`| 恢复最近一次储藏并删除  
`git stash list`| 查看储藏列表  
`git stash drop`| 删除最近一次储藏  
  
### 📖 相关推荐

  * [Git 进阶：交互式 rebase、cherry-pick 和 bisect 实战](<https://dingjiu1989-hue.github.io/tech/git-advanced.html>)
  * [Linux 命令行入门：30 个最常用的命令](<https://dingjiu1989-hue.github.io/tech/linux-commands.html>)
  * [单元测试入门：从零到写出第一个可维护的测试](<https://dingjiu1989-hue.github.io/tech/unit-testing-guide.html>)



**See also:** [VS Code 十大必备插件：让编码效率翻倍](</tech/vscode-extensions.html>), [10 款开发者必备的命令行工具（2026 版）](</tools/cli-tools-collection.html>), [Git 进阶：交互式 rebase、cherry-pick 和 bisect 实战](</tech/git-advanced.html>).
