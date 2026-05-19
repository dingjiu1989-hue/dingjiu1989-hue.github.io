---
title: "Content Security Policy"
description: "Complete guide to Content Security Policy covering directives, nonce/hash strategies, reporting mechanisms, and strict CSP migration."
date: 2026-03-09
board: security
url: https://dingjiu1989-hue.github.io/en/security/content-security-policy.html
---

# Content Security Policy

Introduction 

Content Security Policy (CSP) is a browser security mechanism that mitigates Cross-Site Scripting (XSS), data injection, and clickjacking attacks. By defining a whitelist of trusted content sources, CSP prevents the browser from executing malicious scripts or loading unauthorized resources. 

CSP Directives 

CSP uses HTTP headers with directives that control specific resource types. 

Content-Security-Policy: 

default-src 'self';

script-src 'self' https://cdn.trusted.com;

style-src 'self' 'unsafe-inline';

img-src 'self' data: https://*.cloudfront.net;

connect-src 'self' https://api.example.com;

font-src 'self' https://fonts.gstatic.com;

frame-src 'none';

object-src 'none';

base-uri 'self';

form-action 'self';

Key directives: 

| Directive | Controls | Example | |-----------|----------|---------| | `default-src` | Fallback for all resource types | `default-src 'self'` | | `script-src` | JavaScript sources | `script-src 'self' https://cdn.example.com` | | `style-src` | CSS sources | `style-src 'self' 'unsafe-inline'` | | `img-src` | Image sources | `img-src 'self' data:` | | `connect-src` | XMLHttpRequest, fetch, WebSocket | `connect-src 'self'` | | `frame-ancestors` | Parent page framing | `frame-ancestors 'none'` | | `form-action` | Form submission targets | `form-action 'self'` | | `base-uri` | `` tag URLs |`base-uri 'self'` | 

Nonce and Hash Strategies 

Using `'unsafe-inline'` for scripts weakens CSP. Nonce and hash strategies provide secure inline script handling. 

Nonce-Based CSP 

A nonce is a cryptographically random token generated per-request and included in both the CSP header and the script tag. 

import secrets

from flask import Flask, render_template

app = Flask(**name**)

@app.route('/')

def index():

nonce = secrets.token_urlsafe(16)

response = make_response(render_template('index.html', nonce=nonce))

response.headers['Content-Security-Policy'] = \

f"script-src 'nonce-{nonce}'; object-src 'none'; base-uri 'self'"

return response

Hash-Based CSP 

For static inline scripts, use a hash of the script content instead of a nonce. 

import hashlib

import base64

def generate_script_hash(script_content):

hash_bytes = hashlib.sha256(script_content.encode()).digest()

hash_b64 = base64.b64encode(hash_bytes).decode()

return f"'sha256-{hash_b64}'"

## Generate once, add to CSP

script = "document.getElementById('app').innerHTML = '

Hello

';"

script_hash = generate_script_hash(script)

## CSP: script-src 'sha256-abc123...'

Content-Security-Policy: 

script-src 'sha256-abc123def456...';

object-src 'none';

CSP Reporting 

CSP violations can be reported to an endpoint for monitoring and debugging. 

Content-Security-Policy: 

default-src 'self';

script-src 'self';

report-uri /csp-violation-report;

report-to csp-endpoint;

{

"csp-report": {

"document-uri": "https://example.com/page",

"referrer": "",

"blocked-uri": "https://evil.com/script.js",

"violated-directive": "script-src 'self'",

"effective-directive": "script-src",

"original-policy": "default-src 'self'; script-src 'self'",

"source-file": "https://example.com/page",

"line-number": 42,

"column-number": 10

}

}

## Flask CSP report collector

@app.route('/csp-violation-report', methods=['POST'])

def csp_report():

report = request.get_json(force=True)

blocked = report['csp-report']['blocked-uri']

directive = report['csp-report']['violated-directive']

page = report['csp-report']['document-uri']

## Log to security monitoring

security_logger.warning(

f"CSP violation on {page}: {directive} blocked {blocked}"

)

