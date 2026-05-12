---
title: "Docker安全：镜像扫描、运行时安全、权限控制"
description: "系统讲解Docker容器安全的实践方案，涵盖镜像漏洞扫描、运行时安全配置、容器权限限制以及安全审计的完整指南。"
date: 2026-05-12
board: security
url: https://dingjiu1989-hue.github.io/zh/security/docker-anquan.html
---

## Docker安全威胁

容器化部署带来了新的安全挑战：镜像中的漏洞、容器逃逸风险、不安全的配置和权限过度开放是Docker安全的主要威胁。

## 镜像安全

### 选择可信基础镜像

- 优先使用官方镜像（Docker Official Images）
- 使用经过验证的发行版（Alpine、Distroless）
- 避免使用`latest`标签，指定精确版本

### 镜像扫描

在CI/CD流水线中集成镜像扫描：

```yaml
# CI/CD 中的镜像扫描
- name: Scan Docker image
  run: |
    trivy image myapp:latest
    # 或使用 Docker Scout
    docker scout quickview myapp:latest
```

**推荐工具：**
- **Trivy**：开源，支持多语言和操作系统漏洞
- **Snyk Container**：商业方案，深度集成
- **Docker Scout**：Docker官方安全工具
- **Grype**：Anchore开源扫描器

**扫描策略：**
- 每次构建都扫描
- 设阻断标准（如：不允许Critical级别漏洞）
- 定期扫描已部署的镜像

### 镜像最小化

```dockerfile
# 多阶段构建
FROM golang:1.22 AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o app

FROM scratch
COPY --from=builder /app/app /
ENTRYPOINT ["/app"]
```

最小的镜像意味着最小的攻击面。

## 运行时安全

### 容器运行时配置

```bash
docker run \
  --read-only \                    # 只读文件系统
  --cap-drop=ALL \                 # 删除所有Linux能力
  --cap-add=NET_BIND_SERVICE \     # 只添加必要能力
  --security-opt=no-new-privileges \ # 禁止提权
  --security-opt seccomp=policy.json \ # seccomp策略
  myapp
```

### Docker Compose安全配置

```yaml
services:
  app:
    image: myapp
    read_only: true
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    security_opt:
      - no-new-privileges:true
    restart: unless-stopped
```

### 非root用户运行

```dockerfile
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
```

## 权限控制

### 容器权限最小化

**Linux Capabilities管理：**
默认情况下，Docker容器拥有部分Linux Capabilities。应删除所有不必要的Capabilities。

```
需要网络：cap_add NET_BIND_SERVICE, NET_RAW
需要时间：cap_add SYS_TIME
不需要：全部drop
```

### 资源限制

```bash
docker run \
  --memory="512m" \         # 内存限制
  --cpus="0.5" \             # CPU限制
  --pids-limit=100 \         # 进程数限制
  --ulimit nofile=1024:2048  # 文件描述符限制
  myapp
```

### Docker Socket安全

千万不要将`/var/run/docker.sock`挂载到容器中——这等于给了容器主机的root权限。如果确实需要管理Docker，使用Docker API的远程访问并配置TLS。

## 安全审计

### Docker Bench Security

运行Docker Bench Security进行安全基线检查：

```bash
docker run --it --net host --pid host \
  -v /etc:/etc:ro \
  -v /var:/var:ro \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  docker/docker-bench-security
```

该工具对照CIS Docker Benchmark检查配置项。

### 日志审计

- 启用Docker的审计日志
- 监控容器异常行为
- 记录所有镜像拉取和容器启动事件

## 最佳实践清单

- [ ] 使用受信任的基础镜像
- [ ] 定期扫描镜像漏洞
- [ ] 最小化镜像体积
- [ ] 以非root用户运行容器
- [ ] 删除不必要的Linux Capabilities
- [ ] 设置文件系统为只读
- [ ] 限制资源使用
- [ ] 不挂载Docker Socket
- [ ] 使用Seccomp和AppArmor配置
- [ ] 定期运行安全基准检查

容器安全需要在镜像构建、运行配置和运维管理每个环节都加以重视。
