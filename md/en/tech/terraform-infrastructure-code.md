---
title: "Terraform Infrastructure as Code"
description: "Master Terraform for managing cloud infrastructure with state management, modules, and production best practices."
date: 2025-12-03
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/terraform-infrastructure-code.html
---

# Terraform Infrastructure as Code

Terraform has become the standard tool for Infrastructure as Code (IaC). It allows you to define, provision, and manage cloud resources across providers using declarative configuration. This guide covers practical Terraform patterns for production use.

## Core Concepts

Terraform uses a declarative approach -- you describe the desired state, and Terraform figures out how to reach it:

## main.tf

terraform {

required_version = ">= 1.8"

required_providers {

aws = {

source = "hashicorp/aws"

version = "~> 5.0"

}

}

backend "s3" {

bucket = "myapp-terraform-state"

key = "production/terraform.tfstate"

region = "us-east-1"

}

}

provider "aws" {

region = var.aws_region

}

resource "aws_s3_bucket" "app_data" {

bucket = "myapp-production-data"

tags = {

Name = "Application Data"

Environment = "production"

}

}

Key components: providers connect to cloud APIs, resources define infrastructure components, and the backend stores state.

## State Management

State is the most critical part of Terraform. It maps configuration to real-world resources.

## Remote State Backend

Always use remote state storage with locking:

## backend configuration during init: terraform init -backend-config=backend.hcl

bucket = "company-terraform-state"

key = "env:/${environment}/networking/terraform.tfstate"

region = "us-east-1"

dynamodb_table = "terraform-state-lock"

encrypt = true

DynamoDB provides state locking to prevent concurrent modifications. S3 versioning provides state history for rollback.

## State Access for Other Configurations

Share outputs across configurations:

data "terraform_remote_state" "vpc" {

backend = "s3"

config = {

bucket = "company-terraform-state"

key = "env:/production/vpc/terraform.tfstate"

region = "us-east-1"

}

}

resource "aws_instance" "app" {

subnet_id = data.terraform_remote_state.vpc.outputs.private_subnet_ids[0]

}

## Module Design

Modules are reusable Terraform configurations. Design them for composability:

## modules/vpc/main.tf

variable "vpc_cidr" {

description = "CIDR block for the VPC"

type = string

validation {

condition = can(cidrhost(var.vpc_cidr, 0))

error_message = "Must be a valid CIDR notation."

}

}

variable "environment" {

description = "Environment name for tagging"

type = string

}

resource "aws_vpc" "this" {

cidr_block = var.vpc_cidr

enable_dns_hostnames = true

enable_dns_support = true

tags = {

Name = "vpc-${var.environment}"

Environment = var.environment

}

}

output "vpc_id" {

value = aws_vpc.this.id

}

output "vpc_cidr" {

value = aws_vpc.this.cidr_block

}

Use input validation to catch errors early. Document all variables and outputs with descriptions.

## Workspace and Environment Management

Use workspaces or directory structure for environment isolation:

## Directory structure:

terraform/

env/

production/

main.tf

terraform.tfvars

staging/

main.tf

terraform.tfvars

Or use Terraform workspaces:

terraform workspace new staging

terraform workspace new production

terraform workspace select staging

terraform plan -var-file=staging.tfvars

Workspaces are simpler but can become confusing with many environments. Directory-based separation is clearer for complex setups.

## Terraform Plan and Apply Workflow

The standard workflow in CI/CD:

## Initialize with backend

terraform init -backend-config=backend-$ENV.hcl

## Format and validate

terraform fmt -check

terraform validate

## Plan

terraform plan -out=tfplan -var-file=$ENV.tfvars

## Apply (typically in CI with approval gate)

terraform apply tfplan

Never run `terraform apply` without a plan file in CI. Always review the plan output before applying.

## Managing Secrets

Never hardcode secrets. Use variables with sensitive flag:

variable "db_password" {

description = "Database administrator password"

type = string

sensitive = true

}

For secrets that must be in state, encrypt with a key management service:

resource "aws_db_instance" "main" {

password = var.db_password # Still goes to state, but you can encrypt state

}

Better approach: use AWS Secrets Manager or Vault and reference secrets via data sources:

data "aws_secretsmanager_secret_version" "db_password" {

secret_id = "production/db/password"

}

## Testing Terraform Code

## `terraform plan` as a Test

Run `terraform plan` in CI to detect drift and validate changes without applying:

terraform plan -detailed-exitcode

## Exit code 0: no changes

## Exit code 1: error

## Exit code 2: changes needed

## Terratest for Integration Tests

// test/vpc_test.go

func TestVPC(t *testing.T) {

terraformOptions := &terraform.Options;{

TerraformDir: "../modules/vpc",

Vars: map[string]interface{}{

"vpc_cidr": "10.0.0.0/16",

"environment": "test",

},

}

defer terraform.Destroy(t, terraformOptions)

terraform.InitAndApply(t, terraformOptions)

output := terraform.Output(t, terraformOptions, "vpc_id")

assert.NotEmpty(t, output)

}

## Common Pitfalls

  * **State file leaks** : Never commit state files to Git. Use `.gitignore` and remote backends.

  * **Hardcoded values** : Use variables and locals for everything that varies.

  * **Missing`prevent_destroy`**: Protect critical resources:




