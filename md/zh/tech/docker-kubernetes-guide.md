---
title: "Docker与Kubernetes入门实战"
description: "从零开始学习容器化技术与容器编排，涵盖Docker基础操作、镜像构建、Kubernetes集群部署与日常运维管理实践。"
date: 2026-05-11
board: zh/tech
url: https://dingjiu1989-hue.github.io/zh/tech/docker-kubernetes-guide.html
---

## Docker基础概念

Docker通过容器技术实现应用的轻量级虚拟化。镜像（Image）是只读的模板，容器（Container）是镜像的运行实例，仓库（Registry）用于存储和分发镜像。理解这三者的关系是掌握Docker的第一步。

## Dockerfile编写技巧

编写高效的Dockerfile需要注意多阶段构建（Multi-stage Build）。第一阶段用于编译代码，包含完整的构建工具链；第二阶段仅包含运行环境，将编译产物复制过去，最终镜像体积可以减少数倍。

**最佳实践**：利用层缓存机制，将不常变化的依赖安装命令放在前面，频繁变化的源代码复制放在后面。使用.dockerignore文件排除不必要的文件，进一步减小镜像体积。基础镜像优先选择Alpine或Distroless版本。

## Docker Compose编排

单机多容器场景使用Docker Compose管理。编写docker-compose.yml文件定义服务、网络和卷。典型配置包括Web服务、数据库、缓存和消息队列的组合。使用环境变量文件管理不同环境的配置差异。

## Kubernetes核心概念

K8s解决了容器编排的关键问题：服务发现与负载均衡、自动伸缩、自愈能力和滚动更新。核心资源包括Pod（最小部署单元）、Service（网络访问入口）、Deployment（声明式更新）和ConfigMap（配置管理）。

## 集群搭建入门

学习阶段推荐使用Minikube或Kind在本地搭建单节点集群。生产环境则可以选择云服务商提供的托管K8s服务，如阿里云ACK或AWS EKS。

**命名空间管理**：使用Namespace实现多环境隔离。每个项目或团队使用独立的命名空间，配合ResourceQuota限制资源使用，避免相互影响。

**Ingress配置**：集群外部流量通过Ingress控制器路由到内部服务。推荐使用Nginx Ingress Controller或Traefik，配置TLS证书、路径重写和流量分割规则。

## 日常运维要点

Pod健康状况检查配置Liveness和Readiness探针，确保流量只路由到正常工作的实例。资源限制方面，为每个容器设置requests和limits，避免资源争抢。日志收集建议使用EFK（Elasticsearch+Fluentd+Kibana）或Loki+Promtail方案集中管理。

监控与告警使用Prometheus采集指标，Grafana可视化展示。设置核心指标的告警规则，包括Pod重启次数、CPU和内存使用率超过阈值等情况。
