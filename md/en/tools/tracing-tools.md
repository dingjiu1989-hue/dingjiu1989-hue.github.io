---
title: "Tracing Tools: Jaeger, Zipkin, Tempo, OpenTelemetry Collector"
description: "Compare distributed tracing tools: Jaeger for end-to-end tracing, Zipkin for lineage-based tracing, Grafana Tempo for cost-effective object storage-backed trace"
date: 2026-02-07
board: tools
url: https://dingjiu1989-hue.github.io/en/tools/tracing-tools.html
---

# Tracing Tools: Jaeger, Zipkin, Tempo, OpenTelemetry Collector

## Introduction

Distributed tracing is essential for understanding request flows across microservices. When a single user request hits 10-50 services, traditional logging cannot show you the full picture. Tracing captures the causality chain: which service called which, how long each call took, and where failures occurred. This article covers Jaeger, Zipkin, Grafana Tempo, and the OpenTelemetry Collector.

## OpenTelemetry Collector

The foundation for modern observability — receives, processes, and exports telemetry data:

## otel-collector-config.yaml

receivers:

otlp:

protocols:

grpc:

endpoint: 0.0.0.0:4317

http:

endpoint: 0.0.0.0:4318

processors:

batch:

timeout: 1s

send_batch_size: 1024

memory_limiter:

check_interval: 1s

limit_mib: 512

attributes:

actions:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- key: environment

value: production

action: insert

filter:

error_mode: ignore

traces:

span:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- 'attributes["http.method"] == "OPTIONS"'

## Sampling for cost control

probabilistic_sampler:

sampling_percentage: 10 # Only send 10% of traces

exporters:

otlp:

endpoint: jaeger:4317

tls:

insecure: true

prometheus:

endpoint: 0.0.0.0:8889

debug:

verbosity: detailed

service:

pipelines:

traces:

receivers: [otlp]

processors: [memory_limiter, batch, attributes, filter, probabilistic_sampler]

exporters: [otlp, debug]

metrics:

receivers: [otlp]

processors: [batch]

exporters: [prometheus]

## Run the collector

otelcol --config otel-collector-config.yaml

## Run as Docker

docker run -v $(pwd)/otel-collector-config.yaml:/etc/otel/config.yaml otel/opentelemetry-collector-contrib

**Key features** : Vendor-agnostic data collection, tail-based sampling, attribute enrichment, batch processing, multi-destination export, service graph computation.

## Jaeger

Uber's distributed tracing system, now a CNCF graduated project:

## docker-compose.yml

services:

jaeger:

image: jaegertracing/all-in-one:latest

environment:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- COLLECTOR_OTLP_ENABLED=true

ports:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- "16686:16686" # UI

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- "4317:4317" # OTLP gRPC

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- "4318:4318" # OTLP HTTP

## Python instrumentation with OpenTelemetry

from opentelemetry import trace

from opentelemetry.sdk.trace import TracerProvider

from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from opentelemetry.instrumentation.flask import FlaskInstrumentor

from opentelemetry.instrumentation.requests import RequestsInstrumentor

## Set up tracing

provider = TracerProvider()

processor = BatchSpanProcessor(OTLPSpanExporter(

endpoint="http://jaeger:4317",

insecure=True,

))

provider.add_span_processor(processor)

trace.set_tracer_provider(provider)

## Auto-instrument libraries

FlaskInstrumentor().instrument()

RequestsInstrumentor().instrument()

## Manual instrumentation

from opentelemetry import trace

tracer = trace.get_tracer(**name**)

@app.route("/api/orders/")

def get_order(order_id):

with tracer.start_as_current_span("process_order") as span:

span.set_attribute("order.id", order_id)

span.set_attribute("order.value", 99.50)

with tracer.start_as_current_span("validate_cache") as child:

cached = cache.get(order_id)

child.set_attribute("cache.hit", cached is not None)

with tracer.start_as_current_span("query_database") as db_span:

order = db.query("SELECT * FROM orders WHERE id = ?", order_id)

db_span.set_attribute("db.rows", 1)

return order

**Key features** : Rich UI with trace search and filtering, service dependency graph, deep span detail view, comparison view for similar traces, OTLP native support.

## Tempo (Grafana Tempo)

Grafana's tracing backend with object storage for cost-effective retention:

## tempo-config.yaml

server:

http_listen_port: 3200

distributor:

receivers:

otlp:

protocols:

grpc:

endpoint: 0.0.0.0:4317

ingester:

trace_idle_period: 10s

max_block_duration: 5m

storage:

trace:

backend: s3

s3:

bucket: grafana-tempo-data

endpoint: s3.us-east-1.amazonaws.com

