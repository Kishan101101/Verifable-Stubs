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


class HospitalVerification(Base):
    """Hospital registration verification requests"""
    __tablename__ = 'hospital_verifications'
    
    id = Column(Integer, primary_key=True)
    registration_number = Column(String(255), nullable=False, unique=True)
    hospital_name = Column(String(255), nullable=False)
    verified = Column(Boolean, default=False)
    verified_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'registration_number': self.registration_number,
            'hospital_name': self.hospital_name,
            'verified': self.verified,
            'verified_at': self.verified_at.isoformat() if self.verified_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class PatientVerification(Base):
    """Patient identity verification requests"""
    __tablename__ = 'patient_verifications'
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(String(255), nullable=False, unique=True)
    aadhar_last4 = Column(String(4), nullable=False)
    full_name = Column(String(255), nullable=False)
    date_of_birth = Column(String(10), nullable=False)
    gender = Column(String(10), nullable=False)
    verified = Column(Boolean, default=False)
    verified_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'patient_id': self.patient_id,
            'aadhar_last4': self.aadhar_last4,
            'full_name': self.full_name,
            'date_of_birth': self.date_of_birth,
            'gender': self.gender,
            'verified': self.verified,
            'verified_at': self.verified_at.isoformat() if self.verified_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

