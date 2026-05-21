---
title: "IAM: Identity and Access Management Fundamentals"
description: "IAM fundamentals: user provisioning, authentication, authorization, role-based access, and identity governance."
date: 2026-03-23
board: security
url: https://dingjiu1989-hue.github.io/en/security/identity-access-management.html
---

# IAM: Identity and Access Management Fundamentals

Identity and Access Management (IAM) controls who can access what resources under which conditions. It is the foundation of enterprise security.

## Core Components

Identity management handles user identity throughout the lifecycle: joiner (provision accounts and access), mover (update access as roles change), and leaver (deprovision accounts and revoke access). Identity lifecycle automation reduces both security risk and administrative overhead.

Authentication verifies identity. Methods include passwords (weakest, still most common), multi-factor authentication (something you know + something you have + something you are), single sign-on (authenticate once, access many applications), and passwordless (biometrics, security keys, magic links).

Authorization determines what authenticated users can do. Role-Based Access Control (RBAC) assigns permissions to roles and roles to users. Attribute-Based Access Control (ABAC) considers user attributes, resource attributes, and environmental conditions.

## Single Sign-On

SSO reduces password fatigue and improves security. One strong authentication provides access to all connected applications. SAML 2.0 and OpenID Connect (OIDC) are the standard SSO protocols. OIDC is simpler and more modern, built on OAuth 2.0.

Identity providers (IdP) implement SSO: Azure AD, Okta, Keycloak, Auth0. Service providers (applications) trust the IdP for authentication. When a user accesses an application, they are redirected to the IdP for authentication. The IdP issues a token that the application accepts.

## Multi-Factor Authentication

MFA dramatically reduces account compromise risk. SMS codes are better than no MFA but vulnerable to SIM swapping. Authenticator apps (TOTP) are more secure. Hardware security keys (FIDO2/WebAuthn) provide phishing-resistant authentication.

Implement MFA for all users, not just administrators. Risk-based MFA prompts additional factors for high-risk actions. Enforce MFA for all third-party access. Provide backup MFA methods and account recovery processes.

## Just-in-Time Access

JIT access grants elevated permissions temporarily. Users request access when needed, with automatic approval workflows. Access expires automatically after a defined period. JIT reduces the standing privilege attack surface.

Implement JIT for administrative access, database access, and production systems. Approve via existing workflows (Slack approval, ticketing system). Audit all JIT access requests and durations. Look for patterns indicating excessive JIT requests that should be permanent.

## Identity Governance

Periodic access reviews verify that users still need their permissions. Manager-attested reviews confirm access appropriateness. Automated remediation revokes unnecessary access. Governance reporting demonstrates compliance for auditors.

**See also:** [Identity Providers Compared: Auth0, Okta, Keycloak, Firebase Auth](</en/security/identity-provider-comparison.html>), [Zero Trust Networking: Architecture and Implementation Guide](</en/security/zero-trust-networking.html>), [SOC 2 Technical Controls](</en/security/soc2-technical.html>).

**See also:** [Identity Providers Compared: Auth0, Okta, Keycloak, Firebase Auth](</en/security/identity-provider-comparison.html>), [Zero Trust Networking: Architecture and Implementation Guide](</en/security/zero-trust-networking.html>), [IAM Audit](</en/security/iam-audit.html>)

**See also:** [Identity Providers Compared: Auth0, Okta, Keycloak, Firebase Auth](</en/security/identity-provider-comparison.html>), [Zero Trust Networking: Architecture and Implementation Guide](</en/security/zero-trust-networking.html>), [IAM Audit](</en/security/iam-audit.html>)

**See also:** [Identity Providers Compared: Auth0, Okta, Keycloak, Firebase Auth](</en/security/identity-provider-comparison.html>), [Zero Trust Networking: Architecture and Implementation Guide](</en/security/zero-trust-networking.html>), [IAM Audit](</en/security/iam-audit.html>)

**See also:** [Identity Providers Compared: Auth0, Okta, Keycloak, Firebase Auth](</en/security/identity-provider-comparison.html>), [Zero Trust Networking: Architecture and Implementation Guide](</en/security/zero-trust-networking.html>), [IAM Audit](</en/security/iam-audit.html>)

**See also:** [Identity Providers Compared: Auth0, Okta, Keycloak, Firebase Auth](</en/security/identity-provider-comparison.html>), [Zero Trust Networking: Architecture and Implementation Guide](</en/security/zero-trust-networking.html>), [IAM Audit](</en/security/iam-audit.html>)

**See also:** [API Authentication Methods](</en/security/api-authentication.html>), [Certificate Management](</en/security/certificate-management.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>)

**See also:** [API Authentication Methods](</en/security/api-authentication.html>), [Certificate Management](</en/security/certificate-management.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>)

**See also:** [API Authentication Methods](</en/security/api-authentication.html>), [Certificate Management](</en/security/certificate-management.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>)

**See also:** [API Authentication Methods](</en/security/api-authentication.html>), [Certificate Management](</en/security/certificate-management.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>)

**See also:** [API Authentication Methods](</en/security/api-authentication.html>), [Certificate Management](</en/security/certificate-management.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>)

**See also:** [API Authentication Methods](</en/security/api-authentication.html>), [Certificate Management](</en/security/certificate-management.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>)

**See also:** [API Authentication Methods](</en/security/api-authentication.html>), [Certificate Management](</en/security/certificate-management.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>)

**See also:** [API Authentication Methods](</en/security/api-authentication.html>), [Certificate Management](</en/security/certificate-management.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>)

**See also:** [API Authentication Methods](</en/security/api-authentication.html>), [Certificate Management](</en/security/certificate-management.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>)

**See also:** [API Authentication Methods](</en/security/api-authentication.html>), [Certificate Management](</en/security/certificate-management.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>)

**See also:** [API Authentication Methods](</en/security/api-authentication.html>), [Certificate Management](</en/security/certificate-management.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>)

**See also:** [API Authentication Methods](</en/security/api-authentication.html>), [Certificate Management](</en/security/certificate-management.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>)

**See also:** [API Authentication Methods](</en/security/api-authentication.html>), [Certificate Management](</en/security/certificate-management.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>)

**See also:** [API Authentication Methods](</en/security/api-authentication.html>), [Certificate Management](</en/security/certificate-management.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>)
