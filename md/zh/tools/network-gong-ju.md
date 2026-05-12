---
title: "网络诊断工具：Wireshark、tcpdump、nmap实战使用"
description: "系统讲解三大网络诊断工具——Wireshark、tcpdump和nmap的实战用法，从抓包分析到网络扫描，覆盖常见的网络排查场景。"
date: 2026-05-12
board: tools
url: https://dingjiu1989-hue.github.io/zh/tools/network-gong-ju.html
---

## 网络诊断的重要性

网络问题是后端开发和运维中最常见也最难排查的问题之一。掌握网络诊断工具是每个技术人员的必备技能。

## Wireshark：图形化协议分析

Wireshark是最强大的网络协议分析工具，支持数百种协议的深度解析。

### 核心功能
- 实时抓包和离线分析
- 强大的显示过滤器
- 协议深度解析
- 流量统计和IO图
- 跟踪TCP流

### 常用过滤器

```bash
# 只显示特定IP的流量
ip.addr == 192.168.1.100

# 只显示HTTP流量
http

# 显示特定端口的TCP流量
tcp.port == 443

# 显示DNS查询
dns

# 组合过滤
http and ip.src == 192.168.1.1
```

### 实战场景

**分析API调用延迟：**
1. 抓取调用API期间的网络包
2. 使用HTTP过滤器定位相关请求
3. 查看TCP握手时间和请求响应间隔
4. 分析是否存在DNS解析慢、连接复用等问题

**定位连接重置：**
显示过滤器输入`tcp.flags.reset == 1`，快速定位RST包，分析连接被重置的原因。

## tcpdump：命令行抓包利器

tcpdump是服务器环境中最常用的命令行抓包工具。

### 基本用法

```bash
# 抓取eth0接口上的所有流量
tcpdump -i eth0

# 抓取特定端口的流量，保存到文件
tcpdump -i eth0 port 80 -w capture.pcap

# 抓取并显示包内容（ASCII）
tcpdump -i eth0 -A port 443

# 限制抓取数量
tcpdump -i eth0 -c 100
```

### 实战技巧

**抓取HTTP请求和响应：**
```bash
tcpdump -i eth0 -A -s 0 'tcp port 80 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)'
```

**监控特定IP的流量：**
```bash
tcpdump host 10.0.0.1 and not port 22
```

**后台持续抓取：**
```bash
nohup tcpdump -i eth0 -w /tmp/capture.pcap -G 3600 -W 24 &
```

## nmap：网络扫描工具

nmap用于主机发现、端口扫描和服务探测。

### 常用扫描类型

```bash
# 快速扫描常见端口
nmap -F target.com

# 全面扫描（操作系统+服务版本）
nmap -A target.com

# 扫描特定端口范围
nmap -p 1-1000 192.168.1.1

# 子网扫描
nmap -sP 192.168.1.0/24
```

### 实战场景

**排查端口不可达问题：**
```bash
# 检查目标服务器端口是否开放
nmap -p 8080 target-server.com
```

**发现网络中的设备：**
```bash
# 发现局域网中的活跃设备
nmap -sn 192.168.1.0/24
```

## 工具组合使用

在实际排查中，三种工具通常组合使用：

1. **nmap**发现目标开放的端口和服务
2. **tcpdump**抓取特定流量的原始包
3. **Wireshark**分析抓取到的pcap文件

掌握这些网络诊断工具，可以高效定位从TCP连接问题到应用层协议的各类网络故障。
