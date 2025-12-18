from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.academic import StudentSeed, AcademicRecord, EligibilityRule, MeritRule
from app.schemas.academic_schema import StudentSeedSchema, EligibilityRuleSchema, MeritRuleSchema

router = APIRouter()

# In-memory indexes
ROLL_INDEX = {}      # roll_number → student_id
CERT_INDEX = {}      # certificate_number → student_id

@router.post('/admin/students')
def add_student(data: list[StudentSeedSchema], db: Session = Depends(get_db)):
    """Admin endpoint to seed students into database"""
    try:
        if not isinstance(data, list):
            raise HTTPException(status_code=400, detail='Expected a list of students')
        
        added_ids = []
        
        for student_data in data:
            # Check if student already exists
            existing = db.query(StudentSeed).filter_by(student_id=student_data.student_id).first()
            if existing:
                continue
            
            # Create student
            student = StudentSeed(
                student_id=student_data.student_id,
                name=student_data.name,
                dob=student_data.dob
            )
            
            # Add academic records
            for record in student_data.academic_records:
                acad_record = AcademicRecord(
                    level=record.level,
                    board=record.board,
                    roll_number=record.roll_number,
                    year_of_passing=record.year_of_passing,
                    marks=record.marks,
                    certificate_number=record.certificate_number,
                    student=student
                )
                db.add(acad_record)
                ROLL_INDEX[record.roll_number] = student_data.student_id
                CERT_INDEX[record.certificate_number] = student_data.student_id
            
            db.add(student)
            added_ids.append(student_data.student_id)
        
        db.commit()
        
        return {
            'message': f'Batch processed. {len(added_ids)} students added.',
            'student_ids': added_ids
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/admin/eligibility-rules')
def add_eligibility_rule(data: EligibilityRuleSchema, db: Session = Depends(get_db)):
    """Admin endpoint to add eligibility rules"""
    try:
        existing = db.query(EligibilityRule).filter_by(program=data.program).first()
        if existing:
            raise HTTPException(status_code=400, detail='Rule for this program already exists')
        
        rule = EligibilityRule(
            program=data.program,
            min_marks=data.min_marks,
            age_limit=data.age_limit,
            category_specific=data.category_specific
        )
        
        db.add(rule)
        db.commit()
        
        return {
            'message': 'Eligibility rule added',
            'program': data.program
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/admin/merit-rules')
def add_merit_rule(data: MeritRuleSchema, db: Session = Depends(get_db)):
    """Admin endpoint to add merit calculation rules"""
    try:
        existing = db.query(MeritRule).filter_by(program=data.program).first()
        if existing:
            raise HTTPException(status_code=400, detail='Rule for this program already exists')
        
        rule = MeritRule(
            program=data.program,
            weightage=data.weightage
        )
        
        db.add(rule)
        db.commit()
        
        return {
            'message': 'Merit rule added',
            'program': data.program
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/verify/roll-number')
def verify_roll_number(roll_number: str, db: Session = Depends(get_db)):
    """Verify student roll number"""
    if not roll_number:
        raise HTTPException(status_code=400, detail='roll_number parameter required')
    
    record = db.query(AcademicRecord).filter_by(roll_number=roll_number).first()
    
    if not record:
        raise HTTPException(status_code=404, detail='Roll number not found')
    
    return {
        'student_id': record.student.student_id,
        'roll_number': roll_number,
        'year_of_passing': record.year_of_passing,
        'marks': record.marks,
        'verified': True
    }

@router.get('/verify/certificate')
def verify_certificate(certificate_number: str, db: Session = Depends(get_db)):
    """Verify student certificate"""
    if not certificate_number:
        raise HTTPException(status_code=400, detail='certificate_number parameter required')
    
    record = db.query(AcademicRecord).filter_by(certificate_number=certificate_number).first()
    
    if not record:
        raise HTTPException(status_code=404, detail='Certificate not found')
    
    return {
        'certificate_number': certificate_number,
        'student_id': record.student.student_id,
        'level': record.level,
        'marks': record.marks,
        'verified': True
    }

@router.get('/check-eligibility')
def check_eligibility(student_id: str, program: str, db: Session = Depends(get_db)):
    """Check if student is eligible for a program"""
    if not student_id or not program:
        raise HTTPException(status_code=400, detail='student_id and program parameters required')
    
    student = db.query(StudentSeed).filter_by(student_id=student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')
    
    rule = db.query(EligibilityRule).filter_by(program=program).first()
    if not rule:
        raise HTTPException(status_code=404, detail='Program not found')
    
    # Get the student's highest marks
    max_marks = max([record.marks for record in student.academic_records], default=0)
    eligible = max_marks >= rule.min_marks
    
    return {
        'eligible': eligible,
        'program': program,
        'student_marks': max_marks,
        'required_marks': rule.min_marks,
        'message': 'Student is eligible' if eligible else 'Student does not meet minimum marks'
    }

@router.get('/calculate-merit')
def calculate_merit(student_id: str, program: str, db: Session = Depends(get_db)):
    """Calculate merit score for a student in a program"""
    if not student_id or not program:
        raise HTTPException(status_code=400, detail='student_id and program parameters required')
    
    student = db.query(StudentSeed).filter_by(student_id=student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')
    
    rule = db.query(MeritRule).filter_by(program=program).first()
    if not rule:
        raise HTTPException(status_code=404, detail='Merit rule not found')
    
    # Calculate merit based on weightage
    merit_score = 0.0
    for level, weightage in rule.weightage.items():
        record = next((r for r in student.academic_records if r.level.lower() in level.lower()), None)
        if record:
            merit_score += record.marks * weightage
    
    return {
        'student_id': student_id,
        'program': program,
        'merit_score': merit_score,
        'rank': None
    }
