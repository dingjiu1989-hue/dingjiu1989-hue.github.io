---
title: "WebSocket vs SSE vs Polling: Real-Time Data Patterns for Web Apps"
description: "Compare WebSocket, Server-Sent Events, long polling, and short polling for real-time features. When to use each, with code examples and scaling considerations."
date: 2026-05-08
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/websocket-vs-sse-vs-polling.html
---

# WebSocket vs SSE vs Polling: Real-Time Data Patterns for Web Apps

Real-time features — live chat, notifications, dashboards, collaborative editing — each need a different data delivery pattern. WebSocket, Server-Sent Events (SSE), and polling solve different problems. Here's when to use each, with code examples.

## Quick Comparison

| WebSocket| SSE (Server-Sent Events)| Short Polling| Long Polling  
---|---|---|---|---  
**Direction**|  Bidirectional| Server → Client only| Client → Server (request/response)| Client → Server (request/response)  
**Latency**|  Near real-time| Near real-time| Depends on interval| Low (held connection)  
**Browser support**|  All modern| All (except IE)| Universal| Universal  
**HTTP/2 friendly**|  N/A (upgrades from HTTP)| Yes| Yes| Yes  
**Reconnection**|  Manual (build it)| Built-in (automatic)| Manual| Manual  
**Complexity**|  High| Low| Lowest| Moderate  
  
## WebSocket — Bidirectional Real-Time

WebSocket is the only option when both client and server need to push messages. Use it for: chat applications, collaborative editing, multiplayer games, live auctions, trading platforms.
    
    
    // Server (using ws)
    import { WebSocketServer } from "ws";
    
    const wss = new WebSocketServer({ port: 8080 });
    
    wss.on("connection", (ws, req) => {
      const userId = authenticate(req);
    
      ws.on("message", (data) => {
        const message = JSON.parse(data.toString());
        // Broadcast to all clients in a room
        wss.clients.forEach((client) => {
          if (client.readyState === WebSocket.OPEN) {
            client.send(JSON.stringify({ user: userId, text: message.text }));
          }
        });
      });
    
      ws.on("close", () => {
        // Handle disconnect
      });
    });

## Server-Sent Events (SSE) — Simple Server Push

SSE is simpler than WebSocket when you only need server → client updates. Built-in reconnection, works over HTTP/2, and doesn't need a special protocol. Use for: live dashboards, notification feeds, progress bars, log streaming, sports scores.
    
    
    // Server (Hono)
    app.get("/events", (c) => {
      return c.streamText(async (stream) => {
        // Send events as they happen
        stream.write(`data: ${JSON.stringify({ type: "connected" })}
    
    `);
    
        const interval = setInterval(async () => {
          const updates = await getUpdates();
          stream.write(`data: ${JSON.stringify(updates)}
    
    `);
        }, 1000);
    
        // Auto-cleanup on client disconnect
        stream.onAbort(() => clearInterval(interval));
      });
    });
    
    // Client (native EventSource — zero dependencies)
    const es = new EventSource("/events");
    es.onmessage = (event) => {
      const data = JSON.parse(event.data);
      updateUI(data);
    };

## Short Polling — Simplest, Least Efficient

Client sends a request every N seconds. Simple but wasteful — most requests return empty. Only use when you can't use SSE or WebSocket (e.g., legacy infrastructure) or when data changes very infrequently.
    
    
    // Client — poll every 30 seconds
    setInterval(async () => {
      const res = await fetch("/api/updates?since=" + lastUpdate);
      if (res.ok) {
        const updates = await res.json();
        if (updates.length) updateUI(updates);
      }
    }, 30000);

## Long Polling — Polling Without the Waste

Client sends a request, server holds it open until there's new data (or a timeout). The client immediately reconnects after receiving a response. This is how most "real-time" APIs worked before WebSocket existed.

**Best for:** Legacy systems that can't upgrade to WebSocket, firewalls that block WebSocket connections, APIs where the client can't maintain persistent connections.

## Decision Matrix

Feature| Best Pattern| Why  
---|---|---  
Chat / messaging| **WebSocket**|  Bidirectional, low latency  
Live dashboard / feed| **SSE**|  Simpler than WebSocket. Built-in reconnect. HTTP/2 friendly.  
Notifications| **SSE** or **Web Push**|  SSE if browser is open. Web Push for background notifications.  
Progress bar / file upload| **SSE**|  Push progress from server. Simple to implement.  
Collaborative editing| **WebSocket** (or CRDT)| Low latency bidirectional required.  
Simple status check| **Short Polling**|  If data changes every 5+ minutes, polling is fine.  
  
**Bottom line:** Use SSE for server→client streaming — it's simpler than WebSocket, HTTP/2 friendly, and has built-in reconnection. Use WebSocket only when you need bidirectional communication. Use polling only as a last resort. Server-Sent Events is the most underrated real-time pattern. See also: [Backend Framework Comparison](</en/compare/hono-vs-express-vs-fastify.html>) and [Edge Functions Comparison](</en/compare/cloudflare-workers-vs-lambda-vs-deno-deploy.html>).

**See also:** [Testing Strategies for Web Apps: Unit, Integration, E2E, and When to Use Each](</en/tech/testing-strategies-web-apps.html>), [API Architecture Comparison 2026: REST vs GraphQL vs tRPC vs gRPC vs WebSocket vs SSE](</en/compare/api-architecture-comparison.html>), [Caching Strategies for Web Apps: CDN, Redis, Browser, and API Caching](</en/tech/caching-strategies-web-apps.html>)
