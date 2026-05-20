---
title: "AI Testing Frameworks: DeepEval, Ragas, LangSmith, CI Integration"
description: "Comprehensive guide to AI testing frameworks including DeepEval, Ragas, and LangSmith. Implement automated evaluation in CI pipelines for LLM applications."
date: 2026-02-14
board: ai
url: https://dingjiu1989-hue.github.io/en/ai/ai-testing-frameworks.html
---

# AI Testing Frameworks: DeepEval, Ragas, LangSmith, CI Integration

## Introduction

Testing AI applications is fundamentally different from testing traditional software. LLM outputs are non-deterministic, there is no single correct answer, and failures manifest as subtle quality degradations rather than crashes. Dedicated AI testing frameworks address these challenges with automated evaluation metrics, test case generation, and regression detection.

## DeepEval

DeepEval is an open-source testing framework designed for LLM applications:

from deepeval import assert_test

from deepeval.metrics import (

HallucinationMetric,

AnswerRelevancyMetric,

ContextualPrecisionMetric,

FaithfulnessMetric,

BiasMetric,

ToxicityMetric,

)

from deepeval.test_case import LLMTestCase

def test_rag_response_no_hallucination():

test_case = LLMTestCase(

input="What is the capital of France?",

actual_output="The capital of France is Paris, located in the Ile-de-France region.",

retrieval_context=["Paris is the capital and most populous city of France."],

)

hallucination_metric = HallucinationMetric(threshold=0.3)

assert_test(test_case, [hallucination_metric])

def test_response_relevancy():

test_case = LLMTestCase(

input="Explain Kubernetes pods",

actual_output="Kubernetes is a container orchestration platform...",

retrieval_context=[

"A pod is the smallest deployable unit in Kubernetes.",

"Pods can contain one or more containers.",

],

)

relevancy_metric = AnswerRelevancyMetric(threshold=0.7)

assert_test(test_case, [relevancy_metric])

## Run tests: deepeval test run test_ai.py

DeepEval supports 15+ evaluation metrics including hallucination detection, answer relevancy, faithfulness, contextual precision, bias detection, and toxicity scoring. Each metric returns a score (0-1) that can be compared against a configurable threshold.

## Ragas

Ragas is specialized for evaluating RAG pipelines end-to-end:

from ragas import evaluate

from ragas.metrics import (

faithfulness,

answer_relevancy,

context_precision,

context_recall,

)

from datasets import Dataset

## Prepare evaluation dataset

test_data = Dataset.from_dict({

"question": [

"What is a Kubernetes pod?",

"How does load balancing work?",

],

"answer": [

"A pod is the smallest deployable unit...",

"Load balancing distributes traffic...",

],

"contexts": [

["Pods can contain one or more containers."],

["Load balancers distribute incoming traffic."],

],

"ground_truth": [

"A pod is the smallest deployable unit in Kubernetes.",

"Load balancing distributes network traffic across servers.",

],

})

## Compute RAG metrics

result = evaluate(

test_data,

metrics=[

faithfulness,

answer_relevancy,

context_precision,

context_recall,

],

)

print(result)

## {

## "faithfulness": 0.92,

## "answer_relevancy": 0.88,

## "context_precision": 0.95,

## "context_recall": 0.85

## }

Ragas decomposes RAG quality into four independent metrics: faithfulness (is the answer grounded in context?), answer relevancy (does the answer address the question?), context precision (are retrieved documents relevant?), and context recall (are all relevant documents retrieved?).

## LangSmith

LangSmith provides a hosted evaluation platform with tracing and annotation:

from langsmith import Client, evaluate

from langsmith.schemas import Example, Run

client = Client()

## Define a custom evaluator

def answer_correctness(run: Run, example: Example) -> dict:

## Compare model output against expected output

predicted = run.outputs.get("output", "")

expected = example.outputs.get("answer", "")

## Use LLM-as-judge for evaluation

from langsmith.evaluation import evaluate as langsmith_eval

return {"score": compute_similarity(predicted, expected)}

## Run evaluation on a dataset

