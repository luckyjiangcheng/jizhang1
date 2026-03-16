from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, delete
from typing import Optional
from datetime import datetime
import uuid
from app.database import get_db
from app.models import User, Transaction, FamilyMember, Budget, UserRole
from app.core.security import get_current_user
from app.core.access import get_bound_license_code
from app.schemas import (
    BudgetCreate, BudgetUpdate, BudgetResponse, BudgetStatusResponse, BudgetAlertResponse
)
from app.utils.contracts import month_range

router = APIRouter(dependencies=[Depends(get_bound_license_code)])


@router.post("/", response_model=BudgetResponse, status_code=status.HTTP_201_CREATED)
async def create_budget(
    budget_data: BudgetCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建预算
    """
    if budget_data.family_id:
        result = await db.execute(
            select(FamilyMember)
            .where(
                FamilyMember.family_id == budget_data.family_id,
                FamilyMember.user_id == current_user.id
            )
        )
        member = result.scalar_one_or_none()
        
        if not member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="您不是该家庭成员"
            )
        if member.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="只有家庭管理员可以管理家庭预算"
            )
    
    if budget_data.family_id:
        existing_conditions = [
            Budget.family_id == budget_data.family_id,
            Budget.category == budget_data.category,
            Budget.year == budget_data.year,
            Budget.month == budget_data.month
        ]
    else:
        existing_conditions = [
            Budget.user_id == current_user.id,
            Budget.family_id.is_(None),
            Budget.category == budget_data.category,
            Budget.year == budget_data.year,
            Budget.month == budget_data.month
        ]

    existing = await db.execute(select(Budget).where(and_(*existing_conditions)))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该预算已存在"
        )
    
    new_budget = Budget(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        family_id=budget_data.family_id,
        category=budget_data.category,
        amount=budget_data.amount,
        period=budget_data.period,
        year=budget_data.year,
        month=budget_data.month
    )
    
    db.add(new_budget)
    await db.commit()
    await db.refresh(new_budget)
    
    return new_budget


@router.get("/", response_model=list[BudgetResponse])
async def get_budgets(
    family_id: Optional[str] = None,
    year: Optional[int] = None,
    month: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取预算列表
    """
    if family_id:
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
        conditions = [Budget.family_id == family_id]
    else:
        conditions = [Budget.user_id == current_user.id, Budget.family_id.is_(None)]
    
    if year:
        conditions.append(Budget.year == year)
    
    if month:
        conditions.append(Budget.month == month)
    
    result = await db.execute(
        select(Budget)
        .where(and_(*conditions))
        .order_by(Budget.year.desc(), Budget.month.desc())
    )
    
    return result.scalars().all()


@router.get("/status", response_model=list[BudgetStatusResponse])
async def get_budget_status(
    family_id: Optional[str] = None,
    year: Optional[int] = None,
    month: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取预算状态（包含已花费金额和剩余金额）
    """
    now = datetime.now()
    target_year = year or now.year
    target_month = month or now.month
    
    if family_id:
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
        conditions = [Budget.family_id == family_id]
    else:
        conditions = [Budget.user_id == current_user.id, Budget.family_id.is_(None)]
    
    conditions.extend([
        Budget.year == target_year,
        Budget.month == target_month
    ])
    
    result = await db.execute(
        select(Budget).where(and_(*conditions))
    )
    budgets = result.scalars().all()
    
    status_list = []
    period_start, period_end = month_range(target_year, target_month)
    
    for budget in budgets:
        if budget.family_id:
            tx_conditions = [Transaction.family_id == budget.family_id]
        else:
            tx_conditions = [Transaction.user_id == current_user.id, Transaction.family_id.is_(None)]
        
        if budget.category:
            tx_conditions.append(Transaction.category == budget.category)
        
        tx_conditions.extend([
            Transaction.amount > 0,
            Transaction.deleted_at.is_(None),
            Transaction.date >= period_start,
            Transaction.date < period_end
        ])
        
        spent_result = await db.execute(
            select(func.sum(Transaction.amount))
            .where(and_(*tx_conditions))
        )
        spent_amount = float(spent_result.scalar() or 0)
        
        remaining = budget.amount - spent_amount
        percentage = (spent_amount / budget.amount * 100) if budget.amount > 0 else 0
        
        status_list.append(BudgetStatusResponse(
            budget_id=budget.id,
            category=budget.category,
            budget_amount=budget.amount,
            spent_amount=spent_amount,
            remaining_amount=remaining,
            percentage=min(percentage, 100),
            is_over_budget=spent_amount > budget.amount,
            period=budget.period,
            year=budget.year,
            month=budget.month
        ))
    
    return status_list


@router.put("/{budget_id}", response_model=BudgetResponse)
async def update_budget(
    budget_id: str,
    budget_data: BudgetUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    更新预算
    """
    result = await db.execute(
        select(Budget).where(Budget.id == budget_id)
    )
    budget = result.scalar_one_or_none()
    
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="预算不存在"
        )

    if budget.family_id:
        result = await db.execute(
            select(FamilyMember)
            .where(
                FamilyMember.family_id == budget.family_id,
                FamilyMember.user_id == current_user.id,
                FamilyMember.role == UserRole.ADMIN
            )
        )
        admin = result.scalar_one_or_none()
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="只有家庭管理员可以管理家庭预算"
            )
    else:
        if budget.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="预算不存在"
            )
    
    if budget_data.amount is not None:
        budget.amount = budget_data.amount
    
    if budget_data.period is not None:
        budget.period = budget_data.period
    
    if budget_data.year is not None:
        budget.year = budget_data.year
    
    if budget_data.month is not None:
        budget.month = budget_data.month
    
    await db.commit()
    await db.refresh(budget)
    
    return budget


