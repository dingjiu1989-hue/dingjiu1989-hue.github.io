---
title: "Terraform Tools: Terragrunt, terratest, tfsec, Infracost"
description: "Essential Terraform ecosystem tools: Terragrunt for DRY configurations, terratest for infrastructure testing, tfsec for security scanning, and Infracost for cos"
date: 2026-02-06
board: tools
url: https://dingjiu1989-hue.github.io/en/tools/terraform-tools.html
---

# Terraform Tools: Terragrunt, terratest, tfsec, Infracost

## Introduction

Terraform has become the standard for infrastructure as code, but managing Terraform at scale requires additional tools. Terragrunt reduces configuration duplication. Terratest enables automated infrastructure testing. Tfsec scans configurations for security issues. Infracost provides cost estimates before deployment. This article covers each tool with practical examples.

## Terragrunt

A thin wrapper that keeps Terraform configurations DRY:

## terragrunt.hcl (root configuration)

remote_state {

backend = "s3"

config = {

bucket = "my-company-terraform-state"

key = "${path_relative_to_include()}/terraform.tfstate"

region = "us-east-1"

encrypt = true

dynamodb_table = "terraform-locks"

}

}

generate "provider" {

path = "provider.tf"

if_exists = "overwrite_terragrunt"

contents = <

provider "aws" {

region = local.aws_region

default_tags {

tags = {

Environment = local.environment

ManagedBy = "terragrunt"

}

}

}

EOF

}

locals {

aws_region = "us-east-1"

environment = reverse(split("/", get_terragrunt_dir()))[1]

}

## dev/vpc/terragrunt.hcl

terraform {

source = "../../modules/vpc"

}

include "root" {

path = find_in_parent_folders()

}

inputs = {

vpc_name = "dev-vpc"

cidr_block = "10.0.0.0/16"

enable_nat = true

enable_vpn = false

private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]

public_subnets = ["10.0.101.0/24", "10.0.102.0/24"]

}

## Apply all modules in dependency order

terragrunt run-all apply

## Plan only changed modules

terragrunt run-all plan

## Output dependency graph

terragrunt graph | dot -Tpng > graph.png

## Validate all configurations

terragrunt run-all validate

## Destroy with confirmation

terragrunt run-all destroy

## Terratest

Go library for writing automated infrastructure tests:

package test

import (

"testing"

"github.com/gruntwork-io/terratest/modules/terraform"

"github.com/gruntwork-io/terratest/modules/aws"

"github.com/stretchr/testify/assert"

)

func TestVPCDeployment(t *testing.T) {

terraformOptions := &terraform.Options;{

TerraformDir: "../examples/vpc",

Vars: map[string]interface{}{

"vpc_name": "test-vpc",

"cidr_block": "10.0.0.0/16",

},

NoColor: true,

}

// Clean up at the end

defer terraform.Destroy(t, terraformOptions)

// Deploy infrastructure

terraform.InitAndApply(t, terraformOptions)

// Verify outputs

vpcID := terraform.Output(t, terraformOptions, "vpc_id")

assert.NotEmpty(t, vpcID)

// Verify the VPC actually exists in AWS

vpc := aws.GetVpcById(t, vpcID, "us-east-1")

assert.Equal(t, "10.0.0.0/16", vpc.CidrBlock)

// Verify subnets were created

subnets := aws.GetSubnetsForVpc(t, vpcID, "us-east-1")

assert.Len(t, subnets, 4)

// Verify security group rules

sgID := terraform.Output(t, terraformOptions, "web_sg_id")

sgRules := aws.GetSecurityGroupRules(t, sgID, "us-east-1")

assert.GreaterOrEqual(t, len(sgRules), 2)

}

## tfsec (now Trivy)

Security scanning for Terraform configurations:

## Install tfsec

brew install tfsec

## Or use Trivy which includes tfsec rules

brew install trivy

## Scan Terraform files

tfsec .

tfsec ./environments/production

tfsec --no-color --format json > scan-results.json

## In CI

