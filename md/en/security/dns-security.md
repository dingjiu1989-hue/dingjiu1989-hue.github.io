---
title: "DNS Security"
description: "Comprehensive guide to DNS security including DNSSEC, DNS over HTTPS/TLS, split-horizon DNS, filtering strategies, and common attack vectors."
date: 2026-03-09
board: security
url: https://aidev.fit/en/security/dns-security.html
---

# DNS Security

Introduction 

The Domain Name System (DNS) is a foundational internet protocol that translates human-readable domain names to IP addresses. Despite its critical role, DNS was designed without security considerations, making it a prime target for attacks including cache poisoning, tunneling, and DDoS amplification. 

DNSSEC 

DNS Security Extensions (DNSSEC) adds cryptographic signatures to DNS records, ensuring authenticity and integrity. It protects against cache poisoning attacks where an attacker injects forged DNS responses. 

DNSSEC uses a chain of trust starting from the DNS root zone. Each zone signs its records with a private key, and resolvers verify signatures using corresponding public keys stored as DNSKEY records. 

## Checking DNSSEC validation with dig

dig +dnssec example.com

## Verify DNSSEC chain

delv example.com

## Check if a domain is DNSSEC-signed

dig example.com DNSKEY

Key DNSSEC record types:

  * **RRSIG** : Resource Record Signature — cryptographic signature for a record set

  * **DNSKEY** : Public key used for signature verification

  * **DS** : Delegation Signer — hash of the child zone's DNSKEY, stored in the parent zone

  * **NSEC/NSEC3** : Next Secure — provides authenticated denial of existence




## BIND DNSSEC configuration example

zone "example.com" {

type master;

file "/etc/bind/db.example.com";

auto-dnssec maintain;

inline-signing yes;

key-directory "/etc/bind/keys";

};

DNS over HTTPS and DNS over TLS 

Traditional DNS queries are sent in cleartext over UDP, making them visible to network observers and susceptible to manipulation. DNS over HTTPS (DoH) and DNS over TLS (DoT) encrypt queries. 

  * **DoT** (RFC 7858): DNS over a dedicated TLS connection on port 853

  * **DoH** (RFC 8484): DNS over HTTP/2 or HTTP/3 on port 443, blending with HTTPS traffic




## Nginx DoH proxy configuration

location /dns-query {

proxy_pass http://127.0.0.1:8053;

proxy_set_header Host $host;

proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

}

## unbound configuration with DoT forwarder

forward-zone:

name: "."

forward-tls-upstream: yes

forward-addr: 1.1.1.1@853#cloudflare-dns.com

forward-addr: 8.8.8.8@853#dns.google

Split-Horizon DNS 

Split-horizon DNS returns different responses based on the requester's network origin. Internal users receive private IP addresses while external users receive public addresses. 

## BIND split-horizon configuration

view "internal" {

match-clients { 10.0.0.0/8; 172.16.0.0/12; 192.168.0.0/16; };

zone "example.com" {

type master;

file "/etc/bind/db.example.com.internal";

};

};

view "external" {

match-clients { any; };

zone "example.com" {

type master;

file "/etc/bind/db.example.com.external";

};

};

DNS Filtering and Threat Blocking 

DNS filtering blocks resolution of known malicious domains. Modern solutions integrate threat intelligence feeds to dynamically block malware, phishing, and command-and-control (C2) domains. 

## Simple DNS filter using dnspython

import dns.resolver

THREAT_FEED = set()

def load_threat_feed(feed_url):

## Download and parse threat intelligence feed

response = requests.get(feed_url)

for domain in response.text.splitlines():

THREAT_FEED.add(domain.strip().lower())

def safe_resolve(domain, resolver):

if domain.lower() in THREAT_FEED:

return None # Block resolution

return resolver.resolve(domain, 'A')

