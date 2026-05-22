---
title: "Database Encryption: Data at Rest and in Transit"
description: "Implement database encryption at rest and in transit to protect sensitive data and meet compliance requirements."
date: 2026-04-14
board: database
url: https://aidev.fit/en/database/database-encryption.html
---

# Database Encryption: Data at Rest and in Transit

Database encryption protects data from unauthorized access at multiple levels: encryption at rest protects stored data from physical theft or unauthorized disk access, and encryption in transit protects data during network transmission.

## Encryption at Rest

Transparent Data Encryption (TDE) is available in most commercial databases (SQL Server, Oracle, MySQL Enterprise). The database automatically encrypts data files and backups. Encryption is transparent to applications—no code changes needed.

Application-level encryption encrypts sensitive fields before they reach the database. Values are encrypted in the application, stored as binary or encrypted text, and decrypted when read. This protects data even from database administrators but complicates searches and indexing.

Column-level encryption encrypts specific columns. The database manages encryption keys and handles encryption and decryption transparently. This is a middle ground between TDE and application-level encryption.

## Key Management

The security of any encryption system depends on key management. Use a dedicated key management service (AWS KMS, Azure Key Vault, HashiCorp Vault). Rotate keys regularly. Never store encryption keys in the database, application configuration files, or source code.

Implement key hierarchies: a master key protects data keys, and data keys protect the actual data. Master keys rarely change. Data keys can be rotated independently. This limits the impact of a key compromise.

## Encryption in Transit

Always use TLS for database connections. Configure TLS 1.2 or higher. Disable older, insecure protocols. Require certificate validation on both client and server sides.

For replication traffic, enable TLS between primary and replica instances. Replication streams contain all data changes, including schema definitions and credentials.

## Performance Impact

Encryption adds CPU overhead for encryption and decryption operations. TDE typically adds 3-5% overhead. Application-level encryption can add more depending on the amount of encrypted data. Test encryption performance with production-like workloads.

Querying encrypted columns prevents standard indexing. Searchable encryption techniques (deterministic encryption, order-preserving encryption) trade security for functionality. Evaluate whether the security benefits justify the performance cost.

## Compliance

Encryption is required by most compliance frameworks. GDPR, HIPAA, PCI-DSS, and SOC 2 all mandate encryption at rest and in transit. Document your encryption architecture and key management procedures for auditors.
