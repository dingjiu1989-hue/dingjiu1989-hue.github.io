---
title: "DevSecOps: Integrating Security into CI/CD"
description: "Integrate SAST, DAST, dependency scanning, container scanning, and policy-as-code into your CI/CD pipeline for shift-left security."
date: 2026-03-04
board: security
url: https://aidev.fit/en/security/devsecops-pipeline.html
---

# DevSecOps: Integrating Security into CI/CD

DevSecOps embeds security into every stage of the software development lifecycle. Rather than running security assessments at the end of a release cycle, DevSecOps shifts security left into development and CI/CD pipelines. This article covers how to integrate SAST, DAST, dependency scanning, container scanning, and policy-as-code into your pipelines.

## Shift-Left Security

The shift-left principle moves security testing earlier in the development process. Finding and fixing a vulnerability during development costs 10 times less than fixing it in production, and 100 times less than fixing it after a breach.

## Security Gates in the Pipeline

A mature DevSecOps pipeline has security gates at every stage:

Code Commit -> SAST -> Dependency Scan -> Build -> Container Scan ->

Integration Test -> DAST -> Staging -> Policy Check -> Production

Each gate can pass, fail with a warning, or fail and block the pipeline. The severity determines the action: critical and high findings block the pipeline, while medium and low findings create tickets for the development team.

## Static Application Security Testing (SAST)

SAST analyzes source code without executing it. It identifies vulnerabilities like SQL injection, cross-site scripting (XSS), buffer overflows, and insecure cryptographic usage.

## Popular SAST Tools

  * **Semgrep** : Open-source, fast, and supports custom rules. Works with most programming languages.

  * **SonarQube** : Static analysis with quality gates and technical debt tracking.

  * **CodeQL** : GitHub's semantic code analysis engine. Query-based vulnerability detection.

  * **Checkmarx / Fortify** : Commercial SAST tools with extensive rule sets.




## Pipeline Integration

## GitHub Actions: SAST with Semgrep

name: SAST Scan

on:

pull_request:

branches: [main]

jobs:

semgrep:

runs-on: ubuntu-latest

steps:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- uses: actions/checkout@v4

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- uses: semgrep/semgrep-action@v1

with:

config: p/default

audit_on: push

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: Check for blocking findings

run: |

if [ "${{ steps.semgrep.outputs.results }}" != "" ]; then

echo "SAST found vulnerabilities. Fix before merging."

exit 1

fi

## SAST Best Practices

  * Run SAST on every pull request, not just on push to main.

  * Use incremental scanning for faster feedback on large codebases.

  * Tune rules to reduce false positives. Block only high-confidence findings.

  * Create custom rules for your application's specific security patterns.




## Dependency Scanning

Modern applications use dozens of open-source libraries. Each library introduces transitive dependencies with potential vulnerabilities.

## Software Bill of Materials (SBOM)

An SBOM is a formal inventory of all software components in an application. Generate SBOMs in CycloneDX or SPDX format.

## Generate SBOM with Syft

syft packages . -o cyclonedx-json > sbom.json

## Scan SBOM for vulnerabilities with Grype

grype sbom:./sbom.json

## Dependency Scanning Tools

  * **Dependabot** : GitHub's built-in dependency scanning and automated pull requests for patches.

  * **Renovate** : Open-source dependency update tool with extensive customization.

  * **Snyk** : Commercial vulnerability scanner with fix advice and license compliance.

  * **OWASP Dependency-Check** : Open-source scanner that identifies CVEs in dependencies.




## Dependabot configuration

version: 2

updates:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- package-ecosystem: "npm"

directory: "/"

schedule:

interval: "weekly"

open-pull-requests-limit: 10

labels:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- "dependencies"

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- "security"

## Dependency Scanning Policy

  * Block the pipeline on critical or high severity vulnerabilities in direct dependencies.

  * Flag transitive dependency vulnerabilities but only block if they are exploitable.

  * Require automated dependency updates within 7 days for critical, 30 days for high.

  * Monitor for license compliance alongside vulnerability scanning.




## Dynamic Application Security Testing (DAST)

DAST tests the running application from the outside, simulating real-world attack patterns. It discovers vulnerabilities that SAST misses, such as authentication bypass, session management flaws, and business logic errors.

## DAST Tools

  * **OWASP ZAP** : Open-source web application scanner with automated and manual modes.

  * **Burp Suite** : Commercial web security testing platform with advanced scanning.

  * **Arachni** : Open-source web application security scanner framework.