Common DNS Attacks 

  * **Cache Poisoning** : Attacker injects forged records into a resolver's cache. Mitigated by DNSSEC and source port randomization.



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **DNS Tunneling** : Encodes data in DNS queries to exfiltrate data or bypass network controls. Detected via traffic analysis of unusual query patterns. 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **DNS Amplification DDoS** : Attacker sends small queries with spoofed source IPs; responses can be 50x larger. Mitigated by response rate limiting (RRL) and BCP38 filtering. 4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **NXDOMAIN Attacks** : High volume of queries for non-existent domains exhausts resolver resources. 

## Response Rate Limiting in BIND

options {

rate-limit {

responses-per-second 5;

window 5;

log-only yes;

};

};

Conclusion 

Securing DNS requires a layered approach: DNSSEC for integrity, encrypted transports for confidentiality, split-horizon for network segmentation, and threat intelligence for proactive blocking. Regular monitoring and logging of DNS traffic is essential for detecting anomalous behavior indicative of compromise.

**See also:** [Session Management Security](</en/security/session-management.html>), [Supply Chain Security](</en/security/supply-chain-security.html>), [Threat Hunting](</en/security/threat-hunting.html>).

**See also:** [Content Security Policy](</en/security/content-security-policy.html>), [CORS Security](</en/security/cors-security.html>), [Input Validation Deep Dive](</en/security/input-validation.html>)

**See also:** [Content Security Policy](</en/security/content-security-policy.html>), [CORS Security](</en/security/cors-security.html>), [Input Validation Deep Dive](</en/security/input-validation.html>)

**See also:** [Content Security Policy](</en/security/content-security-policy.html>), [CORS Security](</en/security/cors-security.html>), [Input Validation Deep Dive](</en/security/input-validation.html>)

**See also:** [Content Security Policy](</en/security/content-security-policy.html>), [CORS Security](</en/security/cors-security.html>), [Input Validation Deep Dive](</en/security/input-validation.html>)

**See also:** [Content Security Policy](</en/security/content-security-policy.html>), [CORS Security](</en/security/cors-security.html>), [Input Validation Deep Dive](</en/security/input-validation.html>)

**See also:** [Supply Chain Security](</en/security/supply-chain-security.html>), [Threat Hunting](</en/security/threat-hunting.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [Supply Chain Security](</en/security/supply-chain-security.html>), [Threat Hunting](</en/security/threat-hunting.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [Supply Chain Security](</en/security/supply-chain-security.html>), [Threat Hunting](</en/security/threat-hunting.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [Supply Chain Security](</en/security/supply-chain-security.html>), [Threat Hunting](</en/security/threat-hunting.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [Supply Chain Security](</en/security/supply-chain-security.html>), [Threat Hunting](</en/security/threat-hunting.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [Supply Chain Security](</en/security/supply-chain-security.html>), [Threat Hunting](</en/security/threat-hunting.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [Supply Chain Security](</en/security/supply-chain-security.html>), [Threat Hunting](</en/security/threat-hunting.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [Supply Chain Security](</en/security/supply-chain-security.html>), [Threat Hunting](</en/security/threat-hunting.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [Supply Chain Security](</en/security/supply-chain-security.html>), [Threat Hunting](</en/security/threat-hunting.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [Supply Chain Security](</en/security/supply-chain-security.html>), [Threat Hunting](</en/security/threat-hunting.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [Supply Chain Security](</en/security/supply-chain-security.html>), [Threat Hunting](</en/security/threat-hunting.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [Supply Chain Security](</en/security/supply-chain-security.html>), [Threat Hunting](</en/security/threat-hunting.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [Supply Chain Security](</en/security/supply-chain-security.html>), [Threat Hunting](</en/security/threat-hunting.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [Supply Chain Security](</en/security/supply-chain-security.html>), [Threat Hunting](</en/security/threat-hunting.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [Supply Chain Security](</en/security/supply-chain-security.html>), [Threat Hunting](</en/security/threat-hunting.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [Supply Chain Security](</en/security/supply-chain-security.html>), [Threat Hunting](</en/security/threat-hunting.html>), [API Authentication Methods](</en/security/api-authentication.html>)
