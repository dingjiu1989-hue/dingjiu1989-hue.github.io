---
title: "Threat Modeling"
description: "Threat modeling methodologies including STRIDE, DREAD, PASTA, attack trees, and practical tooling."
date: 2026-03-19
board: security
url: https://dingjiu1989-hue.github.io/en/security/threat-modeling.html
---

# Threat Modeling

Why Threat Model? 

Threat modeling identifies potential security issues during design, when they are cheapest to fix. It shifts security left and builds protection into architecture. 

STRIDE Methodology 

Microsoft's STRIDE categorizes threats: 

| Category | Definition | Example | |----------|------------|---------| | Spoofing | Impersonating someone | Fake login page | | Tampering | Modifying data | Altering database records | | Repudiation | Denying actions | Missing audit logs | | Information Disclosure | Exposing data | SQL injection | | Denial of Service | Disrupting service | DDoS attack | | Elevation of Privilege | Gaining unauthorized access | Buffer overflow | 

## STRIDE threat analysis

def analyze_with_stride(component, data_flow):

threats = []

## Spoofing

if not component.get("authentication"):

threats.append({

"category": "Spoofing",

"threat": f"Attacker could impersonate {component['name']}",

"mitigation": "Implement mutual TLS authentication"

})

## Tampering

if not data_flow.get("integrity_check"):

threats.append({

"category": "Tampering",

"threat": f"Data in {data_flow['name']} could be modified",

"mitigation": "Use message signing or HMAC"

})

## Information Disclosure

if not data_flow.get("encryption"):

threats.append({

"category": "Information Disclosure",

"threat": f"Data in {data_flow['name']} could be intercepted",

"mitigation": "Encrypt data in transit with TLS"

})

return threats

DREAD Risk Rating 

DREAD helps prioritize threats: 

def dread_rating(threat):

scores = {

"damage": threat["damage_potential"], # 1-10

"reproducibility": threat["reproducibility"], # 1-10

"exploitability": threat["exploitability"], # 1-10

"affected_users": threat["affected_users"], # 1-10

"discoverability": threat["discoverability"] # 1-10

}

total = sum(scores.values())

rating = total / 5

if rating >= 7:

return "Critical"

elif rating >= 4:

return "High"

elif rating >= 2:

return "Medium"

else:

return "Low"

PASTA Methodology 

Process for Attack Simulation and Threat Analysis (PASTA) has seven stages: 

pasta_stages:

1: "Define business and security objectives"

2: "Define technical scope"

3: "Application decomposition"

4: "Threat analysis"

5: "Vulnerability analysis"

6: "Attack modeling"

7: "Risk and impact analysis"

stage_4_threat_analysis:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- technique: "Create threat tree for each asset"

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- example:

asset: "User database"

threats:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- "SQL injection via search endpoint"

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- "Insider threat with direct DB access"

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- "Unencrypted backup compromise"

Attack Trees 

Model attacker goals and paths: 

class AttackTreeNode:

def **init**(self, name, description, children=None):

self.name = name

self.description = description

self.children = children or []

self.mitigations = []

def add_child(self, node):

self.children.append(node)

return self

def add_mitigation(self, mitigation):

self.mitigations.append(mitigation)

return self

## Example: Attack tree for credential theft

root = AttackTreeNode(

"Steal User Credentials",

"Attacker goal: acquire valid credentials"

)

root.add_child(AttackTreeNode(

"Phishing Attack",

"Send convincing phishing email"

).add_child(AttackTreeNode(

"Clone legitimate site",

"Create replica of login page"

)))

root.add_child(AttackTreeNode(

"Credential Stuffing",

"Use leaked credentials from other breaches"

))

root.add_child(AttackTreeNode(

"Keylogging",

"Install malware to capture keystrokes"

).add_child(AttackTreeNode(

"Drive-by download",

"Exploit browser vulnerability"

)))

Threat Modeling Tools 

## Microsoft Threat Modeling Tool

## OWASP Threat Dragon

## PyTM - Pythonic threat modeling

## Example: PyTM model

from pytm import TM, Server, Dataflow, Boundary

tm = TM("Web Application")

internet = Boundary("Internet")

web_server = Server("Web Server")

database = Server("Database")

web_server.inBoundary = internet

request = Dataflow(web_server, database, "SQL Query")

request.protocol = "TCP"

request.data = "SQL Query"

tm.process()

Integration with Development 

## Threat modeling in CI

threat_modeling_pipeline:

triggers:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- new_feature_creation

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- architecture_change

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- third_party_integration

