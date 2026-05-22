---
title: "GDPR Technical Controls"
description: "Implementing GDPR technical controls for data mapping, consent management, right to deletion, and PIA."
date: 2026-03-17
board: security
url: https://aidev.fit/en/security/gdpr-technical.html
---

# GDPR Technical Controls

GDPR Technical Requirements 

GDPR requires technical controls for data protection by design and by default. Key areas include data mapping, consent, deletion, and privacy impact assessments. 

Data Mapping 

Maintain a comprehensive data inventory: 

class DataMappingService:

def **init**(self):

self.data_flows = []

def register_data_flow(self, flow):

self.data_flows.append({

"id": str(uuid.uuid4()),

"data_controller": flow["controller"],

"data_processor": flow.get("processor"),

"data_categories": flow["categories"],

"data_subjects": flow["subjects"],

"purpose": flow["purpose"],

"legal_basis": flow["legal_basis"],

"storage_location": flow["location"],

"retention_period": flow["retention"],

"transfers": flow.get("transfers", []),

"created_at": datetime.utcnow().isoformat()

})

def search_data_subject(self, subject_id):

"""Find all data related to a specific subject"""

results = []

for flow in self.data_flows:

if subject_id in flow["data_subjects"]:

results.append(flow)

return results

def generate_roppa_report(self):

"""Generate Record of Processing Activities"""

return {

"organization": "Example Corp",

"dpo": "privacy@example.com",

"processing_activities": self.data_flows,

"generated_at": datetime.utcnow().isoformat()

}

Consent Management 

Implement granular consent tracking: 

// Consent management API

class ConsentManager {

constructor() {

this.consentRecords = new Map();

}

recordConsent(userId, purposes) {

const record = {

userId,

purposes: purposes.map(p => ({

id: p.id,

granted: p.granted,

timestamp: new Date().toISOString(),

ip: p.ip,

userAgent: p.userAgent

})),

version: CONSENT_VERSION,

createdAt: new Date().toISOString()

};

this.consentRecords.set(userId, record);

this.auditLog('consent_recorded', { userId, purposes: p.id });

return record;

}

checkConsent(userId, purposeId) {

const record = this.consentRecords.get(userId);

if (!record) return false;

const purpose = record.purposes.find(p => p.id === purposeId);

return purpose?.granted === true && !this.isWithdrawn(userId, purposeId);

}

withdrawConsent(userId, purposeId) {

// Record withdrawal

this.consentRecords.get(userId)?.purposes.forEach(p => {

if (p.id === purposeId) {

p.granted = false;

p.withdrawnAt = new Date().toISOString();

}

});

// Trigger data deletion if necessary

this.deleteDataForPurpose(userId, purposeId);

}

auditLog(action, details) {

// Immutable audit log

console.log(JSON.stringify({

action,

details,

timestamp: new Date().toISOString()

}));

}

}

Right to Deletion 

Implement the right to be forgotten: 

class DeletionOrchestrator:

def **init**(self):

self.data_sources = []

def register_data_source(self, name, delete_func, retention_days=30):

self.data_sources.append({

"name": name,

"delete": delete_func,

"retention_days": retention_days

})

def delete_user_data(self, user_id):

results = []

errors = []

for source in self.data_sources:

try:

## Soft delete first

source["delete"](<user_id, soft=True>)

results.append({

"source": source["name"],

"status": "soft_deleted",

"retention_until": datetime.utcnow() + timedelta(

days=source["retention_days"]

)

})

except Exception as e:

errors.append({

"source": source["name"],

"error": str(e)

})

## Hard delete after retention period

schedule_hard_delete(user_id, self.data_sources)

return {

"user_id": user_id,

"soft_deletions": results,

"errors": errors,

"deletion_request_id": str(uuid.uuid4())

}

Privacy Impact Assessment 

## Automated PIA template

PIA_TEMPLATE = {

"project_name": "",

"data_flows": [],

"risk_assessment": {

"high_risk_indicators": [

"systematic_profiling",

"large_scale_processing",

"sensitive_data_processing",

"public_area_monitoring",

"cross_border_transfers"

],

"identified_risks": [],

"mitigations": []

},

"privacy_controls": {

"data_minimization": False,

"pseudonymization": False,

"encryption_at_rest": False,

"encryption_in_transit": False,

"access_controls": False,

"audit_logging": False

},

"recommendations": []

}

def conduct_pia(project_name, data_flows):

pia = copy.deepcopy(PIA_TEMPLATE)

pia["project_name"] = project_name

pia["data_flows"] = data_flows

## Auto-detect high risk indicators

for flow in data_flows:

if flow.get("sensitive_data"):

pia["risk_assessment"]["identified_risks"].append({

"flow": flow["name"],

"risk": "Sensitive data processing",

"likelihood": "medium",

"impact": "high"

})

return pia

Conclusion 

