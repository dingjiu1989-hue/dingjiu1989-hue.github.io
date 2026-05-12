---
title: "Logging Tools: ELK Stack vs Loki vs Splunk"
description: "Compare ELK Stack, Grafana Loki, and Splunk for log aggregation, structured logging, indexing strategies, retention policies, query capabilities, and cost."
date: 2026-05-12
board: tools
url: https://dingjiu1989-hue.github.io/en/tools/logging-tools.html
---

# Logging Tools: ELK Stack vs Loki vs Splunk

##  Introduction

Centralized logging transforms noisy application output into a searchable, actionable resource. The three leading approaches--ELK Stack (Elasticsearch, Logstash, Kibana), Grafana Loki, and Splunk--take fundamentally different approaches to log ingestion, indexing, and querying. Choosing the right one affects both your daily operations and your monthly infrastructure bill.

##  Architecture Comparison

### ELK Stack

Elasticsearch indexes every field in every log line, enabling rich full-text search at the cost of higher storage consumption:

    # Filebeat configuration for shipping logs

    filebeat.inputs:

      - type: container

        paths:

          - /var/lib/docker/containers/*/*.log

        json.message_key: log

        json.overwrite_keys: true

        json.add_error_key: true

    processors:

      - add_docker_metadata:

          host: "unix:///var/run/docker.sock"

      - dissect:

          tokenizer: "%{timestamp} %{level} %{logger} %{message}"

          target_prefix: "parsed"

    output.elasticsearch:

      hosts: ["elasticsearch:9200"]

      index: "filebeat-%{[agent.version]}-%{+yyyy.MM.dd}"

      pipeline: "parse-logs"

    # Elasticsearch index lifecycle policy

    PUT _ilm/policy/logs-30day

    {

      "policy": {

        "phases": {

          "hot": {

            "min_age": "0ms",

            "actions": {

              "rollover": { "max_size": "50GB", "max_age": "1d" },

              "set_priority": { "priority": 100 }

            }

          },

          "warm": {

            "min_age": "3d",

            "actions": {

              "shrink": { "number_of_shards": 1 },

              "forcemerge": { "max_num_segments": 1 }

            }

          },

          "delete": {

            "min_age": "30d",

            "actions": { "delete": {} }

          }

        }

      }

    }

### Grafana Loki

Loki indexes only metadata labels, leaving log content unindexed for dramatically lower storage costs:

    # Loki configuration

    auth_enabled: false

    server:

      http_listen_port: 3100

    common:

      replication_factor: 1

      ring:

        kvstore:

          store: inmemory

    schema_config:

      configs:

        - from: 2024-01-01

          store: tsdb

          object_store: s3

          schema: v13

          index:

            prefix: index_

            period: 24h

    storage_config:

      tsdb_shipper:

        active_index_directory: /loki/tsdb-shipper-active

        cache_location: /loki/tsdb-shipper-cache

        shared_store: s3

      aws:

        s3: s3://us-east-1/logs-bucket

        s3forcepathstyle: false

    limits_config:

      retention_period: 30d

      max_query_series: 10000

      ingestion_rate_mb: 10

      ingestion_burst_size_mb: 20

    compactor:

      working_directory: /loki/compactor

      shared_store: s3

      retention_enabled: true

### Splunk

Splunk uses a proprietary indexer architecture with heavy indexing at ingest:

    # inputs.conf - Splunk forwarder configuration

    [monitor:///var/log/app/*.log]

    disabled = false

    index = production

    sourcetype = applog

    crcSalt = <SOURCE>

    # props.conf - Field extraction

    [applog]

    SHOULD_LINEMERGE = true

    LINE_BREAKER = ([\r\n]+)

    TRUNCATE = 20000

    KV_MODE = json

    REPORT-appfields = app-timestamp-extract, app-level-extract

    # transforms.conf

    [app-timestamp-extract]

    REGEX = (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})

    FORMAT = date::$1

    [app-level-extract]

    REGEX = "level":"(\w+)"

    FORMAT = level::$1

##  Structured Logging

No matter which platform you choose, structured logging at the application level is essential:

    package main

    import (

        "go.uber.org/zap"

    )

    func main() {

        logger, _ := zap.NewProduction(

            zap.WithCaller(true),

            zap.AddStacktrace(zap.ErrorLevel),

        )

        defer logger.Sync()

        orderID := "ord-12345"

        amount := 99.50

        // Structured log with context

        logger.Info("processing payment",

            zap.String("order_id", orderID),

            zap.Float64("amount", amount),

            zap.String("currency", "USD"),

            zap.String("payment_method", "credit_card"),

            zap.Duration("processing_time", 250*time.Millisecond),

        )

    }

The same structured log renders differently across platforms:

    {

      "level": "info",

      "ts": "2026-05-12T10:30:00Z",

      "caller": "payment.go:42",

      "msg": "processing payment",

      "order_id": "ord-12345",

      "amount": 99.50,

      "currency": "USD",

      "payment_method": "credit_card",

      "processing_time": "250ms"

    }

##  Query Capabilities

### ELK (Kibana Query Language)

    service:payment AND level:ERROR

    AND NOT message:"timeout retry"

    AND @timestamp >= "now-1h"

### Loki (LogQL)

    {service="payment", level="error"}

    |= "charge_failed"

    | json

    | duration > 5s

    | unwrap latency_ms [5m]

    | rate per second

### Splunk (SPL)

    index=production sourcetype=applog

    service=payment level=ERROR

    | rex field=message "order_id=(?<order_id>\S+)"

    | stats count by order_id

    | sort - count

    | head 10

##  Indexing Strategies

| Strategy | ELK | Loki | Splunk |

|---|---|---|---|

| Index approach | Inverted index on all fields | Label-only index | Proprietary inverted index |

| Storage ratio | 1:1.5 (raw to indexed) | 1:0.3 (minimal overhead) | 1:2+ (heavily optimized) |

| Cardinality limits | 20k fields/document | Label value cardinality | 10k source types |

| Full-text search | Excellent | Limited (filter + grep) | Excellent |

##  Retention Policies

    # Loki: retention via compactor

    compactor:

      retention_enabled: true

      retention_rules:

        - type: series

          selector:

            match: '{service="payment"}'

          priority: 10

          period: 90d  # Payment logs retained longer

        - selector:

            match: '{env="staging"}'

          priority: 1

          period: 7d   # Staging logs retained shorter

##  Cost Comparison

| Factor | ELK (self-hosted) | ELK (Elastic Cloud) | Loki + S3 | Splunk |

|---|---|---|---|---|

| Storage cost | $0.10/GB/month (SSD) | $0.30/GB/month | $0.023/GB/month (S3) | $2/GB/month (ingested) |

| Compute | 3-5 nodes minimum | $500+/month base | 2 nodes minimum | $2,000+/GB/day |

| Free tier | No | 500MB/month | Community (unlimited) | 500MB/day |

Loki offers the lowest storage cost by far due to its S3-based object storage and label-only indexing. ELK provides the best query flexibility at moderate cost. Splunk delivers enterprise-grade reliability but at a premium that only makes sense for compliance-heavy industries.

##  Decision Matrix

* **ELK Stack**: Best for teams needing full-text search across all fields, complex aggregations, and existing Elasticsearch expertise.
* **Grafana Loki**: Best for cost-conscious teams already using Grafana, who can tolerate grep-style log searching.
* **Splunk**: Best for enterprises requiring compliance auditing, RBAC, and have budget for premium support.

For most engineering teams, Loki paired with Grafana offers the best balance of cost and capability. Move to ELK when you need indexed structured search on arbitrary fields. Reserve Splunk for regulated environments where audit trails and access controls justify the expense.
