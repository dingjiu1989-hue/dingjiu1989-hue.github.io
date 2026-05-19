---
title: "Distributed Tracing with OpenTelemetry"
description: "Implement distributed tracing with OpenTelemetry covering spans, context propagation, sampling strategies, Jaeger/Zipkin visualization, and log/metric correlation."
date: 2025-12-30
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/distributed-tracing.html
---

# Distributed Tracing with OpenTelemetry

## Introduction

Distributed tracing provides end-to-end visibility into requests as they traverse multiple services. Unlike logs (which are service-local) and metrics (which are aggregate), traces capture the causal relationship between operations in a distributed system. OpenTelemetry has become the industry standard for instrumentation, offering a unified API for traces, metrics, and logs. This article covers implementing distributed tracing with OpenTelemetry in production.

## Core Concepts: Traces, Spans, and Context

A trace represents a complete request flow. Each unit of work within a trace is a span, carrying metadata about timing, status, and parent-child relationships:

import { trace, Span, SpanStatusCode } from "@opentelemetry/api";

const tracer = trace.getTracer("payment-service");

async function processPayment(orderId: string, amount: number) {

// Create a new span as the root of a sub-operation

const span = tracer.startSpan("process-payment", {

attributes: {

"payment.order_id": orderId,

"payment.amount": amount,

"payment.currency": "USD",

},

});

try {

const result = await chargePaymentGateway(orderId, amount);

span.setStatus({ code: SpanStatusCode.OK });

span.setAttribute("payment.transaction_id", result.transactionId);

return result;

} catch (error) {

span.setStatus({

code: SpanStatusCode.ERROR,

message: error.message,

});

span.recordException(error);

throw error;

} finally {

span.end();

}

}

## Context Propagation

Propagation carries trace context across service boundaries. For HTTP services, the `W3C TraceContext` format is standard:

// Instrument outgoing HTTP requests

import { context, propagation } from "@opentelemetry/api";

import * as http from "http";

function makeRequest(url: string, headers: Record) {

// Inject current context into outgoing headers

const activeContext = context.active();

const carrier: Record = {};

propagation.inject(activeContext, carrier);

const allHeaders = { ...headers, ...carrier };

return http.get(url, { headers: allHeaders });

}

For message queues, propagate context through message headers:

// Producer: inject context into message

import { propagation } from "@opentelemetry/api";

function publishMessage(topic: string, payload: any) {

const carrier: Record = {};

propagation.inject(context.active(), carrier);

const message = {

value: JSON.stringify(payload),

headers: {

...carrier,

"content-type": "application/json",

},

};

return kafkaProducer.send({ topic, messages: [message] });

}

// Consumer: extract context from message

import { propagation, context } from "@opentelemetry/api";

kafkaConsumer.on("message", (message) => {

const extractedContext = propagation.extract(

context.active(),

message.headers

);

context.with(extractedContext, async () => {

// This operation is now part of the parent trace

const span = tracer.startSpan("process-order");

// Process message...

span.end();

});

});

## Sampling Strategies

Sampling controls the volume of traces collected. Use head-based sampling for simplicity or tail-based for intelligent selection:

## OpenTelemetry Collector: tail-based sampling

processors:

tail_sampling:

decision_wait: 30s

num_traces: 10000

expected_new_traces_per_sec: 100

policies:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: error-sampling

type: status_code

config:

status_code: ERROR

sampling_percentage: 100

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: latency-sampling

type: latency

config:

threshold_ms: 500

sampling_percentage: 50

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: probabilistic

type: probabilistic

config:

sampling_percentage: 5

For head-based sampling in application code:

import { SamplingDecision } from "@opentelemetry/api";

import { Sampler, SpanKind, Attributes } from "@opentelemetry/api";

class CustomSampler implements Sampler {

shouldSample(

context: Context,

traceId: string,

spanName: string,

spanKind: SpanKind,

attributes: Attributes

) {

// Always sample error-prone operations

if (spanName.startsWith("payment.")) {

return { decision: SamplingDecision.RECORD_AND_SAMPLED };

}

// Sample 10% of health checks

if (spanName === "health-check") {

return { decision: SamplingDecision.DROP };

}

// Default probabilistic sampling

return { decision: SamplingDecision.RECORD_AND_SAMPLED };

}

}

## Visualization with Jaeger and Zipkin

Jaeger provides rich trace visualization and analysis capabilities:

## docker-compose.yml for Jaeger

services:

jaeger:

image: jaegertracing/all-in-one:latest

environment:

COLLECTOR_OTLP_ENABLED: "true"

ports:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- "16686:16686" # UI

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- "4318:4318" # OTLP HTTP

