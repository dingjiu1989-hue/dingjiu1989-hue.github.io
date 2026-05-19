---
title: "Mocking Tools: MSW, nock, sinon, WireMock — Service Virtualization"
description: "Compare mocking and service virtualization tools: MSW for API mocking in the browser, nock for Node.js HTTP interception, sinon for function stubs, and WireMock"
date: 2026-02-04
board: tools
url: https://dingjiu1989-hue.github.io/en/tools/mock-tools.html
---

# Mocking Tools: MSW, nock, sinon, WireMock — Service Virtualization

## Mocking Tools: MSW, nock, sinon, WireMock — Service Virtualization

### Mocking Tools: MSW, nock, sinon, WireMock — Service Virtualization

#### Mocking Tools: MSW, nock, sinon, WireMock — Service Virtualization

#### Mocking Tools: MSW, nock, sinon, WireMock — Service Virtualization

#### Mocking Tools: MSW, nock, sinon, WireMock — Service Virtualization

#### Mocking Tools: MSW, nock, sinon, WireMock — Service Virtualization

#### Mocking Tools: MSW, nock, sinon, WireMock — Service Virtualization

#### Mocking Tools: MSW, nock, sinon, WireMock — Service Virtualization

#### Mocking Tools: MSW, nock, sinon, WireMock — Service Virtualization

#### Mocking Tools: MSW, nock, sinon, WireMock — Service Virtualization

#### Mocking Tools: MSW, nock, sinon, WireMock — Service Virtualization

#### Mocking Tools: MSW, nock, sinon, WireMock — Service Virtualization

#### Mocking Tools: MSW, nock, sinon, WireMock — Service Virtualization

#### Mocking Tools: MSW, nock, sinon, WireMock — Service Virtualization

#### Mocking Tools: MSW, nock, sinon, WireMock — Service Virtualization

#### Mocking Tools: MSW, nock, sinon, WireMock — Service Virtualization

#### Introduction

Mocking is essential for isolated testing. The right mocking strategy depends on what you are testing: frontend components that make HTTP calls, backend services with external dependencies, or complex interactions between multiple services. This article covers four complementary mocking approaches.

#### MSW (Mock Service Worker)

MSW intercepts network requests at the service worker level, working in both browser and Node.js:

// mocks/handlers.ts

import { http, HttpResponse } from "msw";

export const handlers = [

// REST API handler

http.get("https://api.example.com/users", ({ request }) => {

const url = new URL(request.url);

const page = url.searchParams.get("page") || "1";

return HttpResponse.json({

users: [

{ id: 1, name: "Alice" },

{ id: 2, name: "Bob" },

],

total: 50,

page: Number(page),

});

}),

// POST handler with request validation

http.post("https://api.example.com/users", async ({ request }) => {

const body = await request.json();

if (!body.name) {

return HttpResponse.json(

{ error: "Name is required" },

{ status: 400 }

);

}

return HttpResponse.json(

{ id: 3, name: body.name },

{ status: 201 }

);

}),

// GraphQL handler

http.post("https://api.example.com/graphql", async ({ request }) => {

const { query } = await request.json();

if (query.includes("currentUser")) {

return HttpResponse.json({

data: { currentUser: { id: 1, name: "Alice", role: "admin" } },

});

}

}),

];

// test setup

import { setupServer } from "msw/node";

import { handlers } from "./handlers";

const server = setupServer(...handlers);

beforeAll(() => server.listen());

afterEach(() => server.resetHandlers());

afterAll(() => server.close());

// Override handler for specific test

test("handles network error", async () => {

server.use(

http.get("https://api.example.com/users", () => {

return HttpResponse.error();

})

);

// Test error handling logic

});

**Strengths** : Works at the network level (not module level), browser and Node.js support, realistic interception, first-class GraphQL support.

#### nock

nock intercepts HTTP requests at the Node.js `http` module level:

const nock = require("nock");

// Mock a GET request

nock("https://api.example.com")

.get("/users")

.query({ page: 1, limit: 10 })

.reply(200, {

users: [{ id: 1, name: "Alice" }],

total: 1,

});

// Mock with dynamic response

nock("https://api.example.com")

.post("/users", (body) => body.name && body.email)

.reply(201, (uri, requestBody) => {

const body = JSON.parse(requestBody);

return { id: Date.now(), ...body, createdAt: new Date().toISOString() };

});

// Mock multiple times with different responses

nock("https://api.example.com")

.get("/status")

.times(3)

.reply(200, { status: "ok" });

// Persist mock for repeated calls

nock("https://api.example.com")

.get("/health")

.times(Infinity)

.reply(200, { healthy: true });

// Scope assertion

const scope = nock("https://api.example.com")

.get("/users")

.reply(200, []);

// After test, verify all mocked endpoints were called

expect(scope.isDone()).toBe(true);

nock.cleanAll();

**Strengths** : Fine-grained request matching, supports regex URL matching, response templating, scope isolation.

**Weaknesses** : Node.js only, module-level interception (not browser), can be slow with many mocks.

#### Sinon

Sinon provides standalone test doubles (spies, stubs, mocks):

const sinon = require("sinon");

// Spy: observe function calls

const spy = sinon.spy();

spy("hello", "world");

console.log(spy.calledOnce); // true

console.log(spy.args[0]); // ["hello", "world"]