tfsec --soft-fail # Don't fail CI, just report

## Trivy equivalent

trivy config --severity HIGH,CRITICAL .

## Bad configuration that tfsec catches

resource "aws_s3_bucket" "data" {

bucket = "my-data-bucket"

acl = "public-read" # tfsec: aws-s3-no-public-read-acl

}

resource "aws_security_group" "web" {

ingress {

from_port = 22

to_port = 22

protocol = "tcp"

cidr_blocks = ["0.0.0.0/0"] # tfsec: aws-vpc-no-public-ingress-sgr

}

}

## Fixed configuration

resource "aws_s3_bucket" "data" {

bucket = "my-data-bucket"

acl = "private"

}

resource "aws_security_group" "web" {

ingress {

from_port = 22

to_port = 22

protocol = "tcp"

cidr_blocks = ["10.0.0.0/8"] # Restricted to internal network

}

}

## Infracost

Cost estimation for Terraform projects:

## Install

brew install infracost

infracost auth login

## Generate cost estimate for current state

infracost breakdown --path .

## Compare with previous state

infracost diff --path . --compare-to previous-cost.json

## Output in different formats

infracost breakdown --path . --format json

infracost breakdown --path . --format html --out-file cost-report.html

## In CI

infracost diff --path . --show-skipped

## .infracost.yml — usage estimates

version: 0.1

projects:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- path: ./environments/production

usage:

aws_instance.web:

monthly_cpu_credit_hrs: 100

monthly_hrs: 730

aws_lambda.function:

monthly_requests: 1000000

request_duration_ms: 500

aws_s3_bucket.data:

storage_gb: 500

monthly_tier_1_requests: 10000

## Other Essential Tools

**pre-commit hooks** for Terraform:

## .pre-commit-config.yaml

repos:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- repo: https://github.com/antonbabenko/pre-commit-terraform

rev: v1.96.0

hooks:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- id: terraform_fmt

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- id: terraform_validate

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- id: terraform_tflint

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- id: terraform_trivy

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- id: terraform_docs

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- id: checkov

## Comparison

| Tool | Purpose | Essential For |

|------|---------|---------------|

| Terragrunt | DRY configuration | Multi-environment, multi-module projects |

| Terratest | Infrastructure testing | Automated validation of deployments |

| tfsec/Trivy | Security scanning | Catching misconfigurations before deploy |

| Infracost | Cost estimation | Budget planning and cost awareness |

| pre-commit | Code quality | Consistent formatting and validation |

## Recommendations

  * **Multi-environment IaC** : Use Terragrunt to eliminate configuration duplication across environments.

  * **Production safety** : Use Terratest to write automated tests that verify infrastructure after deployment.

  * **Security compliance** : Run tfsec or Trivy in CI pipelines to catch misconfigurations before merge.

  * **Cost awareness** : Use Infracost in PR pipelines to show cost implications of infrastructure changes.

  * **Code quality** : Set up pre-commit hooks for terraform fmt, validate, tflint, and docs.




The ideal Terraform workflow combines all these tools: Terragrunt for structure, pre-commit for quality, tfssec for security, Infracost for cost awareness, and Terratest for deployment validation.

**See also:** [Helm Tools: Helmfile, helm-docs, helm-secrets, Chart Testing](</en/tools/helm-tools.html>), [Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide](</en/tools/networking-tools.html>), [IaC Tools Compared: Terraform, Pulumi, CDK, OpenTofu, and CloudFormation](</en/tools/iac-tools-compared.html>).

**See also:** [Helm Tools: Helmfile, helm-docs, helm-secrets, Chart Testing](</en/tools/helm-tools.html>), [Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide](</en/tools/networking-tools.html>), [IaC Tools Compared: Terraform, Pulumi, CDK, OpenTofu, and CloudFormation](</en/tools/iac-tools-compared.html>)

**See also:** [Helm Tools: Helmfile, helm-docs, helm-secrets, Chart Testing](</en/tools/helm-tools.html>), [Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide](</en/tools/networking-tools.html>), [IaC Tools Compared: Terraform, Pulumi, CDK, OpenTofu, and CloudFormation](</en/tools/iac-tools-compared.html>)

