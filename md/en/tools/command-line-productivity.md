---
title: "Command-Line Productivity: fzf, ripgrep, jq, bat, tmux, zoxide, and lazygit"
description: "Guide to essential command-line productivity tools covering fzf for fuzzy finding, ripgrep for code search, jq for JSON processing, bat, tmux, zoxide, and lazygit."
date: 2026-01-28
board: tools
url: https://aidev.fit/en/tools/command-line-productivity.html
---

# Command-Line Productivity: fzf, ripgrep, jq, bat, tmux, zoxide, and lazygit

## Introduction

The command line remains the most powerful interface for development, operations, and data processing. Modern command-line tools have transformed the terminal experience, providing capabilities that rival graphical interfaces for many tasks. Mastering these tools significantly reduces friction in daily workflows.

This article covers seven essential CLI productivity tools: fzf, ripgrep, jq, bat, tmux, zoxide, and lazygit.

## fzf: Fuzzy Finder

fzf is a general-purpose fuzzy finder that pipes any list of items into an interactive search interface. It can search files, command history, processes, git branches, and virtually any text stream.

## Search files recursively with preview

vim $(fzf --preview 'bat --color=always {}')

## Search and kill processes

kill -9 $(ps aux | fzf --header-lines=1 | awk '{print $2}')

## Interactive git branch checkout

git checkout $(git branch -a | fzf --height=40%)

fzf's key bindings enhance shell navigation: `Ctrl+T` pastes selected file paths, `Ctrl+R` searches command history, and `Alt+C` changes to selected directories. Custom preview windows using bat, head, or tree provide context before selection.

## ripgrep (rg): Blazingly Fast Code Search

ripgrep recursively searches through files with regex patterns, respecting .gitignore and hidden files by default. It is significantly faster than grep, ack, or ag due to its use of SIMD instructions and optimized search algorithms.

## Search for pattern in current directory

rg "function getUsers" --type ts

## Search with context lines

rg "TODO" --context 3

## Search but exclude specific files

rg "password" --glob '!*.lock'

ripgrep output integrates with editors through the `--json` flag and supports PCRE2 regex features including lookaheads and backreferences. Combined with fzf, it provides instant code search across large repositories.

## jq: JSON Processor

jq is a lightweight and flexible command-line JSON processor. It filters, transforms, and formats JSON data with a powerful expression language.

## Pretty-print JSON

cat data.json | jq '.'

## Extract specific fields

curl -s https://api.github.com/repos/jqlang/jq | jq '{name, description, stars: .stargazers_count}'

## Filter array items

cat logs.json | jq '.[] | select(.severity == "ERROR") | {timestamp, message}'

jq expressions range from simple field access to complex transformations with map, reduce, group_by, and custom functions. The `-c` flag produces compact output for streaming. Combined with `--stream`, jq processes JSON files larger than available memory.

## bat: cat with Syntax Highlighting

bat is a clone of cat with syntax highlighting, Git integration, and automatic paging. It supports hundreds of languages with theme customization.

bat --paging=never file.json

bat --style=plain file.py

bat --language=yaml config.yaml

bat integrates with other tools as a pager. Setting `BAT_THEME` in shell configuration provides consistent color schemes. The `bat cache --build` command regenerates the syntax cache after installing new language definitions.

## tmux: Terminal Multiplexer

tmux enables multiple terminal sessions within a single window, session persistence across disconnections, and split-pane layouts.

tmux new -s project

tmux attach -t project

Essential tmux key bindings:

  * `Ctrl+B %` — Split pane vertically.

  * `Ctrl+B "` — Split pane horizontally.

  * `Ctrl+B c` — Create new window.

  * `Ctrl+B ,` — Rename current window.

  * `Ctrl+B [` — Enter scroll/copy mode.




tmux configuration in `~/.tmux.conf` customizes key bindings, status bar, colors, and mouse support. Plugins via tpm (tmux plugin manager) add features like persistent sessions, save/restore, and CPU monitoring.

## zoxide: Smarter Directory Navigation

zoxide learns your directory usage patterns and allows jumping to frequently accessed directories with partial names.

z proj # Jump to ~/projects/my-project

z proj/src # Jump to subdirectory

zi # Interactive selection with fzf

