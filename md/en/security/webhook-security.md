---
title: "Webhook Security Best Practices"
description: "Secure your webhook endpoints with signature verification, replay protection, IP allowlisting, idempotency, and payload validation."
date: 2026-05-11
board: security
url: https://dingjiu1989-hue.github.io/en/security/webhook-security.html
---

# Webhook Security Best Practices

## Webhook Security Best Practices

## Webhook Security Best Practices

## Webhook Security Best Practices

## Webhook Security Best Practices

## Webhook Security Best Practices

## Webhook Security Best Practices

## Webhook Security Best Practices

## Webhook Security Best Practices

## Webhook Security Best Practices

## Webhook Security Best Practices

## Webhook Security Best Practices

## Webhook Security Best Practices

## Webhook Security Best Practices

## Webhook Security Best Practices

Why Webhook Security Matters 

Webhooks are HTTP callbacks that allow services to push real-time events to your application. Unlike APIs where you initiate the request, webhooks are delivered to a public endpoint that anyone with the URL can call. Without proper security, an attacker can replay webhook events, send fake event data, or probe your internal infrastructure. 

Threat Model 

| Threat | Impact | Likelihood | |--------|--------|------------| | Fake webhook events | Application processes false data | High | | Replay attacks | Duplicate processing of legitimate events | Medium | | Payload tampering | Corrupted data processed as valid | Medium | | Reconnaissance | Attacker probes internal network | Low | | DDoS via webhooks | Service overload from fake events | Medium | 

Defense 1: Signature Verification 

Every webhook provider signs their payloads. Your endpoint must verify this signature before processing. 

Stripe-Style Signatures 

import hmac

import hashlib

def verify_stripe_signature(payload, sig_header, secret):

"""Verify Stripe webhook signature."""

## Signature format: t=timestamp,v1=signature

parts = dict(item.split('=', 1) for item in sig_header.split(','))

if 'v1' not in parts or 't' not in parts:

return False

timestamp = parts['t']

expected_sig = parts['v1']

## Prevent replay: signature must be within 5 minutes

if abs(int(timestamp) - time.time()) > 300:

return False

## Compute expected signature

signed_payload = f"{timestamp}.{payload}".encode()

computed_sig = hmac.new(

secret.encode(),

signed_payload,

hashlib.sha256

).hexdigest()

## Constant-time comparison

return hmac.compare_digest(computed_sig, expected_sig)

GitHub-Style Signatures 

const crypto = require('crypto');

function verifyGitHubSignature(req, secret) {

const signature = req.headers['x-hub-signature-256'];

if (!signature) return false;

const payload = JSON.stringify(req.body);

const computed = 'sha256=' +

crypto.createHmac('sha256', secret)

.update(payload)

.digest('hex');

// Constant-time comparison

return crypto.timingSafeEqual(

Buffer.from(signature),

Buffer.from(computed)

);

}

// Express middleware

app.post('/webhooks/github', express.raw({type: 'application/json'}), (req, res) => {

if (!verifyGitHubSignature(req, process.env.GITHUB_WEBHOOK_SECRET)) {

return res.status(401).send('Invalid signature');

}

// Process webhook

res.status(200).send('OK');

});

Generic Verification Middleware 

from functools import wraps

from flask import request, abort

import hmac

import hashlib

def verify_webhook(secret):

"""Decorator to verify webhook signatures."""

def decorator(f):

@wraps(f)

def decorated_function(_args,_ *kwargs):

payload = request.get_data()

received_sig = request.headers.get('X-Webhook-Signature')

if not received_sig:

abort(401, 'Missing signature')

computed_sig = hmac.new(

secret.encode(),

payload,

hashlib.sha256

).hexdigest()

if not hmac.compare_digest(computed_sig, received_sig):

abort(401, 'Invalid signature')

return f(_args,_ *kwargs)

return decorated_function

return decorator

@app.route('/webhooks/custom', methods=['POST'])

@verify_webhook(WEBHOOK_SECRET)

def handle_webhook():

event = request.json

## Process the verified event

return 'OK', 200

Defense 2: Replay Protection 

Timestamp-Based Prevention 

Include a timestamp in the signed payload and reject webhooks outside a time window: 

