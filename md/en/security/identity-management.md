---
title: "Identity and Access Management (IAM) Guide"
description: "Comprehensive guide to IAM covering SSO, SAML, OIDC, SCIM provisioning, just-in-time access, and access reviews."
date: 2026-03-04
board: security
url: https://aidev.fit/en/security/identity-management.html
---

# Identity and Access Management (IAM) Guide

Identity and Access Management (IAM) is the discipline of ensuring the right people have access to the right resources at the right time for the right reasons. Poor IAM is the leading cause of data breaches. This guide covers modern IAM concepts including SSO, SAML, OIDC, SCIM, just-in-time access, and access reviews.

## Single Sign-On (SSO)

SSO allows users to authenticate once and gain access to multiple applications without re-entering credentials. It improves both security and user experience.

## How SSO Works

An SSO system has three components:

  * **Identity Provider (IdP)** : The authoritative source for user identities. Examples: Okta, Azure AD, Keycloak, Google Workspace.



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Service Provider (SP)** : The application the user wants to access.

3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **User Agent** : Typically a web browser.

When a user accesses an SP, the SP redirects them to the IdP for authentication. The IdP authenticates the user and issues a token. The SP validates the token and grants access.

## Benefits of SSO

  * Users manage one password instead of dozens.

  * Password policies (complexity, rotation) are enforced centrally.

  * Account lockout and deactivation propagate instantly across all applications.

  * Failed login attempts are tracked in one place.




## SAML 2.0

Security Assertion Markup Language (SAML) 2.0 is an XML-based protocol for exchanging authentication and authorization data between IdPs and SPs.

## SAML Flow

  * User attempts to access an SP resource.



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. SP generates a SAML authentication request and redirects the user to the IdP.

3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. IdP authenticates the user (via password, MFA, or other method).

4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. IdP generates a SAML assertion containing user attributes (username, email, groups) and signs it with its private key.

5\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. User is redirected back to the SP with the SAML assertion.

6\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. SP validates the signature, extracts attributes, and creates a session.

ID="_12345" IssueInstant="2026-05-12T10:00:00Z">

https://idp.example.com/metadata

...

user@example.com

user@example.com

engineering

SAML is widely used in enterprise environments for web application SSO. Its XML-based nature makes it verbose, but it remains the standard for many SaaS applications and federated identity scenarios.

## OpenID Connect (OIDC)

OIDC is a modern authentication protocol built on top of OAuth 2.0. It is the preferred protocol for newer applications, particularly in cloud-native environments.

## OIDC vs SAML

  * OIDC uses JSON (JWT tokens) rather than XML. Tokens are smaller and easier to parse.

  * OIDC is designed for modern web and mobile applications, including SPAs and native apps.

  * OIDC provides the `id_token` (authentication) alongside the OAuth `access_token` (authorization).

  * OIDC is the default for cloud provider IAM roles, Kubernetes authentication, and serverless applications.




## OIDC Flow

## Python example: OIDC authentication request

import requests

## Step 1: Redirect user to IdP authorization endpoint

auth_url = "https://idp.example.com/authorize"

params = {

"response_type": "code",

"client_id": "my-app",

"redirect_uri": "https://my-app.example.com/callback",

"scope": "openid profile email",

"state": "random-state-value"

}

## User is redirected to: auth_url?response_type=code&client;_id=...

## Step 2: Exchange authorization code for tokens

token_url = "https://idp.example.com/token"

response = requests.post(token_url, data={

"grant_type": "authorization_code",

"code": "authorization-code-from-callback",

"redirect_uri": "https://my-app.example.com/callback",

"client_id": "my-app",

"client_secret": "my-secret"

})

tokens = response.json()

## tokens contains: access_token, id_token, refresh_token

## OIDC in Cloud Infrastructure

Cloud providers use OIDC for workload identity. A service running in AWS can get an OIDC token from the AWS metadata endpoint and use it to authenticate to external services.

## GitHub Actions OIDC with AWS

name: Deploy

permissions:

id-token: write

contents: read

jobs:

deploy:

runs-on: ubuntu-latest

steps:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- uses: actions/checkout@v4

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- uses: aws-actions/configure-aws-credentials@v4

with:

role-to-assume: arn:aws:iam::123456789:role/github-actions-role

