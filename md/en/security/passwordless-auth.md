---
title: "Passwordless Authentication"
description: "Implementing passwordless authentication with WebAuthn, passkeys, magic links, and FIDO2 standards."
date: 2026-03-18
board: security
url: https://aidev.fit/en/security/passwordless-auth.html
---

# Passwordless Authentication

The Passwordless Vision 

Passwords are the weakest link in authentication. Passwordless authentication eliminates them entirely, replacing secrets with cryptographic keys. 

WebAuthn and FIDO2 

Web Authentication (WebAuthn) is a W3C standard for public-key credential authentication: 

// Registration

async function registerPasskey() {

const credential = await navigator.credentials.create({

publicKey: {

challenge: new Uint8Array([/_server-generated challenge_ /]),

rp: {

id: "example.com",

name: "Example Corp"

},

user: {

id: new TextEncoder().encode("user-123"),

name: "alice@example.com",

displayName: "Alice"

},

pubKeyCredParams: [

{ type: "public-key", alg: -7 }, // ES256

{ type: "public-key", alg: -257 } // RS256

],

authenticatorSelection: {

authenticatorAttachment: "platform",

residentKey: "required",

userVerification: "required"

}

}

});

// Send to server

await fetch("/api/auth/passkey/register", {

method: "POST",

body: JSON.stringify({

id: credential.id,

rawId: arrayBufferToBase64(credential.rawId),

type: credential.type,

response: {

clientDataJSON: arrayBufferToBase64(credential.response.clientDataJSON),

attestationObject: arrayBufferToBase64(credential.response.attestationObject)

}

})

});

}

Server-Side Verification 

from webauthn import generate_registration_options, verify_registration_response

from webauthn.helpers.structs import RegistrationCredential

def start_registration(user):

options = generate_registration_options(

rp_id="example.com",

rp_name="Example Corp",

user_id=str(user.id).encode(),

user_name=user.email,

user_display_name=user.name

)

## Store challenge temporarily

cache.set(f"webauthn:challenge:{user.id}", options.challenge, time=300)

return options

def complete_registration(user, credential_data):

credential = RegistrationCredential(

id=credential_data["id"],

raw_id=credential_data["rawId"],

type=credential_data["type"],

response={

"client_data_json": credential_data["response"]["clientDataJSON"],

"attestation_object": credential_data["response"]["attestationObject"]

}

)

verification = verify_registration_response(

credential=credential,

expected_challenge=cache.get(f"webauthn:challenge:{user.id}"),

expected_rp_id="example.com",

expected_origin="https://example.com"

)

## Store credential for future logins

store_credential(user.id, verification.credential_id, verification.public_key)

Authentication Flow 

// Login with passkey

async function authenticateWithPasskey() {

const credential = await navigator.credentials.get({

publicKey: {

challenge: new Uint8Array([/_server challenge_ /]),

rpId: "example.com",

userVerification: "required"

}

});

const response = await fetch("/api/auth/passkey/authenticate", {

method: "POST",

body: JSON.stringify({

id: credential.id,

rawId: arrayBufferToBase64(credential.rawId),

type: credential.type,

response: {

clientDataJSON: arrayBufferToBase64(credential.response.clientDataJSON),

authenticatorData: arrayBufferToBase64(credential.response.authenticatorData),

signature: arrayBufferToBase64(credential.response.signature),

userHandle: credential.response.userHandle 

? arrayBufferToBase64(credential.response.userHandle) 

: null

}

})

});

if (response.ok) window.location.href = "/dashboard";

}

Magic Links 

For devices without platform authenticators: 

import secrets

from datetime import datetime, timedelta

def send_magic_link(email):

token = secrets.token_urlsafe(32)

expiry = datetime.utcnow() + timedelta(minutes=15)

## Store token

cache.set(f"magic_link:{token}", email, time=900)

## Send email

link = f"https://example.com/auth/magic?token={token}"

send_email(email, "Your login link", f"Click: {link}")

def verify_magic_link(token):

email = cache.get(f"magic_link:{token}")

if email:

cache.delete(f"magic_link:{token}")