access_key: ${AWS_ACCESS_KEY_ID}

secret_key: ${AWS_SECRET_ACCESS_KEY}

pool:

max_workers: 100

queue_depth: 10000

compactor:

compaction:

block_retention: 336h # 14 days

querier:

search:

max_duration: 168h # 7 days of searchable data

## Run Tempo

docker run -v $(pwd)/tempo-config.yaml:/etc/tempo.yaml grafana/tempo:latest

## Query via Grafana

## Grafana datasource: Tempo

## TraceQL query:

## { resource.service.name = "payment-service" && span.http.status_code >= 500 }

**Key features** : Object storage backend (S3, GCS, Azure) for low-cost long retention, TraceQL query language, seamless Grafana integration, high scalability.

## Zipkin

Twitter's distributed tracing system (original inspiration for OpenTracing):

## docker-compose.yml

services:

zipkin:

image: openzipkin/zipkin:latest

ports:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- "9411:9411"

## Zipkin with OpenTelemetry

from opentelemetry.exporter.zipkin.json import ZipkinExporter

zipkin_exporter = ZipkinExporter(

endpoint="http://zipkin:9411/api/v2/spans",

)

provider = TracerProvider()

provider.add_span_processor(BatchSpanProcessor(zipkin_exporter))

trace.set_tracer_provider(provider)

## Comparison

| Feature | Jaeger | Zipkin | Tempo | OTel Collector |

|---------|--------|--------|-------|----------------|

| Storage | Cassandra, ES, Badger | Cassandra, ES, in-memory | S3, GCS, Azure | N/A (pass-through) |

| UI | Standalone | Standalone | Grafana | None |

| Query language | Tags/JSON | Tags | TraceQL | N/A |

| Scalability | High | Medium | Very high | High |

| Sampling | Head, tail | Head | Head | Head, tail |

| Cost at scale | Medium | Medium | Low (S3) | N/A |

## Recommendations

  * **Best all-around** : Jaeger with OTLP ingestion. Rich UI, good scalability, active community.

  * **Grafana ecosystem** : Tempo for seamless integration with Grafana dashboards and Loki logs. TraceQL is powerful.

  * **Minimal setup** : Zipkin for quick local development tracing.

  * **Data pipeline** : OpenTelemetry Collector as the central hub for receiving and routing all telemetry.




The OpenTelemetry Collector should be the first component in any tracing infrastructure. It receives traces from instrumented services, applies sampling and enrichment, and forwards to the backend of your choice (Jaeger, Tempo, or both). This decouples instrumentation from storage decisions.

**See also:** [API Testing Tools: Bruno, Hoppscotch, Postman, Insomnia in 2026](</en/tools/api-testing-2026.html>), [Cloud Cost Management Tools: Saving Money on AWS, Azure, GCP](</en/tools/cloud-cost-tools.html>), [Load Testing Tools: k6, Locust, Gatling, Artillery](</en/tools/load-testing-tools.html>).

**See also:** [API Testing Tools: Bruno, Hoppscotch, Postman, Insomnia in 2026](</en/tools/api-testing-2026.html>), [Load Testing Tools: k6, Locust, Gatling, Artillery](</en/tools/load-testing-tools.html>), [Cloud CLI Tools: aws-cli, gcloud, az, s5cmd, Cloud Comparisons](</en/tools/cloud-cli-tools.html>)

**See also:** [API Testing Tools: Bruno, Hoppscotch, Postman, Insomnia in 2026](</en/tools/api-testing-2026.html>), [Load Testing Tools: k6, Locust, Gatling, Artillery](</en/tools/load-testing-tools.html>), [Cloud CLI Tools: aws-cli, gcloud, az, s5cmd, Cloud Comparisons](</en/tools/cloud-cli-tools.html>)

**See also:** [API Testing Tools: Bruno, Hoppscotch, Postman, Insomnia in 2026](</en/tools/api-testing-2026.html>), [Load Testing Tools: k6, Locust, Gatling, Artillery](</en/tools/load-testing-tools.html>), [Cloud CLI Tools: aws-cli, gcloud, az, s5cmd, Cloud Comparisons](</en/tools/cloud-cli-tools.html>)

**See also:** [API Testing Tools: Bruno, Hoppscotch, Postman, Insomnia in 2026](</en/tools/api-testing-2026.html>), [Load Testing Tools: k6, Locust, Gatling, Artillery](</en/tools/load-testing-tools.html>), [Cloud CLI Tools: aws-cli, gcloud, az, s5cmd, Cloud Comparisons](</en/tools/cloud-cli-tools.html>)

