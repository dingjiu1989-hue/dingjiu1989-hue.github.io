---
title: "MFA Implementation"
description: "Implementing multi-factor authentication with TOTP, SMS, push notifications, and backup codes."
date: 2026-03-18
board: security
url: https://dingjiu1989-hue.github.io/en/security/mfa-implementation.html
---

# MFA Implementation

## MFA Implementation

### MFA Implementation

#### MFA Implementation

#### MFA Implementation

#### MFA Implementation

#### MFA Implementation

#### MFA Implementation

#### MFA Implementation

#### MFA Implementation

#### MFA Implementation

#### MFA Implementation

#### MFA Implementation

#### MFA Implementation

#### MFA Implementation

#### MFA Implementation

MFA Fundamentals 

Multi-factor authentication requires two or more factors: something you know (password), something you have (phone), or something you are (biometric). 

TOTP Implementation 

Time-based One-Time Passwords (TOTP) are the most widely deployed MFA method: 

import pyotp

import qrcode

import io

import base64

class TOTPManager:

def **init**(self, issuer="Example Corp"):

self.issuer = issuer

def generate_secret(self):

return pyotp.random_base32()

def get_provisioning_uri(self, email, secret):

totp = pyotp.TOTP(secret)

return totp.provisioning_uri(name=email, issuer_name=self.issuer)

def generate_qr(self, email, secret):

uri = self.get_provisioning_uri(email, secret)

qr = qrcode.make(uri)

buf = io.BytesIO()

qr.save(buf, format="PNG")

return base64.b64encode(buf.getvalue()).decode()

def verify_code(self, secret, code):

totp = pyotp.TOTP(secret)

#### Allow 1 step before/after for clock drift

return totp.verify(code, valid_window=1)

def get_current_code(self, secret):

totp = pyotp.TOTP(secret)

return totp.now()

SMS-Based MFA 

import random

import string

class SMSMFAManager:

def **init**(self, sms_provider):

self.sms_provider = sms_provider

self.codes = {} # phone -> {code, expires_at}

def send_code(self, phone):

code = ''.join(random.choices(string.digits, k=6))

expiry = datetime.utcnow() + timedelta(minutes=5)

self.codes[phone] = {"code": code, "expires_at": expiry}

self.sms_provider.send(phone, f"Your code is: {code}")

return True

def verify_code(self, phone, code):

stored = self.codes.get(phone)

if not stored:

return False

if datetime.utcnow() > stored["expires_at"]:

del self.codes[phone]

return False

if stored["code"] != code:

return False

del self.codes[phone]

return True

Push Notification MFA 

// Server-side push notification

async function sendPushChallenge(userId, deviceToken) {

const challenge = crypto.randomUUID();

// Store challenge

await redis.set(

`mfa:push:${challenge}`,

userId,

"EX",

120 // 2 minute expiry

);

// Send push notification

await admin.messaging().send({

token: deviceToken,

data: {

type: "MFA_CHALLENGE",

challenge: challenge,

appName: "Example App",

timestamp: Date.now().toString()

}

});

return challenge;

}

// Client-side approval

async function respondToChallenge(challengeId, approved) {

await fetch("/api/auth/mfa/push/respond", {

method: "POST",

body: JSON.stringify({

challenge: challengeId,

approved: approved,

deviceId: deviceId

})

});

}

Backup Codes 

Always provide backup codes when users enroll in MFA: 

def generate_backup_codes(count=10):

codes = []

for _ in range(count):

code = '-'.join([

''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

for _ in range(3)

])

hashed = hashlib.sha256(code.encode()).hexdigest()

codes.append({"raw": code, "hashed": hashed})

return codes

Enforcement Strategy 

mfa_enforcement:

all_users: true

grace_period: 30_days

exclude_service_accounts: true

risk_based_prompting:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- new_device: prompt_mfa

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- new_location: prompt_mfa

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- sensitive_action: require_mfa

recovery:

backup_codes: 10

admin_recovery: "verify_with_id"

recovery_timeout: 24_hours

Conclusion 

MFA is essential but must be implemented thoughtfully. TOTP offers the best balance of security and usability. Provide backup codes during enrollment. Consider risk-based prompting rather than requiring MFA on every request. Guide users toward authenticator apps over SMS when possible.

**See also:** [Two-Factor Authentication Guide](</en/security/two-factor-authentication.html>), [Passwordless Authentication](</en/security/passwordless-auth.html>), [OAuth2 Implementation](</en/security/oauth2-implementation.html>).

**See also:** [Web Application Firewall Implementation](</en/security/waf-implementation.html>), [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [Passwordless Authentication](</en/security/passwordless-auth.html>)

**See also:** [Web Application Firewall Implementation](</en/security/waf-implementation.html>), [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [Passwordless Authentication](</en/security/passwordless-auth.html>)

**See also:** [Web Application Firewall Implementation](</en/security/waf-implementation.html>), [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [Passwordless Authentication](</en/security/passwordless-auth.html>)

**See also:** [Web Application Firewall Implementation](</en/security/waf-implementation.html>), [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [Passwordless Authentication](</en/security/passwordless-auth.html>)

**See also:** [Web Application Firewall Implementation](</en/security/waf-implementation.html>), [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [Passwordless Authentication](</en/security/passwordless-auth.html>)
