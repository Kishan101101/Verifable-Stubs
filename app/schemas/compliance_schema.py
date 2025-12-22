"""
Legacy Compliance Check Schemas
Schemas for specific compliance framework checks (GDPR, PCI, HIPAA, ISO27001, Market)
"""
from pydantic import BaseModel
from typing import List, Optional


class APIResponse(BaseModel):
    """Base API response with common fields"""
    request_id: str
    status: str
    checked_at: str


# ============================================
# PEP Check Schemas
# ============================================

class PEPCheckRequest(BaseModel):
    name: str
    country: str


class PEPCheckResponse(APIResponse):
    is_pep: bool
    pep_category: Optional[str]
    risk_level: str


# ============================================
# GDPR Check Schemas
# ============================================

class GDPRCheckRequest(BaseModel):
    has_privacy_policy: bool
    consent_mechanism: bool
    data_retention_policy: bool


class GDPRCheckResponse(APIResponse):
    compliance_score: int
    missing_requirements: List[str]


# ============================================
# PCI-DSS Check Schemas
# ============================================

class PCICheckRequest(BaseModel):
    stores_card_data: bool
    encryption_enabled: bool
    access_control: bool


class PCICheckResponse(APIResponse):
    compliant: bool
    issues: List[str]


# ============================================
# HIPAA Check Schemas
# ============================================

class HIPAACheckRequest(BaseModel):
    handles_phi: bool
    access_logging: bool
    breach_policy: bool


class HIPAACheckResponse(APIResponse):
    compliant: bool
    violations: List[str]


# ============================================
# ISO 27001 Check Schemas
# ============================================

class ISO27001Request(BaseModel):
    risk_assessment_done: bool
    incident_management: bool
    access_control_policy: bool


class ISO27001Response(APIResponse):
    maturity_level: str
    gaps: List[str]


# ============================================
# Market Compliance Check Schemas
# ============================================

class MarketComplianceRequest(BaseModel):
    trade_monitoring: bool
    conflict_policy: bool


class MarketComplianceResponse(APIResponse):
    compliant: bool
    remarks: List[str]