function verifyWithReplayPrevention(payload, signature, secret, toleranceMs = 300000) {

// Expected format: ts=1234567890,v1=sig_here

const parts = signature.split(',');

const tsPart = parts.find(p => p.startsWith('ts='));

const sigPart = parts.find(p => p.startsWith('v1='));

const timestamp = parseInt(tsPart.split('=')[1]);

const now = Date.now();

// Reject if outside tolerance window

if (Math.abs(now - timestamp) > toleranceMs) {

throw new Error('Webhook replay detected');

}

// Verify signature includes timestamp

const signedContent = `${timestamp}.${JSON.stringify(payload)}`;

const expectedSig = crypto.createHmac('sha256', secret)

.update(signedContent)

.digest('hex');

return crypto.timingSafeEqual(

Buffer.from(expectedSig),

Buffer.from(sigPart.split('=')[1])

);

}

Idempotency Keys 

Track processed webhook IDs to prevent duplicate processing: 

const processedEvents = new Set();

app.post('/webhooks/stripe', async (req, res) => {

const eventId = req.headers['stripe-signature']

.split(',')

.find(p => p.startsWith('t='))

?.split('=')[1];

if (processedEvents.has(eventId)) {

// Already processed, return success to avoid retries

return res.status(200).json({ status: 'already_processed' });

}

// Verify and process

processedEvents.add(eventId);

// Clean old entries periodically

setTimeout(() => processedEvents.delete(eventId), 86400000);

});

Defense 3: IP Allowlisting 

When possible, restrict webhook endpoints to known provider IPs: 

ALLOWED_IPS = {

'stripe': ['3.18.12.63/32', '3.130.192.231/32'],

'github': ['192.30.252.0/22', '185.199.108.0/22'],

'slack': ['52.89.214.238/32', '54.70.199.8/32'],

}

def ip_allowed(provider, request_ip):

import ipaddress

for cidr in ALLOWED_IPS.get(provider, []):

if ipaddress.ip_address(request_ip) in ipaddress.ip_network(cidr):

return True

return False

@app.before_request

def restrict_webhook_ips():

if request.path.startswith('/webhooks/'):

provider = request.path.split('/')[2]

if not ip_allowed(provider, request.remote_addr):

abort(403, 'IP not allowed')

Defense 4: Payload Validation 

Validate the webhook payload schema before processing: 

from pydantic import BaseModel, ValidationError

class GitHubPushEvent(BaseModel):

ref: str

repository: dict

commits: list

sender: dict

forced: bool = False

def validate_webhook_payload(provider, payload):

validators = {

'github': GitHubPushEvent,

'stripe': StripeEvent,

'slack': SlackEvent

}

validator = validators.get(provider)

if not validator:

return False

try:

validator(**payload)

return True

except ValidationError:

return False

Implementation Checklist 

| Security Control | Implementation | Priority | |-----------------|----------------|----------| | HMAC signature verification | Verify every webhook | Critical | | Replay protection | Timestamp + tolerance | Critical | | Idempotency | Track event IDs | High | | IP allowlisting | Restrict by provider CIDR | High | | Payload validation | Schema validation | High | | Rate limiting | Per-IP and per-provider | Medium | | HTTPS only | Reject HTTP | Critical | | Error handling | Generic error messages | Medium | 

Summary 

Webhook endpoints are publicly accessible by design, making them an attractive target. Always verify payload signatures using HMAC-SHA256, implement replay protection with timestamps, track idempotency keys to prevent duplicate processing, validate payload structure, and restrict by IP when possible. These controls turn a publicly accessible endpoint into a secure integration point that only processes legitimate webhook events.

**See also:** [JWT Authentication Best Practices](</en/security/jwt-authentication-guide.html>), [Secure File Upload Implementation](</en/security/secure-file-upload.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>).

**See also:** [JWT Authentication Best Practices](</en/security/jwt-authentication-guide.html>), [Secure File Upload Implementation](</en/security/secure-file-upload.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)

**See also:** [JWT Authentication Best Practices](</en/security/jwt-authentication-guide.html>), [Secure File Upload Implementation](</en/security/secure-file-upload.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)