// Stub: replace function behavior

const stub = sinon.stub();

stub.returns(42);

stub.withArgs("special").returns(100);

console.log(stub("anything")); // 42

console.log(stub("special")); // 100

// Stub an object method

const api = { fetch: async (url) => ({ data: [] }) };

const fetchStub = sinon.stub(api, "fetch");

fetchStub.resolves({ data: [{ id: 1 }] });

fetchStub.rejects(new Error("Network error"));

// Restore original after test

fetchStub.restore();

// Timers: control time-dependent code

const clock = sinon.useFakeTimers();

let callback = sinon.spy();

setTimeout(callback, 1000);

clock.tick(1000);

expect(callback.calledOnce).toBe(true);

clock.restore();

**Strengths** : Rich assertion API, fake timers, standalone (framework-agnostic), excellent for module-level mocking.

#### WireMock

WireMock runs as a standalone HTTP server, perfect for integration tests:

// Java example (WireMock also has HTTP API)

import static com.github.tomakehurst.wiremock.client.WireMock.*;

// Start WireMock server

WireMockServer wireMockServer = new WireMockServer(8089);

wireMockServer.start();

// Stub a GET endpoint

stubFor(get(urlEqualTo("/api/users/1"))

.willReturn(aResponse()

.withStatus(200)

.withHeader("Content-Type", "application/json")

.withBody("{ \"id\": 1, \"name\": \"Alice\" }")));

// Stub with response templating

stubFor(post(urlEqualTo("/api/users"))

.willReturn(aResponse()

.withStatus(201)

.withBody("{{request.body}}")

.withTransformers("response-template")));

// Verify request was made

verify(getRequestedFor(urlPathEqualTo("/api/users/1"))

.withHeader("Authorization", containing("Bearer")));

#### Start WireMock standalone

java -jar wiremock-standalone.jar --port 8089 --verbose

#### Configure via JSON files in mappings/ directory

#### __files/response.json contains the response body

#### Comparison

| Feature | MSW | nock | Sinon | WireMock |

|---------|-----|------|-------|----------|

| Level | Network (SW) | Network (http) | Function | HTTP server |

| Browser | Yes | No | Yes | No |

| Node.js | Yes | Yes | Yes | Yes |

| Real HTTP | Yes | No (hijacked) | No | Yes |

| Setup complexity | Medium | Low | Low | Medium |

| Best for | Frontend tests | Backend tests | Unit tests | Integration tests |

#### Recommendations

  * **Frontend API mocking** : MSW is the best choice — it works in both test and development environments.

  * **Backend HTTP mocking** : nock for simple cases, WireMock for complex integration tests.

  * **Function-level mocking** : Sinon for spying, stubbing, and fake timers.

  * **Integration/E2E tests** : WireMock as a standalone HTTP server for contract testing.




Use MSW + Sinon as your core mocking stack. Add nock or WireMock when testing service-to-service HTTP interactions at the integration level.

**See also:** [API Testing Tools: Bruno, Hoppscotch, Postman, Insomnia in 2026](</en/tools/api-testing-2026.html>), [Load Testing Tools: k6, Locust, Gatling, Artillery](</en/tools/load-testing-tools.html>), [Documentation Tools for Developers 2026](</en/tools/documentation-tools.html>).

**See also:** [API Testing Tools: Bruno, Hoppscotch, Postman, Insomnia in 2026](</en/tools/api-testing-2026.html>), [Load Testing Tools: k6, Locust, Gatling, Artillery](</en/tools/load-testing-tools.html>), [Cloud CLI Tools: aws-cli, gcloud, az, s5cmd, Cloud Comparisons](</en/tools/cloud-cli-tools.html>)

**See also:** [API Testing Tools: Bruno, Hoppscotch, Postman, Insomnia in 2026](</en/tools/api-testing-2026.html>), [Load Testing Tools: k6, Locust, Gatling, Artillery](</en/tools/load-testing-tools.html>), [Cloud CLI Tools: aws-cli, gcloud, az, s5cmd, Cloud Comparisons](</en/tools/cloud-cli-tools.html>)

**See also:** [API Testing Tools: Bruno, Hoppscotch, Postman, Insomnia in 2026](</en/tools/api-testing-2026.html>), [Load Testing Tools: k6, Locust, Gatling, Artillery](</en/tools/load-testing-tools.html>), [Cloud CLI Tools: aws-cli, gcloud, az, s5cmd, Cloud Comparisons](</en/tools/cloud-cli-tools.html>)

**See also:** [API Testing Tools: Bruno, Hoppscotch, Postman, Insomnia in 2026](</en/tools/api-testing-2026.html>), [Load Testing Tools: k6, Locust, Gatling, Artillery](</en/tools/load-testing-tools.html>), [Cloud CLI Tools: aws-cli, gcloud, az, s5cmd, Cloud Comparisons](</en/tools/cloud-cli-tools.html>)

**See also:** [API Testing Tools: Bruno, Hoppscotch, Postman, Insomnia in 2026](</en/tools/api-testing-2026.html>), [Load Testing Tools: k6, Locust, Gatling, Artillery](</en/tools/load-testing-tools.html>), [Cloud CLI Tools: aws-cli, gcloud, az, s5cmd, Cloud Comparisons](</en/tools/cloud-cli-tools.html>)
