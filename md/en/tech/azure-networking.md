---
title: "Azure Networking: VNets, Peering, Azure Firewall, and Load Balancing"
description: "Comprehensive guide to Azure networking covering Virtual Networks, VNet peering, Azure Firewall, Load Balancer, Application Gateway, and network security best practices."
date: 2026-01-01
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/azure-networking.html
---

# Azure Networking: VNets, Peering, Azure Firewall, and Load Balancing

## Introduction

Microsoft Azure provides a comprehensive networking portfolio designed for hybrid cloud architectures. Azure Virtual Network (VNet) is the foundational building block, offering network isolation and connectivity for Azure resources. Azure's networking model differs significantly from AWS and GCP, with unique concepts like network security groups at the subnet level, Azure Firewall as a managed service, and Azure DNS Private Zones.

This article covers Azure VNet design, VNet peering, Azure Firewall, Load Balancer, Application Gateway, and network security practices.

## Virtual Networks and Subnet Design

Azure VNets are regional resources. Each VNet has a CIDR block and contains subnets within a single region. Subnets can be delegated to specific Azure services like Azure App Service or Azure SQL Managed Instance.

Azure reserves five IP addresses per subnet (network, first, second, last two). Subnets cannot be resized after creation without recreation, making initial CIDR planning critical. A recommended design is at least /24 subnets for each application tier, sized generously to accommodate future growth.

Network Security Groups (NSGs) filter traffic at the subnet or network interface level. NSGs support both allow and deny rules with stateful behavior. Default rules block all inbound traffic from the internet and allow outbound traffic, as well as internal VNet traffic and Azure Load Balancer health probes.

az network nsg rule create \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--resource-group my-rg --nsg-name web-nsg \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--name Allow-HTTP --priority 100 \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--direction Inbound --access Allow \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--protocol Tcp --destination-port-ranges 80

## VNet Peering

VNet Peering connects two VNets within the same region (or different regions via Global VNet Peering) using Azure's backbone network. Peered VNets enable resources to communicate with private IP addresses with low latency.

Peering is not transitive — VNet A to VNet B and VNet B to VNet C does not connect A to C. For hub-and-spoke topologies, a hub VNet with peering to all spoke VNets requires explicit two-way peering between the hub and each spoke.

Gateway transit enables spoke VNets to use the hub's VPN gateway for hybrid connectivity without deploying VPN gateways in every spoke — a significant cost optimization.

## Azure Firewall

Azure Firewall is a managed cloud-native firewall service with built-in high availability and auto-scaling. It provides application (FQDN) and network-level filtering, threat intelligence integration, and outbound SNAT support.

Application rules filter outbound HTTP/HTTPS traffic by FQDN. Network rules filter traffic by IP address, port, and protocol. DNAT rules translate inbound traffic to internal resources.

Azure Firewall Manager provides centralized policy management across multiple firewalls in a hub-and-spoke topology. Firewall policies are resources that can be assigned to multiple firewalls, enabling consistent security rules across Azure regions.

For organizations requiring web application firewall (WAF) capabilities, Azure Application Gateway with WAF provides protection against OWASP Top 10 vulnerabilities at Layer 7.

## Azure Load Balancer and Application Gateway

Azure Load Balancer distributes inbound traffic at Layer 4 (TCP/UDP) across virtual machine instances. It supports public and internal load balancing, port forwarding, and outbound SNAT. The Standard SKU provides zone-redundancy and advanced health probes.

Key features include:

  * Backend pools of VMs or VMSS instances.

  * Health probes (TCP, HTTP, HTTPS) that determine backend availability.

  * Session persistence via source IP affinity.

  * Outbound rules for SNAT configuration.




Azure Application Gateway operates at Layer 7, providing HTTP/HTTPS load balancing with TLS termination, URL-based routing, cookie-based session affinity, and a built-in Web Application Firewall.

az network application-gateway create \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--name app-gateway --resource-group my-rg \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--sku WAF_v2 --capacity 2 \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--frontend-port 443 \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--http-settings-cookie-based-affinity Enabled

## Azure DNS and Private Zones

Azure DNS hosts domains and provides name resolution using Azure infrastructure. Azure Private DNS Zones enable internal name resolution within VNets without custom DNS servers. Private zones can be linked to multiple VNets, providing consistent internal DNS resolution across peered networks.

Auto-registration in private zones automatically creates DNS records for VMs, eliminating manual DNS entry management.

## Hybrid Connectivity

Azure VPN Gateway connects on-premises networks to Azure via IPsec tunnels. Active-Active mode provides high availability with two active tunnels. ExpressRoute provides dedicated private connectivity with higher bandwidth guarantees and lower latency than VPN.

ExpressRoute with Global Reach enables on-premises sites connected to different ExpressRoute circuits to communicate through Microsoft's network, eliminating the need for MPLS between data centers.

## Conclusion

Azure's networking services are designed for enterprise hybrid cloud scenarios. VNet peering provides connectivity within Azure, Azure Firewall delivers centralized security, and Application Gateway enables intelligent traffic distribution. NSGs provide granular traffic filtering, while ExpressRoute and VPN Gateway connect on-premises networks. Understanding these services and their interactions is essential for designing secure, scalable Azure network architectures.

