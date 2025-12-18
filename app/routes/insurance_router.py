from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.insurance import (
    MedicalEnrichmentRequest, ReviewerRequest, PayoutRequest, NotificationRequest
)
from app.schemas.insurance_schema import (
    MedicalEnrichmentRequestSchema, ReviewerRequestSchema, 
    PayoutRequestSchema, NotificationRequestSchema
)

router = APIRouter()

# ICD mapping reference data
ICD_MAP = {
    "diabetes": ("E11.9", "Type 2 diabetes mellitus"),
    "hypertension": ("I10", "Essential hypertension"),
    "asthma": ("J45.909", "Unspecified asthma"),
}

@router.post('/admin/medical-enrichment')
def add_medical_enrichment(data: MedicalEnrichmentRequestSchema, db: Session = Depends(get_db)):
    """Admin endpoint to add medical enrichment requests"""
    try:
        # Map diagnosis to ICD code
        diagnosis_lower = data.diagnosis.lower()
        icd_mapping = None
        
        for key, (icd_code, description) in ICD_MAP.items():
            if key in diagnosis_lower:
                icd_mapping = {"icd_code": icd_code, "description": description}
                break
        
        req = MedicalEnrichmentRequest(
            diagnosis=data.diagnosis,
            hospital_name=data.hospital_name,
            icd_mapping=icd_mapping
        )
        
        db.add(req)
        db.commit()
        
        return {
            'id': req.id,
            'diagnosis': req.diagnosis,
            'hospital_name': req.hospital_name,
            'icd_mapping': req.icd_mapping,
            'message': 'Medical enrichment request added'
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/admin/reviewer-request')
def add_reviewer_request(data: ReviewerRequestSchema, db: Session = Depends(get_db)):
    """Admin endpoint to create reviewer assignment requests"""
    try:
        req = ReviewerRequest(workflow_state=data.workflow_state)
        
        db.add(req)
        db.commit()
        
        return {
            'id': req.id,
            'workflow_state': req.workflow_state,
            'message': 'Reviewer request created'
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/admin/payout-request')
def add_payout_request(data: PayoutRequestSchema, db: Session = Depends(get_db)):
    """Admin endpoint to create payout requests"""
    try:
        req = PayoutRequest(
            approved_amount=data.approved_amount,
            deductible=data.deductible,
            policy_limit=data.policy_limit
        )
        
        db.add(req)
        db.commit()
        
        return {
            'id': req.id,
            'approved_amount': float(req.approved_amount),
            'deductible': float(req.deductible),
            'policy_limit': float(req.policy_limit),
            'message': 'Payout request created'
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/admin/notification')
def send_notification(data: NotificationRequestSchema, db: Session = Depends(get_db)):
    """Admin endpoint to send notifications"""
    try:
        req = NotificationRequest(
            recipient_email=data.recipient_email,
            subject=data.subject,
            message=data.message,
            sent=True  # In a real app, this would be sent via email service
        )
        
        db.add(req)
        db.commit()
        
        return {
            'id': req.id,
            'recipient_email': req.recipient_email,
            'subject': req.subject,
            'message': req.message,
            'sent': req.sent,
            'response_message': 'Notification sent successfully'
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/medical/enrich')
def medical_data_enrichment(data: MedicalEnrichmentRequestSchema):
    """Endpoint for medical data enrichment"""
    try:
        # Map diagnosis to ICD code
        diagnosis_lower = data.diagnosis.lower()
        icd_code = "UNKNOWN"
        description = "Unknown diagnosis"
        
        for key, (code, desc) in ICD_MAP.items():
            if key in diagnosis_lower:
                icd_code = code
                description = desc
                break
        
        return {
            'diagnosis': data.diagnosis,
            'icd_code': icd_code,
            'description': description,
            'hospital_name': data.hospital_name,
            'verified': True
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/claims/review')
def claim_review(claim_id: str, status: str = "pending"):
    """Endpoint to review insurance claims"""
    try:
        return {
            'claim_id': claim_id,
            'status': status,
            'message': f'Claim {claim_id} review recorded',
            'reviewed_at': None
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/payout/process')
def process_payout(claim_id: str, payout_amount: float = 0):
    """Endpoint to process payout"""
    try:
        return {
            'claim_id': claim_id,
            'payout_amount': payout_amount,
            'status': 'processed',
            'message': f'Payout of {payout_amount} processed for claim {claim_id}'
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/notification/send')
def send_notification_endpoint(data: NotificationRequestSchema):
    """Endpoint to send notification"""
    try:
        return {
            'recipient_email': data.recipient_email,
            'subject': data.subject,
            'status': 'sent',
            'message': 'Notification sent successfully'
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
