---
title: "Security Engineer Interview"
description: "Key topics, system design questions, and practical exercises for security engineer interviews."
date: 2026-03-19
board: security
url: https://aidev.fit/en/security/security-engineer-interview.html
---

# Security Engineer Interview

Interview Structure 

Security engineer interviews typically cover: security fundamentals, hands-on exercises, system design, and behavioral scenarios. 

Core Knowledge Topics 

Cryptography 

Understand encryption algorithms and their properties: 

## Interview question: Implement a secure password hasher

import hashlib

import os

def hash_password(password):

"""Hash password with bcrypt (the correct answer)"""

import bcrypt

salt = bcrypt.gensalt(rounds=12)

return bcrypt.hashpw(password.encode(), salt)

## Follow-up: Why not SHA-256?

## Answer: SHA-256 is fast, making brute-force feasible.

## bcrypt/argon2 are deliberately slow and include salt.

## Follow-up: What about MD5?

## Answer: MD5 is broken for collision resistance. Never use.

Network Security 

## Interview question: Implement a simple port scanner

import socket

def scan_port(host, port, timeout=1):

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.settimeout(timeout)

result = sock.connect_ex((host, port))

sock.close()

return result == 0

## Follow-up: How would you scan without being detected?

## Answer: Use SYN scan (stealth scan), randomize port order,

## and introduce delays between probes.

System Design Questions 

Design a Secure Authentication System 

## High-level design

class SecureAuthSystem:

components = [

"Rate limiter (token bucket per IP)",

"Account lockout (5 failures, 15 min lockout)",

"MFA enforcement (TOTP preferred)",

"Session management (JWT, short-lived)",

"Anomaly detection (new device/location)",

"Audit logging (immutable, SIEM-forwarded)"

]

def login_flow(self):

return {

"1": "Validate credentials (bcrypt compare)",

"2": "Check rate limits",

"3": "Verify MFA if enabled",

"4": "Check for suspicious context",

"5": "Generate session tokens",

"6": "Log authentication event"

}

Design a Secrets Management System 

Requirements:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- Store secrets encrypted at rest (AES-256-GCM)

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- Access control (RBAC)

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- Audit logging

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- Automatic rotation

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- High availability

Data flow:

1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Client request -> API Gateway -> Auth check

2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Auth check -> JWT validation -> Permission check

3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Permission check -> Key hierarchy -> Decrypt secret

4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Return secret (with audit log)

Key hierarchy:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- Master key (HSM/KMS)

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- Database encryption keys

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- Secret encryption keys

Practical Exercise 

## Exercise: Security incident investigation

incident_logs = [

{"time": "10:00", "user": "alice", "event": "login", "ip": "192.168.1.1"},

{"time": "10:01", "user": "alice", "event": "login_failed", "ip": "10.0.0.5"},

{"time": "10:02", "user": "alice", "event": "login_failed", "ip": "10.0.0.5"},

{"time": "10:03", "user": "alice", "event": "login_failed", "ip": "10.0.0.5"},

{"time": "10:04", "user": "alice", "event": "login_failed", "ip": "10.0.0.5"},

{"time": "10:05", "user": "alice", "event": "login_success", "ip": "10.0.0.5"},

{"time": "10:06", "user": "alice", "event": "export_data", "ip": "10.0.0.5"},

{"time": "10:07", "user": "alice", "event": "delete_logs", "ip": "10.0.0.5"},

]

## Questions:

## 1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. What indicators of compromise do you see?

## 2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. What is the likely attack vector?

## 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. What immediate containment actions?

## 4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. What forensic data would you collect?

## Analysis:

## \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- IP change: 192.168.1.1 (corp) -> 10.0.0.5 (internal)

## \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- Brute force pattern: 4 failed logins

## \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- Suspicious actions after login: data export + log deletion

## \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- Likely: credential stuffing -> account takeover -> data exfiltration

Behavioral Questions 

Be prepared to discuss: 

  * A time you found a critical vulnerability

  * How you convinced developers to fix security issues

  * A security incident you handled

  * How you stay current with security research

  * Conflict between security and business needs




Resources for Preparation 

Study these areas in depth: OWASP Top 10, cloud security (AWS/GCP/Azure), network protocols, cryptography fundamentals, and compliance frameworks. Practice with hands-on labs and capture-the-flag challenges. Be ready to whiteboard system designs and discuss real-world threat scenarios.

**See also:** [Security Metrics and Reporting](</en/security/security-metrics.html>), [SOC Operations](</en/security/soc-operations.html>), [Database Encryption](</en/security/database-encryption.html>).

**See also:** [Bug Bounty Guide](</en/security/bug-bounty.html>), [Microservice Security](</en/security/microservice-security.html>), [Security Metrics and Reporting](</en/security/security-metrics.html>)

**See also:** [Bug Bounty Guide](</en/security/bug-bounty.html>), [Microservice Security](</en/security/microservice-security.html>), [Security Metrics and Reporting](</en/security/security-metrics.html>)

