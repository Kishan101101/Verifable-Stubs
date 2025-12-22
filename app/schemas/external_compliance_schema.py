"""
External Compliance & Verification API Schemas
Comprehensive schemas for regulations, sanctions, financial verification, and fraud detection
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, date


# ============================================
# Base Response Models
# ============================================

class ErrorDetail(BaseModel):
    field: str
    message: str


class ErrorResponse(BaseModel):
    code: str
    message: str
    details: Optional[List[ErrorDetail]] = None


class BaseAPIResponse(BaseModel):
    success: bool = True


# ============================================
# Regulation Schemas
# ============================================

class KeyArticle(BaseModel):
    article_id: str
    title: str
    content: str
    penalties: Optional[str] = None


class RegulationCreateRequest(BaseModel):
    """Schema for creating a new regulation"""
    regulation_id: str = Field(..., example="REG-GDPR-001")
    name: str = Field(..., example="General Data Protection Regulation")
    code: str = Field(..., example="gdpr")
    category: Optional[str] = Field(None, example="data_protection")
    jurisdiction: Optional[str] = Field(None, example="EU")
    version: Optional[str] = Field(None, example="2018")
    effective_date: Optional[date] = Field(None, example="2018-05-25")
    description: Optional[str] = Field(None, example="EU regulation on data protection and privacy")
    required_fields: Optional[List[str]] = None
    key_articles: Optional[List[KeyArticle]] = None
    compliance_checklist: Optional[List[str]] = None
    penalties: Optional[Dict[str, str]] = None
    is_active: bool = True
    tags: Optional[List[str]] = None


class RegulationUpdateRequest(BaseModel):
    """Schema for updating a regulation (partial update)"""
    name: Optional[str] = None
    code: Optional[str] = None
    category: Optional[str] = None
    jurisdiction: Optional[str] = None
    version: Optional[str] = None
    effective_date: Optional[date] = None
    description: Optional[str] = None
    required_fields: Optional[List[str]] = None
    key_articles: Optional[List[KeyArticle]] = None
    compliance_checklist: Optional[List[str]] = None
    penalties: Optional[Dict[str, str]] = None
    is_active: Optional[bool] = None
    tags: Optional[List[str]] = None


class RegulationResponse(BaseModel):
    """Full regulation response"""
    regulation_id: str
    name: str
    code: str
    category: Optional[str]
    jurisdiction: Optional[str]
    version: Optional[str]
    effective_date: Optional[date]
    description: Optional[str]
    required_fields: Optional[List[str]]
    key_articles: Optional[List[Dict[str, Any]]]
    compliance_checklist: Optional[List[str]]
    penalties: Optional[Dict[str, str]]
    is_active: bool
    tags: Optional[List[str]]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class RegulationSummary(BaseModel):
    """Regulation summary for list view"""
    regulation_id: str
    name: str
    code: str
    category: Optional[str]
    jurisdiction: Optional[str]


class RegulationCreateResponse(BaseAPIResponse):
    regulation_id: str
    message: str


class RegulationListResponse(BaseAPIResponse):
    total: int
    page: int
    limit: int
    regulations: List[RegulationSummary]


# ============================================
# Compliance Verification Schemas
# ============================================

class ComplianceVerifyEntityRequest(BaseModel):
    """Request to verify entity compliance"""
    entity_name: str = Field(..., example="Acme Corp")
    entity_type: str = Field(..., example="company")
    entity_country: str = Field(..., example="US")
    industry: Optional[str] = Field(None, example="technology")
    categories: List[str] = Field(..., example=["kyc", "aml", "sox"])
    document_data: Optional[Dict[str, Any]] = None


class Violation(BaseModel):
    regulation: str
    article: Optional[str]
    description: str
    severity: str  # low, medium, high, critical


class ComplianceVerifyEntityResponse(BaseModel):
    """Response from compliance verification"""
    compliance_status: str  # compliant, partial, non_compliant
    compliance_score: int = Field(..., ge=0, le=100)
    risk_level: str  # low, medium, high, critical
    regulations_checked: List[str]
    violations: List[Violation]
    missing_requirements: List[str]
    passed_checks: List[str]
    recommendations: List[str]
    checked_at: datetime


# ============================================
# Sanctions Screening Schemas
# ============================================

class SanctionsScreenRequest(BaseModel):
    """Request for OFAC/Sanctions screening"""
    entity_name: str = Field(..., example="Acme Corp")
    entity_type: str = Field(..., example="company")
    entity_country: Optional[str] = Field(None, example="US")
    check_pep: bool = False
    check_adverse_media: bool = False
    sanctions_lists: Optional[List[str]] = Field(
        default=["ofac_sdn", "eu_consolidated", "un_consolidated", "pep"],
        example=["ofac_sdn", "eu_consolidated", "un_consolidated", "pep"]
    )


class SanctionsMatch(BaseModel):
    list_name: str
    match_score: int
    matched_name: str
    match_type: str  # exact, partial, fuzzy
    sanctions_details: Optional[Dict[str, Any]] = None


class PEPCheck(BaseModel):
    is_pep: bool
    pep_level: Optional[str] = None
    details: Optional[str] = None


class AdverseMedia(BaseModel):
    found: bool
    articles: List[Dict[str, Any]]


class SanctionsScreenResponse(BaseModel):
    """Response from sanctions screening"""
    screening_status: str  # clear, hit, potential_match
    matches_found: int
    risk_level: str
    matches: List[SanctionsMatch]
    pep_check: Optional[PEPCheck] = None
    adverse_media: Optional[AdverseMedia] = None
    lists_checked: List[str]
    screened_at: datetime


# ============================================
# Financial Verification Schemas
# ============================================

class FinancialVerifyRequest(BaseModel):
    """Request for financial health verification"""
    entity_name: str = Field(..., example="Acme Corp")
    entity_country: str = Field(..., example="US")
    industry: Optional[str] = Field(None, example="technology")
    company_size: Optional[str] = Field(None, example="medium")
    check_credit: bool = True
    check_financials: bool = True
    check_bankruptcy: bool = True
    check_liens: bool = True


class CreditDetails(BaseModel):
    score: Optional[int] = None
    payment_history: Optional[str] = None
    credit_utilization: Optional[str] = None


class FinancialIndicators(BaseModel):
    revenue_trend: Optional[str] = None
    profit_margin: Optional[str] = None
    debt_to_equity: Optional[float] = None


class BankruptcyHistory(BaseModel):
    has_history: bool
    filings: List[Dict[str, Any]]


class LiensInfo(BaseModel):
    active_liens: int
    total_amount: float


class FinancialVerifyResponse(BaseModel):
    """Response from financial verification"""
    financial_health_score: int
    risk_level: str
    credit_rating: Optional[str] = None
    financial_stability: Optional[str] = None
    bankruptcy_risk: bool
    liens_found: bool
    credit_details: Optional[CreditDetails] = None
    financial_indicators: Optional[FinancialIndicators] = None
    bankruptcy_history: Optional[BankruptcyHistory] = None
    liens: Optional[LiensInfo] = None
    verified_at: datetime


# ============================================
# Fraud Detection Schemas
# ============================================

class FraudDetectRequest(BaseModel):
    """Request for fraud detection"""
    entity_name: str = Field(..., example="Acme Corp")
    entity_type: str = Field(..., example="company")
    document_data: Optional[Dict[str, Any]] = None


class FraudIndicator(BaseModel):
    type: str
    confidence: int
    description: str


class IdentityVerification(BaseModel):
    verified: bool
    confidence: int


class AddressVerification(BaseModel):
    valid: bool
    type: Optional[str] = None  # commercial, residential, virtual


class FraudDetectResponse(BaseModel):
    """Response from fraud detection"""
    fraud_detected: bool
    risk_level: str
    risk_score: int
    fraud_indicators: List[FraudIndicator]
    patterns_detected: List[str]
    identity_verification: Optional[IdentityVerification] = None
    address_verification: Optional[AddressVerification] = None
    analyzed_at: datetime


class DocumentForgeryRequest(BaseModel):
    """Request for document forgery detection"""
    document_type: str = Field(..., example="business_license")
    document_data: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None


class AuthenticityChecks(BaseModel):
    format_valid: bool
    dates_consistent: bool
    authority_verified: bool
    metadata_clean: bool


class DocumentForgeryResponse(BaseModel):
    """Response from document forgery detection"""
    forgery_detected: bool
    confidence_score: int
    risk_level: str
    tampering_indicators: List[str]
    authenticity_checks: AuthenticityChecks
    analyzed_at: datetime


# ============================================
# Sanctions List Management Schemas
# ============================================

class SanctionsEntryIdentifier(BaseModel):
    type: str
    value: str


class SanctionsEntryAdditionalInfo(BaseModel):
    addresses: Optional[List[str]] = None
    identifiers: Optional[List[SanctionsEntryIdentifier]] = None


class SanctionsEntryCreateRequest(BaseModel):
    """Request to add entry to sanctions list"""
    entry_id: str = Field(..., example="SDN-12345")
    name: str = Field(..., example="ACME EVIL CORP")
    aliases: Optional[List[str]] = None
    entity_type: str = Field(..., example="company")
    country: str = Field(..., example="IR")
    program: Optional[str] = Field(None, example="IRAN")
    listing_date: Optional[date] = None
    reason: Optional[str] = None
    additional_info: Optional[SanctionsEntryAdditionalInfo] = None
    is_active: bool = True


class SanctionsEntryResponse(BaseModel):
    """Response for sanctions entry"""
    entry_id: str
    list_type: str
    name: str
    aliases: Optional[List[str]]
    entity_type: Optional[str]
    country: Optional[str]
    program: Optional[str]
    listing_date: Optional[date]
    reason: Optional[str]
    additional_info: Optional[Dict[str, Any]]
    is_active: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class SanctionsEntryCreateResponse(BaseAPIResponse):
    entry_id: str
    list_type: str
    message: str


class SanctionsListEntriesResponse(BaseAPIResponse):
    total: int
    page: int
    limit: int
    entries: List[SanctionsEntryResponse]


# ============================================
# Fraud Patterns Schemas
# ============================================

class FraudPatternIndicator(BaseModel):
    field: str
    condition: str
    weight: float


class FraudPatternCreateRequest(BaseModel):
    """Request to create fraud pattern"""
    pattern_id: str = Field(..., example="FP-001")
    name: str = Field(..., example="Synthetic Identity Pattern")
    category: str = Field(..., example="identity_fraud")
    description: Optional[str] = None
    indicators: Optional[List[FraudPatternIndicator]] = None
    risk_score_threshold: Optional[int] = Field(None, ge=0, le=100)
    action: Optional[str] = Field(None, example="flag_for_review")
    is_active: bool = True


class FraudPatternUpdateRequest(BaseModel):
    """Request to update fraud pattern"""
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    indicators: Optional[List[FraudPatternIndicator]] = None
    risk_score_threshold: Optional[int] = None
    action: Optional[str] = None
    is_active: Optional[bool] = None


class FraudPatternResponse(BaseModel):
    """Response for fraud pattern"""
    pattern_id: str
    name: str
    category: Optional[str]
    description: Optional[str]
    indicators: Optional[List[Dict[str, Any]]]
    risk_score_threshold: Optional[int]
    action: Optional[str]
    is_active: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class FraudPatternCreateResponse(BaseAPIResponse):
    pattern_id: str
    message: str


class FraudPatternListResponse(BaseAPIResponse):
    total: int
    page: int
    limit: int
    patterns: List[FraudPatternResponse]
