---
title: "Two-Factor Authentication Guide"
description: "A comprehensive guide to implementing two-factor authentication with TOTP, SMS, backup codes, and WebAuthn passkeys."
date: 2026-05-20
board: security
url: https://aidev.fit/en/security/two-factor-authentication.html
---

# Two-Factor Authentication Guide

Why 2FA Matters 

Passwords alone are insufficient. Data breaches expose billions of credentials annually, phishing campaigns trick users into revealing their passwords, and credential stuffing attacks automate login attempts across services. Two-factor authentication (2FA) adds a second layer of verification that renders stolen passwords useless. 

2FA Factor Types 

| Factor | Examples | Security Level | |--------|----------|----------------| | Knowledge | Password, PIN | Weak | | Possession | Phone, hardware key, authenticator app | Strong | | Inherence | Fingerprint, face scan | Strong | | Location | GPS, IP range | Moderate | | Time | One-time codes | Moderate | 

Strong 2FA combines something you know (password) with something you have (phone or key). 

TOTP (Time-Based One-Time Password) 

TOTP is the most widely implemented 2FA method. The client and server share a secret key, and both derive the same 6-8 digit code from the current time. 

Server-Side Implementation 

import pyotp

import base64

import os

class TOTPManager:

def **init**(self):

self.issuer = "MyApp"

def generate_secret(self):

"""Generate a new TOTP secret."""

return pyotp.random_base32()

def get_provisioning_uri(self, username, secret):

"""Generate URI for QR code."""

return pyotp.totp.TOTP(secret).provisioning_uri(

name=username,

issuer_name=self.issuer

)

def verify_code(self, secret, code):

"""Verify a TOTP code with a 1-step window for clock drift."""

totp = pyotp.TOTP(secret)

return totp.verify(code, valid_window=1)

Displaying the QR Code 

import qrcode

import qrcode.image.svg

def render_qr(uri):

img = qrcode.make(uri, image_factory=qrcode.image.svg.SvgImage)

return img.to_string().decode()

Client-Side Setup 

// Generate QR in the browser

const secret = await generateTOTPSecret();

const uri = `otpauth://totp/MyApp:${username}?secret=${secret}&issuer;=MyApp`;

// Show QR code

new QRCode(document.getElementById('qrcode'), { text: uri });

// Verify setup

const result = await fetch('/api/2fa/verify', {

method: 'POST',

body: JSON.stringify({ secret, code: userInputCode })

});

SMS-Based 2FA 

While less secure than TOTP (vulnerable to SIM swapping), SMS remains widely used due to its simplicity. 

import twilio

from twilio.rest import Client

def send_sms_code(phone_number):

code = ''.join(random.choices('0123456789', k=6))

## Store code with expiry in Redis

redis.setex(f"2fa:{phone_number}", 300, code)

client = Client(TWILIO_SID, TWILIO_TOKEN)

client.messages.create(

body=f"Your verification code is: {code}",

from_=TWILIO_PHONE,

to=phone_number

)

return code

Backup Codes 

When users lose access to their 2FA device, backup codes provide a recovery path. Generate 8-10 single-use codes: 

import hashlib

import secrets

def generate_backup_codes(count=10):

codes = []

hashes = []

for _ in range(count):

code = f"{secrets.randbelow(10**8):08d}"

codes.append(code)

hashes.append(hashlib.sha256(code.encode()).hexdigest())

return codes, hashes

Store only the SHA-256 hashes of backup codes in the database. When a user enters a backup code, hash it and compare against stored hashes, then remove the used hash. 

WebAuthn and Passkeys 

WebAuthn is the gold standard for 2FA. It uses public-key cryptography: the private key never leaves the user's device, and the server stores only the public key. 

Registration 

// Server sends challenge

const challenge = await getWebAuthnChallenge();

// Browser creates credential

const credential = await navigator.credentials.create({

publicKey: {

challenge: Uint8Array.from(challenge, c => c.charCodeAt(0)),

rp: { name: "MyApp", id: "example.com" },

user: {

id: Uint8Array.from(userId, c => c.charCodeAt(0)),

name: username,

displayName: displayName

},

pubKeyCredParams: [{ type: "public-key", alg: -7 }], // ES256

authenticatorSelection: { userVerification: "required" }

}

});

// Send credential to server for storage

await registerCredential(credential);

Authentication 

const assertion = await navigator.credentials.get({

publicKey: {

challenge: Uint8Array.from(challenge, c => c.charCodeAt(0)),

allowCredentials: credentials.map(c => ({

id: Uint8Array.from(c.credentialId, c => c.charCodeAt(0)),

type: 'public-key'

})),

userVerification: 'required'

}

});

await verifyAssertion(assertion);

Rate Limiting 2FA Attempts 

2FA endpoints are targets for brute-force attacks. Always rate limit: 

| Endpoint | Limit | Window | |----------|-------|--------| | TOTP verification | 5 attempts | 15 minutes | | SMS send | 3 requests | 30 minutes | | Backup code use | 10 attempts | 1 hour | | Recovery request | 3 attempts | 24 hours | 

