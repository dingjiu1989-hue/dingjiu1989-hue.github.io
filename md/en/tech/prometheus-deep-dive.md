---
title: "Prometheus Deep Dive: Metrics, PromQL, Alerting, and High Availability"
description: "A comprehensive look at Prometheus monitoring covering metrics collection, PromQL queries, recording rules, alertmanager setup, and high availability architecture."
date: 2026-01-02
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/prometheus-deep-dive.html
---

# Prometheus Deep Dive: Metrics, PromQL, Alerting, and High Availability

## Introduction

Prometheus has emerged as the de facto standard for monitoring cloud-native infrastructure. Originally developed at SoundCloud and later donated to the Cloud Native Computing Foundation (CNCF), it has become the second graduated project after Kubernetes. Its pull-based metrics collection model, powerful query language, and multi-dimensional data model differentiate it from traditional monitoring solutions like Nagios or Zabbix.

This article explores Prometheus architecture, metrics collection, PromQL, recording rules, alerting, and strategies for high availability.

## Metrics Collection Architecture

Prometheus scrapes metrics from instrumented targets over HTTP. Targets expose metrics at a standard endpoint, typically `/metrics`, in plaintext format. Exporters bridge the gap for third-party systems: the Node Exporter provides OS-level metrics, the Blackbox Exporter probes external endpoints, and numerous specialized exporters exist for databases, message queues, and cloud services.

A key design choice is the pull model. Prometheus scrapes targets on a configurable interval (default 15 seconds). This simplifies health detection — if a target stops responding, Prometheus immediately detects the absence of metrics. Service discovery integrations for Kubernetes, Consul, EC2, and DNS allow targets to be dynamically discovered without manual reconfiguration.

## The Multi-Dimensional Data Model

Prometheus stores metrics as time series identified by a metric name and a set of key-value labels. For example:

http_requests_total{method="POST", endpoint="/api/users", status="200"}

Labels enable dimensionality. You can aggregate, filter, and compute across any label combination without pre-defining aggregation hierarchies — a significant advantage over tools like Graphite.

Metric types include counters (monotonically increasing values), gauges (arbitrarily fluctuating values), histograms (observations counted into configurable buckets), and summaries (quantiles computed on the client). Choosing the right metric type is critical for accurate monitoring and cost-effective cardinality management.

## PromQL: The Query Language

PromQL is the heart of Prometheus. It supports instant vector queries, range vector queries, aggregation operators, and binary arithmetic.

Key patterns include:

  * Rate calculation: `rate(http_requests_total[5m])` computes per-second request rate averaged over 5 minutes.

  * Aggregation: `sum by (status) (rate(http_requests_total[5m]))` aggregates rates by status code.

  * Percentiles: `histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))` computes the 99th percentile latency.

  * Offset modifier: `rate(http_requests_total[5m] offset 1w)` compares current traffic with last week's.




Understanding PromQL vector matching — one-to-one, many-to-one, and group modifiers — is essential for writing correct queries involving multiple metrics.

## Recording Rules

Recording rules compute frequently needed or computationally expensive expressions in advance. They re-encapsulate a PromQL expression as a new time series, scraped alongside other metrics.

groups:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: recording_rules

interval: 30s

rules:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- record: instance:node_cpu_utilization:rate5m

expr: 100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

Recording rules reduce query latency for dashboards and provide a stable interface between metric collection and consumption.

## Alerting with Alertmanager

Alerting in Prometheus is a two-phase process. The Prometheus server evaluates alerting rules and sends firing alerts to Alertmanager, which handles deduplication, silencing, inhibition, and routing.

groups:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: alerting_rules

rules:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- alert: HighCPUUsage

expr: instance:node_cpu_utilization:rate5m > 80

for: 5m

labels:

severity: warning

annotations:

summary: "CPU usage above 80%"

Alertmanager routes alerts to notification channels (PagerDuty, Slack, email) using route trees. Inhibition rules suppress low-severity alerts when high-severity alerts for the same service are firing, reducing noise during major incidents.

## High Availability and Long-Term Storage

Prometheus is designed for reliability, not durability. A single Prometheus server stores data locally — if it fails, historical data is lost. High availability is achieved by running identical pairs of Prometheus servers with the same scrape configuration, both receiving the same data.

For long-term storage, the Thanos and Cortex projects extend Prometheus. Thanos provides global query views across multiple Prometheus instances, unlimited retention via object storage (S3, GCS), and downsampling for fast queries over large time ranges. Cortex offers a horizontally scalable, multi-tenant Prometheus-compatible backend.

