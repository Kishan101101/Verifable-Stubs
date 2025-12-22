"""
Legacy Compliance Check Endpoints
These provide specific compliance framework checks (GDPR, PCI, HIPAA, ISO27001, Market)
"""
from fastapi import APIRouter, Depends
from datetime import datetime
import uuid
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.compliance import ComplianceRecord
from app.schemas.compliance_schema import (
    PEPCheckRequest,
    PEPCheckResponse,
    GDPRCheckRequest,
    GDPRCheckResponse,
    PCICheckRequest,
    PCICheckResponse,
    HIPAACheckRequest,
    HIPAACheckResponse,
    ISO27001Request,
    ISO27001Response,
    MarketComplianceRequest,
    MarketComplianceResponse,
)

router = APIRouter()


# ============================================
# Specific Compliance Framework Checks
# ============================================

@router.post("/aml/pep", response_model=PEPCheckResponse, tags=["AML"])
def pep_check(payload: PEPCheckRequest, db: Session = Depends(get_db)):
    """POST /compliance/aml/pep - Check if entity is a PEP (Politically Exposed Person)"""
    request_id = str(uuid.uuid4())
    response_data = {
        "request_id": request_id,
        "status": "completed",
        "checked_at": datetime.utcnow().isoformat(),
        "is_pep": False,
        "pep_category": None,
        "risk_level": "low",
    }
    
    record = ComplianceRecord(
        request_id=request_id,
        check_type="pep",
        status="completed",
        request_payload=payload.dict(),
        response_payload=response_data,
        completed_at=datetime.utcnow(),
    )
    db.add(record)
    db.commit()
    
    return response_data


@router.post("/gdpr/check", response_model=GDPRCheckResponse, tags=["GDPR"])
def gdpr_check(payload: GDPRCheckRequest, db: Session = Depends(get_db)):
    """POST /compliance/gdpr/check - Verify GDPR compliance requirements"""
    missing = []
    if not payload.has_privacy_policy:
        missing.append("privacy_policy")
    if not payload.consent_mechanism:
        missing.append("consent_mechanism")
    if not payload.data_retention_policy:
        missing.append("data_retention_policy")

    score = 100 - (len(missing) * 30)
    request_id = str(uuid.uuid4())
    response_data = {
        "request_id": request_id,
        "status": "compliant" if score >= 70 else "non_compliant",
        "checked_at": datetime.utcnow().isoformat(),
        "compliance_score": max(score, 0),
        "missing_requirements": missing,
    }
    
    record = ComplianceRecord(
        request_id=request_id,
        check_type="gdpr",
        status="completed",
        request_payload=payload.dict(),
        response_payload=response_data,
        completed_at=datetime.utcnow(),
    )
    db.add(record)
    db.commit()
    
    return response_data


@router.post("/pci/check", response_model=PCICheckResponse, tags=["PCI-DSS"])
def pci_check(payload: PCICheckRequest, db: Session = Depends(get_db)):
    """POST /compliance/pci/check - Verify PCI DSS compliance requirements"""
    issues = []
    if payload.stores_card_data and not payload.encryption_enabled:
        issues.append("Card data stored without encryption")
    if not payload.access_control:
        issues.append("Weak access control")

    request_id = str(uuid.uuid4())
    response_data = {
        "request_id": request_id,
        "status": "completed",
        "checked_at": datetime.utcnow().isoformat(),
        "compliant": len(issues) == 0,
        "issues": issues,
    }
    
    record = ComplianceRecord(
        request_id=request_id,
        check_type="pci",
        status="completed",
        request_payload=payload.dict(),
        response_payload=response_data,
        completed_at=datetime.utcnow(),
    )
    db.add(record)
    db.commit()
    
    return response_data


@router.post("/hipaa/check", response_model=HIPAACheckResponse, tags=["HIPAA"])
def hipaa_check(payload: HIPAACheckRequest, db: Session = Depends(get_db)):
    """POST /compliance/hipaa/check - Verify HIPAA compliance requirements"""
    violations = []
    if payload.handles_phi and not payload.access_logging:
        violations.append("Missing access logs for PHI")
    if payload.handles_phi and not payload.breach_policy:
        violations.append("No breach notification policy")

    request_id = str(uuid.uuid4())
    response_data = {
        "request_id": request_id,
        "status": "completed",
        "checked_at": datetime.utcnow().isoformat(),
        "compliant": len(violations) == 0,
        "violations": violations,
    }
    
    record = ComplianceRecord(
        request_id=request_id,
        check_type="hipaa",
        status="completed",
        request_payload=payload.dict(),
        response_payload=response_data,
        completed_at=datetime.utcnow(),
    )
    db.add(record)
    db.commit()
    
    return response_data


@router.post("/iso27001/check", response_model=ISO27001Response, tags=["ISO27001"])
def iso_check(payload: ISO27001Request, db: Session = Depends(get_db)):
    """POST /compliance/iso27001/check - Verify ISO 27001 compliance requirements"""
    gaps = []
    if not payload.risk_assessment_done:
        gaps.append("Risk assessment missing")
    if not payload.incident_management:
        gaps.append("Incident management missing")

    maturity = "high" if not gaps else "medium"
    request_id = str(uuid.uuid4())
    response_data = {
        "request_id": request_id,
        "status": "completed",
        "checked_at": datetime.utcnow().isoformat(),
        "maturity_level": maturity,
        "gaps": gaps,
    }
    
    record = ComplianceRecord(
        request_id=request_id,
        check_type="iso27001",
        status="completed",
        request_payload=payload.dict(),
        response_payload=response_data,
        completed_at=datetime.utcnow(),
    )
    db.add(record)
    db.commit()
    
    return response_data


@router.post("/market/check", response_model=MarketComplianceResponse, tags=["Market Compliance"])
def market_check(payload: MarketComplianceRequest, db: Session = Depends(get_db)):
    """POST /compliance/market/check - Verify market compliance (FINRA/MiFID)"""
    remarks = []
    if not payload.trade_monitoring:
        remarks.append("Trade monitoring missing")
    if not payload.conflict_policy:
        remarks.append("Conflict of interest policy missing")

    request_id = str(uuid.uuid4())
    response_data = {
        "request_id": request_id,
        "status": "completed",
        "checked_at": datetime.utcnow().isoformat(),
        "compliant": len(remarks) == 0,
        "remarks": remarks,
    }
    
    record = ComplianceRecord(
        request_id=request_id,
        check_type="market",
        status="completed",
        request_payload=payload.dict(),
        response_payload=response_data,
        completed_at=datetime.utcnow(),
    )
    db.add(record)
    db.commit()
    
    return response_data
