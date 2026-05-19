---
title: "OAuth 2.0 and PKCE Explained"
description: "A deep dive into OAuth 2.0 authorization framework and PKCE flow for securing single-page and mobile applications."
date: 2025-12-18
board: security
url: https://dingjiu1989-hue.github.io/en/security/oauth2-pkce.html
---

# OAuth 2.0 and PKCE Explained

OAuth 2.0 Overview 

OAuth 2.0 is an authorization framework that enables third-party applications to obtain limited access to a user's resources without exposing credentials. It has become the industry standard for API authorization, used by Google, GitHub, Facebook, and virtually every major platform. 

Core Roles 

| Role | Description | Example | |------|-------------|---------| | Resource Owner | The user who grants access | You, the end user | | Client | The application requesting access | Your mobile app or SPA | | Authorization Server | Issues tokens after authentication | Google's OAuth 2.0 endpoint | | Resource Server | Hosts the protected resources | Google Calendar API | 

Grant Types 

OAuth 2.0 defines several grant types for different scenarios: 

  * **Authorization Code** : The most secure flow, designed for server-side applications.

  * **Authorization Code with PKCE** : An enhanced version for mobile and single-page applications.

  * **Client Credentials** : For server-to-server communication without user involvement.

  * **Device Code** : For devices without a browser, like smart TVs or CLI tools.




The Problem PKCE Solves 

Before PKCE (Proof Key for Code Exchange), public clients like SPAs and mobile apps used the Implicit Grant, which returned the access token directly in the URL fragment. This approach had serious security issues: 

  * Access tokens leaked via browser history



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Tokens were accessible to JavaScript in the same origin 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. No way to verify the authorization code exchange came from the legitimate client 

PKCE eliminates these issues by introducing a cryptographic challenge-verifier pair. 

PKCE Flow Step by Step 

Step 1: Generate Code Verifier and Challenge 

The client generates a cryptographically random string called the code verifier, then creates a SHA-256 hash (the code challenge). 

function generateCodeVerifier() {

const array = new Uint8Array(32);

crypto.getRandomValues(array);

return base64URLEncode(array);

}

async function generateCodeChallenge(verifier) {

const encoder = new TextEncoder();

const data = encoder.encode(verifier);

const digest = await crypto.subtle.digest('SHA-256', data);

return base64URLEncode(new Uint8Array(digest));

}

