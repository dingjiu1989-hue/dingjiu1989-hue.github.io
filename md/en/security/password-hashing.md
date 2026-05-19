---
title: "Password Hashing Algorithms Compared"
description: "Compare bcrypt, Argon2, scrypt, and PBKDF2 password hashing algorithms for security, performance, and implementation guidance."
date: 2025-12-18
board: security
url: https://dingjiu1989-hue.github.io/en/security/password-hashing.html
---

# Password Hashing Algorithms Compared

The Difference Between Hashing and Encryption 

Password hashing is fundamentally different from encryption. Hashing is a one-way function: you cannot reverse a hash to recover the original password. Encryption is two-way: data can be decrypted with the correct key. Passwords must always be hashed, never encrypted, because the application should never be able to recover the original plaintext. 

Why Not Plain Hashes (SHA-256, MD5) 

Simple cryptographic hash functions like SHA-256 are designed for speed and correctness, not password storage. An attacker can compute billions of SHA-256 hashes per second using a GPU, making it trivial to brute-force leaked password hashes. 

Modern password hashing algorithms are intentionally slow and memory-hard, making brute-force attacks economically infeasible. 

Algorithm Comparison 

| Algorithm | Year | Memory Hard | Configurable | Recommended | |-----------|------|-------------|--------------|-------------| | bcrypt | 1999 | No | Cost factor | Yes (minimum) | | PBKDF2 | 2000 | No | Iterations | Yes (with high iterations) | | scrypt | 2009 | Yes | N, r, p params | Yes | | Argon2id | 2015 | Yes | Memory, time, parallelism | **Best** | 

bcrypt 

bcrypt remains the most widely deployed password hashing algorithm. It includes a built-in salt and a configurable cost factor. 

const bcrypt = require('bcrypt');

async function hashPassword(password) {

const saltRounds = 12; // Cost factor

const hash = await bcrypt.hash(password, saltRounds);

return hash;

}

async function verifyPassword(password, hash) {

return await bcrypt.compare(password, hash);

}

import bcrypt

def hash_password(password):

salt = bcrypt.gensalt(rounds=12)

return bcrypt.hashpw(password.encode(), salt)

def verify_password(password, hashed):

return bcrypt.checkpw(password.encode(), hashed)

The bcrypt output includes the version, cost factor, salt, and hash: 

$2b$12$LJ3m4ys3Lk0TSwHnbfgZxeCk7NaML3C1yVvvSxYf1UcJm9xHvKXq

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\**/ \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_ / \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\****_**_**___ _**_** _/\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_**_** ______ * __ *__ _**_** * __ * _/

| | Salt Hash

| Cost

Version

Choosing the Cost Factor 

Run a benchmark on your production hardware to determine the appropriate cost factor: 

| Cost Factor | Time (approx on modern CPU) | |-------------|----------------------------| | 10 | ~80ms | | 12 | ~320ms | | 14 | ~1.3s | | 16 | ~5s | 

Choose the highest cost factor that keeps authentication response time under 500ms. 

Argon2id 

Argon2id is the winner of the Password Hashing Competition (2015) and is the recommended algorithm for new applications. It resists both side-channel and GPU-based attacks. 

from argon2 import PasswordHasher

ph = PasswordHasher(

time_cost=3, # Number of iterations

memory_cost=65536, # 64 MB

parallelism=4, # Number of threads

hash_len=32, # Output length

salt_len=16 # Salt length

)

hash = ph.hash("correct horse battery staple")

verify = ph.verify(hash, "correct horse battery staple")

const argon2 = require('argon2');

const hash = await argon2.hash(password, {

type: argon2.argon2id,

memoryCost: 65536, // 64 MB

timeCost: 3, // 3 iterations

parallelism: 4

});

const valid = await argon2.verify(hash, password);

Tuning Argon2 Parameters 

| Parameter | Purpose | Recommendation | |-----------|---------|----------------| | memoryCost | Memory usage in KB | 64 MB minimum, 128 MB preferred | | timeCost | CPU iterations | 3 minimum, 5 for high security | | parallelism | Thread count | Equal to CPU core count | 