**See also:** [Helm Tools: Helmfile, helm-docs, helm-secrets, Chart Testing](</en/tools/helm-tools.html>), [Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide](</en/tools/networking-tools.html>), [IaC Tools Compared: Terraform, Pulumi, CDK, OpenTofu, and CloudFormation](</en/tools/iac-tools-compared.html>)

**See also:** [Helm Tools: Helmfile, helm-docs, helm-secrets, Chart Testing](</en/tools/helm-tools.html>), [Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide](</en/tools/networking-tools.html>), [IaC Tools Compared: Terraform, Pulumi, CDK, OpenTofu, and CloudFormation](</en/tools/iac-tools-compared.html>)

**See also:** [Helm Tools: Helmfile, helm-docs, helm-secrets, Chart Testing](</en/tools/helm-tools.html>), [Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide](</en/tools/networking-tools.html>), [IaC Tools Compared: Terraform, Pulumi, CDK, OpenTofu, and CloudFormation](</en/tools/iac-tools-compared.html>)

**See also:** [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>), [Infrastructure Scanners 2026: Trivy, Checkov, Terrascan, kube-bench](</en/tools/infrastructure-scanners-2026.html>), [Kubernetes Tools: kubectl Plugins, k9s, Lens, Kustomize](</en/tools/kubernetes-tools.html>)

**See also:** [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>), [Infrastructure Scanners 2026: Trivy, Checkov, Terrascan, kube-bench](</en/tools/infrastructure-scanners-2026.html>), [Kubernetes Tools: kubectl Plugins, k9s, Lens, Kustomize](</en/tools/kubernetes-tools.html>)

**See also:** [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>), [Infrastructure Scanners 2026: Trivy, Checkov, Terrascan, kube-bench](</en/tools/infrastructure-scanners-2026.html>), [Kubernetes Tools: kubectl Plugins, k9s, Lens, Kustomize](</en/tools/kubernetes-tools.html>)

**See also:** [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>), [Infrastructure Scanners 2026: Trivy, Checkov, Terrascan, kube-bench](</en/tools/infrastructure-scanners-2026.html>), [Kubernetes Tools: kubectl Plugins, k9s, Lens, Kustomize](</en/tools/kubernetes-tools.html>)

**See also:** [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>), [Infrastructure Scanners 2026: Trivy, Checkov, Terrascan, kube-bench](</en/tools/infrastructure-scanners-2026.html>), [Kubernetes Tools: kubectl Plugins, k9s, Lens, Kustomize](</en/tools/kubernetes-tools.html>)

**See also:** [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>), [Infrastructure Scanners 2026: Trivy, Checkov, Terrascan, kube-bench](</en/tools/infrastructure-scanners-2026.html>), [Kubernetes Tools: kubectl Plugins, k9s, Lens, Kustomize](</en/tools/kubernetes-tools.html>)

**See also:** [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>), [Infrastructure Scanners 2026: Trivy, Checkov, Terrascan, kube-bench](</en/tools/infrastructure-scanners-2026.html>), [Kubernetes Tools: kubectl Plugins, k9s, Lens, Kustomize](</en/tools/kubernetes-tools.html>)

**See also:** [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>), [Infrastructure Scanners 2026: Trivy, Checkov, Terrascan, kube-bench](</en/tools/infrastructure-scanners-2026.html>), [Kubernetes Tools: kubectl Plugins, k9s, Lens, Kustomize](</en/tools/kubernetes-tools.html>)

**See also:** [Debugging Tools: lldb, gdb, strace, ltrace, rr Reverse Debugging](</en/tools/debugging-tools.html>), [Infrastructure Scanners 2026: Trivy, Checkov, Terrascan, kube-bench](</en/tools/infrastructure-scanners-2026.html>), [Kubernetes Tools: kubectl Plugins, k9s, Lens, Kustomize](</en/tools/kubernetes-tools.html>)
