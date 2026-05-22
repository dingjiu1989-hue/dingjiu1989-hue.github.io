---
title: "Container Runtime Security"
description: "Securing container runtime with seccomp, AppArmor, SELinux, Falco, and runtime threat detection."
date: 2026-03-16
board: security
url: https://aidev.fit/en/security/container-runtime-security.html
---

# Container Runtime Security

Runtime Security Fundamentals 

Container runtime security monitors and restricts container behavior during execution. It prevents attackers who gain container access from breaking out or causing damage. 

seccomp Profiles 

seccomp (Secure Computing Mode) restricts system calls: 

{

"defaultAction": "SCMP_ACT_ERRNO",

"architectures": ["SCMP_ARCH_X86_64"],

"syscalls": [

{

"names": [

"accept4", "bind", "connect", "listen",

"read", "write", "open", "close",

"mmap", "munmap", "brk",

"exit", "exit_group", "getpid"

],

"action": "SCMP_ACT_ALLOW"

}

]

}

Apply profiles in Kubernetes: 

apiVersion: v1

kind: Pod

metadata:

name: secure-app

spec:

securityContext:

seccompProfile:

type: Localhost

localhostProfile: profiles/audit.json

containers:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: app

image: myapp:latest

securityContext:

seccompProfile:

type: Localhost

localhostProfile: profiles/strict.json

AppArmor 

AppArmor uses path-based access control: 

## AppArmor profile for container

## include

