---
title: "SBOM Management"
description: "Managing Software Bill of Materials with generation, verification, vulnerability correlation, and compliance."
date: 2026-03-18
board: security
url: https://dingjiu1989-hue.github.io/en/security/sbom-management.html
---

# SBOM Management

What is an SBOM? 

A Software Bill of Materials (SBOM) is a detailed inventory of all components in a software application. It enables vulnerability tracking, license compliance, and supply chain risk management. 

SBOM Generation 

Generate SBOMs using SPDX or CycloneDX formats: 

## Generate SBOM with Syft

syft packages myapp:latest -o cyclonedx-json > sbom.cyclonedx.json

syft packages myapp:latest -o spdx-json > sbom.spdx.json

syft dir:./src -o cyclonedx-json > src-sbom.json

## Generate SBOM for multiple languages

syft packages package-lock.json -o cyclonedx-json

syft packages requirements.txt -o cyclonedx-json

syft packages go.sum -o cyclonedx-json

## Programmatic SBOM generation

import json

def generate_sbom(packages, metadata):

sbom = {

"bomFormat": "CycloneDX",

"specVersion": "1.5",

"version": 1,

"metadata": {

"timestamp": datetime.utcnow().isoformat() + "Z",

"tools": [{"name": "custom-bom-generator", "version": "1.0"}],

"component": {

"type": "application",

"name": metadata["name"],

"version": metadata["version"]

}

},

"components": []

}

for pkg in packages:

sbom["components"].append({

"type": "library",

"name": pkg["name"],

"version": pkg["version"],

"purl": pkg.get("purl"),

"licenses": pkg.get("licenses", []),

"supplier": pkg.get("supplier", {})

})

return sbom

SBOM Verification 

Verify SBOM integrity and completeness: 

## sbom-verification-pipeline.yaml

verification_steps:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: validate_format

tool: cyclonedx-cli

command: validate sbom.cyclonedx.json

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: check_completeness

rules:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- all_packages_have_version: true

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- all_packages_have_purl: true

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- license_information_present: true

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- dependency_graph_complete: true

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: verify_signature

tool: cosign

command: cosign verify-blob --signature sbom.json.sig sbom.json

Vulnerability Correlation 

Correlate SBOM components with known vulnerabilities: 

import requests

class SBOMVulnerabilityCorrelator:

def **init**(self):

self.osv_api = "https://api.osv.dev/v1/query"

def correlate(self, sbom):

vulnerabilities = []

for component in sbom["components"]:

purl = component.get("purl")

if not purl:

continue

## Query OSV database

response = requests.post(self.osv_api, json={

"package": {

"purl": purl

},

"version": component["version"]

})

if response.status_code == 200:

results = response.json()

for vuln in results.get("vulns", []):

vulnerabilities.append({

"component": component["name"],

"version": component["version"],

"vuln_id": vuln["id"],

"severity": vuln.get("severity", [{}])[0].get("score", "unknown"),

"summary": vuln.get("summary", "")

})

return vulnerabilities

SBOM Storage and Management 

## SBOM storage strategy

sbom_storage:

format: cyclonedx-json

storage: s3://sbom-bucket/

retention: 90_days

indexing:

database: opensearch

index_pattern: "sbom-*"

fields:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- component.name

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- component.version

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- component.purl

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- metadata.timestamp

lifecycle:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- stage: generated

action: store_and_index

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- stage: verified

action: mark_verified

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- stage: expired

action: archive

SBOM as Attestation 

## Sign SBOM with cosign

cosign attest-blob sbom.cyclonedx.json \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--signer "identity" \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--type cyclonedx \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--predicate sbom.cyclonedx.json

## Verify attestation

cosign verify-attestation --type cyclonedx sbom.cyclonedx.json

Conclusion 

SBOMs are essential for supply chain security. Generate them automatically in your CI pipeline, verify their integrity, and correlate components with vulnerability databases. Store SBOMs alongside your artifacts and sign them for tamper evidence. Use SBOMs for compliance, vulnerability management, and incident response.

**See also:** [Vulnerability Management](</en/security/vulnerability-management.html>), [Helm Security](</en/security/helm-security.html>), [Patching Strategy](</en/security/patching-strategy.html>).

**See also:** [Helm Security](</en/security/helm-security.html>), [Vulnerability Management](</en/security/vulnerability-management.html>), [Audit Logging Best Practices](</en/security/audit-logging.html>)

**See also:** [Helm Security](</en/security/helm-security.html>), [Vulnerability Management](</en/security/vulnerability-management.html>), [Audit Logging Best Practices](</en/security/audit-logging.html>)

**See also:** [Helm Security](</en/security/helm-security.html>), [Vulnerability Management](</en/security/vulnerability-management.html>), [Audit Logging Best Practices](</en/security/audit-logging.html>)

**See also:** [Helm Security](</en/security/helm-security.html>), [Vulnerability Management](</en/security/vulnerability-management.html>), [Audit Logging Best Practices](</en/security/audit-logging.html>)

**See also:** [Helm Security](</en/security/helm-security.html>), [Vulnerability Management](</en/security/vulnerability-management.html>), [Audit Logging Best Practices](</en/security/audit-logging.html>)

**See also:** [Patching Strategy](</en/security/patching-strategy.html>), [Supply Chain Security](</en/security/supply-chain-security.html>), [Compliance Automation](</en/security/compliance-automation.html>)

**See also:** [Patching Strategy](</en/security/patching-strategy.html>), [Supply Chain Security](</en/security/supply-chain-security.html>), [Compliance Automation](</en/security/compliance-automation.html>)

**See also:** [Patching Strategy](</en/security/patching-strategy.html>), [Supply Chain Security](</en/security/supply-chain-security.html>), [Compliance Automation](</en/security/compliance-automation.html>)

**See also:** [Patching Strategy](</en/security/patching-strategy.html>), [Supply Chain Security](</en/security/supply-chain-security.html>), [Compliance Automation](</en/security/compliance-automation.html>)

**See also:** [Patching Strategy](</en/security/patching-strategy.html>), [Supply Chain Security](</en/security/supply-chain-security.html>), [Compliance Automation](</en/security/compliance-automation.html>)

**See also:** [Patching Strategy](</en/security/patching-strategy.html>), [Supply Chain Security](</en/security/supply-chain-security.html>), [Compliance Automation](</en/security/compliance-automation.html>)