zoxide replaces cd with a learning database: `z foo` navigates to the most relevant directory containing "foo" based on frequency and recency. The `zi` command opens an interactive fzf selector for ambiguous matches.

## lazygit: Terminal Git Interface

lazygit provides a terminal-based Git interface with vim-like keybindings. It visualizes the staging area, commit graph, branch tree, and file changes in split-pane views.

lazygit

Essential operations:

  * Arrow keys navigate files and commits.

  * Space to stage/unstage files.

  * `c` to commit, `p` to push.

  * `m` to merge, `r` to rebase.

  * `d` to view diff of selected file.

  * `:` for custom commands.




lazygit significantly reduces Git command memorization while providing visual feedback for complex operations like interactive rebase, conflict resolution, and cherry-picking.

## Conclusion

Modern CLI tools dramatically improve terminal productivity. fzf provides instant interactive filtering. ripgrep replaces slow grep with millisecond code search. jq transforms JSON manipulation on the command line. bat enhances file viewing. tmux enables persistent, multi-window terminal sessions. zoxide eliminates directory navigation friction. lazygit provides visual Git operations without leaving the terminal. Investing time to learn these tools pays dividends in daily efficiency.

**See also:** [Redis Tools: RedisInsight, Redis CLI, Redis Commander](</en/tools/redis-tools.html>), [Code Editor Plugins: Must-Have Extensions for Productivity](</en/tools/code-editor-plugins.html>), [Developer Productivity Tools: Essential Toolkit for 2026](</en/tools/productivity-tools.html>).

**See also:** [Code Editor Plugins: Must-Have Extensions for Productivity](</en/tools/code-editor-plugins.html>), [Redis Tools: RedisInsight, Redis CLI, Redis Commander](</en/tools/redis-tools.html>), [Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide](</en/tools/networking-tools.html>)

**See also:** [Code Editor Plugins: Must-Have Extensions for Productivity](</en/tools/code-editor-plugins.html>), [Redis Tools: RedisInsight, Redis CLI, Redis Commander](</en/tools/redis-tools.html>), [Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide](</en/tools/networking-tools.html>)

**See also:** [Code Editor Plugins: Must-Have Extensions for Productivity](</en/tools/code-editor-plugins.html>), [Redis Tools: RedisInsight, Redis CLI, Redis Commander](</en/tools/redis-tools.html>), [Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide](</en/tools/networking-tools.html>)

**See also:** [Code Editor Plugins: Must-Have Extensions for Productivity](</en/tools/code-editor-plugins.html>), [Redis Tools: RedisInsight, Redis CLI, Redis Commander](</en/tools/redis-tools.html>), [Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide](</en/tools/networking-tools.html>)

**See also:** [Code Editor Plugins: Must-Have Extensions for Productivity](</en/tools/code-editor-plugins.html>), [Redis Tools: RedisInsight, Redis CLI, Redis Commander](</en/tools/redis-tools.html>), [Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide](</en/tools/networking-tools.html>)

**See also:** [IaC Tools Compared: Terraform, Pulumi, CDK, OpenTofu, and CloudFormation](</en/tools/iac-tools-compared.html>), [Cloud CLI Tools: aws-cli, gcloud, az, s5cmd, Cloud Comparisons](</en/tools/cloud-cli-tools.html>), [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>)

**See also:** [IaC Tools Compared: Terraform, Pulumi, CDK, OpenTofu, and CloudFormation](</en/tools/iac-tools-compared.html>), [Cloud CLI Tools: aws-cli, gcloud, az, s5cmd, Cloud Comparisons](</en/tools/cloud-cli-tools.html>), [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>)

**See also:** [IaC Tools Compared: Terraform, Pulumi, CDK, OpenTofu, and CloudFormation](</en/tools/iac-tools-compared.html>), [Cloud CLI Tools: aws-cli, gcloud, az, s5cmd, Cloud Comparisons](</en/tools/cloud-cli-tools.html>), [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>)

**See also:** [IaC Tools Compared: Terraform, Pulumi, CDK, OpenTofu, and CloudFormation](</en/tools/iac-tools-compared.html>), [Cloud CLI Tools: aws-cli, gcloud, az, s5cmd, Cloud Comparisons](</en/tools/cloud-cli-tools.html>), [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>)

