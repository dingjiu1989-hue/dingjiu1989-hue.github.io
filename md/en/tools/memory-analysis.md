---
title: "Memory Analysis: Valgrind, heaptrack, memray, Heap Profiling"
description: "Comprehensive guide to memory analysis tools: Valgrind for memory error detection, heaptrack for Linux heap profiling, memray for Python memory analysis, and ge"
date: 2026-02-04
board: tools
url: https://dingjiu1989-hue.github.io/en/tools/memory-analysis.html
---

# Memory Analysis: Valgrind, heaptrack, memray, Heap Profiling

## Introduction

Memory issues — leaks, fragmentation, excessive allocation, and buffer overflows — are among the hardest bugs to diagnose. Specialized memory analysis tools can pinpoint the exact line of code causing the problem. This article covers Valgrind for C/C++ memory errors, heaptrack for Linux heap profiling, memray for Python memory tracking, and general heap profiling techniques.

## Valgrind

The gold standard for C/C++ memory error detection:

## Basic memory check

valgrind ./myapp

valgrind --leak-check=yes ./myapp

valgrind --tool=memcheck --leak-check=full ./myapp

## Detailed output

valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes ./myapp

## Suppress known leaks

valgrind --suppressions=suppressions.txt ./myapp

## Generate suppression file

valgrind --leak-check=full --gen-suppressions=all ./myapp 2> suppressions.txt

## Cache profiling

valgrind --tool=cachegrind ./myapp

## Call graph profiling

valgrind --tool=callgrind ./myapp

## Massif (heap profiler)

valgrind --tool=massif ./myapp

ms_print massif.out.12345 # View heap profile

## Profile specific duration

valgrind --tool=callgrind --dump-instr=yes --simulate-cache=yes ./myapp

// Example of errors Valgrind catches

void memory_errors() {

// Buffer overflow — Valgrind catches this

char buf[10];

buf[10] = 'x'; // Error: invalid write

// Use-after-free

char *ptr = malloc(10);

free(ptr);

ptr[0] = 'a'; // Error: invalid read/write

// Memory leak

char *leak = malloc(100); // Never freed

// Valgrind: definitely lost: 100 bytes

// Uninitialized value

int x;

if (x == 5) {} // Error: conditional depends on uninit value

}

**Key tools** : `memcheck` for memory errors and leaks, `cachegrind` for cache profiling, `callgrind` for call graph analysis, `massif` for heap profiling.

## heaptrack

A modern Linux heap memory profiler with lower overhead than Valgrind:

## Installation

sudo apt install heaptrack # Debian/Ubuntu

brew install heaptrack # macOS (partial)

## Profile an application

heaptrack ./myapp

heaptrack ./myapp arg1 arg2

## Attach to running process

heaptrack -p 12345

## Analyze results

heaptrack_print heaptrack.myapp.12345.gz

heaptrack_gui heaptrack.myapp.12345.gz # GUI viewer

## Output analysis

heaptrack_print --print-leak-types --print-total heaptrack.myapp.12345.gz

**Key features** : Lower overhead than Valgrind (suitable for production-like loads), call-stack-based allocation tracking, detailed time-based allocation charts, peak memory analysis, leak detection.

## memray

Python memory profiler with high-resolution tracking:

## Installation

pip install memray

## Profile a script

memray run myapp.py

memray run -o output.bin myapp.py

## Profile with live tracking

memray run --live myapp.py

## Attach to running process

memray attach --pid 12345 --output output.bin

## Generate reports

memray flamegraph output.bin # Interactive flamegraph

memray table output.bin # Text table report

memray tree output.bin # Tree view

memray stats output.bin # Summary statistics

memray summary output.bin # High-level summary

## Compare allocations

memray diff before.bin after.bin

## Python native support

## Programmatic memory tracking

import memray

with memray.Tracker("profile.bin"):

## Code to profile

data = [i for i in range(1000000)]

processed = [x * 2 for x in data]

## Decorator for function profiling

@memray.tracker("func_profile.bin")

def my_function():

pass

## Context manager with specific recording

with memray.Tracker("allocations.bin", native_traces=True):

large_list = [object() for _ in range(500000)]

**Key features** : Python-native (no C extension needed in many cases), thread-safe, native stack traces, live tracking, multiple report formats including interactive flamegraphs.

## General Heap Profiling

## jemalloc heap profiling

## Enable jemalloc profiling

export MALLOC_CONF="prof:true,prof_active:true,lg_prof_sample:17"

./myapp

## Trigger profile dump

kill -SIGUSR2 $PID # Dumps heap profile

jeprof --show_bytes --pdf ./myapp heap.prof > heap.pdf

## Compare profiles

jeprof --show_bytes --pdf ./myapp --base=heap1.prof heap2.prof > diff.pdf

## GCC address sanitizer

## Compile with address sanitizer

gcc -fsanitize=address -g -O1 myapp.c -o myapp

./myapp # Will detect buffer overflows and use-after-free

## Leak sanitizer

gcc -fsanitize=leak -g myapp.c -o myapp

## Memory Analysis Workflow

## 1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Detect the issue (OOM or high RSS growth)

## 2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Run with memcheck for memory errors

valgrind --leak-check=full ./myapp

## 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Profile heap with massif or heaptrack

heaptrack ./myapp

## 4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Analyze the profile

heaptrack_print heaptrack.*.gz

## 5\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. For Python: use memray

memray run myapp.py

memray flamegraph memray-myapp.*.bin

