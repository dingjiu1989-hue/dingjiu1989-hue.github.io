---
title: "Cloud Network Security"
description: "Designing cloud network security with security groups, NACLs, firewall rules, and traffic inspection."
date: 2026-03-16
board: security
url: https://dingjiu1989-hue.github.io/en/security/cloud-network-security.html
---

# Cloud Network Security

Cloud Network Security Layers 

Cloud networks require defense in depth: VPC isolation, subnet segmentation, security groups, network ACLs, and traffic inspection. 

Security Groups vs NACLs 

Security groups are stateful instance-level firewalls. NACLs are stateless subnet-level filters: 

## Security Group (stateful)

resource "aws_security_group" "web_sg" {

name = "web-tier"

description = "Security group for web instances"

vpc_id = var.vpc_id

ingress {

description = "HTTPS from anywhere"

from_port = 443

to_port = 443

protocol = "tcp"

cidr_blocks = ["0.0.0.0/0"]

}

ingress {

description = "SSH from bastion only"

from_port = 22

to_port = 22

protocol = "tcp"

security_groups = [aws_security_group.bastion.id]

}

egress {

from_port = 0

to_port = 0

protocol = "-1"

cidr_blocks = ["0.0.0.0/0"]

}

}

## NACL (stateless - must allow both directions)

resource "aws_network_acl" "public_subnet_acl" {

vpc_id = var.vpc_id

ingress {

rule_no = 100

protocol = "tcp"

from_port = 443

to_port = 443

cidr_block = "0.0.0.0/0"

action = "allow"

}

egress {

rule_no = 100

protocol = "tcp"

from_port = 1024

to_port = 65535

cidr_block = "0.0.0.0/0"

action = "allow"

}

}

VPC Design 

## Multi-tier VPC design

class VPCDesign:

def **init**(self, cidr="10.0.0.0/16"):

self.cidr = cidr

self.tiers = {

"public": {"cidr": "10.0.1.0/24", "public": True},

"web": {"cidr": "10.0.10.0/24", "public": False},

"app": {"cidr": "10.0.20.0/24", "public": False},

"db": {"cidr": "10.0.30.0/24", "public": False},

"management": {"cidr": "10.0.100.0/24", "public": False}

}

def generate_routing_rules(self):

rules = []

## Web tier: inbound from public, outbound to app

rules.append({

"from": "web",

"to": "app",

"ports": [8080, 8443],

"protocol": "tcp"

})

## App tier: outbound to db

rules.append({

"from": "app", 

"to": "db",

"ports": [5432],

"protocol": "tcp"

})

## No direct public access to app or db

return rules

Traffic Inspection 

Deploy inline inspection for east-west traffic: 

## Traffic inspection rules

inspection_rules:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: inspect_web_app_traffic

source: web-subnet

destination: app-subnet

inspection: deep_packet

threat_prevention: enabled

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: inspect_app_db_traffic

source: app-subnet

destination: db-subnet

inspection: metadata_only

anomaly_detection: enabled

Firewall Rule Management 

## Firewall rule analyzer

def analyze_firewall_rules(rules):

issues = []

for rule in rules:

## Check for overly permissive rules

if rule.get("cidr") == "0.0.0.0/0" and rule.get("port") in [22, 3389]:

issues.append(f"Overly permissive: {rule['name']} allows SSH/RDP from anywhere")

## Check for rules with no hits

if rule.get("hit_count", 0) == 0 and rule["age_days"] > 30:

issues.append(f"Unused rule: {rule['name']} has no hits in 30+ days")

## Check for duplicate rules

## ...

return issues

Conclusion 

Cloud network security requires layered controls. Use security groups for instance-level filtering and NACLs for subnet-level guardrails. Design VPCs with multiple tiers and restrict traffic between them. Deploy traffic inspection for critical paths. Review firewall rules quarterly and remove unused rules. Automate everything with infrastructure as code.

**See also:** [Kubernetes Security](</en/security/kubernetes-security.html>), [Cloud Security Posture Management](</en/security/cloud-security-posture.html>), [Kubernetes Network Policies](</en/security/kubernetes-network-policies.html>).

**See also:** [Data Loss Prevention Strategies](</en/security/dlp-strategies.html>), [Kubernetes Security](</en/security/kubernetes-security.html>), [Cloud Security Posture Management](</en/security/cloud-security-posture.html>)

**See also:** [Data Loss Prevention Strategies](</en/security/dlp-strategies.html>), [Kubernetes Security](</en/security/kubernetes-security.html>), [Cloud Security Posture Management](</en/security/cloud-security-posture.html>)

**See also:** [Data Loss Prevention Strategies](</en/security/dlp-strategies.html>), [Kubernetes Security](</en/security/kubernetes-security.html>), [Cloud Security Posture Management](</en/security/cloud-security-posture.html>)

**See also:** [Data Loss Prevention Strategies](</en/security/dlp-strategies.html>), [Kubernetes Security](</en/security/kubernetes-security.html>), [Cloud Security Posture Management](</en/security/cloud-security-posture.html>)

**See also:** [Data Loss Prevention Strategies](</en/security/dlp-strategies.html>), [Kubernetes Security](</en/security/kubernetes-security.html>), [Cloud Security Posture Management](</en/security/cloud-security-posture.html>)

**See also:** [Container Runtime Security](</en/security/container-runtime-security.html>), [DDoS Mitigation](</en/security/ddos-mitigation.html>), [Helm Security](</en/security/helm-security.html>)

**See also:** [Container Runtime Security](</en/security/container-runtime-security.html>), [DDoS Mitigation](</en/security/ddos-mitigation.html>), [Helm Security](</en/security/helm-security.html>)

**See also:** [Container Runtime Security](</en/security/container-runtime-security.html>), [DDoS Mitigation](</en/security/ddos-mitigation.html>), [Helm Security](</en/security/helm-security.html>)

**See also:** [Container Runtime Security](</en/security/container-runtime-security.html>), [DDoS Mitigation](</en/security/ddos-mitigation.html>), [Helm Security](</en/security/helm-security.html>)

**See also:** [Container Runtime Security](</en/security/container-runtime-security.html>), [DDoS Mitigation](</en/security/ddos-mitigation.html>), [Helm Security](</en/security/helm-security.html>)

**See also:** [Container Runtime Security](</en/security/container-runtime-security.html>), [DDoS Mitigation](</en/security/ddos-mitigation.html>), [Helm Security](</en/security/helm-security.html>)

**See also:** [Container Runtime Security](</en/security/container-runtime-security.html>), [DDoS Mitigation](</en/security/ddos-mitigation.html>), [Helm Security](</en/security/helm-security.html>)

**See also:** [Container Runtime Security](</en/security/container-runtime-security.html>), [DDoS Mitigation](</en/security/ddos-mitigation.html>), [Helm Security](</en/security/helm-security.html>)

**See also:** [Container Runtime Security](</en/security/container-runtime-security.html>), [DDoS Mitigation](</en/security/ddos-mitigation.html>), [Helm Security](</en/security/helm-security.html>)

**See also:** [Container Runtime Security](</en/security/container-runtime-security.html>), [DDoS Mitigation](</en/security/ddos-mitigation.html>), [Helm Security](</en/security/helm-security.html>)
