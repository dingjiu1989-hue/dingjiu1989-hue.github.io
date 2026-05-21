---
title: "ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization"
description: "Comprehensive guide to ELK Stack covering Elasticsearch cluster setup, Logstash pipeline configuration, Kibana visualization, performance tuning, and index lifecycle management."
date: 2026-01-01
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/elk-stack-setup.html
---

# ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization

## Introduction

The ELK Stack — Elasticsearch, Logstash, and Kibana — is the most widely deployed open-source log management platform. Elasticsearch provides distributed full-text search and analytics, Logstash offers server-side data processing, and Kibana delivers visualization and exploration capabilities. The stack was later joined by Beats, lightweight data shippers that extend the Elastic ecosystem.

This article covers ELK stack setup, Logstash pipeline configuration, performance tuning, and index lifecycle management (ILM).

## Elasticsearch: The Storage and Search Engine

Elasticsearch is a distributed, RESTful search and analytics engine built on Apache Lucene. Data is organized into indices, which are collections of documents. Each index is divided into shards, which are distributed across nodes in a cluster.

A production Elasticsearch cluster should have a minimum of three master-eligible nodes for high availability. Data nodes store data and perform CRUD operations. Dedicated coordinating-only nodes handle incoming requests and distribute them to data nodes, improving query performance for clusters with complex search patterns.

Key configuration parameters include `indices.memory.index_buffer_size`, `thread_pool.search.queue_size`, and `discovery.seed_hosts` for cluster formation. The `elasticsearch.yml` configuration file controls all node-level settings.

Mapping defines how documents and their fields are stored and indexed. Dynamic mapping auto-detects field types at index time, but explicit mapping is strongly recommended for production use to avoid type conflicts.

## Logstash: Data Processing Pipeline

Logstash is a server-side data processing pipeline that ingests data from multiple sources, transforms it, and sends it to a destination. The pipeline has three stages: input, filter, and output.

input {

beats {

port => 5044

}

}

filter {

grok {

match => { "message" => "%{COMBINEDAPACHELOG}" }

}

geoip {

source => "clientip"

}

date {

match => ["timestamp", "dd/MMM/yyyy:HH:mm:ss Z"]

}

}

output {

elasticsearch {

hosts => ["https://elasticsearch:9200"]

index => "apache-logs-%{+YYYY.MM.dd}"

ssl => true

cacert => "/etc/logstash/certs/http_ca.crt"

}

}

The grok filter is the most powerful Logstash plugin, parsing unstructured log data into structured fields using predefined patterns. Performance considerations: reduce the number of filter plugins, use conditional logic to skip unnecessary processing, and configure pipeline workers to match CPU cores.

## Kibana: Visualization and Exploration

Kibana provides the user interface for the ELK stack. The Discover tab allows ad-hoc log exploration with Lucene or KQL (Kibana Query Language). Visualizations are organized into dashboards providing operational views.

Lens is Kibana's drag-and-drop visualization builder, enabling rapid dashboard creation without learning aggregation syntax. Canvas provides pixel-perfect infographic-style presentations. Maps visualizes geospatial data with multiple layers.

Kibana Alerting provides rule types for threshold conditions, anomaly detection, and tracking containment. Rules can trigger actions via email, Slack, PagerDuty, or webhooks.

## Performance Tuning

Elasticsearch performance tuning begins with shard sizing: 20-40 GB per shard is the recommended range. Too many small shards waste resources; too few large shards slow recovery. Refresh interval should be increased to 30-60 seconds for bulk indexing workloads.

Heap size should be set to no more than 50% of available RAM, with a hard cap of 31 GB (above which compressed object pointers are disabled in the JVM). The `_forcemerge` API merges segments after indexing completes, improving query performance.

Logstash performance depends on pipeline workers, batch size, and batch delay. Setting `pipeline.workers` to match CPU core count and `pipeline.batch.size` to 125-500 generally provides good throughput.

## Index Lifecycle Management

