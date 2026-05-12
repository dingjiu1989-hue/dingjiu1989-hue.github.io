---
title: "Helm Security"
description: "Securing Helm deployments with chart signing, provenance verification, secrets management, and best practices."
date: 2026-05-12
board: security
url: https://dingjiu1989-hue.github.io/en/security/helm-security.html
---

# Helm Security

Helm Security Challenges   
Helm simplifies Kubernetes deployments but introduces security concerns: untrusted charts, unprotected secrets, and supply chain risks.   
Chart Signing   
Sign charts with GPG to verify authenticity:   

    
    
    # Generate signing key
    
    gpg --full-generate-key
    
    gpg --list-secret-keys
    
    
    
    # Sign a chart
    
    helm package mychart/
    
    helm sign mychart-1.0.0.tgz --key "developer@example.com"
    
    
    
    # Verify a chart
    
    helm verify mychart-1.0.0.tgz
    
    
    
    # With custom public key
    
    gpg --export developer@example.com > pubkey.asc
    
    helm verify mychart-1.0.0.tgz --keyring pubkey.asc
    
    

  
Provenance Files   
Provenance files contain the chart hash and signature:   

    
    
    # mychart-1.0.0.tgz.prov
    
    apiVersion: v1
    
    files:
    
      - mychart-1.0.0.tgz
    
    chart: |
    
      sha256: a1b2c3d4...
    
    signature: |
    
      -----BEGIN PGP SIGNATURE-----
    
      iQEzBAABCAAdFiEE...
    
      -----END PGP SIGNATURE-----
    
    

  
Automated Verification in CI   

    
    
    # CI pipeline chart verification
    
    pipeline:
    
      - name: verify-charts
    
        commands:
    
          # Import trusted keys
    
          - gpg --import trusted-keys.asc
    
          
    
          # Verify all charts
    
          - for chart in charts/*.tgz; do
    
              helm verify "$chart" --keyring trusted-keys.asc || exit 1
    
            done
    
          
    
          # Scan for vulnerabilities
    
          - trivy fs charts/
    
          
    
          # Lint charts
    
          - helm lint charts/*
    
          
    
          # Check for deprecated APIs
    
          - pluto detect-files -d charts/
    
    

  
Secrets Management   
Never store secrets in values files:   

    
    
    # BAD: Secrets in values
    
    apiKey: "sk-1234567890"
    
    dbPassword: "password123"
    
    
    
    # GOOD: Reference external secret
    
    apiKey: "{{ .Values.externalSecrets.apiKey }}"
    
    dbPassword: "{{ .Values.externalSecrets.dbPassword }}"
    
    

  
Use external secrets operator:   

    
    
    apiVersion: external-secrets.io/v1beta1
    
    kind: ExternalSecret
    
    metadata:
    
      name: app-secrets
    
    spec:
    
      refreshInterval: 1h
    
      secretStoreRef:
    
        name: vault-backend
    
        kind: ClusterSecretStore
    
      target:
    
        name: app-secret
    
      data:
    
      - secretKey: api-key
    
        remoteRef:
    
          key: secret/data/app
    
          property: api-key
    
      - secretKey: db-password
    
        remoteRef:
    
          key: secret/data/app
    
          property: db-password
    
    

  
Values Security   
Validate values with JSON Schema:   

    
    
    {
    
      "$schema": "https://json-schema.org/draft-07/schema",
    
      "type": "object",
    
      "properties": {
    
        "image": {
    
          "type": "object",
    
          "properties": {
    
            "repository": { "type": "string" },
    
            "tag": { "type": "string", "pattern": "^[a-zA-Z0-9._-]+$" },
    
            "pullPolicy": { 
    
              "type": "string",
    
              "enum": ["Always", "IfNotPresent", "Never"]
    
            }
    
          },
    
          "required": ["repository"]
    
        },
    
        "securityContext": {
    
          "type": "object",
    
          "required": ["runAsNonRoot"],
    
          "properties": {
    
            "runAsNonRoot": { "type": "boolean", "const": true },
    
            "runAsUser": { "type": "integer", "minimum": 1000 }
    
          }
    
        }
    
      }
    
    }
    
    

  
RBAC for Helm Operations   

    
    
    apiVersion: rbac.authorization.k8s.io/v1
    
    kind: Role
    
    metadata:
    
      name: helm-deployer
    
    rules:
    
    - apiGroups: ["apps", "extensions"]
    
      resources: ["deployments", "statefulsets"]
    
      verbs: ["get", "list", "create", "update", "patch"]
    
    - apiGroups: [""]
    
      resources: ["secrets", "configmaps"]
    
      verbs: ["get", "list", "create"]
    
    - apiGroups: ["batch"]
    
      resources: ["jobs"]
    
      verbs: ["get", "create", "delete"]
    
    

  
Conclusion   
Secure Helm deployments with chart signing and provenance verification. Use external secrets management instead of storing secrets in values files. Validate values with JSON Schema. Restrict Helm RBAC to specific operations. Scan charts for vulnerabilities before deployment. Always verify chart signatures from third-party repositories.
