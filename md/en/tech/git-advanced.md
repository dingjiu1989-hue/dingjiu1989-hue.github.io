---
title: "Git Advanced: Interactive Rebase, Cherry-Pick, Bisect, and More"
description: "Master the Git commands that separate senior developers from juniors. Interactive rebase, cherry-pick, bisect, reflog recovery, and custom Git hooks."
date: 2026-05-07
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/git-advanced.html
---

# Git Advanced: Interactive Rebase, Cherry-Pick, Bisect, and More

Most developers stop at `add`, `commit`, `push`, and `pull`. But Git has a set of advanced commands that can save hours of frustration and make your commit history something you're actually proud of. Here's your guide to interactive rebase, cherry-pick, bisect, reflog, and hooks.

## Interactive Rebase: Rewrite History Cleanly

The most powerful Git feature most developers never learn. Interactive rebase lets you reorder, squash, split, and edit commits before pushing.
    
    
    # Squash last 4 commits into 1 clean commit
    git rebase -i HEAD~4
    
    # In the editor, mark commits:
    # pick abc1234 First commit message      (keep as-is)
    # squash def5678 Fix typo                (merge into previous)
    # squash ghi9012 Format code             (merge into previous)
    # squash jkl3456 Update tests            (merge into previous)
    # Then write a single commit message

### When to Use Interactive Rebase

  * **Before pushing to main:** Squash "WIP" and "fix typo" commits into meaningful units
  * **Before opening a PR:** Reorder commits so they tell a logical story
  * **Never:** On shared branches or commits that have been pushed. Rewriting public history causes chaos.



## Cherry-Pick: Apply a Specific Commit Anywhere

When you need one specific commit from another branch without merging everything:
    
    
    # Apply a single commit to the current branch
    git cherry-pick abc1234
    
    # Apply a range of commits
    git cherry-pick abc1234..def5678
    
    # Cherry-pick without committing (stage changes only)
    git cherry-pick -n abc1234

Common use: a bug fix on a release branch that you need on main, but main has diverged significantly. Cherry-pick the fix commit.

## Git Bisect: Find the Commit That Broke Everything

Binary search through your commit history to find exactly which commit introduced a bug:
    
    
    # Start bisect session
    git bisect start
    git bisect bad HEAD          # current commit is broken
    git bisect good v2.5.0       # this tag was working
    
    # Git checks out a commit halfway between. Test it.
    # If broken:  git bisect bad
    # If working: git bisect good
    
    # Repeat until Git identifies the culprit commit.
    # Then end the session:
    git bisect reset

For automated bisecting, provide a test script:
    
    
    git bisect run npm test     # Git runs the test on each step
    # If the test exits with code 0 → good, non-zero → bad
    # Git finds the breaking commit automatically

## Git Reflog: The Ultimate Undo

Reflog records every movement of HEAD — commits, checkouts, rebases, resets. When you think you've lost work, reflog is your safety net:
    
    
    git reflog
    # Shows: abc1234 HEAD@{{0}}: commit: Add login feature
    #        def5678 HEAD@{{1}}: rebase (finish): returning to refs/heads/main
    #        ghi9012 HEAD@{{2}}: reset: moving to HEAD~3
    
    # Recover that "lost" commit
    git checkout HEAD@{{2}}       # go back to before the reset
    git branch recovered-branch   # save it to a branch

Scenario| Recovery Command  
---|---  
Undo a bad rebase| `git reset --hard HEAD@{{1}}`  
Recover deleted branch| `git checkout -b recovered HEAD@{{3}}`  
Undo amend on wrong commit| `git reset --soft HEAD@{{1}}`  
  
## Git Hooks: Automate Your Workflow

Hooks are scripts that run automatically on Git events. They live in `.git/hooks/` and can be written in any language. Use them to prevent mistakes before they happen:
    
    
    #!/bin/bash
    # .git/hooks/pre-commit — run linter before every commit
    npm run lint
    if [ $? -ne 0 ]; then
      echo "Linting failed. Commit aborted."
      exit 1
    fi
    
    
    #!/bin/bash
    # .git/hooks/commit-msg — enforce conventional commits
    MSG=$(cat "$1")
    if ! echo "$MSG" | grep -qE "^(feat|fix|refactor|test|docs|chore)(\(.+\))?: "; then
      echo "Commit message must follow conventional commits format"
      echo "  feat: add feature"
      echo "  fix: resolve bug"
      exit 1
    fi

Hook| When It Runs| Use For  
---|---|---  
pre-commit| Before commit is created| Linting, formatting, unit tests  
commit-msg| After message is entered| Enforce message format  
pre-push| Before push to remote| Integration tests, security scans  
post-checkout| After checkout/switching branches| Install dependencies if changed  
  
**See also:** [Git Commands Cheat Sheet: The Only Reference You Need](</en/tech/git-cheatsheet.html>), [Advanced Prompt Engineering: Techniques That Actually Work for Developers](</en/ai/prompt-engineering-advanced.html>), [Git Workflows: Git Flow vs GitHub Flow vs Trunk-Based Development](</en/tech/git-workflows-team-guide.html>).
