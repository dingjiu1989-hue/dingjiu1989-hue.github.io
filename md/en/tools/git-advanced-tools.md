---
title: "Git Advanced Tools: Interactive Rebase, Bisect, Worktree, Submodules, and Hooks"
description: "Technical exploration of advanced Git features covering interactive rebase, git bisect for debugging, worktree management, submodule strategies, and hook automation."
date: 2026-01-29
board: tools
url: https://dingjiu1989-hue.github.io/en/tools/git-advanced-tools.html
---

# Git Advanced Tools: Interactive Rebase, Bisect, Worktree, Submodules, and Hooks

## Introduction

Most developers use Git at a surface level: add, commit, push, pull, merge. Git's advanced features, however, provide powerful capabilities for history manipulation, debugging, parallel development, dependency management, and automation. These tools separate proficient Git users from experts and significantly impact code quality and development workflow efficiency.

This article covers interactive rebase, git bisect, worktree, submodules, and hooks.

## Interactive Rebase

Interactive rebase rewrites commit history by reordering, squashing, editing, dropping, or splitting commits. It is the primary tool for maintaining a clean, readable commit history before merging feature branches.

git rebase -i HEAD~5

The interactive rebase editor presents a list of commits with actions:

  * `pick` — Use the commit as-is.

  * `reword` — Change the commit message.

  * `edit` — Amend the commit content.

  * `squash` — Combine with the previous commit, merging messages.

  * `fixup` — Combine with the previous commit, discarding message.

  * `drop` — Remove the commit entirely.




Best practices include squashing fixup commits, splitting large commits into logical units, and rewriting messages for clarity. Interactive rebase should only be used on branches not shared with other developers — rewriting public history causes painful merge conflicts for collaborators.

Conflict resolution during rebase requires solving conflicts per commit, not per merge. Each commit in the rebase sequence is applied and paused on conflict. The `git rerere` (reuse recorded resolution) feature automatically applies previously resolved conflict resolutions.

git config --global rerere.enabled true

## Git Bisect: Binary Search for Bugs

git bisect performs binary search through commit history to find the exact commit that introduced a bug. It automates what would otherwise be a manual, tedious process.

git bisect start

git bisect bad HEAD # Current commit is broken

git bisect good v2.3.0 # This tag is known good

## Git checks out a commit halfway between good and bad

## Test the commit and mark:

git bisect good # This commit is still good

## or

git bisect bad # This commit is already broken

## Repeat until the first bad commit is identified

git bisect reset # Return to original HEAD

Automating bisect with a test script speeds the process significantly:

git bisect run npm test

The script should exit 0 for good commits and non-zero for bad commits. For best results, the test should be fast and focused on the bug's symptom.

Bisect is most effective when commits are small, atomic, and well-described. Large commits touching multiple files make bisect identification harder.

## Git Worktree

git worktree allows checking out multiple branches simultaneously in separate directories, sharing a single Git repository. This eliminates the need for multiple clones or stashing changes when switching contexts.

git worktree add ../feature-branch feature-branch

git worktree add ../hotfix hotfix --detach

Use cases include:

  * Working on a hotfix while mid-project in another branch.

  * Running parallel CI verification on different branches.

  * Reviewing pull requests without disrupting current work.

  * Maintaining separate directories for development and production builds.




Worktrees share the same repository objects but maintain separate working directories and indexes. Each worktree has its own HEAD, branch, and staging area.

git worktree list

git worktree remove ../feature-branch

git worktree prune # Clean up references to removed worktrees

## Git Submodules

Submodules embed one Git repository inside another at a specific commit. They are Git's native mechanism for managing external dependencies.

git submodule add https://github.com/org/library.git lib/library

git submodule update --init --recursive

Submodules track a specific commit, not a branch. Updating requires explicitly checking out a new commit in the submodule and committing the change in the parent repository.

cd lib/library

git checkout v2.1.0

cd ../..

git add lib/library

git commit -m "Update library to v2.1.0"

Subtree merging is an alternative to submodules that merges external repositories directly into the parent repository's directory tree. Unlike submodules, subtrees have no separate configuration and do not require developers to learn submodule commands. The trade-off is less clear separation of concerns.

## Git Hooks

Git hooks are scripts that execute at specific points in the Git workflow. They automate validation, enforcement, and integration tasks.

Client-side hooks include:

  * `pre-commit`: Lint code, run formatters, check for secrets.

  * `commit-msg`: Validate commit message format.

  * `pre-push`: Run test suite before pushing.

  * `post-commit`: Notify CI system, update issue tracker.




