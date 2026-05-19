---
title: "Database Encryption"
description: "Implementing database encryption with TDE, column-level encryption, application-level encryption, and key management."
date: 2026-03-17
board: security
url: https://dingjiu1989-hue.github.io/en/security/database-encryption.html
---

# Database Encryption

Database Encryption Layers 

Database encryption protects data at rest and in transit. Multiple layers provide defense in depth. 

Transparent Data Encryption (TDE) 

TDE encrypts the entire database at the storage layer: 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- SQL Server TDE

CREATE DATABASE ENCRYPTION KEY

WITH ALGORITHM = AES_256

ENCRYPTION BY SERVER CERTIFICATE DatabaseCert;

ALTER DATABASE ProductionDB

SET ENCRYPTION ON;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Check encryption status

SELECT DB_NAME(database_id) as DatabaseName,

encryption_state_desc,

percent_complete

FROM sys.dm_database_encryption_keys;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- PostgreSQL TDE (with pg_tde extension)

CREATE EXTENSION pg_tde;

SELECT pg_tde_add_database_key_provider(

'file-vault',

'{"type":"file","path":"/etc/postgresql/keys.json"}'

);

SELECT pg_tde_set_principal_key('production-db-key', 'file-vault');

Column-Level Encryption 

Encrypt specific sensitive columns: 

from cryptography.fernet import Fernet

import base64

class ColumnEncryptor:

def **init**(self, master_key):

self.fernet = Fernet(master_key)

def encrypt_column(self, value):

if value is None:

return None

return self.fernet.encrypt(value.encode()).decode()

def decrypt_column(self, encrypted_value):

if encrypted_value is None:

return None

return self.fernet.decrypt(encrypted_value.encode()).decode()

def searchable_encryption(self, value):

"""Deterministic encryption for searchable columns"""

from cryptography.hazmat.primitives import hashes

digest = hashes.Hash(hashes.SHA256())

digest.update(value.encode())

digest.update(b"deterministic_salt")

return digest.finalize().hex()[:32]

## Usage

encryptor = ColumnEncryptor(os.environ["COLUMN_ENCRYPTION_KEY"])

## Encrypt PII before storage

cursor.execute("""

INSERT INTO users (email, ssn, name)

VALUES (%s, %s, %s)

""", (

encryptor.encrypt_column("alice@example.com"),

encryptor.encrypt_column("123-45-6789"),

"Alice"

))

Application-Level Encryption 

Encrypt data before it reaches the database: 

// Node.js application-level encryption

const crypto = require("crypto");

class ApplicationEncryptor {

constructor(encryptionKey) {

this.algorithm = "aes-256-gcm";

this.key = crypto.scryptSync(encryptionKey, "salt", 32);

}

encrypt(plaintext) {

const iv = crypto.randomBytes(12);

const cipher = crypto.createCipheriv(this.algorithm, this.key, iv);

let encrypted = cipher.update(plaintext, "utf8", "hex");

encrypted += cipher.final("hex");

const authTag = cipher.getAuthTag().toString("hex");

return JSON.stringify({

iv: iv.toString("hex"),

data: encrypted,

tag: authTag,

version: 1

});

}

decrypt(encrypted) {

const { iv, data, tag } = JSON.parse(encrypted);

const decipher = crypto.createDecipheriv(

this.algorithm,

this.key,

Buffer.from(iv, "hex")

);

decipher.setAuthTag(Buffer.from(tag, "hex"));

let decrypted = decipher.update(data, "hex", "utf8");

decrypted += decipher.final("utf8");

return decrypted;

}

}

Key Management 

key_management:

key_hierarchy:

master_key: aws_kms / hsm

database_key: encrypted_by_master_key

column_keys: encrypted_by_database_key

rotation:

master_key: yearly

database_key: monthly

column_keys: on_demand

access_control:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- kms:key_owner

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- kms:encrypt

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- kms:decrypt

audit:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- all_key_usage_logged

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- key_access_alerting

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- unauthorized_access_blocked

Performance Considerations 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Benchmark: Column-level vs TDE

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- TDE overhead: 1-3% performance impact

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Column-level overhead: 5-15% per encrypted column

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Indexes on encrypted columns

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Deterministic encryption allows exact match

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Order-preserving encryption allows range queries

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Homomorphic encryption allows computations (slow)

CREATE INDEX idx_email_hash 

ON users (sha2(email, 256)); -- Searchable hash

Conclusion 

Layer your database encryption strategy. Use TDE for bulk encryption with minimal performance impact. Use column-level encryption for specific PII fields. Use application-level encryption for the strongest protection. Manage keys carefully with a hierarchical key system and rotate regularly. Always encrypt data in transit with TLS.

**See also:** [Encryption Key Management Best Practices](</en/security/encryption-key-management.html>), [Key Management Systems](</en/security/key-management.html>), [SOC 2 Technical Controls](</en/security/soc2-technical.html>).

**See also:** [Key Management Systems](</en/security/key-management.html>), [Web Application Firewall Implementation](</en/security/waf-implementation.html>), [Encryption Key Management Best Practices](</en/security/encryption-key-management.html>)

**See also:** [Key Management Systems](</en/security/key-management.html>), [Web Application Firewall Implementation](</en/security/waf-implementation.html>), [Encryption Key Management Best Practices](</en/security/encryption-key-management.html>)

**See also:** [Key Management Systems](</en/security/key-management.html>), [Web Application Firewall Implementation](</en/security/waf-implementation.html>), [Encryption Key Management Best Practices](</en/security/encryption-key-management.html>)

**See also:** [Key Management Systems](</en/security/key-management.html>), [Web Application Firewall Implementation](</en/security/waf-implementation.html>), [Encryption Key Management Best Practices](</en/security/encryption-key-management.html>)

**See also:** [Key Management Systems](</en/security/key-management.html>), [Web Application Firewall Implementation](</en/security/waf-implementation.html>), [Encryption Key Management Best Practices](</en/security/encryption-key-management.html>)

**See also:** [GDPR Technical Controls](</en/security/gdpr-technical.html>), [Helm Security](</en/security/helm-security.html>), [MFA Implementation](</en/security/mfa-implementation.html>)

**See also:** [GDPR Technical Controls](</en/security/gdpr-technical.html>), [Helm Security](</en/security/helm-security.html>), [MFA Implementation](</en/security/mfa-implementation.html>)

**See also:** [GDPR Technical Controls](</en/security/gdpr-technical.html>), [Helm Security](</en/security/helm-security.html>), [MFA Implementation](</en/security/mfa-implementation.html>)

**See also:** [GDPR Technical Controls](</en/security/gdpr-technical.html>), [Helm Security](</en/security/helm-security.html>), [MFA Implementation](</en/security/mfa-implementation.html>)

**See also:** [GDPR Technical Controls](</en/security/gdpr-technical.html>), [Helm Security](</en/security/helm-security.html>), [MFA Implementation](</en/security/mfa-implementation.html>)

**See also:** [GDPR Technical Controls](</en/security/gdpr-technical.html>), [Helm Security](</en/security/helm-security.html>), [MFA Implementation](</en/security/mfa-implementation.html>)

**See also:** [GDPR Technical Controls](</en/security/gdpr-technical.html>), [Helm Security](</en/security/helm-security.html>), [MFA Implementation](</en/security/mfa-implementation.html>)
