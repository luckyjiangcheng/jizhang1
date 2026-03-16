from sqlalchemy import Column, String, DateTime, Float, Integer, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MEMBER = "member"


class SystemRole(str, enum.Enum):
    ROOT = "root"
    USER = "user"


class AccountType(str, enum.Enum):
    PERSONAL = "personal"
    FAMILY = "family"


class LicenseCodeStatus(str, enum.Enum):
    UNUSED = "unused"
    USED = "used"
    DISABLED = "disabled"


class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, index=True)  # UUID
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(20), unique=True, index=True, nullable=True)
    password_hash = Column(String(255), nullable=False)
    system_role = Column(SQLEnum(SystemRole), default=SystemRole.USER, nullable=False, index=True)
    account_type = Column(SQLEnum(AccountType), default=AccountType.PERSONAL, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    family_memberships = relationship("FamilyMember", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")
    license_codes = relationship("LicenseCode", back_populates="user")


class Family(Base):
    __tablename__ = "families"
    
    id = Column(String(36), primary_key=True, index=True)  # UUID
    name = Column(String(100), nullable=False)
    creator_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    members = relationship("FamilyMember", back_populates="family")
    transactions = relationship("Transaction", back_populates="family")


class FamilyMember(Base):
    __tablename__ = "family_members"
    
    id = Column(String(36), primary_key=True, index=True)  # UUID
    family_id = Column(String(36), ForeignKey("families.id"), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    role = Column(SQLEnum(UserRole), default=UserRole.MEMBER, nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    family = relationship("Family", back_populates="members")
    user = relationship("User", back_populates="family_memberships")


class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(String(36), primary_key=True, index=True)  # UUID
    family_id = Column(String(36), ForeignKey("families.id"), nullable=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    license_code_id = Column(String(36), ForeignKey("license_codes.id"), nullable=True, index=True)
    date = Column(DateTime, nullable=False, index=True)
    time = Column(String(5))  # HH:MM格式
    amount = Column(Float, nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)
    item = Column(String(200))
    merchant = Column(String(200))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True, index=True)
    
    family = relationship("Family", back_populates="transactions")
    user = relationship("User", back_populates="transactions")
    license_code = relationship("LicenseCode", back_populates="transactions")


class LicenseCode(Base):
    __tablename__ = "license_codes"
    
    id = Column(String(36), primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    code = Column(String(32), unique=True, nullable=False, index=True)
    status = Column(SQLEnum(LicenseCodeStatus), default=LicenseCodeStatus.UNUSED, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    used_at = Column(DateTime, nullable=True)
    
    user = relationship("User", back_populates="license_codes")
    transactions = relationship("Transaction", back_populates="license_code")


class Budget(Base):
    __tablename__ = "budgets"
    
    id = Column(String(36), primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    family_id = Column(String(36), ForeignKey("families.id"), nullable=True, index=True)
    category = Column(String(50), nullable=True)  # None表示总预算，有值表示分类预算
    amount = Column(Float, nullable=False)  # 预算金额
    period = Column(String(20), default="monthly")  # monthly, weekly, yearly
    year = Column(Integer, nullable=False)  # 年份
    month = Column(Integer, nullable=True)  # 月份（月度预算时使用）
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    user = relationship("User")
    family = relationship("Family")
