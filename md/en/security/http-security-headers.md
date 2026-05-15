---
title: "HTTP Security Headers Checklist"
description: "A complete checklist of HTTP security headers to protect your web application from XSS, clickjacking, MIME sniffing, and other attacks."
date: 2026-05-11
board: security
url: https://dingjiu1989-hue.github.io/en/security/http-security-headers.html
---

# HTTP Security Headers Checklist

# HTTP Security Headers Checklist

# HTTP Security Headers Checklist

# HTTP Security Headers Checklist

# HTTP Security Headers Checklist

# HTTP Security Headers Checklist

# HTTP Security Headers Checklist

# HTTP Security Headers Checklist

# HTTP Security Headers Checklist

# HTTP Security Headers Checklist

# HTTP Security Headers Checklist

# HTTP Security Headers Checklist

# HTTP Security Headers Checklist

# HTTP Security Headers Checklist

Why Security Headers Matter 

HTTP security headers are the first line of defense for any web application. They tell the browser how to behave when rendering your content, preventing a wide range of attacks including cross-site scripting (XSS), clickjacking, MIME-type sniffing, and protocol downgrade attacks. Many of these headers are easy to implement yet remain missing on the majority of production websites. 

Essential Headers 

Strict-Transport-Security 

Forces all communication to use HTTPS, preventing man-in-the-middle attacks and protocol downgrades. 

Strict-Transport-Security: max-age=63072000; includeSubDomains; preload

Set `max-age` to at least 1 year (31536000 seconds) once you are confident HTTPS is stable. `includeSubDomains` extends protection to all subdomains. `preload` allows your domain to be included in browser preload lists. 

Content-Security-Policy 

The most powerful defense against XSS attacks. CSP restricts which resources the browser can load and execute. 

Content-Security-Policy: default-src 'self';

script-src 'self' https://analytics.example.com;

style-src 'self' 'unsafe-inline';

img-src 'self' data: https:;

font-src 'self' https://fonts.gstatic.com;

connect-src 'self' https://api.example.com;

frame-ancestors 'none';

form-action 'self'

Start with a report-only policy to identify violations before enforcing: 

Content-Security-Policy-Report-Only: default-src 'self';

report-uri /csp-violations

X-Content-Type-Options 

Prevents browsers from MIME-type sniffing, which can be used to bypass content type checks. 

X-Content-Type-Options: nosniff

X-Frame-Options 

Prevents clickjacking by controlling whether your page can be embedded in a frame. 

X-Frame-Options: DENY

Use `DENY` to block all framing, or `SAMEORIGIN` to allow framing on pages sharing the same origin. 

Referrer-Policy 

Controls how much referrer information is included with requests. 

Referrer-Policy: strict-origin-when-cross-origin

This sends the full URL as referrer for same-origin requests, only the origin for cross-origin requests, and nothing when navigating from HTTPS to HTTP. 

Recommended Headers 

Permissions-Policy (formerly Feature-Policy) 

Controls which browser features your page can use. 

Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=()

Disable all features you do not need. This prevents malicious scripts from accessing device capabilities even if they bypass other controls. 

Cross-Origin-Opener-Policy 

Isolates your page from cross-origin windows, preventing Spectre-type side-channel attacks. 

Cross-Origin-Opener-Policy: same-origin-allow-popups

Cross-Origin-Resource-Policy 

Controls which origins can load your resources. 

Cross-Origin-Resource-Policy: same-origin

Cross-Origin-Embedder-Policy 

Requires cross-origin resources to explicitly grant permission to load. 

Cross-Origin-Embedder-Policy: require-corp

Implementation Checklist 

| Header | Value | Risk if Missing | |--------|-------|-----------------| | Strict-Transport-Security | `max-age=63072000; includeSubDomains` | SSL stripping | | Content-Security-Policy | Custom policy | XSS, data injection | | X-Content-Type-Options | `nosniff` | MIME confusion | | X-Frame-Options | `DENY` | Clickjacking | | Referrer-Policy | `strict-origin-when-cross-origin` | Privacy leakage | | Permissions-Policy | Restrictive policy | API abuse | | Cross-Origin-Opener-Policy | `same-origin-allow-popups` | Side-channel attacks | 

Testing Your Headers 

Several tools can validate your security headers: 

  * **securityheaders.com** : Scans and grades your headers.

  * **Observatory by Mozilla** : Provides an overall security score.

  * **Chrome DevTools** : Inspect headers in the Network tab.

  * **curl** : Quick manual check:




curl -sI https://example.com | grep -i '^strict-transport|^content-security|^x-content-type|^x-frame|^referrer'

Common Mistakes 

  * **Setting CSP too broadly** : `script-src 'unsafe-inline' https:` effectively disables CSP protection. Use strict CSP with nonces or hashes instead.

  * **Missing report-uri on CSP** : Without a reporting endpoint, you will not know when violations occur.

  * **Forgetting includeSubDomains on HSTS** : Users accessing subdomains over HTTP remain vulnerable.

  * **Not preloading HSTS** : The first request is still vulnerable without preloading.

  * **Overly permissive CORS headers** : `Access-Control-Allow-Origin: *` combined with credentials exposes your API to any site.




Summary 

Implementing HTTP security headers is one of the highest-ROI security improvements you can make. Start with HSTS, CSP, X-Content-Type-Options, and X-Frame-Options, then progressively add the remaining headers. Test regularly with automated scanners, and monitor CSP reports to catch new vulnerabilities as your application evolves.

**See also:** [Mobile Application Security Guide](</en/security/mobile-security.html>), [XSRF/CSRF Protection Guide](</en/security/xsrf-csrf-protection.html>), [Container Security Best Practices](</en/security/container-security.html>).

**See also:** [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>), [Webhook Security Best Practices](</en/security/webhook-security.html>)