scrypt 

scrypt is a memory-hard function designed to be expensive on custom hardware. 

const crypto = require('crypto');

crypto.scrypt(password, salt, 64, {

N: 16384, // CPU/memory cost

r: 8, // Block size

p: 1 // Parallelization

}, (err, key) => {

// key is the derived hash

});

Common Mistakes 

| Mistake | Why It Is Dangerous | |---------|---------------------| | Unsalted hashes | Same passwords produce same hash; rainbow tables work | | MD5/SHA-1/SHA-256 | Too fast; billions of hashes per second on GPU | | Base64 as hashing | Encoding is not hashing; trivially reversible | | Truncated hashes | Increases collision probability | | Custom algorithms | Almost certainly has design flaws | | Peppers stored in code | Adds minimal protection, complicates rotation | 

Migration Strategy 

When upgrading from a weaker algorithm, use a rehash-on-verify pattern: 

def verify_and_upgrade(password, stored_hash):

if is_bcrypt_hash(stored_hash):

if bcrypt.checkpw(password.encode(), stored_hash):

if needs_upgrade(stored_hash): # cost factor too low?

new_hash = argon2.hash(password)

update_user_hash(user_id, new_hash)

return True

elif is_argon2_hash(stored_hash):

return argon2.verify(stored_hash, password)

return False

Summary 

Use Argon2id for all new applications. If Argon2 is not available, use bcrypt with a cost factor of 12 or higher. Never use SHA-256, MD5, or any fast hash for password storage. Always use a unique salt per password, and implement a rehash-on-verify strategy to upgrade existing hashes to stronger algorithms over time.

**See also:** [API Rate Limiting Implementation](</en/security/api-rate-limiting.html>), [Security Log Management](</en/security/log-management-security.html>), [Encryption at Rest Guide](</en/security/encryption-at-rest.html>).

**See also:** [Security Log Management](</en/security/log-management-security.html>), [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>)

**See also:** [Security Log Management](</en/security/log-management-security.html>), [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>)

**See also:** [Security Log Management](</en/security/log-management-security.html>), [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>)

**See also:** [Security Log Management](</en/security/log-management-security.html>), [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>)

**See also:** [Security Log Management](</en/security/log-management-security.html>), [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>)

**See also:** [Blockchain and Smart Contract Security](</en/security/blockchain-security.html>), [Cloud Security Basics: Shared Responsibility Model Explained](</en/security/cloud-security-basics.html>), [Incident Response Playbook for Developers](</en/security/incident-response.html>)

**See also:** [Blockchain and Smart Contract Security](</en/security/blockchain-security.html>), [Cloud Security Basics: Shared Responsibility Model Explained](</en/security/cloud-security-basics.html>), [Incident Response Playbook for Developers](</en/security/incident-response.html>)

**See also:** [Blockchain and Smart Contract Security](</en/security/blockchain-security.html>), [Cloud Security Basics: Shared Responsibility Model Explained](</en/security/cloud-security-basics.html>), [Incident Response Playbook for Developers](</en/security/incident-response.html>)

**See also:** [Blockchain and Smart Contract Security](</en/security/blockchain-security.html>), [Cloud Security Basics: Shared Responsibility Model Explained](</en/security/cloud-security-basics.html>), [Incident Response Playbook for Developers](</en/security/incident-response.html>)

**See also:** [Blockchain and Smart Contract Security](</en/security/blockchain-security.html>), [Cloud Security Basics: Shared Responsibility Model Explained](</en/security/cloud-security-basics.html>), [Incident Response Playbook for Developers](</en/security/incident-response.html>)

**See also:** [Blockchain and Smart Contract Security](</en/security/blockchain-security.html>), [Cloud Security Basics: Shared Responsibility Model Explained](</en/security/cloud-security-basics.html>), [Incident Response Playbook for Developers](</en/security/incident-response.html>)

**See also:** [Blockchain and Smart Contract Security](</en/security/blockchain-security.html>), [Cloud Security Basics: Shared Responsibility Model Explained](</en/security/cloud-security-basics.html>), [Incident Response Playbook for Developers](</en/security/incident-response.html>)
