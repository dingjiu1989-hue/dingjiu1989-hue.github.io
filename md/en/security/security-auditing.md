---
title: "Security Auditing and Compliance Frameworks"
description: "Overview of SOC 2, ISO 27001, PCI DSS, HIPAA compliance frameworks and how to collect audit evidence for continuous compliance."
date: 2026-03-05
board: security
url: https://dingjiu1989-hue.github.io/en/security/security-auditing.html
---

# Security Auditing and Compliance Frameworks

Security auditing is the systematic evaluation of an organization's security controls against established standards. Compliance with frameworks like SOC 2, ISO 27001, PCI DSS, and HIPAA demonstrates to customers and regulators that security is taken seriously. This article covers the major frameworks, audit evidence collection, and continuous compliance strategies.

## Major Compliance Frameworks

## SOC 2 (Service Organization Control 2)

SOC 2 is designed for service organizations that store customer data. It is based on five Trust Service Criteria:

  * **Security** : The system is protected against unauthorized access. This is the only mandatory criterion.



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Availability** : The system is available for operation and use as committed.

3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Processing Integrity** : System processing is complete, valid, accurate, and authorized.

4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Confidentiality** : Confidential information is protected.

5\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Privacy** : Personal information is collected, used, retained, and disclosed in accordance with commitments.

SOC 2 has two report types:

  * **Type I** : Reports on the design of controls at a specific point in time.

  * **Type II** : Reports on the operating effectiveness of controls over a period (typically 6-12 months).




SOC 2 is common among SaaS companies, cloud service providers, and data processors.

## ISO 27001

ISO 27001 is an international standard for information security management systems (ISMS). It specifies requirements for establishing, implementing, maintaining, and continually improving an ISMS.

**Key requirements** :

  * Clause 4: Context of the organization

  * Clause 5: Leadership and commitment

  * Clause 6: Planning (risk assessment and treatment)

  * Clause 7: Support (resources, competence, awareness, communication)

  * Clause 8: Operation (risk treatment plan, controls)

  * Clause 9: Performance evaluation (monitoring, measurement, internal audit)

  * Clause 10: Improvement (nonconformity, corrective action)




Annex A controls cover 93 controls across four domains: Organizational, People, Physical, and Technological.

## PCI DSS (Payment Card Industry Data Security Standard)

PCI DSS applies to any organization that stores, processes, or transmits credit card data. The standard has 12 requirements across six goals:

  * Build and maintain a secure network (firewalls, secure configurations).



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Protect cardholder data (encryption at rest and in transit).

3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Maintain a vulnerability management program (antivirus, secure coding, patching).

4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Implement strong access control measures (least privilege, unique IDs, physical security).

5\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Regularly monitor and test networks (logging, scanning, penetration testing).

6\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Maintain an information security policy.

PCI DSS compliance levels depend on transaction volume. Merchants processing over 6 million transactions annually require an annual on-site assessment by a Qualified Security Assessor (QSA).

## HIPAA (Health Insurance Portability and Accountability Act)

HIPAA applies to healthcare providers, health plans, and healthcare clearinghouses. It has two main rules:

  * **Privacy Rule** : Protects individually identifiable health information (PHI). Defines permitted uses and disclosures.

  * **Security Rule** : Requires administrative, physical, and technical safeguards for electronic PHI (ePHI).




**HIPAA Security Rule safeguards** :

  * Administrative: Risk analysis, workforce training, contingency planning.

  * Physical: Facility access controls, workstation security, device and media controls.

  * Technical: Access control, audit controls, integrity controls, transmission security.




## Audit Evidence Collection

Auditors require evidence that controls are operating effectively. Evidence must be objective, verifiable, and sufficient.

## Types of Evidence

  * **Configuration screenshots** : Evidence of properly configured security settings.

  * **Log files** : System, application, and security logs showing monitoring and access controls.

  * **Policy documents** : Written policies and procedures.

  * **Training records** : Evidence of security awareness training completion.

  * **Change management records** : Approvals, testing, and deployment documentation.

  * **Access review records** : Quarterly or annual access certification results.

  * **Vulnerability scan reports** : Scheduled and on-demand scan results.

  * **Incident response records** : Documented incidents and post-mortems.




## Evidence Collection Automation

Manual evidence collection is time-consuming and error-prone. Automation tools collect evidence continuously and respond to auditor requests instantly.

## Automated evidence collection for SOC 2

def collect_iam_evidence():

"""Collect IAM-related evidence for SOC 2 audit."""

evidence = {

"collection_date": datetime.utcnow().isoformat(),

"controls": {}

}

## Evidence: MFA is enabled for all console users

evidence["controls"]["mfa_enabled"] = {

"status": check_mfa_enforcement(),

"sample_size": count_active_users(),

"compliance_pct": calculate_mfa_compliance()

}

## Evidence: Access keys are rotated within 90 days

evidence["controls"]["key_rotation"] = {

"status": check_key_rotation_compliance(90),

"expired_keys": find_expired_access_keys(90)

}

## Evidence: Inactive accounts are disabled

evidence["controls"]["inactive_accounts"] = {

"status": check_inactive_accounts(90),

"disabled_count": disable_inactive_accounts(90)

}

return evidence

