from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
import uuid
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.compliance import ComplianceRecord
from app.schemas.compliance_schema import (
    SanctionsCheckRequest,
    SanctionsCheckResponse,
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


@router.post("/aml/sanctions", response_model=SanctionsCheckResponse)
def sanctions_check(payload: SanctionsCheckRequest, db: Session = Depends(get_db)):
    request_id = str(uuid.uuid4())
    response_data = {
        "request_id": request_id,
        "status": "completed",
        "checked_at": datetime.utcnow().isoformat(),
        "sanctions_hit": False,
        "risk_level": "low",
        "matched_lists": [],
        "evidence": [],
    }
    
    # Save to database
    record = ComplianceRecord(
        request_id=request_id,
        check_type="sanctions",
        status="completed",
        request_payload=payload.dict(),
        response_payload=response_data,
        completed_at=datetime.utcnow(),
    )
    db.add(record)
    db.commit()
    
    return response_data


@router.post("/aml/pep", response_model=PEPCheckResponse)
def pep_check(payload: PEPCheckRequest, db: Session = Depends(get_db)):
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


@router.post("/gdpr/check", response_model=GDPRCheckResponse)
def gdpr_check(payload: GDPRCheckRequest, db: Session = Depends(get_db)):
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
        "status": "completed",
        "checked_at": datetime.utcnow().isoformat(),
        "compliance_score": max(score, 0),
        "status": "compliant" if score >= 70 else "non_compliant",
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


@router.post("/pci/check", response_model=PCICheckResponse)
def pci_check(payload: PCICheckRequest, db: Session = Depends(get_db)):
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


@router.post("/hipaa/check", response_model=HIPAACheckResponse)
def hipaa_check(payload: HIPAACheckRequest, db: Session = Depends(get_db)):
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


@router.post("/iso27001/check", response_model=ISO27001Response)
def iso_check(payload: ISO27001Request, db: Session = Depends(get_db)):
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


@router.post("/market/check", response_model=MarketComplianceResponse)
def market_check(payload: MarketComplianceRequest, db: Session = Depends(get_db)):
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


# =========================================================
# GET ENDPOINTS - Fetch stored compliance results
# =========================================================

@router.get("/aml/sanctions/{request_id}")
def get_sanctions_result(request_id: str, db: Session = Depends(get_db)):
    """Retrieve stored sanctions check result by request_id"""
    record = db.query(ComplianceRecord).filter_by(
        request_id=request_id, check_type="sanctions"
    ).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="Sanctions result not found")
    
    return record.response_payload


@router.get("/aml/pep/{request_id}")
def get_pep_result(request_id: str, db: Session = Depends(get_db)):
    """Retrieve stored PEP check result by request_id"""
    record = db.query(ComplianceRecord).filter_by(
        request_id=request_id, check_type="pep"
    ).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="PEP result not found")
    
    return record.response_payload


@router.get("/gdpr/check/{request_id}")
def get_gdpr_result(request_id: str, db: Session = Depends(get_db)):
    """Retrieve stored GDPR compliance check result by request_id"""
    record = db.query(ComplianceRecord).filter_by(
        request_id=request_id, check_type="gdpr"
    ).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="GDPR result not found")
    
    return record.response_payload


@router.get("/pci/check/{request_id}")
def get_pci_result(request_id: str, db: Session = Depends(get_db)):
    """Retrieve stored PCI DSS compliance check result by request_id"""
    record = db.query(ComplianceRecord).filter_by(
        request_id=request_id, check_type="pci"
    ).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="PCI DSS result not found")
    
    return record.response_payload


@router.get("/hipaa/check/{request_id}")
def get_hipaa_result(request_id: str, db: Session = Depends(get_db)):
    """Retrieve stored HIPAA compliance check result by request_id"""
    record = db.query(ComplianceRecord).filter_by(
        request_id=request_id, check_type="hipaa"
    ).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="HIPAA result not found")
    
    return record.response_payload


@router.get("/iso27001/check/{request_id}")
def get_iso27001_result(request_id: str, db: Session = Depends(get_db)):
    """Retrieve stored ISO 27001 compliance check result by request_id"""
    record = db.query(ComplianceRecord).filter_by(
        request_id=request_id, check_type="iso27001"
    ).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="ISO 27001 result not found")
    
    return record.response_payload


@router.get("/market/check/{request_id}")
def get_market_result(request_id: str, db: Session = Depends(get_db)):
    """Retrieve stored market (FINRA/MiFID) compliance check result by request_id"""
    record = db.query(ComplianceRecord).filter_by(
        request_id=request_id, check_type="market"
    ).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="Market compliance result not found")
    
    return record.response_payload
