---
title: "Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging"
description: "Essential debugging tools for developers: lldb and gdb for native debugging, strace for system call tracing, ltrace for library call tracing, and rr for reverse"
date: 2026-02-02
board: tools
url: https://dingjiu1989-hue.github.io/en/tools/debugging-tools.html
---

# Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging

## Introduction

Debugging is a core developer skill. Beyond print statements and basic breakpoints, advanced debugging tools provide deep insight into program behavior. This article covers lldb and gdb for native code debugging, strace for system call tracing, ltrace for library call analysis, and rr for the revolutionary capability of reverse execution.

## lldb (LLVM Debugger)

The modern debugger from the LLVM project, preferred for Clang-compiled code:

## Start debugging

lldb ./myapp

lldb -p 12345 # Attach to process

lldb -c core.dump ./myapp # Analyze core dump

## Breakpoints

(lldb) breakpoint set --name main

(lldb) breakpoint set --file app.c --line 42

(lldb) breakpoint set --selector viewDidLoad

(lldb) breakpoint set --func-regex "._alloc._ "

(lldb) breakpoint command add 1

> frame variable
> 
> continue
> 
> DONE

## Execution control

(lldb) run

(lldb) continue

(lldb) next # Step over

(lldb) step # Step into

(lldb) finish # Step out

## Variable inspection

(lldb) frame variable

(lldb) frame variable --regex "._error._ "

(lldb) expression myVar

(lldb) expression self->name

(lldb) expression --objc -- print [NSString stringWithFormat:@"%@", myString]

## Thread and backtrace

(lldb) thread backtrace

(lldb) thread backtrace all

(lldb) thread select 2

## Watchpoints (break on data access)

(lldb) watchpoint set variable myVar

(lldb) watchpoint set expression -- myPointer[5]

## gdb (GNU Debugger)

The traditional Unix debugger:

## Compile with debug symbols

gcc -g -O0 myapp.c -o myapp

## Start debugging

gdb ./myapp

gdb -p 12345

gdb ./myapp core

## Common commands

(gdb) break main

(gdb) break app.c:42 if x > 5

(gdb) run arg1 arg2

(gdb) bt # Backtrace

(gdb) info locals # Show local variables

(gdb) print x

(gdb) display x # Auto-display every stop

(gdb) watch y # Break when y changes

(gdb) x/20x ptr # Examine memory as hex

(gdb) disassemble # Show assembly

## Scripted debugging

(gdb) set pagination off

(gdb) set logging on

(gdb) commands

> print x
> 
> continue
> 
> end

## TUI mode (split view)

gdb -tui ./myapp

## strace (System Call Trace)

Trace all system calls a program makes:

## Trace a command

strace -o trace.log ./myapp

strace -f ./myapp # Follow forks

## Common filters

strace -e open,read,write ./myapp # Specific syscalls

strace -e network ./myapp # Network-related calls

strace -e trace=file ./myapp # File operations

strace -e trace=process ./myapp # Process management

strace -e trace=signal ./myapp # Signal handling

## Performance analysis

strace -c ./myapp # Syscall count and time summary

strace -T ./myapp # Time spent in each syscall

strace -r ./myapp # Relative timestamps

## Useful patterns

strace -p 12345 -e write -s 1000 # See what a process writes

strace -f -e openat -p $(pgrep nginx) # File opens by nginx workers

strace -e read -s 10000 python3 app.py # Show read content

## PID tracking and timing

strace -fy -t -T -o trace.log -p 12345

**What to look for** : `ENOENT` (file not found), `EACCES` (permission denied), `ECONNREFUSED` (connection refused), slow syscalls (high `-T` values), unexpected file opens, excessive context switching.

## ltrace (Library Call Trace)

Trace library function calls:

## Basic usage

ltrace ./myapp

ltrace -o libcalls.log ./myapp

## Filter specific libraries

ltrace -e malloc+free ./myapp # Memory allocation calls

ltrace -e str* ./myapp # String functions

ltrace -e 'libc.*' ./myapp # All libc functions

## Count library calls

ltrace -c ./myapp

## With timing

ltrace -T ./myapp # Time per call

ltrace -S ./myapp # Show syscalls too

## Suppress repetitive calls

ltrace -n 2 ./myapp # Indent by call depth

## rr (Reverse Debugger)

Record and replay debugging with reverse execution:

## Record execution

rr record ./myapp

rr record -- ./myapp arg1 arg2

## Replay (deterministic)

rr replay

rr replay -p 12345

## Reverse debugging commands

(gdb) reverse-continue # Go back to most recent event

(gdb) reverse-step # Step back

(gdb) reverse-next # Step over back

(gdb) reverse-finish # Go back to function entry

## Find when a variable changed

(gdb) watch -l myVar

(gdb) reverse-continue # Stops when myVar last changed

## Go to specific event

rr replay -M 12345 # Replay to event number 12345

## Chaos mode (test concurrency)

rr record --chaos ./myapp # Randomize thread scheduling

**Key strength** : Debug intermittent bugs by recording once, then replaying infinitely. When you miss the bug, just restart replay and be more prepared. Chaos mode helps find concurrency bugs.

## Debugging Workflow

## 1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Program crashes — get a core dump

ulimit -c unlimited

./myapp

gdb ./myapp core

## 2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Use strace to see what the program is doing

strace -f -o trace.log ./myapp

less trace.log # Look for error syscalls

## 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. For tricky bugs, use rr

