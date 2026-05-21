---
title: "SSH Security Hardening"
description: "Practical steps to secure SSH access including key management, configuration hardening, and fail2ban setup."
date: 2025-12-03
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/ssh-security-hardening.html
---

# SSH Security Hardening

SSH is the gateway to your infrastructure. A compromised SSH key or misconfigured daemon can lead to complete server takeover. Hardening SSH is one of the highest-impact security improvements you can make.

## Disable Password Authentication

Password authentication is susceptible to brute-force attacks. Disable it and use key-based authentication only:

## /etc/ssh/sshd_config

PasswordAuthentication no

ChallengeResponseAuthentication no

UsePAM no

PubkeyAuthentication yes

After making changes, restart the SSH daemon:

sudo systemctl restart sshd

Always keep an active SSH session open while testing changes. If something breaks, you can debug before the session closes.

## Use Ed25519 Keys

Ed25519 keys offer better security and performance than RSA:

ssh-keygen -t ed25519 -a 100 -f ~/.ssh/id_ed25519

The `-a 100` option increases the KDF rounds for the private key file, making it harder to crack if the file is stolen. For legacy systems that require RSA, use at least 4096-bit keys:

ssh-keygen -t rsa -b 4096 -a 100 -f ~/.ssh/id_rsa

## Restrict Key Usage

Limit what individual keys can do using the `authorized_keys` file:

## ~/.ssh/authorized_keys

restrict,command="/usr/bin/git-shell",from="192.168.1.0/24" ssh-ed25519 AAA...

The `restrict` keyword denies all forwarding and agent access. `command=` limits the key to a specific command. `from=` restricts which IP addresses can use this key.

## Disable Root Login

Never allow direct root SSH access:

PermitRootLogin no

Use a regular user account with `sudo` access instead. This creates an audit trail -- every privileged command is logged with the user who ran it.

## Change the Default Port

Changing the default port (22) reduces automated attack noise:

Port 2222

This is not real security (a determined attacker will find your SSH port), but it dramatically reduces log noise from automated scanners.

## Use a Strong Cipher Configuration

Modern SSH supports strong ciphers. Enforce them:

Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com

MACs hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com

KexAlgorithms curve25519-sha256,diffie-hellman-group16-sha512

HostKeyAlgorithms ssh-ed25519,rsa-sha2-512

This configuration only allows algorithms with proven security. Remove legacy algorithms like `diffie-hellman-group14-sha1` and `hmac-sha1`.

## SSH Timeout and Session Limits

Prevent idle sessions from accumulating:

ClientAliveInterval 300

ClientAliveCountMax 2

TCPKeepAlive no

MaxSessions 10

MaxStartups 10:30:60

`ClientAliveInterval=300` with `ClientAliveCountMax=2` means the server checks every 5 minutes and disconnects after 10 minutes of inactivity. `MaxStartups` limits concurrent unauthenticated connections to prevent DoS attacks.

## Fail2Ban Integration

Install and configure Fail2Ban to block brute-force attempts:

sudo apt install fail2ban

## /etc/fail2ban/jail.local

[sshd]

enabled = true

port = ssh

filter = sshd

logpath = /var/log/auth.log

maxretry = 3

bantime = 3600

findtime = 600

This bans IPs for one hour after three failed attempts within ten minutes. For internet-facing SSH, consider longer ban times (24 hours) to be more aggressive.

## Two-Factor Authentication

Add a second factor with `libpam-google-authenticator`:

sudo apt install libpam-google-authenticator

google-authenticator

## /etc/pam.d/sshd

auth required pam_google_authenticator.so

## /etc/ssh/sshd_config

ChallengeResponseAuthentication yes

AuthenticationMethods publickey,keyboard-interactive

This requires both an SSH key and a TOTP code to authenticate. Use this for high-value jump boxes and production servers.

## SSH Agent Forwarding

Be careful with agent forwarding. Use `-J` (jump host) instead when possible:

## Instead of forwarding your agent through a chain:

ssh -J bastion.example.com target.internal

## Or use ProxyJump in ~/.ssh/config:

Host internal-*

ProxyJump bastion.example.com

If you must use agent forwarding, use `ssh -A` with the `-t` flag for a single session rather than enabling forwarding globally in your config.

## Key Rotation

Regularly rotate SSH keys and audit authorized keys:

## !/bin/bash

## audit-ssh-keys.sh

for user in $(getent passwd | cut -d: -f1); do

home=$(getent passwd "$user" | cut -d: -f6)

if [[ -f "$home/.ssh/authorized_keys" ]]; then

echo "User: $user"

cat "$home/.ssh/authorized_keys"

fi

done

Remove keys belonging to departed team members and replace keys that are over a year old. Integrate key management with your identity provider (Okta, Azure AD) using tools like `ssh-ca` for certificate-based auth.

## Monitor SSH Access

Monitor SSH access in real-time:

## Watch auth log for SSH activity

tail -f /var/log/auth.log | grep sshd

## Audit currently logged-in users

w

## Last login times for all users

lastlog

Set up alerts for SSH logins from unexpected IP ranges or at unusual hours using log ingestion tools.

