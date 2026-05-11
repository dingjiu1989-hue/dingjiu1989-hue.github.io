---
title: "Serverless Architecture Patterns"
description: "Explore serverless architecture patterns for building scalable, cost-effective applications."
date: 2026-05-11
board: architecture
url: https://dingjiu1989-hue.github.io/en/architecture/serverless-architecture.html
---

Serverless architecture allows you to build and run applications without managing servers. Cloud providers handle infrastructure provisioning, scaling, and maintenance automatically. This article covers the core patterns, best practices, and trade-offs of serverless architecture.

## What Serverless Really Means

Serverless does not mean there are no servers. It means you do not think about servers. The cloud provider manages capacity, patching, and availability. You focus on writing code.

The key characteristics:

- **No server management**: You do not provision, scale, or maintain servers.
- **Autoscaling**: Resources scale automatically with demand, from zero to thousands of concurrent executions.
- **Pay-per-execution**: You pay only for the compute time you use, often measured in milliseconds.
- **Stateless**: Functions are ephemeral and stateless. Persistent state must be stored externally.

## The Function as a Service Pattern

FaaS is the core building block. Each function handles a single concern:

```javascript
// AWS Lambda handler for image resizing
exports.handler = async (event) => {
    const { key, bucket } = JSON.parse(event.body);
    const image = await s3.getObject({ Bucket: bucket, Key: key });
    const resized = await sharp(image.Body).resize(200, 200).toBuffer();
    await s3.putObject({
        Bucket: bucket,
        Key: `thumbnails/${key}`,
        Body: resized
    });
    return { statusCode: 200, body: JSON.stringify({ success: true }) };
};
```

Functions should be small, focused, and stateless. Each function does one thing and does it well.

## Event-Driven Pattern

Serverless functions are typically triggered by events from other services:

```
[S3 Upload] -> [Lambda: Process File] -> [DynamoDB: Update Metadata] -> [SNS: Notify User]
            -> [Lambda: Generate Thumbnail]
```

Common event sources:
- **S3 events**: File uploads trigger processing pipelines.
- **DynamoDB Streams**: Database changes trigger downstream updates.
- **SQS/SNS**: Messages trigger background processing.
- **API Gateway**: HTTP requests trigger request handlers.
- **CloudWatch Events**: Scheduled tasks trigger periodic jobs.

This pattern creates loosely coupled, resilient pipelines. If one step fails, the event can be retried or sent to a dead-letter queue.

## API Gateway + Lambda Pattern

The most common serverless web application pattern. API Gateway handles HTTP requests and triggers Lambda functions:

```
[Client] -> [API Gateway] -> [Lambda] -> [DynamoDB]
```

API Gateway provides:
- HTTP endpoint management
- Request validation
- Authentication and authorization
- Rate limiting
- CORS handling
- Response caching

Lambda handles business logic. DynamoDB, RDS Proxy, or Aurora Serverless provides data persistence.

This pattern works well for REST APIs, GraphQL endpoints, and webhook handlers. The combination scales automatically from zero to thousands of requests per second.

## Fan-Out Pattern

A single event triggers multiple parallel operations:

```
[Event] -> [SNS Topic]
                  |
        +---------+---------+
        |         |         |
    [Lambda A] [Lambda B] [Lambda C]
```

Use SNS, SQS, or EventBridge to broadcast events to multiple subscribers. Each subscriber processes independently. Failures in one subscriber do not affect others.

This pattern is ideal for scenarios like:
- New user registration triggers email verification, welcome email, analytics tracking, and CRM updates.
- New order triggers inventory update, payment processing, shipping label generation, and notification.

## Step Functions for Orchestration

For complex workflows, use AWS Step Functions to coordinate multiple Lambda functions:

```
[Start Order] -> [Validate] -> [Process Payment] -> [Reserve Inventory]
                                                       |
                                                    [Failed]
                                                       |
                                               [Refund Payment] -> [Notify User]
```

Step Functions provide:
- State machine definition in JSON or YAML.
- Built-in retry, error handling, and timeout.
- Visual monitoring of workflow execution.
- Long-running workflow support (up to one year).

Use Step Functions whenever your workflow has conditional logic, parallel branches, or human-in-the-loop steps. It is far easier to manage than orchestrating Lambda functions from code.

## Warm Starts vs. Cold Starts

Lambda functions experience cold starts when a new container is spun up. Cold starts add latency (100ms to several seconds depending on runtime).

**Strategies to reduce cold starts:**
- Use provisioned concurrency to keep a specified number of instances warm.
- Use a lighter runtime (Node.js vs. Java or .NET).
- Minimize deployment package size.
- Keep dependencies to a minimum.

**When cold starts matter:**
- User-facing APIs that need sub-100ms response times.
- Real-time applications.

**When cold starts do not matter:**
- Background job processing.
- Scheduled tasks.
- Queue consumers.

## Best Practices

**Statelessness.** Do not store state in the function container. Use DynamoDB, S3, or ElastiCache for state.

**Small functions.** Each function should do one thing. A function doing multiple things is harder to test, deploy, and scale independently.

**Proper error handling.** Use dead-letter queues for failed events. Implement idempotent processing to handle duplicate invocations.

**Security.** Follow the principle of least privilege for IAM roles. Encrypt environment variables. Validate all inputs.

**Monitoring.** Use structured logging with correlation IDs. Set up CloudWatch alarms for error rates and duration. Use distributed tracing with X-Ray.

## When Not to Use Serverless

Serverless is not ideal for:
- Long-running processes (Lambda max execution is 15 minutes).
- High-throughput, latency-sensitive workloads.
- Stateful applications with persistent connections.
- Monolithic applications that are hard to split into functions.
- Workloads with predictable, steady-state traffic (provisioned instances may be cheaper).

## Summary

Serverless architecture enables building scalable applications with minimal operational overhead. Use event-driven patterns for loosely coupled pipelines. Use Step Functions for complex orchestration. Be aware of cold starts and design your application accordingly. Serverless is a powerful tool, but it is not the right choice for every workload. Evaluate your requirements against the trade-offs before committing.