aws-region: us-east-1

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- run: aws s3 sync ./dist s3://my-bucket

## SCIM Provisioning

System for Cross-domain Identity Management (SCIM) is a standard for automating user provisioning and deprovisioning between identity domains.

## How SCIM Works

SCIM exposes RESTful endpoints for creating, reading, updating, and deleting user accounts and groups. An IdP like Okta or Azure AD connects to an SCIM endpoint to synchronize users automatically.

// SCIM Create User Request

POST /scim/v2/Users

Content-Type: application/scim+json

{

"schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],

"userName": "jdoe@example.com",

"name": {

"givenName": "John",

"familyName": "Doe"

},

"emails": [

{

"value": "jdoe@example.com",

"type": "work",

"primary": true

}

],

"active": true

}

SCIM ensures that when an employee leaves the company, their access is automatically revoked across all SCIM-integrated applications within minutes.

## Just-in-Time (JIT) Access

JIT access grants elevated permissions only when needed, for a limited duration. It replaces standing privileges that attackers can exploit.

## Implementation

JIT access typically requires:

  * A request with a business justification.



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Approval from a manager or ticket system.

3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Automatic expiration after the approved window.

4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Full audit logging of the elevation.

## Example: PagerDuty JIT access request

def request_jit_access(resource, duration_minutes=60, reason=""):

approval = submit_approval_request(

requester=get_current_user(),

resource=resource,

reason=reason,

approver=resource_manager

)

if approval.status == "approved":

grant_temporary_role(

user=get_current_user(),

role=f"admin-{resource}",

ttl=duration_minutes

)

return f"Access to {resource} granted until T+{duration_minutes}m"

raise PermissionError("Access request denied")

JIT access is critical for protecting sensitive systems like production databases, cloud admin consoles, and CI/CD deployment pipelines.

## Access Reviews

Access reviews are periodic audits of who has access to what. They are required by compliance frameworks (SOC 2, SOX) and are essential for preventing privilege creep.

## Best Practices

  * Conduct access reviews every quarter for critical systems, annually for low-risk systems.

  * Automate the review process using your IdP or dedicated tools.

  * Focus on active users; disable accounts for users who have not logged in for 90 days.

  * Review group memberships, not just individual permissions.

  * Require managers to certify their direct reports' access.

  * Document all review outcomes for audit purposes.




## Automated access review report

def generate_access_review():

users = list_all_users()

report = []

for user in users:

if user.last_login < (now() - timedelta(days=90)):

report.append({

"user": user.email,

"status": "suggest_disable",

"reason": "No login in 90 days",

"groups": user.groups

})

return report

## Conclusion

Modern IAM requires SSO for user convenience, SAML or OIDC for protocol support, SCIM for automated provisioning, JIT access for privilege management, and regular access reviews to prevent creep. The goal is simple: every access decision should be intentional, verifiable, and timely.

**See also:** [Encryption at Rest Guide](</en/security/encryption-at-rest.html>), [SSO Architecture](</en/security/sso-architecture.html>), [Two-Factor Authentication Guide](</en/security/two-factor-authentication.html>).

**See also:** [Encryption at Rest Guide](</en/security/encryption-at-rest.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>), [API Rate Limiting Implementation](</en/security/api-rate-limiting.html>)

**See also:** [Encryption at Rest Guide](</en/security/encryption-at-rest.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>), [API Rate Limiting Implementation](</en/security/api-rate-limiting.html>)

**See also:** [Encryption at Rest Guide](</en/security/encryption-at-rest.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>), [API Rate Limiting Implementation](</en/security/api-rate-limiting.html>)

**See also:** [Encryption at Rest Guide](</en/security/encryption-at-rest.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>), [API Rate Limiting Implementation](</en/security/api-rate-limiting.html>)

**See also:** [Encryption at Rest Guide](</en/security/encryption-at-rest.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>), [API Rate Limiting Implementation](</en/security/api-rate-limiting.html>)

**See also:** [Zero Trust Architecture for Startups](</en/security/zero-trust-architecture.html>), [SSO Architecture](</en/security/sso-architecture.html>), [IAM: Identity and Access Management Fundamentals](</en/security/identity-access-management.html>)

