---
title: "Messaging Patterns: Pub/Sub and Request/Reply"
description: "Explore messaging patterns including publish-subscribe and request-reply for distributed systems."
date: 2025-12-29
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/messaging-patterns.html
---

# Messaging Patterns: Pub/Sub and Request/Reply

Messaging is the backbone of distributed systems. It enables services to communicate asynchronously, decouple dependencies, and build resilient architectures. This article covers the two most fundamental messaging patterns: publish-subscribe and request-reply. 

The Case for Messaging 

Direct HTTP calls between services create tight coupling. When Service A calls Service B directly: 

  * Service A must know Service B's location and API contract.

  * Service A is blocked while Service B processes the request.

  * If Service B is down, Service A fails.

  * Scaling Service B does not help Service A's performance.




Messaging intermediaries (message brokers like Kafka, RabbitMQ, SQS, or Pub/Sub) solve these problems by decoupling senders from receivers. 

Publish-Subscribe (Pub/Sub) 

In the pub/sub pattern, publishers send messages to a topic without knowing who the subscribers are. Subscribers receive messages from topics they have subscribed to. 

[Publisher] -> [Topic] -> [Subscriber A]

-> [Subscriber B]

-> [Subscriber C]

How Pub/Sub Works 

  * **Topics** are named channels that hold messages.



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Publishers** send messages to a topic. 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Subscribers** register interest in a topic and receive all messages published to it. 4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Each subscriber receives a copy of every message (fan-out delivery). 

Use Cases 

**Event notification.** When a user signs up, publish a `UserRegistered` event. Multiple subscribers react: the email service sends a welcome email, the analytics service records the event, the CRM service creates a contact. 

**Broadcasting.** A live sports app publishes score updates. Thousands of clients receive updates in real-time. 

**Log aggregation.** Multiple services publish log entries to a central topic. A log processing service stores and indexes them. 

Example with Kafka 

## Publisher

producer.send('order-events', {

'type': 'OrderPlaced',

'order_id': '123',

'customer_id': '456',

'total': 99.99

})

## Subscriber

@kafka_listener('order-events')

def handle_order_placed(event):

if event['type'] == 'OrderPlaced':

inventory_service.reserve_inventory(event['order_id'])

notification_service.send_confirmation(event['customer_id'])

Pub/Sub is ideal for one-to-many communication where the publisher does not need a response. 

Request-Reply 

The request-reply pattern is fundamentally different from pub/sub. A sender sends a request and expects a response. The two are correlated so the sender knows which response goes with which request. 

In messaging systems, request-reply requires correlation: 

[Requestor] -> [Request Queue] -> [Replier]

[Requestor] <\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- [Reply Queue] <\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- [Replier]

Correlation ID 

The key mechanism is the correlation ID. The requestor includes a unique ID in the request message. The replier includes the same ID in the reply message. The requestor uses this ID to match replies to pending requests. 

## Requestor

correlation_id = str(uuid.uuid4())

reply_queue = f"reply-{correlation_id}"

message = {

'correlation_id': correlation_id,

'payload': {'user_id': '123', 'amount': 100}

}

request_queue.send(message)

## Wait for reply on the reply queue

reply = reply_queue.receive(timeout=30)

## Replier

def handle_request(message):

result = process(message['payload'])

reply = {

'correlation_id': message['correlation_id'],

'payload': result

}

reply_queue.send(reply)

Use Cases 

**Remote procedure calls.** Service A asks Service B to compute something and return the result. Unlike HTTP RPC, the messaging-based approach allows the requestor to be decoupled in time -- it can send the request and check for the reply later. 

**Long-running operations.** Submit a job, get back a job ID, check progress, and eventually receive the result. The reply might arrive minutes or hours later. 

Pub/Sub vs. Request-Reply 

| Aspect | Pub/Sub | Request-Reply | |--------|---------|---------------| | Communication | One-to-many | One-to-one | | Response expected? | No | Yes | | Coupling | Very loose | Moderate | | Use case | Event notification, broadcasting | Remote procedure, query | | Message ordering | Per partition/topic | Per conversation | | Error handling | Dead letter queue | Timeout + retry | 

