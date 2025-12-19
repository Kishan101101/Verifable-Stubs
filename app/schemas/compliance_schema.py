from pydantic import BaseModel
from typing import List, Optional

class Evidence(BaseModel):
    document_id: str
    confidence: float
    notes: Optional[str] = None


class APIResponse(BaseModel):
    request_id: str
    status: str
    checked_at: str


class SanctionsCheckRequest(BaseModel):
    name: str
    country: str
    id_number: Optional[str] = None


class SanctionsCheckResponse(APIResponse):
    sanctions_hit: bool
    risk_level: str
    matched_lists: List[str]
    evidence: List[Evidence]


class PEPCheckRequest(BaseModel):
    name: str
    country: str


class PEPCheckResponse(APIResponse):
    is_pep: bool
    pep_category: Optional[str]
    risk_level: str


class GDPRCheckRequest(BaseModel):
    has_privacy_policy: bool
    consent_mechanism: bool
    data_retention_policy: bool


class GDPRCheckResponse(APIResponse):
    compliance_score: int
    status: str
    missing_requirements: List[str]


class PCICheckRequest(BaseModel):
    stores_card_data: bool
    encryption_enabled: bool
    access_control: bool


class PCICheckResponse(APIResponse):
    compliant: bool
    issues: List[str]


class HIPAACheckRequest(BaseModel):
    handles_phi: bool
    access_logging: bool
    breach_policy: bool


class HIPAACheckResponse(APIResponse):
    compliant: bool
    violations: List[str]


class ISO27001Request(BaseModel):
    risk_assessment_done: bool
    incident_management: bool
    access_control_policy: bool


class ISO27001Response(APIResponse):
    maturity_level: str
    gaps: List[str]


class MarketComplianceRequest(BaseModel):
    trade_monitoring: bool
    conflict_policy: bool


class MarketComplianceResponse(APIResponse):
    compliant: bool
    remarks: List[str]