---
title: "SOC Operations"
description: "Practical guide to Security Operations Center operations including tier model, SIEM tuning, playbooks, KPIs, and shift handoff procedures."
date: 2026-03-13
board: security
url: https://aidev.fit/en/security/soc-operations.html
---

# SOC Operations

Introduction 

A Security Operations Center (SOC) is a centralized team responsible for monitoring, detecting, analyzing, and responding to security incidents. Building an effective SOC requires structured processes, skilled personnel, appropriate tools, and continuous improvement. 

SOC Tier Model 

The SOC team structure typically follows a three-tier model that provides clear career progression and escalation paths. 

Tier 1 — Triage 

Tier 1 analysts monitor dashboards, triage alerts, and determine initial severity. They handle known false positives and escalate suspicious events to Tier 2. 

Responsibilities:

  * Monitor SIEM dashboards and alert queues

  * Perform initial alert triage and categorization

  * Execute basic investigation steps per playbooks

  * Create tickets for escalated incidents

  * Maintain shift logs




## Tier 1 triage automation example

def triage_alert(alert):

## Check against known false positive patterns

for fp_pattern in false_positive_patterns:

if fp_pattern.matches(alert):

alert.auto_close()

return

## Enrich with threat intelligence

alert.iocs = enrich_iocs(alert.extract_iocs())

## Escalate if critical

if alert.severity == 'critical':

alert.assign_tier(2)

alert.notify('pagerduty')

else:

alert.assign_tier(2, queue='standard')

Tier 2 — Investigation 

Tier 2 analysts perform deep investigation, containment, and remediation. They correlate data from multiple sources and determine the full scope of incidents. 

Responsibilities:

  * Deep-dive analysis of escalated alerts

  * Host and network forensic analysis

  * Malware triage and reverse engineering

  * Incident containment and remediation

  * Playbook refinement




Tier 3 — Advanced Analysis 

Tier 3 analysts handle the most complex incidents, develop detection rules, perform threat hunting, and conduct post-incident reviews. 

Responsibilities:

  * Advanced malware analysis and reverse engineering

  * Threat hunt development and execution

  * SIEM content development and tuning

  * Red/purple team collaboration

  * Incident review and lessons learned




SIEM Tuning 

SIEM tuning reduces noise while maintaining detection coverage. A well-tuned SIEM generates alerts that analysts can actually investigate. 

## Example: correlation rule tuning cycle

SIEM_ALERTS=10000

FALSE_POSITIVES=8500

TRUE_POSITIVES=1000

ESCALATIONS=500

echo "Alert volume: $SIEM_ALERTS"

echo "False positive rate: $((FALSE_POSITIVES * 100 / SIEM_ALERTS))%"

echo "Escalation rate: $((ESCALATIONS * 100 / SIEM_ALERTS))%"

Playbooks 

Playbooks provide step-by-step instructions for handling specific scenarios. They reduce mean time to respond (MTTR) and ensure consistency. 

## Incident response playbook example

playbook:

id: IR-001

name: "Ransomware Detection and Response"

severity: critical

steps:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- phase: identification

actions:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- task: "Verify alert from EDR or user report"

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- task: "Identify affected systems"

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- task: "Determine ransomware variant via IOC hash"

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- phase: containment

actions:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- task: "Isolate affected hosts from network"

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- task: "Disable compromised accounts"

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- task: "Block C2 infrastructure at firewall"

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- phase: eradication

actions:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- task: "Remove malware from affected systems"

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- task: "Patch vulnerability used for initial access"

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- task: "Reset credentials for affected accounts"

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- phase: recovery

actions:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- task: "Restore from clean backups"

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- task: "Verify system integrity"

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- task: "Gradually restore connectivity"

SOC KPIs 

Key performance indicators measure SOC effectiveness and efficiency. 

| KPI | Target | Measurement | |-----|--------|-------------| | Mean Time to Detect (MTTD) | < 1 hour | Time from compromise to detection | | Mean Time to Respond (MTTR) | < 4 hours | Time from detection to containment | | Alert Triage Time | < 15 minutes | Time to categorize initial alert | | False Positive Rate | < 30% | False alerts / total alerts | | Escalation Rate | 5-15% | Escalated alerts / total alerts | | Coverage Gap | < 5% | Unmonitored assets / total assets | 

Shift Handoff 

Effective shift handoffs prevent incidents from falling through the cracks. 

shift_handoff:

sections:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: "Active Incidents"

fields: [id, severity, status, owner, summary, next_steps]

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: "Pending Investigations"

fields: [alert_id, initial_findings, pending_actions]

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: "Maintenance and Outages"

