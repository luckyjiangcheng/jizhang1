from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional
from datetime import datetime
import uuid


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    phone: str = Field(..., max_length=100)
    password: str


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    phone: Optional[str] = None
    account_type: Optional[str] = None
    system_role: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class AdminLoginRequest(BaseModel):
    email: EmailStr
    password: str


class AdminCreateUserRequest(BaseModel):
    phone: str = Field(..., max_length=100)
    account_type: str = Field(..., pattern="^(personal|family)$")


class AdminUserResponse(BaseModel):
    id: str
    username: str
    email: str
    phone: Optional[str]
    system_role: str
    account_type: str
    created_at: datetime

    class Config:
        from_attributes = True


class AdminCreateUserResponse(AdminUserResponse):
    initial_password: str
    issued_license_count: int


class LicenseCodeResponse(BaseModel):
    id: str
    user_id: str
    phone: Optional[str] = None
    code: str
    status: str
    created_at: datetime
    used_at: Optional[datetime]

    class Config:
        from_attributes = True


class IssueLicenseCodeRequest(BaseModel):
    phone: str = Field(..., max_length=100)


class DisableLicenseCodeRequest(BaseModel):
    disabled: bool = True


class InstallVerifyRequest(BaseModel):
    code: Optional[str] = Field(default=None, min_length=6, max_length=32)
    license_code: Optional[str] = Field(default=None, min_length=6, max_length=32)

    @model_validator(mode="after")
    def ensure_code(self):
        if self.code:
            return self
        if self.license_code:
            self.code = self.license_code
            return self
        raise ValueError("code or license_code is required")


class InstallVerifyResponse(BaseModel):
    allowed: bool
    user_id: str
    account_type: str
    code_status: str


class InstallCheckResponse(BaseModel):
    allowed: bool
    code_status: str
    reason: Optional[str] = None


class ShortcutTransactionCreate(BaseModel):
    code: Optional[str] = Field(default=None, min_length=6, max_length=32)
    license_code: Optional[str] = Field(default=None, min_length=6, max_length=32)
    text: Optional[str] = None
    date: Optional[datetime] = None
    time: Optional[str] = None
    amount: Optional[float] = Field(default=None, gt=0)
    category: Optional[str] = Field(default=None, min_length=1, max_length=50)
    item: Optional[str] = None
    merchant: Optional[str] = None
    notes: Optional[str] = None

    @model_validator(mode="after")
    def ensure_code(self):
        if self.code:
            return self
        if self.license_code:
            self.code = self.license_code
            return self
        raise ValueError("code or license_code is required")


class ShortcutTransactionItem(BaseModel):
    id: str
    phone: Optional[str] = None
    license_code: str
    date: str
    time: str
    amount: float
    category: str
    item: Optional[str] = None
    merchant: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime


class FamilyCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class FamilyResponse(BaseModel):
    id: str
    name: str
    creator_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class FamilyInvite(BaseModel):
    phone: str = Field(..., max_length=100)


class TransactionCreate(BaseModel):
    date: datetime
    time: Optional[str] = None
    amount: float = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=50)
    item: Optional[str] = None
    merchant: Optional[str] = None
    notes: Optional[str] = None


class TransactionUpdate(BaseModel):
    date: Optional[datetime] = None
    time: Optional[str] = None
    amount: Optional[float] = Field(None, gt=0)
    category: Optional[str] = None
    item: Optional[str] = None
    merchant: Optional[str] = None
    notes: Optional[str] = None


class TransactionResponse(BaseModel):
    id: str
    family_id: Optional[str] = None
    user_id: str
    license_code_id: Optional[str] = None
    phone: Optional[str] = None
    license_code: Optional[str] = None
    date: datetime
    time: Optional[str]
    amount: float
    category: str
    item: Optional[str]
    merchant: Optional[str]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ShortcutTransactionWriteResponse(BaseModel):
    allowed: bool
    message: str
    transaction: Optional[TransactionResponse] = None


class StatsSummary(BaseModel):
    total_expense: float
    transaction_count: int
    average_amount: float
    max_amount: float


class CategoryStats(BaseModel):
    category: str
    amount: float
    count: int


class TrendData(BaseModel):
    date: str
    amount: float


class LicenseDistributionItem(BaseModel):
    license_code: str
    amount: float
    count: int


class PeriodComparison(BaseModel):
    current_amount: float
    previous_amount: float
    change_percent: Optional[float]
    current_count: int
    previous_count: int
    count_change_percent: Optional[float]


class StatsPeriodsResponse(BaseModel):
    day: PeriodComparison
    week: PeriodComparison
    month: PeriodComparison
    year: PeriodComparison


class StatsForecastResponse(BaseModel):
    period: str
    predicted_amount: float
    method: str


class AIExtractRequest(BaseModel):
    text: Optional[str] = None
    image: Optional[str] = None  # Base64编码的图片


class AIExtractResponse(BaseModel):
    date: str
    time: Optional[str]
    amount: float
    category: str
    item: Optional[str]
    merchant: Optional[str]


class MigrateRequest(BaseModel):
    csv_data: str


class MigrateResponse(BaseModel):
    message: str
    migrated_count: int
    failed_count: int
    family_id: Optional[str] = None


class ExportResponse(BaseModel):
    filename: str
    content: str
    count: int


class SwitchVersionRequest(BaseModel):
    target_version: str


class SwitchVersionResponse(BaseModel):
    message: str
    target_version: str
    timestamp: str


class VersionStatusResponse(BaseModel):
    current_version: str
    has_server_data: bool
    server_data_count: int


class BudgetCreate(BaseModel):
    family_id: Optional[str] = None
    category: Optional[str] = None  # None表示总预算
    amount: float = Field(..., gt=0)
    period: str = "monthly"  # monthly, weekly, yearly
    year: int
    month: Optional[int] = None


class BudgetUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    period: Optional[str] = None
    year: Optional[int] = None
    month: Optional[int] = None


class BudgetResponse(BaseModel):
    id: str
    user_id: str
    family_id: Optional[str]
    category: Optional[str]
    amount: float
    period: str
    year: int
    month: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class BudgetStatusResponse(BaseModel):
    budget_id: str
    category: Optional[str]
    budget_amount: float
    spent_amount: float
    remaining_amount: float
    percentage: float
    is_over_budget: bool
    period: str
    year: int
    month: Optional[int]


class BudgetMonthlyResponse(BaseModel):
    year: int
    month: int
    budget_amount: float
    spent_amount: float
    remaining_amount: float
    percentage: float
    is_over_budget: bool


class BudgetAlertResponse(BaseModel):
    budget_id: str
    category: Optional[str]
    budget_amount: float
    spent_amount: float
    over_amount: float
    period: str
    year: int
    month: Optional[int]