**See also:** [Zero Trust Architecture for Startups](</en/security/zero-trust-architecture.html>), [SSO Architecture](</en/security/sso-architecture.html>), [IAM: Identity and Access Management Fundamentals](</en/security/identity-access-management.html>)

**See also:** [Zero Trust Architecture for Startups](</en/security/zero-trust-architecture.html>), [SSO Architecture](</en/security/sso-architecture.html>), [IAM: Identity and Access Management Fundamentals](</en/security/identity-access-management.html>)

**See also:** [Zero Trust Architecture for Startups](</en/security/zero-trust-architecture.html>), [SSO Architecture](</en/security/sso-architecture.html>), [IAM: Identity and Access Management Fundamentals](</en/security/identity-access-management.html>)

**See also:** [Zero Trust Architecture for Startups](</en/security/zero-trust-architecture.html>), [SSO Architecture](</en/security/sso-architecture.html>), [IAM: Identity and Access Management Fundamentals](</en/security/identity-access-management.html>)

**See also:** [Zero Trust Architecture for Startups](</en/security/zero-trust-architecture.html>), [SSO Architecture](</en/security/sso-architecture.html>), [IAM: Identity and Access Management Fundamentals](</en/security/identity-access-management.html>)

**See also:** [Zero Trust Architecture for Startups](</en/security/zero-trust-architecture.html>), [SSO Architecture](</en/security/sso-architecture.html>), [IAM: Identity and Access Management Fundamentals](</en/security/identity-access-management.html>)

**See also:** [Zero Trust Architecture for Startups](</en/security/zero-trust-architecture.html>), [SSO Architecture](</en/security/sso-architecture.html>), [IAM: Identity and Access Management Fundamentals](</en/security/identity-access-management.html>)

**See also:** [Zero Trust Architecture for Startups](</en/security/zero-trust-architecture.html>), [SSO Architecture](</en/security/sso-architecture.html>), [IAM: Identity and Access Management Fundamentals](</en/security/identity-access-management.html>)

**See also:** [Zero Trust Architecture for Startups](</en/security/zero-trust-architecture.html>), [SSO Architecture](</en/security/sso-architecture.html>), [IAM: Identity and Access Management Fundamentals](</en/security/identity-access-management.html>)

**See also:** [Zero Trust Architecture for Startups](</en/security/zero-trust-architecture.html>), [SSO Architecture](</en/security/sso-architecture.html>), [IAM: Identity and Access Management Fundamentals](</en/security/identity-access-management.html>)

**See also:** [Zero Trust Architecture for Startups](</en/security/zero-trust-architecture.html>), [SSO Architecture](</en/security/sso-architecture.html>), [IAM: Identity and Access Management Fundamentals](</en/security/identity-access-management.html>)

**See also:** [Zero Trust Architecture for Startups](</en/security/zero-trust-architecture.html>), [SSO Architecture](</en/security/sso-architecture.html>), [IAM: Identity and Access Management Fundamentals](</en/security/identity-access-management.html>)

**See also:** [Zero Trust Architecture for Startups](</en/security/zero-trust-architecture.html>), [SSO Architecture](</en/security/sso-architecture.html>), [IAM: Identity and Access Management Fundamentals](</en/security/identity-access-management.html>)

**See also:** [Zero Trust Architecture for Startups](</en/security/zero-trust-architecture.html>), [SSO Architecture](</en/security/sso-architecture.html>), [IAM: Identity and Access Management Fundamentals](</en/security/identity-access-management.html>)

**See also:** [Zero Trust Architecture for Startups](</en/security/zero-trust-architecture.html>), [SSO Architecture](</en/security/sso-architecture.html>), [IAM: Identity and Access Management Fundamentals](</en/security/identity-access-management.html>)

**See also:** [Zero Trust Architecture for Startups](</en/security/zero-trust-architecture.html>), [SSO Architecture](</en/security/sso-architecture.html>), [IAM: Identity and Access Management Fundamentals](</en/security/identity-access-management.html>)

**See also:** [Zero Trust Architecture for Startups](</en/security/zero-trust-architecture.html>), [SSO Architecture](</en/security/sso-architecture.html>), [IAM: Identity and Access Management Fundamentals](</en/security/identity-access-management.html>)
