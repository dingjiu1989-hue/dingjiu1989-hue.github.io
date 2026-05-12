---
title: "Output Encoding: Cross-Site Scripting (XSS) Prevention Guide"
description: "Master output encoding for XSS prevention: context-aware encoding, HTML/JS/URL/CSS contexts, and defense-in-depth strategies."
date: 2026-05-12
board: security
url: https://dingjiu1989-hue.github.io/en/security/output-encoding.html
---

# Output Encoding: Cross-Site Scripting (XSS) Prevention Guide

Output encoding is the strongest defense against Cross-Site Scripting (XSS). It transforms untrusted data into a safe representation before inserting it into an HTML page. When done correctly for each output context, it neutralizes even sophisticated injection attacks.

## Why Encoding Matters

XSS happens when user-controlled data is inserted into a web page without proper encoding. An attacker who submits `<script>alert(1)</script>` as their username expects the browser to execute that script. Output encoding converts `<` to `&lt;` and `>` to `&gt;`, rendering the attack inert — the browser displays the text literally instead of executing it.

Encoding must be context-aware. The same data needs different encoding depending on where it appears: HTML body, HTML attribute, JavaScript string, URL parameter, or CSS. Using the wrong encoder for the context leaves an opening for attackers.

## HTML Body Context

Data inserted between HTML tags needs HTML entity encoding. The critical characters are `<`, `>`, `&`, `"`, and `'`. Most frameworks handle this automatically through template engines.

```
import html
safe_output = html.escape(user_input)
# "<script>alert(1)</script>" becomes "&lt;script&gt;alert(1)&lt;/script&gt;"
```

Template engines like Jinja2, ERB, and Thymeleaf auto-escape by default. This handles 80% of encoding needs. Verify that auto-escaping is enabled and never disable it without a documented reason.

## HTML Attribute Context

Attribute encoding is stricter than body encoding. In addition to the standard entities, you must encode spaces, equals signs, and backticks. Unquoted attributes are particularly dangerous — avoid them entirely.

```
def encode_html_attribute(value):
    value = value.replace('&', '&amp;')
    value = value.replace('"', '&quot;')
    value = value.replace("'", '&#x27;')
    value = value.replace('<', '&lt;')
    value = value.replace('>', '&gt;')
    value = value.replace('/', '&#x2F;')
    value = value.replace('`', '&#x60;')
    return value
```

Always quote HTML attributes. Never construct HTML by concatenating strings — use the DOM API or a template engine.

## JavaScript Context

Data inserted into JavaScript requires JSON encoding or hex entity encoding. Never insert untrusted data directly into a `<script>` block.

```
import json
safe_js = json.dumps(user_input)
# "</script><script>alert(1)</script>" becomes
# "<\/script><script>alert(1)<\/script>"
```

Avoid inline event handlers (`onclick`, `onerror`) with dynamic data. Use `addEventListener` instead. If you must embed server data in JavaScript, use JSON script tags with CSP nonces.

## URL Context

Data inserted into URLs must be percent-encoded, which is different from HTML encoding.

```
from urllib.parse import quote
safe_url = quote(user_input, safe='')
```

Validate URL protocols before encoding. Only allow `http:` and `https:` for href attributes. Block `javascript:`, `data:`, and `vbscript:` protocols.

## CSS Context

CSS injection can exfiltrate data through attribute selectors and background-image URLs. The safest approach is to avoid inserting user data into CSS entirely. Use CSS custom properties with predefined values instead of inline styles.

```
import re
def encode_css(value):
    if not re.match(r'^[a-zA-Z0-9\s\-_.#]+$', value):
        raise ValueError("Unsafe CSS value")
    return value
```

## Nested Contexts

The hardest case: data that passes through multiple contexts. A URL inside a JavaScript string inside an HTML attribute requires three layers of encoding. Each layer demands the correct encoder. Simplify by avoiding nested contexts — use data attributes and DOM manipulation instead of inline handlers.

## Defense in Depth

Encoding is your last line of defense. Validate input at the boundary using strict allowlists. Use Content Security Policy (CSP) to block inline scripts. Set `HttpOnly` and `Secure` flags on cookies. Deploy a WAF for an additional security layer.

Output encoding remains essential because validation alone cannot catch every attack vector. Encode all output, in the correct context, every time.
