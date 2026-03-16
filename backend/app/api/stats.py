from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, extract, or_
from typing import Optional
from datetime import datetime, timedelta
from app.database import get_db
from app.models import User, Transaction, FamilyMember
from app.core.security import get_current_user
from app.core.access import get_bound_license_code
from app.schemas import StatsSummary, CategoryStats, TrendData, StatsPeriodsResponse, PeriodComparison, StatsForecastResponse

router = APIRouter(dependencies=[Depends(get_bound_license_code)])

async def _build_scope_conditions(db: AsyncSession, current_user: User, family_id: Optional[str]) -> list:
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
        return [Transaction.family_id == family_id]

    result = await db.execute(
        select(FamilyMember.family_id)
        .where(FamilyMember.user_id == current_user.id)
    )
    family_ids = [row[0] for row in result.all()]
    if family_ids:
        return [
            or_(
                Transaction.user_id == current_user.id,
                Transaction.family_id.in_(family_ids)
            )
        ]
    return [Transaction.user_id == current_user.id]


@router.get("/summary", response_model=StatsSummary)
async def get_summary(
    family_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # 构建时间范围
    if not start_date:
        start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    if not end_date:
        end_date = datetime.now()
    
    conditions = await _build_scope_conditions(db, current_user, family_id)
    
    conditions.extend([
        Transaction.deleted_at.is_(None),
        Transaction.amount > 0,
        Transaction.date >= start_date,
        Transaction.date <= end_date
    ])
    
    # 计算统计数据
    result = await db.execute(
        select(
            func.sum(Transaction.amount).label('total'),
            func.count(Transaction.id).label('count'),
            func.avg(Transaction.amount).label('average'),
            func.max(Transaction.amount).label('maximum')
        )
        .where(and_(*conditions))
    )
    stats = result.one()
    
    return StatsSummary(
        total_expense=float(stats.total or 0),
        transaction_count=int(stats.count),
        average_amount=float(stats.average or 0),
        max_amount=float(stats.maximum or 0)
    )


@router.get("/category", response_model=list[CategoryStats])
async def get_category_stats(
    family_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # 构建时间范围
    if not start_date:
        start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    if not end_date:
        end_date = datetime.now()
    
    conditions = await _build_scope_conditions(db, current_user, family_id)
    
    conditions.extend([
        Transaction.deleted_at.is_(None),
        Transaction.amount > 0,
        Transaction.date >= start_date,
        Transaction.date <= end_date
    ])
    
    # 按分类统计
    result = await db.execute(
        select(
            Transaction.category,
            func.sum(Transaction.amount).label('total'),
            func.count(Transaction.id).label('count')
        )
        .where(and_(*conditions))
        .group_by(Transaction.category)
        .order_by(func.sum(Transaction.amount).desc())
    )
    
    return [
        CategoryStats(
            category=row.category,
            amount=float(row.total),
            count=int(row.count)
        )
        for row in result.all()
    ]


@router.get("/trend", response_model=list[TrendData])
async def get_trend(
    family_id: Optional[str] = None,
    period: str = Query("month", regex="^(day|week|month|year)$"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    conditions = await _build_scope_conditions(db, current_user, family_id)
    
    # 根据周期确定时间范围和分组方式
    now = datetime.now()
    
    if period == "day":
        # 按小时统计
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        conditions.append(Transaction.date >= start_date)
        conditions.append(Transaction.deleted_at.is_(None))
        conditions.append(Transaction.amount > 0)
        result = await db.execute(
            select(
                extract('hour', Transaction.date).label('period'),
                func.sum(Transaction.amount).label('amount')
            )
            .where(and_(*conditions))
            .group_by(extract('hour', Transaction.date))
            .order_by(extract('hour', Transaction.date))
        )
        return [
            TrendData(date=f"{int(row.period)}:00", amount=float(row.amount or 0))
            for row in result.all()
        ]
    
    elif period == "week":
        # 按天统计（最近7天）
        start_date = now - timedelta(days=7)
        conditions.append(Transaction.date >= start_date)
        conditions.append(Transaction.deleted_at.is_(None))
        conditions.append(Transaction.amount > 0)
        result = await db.execute(
            select(
                func.date(Transaction.date).label('period'),
                func.sum(Transaction.amount).label('amount')
            )
            .where(and_(*conditions))
            .group_by(func.date(Transaction.date))
            .order_by(func.date(Transaction.date))
        )
        return [
            TrendData(date=str(row.period), amount=float(row.amount or 0))
            for row in result.all()
        ]
    
    elif period == "month":
        # 按天统计（本月）
        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        conditions.append(Transaction.date >= start_date)
        conditions.append(Transaction.deleted_at.is_(None))
        conditions.append(Transaction.amount > 0)
        result = await db.execute(
            select(
                func.date(Transaction.date).label('period'),
                func.sum(Transaction.amount).label('amount')
            )
            .where(and_(*conditions))
            .group_by(func.date(Transaction.date))
            .order_by(func.date(Transaction.date))
        )
        return [
            TrendData(date=str(row.period), amount=float(row.amount or 0))
            for row in result.all()
        ]
    
    else:  # year
        # 按月统计
        start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        conditions.append(Transaction.date >= start_date)
        conditions.append(Transaction.deleted_at.is_(None))
        conditions.append(Transaction.amount > 0)
        result = await db.execute(
            select(
                extract('month', Transaction.date).label('period'),
                func.sum(Transaction.amount).label('amount')
            )
            .where(and_(*conditions))
            .group_by(extract('month', Transaction.date))
            .order_by(extract('month', Transaction.date))
        )
        return [
            TrendData(date=f"{int(row.period)}月", amount=float(row.amount or 0))
            for row in result.all()
        ]


def _calc_change(current: float, previous: float) -> Optional[float]:
    if previous == 0:
        return None if current == 0 else 100.0
    return ((current - previous) / previous) * 100


async def _period_stats(db: AsyncSession, base_conditions: list, start: datetime, end: datetime) -> tuple[float, int]:
    result = await db.execute(
        select(
            func.sum(Transaction.amount).label('total'),
            func.count(Transaction.id).label('count')
        )
        .where(and_(*base_conditions, Transaction.date >= start, Transaction.date <= end))
    )
    row = result.one()
    return float(row.total or 0), int(row.count or 0)


@router.get("/periods", response_model=StatsPeriodsResponse)
async def get_periods(
    family_id: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    now = datetime.now()
    today_start = datetime(now.year, now.month, now.day)

    base_conditions = await _build_scope_conditions(db, current_user, family_id)

    base_conditions.extend([Transaction.deleted_at.is_(None), Transaction.amount > 0])

    day_start = today_start
    day_end = today_start + timedelta(days=1) - timedelta(milliseconds=1)
    prev_day_start = day_start - timedelta(days=1)
    prev_day_end = day_end - timedelta(days=1)

    weekday = today_start.isoweekday()
    week_start = today_start - timedelta(days=weekday - 1)
    week_end = week_start + timedelta(days=7) - timedelta(milliseconds=1)
    prev_week_start = week_start - timedelta(days=7)
    prev_week_end = week_end - timedelta(days=7)

    month_start = datetime(today_start.year, today_start.month, 1)
    next_month = datetime(today_start.year + (1 if today_start.month == 12 else 0), 1 if today_start.month == 12 else today_start.month + 1, 1)
    month_end = next_month - timedelta(milliseconds=1)
    prev_month_end = month_start - timedelta(milliseconds=1)
    prev_month_start = datetime(prev_month_end.year, prev_month_end.month, 1)

    year_start = datetime(today_start.year, 1, 1)
    next_year = datetime(today_start.year + 1, 1, 1)
    year_end = next_year - timedelta(milliseconds=1)
    prev_year_start = datetime(today_start.year - 1, 1, 1)
    prev_year_end = datetime(today_start.year, 1, 1) - timedelta(milliseconds=1)

    day_amount, day_count = await _period_stats(db, base_conditions, day_start, day_end)
    prev_day_amount, prev_day_count = await _period_stats(db, base_conditions, prev_day_start, prev_day_end)
    week_amount, week_count = await _period_stats(db, base_conditions, week_start, week_end)
    prev_week_amount, prev_week_count = await _period_stats(db, base_conditions, prev_week_start, prev_week_end)
    month_amount, month_count = await _period_stats(db, base_conditions, month_start, month_end)
    prev_month_amount, prev_month_count = await _period_stats(db, base_conditions, prev_month_start, prev_month_end)
    year_amount, year_count = await _period_stats(db, base_conditions, year_start, year_end)
    prev_year_amount, prev_year_count = await _period_stats(db, base_conditions, prev_year_start, prev_year_end)

    return StatsPeriodsResponse(
        day=PeriodComparison(
            current_amount=day_amount,
            previous_amount=prev_day_amount,
            change_percent=_calc_change(day_amount, prev_day_amount),
            current_count=day_count,
            previous_count=prev_day_count,
            count_change_percent=_calc_change(float(day_count), float(prev_day_count))
        ),
        week=PeriodComparison(
            current_amount=week_amount,
            previous_amount=prev_week_amount,
            change_percent=_calc_change(week_amount, prev_week_amount),
            current_count=week_count,
            previous_count=prev_week_count,
            count_change_percent=_calc_change(float(week_count), float(prev_week_count))
        ),
        month=PeriodComparison(
            current_amount=month_amount,
            previous_amount=prev_month_amount,
            change_percent=_calc_change(month_amount, prev_month_amount),
            current_count=month_count,
            previous_count=prev_month_count,
            count_change_percent=_calc_change(float(month_count), float(prev_month_count))
        ),
        year=PeriodComparison(
            current_amount=year_amount,
            previous_amount=prev_year_amount,
            change_percent=_calc_change(year_amount, prev_year_amount),
            current_count=year_count,
            previous_count=prev_year_count,
            count_change_percent=_calc_change(float(year_count), float(prev_year_count))
        )
    )


@router.get("/forecast", response_model=StatsForecastResponse)
async def get_forecast(
    family_id: Optional[str] = None,
    period: str = Query("month", regex="^(week|month)$"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    now = datetime.now()
    today_start = datetime(now.year, now.month, now.day)

    base_conditions = await _build_scope_conditions(db, current_user, family_id)

    base_conditions.extend([Transaction.deleted_at.is_(None), Transaction.amount > 0])

    totals: list[float] = []
    if period == "week":
        weekday = today_start.isoweekday()
        week_start = today_start - timedelta(days=weekday - 1)
        for i in range(4):
            start = week_start - timedelta(days=7 * (i + 1))
            end = start + timedelta(days=7) - timedelta(milliseconds=1)
            amount, _ = await _period_stats(db, base_conditions, start, end)
            totals.append(amount)
        method = "avg_last_4_weeks"
    else:
        month_start = datetime(today_start.year, today_start.month, 1)
        cursor = month_start
        for _ in range(3):
            prev_month_end = cursor - timedelta(milliseconds=1)
            prev_month_start = datetime(prev_month_end.year, prev_month_end.month, 1)
            amount, _ = await _period_stats(db, base_conditions, prev_month_start, prev_month_end)
            totals.append(amount)
            cursor = prev_month_start
        method = "avg_last_3_months"

    predicted = sum(totals) / len(totals) if totals else 0.0
    return StatsForecastResponse(period=period, predicted_amount=float(predicted), method=method)
