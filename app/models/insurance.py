from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON

class MedicalEnrichmentRequest(db.Model):
    """Medical data enrichment requests"""
    __tablename__ = 'medical_enrichment_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    diagnosis = db.Column(db.String(255), nullable=False)
    hospital_name = db.Column(db.String(255), nullable=False)
    icd_mapping = db.Column(JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'diagnosis': self.diagnosis,
            'hospital_name': self.hospital_name,
            'icd_mapping': self.icd_mapping,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class ReviewerRequest(db.Model):
    """Reviewer assignment requests"""
    __tablename__ = 'reviewer_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    workflow_state = db.Column(JSON, nullable=False)  # Dict with workflow state
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'workflow_state': self.workflow_state,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class PayoutRequest(db.Model):
    """Payout request information"""
    __tablename__ = 'payout_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    approved_amount = db.Column(db.Numeric(10, 2), nullable=False)
    deductible = db.Column(db.Numeric(10, 2), nullable=False)
    policy_limit = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'approved_amount': float(self.approved_amount),
            'deductible': float(self.deductible),
            'policy_limit': float(self.policy_limit),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class NotificationRequest(db.Model):
    """Notification requests"""
    __tablename__ = 'notification_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    recipient_email = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sent = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'recipient_email': self.recipient_email,
            'subject': self.subject,
            'message': self.message,
            'sent': self.sent,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