fields: [system, type, eta, impact]

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: "Notable Events"

fields: [timestamp, description, action_taken]

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: "Tool Status"

fields: [tool, status, known_issues]

Conclusion 

A well-structured SOC combines skilled personnel, documented processes, and appropriate technology. Focus on reducing alert fatigue through continuous tuning, maintaining comprehensive playbooks, measuring performance with meaningful KPIs, and ensuring smooth shift transitions.

**See also:** [Security Metrics and Reporting](</en/security/security-metrics.html>), [Bug Bounty Guide](</en/security/bug-bounty.html>), [DNS Security](</en/security/dns-security.html>).

**See also:** [Bug Bounty Guide](</en/security/bug-bounty.html>), [DNS Security](</en/security/dns-security.html>), [Security Metrics and Reporting](</en/security/security-metrics.html>)

**See also:** [Bug Bounty Guide](</en/security/bug-bounty.html>), [DNS Security](</en/security/dns-security.html>), [Security Metrics and Reporting](</en/security/security-metrics.html>)

**See also:** [Bug Bounty Guide](</en/security/bug-bounty.html>), [DNS Security](</en/security/dns-security.html>), [Security Metrics and Reporting](</en/security/security-metrics.html>)

**See also:** [Bug Bounty Guide](</en/security/bug-bounty.html>), [DNS Security](</en/security/dns-security.html>), [Security Metrics and Reporting](</en/security/security-metrics.html>)

**See also:** [Bug Bounty Guide](</en/security/bug-bounty.html>), [DNS Security](</en/security/dns-security.html>), [Security Metrics and Reporting](</en/security/security-metrics.html>)

**See also:** [Container Image Security](</en/security/container-image-security.html>), [Content Security Policy](</en/security/content-security-policy.html>), [CORS Security](</en/security/cors-security.html>)

**See also:** [Container Image Security](</en/security/container-image-security.html>), [Content Security Policy](</en/security/content-security-policy.html>), [CORS Security](</en/security/cors-security.html>)

**See also:** [Container Image Security](</en/security/container-image-security.html>), [Content Security Policy](</en/security/content-security-policy.html>), [CORS Security](</en/security/cors-security.html>)

**See also:** [Container Image Security](</en/security/container-image-security.html>), [Content Security Policy](</en/security/content-security-policy.html>), [CORS Security](</en/security/cors-security.html>)

**See also:** [Container Image Security](</en/security/container-image-security.html>), [Content Security Policy](</en/security/content-security-policy.html>), [CORS Security](</en/security/cors-security.html>)

**See also:** [Container Image Security](</en/security/container-image-security.html>), [Content Security Policy](</en/security/content-security-policy.html>), [CORS Security](</en/security/cors-security.html>)

**See also:** [Container Image Security](</en/security/container-image-security.html>), [Content Security Policy](</en/security/content-security-policy.html>), [CORS Security](</en/security/cors-security.html>)

**See also:** [Container Image Security](</en/security/container-image-security.html>), [Content Security Policy](</en/security/content-security-policy.html>), [CORS Security](</en/security/cors-security.html>)

**See also:** [Container Image Security](</en/security/container-image-security.html>), [Content Security Policy](</en/security/content-security-policy.html>), [CORS Security](</en/security/cors-security.html>)

**See also:** [Container Image Security](</en/security/container-image-security.html>), [Content Security Policy](</en/security/content-security-policy.html>), [CORS Security](</en/security/cors-security.html>)

**See also:** [Container Image Security](</en/security/container-image-security.html>), [Content Security Policy](</en/security/content-security-policy.html>), [CORS Security](</en/security/cors-security.html>)

**See also:** [Container Image Security](</en/security/container-image-security.html>), [Content Security Policy](</en/security/content-security-policy.html>), [CORS Security](</en/security/cors-security.html>)

**See also:** [Container Image Security](</en/security/container-image-security.html>), [Content Security Policy](</en/security/content-security-policy.html>), [CORS Security](</en/security/cors-security.html>)

**See also:** [Container Image Security](</en/security/container-image-security.html>), [Content Security Policy](</en/security/content-security-policy.html>), [CORS Security](</en/security/cors-security.html>)

**See also:** [Container Image Security](</en/security/container-image-security.html>), [Content Security Policy](</en/security/content-security-policy.html>), [CORS Security](</en/security/cors-security.html>)

**See also:** [Container Image Security](</en/security/container-image-security.html>), [Content Security Policy](</en/security/content-security-policy.html>), [CORS Security](</en/security/cors-security.html>)
