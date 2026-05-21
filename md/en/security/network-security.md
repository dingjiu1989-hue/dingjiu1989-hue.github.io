---
title: "Network Security Fundamentals"
description: "Core network security concepts: firewalls, VPNs, IDS/IPS, zero-trust networking, segmentation, and micro-segmentation."
date: 2026-03-05
board: security
url: https://dingjiu1989-hue.github.io/en/security/network-security.html
---

# Network Security Fundamentals

Network security protects the communication channels between systems. As organizations move to the cloud and adopt zero-trust architectures, traditional perimeter-based network security is giving way to more granular, identity-aware approaches. This article covers the foundational concepts every developer and security practitioner needs.

## Firewalls

Firewalls filter network traffic based on pre-defined rules. They are the first line of defense in network security.

## Packet Filtering Firewalls

Packet filtering firewalls inspect individual packets against rule sets. They examine source and destination IP addresses, ports, and protocols. They operate at layers 3 and 4 of the OSI model.

Rule table example:

Source IP Dest IP Port Protocol Action

10.0.1.0/24 10.0.2.0/24 443 TCP Allow

0.0.0.0/0 10.0.1.5 22 TCP Deny

## Stateful Firewalls

Stateful firewalls maintain a connection table. They track the state of active connections and make decisions based on the connection state, not just individual packets. This allows them to permit return traffic for legitimate outbound connections while blocking unsolicited inbound traffic.

## Next-Generation Firewalls (NGFW)

NGFWs combine traditional firewall capabilities with application-layer inspection, intrusion prevention, and threat intelligence. They can identify applications regardless of port or protocol and enforce policies based on user identity.

## iptables stateful rule example

iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

iptables -A INPUT -m state --state NEW -p tcp --dport 443 -j ACCEPT

iptables -A INPUT -m state --state NEW -p tcp --dport 80 -j ACCEPT

iptables -A INPUT -j DROP

## Virtual Private Networks (VPNs)

VPNs create encrypted tunnels between endpoints over untrusted networks. They extend a private network across a public network, allowing remote users and branch offices to access internal resources.

## Site-to-Site VPN

Connects entire networks to each other, such as an office to a cloud VPC. AWS VPN, Azure VPN Gateway, and GCP Cloud VPN all implement IPsec tunnels.

## AWS CLI: create a VPN connection

aws ec2 create-vpn-connection \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--customer-gateway-id cgw-123 \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--vpn-gateway-id vgw-456 \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--type ipsec.1

## Remote Access VPN

Connects individual users to the corporate network. VPN clients include OpenVPN, WireGuard, and proprietary solutions like Palo Alto GlobalProtect.

## VPN Limitations

VPNs are not a panacea. They grant broad network access, often violating least-privilege principles. If a VPN credential is compromised, the attacker gains full network access. Modern architectures increasingly replace VPNs with zero-trust network access (ZTNA) solutions.

## Intrusion Detection and Prevention Systems (IDS/IPS)

IDS monitors network traffic for suspicious activity and generates alerts. IPS sits inline and actively blocks detected threats.

## Detection Methods

  * **Signature-based** : Matches traffic against known attack patterns. Effective for known threats but misses zero-day attacks.

  * **Anomaly-based** : Establishes a baseline of normal traffic and alerts on deviations. Catches novel attacks but produces more false positives.

  * **Behavioral** : Analyzes traffic patterns over time. Detects slow, low-and-slow attacks that evade other methods.




## Popular Tools

  * **Snort** : Open-source NIDS with a large rule set. Widely deployed for packet logging and real-time traffic analysis.

  * **Suricata** : High-performance IDS/IPS with GPU acceleration. Supports multi-threading and modern protocols like HTTP/2.

  * **Zeek (formerly Bro)** : Network analysis framework that produces detailed logs about connections, protocols, and files.




## Suricata configuration snippet

vars:

address-groups:

HOME_NET: "[10.0.0.0/8,172.16.0.0/12]"

EXTERNAL_NET: "!$HOME_NET"

rule-files:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- emerging-threats.rules

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- malware-cnc.rules

af-packet:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- interface: eth0

cluster-id: 99

cluster-type: cluster_flow

## Zero-Trust Networking

Zero trust assumes no implicit trust based on network location. Every access request must be authenticated, authorized, and encrypted.

## Core Principles

  * **Never trust, always verify** : Every request, whether from inside or outside the network, must be validated.



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Assume breach** : Design the network as if attackers already have a foothold. Limit lateral movement.

3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Least privilege** : Grant the minimum access necessary for each user or service.

## Zero-Trust Implementation

  * **Micro-segmentation** : Divide the network into small, isolated zones. Each zone requires separate authentication.

  * **Identity-aware proxies** : Gateways that authenticate every request before forwarding traffic to internal services.

  * **BeyondCorp / Cloudflare Access** : Google's BeyondCorp model removes the VPN entirely. Access decisions are based on device identity, user identity, and context, not network location.