## Pipeline Integration

## DAST with OWASP ZAP in CI/CD

services:

zap:

image: ghcr.io/zaproxy/zaproxy:stable

options: --user root

steps:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: Run ZAP Scan

run: |

docker run -v $(pwd):/zap/wrk:rw \

ghcr.io/zaproxy/zaproxy:stable \

zap-full-scan.py \

-t https://staging.example.com \

-r zap_report.html \

-z "-config spider.maxDuration=10"

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: Check ZAP Results

run: |

if grep -q "High" zap_report.html; then

echo "DAST found High severity issues"

exit 1

fi

## DAST Best Practices

  * Run DAST against staging or review environments, not production.

  * Authenticate DAST scanners to test authenticated functionality.

  * Use baseline scans for smoke testing and full scans for release candidates.

  * Integrate with Jira or ticketing for automatic issue creation.




## Container Scanning

Container images bundle applications with their runtime dependencies. Vulnerabilities in base images or installed packages become part of the container.

## Scanning Pipeline Integration

## Dockerfile with security best practices

FROM alpine:3.19 AS builder

RUN apk add --no-cache build-base

FROM alpine:3.19

RUN apk add --no-cache ca-certificates && \

addgroup -S app && adduser -S app -G app

COPY --from=builder /app/bin/server /app/server

USER app

EXPOSE 8080

## Container scanning with Trivy in CI/CD

jobs:

scan:

runs-on: ubuntu-latest

steps:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- uses: actions/checkout@v4

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: Build image

run: docker build -t myapp:${{ github.sha }} .

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: Scan with Trivy

uses: aquasecurity/trivy-action@master

with:

image-ref: myapp:${{ github.sha }}

format: sarif

output: trivy-results.sarif

severity: CRITICAL,HIGH

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: Upload results

uses: github/codeql-action/upload-sarif@v3

with:

sarif_file: trivy-results.sarif

## Container Security Practices

  * Use minimal base images (Alpine, distroless) to reduce attack surface.

  * Scan images before pushing to the registry.

  * Enforce signed images with Cosign.

  * Enable granular runtime security with seccomp, AppArmor, or SELinux policies.




## Policy-as-Code

Policy-as-code defines security and compliance rules as executable code. Policies are versioned, reviewed, and enforced automatically in the pipeline.

## Open Policy Agent (OPA) and Rego

OPA enforces policies across the software lifecycle. Rego is OPA's policy language.

## Rego policy: Require encryption at rest

package kubernetes.storage

deny[msg] {

volume := input.volumes[_]

volume.persistentVolumeClaim

not volume.encrypted

msg := sprintf("Volume %v must have encryption enabled", [volume.name])

}

## Policy Gates in the Pipeline

## Conftest: Policy enforcement for Kubernetes manifests

steps:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: Check Kubernetes policies

run: |

conftest test deployment.yaml \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--policy policies/ \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--namespace kubernetes

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: Check Terraform policies

run: |

conftest test main.tf \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--policy policies/terraform/

## Common Policy Rules

  * Containers must not run as root.

  * All ingress must have TLS enabled.

  * S3 buckets must block public access.

  * Database instances must have encryption at rest.

  * IAM roles must have resource-level constraints.




## Building a DevSecOps Culture

Tools alone do not make DevSecOps successful. The human elements matter more.

  * **Developer empowerment** : Give developers access to security scan results and fix guidance. Do not use security as a gate without providing remediation support.

  * **Security champions** : Train security champions in each development team. They bridge the gap between security and engineering.

  * **Friction reduction** : Optimize scan times. A 30-minute SAST scan encourages skipping. A 2-minute scan integrates naturally into the workflow.

  * **Blameless culture** : When security scans find issues, the process worked correctly. Celebrate catching issues early rather than blaming developers.




## Conclusion

DevSecOps shifts security from a final gate to an integrated part of the development process. SAST catches code-level vulnerabilities, dependency scanning manages supply chain risk, DAST validates runtime behavior, container scanning secures artifacts, and policy-as-code enforces standards. Together, these practices make security a natural part of delivering software, not an obstacle to it.

**See also:** [Secure Software Development Lifecycle](</en/security/secure-sdlc.html>), [Container Security Best Practices](</en/security/container-security.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>).

**See also:** [Secure Software Development Lifecycle](</en/security/secure-sdlc.html>), [Container Security Best Practices](</en/security/container-security.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)

