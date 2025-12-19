"""
Backward compatibility shim: re-export the router from the
`app.routes.compliance` module so old imports continue to work.
"""

from app.routes.compliance import router as router


@router.post("/aml/sanctions", response_model=SanctionsCheckResponse)
def demo_sanctions_check(payload: SanctionsCheckRequest):
    return {
        "request_id": str(uuid.uuid4()),
        "status": "completed",
        "checked_at": datetime.utcnow().isoformat(),
        "sanctions_hit": False,
        "risk_level": "low",
        "matched_lists": [],
        "evidence": [],
    }


@router.post("/aml/pep", response_model=PEPCheckResponse)
def demo_pep_check(payload: PEPCheckRequest):
    return {
        "request_id": str(uuid.uuid4()),
        "status": "completed",
        "checked_at": datetime.utcnow().isoformat(),
        "is_pep": False,
        "pep_category": None,
        "risk_level": "low",
    }


@router.post("/gdpr/check", response_model=GDPRCheckResponse)
def demo_gdpr_check(payload: GDPRCheckRequest):
    missing = []
    if not payload.has_privacy_policy:
        missing.append("privacy_policy")
    if not payload.consent_mechanism:
        missing.append("consent_mechanism")
    if not payload.data_retention_policy:
        missing.append("data_retention_policy")

    score = 100 - (len(missing) * 30)

    return {
        "request_id": str(uuid.uuid4()),
        "status": "completed",
        "checked_at": datetime.utcnow().isoformat(),
        "compliance_score": max(score, 0),
        "status": "compliant" if score >= 70 else "non_compliant",
        "missing_requirements": missing,
    }


@router.post("/pci/check", response_model=PCICheckResponse)
def demo_pci_check(payload: PCICheckRequest):
    issues = []
    if payload.stores_card_data and not payload.encryption_enabled:
        issues.append("Card data stored without encryption")
    if not payload.access_control:
        issues.append("Weak access control")

    return {
        "request_id": str(uuid.uuid4()),
        "status": "completed",
        "checked_at": datetime.utcnow().isoformat(),
        "compliant": len(issues) == 0,
        "issues": issues,
    }


@router.post("/hipaa/check", response_model=HIPAACheckResponse)
def demo_hipaa_check(payload: HIPAACheckRequest):
    violations = []
    if payload.handles_phi and not payload.access_logging:
        violations.append("Missing access logs for PHI")
    if payload.handles_phi and not payload.breach_policy:
        violations.append("No breach notification policy")

    return {
        "request_id": str(uuid.uuid4()),
        "status": "completed",
        "checked_at": datetime.utcnow().isoformat(),
        "compliant": len(violations) == 0,
        "violations": violations,
    }


@router.post("/iso27001/check", response_model=ISO27001Response)
def demo_iso_check(payload: ISO27001Request):
    gaps = []
    if not payload.risk_assessment_done:
        gaps.append("Risk assessment missing")
    if not payload.incident_management:
        gaps.append("Incident management missing")

    maturity = "high" if not gaps else "medium"

    return {
        "request_id": str(uuid.uuid4()),
        "status": "completed",
        "checked_at": datetime.utcnow().isoformat(),
        "maturity_level": maturity,
        "gaps": gaps,
    }


@router.post("/market/check", response_model=MarketComplianceResponse)
def demo_market_check(payload: MarketComplianceRequest):
    remarks = []
    if not payload.trade_monitoring:
        remarks.append("Trade monitoring missing")
    if not payload.conflict_policy:
        remarks.append("Conflict of interest policy missing")

    return {
        "request_id": str(uuid.uuid4()),
        "status": "completed",
        "checked_at": datetime.utcnow().isoformat(),
        "compliant": len(remarks) == 0,
        "remarks": remarks,
    }