## Comparison

| Tool | Language | Overhead | Best For |

|------|----------|----------|----------|

| Valgrind | C/C++ | 10-20x | Memory errors, leaks |

| heaptrack | C/C++/Rust | 2-3x | Heap allocation profiling |

| memray | Python | 1.5-3x | Python memory tracking |

| jemalloc | C/C++ | Low | Production heap profiling |

| ASan | C/C++ | 2x | Buffer overflows, UAF |

## Recommendations

  * **C/C++ memory errors** : Valgrind memcheck is the definitive tool for finding use-after-free, buffer overflows, and uninitialized values.

  * **C/C++ heap profiling** : heaptrack for lower overhead than Valgrind, suitable for larger applications.

  * **Python memory analysis** : memray for high-resolution tracking and flamegraph visualization.

  * **Production C/C++** : jemalloc profiling for continuous heap monitoring with minimal overhead.

  * **Quick memory error detection** : GCC/Clang address sanitizer during development.




Start with the lowest-overhead tool for your language. For C/C++, use ASan during development and heaptrack for deeper analysis. For Python, memray is the best all-around choice. Reserve Valgrind for hard-to-find memory errors that simpler tools miss.

**See also:** [Performance Profiling: perf, Flamegraphs, py-spy, pprof](</en/tools/performance-profiling.html>), [Browser DevTools: Advanced Debugging Techniques](</en/tools/browser-devtools.html>), [Reverse Engineering Tools: Ghidra, IDA Free, radare2, Binary Ninja](</en/tools/reverse-engineering.html>).

**See also:** [Performance Profiling: perf, Flamegraphs, py-spy, pprof](</en/tools/performance-profiling.html>), [Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide](</en/tools/networking-tools.html>), [Command-Line Productivity: fzf, ripgrep, jq, bat, tmux, zoxide, and lazygit](</en/tools/command-line-productivity.html>)

**See also:** [Performance Profiling: perf, Flamegraphs, py-spy, pprof](</en/tools/performance-profiling.html>), [Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide](</en/tools/networking-tools.html>), [Command-Line Productivity: fzf, ripgrep, jq, bat, tmux, zoxide, and lazygit](</en/tools/command-line-productivity.html>)

**See also:** [Performance Profiling: perf, Flamegraphs, py-spy, pprof](</en/tools/performance-profiling.html>), [Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide](</en/tools/networking-tools.html>), [Command-Line Productivity: fzf, ripgrep, jq, bat, tmux, zoxide, and lazygit](</en/tools/command-line-productivity.html>)

**See also:** [Performance Profiling: perf, Flamegraphs, py-spy, pprof](</en/tools/performance-profiling.html>), [Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide](</en/tools/networking-tools.html>), [Command-Line Productivity: fzf, ripgrep, jq, bat, tmux, zoxide, and lazygit](</en/tools/command-line-productivity.html>)

**See also:** [Performance Profiling: perf, Flamegraphs, py-spy, pprof](</en/tools/performance-profiling.html>), [Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide](</en/tools/networking-tools.html>), [Command-Line Productivity: fzf, ripgrep, jq, bat, tmux, zoxide, and lazygit](</en/tools/command-line-productivity.html>)

**See also:** [Reverse Engineering Tools: Ghidra, IDA Free, radare2, Binary Ninja](</en/tools/reverse-engineering.html>), [Browser DevTools: Advanced Debugging Techniques](</en/tools/browser-devtools.html>), [API Development Tools: Postman, Insomnia, Bruno, Hoppscotch, and Swagger UI](</en/tools/api-development-tools.html>)

**See also:** [Reverse Engineering Tools: Ghidra, IDA Free, radare2, Binary Ninja](</en/tools/reverse-engineering.html>), [Browser DevTools: Advanced Debugging Techniques](</en/tools/browser-devtools.html>), [API Development Tools: Postman, Insomnia, Bruno, Hoppscotch, and Swagger UI](</en/tools/api-development-tools.html>)

**See also:** [Reverse Engineering Tools: Ghidra, IDA Free, radare2, Binary Ninja](</en/tools/reverse-engineering.html>), [Browser DevTools: Advanced Debugging Techniques](</en/tools/browser-devtools.html>), [API Development Tools: Postman, Insomnia, Bruno, Hoppscotch, and Swagger UI](</en/tools/api-development-tools.html>)

**See also:** [Reverse Engineering Tools: Ghidra, IDA Free, radare2, Binary Ninja](</en/tools/reverse-engineering.html>), [Browser DevTools: Advanced Debugging Techniques](</en/tools/browser-devtools.html>), [API Development Tools: Postman, Insomnia, Bruno, Hoppscotch, and Swagger UI](</en/tools/api-development-tools.html>)

**See also:** [Reverse Engineering Tools: Ghidra, IDA Free, radare2, Binary Ninja](</en/tools/reverse-engineering.html>), [Browser DevTools: Advanced Debugging Techniques](</en/tools/browser-devtools.html>), [API Development Tools: Postman, Insomnia, Bruno, Hoppscotch, and Swagger UI](</en/tools/api-development-tools.html>)

**See also:** [Reverse Engineering Tools: Ghidra, IDA Free, radare2, Binary Ninja](</en/tools/reverse-engineering.html>), [Browser DevTools: Advanced Debugging Techniques](</en/tools/browser-devtools.html>), [API Development Tools: Postman, Insomnia, Bruno, Hoppscotch, and Swagger UI](</en/tools/api-development-tools.html>)
