"""Family edition support

Revision ID: 002
Revises: 001
Create Date: 2026-03-15

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        'transactions',
        'family_id',
        existing_type=sa.String(length=36),
        nullable=True
    )

    op.add_column('transactions', sa.Column('deleted_at', sa.DateTime(), nullable=True))
    op.create_index('ix_transactions_deleted_at', 'transactions', ['deleted_at'])

    op.create_table(
        'budgets',
        sa.Column('id', sa.String(36), primary_key=True, comment='预算唯一标识'),
        sa.Column('user_id', sa.String(36), nullable=False, comment='用户ID'),
        sa.Column('family_id', sa.String(36), nullable=True, comment='家庭ID'),
        sa.Column('category', sa.String(50), nullable=True, comment='分类'),
        sa.Column('amount', sa.Float(), nullable=False, comment='预算金额'),
        sa.Column('period', sa.String(20), nullable=False, comment='预算周期'),
        sa.Column('year', sa.Integer(), nullable=False, comment='年份'),
        sa.Column('month', sa.Integer(), nullable=True, comment='月份'),
        sa.Column('created_at', sa.DateTime(), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(), nullable=False, comment='更新时间'),
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_unicode_ci'
    )

    op.create_index('ix_budgets_id', 'budgets', ['id'])
    op.create_index('ix_budgets_user_id', 'budgets', ['user_id'])
    op.create_index('ix_budgets_family_id', 'budgets', ['family_id'])


def downgrade() -> None:
    op.drop_index('ix_budgets_family_id', 'budgets')
    op.drop_index('ix_budgets_user_id', 'budgets')
    op.drop_index('ix_budgets_id', 'budgets')
    op.drop_table('budgets')

    op.drop_index('ix_transactions_deleted_at', 'transactions')
    op.drop_column('transactions', 'deleted_at')

    op.alter_column(
        'transactions',
        'family_id',
        existing_type=sa.String(length=36),
        nullable=False
    )