ILM automates index management through policy-driven phases: hot, warm, cold, frozen, and delete.

{

"policy": {

"phases": {

"hot": {

"min_age": "0ms",

"actions": {

"rollover": { "max_size": "50GB", "max_age": "30d" }

}

},

"warm": {

"min_age": "30d",

"actions": { "allocate": { "require": { "data_type": "warm" } } }

},

"cold": {

"min_age": "90d",

"actions": { "freeze": {} }

},

"delete": {

"min_age": "365d",

"actions": { "delete": {} }

}

}

}

}

ILM reduces manual index management overhead, optimizes storage costs, and ensures data retention policies are consistently enforced.

## Conclusion

The ELK stack provides a complete log management solution. Elasticsearch delivers scalable search and analytics, Logstash provides flexible data processing, and Kibana enables powerful visualization. With careful performance tuning and ILM policies, the ELK stack can handle terabytes of daily log data while maintaining query performance and controlling storage costs.

**See also:** [Node.js Performance Optimization Guide](</en/tech/nodejs-performance.html>), [Incident Management: Severity Levels, Response Process, and Postmortems](</en/tech/incident-management.html>), [Azure Networking: VNets, Peering, Azure Firewall, and Load Balancing](</en/tech/azure-networking.html>).

**See also:** [Node.js Performance Optimization Guide](</en/tech/nodejs-performance.html>), [Azure Networking: VNets, Peering, Azure Firewall, and Load Balancing](</en/tech/azure-networking.html>), [Cloud Capacity Planning: Auto-Scaling, Reserved Instances, Spot Instances, and Demand Forecasting](</en/tech/capacity-planning-cloud.html>)

**See also:** [Node.js Performance Optimization Guide](</en/tech/nodejs-performance.html>), [Azure Networking: VNets, Peering, Azure Firewall, and Load Balancing](</en/tech/azure-networking.html>), [Cloud Capacity Planning: Auto-Scaling, Reserved Instances, Spot Instances, and Demand Forecasting](</en/tech/capacity-planning-cloud.html>)

**See also:** [Node.js Performance Optimization Guide](</en/tech/nodejs-performance.html>), [Azure Networking: VNets, Peering, Azure Firewall, and Load Balancing](</en/tech/azure-networking.html>), [Cloud Capacity Planning: Auto-Scaling, Reserved Instances, Spot Instances, and Demand Forecasting](</en/tech/capacity-planning-cloud.html>)

**See also:** [Node.js Performance Optimization Guide](</en/tech/nodejs-performance.html>), [Azure Networking: VNets, Peering, Azure Firewall, and Load Balancing](</en/tech/azure-networking.html>), [Cloud Capacity Planning: Auto-Scaling, Reserved Instances, Spot Instances, and Demand Forecasting](</en/tech/capacity-planning-cloud.html>)

**See also:** [Node.js Performance Optimization Guide](</en/tech/nodejs-performance.html>), [Azure Networking: VNets, Peering, Azure Firewall, and Load Balancing](</en/tech/azure-networking.html>), [Cloud Capacity Planning: Auto-Scaling, Reserved Instances, Spot Instances, and Demand Forecasting](</en/tech/capacity-planning-cloud.html>)

**See also:** [Docker Networking: Bridge, Overlay, Host, Macvlan, and Troubleshooting](</en/tech/docker-networking.html>), [GCP Networking: VPCs, Cloud NAT, Private Google Access, and Shared VPC](</en/tech/gcp-networking.html>), [Grafana Dashboards: Panels, Variables, Annotations, and Alerting](</en/tech/grafana-dashboards.html>)

**See also:** [Docker Networking: Bridge, Overlay, Host, Macvlan, and Troubleshooting](</en/tech/docker-networking.html>), [GCP Networking: VPCs, Cloud NAT, Private Google Access, and Shared VPC](</en/tech/gcp-networking.html>), [Grafana Dashboards: Panels, Variables, Annotations, and Alerting](</en/tech/grafana-dashboards.html>)

