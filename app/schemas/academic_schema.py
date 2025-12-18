from pydantic import BaseModel
from typing import List, Dict, Optional

# ============================
# ACADEMIC PROCESSING SCHEMAS
# ============================

class AcademicRecordSchema(BaseModel):
    level: str  # 10th, 12th, Graduation
    board: str
    roll_number: str
    year_of_passing: str
    marks: float
    certificate_number: str

class StudentSeedSchema(BaseModel):
    student_id: str
    name: str
    dob: str
    academic_records: List[AcademicRecordSchema]

class StudentResponseSchema(BaseModel):
    message: str
    student_ids: List[str]

class EligibilityRuleSchema(BaseModel):
    program: str
    min_marks: float
    age_limit: Optional[int] = None
    category_specific: Optional[Dict[str, float]] = None

class MeritRuleSchema(BaseModel):
    program: str
    weightage: Dict[str, float]

class EligibilityCheckSchema(BaseModel):
    eligible: bool
    program: str
    student_marks: float
    required_marks: float
    message: str

class MeritCalculationSchema(BaseModel):
    student_id: str
    program: str
    merit_score: float
    rank: Optional[int] = None

class RollNumberLookupSchema(BaseModel):
    student_id: str
    roll_number: str
    year_of_passing: str
    marks: float
    verified: bool