Configure the OpenTelemetry Collector to forward traces to Jaeger:

receivers:

otlp:

protocols:

http:

endpoint: "0.0.0.0:4318"

exporters:

jaeger:

endpoint: "jaeger:14250"

tls:

insecure: true

service:

pipelines:

traces:

receivers: [otlp]

exporters: [jaeger]

## Baggage Propagation

Baggage carries non-sampling key-value pairs across service boundaries for contextual information:

import { propagation } from "@opentelemetry/api";

// Set baggage in the entry service

propagation.setBaggage(context.active(),

propagation.createBaggage({

"user.id": { value: userId },

"session.region": { value: region },

"request.source": { value: source },

})

);

Access baggage in downstream services without modifying API contracts:

import { propagation, getBaggage } from "@opentelemetry/api";

function getCurrentUserId(): string | undefined {

const baggage = getBaggage(context.active());

return baggage?.getEntry("user.id")?.value;

}

## Correlation with Logs and Metrics

Link traces to logs using `trace_id` and `span_id`:

import { trace } from "@opentelemetry/api";

function enrichLogger(logger: Logger): Logger {

const span = trace.getActiveSpan();

return logger.child({

trace_id: span?.spanContext().traceId,

span_id: span?.spanContext().spanId,

trace_flags: span?.spanContext().traceFlags,

});

}

Emit metrics with trace context for full observability:

import { metrics } from "@opentelemetry/api";

const meter = metrics.getMeter("payment-service");

const requestCounter = meter.createCounter("payment.requests", {

description: "Count of payment requests",

});

function trackPayment(status: string) {

const spanContext = trace.getActiveSpan()?.spanContext();

requestCounter.add(1, {

status,

trace_id: spanContext?.traceId,

});

}

## Production Configuration

Deploy the OpenTelemetry Collector as a sidecar or DaemonSet for centralized configuration:

apiVersion: apps/v1

kind: DaemonSet

metadata:

name: otel-collector

spec:

template:

spec:

containers:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: otel-collector

image: otel/opentelemetry-collector-contrib:latest

args: ["--config=/etc/otel/config.yaml"]

ports:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- containerPort: 4318 # OTLP HTTP

Instrumentation should be additive and never break business logic. Start with critical paths (payment, auth, order creation) and expand coverage iteratively. A well-instrumented system reduces mean time to diagnosis from hours to minutes.

**See also:** [Monitoring and Alerting Setup](</en/tech/monitoring-alerting-setup.html>), [Reverse Proxy Guide](</en/tech/reverse-proxy-guide.html>), [Webpack vs Vite Comparison](</en/tech/webpack-vs-vite-bundlers.html>).

**See also:** [Chaos Engineering: Principles and Practical Tools](</en/tech/chaos-engineering.html>), [Serverless Framework: From Zero to Production](</en/tech/serverless-framework.html>), [Service Discovery in Microservices](</en/tech/service-discovery.html>)

**See also:** [Chaos Engineering: Principles and Practical Tools](</en/tech/chaos-engineering.html>), [Serverless Framework: From Zero to Production](</en/tech/serverless-framework.html>), [Service Discovery in Microservices](</en/tech/service-discovery.html>)

**See also:** [Chaos Engineering: Principles and Practical Tools](</en/tech/chaos-engineering.html>), [Serverless Framework: From Zero to Production](</en/tech/serverless-framework.html>), [Service Discovery in Microservices](</en/tech/service-discovery.html>)

**See also:** [Chaos Engineering: Principles and Practical Tools](</en/tech/chaos-engineering.html>), [Serverless Framework: From Zero to Production](</en/tech/serverless-framework.html>), [Service Discovery in Microservices](</en/tech/service-discovery.html>)

**See also:** [Chaos Engineering: Principles and Practical Tools](</en/tech/chaos-engineering.html>), [Serverless Framework: From Zero to Production](</en/tech/serverless-framework.html>), [Service Discovery in Microservices](</en/tech/service-discovery.html>)

**See also:** [Advanced GitHub Actions Workflows](</en/tech/github-actions-advanced.html>), [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>), [Cloud Cost Optimization Tips](</en/tech/cloud-cost-optimization.html>)

**See also:** [Advanced GitHub Actions Workflows](</en/tech/github-actions-advanced.html>), [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>), [Cloud Cost Optimization Tips](</en/tech/cloud-cost-optimization.html>)

**See also:** [Advanced GitHub Actions Workflows](</en/tech/github-actions-advanced.html>), [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>), [Cloud Cost Optimization Tips](</en/tech/cloud-cost-optimization.html>)