resource "aws_db_instance" "production" {

lifecycle {

prevent_destroy = true

}

}

  * **Large state files** : Split infrastructure into manageable chunks by service layer (networking, compute, data).



## Sentinel and Policy as Code

For teams, enforce policies with Sentinel (HashiCorp Enterprise) or Open Policy Agent:

## Deny public S3 buckets

deny[msg] {

resource := input.resource_changes[_]

resource.type == "aws_s3_bucket"

resource.change.after.acl == "public-read"

msg := "S3 buckets must not be publicly readable"

}

## Summary

Terraform brings software engineering practices to infrastructure. Use remote state with locking, compose resources into modules, separate environments, and integrate planning into CI/CD. Never hardcode secrets, always validate configurations, and protect critical resources from accidental destruction. With these practices, Terraform enables infrastructure that is versioned, reviewable, reproducible, and auditable.

**See also:** [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>), [Serverless Framework: From Zero to Production](</en/tech/serverless-framework.html>), [Kubernetes Security Best Practices](</en/tech/kubernetes-services-security.html>).

**See also:** [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>), [Serverless Framework: From Zero to Production](</en/tech/serverless-framework.html>), [Kubernetes Security Best Practices](</en/tech/kubernetes-services-security.html>)

**See also:** [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>), [Serverless Framework: From Zero to Production](</en/tech/serverless-framework.html>), [Kubernetes Security Best Practices](</en/tech/kubernetes-services-security.html>)

**See also:** [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>), [Serverless Framework: From Zero to Production](</en/tech/serverless-framework.html>), [Kubernetes Security Best Practices](</en/tech/kubernetes-services-security.html>)

**See also:** [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>), [Serverless Framework: From Zero to Production](</en/tech/serverless-framework.html>), [Kubernetes Security Best Practices](</en/tech/kubernetes-services-security.html>)

**See also:** [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>), [Serverless Framework: From Zero to Production](</en/tech/serverless-framework.html>), [Kubernetes Security Best Practices](</en/tech/kubernetes-services-security.html>)

**See also:** [Chaos Engineering: Principles and Practical Tools](</en/tech/chaos-engineering.html>), [Helm Charts: Kubernetes Package Management](</en/tech/helm-kubernetes-package-management.html>), [Cloud Cost Optimization Tips](</en/tech/cloud-cost-optimization.html>)

**See also:** [Chaos Engineering: Principles and Practical Tools](</en/tech/chaos-engineering.html>), [Helm Charts: Kubernetes Package Management](</en/tech/helm-kubernetes-package-management.html>), [Cloud Cost Optimization Tips](</en/tech/cloud-cost-optimization.html>)

**See also:** [Chaos Engineering: Principles and Practical Tools](</en/tech/chaos-engineering.html>), [Helm Charts: Kubernetes Package Management](</en/tech/helm-kubernetes-package-management.html>), [Cloud Cost Optimization Tips](</en/tech/cloud-cost-optimization.html>)

**See also:** [Chaos Engineering: Principles and Practical Tools](</en/tech/chaos-engineering.html>), [Helm Charts: Kubernetes Package Management](</en/tech/helm-kubernetes-package-management.html>), [Cloud Cost Optimization Tips](</en/tech/cloud-cost-optimization.html>)

**See also:** [Chaos Engineering: Principles and Practical Tools](</en/tech/chaos-engineering.html>), [Helm Charts: Kubernetes Package Management](</en/tech/helm-kubernetes-package-management.html>), [Cloud Cost Optimization Tips](</en/tech/cloud-cost-optimization.html>)

**See also:** [Chaos Engineering: Principles and Practical Tools](</en/tech/chaos-engineering.html>), [Helm Charts: Kubernetes Package Management](</en/tech/helm-kubernetes-package-management.html>), [Cloud Cost Optimization Tips](</en/tech/cloud-cost-optimization.html>)

**See also:** [Chaos Engineering: Principles and Practical Tools](</en/tech/chaos-engineering.html>), [Helm Charts: Kubernetes Package Management](</en/tech/helm-kubernetes-package-management.html>), [Cloud Cost Optimization Tips](</en/tech/cloud-cost-optimization.html>)

**See also:** [Chaos Engineering: Principles and Practical Tools](</en/tech/chaos-engineering.html>), [Helm Charts: Kubernetes Package Management](</en/tech/helm-kubernetes-package-management.html>), [Cloud Cost Optimization Tips](</en/tech/cloud-cost-optimization.html>)

**See also:** [Chaos Engineering: Principles and Practical Tools](</en/tech/chaos-engineering.html>), [Helm Charts: Kubernetes Package Management](</en/tech/helm-kubernetes-package-management.html>), [Cloud Cost Optimization Tips](</en/tech/cloud-cost-optimization.html>)

**See also:** [Chaos Engineering: Principles and Practical Tools](</en/tech/chaos-engineering.html>), [Helm Charts: Kubernetes Package Management](</en/tech/helm-kubernetes-package-management.html>), [Cloud Cost Optimization Tips](</en/tech/cloud-cost-optimization.html>)

**See also:** [Chaos Engineering: Principles and Practical Tools](</en/tech/chaos-engineering.html>), [Helm Charts: Kubernetes Package Management](</en/tech/helm-kubernetes-package-management.html>), [Cloud Cost Optimization Tips](</en/tech/cloud-cost-optimization.html>)
