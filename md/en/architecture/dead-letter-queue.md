---
title: "Dead Letter Queues: Handling Message Failures"
description: "Understanding dead letter queues: how to handle failed messages in event-driven architectures and message brokers."
date: 2026-05-07
board: architecture
url: https://aidev.fit/en/architecture/dead-letter-queue.html
---

# Dead Letter Queues: Handling Message Failures

A dead letter queue (DLQ) is a message queue that stores messages that a system cannot successfully process. When a consumer repeatedly fails to process a message, the message broker moves it to the DLQ instead of discarding it. This prevents message loss while isolating problematic messages from the main processing pipeline.

## How DLQ Works

Most message brokers support a configurable retry policy. A message is delivered to a consumer. If processing fails, the consumer rejects or nacks the message. The broker redelivers the message up to the maximum retry count. After exhausting retries, the broker moves the message to the DLQ.

The DLQ stores the original message along with metadata such as the failure reason, retry count, and timestamps. Operators can inspect DLQ messages, fix the underlying issue, and replay messages back to the main queue.

## Message Brokers and DLQ

AWS SQS has built-in DLQ support with redrive functionality. You can configure a source queue to send failed messages to a DLQ after a specified number of receive attempts. AWS provides a "redrive" mechanism to move messages back to the source queue after the issue is resolved.

RabbitMQ implements DLQ through dead letter exchanges. When a message is rejected or expires, the broker routes it to the configured dead letter exchange, which forwards it to the DLQ. This flexible approach supports complex routing scenarios.

Apache Kafka uses a different model—consumers write failed messages to a separate "dead letter topic." Kafka's log-based architecture makes this approach natural and efficient.

## Processing Failed Messages

Set up monitoring alerts on DLQ depth. A growing DLQ indicates persistent processing failures. Build a DLQ processing dashboard showing failure reasons, age, and source queue. Implement automated replay for retryable failures after a cooldown period.

Manual inspection and replay tools should be available for operational teams. Some DLQ messages require code fixes before replay. Archive messages that represent invalid data or permanent failures.
