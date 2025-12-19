"""Add compliance_records table

Revision ID: 002_compliance
Revises: 001_initial
Create Date: 2025-12-19 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002_compliance'
down_revision = '001_initial'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'compliance_records',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('request_id', sa.String(100), nullable=False, unique=True),
        sa.Column('check_type', sa.String(100), nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('request_payload', sa.JSON(), nullable=True),
        sa.Column('response_payload', sa.JSON(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_compliance_records_request_id'), 'compliance_records', ['request_id'], unique=True)
    op.create_index(op.f('ix_compliance_records_check_type'), 'compliance_records', ['check_type'])


def downgrade():
    op.drop_index(op.f('ix_compliance_records_check_type'), table_name='compliance_records')
    op.drop_index(op.f('ix_compliance_records_request_id'), table_name='compliance_records')
    op.drop_table('compliance_records')
