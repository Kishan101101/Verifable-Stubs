from app.core.database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON, Text


class ComplianceRecord(Base):
    """Generic record to persist compliance API requests and results."""
    __tablename__ = "compliance_records"

    id = Column(Integer, primary_key=True)
    request_id = Column(String(100), unique=True, nullable=False, index=True)
    check_type = Column(String(100), nullable=False, index=True)  # e.g. sanctions, pep, gdpr, pci, hipaa, iso27001
    status = Column(String(50), nullable=False, default="pending")
    request_payload = Column(JSON, nullable=True)
    response_payload = Column(JSON, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    def to_dict(self):
        return {
            "request_id": self.request_id,
            "check_type": self.check_type,
            "status": self.status,
            "request_payload": self.request_payload,
            "response_payload": self.response_payload,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
