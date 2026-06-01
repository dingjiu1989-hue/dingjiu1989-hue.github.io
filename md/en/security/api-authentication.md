---
title: "API Authentication Methods"
description: "Comprehensive guide to API authentication covering API keys, OAuth2 client credentials, mTLS, HMAC signing, and implementation trade-offs."
date: 2026-03-06
board: security
url: https://aidev.fit/en/security/api-authentication.html
---

# API Authentication Methods

Introduction 

API authentication verifies the identity of clients calling your API. Choosing the right authentication method depends on the threat model, client type, and operational requirements. This guide covers the four dominant approaches and their appropriate use cases. 

API Keys 

API keys are the simplest form of API authentication. A static token is issued to each client and included in every request. 

from fastapi import FastAPI, HTTPException, Depends

from fastapi.security import APIKeyHeader

app = FastAPI()

api_key_header = APIKeyHeader(name="X-API-Key")

API_KEYS = {

"sk-live-a1b2c3d4": {"client": "payment-service", "scopes": ["read:transactions"]},

"sk-test-e5f6g7h8": {"client": "test-client", "scopes": ["read:test"]},

}

def validate_api_key(api_key: str = Depends(api_key_header)):

if api_key not in API_KEYS:

raise HTTPException(status_code=403, detail="Invalid API key")

return API_KEYS[api_key]

@app.get("/api/transactions")

def get_transactions(client=Depends(validate_api_key)):

if "read:transactions" not in client["scopes"]:

raise HTTPException(status_code=403, detail="Insufficient permissions")

return {"transactions": [...]}

**Pros** : Simple, fast, easy to revoke. **Cons** : Static keys can leak, no identity delegation, limited granularity. 

OAuth2 Client Credentials 

The OAuth2 client credentials grant is designed for server-to-server communication where the client is the resource owner. 

import requests

from authlib.integrations.requests_client import OAuth2Session

## Client configuration

client = OAuth2Session(

client_id='my-service',

client_secret='my-secret',

scope='read:orders write:orders'

)

## Obtain access token

token = client.fetch_token(

url='https://auth.example.com/oauth/token',

grant_type='client_credentials'

)

## Use token for API calls

response = client.get(

'https://api.example.com/orders',

headers={'Accept': 'application/json'}

)

Server-side token validation: 

import jwt

from jwt import PyJWKClient

JWKS_URL = "https://auth.example.com/.well-known/jwks.json"

def validate_bearer_token(token: str):

jwks_client = PyJWKClient(JWKS_URL)

signing_key = jwks_client.get_signing_key_from_jwt(token)

payload = jwt.decode(

token,

signing_key.key,

algorithms=["RS256"],

audience="https://api.example.com",

issuer="https://auth.example.com",

options={"verify_exp": True}

)

## Validate scopes

token_scopes = payload.get("scope", "").split()

required_scopes = {"read:orders"}

if not required_scopes.issubset(set(token_scopes)):

raise PermissionError("Insufficient scope")

return payload

Mutual TLS (mTLS) 

mTLS extends TLS so that both client and server present certificates, establishing mutual authentication at the transport layer. 

## Generate client certificate

openssl req -newkey rsa:2048 -nodes \

-keyout client-key.pem \

-out client-csr.pem \

-subj "/CN=payment-service.production.internal"

## Sign with internal CA

openssl x509 -req -in client-csr.pem \

-CA ca-cert.pem -CAkey ca-key.pem \

-CAcreateserial -out client-cert.pem \

-days 365 -sha256

## Configure server for mTLS (Nginx)

server {

listen 443 ssl;

ssl_certificate /etc/nginx/server-cert.pem;

ssl_certificate_key /etc/nginx/server-key.pem;

ssl_client_certificate /etc/nginx/ca-cert.pem;

ssl_verify_client on;

ssl_verify_depth 2;

location /api/ {

## Extract client certificate info

proxy_set_header X-Client-CN $ssl_client_s_dn;

proxy_set_header X-Client-Verify $ssl_client_verify;

proxy_pass http://backend;

}

}

## Flask app reading mTLS client info

from flask import Flask, request

app = Flask(**name**)

@app.route('/api/data')

def api_data():

client_cn = request.headers.get('X-Client-CN')

client_verify = request.headers.get('X-Client-Verify')

if client_verify != 'SUCCESS':

return {"error": "TLS verification failed"}, 403

## Authorize based on client certificate CN

allowed_clients = {

'payment-service.production.internal': ['read:transactions'],

'order-service.production.internal': ['read:write:orders'],

}

if client_cn not in allowed_clients:

return {"error": "Unauthorized client"}, 403

return {"data": "sensitive data"}

HMAC Signing 

HMAC signing creates request-specific signatures that prevent tampering and replay attacks. 

import hmac

import hashlib

import time

from typing import Dict

class HMACAuthClient:

def **init**(self, api_key: str, api_secret: str):

self.api_key = api_key

self.api_secret = api_secret.encode()

def sign_request(self, method: str, path: str, body: bytes = b'') -> Dict[str, str]:

timestamp = str(int(time.time()))

nonce = secrets.token_hex(8)

## Build message to sign

message = f"{method}
{path}
{timestamp}
{nonce}
".encode() + body

signature = hmac.new(

self.api_secret,

message,

hashlib.sha256

).hexdigest()

return {

'X-API-Key': self.api_key,

'X-Timestamp': timestamp,

'X-Nonce': nonce,

'X-Signature': signature,

}

class HMACAuthServer:

def **init**(self):

self.secrets = {"client-1": "supersecret123"}

self.nonce_store = set()

def verify_request(self, method, path, headers, body):

api_key = headers.get('X-API-Key')

timestamp = headers.get('X-Timestamp')

nonce = headers.get('X-Nonce')

signature = headers.get('X-Signature')

## Replay protection

if int(time.time()) - int(timestamp) > 300:

return False # Expired

if nonce in self.nonce_store:

return False # Replay

self.nonce_store.add(nonce)

## Verify signature

secret = self.secrets.get(api_key)

if not secret:

return False

message = f"{method}
{path}
{timestamp}
{nonce}
".encode() + body

expected = hmac.new(secret.encode(), message, hashlib.sha256).hexdigest()

return hmac.compare_digest(expected, signature)

Choosing the Right Method 

| Method | Best For | Security Level | Complexity | |--------|----------|---------------|------------| | API Keys | Simple internal services, quick integration | Low-Medium | Very Low | | OAuth2 Client Credentials | Third-party integrations, scoped access | High | Medium | | mTLS | Service mesh, zero-trust, internal microservices | Very High | High | | HMAC Signing | Financial APIs, requests that must be non-repudiable | High | Medium | 

Conclusion 

No single API authentication method fits all use cases. Use API keys for low-risk internal tools, OAuth2 client credentials for third-party integrations with scope requirements, mTLS for service mesh and zero-trust architectures, and HMAC signing when request integrity and non-repudiation are critical. Always combine authentication with TLS encryption.
