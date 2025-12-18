"""Initial migration

Revision ID: 001_initial
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Doctor tables
    op.create_table(
        'doctors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('doctor_id', sa.String(255), nullable=False, unique=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('license_number', sa.String(255), nullable=False, unique=True),
        sa.Column('license_status', sa.String(50), nullable=False),
        sa.Column('license_expiry', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_doctors_doctor_id'), 'doctors', ['doctor_id'], unique=True)
    op.create_index(op.f('ix_doctors_license_number'), 'doctors', ['license_number'], unique=True)
    
    op.create_table(
        'degrees',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('doctor_id', sa.Integer(), nullable=False),
        sa.Column('degree_name', sa.String(255), nullable=False),
        sa.Column('university', sa.String(255), nullable=False),
        sa.Column('year_of_passing', sa.String(50), nullable=False),
        sa.Column('registration_number', sa.String(255), nullable=False),
        sa.ForeignKeyConstraint(['doctor_id'], ['doctors.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table(
        'board_certifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('doctor_id', sa.Integer(), nullable=False),
        sa.Column('board_name', sa.String(255), nullable=False),
        sa.Column('certificate_number', sa.String(255), nullable=False, unique=True),
        sa.Column('valid_till', sa.String(50), nullable=False),
        sa.ForeignKeyConstraint(['doctor_id'], ['doctors.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_board_certifications_certificate_number'), 'board_certifications', ['certificate_number'], unique=True)
    
    op.create_table(
        'trainings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('doctor_id', sa.Integer(), nullable=False),
        sa.Column('program_name', sa.String(255), nullable=False),
        sa.Column('institution', sa.String(255), nullable=False),
        sa.Column('completion_year', sa.String(50), nullable=False),
        sa.ForeignKeyConstraint(['doctor_id'], ['doctors.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table(
        'employments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('doctor_id', sa.Integer(), nullable=False),
        sa.Column('employer_name', sa.String(255), nullable=False),
        sa.Column('role', sa.String(255), nullable=False),
        sa.Column('years', sa.String(50), nullable=False),
        sa.ForeignKeyConstraint(['doctor_id'], ['doctors.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table(
        'disciplinary_actions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('doctor_id', sa.Integer(), nullable=False),
        sa.Column('data', sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(['doctor_id'], ['doctors.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table(
        'malpractice_cases',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('doctor_id', sa.Integer(), nullable=False),
        sa.Column('data', sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(['doctor_id'], ['doctors.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Academic tables
    op.create_table(
        'student_seeds',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.String(255), nullable=False, unique=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('dob', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_student_seeds_student_id'), 'student_seeds', ['student_id'], unique=True)
    
    op.create_table(
        'academic_records',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('level', sa.String(50), nullable=False),
        sa.Column('board', sa.String(255), nullable=False),
        sa.Column('roll_number', sa.String(255), nullable=False),
        sa.Column('year_of_passing', sa.String(50), nullable=False),
        sa.Column('marks', sa.Float(), nullable=False),
        sa.Column('certificate_number', sa.String(255), nullable=False, unique=True),
        sa.ForeignKeyConstraint(['student_id'], ['student_seeds.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_academic_records_roll_number'), 'academic_records', ['roll_number'])
    op.create_index(op.f('ix_academic_records_certificate_number'), 'academic_records', ['certificate_number'], unique=True)
    
    op.create_table(
        'eligibility_rules',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('program', sa.String(255), nullable=False, unique=True),
        sa.Column('min_marks', sa.Float(), nullable=False),
        sa.Column('age_limit', sa.Integer(), nullable=True),
        sa.Column('category_specific', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_eligibility_rules_program'), 'eligibility_rules', ['program'], unique=True)
    
    op.create_table(
        'merit_rules',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('program', sa.String(255), nullable=False, unique=True),
        sa.Column('weightage', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_merit_rules_program'), 'merit_rules', ['program'], unique=True)
    
    # Insurance tables
    op.create_table(
        'medical_enrichment_requests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('diagnosis', sa.String(255), nullable=False),
        sa.Column('hospital_name', sa.String(255), nullable=False),
        sa.Column('icd_mapping', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table(
        'reviewer_requests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('workflow_state', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table(
        'payout_requests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('approved_amount', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('deductible', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('policy_limit', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table(
        'notification_requests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('recipient_email', sa.String(255), nullable=False),
        sa.Column('subject', sa.String(255), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('sent', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    # Drop insurance tables
    op.drop_table('notification_requests')
    op.drop_table('payout_requests')
    op.drop_table('reviewer_requests')
    op.drop_table('medical_enrichment_requests')
    
    # Drop academic tables
    op.drop_index(op.f('ix_merit_rules_program'), table_name='merit_rules')
    op.drop_table('merit_rules')
    op.drop_index(op.f('ix_eligibility_rules_program'), table_name='eligibility_rules')
    op.drop_table('eligibility_rules')
    op.drop_index(op.f('ix_academic_records_certificate_number'), table_name='academic_records')
    op.drop_index(op.f('ix_academic_records_roll_number'), table_name='academic_records')
    op.drop_table('academic_records')
    op.drop_index(op.f('ix_student_seeds_student_id'), table_name='student_seeds')
    op.drop_table('student_seeds')
    
    # Drop doctor tables
    op.drop_table('malpractice_cases')
    op.drop_table('disciplinary_actions')
    op.drop_table('employments')
    op.drop_table('trainings')
    op.drop_index(op.f('ix_board_certifications_certificate_number'), table_name='board_certifications')
    op.drop_table('board_certifications')
    op.drop_table('degrees')
    op.drop_index(op.f('ix_doctors_license_number'), table_name='doctors')
    op.drop_index(op.f('ix_doctors_doctor_id'), table_name='doctors')
    op.drop_table('doctors')