automated_checks:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- data_flow_diagram_required

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- trust_boundaries_defined

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- authentication_documented

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- authorization_model_defined

review_gates:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- critical_threats: must_have_mitigation

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- high_threats: must_have_mitigation_or_acceptance

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- medium_threats: reviewed_and_documented

Conclusion 

Threat modeling is an essential security practice. Use STRIDE for threat identification, DREAD for prioritization, and PASTA for comprehensive analysis. Build attack trees to explore attacker paths. Integrate threat modeling into your development lifecycle. Automate where possible but maintain human oversight for design-level analysis. The goal is to find and fix security issues before they reach production.

**See also:** [Threat Hunting](</en/security/threat-hunting.html>), [Bug Bounty Guide](</en/security/bug-bounty.html>), [DNS Security](</en/security/dns-security.html>).

**See also:** [Bug Bounty Guide](</en/security/bug-bounty.html>), [DNS Security](</en/security/dns-security.html>), [SOC Operations](</en/security/soc-operations.html>)

**See also:** [Bug Bounty Guide](</en/security/bug-bounty.html>), [DNS Security](</en/security/dns-security.html>), [SOC Operations](</en/security/soc-operations.html>)

**See also:** [Bug Bounty Guide](</en/security/bug-bounty.html>), [DNS Security](</en/security/dns-security.html>), [SOC Operations](</en/security/soc-operations.html>)

**See also:** [Bug Bounty Guide](</en/security/bug-bounty.html>), [DNS Security](</en/security/dns-security.html>), [SOC Operations](</en/security/soc-operations.html>)

**See also:** [Bug Bounty Guide](</en/security/bug-bounty.html>), [DNS Security](</en/security/dns-security.html>), [SOC Operations](</en/security/soc-operations.html>)

**See also:** [TLS Configuration Guide](</en/security/tls-configuration.html>), [Web Application Firewall Implementation](</en/security/waf-implementation.html>), [Container Runtime Security](</en/security/container-runtime-security.html>)

**See also:** [TLS Configuration Guide](</en/security/tls-configuration.html>), [Web Application Firewall Implementation](</en/security/waf-implementation.html>), [Container Runtime Security](</en/security/container-runtime-security.html>)

**See also:** [TLS Configuration Guide](</en/security/tls-configuration.html>), [Web Application Firewall Implementation](</en/security/waf-implementation.html>), [Container Runtime Security](</en/security/container-runtime-security.html>)

**See also:** [TLS Configuration Guide](</en/security/tls-configuration.html>), [Web Application Firewall Implementation](</en/security/waf-implementation.html>), [Container Runtime Security](</en/security/container-runtime-security.html>)

**See also:** [TLS Configuration Guide](</en/security/tls-configuration.html>), [Web Application Firewall Implementation](</en/security/waf-implementation.html>), [Container Runtime Security](</en/security/container-runtime-security.html>)

**See also:** [TLS Configuration Guide](</en/security/tls-configuration.html>), [Web Application Firewall Implementation](</en/security/waf-implementation.html>), [Container Runtime Security](</en/security/container-runtime-security.html>)

**See also:** [TLS Configuration Guide](</en/security/tls-configuration.html>), [Web Application Firewall Implementation](</en/security/waf-implementation.html>), [Container Runtime Security](</en/security/container-runtime-security.html>)

**See also:** [TLS Configuration Guide](</en/security/tls-configuration.html>), [Web Application Firewall Implementation](</en/security/waf-implementation.html>), [Container Runtime Security](</en/security/container-runtime-security.html>)

**See also:** [TLS Configuration Guide](</en/security/tls-configuration.html>), [Web Application Firewall Implementation](</en/security/waf-implementation.html>), [Container Runtime Security](</en/security/container-runtime-security.html>)

**See also:** [TLS Configuration Guide](</en/security/tls-configuration.html>), [Web Application Firewall Implementation](</en/security/waf-implementation.html>), [Container Runtime Security](</en/security/container-runtime-security.html>)

**See also:** [TLS Configuration Guide](</en/security/tls-configuration.html>), [Web Application Firewall Implementation](</en/security/waf-implementation.html>), [Container Runtime Security](</en/security/container-runtime-security.html>)

**See also:** [TLS Configuration Guide](</en/security/tls-configuration.html>), [Web Application Firewall Implementation](</en/security/waf-implementation.html>), [Container Runtime Security](</en/security/container-runtime-security.html>)

**See also:** [TLS Configuration Guide](</en/security/tls-configuration.html>), [Web Application Firewall Implementation](</en/security/waf-implementation.html>), [Container Runtime Security](</en/security/container-runtime-security.html>)