**See also:** [Secure Software Development Lifecycle](</en/security/secure-sdlc.html>), [Container Security Best Practices](</en/security/container-security.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)

**See also:** [Secure Software Development Lifecycle](</en/security/secure-sdlc.html>), [Container Security Best Practices](</en/security/container-security.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)

**See also:** [Secure Software Development Lifecycle](</en/security/secure-sdlc.html>), [Container Security Best Practices](</en/security/container-security.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)

**See also:** [Secure Software Development Lifecycle](</en/security/secure-sdlc.html>), [Container Security Best Practices](</en/security/container-security.html>), [Mobile Application Security Guide](</en/security/mobile-security.html>)

**See also:** [Security Log Management](</en/security/log-management-security.html>), [OAuth 2.0 and PKCE Explained](</en/security/oauth2-pkce.html>), [Password Hashing Algorithms Compared](</en/security/password-hashing.html>)

**See also:** [Security Log Management](</en/security/log-management-security.html>), [OAuth 2.0 and PKCE Explained](</en/security/oauth2-pkce.html>), [Password Hashing Algorithms Compared](</en/security/password-hashing.html>)

**See also:** [Security Log Management](</en/security/log-management-security.html>), [OAuth 2.0 and PKCE Explained](</en/security/oauth2-pkce.html>), [Password Hashing Algorithms Compared](</en/security/password-hashing.html>)

**See also:** [Security Log Management](</en/security/log-management-security.html>), [OAuth 2.0 and PKCE Explained](</en/security/oauth2-pkce.html>), [Password Hashing Algorithms Compared](</en/security/password-hashing.html>)

**See also:** [Security Log Management](</en/security/log-management-security.html>), [OAuth 2.0 and PKCE Explained](</en/security/oauth2-pkce.html>), [Password Hashing Algorithms Compared](</en/security/password-hashing.html>)

**See also:** [Security Log Management](</en/security/log-management-security.html>), [OAuth 2.0 and PKCE Explained](</en/security/oauth2-pkce.html>), [Password Hashing Algorithms Compared](</en/security/password-hashing.html>)

**See also:** [Security Log Management](</en/security/log-management-security.html>), [OAuth 2.0 and PKCE Explained](</en/security/oauth2-pkce.html>), [Password Hashing Algorithms Compared](</en/security/password-hashing.html>)

**See also:** [Security Log Management](</en/security/log-management-security.html>), [OAuth 2.0 and PKCE Explained](</en/security/oauth2-pkce.html>), [Password Hashing Algorithms Compared](</en/security/password-hashing.html>)

**See also:** [Security Log Management](</en/security/log-management-security.html>), [OAuth 2.0 and PKCE Explained](</en/security/oauth2-pkce.html>), [Password Hashing Algorithms Compared](</en/security/password-hashing.html>)

**See also:** [Security Log Management](</en/security/log-management-security.html>), [OAuth 2.0 and PKCE Explained](</en/security/oauth2-pkce.html>), [Password Hashing Algorithms Compared](</en/security/password-hashing.html>)

**See also:** [Security Log Management](</en/security/log-management-security.html>), [OAuth 2.0 and PKCE Explained](</en/security/oauth2-pkce.html>), [Password Hashing Algorithms Compared](</en/security/password-hashing.html>)

**See also:** [Security Log Management](</en/security/log-management-security.html>), [OAuth 2.0 and PKCE Explained](</en/security/oauth2-pkce.html>), [Password Hashing Algorithms Compared](</en/security/password-hashing.html>)

**See also:** [Security Log Management](</en/security/log-management-security.html>), [OAuth 2.0 and PKCE Explained](</en/security/oauth2-pkce.html>), [Password Hashing Algorithms Compared](</en/security/password-hashing.html>)

**See also:** [Security Log Management](</en/security/log-management-security.html>), [OAuth 2.0 and PKCE Explained](</en/security/oauth2-pkce.html>), [Password Hashing Algorithms Compared](</en/security/password-hashing.html>)

**See also:** [Security Log Management](</en/security/log-management-security.html>), [OAuth 2.0 and PKCE Explained](</en/security/oauth2-pkce.html>), [Password Hashing Algorithms Compared](</en/security/password-hashing.html>)

**See also:** [Security Log Management](</en/security/log-management-security.html>), [OAuth 2.0 and PKCE Explained](</en/security/oauth2-pkce.html>), [Password Hashing Algorithms Compared](</en/security/password-hashing.html>)
