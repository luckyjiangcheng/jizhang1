from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
import uuid
from app.database import get_db
from app.models import User, Family, FamilyMember, UserRole, Transaction, AccountType
from app.core.security import get_current_user
from app.schemas import FamilyCreate, FamilyResponse, FamilyInvite

router = APIRouter()


def _ensure_family_account(current_user: User):
    if current_user.account_type != AccountType.FAMILY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="仅家庭版账号可使用，请升级到家庭版"
        )


@router.post("/", response_model=FamilyResponse, status_code=status.HTTP_201_CREATED)
async def create_family(
    family_data: FamilyCreate,
    associate_transactions: bool = Query(False, description="是否将现有个人交易关联到新家庭"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    _ensure_family_account(current_user)
    # 创建新家庭
    new_family = Family(
        id=str(uuid.uuid4()),
        name=family_data.name,
        creator_id=current_user.id
    )
    
    db.add(new_family)
    await db.commit()
    await db.refresh(new_family)
    
    # 创建者自动成为管理员成员
    new_member = FamilyMember(
        id=str(uuid.uuid4()),
        family_id=new_family.id,
        user_id=current_user.id,
        role=UserRole.ADMIN
    )
    
    db.add(new_member)
    await db.commit()
    
    # 如果用户选择关联现有交易
    if associate_transactions:
        # 更新用户的个人交易，关联到新家庭
        await db.execute(
            update(Transaction)
            .where(
                Transaction.user_id == current_user.id,
                Transaction.family_id.is_(None)
            )
            .values(family_id=new_family.id)
        )
        await db.commit()
    
    return new_family


@router.get("/", response_model=list[FamilyResponse])
async def get_families(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    _ensure_family_account(current_user)
    # 获取用户所属的所有家庭
    result = await db.execute(
        select(Family)
        .join(FamilyMember, Family.id == FamilyMember.family_id)
        .where(FamilyMember.user_id == current_user.id)
    )
    families = result.scalars().all()
    return families


@router.post("/{family_id}/invite")
async def invite_member(
    family_id: str,
    invite_data: FamilyInvite,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    _ensure_family_account(current_user)
    # 验证用户是否是家庭成员
    result = await db.execute(
        select(FamilyMember)
        .where(
            FamilyMember.family_id == family_id,
            FamilyMember.user_id == current_user.id
        )
    )
    member = result.scalar_one_or_none()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您不是该家庭成员"
        )
    
    # 检查被邀请用户是否存在
    result = await db.execute(select(User).where(User.phone == invite_data.phone))
    invited_user = result.scalar_one_or_none()
    
    if not invited_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    if invited_user.account_type != AccountType.FAMILY:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="仅家庭版账号可加入家庭"
        )
    
    # 检查用户是否已经是家庭成员
    result = await db.execute(
        select(FamilyMember)
        .where(
            FamilyMember.family_id == family_id,
            FamilyMember.user_id == invited_user.id
        )
    )
    existing_member = result.scalar_one_or_none()
    
    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户已经是家庭成员"
        )

    result = await db.execute(
        select(func.count(FamilyMember.id))
        .where(FamilyMember.family_id == family_id)
    )
    member_count = int(result.scalar() or 0)
    if member_count >= 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="家庭成员已满(5人)"
        )
    
    # 添加家庭成员
    new_member = FamilyMember(
        id=str(uuid.uuid4()),
        family_id=family_id,
        user_id=invited_user.id,
        role=UserRole.MEMBER
    )
    
    db.add(new_member)
    await db.commit()
    
    return {"message": "邀请成功"}


@router.get("/{family_id}/members")
async def get_family_members(
    family_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    _ensure_family_account(current_user)
    # 验证用户是否是家庭成员
    result = await db.execute(
        select(FamilyMember)
        .where(
            FamilyMember.family_id == family_id,
            FamilyMember.user_id == current_user.id
        )
    )
    member = result.scalar_one_or_none()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您不是该家庭成员"
        )
    
    # 获取所有家庭成员
    result = await db.execute(
        select(FamilyMember, User)
        .join(User, FamilyMember.user_id == User.id)
        .where(FamilyMember.family_id == family_id)
    )
    members = result.all()
    
    return [
        {
            "id": member.id,
            "user_id": member.user_id,
            "username": user.username,
            "phone": user.phone,
            "email": user.email,
            "role": "member",
            "joined_at": member.joined_at
        }
        for member, user in members
    ]


@router.delete("/{family_id}/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_family_member(
    family_id: str,
    member_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    _ensure_family_account(current_user)
    access_result = await db.execute(
        select(FamilyMember).where(
            FamilyMember.family_id == family_id,
            FamilyMember.user_id == current_user.id
        )
    )
    access_member = access_result.scalar_one_or_none()
    if not access_member:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="您不是该家庭成员")

    target_result = await db.execute(
        select(FamilyMember).where(
            FamilyMember.family_id == family_id,
            FamilyMember.id == member_id
        )
    )
    target_member = target_result.scalar_one_or_none()
    if not target_member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="成员不存在")

    count_result = await db.execute(
        select(func.count(FamilyMember.id)).where(FamilyMember.family_id == family_id)
    )
    member_count = int(count_result.scalar() or 0)
    if member_count <= 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="至少保留1名成员")

    await db.delete(target_member)
    await db.commit()
    return None


@router.post("/{family_id}/associate-transactions")
async def associate_transactions(
    family_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    _ensure_family_account(current_user)
    # 验证用户是否是家庭成员
    result = await db.execute(
        select(FamilyMember)
        .where(
            FamilyMember.family_id == family_id,
            FamilyMember.user_id == current_user.id
        )
    )
    member = result.scalar_one_or_none()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您不是该家庭成员"
        )
    
    # 将用户的个人交易关联到家庭
    await db.execute(
        update(Transaction)
        .where(
            Transaction.user_id == current_user.id,
            Transaction.family_id.is_(None)
        )
        .values(family_id=family_id)
    )
    await db.commit()
    
    return {"message": "交易关联成功"}
