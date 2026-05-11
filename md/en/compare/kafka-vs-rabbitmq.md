---
title: "Kafka vs RabbitMQ vs Apache Pulsar"
description: "Compare Kafka, RabbitMQ, and Apache Pulsar across throughput, latency, message model, persistence, routing, ecosystem, and migration scenarios."
date: 2026-05-12
board: compare
url: https://dingjiu1989-hue.github.io/en/compare/kafka-vs-rabbitmq.html
---

## Introduction

Message brokers are the nervous system of distributed architectures, enabling asynchronous communication between services at scale. Apache Kafka, RabbitMQ, and Apache Pulsar represent three distinct approaches to message processing. Choosing the wrong broker leads to architecture that fights against the tool's strengths. This article provides a technical comparison to guide your decision.

## Architecture and Message Model

### Apache Kafka

Kafka uses a distributed commit log model with partitioned topics:

```yaml
# Kafka topic configuration
topic_config:
  name: orders
  partitions: 12
  replication_factor: 3
  configs:
    cleanup.policy: delete
    retention.ms: 604800000  # 7 days
    retention.bytes: 1073741824  # 1 GB
    compression.type: snappy
    min.insync.replicas: 2
    max.message.bytes: 1048576  # 1 MB

# Producer configuration (Go)
producer_config:
  acks: all           # Wait for all replicas
  retries: 3
  batch.size: 16384   # 16KB
  linger.ms: 5        # Wait up to 5ms to batch
  compression: snappy
  enable.idempotence: true  # Exactly-once semantics
```

Kafka consumers track their position via offsets, enabling replay:

```python
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'orders',
    bootstrap_servers=['kafka-1:9092', 'kafka-2:9092'],
    group_id='order-processor',
    enable_auto_commit=False,  # Manual offset management
    auto_offset_reset='earliest',  # Start from beginning if no offset
    max_poll_records=500,
    session_timeout_ms=30000,
)

for message in consumer:
    process_order(message.value)
    # Commit offset after successful processing
    consumer.commit()
```

### RabbitMQ

RabbitMQ uses a message broker model with exchanges and queues:

```python
import pika

# Connection
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='rabbitmq-1',
        port=5672,
        credentials=pika.PlainCredentials('user', 'pass'),
        heartbeat=600,
        blocked_connection_timeout=300,
    )
)
channel = connection.channel()

# Declare exchange and queue
channel.exchange_declare(
    exchange='orders',
    exchange_type='topic',
    durable=True,
)

channel.queue_declare(
    queue='order-processing',
    durable=True,
    arguments={
        'x-queue-type': 'quorum',  # Highly available queue
        'x-message-ttl': 86400000,  # 24 hours
        'x-dead-letter-exchange': 'orders-dlx',
    }
)

# Bind queue to exchange with routing key
channel.queue_bind(
    exchange='orders',
    queue='order-processing',
    routing_key='order.created.*',
)

# Publish message with delivery mode 2 for persistence
channel.basic_publish(
    exchange='orders',
    routing_key='order.created.europe',
    body=json.dumps(order_data),
    properties=pika.BasicProperties(
        delivery_mode=2,  # Persistent
        content_type='application/json',
        priority=5,
    ),
)
```

### Apache Pulsar

Pulsar separates compute and storage with a two-layer architecture:

```python
import pulsar

# Pulsar client
client = pulsar.Client(
    'pulsar://pulsar-broker:6650',
    authentication=pulsar.AuthenticationToken('token'),
)

# Producer with schema
producer = client.create_producer(
    'persistent://public/default/orders',
    schema=pulsar.schema.JsonSchema(Order),
    send_timeout_millis=30000,
    batching_enabled=True,
    batching_max_publish_delay_ms=10,
    compression_type=pulsar.CompressionType.LZ4,
)

# Consumer with subscription type
consumer = client.subscribe(
    'persistent://public/default/orders',
    subscription_name='order-processor',
    subscription_type=pulsar.SubscriptionType.Shared,  # Load balanced
    initial_position=pulsar.InitialPosition.Earliest,
)

# Negative acknowledgement for retry
while True:
    msg = consumer.receive()
    try:
        order = msg.value()
        process_order(order)
        consumer.acknowledge(msg)
    except Exception:
        consumer.negative_acknowledge(msg)  # Requeue for retry
```

## Performance Comparison

| Metric | Kafka | RabbitMQ | Pulsar |
|---|---|---|---|
| Max throughput (single partition) | ~100 MB/s | ~10 MB/s | ~100 MB/s |
| End-to-end latency (p99) | 5-50ms | <1ms | 5-20ms |
| Max message size | 1MB (default, configurable) | 128MB | 5MB |
| Partition scaling | Add partitions (no rebalancing in v3+) | Cluster of nodes | Segmented (no rebalancing) |
| Storage efficiency | High (zero-copy) | Medium | Very high (tiered storage) |

