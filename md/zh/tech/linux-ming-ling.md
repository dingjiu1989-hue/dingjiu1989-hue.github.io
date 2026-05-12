---
title: "Linux运维必备命令：性能分析、日志排查、网络诊断"
description: "系统梳理Linux运维中最实用的命令，涵盖系统性能分析、日志排查技巧、网络诊断方法和文件操作的实战经验。"
date: 2026-05-12
board: tech
url: https://dingjiu1989-hue.github.io/zh/tech/linux-ming-ling.html
---

## 系统性能分析

### CPU分析

- **top/htop**：实时查看进程CPU占用，按P键按CPU降序排列
- **mpstat -P ALL 1**：查看每个CPU核心的使用率
- **pidstat -p PID 1**：监控特定进程的CPU使用
- **perf top**：查看CPU热点函数，定位性能瓶颈

排查CPU问题的典型流程：先用top找到高CPU进程，再用perf top定位热点函数，最后分析代码优化。

### 内存分析

- **free -h**：查看系统内存使用概况
- **vmstat 1**：监控内存、交换分区和IO状态
- **smem**：查看进程实际物理内存使用
- **/proc/meminfo**：内存详细指标

当发现Swap使用率上升时，说明物理内存可能不足，需要排查内存泄漏或增加内存容量。

### 磁盘IO分析

- **iostat -x 1**：查看磁盘IOPS、吞吐量和等待时间
- **iotop**：实时查看进程IO使用
- **df -h**：查看磁盘空间使用
- **du -sh ***：查看当前目录下各文件/目录大小

## 日志排查

### 日志查看

- **journalctl -u nginx --since "1 hour ago"**：查看特定服务的近期日志
- **tail -f /var/log/syslog | grep ERROR**：实时跟踪错误日志
- **less +F /var/log/app.log**：类似tail -f但支持查看历史
- **awk '/ERROR/{print}' app.log | sort | uniq -c**：统计错误类型

### 日志分析技巧

使用组合命令快速定位问题：

```bash
# 统计最近5分钟的错误数
grep "$(date -d '5 min ago' '+%H:%M')" app.log | grep ERROR | wc -l

# 找出出现最频繁的IP
awk '{print $1}' access.log | sort | uniq -c | sort -nr | head -10

# 提取两个时间戳之间的日志
sed -n '/2026-05-12 10:00/,/2026-05-12 11:00/p' app.log
```

## 网络诊断

### 连接检查

- **ping**：基础连通性测试
- **traceroute**：路由路径追踪
- **ss -tuln**：查看监听端口
- **netstat -anp**：查看所有连接状态

### 带宽分析

- **nload**：实时查看网络带宽
- **iftop**：查看进程级别的网络流量
- **nethogs**：按进程排序的网络流量监控

### DNS排查

- **dig example.com**：DNS查询详细信息
- **nslookup example.com**：快速DNS查询
- **host example.com**：简单的IP查询

## 常用组合技巧

```bash
# 查找大文件
find / -type f -size +100M -exec ls -lh {} \;

# 杀死僵尸进程
ps aux | grep Z | awk '{print $2}' | xargs kill -9

# 实时追踪系统调用
strace -p PID -e trace=network

# 批量替换文本
find . -name "*.conf" -exec sed -i 's/old/new/g' {} \;
```

掌握这些命令能帮助运维人员在日常工作中快速定位和解决问题，提升系统稳定性。
