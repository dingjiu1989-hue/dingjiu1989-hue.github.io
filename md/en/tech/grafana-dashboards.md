---
title: "Grafana Dashboards: Panels, Variables, Annotations, and Alerting"
description: "Technical exploration of Grafana dashboard design covering panel types, template variables, annotations, alerting configuration, and provisioning with infrastructure as code."
date: 2026-01-02
board: tech
url: https://aidev.fit/en/tech/grafana-dashboards.html
---

# Grafana Dashboards: Panels, Variables, Annotations, and Alerting

## Introduction

Grafana has become the industry standard for observability dashboards, providing unified visualization across metrics, logs, traces, and other data sources. Its modular architecture supports Prometheus, Elasticsearch, InfluxDB, Loki, Tempo, and dozens of other backends. Beyond visualization, Grafana has evolved into a full observability platform with alerting, anomaly detection, and incident management capabilities.

This article covers Grafana dashboard design in detail: panel types, template variables, annotations, alerting, and provisioning.

## Panel Types and Visualization Options

Grafana offers a rich set of visualization panels. The time series panel is the workhorse for metric data, supporting line charts, bar charts, and area graphs with multiple display options. The state timeline panel visualizes state changes over time, ideal for showing service health or deployment status.

The stat panel displays a single numeric value with optional sparkline, perfect for showing current CPU usage or error rate. The gauge panel presents values in a radial format. The table panel provides detailed data inspection with sorting, filtering, and field overrides.

The geomap panel renders geographic data on interactive maps, useful for visualizing request origins or data center health. The logs panel streams log lines in real time with highlighting and filtering. The traces panel visualizes distributed trace spans in waterfall format.

Field overrides allow per-field customization without duplicating queries. Transformations transform query results without modifying the data source: merging series, calculating percentages, grouping by field values, and applying mathematical operations.

## Template Variables: Dynamic Dashboards

Template variables make dashboards interactive and reusable. Instead of hardcoding values, queries use variables that users can change via dropdowns at the top of the dashboard.

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Prometheus query using variables

rate(http_requests_total{job="$job", namespace="$namespace"}[5m])

Variable types include:

  * Query variables populated by querying data sources, e.g., `label_values(job)` in Prometheus.

  * Custom variables with manually defined options.

  * Interval variables for time range controls.

  * Data source variables for switching between backends.




Chained (dependent) variables filter subsequent variable options based on previous selections, enabling drill-down navigation from datacenter to cluster to pod.

## Annotations: Events on Timelines

Annotations overlay events on graph panels, correlating infrastructure changes with metric behavior. Common annotation sources include deployment events from CI/CD pipelines, configuration changes, and incident timestamps.

Grafana supports annotation queries from data sources. For example, annotations can pull deployment timestamps from Loki logs or from a dedicated annotation database. Native annotations are stored in a Grafana internal database and support rich text descriptions.

Using annotations effectively transforms dashboards from metric viewers into forensic tools for understanding what caused metric anomalies.

## Alerting in Grafana

Grafana Alerting (introduced in Grafana 8 and unified in Grafana 9) provides a centralized alert system. Alerts evaluate queries on a schedule and route notifications through contact points.

An alert rule consists of a query, a condition evaluation interval, a pending period, and labels. Multiple rules can be grouped into alert groups. The Alertmanager handles notification routing, grouping, silencing, and inhibition.

groups:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: alert-group

rules:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- alert: HighErrorRate

expr: rate(errors_total[5m]) > 0.01

for: 5m

labels:

severity: critical

Contact points support PagerDuty, Slack, email, webhooks, OpsGenie, VictorOps, Teams, and custom integrations. Notification policies route alerts based on labels and grouping rules.

## Provisioning Dashboards as Code

Grafana supports provisioning dashboards, data sources, alert rules, and contact points through YAML configuration files. This enables infrastructure-as-code workflows for observability.

apiVersion: 1

providers:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: "default"

orgId: 1

folder: "infrastructure"

type: file

options:

path: /etc/grafana/provisioning/dashboards

Dashboards are exported as JSON and version-controlled alongside application code. CI/CD pipelines deploy dashboard changes through Git workflows, enabling peer review and rollback.

## Conclusion

Grafana's composable architecture — panels, variables, annotations, and alerting — makes it the central hub for observability. Provisioning dashboards as code ensures consistency across environments and enables GitOps workflows. As Grafana continues to add capabilities like explore mode, correlate metrics with logs and traces, and incident management, it solidifies its position as the primary interface for understanding system behavior.

**See also:** [GCP Networking: VPCs, Cloud NAT, Private Google Access, and Shared VPC](</en/tech/gcp-networking.html>), [Advanced TypeScript Types for Better Code](</en/tech/typescript-advanced-types.html>), [Cloud Capacity Planning: Auto-Scaling, Reserved Instances, Spot Instances, and Demand Forecasting](</en/tech/capacity-planning-cloud.html>).

