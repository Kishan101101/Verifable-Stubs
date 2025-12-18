from app.core.database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

class Doctor(Base):
    """Doctor model for storing doctor information"""
    __tablename__ = 'doctors'
    
    id = Column(Integer, primary_key=True)
    doctor_id = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    license_number = Column(String(255), unique=True, nullable=False, index=True)
    license_status = Column(String(50), nullable=False)  # Active, Inactive, Suspended
    license_expiry = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    degrees = relationship('Degree', backref='doctor', lazy=True, cascade='all, delete-orphan')
    board_certifications = relationship('BoardCertification', backref='doctor', lazy=True, cascade='all, delete-orphan')
    trainings = relationship('Training', backref='doctor', lazy=True, cascade='all, delete-orphan')
    employments = relationship('Employment', backref='doctor', lazy=True, cascade='all, delete-orphan')
    disciplinary_actions = relationship('DisciplinaryAction', backref='doctor', lazy=True, cascade='all, delete-orphan')
    malpractice_cases = relationship('MalpracticeCase', backref='doctor', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'doctor_id': self.doctor_id,
            'name': self.name,
            'license_number': self.license_number,
            'license_status': self.license_status,
            'license_expiry': self.license_expiry,
            'degree': [d.to_dict() for d in self.degrees],
            'board_certifications': [bc.to_dict() for bc in self.board_certifications],
            'training': [t.to_dict() for t in self.trainings],
            'employment_history': [e.to_dict() for e in self.employments],
            'disciplinary_actions': [da.to_dict() for da in self.disciplinary_actions],
            'malpractice_cases': [mc.to_dict() for mc in self.malpractice_cases],
        }

class Degree(Base):
    """Doctor's degree information"""
    __tablename__ = 'degrees'
    
    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id'), nullable=False)
    degree_name = Column(String(255), nullable=False)
    university = Column(String(255), nullable=False)
    year_of_passing = Column(String(50), nullable=False)
    registration_number = Column(String(255), nullable=False)
    
    def to_dict(self):
        return {
            'degree_name': self.degree_name,
            'university': self.university,
            'year_of_passing': self.year_of_passing,
            'registration_number': self.registration_number
        }

class BoardCertification(Base):
    """Doctor's board certification"""
    __tablename__ = 'board_certifications'
    
    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id'), nullable=False)
    board_name = Column(String(255), nullable=False)
    certificate_number = Column(String(255), unique=True, nullable=False, index=True)
    valid_till = Column(String(50), nullable=False)
    
    def to_dict(self):
        return {
            'board_name': self.board_name,
            'certificate_number': self.certificate_number,
            'valid_till': self.valid_till
        }

class Training(Base):
    """Doctor's training information"""
    __tablename__ = 'trainings'
    
    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id'), nullable=False)
    program_name = Column(String(255), nullable=False)
    institution = Column(String(255), nullable=False)
    completion_year = Column(String(50), nullable=False)
    
    def to_dict(self):
        return {
            'program_name': self.program_name,
            'institution': self.institution,
            'completion_year': self.completion_year
        }

class Employment(Base):
    """Doctor's employment history"""
    __tablename__ = 'employments'
    
    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id'), nullable=False)
    employer_name = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)
    years = Column(String(50), nullable=False)
    
    def to_dict(self):
        return {
            'employer_name': self.employer_name,
            'role': self.role,
            'years': self.years
        }

class DisciplinaryAction(Base):
    """Doctor's disciplinary actions"""
    __tablename__ = 'disciplinary_actions'
    
    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id'), nullable=False)
    data = Column(JSON, nullable=False)
    
    def to_dict(self):
        return self.data

class MalpracticeCase(Base):
    """Doctor's malpractice cases"""
    __tablename__ = 'malpractice_cases'
    
    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id'), nullable=False)
    data = Column(JSON, nullable=False)
    
    def to_dict(self):
        return self.data
