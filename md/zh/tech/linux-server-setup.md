---
title: "Linux服务器初始化配置"
description: "新服务器到手后的标准操作流程，包括系统更新、安全加固、SSH配置、防火墙设置以及开发环境搭建等关键步骤。"
date: 2026-05-11
board: zh/tech
url: https://dingjiu1989-hue.github.io/zh/tech/linux-server-setup.html
---

## 初始登录与系统更新

拿到新服务器后的第一件事是更新系统。使用`apt update && apt upgrade -y`（Debian/Ubuntu）或`yum update`（CentOS/RHEL）将所有软件包更新到最新版本。安装必要的工具集：curl、wget、vim、git、htop、net-tools等。

## SSH安全加固

SSH是服务器的首要攻击入口，必须进行加固。第一步，修改默认端口22为高位端口（如2222），减少自动化扫描攻击。第二步，禁用root密码登录，使用密钥认证。编辑`/etc/ssh/sshd_config`设置`PasswordAuthentication no`和`PermitRootLogin prohibit-password`。

**密钥管理**：生成ED25519类型密钥对，相比RSA更安全且性能更好。将公钥添加到`~/.ssh/authorized_keys`，私钥保存在本地并设置600权限。多个团队成员使用时，每个成员添加独立的公钥，便于权限回收。

## 防火墙配置

使用iptables或ufw配置防火墙规则。基础策略为默认拒绝入站流量，仅放行必要端口。SSH端口、Web服务（80/443）和运维端口按需开启。

高级配置包括IP白名单（仅允许公司IP访问SSH）、连接频率限制以及端口敲门（Port Knocking）机制。使用fail2ban工具自动封禁多次登录失败的IP地址。

## 用户与权限管理

遵循最小权限原则。创建普通用户用于日常操作，仅在需要时使用sudo提权。配置sudoers文件时指定具体可执行的命令，避免ALL权限溢出。

示例配置：`deploy ALL=(ALL) /usr/bin/systemctl, /usr/bin/journalctl`限制部署用户只能管理系统服务和查看日志。

## 系统监控与日志

安装系统监控工具：使用netdata或Prometheus Node Exporter采集系统指标，包括CPU使用率、内存占用、磁盘IO和网络流量。配置日志轮转（logrotate）避免日志文件撑满磁盘。

**关键指标**：设置磁盘使用率超过80%自动告警，内存交换分区使用异常时通知运维。使用sysstat工具包采集历史性能数据，便于回溯分析。

## 开发环境搭建

根据项目需求安装运行时环境。Node.js推荐使用nvm管理多版本；Python使用pyenv或conda管理虚拟环境；Go直接从官网下载二进制包。使用Docker部署应用时，安装Docker CE并配置非root用户运行权限。

所有配置操作建议使用Ansible或Shell脚本实现自动化，确保每次搭建新服务器的流程一致且可重复。将配置脚本纳入版本管理，环境变更应有完整的审计记录。
