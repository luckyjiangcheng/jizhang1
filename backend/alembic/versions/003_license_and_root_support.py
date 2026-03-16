"""License and root support

Revision ID: 003
Revises: 002
Create Date: 2026-03-15

"""
from alembic import op
import sqlalchemy as sa


revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('system_role', sa.String(length=10), nullable=False, server_default='user'))
    op.add_column('users', sa.Column('account_type', sa.String(length=10), nullable=False, server_default='personal'))
    op.create_index('ix_users_system_role', 'users', ['system_role'])

    op.create_table(
        'license_codes',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('code', sa.String(32), nullable=False),
        sa.Column('status', sa.String(10), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('used_at', sa.DateTime(), nullable=True),
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_unicode_ci'
    )
    op.create_index('ix_license_codes_id', 'license_codes', ['id'])
    op.create_index('ix_license_codes_user_id', 'license_codes', ['user_id'])
    op.create_index('ix_license_codes_code', 'license_codes', ['code'], unique=True)
    op.create_index('ix_license_codes_status', 'license_codes', ['status'])

    op.add_column('transactions', sa.Column('license_code_id', sa.String(length=36), nullable=True))
    op.create_index('ix_transactions_license_code_id', 'transactions', ['license_code_id'])

    op.alter_column('users', 'system_role', server_default=None)
    op.alter_column('users', 'account_type', server_default=None)


def downgrade() -> None:
    op.drop_index('ix_transactions_license_code_id', 'transactions')
    op.drop_column('transactions', 'license_code_id')

    op.drop_index('ix_license_codes_status', 'license_codes')
    op.drop_index('ix_license_codes_code', 'license_codes')
    op.drop_index('ix_license_codes_user_id', 'license_codes')
    op.drop_index('ix_license_codes_id', 'license_codes')
    op.drop_table('license_codes')

    op.drop_index('ix_users_system_role', 'users')
    op.drop_column('users', 'account_type')
    op.drop_column('users', 'system_role')
