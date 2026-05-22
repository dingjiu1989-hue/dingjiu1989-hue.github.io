---
title: "Incident Response Playbook for Developers"
description: "Practical incident response using the NIST framework: preparation, detection, containment, eradication, recovery, and post-mortems."
date: 2026-03-04
board: security
url: https://aidev.fit/en/security/incident-response.html
---

# Incident Response Playbook for Developers

Incident response is the structured process of handling security breaches and cyber attacks. Every development team needs a plan, because it is not a matter of if an incident will happen, but when. This article presents a practical incident response playbook based on the NIST SP 800-61 framework.

## The NIST Incident Response Framework

The NIST framework defines four phases: Preparation, Detection and Analysis, Containment Eradication and Recovery, and Post-Incident Activity. We add a fifth phase, Triage, between Detection and Containment.

## Phase 1: Preparation

Preparation is the most important phase. Without preparation, every incident becomes a chaotic scramble.

**Build a response team** : Identify who handles security incidents. The team should include a incident commander, a security analyst, a system owner, a communications lead, and a legal representative.

**Create runbooks** : Document step-by-step procedures for common incident types: phishing, malware outbreak, data breach, ransomware, denial of service, and insider threat.

**Set up tooling** : Ensure the team has access to:

  * Centralized logging (SIEM like Splunk, ELK, or Sentinel)

  * Endpoint detection and response (EDR like CrowdStrike or Defender)

  * Network monitoring and packet capture

  * Secure communication channels (Slack, Teams, or Signal)

  * Evidence collection tools (FTK Imager, Volatility, tcpdump)




**Practice regularly** : Run tabletop exercises every quarter. Simulate a ransomware attack, a data exposure, or a compromised credential. Practice builds muscle memory.

## Phase 2: Detection and Analysis

Detection relies on monitoring and alerting. Every alert is a potential incident candidate.

**Alert sources** :

  * SIEM correlation rules detecting anomalous patterns

  * EDR alerts for malware execution or suspicious process behavior

  * Cloud provider alerts (GuardDuty, Security Command Center, Defender)

  * Application logs showing unusual error rates or access patterns

  * User reports of suspicious activity




**Triage questions** :

  * What happened? What systems are affected?

  * When did it start? Is it ongoing?

  * What is the impact? Data loss? Service disruption?

  * Is this a true positive or a false alarm?

  * What severity level applies?




**Severity classification** :

  * SEV-1: Critical. Active data exfiltration, ransomware, or service-wide compromise. Immediate response required.

  * SEV-2: High. Confirmed intrusion but contained. Credential compromise affecting multiple users.

  * SEV-3: Medium. Potential compromise under investigation. Phishing campaign targeting employees.

  * SEV-4: Low. Minor policy violations. Automated scans with no evidence of exploitation.




## Phase 3: Containment, Eradication, and Recovery

Containment stops the attack from spreading. Eradication removes the attacker's presence. Recovery returns systems to normal operation.

**Short-term containment** :

  * Disconnect affected systems from the network.

  * Disable compromised user accounts.

  * Block attacker IP addresses at the firewall.

  * Rotate credentials for affected services.




## Example: Block an IP at the firewall

iptables -A INPUT -s 203.0.113.50 -j DROP

## Example: Disable a compromised AWS IAM user

aws iam update-access-key \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--access-key-id AKIAIOSFODNN7EXAMPLE \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--status Inactive \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--user-name compromised-user

**Long-term containment** :

  * Apply security patches.

  * Implement additional monitoring for affected systems.

  * Deploy WAF rules to block attack patterns.




**Eradication** :

  * Remove malware using EDR tools.

  * Rebuild compromised servers from known-good images.

  * Revoke all session tokens and API keys.

  * Reset root passwords and privileged credentials.




**Recovery** :

  * Restore systems from clean backups.

  * Verify system integrity before returning to production.

  * Gradually reintroduce traffic while monitoring for recurrence.

  * Communicate recovery status to stakeholders.




## Phase 4: Post-Incident Activity

The post-mortem is where the team learns from the incident and improves processes.

**Post-mortem meeting** : Within one week of containment, gather everyone involved. Blameless culture is essential — the goal is to improve systems, not assign blame.

**Post-mortem document** :

  * Timeline of the incident

  * Root cause analysis

  * What went well and what went wrong

  * Detection gaps and containment delays

  * Remediation items with owners and deadlines

  * Changes to runbooks, tooling, or architecture




## Post-Mortem: Service Credential Leak

**Date** : 2026-04-15

**Severity** : SEV-2