## Conclusion

Prometheus fundamentally changed how teams approach monitoring. Its pull model, label-based data model, and powerful PromQL language provide capabilities that traditional tools cannot match. When paired with Thanos for long-term storage and Alertmanager for sophisticated notification routing, Prometheus forms a complete monitoring stack suitable for infrastructure of any scale.

**See also:** [Ansible Automation: Playbooks, Roles, Inventory, and Vault](</en/tech/ansible-automation.html>), [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>).

**See also:** [Ansible Automation: Playbooks, Roles, Inventory, and Vault](</en/tech/ansible-automation.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>), [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>)

**See also:** [Ansible Automation: Playbooks, Roles, Inventory, and Vault](</en/tech/ansible-automation.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>), [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>)

**See also:** [Ansible Automation: Playbooks, Roles, Inventory, and Vault](</en/tech/ansible-automation.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>), [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>)

**See also:** [Ansible Automation: Playbooks, Roles, Inventory, and Vault](</en/tech/ansible-automation.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>), [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>)

**See also:** [Ansible Automation: Playbooks, Roles, Inventory, and Vault](</en/tech/ansible-automation.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>), [Terraform State Management: Remote State, Locking, Migration, and Workspaces](</en/tech/terraform-state-management.html>)

**See also:** [Grafana Dashboards: Panels, Variables, Annotations, and Alerting](</en/tech/grafana-dashboards.html>), [Multi-Cloud Strategy: When and Why, Abstraction Layers, and Cost Comparison](</en/tech/multi-cloud-strategy.html>), [React Server Components](</en/tech/react-server-components.html>)

**See also:** [Grafana Dashboards: Panels, Variables, Annotations, and Alerting](</en/tech/grafana-dashboards.html>), [Multi-Cloud Strategy: When and Why, Abstraction Layers, and Cost Comparison](</en/tech/multi-cloud-strategy.html>), [React Server Components](</en/tech/react-server-components.html>)

**See also:** [Grafana Dashboards: Panels, Variables, Annotations, and Alerting](</en/tech/grafana-dashboards.html>), [Multi-Cloud Strategy: When and Why, Abstraction Layers, and Cost Comparison](</en/tech/multi-cloud-strategy.html>), [React Server Components](</en/tech/react-server-components.html>)

**See also:** [Grafana Dashboards: Panels, Variables, Annotations, and Alerting](</en/tech/grafana-dashboards.html>), [Multi-Cloud Strategy: When and Why, Abstraction Layers, and Cost Comparison](</en/tech/multi-cloud-strategy.html>), [React Server Components](</en/tech/react-server-components.html>)

**See also:** [Grafana Dashboards: Panels, Variables, Annotations, and Alerting](</en/tech/grafana-dashboards.html>), [Multi-Cloud Strategy: When and Why, Abstraction Layers, and Cost Comparison](</en/tech/multi-cloud-strategy.html>), [React Server Components](</en/tech/react-server-components.html>)

**See also:** [Grafana Dashboards: Panels, Variables, Annotations, and Alerting](</en/tech/grafana-dashboards.html>), [Multi-Cloud Strategy: When and Why, Abstraction Layers, and Cost Comparison](</en/tech/multi-cloud-strategy.html>), [React Server Components](</en/tech/react-server-components.html>)

**See also:** [Grafana Dashboards: Panels, Variables, Annotations, and Alerting](</en/tech/grafana-dashboards.html>), [Multi-Cloud Strategy: When and Why, Abstraction Layers, and Cost Comparison](</en/tech/multi-cloud-strategy.html>), [React Server Components](</en/tech/react-server-components.html>)

**See also:** [Grafana Dashboards: Panels, Variables, Annotations, and Alerting](</en/tech/grafana-dashboards.html>), [Multi-Cloud Strategy: When and Why, Abstraction Layers, and Cost Comparison](</en/tech/multi-cloud-strategy.html>), [React Server Components](</en/tech/react-server-components.html>)

**See also:** [Grafana Dashboards: Panels, Variables, Annotations, and Alerting](</en/tech/grafana-dashboards.html>), [Multi-Cloud Strategy: When and Why, Abstraction Layers, and Cost Comparison](</en/tech/multi-cloud-strategy.html>), [React Server Components](</en/tech/react-server-components.html>)
