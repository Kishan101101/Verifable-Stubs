from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON

class Doctor(db.Model):
    """Doctor model for storing doctor information"""
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.String(255), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    license_number = db.Column(db.String(255), unique=True, nullable=False, index=True)
    license_status = db.Column(db.String(50), nullable=False)  # Active, Inactive, Suspended
    license_expiry = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    degrees = db.relationship('Degree', backref='doctor', lazy=True, cascade='all, delete-orphan')
    board_certifications = db.relationship('BoardCertification', backref='doctor', lazy=True, cascade='all, delete-orphan')
    trainings = db.relationship('Training', backref='doctor', lazy=True, cascade='all, delete-orphan')
    employments = db.relationship('Employment', backref='doctor', lazy=True, cascade='all, delete-orphan')
    disciplinary_actions = db.relationship('DisciplinaryAction', backref='doctor', lazy=True, cascade='all, delete-orphan')
    malpractice_cases = db.relationship('MalpracticeCase', backref='doctor', lazy=True, cascade='all, delete-orphan')
    
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

class Degree(db.Model):
    """Doctor's degree information"""
    __tablename__ = 'degrees'
    
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    degree_name = db.Column(db.String(255), nullable=False)
    university = db.Column(db.String(255), nullable=False)
    year_of_passing = db.Column(db.String(50), nullable=False)
    registration_number = db.Column(db.String(255), nullable=False)
    
    def to_dict(self):
        return {
            'degree_name': self.degree_name,
            'university': self.university,
            'year_of_passing': self.year_of_passing,
            'registration_number': self.registration_number
        }

class BoardCertification(db.Model):
    """Doctor's board certification"""
    __tablename__ = 'board_certifications'
    
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    board_name = db.Column(db.String(255), nullable=False)
    certificate_number = db.Column(db.String(255), unique=True, nullable=False, index=True)
    valid_till = db.Column(db.String(50), nullable=False)
    
    def to_dict(self):
        return {
            'board_name': self.board_name,
            'certificate_number': self.certificate_number,
            'valid_till': self.valid_till
        }

class Training(db.Model):
    """Doctor's training information"""
    __tablename__ = 'trainings'
    
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    program_name = db.Column(db.String(255), nullable=False)
    institution = db.Column(db.String(255), nullable=False)
    completion_year = db.Column(db.String(50), nullable=False)
    
    def to_dict(self):
        return {
            'program_name': self.program_name,
            'institution': self.institution,
            'completion_year': self.completion_year
        }

class Employment(db.Model):
    """Doctor's employment history"""
    __tablename__ = 'employments'
    
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    employer_name = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable=False)
    years = db.Column(db.String(50), nullable=False)
    
    def to_dict(self):
        return {
            'employer_name': self.employer_name,
            'role': self.role,
            'years': self.years
        }

class DisciplinaryAction(db.Model):
    """Doctor's disciplinary actions"""
    __tablename__ = 'disciplinary_actions'
    
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    data = db.Column(JSON, nullable=False)
    
    def to_dict(self):
        return self.data

class MalpracticeCase(db.Model):
    """Doctor's malpractice cases"""
    __tablename__ = 'malpractice_cases'
    
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    data = db.Column(JSON, nullable=False)
    
    def to_dict(self):
        return self.data
