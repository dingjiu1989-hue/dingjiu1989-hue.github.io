---
title: "Secure Configuration Management"
description: "Comprehensive guide to secure configuration covering infrastructure as code scanning, drift detection, configuration validation, and policy enforcement."
date: 2026-03-13
board: security
url: https://aidev.fit/en/security/secure-configuration.html
---

# Secure Configuration Management

Introduction 

Configuration drift — when actual system configuration diverges from the intended secure baseline — is a leading cause of security incidents. Secure configuration management ensures that systems remain in a known, compliant state throughout their lifecycle. This requires automation at every stage: validation at build time, enforcement at deploy time, and detection at runtime. 

Infrastructure as Code Scanning 

IaC scanning catches misconfigurations before they reach production. 

## Checkov: scan Terraform for security issues

checkov -d terraform/environments/production

## tfsec: Terraform security scanner

tfsec terraform/environments/production --config-file tfsec.yaml

## kics: Keep Infrastructure as Code Secure

kics scan -p kubernetes/deployments --output-path kics-report.json

## checkov policy: S3 bucket must have encryption enabled

resource "aws_s3_bucket" "data" {

bucket = "my-data-bucket"

## This will fail checkov check CKV_AWS_21

## Missing: server_side_encryption_configuration

}

## Custom Checkov policy

from checkov.common.models.enums import CheckResult

from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck

class S3EncryptionCheck(BaseResourceCheck):

def **init**(self):

name = "Ensure S3 bucket has encryption enabled"

id = "CKV_CUSTOM_001"

supported_resources = ['aws_s3_bucket']

super().**init**(name=name, id=id, supported_resources=supported_resources)

def scan_resource_conf(self, conf):

if 'server_side_encryption_configuration' in conf:

return CheckResult.PASSED

return CheckResult.FAILED

Drift Detection 

Drift detection identifies when live infrastructure differs from the declared configuration. 

## Terraform plan detects drift

terraform plan -refresh-only # Check for manual changes

## Terraform drift detection with AWS Config

resource "aws_config_config_rule" "s3_bucket_ssl" {

name = "s3-bucket-ssl-requests-only"

source {

owner = "AWS"

source_identifier = "S3_BUCKET_SSL_REQUESTS_ONLY"

}

}

## Continuous drift monitoring

## 1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Schedule terraform plan to run daily

## 2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Compare output with baseline

## 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Alert on unexpected changes

## !/bin/bash

## drift_detection.sh

BASELINE_DIR="/config/baselines"

REPORT_DIR="/config/reports"

for env in production staging; do

cd terraform/environments/$env

terraform plan -refresh-only -out=plan.tfplan 2>&1 | \

grep -E "changed|destroyed|added" > /tmp/drift.txt

if [ -s /tmp/drift.txt ]; then

## Send alert

./send_alert.sh "Drift detected in $env environment"

cp /tmp/drift.txt "$REPORT_DIR/${env}_drift_ $(date +%Y%m%d).txt"

fi

done

Configuration Validation Pipeline 

## CI/CD configuration validation stage

stages:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- validate

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- scan

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- deploy

validate:

stage: validate

script:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- terraform fmt -check

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- terraform validate

scan:

stage: scan

script:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- checkov -d . -o json > checkov-report.json

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- tfsec . --format sarif > tfsec-report.sarif

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- conftest test . --policy policies/

artifacts:

reports:

checkov: checkov-report.json

tfsec: tfsec-report.sarif

deploy:

stage: deploy

script:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- terraform apply -auto-approve

only:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- main

when: manual

Configuration Validation with Conftest 

Conftest applies policy-as-code to configuration files using Open Policy Agent (OPA). 

## conftest policy for Kubernetes

package main

deny[msg] {

input.kind == "Deployment"

not input.spec.template.spec.containers[_].securityContext.runAsNonRoot

msg = "Containers must run as non-root"

}

deny[msg] {

input.kind == "Deployment"

input.spec.template.spec.containers[_].securityContext.privileged == true

msg = "Privileged containers are not allowed"

}

deny[msg] {

input.kind == "Service"

input.spec.type == "LoadBalancer"

msg = "LoadBalancer services are not allowed"

}

deny[msg] {

input.kind == "Pod"

not input.spec.containers[_].resources.limits.memory

msg = "Memory limits are required"

}

## Run conftest policies

conftest test deployment.yaml --policy conftest/policies/

Policy as Code with OPA 

## OPA policy for Terraform

package terraform

deny[msg] {

resource := input.resource.aws_security_group[_]

rule := resource.ingress[_]

rule.from_port == 22

rule.cidr_blocks[_] == "0.0.0.0/0"

msg = sprintf("Security group %v allows SSH from anywhere", [resource.name])

}

