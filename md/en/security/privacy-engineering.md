---
title: "Privacy Engineering"
description: "Guide to privacy engineering covering privacy by design principles, data mapping, Privacy Impact Assessments (PIA), and consent management."
date: 2026-03-12
board: security
url: https://aidev.fit/en/security/privacy-engineering.html
---

# Privacy Engineering

Introduction 

Privacy engineering integrates data protection principles into system architecture from the earliest design stages. Rather than treating privacy as an afterthought or compliance checkbox, privacy engineering embeds controls into the fabric of software systems. This approach aligns with the "privacy by design" framework and regulatory requirements like GDPR and CCPA. 

Privacy by Design 

Privacy by Design (PbD) is a framework developed by the Information and Privacy Commissioner of Ontario, articulated through seven foundational principles. 

The Seven Principles 

  * **Proactive not Reactive** : Prevent privacy risks from occurring, not remediate after the fact

2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Privacy as Default** : Personal data is automatically protected without user action 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Privacy Embedded into Design** : Privacy is integral to the system, not bolted on 4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Full Functionality** : Privacy does not sacrifice functionality — positive-sum, not zero-sum 5\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **End-to-End Security** : Full lifecycle protection from collection to destruction 6\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Visibility and Transparency** : Processes are open, accountable, and auditable 7\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Respect for User Privacy** : User-centric design with strong defaults and clear notices 

## Privacy by design: data minimization example

class UserRegistrationService:

def register_minimal(self, email, password):

"""Collect only necessary data (Principle 3: Data Minimization)."""

return User(

email=email,

password_hash=self.hash_password(password),

## Don't collect: phone, address, birthday, etc.

created_at=datetime.utcnow()

)

def set_default_privacy(self, user):

"""Privacy as default: opt-in for data sharing (Principle 2)."""

user.privacy_settings = PrivacySettings(

share_analytics=False, # Default: not shared

share_profile=False, # Default: not shared

email_marketing=False, # Default: not subscribed

data_retention_days=90 # Default: minimal retention

)

return user

Data Mapping 

Data mapping identifies what personal data is collected, where it flows, how it is processed, and who has access. It is the foundation of any privacy program. 

from dataclasses import dataclass

from enum import Enum

from typing import List, Dict

class DataCategory(Enum):

PERSONAL_IDENTIFIABLE = "PII"

FINANCIAL = "FINANCIAL"

HEALTH = "HEALTH"

BIOMETRIC = "BIOMETRIC"

BEHAVIORAL = "BEHAVIORAL"

LOCATION = "LOCATION"

COMMUNICATION = "COMMUNICATION"

class ProcessingPurpose(Enum):

ACCOUNT_MGMT = "account_management"

ANALYTICS = "analytics"

MARKETING = "marketing"

FRAUD_DETECTION = "fraud_detection"

LEGAL_COMPLIANCE = "legal_compliance"

@dataclass

class DataFlow:

source: str

destination: str

data_elements: List[str]

categories: List[DataCategory]

purposes: List[ProcessingPurpose]

legal_basis: str

retention_days: int

encryption: bool

third_party_sharing: bool

class DataMapper:

def **init**(self):

self.data_flows = []

def add_flow(self, flow: DataFlow):

"""Register a data flow in the mapping."""

self.data_flows.append(flow)

def generate_roda(self):

"""Generate Record of Processing Activities (GDPR Art. 30)."""

roda = []

for flow in self.data_flows:

roda.append({

'purpose': [p.value for p in flow.purposes],

'data_categories': [c.value for c in flow.categories],

'data_elements': flow.data_elements,

'data_subjects': flow.source,

'recipients': flow.destination,

'third_country_transfers': flow.third_party_sharing,

'retention_period': f"{flow.retention_days} days",

'security_measures': {

'encryption_at_rest': flow.encryption,

'encryption_in_transit': True,

'access_controls': 'role_based',

}

})

return roda

Privacy Impact Assessment (PIA) 

A PIA systematically evaluates how a project or system affects individual privacy. 

class PrivacyImpactAssessment:

def **init**(self, project_name, data_processor):

self.project_name = project_name

self.processor = data_processor

self.risks = []

self.mitigations = []

def assess_data_collection(self, data_flow: DataFlow):

"""Assess whether data collection is necessary and proportional."""

findings = []

## Necessity check

if DataCategory.LOCATION in data_flow.categories:

necessity = False

for purpose in data_flow.purposes:

if purpose in (ProcessingPurpose.ACCOUNT_MGMT, 

ProcessingPurpose.FRAUD_DETECTION):

necessity = True

break

if not necessity:

findings.append({

'risk': 'Unnecessary location data collection',

'severity': 'HIGH',

'remediation': 'Remove location collection or add justification'

})

## Minimization check

if len(data_flow.data_elements) > 10:

findings.append({

'risk': 'Excessive data collection',

'severity': 'MEDIUM',

'remediation': 'Review each data element for necessity'

})

return findings

def generate_report(self):

"""Generate structured PIA report."""

return {

'project': self.project_name,

'assessment_date': datetime.utcnow().isoformat(),

'data_flows_analyzed': len(self.processor.data_flows),

'risks_identified': len(self.risks),

'mitigations_proposed': len(self.mitigations),

'residual_risk': self._calculate_residual_risk(),

'recommendation': self._get_recommendation(),

}

Consent Management 

Consent management systems track user consent preferences and enforce them across data processing activities. 

class ConsentManager:

def **init**(self, storage_backend):

self.storage = storage_backend

CONSENT_TYPES = {

'essential': {

'required': True,

'purpose': 'Website functionality',

'cookies': ['session', 'csrf']

},

'analytics': {

'required': False,

'purpose': 'Usage analysis and improvement',

'cookies': ['_ga', '_gid']

},

'marketing': {

'required': False,

'purpose': 'Personalized advertising',

'cookies': ['_fbp', 'ads_prefs']

},

'functional': {

'required': False,

'purpose': 'Enhanced features and preferences',

'cookies': ['lang_pref', 'theme']

}

}

def record_consent(self, user_id, consent_preferences, ip_address):

"""Record granular consent preferences."""

consent_record = {

'user_id': user_id,

'timestamp': datetime.utcnow().isoformat(),

'preferences': consent_preferences,

'ip_address': ip_address,

'user_agent': request.user_agent,

'consent_version': '2.1'

}

self.storage.store(f"consent:{user_id}", consent_record)

return consent_record

def check_consent(self, user_id, consent_type):

"""Check if user has granted specific consent."""

record = self.storage.retrieve(f"consent:{user_id}")

if not record:

return False

consent_config = self.CONSENT_TYPES.get(consent_type)

if consent_config and consent_config['required']:

return True # Essential consent is always active

return record['preferences'].get(consent_type, False)

def withdraw_consent(self, user_id, consent_type=None):

"""Withdraw consent (specific type or all)."""

record = self.storage.retrieve(f"consent:{user_id}")

if consent_type:

record['preferences'][consent_type] = False

record['withdrawn_at'] = datetime.utcnow().isoformat()

else:

for ctype in record['preferences']:

record['preferences'][ctype] = False

record['all_withdrawn_at'] = datetime.utcnow().isoformat()

self.storage.store(f"consent:{user_id}", record)

Conclusion 

Privacy engineering requires embedding privacy controls into the design and architecture of systems, not layering them on afterward. Implement data mapping to understand data flows, conduct PIAs for high-risk processing, build consent management that respects user choice, and apply data minimization as a default. Privacy is a engineering discipline — treat it with the same rigor as security or performance engineering.