## Example: zero-trust access policy via proxy

policies:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: "api-access"

subject: "service:api-gateway"

resource: "app:payment-service"

condition:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- attribute: "tls.client_cert.present"

operator: "equals"

value: true

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- attribute: "request.ip"

operator: "in_cidr"

value: "10.0.0.0/8"

action: "allow"

## Network Segmentation and Micro-Segmentation

Segmentation divides a network into smaller segments to limit attack propagation.

## Traditional Segmentation

Uses VLANs and subnets to separate traffic. A web server resides in one subnet, a database server in another. Firewalls control traffic between subnets.

[Internet] -> [DMZ: Web Servers] -> [App Tier] -> [DB Tier]

## Micro-Segmentation

Micro-segmentation takes segmentation to the individual workload level. In a cloud environment, every workload has its own security group that allows traffic only from specific sources on specific ports.

## AWS Security Group for a database instance

resource "aws_security_group" "db" {

ingress {

from_port = 5432

to_port = 5432

protocol = "tcp"

security_groups = [aws_security_group.app.id]

}

egress {

from_port = 0

to_port = 0

protocol = "-1"

cidr_blocks = ["0.0.0.0/0"]

}

}

Micro-segmentation is essential in Kubernetes environments. Network policies control which pods can communicate.

## Kubernetes network policy

apiVersion: networking.k8s.io/v1

kind: NetworkPolicy

metadata:

name: api-allow

spec:

podSelector:

matchLabels:

app: api

ingress:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- from:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- podSelector:

matchLabels:

app: frontend

ports:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- port: 8080

## Conclusion

Network security has evolved from simple perimeter firewalls to sophisticated zero-trust architectures. The fundamentals still matter: proper firewall rules, careful VPN use, intrusion detection, and network segmentation. But the trend is clear — the network boundary is disappearing, and security must follow the workload, not the perimeter.

**See also:** [Zero Trust Architecture for Startups](</en/security/zero-trust-architecture.html>), [Cloud Security Basics: Shared Responsibility Model Explained](</en/security/cloud-security-basics.html>), [Zero Trust Networking: Architecture and Implementation Guide](</en/security/zero-trust-networking.html>).

**See also:** [Cloud Security Basics: Shared Responsibility Model Explained](</en/security/cloud-security-basics.html>), [Zero Trust Architecture for Startups](</en/security/zero-trust-architecture.html>), [Zero Trust Networking: Architecture and Implementation Guide](</en/security/zero-trust-networking.html>)

**See also:** [Cloud Security Basics: Shared Responsibility Model Explained](</en/security/cloud-security-basics.html>), [Zero Trust Architecture for Startups](</en/security/zero-trust-architecture.html>), [Zero Trust Networking: Architecture and Implementation Guide](</en/security/zero-trust-networking.html>)

**See also:** [Cloud Security Basics: Shared Responsibility Model Explained](</en/security/cloud-security-basics.html>), [Zero Trust Architecture for Startups](</en/security/zero-trust-architecture.html>), [Zero Trust Networking: Architecture and Implementation Guide](</en/security/zero-trust-networking.html>)

**See also:** [Cloud Security Basics: Shared Responsibility Model Explained](</en/security/cloud-security-basics.html>), [Zero Trust Architecture for Startups](</en/security/zero-trust-architecture.html>), [Zero Trust Networking: Architecture and Implementation Guide](</en/security/zero-trust-networking.html>)

**See also:** [Cloud Security Basics: Shared Responsibility Model Explained](</en/security/cloud-security-basics.html>), [Zero Trust Architecture for Startups](</en/security/zero-trust-architecture.html>), [Zero Trust Networking: Architecture and Implementation Guide](</en/security/zero-trust-networking.html>)

**See also:** [Mobile Application Security Guide](</en/security/mobile-security.html>), [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>)

**See also:** [Mobile Application Security Guide](</en/security/mobile-security.html>), [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>)

**See also:** [Mobile Application Security Guide](</en/security/mobile-security.html>), [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>)

**See also:** [Mobile Application Security Guide](</en/security/mobile-security.html>), [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>)

**See also:** [Mobile Application Security Guide](</en/security/mobile-security.html>), [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>)

**See also:** [Mobile Application Security Guide](</en/security/mobile-security.html>), [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>)

**See also:** [Mobile Application Security Guide](</en/security/mobile-security.html>), [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>)

**See also:** [Mobile Application Security Guide](</en/security/mobile-security.html>), [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>)

**See also:** [Mobile Application Security Guide](</en/security/mobile-security.html>), [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>)

**See also:** [Mobile Application Security Guide](</en/security/mobile-security.html>), [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>)

**See also:** [Mobile Application Security Guide](</en/security/mobile-security.html>), [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>)

**See also:** [Mobile Application Security Guide](</en/security/mobile-security.html>), [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>)
