---
title: "Certificate Management"
description: "Practical guide to TLS certificate management covering Let's Encrypt, ACME protocol, automated renewal, and certificate monitoring."
date: 2026-03-08
board: security
url: https://dingjiu1989-hue.github.io/en/security/certificate-management.html
---

# Certificate Management

## Certificate Management

### Certificate Management

#### Certificate Management

#### Certificate Management

#### Certificate Management

#### Certificate Management

#### Certificate Management

#### Certificate Management

#### Certificate Management

#### Certificate Management

#### Certificate Management

#### Certificate Management

#### Certificate Management

#### Certificate Management

#### Certificate Management

#### Certificate Management

#### Certificate Management

Introduction 

TLS certificate management is a critical operational responsibility. Expired certificates cause service outages, security warnings, and loss of user trust. Modern certificate management leverages the ACME protocol and Let's Encrypt to automate issuance and renewal at scale. 

Let's Encrypt 

Let's Encrypt is a free, automated, and open certificate authority (CA) that provides DV certificates trusted by all major browsers. 

#### Install Certbot (Let's Encrypt client)

sudo apt install certbot python3-certbot-nginx

#### Obtain certificate with webroot authentication

sudo certbot certonly --webroot \

-w /var/www/example.com -d example.com \

-w /var/www/api.example.com -d api.example.com \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--email admin@example.com \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--agree-tos \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--non-interactive

#### Obtain certificate with DNS challenge (for wildcards)

sudo certbot certonly --manual \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--preferred-challenges dns \

-d example.com -d *.example.com

ACME Protocol 

The Automated Certificate Management Environment (ACME) protocol automates certificate issuance, renewal, and revocation. 

import josepy as jose

from acme import client, messages

from cryptography import x509

from cryptography.hazmat.primitives import hashes

class ACMEClient:

def **init**(self, directory_url, email):

self.directory_url = directory_url

self.email = email

self.net = client.ClientNetwork(

jose.JWKRSA(key=rsa_private_key),

user_agent="my-acme-client/1.0"

)

self.directory = messages.Directory.from_json(

self.net.get(directory_url).json()

)

self.acme = client.ClientV2(self.directory, self.net)

def register_account(self):

"""Register ACME account with Let's Encrypt."""

terms = self.directory.meta.terms_of_service

registration = self.acme.new_account(

messages.NewRegistration(

key=self.net.key,

terms_of_service_agreed=True,

contact=[f"mailto:{self.email}"]

)

)

return registration

def request_certificate(self, domain, csr_pem):

"""Request certificate issuance."""

#### Create authorization

order = self.acme.new_order(csr_pem)

#### Complete challenges for each identifier

for auth in order.authorizations:

#### HTTP-01 or DNS-01 challenge

challenge = auth.body.challenges[0]

self.respond_challenge(challenge)

#### Finalize order

order = self.acme.finalize_order(order, csr_pem)

return order.fullchain_pem

Automated Renewal 

Certificate renewal should be fully automated with monitoring and alerting. 

#### Certbot systemd timer for automatic renewal

#### /etc/systemd/system/certbot-renewal.service

[Unit]

Description=Certbot Renewal

[Service]

Type=oneshot

ExecStart=/usr/bin/certbot renew --quiet --pre-hook "systemctl reload nginx"

ExecStartPost=/usr/bin/systemctl reload nginx

#### /etc/systemd/system/certbot-renewal.timer

[Unit]

Description=Run certbot renewal twice daily

[Timer]

OnCalendar=_-_ -* 00:00,12:00

RandomizedDelaySec=3600

Persistent=true

[Install]

WantedBy=timers.target

#### Enable timer

sudo systemctl enable certbot-renewal.timer

sudo systemctl start certbot-renewal.timer

#### Test renewal process

sudo certbot renew --dry-run

Certificate Monitoring 

Monitor certificate expiration to catch renewal failures before they cause outages. 

import ssl

import datetime

import socket

from typing import Dict, List

class CertificateMonitor:

def **init**(self, warning_days: int = 30, critical_days: int = 7):

self.warning_days = warning_days

self.critical_days = critical_days

def check_certificate(self, hostname: str, port: int = 443) -> Dict:

context = ssl.create_default_context()

context.check_hostname = True

with socket.create_connection((hostname, port), timeout=10) as sock:

with context.wrap_socket(sock, server_hostname=hostname) as ssock:

cert = ssock.getpeercert()

#### Parse expiration

expires = datetime.datetime.strptime(

cert['notAfter'], '%b %d %H:%M:%S %Y %Z'

)

remaining = (expires - datetime.datetime.utcnow()).days

#### Check issuer

issuer = dict(x[0] for x in cert['issuer'])

#### Check SANs

sans = [san[1] for san in cert.get('subjectAltName', [])]

return {

'hostname': hostname,

'subject': cert['subject'],

'issuer': issuer.get('organizationName', 'Unknown'),

'expires': expires.isoformat(),

'remaining_days': remaining,

'sans': sans,

'serial': cert.get('serialNumber'),

'status': self._get_status(remaining),

}

def _get_status(self, remaining_days: int) -> str:

if remaining_days <= 0:

return 'EXPIRED'

elif remaining_days <= self.critical_days:

return 'CRITICAL'

elif remaining_days <= self.warning_days:

return 'WARNING'

return 'OK'

def monitor_domains(self, domains: List[str]) -> List[Dict]:

results = []

for domain in domains:

try:

result = self.check_certificate(domain)

results.append(result)

if result['status'] in ('CRITICAL', 'EXPIRED'):

self.alert(result)

except Exception as e:

results.append({

'hostname': domain,

'status': 'ERROR',

'error': str(e)

})

return results

#### OpenSSL-based certificate check

echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | \

openssl x509 -noout -enddate -subject -issuer

#### Mass certificate check

for domain in $(cat domains.txt); do

expires=$(echo | openssl s_client -connect $domain:443 -servername $domain 2>/dev/null | \

openssl x509 -noout -enddate | cut -d= -f2)

remaining=$(( ($(date -d "$expires" +%s) - $(date +%s)) / 86400 ))

echo "$domain: expires in $remaining days ($expires)"

done

Certificate Revocation 

#### Check OCSP status

openssl ocsp -issuer chain.pem -cert cert.pem \

-url $(openssl x509 -in cert.pem -noout -ocsp_uri) \

-header "Host" $(openssl x509 -in cert.pem -noout -ocsp_uri | cut -d/ -f3) \

-CAfile root.pem

#### CRL check

curl -O http://crl.example.com/intermediate.crl

openssl crl -in intermediate.crl -noout -text | grep -A1 "Serial Number"

Conclusion 

Modern certificate management means automation. Use Let's Encrypt with Certbot for domain-validated certificates, implement ACME for custom automation, set up systemd timers for renewal, and deploy monitoring that alerts days or weeks before expiration. Never rely on manual renewal processes — they fail under pressure and at scale.

**See also:** [TLS Configuration Guide](</en/security/tls-configuration.html>), [Cloud Security Posture Management](</en/security/cloud-security-posture.html>), [Infrastructure as Code Security](</en/security/iac-security.html>).

**See also:** [Cloud Security Posture Management](</en/security/cloud-security-posture.html>), [TLS Configuration Guide](</en/security/tls-configuration.html>), [Infrastructure as Code Security](</en/security/iac-security.html>)

**See also:** [Cloud Security Posture Management](</en/security/cloud-security-posture.html>), [TLS Configuration Guide](</en/security/tls-configuration.html>), [Infrastructure as Code Security](</en/security/iac-security.html>)

**See also:** [Cloud Security Posture Management](</en/security/cloud-security-posture.html>), [TLS Configuration Guide](</en/security/tls-configuration.html>), [Infrastructure as Code Security](</en/security/iac-security.html>)

**See also:** [Cloud Security Posture Management](</en/security/cloud-security-posture.html>), [TLS Configuration Guide](</en/security/tls-configuration.html>), [Infrastructure as Code Security](</en/security/iac-security.html>)

**See also:** [Cloud Security Posture Management](</en/security/cloud-security-posture.html>), [TLS Configuration Guide](</en/security/tls-configuration.html>), [Infrastructure as Code Security](</en/security/iac-security.html>)