return create_session(email)

return None

Conclusion 

Passwordless authentication improves both security and UX. Use WebAuthn with platform authenticators as the primary method, fall back to magic links for cross-device scenarios. Store public keys for verification and never handle private keys server-side. Passkeys sync across devices via platform providers, making them the most practical passwordless solution for 2026.

**See also:** [MFA Implementation](</en/security/mfa-implementation.html>), [Data Classification](</en/security/data-classification.html>), [Database Encryption](</en/security/database-encryption.html>).

**See also:** [MFA Implementation](</en/security/mfa-implementation.html>), [Web Application Firewall Implementation](</en/security/waf-implementation.html>), [Data Classification](</en/security/data-classification.html>)

**See also:** [MFA Implementation](</en/security/mfa-implementation.html>), [Web Application Firewall Implementation](</en/security/waf-implementation.html>), [Data Classification](</en/security/data-classification.html>)

**See also:** [MFA Implementation](</en/security/mfa-implementation.html>), [Web Application Firewall Implementation](</en/security/waf-implementation.html>), [Data Classification](</en/security/data-classification.html>)

**See also:** [MFA Implementation](</en/security/mfa-implementation.html>), [Web Application Firewall Implementation](</en/security/waf-implementation.html>), [Data Classification](</en/security/data-classification.html>)

**See also:** [MFA Implementation](</en/security/mfa-implementation.html>), [Web Application Firewall Implementation](</en/security/waf-implementation.html>), [Data Classification](</en/security/data-classification.html>)

**See also:** [Kubernetes Security](</en/security/kubernetes-security.html>), [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [Secrets Rotation](</en/security/secrets-rotation.html>)

**See also:** [Kubernetes Security](</en/security/kubernetes-security.html>), [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [Secrets Rotation](</en/security/secrets-rotation.html>)

**See also:** [Kubernetes Security](</en/security/kubernetes-security.html>), [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [Secrets Rotation](</en/security/secrets-rotation.html>)

**See also:** [Kubernetes Security](</en/security/kubernetes-security.html>), [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [Secrets Rotation](</en/security/secrets-rotation.html>)

**See also:** [Kubernetes Security](</en/security/kubernetes-security.html>), [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [Secrets Rotation](</en/security/secrets-rotation.html>)

**See also:** [Kubernetes Security](</en/security/kubernetes-security.html>), [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [Secrets Rotation](</en/security/secrets-rotation.html>)

**See also:** [Kubernetes Security](</en/security/kubernetes-security.html>), [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [Secrets Rotation](</en/security/secrets-rotation.html>)

**See also:** [Kubernetes Security](</en/security/kubernetes-security.html>), [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [Secrets Rotation](</en/security/secrets-rotation.html>)

**See also:** [Kubernetes Security](</en/security/kubernetes-security.html>), [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [Secrets Rotation](</en/security/secrets-rotation.html>)

**See also:** [Kubernetes Security](</en/security/kubernetes-security.html>), [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [Secrets Rotation](</en/security/secrets-rotation.html>)

**See also:** [Kubernetes Security](</en/security/kubernetes-security.html>), [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [Secrets Rotation](</en/security/secrets-rotation.html>)

**See also:** [Kubernetes Security](</en/security/kubernetes-security.html>), [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [Secrets Rotation](</en/security/secrets-rotation.html>)

**See also:** [Kubernetes Security](</en/security/kubernetes-security.html>), [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [Secrets Rotation](</en/security/secrets-rotation.html>)

**See also:** [Kubernetes Security](</en/security/kubernetes-security.html>), [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [Secrets Rotation](</en/security/secrets-rotation.html>)

**See also:** [Kubernetes Security](</en/security/kubernetes-security.html>), [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [Secrets Rotation](</en/security/secrets-rotation.html>)

**See also:** [Kubernetes Security](</en/security/kubernetes-security.html>), [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [Secrets Rotation](</en/security/secrets-rotation.html>)

**See also:** [Kubernetes Security](</en/security/kubernetes-security.html>), [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [Secrets Rotation](</en/security/secrets-rotation.html>)