User Experience Best Practices 

  * Allow users to register multiple 2FA methods (TOTP + backup codes + passkey).

  * Provide a recovery workflow with backup codes during initial setup.

  * Remember trusted devices with a cookie so 2FA is not required on every login.

  * Send notification emails when 2FA is enabled, disabled, or recovery codes are used.

  * Show which 2FA methods are registered in the security settings page.




Summary 

Implement TOTP as the primary 2FA method, supplement with backup codes for recovery, and offer WebAuthn/passkeys as an upgrade path for security-conscious users. Always rate limit 2FA endpoints, hash backup codes before storage, and provide clear recovery workflows. SMS-based 2FA is better than no 2FA but should be deprecated in favor of app-based or hardware-based authenticators.

**See also:** [MFA Implementation](</en/security/mfa-implementation.html>), [API Rate Limiting Implementation](</en/security/api-rate-limiting.html>), [Encryption at Rest Guide](</en/security/encryption-at-rest.html>).

**See also:** [MFA Implementation](</en/security/mfa-implementation.html>), [API Rate Limiting Implementation](</en/security/api-rate-limiting.html>), [RBAC Authorization Implementation](</en/security/rbac-authorization.html>)

**See also:** [MFA Implementation](</en/security/mfa-implementation.html>), [API Rate Limiting Implementation](</en/security/api-rate-limiting.html>), [RBAC Authorization Implementation](</en/security/rbac-authorization.html>)

**See also:** [MFA Implementation](</en/security/mfa-implementation.html>), [API Rate Limiting Implementation](</en/security/api-rate-limiting.html>), [RBAC Authorization Implementation](</en/security/rbac-authorization.html>)

**See also:** [MFA Implementation](</en/security/mfa-implementation.html>), [API Rate Limiting Implementation](</en/security/api-rate-limiting.html>), [RBAC Authorization Implementation](</en/security/rbac-authorization.html>)

**See also:** [MFA Implementation](</en/security/mfa-implementation.html>), [API Rate Limiting Implementation](</en/security/api-rate-limiting.html>), [RBAC Authorization Implementation](</en/security/rbac-authorization.html>)

**See also:** [Passwordless Authentication](</en/security/passwordless-auth.html>), [Data Loss Prevention (DLP) Strategies](</en/security/data-loss-prevention.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)

**See also:** [Passwordless Authentication](</en/security/passwordless-auth.html>), [Data Loss Prevention (DLP) Strategies](</en/security/data-loss-prevention.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)

**See also:** [Passwordless Authentication](</en/security/passwordless-auth.html>), [Data Loss Prevention (DLP) Strategies](</en/security/data-loss-prevention.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)

**See also:** [Passwordless Authentication](</en/security/passwordless-auth.html>), [Data Loss Prevention (DLP) Strategies](</en/security/data-loss-prevention.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)

**See also:** [Passwordless Authentication](</en/security/passwordless-auth.html>), [Data Loss Prevention (DLP) Strategies](</en/security/data-loss-prevention.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)

**See also:** [Passwordless Authentication](</en/security/passwordless-auth.html>), [Data Loss Prevention (DLP) Strategies](</en/security/data-loss-prevention.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)

**See also:** [Passwordless Authentication](</en/security/passwordless-auth.html>), [Data Loss Prevention (DLP) Strategies](</en/security/data-loss-prevention.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)

**See also:** [Passwordless Authentication](</en/security/passwordless-auth.html>), [Data Loss Prevention (DLP) Strategies](</en/security/data-loss-prevention.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)

**See also:** [Passwordless Authentication](</en/security/passwordless-auth.html>), [Data Loss Prevention (DLP) Strategies](</en/security/data-loss-prevention.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)

**See also:** [Passwordless Authentication](</en/security/passwordless-auth.html>), [Data Loss Prevention (DLP) Strategies](</en/security/data-loss-prevention.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)

**See also:** [Passwordless Authentication](</en/security/passwordless-auth.html>), [Data Loss Prevention (DLP) Strategies](</en/security/data-loss-prevention.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)

**See also:** [Passwordless Authentication](</en/security/passwordless-auth.html>), [Data Loss Prevention (DLP) Strategies](</en/security/data-loss-prevention.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)

**See also:** [Passwordless Authentication](</en/security/passwordless-auth.html>), [Data Loss Prevention (DLP) Strategies](</en/security/data-loss-prevention.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)

**See also:** [Passwordless Authentication](</en/security/passwordless-auth.html>), [Data Loss Prevention (DLP) Strategies](</en/security/data-loss-prevention.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)

**See also:** [Passwordless Authentication](</en/security/passwordless-auth.html>), [Data Loss Prevention (DLP) Strategies](</en/security/data-loss-prevention.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)

**See also:** [Passwordless Authentication](</en/security/passwordless-auth.html>), [Data Loss Prevention (DLP) Strategies](</en/security/data-loss-prevention.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)

**See also:** [Passwordless Authentication](</en/security/passwordless-auth.html>), [Data Loss Prevention (DLP) Strategies](</en/security/data-loss-prevention.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)
