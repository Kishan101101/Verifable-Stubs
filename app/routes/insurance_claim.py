from flask import Blueprint, request, jsonify
from app import db
from app.models.insurance import (
    MedicalEnrichmentRequest, ReviewerRequest, PayoutRequest, NotificationRequest
)
from app.schemas.insurance_schema import (
    MedicalEnrichmentRequestSchema, ReviewerRequestSchema, 
    PayoutRequestSchema, NotificationRequestSchema
)

insurance_bp = Blueprint('insurance', __name__)

# ICD mapping reference data
ICD_MAP = {
    "diabetes": ("E11.9", "Type 2 diabetes mellitus"),
    "hypertension": ("I10", "Essential hypertension"),
    "asthma": ("J45.909", "Unspecified asthma"),
}

@insurance_bp.route('/admin/medical-enrichment', methods=['POST'])
def add_medical_enrichment():
    """
    Admin endpoint to add medical enrichment requests
    ---
    tags:
      - Insurance Admin
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/MedicalEnrichmentRequestSchema'
    responses:
      200:
        description: Medical enrichment request added
      400:
        description: Invalid request
    """
    try:
        data = request.get_json()
        validated_req = MedicalEnrichmentRequestSchema(**data)
        
        # Map diagnosis to ICD code
        diagnosis_lower = validated_req.diagnosis.lower()
        icd_mapping = None
        
        for key, (icd_code, description) in ICD_MAP.items():
            if key in diagnosis_lower:
                icd_mapping = {"icd_code": icd_code, "description": description}
                break
        
        req = MedicalEnrichmentRequest(
            diagnosis=validated_req.diagnosis,
            hospital_name=validated_req.hospital_name,
            icd_mapping=icd_mapping
        )
        
        db.session.add(req)
        db.session.commit()
        
        return jsonify({
            'id': req.id,
            'diagnosis': req.diagnosis,
            'hospital_name': req.hospital_name,
            'icd_mapping': req.icd_mapping,
            'message': 'Medical enrichment request added'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@insurance_bp.route('/admin/reviewer-request', methods=['POST'])
def add_reviewer_request():
    """
    Admin endpoint to create reviewer assignment requests
    ---
    tags:
      - Insurance Admin
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/ReviewerRequestSchema'
    responses:
      200:
        description: Reviewer request created
      400:
        description: Invalid request
    """
    try:
        data = request.get_json()
        validated_req = ReviewerRequestSchema(**data)
        
        req = ReviewerRequest(workflow_state=validated_req.workflow_state)
        
        db.session.add(req)
        db.session.commit()
        
        return jsonify({
            'id': req.id,
            'workflow_state': req.workflow_state,
            'message': 'Reviewer request created'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@insurance_bp.route('/admin/payout-request', methods=['POST'])
def add_payout_request():
    """
    Admin endpoint to create payout requests
    ---
    tags:
      - Insurance Admin
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/PayoutRequestSchema'
    responses:
      200:
        description: Payout request created
      400:
        description: Invalid request
    """
    try:
        data = request.get_json()
        validated_req = PayoutRequestSchema(**data)
        
        req = PayoutRequest(
            approved_amount=validated_req.approved_amount,
            deductible=validated_req.deductible,
            policy_limit=validated_req.policy_limit
        )
        
        db.session.add(req)
        db.session.commit()
        
        return jsonify({
            'id': req.id,
            'approved_amount': float(req.approved_amount),
            'deductible': float(req.deductible),
            'policy_limit': float(req.policy_limit),
            'message': 'Payout request created'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@insurance_bp.route('/admin/notification', methods=['POST'])
def send_notification():
    """
    Admin endpoint to send notifications
    ---
    tags:
      - Insurance Admin
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/NotificationRequestSchema'
    responses:
      200:
        description: Notification sent
      400:
        description: Invalid request
    """
    try:
        data = request.get_json()
        validated_req = NotificationRequestSchema(**data)
        
        req = NotificationRequest(
            recipient_email=validated_req.recipient_email,
            subject=validated_req.subject,
            message=validated_req.message,
            sent=True  # In a real app, this would be sent via email service
        )
        
        db.session.add(req)
        db.session.commit()
        
        return jsonify({
            'id': req.id,
            'recipient_email': req.recipient_email,
            'subject': req.subject,
            'message': req.message,
            'sent': req.sent,
            'response_message': 'Notification sent successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@insurance_bp.route('/medical/enrich', methods=['POST'])
def medical_data_enrichment():
    """
    Endpoint for medical data enrichment
    ---
    tags:
      - Insurance Medical Data
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/MedicalEnrichmentRequestSchema'
    responses:
      200:
        description: Medical data enriched
      400:
        description: Invalid request
    """
    try:
        data = request.get_json()
        validated_req = MedicalEnrichmentRequestSchema(**data)
        
        # Map diagnosis to ICD code
        diagnosis_lower = validated_req.diagnosis.lower()
        icd_code = "UNKNOWN"
        description = "Unknown diagnosis"
        
        for key, (code, desc) in ICD_MAP.items():
            if key in diagnosis_lower:
                icd_code = code
                description = desc
                break
        
        return jsonify({
            'diagnosis': validated_req.diagnosis,
            'icd_code': icd_code,
            'description': description,
            'hospital_name': validated_req.hospital_name,
            'verified': True
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@insurance_bp.route('/claims/review', methods=['POST'])
def claim_review():
    """
    Endpoint to review insurance claims
    ---
    tags:
      - Insurance Claims
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            claim_id:
              type: string
            status:
              type: string
              enum: ['approved', 'denied', 'pending']
    responses:
      200:
        description: Claim review result
    """
    try:
        data = request.get_json()
        claim_id = data.get('claim_id')
        status = data.get('status', 'pending')
        
        return jsonify({
            'claim_id': claim_id,
            'status': status,
            'message': f'Claim {claim_id} review recorded',
            'reviewed_at': None
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@insurance_bp.route('/payout/process', methods=['POST'])
def process_payout():
    """
    Endpoint to process payout
    ---
    tags:
      - Insurance Payout
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            claim_id:
              type: string
            payout_amount:
              type: number
    responses:
      200:
        description: Payout processed
    """
    try:
        data = request.get_json()
        claim_id = data.get('claim_id')
        payout_amount = data.get('payout_amount', 0)
        
        return jsonify({
            'claim_id': claim_id,
            'payout_amount': payout_amount,
            'status': 'processed',
            'message': f'Payout of {payout_amount} processed for claim {claim_id}'
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@insurance_bp.route('/notification/send', methods=['POST'])
def send_notification_endpoint():
    """
    Endpoint to send notification
    ---
    tags:
      - Insurance Notification
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/NotificationRequestSchema'
    responses:
      200:
        description: Notification sent
    """
    try:
        data = request.get_json()
        validated_req = NotificationRequestSchema(**data)
        
        return jsonify({
            'recipient_email': validated_req.recipient_email,
            'subject': validated_req.subject,
            'status': 'sent',
            'message': 'Notification sent successfully'
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