**See also:** [GCP Networking: VPCs, Cloud NAT, Private Google Access, and Shared VPC](</en/tech/gcp-networking.html>), [Cloud Capacity Planning: Auto-Scaling, Reserved Instances, Spot Instances, and Demand Forecasting](</en/tech/capacity-planning-cloud.html>), [SLI/SLO/Error Budgets: Defining SLIs, Setting SLOs, and Burn Rate Alerts](</en/tech/sli-slo-error-budget.html>)

**See also:** [GCP Networking: VPCs, Cloud NAT, Private Google Access, and Shared VPC](</en/tech/gcp-networking.html>), [Cloud Capacity Planning: Auto-Scaling, Reserved Instances, Spot Instances, and Demand Forecasting](</en/tech/capacity-planning-cloud.html>), [SLI/SLO/Error Budgets: Defining SLIs, Setting SLOs, and Burn Rate Alerts](</en/tech/sli-slo-error-budget.html>)

**See also:** [GCP Networking: VPCs, Cloud NAT, Private Google Access, and Shared VPC](</en/tech/gcp-networking.html>), [Cloud Capacity Planning: Auto-Scaling, Reserved Instances, Spot Instances, and Demand Forecasting](</en/tech/capacity-planning-cloud.html>), [SLI/SLO/Error Budgets: Defining SLIs, Setting SLOs, and Burn Rate Alerts](</en/tech/sli-slo-error-budget.html>)

**See also:** [GCP Networking: VPCs, Cloud NAT, Private Google Access, and Shared VPC](</en/tech/gcp-networking.html>), [Cloud Capacity Planning: Auto-Scaling, Reserved Instances, Spot Instances, and Demand Forecasting](</en/tech/capacity-planning-cloud.html>), [SLI/SLO/Error Budgets: Defining SLIs, Setting SLOs, and Burn Rate Alerts](</en/tech/sli-slo-error-budget.html>)

**See also:** [GCP Networking: VPCs, Cloud NAT, Private Google Access, and Shared VPC](</en/tech/gcp-networking.html>), [Cloud Capacity Planning: Auto-Scaling, Reserved Instances, Spot Instances, and Demand Forecasting](</en/tech/capacity-planning-cloud.html>), [SLI/SLO/Error Budgets: Defining SLIs, Setting SLOs, and Burn Rate Alerts](</en/tech/sli-slo-error-budget.html>)

**See also:** [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Prometheus Deep Dive: Metrics, PromQL, Alerting, and High Availability](</en/tech/prometheus-deep-dive.html>)

**See also:** [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Prometheus Deep Dive: Metrics, PromQL, Alerting, and High Availability](</en/tech/prometheus-deep-dive.html>)

**See also:** [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Prometheus Deep Dive: Metrics, PromQL, Alerting, and High Availability](</en/tech/prometheus-deep-dive.html>)

**See also:** [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Prometheus Deep Dive: Metrics, PromQL, Alerting, and High Availability](</en/tech/prometheus-deep-dive.html>)

**See also:** [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Prometheus Deep Dive: Metrics, PromQL, Alerting, and High Availability](</en/tech/prometheus-deep-dive.html>)

**See also:** [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Prometheus Deep Dive: Metrics, PromQL, Alerting, and High Availability](</en/tech/prometheus-deep-dive.html>)

**See also:** [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Prometheus Deep Dive: Metrics, PromQL, Alerting, and High Availability](</en/tech/prometheus-deep-dive.html>)

**See also:** [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Prometheus Deep Dive: Metrics, PromQL, Alerting, and High Availability](</en/tech/prometheus-deep-dive.html>)

**See also:** [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Prometheus Deep Dive: Metrics, PromQL, Alerting, and High Availability](</en/tech/prometheus-deep-dive.html>)

**See also:** [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Prometheus Deep Dive: Metrics, PromQL, Alerting, and High Availability](</en/tech/prometheus-deep-dive.html>)

**See also:** [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Prometheus Deep Dive: Metrics, PromQL, Alerting, and High Availability](</en/tech/prometheus-deep-dive.html>)

**See also:** [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Prometheus Deep Dive: Metrics, PromQL, Alerting, and High Availability](</en/tech/prometheus-deep-dive.html>)

**See also:** [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Prometheus Deep Dive: Metrics, PromQL, Alerting, and High Availability](</en/tech/prometheus-deep-dive.html>)

**See also:** [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Prometheus Deep Dive: Metrics, PromQL, Alerting, and High Availability](</en/tech/prometheus-deep-dive.html>)

**See also:** [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Prometheus Deep Dive: Metrics, PromQL, Alerting, and High Availability](</en/tech/prometheus-deep-dive.html>)

**See also:** [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>), [On-Call Best Practices: Rotation, Escalation, Runbooks, and Alert Fatigue Prevention](</en/tech/on-call-best-practices.html>), [Prometheus Deep Dive: Metrics, PromQL, Alerting, and High Availability](</en/tech/prometheus-deep-dive.html>)