results = evaluate(

lambda inputs: my_llm_chain(inputs["question"]),

data="my-test-dataset",

evaluators=[answer_correctness],

experiment_prefix="rag-v2-eval",

)

## View results in LangSmith dashboard

print(results)

LangSmith excels at trace-level evaluation. Every LLM call, retrieval step, and prompt template is recorded and can be compared across experiments.

## CI Integration

Integrate AI tests into your CI pipeline to catch regressions automatically:

## .github/workflows/ai-tests.yml

name: AI Evaluation Tests

on:

push:

branches: [main]

pull_request:

jobs:

evaluate:

runs-on: ubuntu-latest

steps:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- uses: actions/checkout@v4

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- uses: actions/setup-python@v5

with:

python-version: "3.11"

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: Install dependencies

run: pip install deepeval ragas langsmith

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: Run AI evaluation tests

env:

OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}

LANGCHAIN_API_KEY: ${{ secrets.LANGCHAIN_API_KEY }}

run: |

deepeval test run tests/ai_evaluation.py

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: Check quality gate

run: |

deepeval metrics --min-threshold 0.7

Set a quality gate that blocks merges when metrics fall below thresholds. This prevents gradual quality degradation that is invisible in traditional tests.

## Conclusion

AI testing requires specialized frameworks that understand non-deterministic outputs. Use DeepEval for unit-test-style evaluation with configurable metrics. Use Ragas for end-to-end RAG pipeline evaluation. Use LangSmith for trace-level debugging and comparison across experiments. Integrate all three into CI pipelines with automated quality gates to maintain production AI quality over time.

**See also:** [LLM Version Management: Model Registry, A/B Testing, Rollback](</en/ai/llm-version-management.html>), [Model Evaluation: Benchmarks, Human Evaluation, LLM-as-Judge, and A/B Testing in Production](</en/ai/model-evaluation-harness.html>), [RAG Evaluation: Retrieval Metrics, Generation Quality, End-to-End Testing, and Datasets](</en/ai/rag-evaluation.html>).

**See also:** [LLM Safety: RLHF, Constitutional AI, Content Filtering, Red Teaming](</en/ai/llm-safety.html>), [LLM Version Management: Model Registry, A/B Testing, Rollback](</en/ai/llm-version-management.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>)

**See also:** [LLM Safety: RLHF, Constitutional AI, Content Filtering, Red Teaming](</en/ai/llm-safety.html>), [LLM Version Management: Model Registry, A/B Testing, Rollback](</en/ai/llm-version-management.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>)

**See also:** [LLM Safety: RLHF, Constitutional AI, Content Filtering, Red Teaming](</en/ai/llm-safety.html>), [LLM Version Management: Model Registry, A/B Testing, Rollback](</en/ai/llm-version-management.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>)

**See also:** [LLM Safety: RLHF, Constitutional AI, Content Filtering, Red Teaming](</en/ai/llm-safety.html>), [LLM Version Management: Model Registry, A/B Testing, Rollback](</en/ai/llm-version-management.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>)

**See also:** [LLM Safety: RLHF, Constitutional AI, Content Filtering, Red Teaming](</en/ai/llm-safety.html>), [LLM Version Management: Model Registry, A/B Testing, Rollback](</en/ai/llm-version-management.html>), [LLM Observability: Tracing, Token Tracking, Latency Monitoring, and Cost Attribution](</en/ai/llm-observability.html>)

**See also:** [AI Red Teaming: Adversarial Testing, Jailbreak Attempts, Safety Evaluation, and Automated Testing](</en/ai/ai-red-teaming.html>), [AI Monitoring and Alerting: Latency, Token Usage, Error Rates, Drift Detection](</en/ai/ai-monitoring-alerting.html>), [Fine-Tuning vs RAG: When to Use Each, Hybrid Approaches, Cost Comparison](</en/ai/fine-tuning-vs-rag.html>)

**See also:** [AI Red Teaming: Adversarial Testing, Jailbreak Attempts, Safety Evaluation, and Automated Testing](</en/ai/ai-red-teaming.html>), [AI Monitoring and Alerting: Latency, Token Usage, Error Rates, Drift Detection](</en/ai/ai-monitoring-alerting.html>), [Fine-Tuning vs RAG: When to Use Each, Hybrid Approaches, Cost Comparison](</en/ai/fine-tuning-vs-rag.html>)

