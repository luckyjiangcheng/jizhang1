from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
import uuid
from app.database import get_db
from app.config import settings
from app.models import User, SystemRole, AccountType, LicenseCode, LicenseCodeStatus, Transaction
from app.schemas import (
    AdminLoginRequest,
    AdminCreateUserRequest,
    Token,
    AdminUserResponse,
    AdminCreateUserResponse,
    LicenseCodeResponse,
    IssueLicenseCodeRequest,
    DisableLicenseCodeRequest,
    TransactionResponse
)
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.access import get_current_root_user
from app.utils.license_codes import generate_license_code
from app.utils.admin_user_rules import is_valid_phone, build_initial_password

router = APIRouter()


async def _ensure_root_exists(db: AsyncSession) -> User:
    result = await db.execute(
        select(User).where(User.system_role == SystemRole.ROOT)
    )
    root_user = result.scalar_one_or_none()
    if root_user:
        return root_user

    root_user = User(
        id=str(uuid.uuid4()),
        username=settings.ROOT_USERNAME,
        email=settings.ROOT_EMAIL,
        password_hash=get_password_hash(settings.ROOT_PASSWORD),
        system_role=SystemRole.ROOT,
        account_type=AccountType.PERSONAL
    )
    db.add(root_user)
    await db.commit()
    await db.refresh(root_user)
    return root_user


async def _generate_unique_license_codes(db: AsyncSession, user_id: str, count: int) -> list[LicenseCode]:
    created_codes: list[LicenseCode] = []
    while len(created_codes) < count:
        code_value = generate_license_code()
        result = await db.execute(
            select(LicenseCode).where(LicenseCode.code == code_value)
        )
        exists = result.scalar_one_or_none()
        if exists:
            continue
        created_codes.append(
            LicenseCode(
                id=str(uuid.uuid4()),
                user_id=user_id,
                code=code_value,
                status=LicenseCodeStatus.UNUSED
            )
        )
    return created_codes


async def _build_unique_identity(db: AsyncSession, account_type: AccountType, phone: str) -> tuple[str, str]:
    prefix = "f" if account_type == AccountType.FAMILY else "p"
    phone_part = phone[-6:]
    while True:
        suffix = uuid.uuid4().hex[:6]
        username = f"{prefix}_{phone_part}{suffix}"
        email = f"{username}@example.com"
        username_exists = await db.execute(select(User.id).where(User.username == username))
        if username_exists.scalar_one_or_none():
            continue
        email_exists = await db.execute(select(User.id).where(User.email == email))
        if email_exists.scalar_one_or_none():
            continue
        return username, email


@router.post("/auth/login", response_model=Token)
async def admin_login(
    login_data: AdminLoginRequest,
    db: AsyncSession = Depends(get_db)
):
    await _ensure_root_exists(db)
    result = await db.execute(
        select(User).where(
            and_(
                User.email == login_data.email,
                User.system_role == SystemRole.ROOT
            )
        )
    )
    root_user = result.scalar_one_or_none()
    if not root_user or not verify_password(login_data.password, root_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="root 邮箱或密码错误"
        )

    access_token = create_access_token(
        data={"sub": root_user.id},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users", response_model=list[AdminUserResponse])
async def list_users(
    phone: str | None = Query(default=None),
    account_type: str | None = Query(default=None),
    current_root_user: User = Depends(get_current_root_user),
    db: AsyncSession = Depends(get_db)
):
    _ = current_root_user
    conditions = [User.system_role == SystemRole.USER]
    if phone:
        conditions.append(User.phone.like(f"%{phone}%"))
    if account_type:
        try:
            conditions.append(User.account_type == AccountType(account_type))
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="账号类型错误")
    result = await db.execute(select(User).where(and_(*conditions)).order_by(User.created_at.desc()))
    return result.scalars().all()


@router.post("/users", response_model=AdminCreateUserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: AdminCreateUserRequest,
    current_root_user: User = Depends(get_current_root_user),
    db: AsyncSession = Depends(get_db)
):
    _ = current_root_user
    result = await db.execute(select(User).where(User.phone == user_data.phone))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="账号已被使用")
    if not is_valid_phone(user_data.phone):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="账号格式错误")

    account_type = AccountType(user_data.account_type)
    initial_password = build_initial_password(user_data.phone)
    username, email = await _build_unique_identity(db, account_type, user_data.phone)
    new_user = User(
        id=str(uuid.uuid4()),
        username=username,
        email=email,
        phone=user_data.phone,
        password_hash=get_password_hash(initial_password),
        system_role=SystemRole.USER,
        account_type=account_type
    )
    db.add(new_user)
    await db.flush()

    license_count = 1 if account_type == AccountType.PERSONAL else 5
    license_codes = await _generate_unique_license_codes(db, new_user.id, license_count)
    db.add_all(license_codes)

    await db.commit()
    await db.refresh(new_user)
    return AdminCreateUserResponse(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        phone=new_user.phone,
        system_role=new_user.system_role.value,
        account_type=new_user.account_type.value,
        created_at=new_user.created_at,
        initial_password=initial_password,
        issued_license_count=license_count
    )


