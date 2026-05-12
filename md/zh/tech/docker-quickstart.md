---
title: "Docker 30 分钟入门：从安装到第一个容器"
description: "零基础 Docker 入门教程，30 分钟掌握镜像、容器、Dockerfile 核心概念，亲手构建并运行你的第一个容器化应用。"
date: 2026-05-12
board: tech
url: https://dingjiu1989-hue.github.io/zh/tech/docker-quickstart.html
---

# Docker 30 分钟入门：从安装到第一个容器

Docker 是现代开发者的必备技能。这篇文章用最通俗的语言带你 30 分钟上手。 为什么需要 Docker

  * **环境一致性** — "我电脑上能跑啊" 从此成为历史。开发、测试、生产环境完全一致。
  * **快速部署** — 一条命令启动完整环境，不用装数据库、配环境变量。
  * **资源隔离** — 每个项目独立运行，不互相干扰。

核心概念三件套 概念| 比喻| 说明  
---|---|---  
镜像 (Image)| 系统安装盘| 只读模板，包含运行应用所需的一切  
容器 (Container)| 运行中的虚拟机| 镜像的运行实例，相互隔离  
Dockerfile| 安装说明书| 定义如何构建镜像的文本文件  
安装 Docker macOS 用户推荐 [OrbStack](<https://orbstack.dev/>)（轻量替代 Docker Desktop），或直接 `brew install docker`。Windows/Linux 用户去 docker.com 下载即可。 第一个容器

    # 拉取并运行 nginx
    docker run -d -p 8080:80 --name my-nginx nginx

    # 浏览器打开 http://localhost:8080 就能看到 nginx 欢迎页

写一个 Dockerfile

    FROM python:3.12-slim
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install -r requirements.txt
    COPY . .
    EXPOSE 8000
    CMD ["python", "app.py"]

常用命令速查 `docker ps`| 查看运行中的容器  
---|---  
`docker images`| 查看本地镜像  
`docker build -t name .`| 构建镜像  
`docker exec -it name bash`| 进入容器 shell  
`docker-compose up -d`| 启动多容器应用  
下一步 掌握这些就可以开始在工作中使用 Docker 了。推荐下一步学习 docker-compose 多容器编排和 Docker Hub 镜像仓库。 📖 相关推荐

  * [Git 进阶：交互式 rebase、cherry-pick 和 bisect 实战](<https://dingjiu1989-hue.github.io/zh/tech/git-advanced.html>)
  * [单元测试入门：从零到写出第一个可维护的测试](<https://dingjiu1989-hue.github.io/zh/tech/unit-testing-guide.html>)
  * [REST API 设计最佳实践：写出让人愿意用的接口](<https://dingjiu1989-hue.github.io/zh/tech/rest-api-best-practices.html>)

**See also:** [Git 进阶：交互式 rebase、cherry-pick 和 bisect 实战](</zh/tech/git-advanced.html>), [单元测试入门：从零到写出第一个可维护的测试](</zh/tech/unit-testing-guide.html>), [REST API 设计最佳实践：写出让人愿意用的接口](</zh/tech/rest-api-best-practices.html>).
