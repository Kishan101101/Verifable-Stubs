"""External compliance tables

Revision ID: 003_external_compliance
Revises: 002_compliance
Create Date: 2024-12-22

"""
from alembic import op
import sqlalchemy as sa

revision = '003_external_compliance'
down_revision = '002_compliance'
branch_labels = None
depends_on = None


def upgrade():
    # Create regulations table
    op.create_table(
        'regulations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('regulation_id', sa.String(50), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('code', sa.String(50), nullable=False),
        sa.Column('category', sa.String(100), nullable=True),
        sa.Column('jurisdiction', sa.String(50), nullable=True),
        sa.Column('version', sa.String(20), nullable=True),
        sa.Column('effective_date', sa.Date(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('required_fields', sa.JSON(), nullable=True),
        sa.Column('key_articles', sa.JSON(), nullable=True),
        sa.Column('compliance_checklist', sa.JSON(), nullable=True),
        sa.Column('penalties', sa.JSON(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('regulation_id')
    )
    op.create_index('idx_regulations_code', 'regulations', ['code'])
    op.create_index('idx_regulations_category', 'regulations', ['category'])
    op.create_index('idx_regulations_jurisdiction', 'regulations', ['jurisdiction'])

    # Create sanctions_entries table
    op.create_table(
        'sanctions_entries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('entry_id', sa.String(50), nullable=False),
        sa.Column('list_type', sa.String(50), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('aliases', sa.JSON(), nullable=True),
        sa.Column('entity_type', sa.String(50), nullable=True),
        sa.Column('country', sa.String(10), nullable=True),
        sa.Column('program', sa.String(100), nullable=True),
        sa.Column('listing_date', sa.Date(), nullable=True),
        sa.Column('reason', sa.Text(), nullable=True),
        sa.Column('additional_info', sa.JSON(), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('entry_id')
    )
    op.create_index('idx_sanctions_list_type', 'sanctions_entries', ['list_type'])
    op.create_index('idx_sanctions_name', 'sanctions_entries', ['name'])
    op.create_index('idx_sanctions_country', 'sanctions_entries', ['country'])

    # Create fraud_patterns table
    op.create_table(
        'fraud_patterns',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('pattern_id', sa.String(150), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('category', sa.String(100), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('indicators', sa.JSON(), nullable=True),
        sa.Column('risk_score_threshold', sa.Integer(), nullable=True),
        sa.Column('action', sa.String(50), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('pattern_id')
    )
    op.create_index('idx_fraud_patterns_category', 'fraud_patterns', ['category'])


def downgrade():
    op.drop_table('fraud_patterns')
    op.drop_table('sanctions_entries')
    op.drop_table('regulations')
