from pydantic import BaseModel
from typing import List, Dict, Optional, Any

# ============================
# DOCTOR ONBOARDING SCHEMAS
# ============================

class DegreeSchema(BaseModel):
    degree_name: str
    university: str
    year_of_passing: str
    registration_number: str

class BoardCertSchema(BaseModel):
    board_name: str
    certificate_number: str
    valid_till: str

class TrainingSchema(BaseModel):
    program_name: str
    institution: str
    completion_year: str

class EmploymentSchema(BaseModel):
    employer_name: str
    role: str
    years: str

class DoctorSeedSchema(BaseModel):
    doctor_id: str
    name: str
    license_number: str
    license_status: str
    license_expiry: str
    degree: DegreeSchema
    board_certifications: List[BoardCertSchema]
    training: List[TrainingSchema]
    employment_history: List[EmploymentSchema]
    disciplinary_actions: List[Any] = []
    malpractice_cases: List[Any] = []

class DoctorResponseSchema(BaseModel):
    message: str
    doctor_ids: List[str]

class LicenseStatusSchema(BaseModel):
    license_number: str
    status: str
    expiry_date: str
    issuer: str
    doctor_id: str

class DegreeInfoSchema(BaseModel):
    degree_name: str
    university: str
    year_of_passing: str
    registration_number: str
    verified: bool
    source_authority: str

class BoardCertInfoSchema(BaseModel):
    board_name: str
    certificate_number: str
    valid_till: str
    verified: bool

class TrainingInfoSchema(BaseModel):
    program_name: Optional[str] = None
    institution: Optional[str] = None
    completion_year: Optional[str] = None
    verified: bool

class EmploymentInfoSchema(BaseModel):
    employment_details: List[dict]
    verified: bool

class DisciplinaryCheckSchema(BaseModel):
    has_disciplinary_action: bool
    records: List[dict]

class MalpracticeHistorySchema(BaseModel):
    has_malpractice_history: bool
    cases: List[dict]

class GenericVerifySchema(BaseModel):
    verified: bool
    confidence: float
    type: str
    value: str

