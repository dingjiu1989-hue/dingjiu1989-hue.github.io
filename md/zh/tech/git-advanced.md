---
title: "Git 进阶：交互式 rebase、cherry-pick 和 bisect 实战"
description: "进阶 Git 技巧三件套：用交互式 rebase 整理提交历史、用 cherry-pick 精确移植代码、用 bisect 二分法定位 Bug，让你的 Git 段位从熟练进化到精通。"
date: 2026-05-07
board: tech
url: https://dingjiu1989-hue.github.io/zh/tech/git-advanced.html
---

# Git 进阶：交互式 rebase、cherry-pick 和 bisect 实战

如果你已经会 add/commit/push/pull，是时候学这三个进阶命令了。它们不会让你每天多用 Git，但在关键时刻能省下几个小时。 交互式 Rebase：整理你的提交历史 场景：你吭哧吭哧写了一下午，做了 12 个小提交，但提交信息都是 "wip"、"fix"、"fix again"。现在要提交 PR 了——这些乱七八糟的提交历史会让同事鄙视你。

    git rebase -i HEAD~12

会打开编辑器，列出最近 12 个提交：

    pick a1b2c3d wip
    pick e4f5g6h fix typo
    pick i7j8k9l fix again
    pick m0n1o2p actually works now
    ...

核心操作：

  * **squash (s)** — 把当前提交合并到上一个，保留所有更改但合并为一个提交
  * **fixup (f)** — 类似 squash，但丢弃当前提交的信息（适合那些 "wip" 提交）
  * **reword (r)** — 只改提交信息，不改内容
  * **drop (d)** — 删除这个提交
  * **edit (e)** — 停下来让你修改这个提交的内容

把 12 个乱七八糟的提交整理成 3 个逻辑清晰的提交：

    pick a1b2c3d feat: 添加用户登录 API
    fixup e4f5g6h wip
    fixup i7j8k9l fix typo
    pick m0n1o2p feat: 添加 JWT Token 验证
    fixup n2o3p4q fix again
    pick r5s6t7u docs: 更新 API 文档
    fixup v8w9x0y wip doc

保存退出，Git 自动完成。提交历史从一团乱麻变成清晰的叙事。**注意：只在还没 push 的分支上做 rebase。已经 push 的提交，rebase 会改写历史，需要 force push——在共享分支上这是灾难。** Cherry-Pick：精准移植代码 场景：你在 feature-A 分支上写了一个特别好用的工具函数，feature-B 也需要它。但你不想合并整个 feature-A 分支。

    # 找到那个提交的 hash
    git log feature-A --oneline

    # 摘樱桃
    git checkout feature-B
    git cherry-pick a1b2c3d

Git 会把这个提交的变更单独应用到 feature-B 上，生成一个新的提交（hash 不同，内容相同）。 常见用法：

  * **移植 Bug 修复** — 在 hotfix 分支修了一个 Bug，cherry-pick 到 main 和 dev 分支
  * **复用工具代码** — 在一个分支写的基础组件，移植到另一个分支
  * **回滚后重新应用** — revert 了一个提交后又想加回来

    # 一次 cherry-pick 多个提交
    git cherry-pick a1b2c3d e4f5g6h i7j8k9l

    # 如果冲突了
    git cherry-pick a1b2c3d
    # 解决冲突...
    git add .
    git cherry-pick --continue

    # 放弃这次 cherry-pick
    git cherry-pick --abort

Git Bisect：二分法定位 Bug 场景：两周前一切正常，今天发现一个 Bug，但中间有 200 个提交。是谁引入的？ Bisect 用二分查找自动定位——你只需要告诉 Git 哪个提交是好的、哪个是坏的，然后 Git 切到中间点让你测试。

    git bisect start
    git bisect bad HEAD          # 当前版本有 Bug
    git bisect good v2.0.0       # v2.0.0 是正常的

    # Git 自动切到中间某个提交
    # 测试这个版本有没有 Bug...

    # 如果有 Bug:
    git bisect bad

    # 如果正常:
    git bisect good

    # 重复 5-8 次，Git 定位到引入 Bug 的那个提交
    # de7f3a2 is the first bad commit

    # 结束 bisect
    git bisect reset

200 个提交，log2(200) ≈ 8 次测试就能定位。比一个一个找快 25 倍。

    # 自动化 bisect（如果你的测试可以用脚本跑）
    git bisect start
    git bisect bad HEAD
    git bisect good v2.0.0
    git bisect run python test_specific_feature.py
    # Git 自动二分查找，输出引入 Bug 的提交

总结 命令| 用途| 一句话  
---|---|---  
`git rebase -i`| 整理提交历史| 把 12 个 wip 整理成 3 个清晰的 commit  
`git cherry-pick`| 移植单个提交| 把 A 分支的好代码复制到 B 分支  
`git bisect`| 二分查找 Bug| 从 200 个提交中快速定位是谁引入的 Bug  
这三个命令是高级 Git 用户的标志。不需要每天用，但需要的时候知道怎么用——你的同事会以为你是 Git 魔法师。 📖 相关推荐

  * [Git 常用命令速查表](<https://dingjiu1989-hue.github.io/zh/tech/git-cheatsheet.html>)
  * [单元测试入门：从零到写出第一个可维护的测试](<https://dingjiu1989-hue.github.io/zh/tech/unit-testing-guide.html>)
  * [REST API 设计最佳实践：写出让人愿意用的接口](<https://dingjiu1989-hue.github.io/zh/tech/rest-api-best-practices.html>)

**See also:** [Git 常用命令速查表](</zh/tech/git-cheatsheet.html>), [VS Code 十大必备插件：让编码效率翻倍](</zh/tech/vscode-extensions.html>), [10 款开发者必备的命令行工具（2026 版）](</zh/tools/cli-tools-collection.html>).