**See also:** [API Testing Tools: Bruno, Hoppscotch, Postman, Insomnia in 2026](</en/tools/api-testing-2026.html>), [Load Testing Tools: k6, Locust, Gatling, Artillery](</en/tools/load-testing-tools.html>), [Cloud CLI Tools: aws-cli, gcloud, az, s5cmd, Cloud Comparisons](</en/tools/cloud-cli-tools.html>)

**See also:** [Kafka Tools: AKHQ, Kafka UI, Kowl, Offset Explorer](</en/tools/kafka-tools.html>), [Mocking Tools: MSW, nock, sinon, WireMock — Service Virtualization](</en/tools/mock-tools.html>), [Monorepo Tools: Turborepo, Nx, Bazel, Lage Comparison](</en/tools/monorepo-tools.html>)

**See also:** [Kafka Tools: AKHQ, Kafka UI, Kowl, Offset Explorer](</en/tools/kafka-tools.html>), [Mocking Tools: MSW, nock, sinon, WireMock — Service Virtualization](</en/tools/mock-tools.html>), [Monorepo Tools: Turborepo, Nx, Bazel, Lage Comparison](</en/tools/monorepo-tools.html>)

**See also:** [Kafka Tools: AKHQ, Kafka UI, Kowl, Offset Explorer](</en/tools/kafka-tools.html>), [Mocking Tools: MSW, nock, sinon, WireMock — Service Virtualization](</en/tools/mock-tools.html>), [Monorepo Tools: Turborepo, Nx, Bazel, Lage Comparison](</en/tools/monorepo-tools.html>)

**See also:** [Kafka Tools: AKHQ, Kafka UI, Kowl, Offset Explorer](</en/tools/kafka-tools.html>), [Mocking Tools: MSW, nock, sinon, WireMock — Service Virtualization](</en/tools/mock-tools.html>), [Monorepo Tools: Turborepo, Nx, Bazel, Lage Comparison](</en/tools/monorepo-tools.html>)

**See also:** [Kafka Tools: AKHQ, Kafka UI, Kowl, Offset Explorer](</en/tools/kafka-tools.html>), [Mocking Tools: MSW, nock, sinon, WireMock — Service Virtualization](</en/tools/mock-tools.html>), [Monorepo Tools: Turborepo, Nx, Bazel, Lage Comparison](</en/tools/monorepo-tools.html>)

**See also:** [Kafka Tools: AKHQ, Kafka UI, Kowl, Offset Explorer](</en/tools/kafka-tools.html>), [Mocking Tools: MSW, nock, sinon, WireMock — Service Virtualization](</en/tools/mock-tools.html>), [Monorepo Tools: Turborepo, Nx, Bazel, Lage Comparison](</en/tools/monorepo-tools.html>)

**See also:** [Kafka Tools: AKHQ, Kafka UI, Kowl, Offset Explorer](</en/tools/kafka-tools.html>), [Mocking Tools: MSW, nock, sinon, WireMock — Service Virtualization](</en/tools/mock-tools.html>), [Monorepo Tools: Turborepo, Nx, Bazel, Lage Comparison](</en/tools/monorepo-tools.html>)

**See also:** [Kafka Tools: AKHQ, Kafka UI, Kowl, Offset Explorer](</en/tools/kafka-tools.html>), [Mocking Tools: MSW, nock, sinon, WireMock — Service Virtualization](</en/tools/mock-tools.html>), [Monorepo Tools: Turborepo, Nx, Bazel, Lage Comparison](</en/tools/monorepo-tools.html>)

**See also:** [Kafka Tools: AKHQ, Kafka UI, Kowl, Offset Explorer](</en/tools/kafka-tools.html>), [Mocking Tools: MSW, nock, sinon, WireMock — Service Virtualization](</en/tools/mock-tools.html>), [Monorepo Tools: Turborepo, Nx, Bazel, Lage Comparison](</en/tools/monorepo-tools.html>)

**See also:** [Kafka Tools: AKHQ, Kafka UI, Kowl, Offset Explorer](</en/tools/kafka-tools.html>), [Mocking Tools: MSW, nock, sinon, WireMock — Service Virtualization](</en/tools/mock-tools.html>), [Monorepo Tools: Turborepo, Nx, Bazel, Lage Comparison](</en/tools/monorepo-tools.html>)

**See also:** [Kafka Tools: AKHQ, Kafka UI, Kowl, Offset Explorer](</en/tools/kafka-tools.html>), [Mocking Tools: MSW, nock, sinon, WireMock — Service Virtualization](</en/tools/mock-tools.html>), [Monorepo Tools: Turborepo, Nx, Bazel, Lage Comparison](</en/tools/monorepo-tools.html>)
