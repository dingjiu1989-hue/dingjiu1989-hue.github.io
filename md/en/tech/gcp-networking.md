---
title: "GCP Networking: VPCs, Cloud NAT, Private Google Access, and Shared VPC"
description: "Technical exploration of Google Cloud networking covering VPC design, Cloud NAT configuration, Private Google Access, Shared VPC architecture, and Cloud Interconnect."
date: 2026-01-01
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/gcp-networking.html
---

# GCP Networking: VPCs, Cloud NAT, Private Google Access, and Shared VPC

## Introduction

Google Cloud Platform (GCP) offers a distinctive networking model compared to AWS and Azure. GCP VPCs are global resources, not regional — a single VPC spans all regions, simplifying multi-region architectures. Firewall rules are distributed and stateful, and Cloud NAT provides managed outbound connectivity. Understanding these differences is critical for designing efficient and secure GCP networks.

This article covers GCP VPC design, Cloud NAT, Private Google Access, Shared VPC, and Cloud Interconnect.

## Global VPCs and Subnet Design

Unlike AWS VPCs, which are regional, GCP VPCs are global. Subnets are regional but belong to a global VPC. This design enables seamless multi-region communication without VPC peering or transit gateways. A single global VPC with subnets in each region provides a flat network for global services.

Subnet CIDR ranges must be unique within a VPC and cannot overlap. GCP reserves four IP addresses per subnet (network, first, second, and last). Subnets can be expanded without downtime by adding secondary CIDR ranges — a valuable feature not available in AWS.

gcloud compute networks create my-global-vpc --subnet-mode=custom

gcloud compute networks subnets create us-east-subnet \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--network=my-global-vpc --region=us-east1 \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--range=10.0.1.0/24 \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--secondary-range=services=10.1.0.0/16

## Cloud NAT

Cloud NAT provides outbound internet connectivity for private instances. It uses NAT gateways managed by Google, with no manual patching or scaling required. Cloud NAT supports IP masquerading, allowing thousands of instances to share a single external IP or pool.

Key configuration parameters include minimum and maximum ports per VM, NAT IP allocation (manual or automatic), and timeout settings. Cloud NAT integrates with Cloud Router for dynamic route exchange. Each Cloud NAT gateway is regional but spans all zones in a region.

## Private Google Access

Private Google Access enables on-premises or VM instances without external IPs to reach Google APIs and services (Cloud Storage, BigQuery, Cloud Functions) through Google's private network. Traffic never traverses the public internet.

Configuration requires a VPC network with Private Google Access enabled on the subnet. DNS resolution for `googleapis.com` must resolve to private IPs. For hybrid connectivity, on-premises networks access Google APIs privately through Cloud VPN or Cloud Interconnect.

## Shared VPC Architecture

Shared VPC allows an organization to centrally manage a VPC from a host project while delegating subnet access to multiple service projects. This is GCP's answer to multi-account networking requirements.

gcloud compute shared-vpc enable host-project-id

gcloud compute shared-vpc associated-projects add host-project-id \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--service-project service-project-id

Shared VPC provides centralized control of firewall rules, VPN tunnels, and NAT gateways while giving service project owners autonomy over their resources. IAM roles control subnet-level access: `compute.networkUser` grants access to specific subnets.

The `xpn` (Cross-Project Networking) configuration is essential for organizations using GCP's resource hierarchy — organization, folders, projects — and following the hub-and-spoke network model.

## Cloud Interconnect

Cloud Interconnect provides dedicated connectivity between on-premises networks and GCP. Dedicated Interconnect offers 10 Gbps or 100 Gbps connections with a service availability SLA of 99.99% when configured with redundant connections. Partner Interconnect provides lower bandwidth options (50 Mbps to 10 Gbps) through supported service providers.

Cloud Interconnect reduces data transfer costs, improves reliability over internet-based VPN, and provides consistent latency. It pairs with Cloud Router for BGP route exchange and supports VLAN attachments for network segmentation.

For smaller deployments or fallback connectivity, Cloud VPN provides IPsec tunnels over the public internet with up to 3 Gbps per tunnel using HA VPN gateways.

## VPC Firewall Rules and Network Tags

GCP firewall rules are stateful, global, and distributed. They are applied at the instance level rather than the subnet level. Rules can be defined to allow or deny traffic based on network tags, service accounts, source IP ranges, or target IP ranges.

Network tags are the primary mechanism for applying firewall rules to groups of instances. Service account-based rules provide identity-aware firewall control, allowing access policies to follow workloads across instance groups.

