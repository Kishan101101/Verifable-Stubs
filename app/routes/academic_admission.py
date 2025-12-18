from flask import Blueprint, request, jsonify
from app import db
from app.models.academic import StudentSeed, AcademicRecord, EligibilityRule, MeritRule
from app.schemas.academic_schema import StudentSeedSchema, EligibilityRuleSchema, MeritRuleSchema

academic_bp = Blueprint('academic', __name__)

# In-memory indexes
ROLL_INDEX = {}      # roll_number → student_id
CERT_INDEX = {}      # certificate_number → student_id

@academic_bp.route('/admin/students', methods=['POST'])
def add_student():
    """
    Admin endpoint to seed students into database
    ---
    tags:
      - Academic Admin
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: array
          items:
            $ref: '#/definitions/StudentSeedSchema'
    responses:
      200:
        description: Batch processed successfully
      400:
        description: Invalid request
    """
    try:
        data = request.get_json()
        if not isinstance(data, list):
            return jsonify({'error': 'Expected a list of students'}), 400
        
        added_ids = []
        
        for student_data in data:
            try:
                validated_student = StudentSeedSchema(**student_data)
            except Exception as e:
                continue
            
            # Check if student already exists
            existing = StudentSeed.query.filter_by(student_id=validated_student.student_id).first()
            if existing:
                continue
            
            # Create student
            student = StudentSeed(
                student_id=validated_student.student_id,
                name=validated_student.name,
                dob=validated_student.dob
            )
            
            # Add academic records
            for record in validated_student.academic_records:
                acad_record = AcademicRecord(
                    level=record.level,
                    board=record.board,
                    roll_number=record.roll_number,
                    year_of_passing=record.year_of_passing,
                    marks=record.marks,
                    certificate_number=record.certificate_number,
                    student=student
                )
                db.session.add(acad_record)
                ROLL_INDEX[record.roll_number] = validated_student.student_id
                CERT_INDEX[record.certificate_number] = validated_student.student_id
            
            db.session.add(student)
            added_ids.append(validated_student.student_id)
        
        db.session.commit()
        
        return jsonify({
            'message': f'Batch processed. {len(added_ids)} students added.',
            'student_ids': added_ids
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@academic_bp.route('/admin/eligibility-rules', methods=['POST'])
def add_eligibility_rule():
    """
    Admin endpoint to add eligibility rules
    ---
    tags:
      - Academic Admin
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/EligibilityRuleSchema'
    responses:
      200:
        description: Eligibility rule added
      400:
        description: Invalid request
    """
    try:
        data = request.get_json()
        validated_rule = EligibilityRuleSchema(**data)
        
        existing = EligibilityRule.query.filter_by(program=validated_rule.program).first()
        if existing:
            return jsonify({'error': 'Rule for this program already exists'}), 400
        
        rule = EligibilityRule(
            program=validated_rule.program,
            min_marks=validated_rule.min_marks,
            age_limit=validated_rule.age_limit,
            category_specific=validated_rule.category_specific
        )
        
        db.session.add(rule)
        db.session.commit()
        
        return jsonify({
            'message': 'Eligibility rule added',
            'program': validated_rule.program
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@academic_bp.route('/admin/merit-rules', methods=['POST'])
def add_merit_rule():
    """
    Admin endpoint to add merit calculation rules
    ---
    tags:
      - Academic Admin
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/MeritRuleSchema'
    responses:
      200:
        description: Merit rule added
      400:
        description: Invalid request
    """
    try:
        data = request.get_json()
        validated_rule = MeritRuleSchema(**data)
        
        existing = MeritRule.query.filter_by(program=validated_rule.program).first()
        if existing:
            return jsonify({'error': 'Rule for this program already exists'}), 400
        
        rule = MeritRule(
            program=validated_rule.program,
            weightage=validated_rule.weightage
        )
        
        db.session.add(rule)
        db.session.commit()
        
        return jsonify({
            'message': 'Merit rule added',
            'program': validated_rule.program
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@academic_bp.route('/verify/roll-number', methods=['GET'])
def verify_roll_number():
    """
    Verify student by roll number
    ---
    tags:
      - Academic Verification
    parameters:
      - name: roll_number
        in: query
        type: string
        required: true
    responses:
      200:
        description: Roll number verification result
      404:
        description: Roll number not found
    """
    roll_number = request.args.get('roll_number')
    
    if not roll_number:
        return jsonify({'error': 'roll_number parameter required'}), 400
    
    record = AcademicRecord.query.filter_by(roll_number=roll_number).first()
    
    if not record:
        return jsonify({'error': 'Roll number not found'}), 404
    
    return jsonify({
        'student_id': record.student.student_id,
        'roll_number': roll_number,
        'year_of_passing': record.year_of_passing,
        'marks': record.marks,
        'verified': True
    }), 200

@academic_bp.route('/verify/certificate', methods=['GET'])
def verify_certificate():
    """
    Verify student certificate
    ---
    tags:
      - Academic Verification
    parameters:
      - name: certificate_number
        in: query
        type: string
        required: true
    responses:
      200:
        description: Certificate verification result
      404:
        description: Certificate not found
    """
    certificate_number = request.args.get('certificate_number')
    
    if not certificate_number:
        return jsonify({'error': 'certificate_number parameter required'}), 400
    
    record = AcademicRecord.query.filter_by(certificate_number=certificate_number).first()
    
    if not record:
        return jsonify({'error': 'Certificate not found'}), 404
    
    return jsonify({
        'certificate_number': certificate_number,
        'student_id': record.student.student_id,
        'level': record.level,
        'marks': record.marks,
        'verified': True
    }), 200

@academic_bp.route('/check-eligibility', methods=['GET'])
def check_eligibility():
    """
    Check if student is eligible for a program
    ---
    tags:
      - Academic Verification
    parameters:
      - name: student_id
        in: query
        type: string
        required: true
      - name: program
        in: query
        type: string
        required: true
    responses:
      200:
        description: Eligibility check result
      404:
        description: Student or program not found
    """
    student_id = request.args.get('student_id')
    program = request.args.get('program')
    
    if not student_id or not program:
        return jsonify({'error': 'student_id and program parameters required'}), 400
    
    student = StudentSeed.query.filter_by(student_id=student_id).first()
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    rule = EligibilityRule.query.filter_by(program=program).first()
    if not rule:
        return jsonify({'error': 'Program not found'}), 404
    
    # Get the student's highest marks
    max_marks = max([record.marks for record in student.academic_records], default=0)
    eligible = max_marks >= rule.min_marks
    
    return jsonify({
        'eligible': eligible,
        'program': program,
        'student_marks': max_marks,
        'required_marks': rule.min_marks,
        'message': 'Student is eligible' if eligible else 'Student does not meet minimum marks'
    }), 200

@academic_bp.route('/calculate-merit', methods=['GET'])
def calculate_merit():
    """
    Calculate merit score for a student in a program
    ---
    tags:
      - Academic Verification
    parameters:
      - name: student_id
        in: query
        type: string
        required: true
      - name: program
        in: query
        type: string
        required: true
    responses:
      200:
        description: Merit calculation result
      404:
        description: Student or program not found
    """
    student_id = request.args.get('student_id')
    program = request.args.get('program')
    
    if not student_id or not program:
        return jsonify({'error': 'student_id and program parameters required'}), 400
    
    student = StudentSeed.query.filter_by(student_id=student_id).first()
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    rule = MeritRule.query.filter_by(program=program).first()
    if not rule:
        return jsonify({'error': 'Merit rule not found'}), 404
    
    # Calculate merit based on weightage
    merit_score = 0.0
    for level, weightage in rule.weightage.items():
        record = next((r for r in student.academic_records if r.level.lower() in level.lower()), None)
        if record:
            merit_score += record.marks * weightage
    
    return jsonify({
        'student_id': student_id,
        'program': program,
        'merit_score': merit_score,
        'rank': None  # Can be calculated based on all students
    }), 200