## Summary

SSH hardening follows defense in depth: disable passwords, use Ed25519 keys, lock down the daemon configuration, and add Fail2Ban. For production systems, add two-factor authentication and eliminate agent forwarding in favor of jump hosts. Regularly audit authorized keys and rotate them. Most SSH compromises come from weak configurations, not zero-days -- hardening your SSH setup prevents the majority of attack vectors.

**See also:** [Developer Environment Setup Guide](</en/tech/dev-environment-setup.html>), [Kubernetes Security Best Practices](</en/tech/kubernetes-services-security.html>), [Nginx Configuration Guide](</en/tech/nginx-configuration-guide.html>).

**See also:** [Developer Environment Setup Guide](</en/tech/dev-environment-setup.html>), [Kubernetes Security Best Practices](</en/tech/kubernetes-services-security.html>), [Nginx Configuration Guide](</en/tech/nginx-configuration-guide.html>)

**See also:** [Developer Environment Setup Guide](</en/tech/dev-environment-setup.html>), [Kubernetes Security Best Practices](</en/tech/kubernetes-services-security.html>), [Nginx Configuration Guide](</en/tech/nginx-configuration-guide.html>)

**See also:** [Developer Environment Setup Guide](</en/tech/dev-environment-setup.html>), [Kubernetes Security Best Practices](</en/tech/kubernetes-services-security.html>), [Nginx Configuration Guide](</en/tech/nginx-configuration-guide.html>)

**See also:** [Developer Environment Setup Guide](</en/tech/dev-environment-setup.html>), [Kubernetes Security Best Practices](</en/tech/kubernetes-services-security.html>), [Nginx Configuration Guide](</en/tech/nginx-configuration-guide.html>)

**See also:** [Developer Environment Setup Guide](</en/tech/dev-environment-setup.html>), [Kubernetes Security Best Practices](</en/tech/kubernetes-services-security.html>), [Nginx Configuration Guide](</en/tech/nginx-configuration-guide.html>)

**See also:** [Microservices Communication Patterns](</en/tech/microservices-communication.html>), [Monitoring and Alerting Setup](</en/tech/monitoring-alerting-setup.html>), [Reverse Proxy Guide](</en/tech/reverse-proxy-guide.html>)

**See also:** [Microservices Communication Patterns](</en/tech/microservices-communication.html>), [Monitoring and Alerting Setup](</en/tech/monitoring-alerting-setup.html>), [Reverse Proxy Guide](</en/tech/reverse-proxy-guide.html>)

**See also:** [Microservices Communication Patterns](</en/tech/microservices-communication.html>), [Monitoring and Alerting Setup](</en/tech/monitoring-alerting-setup.html>), [Reverse Proxy Guide](</en/tech/reverse-proxy-guide.html>)

**See also:** [Microservices Communication Patterns](</en/tech/microservices-communication.html>), [Monitoring and Alerting Setup](</en/tech/monitoring-alerting-setup.html>), [Reverse Proxy Guide](</en/tech/reverse-proxy-guide.html>)

**See also:** [Microservices Communication Patterns](</en/tech/microservices-communication.html>), [Monitoring and Alerting Setup](</en/tech/monitoring-alerting-setup.html>), [Reverse Proxy Guide](</en/tech/reverse-proxy-guide.html>)

**See also:** [Microservices Communication Patterns](</en/tech/microservices-communication.html>), [Monitoring and Alerting Setup](</en/tech/monitoring-alerting-setup.html>), [Reverse Proxy Guide](</en/tech/reverse-proxy-guide.html>)

**See also:** [Microservices Communication Patterns](</en/tech/microservices-communication.html>), [Monitoring and Alerting Setup](</en/tech/monitoring-alerting-setup.html>), [Reverse Proxy Guide](</en/tech/reverse-proxy-guide.html>)

**See also:** [Microservices Communication Patterns](</en/tech/microservices-communication.html>), [Monitoring and Alerting Setup](</en/tech/monitoring-alerting-setup.html>), [Reverse Proxy Guide](</en/tech/reverse-proxy-guide.html>)

**See also:** [Microservices Communication Patterns](</en/tech/microservices-communication.html>), [Monitoring and Alerting Setup](</en/tech/monitoring-alerting-setup.html>), [Reverse Proxy Guide](</en/tech/reverse-proxy-guide.html>)

**See also:** [Microservices Communication Patterns](</en/tech/microservices-communication.html>), [Monitoring and Alerting Setup](</en/tech/monitoring-alerting-setup.html>), [Reverse Proxy Guide](</en/tech/reverse-proxy-guide.html>)

**See also:** [Microservices Communication Patterns](</en/tech/microservices-communication.html>), [Monitoring and Alerting Setup](</en/tech/monitoring-alerting-setup.html>), [Reverse Proxy Guide](</en/tech/reverse-proxy-guide.html>)

**See also:** [Microservices Communication Patterns](</en/tech/microservices-communication.html>), [Monitoring and Alerting Setup](</en/tech/monitoring-alerting-setup.html>), [Reverse Proxy Guide](</en/tech/reverse-proxy-guide.html>)