function base64URLEncode(buffer) {

return btoa(String.fromCharCode(...new Uint8Array(buffer)))

.replace(/\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\+/g, '-')

.replace(/\//g, '_')

.replace(/=+$/, '');

}

Step 2: Redirect to Authorization Server 

The client redirects the user to the authorization server, including the code challenge and the method used (`S256`). 

https://auth.example.com/authorize?

response_type=code&

client_id=YOUR_CLIENT_ID&

redirect_uri=https://yourapp.com/callback&

code_challenge=YOUR_SHA256_CHALLENGE&

code_challenge_method=S256&

state=CSRF_TOKEN

The `state` parameter is a CSRF token that must be verified when the user returns. 

Step 3: User Authenticates and Consents 

The authorization server authenticates the user, presents a consent screen, and redirects back to the client with a temporary authorization code. 

https://yourapp.com/callback?code=AUTH_CODE&state;=CSRF_TOKEN

The client must verify that the `state` parameter matches what it sent. 

Step 4: Exchange Code for Token 

The client sends the authorization code along with the original plain-text code verifier to the token endpoint. 

curl -X POST https://auth.example.com/token \

-H "Content-Type: application/x-www-form-urlencoded" \

-d "grant_type=authorization_code" \

-d "code=AUTH_CODE" \

-d "redirect_uri=https://yourapp.com/callback" \

-d "client_id=YOUR_CLIENT_ID" \

-d "code_verifier=ORIGINAL_VERIFIER"

The authorization server computes the SHA-256 hash of the verifier and compares it to the challenge received in step 2. If they match, it issues tokens. 

{

"access_token": "eyJhbGciOiJSUzI1NiIs...",

"token_type": "Bearer",

"expires_in": 3600,

"refresh_token": "dGhpcyBpcyBhIHJlZnJl...",

"scope": "openid profile email"

}

Why PKCE Is Secure 

Without PKCE, an intercepted authorization code could be exchanged by an attacker. With PKCE, the attacker would also need the original code verifier, which was never transmitted during the authorization step. Since only the legitimate client possesses the verifier, the exchange is secure even over an insecure channel. 

Refresh Tokens with PKCE 

Refresh tokens extend access without requiring the user to re-authenticate. When the access token expires, the client uses the refresh token to obtain a new one: 

curl -X POST https://auth.example.com/token \

-H "Content-Type: application/x-www-form-urlencoded" \

-d "grant_type=refresh_token" \

-d "refresh_token=REFRESH_TOKEN" \

-d "client_id=YOUR_CLIENT_ID"

Best Practices 

  * Always use PKCE for SPAs and mobile apps. Never use the Implicit Grant.

  * Store tokens in memory for SPAs, never in localStorage or sessionStorage.

  * Use short-lived access tokens (15-60 minutes) with longer-lived refresh tokens.

  * Implement token rotation for refresh tokens to detect theft.

  * Validate the `state` parameter to prevent CSRF attacks on the callback.

  * Use the `S256` challenge method instead of `plain`.

  * Never log tokens or authorization codes in server logs.




Summary 

PKCE transforms the authorization code flow into a secure protocol for public clients by adding a cryptographic binding between the authorization request and the token exchange. Its proof-of-possession model ensures that even if the authorization code is intercepted, it cannot be exchanged without the original verifier. For any new application, the PKCE-authorized code flow is the recommended OAuth 2.0 grant type.

**See also:** [Incident Response Playbook for Developers](</en/security/incident-response.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>), [RBAC Authorization Implementation](</en/security/rbac-authorization.html>).

**See also:** [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Incident Response Playbook for Developers](</en/security/incident-response.html>), [Cloud Security Basics: Shared Responsibility Model Explained](</en/security/cloud-security-basics.html>)

**See also:** [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Incident Response Playbook for Developers](</en/security/incident-response.html>), [Cloud Security Basics: Shared Responsibility Model Explained](</en/security/cloud-security-basics.html>)

**See also:** [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Incident Response Playbook for Developers](</en/security/incident-response.html>), [Cloud Security Basics: Shared Responsibility Model Explained](</en/security/cloud-security-basics.html>)

**See also:** [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Incident Response Playbook for Developers](</en/security/incident-response.html>), [Cloud Security Basics: Shared Responsibility Model Explained](</en/security/cloud-security-basics.html>)

**See also:** [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Incident Response Playbook for Developers](</en/security/incident-response.html>), [Cloud Security Basics: Shared Responsibility Model Explained](</en/security/cloud-security-basics.html>)

**See also:** [Security Log Management](</en/security/log-management-security.html>), [Password Hashing Algorithms Compared](</en/security/password-hashing.html>), [RBAC Authorization Implementation](</en/security/rbac-authorization.html>)

**See also:** [Security Log Management](</en/security/log-management-security.html>), [Password Hashing Algorithms Compared](</en/security/password-hashing.html>), [RBAC Authorization Implementation](</en/security/rbac-authorization.html>)

**See also:** [Security Log Management](</en/security/log-management-security.html>), [Password Hashing Algorithms Compared](</en/security/password-hashing.html>), [RBAC Authorization Implementation](</en/security/rbac-authorization.html>)

**See also:** [Security Log Management](</en/security/log-management-security.html>), [Password Hashing Algorithms Compared](</en/security/password-hashing.html>), [RBAC Authorization Implementation](</en/security/rbac-authorization.html>)

**See also:** [Security Log Management](</en/security/log-management-security.html>), [Password Hashing Algorithms Compared](</en/security/password-hashing.html>), [RBAC Authorization Implementation](</en/security/rbac-authorization.html>)
