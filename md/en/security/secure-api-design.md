---
title: "Secure API Design Principles"
description: "Guide to secure API design covering input validation, rate limiting, idempotency, error handling, and defense-in-depth strategies."
date: 2026-03-12
board: security
url: https://dingjiu1989-hue.github.io/en/security/secure-api-design.html
---

# Secure API Design Principles

Introduction 

APIs are the backbone of modern application architecture. A well-designed API considers security at every layer, from request validation to response handling. Security must be built into the API contract — it cannot be bolted on afterward. 

Input Validation 

Validate all input at the API boundary before processing. Never trust client-provided data. 

from pydantic import BaseModel, Field, validator

from fastapi import FastAPI, HTTPException

from typing import Optional

import re

app = FastAPI()

class CreateUserRequest(BaseModel):

username: str = Field(..., min_length=3, max_length=32)

email: str = Field(..., max_length=255)

age: int = Field(..., ge=0, le=150)

@validator('username')

def validate_username(cls, v):

if not re.match(r'^[a-zA-Z0-9_-]+$', v):

raise ValueError('Username must be alphanumeric')

## Blocklist certain patterns

blocklist = ['admin', 'root', 'null', 'undefined']

if v.lower() in blocklist:

raise ValueError('Username not allowed')

return v.lower()

@validator('email')

def validate_email(cls, v):

if not re.match(r'^[\w\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\.-]+@[\w\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\.-]+\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\.\w+$', v):

raise ValueError('Invalid email format')

return v.lower()

@app.post("/api/users")

def create_user(user: CreateUserRequest):

return {"user": user.username, "email": user.email}

Rate Limiting 

Rate limiting prevents abuse, brute force attacks, and resource exhaustion. 

import time

from collections import defaultdict

from functools import wraps

class RateLimiter:

def **init**(self):

self.requests = defaultdict(list)

def check(self, key: str, max_requests: int, window_seconds: int) -> bool:

now = time.time()

window_start = now - window_seconds

## Clean old entries

self.requests[key] = [

t for t in self.requests[key] if t > window_start

]

## Check limit

if len(self.requests[key]) >= max_requests:

return False

self.requests[key].append(now)

return True

## Token bucket algorithm

class TokenBucket:

def **init**(self, capacity: int, refill_rate: float):

self.capacity = capacity

self.tokens = capacity

self.refill_rate = refill_rate

self.last_refill = time.time()

def consume(self, tokens: int = 1) -> bool:

self._refill()

if self.tokens >= tokens:

self.tokens -= tokens

return True

return False

def _refill(self):

now = time.time()

elapsed = now - self.last_refill

self.tokens = min(self.capacity, 

self.tokens + elapsed * self.refill_rate)

self.last_refill = now

## Apply rate limiting via middleware

from fastapi import Request, HTTPException

RATE_LIMITER = TokenBucket(capacity=100, refill_rate=10)

@app.middleware("http")

async def rate_limit_middleware(request: Request, call_next):

client_ip = request.client.host

if not RATE_LIMITER.consume():

raise HTTPException(status_code=429, detail="Rate limit exceeded")

return await call_next(request)

Idempotency 

Idempotent APIs prevent duplicate operations when clients retry requests. 

import uuid

from datetime import datetime, timedelta

class IdempotencyMiddleware:

def **init**(self, redis_client, ttl_hours=24):

self.redis = redis_client

self.ttl = timedelta(hours=ttl_hours)

async def process_request(self, request):

## Check for idempotency key on mutating requests

if request.method in ('POST', 'PATCH', 'PUT', 'DELETE'):

idempotency_key = request.headers.get('Idempotency-Key')

if not idempotency_key:

raise HTTPException(

status_code=400,

detail="Idempotency-Key header required for mutating requests"

)

## Check for existing result

cache_key = f"idempotency:{idempotency_key}"

existing = await self.redis.get(cache_key)

if existing:

## Return cached response (idempotent replay)

return json.loads(existing)

## Process request and cache result

response = await self.process_request_internal(request)

await self.redis.setex(

cache_key,

self.ttl.seconds,

json.dumps(response)

)

return response

Error Handling 

Secure error handling reveals minimal information while providing useful feedback to legitimate clients. 

from fastapi import Request, HTTPException

from fastapi.responses import JSONResponse

class SecureExceptionHandler:

@staticmethod

def handle_validation_error(request: Request, exc: Exception):

## Generic message, don't reveal internal details

