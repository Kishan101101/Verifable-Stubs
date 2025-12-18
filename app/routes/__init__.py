# Routes module
from .doctor_onboarding import doctor_bp
from .academic_admission import academic_bp
from .insurance_claim import insurance_bp

__all__ = ['doctor_bp', 'academic_bp', 'insurance_bp']