## Alert if critical pattern

if 'exfiltration' in blocked.lower():

security_logger.critical(f"Potential data exfiltration: {blocked}")

return '', 204

Strict CSP Migration 

Migrating from allowlist CSP to strict CSP provides better security. 

## Allowlist CSP (vulnerable to CDN-based bypass)

Content-Security-Policy: 

script-src 'self' https://ajax.googleapis.com https://cdnjs.cloudflare.com;

## Strict CSP (nonce-based, resistant to bypass)

Content-Security-Policy: 

script-src 'nonce-random123' 'strict-dynamic' https: 'unsafe-inline';

object-src 'none';

base-uri 'none';

The `'strict-dynamic'` keyword propagates trust from nonced scripts to their dynamically loaded children, enabling modern SPA frameworks while maintaining security. 

Deployment Strategy 

## Step 1: Deploy in report-only mode

Content-Security-Policy-Report-Only: 

default-src 'self';

script-src 'nonce-abc123';

report-uri /csp-reports;

## Step 2: Monitor reports for 2-4 weeks

## Step 3: Fix violations identified in reports

## Step 4: Switch to enforcement mode

Content-Security-Policy:

default-src 'self';

script-src 'nonce-abc123';

report-uri /csp-reports;

## Step 5: Gradually remove report-uri when confident

Conclusion 

CSP is one of the most powerful defense-in-depth mechanisms against XSS. Use nonce-based strict CSP rather than allowlist-based policies, deploy in report-only mode initially to identify violations, always set `object-src 'none'` and `base-uri 'self'` as hardening measures, and monitor reports continuously for policy violations and potential attacks.

**See also:** [Infrastructure as Code Security](</en/security/iac-security.html>), [Clickjacking Protection](</en/security/clickjacking-protection.html>), [Session Management Security](</en/security/session-management.html>).

**See also:** [Clickjacking Protection](</en/security/clickjacking-protection.html>), [Email Security](</en/security/email-security.html>), [Infrastructure as Code Security](</en/security/iac-security.html>)

**See also:** [Clickjacking Protection](</en/security/clickjacking-protection.html>), [Email Security](</en/security/email-security.html>), [Infrastructure as Code Security](</en/security/iac-security.html>)

**See also:** [Clickjacking Protection](</en/security/clickjacking-protection.html>), [Email Security](</en/security/email-security.html>), [Infrastructure as Code Security](</en/security/iac-security.html>)

**See also:** [Clickjacking Protection](</en/security/clickjacking-protection.html>), [Email Security](</en/security/email-security.html>), [Infrastructure as Code Security](</en/security/iac-security.html>)

**See also:** [Clickjacking Protection](</en/security/clickjacking-protection.html>), [Email Security](</en/security/email-security.html>), [Infrastructure as Code Security](</en/security/iac-security.html>)

**See also:** [Cloud Security Posture Management](</en/security/cloud-security-posture.html>), [Container Image Security](</en/security/container-image-security.html>), [CORS Security](</en/security/cors-security.html>)

**See also:** [Cloud Security Posture Management](</en/security/cloud-security-posture.html>), [Container Image Security](</en/security/container-image-security.html>), [CORS Security](</en/security/cors-security.html>)

**See also:** [Cloud Security Posture Management](</en/security/cloud-security-posture.html>), [Container Image Security](</en/security/container-image-security.html>), [CORS Security](</en/security/cors-security.html>)

**See also:** [Cloud Security Posture Management](</en/security/cloud-security-posture.html>), [Container Image Security](</en/security/container-image-security.html>), [CORS Security](</en/security/cors-security.html>)

**See also:** [Cloud Security Posture Management](</en/security/cloud-security-posture.html>), [Container Image Security](</en/security/container-image-security.html>), [CORS Security](</en/security/cors-security.html>)

**See also:** [Cloud Security Posture Management](</en/security/cloud-security-posture.html>), [Container Image Security](</en/security/container-image-security.html>), [CORS Security](</en/security/cors-security.html>)