gcloud compute firewall-rules create allow-http \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--network=my-global-vpc \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--direction=INGRESS --priority=1000 \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--target-tags=http-server \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--allow=tcp:80

## Conclusion

GCP's global VPC model simplifies multi-region architectures and reduces networking complexity. Cloud NAT provides managed outbound connectivity, Shared VPC enables centralized network governance, and Cloud Interconnect delivers dedicated hybrid connectivity. Understanding these services enables network architects to design GCP networks that are secure, scalable, and cost-effective.

**See also:** [Grafana Dashboards: Panels, Variables, Annotations, and Alerting](</en/tech/grafana-dashboards.html>), [AWS VPC Design: Subnets, NAT, Peering, Transit Gateway, and Security Groups](</en/tech/aws-vpc-design.html>), [Cloud Capacity Planning: Auto-Scaling, Reserved Instances, Spot Instances, and Demand Forecasting](</en/tech/capacity-planning-cloud.html>).

**See also:** [AWS VPC Design: Subnets, NAT, Peering, Transit Gateway, and Security Groups](</en/tech/aws-vpc-design.html>), [Grafana Dashboards: Panels, Variables, Annotations, and Alerting](</en/tech/grafana-dashboards.html>), [Cloud Capacity Planning: Auto-Scaling, Reserved Instances, Spot Instances, and Demand Forecasting](</en/tech/capacity-planning-cloud.html>)

**See also:** [AWS VPC Design: Subnets, NAT, Peering, Transit Gateway, and Security Groups](</en/tech/aws-vpc-design.html>), [Grafana Dashboards: Panels, Variables, Annotations, and Alerting](</en/tech/grafana-dashboards.html>), [Cloud Capacity Planning: Auto-Scaling, Reserved Instances, Spot Instances, and Demand Forecasting](</en/tech/capacity-planning-cloud.html>)

**See also:** [AWS VPC Design: Subnets, NAT, Peering, Transit Gateway, and Security Groups](</en/tech/aws-vpc-design.html>), [Grafana Dashboards: Panels, Variables, Annotations, and Alerting](</en/tech/grafana-dashboards.html>), [Cloud Capacity Planning: Auto-Scaling, Reserved Instances, Spot Instances, and Demand Forecasting](</en/tech/capacity-planning-cloud.html>)

**See also:** [AWS VPC Design: Subnets, NAT, Peering, Transit Gateway, and Security Groups](</en/tech/aws-vpc-design.html>), [Grafana Dashboards: Panels, Variables, Annotations, and Alerting](</en/tech/grafana-dashboards.html>), [Cloud Capacity Planning: Auto-Scaling, Reserved Instances, Spot Instances, and Demand Forecasting](</en/tech/capacity-planning-cloud.html>)

**See also:** [AWS VPC Design: Subnets, NAT, Peering, Transit Gateway, and Security Groups](</en/tech/aws-vpc-design.html>), [Grafana Dashboards: Panels, Variables, Annotations, and Alerting](</en/tech/grafana-dashboards.html>), [Cloud Capacity Planning: Auto-Scaling, Reserved Instances, Spot Instances, and Demand Forecasting](</en/tech/capacity-planning-cloud.html>)

**See also:** [Docker Networking: Bridge, Overlay, Host, Macvlan, and Troubleshooting](</en/tech/docker-networking.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>)

**See also:** [Docker Networking: Bridge, Overlay, Host, Macvlan, and Troubleshooting](</en/tech/docker-networking.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>)

**See also:** [Docker Networking: Bridge, Overlay, Host, Macvlan, and Troubleshooting](</en/tech/docker-networking.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>)

**See also:** [Docker Networking: Bridge, Overlay, Host, Macvlan, and Troubleshooting](</en/tech/docker-networking.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>)

**See also:** [Docker Networking: Bridge, Overlay, Host, Macvlan, and Troubleshooting](</en/tech/docker-networking.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>)

**See also:** [Docker Networking: Bridge, Overlay, Host, Macvlan, and Troubleshooting](</en/tech/docker-networking.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>)

**See also:** [Docker Networking: Bridge, Overlay, Host, Macvlan, and Troubleshooting](</en/tech/docker-networking.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>)

**See also:** [Docker Networking: Bridge, Overlay, Host, Macvlan, and Troubleshooting](</en/tech/docker-networking.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>)

**See also:** [Docker Networking: Bridge, Overlay, Host, Macvlan, and Troubleshooting](</en/tech/docker-networking.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>)

**See also:** [Docker Networking: Bridge, Overlay, Host, Macvlan, and Troubleshooting](</en/tech/docker-networking.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>)