Server-side hooks include:

  * `pre-receive`: Enforce commit policies, block force pushes.

  * `update`: Per-branch policy enforcement.

  * `post-receive`: Deploy to production, send notifications.




The pre-commit framework manages hooks declaratively:

## .pre-commit-config.yaml

repos:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- repo: https://github.com/pre-commit/pre-commit-hooks

rev: v4.5.0

hooks:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- id: trailing-whitespace

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- id: end-of-file-fixer

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- id: check-yaml

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- repo: https://github.com/psf/black

rev: 24.2.0

hooks:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- id: black

## Conclusion

Advanced Git tools significantly improve development workflows. Interactive rebase maintains clean history. git bisect accelerates debugging through automated binary search. git worktree enables parallel branch work without context switching. Submodules manage dependencies with precise version tracking. Git hooks automate quality enforcement at every workflow stage. Mastering these tools distinguishes proficient Git users and directly improves code quality and team productivity.

**See also:** [Database Management Tools: DBeaver, TablePlus, DataGrip, pgAdmin, and MongoDB Compass](</en/tools/database-management-tools.html>), [Developer Productivity Tools: Essential Toolkit for 2026](</en/tools/productivity-tools.html>), [API Development Tools: Postman, Insomnia, Bruno, Hoppscotch, and Swagger UI](</en/tools/api-development-tools.html>).

**See also:** [Database Management Tools: DBeaver, TablePlus, DataGrip, pgAdmin, and MongoDB Compass](</en/tools/database-management-tools.html>), [Developer Productivity Tools: Essential Toolkit for 2026](</en/tools/productivity-tools.html>), [API Development Tools: Postman, Insomnia, Bruno, Hoppscotch, and Swagger UI](</en/tools/api-development-tools.html>)

**See also:** [Database Management Tools: DBeaver, TablePlus, DataGrip, pgAdmin, and MongoDB Compass](</en/tools/database-management-tools.html>), [Developer Productivity Tools: Essential Toolkit for 2026](</en/tools/productivity-tools.html>), [API Development Tools: Postman, Insomnia, Bruno, Hoppscotch, and Swagger UI](</en/tools/api-development-tools.html>)

**See also:** [Database Management Tools: DBeaver, TablePlus, DataGrip, pgAdmin, and MongoDB Compass](</en/tools/database-management-tools.html>), [Developer Productivity Tools: Essential Toolkit for 2026](</en/tools/productivity-tools.html>), [API Development Tools: Postman, Insomnia, Bruno, Hoppscotch, and Swagger UI](</en/tools/api-development-tools.html>)

**See also:** [Database Management Tools: DBeaver, TablePlus, DataGrip, pgAdmin, and MongoDB Compass](</en/tools/database-management-tools.html>), [Developer Productivity Tools: Essential Toolkit for 2026](</en/tools/productivity-tools.html>), [API Development Tools: Postman, Insomnia, Bruno, Hoppscotch, and Swagger UI](</en/tools/api-development-tools.html>)

**See also:** [Database Management Tools: DBeaver, TablePlus, DataGrip, pgAdmin, and MongoDB Compass](</en/tools/database-management-tools.html>), [Developer Productivity Tools: Essential Toolkit for 2026](</en/tools/productivity-tools.html>), [API Development Tools: Postman, Insomnia, Bruno, Hoppscotch, and Swagger UI](</en/tools/api-development-tools.html>)

**See also:** [API Testing Tools: Bruno, Hoppscotch, Postman, Insomnia in 2026](</en/tools/api-testing-2026.html>), [Code Editor Plugins: Must-Have Extensions for Productivity](</en/tools/code-editor-plugins.html>), [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>)

**See also:** [API Testing Tools: Bruno, Hoppscotch, Postman, Insomnia in 2026](</en/tools/api-testing-2026.html>), [Code Editor Plugins: Must-Have Extensions for Productivity](</en/tools/code-editor-plugins.html>), [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>)

**See also:** [API Testing Tools: Bruno, Hoppscotch, Postman, Insomnia in 2026](</en/tools/api-testing-2026.html>), [Code Editor Plugins: Must-Have Extensions for Productivity](</en/tools/code-editor-plugins.html>), [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>)

**See also:** [API Testing Tools: Bruno, Hoppscotch, Postman, Insomnia in 2026](</en/tools/api-testing-2026.html>), [Code Editor Plugins: Must-Have Extensions for Productivity](</en/tools/code-editor-plugins.html>), [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>)

**See also:** [API Testing Tools: Bruno, Hoppscotch, Postman, Insomnia in 2026](</en/tools/api-testing-2026.html>), [Code Editor Plugins: Must-Have Extensions for Productivity](</en/tools/code-editor-plugins.html>), [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>)