**See also:** [IaC Tools Compared: Terraform, Pulumi, CDK, OpenTofu, and CloudFormation](</en/tools/iac-tools-compared.html>), [Cloud CLI Tools: aws-cli, gcloud, az, s5cmd, Cloud Comparisons](</en/tools/cloud-cli-tools.html>), [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>)

**See also:** [IaC Tools Compared: Terraform, Pulumi, CDK, OpenTofu, and CloudFormation](</en/tools/iac-tools-compared.html>), [Cloud CLI Tools: aws-cli, gcloud, az, s5cmd, Cloud Comparisons](</en/tools/cloud-cli-tools.html>), [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>)

**See also:** [IaC Tools Compared: Terraform, Pulumi, CDK, OpenTofu, and CloudFormation](</en/tools/iac-tools-compared.html>), [Cloud CLI Tools: aws-cli, gcloud, az, s5cmd, Cloud Comparisons](</en/tools/cloud-cli-tools.html>), [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>)

**See also:** [IaC Tools Compared: Terraform, Pulumi, CDK, OpenTofu, and CloudFormation](</en/tools/iac-tools-compared.html>), [Cloud CLI Tools: aws-cli, gcloud, az, s5cmd, Cloud Comparisons](</en/tools/cloud-cli-tools.html>), [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>)

**See also:** [IaC Tools Compared: Terraform, Pulumi, CDK, OpenTofu, and CloudFormation](</en/tools/iac-tools-compared.html>), [Cloud CLI Tools: aws-cli, gcloud, az, s5cmd, Cloud Comparisons](</en/tools/cloud-cli-tools.html>), [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>)

**See also:** [IaC Tools Compared: Terraform, Pulumi, CDK, OpenTofu, and CloudFormation](</en/tools/iac-tools-compared.html>), [Cloud CLI Tools: aws-cli, gcloud, az, s5cmd, Cloud Comparisons](</en/tools/cloud-cli-tools.html>), [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>)

**See also:** [IaC Tools Compared: Terraform, Pulumi, CDK, OpenTofu, and CloudFormation](</en/tools/iac-tools-compared.html>), [Cloud CLI Tools: aws-cli, gcloud, az, s5cmd, Cloud Comparisons](</en/tools/cloud-cli-tools.html>), [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>)

**See also:** [IaC Tools Compared: Terraform, Pulumi, CDK, OpenTofu, and CloudFormation](</en/tools/iac-tools-compared.html>), [Cloud CLI Tools: aws-cli, gcloud, az, s5cmd, Cloud Comparisons](</en/tools/cloud-cli-tools.html>), [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>)

**See also:** [IaC Tools Compared: Terraform, Pulumi, CDK, OpenTofu, and CloudFormation](</en/tools/iac-tools-compared.html>), [Cloud CLI Tools: aws-cli, gcloud, az, s5cmd, Cloud Comparisons](</en/tools/cloud-cli-tools.html>), [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>)

**See also:** [IaC Tools Compared: Terraform, Pulumi, CDK, OpenTofu, and CloudFormation](</en/tools/iac-tools-compared.html>), [Cloud CLI Tools: aws-cli, gcloud, az, s5cmd, Cloud Comparisons](</en/tools/cloud-cli-tools.html>), [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>)

**See also:** [IaC Tools Compared: Terraform, Pulumi, CDK, OpenTofu, and CloudFormation](</en/tools/iac-tools-compared.html>), [Cloud CLI Tools: aws-cli, gcloud, az, s5cmd, Cloud Comparisons](</en/tools/cloud-cli-tools.html>), [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>)

**See also:** [IaC Tools Compared: Terraform, Pulumi, CDK, OpenTofu, and CloudFormation](</en/tools/iac-tools-compared.html>), [Cloud CLI Tools: aws-cli, gcloud, az, s5cmd, Cloud Comparisons](</en/tools/cloud-cli-tools.html>), [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>)

**See also:** [IaC Tools Compared: Terraform, Pulumi, CDK, OpenTofu, and CloudFormation](</en/tools/iac-tools-compared.html>), [Cloud CLI Tools: aws-cli, gcloud, az, s5cmd, Cloud Comparisons](</en/tools/cloud-cli-tools.html>), [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>)