## Message Persistence and Durability

| Feature | Kafka | RabbitMQ | Pulsar |
|---|---|---|---|
| Default persistence | Disk (all messages) | Memory (configurable) | Disk (all messages) |
| Replication | Partition-based | Queue mirroring / Quorum | BookKeeper (segments) |
| Data retention | Time/Size based | Queue TTL + DLQ | Time/Size + tiered storage |
| Exactly-once | Yes (idempotent producer) | No (at-least-once by default) | Yes (deduplication) |
| Message replay | Yes (offset reset) | No (consumed messages deleted) | Yes (cursor reset) |

## Routing and Message Patterns

### Kafka: Topic-based routing

```python
# Kafka routing via topic naming convention
TOPIC_ORDER_CREATED = "orders.events.created"
TOPIC_ORDER_CANCELLED = "orders.events.cancelled"
TOPIC_ORDER_SHIPPED = "orders.events.shipped"
```

### RabbitMQ: Flexible exchange types

```python
# Direct exchange: route by exact routing key
channel.exchange_declare('direct-orders', 'direct')
channel.queue_bind('europe-queue', 'direct-orders', 'order.europe')
channel.queue_bind('asia-queue', 'direct-orders', 'order.asia')

# Topic exchange: pattern matching
channel.exchange_declare('topic-orders', 'topic')
channel.queue_bind('all-orders', 'topic-orders', 'order.#')
channel.queue_bind('europe-only', 'topic-orders', 'order.europe.*')

# Fanout exchange: broadcast
channel.exchange_declare('broadcast', 'fanout')
channel.queue_bind('audit-log', 'broadcast', '')
channel.queue_bind('metrics', 'broadcast', '')
```

### Pulsar: Flexible subscriptions

```python
# Exclusive: only one consumer
consumer = client.subscribe('orders', 'exclusive-sub',
    subscription_type=pulsar.SubscriptionType.Exclusive)

# Shared: round-robin across consumers
consumer = client.subscribe('orders', 'shared-sub',
    subscription_type=pulsar.SubscriptionType.Shared)

# Failover: primary + standby consumers
consumer = client.subscribe('orders', 'failover-sub',
    subscription_type=pulsar.SubscriptionType.Failover)

# Key_Shared: ordered delivery per key
consumer = client.subscribe('orders', 'key-shared-sub',
    subscription_type=pulsar.SubscriptionType.Key_Shared)
```

## Ecosystem and Operations

| Factor | Kafka | RabbitMQ | Pulsar |
|---|---|---|---|
| Client libraries | Java, Python, Go, .NET, C/C++ | 30+ languages | 10+ languages |
| Monitoring | JMX, Prometheus exporter | Management plugin, Prometheus | Prometheus, Grafana |
| Schema registry | Confluent Schema Registry | Custom | Built-in Schema Registry |
| Tiered storage | Confluent Tiered Storage | No | Built-in (S3, GCS) |
| Multi-tenancy | Topic naming convention | Virtual hosts | Built-in (namespaces, tenants) |

## Migration Scenarios

```python
# Dual-write migration pattern
class DualWriteBroker:
    def __init__(self, source_broker, target_broker):
        self.source = source_broker
        self.target = target_broker

    async def publish(self, topic: str, message: dict):
        # Write to both brokers during migration
        results = await asyncio.gather(
            self.source.publish(topic, message),
            self.target.publish(topic, message),
            return_exceptions=True,
        )
        # Check source first, then target
        if results[0]:
            raise results[0]
        if results[1]:
            print(f"Warning: target broker failed: {results[1]}")

    async def switch_to_target(self):
        """Once all consumers migrated, stop source writes."""
        self.source = NullBroker()  # No-op

    async def backfill(self, source_topic: str, target_topic: str):
        """Backfill historical data to new broker."""
        for message in self.source.consume_from_beginning(source_topic):
            await self.target.publish(target_topic, message)
```

## Decision Guide

- **Choose Kafka** for high-throughput event streaming, log aggregation, data pipelines, and systems that need message replay and exactly-once semantics.
- **Choose RabbitMQ** for low-latency message delivery, complex routing patterns, RPC-style messaging, and systems where sub-millisecond latency matters.
- **Choose Pulsar** for multi-tenant environments, geo-replication across regions, systems needing both queuing and streaming, and deployments that benefit from tiered storage.

Kafka remains the default choice for most event-driven architectures, but RabbitMQ excels where complex routing and low latency are paramount, and Pulsar is the strongest contender for large-scale multi-tenant deployments.