## Timeline

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- 2026-04-15 09:23 UTC — GuardDuty alert for anomalous API calls

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- 09:25 — Triage begins

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- 09:45 — Compromised key identified and revoked

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- 10:30 — Containment confirmed

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- 14:00 — All affected resources rotated

## Root Cause

GitHub Actions workflow accidentally logged AWS_SECRET_ACCESS_KEY to debug output. Logs were publicly accessible.

## Action Items

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- [ ] Remove debug logging from CI/CD workflows (owner: DevOps, due: 04-22)

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- [ ] Enable secret scanning on GitHub repository (owner: Security, due: 04-18)

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- [ ] Add alert for API keys used outside expected regions (owner: Platform, due: 04-30)

## Forensic Evidence Collection

Proper evidence collection preserves data for legal action and root cause analysis.

  * Capture memory dumps using tools like LiME or Volatility before powering off systems.

  * Collect disk images using `dd` or FTK Imager rather than copying files live.

  * Record command output with timestamps using the `script` command.

  * Maintain chain of custody documentation for all evidence.




## Capture memory dump with LiME

insmod lime.ko "path=/evidence/memory.dump format=lime"

## Capture disk image

dd if=/dev/sda of=/evidence/disk.img bs=4M conv=noerror,sync

## Conclusion

A well-practiced incident response process turns a potential disaster into a manageable event. Preparation separates professional teams from those that panic. Detection without response is just noise. And every incident, no matter how small, is an opportunity to improve.

**See also:** [Incident Response Plan](</en/security/incident-response-plan.html>), [XSRF/CSRF Protection Guide](</en/security/xsrf-csrf-protection.html>), [OAuth 2.0 and PKCE Explained](</en/security/oauth2-pkce.html>).

**See also:** [Incident Response Plan](</en/security/incident-response-plan.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>), [OAuth 2.0 and PKCE Explained](</en/security/oauth2-pkce.html>)

**See also:** [Incident Response Plan](</en/security/incident-response-plan.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>), [OAuth 2.0 and PKCE Explained](</en/security/oauth2-pkce.html>)

**See also:** [Incident Response Plan](</en/security/incident-response-plan.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>), [OAuth 2.0 and PKCE Explained](</en/security/oauth2-pkce.html>)

**See also:** [Incident Response Plan](</en/security/incident-response-plan.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>), [OAuth 2.0 and PKCE Explained](</en/security/oauth2-pkce.html>)

**See also:** [Incident Response Plan](</en/security/incident-response-plan.html>), [API Gateway Security Patterns](</en/security/api-gateway-security.html>), [OAuth 2.0 and PKCE Explained](</en/security/oauth2-pkce.html>)

**See also:** [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>), [Threat Intelligence: Gathering and Applying Intel](</en/security/threat-intelligence.html>)

**See also:** [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>), [Threat Intelligence: Gathering and Applying Intel](</en/security/threat-intelligence.html>)

**See also:** [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>), [Threat Intelligence: Gathering and Applying Intel](</en/security/threat-intelligence.html>)

**See also:** [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>), [Threat Intelligence: Gathering and Applying Intel](</en/security/threat-intelligence.html>)

**See also:** [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>), [Threat Intelligence: Gathering and Applying Intel](</en/security/threat-intelligence.html>)

**See also:** [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>), [Threat Intelligence: Gathering and Applying Intel](</en/security/threat-intelligence.html>)

**See also:** [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>), [Threat Intelligence: Gathering and Applying Intel](</en/security/threat-intelligence.html>)

**See also:** [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>), [Threat Intelligence: Gathering and Applying Intel](</en/security/threat-intelligence.html>)

**See also:** [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>), [Threat Intelligence: Gathering and Applying Intel](</en/security/threat-intelligence.html>)

**See also:** [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>), [Threat Intelligence: Gathering and Applying Intel](</en/security/threat-intelligence.html>)

**See also:** [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>), [Threat Intelligence: Gathering and Applying Intel](</en/security/threat-intelligence.html>)

**See also:** [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>), [Threat Intelligence: Gathering and Applying Intel](</en/security/threat-intelligence.html>)

**See also:** [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>), [Threat Intelligence: Gathering and Applying Intel](</en/security/threat-intelligence.html>)

**See also:** [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>), [Threat Intelligence: Gathering and Applying Intel](</en/security/threat-intelligence.html>)

**See also:** [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>), [Threat Intelligence: Gathering and Applying Intel](</en/security/threat-intelligence.html>)

**See also:** [DevSecOps: Integrating Security into CI/CD](</en/security/devsecops-pipeline.html>), [Security Auditing and Compliance Frameworks](</en/security/security-auditing.html>), [Threat Intelligence: Gathering and Applying Intel](</en/security/threat-intelligence.html>)
