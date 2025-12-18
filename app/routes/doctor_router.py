from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.doctor import Doctor, Degree, BoardCertification, Training, Employment, DisciplinaryAction, MalpracticeCase
from app.schemas.doctor_schema import DoctorSeedSchema

router = APIRouter()

# In-memory indexes for fast lookups
LICENSE_INDEX = {}  # license_number → doctor_id
BOARD_INDEX = {}    # certificate_number → doctor_id

@router.post('/admin/add')
def add_doctor(data: list[DoctorSeedSchema], db: Session = Depends(get_db)):
    """Admin endpoint to seed doctors into database"""
    try:
        if not isinstance(data, list):
            raise HTTPException(status_code=400, detail='Expected a list of doctors')
        
        added_ids = []
        
        for doctor_data in data:
            # Check if doctor already exists
            existing = db.query(Doctor).filter_by(doctor_id=doctor_data.doctor_id).first()
            if existing:
                continue
            
            # Create doctor
            doctor = Doctor(
                doctor_id=doctor_data.doctor_id,
                name=doctor_data.name,
                license_number=doctor_data.license_number,
                license_status=doctor_data.license_status,
                license_expiry=doctor_data.license_expiry
            )
            
            # Add degree
            degree = Degree(
                degree_name=doctor_data.degree.degree_name,
                university=doctor_data.degree.university,
                year_of_passing=doctor_data.degree.year_of_passing,
                registration_number=doctor_data.degree.registration_number,
                doctor=doctor
            )
            
            # Add board certifications
            for cert in doctor_data.board_certifications:
                board_cert = BoardCertification(
                    board_name=cert.board_name,
                    certificate_number=cert.certificate_number,
                    valid_till=cert.valid_till,
                    doctor=doctor
                )
                db.add(board_cert)
                BOARD_INDEX[cert.certificate_number] = doctor_data.doctor_id
            
            # Add trainings
            for training in doctor_data.training:
                train = Training(
                    program_name=training.program_name,
                    institution=training.institution,
                    completion_year=training.completion_year,
                    doctor=doctor
                )
                db.add(train)
            
            # Add employments
            for employment in doctor_data.employment_history:
                emp = Employment(
                    employer_name=employment.employer_name,
                    role=employment.role,
                    years=employment.years,
                    doctor=doctor
                )
                db.add(emp)
            
            # Add disciplinary actions
            for action in doctor_data.disciplinary_actions:
                action_dict = action.dict() if hasattr(action, 'dict') else action
                disc = DisciplinaryAction(data=action_dict, doctor=doctor)
                db.add(disc)
            
            # Add malpractice cases
            for case in doctor_data.malpractice_cases:
                case_dict = case.dict() if hasattr(case, 'dict') else case
                malpractice = MalpracticeCase(data=case_dict, doctor=doctor)
                db.add(malpractice)
            
            db.add(degree)
            db.add(doctor)
            LICENSE_INDEX[doctor_data.license_number] = doctor_data.doctor_id
            added_ids.append(doctor_data.doctor_id)
        
        db.commit()
        
        return {
            'message': f'Batch processed. {len(added_ids)} doctors added.',
            'doctor_ids': added_ids
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/psv/license/status')
def psv_license_status(license_number: str, db: Session = Depends(get_db)):
    """Get license status for a doctor"""
    if not license_number:
        raise HTTPException(status_code=400, detail='license_number parameter required')
    
    doctor = db.query(Doctor).filter_by(license_number=license_number).first()
    
    if not doctor:
        raise HTTPException(status_code=404, detail='License not found')
    
    return {
        'license_number': license_number,
        'status': doctor.license_status,
        'expiry_date': doctor.license_expiry,
        'issuer': 'State Medical Board',
        'doctor_id': doctor.doctor_id
    }

@router.get('/psv/degree/info')
def psv_degree_info(doctor_id: str, db: Session = Depends(get_db)):
    """Get degree information for a doctor"""
    if not doctor_id:
        raise HTTPException(status_code=400, detail='doctor_id parameter required')
    
    doctor = db.query(Doctor).filter_by(doctor_id=doctor_id).first()
    
    if not doctor:
        raise HTTPException(status_code=404, detail='Doctor not found')
    
    if not doctor.degrees:
        raise HTTPException(status_code=404, detail='No degree found')
    
    degree = doctor.degrees[0]
    
    return {
        'degree_name': degree.degree_name,
        'university': degree.university,
        'year_of_passing': degree.year_of_passing,
        'registration_number': degree.registration_number,
        'verified': True,
        'source_authority': f"{degree.university} Registrar"
    }

@router.get('/psv/board-cert/info')
def psv_board_cert_info(certificate_number: str, db: Session = Depends(get_db)):
    """Get board certification information"""
    if not certificate_number:
        raise HTTPException(status_code=400, detail='certificate_number parameter required')
    
    cert = db.query(BoardCertification).filter_by(certificate_number=certificate_number).first()
    
    if not cert:
        raise HTTPException(status_code=404, detail='Certificate not found')
    
    return {
        'board_name': cert.board_name,
        'certificate_number': certificate_number,
        'valid_till': cert.valid_till,
        'verified': True
    }

@router.get('/psv/training/info')
def psv_training_info(doctor_id: str, db: Session = Depends(get_db)):
    """Get training information for a doctor"""
    if not doctor_id:
        raise HTTPException(status_code=400, detail='doctor_id parameter required')
    
    doctor = db.query(Doctor).filter_by(doctor_id=doctor_id).first()
    
    if not doctor:
        raise HTTPException(status_code=404, detail='Doctor not found')
    
    training_list = doctor.trainings
    
    if not training_list:
        return {'verified': False}
    
    t = training_list[0]
    
    return {
        'program_name': t.program_name,
        'institution': t.institution,
        'completion_year': t.completion_year,
        'verified': True
    }

@router.get('/psv/employment/info')
def psv_employment_info(doctor_id: str, db: Session = Depends(get_db)):
    """Get employment history for a doctor"""
    if not doctor_id:
        raise HTTPException(status_code=400, detail='doctor_id parameter required')
    
    doctor = db.query(Doctor).filter_by(doctor_id=doctor_id).first()
    
    if not doctor:
        raise HTTPException(status_code=404, detail='Doctor not found')
    
    employment_details = [e.to_dict() for e in doctor.employments]
    
    return {
        'employment_details': employment_details,
        'verified': True
    }

@router.get('/psv/disciplines/check')
def psv_disciplines_check(license_number: str, db: Session = Depends(get_db)):
    """Check disciplinary actions for a doctor"""
    if not license_number:
        raise HTTPException(status_code=400, detail='license_number parameter required')
    
    doctor = db.query(Doctor).filter_by(license_number=license_number).first()
    
    if not doctor:
        raise HTTPException(status_code=404, detail='License not found')
    
    records = [d.to_dict() for d in doctor.disciplinary_actions]
    
    return {
        'has_disciplinary_action': len(records) > 0,
        'records': records
    }

@router.get('/psv/malpractice/history')
def psv_malpractice_history(doctor_id: str, db: Session = Depends(get_db)):
    """Get malpractice history for a doctor"""
    if not doctor_id:
        raise HTTPException(status_code=400, detail='doctor_id parameter required')
    
    doctor = db.query(Doctor).filter_by(doctor_id=doctor_id).first()
    
    if not doctor:
        raise HTTPException(status_code=404, detail='Doctor not found')
    
    cases = [mc.to_dict() for mc in doctor.malpractice_cases]
    
    return {
        'has_malpractice_history': len(cases) > 0,
        'cases': cases
    }

@router.get('/psv/verify')
def psv_generic_verify(type: str, value: str):
    """Generic verification endpoint"""
    if not type or not value:
        raise HTTPException(status_code=400, detail='type and value parameters required')
    
    return {
        'verified': True,
        'confidence': 0.87,
        'type': type,
        'value': value
    }
