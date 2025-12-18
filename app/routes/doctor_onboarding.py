from flask import Blueprint, request, jsonify
from app import db
from app.models.doctor import Doctor, Degree, BoardCertification, Training, Employment, DisciplinaryAction, MalpracticeCase
from app.schemas.doctor_schema import DoctorSeedSchema

doctor_bp = Blueprint('doctor', __name__)

# In-memory indexes for fast lookups
LICENSE_INDEX = {}  # license_number → doctor_id
BOARD_INDEX = {}    # certificate_number → doctor_id

@doctor_bp.route('/admin/add', methods=['POST'])
def add_doctor():
    """
    Admin endpoint to seed doctors into database
    ---
    tags:
      - Doctor Admin
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: array
          items:
            $ref: '#/definitions/DoctorSeedSchema'
    responses:
      200:
        description: Batch processed successfully
      400:
        description: Invalid request
    """
    try:
        data = request.get_json()
        if not isinstance(data, list):
            return jsonify({'error': 'Expected a list of doctors'}), 400
        
        added_ids = []
        
        for doctor_data in data:
            # Validate schema
            try:
                validated_doctor = DoctorSeedSchema(**doctor_data)
            except Exception as e:
                continue
            
            # Check if doctor already exists
            existing = Doctor.query.filter_by(doctor_id=validated_doctor.doctor_id).first()
            if existing:
                continue
            
            # Create doctor
            doctor = Doctor(
                doctor_id=validated_doctor.doctor_id,
                name=validated_doctor.name,
                license_number=validated_doctor.license_number,
                license_status=validated_doctor.license_status,
                license_expiry=validated_doctor.license_expiry
            )
            
            # Add degree
            degree = Degree(
                degree_name=validated_doctor.degree.degree_name,
                university=validated_doctor.degree.university,
                year_of_passing=validated_doctor.degree.year_of_passing,
                registration_number=validated_doctor.degree.registration_number,
                doctor=doctor
            )
            
            # Add board certifications
            for cert in validated_doctor.board_certifications:
                board_cert = BoardCertification(
                    board_name=cert.board_name,
                    certificate_number=cert.certificate_number,
                    valid_till=cert.valid_till,
                    doctor=doctor
                )
                db.session.add(board_cert)
                BOARD_INDEX[cert.certificate_number] = validated_doctor.doctor_id
            
            # Add trainings
            for training in validated_doctor.training:
                train = Training(
                    program_name=training.program_name,
                    institution=training.institution,
                    completion_year=training.completion_year,
                    doctor=doctor
                )
                db.session.add(train)
            
            # Add employments
            for employment in validated_doctor.employment_history:
                emp = Employment(
                    employer_name=employment.employer_name,
                    role=employment.role,
                    years=employment.years,
                    doctor=doctor
                )
                db.session.add(emp)
            
            # Add disciplinary actions
            for action in validated_doctor.disciplinary_actions:
                disc = DisciplinaryAction(data=action, doctor=doctor)
                db.session.add(disc)
            
            # Add malpractice cases
            for case in validated_doctor.malpractice_cases:
                malpractice = MalpracticeCase(data=case, doctor=doctor)
                db.session.add(malpractice)
            
            db.session.add(degree)
            db.session.add(doctor)
            LICENSE_INDEX[validated_doctor.license_number] = validated_doctor.doctor_id
            added_ids.append(validated_doctor.doctor_id)
        
        db.session.commit()
        
        return jsonify({
            'message': f'Batch processed. {len(added_ids)} doctors added.',
            'doctor_ids': added_ids
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@doctor_bp.route('/psv/license/status', methods=['GET'])
def psv_license_status():
    """
    Get license status for a doctor
    ---
    tags:
      - Doctor PSV (Professional Verification)
    parameters:
      - name: license_number
        in: query
        type: string
        required: true
    responses:
      200:
        description: License status retrieved
      404:
        description: License not found
    """
    license_number = request.args.get('license_number')
    
    if not license_number:
        return jsonify({'error': 'license_number parameter required'}), 400
    
    doctor = Doctor.query.filter_by(license_number=license_number).first()
    
    if not doctor:
        return jsonify({'error': 'License not found'}), 404
    
    return jsonify({
        'license_number': license_number,
        'status': doctor.license_status,
        'expiry_date': doctor.license_expiry,
        'issuer': 'State Medical Board',
        'doctor_id': doctor.doctor_id
    }), 200

@doctor_bp.route('/psv/degree/info', methods=['GET'])
def psv_degree_info():
    """
    Get degree information for a doctor
    ---
    tags:
      - Doctor PSV (Professional Verification)
    parameters:
      - name: doctor_id
        in: query
        type: string
        required: true
    responses:
      200:
        description: Degree information retrieved
      404:
        description: Doctor not found
    """
    doctor_id = request.args.get('doctor_id')
    
    if not doctor_id:
        return jsonify({'error': 'doctor_id parameter required'}), 400
    
    doctor = Doctor.query.filter_by(doctor_id=doctor_id).first()
    
    if not doctor:
        return jsonify({'error': 'Doctor not found'}), 404
    
    if not doctor.degrees:
        return jsonify({'error': 'No degree found'}), 404
    
    degree = doctor.degrees[0]
    
    return jsonify({
        'degree_name': degree.degree_name,
        'university': degree.university,
        'year_of_passing': degree.year_of_passing,
        'registration_number': degree.registration_number,
        'verified': True,
        'source_authority': f"{degree.university} Registrar"
    }), 200

@doctor_bp.route('/psv/board-cert/info', methods=['GET'])
def psv_board_cert_info():
    """
    Get board certification information
    ---
    tags:
      - Doctor PSV (Professional Verification)
    parameters:
      - name: certificate_number
        in: query
        type: string
        required: true
    responses:
      200:
        description: Certificate information retrieved
      404:
        description: Certificate not found
    """
    certificate_number = request.args.get('certificate_number')
    
    if not certificate_number:
        return jsonify({'error': 'certificate_number parameter required'}), 400
    
    cert = BoardCertification.query.filter_by(certificate_number=certificate_number).first()
    
    if not cert:
        return jsonify({'error': 'Certificate not found'}), 404
    
    return jsonify({
        'board_name': cert.board_name,
        'certificate_number': certificate_number,
        'valid_till': cert.valid_till,
        'verified': True
    }), 200

@doctor_bp.route('/psv/training/info', methods=['GET'])
def psv_training_info():
    """
    Get training information for a doctor
    ---
    tags:
      - Doctor PSV (Professional Verification)
    parameters:
      - name: doctor_id
        in: query
        type: string
        required: true
    responses:
      200:
        description: Training information retrieved
      404:
        description: Doctor not found
    """
    doctor_id = request.args.get('doctor_id')
    
    if not doctor_id:
        return jsonify({'error': 'doctor_id parameter required'}), 400
    
    doctor = Doctor.query.filter_by(doctor_id=doctor_id).first()
    
    if not doctor:
        return jsonify({'error': 'Doctor not found'}), 404
    
    training_list = doctor.trainings
    
    if not training_list:
        return jsonify({'verified': False}), 200
    
    t = training_list[0]
    
    return jsonify({
        'program_name': t.program_name,
        'institution': t.institution,
        'completion_year': t.completion_year,
        'verified': True
    }), 200

@doctor_bp.route('/psv/employment/info', methods=['GET'])
def psv_employment_info():
    """
    Get employment history for a doctor
    ---
    tags:
      - Doctor PSV (Professional Verification)
    parameters:
      - name: doctor_id
        in: query
        type: string
        required: true
    responses:
      200:
        description: Employment information retrieved
      404:
        description: Doctor not found
    """
    doctor_id = request.args.get('doctor_id')
    
    if not doctor_id:
        return jsonify({'error': 'doctor_id parameter required'}), 400
    
    doctor = Doctor.query.filter_by(doctor_id=doctor_id).first()
    
    if not doctor:
        return jsonify({'error': 'Doctor not found'}), 404
    
    employment_details = [e.to_dict() for e in doctor.employments]
    
    return jsonify({
        'employment_details': employment_details,
        'verified': True
    }), 200

@doctor_bp.route('/psv/disciplines/check', methods=['GET'])
def psv_disciplines_check():
    """
    Check disciplinary actions for a doctor
    ---
    tags:
      - Doctor PSV (Professional Verification)
    parameters:
      - name: license_number
        in: query
        type: string
        required: true
    responses:
      200:
        description: Disciplinary check result
      404:
        description: License not found
    """
    license_number = request.args.get('license_number')
    
    if not license_number:
        return jsonify({'error': 'license_number parameter required'}), 400
    
    doctor = Doctor.query.filter_by(license_number=license_number).first()
    
    if not doctor:
        return jsonify({'error': 'License not found'}), 404
    
    records = [d.to_dict() for d in doctor.disciplinary_actions]
    
    return jsonify({
        'has_disciplinary_action': len(records) > 0,
        'records': records
    }), 200

@doctor_bp.route('/psv/malpractice/history', methods=['GET'])
def psv_malpractice_history():
    """
    Get malpractice history for a doctor
    ---
    tags:
      - Doctor PSV (Professional Verification)
    parameters:
      - name: doctor_id
        in: query
        type: string
        required: true
    responses:
      200:
        description: Malpractice history retrieved
      404:
        description: Doctor not found
    """
    doctor_id = request.args.get('doctor_id')
    
    if not doctor_id:
        return jsonify({'error': 'doctor_id parameter required'}), 400
    
    doctor = Doctor.query.filter_by(doctor_id=doctor_id).first()
    
    if not doctor:
        return jsonify({'error': 'Doctor not found'}), 404
    
    cases = [mc.to_dict() for mc in doctor.malpractice_cases]
    
    return jsonify({
        'has_malpractice_history': len(cases) > 0,
        'cases': cases
    }), 200

@doctor_bp.route('/psv/verify', methods=['GET'])
def psv_generic_verify():
    """
    Generic verification endpoint
    ---
    tags:
      - Doctor PSV (Professional Verification)
    parameters:
      - name: type
        in: query
        type: string
        required: true
      - name: value
        in: query
        type: string
        required: true
    responses:
      200:
        description: Generic verification result
    """
    verify_type = request.args.get('type')
    value = request.args.get('value')
    
    if not verify_type or not value:
        return jsonify({'error': 'type and value parameters required'}), 400
    
    return jsonify({
        'verified': True,
        'confidence': 0.87,
        'type': verify_type,
        'value': value
    }), 200
