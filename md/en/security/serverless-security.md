---
title: "Serverless Security"
description: "Guide to serverless security covering function permissions, event validation, cold start risks, dependency management, and defense in depth."
date: 2026-03-13
board: security
url: https://dingjiu1989-hue.github.io/en/security/serverless-security.html
---

# Serverless Security

Introduction 

Serverless computing shifts operational responsibility to the cloud provider but introduces unique security challenges. Functions have expanded attack surfaces through event sources, third-party dependencies, and IAM roles. Understanding the serverless shared responsibility model is the first step toward securing these architectures. 

Function Permissions 

Serverless functions operate under IAM roles that should follow least privilege. Overly permissive roles are the most common serverless security issue. 

{

"Effect": "Allow",

"Action": [

"sqs:ReceiveMessage",

"sqs:DeleteMessage",

"sqs:GetQueueAttributes"

],

"Resource": "arn:aws:sqs:us-east-1:123456789012:my-queue"

}

// BAD: Wildcard permissions on DynamoDB

{

"Effect": "Allow",

"Action": "dynamodb:*",

"Resource": "*"

}

// GOOD: Scoped to specific table and actions

{

"Effect": "Allow",

"Action": [

"dynamodb:GetItem",

"dynamodb:PutItem",

"dynamodb:UpdateItem"

],

"Resource": "arn:aws:dynamodb:us-east-1:123456789012:table/Orders"

}

## AWS Lambda function handler with minimal permissions

import boto3

import os

TABLE_NAME = os.environ['TABLE_NAME']

def handler(event, context):

## The function IAM role only has access to this specific table

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table(TABLE_NAME)

order_id = event['order_id']

response = table.get_item(Key={'id': order_id})

return response['Item']

Event Validation 

Serverless functions are triggered by events from various sources. Each event must be validated before processing. 

import json

import re

def validate_s3_event(event):

"""Validate S3 event notification structure."""

required_keys = {'Records', 'eventVersion', 'eventSource'}

if not all(key in event for key in required_keys):

raise ValueError("Invalid S3 event structure")

for record in event['Records']:

## Validate S3 record structure

s3 = record.get('s3', {})

bucket = s3.get('bucket', {})

obj = s3.get('object', {})

if not bucket.get('name') or not obj.get('key'):

raise ValueError("Invalid S3 record")

## Validate object key to prevent path traversal

key = obj['key']

if '..' in key or key.startswith('/'):

raise ValueError(f"Invalid object key: {key}")

## Check file extension whitelist

allowed_extensions = {'.csv', '.json', '.parquet'}

if not any(key.endswith(ext) for ext in allowed_extensions):

raise ValueError(f"Unsupported file type: {key}")

return True

def validate_api_gateway_event(event):

"""Validate API Gateway proxy event."""

## Validate HTTP method

allowed_methods = {'GET', 'POST', 'PUT', 'DELETE'}

method = event.get('httpMethod')

if method not in allowed_methods:

raise ValueError(f"Invalid HTTP method: {method}")

## Validate path parameters

path = event.get('path', '')

if not re.match(r'^/[a-zA-Z0-9/_-]+$', path):

raise ValueError(f"Invalid path: {path}")

## Validate query string parameters

params = event.get('queryStringParameters') or {}

for key, value in params.items():

if len(value) > 1000:

raise ValueError(f"Parameter {key} exceeds maximum length")

return True

Cold Start Risks 

Cold starts occur when a function is invoked after being idle. They create windows where code is freshly loaded, which can be exploited. 

## Vulnerability scanner for cold start

import importlib

import sys

class ColdStartScanner:

def **init**(self):

self.known_vulnerable = self._load_vulnerability_db()

def scan_dependencies(self):

"""Scan all imported modules for known vulnerabilities."""

vulnerabilities = []

for module_name, module in sys.modules.items():

if hasattr(module, '**version** '):

version = module.**version**

if module_name in self.known_vulnerable:

vulns = self.known_vulnerable[module_name]

for vuln in vulns:

if self._version_in_range(version, vuln['affected']):

vulnerabilities.append({

'module': module_name,

'version': version,

'cve': vuln['cve'],

'severity': vuln['severity']

})

return vulnerabilities

## Dependencies: pin versions and scan regularly

## requirements.txt

requests==2.31.0

pydantic==2.5.0

cryptography==41.0.7

## npm package.json

{

"dependencies": {

"axios": "1.6.2",

"lodash": "4.17.21"

},

"scripts": {

"audit": "npm audit --audit-level=high"

}

}

Defense in Depth 

Serverless security requires multiple layers, as there is no host-based security (no antivirus, no host IDS). 

## Defense layer 1: Input validation at API Gateway

## Use request validation templates

## API Gateway JSON Schema validation

VALIDATION_SCHEMA = {

"$schema": "http://json-schema.org/draft-04/schema#",

"type": "object",

"properties": {

"email": {"type": "string", "format": "email"},

"amount": {"type": "number", "minimum": 0.01, "maximum": 10000}

},

"required": ["email", "amount"]

}