**See also:** [Docker Networking: Bridge, Overlay, Host, Macvlan, and Troubleshooting](</en/tech/docker-networking.html>), [GCP Networking: VPCs, Cloud NAT, Private Google Access, and Shared VPC](</en/tech/gcp-networking.html>), [Grafana Dashboards: Panels, Variables, Annotations, and Alerting](</en/tech/grafana-dashboards.html>)

**See also:** [Docker Networking: Bridge, Overlay, Host, Macvlan, and Troubleshooting](</en/tech/docker-networking.html>), [GCP Networking: VPCs, Cloud NAT, Private Google Access, and Shared VPC](</en/tech/gcp-networking.html>), [Grafana Dashboards: Panels, Variables, Annotations, and Alerting](</en/tech/grafana-dashboards.html>)

**See also:** [Docker Networking: Bridge, Overlay, Host, Macvlan, and Troubleshooting](</en/tech/docker-networking.html>), [GCP Networking: VPCs, Cloud NAT, Private Google Access, and Shared VPC](</en/tech/gcp-networking.html>), [Grafana Dashboards: Panels, Variables, Annotations, and Alerting](</en/tech/grafana-dashboards.html>)

**See also:** [Docker Networking: Bridge, Overlay, Host, Macvlan, and Troubleshooting](</en/tech/docker-networking.html>), [GCP Networking: VPCs, Cloud NAT, Private Google Access, and Shared VPC](</en/tech/gcp-networking.html>), [Grafana Dashboards: Panels, Variables, Annotations, and Alerting](</en/tech/grafana-dashboards.html>)

**See also:** [Docker Networking: Bridge, Overlay, Host, Macvlan, and Troubleshooting](</en/tech/docker-networking.html>), [GCP Networking: VPCs, Cloud NAT, Private Google Access, and Shared VPC](</en/tech/gcp-networking.html>), [Grafana Dashboards: Panels, Variables, Annotations, and Alerting](</en/tech/grafana-dashboards.html>)

**See also:** [Docker Networking: Bridge, Overlay, Host, Macvlan, and Troubleshooting](</en/tech/docker-networking.html>), [GCP Networking: VPCs, Cloud NAT, Private Google Access, and Shared VPC](</en/tech/gcp-networking.html>), [Grafana Dashboards: Panels, Variables, Annotations, and Alerting](</en/tech/grafana-dashboards.html>)

**See also:** [Docker Networking: Bridge, Overlay, Host, Macvlan, and Troubleshooting](</en/tech/docker-networking.html>), [GCP Networking: VPCs, Cloud NAT, Private Google Access, and Shared VPC](</en/tech/gcp-networking.html>), [Grafana Dashboards: Panels, Variables, Annotations, and Alerting](</en/tech/grafana-dashboards.html>)

**See also:** [Docker Networking: Bridge, Overlay, Host, Macvlan, and Troubleshooting](</en/tech/docker-networking.html>), [GCP Networking: VPCs, Cloud NAT, Private Google Access, and Shared VPC](</en/tech/gcp-networking.html>), [Grafana Dashboards: Panels, Variables, Annotations, and Alerting](</en/tech/grafana-dashboards.html>)

**See also:** [Docker Networking: Bridge, Overlay, Host, Macvlan, and Troubleshooting](</en/tech/docker-networking.html>), [GCP Networking: VPCs, Cloud NAT, Private Google Access, and Shared VPC](</en/tech/gcp-networking.html>), [Grafana Dashboards: Panels, Variables, Annotations, and Alerting](</en/tech/grafana-dashboards.html>)

**See also:** [Docker Networking: Bridge, Overlay, Host, Macvlan, and Troubleshooting](</en/tech/docker-networking.html>), [GCP Networking: VPCs, Cloud NAT, Private Google Access, and Shared VPC](</en/tech/gcp-networking.html>), [Grafana Dashboards: Panels, Variables, Annotations, and Alerting](</en/tech/grafana-dashboards.html>)