**See also:** [Bug Bounty Guide](</en/security/bug-bounty.html>), [Microservice Security](</en/security/microservice-security.html>), [Security Metrics and Reporting](</en/security/security-metrics.html>)

**See also:** [Bug Bounty Guide](</en/security/bug-bounty.html>), [Microservice Security](</en/security/microservice-security.html>), [Security Metrics and Reporting](</en/security/security-metrics.html>)

**See also:** [Bug Bounty Guide](</en/security/bug-bounty.html>), [Microservice Security](</en/security/microservice-security.html>), [Security Metrics and Reporting](</en/security/security-metrics.html>)

**See also:** [EDR: Endpoint Detection and Response Solutions](</en/security/endpoint-detection-response.html>), [SIEM: Security Information and Event Management](</en/security/security-information-event-management.html>), [Certificate Management](</en/security/certificate-management.html>)

**See also:** [EDR: Endpoint Detection and Response Solutions](</en/security/endpoint-detection-response.html>), [SIEM: Security Information and Event Management](</en/security/security-information-event-management.html>), [Certificate Management](</en/security/certificate-management.html>)

**See also:** [EDR: Endpoint Detection and Response Solutions](</en/security/endpoint-detection-response.html>), [SIEM: Security Information and Event Management](</en/security/security-information-event-management.html>), [Certificate Management](</en/security/certificate-management.html>)

**See also:** [EDR: Endpoint Detection and Response Solutions](</en/security/endpoint-detection-response.html>), [SIEM: Security Information and Event Management](</en/security/security-information-event-management.html>), [Certificate Management](</en/security/certificate-management.html>)

**See also:** [EDR: Endpoint Detection and Response Solutions](</en/security/endpoint-detection-response.html>), [SIEM: Security Information and Event Management](</en/security/security-information-event-management.html>), [Certificate Management](</en/security/certificate-management.html>)

**See also:** [EDR: Endpoint Detection and Response Solutions](</en/security/endpoint-detection-response.html>), [SIEM: Security Information and Event Management](</en/security/security-information-event-management.html>), [Certificate Management](</en/security/certificate-management.html>)

**See also:** [EDR: Endpoint Detection and Response Solutions](</en/security/endpoint-detection-response.html>), [SIEM: Security Information and Event Management](</en/security/security-information-event-management.html>), [Certificate Management](</en/security/certificate-management.html>)

**See also:** [EDR: Endpoint Detection and Response Solutions](</en/security/endpoint-detection-response.html>), [SIEM: Security Information and Event Management](</en/security/security-information-event-management.html>), [Certificate Management](</en/security/certificate-management.html>)

**See also:** [EDR: Endpoint Detection and Response Solutions](</en/security/endpoint-detection-response.html>), [SIEM: Security Information and Event Management](</en/security/security-information-event-management.html>), [Certificate Management](</en/security/certificate-management.html>)

**See also:** [EDR: Endpoint Detection and Response Solutions](</en/security/endpoint-detection-response.html>), [SIEM: Security Information and Event Management](</en/security/security-information-event-management.html>), [Certificate Management](</en/security/certificate-management.html>)

**See also:** [EDR: Endpoint Detection and Response Solutions](</en/security/endpoint-detection-response.html>), [SIEM: Security Information and Event Management](</en/security/security-information-event-management.html>), [Certificate Management](</en/security/certificate-management.html>)

**See also:** [EDR: Endpoint Detection and Response Solutions](</en/security/endpoint-detection-response.html>), [SIEM: Security Information and Event Management](</en/security/security-information-event-management.html>), [Certificate Management](</en/security/certificate-management.html>)

**See also:** [EDR: Endpoint Detection and Response Solutions](</en/security/endpoint-detection-response.html>), [SIEM: Security Information and Event Management](</en/security/security-information-event-management.html>), [Certificate Management](</en/security/certificate-management.html>)

**See also:** [EDR: Endpoint Detection and Response Solutions](</en/security/endpoint-detection-response.html>), [SIEM: Security Information and Event Management](</en/security/security-information-event-management.html>), [Certificate Management](</en/security/certificate-management.html>)

**See also:** [EDR: Endpoint Detection and Response Solutions](</en/security/endpoint-detection-response.html>), [SIEM: Security Information and Event Management](</en/security/security-information-event-management.html>), [Certificate Management](</en/security/certificate-management.html>)

**See also:** [EDR: Endpoint Detection and Response Solutions](</en/security/endpoint-detection-response.html>), [SIEM: Security Information and Event Management](</en/security/security-information-event-management.html>), [Certificate Management](</en/security/certificate-management.html>)

**See also:** [EDR: Endpoint Detection and Response Solutions](</en/security/endpoint-detection-response.html>), [SIEM: Security Information and Event Management](</en/security/security-information-event-management.html>), [Certificate Management](</en/security/certificate-management.html>)