## Defense layer 2: Function-level validation

def process_order(event, context):

## Validate input structure

required_fields = ['user_id', 'product_id', 'quantity']

for field in required_fields:

if field not in event:

return {'statusCode': 400, 'body': f'Missing field: {field}'}

## Validate data types and ranges

if not isinstance(event['quantity'], int) or event['quantity'] < 1:

return {'statusCode': 400, 'body': 'Invalid quantity'}

## Defense layer 3: Principle of least function scope

## Each function should do ONE thing

return process_payment(event)

## Defense layer 4: Encryption at rest and in transit

from cryptography.fernet import Fernet

def encrypt_sensitive_data(data, key):

f = Fernet(key)

return f.encrypt(data.encode())

Monitoring and Logging 

import json

class ServerlessAuditLogger:

def **init**(self):

self.logs = []

def log_invocation(self, event, context, response):

"""Log sanitized invocation details."""

log_entry = {

'function_name': context.function_name,

'aws_request_id': context.aws_request_id,

'remaining_time': context.get_remaining_time_in_millis(),

'event_source': event.get('Records', [{}])[0].get('eventSource', 'unknown'),

'log_group': context.log_group_name,

'timestamp': datetime.utcnow().isoformat()

}

## Don't log sensitive data

self.logs.append(log_entry)

print(json.dumps(log_entry))

Conclusion 

Serverless security requires adapting traditional security principles to a new execution model. Enforce least privilege on function IAM roles, validate every event before processing, pin and scan dependencies, and implement defense in depth since traditional host-based controls are unavailable. Monitor function invocations and log appropriately, but never log sensitive data in function output.

**See also:** [CORS Security](</en/security/cors-security.html>), [Secure API Design Principles](</en/security/secure-api-design.html>), [Secure Configuration Management](</en/security/secure-configuration.html>).

**See also:** [CORS Security](</en/security/cors-security.html>), [Secure API Design Principles](</en/security/secure-api-design.html>), [Cloud Security Posture Management](</en/security/cloud-security-posture.html>)

**See also:** [CORS Security](</en/security/cors-security.html>), [Secure API Design Principles](</en/security/secure-api-design.html>), [Cloud Security Posture Management](</en/security/cloud-security-posture.html>)

**See also:** [CORS Security](</en/security/cors-security.html>), [Secure API Design Principles](</en/security/secure-api-design.html>), [Cloud Security Posture Management](</en/security/cloud-security-posture.html>)

**See also:** [CORS Security](</en/security/cors-security.html>), [Secure API Design Principles](</en/security/secure-api-design.html>), [Cloud Security Posture Management](</en/security/cloud-security-posture.html>)

**See also:** [CORS Security](</en/security/cors-security.html>), [Secure API Design Principles](</en/security/secure-api-design.html>), [Cloud Security Posture Management](</en/security/cloud-security-posture.html>)

**See also:** [Session Management Security](</en/security/session-management.html>), [Supply Chain Security](</en/security/supply-chain-security.html>), [Certificate Management](</en/security/certificate-management.html>)

**See also:** [Session Management Security](</en/security/session-management.html>), [Supply Chain Security](</en/security/supply-chain-security.html>), [Certificate Management](</en/security/certificate-management.html>)

**See also:** [Session Management Security](</en/security/session-management.html>), [Supply Chain Security](</en/security/supply-chain-security.html>), [Certificate Management](</en/security/certificate-management.html>)

**See also:** [Session Management Security](</en/security/session-management.html>), [Supply Chain Security](</en/security/supply-chain-security.html>), [Certificate Management](</en/security/certificate-management.html>)

**See also:** [Session Management Security](</en/security/session-management.html>), [Supply Chain Security](</en/security/supply-chain-security.html>), [Certificate Management](</en/security/certificate-management.html>)

**See also:** [Session Management Security](</en/security/session-management.html>), [Supply Chain Security](</en/security/supply-chain-security.html>), [Certificate Management](</en/security/certificate-management.html>)

**See also:** [Session Management Security](</en/security/session-management.html>), [Supply Chain Security](</en/security/supply-chain-security.html>), [Certificate Management](</en/security/certificate-management.html>)

**See also:** [Session Management Security](</en/security/session-management.html>), [Supply Chain Security](</en/security/supply-chain-security.html>), [Certificate Management](</en/security/certificate-management.html>)

**See also:** [Session Management Security](</en/security/session-management.html>), [Supply Chain Security](</en/security/supply-chain-security.html>), [Certificate Management](</en/security/certificate-management.html>)

**See also:** [Session Management Security](</en/security/session-management.html>), [Supply Chain Security](</en/security/supply-chain-security.html>), [Certificate Management](</en/security/certificate-management.html>)

**See also:** [Session Management Security](</en/security/session-management.html>), [Supply Chain Security](</en/security/supply-chain-security.html>), [Certificate Management](</en/security/certificate-management.html>)
