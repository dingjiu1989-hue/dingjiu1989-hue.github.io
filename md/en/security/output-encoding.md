---
title: "Output Encoding"
description: "Guide to output encoding covering context-sensitive encoding, XSS prevention, template engine auto-escaping, and common encoding pitfalls."
date: 2026-03-12
board: security
url: https://dingjiu1989-hue.github.io/en/security/output-encoding.html
---

# Output Encoding

## Output Encoding: Cross-Site Scripting (XSS) Prevention Guide

Output encoding is the strongest defense against Cross-Site Scripting (XSS). It transforms untrusted data into a safe representation before inserting it into an HTML page. When done correctly for each output context, it neutralizes even sophisticated injection attacks.

## Why Encoding Matters

XSS happens when user-controlled data is inserted into a web page without proper encoding. An attacker who submits `` as their username expects the browser to execute that script. Output encoding converts`<`to`<`and`>`to`>`, rendering the attack inert — the browser displays the text literally instead of executing it.

Encoding must be context-aware. The same data needs different encoding depending on where it appears: HTML body, HTML attribute, JavaScript string, URL parameter, or CSS. Using the wrong encoder for the context leaves an opening for attackers.

## HTML Body Context

Data inserted between HTML tags needs HTML entity encoding. The critical characters are `<`, `>`, `&`, `"`, and `'`. Most frameworks handle this automatically through template engines.

import html

safe_output = html.escape(user_input)

## "" becomes ""

Template engines like Jinja2, ERB, and Thymeleaf auto-escape by default. This handles 80% of encoding needs. Verify that auto-escaping is enabled and never disable it without a documented reason.

## HTML Attribute Context

Attribute encoding is stricter than body encoding. In addition to the standard entities, you must encode spaces, equals signs, and backticks. Unquoted attributes are particularly dangerous — avoid them entirely.

def encode_html_attribute(value):

value = value.replace('&', '&')

value = value.replace('"', '"')

value = value.replace("'", ''')

value = value.replace('<', '<')

value = value.replace('>', '>')

value = value.replace('/', '/')

value = value.replace('`', '`')

return value

Always quote HTML attributes. Never construct HTML by concatenating strings — use the DOM API or a template engine.

## JavaScript Context

Data inserted into JavaScript requires JSON encoding or hex entity encoding. Never insert untrusted data directly into a `

**See also:** [Input Validation Deep Dive](</en/security/input-validation.html>), [Session Management Security](</en/security/session-management.html>), [CORS Security](</en/security/cors-security.html>).

**See also:** [Input Validation Deep Dive](</en/security/input-validation.html>), [CORS Security](</en/security/cors-security.html>), [Session Management Security](</en/security/session-management.html>)

**See also:** [Input Validation Deep Dive](</en/security/input-validation.html>), [CORS Security](</en/security/cors-security.html>), [Session Management Security](</en/security/session-management.html>)

**See also:** [Input Validation Deep Dive](</en/security/input-validation.html>), [CORS Security](</en/security/cors-security.html>), [Session Management Security](</en/security/session-management.html>)

**See also:** [Input Validation Deep Dive](</en/security/input-validation.html>), [CORS Security](</en/security/cors-security.html>), [Session Management Security](</en/security/session-management.html>)

**See also:** [Input Validation Deep Dive](</en/security/input-validation.html>), [CORS Security](</en/security/cors-security.html>), [Session Management Security](</en/security/session-management.html>)

**See also:** [Clickjacking Protection](</en/security/clickjacking-protection.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>), [Cloud Security Posture Management](</en/security/cloud-security-posture.html>)

**See also:** [Clickjacking Protection](</en/security/clickjacking-protection.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>), [Cloud Security Posture Management](</en/security/cloud-security-posture.html>)

**See also:** [Clickjacking Protection](</en/security/clickjacking-protection.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>), [Cloud Security Posture Management](</en/security/cloud-security-posture.html>)

**See also:** [Clickjacking Protection](</en/security/clickjacking-protection.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>), [Cloud Security Posture Management](</en/security/cloud-security-posture.html>)

**See also:** [Clickjacking Protection](</en/security/clickjacking-protection.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>), [Cloud Security Posture Management](</en/security/cloud-security-posture.html>)

**See also:** [Clickjacking Protection](</en/security/clickjacking-protection.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>), [Cloud Security Posture Management](</en/security/cloud-security-posture.html>)

**See also:** [Clickjacking Protection](</en/security/clickjacking-protection.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>), [Cloud Security Posture Management](</en/security/cloud-security-posture.html>)

**See also:** [Clickjacking Protection](</en/security/clickjacking-protection.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>), [Cloud Security Posture Management](</en/security/cloud-security-posture.html>)

**See also:** [Clickjacking Protection](</en/security/clickjacking-protection.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>), [Cloud Security Posture Management](</en/security/cloud-security-posture.html>)

**See also:** [Clickjacking Protection](</en/security/clickjacking-protection.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>), [Cloud Security Posture Management](</en/security/cloud-security-posture.html>)

**See also:** [Clickjacking Protection](</en/security/clickjacking-protection.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>), [Cloud Security Posture Management](</en/security/cloud-security-posture.html>)

**See also:** [Clickjacking Protection](</en/security/clickjacking-protection.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>), [Cloud Security Posture Management](</en/security/cloud-security-posture.html>)
