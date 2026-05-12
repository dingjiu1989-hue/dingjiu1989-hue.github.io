---
title: "CI/CD流水线设计：GitHub Actions从入门到生产级配置"
description: "系统讲解CI/CD流水线的设计原则和GitHub Actions的实战配置，涵盖工作流编写、缓存优化、安全扫描和生产部署的最佳实践。"
date: 2026-05-12
board: tech
url: https://dingjiu1989-hue.github.io/zh/tech/ci-cd-liu-cheng.html
---

## CI/CD核心原则

持续集成和持续部署是现代软件工程的核心实践。好的CI/CD流水线应遵循：快速反馈、可靠性优先、安全左移和环境一致性。

## GitHub Actions基础

GitHub Actions使用YAML定义工作流，核心概念包括Workflow、Job、Step和Action。

### 基础工作流

```yaml
name: CI Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm test
```

## 构建优化

### 缓存策略

合理缓存依赖可以显著减少构建时间：

```yaml
- uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

### 矩阵构建

并行测试多个版本和平台：

```yaml
strategy:
  matrix:
    node-version: [18, 20, 22]
    os: [ubuntu-latest, windows-latest]
```

## 安全集成

### 代码质量与安全

- **Lint检查**：ESLint、Pylint等
- **SAST扫描**：CodeQL、SonarQube
- **依赖扫描**：Dependabot、Snyk
- **密钥检测**：防止硬编码密钥泄露

### 容器安全

构建镜像后自动扫描漏洞：

```yaml
- name: Build and scan Docker image
  run: |
    docker build -t myapp:${{ github.sha }} .
    trivy image myapp:${{ github.sha }}
```

## 部署策略

### 环境分离

```
开发分支 → 自动部署到dev环境
功能分支 → 预览环境（PR触发）
主分支 → 自动部署到staging → 手动审批 → 生产环境
```

### 金丝雀发布

通过GitHub Actions的部署环境功能实现逐步发布：

```yaml
environment:
  name: production
  url: https://myapp.com

# 分阶段发布
- name: Deploy 10% traffic
  run: ./deploy-canary.sh 10
- name: Wait for health check
  run: ./wait-for-health.sh
- name: Deploy 100%
  run: ./deploy-full.sh
```

## 生产级配置示例

### 一个完整的CI/CD流程

1. **代码提交**触发CI流水线
2. 并行运行lint、测试、构建
3. 测试通过后构建Docker镜像
4. 镜像安全扫描
5. 推送到容器仓库
6. 自动部署到预发布环境
7. 集成测试
8. 手动审批后部署到生产环境
9. 部署后监控

### 状态通知

集成Slack、邮件或飞书通知构建状态：

```yaml
- name: Notify on failure
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    payload: '{"text": "构建失败: ${{ github.repository }}"}'
```

设计良好的CI/CD流水线是团队高效交付的基石，值得投入时间持续优化。
