from pydantic import BaseModel
from typing import Dict, Any, Optional
from decimal import Decimal

# ============================
# INSURANCE CLAIM SCHEMAS
# ============================

class MedicalEnrichmentRequestSchema(BaseModel):
    diagnosis: str
    hospital_name: str

class MedicalEnrichmentResponseSchema(BaseModel):
    id: int
    diagnosis: str
    hospital_name: str
    icd_mapping: Optional[Dict[str, str]] = None
    message: str

class ReviewerRequestSchema(BaseModel):
    workflow_state: Dict[str, Any]

class ReviewerRequestResponseSchema(BaseModel):
    id: int
    workflow_state: Dict[str, Any]
    message: str

class PayoutRequestSchema(BaseModel):
    approved_amount: float
    deductible: float
    policy_limit: float

class PayoutRequestResponseSchema(BaseModel):
    id: int
    approved_amount: float
    deductible: float
    policy_limit: float
    message: str

class NotificationRequestSchema(BaseModel):
    recipient_email: str
    subject: str
    message: str

class NotificationResponseSchema(BaseModel):
    id: int
    recipient_email: str
    subject: str
    message: str
    sent: bool
    response_message: str

class MedicalDataEnrichmentSchema(BaseModel):
    diagnosis: str
    icd_code: str
    description: str
    hospital_name: str
    verified: bool