Choosing a Message Broker 

**Apache Kafka:** Best for high-throughput event streaming, log aggregation, and event sourcing. Messages are persisted and replayable. Excellent for building event-driven architectures. 

**RabbitMQ:** Best for traditional messaging with complex routing (direct, topic, headers, fanout exchanges). Good for request-reply patterns. Lower throughput than Kafka but richer routing features. 

**Amazon SQS/SNS:** Fully managed. SQS for request-reply, SNS for pub/sub. No infrastructure to manage. Good for AWS-native applications. 

**Google Cloud Pub/Sub:** Fully managed, global. Good for Google Cloud-native applications. 

Advanced Patterns 

**Dead letter queues.** When a message cannot be processed (after retries), move it to a dead letter queue for manual inspection. Prevents poison messages from blocking the main queue. 

**Message bridging.** Forward messages between different messaging systems. For example, consume from SQS and publish to Kafka for long-term storage. 

**Publisher confirms.** In Pub/Sub, some brokers support acknowledgments from publishers to confirm the message was received. Use this for at-least-once delivery guarantees. 

Common Pitfalls 

**Message ordering.** Distributed messaging systems rarely guarantee total order. Kafka guarantees order within a partition, not across partitions. Design your system to handle out-of-order messages. 

**Idempotency.** Messages may be delivered more than once. Ensure your message handlers are idempotent. Use idempotency keys or deduplication. 

**Monitoring.** Monitor queue depth, consumer lag, and processing time. Set up alerts for growing backlog. 

Summary 

Pub/Sub and Request-Reply serve different purposes. Use Pub/Sub when you need to notify multiple consumers of an event. Use Request-Reply when a service needs a response. Many systems use both patterns together. Choose your message broker based on throughput requirements, routing complexity, and operational preferences. Always design for idempotency and handle duplicate messages gracefully.

**See also:** [Pub-Sub Patterns: Event-Driven Communication](</en/architecture/pub-sub-patterns.html>), [Request-Reply Pattern for Asynchronous Communication](</en/architecture/request-reply-pattern.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>).

**See also:** [Pub-Sub Patterns: Event-Driven Communication](</en/architecture/pub-sub-patterns.html>), [Caching Strategies and Patterns in Distributed Systems](</en/architecture/caching-strategies.html>), [Event-Driven Architecture: Patterns and Practice](</en/architecture/event-driven-architecture.html>)

**See also:** [Pub-Sub Patterns: Event-Driven Communication](</en/architecture/pub-sub-patterns.html>), [Caching Strategies and Patterns in Distributed Systems](</en/architecture/caching-strategies.html>), [Event-Driven Architecture: Patterns and Practice](</en/architecture/event-driven-architecture.html>)

**See also:** [Pub-Sub Patterns: Event-Driven Communication](</en/architecture/pub-sub-patterns.html>), [Bulkhead Pattern for Resilience](</en/architecture/bulkhead-pattern.html>), [Rate Limiting Patterns](</en/architecture/rate-limiting-patterns.html>)

**See also:** [Pub-Sub Patterns: Event-Driven Communication](</en/architecture/pub-sub-patterns.html>), [Bulkhead Pattern for Resilience](</en/architecture/bulkhead-pattern.html>), [Rate Limiting Patterns](</en/architecture/rate-limiting-patterns.html>)

**See also:** [Pub-Sub Patterns: Event-Driven Communication](</en/architecture/pub-sub-patterns.html>), [Bulkhead Pattern for Resilience](</en/architecture/bulkhead-pattern.html>), [Rate Limiting Patterns](</en/architecture/rate-limiting-patterns.html>)

**See also:** [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>)

**See also:** [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>)

**See also:** [Asynchronous Communication in Distributed Systems](</en/architecture/asynchronous-communication.html>), [Consensus Algorithms: Paxos, Raft, Zab](</en/architecture/consensus-algorithms.html>), [Idempotency Patterns in Distributed Systems](</en/architecture/idempotency-patterns.html>)
