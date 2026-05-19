---
title: "WAF Deployment Patterns"
description: "WAF deployment patterns including inline, reverse proxy, cloud WAF, and API protection strategies."
date: 2026-03-20
board: security
url: https://dingjiu1989-hue.github.io/en/security/waf-deployment.html
---

# WAF Deployment Patterns

WAF Overview 

A Web Application Firewall (WAF) filters and monitors HTTP traffic between web applications and the internet. It protects against common attacks like SQL injection, XSS, and CSRF. 

Inline WAF Deployment 

The WAF sits directly in the request path: 

## ModSecurity configuration

SecRuleEngine On

SecRequestBodyAccess On

SecResponseBodyAccess On

## SQL Injection prevention

SecRule REQUEST_COOKIES|REQUEST_COOKIES_NAMES|ARGS_NAMES|ARGS|XML:/* \

"/((\%27)|(\'))\s*((\%6F)|o|(\%4F))((\%72)|r|(\%52))/ix" \

"id:'981173',\

phase:2,\

deny,\

status:403,\

msg:'SQL Injection Attack'"

## XSS prevention

SecRule ARGS "@detectXSS" \

"id:'958056',\

phase:2,\

deny,\

status:403,\

msg:'XSS Attack Detected'"

Reverse Proxy WAF 

Deploy WAF as a reverse proxy for centralized protection: 

## Nginx with ModSecurity

server {

listen 443 ssl;

server_name app.example.com;

## ModSecurity enabled

modsecurity on;

modsecurity_rules_file /etc/nginx/modsec/main.conf;

location / {

proxy_pass http://backend:8080;

proxy_set_header Host $host;

proxy_set_header X-Real-IP $remote_addr;

proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

}

}

Cloud WAF (AWS WAF) 

## AWS WAF with rate limiting and SQL injection protection

resource "aws_wafv2_web_acl" "main" {

name = "main-waf"

description = "Main WAF ACL"

scope = "REGIONAL"

default_action {

allow {}

}

rule {

name = "RateLimit"

priority = 1

action {

block {}

}

statement {

rate_based_statement {

limit = 2000

aggregate_key_type = "IP"

}

}

visibility_config {

cloudwatch_metrics_enabled = true

metric_name = "RateLimit"

sampled_requests_enabled = true

}

}

rule {

name = "SQLInjection"

priority = 2

action {

block {}

}

statement {

sql_injection_match_statement {

field_to_match {

body {}

}

text_transformation {

priority = 0

type = "URL_DECODE"

}

}

}

visibility_config {

cloudwatch_metrics_enabled = true

metric_name = "SQLInjection"

sampled_requests_enabled = true

}

}

}

API Protection 

APIs require different WAF rules than web applications: 

## Custom WAF rule for API protection

API_WAF_RULES = {

"missing_auth_header": {

"priority": 1,

"match": lambda req: "Authorization" not in req.headers,

"action": "block",

"response": 401

},

"invalid_content_type": {

"priority": 2,

"match": lambda req: (

req.method in ["POST", "PUT", "PATCH"]

and req.headers.get("Content-Type") != "application/json"

),

"action": "block",

"response": 415

},

"path_traversal": {

"priority": 3,

"match": lambda req: "../" in req.path or "..\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\" in req.path,

"action": "block",

"response": 403

}

}

WAF Logging and Monitoring 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Analyze blocked requests

SELECT country, COUNT(*) as blocked_count,

ARRAY_AGG(DISTINCT rule_id) as triggered_rules

FROM waf_logs

WHERE action = 'BLOCK'

AND timestamp > NOW() - INTERVAL '24 hours'

GROUP BY country

ORDER BY blocked_count DESC;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- False positive analysis

SELECT rule_id, COUNT(*) as false_positives

FROM waf_logs

WHERE action = 'BLOCK'

AND downstream_status = 200

AND timestamp > NOW() - INTERVAL '7 days'

GROUP BY rule_id

ORDER BY false_positives DESC;

Conclusion 

Choose the WAF deployment pattern that fits your architecture. Inline WAF offers the strongest protection but adds latency. Cloud WAF provides scalability with minimal maintenance. Reverse proxy WAF is ideal for centralized management. Tune your WAF rules carefully to minimize false positives and monitor blocked requests regularly.

**See also:** [WAF Solutions Compared: Cloudflare, AWS WAF, ModSecurity, Akamai](</en/security/waf-comparison.html>), [Email Security](</en/security/email-security.html>), [Data Loss Prevention Strategies](</en/security/dlp-strategies.html>).

**See also:** [DNS Security](</en/security/dns-security.html>), [Email Security](</en/security/email-security.html>), [Key Management Systems](</en/security/key-management.html>)

**See also:** [DNS Security](</en/security/dns-security.html>), [Email Security](</en/security/email-security.html>), [Key Management Systems](</en/security/key-management.html>)

**See also:** [DNS Security](</en/security/dns-security.html>), [Email Security](</en/security/email-security.html>), [Key Management Systems](</en/security/key-management.html>)

**See also:** [DNS Security](</en/security/dns-security.html>), [Email Security](</en/security/email-security.html>), [Key Management Systems](</en/security/key-management.html>)

**See also:** [DNS Security](</en/security/dns-security.html>), [Email Security](</en/security/email-security.html>), [Key Management Systems](</en/security/key-management.html>)

**See also:** [Bug Bounty Guide](</en/security/bug-bounty.html>), [Clickjacking Protection](</en/security/clickjacking-protection.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>)

**See also:** [Bug Bounty Guide](</en/security/bug-bounty.html>), [Clickjacking Protection](</en/security/clickjacking-protection.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>)

**See also:** [Bug Bounty Guide](</en/security/bug-bounty.html>), [Clickjacking Protection](</en/security/clickjacking-protection.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>)

**See also:** [Bug Bounty Guide](</en/security/bug-bounty.html>), [Clickjacking Protection](</en/security/clickjacking-protection.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>)

**See also:** [Bug Bounty Guide](</en/security/bug-bounty.html>), [Clickjacking Protection](</en/security/clickjacking-protection.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>)
