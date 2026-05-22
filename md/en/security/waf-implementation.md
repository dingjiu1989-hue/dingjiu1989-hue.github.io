---
title: "Web Application Firewall Implementation"
description: "Practical guide to implementing ModSecurity with OWASP CRS, custom rule writing, false positive tuning, and performance optimization."
date: 2026-03-15
board: security
url: https://aidev.fit/en/security/waf-implementation.html
---

# Web Application Firewall Implementation

Introduction 

A Web Application Firewall (WAF) is a security layer that monitors, filters, and blocks HTTP traffic to and from a web application. Unlike network firewalls that operate at layers 3-4, WAFs inspect application-layer traffic (layer 7) and understand HTTP semantics, making them essential for defending against OWASP Top 10 attacks. 

ModSecurity and OWASP CRS 

ModSecurity is the most widely deployed open-source WAF engine. It operates as a module within web servers like Apache, Nginx, and IIS, or as a reverse proxy. The OWASP Core Rule Set (CRS) provides generic attack detection rules. 

## Basic ModSecurity configuration

SecRuleEngine On

SecRequestBodyAccess On

SecResponseBodyAccess On

SecDataDir /tmp/modsecurity/data

## Include OWASP CRS

Include /etc/modsecurity/crs/crs-setup.conf

Include /etc/modsecurity/crs/rules/*.conf

## Custom rule: block requests with suspicious User-Agent

SecRule REQUEST_HEADERS:User-Agent "@pmFromFile /etc/modsecurity/blocked-agents.txt" \

"id:1000001,phase:1,deny,status:403,msg:'Blocked malicious User-Agent'"

CRS includes rules for SQL injection (942xxx), XSS (941xxx), LFI (931xxx), RFI (932xxx), and more. Each rule set is categorized by phase and severity. 

Custom Rule Writing 

Custom rules extend the WAF to handle application-specific threats or business logic. ModSecurity rules consist of three components: variables, operators, and actions. 

## Custom rule: protect /api/checkout from parameter tampering

SecRule REQUEST_URI "@beginsWith /api/checkout" \

"id:1000002,phase:2,deny,status:403,\

msg:'Checkout parameter tampering detected',\

chain"

SecRule ARGS:quantity "!@rx ^[0-9]+$"

## Rate limiting per IP

SecRule IP:COUNT "@gt 100" \

"id:1000003,phase:5,deny,status:429,\

msg:'Rate limit exceeded',\

setvar:ip.rate_limit=1,\

expirevar:ip.rate_limit=60"

SecAction "id:1000004,phase:5,nolog,\

initcol:ip=%{REMOTE_ADDR},\

setvar:ip.count=+1"

False Positive Tuning 

Overly aggressive WAF rules generate false positives that block legitimate traffic. Tuning is an iterative process: 

  * **Deploy in detection-only mode** initially to identify false positives without impacting production.



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Analyze audit logs** for blocked requests that appear legitimate. 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Disable specific rules** or adjust paranoia levels. 

## Set CRS paranoia level (1-4, higher = stricter)

SecAction \

"id:900000,\

phase:1,\

nolog,\

pass,\

t:none,\

setvar:tx.paranoia_level=2"

## Remove a specific rule for a specific URI

SecRuleRemoveById 942100

## This removes the rule globally; better to scope it:

SecRule REQUEST_URI "@beginsWith /api/public" \

"id:1000005,phase:1,nolog,pass,ctl:ruleRemoveById=942100"

Performance Impact 

WAF inspection introduces latency. Key optimization strategies: 

  * **Request body limits** : Large request bodies increase processing time. Set practical limits.

  * **Static file exclusion** : Skip WAF processing for static assets (images, CSS, JS).

  * **Rule ordering** : Place cheaper checks (URI matching) before expensive ones (regex).




## Skip WAF for static files

SecRule REQUEST_URI "\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\.(jpg|png|css|js|ico)$" \

"id:1000006,phase:1,nolog,pass,ctl:ruleEngine=Off"

Benchmarking shows ModSecurity with CRS at paranoia level 2 adds approximately 1-3ms per request on modern hardware. Full inspection at paranoia level 4 can add 10-20ms. 

Conclusion 

A properly tuned WAF is a critical defense layer. Start with CRS in detection mode, monitor logs aggressively, tune false positives before enforcing, and always be aware of the performance trade-offs at each paranoia level.

**See also:** [WAF Solutions Compared: Cloudflare, AWS WAF, ModSecurity, Akamai](</en/security/waf-comparison.html>), [Zero Trust Implementation](</en/security/zero-trust-implementation.html>), [Bug Bounty Guide](</en/security/bug-bounty.html>).

**See also:** [Zero Trust Implementation](</en/security/zero-trust-implementation.html>), [Bug Bounty Guide](</en/security/bug-bounty.html>), [SOC Operations](</en/security/soc-operations.html>)

**See also:** [Zero Trust Implementation](</en/security/zero-trust-implementation.html>), [Bug Bounty Guide](</en/security/bug-bounty.html>), [SOC Operations](</en/security/soc-operations.html>)

**See also:** [Zero Trust Implementation](</en/security/zero-trust-implementation.html>), [Bug Bounty Guide](</en/security/bug-bounty.html>), [SOC Operations](</en/security/soc-operations.html>)

**See also:** [Zero Trust Implementation](</en/security/zero-trust-implementation.html>), [Bug Bounty Guide](</en/security/bug-bounty.html>), [SOC Operations](</en/security/soc-operations.html>)

**See also:** [Zero Trust Implementation](</en/security/zero-trust-implementation.html>), [Bug Bounty Guide](</en/security/bug-bounty.html>), [SOC Operations](</en/security/soc-operations.html>)

**See also:** [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [WAF Solutions Compared: Cloudflare, AWS WAF, ModSecurity, Akamai](</en/security/waf-comparison.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [WAF Solutions Compared: Cloudflare, AWS WAF, ModSecurity, Akamai](</en/security/waf-comparison.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [WAF Solutions Compared: Cloudflare, AWS WAF, ModSecurity, Akamai](</en/security/waf-comparison.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [WAF Solutions Compared: Cloudflare, AWS WAF, ModSecurity, Akamai](</en/security/waf-comparison.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [WAF Solutions Compared: Cloudflare, AWS WAF, ModSecurity, Akamai](</en/security/waf-comparison.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [WAF Solutions Compared: Cloudflare, AWS WAF, ModSecurity, Akamai](</en/security/waf-comparison.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [WAF Solutions Compared: Cloudflare, AWS WAF, ModSecurity, Akamai](</en/security/waf-comparison.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [WAF Solutions Compared: Cloudflare, AWS WAF, ModSecurity, Akamai](</en/security/waf-comparison.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [WAF Solutions Compared: Cloudflare, AWS WAF, ModSecurity, Akamai](</en/security/waf-comparison.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [WAF Solutions Compared: Cloudflare, AWS WAF, ModSecurity, Akamai](</en/security/waf-comparison.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [WAF Solutions Compared: Cloudflare, AWS WAF, ModSecurity, Akamai](</en/security/waf-comparison.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [WAF Solutions Compared: Cloudflare, AWS WAF, ModSecurity, Akamai](</en/security/waf-comparison.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [WAF Solutions Compared: Cloudflare, AWS WAF, ModSecurity, Akamai](</en/security/waf-comparison.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [WAF Solutions Compared: Cloudflare, AWS WAF, ModSecurity, Akamai](</en/security/waf-comparison.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [WAF Solutions Compared: Cloudflare, AWS WAF, ModSecurity, Akamai](</en/security/waf-comparison.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [WAF Solutions Compared: Cloudflare, AWS WAF, ModSecurity, Akamai](</en/security/waf-comparison.html>), [API Authentication Methods](</en/security/api-authentication.html>)
