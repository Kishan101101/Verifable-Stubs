# External Compliance & Verification API - Mock Data

This document contains mock data for the External Compliance & Verification API. You can use these JSON objects to test the API endpoints or seed your database.

## 1. Regulations (`/regulations`)

### GDPR (General Data Protection Regulation)
```json
{
  "regulation_id": "REG-GDPR-001",
  "name": "General Data Protection Regulation",
  "code": "GDPR",
  "category": "Data Privacy",
  "jurisdiction": "European Union",
  "version": "2016/679",
  "effective_date": "2018-05-25",
  "description": "The General Data Protection Regulation (GDPR) is a regulation in EU law on data protection and privacy in the European Union and the European Economic Area.",
  "required_fields": ["data_subject_consent", "purpose_limitation", "data_minimization"],
  "key_articles": [
    {"article": "5", "title": "Principles relating to processing of personal data"},
    {"article": "6", "title": "Lawfulness of processing"},
    {"article": "32", "title": "Security of processing"}
  ],
  "compliance_checklist": [
    "Obtain explicit consent",
    "Implement data encryption",
    "Appoint a Data Protection Officer (DPO)",
    "Maintain processing records"
  ],
  "tags": ["privacy", "eu", "data-protection"]
}
```

### KYC/AML (Know Your Customer / Anti-Money Laundering)
```json
{
  "regulation_id": "REG-KYC-001",
  "name": "KYC/AML - FATF 40 Recommendations",
  "code": "KYC-AML",
  "category": "Financial Compliance",
  "jurisdiction": "International",
  "version": "2023",
  "effective_date": "2023-01-01",
  "description": "International standards for combating money laundering and the financing of terrorism and proliferation.",
  "required_fields": ["customer_id", "beneficial_owner", "source_of_funds"],
  "key_articles": [
    {"recommendation": "10", "title": "Customer due diligence"},
    {"recommendation": "11", "title": "Record-keeping"}
  ],
  "compliance_checklist": [
    "Verify customer identity",
    "Identify beneficial owners",
    "Screen against sanctions lists",
    "Monitor transactions for suspicious activity"
  ],
  "tags": ["finance", "aml", "kyc", "fatf"]
}
```

### HIPAA (Health Insurance Portability and Accountability Act)
```json
{
  "regulation_id": "REG-HIPAA-001",
  "name": "Health Insurance Portability and Accountability Act",
  "code": "HIPAA",
  "category": "Healthcare Privacy",
  "jurisdiction": "United States",
  "version": "1996",
  "effective_date": "1996-08-21",
  "description": "US federal law that required the creation of national standards to protect sensitive patient health information from being disclosed without the patient's consent or knowledge.",
  "required_fields": ["phi_protection", "access_control", "audit_logs"],
  "key_articles": [
    {"rule": "Privacy Rule", "section": "Protected Health Information (PHI)"},
    {"rule": "Security Rule", "section": "Administrative, Physical, and Technical Safeguards"}
  ],
  "compliance_checklist": [
    "Ensure confidentiality of e-PHI",
    "Protect against anticipated threats",
    "Train workforce on security",
    "Implement access controls"
  ],
  "tags": ["healthcare", "privacy", "us", "phi"]
}
```

## 2. Fraud Patterns (`/fraud/patterns`)

### Identity Theft
```json
{
  "pattern_id": "FRAUD-ID-001",
  "pattern_name": "Identity Theft Indicators",
  "category": "Identity Fraud",
  "description": "Common indicators and methods used in identity theft.",
  "indicators": [
    "Multiple applications using same identity",
    "Inconsistent personal information",
    "Recent address changes without verification",
    "Mismatched biometric data"
  ],
  "risk_score": 85,
  "is_active": true
}
```

### Document Tampering
```json
{
  "pattern_id": "FRAUD-DOC-001",
  "pattern_name": "Document Tampering Detection",
  "category": "Document Fraud",
  "description": "Physical and digital indicators of document manipulation.",
  "indicators": [
    "Inconsistent fonts or sizes",
    "Misaligned text or graphics",
    "Metadata inconsistencies",
    "Pixelation or compression artifacts"
  ],
  "risk_score": 90,
  "is_active": true
}
```

### Synthetic Identity
```json
{
  "pattern_id": "FRAUD-SYN-001",
  "pattern_name": "Synthetic Identity Fraud",
  "category": "Identity Fraud",
  "description": "Identity built from a combination of real and fake information.",
  "indicators": [
    "Legitimate SSN with fake name",
    "Employment at non-existent companies",
    "Credit history built slowly over time",
    "Sudden large purchases"
  ],
  "risk_score": 95,
  "is_active": true
}
```

## 3. Sanctions Entries (`/sanctions/lists/{list_type}/entries`)

### OFAC SDN Entry Example
```json
{
  "entry_id": "SANC-OFAC-001",
  "list_type": "OFAC-SDN",
  "name": "AL-QA'IDA",
  "aliases": ["AL-QAEDA", "THE BASE"],
  "entity_type": "Organization",
  "country": "AF",
  "program": "SDGT",
  "identifiers": [{"type": "Tax ID", "value": "123456789"}],
  "reasons": ["Terrorism financing", "Global security threat"],
  "source_url": "https://sanctionssearch.ofac.treas.gov/"
}
```

### PEP (Politically Exposed Person) Example
```json
{
  "entry_id": "SANC-PEP-001",
  "list_type": "PEP",
  "name": "John Doe",
  "aliases": ["J. Doe"],
  "entity_type": "Individual",
  "country": "US",
  "program": "PEP-US",
  "identifiers": [{"type": "Passport", "value": "A1234567"}],
  "reasons": ["High-ranking government official"],
  "source_url": "Internal PEP Database"
}
```
