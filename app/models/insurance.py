from app.core.database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, Numeric, JSON

class MedicalEnrichmentRequest(Base):
    """Medical data enrichment requests"""
    __tablename__ = 'medical_enrichment_requests'
    
    id = Column(Integer, primary_key=True)
    diagnosis = Column(String(255), nullable=False)
    hospital_name = Column(String(255), nullable=False)
    icd_mapping = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'diagnosis': self.diagnosis,
            'hospital_name': self.hospital_name,
            'icd_mapping': self.icd_mapping,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class ReviewerRequest(Base):
    """Reviewer assignment requests"""
    __tablename__ = 'reviewer_requests'
    
    id = Column(Integer, primary_key=True)
    workflow_state = Column(JSON, nullable=False)  # Dict with workflow state
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'workflow_state': self.workflow_state,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class PayoutRequest(Base):
    """Payout request information"""
    __tablename__ = 'payout_requests'
    
    id = Column(Integer, primary_key=True)
    approved_amount = Column(Numeric(10, 2), nullable=False)
    deductible = Column(Numeric(10, 2), nullable=False)
    policy_limit = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'approved_amount': float(self.approved_amount),
            'deductible': float(self.deductible),
            'policy_limit': float(self.policy_limit),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class NotificationRequest(Base):
    """Notification requests"""
    __tablename__ = 'notification_requests'
    
    id = Column(Integer, primary_key=True)
    recipient_email = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
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

