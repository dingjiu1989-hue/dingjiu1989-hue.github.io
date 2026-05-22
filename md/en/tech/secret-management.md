---
title: "Secret Management"
description: "Learn secret management: Vault, AWS Secrets Manager, SOPS, encryption approaches, rotation policies, and best practices"
date: 2026-01-12
board: tech
url: https://aidev.fit/en/tech/secret-management.html
---

# Secret Management

Secret management is the practice of securely storing, accessing, and rotating sensitive information: API keys, database passwords, TLS certificates, and encryption keys. Poor secret management is a leading cause of security breaches. This article covers the major secret management tools and practices for keeping secrets safe.

## What Are Secrets?

Secrets are any sensitive information that controls access to systems or data. Database credentials authenticate applications to databases. API keys authorize access to external services. TLS certificates prove identity and enable encryption. Encryption keys protect data at rest.

Secrets differ from regular configuration. Configuration values can be committed to version control and shared openly. Secrets must be protected with encryption, access controls, and audit logging. Treating secrets as regular configuration is the most common secret management mistake.

## The Threat Model

Secret management protects against several threats. Accidental exposure: secrets committed to version control, logged in debug output, or included in error messages. Unauthorized access: an attacker who gains access to the application or infrastructure can read secrets. Insider threats: developers or operators with unnecessary access to production secrets.

The defense-in-depth approach layers protection: encryption at rest and in transit, access controls with least privilege, audit logging for all secret access, and automatic rotation to limit the impact of exposure.

## HashiCorp Vault

Vault is the most comprehensive secret management platform. It stores secrets in encrypted storage, provides dynamic secrets that expire after use, supports automatic rotation, and generates audit logs for all secret access.

Vault's dynamic secrets are a powerful feature. Instead of sharing a static database password, Vault generates a temporary password with a limited time-to-live. When the application no longer needs access, the credential automatically expires. This eliminates long-lived static secrets.

Vault supports multiple secret engines: KV store for static secrets, database engines for dynamic credentials, PKI engines for certificate generation, and transit engines for encryption-as-a-service. Each engine follows the same API for a consistent access pattern.

## AWS Secrets Manager

AWS Secrets Manager provides managed secret storage for AWS environments. It integrates with AWS services (RDS, Redshift, DocumentDB) for automatic credential rotation. Secrets can be accessed through the AWS SDK, CLI, or console.

Secrets Manager encrypts secrets using AWS KMS. Access is controlled through IAM policies. Audit logging through CloudTrail provides a record of all secret access. Automatic rotation triggers Lambda functions to update credentials in target services.

Secrets Manager is the natural choice for AWS-native applications. It requires no infrastructure to manage and integrates with existing AWS authorization and auditing. The cost is per-secret-per-month plus API calls, which becomes significant at scale.

## SOPS

SOPS (Secrets OPerationS) takes a different approach: encrypt individual values within files, then store the encrypted files in version control. SOPS encrypts YAML, JSON, ENV, and INI files, preserving the file structure while encrypting sensitive values.

SOPS uses AWS KMS, GCP KMS, Azure Key Vault, or age for encryption. Developers decrypt files locally using their cloud provider credentials. CI/CD pipelines decrypt files during deployment.

The advantage of this approach is simplicity. No secret management server to run. Secrets are versioned alongside code (encrypted). Decryption happens at deploy time. The trade-off is weaker security: static encrypted secrets live in the repository, and rotation requires file updates.

## Encryption Approaches

Secrets should be encrypted at rest and in transit. At-rest encryption protects secrets stored in databases, files, or vaults. In-transit encryption protects secrets as they travel from the secret store to the application.

Encryption key management is critical. Encryption keys need their own protection. HSM (Hardware Security Module) provides hardware-backed key protection. KMS services provide managed key rotation and access control. The encryption key hierarchy typically uses a master key to encrypt data keys, which encrypt the actual secrets.

## Rotation Policies

Secret rotation limits the damage from credential exposure. If a database password is compromised, rotation renders the exposed credential useless. Rotation frequency depends on the secret type: TLS certificates rotate every 90 days or less, database passwords rotate monthly, and API keys rotate on detection of exposure.

Automated rotation is essential. Manual rotation is unreliable and often forgotten. Vault's dynamic secrets rotate automatically on each access. AWS Secrets Manager can trigger rotation on a schedule. Custom rotation scripts should be tested regularly to verify they work correctly.

## Application Integration

Applications should fetch secrets at startup, not embed them in code or configuration files. The secret management client authenticates to the secret store, retrieves the necessary secrets, and provides them to the application. Many secret management tools provide sidecar proxies or SDK integration libraries.

Secret injection at deployment time is an alternative to runtime fetching. Kubernetes can inject secrets as environment variables or mounted volumes at pod startup. This approach is simpler but means the secret data exists in the pod's environment and may be visible through debug tools.

Secret management is a foundational security practice. The investment in robust secret management prevents one of the most common attack vectors and enables compliance with security standards and regulations.
