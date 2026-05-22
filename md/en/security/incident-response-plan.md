---
title: "Incident Response Plan"
description: "Building an incident response plan using the NIST framework with tabletop exercises and communication strategies."
date: 2026-03-18
board: security
url: https://aidev.fit/en/security/incident-response-plan.html
---

# Incident Response Plan

The NIST Framework 

The NIST SP 800-61 framework defines four phases of incident response: Preparation, Detection & Analysis, Containment Eradication & Recovery, and Post-Incident Activity. 

Phase 1: Preparation 

Preparation determines response success. Key elements include: 

## incident-response-tools.yaml

tools:

siem: elastic-security

edr: crowdstrike-falcon

ticketing: jira-servicedesk

communication: slack + pagerduty

playbooks:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- ransomware.md

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- data-breach.md

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- ddos.md

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- insider-threat.md

team:

incident_commander: rotate weekly

security_analyst: tier-1/tier-2

legal: on-call

communications: PR team

Phase 2: Detection and Analysis 

Detect incidents through multiple signals: 

import json

from datetime import datetime, timedelta

class IncidentDetector:

def **init**(self):

self.correlation_rules = []

def add_rule(self, rule):

self.correlation_rules.append(rule)

def evaluate(self, events):

alerts = []

for rule in self.correlation_rules:

matching = [e for e in events if rule["condition"](<e>)]

if len(matching) >= rule["threshold"]:

alerts.append({

"rule": rule["name"],

"severity": rule["severity"],

"events": matching,

"timestamp": datetime.utcnow().isoformat()

})

return alerts

## Example: Correlate failed logins across accounts

detector = IncidentDetector()

detector.add_rule({

"name": "Brute Force Detection",

"condition": lambda e: e["type"] == "failed_login",

"threshold": 10,

"severity": "high",

"window": timedelta(minutes=5)

})

Phase 3: Containment, Eradication, Recovery 

## !/bin/bash

## Incident containment script

isolate_host() {

local host=$1

## Block at network level

ansible-playbook isolate_host.yml -e "target=$host"

## Capture forensic data

ssh "user@$host" "tar czf /tmp/forensics.tar.gz /var/log /tmp /home"

scp "user@$host:/tmp/forensics.tar.gz" ./evidence/

## Snapshot for analysis

aws ec2 create-snapshot --volume-id $(get_volume_id $host)

echo "Host $host isolated. Forensic data captured."

}

## Eradicate malware

eradicate() {

local host=$1

ansible-playbook malware_removal.yml -e "target=$host"

verify_clean $host && restore_from_clean_backup $host

}

Communication Plan 

Clear communication channels are critical: 

incident_communication:

internal:

slacks:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- channel: "#security-alerts"

purpose: "Real-time technical coordination"

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- channel: "#incident-comm"

purpose: "Executive updates"

email: incident-response@company.com

external:

legal_review: required before all external communication

breach_notification:

timeline: 72_hours

template: breach_notification_template.md

regulatory:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: "ICO"

jurisdiction: "UK"

notification_url: "https://ico.org.uk/breach"

Tabletop Exercises 

Run quarterly tabletops to test the plan: 

Scenario: Ransomware on critical database server

Inject 1: Encrypted files detected at 09:00

Question: Who declares the incident?

Inject 2: Attacker demands 5 BTC

Question: Do we pay? Who decides?

Inject 3: Backup restoration fails

Question: What is the fallback?

Post-Incident Activity 

Conduct thorough post-mortems: 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Track incident metrics

SELECT incident_type, 

AVG(EXTRACT(EPOCH FROM (contained_at - detected_at))) as avg_containment_time,

AVG(EXTRACT(EPOCH FROM (resolved_at - detected_at))) as avg_resolution_time

FROM incidents

WHERE created_at > NOW() - INTERVAL '1 year'

GROUP BY incident_type;

Conclusion 

A well-rehearsed incident response plan reduces breach impact by 50% or more. Invest in preparation, run regular tabletop exercises, automate containment where possible, and learn from every incident.
