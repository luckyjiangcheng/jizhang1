from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from typing import Optional, List
from datetime import datetime
import uuid
from app.database import get_db
from app.models import User, Transaction, FamilyMember
from app.core.security import get_current_user
from app.core.access import get_bound_license_code
from app.schemas import TransactionCreate, TransactionUpdate, TransactionResponse

router = APIRouter(dependencies=[Depends(get_bound_license_code)])


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_data: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # 获取用户的默认家庭
    result = await db.execute(
        select(FamilyMember)
        .where(FamilyMember.user_id == current_user.id)
        .order_by(FamilyMember.joined_at)
    )
    family_member = result.scalar_one_or_none()
    
    # 确定交易的家庭ID（如果用户加入了家庭）
    family_id = family_member.family_id if family_member else None
    
    # 创建新交易
    new_transaction = Transaction(
        id=str(uuid.uuid4()),
        family_id=family_id,
        user_id=current_user.id,
        date=transaction_data.date,
        time=transaction_data.time[:5] if transaction_data.time else None,
        amount=transaction_data.amount,
        category=transaction_data.category,
        item=transaction_data.item,
        merchant=transaction_data.merchant,
        notes=transaction_data.notes
    )
    
    db.add(new_transaction)
    await db.commit()
    await db.refresh(new_transaction)
    
    return new_transaction


@router.get("/", response_model=List[TransactionResponse])
async def get_transactions(
    family_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    updated_since: Optional[datetime] = None,
    include_deleted: bool = False,
    category: Optional[str] = None,
    user_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    conditions = []
    
    if family_id:
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
        conditions.append(Transaction.family_id == family_id)
    else:
        # 获取用户可见范围：个人交易 + 所属家庭交易
        result = await db.execute(
            select(FamilyMember.family_id)
            .where(FamilyMember.user_id == current_user.id)
        )
        family_ids = [row[0] for row in result.all()]
        if family_ids:
            conditions.append(
                or_(
                    Transaction.user_id == current_user.id,
                    Transaction.family_id.in_(family_ids)
                )
            )
        else:
            # 用户未加入任何家庭，只查询个人交易
            conditions.append(Transaction.user_id == current_user.id)
    
    if start_date:
        conditions.append(Transaction.date >= start_date)
    
    if end_date:
        conditions.append(Transaction.date <= end_date)

    if updated_since:
        conditions.append(
            or_(
                Transaction.updated_at >= updated_since,
                Transaction.deleted_at >= updated_since
            )
        )

    if not include_deleted:
        conditions.append(Transaction.deleted_at.is_(None))
    
    if category:
        conditions.append(Transaction.category == category)
    
    if user_id:
        conditions.append(Transaction.user_id == user_id)
    
    # 执行查询
    query = select(Transaction).where(and_(*conditions))
    query = query.order_by(Transaction.date.desc(), Transaction.created_at.desc())
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    transactions = result.scalars().all()
    
    return transactions


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # 获取交易并验证可见权限
    result = await db.execute(
        select(Transaction)
        .where(Transaction.id == transaction_id)
    )
    transaction = result.scalar_one_or_none()

    if not transaction or transaction.deleted_at:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="交易不存在或无权访问"
        )

    # 家庭交易：家庭成员可见
    if transaction.family_id:
        member_result = await db.execute(
            select(FamilyMember)
            .where(
                FamilyMember.family_id == transaction.family_id,
                FamilyMember.user_id == current_user.id
            )
        )
        if not member_result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="交易不存在或无权访问"
            )
    # 个人交易：仅本人可见
    elif transaction.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="交易不存在或无权访问"
        )
    
    return transaction


@router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: str,
    transaction_data: TransactionUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # 获取交易并验证权限
    result = await db.execute(
        select(Transaction)
        .where(
            Transaction.id == transaction_id,
            Transaction.user_id == current_user.id
        )
    )
    transaction = result.scalar_one_or_none()
    
    # 如果交易属于家庭，验证用户是否是家庭成员
    if transaction and transaction.family_id:
        member_result = await db.execute(
            select(FamilyMember)
            .where(
                FamilyMember.family_id == transaction.family_id,
                FamilyMember.user_id == current_user.id
            )
        )
        if not member_result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="交易不存在或无权访问"
            )
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="交易不存在或无权访问"
        )

    if transaction.deleted_at:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="交易不存在或无权访问"
        )
    
    # 更新交易字段
    update_data = transaction_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(transaction, field, value)
    
    await db.commit()
    await db.refresh(transaction)
    
    return transaction


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # 获取交易并验证权限
    result = await db.execute(
        select(Transaction)
        .where(
            Transaction.id == transaction_id,
            Transaction.user_id == current_user.id
        )
    )
    transaction = result.scalar_one_or_none()
    
    # 如果交易属于家庭，验证用户是否是家庭成员
    if transaction and transaction.family_id:
        member_result = await db.execute(
            select(FamilyMember)
            .where(
                FamilyMember.family_id == transaction.family_id,
                FamilyMember.user_id == current_user.id
            )
        )
        if not member_result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="交易不存在或无权访问"
            )
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="交易不存在或无权访问"
        )

    if transaction.deleted_at:
        return None

    transaction.deleted_at = datetime.utcnow()
    await db.commit()
    await db.refresh(transaction)

    return None