rr record ./myapp

rr replay

## Now you can step forward AND backward

## 4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Library call issues

ltrace -c ./myapp # Which library calls are most frequent?

## Comparison

| Tool | Best For | Overhead | Learning Curve |

|------|----------|----------|----------------|

| lldb | Native debugging (LLVM) | Low | Medium |

| gdb | Native debugging (GCC) | Low | High (many commands) |

| strace | System call tracing | Medium | Low |

| ltrace | Library call tracing | Medium | Low |

| rr | Reverse debugging | High (record) | Medium |

## Recommendations

  * **General debugging** : lldb for new projects, gdb for legacy code. Both support the same core debugging workflow.

  * **File/permission issues** : strace is the fastest way to find "file not found" or "permission denied" problems.

  * **Performance debugging** : strace -c shows where your program spends time in syscalls.

  * **Intermittent bugs** : rr is revolutionary — record once, replay infinitely with reverse execution.

  * **Library comprehension** : ltrace shows which library functions are called and how often.




Start with strace for quick diagnostics. Use lldb/gdb for step-through debugging. Deploy rr for your hardest bugs — the reverse execution capability makes "oops, I missed that" a thing of the past.

**See also:** [Documentation Tools for Developers 2026](</en/tools/documentation-tools.html>), [Developer Productivity Tools: Essential Toolkit for 2026](</en/tools/productivity-tools.html>), [Note-Taking and Knowledge Management Tools](</en/tools/note-taking-apps.html>).

**See also:** [Command-Line Productivity: fzf, ripgrep, jq, bat, tmux, zoxide, and lazygit](</en/tools/command-line-productivity.html>), [Git Advanced Tools: Interactive Rebase, Bisect, Worktree, Submodules, and Hooks](</en/tools/git-advanced-tools.html>), [Code Editor Plugins: Must-Have Extensions for Productivity](</en/tools/code-editor-plugins.html>)

**See also:** [Command-Line Productivity: fzf, ripgrep, jq, bat, tmux, zoxide, and lazygit](</en/tools/command-line-productivity.html>), [Git Advanced Tools: Interactive Rebase, Bisect, Worktree, Submodules, and Hooks](</en/tools/git-advanced-tools.html>), [Code Editor Plugins: Must-Have Extensions for Productivity](</en/tools/code-editor-plugins.html>)

**See also:** [Command-Line Productivity: fzf, ripgrep, jq, bat, tmux, zoxide, and lazygit](</en/tools/command-line-productivity.html>), [Git Advanced Tools: Interactive Rebase, Bisect, Worktree, Submodules, and Hooks](</en/tools/git-advanced-tools.html>), [Code Editor Plugins: Must-Have Extensions for Productivity](</en/tools/code-editor-plugins.html>)

**See also:** [Command-Line Productivity: fzf, ripgrep, jq, bat, tmux, zoxide, and lazygit](</en/tools/command-line-productivity.html>), [Git Advanced Tools: Interactive Rebase, Bisect, Worktree, Submodules, and Hooks](</en/tools/git-advanced-tools.html>), [Code Editor Plugins: Must-Have Extensions for Productivity](</en/tools/code-editor-plugins.html>)

**See also:** [Command-Line Productivity: fzf, ripgrep, jq, bat, tmux, zoxide, and lazygit](</en/tools/command-line-productivity.html>), [Git Advanced Tools: Interactive Rebase, Bisect, Worktree, Submodules, and Hooks](</en/tools/git-advanced-tools.html>), [Code Editor Plugins: Must-Have Extensions for Productivity](</en/tools/code-editor-plugins.html>)

**See also:** [Kubernetes Tools: kubectl Plugins, k9s, Lens, Kustomize](</en/tools/kubernetes-tools.html>), [Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide](</en/tools/networking-tools.html>), [Redis Tools: RedisInsight, Redis CLI, Redis Commander](</en/tools/redis-tools.html>)

**See also:** [Kubernetes Tools: kubectl Plugins, k9s, Lens, Kustomize](</en/tools/kubernetes-tools.html>), [Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide](</en/tools/networking-tools.html>), [Redis Tools: RedisInsight, Redis CLI, Redis Commander](</en/tools/redis-tools.html>)

**See also:** [Kubernetes Tools: kubectl Plugins, k9s, Lens, Kustomize](</en/tools/kubernetes-tools.html>), [Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide](</en/tools/networking-tools.html>), [Redis Tools: RedisInsight, Redis CLI, Redis Commander](</en/tools/redis-tools.html>)

**See also:** [Kubernetes Tools: kubectl Plugins, k9s, Lens, Kustomize](</en/tools/kubernetes-tools.html>), [Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide](</en/tools/networking-tools.html>), [Redis Tools: RedisInsight, Redis CLI, Redis Commander](</en/tools/redis-tools.html>)

**See also:** [Kubernetes Tools: kubectl Plugins, k9s, Lens, Kustomize](</en/tools/kubernetes-tools.html>), [Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide](</en/tools/networking-tools.html>), [Redis Tools: RedisInsight, Redis CLI, Redis Commander](</en/tools/redis-tools.html>)

**See also:** [Kubernetes Tools: kubectl Plugins, k9s, Lens, Kustomize](</en/tools/kubernetes-tools.html>), [Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide](</en/tools/networking-tools.html>), [Redis Tools: RedisInsight, Redis CLI, Redis Commander](</en/tools/redis-tools.html>)
