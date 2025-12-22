"""
Compliance Models
Database models for compliance records, regulations, sanctions, and fraud patterns
"""
from app.core.database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON, Text, Boolean, Date


class ComplianceRecord(Base):
    """Generic record to persist compliance API requests and results."""
    __tablename__ = "compliance_records"

    id = Column(Integer, primary_key=True)
    request_id = Column(String(100), unique=True, nullable=False, index=True)
    check_type = Column(String(100), nullable=False, index=True)
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


class Regulation(Base):
    """Store regulations and compliance requirements"""
    __tablename__ = "regulations"

    id = Column(Integer, primary_key=True)
    regulation_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=False, index=True)
    category = Column(String(100), nullable=True, index=True)
    jurisdiction = Column(String(50), nullable=True, index=True)
    version = Column(String(20), nullable=True)
    effective_date = Column(Date, nullable=True)
    description = Column(Text, nullable=True)
    required_fields = Column(JSON, nullable=True)
    key_articles = Column(JSON, nullable=True)
    compliance_checklist = Column(JSON, nullable=True)
    penalties = Column(JSON, nullable=True)
    tags = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "regulation_id": self.regulation_id,
            "name": self.name,
            "code": self.code,
            "category": self.category,
            "jurisdiction": self.jurisdiction,
            "version": self.version,
            "effective_date": self.effective_date.isoformat() if self.effective_date else None,
            "description": self.description,
            "required_fields": self.required_fields,
            "key_articles": self.key_articles,
            "compliance_checklist": self.compliance_checklist,
            "penalties": self.penalties,
            "tags": self.tags,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def to_summary(self):
        return {
            "regulation_id": self.regulation_id,
            "name": self.name,
            "code": self.code,
            "category": self.category,
            "jurisdiction": self.jurisdiction,
        }


class SanctionsEntry(Base):
    """Store sanctions list entries (OFAC, EU, UN, PEP)"""
    __tablename__ = "sanctions_entries"

    id = Column(Integer, primary_key=True)
    entry_id = Column(String(50), unique=True, nullable=False, index=True)
    list_type = Column(String(50), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    aliases = Column(JSON, nullable=True)
    entity_type = Column(String(50), nullable=True)
    country = Column(String(10), nullable=True, index=True)
    program = Column(String(100), nullable=True)
    listing_date = Column(Date, nullable=True)
    reason = Column(Text, nullable=True)
    additional_info = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "entry_id": self.entry_id,
            "list_type": self.list_type,
            "name": self.name,
            "aliases": self.aliases,
            "entity_type": self.entity_type,
            "country": self.country,
            "program": self.program,
            "listing_date": self.listing_date.isoformat() if self.listing_date else None,
            "reason": self.reason,
            "additional_info": self.additional_info,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class FraudPattern(Base):
    """Store fraud patterns and detection rules"""
    __tablename__ = "fraud_patterns"

    id = Column(Integer, primary_key=True)
    pattern_id = Column(String(150), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=True, index=True)
    description = Column(Text, nullable=True)
    indicators = Column(JSON, nullable=True)
    risk_score_threshold = Column(Integer, nullable=True)
    action = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "pattern_id": self.pattern_id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "indicators": self.indicators,
            "risk_score_threshold": self.risk_score_threshold,
            "action": self.action,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