## Continuous Compliance Tools

  * **AWS Audit Manager** : Continuously collects evidence against AWS-managed frameworks.

  * **GCP Assured Workloads** : Automates compliance controls for regulated workloads.

  * **Azure Policy** : Enforces and audits compliance with built-in initiative definitions.

  * **Turbot / CloudQuery** : Open-source platforms for cloud compliance and asset inventory.

  * **Vanta / Drata / Secureframe** : Continuous compliance platforms that automate evidence collection and auditor collaboration.




## Building a Compliance Program

## Step 1: Scope Definition

Define what systems, data, and processes are in scope. A SOC 2 audit might scope to the production environment, while excluding internal IT systems.

## Step 2: Gap Analysis

Assess current controls against framework requirements. Identify gaps and create remediation plans.

gap_analysis:

framework: "SOC 2 Security Criterion"

cc_6_1:

description: "Logical access security controls"

current_state: "MFA enabled for console, not for API"

gap: "API access keys lack MFA requirement"

remediation: "Implement IAM access key MFA or key rotation policy"

owner: "DevOps Team"

deadline: "2026-06-30"

## Step 3: Control Implementation

Implement the controls identified in the gap analysis. Prioritize based on risk and compliance requirements.

## Step 4: Evidence Collection

Begin collecting evidence for each control. Automate where possible. Organize evidence by control ID for easy auditor access.

## Step 5: Internal Audit

Conduct a pre-audit assessment. Review evidence completeness, test control effectiveness, and fix any findings before the external audit.

## Step 6: External Audit

Auditors will request evidence, conduct interviews, and perform testing. Cooperate fully and respond promptly to requests. Preparation is the key to a smooth audit.

## Managing Multiple Frameworks

Organizations often need to comply with multiple frameworks. A unified compliance approach maps common controls across frameworks:

common_controls:

access_reviews:

soc_2: "CC6.1, CC6.2"

iso_27001: "A.9.2.5, A.9.2.6"

pci_dss: "7.2.1, 8.1.4"

hipaa: "164.312(a)(1)"

encryption_at_rest:

soc_2: "CC6.7"

iso_27001: "A.10.1.1"

pci_dss: "3.4, 3.6"

hipaa: "164.312(a)(2)(iv), 164.312(e)(2)(ii)"

This common control mapping allows teams to implement one control that satisfies multiple frameworks, reducing duplication and audit fatigue.

## Conclusion

Compliance is not security, but well-designed compliance programs significantly improve security posture. Choose the right framework for your business (SOC 2 for SaaS, PCI DSS for payments, HIPAA for healthcare, ISO 27001 for international credibility), automate evidence collection, and maintain continuous compliance rather than scrambling before annual audits.

**See also:** [Security Compliance Automation: SOC 2, ISO 27001, HIPAA Tools](</en/security/security-compliance-tools.html>), [Security Log Management](</en/security/log-management-security.html>), [Blockchain and Smart Contract Security](</en/security/blockchain-security.html>).

**See also:** [Security Compliance Automation: SOC 2, ISO 27001, HIPAA Tools](</en/security/security-compliance-tools.html>), [Security Log Management](</en/security/log-management-security.html>), [Blockchain and Smart Contract Security](</en/security/blockchain-security.html>)

**See also:** [Security Compliance Automation: SOC 2, ISO 27001, HIPAA Tools](</en/security/security-compliance-tools.html>), [Security Log Management](</en/security/log-management-security.html>), [Blockchain and Smart Contract Security](</en/security/blockchain-security.html>)

**See also:** [Security Compliance Automation: SOC 2, ISO 27001, HIPAA Tools](</en/security/security-compliance-tools.html>), [Security Log Management](</en/security/log-management-security.html>), [Blockchain and Smart Contract Security](</en/security/blockchain-security.html>)

**See also:** [Security Compliance Automation: SOC 2, ISO 27001, HIPAA Tools](</en/security/security-compliance-tools.html>), [Security Log Management](</en/security/log-management-security.html>), [Blockchain and Smart Contract Security](</en/security/blockchain-security.html>)

**See also:** [Security Compliance Automation: SOC 2, ISO 27001, HIPAA Tools](</en/security/security-compliance-tools.html>), [Security Log Management](</en/security/log-management-security.html>), [Blockchain and Smart Contract Security](</en/security/blockchain-security.html>)

**See also:** [Zero Trust Architecture for Startups](</en/security/zero-trust-architecture.html>), [Cloud Security Basics: Shared Responsibility Model Explained](</en/security/cloud-security-basics.html>), [Incident Response Playbook for Developers](</en/security/incident-response.html>)

**See also:** [Zero Trust Architecture for Startups](</en/security/zero-trust-architecture.html>), [Cloud Security Basics: Shared Responsibility Model Explained](</en/security/cloud-security-basics.html>), [Incident Response Playbook for Developers](</en/security/incident-response.html>)

**See also:** [Zero Trust Architecture for Startups](</en/security/zero-trust-architecture.html>), [Cloud Security Basics: Shared Responsibility Model Explained](</en/security/cloud-security-basics.html>), [Incident Response Playbook for Developers](</en/security/incident-response.html>)

**See also:** [Zero Trust Architecture for Startups](</en/security/zero-trust-architecture.html>), [Cloud Security Basics: Shared Responsibility Model Explained](</en/security/cloud-security-basics.html>), [Incident Response Playbook for Developers](</en/security/incident-response.html>)