return JSONResponse(

status_code=422,

content={

"error": "validation_error",

"message": "The request contains invalid data"

}

)

@staticmethod

def handle_auth_error(request: Request, exc: Exception):

## Don't distinguish between "user not found" and "wrong password"

return JSONResponse(

status_code=401,

content={

"error": "authentication_failed",

"message": "Invalid credentials"

}

)

@staticmethod

def handle_internal_error(request: Request, exc: Exception):

## Log full details internally

import logging

logger = logging.getLogger(**name**)

logger.error(f"Internal error: {exc}", exc_info=True)

## Return minimal info to client

error_id = str(uuid.uuid4())

return JSONResponse(

status_code=500,

content={

"error": "internal_error",

"message": "An unexpected error occurred",

"error_id": error_id

}

)

app.add_exception_handler(ValueError, SecureExceptionHandler.handle_validation_error)

app.add_exception_handler(HTTPException, SecureExceptionHandler.handle_auth_error)

API Security Checklist 

api_security:

authentication:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- use_jwt_or_oauth2_not_basic_auth

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- enforce_short_token_expiry: 15_minutes

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- implement_token_rotation

authorization:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- enforce_least_privilege

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- validate_permissions_on_every_request

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- never_trust_url_parameters_for_authz

input_validation:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- validate_all_input_at_boundary

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- use_schema_validation_framework

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- enforce_strict_data_types

rate_limiting:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- per_client_rate_limits

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- tiered_throttling

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- ip_based_fallback

error_handling:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- consistent_error_format

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- no_stack_traces_in_production

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- log_all_errors_internally

headers:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- enforce_strict_transport_security

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- set_x_content_type_options: nosniff

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- set_x_frame_options: DENY

Conclusion 

Secure API design integrates security into every layer: validate and sanitize all input, apply rate limiting to prevent abuse, implement idempotency for reliable retries, handle errors without leaking information, and enforce authentication and authorization on every endpoint. Security is not an endpoint feature — it is a design property.

**See also:** [Input Validation Deep Dive](</en/security/input-validation.html>), [Serverless Security](</en/security/serverless-security.html>), [API Security: Protecting Your REST and GraphQL APIs](</en/security/api-security-guide.html>).

**See also:** [Input Validation Deep Dive](</en/security/input-validation.html>), [CORS Security](</en/security/cors-security.html>), [Serverless Security](</en/security/serverless-security.html>)

**See also:** [Input Validation Deep Dive](</en/security/input-validation.html>), [CORS Security](</en/security/cors-security.html>), [Serverless Security](</en/security/serverless-security.html>)

**See also:** [Input Validation Deep Dive](</en/security/input-validation.html>), [CORS Security](</en/security/cors-security.html>), [Serverless Security](</en/security/serverless-security.html>)

**See also:** [Input Validation Deep Dive](</en/security/input-validation.html>), [CORS Security](</en/security/cors-security.html>), [Serverless Security](</en/security/serverless-security.html>)

**See also:** [Input Validation Deep Dive](</en/security/input-validation.html>), [CORS Security](</en/security/cors-security.html>), [Serverless Security](</en/security/serverless-security.html>)

**See also:** [Secure Configuration Management](</en/security/secure-configuration.html>), [Session Management Security](</en/security/session-management.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [Secure Configuration Management](</en/security/secure-configuration.html>), [Session Management Security](</en/security/session-management.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [Secure Configuration Management](</en/security/secure-configuration.html>), [Session Management Security](</en/security/session-management.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [Secure Configuration Management](</en/security/secure-configuration.html>), [Session Management Security](</en/security/session-management.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [Secure Configuration Management](</en/security/secure-configuration.html>), [Session Management Security](</en/security/session-management.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [Secure Configuration Management](</en/security/secure-configuration.html>), [Session Management Security](</en/security/session-management.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [Secure Configuration Management](</en/security/secure-configuration.html>), [Session Management Security](</en/security/session-management.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [Secure Configuration Management](</en/security/secure-configuration.html>), [Session Management Security](</en/security/session-management.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [Secure Configuration Management](</en/security/secure-configuration.html>), [Session Management Security](</en/security/session-management.html>), [API Authentication Methods](</en/security/api-authentication.html>)

**See also:** [Secure Configuration Management](</en/security/secure-configuration.html>), [Session Management Security](</en/security/session-management.html>), [API Authentication Methods](</en/security/api-authentication.html>)
