---
title: "Clickjacking Protection"
description: "Complete guide to clickjacking defense covering X-Frame-Options, CSP frame-ancestors, framebusting techniques, and testing tools."
date: 2026-05-12
board: security
url: https://dingjiu1989-hue.github.io/en/security/clickjacking-protection.html
---

# Clickjacking Protection

## Clickjacking Protection

## Clickjacking Protection

## Clickjacking Protection

## Clickjacking Protection

## Clickjacking Protection

## Clickjacking Protection

## Clickjacking Protection

## Clickjacking Protection

## Clickjacking Protection

## Clickjacking Protection

## Clickjacking Protection

## Clickjacking Protection

## Clickjacking Protection

## Clickjacking Protection

Introduction 

Clickjacking, also known as a UI redress attack, tricks users into clicking on something different from what they perceive. An attacker embeds a target page in a transparent iframe overlaid on a decoy interface. When the user clicks a visible button, they actually interact with the hidden target page — potentially authorizing a transaction, changing settings, or granting permissions. 

How Clickjacking Works 

A clickjacking exploit involves three elements: 

Click here for a free prize!

The user sees a game or prize button but actually clicks the bank's transfer confirmation. With precise CSS positioning, the attacker makes the real button overlap the decoy. 

X-Frame-Options 

X-Frame-Options is a response header that controls whether a page can be displayed in an iframe. 

## Deny all framing

add_header X-Frame-Options "DENY" always;

## Allow only same-origin framing

add_header X-Frame-Options "SAMEORIGIN" always;

## Flask example: set X-Frame-Options

from flask import Flask, make_response

app = Flask(**name**)

@app.after_request

def set_frame_options(response):

response.headers['X-Frame-Options'] = 'SAMEORIGIN'

return response

## For sensitive pages (banking, admin panels), use DENY

@app.route('/admin/transfer')

def admin_transfer():

response = make_response(render_template('transfer.html'))

response.headers['X-Frame-Options'] = 'DENY'

return response

X-Frame-Options has three values: `DENY` (no framing ever), `SAMEORIGIN` (same-origin only), and `ALLOW-FROM` (deprecated, not supported in modern browsers). 

CSP frame-ancestors 

Content Security Policy's `frame-ancestors` directive supersedes X-Frame-Options with more granular control. It specifies which origins are allowed to embed the page. 

## Allow only same-origin

add_header Content-Security-Policy "frame-ancestors 'self'" always;

## Allow specific origins

add_header Content-Security-Policy "frame-ancestors 'self' https://trusted-app.example.com" always;

## Allow none (equivalent to DENY)

add_header Content-Security-Policy "frame-ancestors 'none'" always;

## Allow multiple specific origins

add_header Content-Security-Policy "frame-ancestors https://app1.example.com https://app2.example.com" always;

When both X-Frame-Options and CSP `frame-ancestors` are present, browsers honor the more restrictive policy. CSP `frame-ancestors` is preferred because it supports multiple origins. 

## Python/Flask CSP middleware

from flask import Flask

from flask_talisman import Talisman

app = Flask(**name**)

Talisman(app, 

content_security_policy={

'frame-ancestors': ["'self'", "https://dashboard.example.com"]

}

)

Framebusting JavaScript 

Client-side framebusting detects if the page is loaded in an iframe and breaks out. However, JavaScript-based protection can be bypassed. 

// Basic framebuster

if (top !== self) {

top.location = self.location;

}

// Robust framebuster with null check

if (top.location !== self.location) {

// In some browsers, accessing top.location throws SecurityError

try {

top.location.href = self.location.href;

} catch (e) {

// If blocked by cross-origin policy, still possible to break out

top.location = self.location;

}

}

// Prevention of iframe-based clickjacking with style override

Framebusting limitations:

  * `sandbox` attribute on iframes can prevent `top.location` modification

  * `noopener` links bypass frame busters

  * Attackers can use `onbeforeunload` to prevent navigation




Testing for Clickjacking Vulnerabilities 

## Test with curl

curl -I https://target-website.com/admin | grep -i "x-frame-options|content-security-policy"

## Check for frame-ancestors specifically

curl -sI https://target-website.com | \

grep -E 'X-Frame-Options|frame-ancestors' || \

echo "NO PROTECTION DETECTED"

## Python automated check

python3 -c "

import requests

urls = [

'https://target.com/login',

'https://target.com/transfer',

'https://target.com/admin',

]

for url in urls:

resp = requests.get(url)

xfo = resp.headers.get('X-Frame-Options', 'MISSING')

csp = resp.headers.get('Content-Security-Policy', '')

fa = 'frame-ancestors' in csp or 'frame-ancestors' not in csp

if 'frame-ancestors' in csp:

print(f'[PROTECTED] {url}: CSP frame-ancestors')

elif xfo in ('DENY', 'SAMEORIGIN'):

print(f'[PROTECTED] {url}: X-Frame-Options: {xfo}')

else:

print(f'[VULNERABLE] {url}: No framing protection')

"

Comprehensive Protection Strategy 

## Nginx: full clickjacking protection

server {

## X-Frame-Options as fallback

add_header X-Frame-Options "SAMEORIGIN" always;

## CSP frame-ancestors as modern replacement

add_header Content-Security-Policy "frame-ancestors 'self'" always;

location /admin/ {

## Stricter for sensitive areas

add_header X-Frame-Options "DENY" always;

add_header Content-Security-Policy "frame-ancestors 'none'" always;

}

location /api/ {

## APIs should never be framed

add_header X-Frame-Options "DENY" always;

add_header Content-Security-Policy "frame-ancestors 'none'" always;

}

}

Conclusion 

Clickjacking is one of the easiest vulnerabilities to prevent but remains surprisingly common. Set `X-Frame-Options: DENY` or `SAMEORIGIN` on every response, and use CSP `frame-ancestors` for fine-grained control. For the strongest protection, deploy both headers, and always test new pages before deployment.

**See also:** [Email Security](</en/security/email-security.html>), [Content Security Policy](</en/security/content-security-policy.html>), [Penetration Testing Methodology](</en/security/penetration-testing.html>).

**See also:** [Email Security](</en/security/email-security.html>), [Content Security Policy](</en/security/content-security-policy.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>)

**See also:** [Email Security](</en/security/email-security.html>), [Content Security Policy](</en/security/content-security-policy.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>)