**See also:** [Docker Networking: Bridge, Overlay, Host, Macvlan, and Troubleshooting](</en/tech/docker-networking.html>), [AWS VPC Design: Subnets, NAT, Peering, Transit Gateway, and Security Groups](</en/tech/aws-vpc-design.html>), [Nginx Configuration: Performance and Security](</en/tech/nginx-configuration.html>).

**See also:** [AWS VPC Design: Subnets, NAT, Peering, Transit Gateway, and Security Groups](</en/tech/aws-vpc-design.html>), [Docker Networking: Bridge, Overlay, Host, Macvlan, and Troubleshooting](</en/tech/docker-networking.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>)

**See also:** [AWS VPC Design: Subnets, NAT, Peering, Transit Gateway, and Security Groups](</en/tech/aws-vpc-design.html>), [Docker Networking: Bridge, Overlay, Host, Macvlan, and Troubleshooting](</en/tech/docker-networking.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>)

**See also:** [AWS VPC Design: Subnets, NAT, Peering, Transit Gateway, and Security Groups](</en/tech/aws-vpc-design.html>), [Docker Networking: Bridge, Overlay, Host, Macvlan, and Troubleshooting](</en/tech/docker-networking.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>)

**See also:** [AWS VPC Design: Subnets, NAT, Peering, Transit Gateway, and Security Groups](</en/tech/aws-vpc-design.html>), [Docker Networking: Bridge, Overlay, Host, Macvlan, and Troubleshooting](</en/tech/docker-networking.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>)

**See also:** [AWS VPC Design: Subnets, NAT, Peering, Transit Gateway, and Security Groups](</en/tech/aws-vpc-design.html>), [Docker Networking: Bridge, Overlay, Host, Macvlan, and Troubleshooting](</en/tech/docker-networking.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>)

**See also:** [GCP Networking: VPCs, Cloud NAT, Private Google Access, and Shared VPC](</en/tech/gcp-networking.html>), [Incident Management: Severity Levels, Response Process, and Postmortems](</en/tech/incident-management.html>), [Prometheus Deep Dive: Metrics, PromQL, Alerting, and High Availability](</en/tech/prometheus-deep-dive.html>)

**See also:** [GCP Networking: VPCs, Cloud NAT, Private Google Access, and Shared VPC](</en/tech/gcp-networking.html>), [Incident Management: Severity Levels, Response Process, and Postmortems](</en/tech/incident-management.html>), [Prometheus Deep Dive: Metrics, PromQL, Alerting, and High Availability](</en/tech/prometheus-deep-dive.html>)

**See also:** [GCP Networking: VPCs, Cloud NAT, Private Google Access, and Shared VPC](</en/tech/gcp-networking.html>), [Incident Management: Severity Levels, Response Process, and Postmortems](</en/tech/incident-management.html>), [Prometheus Deep Dive: Metrics, PromQL, Alerting, and High Availability](</en/tech/prometheus-deep-dive.html>)

**See also:** [GCP Networking: VPCs, Cloud NAT, Private Google Access, and Shared VPC](</en/tech/gcp-networking.html>), [Incident Management: Severity Levels, Response Process, and Postmortems](</en/tech/incident-management.html>), [Prometheus Deep Dive: Metrics, PromQL, Alerting, and High Availability](</en/tech/prometheus-deep-dive.html>)

**See also:** [GCP Networking: VPCs, Cloud NAT, Private Google Access, and Shared VPC](</en/tech/gcp-networking.html>), [Incident Management: Severity Levels, Response Process, and Postmortems](</en/tech/incident-management.html>), [Prometheus Deep Dive: Metrics, PromQL, Alerting, and High Availability](</en/tech/prometheus-deep-dive.html>)

**See also:** [GCP Networking: VPCs, Cloud NAT, Private Google Access, and Shared VPC](</en/tech/gcp-networking.html>), [Incident Management: Severity Levels, Response Process, and Postmortems](</en/tech/incident-management.html>), [Prometheus Deep Dive: Metrics, PromQL, Alerting, and High Availability](</en/tech/prometheus-deep-dive.html>)

**See also:** [GCP Networking: VPCs, Cloud NAT, Private Google Access, and Shared VPC](</en/tech/gcp-networking.html>), [Incident Management: Severity Levels, Response Process, and Postmortems](</en/tech/incident-management.html>), [Prometheus Deep Dive: Metrics, PromQL, Alerting, and High Availability](</en/tech/prometheus-deep-dive.html>)

**See also:** [GCP Networking: VPCs, Cloud NAT, Private Google Access, and Shared VPC](</en/tech/gcp-networking.html>), [Incident Management: Severity Levels, Response Process, and Postmortems](</en/tech/incident-management.html>), [Prometheus Deep Dive: Metrics, PromQL, Alerting, and High Availability](</en/tech/prometheus-deep-dive.html>)

**See also:** [GCP Networking: VPCs, Cloud NAT, Private Google Access, and Shared VPC](</en/tech/gcp-networking.html>), [Incident Management: Severity Levels, Response Process, and Postmortems](</en/tech/incident-management.html>), [Prometheus Deep Dive: Metrics, PromQL, Alerting, and High Availability](</en/tech/prometheus-deep-dive.html>)