GDPR technical controls require systematic implementation. Maintain detailed data mapping, implement robust consent management, build capabilities for right to deletion, and conduct privacy impact assessments. Automate where possible and maintain comprehensive audit trails. Remember: privacy by design means building controls into your architecture from the start.

**See also:** [Privacy Engineering](</en/security/privacy-engineering.html>), [SOC 2 Technical Controls](</en/security/soc2-technical.html>), [Data Classification](</en/security/data-classification.html>).

**See also:** [Privacy Engineering](</en/security/privacy-engineering.html>), [SOC 2 Technical Controls](</en/security/soc2-technical.html>), [Data Masking and Redaction](</en/security/data-masking.html>)

**See also:** [Privacy Engineering](</en/security/privacy-engineering.html>), [SOC 2 Technical Controls](</en/security/soc2-technical.html>), [Data Masking and Redaction](</en/security/data-masking.html>)

**See also:** [Privacy Engineering](</en/security/privacy-engineering.html>), [SOC 2 Technical Controls](</en/security/soc2-technical.html>), [Data Masking and Redaction](</en/security/data-masking.html>)

**See also:** [Privacy Engineering](</en/security/privacy-engineering.html>), [SOC 2 Technical Controls](</en/security/soc2-technical.html>), [Data Masking and Redaction](</en/security/data-masking.html>)

**See also:** [Privacy Engineering](</en/security/privacy-engineering.html>), [SOC 2 Technical Controls](</en/security/soc2-technical.html>), [Data Masking and Redaction](</en/security/data-masking.html>)

**See also:** [Data Loss Prevention Strategies](</en/security/dlp-strategies.html>), [Software Signing](</en/security/software-signing.html>), [Encryption Key Management Best Practices](</en/security/encryption-key-management.html>)

**See also:** [Data Loss Prevention Strategies](</en/security/dlp-strategies.html>), [Software Signing](</en/security/software-signing.html>), [Encryption Key Management Best Practices](</en/security/encryption-key-management.html>)

**See also:** [Data Loss Prevention Strategies](</en/security/dlp-strategies.html>), [Software Signing](</en/security/software-signing.html>), [Encryption Key Management Best Practices](</en/security/encryption-key-management.html>)

**See also:** [Data Loss Prevention Strategies](</en/security/dlp-strategies.html>), [Software Signing](</en/security/software-signing.html>), [Encryption Key Management Best Practices](</en/security/encryption-key-management.html>)

**See also:** [Data Loss Prevention Strategies](</en/security/dlp-strategies.html>), [Software Signing](</en/security/software-signing.html>), [Encryption Key Management Best Practices](</en/security/encryption-key-management.html>)

**See also:** [Data Loss Prevention Strategies](</en/security/dlp-strategies.html>), [Software Signing](</en/security/software-signing.html>), [Encryption Key Management Best Practices](</en/security/encryption-key-management.html>)

**See also:** [Data Loss Prevention Strategies](</en/security/dlp-strategies.html>), [Software Signing](</en/security/software-signing.html>), [Encryption Key Management Best Practices](</en/security/encryption-key-management.html>)

**See also:** [Data Loss Prevention Strategies](</en/security/dlp-strategies.html>), [Software Signing](</en/security/software-signing.html>), [Encryption Key Management Best Practices](</en/security/encryption-key-management.html>)

**See also:** [Data Loss Prevention Strategies](</en/security/dlp-strategies.html>), [Software Signing](</en/security/software-signing.html>), [Encryption Key Management Best Practices](</en/security/encryption-key-management.html>)

**See also:** [Data Loss Prevention Strategies](</en/security/dlp-strategies.html>), [Software Signing](</en/security/software-signing.html>), [Encryption Key Management Best Practices](</en/security/encryption-key-management.html>)

**See also:** [Data Loss Prevention Strategies](</en/security/dlp-strategies.html>), [Software Signing](</en/security/software-signing.html>), [Encryption Key Management Best Practices](</en/security/encryption-key-management.html>)

**See also:** [Data Loss Prevention Strategies](</en/security/dlp-strategies.html>), [Software Signing](</en/security/software-signing.html>), [Encryption Key Management Best Practices](</en/security/encryption-key-management.html>)

**See also:** [Data Loss Prevention Strategies](</en/security/dlp-strategies.html>), [Software Signing](</en/security/software-signing.html>), [Encryption Key Management Best Practices](</en/security/encryption-key-management.html>)

**See also:** [Data Loss Prevention Strategies](</en/security/dlp-strategies.html>), [Software Signing](</en/security/software-signing.html>), [Encryption Key Management Best Practices](</en/security/encryption-key-management.html>)

**See also:** [Data Loss Prevention Strategies](</en/security/dlp-strategies.html>), [Software Signing](</en/security/software-signing.html>), [Encryption Key Management Best Practices](</en/security/encryption-key-management.html>)

**See also:** [Data Loss Prevention Strategies](</en/security/dlp-strategies.html>), [Software Signing](</en/security/software-signing.html>), [Encryption Key Management Best Practices](</en/security/encryption-key-management.html>)
