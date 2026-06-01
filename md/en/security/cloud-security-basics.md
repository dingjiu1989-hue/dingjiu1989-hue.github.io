---
title: "Cloud Security Basics: Shared Responsibility Model Explained"
description: "Understand the AWS/GCP/Azure shared responsibility model, IAM policies, network security groups, and key cloud security services."
date: 2026-03-03
board: security
url: https://aidev.fit/en/security/cloud-security-basics.html
---

# Cloud Security Basics: Shared Responsibility Model Explained

The shared responsibility model is the foundational concept in cloud security. It defines what the cloud provider secures versus what the customer must secure. Misunderstanding this boundary is the root cause of most cloud data breaches.

## The Shared Responsibility Model

Every major cloud provider — AWS, Google Cloud, and Azure — operates under a shared responsibility model. The provider secures the infrastructure that runs the services. The customer secures everything they deploy on top of that infrastructure.

**AWS shared responsibility** : AWS secures the hardware, software, networking, and facilities that run AWS services. The customer secures their data, platform applications, identity and access management, operating system patches, network firewall configurations, and client-side encryption.

**GCP shared responsibility** : Google secures the physical infrastructure, storage, networking, and encryption-at-rest infrastructure. The customer secures their data classifications, access policies, application configurations, and identity management.

**Azure shared responsibility** : Microsoft secures physical hosts, networks, and datacenters. The customer secures their data, identities, applications, and account management. For platform-as-a-service (PaaS) services, Microsoft takes on more responsibility for the runtime.

## Identity and Access Management (IAM)

IAM is the gatekeeper of your cloud environment. Every API call to a cloud provider passes through IAM authorization.

## AWS IAM

AWS IAM uses policies written in JSON to grant or deny permissions. Policies attach to users, groups, or roles.

{

"Version": "2012-10-17",

"Statement": [

{

"Effect": "Allow",

"Action": ["s3:GetObject", "s3:ListBucket"],

"Resource": [

"arn:aws:s3:::example-bucket",

"arn:aws:s3:::example-bucket/*"

]

}

]

}

Best practices for IAM:

  * Apply the principle of least privilege. Grant only the permissions a role or user needs.

  * Use IAM roles rather than long-lived access keys. EC2 instances and Lambda functions should assume roles.

  * Enable AWS IAM Access Analyzer to identify unused permissions.

  * Require multi-factor authentication for the root account and all privileged users.

## GCP IAM

GCP IAM uses roles that are collections of permissions. Primitive roles (Owner, Editor, Viewer) are broad. Predefined roles are service-specific and more granular.

## Assign a predefined role to a service account

gcloud projects add-iam-policy-binding my-project \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--member="serviceAccount:sa@my-project.iam.gserviceaccount.com" \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--role="roles/storage.objectViewer"

## Azure RBAC

Azure uses Role-Based Access Control with built-in or custom roles. Roles are assigned at management group, subscription, resource group, or resource scope.

az role assignment create \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--assignee user@example.com \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--role "Reader" \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--scope "/subscriptions/SUB_ID/resourceGroups/RG"

## Network Security Groups

Cloud virtual networks need traffic filtering at multiple layers.

**AWS Security Groups** : Stateful firewalls at the instance level. You define inbound and outbound rules. Allow rules only — there is no explicit deny in security groups. Network ACLs provide stateless filtering at the subnet level with both allow and deny rules.

**GCP Firewall Rules** : Applied at the VPC network level. They can be ingress or egress rules with allow or deny actions. Rules include source and destination IP ranges, protocols, and ports.

**Azure Network Security Groups (NSGs)** : Filter traffic at the subnet or NIC level. NSGs contain security rules with priority, source, destination, protocol, direction, and action (allow or deny).

## Cloud Security Services

## AWS CloudTrail

CloudTrail records every API call made in your AWS account. It logs the caller identity, time, source IP, request parameters, and response elements. Enable CloudTrail in all regions and use a single trail for all accounts in AWS Organizations.

## AWS GuardDuty

GuardDuty is a threat detection service that analyzes CloudTrail events, VPC flow logs, and DNS logs. It uses machine learning to detect unusual behavior such as crypto mining activity, anomalous API calls, or compromised credentials.

## GCP Security Command Center

Security Command Center provides threat detection, vulnerability scanning, and asset inventory for GCP. It surfaces misconfigurations like public buckets, open firewall ports, and IAM policy violations.

## Azure Defender

Azure Defender (formerly Azure Security Center) provides unified security management and advanced threat protection across hybrid cloud workloads. It includes just-in-time VM access, file integrity monitoring, and vulnerability assessments.

## Key Management

Encryption key management differs across providers:

  * **AWS KMS** : Managed service for creating and controlling encryption keys. Supports automatic key rotation, key policies, and integration with most AWS services.

  * **GCP Cloud KMS** : Similar capabilities with Cloud HSM option for FIPS 140-2 Level 3 validation.

  * **Azure Key Vault** : Stores keys, secrets, and certificates. Integrates with Azure Disk Encryption, SQL Server TDE, and App Service.

Never store secrets in code, configuration files, or environment variables exposed through debugging endpoints. Use a proper secrets manager with automatic rotation.

## Conclusion

Cloud security starts with understanding the shared responsibility model. From there, it requires disciplined IAM management, proper network segmentation, and full utilization of your provider's security tooling. The shift to cloud does not eliminate security responsibilities — it transforms them.
