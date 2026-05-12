---
title: "LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution"
description: "Implement LLM observability for production AI applications: distributed tracing, token usage tracking, latency monitoring, and cost attribution."
date: 2026-05-12
board: ai
url: https://dingjiu1989-hue.github.io/en/ai/llm-observability.html
---

# LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution

Production LLM applications fail in ways traditional monitoring does not capture. You need observability that tracks prompts, responses, tokens, latency, and costs across every model call. Here is the LLM observability framework.

##  Why LLM Observability Is Different

Traditional application monitoring tracks request volume, error rates, and response times. LLM applications need all of that plus token counts, model versions, prompt templates, and generation parameters.

LLM failures are subtle. The API returns 200 OK, but the response is hallucinated, truncated, or refused. Your uptime monitor shows green while users get useless answers. Only detailed observability catches these failures.

LLM costs are non-trivial. A single GPT-4 call can cost cents, but thousands of calls per day add up to real money. Without token tracking, you cannot attribute costs to users, features, or prompt templates.

##  Tracing LLM Calls

Distributed tracing for LLM applications should capture the full lifecycle of each request: the user input, the system prompt, any retrieved context, the model parameters, the response, and post-processing.

Each trace should include a unique request ID that correlates the user session, the specific model call, and downstream processing. This lets you debug end-to-end problems where a bad embedding lookup causes a poor generation.

Instrument your LLM calls with OpenTelemetry. Add spans for each stage: retrieval, prompt assembly, model inference, response parsing, and guardrail checks. This gives you granular latency data for each component.

Use an observability platform that supports LLM-specific data. LangSmith, Weights and Biases, and Arize AI offer LLM observability features. Open-source alternatives include Langfuse and Helicone.

##  Token Tracking

Token usage is the currency of LLM applications. Track input tokens, output tokens, and total tokens for every call. This is the basis for cost calculation and capacity planning.

Log token usage per model, per user, and per feature. This tells you which features are driving costs and which users are consuming the most. An expensive feature with low engagement might need optimization or removal.

Track token usage trends over time. If token consumption per request is increasing, your prompts may be growing without corresponding quality improvement. Periodic prompt optimization reduces costs significantly.

Monitor token limits. If your output frequently gets truncated because it exceeds max_tokens, your use case needs either longer context or shorter responses. Both are actionable signals.

##  Latency Monitoring

LLM latency varies wildly. Same model, same prompt, same token count can take 500 milliseconds or 5 seconds depending on server load and request queuing.

Measure end-to-end latency per request and break it down into components: network latency, queue time, inference time, and post-processing time. Inference time is the largest component and the hardest to optimize.

Set latency budgets per feature. A chatbot needs responses in under 2 seconds. A batch summarization job can tolerate 30 seconds. Alert when features exceed their latency budgets.

Monitor percentile latency, not averages. P50 might be 1 second while P95 is 8 seconds, which means one in twenty users has a terrible experience. Optimize for P95 and P99.

##  Cost Attribution

Cost attribution answers the question: where is the money going? Tag every LLM call with metadata: feature name, user ID, model name, and prompt template version. This lets you slice costs by any dimension.

Report costs per feature monthly. If your code generation feature costs $500 per month and your chat feature costs $5,000 per month, you can make informed decisions about optimization priorities.

Set cost alerts per feature. If a feature suddenly doubles in cost, something changed. It might be a prompt change, a user going rogue, or a traffic spike. Alerting prevents bill shock.

Track cost per user session. A user that generates $2 in LLM costs per session needs to generate at least that much in revenue or value. Unprofitable user segments might need different pricing or feature limits.

##  Alerting and Incident Response

Define alert thresholds for the metrics that matter. Response time exceeds 5 seconds for P95. Error rate exceeds 2%. Cost per day exceeds a threshold. Tokens per request exceed expected range.

When an alert fires, the trace data should let you identify the problematic request, reproduce it, and understand what went wrong. Without traces, you know something is broken but cannot diagnose it.

Build runbooks for common LLM failures. Model down: failover to a fallback model. High latency: reduce max_tokens or switch to a smaller model. Cost spike: identify the source and apply rate limits.

LLM observability is not optional for production applications. Start with basic token and latency tracking, add tracing for critical paths, and expand gradually. The cost of observability is a fraction of the cost of undetected LLM failures.
