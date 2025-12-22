import asyncio
import logging
from datetime import datetime, date
from sqlalchemy.orm import Session
from app.core.database import get_session_local, get_engine, Base
from app.models.compliance import Regulation, FraudPattern, SanctionsEntry

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_data():
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        logger.info("Starting database seeding...")

        # 1. Seed Regulations
        regulations = [
            {
                "regulation_id": "REG-GDPR-001",
                "name": "General Data Protection Regulation",
                "code": "GDPR",
                "category": "Data Privacy",
                "jurisdiction": "European Union",
                "version": "2016/679",
                "effective_date": date(2018, 5, 25),
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
            },
            {
                "regulation_id": "REG-KYC-001",
                "name": "KYC/AML - FATF 40 Recommendations",
                "code": "KYC-AML",
                "category": "Financial Compliance",
                "jurisdiction": "International",
                "version": "2023",
                "effective_date": date(2023, 1, 1),
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
            },
            {
                "regulation_id": "REG-HIPAA-001",
                "name": "Health Insurance Portability and Accountability Act",
                "code": "HIPAA",
                "category": "Healthcare Privacy",
                "jurisdiction": "United States",
                "version": "1996",
                "effective_date": date(1996, 8, 21),
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
            },
            {
                "regulation_id": "REG-SOX-001",
                "name": "Sarbanes-Oxley Act",
                "code": "SOX",
                "category": "Financial Reporting",
                "jurisdiction": "United States",
                "version": "2002",
                "effective_date": date(2002, 7, 30),
                "description": "US federal law that set new or expanded requirements for all US public company boards, management and public accounting firms.",
                "key_articles": [
                    {"section": "302", "title": "Corporate Responsibility for Financial Reports"},
                    {"section": "404", "title": "Management Assessment of Internal Controls"}
                ],
                "tags": ["finance", "audit", "us"]
            },
            {
                "regulation_id": "REG-PCI-001",
                "name": "Payment Card Industry Data Security Standard",
                "code": "PCI-DSS",
                "category": "Payment Security",
                "jurisdiction": "International",
                "version": "4.0",
                "description": "Information security standard for organizations that handle branded credit cards from the major card schemes.",
                "key_articles": [
                    {"requirement": "3", "title": "Protect stored cardholder data"},
                    {"requirement": "4", "title": "Encrypt transmission of cardholder data"}
                ],
                "tags": ["payment", "security", "pci"]
            },
            {
                "regulation_id": "REG-MED-001",
                "name": "General Medical Credentialing Standards",
                "code": "MED-CRED",
                "category": "Healthcare Compliance",
                "jurisdiction": "United States",
                "description": "Standards for verifying the qualifications of healthcare professionals.",
                "key_articles": [
                    {"standard": "PSV_001", "title": "Primary Source Verification (PSV)"},
                    {"standard": "GAP_ANALYSIS_002", "title": "Work History and Gap Analysis"}
                ],
                "tags": ["healthcare", "credentialing", "medical"]
            },
            {
                "regulation_id": "REG-VENDOR-001",
                "name": "Vendor Onboarding Compliance Requirements",
                "code": "VENDOR-ONB",
                "category": "Vendor Management",
                "jurisdiction": "Global",
                "description": "Requirements and standards for onboarding new vendors and third-party partners.",
                "key_articles": [
                    {"section": "1", "title": "KYC/AML Requirements for Vendor Onboarding"},
                    {"section": "2", "title": "Vendor Document Quality and Authenticity Standards"}
                ],
                "tags": ["vendor", "onboarding", "compliance"]
            }
        ]

        for reg_data in regulations:
            existing = db.query(Regulation).filter(Regulation.regulation_id == reg_data["regulation_id"]).first()
            if not existing:
                reg = Regulation(**reg_data)
                db.add(reg)
                logger.info(f"Added regulation: {reg_data['name']}")

        # 2. Seed Fraud Patterns
        patterns = [
            {
                "pattern_id": "FRAUD-ID-001",
                "name": "Identity Theft Indicators",
                "category": "Identity Fraud",
                "description": "Common indicators and methods used in identity theft.",
                "indicators": [
                    "Multiple applications using same identity",
                    "Inconsistent personal information",
                    "Recent address changes without verification",
                    "Mismatched biometric data"
                ],
                "risk_score_threshold": 85
            },
            {
                "pattern_id": "FRAUD-DOC-001",
                "name": "Document Tampering Detection",
                "category": "Document Fraud",
                "description": "Physical and digital indicators of document manipulation.",
                "indicators": [
                    "Inconsistent fonts or sizes",
                    "Misaligned text or graphics",
                    "Metadata inconsistencies",
                    "Pixelation or compression artifacts"
                ],
                "risk_score_threshold": 90
            },
            {
                "pattern_id": "FRAUD-SYN-001",
                "name": "Synthetic Identity Fraud",
                "category": "Identity Fraud",
                "description": "Identity built from a combination of real and fake information.",
                "indicators": [
                    "Legitimate SSN with fake name",
                    "Employment at non-existent companies",
                    "Credit history built slowly over time",
                    "Sudden large purchases"
                ],
                "risk_score_threshold": 95
            },
            {
                "pattern_id": "FRAUD-AML-001",
                "name": "Money Laundering Patterns",
                "category": "Financial Fraud",
                "description": "Common patterns used in money laundering stages.",
                "indicators": [
                    "Large cash deposits inconsistent with income",
                    "Frequent structured transactions",
                    "Complex transaction chains",
                    "Sudden wealth without clear source"
                ],
                "risk_score_threshold": 90
            },
            {
                "pattern_id": "FRAUD-MED-001",
                "name": "Healthcare Billing Fraud",
                "category": "Medical Fraud",
                "description": "Patterns of fraudulent medical billing and identity theft.",
                "indicators": [
                    "Upcoding (billing for higher level of service)",
                    "Unbundling (billing separately for bundled services)",
                    "Phantom billing (billing for services not performed)",
                    "Medical identity theft"
                ],
                "risk_score_threshold": 85
            }
        ]

        for pattern_data in patterns:
            existing = db.query(FraudPattern).filter(FraudPattern.pattern_id == pattern_data["pattern_id"]).first()
            if not existing:
                pattern = FraudPattern(**pattern_data)
                db.add(pattern)
                logger.info(f"Added fraud pattern: {pattern_data['name']}")

        # 3. Seed Sanctions Entries
        sanctions = [
            {
                "entry_id": "SANC-OFAC-001",
                "list_type": "OFAC-SDN",
                "name": "AL-QA'IDA",
                "aliases": ["AL-QAEDA", "THE BASE"],
                "entity_type": "Organization",
                "country": "AF",
                "program": "SDGT",
                "reason": "Terrorism financing; Global security threat",
                "additional_info": {
                    "identifiers": [{"type": "Tax ID", "value": "123456789"}],
                    "source_url": "https://sanctionssearch.ofac.treas.gov/"
                }
            },
            {
                "entry_id": "SANC-PEP-001",
                "list_type": "PEP",
                "name": "John Doe",
                "aliases": ["J. Doe"],
                "entity_type": "Individual",
                "country": "US",
                "program": "PEP-US",
                "reason": "High-ranking government official",
                "additional_info": {
                    "identifiers": [{"type": "Passport", "value": "A1234567"}],
                    "source_url": "Internal PEP Database"
                }
            }
        ]

        for sanc_data in sanctions:
            existing = db.query(SanctionsEntry).filter(SanctionsEntry.entry_id == sanc_data["entry_id"]).first()
            if not existing:
                sanc = SanctionsEntry(**sanc_data)
                db.add(sanc)
                logger.info(f"Added sanctions entry: {sanc_data['name']}")

        db.commit()
        logger.info("Database seeding completed successfully!")

    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