**See also:** [AI Red Teaming: Adversarial Testing, Jailbreak Attempts, Safety Evaluation, and Automated Testing](</en/ai/ai-red-teaming.html>), [AI Monitoring and Alerting: Latency, Token Usage, Error Rates, Drift Detection](</en/ai/ai-monitoring-alerting.html>), [Fine-Tuning vs RAG: When to Use Each, Hybrid Approaches, Cost Comparison](</en/ai/fine-tuning-vs-rag.html>)

**See also:** [AI Red Teaming: Adversarial Testing, Jailbreak Attempts, Safety Evaluation, and Automated Testing](</en/ai/ai-red-teaming.html>), [AI Monitoring and Alerting: Latency, Token Usage, Error Rates, Drift Detection](</en/ai/ai-monitoring-alerting.html>), [Fine-Tuning vs RAG: When to Use Each, Hybrid Approaches, Cost Comparison](</en/ai/fine-tuning-vs-rag.html>)

**See also:** [AI Red Teaming: Adversarial Testing, Jailbreak Attempts, Safety Evaluation, and Automated Testing](</en/ai/ai-red-teaming.html>), [AI Monitoring and Alerting: Latency, Token Usage, Error Rates, Drift Detection](</en/ai/ai-monitoring-alerting.html>), [Fine-Tuning vs RAG: When to Use Each, Hybrid Approaches, Cost Comparison](</en/ai/fine-tuning-vs-rag.html>)

**See also:** [AI Red Teaming: Adversarial Testing, Jailbreak Attempts, Safety Evaluation, and Automated Testing](</en/ai/ai-red-teaming.html>), [AI Monitoring and Alerting: Latency, Token Usage, Error Rates, Drift Detection](</en/ai/ai-monitoring-alerting.html>), [Fine-Tuning vs RAG: When to Use Each, Hybrid Approaches, Cost Comparison](</en/ai/fine-tuning-vs-rag.html>)

**See also:** [AI Red Teaming: Adversarial Testing, Jailbreak Attempts, Safety Evaluation, and Automated Testing](</en/ai/ai-red-teaming.html>), [AI Monitoring and Alerting: Latency, Token Usage, Error Rates, Drift Detection](</en/ai/ai-monitoring-alerting.html>), [Fine-Tuning vs RAG: When to Use Each, Hybrid Approaches, Cost Comparison](</en/ai/fine-tuning-vs-rag.html>)

**See also:** [AI Red Teaming: Adversarial Testing, Jailbreak Attempts, Safety Evaluation, and Automated Testing](</en/ai/ai-red-teaming.html>), [AI Monitoring and Alerting: Latency, Token Usage, Error Rates, Drift Detection](</en/ai/ai-monitoring-alerting.html>), [Fine-Tuning vs RAG: When to Use Each, Hybrid Approaches, Cost Comparison](</en/ai/fine-tuning-vs-rag.html>)

**See also:** [AI Red Teaming: Adversarial Testing, Jailbreak Attempts, Safety Evaluation, and Automated Testing](</en/ai/ai-red-teaming.html>), [AI Monitoring and Alerting: Latency, Token Usage, Error Rates, Drift Detection](</en/ai/ai-monitoring-alerting.html>), [Fine-Tuning vs RAG: When to Use Each, Hybrid Approaches, Cost Comparison](</en/ai/fine-tuning-vs-rag.html>)

**See also:** [AI Red Teaming: Adversarial Testing, Jailbreak Attempts, Safety Evaluation, and Automated Testing](</en/ai/ai-red-teaming.html>), [AI Monitoring and Alerting: Latency, Token Usage, Error Rates, Drift Detection](</en/ai/ai-monitoring-alerting.html>), [Fine-Tuning vs RAG: When to Use Each, Hybrid Approaches, Cost Comparison](</en/ai/fine-tuning-vs-rag.html>)