@router.get("/license-codes", response_model=list[LicenseCodeResponse])
async def list_license_codes(
    phone: str | None = Query(default=None),
    code: str | None = Query(default=None),
    current_root_user: User = Depends(get_current_root_user),
    db: AsyncSession = Depends(get_db)
):
    _ = current_root_user
    conditions = []
    if phone:
        conditions.append(User.phone.like(f"%{phone}%"))
    if code:
        conditions.append(LicenseCode.code.like(f"%{code}%"))

    query = (
        select(LicenseCode, User.phone)
        .join(User, User.id == LicenseCode.user_id)
        .where(User.system_role == SystemRole.USER)
        .order_by(LicenseCode.created_at.desc())
    )
    if conditions:
        query = query.where(and_(*conditions))

    result = await db.execute(query)
    rows = result.all()
    return [
        LicenseCodeResponse(
            id=item.id,
            user_id=item.user_id,
            phone=item_phone,
            code=item.code,
            status=item.status.value,
            created_at=item.created_at,
            used_at=item.used_at
        )
        for item, item_phone in rows
    ]


@router.post("/license-codes/issue", response_model=list[LicenseCodeResponse], status_code=status.HTTP_201_CREATED)
async def issue_license_codes(
    request: IssueLicenseCodeRequest,
    current_root_user: User = Depends(get_current_root_user),
    db: AsyncSession = Depends(get_db)
):
    _ = current_root_user
    result = await db.execute(
        select(User).where(and_(User.phone == request.phone, User.system_role == SystemRole.USER))
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")

    license_codes = await _generate_unique_license_codes(db, user.id, 1)
    db.add_all(license_codes)
    await db.commit()

    for item in license_codes:
        await db.refresh(item)
    return [
        LicenseCodeResponse(
            id=item.id,
            user_id=item.user_id,
            phone=user.phone,
            code=item.code,
            status=item.status.value,
            created_at=item.created_at,
            used_at=item.used_at
        )
        for item in license_codes
    ]


@router.patch("/license-codes/{license_code_id}", response_model=LicenseCodeResponse)
async def disable_license_code(
    license_code_id: str,
    request: DisableLicenseCodeRequest,
    current_root_user: User = Depends(get_current_root_user),
    db: AsyncSession = Depends(get_db)
):
    _ = current_root_user
    result = await db.execute(select(LicenseCode).where(LicenseCode.id == license_code_id))
    license_code = result.scalar_one_or_none()
    if not license_code:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="授权码不存在")

    if request.disabled:
        license_code.status = LicenseCodeStatus.DISABLED
    elif license_code.status in (LicenseCodeStatus.DISABLED, LicenseCodeStatus.USED):
        license_code.status = LicenseCodeStatus.UNUSED
        license_code.used_at = None
    elif license_code.status == LicenseCodeStatus.UNUSED:
        license_code.status = LicenseCodeStatus.UNUSED

    await db.commit()
    await db.refresh(license_code)
    return license_code


@router.delete("/license-codes/{license_code_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_license_code(
    license_code_id: str,
    current_root_user: User = Depends(get_current_root_user),
    db: AsyncSession = Depends(get_db)
):
    _ = current_root_user
    result = await db.execute(select(LicenseCode).where(LicenseCode.id == license_code_id))
    license_code = result.scalar_one_or_none()
    if not license_code:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="授权码不存在")
    await db.delete(license_code)
    await db.commit()
    return None


@router.get("/transactions", response_model=list[TransactionResponse])
async def list_transactions(
    phone: str | None = Query(default=None),
    license_code: str | None = Query(default=None),
    current_root_user: User = Depends(get_current_root_user),
    db: AsyncSession = Depends(get_db)
):
    _ = current_root_user
    conditions = [Transaction.deleted_at.is_(None), User.system_role == SystemRole.USER]
    if phone:
        conditions.append(User.phone.like(f"%{phone}%"))

    if license_code:
        conditions.append(LicenseCode.code.like(f"%{license_code}%"))

    query = (
        select(Transaction, User.phone, LicenseCode.code)
        .join(User, User.id == Transaction.user_id)
        .outerjoin(LicenseCode, LicenseCode.id == Transaction.license_code_id)
        .where(and_(*conditions))
        .order_by(Transaction.date.desc(), Transaction.created_at.desc())
    )
    result = await db.execute(query)
    rows = result.all()
    return [
        TransactionResponse(
            id=tx.id,
            family_id=tx.family_id,
            user_id=tx.user_id,
            license_code_id=tx.license_code_id,
            phone=phone,
            license_code=code,
            date=tx.date,
            time=tx.time,
            amount=tx.amount,
            category=tx.category,
            item=tx.item,
            merchant=tx.merchant,
            notes=tx.notes,
            created_at=tx.created_at,
            updated_at=tx.updated_at,
            deleted_at=tx.deleted_at
        )
        for tx, phone, code in rows
    ]


@router.delete("/transactions/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: str,
    current_root_user: User = Depends(get_current_root_user),
    db: AsyncSession = Depends(get_db)
):
    _ = current_root_user
    result = await db.execute(select(Transaction).where(Transaction.id == transaction_id))
    transaction = result.scalar_one_or_none()
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="交易不存在")
    transaction.deleted_at = datetime.utcnow()
    await db.commit()
    return None