profile container-strict flags=(attach_disconnected) {

## include

## Network

network inet tcp,

network inet udp,

## Filesystem

/ r,

/proc/*/status r,

/etc/resolv.conf r,

/app/** r,

/app/bin ix,

## Deny everything else

deny /etc/shadow r,

deny /sys/** r,

deny /proc/** w,

}

SELinux for Containers 

SELinux provides mandatory access control: 

## Enable SELinux for container runtime

sudo setenforce 1

sudo semanage permissive -a container_t

## Apply SELinux context to container

podman run \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--security-opt label=type:container_t \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--security-opt label=level:s0:c1,c2 \

nginx

## Check SELinux context

ps -eZ | grep container

Falco Runtime Detection 

Falco detects anomalous behavior: 

## falco-rules.yaml

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- rule: Terminal shell in container

desc: Detect shell spawn in container

condition: >

spawned_process 

and container 

and proc.name in (bash, zsh, sh, dash)

and not proc.pname in (docker, kubectl)

output: >

Shell spawned in container (%user_name %container_name)

priority: WARNING

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- rule: Unexpected outbound connection

desc: Detect reverse shell or data exfiltration

condition: >

outbound 

and container 

and not allowed_outbound_destination

output: >

Unexpected outbound connection from container

priority: CRITICAL

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- rule: Write to sensitive path

desc: Detect attempts to write to host filesystem

condition: >

open_write 

and container 

and fd.name startswith /etc/cron

output: >

Write to sensitive host path from container

priority: CRITICAL

## Falco event consumer

import json

import requests

def handle_falco_events():

resp = requests.get(

"http://localhost:8765/events",

stream=True

)

for line in resp.iter_lines():

if line:

event = json.loads(line)

priority = event.get("priority")

rule = event.get("rule")

output = event.get("output")

if priority in ["CRITICAL", "EMERGENCY"]:

trigger_incident_response(rule, output)

elif priority in ["WARNING", "ERROR"]:

alert_security_team(rule, output)

Runtime Security Best Practices 

runtime_security:

images:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- scan_before_run

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- block_known_vulnerable

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- enforce_signing

containers:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- read_only_root_filesystem: true

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- drop_all_capabilities

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- add_capabilities_selectively

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- run_as_non_root

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- seccomp: custom_profile

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- apparmor: enforced

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- no_new_privileges: true

monitoring:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- falco_runtime_detection

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- audit_log_collection

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- behavioral_baselining

Conclusion 

Container runtime security requires multiple layers. Use seccomp to restrict system calls, AppArmor for path-based controls, and SELinux for mandatory access. Deploy Falco for runtime threat detection. Run containers with the minimum capabilities required. Monitor and alert on suspicious behavior in real time.

**See also:** [EDR: Endpoint Detection and Response Solutions](</en/security/endpoint-detection-response.html>), [Container Scanning Tools: Securing Images in CI/CD](</en/security/container-scanning-tools.html>), [SIEM: Security Information and Event Management](</en/security/security-information-event-management.html>).

**See also:** [Container Image Security](</en/security/container-image-security.html>), [Helm Security](</en/security/helm-security.html>), [Kubernetes Security](</en/security/kubernetes-security.html>)

**See also:** [Container Image Security](</en/security/container-image-security.html>), [Helm Security](</en/security/helm-security.html>), [Kubernetes Security](</en/security/kubernetes-security.html>)

**See also:** [Container Image Security](</en/security/container-image-security.html>), [Helm Security](</en/security/helm-security.html>), [Kubernetes Security](</en/security/kubernetes-security.html>)

**See also:** [Container Image Security](</en/security/container-image-security.html>), [Helm Security](</en/security/helm-security.html>), [Kubernetes Security](</en/security/kubernetes-security.html>)

**See also:** [Container Image Security](</en/security/container-image-security.html>), [Helm Security](</en/security/helm-security.html>), [Kubernetes Security](</en/security/kubernetes-security.html>)

**See also:** [Endpoint Security](</en/security/endpoint-security.html>), [Infrastructure as Code Security](</en/security/iac-security.html>), [Threat Hunting](</en/security/threat-hunting.html>)

**See also:** [Endpoint Security](</en/security/endpoint-security.html>), [Infrastructure as Code Security](</en/security/iac-security.html>), [Threat Hunting](</en/security/threat-hunting.html>)

**See also:** [Endpoint Security](</en/security/endpoint-security.html>), [Infrastructure as Code Security](</en/security/iac-security.html>), [Threat Hunting](</en/security/threat-hunting.html>)

**See also:** [Endpoint Security](</en/security/endpoint-security.html>), [Infrastructure as Code Security](</en/security/iac-security.html>), [Threat Hunting](</en/security/threat-hunting.html>)

**See also:** [Endpoint Security](</en/security/endpoint-security.html>), [Infrastructure as Code Security](</en/security/iac-security.html>), [Threat Hunting](</en/security/threat-hunting.html>)

**See also:** [Endpoint Security](</en/security/endpoint-security.html>), [Infrastructure as Code Security](</en/security/iac-security.html>), [Threat Hunting](</en/security/threat-hunting.html>)

**See also:** [Endpoint Security](</en/security/endpoint-security.html>), [Infrastructure as Code Security](</en/security/iac-security.html>), [Threat Hunting](</en/security/threat-hunting.html>)

**See also:** [Endpoint Security](</en/security/endpoint-security.html>), [Infrastructure as Code Security](</en/security/iac-security.html>), [Threat Hunting](</en/security/threat-hunting.html>)

**See also:** [Endpoint Security](</en/security/endpoint-security.html>), [Infrastructure as Code Security](</en/security/iac-security.html>), [Threat Hunting](</en/security/threat-hunting.html>)

**See also:** [Endpoint Security](</en/security/endpoint-security.html>), [Infrastructure as Code Security](</en/security/iac-security.html>), [Threat Hunting](</en/security/threat-hunting.html>)

**See also:** [Endpoint Security](</en/security/endpoint-security.html>), [Infrastructure as Code Security](</en/security/iac-security.html>), [Threat Hunting](</en/security/threat-hunting.html>)

**See also:** [Endpoint Security](</en/security/endpoint-security.html>), [Infrastructure as Code Security](</en/security/iac-security.html>), [Threat Hunting](</en/security/threat-hunting.html>)

**See also:** [Endpoint Security](</en/security/endpoint-security.html>), [Infrastructure as Code Security](</en/security/iac-security.html>), [Threat Hunting](</en/security/threat-hunting.html>)

**See also:** [Endpoint Security](</en/security/endpoint-security.html>), [Infrastructure as Code Security](</en/security/iac-security.html>), [Threat Hunting](</en/security/threat-hunting.html>)

**See also:** [Endpoint Security](</en/security/endpoint-security.html>), [Infrastructure as Code Security](</en/security/iac-security.html>), [Threat Hunting](</en/security/threat-hunting.html>)

**See also:** [Endpoint Security](</en/security/endpoint-security.html>), [Infrastructure as Code Security](</en/security/iac-security.html>), [Threat Hunting](</en/security/threat-hunting.html>)

**See also:** [Endpoint Security](</en/security/endpoint-security.html>), [Infrastructure as Code Security](</en/security/iac-security.html>), [Threat Hunting](</en/security/threat-hunting.html>)

**See also:** [Endpoint Security](</en/security/endpoint-security.html>), [Infrastructure as Code Security](</en/security/iac-security.html>), [Threat Hunting](</en/security/threat-hunting.html>)
