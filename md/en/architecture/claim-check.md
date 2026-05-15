---
title: "Claim Check Pattern"
description: "Learn the claim check pattern: store large payloads, pass references, and enable asynchronous processing"
date: 2026-05-12
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/claim-check.html
---

# Claim Check Pattern

# Claim Check Pattern

# Claim Check Pattern

# Claim Check Pattern

# Claim Check Pattern

# Claim Check Pattern

# Claim Check Pattern

# Claim Check Pattern

# Claim Check Pattern

# Claim Check Pattern

# Claim Check Pattern

# Claim Check Pattern

The claim check pattern is a messaging pattern that addresses the challenge of passing large payloads through a message broker. Instead of including the payload in the message, the producer stores the payload in a shared data store and sends a reference (claim check) in the message. The consumer retrieves the payload using the reference. This pattern is essential for systems where message size limits are a concern. 

The Problem with Large Messages 

Message brokers impose size limits. Kafka has a default max message size of 1MB, though this can be increased. SQS has a 256KB limit. RabbitMQ can handle larger messages but performance degrades significantly. Even where limits can be increased, large messages cause problems: increased broker storage, slower serialization and deserialization, increased network transfer time, and memory pressure on consumers. 

A single high-resolution image, a large CSV file, or a JSON document with many nested objects can easily exceed these limits. The claim check pattern solves this problem without requiring changes to the message broker configuration. 

How It Works 

The claim check pattern has three steps. First, the producer stores the large payload in a shared data store—an object store like S3, a key-value store like Redis, or a database. The store returns a reference to the stored payload, typically a URL or a unique key. 

Second, the producer sends a message containing only the reference (the claim check) plus metadata. The message is small, fast to serialize, and well within broker size limits. Third, the consumer receives the message, extracts the reference, retrieves the payload from the shared store, and processes it. 

The consumer should clean up the stored data after processing, either through explicit deletion or a retention policy on the data store. 

Implementation Considerations 

The shared data store must be accessible by both the producer and consumer. In distributed systems, this often means a network-accessible store like S3, GCS, or Azure Blob Storage. The store should have a retention policy to clean up unclaimed payloads—messages may fail and never be consumed. 

The reference should be opaque and contain enough information to locate the payload: the storage system, bucket or container, object key, and optionally a version or checksum. URLs are common but should not expose internal storage paths if the store is not publicly accessible. 

Security is important. The stored payload may contain sensitive data. Access controls on the shared store should restrict access to authorized producers and consumers. Encryption at rest and in transit should be standard. The claim check itself is not encrypted in the message, so the reference should not contain sensitive information. 

Async Processing Integration 

The claim check pattern integrates naturally with asynchronous processing workflows. When a message arrives at the consumer, it retrieves the payload and starts processing. If processing fails, the consumer can re-queue the message or store the failed payload reference for later analysis. 

For long-running processing, the consumer can store intermediate state in the shared store and include updated references in subsequent messages. This creates a workflow where each processing step passes references to payload data. 

Alternatives 

Alternatives to the claim check pattern include increasing broker message limits, splitting large payloads into smaller chunks, and using a dedicated large-message channel. Each has trade-offs. Increasing limits works for moderate increases but degrades broker performance. 

Splitting payloads introduces complexity around reassembly and ordering. Dedicated large-message channels require separate infrastructure and routing logic. The claim check pattern is generally the cleanest solution because it separates concerns: the message broker handles state changes, and the data store handles payload storage. 

Best Practices 

Use the claim check pattern when payloads regularly exceed 80% of the broker's message size limit. Store payloads with a TTL or retention period to prevent orphaned data. Include a checksum in the reference to validate payload integrity. Log claim check retrieval failures separately from general message processing failures. Monitor the size of stored payloads and the number of unclaimed references to detect processing issues. 

The claim check pattern is a simple, effective solution for handling large payloads in message-based systems. It preserves the benefits of asynchronous messaging while avoiding the performance and reliability problems of large messages.

**See also:** [Request-Reply Pattern for Asynchronous Communication](</en/architecture/request-reply-pattern.html>), [Event-Carried State Transfer Pattern](</en/architecture/event-carried-state-transfer.html>), [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>).

**See also:** [Scheduler Supervisor Pattern](</en/architecture/scheduler-supervisor.html>), [Scatter-Gather Pattern for Parallel Processing](</en/architecture/scatter-gather.html>), [Domain Events: Design and Implementation](</en/architecture/domain-events.html>)
