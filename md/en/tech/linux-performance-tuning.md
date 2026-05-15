---
title: "Linux Performance Tuning"
description: "Practical techniques for optimizing Linux system performance, from kernel parameters to storage I/O tuning."
date: 2026-05-11
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/linux-performance-tuning.html
---

# Linux Performance Tuning

## Linux Performance Tuning

## Linux Performance Tuning

## Linux Performance Tuning

## Linux Performance Tuning

## Linux Performance Tuning

## Linux Performance Tuning

## Linux Performance Tuning

## Linux Performance Tuning

## Linux Performance Tuning

## Linux Performance Tuning

## Linux Performance Tuning

## Linux Performance Tuning

## Linux Performance Tuning

## Linux Performance Tuning

Linux performance tuning is essential for running efficient production workloads. Understanding how the kernel manages CPU, memory, disk, and network resources allows you to identify bottlenecks and optimize accordingly.

### The USE Method

Brendan Gregg's USE (Utilization, Saturation, Errors) method provides a systematic approach to performance analysis:

  * **Utilization** : What percentage of the resource is busy?

  * **Saturation** : How much extra work is queued?

  * **Errors** : How many error events are there?




Apply this to CPU, memory, storage, and network resources to quickly identify the bottleneck.

### CPU Performance Tuning

#### Monitoring Tools

## Real-time CPU monitoring

htop

## Per-process CPU usage

top -o %CPU

## CPU statistics and context switches

vmstat 1 5

## Detailed per-CPU utilization

mpstat -P ALL 1

High context switch rates (above 50,000 per second per core) may indicate inefficient application architecture. Use `pidstat -w` to identify processes causing excessive context switches.

#### Kernel Parameters

## cat /etc/sysctl.d/99-performance.conf

kernel.sched_min_granularity_ns = 3000000

kernel.sched_wakeup_granularity_ns = 4000000

kernel.sched_migration_cost_ns = 500000

kernel.sched_nr_migrate = 32

These scheduler parameters reduce latency for interactive workloads. Adjust carefully -- aggressive settings can hurt throughput.

### Memory Tuning

#### Monitoring Memory

## Memory usage overview

free -h

## Detailed memory breakdown

cat /proc/meminfo

## Page fault statistics

sar -B 1

## Top memory consumers

ps aux --sort=-%mem | head

Check `sar -B` for page fault rates. High `pgmajfault` values indicate the system is swapping -- add more RAM or reduce memory pressure.

#### Swappiness

## Reduce swapping tendency (default is 60)

vm.swappiness = 10

## Set temporarily

sysctl vm.swappiness=10

For database servers, set swappiness to 1 to avoid swapping. For desktops and general-purpose servers, 10-20 balances responsiveness with memory efficiency.

#### Transparent Huge Pages

Disable THP for database workloads:

echo never > /sys/kernel/mm/transparent_hugepage/enabled

echo never > /sys/kernel/mm/transparent_hugepage/defrag

THP can cause latency spikes in database systems due to memory defragmentation pauses.

### Disk I/O Tuning

#### I/O Scheduler

Choose the right I/O scheduler for your workload:

## Check current scheduler

cat /sys/block/nvme0n1/queue/scheduler

## Set to none for NVMe, mq-deadline for spinning disks

echo none > /sys/block/nvme0n1/queue/scheduler

Modern NVMe drives perform best with the `none` (or `nvme`) scheduler. Spinning disks benefit from `mq-deadline` which minimizes seek times.

#### Monitoring Disk Performance

## I/O statistics per device

iostat -x 1

## Process-level I/O

iotop

## File system latency

bcc-tools/biolatency

High `await` times (above 20ms) indicate disk saturation. Check `iowait` in `top` and `svctm` in `iostat` for confirmation.

### Network Tuning

#### Kernel Network Parameters

## /etc/sysctl.d/99-network.conf

net.core.somaxconn = 65535

net.core.netdev_max_backlog = 50000

net.ipv4.tcp_tw_reuse = 1

net.ipv4.tcp_fin_timeout = 15

net.ipv4.tcp_keepalive_time = 300

net.ipv4.tcp_keepalive_intvl = 60

net.ipv4.tcp_keepalive_probes = 5

net.core.rmem_max = 134217728

net.core.wmem_max = 134217728

net.ipv4.tcp_rmem = 4096 87380 134217728

net.ipv4.tcp_wmem = 4096 65536 134217728

Increase socket buffer sizes for high-throughput applications. `tcp_tw_reuse` allows reuse of connections in TIME_WAIT state, important for high-connection-rate servers.

#### Network Monitoring

## Per-interface statistics

sar -n DEV 1

## Socket statistics

ss -s

## Connection tracking

netstat -s | grep -i "connections established"

Monitor for dropped packets in `/proc/net/softnet_stat` and TCP retransmits with `netstat -s | grep retransmit`.

### File System Tuning

#### Mount Options

Optimize filesystem mount options for performance:

## /etc/fstab

/dev/sda1 / ext4 noatime,nodiratime,data=ordered 0 0

The `noatime` option eliminates update timestamps on every file read, significantly reducing disk writes. Use `nodiratime` for directories.

#### I/O Limits with cgroups

Control per-process I/O with cgroups v2:

## Limit read/write to 50 MB/s

echo "8:0 rbps=52428800 wbps=52428800" > /sys/fs/cgroup//io.max

### Application-Level Tuning

Profile before tuning. Use `perf` for CPU profiling, `flamegraphs` for visualization, and `strace` for system call analysis:

## Sample CPU stacks at 99Hz

perf record -F 99 -a -g -- sleep 30

perf script | ./stackcollapse-perf.pl | ./flamegraph.pl > profile.svg

Always measure before and after changes. A single benchmark run is unreliable -- run multiple iterations and report the median.

### Summary

Linux performance tuning is a systematic process of identifying bottlenecks, applying targeted optimizations, and measuring the impact. Start with the USE method to find the bottleneck, use the right monitoring tools, and tune one parameter at a time. Common wins include setting the correct I/O scheduler, reducing swappiness for databases, disabling THP, and increasing network buffer sizes. Profile first, tune second, and always validate with benchmarks.

**See also:** [Git Workflows for Teams](</en/tech/git-workflows-2026.html>), [Microservices Communication Patterns](</en/tech/microservices-communication.html>), [Webpack vs Vite Comparison](</en/tech/webpack-vs-vite-bundlers.html>).

**See also:** [Git Workflows for Teams](</en/tech/git-workflows-2026.html>), [Microservices Communication Patterns](</en/tech/microservices-communication.html>), [Nginx Configuration Guide](</en/tech/nginx-configuration-guide.html>)

**See also:** [Git Workflows for Teams](</en/tech/git-workflows-2026.html>), [Microservices Communication Patterns](</en/tech/microservices-communication.html>), [Nginx Configuration Guide](</en/tech/nginx-configuration-guide.html>)
