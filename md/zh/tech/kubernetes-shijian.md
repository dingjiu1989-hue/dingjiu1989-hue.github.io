---
title: "Kubernetes实战：Pod部署、服务发现、自动伸缩"
description: "深入讲解Kubernetes的核心实战技能，包括Pod管理与调度、Service服务发现机制、HPA自动伸缩配置和生产集群运维经验。"
date: 2026-05-12
board: tech
url: https://dingjiu1989-hue.github.io/zh/tech/kubernetes-shijian.html
---

## Kubernetes核心组件

Kubernetes是目前最主流的容器编排平台。理解其核心组件是掌握K8s的第一步：Pod是最小部署单元，Service提供网络抽象，Deployment管理副本，Ingress处理外部流量。

## Pod管理与调度

Pod是K8s中最基本的计算单元，可以包含一个或多个容器。

### Pod设计模式

- **Sidecar模式**：主容器+辅助容器（如日志收集、代理）
- **Init容器**：在主容器启动前执行初始化任务
- **Adapters**：将不同应用的输出标准化

### 资源管理

合理设置资源请求和限制是保证集群稳定的关键：

```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "500m"
  limits:
    memory: "512Mi"
    cpu: "1000m"
```

### 调度策略

- **节点选择器**：将Pod调度到特定标签的节点
- **节点亲和性**：更灵活的节点选择规则
- **Pod亲和性/反亲和性**：控制Pod之间的分布关系

## 服务发现

K8s中的服务发现通过Service和DNS实现。

### Service类型

- **ClusterIP**：集群内部访问，默认类型
- **NodePort**：通过节点IP和端口访问
- **LoadBalancer**：云平台负载均衡器
- **ExternalName**：外部服务的DNS别名

### Ingress控制器

Ingress负责将外部HTTP/HTTPS流量路由到集群内部服务：

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
spec:
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
```

## 自动伸缩

### HPA（水平Pod自动伸缩）

基于CPU、内存或自定义指标自动调整Pod数量：

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## 生产环境运维

### 监控与日志

- **Metrics Server**：基础资源指标收集
- **Prometheus + Grafana**：全面监控方案
- **EFK/PLG**：日志收集和分析

### 安全最佳实践

- 使用RBAC控制访问权限
- 启用NetworkPolicy隔离网络
- 使用PodSecurityAdmission限制Pod权限
- 定期更新集群版本和节点镜像

### 故障排查

常用命令：`kubectl describe`查看资源详情，`kubectl logs`查看Pod日志，`kubectl exec`进入容器调试，`kubectl top`查看资源使用情况。

掌握这些核心实践，能够帮助团队构建稳定、可扩展的Kubernetes生产集群。
