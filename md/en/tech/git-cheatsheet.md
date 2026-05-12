---
title: "Git Commands Cheat Sheet: The Only Reference You Need"
description: "A comprehensive Git cheat sheet covering branches, undo operations, staging, commits, and remote collaboration. Bookmark this for quick lookups."
date: 2026-05-07
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/git-cheatsheet.html
---

# Git Commands Cheat Sheet: The Only Reference You Need

Git is the backbone of modern software development. This cheat sheet covers every command you'll need in daily work — from basic commits to hairy rebase scenarios.

## Setup & Configuration
    
    
    git config --global user.name "Your Name"
    git config --global user.email "you@example.com"
    git config --global init.defaultBranch main
    git config --list  # show all settings

## Starting a Repository
    
    
    git init                    # create a new repo
    git clone <url>             # clone an existing repo
    git clone -b <branch> <url> # clone a specific branch

## Staging & Committing
    
    
    git status                  # what changed?
    git add <file>              # stage a file
    git add -p                  # stage interactively (hunks)
    git commit -m "message"     # commit staged changes
    git commit -am "message"    # add tracked files AND commit
    git commit --amend          # fix the last commit message

## Branching
    
    
    git branch                  # list local branches
    git branch <name>           # create a branch
    git checkout <name>         # switch to a branch
    git checkout -b <name>      # create AND switch
    git switch <name>           # modern way to switch
    git switch -c <name>        # modern create + switch
    git merge <branch>          # merge branch into current
    git branch -d <name>        # delete a branch (safe)
    git branch -D <name>        # force delete

## Undoing Things
    
    
    git restore <file>          # discard working changes
    git restore --staged <file> # unstage a file
    git reset --soft HEAD~1     # undo last commit, keep changes staged
    git reset --hard HEAD~1     # undo last commit, discard changes (DANGER)
    git revert <commit>         # safe undo — creates a new commit
    git stash                    # save uncommitted changes
    git stash pop                # restore stashed changes

## Remote Repositories
    
    
    git remote -v                        # list remotes
    git remote add origin <url>          # add a remote
    git push origin main                 # push to remote
    git push -u origin main              # push and set upstream
    git pull origin main                 # fetch + merge
    git fetch origin                     # fetch without merging
    git push origin --delete <branch>    # delete remote branch

## Log & History
    
    
    git log --oneline --graph --all      # pretty history graph
    git log -p <file>                    # see changes to a file
    git blame <file>                     # who changed what line
    git diff                             # unstaged changes
    git diff --staged                    # staged changes
    git show <commit>                    # details of a commit

## Advanced: Interactive Rebase
    
    
    git rebase -i HEAD~3                 # squash/reword last 3 commits
    git rebase -i --autosquash           # auto-squash fixup commits
    git rebase --continue | --abort | --skip

## Quick Reference Card

Task| Command  
---|---  
Create branch| `git checkout -b feature/x`  
Save work| `git stash`  
Undo last commit| `git reset --soft HEAD~1`  
Discard file changes| `git restore file.txt`  
See what you did| `git log --oneline -10`  
Sync with remote| `git pull --rebase`  
  
Bookmark this page. You'll be back.
