---
title: "IAM Audit"
description: "Performing effective IAM audits with permission reviews, unused role detection, and privilege escalation path analysis."
date: 2026-03-18
board: security
url: https://dingjiu1989-hue.github.io/en/security/iam-audit.html
---

# IAM Audit

IAM Audit Fundamentals 

Identity and Access Management (IAM) audits verify that users have appropriate permissions. Regular audits prevent privilege creep, detect unused roles, and identify security gaps. 

Permission Review 

Automate permission reviews across cloud providers: 

import boto3

import json

class IAMAuditor:

def **init**(self):

self.iam = boto3.client("iam")

def get_all_users_with_permissions(self):

users = []

paginator = self.iam.get_paginator("list_users")

for page in paginator.paginate():

for user in page["Users"]:

user_info = {

"username": user["UserName"],

"created": user["CreateDate"],

"policies": [],

"groups": [],

"last_used": None

}

## Inline policies

policies = self.iam.list_user_policies(UserName=user["UserName"])

user_info["policies"] = policies["PolicyNames"]

## Attached managed policies

attached = self.iam.list_attached_user_policies(UserName=user["UserName"])

user_info["managed_policies"] = [p["PolicyName"] for p in attached["AttachedPolicies"]]

## Groups

groups = self.iam.list_groups_for_user(UserName=user["UserName"])

user_info["groups"] = [g["GroupName"] for g in groups["Groups"]]

## Last activity

last_used = self.iam.get_user(UserName=user["UserName"])

if "PasswordLastUsed" in last_used["User"]:

user_info["last_used"] = last_used["User"]["PasswordLastUsed"]

users.append(user_info)

return users

Unused Role Detection 

def find_unused_roles(days_threshold=90):

cutoff = datetime.utcnow() - timedelta(days=days_threshold)

unused = []

paginator = client.get_paginator("list_roles")

for page in paginator.paginate():

for role in page["Roles"]:

if "LastUsedDate" not in role:

unused.append({

"role": role["RoleName"],

"created": role["CreateDate"],

"reason": "Never used"

})

elif role["LastUsedDate"] < cutoff:

unused.append({

"role": role["RoleName"],

"last_used": role["LastUsedDate"],

"reason": f"Not used in {days_threshold} days"

})

return unused

Privilege Escalation Path Analysis 

Identify paths where a user can grant themselves additional permissions: 

def analyze_escalation_paths(policy_document):

"""

Check if a policy allows privilege escalation.

"""

risks = []

statement = policy_document.get("Statement", [])

for stmt in statement:

actions = stmt.get("Action", [])

if isinstance(actions, str):

actions = [actions]

resource = stmt.get("Resource", "*")

## Check for IAM modify permissions

escalation_actions = [

"iam:CreatePolicy",

"iam:AttachUserPolicy",

"iam:PutUserPolicy",

"iam:CreateAccessKey",

"iam:UpdateAssumeRolePolicy",

"iam:PassRole"

]

for action in actions:

if any(action.endswith(esc_act.split(":")[1]) or action == "*" 

for esc_act in escalation_actions):

risks.append({

"risk": f"Privilege escalation via {action}",

"resource": resource

})

return risks

Audit Report Generation 

def generate_audit_report(findings):

report = {

"generated_at": datetime.utcnow().isoformat(),

"summary": {

"total_users": len(findings["users"]),

"unused_roles": len(findings["unused_roles"]),

"escalation_paths": len(findings["escalation_risks"]),

"over_permissioned": 0

},

"findings": findings

}

## Flag users with admin access who don't need it

for user in findings["users"]:

if "AdministratorAccess" in user.get("managed_policies", []):

if user.get("last_used") and \

(datetime.utcnow() - user["last_used"]).days > 30:

report["summary"]["over_permissioned"] += 1

return report

Remediation Workflow 

iam_audit_remediation:

critical:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- privilege_escalation_path: immediate_revoke

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- unused_admin_role: disable_within_24h

high:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- over_permissioned_user: reduce_to_least_privilege

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- unused_role_over_90_days: request_review

medium:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- missing_mfa: require_enrollment

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- no_password_rotation: enforce_policy

low:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- missing_tags: auto_tag

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- incomplete_documentation: notify_owner

Conclusion 

Regular IAM audits are essential for maintaining least privilege. Automate permission reviews, detect unused roles, and analyze privilege escalation paths. Generate actionable reports and enforce remediation SLAs. Audit at least quarterly, with automated scanning running continuously.

**See also:** [IAM: Identity and Access Management Fundamentals](</en/security/identity-access-management.html>), [EDR: Endpoint Detection and Response Solutions](</en/security/endpoint-detection-response.html>), [Cloud IAM Deep Dive](</en/security/cloud-iam.html>).

**See also:** [Cloud IAM Deep Dive](</en/security/cloud-iam.html>), [Threat Hunting](</en/security/threat-hunting.html>), [Container Runtime Security](</en/security/container-runtime-security.html>)

**See also:** [Cloud IAM Deep Dive](</en/security/cloud-iam.html>), [Threat Hunting](</en/security/threat-hunting.html>), [Container Runtime Security](</en/security/container-runtime-security.html>)

**See also:** [Cloud IAM Deep Dive](</en/security/cloud-iam.html>), [Threat Hunting](</en/security/threat-hunting.html>), [Container Runtime Security](</en/security/container-runtime-security.html>)

**See also:** [Cloud IAM Deep Dive](</en/security/cloud-iam.html>), [Threat Hunting](</en/security/threat-hunting.html>), [Container Runtime Security](</en/security/container-runtime-security.html>)

**See also:** [Cloud IAM Deep Dive](</en/security/cloud-iam.html>), [Threat Hunting](</en/security/threat-hunting.html>), [Container Runtime Security](</en/security/container-runtime-security.html>)

**See also:** [Security Awareness Training](</en/security/security-awareness.html>), [Vulnerability Management](</en/security/vulnerability-management.html>), [Zero Trust Implementation](</en/security/zero-trust-implementation.html>)

**See also:** [Security Awareness Training](</en/security/security-awareness.html>), [Vulnerability Management](</en/security/vulnerability-management.html>), [Zero Trust Implementation](</en/security/zero-trust-implementation.html>)

**See also:** [Security Awareness Training](</en/security/security-awareness.html>), [Vulnerability Management](</en/security/vulnerability-management.html>), [Zero Trust Implementation](</en/security/zero-trust-implementation.html>)

**See also:** [Security Awareness Training](</en/security/security-awareness.html>), [Vulnerability Management](</en/security/vulnerability-management.html>), [Zero Trust Implementation](</en/security/zero-trust-implementation.html>)

**See also:** [Security Awareness Training](</en/security/security-awareness.html>), [Vulnerability Management](</en/security/vulnerability-management.html>), [Zero Trust Implementation](</en/security/zero-trust-implementation.html>)

**See also:** [Security Awareness Training](</en/security/security-awareness.html>), [Vulnerability Management](</en/security/vulnerability-management.html>), [Zero Trust Implementation](</en/security/zero-trust-implementation.html>)

**See also:** [Security Awareness Training](</en/security/security-awareness.html>), [Vulnerability Management](</en/security/vulnerability-management.html>), [Zero Trust Implementation](</en/security/zero-trust-implementation.html>)
