---
title: "Data Classification"
description: "Implementing data classification with labeling, handling procedures, and automated classification tools."
date: 2026-05-12
board: security
url: https://dingjiu1989-hue.github.io/en/security/data-classification.html
---

# Data Classification

## Data Classification

## Data Classification

## Data Classification

## Data Classification

## Data Classification

## Data Classification

## Data Classification

## Data Classification

## Data Classification

## Data Classification

## Data Classification

## Data Classification

Why Classify Data? 

Data classification ensures sensitive information receives appropriate protection. Without classification, you either over-protect everything (wasting resources) or under-protect critical data (inviting breaches). 

Classification Levels 

Define clear tiers: 

| Level | Label | Examples | Controls | |-------|-------|----------|----------| | 4 | Restricted | PII, trade secrets | Encryption, MFA, DLP | | 3 | Confidential | Financial reports | Encryption at rest | | 2 | Internal | HR policies | Access control | | 1 | Public | Marketing materials | No restrictions | 

Automated Classification 

Use content inspection to classify data automatically: 

import re

import hashlib

class DataClassifier:

def **init**(self):

self.patterns = {

"ssn": r"\d{3}-\d{2}-\d{4}",

"email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\.[a-zA-Z]{2,}",

"credit_card": r"\b(?:\d[ -]*?){13,16}\b"

}

def classify_document(self, content, metadata):

score = 0

findings = []

for label, pattern in self.patterns.items():

matches = re.findall(pattern, content)

if matches:

score += len(matches) * 10

findings.append({"type": label, "count": len(matches)})

if score > 50:

return "restricted", findings

elif score > 10:

return "confidential", findings

elif metadata.get("internal"):

return "internal", findings

return "public", findings

Handling Procedures 

Define procedures for each classification level: 

## handling-policies.yaml

restricted:

storage: encrypted_bucket_kms

transmission: require_tls_1.3

retention: 7_years

destruction: shred_and_degauss

sharing: require_nda_and_approval

confidential:

storage: encrypted_bucket

transmission: require_tls_1.2

retention: 3_years

destruction: shred

sharing: require_approval

Labeling Implementation 

Apply labels at multiple layers: 

// S3 object tagging for classification

const AWS = require("aws-sdk");

const s3 = new AWS.S3();

async function tagObject(bucket, key, classification) {

await s3.putObjectTagging({

Bucket: bucket,

Key: key,

Tagging: {

TagSet: [

{ Key: "classification", Value: classification },

{ Key: "classified-by", Value: "auto-classifier-v2" },

{ Key: "classified-at", Value: new Date().toISOString() }

]

}

}).promise();

}

Integration with DLP 

Classification feeds directly into DLP policies: 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Block restricted data leaving the network

CREATE DLP POLICY block_restricted_exfiltration

MATCHES classification = 'restricted'

AND operation IN ('email.send', 'usb.copy', 'cloud.upload')

ACTION block;

Conclusion 

Data classification is foundational to information security. Automate where possible, define clear handling procedures, and integrate classification labels across your data protection stack. Start with the most sensitive data and expand coverage iteratively.

**See also:** [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [Secrets Rotation](</en/security/secrets-rotation.html>), [GDPR Technical Controls](</en/security/gdpr-technical.html>).

**See also:** [Data Loss Prevention Strategies](</en/security/dlp-strategies.html>), [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [Secrets Rotation](</en/security/secrets-rotation.html>)

**See also:** [Data Loss Prevention Strategies](</en/security/dlp-strategies.html>), [OAuth2 Implementation](</en/security/oauth2-implementation.html>), [Secrets Rotation](</en/security/secrets-rotation.html>)
