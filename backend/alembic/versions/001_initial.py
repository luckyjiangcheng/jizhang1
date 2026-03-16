"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2026-03-14

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 创建用户表
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), primary_key=True, comment='用户唯一标识'),
        sa.Column('username', sa.String(50), nullable=False, comment='用户名'),
        sa.Column('email', sa.String(100), nullable=False, comment='邮箱'),
        sa.Column('password_hash', sa.String(255), nullable=False, comment='密码哈希'),
        sa.Column('created_at', sa.DateTime(), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(), nullable=False, comment='更新时间'),
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_unicode_ci'
    )
    
    # 为用户表创建索引
    op.create_index('ix_users_id', 'users', ['id'])
    op.create_index('ix_users_username', 'users', ['username'])
    op.create_index('ix_users_email', 'users', ['email'])
    
    # 创建家庭表
    op.create_table(
        'families',
        sa.Column('id', sa.String(36), primary_key=True, comment='家庭唯一标识'),
        sa.Column('name', sa.String(100), nullable=False, comment='家庭名称'),
        sa.Column('creator_id', sa.String(36), nullable=False, comment='创建者ID'),
        sa.Column('created_at', sa.DateTime(), nullable=False, comment='创建时间'),
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_unicode_ci'
    )
    
    op.create_index('ix_families_id', 'families', ['id'])
    
    # 创建家庭成员表
    op.create_table(
        'family_members',
        sa.Column('id', sa.String(36), primary_key=True, comment='记录唯一标识'),
        sa.Column('family_id', sa.String(36), nullable=False, comment='家庭ID'),
        sa.Column('user_id', sa.String(36), nullable=False, comment='用户ID'),
        sa.Column('role', sa.String(20), nullable=False, comment='角色'),
        sa.Column('joined_at', sa.DateTime(), nullable=False, comment='加入时间'),
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_unicode_ci'
    )
    
    op.create_index('ix_family_members_id', 'family_members', ['id'])
    op.create_index('ix_family_members_family_id', 'family_members', ['family_id'])
    op.create_index('ix_family_members_user_id', 'family_members', ['user_id'])
    
    # 创建交易表
    op.create_table(
        'transactions',
        sa.Column('id', sa.String(36), primary_key=True, comment='交易唯一标识'),
        sa.Column('family_id', sa.String(36), nullable=False, comment='家庭ID'),
        sa.Column('user_id', sa.String(36), nullable=False, comment='录入用户ID'),
        sa.Column('date', sa.DateTime(), nullable=False, comment='交易日期'),
        sa.Column('time', sa.String(5), comment='交易时间'),
        sa.Column('amount', sa.Float(), nullable=False, comment='金额'),
        sa.Column('category', sa.String(50), nullable=False, comment='分类'),
        sa.Column('item', sa.String(200), comment='项目'),
        sa.Column('merchant', sa.String(200), comment='商家'),
        sa.Column('notes', sa.Text(), comment='备注'),
        sa.Column('created_at', sa.DateTime(), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(), nullable=False, comment='更新时间'),
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_unicode_ci'
    )
    
    # 为交易表创建索引
    op.create_index('ix_transactions_id', 'transactions', ['id'])
    op.create_index('ix_transactions_family_id', 'transactions', ['family_id'])
    op.create_index('ix_transactions_user_id', 'transactions', ['user_id'])
    op.create_index('ix_transactions_date', 'transactions', ['date'])
    op.create_index('ix_transactions_amount', 'transactions', ['amount'])
    op.create_index('ix_transactions_category', 'transactions', ['category'])
    op.create_index('ix_transactions_created_at', 'transactions', ['created_at'])


def downgrade() -> None:
    # 删除交易表
    op.drop_index('ix_transactions_created_at', 'transactions')
    op.drop_index('ix_transactions_category', 'transactions')
    op.drop_index('ix_transactions_amount', 'transactions')
    op.drop_index('ix_transactions_date', 'transactions')
    op.drop_index('ix_transactions_user_id', 'transactions')
    op.drop_index('ix_transactions_family_id', 'transactions')
    op.drop_index('ix_transactions_id', 'transactions')
    op.drop_table('transactions')
    
    # 删除家庭成员表
    op.drop_index('ix_family_members_user_id', 'family_members')
    op.drop_index('ix_family_members_family_id', 'family_members')
    op.drop_index('ix_family_members_id', 'family_members')
    op.drop_table('family_members')
    
    # 删除家庭表
    op.drop_index('ix_families_id', 'families')
    op.drop_table('families')
    
    # 删除用户表
    op.drop_index('ix_users_email', 'users')
    op.drop_index('ix_users_username', 'users')
    op.drop_index('ix_users_id', 'users')
    op.drop_table('users')