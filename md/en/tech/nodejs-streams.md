---
title: "Node.js Streams"
description: "Master Node.js streams: readable, writable, transform streams, backpressure handling, and the pipeline API"
date: 2026-01-09
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/nodejs-streams.html
---

# Node.js Streams

Node.js streams are one of the most powerful yet misunderstood features of the platform. Streams enable processing of data piece by piece rather than loading entire datasets into memory. This makes them essential for handling large files, network communication, and data processing pipelines. This article covers the four stream types, backpressure, and the pipeline API.

## Stream Types

Node.js has four fundamental stream types. Readable streams produce data that can be consumed. Writable streams consume data. Transform streams read data, transform it, and write the transformed data. Duplex streams implement both readable and writable interfaces independently.

Readable streams include `fs.createReadStream` for files, HTTP request objects, and `process.stdin`. Writable streams include `fs.createWriteStream`, HTTP response objects, and `process.stdout`. Transform streams like `zlib.createGzip` and `crypto.createCipher` sit between readable and writable streams.

## Reading from Streams

Readable streams operate in two modes: flowing and paused. In flowing mode, data is read automatically and emitted via the `'data'` event. In paused mode, `read()` must be called explicitly to pull data from the stream. Modern code prefers async iteration with `for await...of`.

For example, reading a file line by line uses `readline` with a file stream: `const rl = readline.createInterface({ input: fs.createReadStream('file.txt') })`. This processes the file one line at a time without loading the entire file into memory.

## Writing to Streams

Writing to a writable stream uses the `write()` method, which returns a boolean indicating whether the internal buffer is full. A `false` return signals that the consumer cannot keep up—this is backpressure. The `'drain'` event fires when the buffer is ready for more data.

The `end()` method signals that no more data will be written. After `end()`, the stream finishes processing buffered data and emits `'finish'`. Proper stream cleanup handles errors and ensures streams are closed, especially in long-running processes.

## Transform Streams

Transform streams implement both readable and writable interfaces. They receive chunks of data, transform them, and push the transformed chunks downstream. Common use cases include compression, encryption, format conversion, and data validation.

Implementing a custom transform stream requires implementing the `_transform()` method. Each chunk arrives via `_transform`, and you push the transformed result. The `_flush()` method handles remaining data when the input stream ends. This pattern is used by `zlib`, `crypto`, and user-defined stream processors.

## Backpressure

Backpressure is the mechanism that regulates data flow between fast producers and slow consumers. When a writable stream's internal buffer exceeds `highWaterMark`, `write()` returns `false`. The readable stream should pause until `'drain'` fires, preventing memory exhaustion.

Improper backpressure handling is a common source of memory issues in Node.js applications. Without backpressure awareness, a fast readable stream can fill memory with buffered data that a slow consumer cannot process. The `pipeline()` API handles backpressure automatically.

## The Pipeline API

The `stream.pipeline()` function chains multiple streams together, handling backpressure, error propagation, and cleanup automatically. It propagates errors from any stream in the pipeline and cleans up all streams when done. A `stream.finished()` utility detects when a stream is no longer usable.

The pipeline API is the recommended way to compose streams:

const { pipeline } = require('stream/promises');

await pipeline(

fs.createReadStream('input.gz'),

zlib.createGunzip(),

fs.createWriteStream('output.txt')

);

This decompresses a gzipped file with proper backpressure and error handling—something that is surprisingly difficult to implement correctly with manual stream events.

## Error Handling

Stream errors must be handled explicitly. An unhandled `'error'` event on a stream crashes the process. The pipeline API handles errors from all chained streams, but when using streams directly, every stream needs an error handler.

Streams also emit `'close'` when the stream and its underlying resources are closed. The `'close'` event is guaranteed to fire even if an error occurred, making it suitable for cleanup logic. The `destroyed` property indicates whether the stream has been destroyed.

Node.js streams are fundamental to building efficient, memory-conscious applications. Whether processing large files, handling HTTP requests, or building data transformation pipelines, understanding streams enables scalable data processing with predictable memory usage.

**See also:** [CI/CD Best Practices](</en/tech/ci-cd-best-practices.html>), [Error Handling Patterns](</en/tech/error-handling-patterns.html>), [API Documentation](</en/tech/api-documentation.html>).

**See also:** [CI/CD Best Practices](</en/tech/ci-cd-best-practices.html>), [Error Handling Patterns](</en/tech/error-handling-patterns.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>)

**See also:** [CI/CD Best Practices](</en/tech/ci-cd-best-practices.html>), [Error Handling Patterns](</en/tech/error-handling-patterns.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>)

**See also:** [CI/CD Best Practices](</en/tech/ci-cd-best-practices.html>), [Error Handling Patterns](</en/tech/error-handling-patterns.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>)

**See also:** [CI/CD Best Practices](</en/tech/ci-cd-best-practices.html>), [Error Handling Patterns](</en/tech/error-handling-patterns.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>)

**See also:** [CI/CD Best Practices](</en/tech/ci-cd-best-practices.html>), [Error Handling Patterns](</en/tech/error-handling-patterns.html>), [ELK Stack Setup: Elasticsearch, Logstash, Kibana, and Pipeline Optimization](</en/tech/elk-stack-setup.html>)

**See also:** [Developer Portal](</en/tech/developer-portal.html>), [Event Processing](</en/tech/event-processing.html>), [Metric Collection](</en/tech/metric-collection.html>)

**See also:** [Developer Portal](</en/tech/developer-portal.html>), [Event Processing](</en/tech/event-processing.html>), [Metric Collection](</en/tech/metric-collection.html>)

**See also:** [Developer Portal](</en/tech/developer-portal.html>), [Event Processing](</en/tech/event-processing.html>), [Metric Collection](</en/tech/metric-collection.html>)

**See also:** [Developer Portal](</en/tech/developer-portal.html>), [Event Processing](</en/tech/event-processing.html>), [Metric Collection](</en/tech/metric-collection.html>)

**See also:** [Developer Portal](</en/tech/developer-portal.html>), [Event Processing](</en/tech/event-processing.html>), [Metric Collection](</en/tech/metric-collection.html>)

**See also:** [Developer Portal](</en/tech/developer-portal.html>), [Event Processing](</en/tech/event-processing.html>), [Metric Collection](</en/tech/metric-collection.html>)

**See also:** [Developer Portal](</en/tech/developer-portal.html>), [Event Processing](</en/tech/event-processing.html>), [Metric Collection](</en/tech/metric-collection.html>)

**See also:** [Developer Portal](</en/tech/developer-portal.html>), [Event Processing](</en/tech/event-processing.html>), [Metric Collection](</en/tech/metric-collection.html>)

**See also:** [Developer Portal](</en/tech/developer-portal.html>), [Event Processing](</en/tech/event-processing.html>), [Metric Collection](</en/tech/metric-collection.html>)

**See also:** [Developer Portal](</en/tech/developer-portal.html>), [Event Processing](</en/tech/event-processing.html>), [Metric Collection](</en/tech/metric-collection.html>)
