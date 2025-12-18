from app.core.database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

class StudentSeed(Base):
    """Student model for academic processing"""
    __tablename__ = 'student_seeds'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    dob = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    academic_records = relationship('AcademicRecord', backref='student', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'student_id': self.student_id,
            'name': self.name,
            'dob': self.dob,
            'academic_records': [ar.to_dict() for ar in self.academic_records]
        }

class AcademicRecord(Base):
    """Academic record for student"""
    __tablename__ = 'academic_records'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student_seeds.id'), nullable=False)
    level = Column(String(50), nullable=False)  # 10th, 12th, Graduation
    board = Column(String(255), nullable=False)
    roll_number = Column(String(255), nullable=False, index=True)
    year_of_passing = Column(String(50), nullable=False)
    marks = Column(Float, nullable=False)
    certificate_number = Column(String(255), unique=True, nullable=False, index=True)
    
    def to_dict(self):
        return {
            'level': self.level,
            'board': self.board,
            'roll_number': self.roll_number,
            'year_of_passing': self.year_of_passing,
            'marks': self.marks,
            'certificate_number': self.certificate_number
        }

class EligibilityRule(Base):
    """Eligibility rules for programs"""
    __tablename__ = 'eligibility_rules'
    
    id = Column(Integer, primary_key=True)
    program = Column(String(255), unique=True, nullable=False, index=True)
    min_marks = Column(Float, nullable=False)
    age_limit = Column(Integer, nullable=True)
    category_specific = Column(JSON, nullable=True)  # e.g., {"OBC": 55, "SC": 50}
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'program': self.program,
            'min_marks': self.min_marks,
            'age_limit': self.age_limit,
            'category_specific': self.category_specific
        }

class MeritRule(Base):
    """Merit calculation rules"""
    __tablename__ = 'merit_rules'
    
    id = Column(Integer, primary_key=True)
    program = Column(String(255), unique=True, nullable=False, index=True)
    weightage = Column(JSON, nullable=False)  # e.g., {"12th_marks": 0.7, "graduation_marks": 0.3}
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'program': self.program,
            'weightage': self.weightage
        }

