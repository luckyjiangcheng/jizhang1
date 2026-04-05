from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from datetime import timedelta
import uuid
from app.database import get_db
from app.models import User, FamilyMember, LicenseCode
from app.core.security import verify_password, get_password_hash, create_access_token, get_current_user
from app.schemas import UserCreate, UserLogin, Token, UserResponse, LicenseCodeResponse

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # 检查邮箱是否已存在
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册"
        )
    
    # 检查用户名是否已存在
    result = await db.execute(select(User).where(User.username == user_data.username))
    existing_username = result.scalar_one_or_none()
    
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已被使用"
        )
    
    # 创建新用户
    new_user = User(
        id=str(uuid.uuid4()),
        username=user_data.username,
        email=user_data.email,
        password_hash=get_password_hash(user_data.password)
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user


@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    # 查找用户（支持账号或用户名登录）
    result = await db.execute(
        select(User).where(
            or_(
                User.phone == user_data.phone,
                User.username == user_data.phone
            )
        )
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在，请联系客服申请"
        )
    
    # 验证密码
    if not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="密码错误"
        )
    
    # 创建访问令牌
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/license-codes", response_model=list[LicenseCodeResponse])
async def get_my_license_codes(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(LicenseCode)
        .where(LicenseCode.user_id == current_user.id)
        .order_by(LicenseCode.created_at.desc())
    )
    return result.scalars().all()


@router.get("/usage-mode")
async def get_usage_mode(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # 检查用户是否加入了任何家庭
    result = await db.execute(
        select(FamilyMember)
        .where(FamilyMember.user_id == current_user.id)
    )
    family_memberships = result.scalars().all()
    
    if family_memberships:
        # 用户已加入家庭，使用模式为家庭
        return {
            "mode": "family",
            "family_count": len(family_memberships),
            "message": "您当前处于家庭模式"
        }
    else:
        # 用户未加入任何家庭，使用模式为个人
        return {
            "mode": "individual",
            "message": "您当前处于个人模式"
        }