@router.delete("/{budget_id}")
async def delete_budget(
    budget_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    删除预算
    """
    result = await db.execute(
        select(Budget).where(Budget.id == budget_id)
    )
    budget = result.scalar_one_or_none()
    
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="预算不存在"
        )

    if budget.family_id:
        result = await db.execute(
            select(FamilyMember)
            .where(
                FamilyMember.family_id == budget.family_id,
                FamilyMember.user_id == current_user.id,
                FamilyMember.role == UserRole.ADMIN
            )
        )
        admin = result.scalar_one_or_none()
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="只有家庭管理员可以管理家庭预算"
            )
    else:
        if budget.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="预算不存在"
            )
    
    await db.execute(
        delete(Budget).where(Budget.id == budget_id)
    )
    await db.commit()
    
    return {"message": "预算已删除"}


@router.get("/alerts", response_model=list[BudgetAlertResponse])
async def get_budget_alerts(
    family_id: Optional[str] = None,
    year: Optional[int] = None,
    month: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    now = datetime.now()
    target_year = year or now.year
    target_month = month or now.month

    if family_id:
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
        budget_conditions = [Budget.family_id == family_id]
    else:
        budget_conditions = [Budget.user_id == current_user.id, Budget.family_id.is_(None)]

    budget_conditions.extend([Budget.year == target_year, Budget.month == target_month])
    result = await db.execute(select(Budget).where(and_(*budget_conditions)))
    budgets = result.scalars().all()

    alerts: list[BudgetAlertResponse] = []
    period_start, period_end = month_range(target_year, target_month)
    for budget in budgets:
        if budget.family_id:
            tx_conditions = [Transaction.family_id == budget.family_id]
        else:
            tx_conditions = [Transaction.user_id == current_user.id, Transaction.family_id.is_(None)]

        if budget.category:
            tx_conditions.append(Transaction.category == budget.category)

        tx_conditions.extend([
            Transaction.amount > 0,
            Transaction.deleted_at.is_(None),
            Transaction.date >= period_start,
            Transaction.date < period_end
        ])

        spent_result = await db.execute(
            select(func.sum(Transaction.amount)).where(and_(*tx_conditions))
        )
        spent_amount = float(spent_result.scalar() or 0)
        if spent_amount > budget.amount:
            alerts.append(BudgetAlertResponse(
                budget_id=budget.id,
                category=budget.category,
                budget_amount=budget.amount,
                spent_amount=spent_amount,
                over_amount=spent_amount - budget.amount,
                period=budget.period,
                year=budget.year,
                month=budget.month
            ))

    return alerts
