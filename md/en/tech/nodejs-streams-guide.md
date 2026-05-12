---
title: "Node.js Streams: Complete Guide to Efficient Data Processing"
description: "Master Node.js streams: Readable, Writable, Transform, and Duplex. Real-world examples for file processing, HTTP streaming, CSV parsing, and backpressure handling. Avoid memory issues at scale."
date: 2026-05-08
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/nodejs-streams-guide.html
---

# Node.js Streams: Complete Guide to Efficient Data Processing

Node.js Streams are one of the most powerful and underused features of the platform. They enable processing large amounts of data without loading everything into memory — critical for file uploads, data pipelines, and HTTP responses. Yet most Node.js developers avoid streams because the API (even the modern pipeline-based one) has non-obvious patterns. This guide covers streams from the ground up with practical examples you can use today.

## The Four Stream Types

Type| What It Does| Examples| Key Events/Methods  
---|---|---|---  
Readable| Produces data that can be consumed| fs.createReadStream, HTTP request (req), process.stdin| data, end, error, pipe(), readable.read()  
Writable| Consumes data that is written to it| fs.createWriteStream, HTTP response (res), process.stdout| write(), end(), drain, finish  
Transform| Both reads and writes — modifies data in transit| zlib.createGzip, crypto.createCipher, CSV parser| Same as Readable + Writable, _transform() method  
Duplex| Independent read and write sides (like a telephone)| net.Socket, TLS socket, WebSocket| read() + write(), data flowing in both directions  

## Pipeline API (Modern, Recommended)

**Best for:** Any time you connect streams together. pipeline() handles cleanup and error propagation automatically — raw .pipe() does not.

    const { pipeline } = require('node:stream/promises');
    const { createReadStream, createWriteStream } = require('node:fs');
    const { createGzip } = require('node:zlib');

    await pipeline(
      createReadStream('input.json'),
      createGzip(),
      createWriteStream('input.json.gz'),
    );
    console.log('Pipeline succeeded — file compressed');

## Real-World Use Cases

### 1\. Streaming CSV Processing (Avoid OOM on Large Files)

    const { createReadStream } = require('node:fs');
    const { parse } = require('csv-parse');
    const { Transform } = require('node:stream');

    // Process a 5GB CSV file with constant memory (~50MB)
    const results = [];
    createReadStream('massive-file.csv')
      .pipe(parse({ columns: true }))
      .pipe(new Transform({
        objectMode: true,
        transform(row, encoding, callback) {
          // Process and optionally filter each row
          if (row.status === 'active') {
            this.push({ id: row.id, name: row.name });
          }
          callback();
        }
      }))
      .on('data', (row) => results.push(row))
      .on('end', () => console.log(`Processed ${results.length} rows`));

### 2\. HTTP Streaming Large Responses

    // Instead of: res.json(allData) — loads all data into memory
    // Use: stream data to client as you produce it
    app.get('/api/export', async (req, res) => {
      res.setHeader('Content-Type', 'application/json');
      res.write('[');
      let first = true;
      const cursor = db.collection('events').find().stream();
      for await (const doc of cursor) {
        if (!first) res.write(',');
        res.write(JSON.stringify(doc));
        first = false;
      }
      res.write(']');
      res.end();
    });

### 3\. Handling Backpressure

**Best practice:** Respect the return value of write(). When write() returns false, the writable stream's internal buffer is full — pause reading until the drain event fires.

    const readStream = createReadStream('huge-file.bin');
    const writeStream = createWriteStream('copy.bin');

    readStream.on('data', (chunk) => {
      const canContinue = writeStream.write(chunk);
      if (!canContinue) {
        readStream.pause(); // Stop reading — buffer is full
        writeStream.once('drain', () => readStream.resume()); // Resume when drained
      }
    });
    // Note: pipeline() handles this automatically — prefer it over manual piping

**Bottom line:** Streams are essential for processing data that exceeds memory limits. The pipeline() API should be your default — it handles backpressure, error propagation, and cleanup correctly. Avoid raw .pipe() and .on('data') patterns unless you have a specific reason. See also: [Caching Strategies](</en/tech/caching-strategies-web-apps.html>) and [REST API Best Practices](</en/tech/rest-api-best-practices.html>).
