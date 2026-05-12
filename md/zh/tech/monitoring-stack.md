---
title: "监控体系搭建：Prometheus + Grafana + Alertmanager"
description: "系统讲解从零搭建Prometheus+Grafana+Alertmanager监控体系，涵盖指标收集、可视化面板设计、告警规则配置和故障自愈的完整实践。"
date: 2026-05-12
board: tech
url: https://dingjiu1989-hue.github.io/zh/tech/monitoring-stack.html
---

## 监控体系概述

一个完整的监控体系需要覆盖四个层次：基础设施监控、应用性能监控、业务指标监控和用户体验监控。Prometheus + Grafana + Alertmanager是目前最流行的开源监控方案组合。

## Prometheus指标收集

### 架构原理

Prometheus采用拉模式（Pull）采集指标，每个被监控的目标暴露HTTP端点，Prometheus定期拉取数据。

### 核心概念

**Metric类型：**
- **Counter**：只增不减的计数器，适合请求数、错误数
- **Gauge**：可增可减的度量，适合内存使用、连接数
- **Histogram**：分桶直方图，适合请求延迟分布
- **Summary**：分位数统计，类似Histogram但客户端计算

### 指标暴露

在应用中集成Prometheus客户端库：

```python
from prometheus_client import Counter, Histogram, generate_latest

REQUEST_COUNT = Counter('http_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'Request duration', ['method'])

@app.route('/api/users')
def get_users():
    REQUEST_COUNT.labels(method='GET', endpoint='/api/users').inc()
    with REQUEST_DURATION.labels(method='GET').time():
        return get_users_from_db()
```

## Grafana可视化

### 数据源配置

Grafana支持Prometheus、InfluxDB、Elasticsearch等多种数据源。配置Prometheus数据源后即可创建仪表盘。

### 面板设计原则

1. **黄金信号**：延迟、流量、错误数、饱和度
2. **USE方法**：使用率、饱和度、错误率（资源视角）
3. **RED方法**：请求速率、错误数、持续时间（服务视角）

### 常用面板示例

**系统概览面板：**
```
CPU使用率: 100 - (avg by(instance)(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
内存使用率: (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100
磁盘IO: rate(node_disk_io_time_seconds_total[5m])
网络流量: rate(node_network_receive_bytes_total[5m])
```

## Alertmanager告警

### 告警规则配置

```yaml
groups:
- name: server_alerts
  rules:
  - alert: HighCPUUsage
    expr: 100 - (avg by(instance)(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "实例 {{ $labels.instance }} CPU使用率超过80%"
      description: "CPU使用率当前为 {{ $value }}%"

  - alert: DiskSpaceLow
    expr: (node_filesystem_avail_bytes / node_filesystem_size_bytes) < 0.1
    for: 2m
    labels:
      severity: critical
    annotations:
      summary: "{{ $labels.instance }} 磁盘空间不足"
```

### 告警路由与通知

```yaml
route:
  receiver: 'team-ops'
  routes:
  - match:
      severity: critical
    receiver: 'team-ops-critical'
    repeat_interval: 5m

receivers:
- name: 'team-ops-critical'
  webhook_configs:
  - url: 'https://hooks.example.com/alert'
```

## 告警管理最佳实践

1. **减少告警噪音**：避免过度告警，关注真正需要人工介入的事件
2. **设置合理的告警级别**：Warning（关注）和Critical（立即处理）
3. **定义SLA/SLO**：基于服务等级目标设置告警阈值
4. **告警自愈**：对常见问题配置自动化修复脚本
5. **告警升级机制**：长时间未处理逐级升级通知

## 实战架构

```
应用/服务器 → Exporter(节点指标) → Prometheus(存储+查询)
                                       ↓
                                  Alertmanager → 通知(飞书/Slack/邮件)
                                       ↓
                                  Grafana(可视化 + 告警管理)
```

完善的监控体系是保障系统稳定性的基础，能够在问题影响用户之前及时发现和处理。
