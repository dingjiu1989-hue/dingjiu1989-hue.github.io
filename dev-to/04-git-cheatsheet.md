---
title: "Git Commands Cheat Sheet: The Only Reference You'll Ever Need"
published: true
description: "Every Git command you need in daily work — from basic staging to interactive rebase. Includes undo operations, branching strategy, and a printable quick-reference card."
tags: git, beginners, programming, devops, tutorial
canonical_url: https://dingjiu1989-hue.github.io/en/tech/git-cheatsheet.html
---

Git is the backbone of modern software development. This cheat sheet covers every command you'll need in daily work.

## Setup & Starting a Repository

```bash
git config --global user.name "Your Name"
git config --global init.defaultBranch main
git init                    # create a new repo
git clone <url>             # clone an existing repo
```

## Staging & Committing

```bash
git status                  # what changed?
git add -p                  # stage interactively (hunks)
git commit -m "message"     # commit staged changes
git commit --amend          # fix the last commit message
```

## Branching

```bash
git branch                  # list local branches
git checkout -b feature/x   # create AND switch
git switch -c feature/x     # modern create + switch
git merge feature/x         # merge into current branch
git branch -d feature/x     # delete (safe — warns if unmerged)
```

## Undoing Things (Save This Section)

```bash
git restore <file>           # discard working changes
git restore --staged <file>  # unstage a file
git reset --soft HEAD~1      # undo last commit, keep changes staged
git stash                     # save uncommitted changes
git stash pop                 # restore stashed changes
git revert <commit>           # safe undo — creates a new commit
```

## Remote Repositories

```bash
git remote -v                        # list remotes
git push -u origin main              # push and set upstream
git pull --rebase origin main        # fetch + rebase (cleaner history)
git push origin --delete feature/x   # delete remote branch
```

## Log & History

```bash
git log --oneline --graph --all      # pretty history graph
git log -p <file>                    # see changes to a file
git blame <file>                     # who changed what line
git show <commit>                    # details of a specific commit
```

## Interactive Rebase (Advanced But Essential)

```bash
git rebase -i HEAD~3                 # squash/reword last 3 commits
git rebase -i --autosquash           # auto-squash fixup commits
```

## Quick Reference Card

| Task | Command |
|---|---|
| Create branch | `git checkout -b feature/x` |
| Save work temporarily | `git stash` |
| Undo last commit | `git reset --soft HEAD~1` |
| Discard file changes | `git restore file.txt` |
| See recent work | `git log --oneline -10` |
| Sync with remote | `git pull --rebase` |

**Bookmark this page. You'll be back.**

---

*Originally published at [AI Study Room](https://dingjiu1989-hue.github.io/en/tech/git-cheatsheet.html) — 70+ curated articles for developers.*
