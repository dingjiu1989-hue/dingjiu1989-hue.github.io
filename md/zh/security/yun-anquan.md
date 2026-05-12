---
title: "云安全基础：IAM策略、网络安全组、加密配置最佳实践"
description: "系统讲解云计算环境的安全配置最佳实践，涵盖IAM身份与访问管理、VPC网络安全组配置和数据加密策略的核心要点。"
date: 2026-05-12
board: security
url: https://dingjiu1989-hue.github.io/zh/security/yun-anquan.html
---

## 共享责任模型

云安全遵循共享责任模型：云服务商负责"云的安全"（基础设施、物理安全），用户负责"云中的安全"（数据、配置、访问控制）。

## IAM策略

IAM（身份与访问管理）是云安全的第一道防线。

### 最小权限原则

每个实体（用户、服务、角色）只授予完成其任务所需的最小权限集。

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::myapp-assets",
                "arn:aws:s3:::myapp-assets/*"
            ]
        }
    ]
}
```

**原则：** 拒绝所有，按需开放。定期审计未使用的权限。

### 角色而非用户

- 使用IAM Role而非长期Access Key
- 为EC2、Lambda等服务分配角色
- 使用临时凭证（STS）管理

### 权限边界

使用权限边界（Permissions Boundary）设置角色能获得的最高权限，防止权限提升。

## 网络安全组

### VPC隔离

- 将不同环境（开发、测试、生产）放在不同VPC中
- 使用VPC Peering或Transit Gateway连接VPC
- 敏感服务部署在私有子网中

### 安全组规则

```terraform
# 安全组最佳实践
resource "aws_security_group" "web" {
  name        = "web-sg"
  description = "Web服务器安全组"
  vpc_id      = aws_vpc.main.id

  # 入站规则：只允许80和443
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # 出站规则：限制出站流量
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

### NACL配置

网络ACL提供子网级别的状态无关过滤，作为安全组的补充。

## 加密配置

### 传输中加密

- 所有对外服务使用TLS 1.2+
- 内部服务间通讯使用mTLS
- RDS连接启用SSL/TLS

### 静态加密

**存储加密：**
```bash
# EBS加密
aws ec2 enable-ebs-encryption-by-default

# S3默认加密
aws s3api put-bucket-encryption \
  --bucket myapp-data \
  --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'
```

**密钥管理：**
- 使用KMS托管密钥
- 定期轮换密钥
- 区分客户主密钥和加密密钥

### 密钥轮换

自动轮换IAM访问密钥、数据库密码和加密密钥。使用AWS Secrets Manager或AWS Parameter Store管理敏感配置。

## 合规监控

### 配置审计

- **AWS Config**：持续监控资源配置变化
- **Security Hub**：安全状态聚合
- **GuardDuty**：威胁检测

### 合规扫描

```bash
# 使用Prowler进行云安全审计
prowler aws --checks extra-79 --checks extra-761
```

### 事件响应

1. 检测异常活动（GuardDuty发现异常API调用）
2. 自动隔离受影响资源（Lambda自动响应）
3. 取证分析（CloudTrail日志分析）
4. 恢复和加固

## 日常检查清单

- [ ] 是否有多余的开放端口（22、3306等）
- [ ] S3存储桶是否公开可访问
- [ ] IAM密钥是否定期轮换
- [ ] 是否启用了CloudTrail（操作审计）
- [ ] 是否有未使用的安全组规则
- [ ] 根账号是否启用了MFA

云安全需要持续的监控和优化，没有一劳永逸的解决方案。