deny[msg] {

resource := input.resource.aws_s3_bucket[_]

resource.acl == "public-read" || resource.acl == "public-read-write"

msg = sprintf("S3 bucket %v has public ACL", [resource.name])

}

Secrets in Configuration 

Never hardcode secrets in configuration. Use a secrets manager. 

## BAD: Hardcoded secret

resource "aws_db_instance" "database" {

username = "admin"

password = "P@ssw0rd123!" # NEVER hardcode

}

## GOOD: Secrets Manager reference

data "aws_secretsmanager_secret_version" "db_creds" {

secret_id = "production/database/credentials"

}

resource "aws_db_instance" "database" {

username = jsondecode(

data.aws_secretsmanager_secret_version.db_creds.secret_string

)["username"]

password = jsondecode(

data.aws_secretsmanager_secret_version.db_creds.secret_string

)["password"]

}

Conclusion 

Secure configuration management requires automation at every stage: scan IaC before deployment, validate against policy as code, detect drift continuously, and never embed secrets in configuration. Shift security left by validating configuration at build time rather than discovering issues in production. Use tools like Checkov, tfsec, conftest, and OPA to enforce your security baseline automatically.

**See also:** [Infrastructure as Code Security](</en/security/iac-security.html>), [Cloud Security Posture Management](</en/security/cloud-security-posture.html>), [Session Management Security](</en/security/session-management.html>).

**See also:** [Infrastructure as Code Security](</en/security/iac-security.html>), [Cloud Security Posture Management](</en/security/cloud-security-posture.html>), [Secure API Design Principles](</en/security/secure-api-design.html>)

**See also:** [Infrastructure as Code Security](</en/security/iac-security.html>), [Cloud Security Posture Management](</en/security/cloud-security-posture.html>), [Secure API Design Principles](</en/security/secure-api-design.html>)

**See also:** [Infrastructure as Code Security](</en/security/iac-security.html>), [Cloud Security Posture Management](</en/security/cloud-security-posture.html>), [Secure API Design Principles](</en/security/secure-api-design.html>)

**See also:** [Infrastructure as Code Security](</en/security/iac-security.html>), [Cloud Security Posture Management](</en/security/cloud-security-posture.html>), [Secure API Design Principles](</en/security/secure-api-design.html>)

**See also:** [Infrastructure as Code Security](</en/security/iac-security.html>), [Cloud Security Posture Management](</en/security/cloud-security-posture.html>), [Secure API Design Principles](</en/security/secure-api-design.html>)

**See also:** [Certificate Management](</en/security/certificate-management.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>), [Container Image Security](</en/security/container-image-security.html>)

**See also:** [Certificate Management](</en/security/certificate-management.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>), [Container Image Security](</en/security/container-image-security.html>)

**See also:** [Certificate Management](</en/security/certificate-management.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>), [Container Image Security](</en/security/container-image-security.html>)

**See also:** [Certificate Management](</en/security/certificate-management.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>), [Container Image Security](</en/security/container-image-security.html>)

**See also:** [Certificate Management](</en/security/certificate-management.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>), [Container Image Security](</en/security/container-image-security.html>)

**See also:** [Certificate Management](</en/security/certificate-management.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>), [Container Image Security](</en/security/container-image-security.html>)

**See also:** [Certificate Management](</en/security/certificate-management.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>), [Container Image Security](</en/security/container-image-security.html>)

**See also:** [Certificate Management](</en/security/certificate-management.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>), [Container Image Security](</en/security/container-image-security.html>)

**See also:** [Certificate Management](</en/security/certificate-management.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>), [Container Image Security](</en/security/container-image-security.html>)

**See also:** [Certificate Management](</en/security/certificate-management.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>), [Container Image Security](</en/security/container-image-security.html>)

**See also:** [Certificate Management](</en/security/certificate-management.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>), [Container Image Security](</en/security/container-image-security.html>)

**See also:** [Certificate Management](</en/security/certificate-management.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>), [Container Image Security](</en/security/container-image-security.html>)

**See also:** [Certificate Management](</en/security/certificate-management.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>), [Container Image Security](</en/security/container-image-security.html>)

**See also:** [Certificate Management](</en/security/certificate-management.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>), [Container Image Security](</en/security/container-image-security.html>)

**See also:** [Certificate Management](</en/security/certificate-management.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>), [Container Image Security](</en/security/container-image-security.html>)

**See also:** [Certificate Management](</en/security/certificate-management.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>), [Container Image Security](</en/security/container-image-security.html>)
