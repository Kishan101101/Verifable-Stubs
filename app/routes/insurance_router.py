from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.models.insurance import HospitalVerification, PatientVerification
from app.schemas.insurance_schema import (
    HospitalVerificationRequestSchema, PatientVerificationRequestSchema
)

router = APIRouter()


# =========================================================
# HOSPITAL VERIFICATION ENDPOINTS
# =========================================================

@router.post('/psv/hospital/registration')
def verify_hospital_registration(data: HospitalVerificationRequestSchema, db: Session = Depends(get_db)):
    """POST /api/v1/insurance/hospital/verify - Verify hospital registration by registration number"""
    try:
        # Mock hospital registry - in production this would check against real registry
        hospital_registry = {
            "H001": True,  # apollo hospital
            "H002": True,  # fortis hospital
            "H003": True,  # aiims delhi
        }
        
        # Check if registration number exists in mock registry
        is_verified = hospital_registry.get(data.registration_number.upper(), False)
        
        # Store verification record
        verification = HospitalVerification(
            registration_number=data.registration_number,
            hospital_name=data.hospital_name,
            verified=is_verified,
            verified_at=datetime.utcnow() if is_verified else None
        )
        
        db.add(verification)
        db.commit()
        
        return {
            'registration_number': data.registration_number,
            'hospital_name': data.hospital_name,
            'verified': is_verified,
            'verified_at': verification.verified_at.isoformat() if is_verified else None
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/psv/hospital/registration/{registration_number}')
def get_hospital_verification(registration_number: str, db: Session = Depends(get_db)):
    """GET /api/v1/insurance/hospital/{registration_number} - Retrieve hospital verification result"""
    try:
        record = db.query(HospitalVerification).filter_by(
            registration_number=registration_number
        ).first()
        
        if not record:
            raise HTTPException(status_code=404, detail="Hospital verification record not found")
        
        return record.to_dict()
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================================================
# PATIENT VERIFICATION ENDPOINTS
# =========================================================

@router.post('/psv/patient/identity')
def verify_patient_identity(data: PatientVerificationRequestSchema, db: Session = Depends(get_db)):
    """POST /api/v1/insurance/patient/verify - Verify patient identity by Aadhar and other details"""
    try:
        # Mock patient Aadhar registry - in production this would verify against real government registry
        patient_aadhar_db = {
            "1234": ("Rajesh Kumar", "1990-05-15", "M"),  # aadhar ending in 1234
            "5678": ("Priya Singh", "1985-03-22", "F"),   # aadhar ending in 5678
            "9012": ("Arjun Patel", "1992-08-10", "M"),   # aadhar ending in 9012
        }
        
        # Verify Aadhar details match
        aadhar_data = patient_aadhar_db.get(data.aadhar_last4)
        is_verified = False
        
        if aadhar_data:
            stored_name, stored_dob, stored_gender = aadhar_data
            is_verified = (
                data.full_name.lower() == stored_name.lower() and
                data.date_of_birth == stored_dob and
                data.gender.upper() == stored_gender.upper()
            )
        
        # Store verification record
        verification = PatientVerification(
            patient_id=data.patient_id,
            aadhar_last4=data.aadhar_last4,
            full_name=data.full_name,
            date_of_birth=data.date_of_birth,
            gender=data.gender,
            verified=is_verified,
            verified_at=datetime.utcnow() if is_verified else None
        )
        
        db.add(verification)
        db.commit()
        
        return {
            'patient_id': data.patient_id,
            'aadhar_last4': data.aadhar_last4,
            'full_name': data.full_name,
            'date_of_birth': data.date_of_birth,
            'gender': data.gender,
            'verified': is_verified,
            'verified_at': verification.verified_at.isoformat() if is_verified else None
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/psv/patient/identity/{patient_id}')
def get_patient_verification(patient_id: str, db: Session = Depends(get_db)):
    """GET /api/v1/insurance/patient/{patient_id} - Retrieve patient identity verification result"""
    try:
        record = db.query(PatientVerification).filter_by(
            patient_id=patient_id
        ).first()
        
        if not record:
            raise HTTPException(status_code=404, detail="Patient verification record not found")
        
        return record.to_dict()
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
