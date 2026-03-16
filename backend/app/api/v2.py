from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func, extract
import csv
import io
import json
from pathlib import Path
import uuid
import httpx
from zoneinfo import ZoneInfo
from app.database import get_db
from app.models import User, Transaction, FamilyMember, LicenseCode, LicenseCodeStatus, Budget, SystemRole
from app.config import settings
from app.schemas import (
    InstallVerifyRequest,
    InstallVerifyResponse,
    InstallCheckResponse,
    ShortcutTransactionCreate,
    ShortcutTransactionItem,
    ShortcutTransactionWriteResponse,
    TransactionCreate,
    TransactionResponse,
    StatsSummary,
    CategoryStats,
    TrendData,
    LicenseDistributionItem,
    BudgetCreate,
    BudgetResponse,
    BudgetStatusResponse,
    BudgetMonthlyResponse
)
from app.core.security import get_current_user
from app.core.access import get_bound_license_code
from app.utils.license_codes import is_installable_status

router = APIRouter()


def _build_transaction_response(
    tx: Transaction,
    phone: str | None,
    code: str | None
) -> TransactionResponse:
    return TransactionResponse(
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


async def _activate_install_code(
    request: InstallVerifyRequest,
    db: AsyncSession
):
    result = await db.execute(
        select(LicenseCode).where(LicenseCode.code == request.code)
    )
    license_code = result.scalar_one_or_none()
    if not license_code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="授权码不存在"
        )

    if not is_installable_status(license_code.status):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="授权码不可安装"
        )

    user_result = await db.execute(select(User).where(User.id == license_code.user_id))
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="授权码绑定用户不存在"
        )

    license_code.status = LicenseCodeStatus.USED
    license_code.used_at = datetime.utcnow()
    await db.commit()
    await db.refresh(license_code)

    return InstallVerifyResponse(
        allowed=True,
        user_id=user.id,
        account_type=user.account_type.value,
        code_status=license_code.status.value
    )


async def _resolve_license_and_user(
    db: AsyncSession,
    code_value: str,
    require_used: bool
) -> tuple[LicenseCode, User]:
    result = await db.execute(select(LicenseCode).where(LicenseCode.code == code_value))
    license_code = result.scalar_one_or_none()
    if not license_code:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="授权码不存在")
    if license_code.status == LicenseCodeStatus.DISABLED:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="授权码已禁用")
    if require_used and license_code.status != LicenseCodeStatus.USED:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="授权码未激活")
    user_result = await db.execute(select(User).where(User.id == license_code.user_id))
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="授权码绑定用户不存在")
    return license_code, user


async def _load_shortcut_dashboard_rows(db: AsyncSession, code_value: str) -> list[ShortcutTransactionItem]:
    _, user = await _resolve_license_and_user(db, code_value, require_used=True)
    user_ids = [user.id]
    if user.phone:
        users_result = await db.execute(
            select(User.id).where(
                and_(
                    User.phone == user.phone,
                    User.system_role == SystemRole.USER
                )
            )
        )
        ids = [item for item in users_result.scalars().all()]
        if ids:
            user_ids = ids
    tx_result = await db.execute(
        select(Transaction, LicenseCode.code, User.phone)
        .join(LicenseCode, LicenseCode.id == Transaction.license_code_id, isouter=True)
        .join(User, User.id == Transaction.user_id)
        .where(
            and_(
                Transaction.user_id.in_(user_ids),
                Transaction.deleted_at.is_(None)
            )
        )
        .order_by(Transaction.date.desc(), Transaction.created_at.desc())
    )
    rows = tx_result.all()
    return [
        ShortcutTransactionItem(
            id=tx.id,
            phone=phone,
            license_code=license or "--",
            date=tx.date.strftime("%Y-%m-%d"),
            time=tx.time or tx.date.strftime("%H:%M"),
            amount=float(tx.amount or 0),
            category=tx.category,
            item=tx.item,
            merchant=tx.merchant,
            notes=tx.notes,
            created_at=tx.created_at
        )
        for tx, license, phone in rows
    ]


async def _load_runtime_ai_config() -> dict:
    candidates = [
        Path(__file__).resolve().parents[3] / "public" / "config.json",
        Path("/app/public/config.json"),
        Path("/app/config.json"),
    ]
    for config_path in candidates:
        try:
            if config_path.exists():
                data = json.loads(config_path.read_text(encoding="utf-8"))
                return {
                    "api_key": data.get("api_key") or settings.AI_API_KEY,
                    "api_base": data.get("api_base") or settings.AI_API_BASE,
                    "text_model": data.get("text_model") or settings.AI_TEXT_MODEL,
                    "jj_prompt": data.get("jj_prompt") or ""
                }
        except Exception:
            continue
    urls = [
        "http://frontend/config.json",
        "http://jizhang_frontend/config.json",
    ]
    async with httpx.AsyncClient(timeout=3.0) as client:
        for url in urls:
            try:
                resp = await client.get(url)
                if resp.status_code >= 400:
                    continue
                data = resp.json()
                return {
                    "api_key": data.get("api_key") or settings.AI_API_KEY,
                    "api_base": data.get("api_base") or settings.AI_API_BASE,
                    "text_model": data.get("text_model") or settings.AI_TEXT_MODEL,
                    "jj_prompt": data.get("jj_prompt") or ""
                }
            except Exception:
                continue
    return {
        "api_key": settings.AI_API_KEY,
        "api_base": settings.AI_API_BASE,
        "text_model": settings.AI_TEXT_MODEL,
        "jj_prompt": ""
    }


async def _extract_transaction_from_text(input_text: str) -> dict:
    cfg = await _load_runtime_ai_config()
    if not cfg["jj_prompt"]:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="jj_prompt 未配置")
    now = datetime.now(ZoneInfo("Asia/Shanghai"))
    today = now.strftime("%Y-%m-%d")
    now_time = now.strftime("%H:%M")
    system_prompt = (
        cfg["jj_prompt"]
        + f"\n动态上下文：当前日期是 {today}，当前时间是 {now_time}。"
        + "\n日期时间规则：如果用户输入中包含明确日期/时间（例如 2026-03-16、3月16日、昨晚8点），必须优先使用用户输入。"
        + "\n如果用户仅说“今天/昨天/前天”，请基于当前日期推算 Date。"
        + "\n如果用户未提供任何可识别日期，则 Date 使用当前日期。"
        + "\n如果用户未提供任何可识别时间，则 Time 使用当前时间。"
    )
    payload = {
        "model": cfg["text_model"],
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"当前日期: {today}\n当前时间: {now_time}\n用户输入: {input_text}"}
        ],
        "temperature": 0.2,
        "max_tokens": 300
    }
    headers = {
        "Authorization": f"Bearer {cfg['api_key']}",
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(f"{cfg['api_base'].rstrip('/')}/chat/completions", headers=headers, json=payload)
        if resp.status_code >= 400:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="大模型调用失败")
        data = resp.json()
    content = (data.get("choices", [{}])[0].get("message", {}).get("content") or "").strip()
    if not content:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="大模型返回为空")
    line = content.splitlines()[0].strip().strip("`")
    row = next(csv.reader([line]))
    if len(row) < 6:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="大模型账单解析失败")
    text_value = (input_text or "").strip()
    eating_words = ("水果", "买菜", "食材", "早餐", "午餐", "晚餐", "吃", "喝", "外卖", "零食")
    apple_device_words = ("苹果手机", "iphone", "mac", "ipad", "airpods")
    date_str = (row[0] or "").strip()
    time_str = (row[1] or "").strip()
    amount_str = (row[2] or "").strip()
    category = (row[3] or "").strip() or "其他支出"
    item = (row[4] or "").strip() or None
    merchant = (row[5] or "").strip() or None
    if time_str in ("空", "未知", "null", "None"):
        time_str = ""
    if item in ("空", "未知", "null", "None"):
        item = None
    if merchant in ("空", "未知", "null", "None"):
        merchant = None
    lower_text = text_value.lower()
    if any(word in text_value for word in eating_words) and not any(word in lower_text for word in apple_device_words):
        category = "餐饮美食"
    if not date_str:
        date_str = today
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        dt = now
    try:
        amount = float(amount_str or 0)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="账单金额格式错误")
    if amount <= 0:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="账单金额无效")
    return {
        "date": dt,
        "time": time_str[:5] if time_str else now_time,
        "amount": amount,
        "category": category,
        "item": item,
        "merchant": merchant
    }


@router.post("/install/verify", response_model=InstallVerifyResponse)
async def verify_install(
    request: InstallVerifyRequest,
    db: AsyncSession = Depends(get_db)
):
    return await _activate_install_code(request, db)


@router.post("/install/activate", response_model=InstallVerifyResponse)
async def activate_install(
    request: InstallVerifyRequest,
    db: AsyncSession = Depends(get_db)
):
    return await _activate_install_code(request, db)


@router.post("/shortcut/install/check", response_model=InstallCheckResponse)
async def shortcut_install_check(
    request: InstallVerifyRequest,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(LicenseCode.status).where(LicenseCode.code == request.code))
    status_value = result.scalar_one_or_none()
    if status_value is None:
        return InstallCheckResponse(allowed=False, code_status="not_found", reason="授权码不存在")
    if status_value == LicenseCodeStatus.UNUSED:
        return InstallCheckResponse(allowed=True, code_status=status_value.value, reason=None)
    if status_value == LicenseCodeStatus.USED:
        return InstallCheckResponse(allowed=False, code_status=status_value.value, reason="授权码已安装激活")
    return InstallCheckResponse(allowed=False, code_status=status_value.value, reason="授权码已禁用")


@router.post("/shortcut/install/activate", response_model=InstallVerifyResponse)
async def shortcut_install_activate(
    request: InstallVerifyRequest,
    db: AsyncSession = Depends(get_db)
):
    return await _activate_install_code(request, db)


@router.post("/shortcut/transactions", response_model=ShortcutTransactionWriteResponse)
async def shortcut_create_transaction(
    payload: ShortcutTransactionCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        license_code, user = await _resolve_license_and_user(db, payload.code, require_used=True)
        tx_payload = None
        if payload.text and payload.text.strip():
            tx_payload = await _extract_transaction_from_text(payload.text.strip())
        else:
            if payload.date is None or payload.amount is None or not payload.category:
                return ShortcutTransactionWriteResponse(
                    allowed=False,
                    message="缺少记账字段，需提供 text 或 date/amount/category",
                    transaction=None
                )
            tx_payload = {
                "date": payload.date,
                "time": payload.time[:5] if payload.time else None,
                "amount": payload.amount,
                "category": payload.category,
                "item": payload.item,
                "merchant": payload.merchant
            }
        result = await db.execute(
            select(FamilyMember)
            .where(FamilyMember.user_id == user.id)
            .order_by(FamilyMember.joined_at)
        )
        family_member = result.scalar_one_or_none()
        family_id = family_member.family_id if family_member else None
        tx = Transaction(
            id=str(uuid.uuid4()),
            family_id=family_id,
            user_id=user.id,
            license_code_id=license_code.id,
            date=tx_payload["date"],
            time=tx_payload["time"],
            amount=tx_payload["amount"],
            category=tx_payload["category"],
            item=tx_payload["item"],
            merchant=tx_payload["merchant"],
            notes=payload.notes
        )
        db.add(tx)
        await db.commit()
        await db.refresh(tx)
        return ShortcutTransactionWriteResponse(
            allowed=True,
            message="写入成功",
            transaction=_build_transaction_response(tx, user.phone, license_code.code)
        )
    except HTTPException as e:
        return ShortcutTransactionWriteResponse(
            allowed=False,
            message=str(e.detail),
            transaction=None
        )
    except Exception:
        return ShortcutTransactionWriteResponse(
            allowed=False,
            message="写入失败",
            transaction=None
        )


@router.get("/shortcut/transactions/dashboard", response_model=list[ShortcutTransactionItem])
async def shortcut_dashboard_list(
    license_code: str = Query(..., min_length=6, max_length=32),
    db: AsyncSession = Depends(get_db)
):
    return await _load_shortcut_dashboard_rows(db, license_code)


@router.get("/shortcut/transactions/dashboardforcsv")
async def shortcut_dashboard_csv(
    license_code: str = Query(..., min_length=6, max_length=32),
    db: AsyncSession = Depends(get_db)
):
    rows = await _load_shortcut_dashboard_rows(db, license_code)
    stream = io.StringIO()
    writer = csv.writer(stream)
    writer.writerow(["Date", "Time", "Amount", "Category", "Item", "Merchant"])
    for item in rows:
        writer.writerow([
            item.date,
            item.time,
            f"{item.amount:.2f}",
            item.category or "",
            item.item or "",
            item.merchant or ""
        ])
    return Response(content=stream.getvalue(), media_type="text/csv; charset=utf-8")


@router.post("/transactions", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction_v2(
    transaction_data: TransactionCreate,
    current_user: User = Depends(get_current_user),
    license_code: LicenseCode = Depends(get_bound_license_code),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(FamilyMember)
        .where(FamilyMember.user_id == current_user.id)
        .order_by(FamilyMember.joined_at)
    )
    family_member = result.scalar_one_or_none()
    family_id = family_member.family_id if family_member else None

    new_transaction = Transaction(
        id=str(uuid.uuid4()),
        family_id=family_id,
        user_id=current_user.id,
        license_code_id=license_code.id,
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
    return _build_transaction_response(new_transaction, current_user.phone, license_code.code)


@router.get("/transactions", response_model=list[TransactionResponse])
async def get_transactions_v2(
    current_user: User = Depends(get_current_user),
    license_code: LicenseCode = Depends(get_bound_license_code),
    db: AsyncSession = Depends(get_db)
):
    query = (
        select(Transaction)
        .where(
            and_(
                Transaction.user_id == current_user.id,
                Transaction.license_code_id == license_code.id,
                Transaction.deleted_at.is_(None)
            )
        )
        .order_by(Transaction.date.desc(), Transaction.created_at.desc())
    )
    result = await db.execute(query)
    rows = result.scalars().all()
    return [_build_transaction_response(item, current_user.phone, license_code.code) for item in rows]


@router.delete("/transactions/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction_v2(
    transaction_id: str,
    current_user: User = Depends(get_current_user),
    license_code: LicenseCode = Depends(get_bound_license_code),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Transaction).where(
            and_(
                Transaction.id == transaction_id,
                Transaction.user_id == current_user.id,
                Transaction.license_code_id == license_code.id,
                Transaction.deleted_at.is_(None)
            )
        )
    )
    transaction = result.scalar_one_or_none()
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="交易记录不存在"
        )

    transaction.deleted_at = datetime.utcnow()
    await db.commit()


@router.get("/stats/summary", response_model=StatsSummary)
async def get_stats_summary_v2(
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    current_user: User = Depends(get_current_user),
    license_code: LicenseCode = Depends(get_bound_license_code),
    db: AsyncSession = Depends(get_db)
):
    if not start_date:
        start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if not end_date:
        end_date = datetime.now()

    conditions = [
        Transaction.user_id == current_user.id,
        Transaction.license_code_id == license_code.id,
        Transaction.deleted_at.is_(None),
        Transaction.amount > 0,
        Transaction.date >= start_date,
        Transaction.date <= end_date
    ]

    result = await db.execute(
        select(
            func.sum(Transaction.amount).label("total"),
            func.count(Transaction.id).label("count"),
            func.avg(Transaction.amount).label("average"),
            func.max(Transaction.amount).label("maximum")
        ).where(and_(*conditions))
    )
    row = result.one()
    return StatsSummary(
        total_expense=float(row.total or 0),
        transaction_count=int(row.count or 0),
        average_amount=float(row.average or 0),
        max_amount=float(row.maximum or 0)
    )


@router.get("/stats/category", response_model=list[CategoryStats])
async def get_stats_category_v2(
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    current_user: User = Depends(get_current_user),
    license_code: LicenseCode = Depends(get_bound_license_code),
    db: AsyncSession = Depends(get_db)
):
    if not start_date:
        start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if not end_date:
        end_date = datetime.now()

    conditions = [
        Transaction.user_id == current_user.id,
        Transaction.license_code_id == license_code.id,
        Transaction.deleted_at.is_(None),
        Transaction.amount > 0,
        Transaction.date >= start_date,
        Transaction.date <= end_date
    ]
    result = await db.execute(
        select(
            Transaction.category,
            func.sum(Transaction.amount).label("total"),
            func.count(Transaction.id).label("count")
        )
        .where(and_(*conditions))
        .group_by(Transaction.category)
        .order_by(func.sum(Transaction.amount).desc())
    )
    return [
        CategoryStats(category=row.category, amount=float(row.total or 0), count=int(row.count or 0))
        for row in result.all()
    ]


@router.get("/stats/trend", response_model=list[TrendData])
async def get_stats_trend_v2(
    period: str = Query("month", pattern="^(day|week|month|year)$"),
    current_user: User = Depends(get_current_user),
    license_code: LicenseCode = Depends(get_bound_license_code),
    db: AsyncSession = Depends(get_db)
):
    now = datetime.now()
    base = [
        Transaction.user_id == current_user.id,
        Transaction.license_code_id == license_code.id,
        Transaction.deleted_at.is_(None),
        Transaction.amount > 0
    ]
    if period == "day":
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        result = await db.execute(
            select(
                extract("hour", Transaction.date).label("p"),
                func.sum(Transaction.amount).label("a")
            )
            .where(and_(*base, Transaction.date >= start_date))
            .group_by(extract("hour", Transaction.date))
            .order_by(extract("hour", Transaction.date))
        )
        return [TrendData(date=f"{int(r.p)}:00", amount=float(r.a or 0)) for r in result.all()]
    if period == "week":
        start_date = now - timedelta(days=7)
        result = await db.execute(
            select(func.date(Transaction.date).label("p"), func.sum(Transaction.amount).label("a"))
            .where(and_(*base, Transaction.date >= start_date))
            .group_by(func.date(Transaction.date))
            .order_by(func.date(Transaction.date))
        )
        return [TrendData(date=str(r.p), amount=float(r.a or 0)) for r in result.all()]
    if period == "year":
        start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        result = await db.execute(
            select(extract("month", Transaction.date).label("p"), func.sum(Transaction.amount).label("a"))
            .where(and_(*base, Transaction.date >= start_date))
            .group_by(extract("month", Transaction.date))
            .order_by(extract("month", Transaction.date))
        )
        return [TrendData(date=f"{int(r.p)}月", amount=float(r.a or 0)) for r in result.all()]
    start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    result = await db.execute(
        select(func.date(Transaction.date).label("p"), func.sum(Transaction.amount).label("a"))
        .where(and_(*base, Transaction.date >= start_date))
        .group_by(func.date(Transaction.date))
        .order_by(func.date(Transaction.date))
    )
    return [TrendData(date=str(r.p), amount=float(r.a or 0)) for r in result.all()]


@router.get("/stats/license-distribution", response_model=list[LicenseDistributionItem])
async def get_stats_license_distribution_v2(
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    current_user: User = Depends(get_current_user),
    _: LicenseCode = Depends(get_bound_license_code),
    db: AsyncSession = Depends(get_db)
):
    if not start_date:
        start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if not end_date:
        end_date = datetime.now()
    result = await db.execute(
        select(
            LicenseCode.code.label("license_code"),
            func.sum(Transaction.amount).label("amount"),
            func.count(Transaction.id).label("count")
        )
        .join(LicenseCode, LicenseCode.id == Transaction.license_code_id)
        .where(
            and_(
                Transaction.user_id == current_user.id,
                Transaction.deleted_at.is_(None),
                Transaction.amount > 0,
                Transaction.date >= start_date,
                Transaction.date <= end_date
            )
        )
        .group_by(LicenseCode.code)
        .order_by(func.sum(Transaction.amount).desc())
    )
    return [
        LicenseDistributionItem(
            license_code=row.license_code,
            amount=float(row.amount or 0),
            count=int(row.count or 0)
        )
        for row in result.all()
    ]


@router.post("/budgets", response_model=BudgetResponse, status_code=status.HTTP_201_CREATED)
async def create_budget_v2(
    budget_data: BudgetCreate,
    current_user: User = Depends(get_current_user),
    _: LicenseCode = Depends(get_bound_license_code),
    db: AsyncSession = Depends(get_db)
):
    if budget_data.month is None and budget_data.category is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="默认预算仅支持总预算")
    if budget_data.month is None:
        existing_result = await db.execute(
            select(Budget).where(
                and_(
                    Budget.user_id == current_user.id,
                    Budget.year == budget_data.year,
                    Budget.month.is_(None),
                    Budget.category.is_(None)
                )
            )
        )
        existing_default = existing_result.scalar_one_or_none()
        if existing_default:
            existing_default.amount = budget_data.amount
            existing_default.period = "monthly"
            await db.commit()
            await db.refresh(existing_default)
            return existing_default
    else:
        existing_result = await db.execute(
            select(Budget).where(
                and_(
                    Budget.user_id == current_user.id,
                    Budget.year == budget_data.year,
                    Budget.month == budget_data.month,
                    Budget.category == budget_data.category
                )
            )
        )
        existing_budget = existing_result.scalar_one_or_none()
        if existing_budget:
            existing_budget.amount = budget_data.amount
            existing_budget.period = "monthly"
            await db.commit()
            await db.refresh(existing_budget)
            return existing_budget
    budget = Budget(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        family_id=None,
        category=budget_data.category,
        amount=budget_data.amount,
        period="monthly",
        year=budget_data.year,
        month=budget_data.month
    )
    db.add(budget)
    await db.commit()
    await db.refresh(budget)
    return budget


@router.get("/budgets/status", response_model=list[BudgetStatusResponse])
async def get_budget_status_v2(
    year: int,
    month: int,
    current_user: User = Depends(get_current_user),
    license_code: LicenseCode = Depends(get_bound_license_code),
    db: AsyncSession = Depends(get_db)
):
    budgets_result = await db.execute(
        select(Budget).where(
            and_(
                Budget.user_id == current_user.id,
                Budget.year == year,
                Budget.month == month
            )
        )
    )
    budgets = budgets_result.scalars().all()
    has_total_budget = any(item.category is None for item in budgets)
    if not has_total_budget:
        default_result = await db.execute(
            select(Budget).where(
                and_(
                    Budget.user_id == current_user.id,
                    Budget.year == year,
                    Budget.month.is_(None),
                    Budget.category.is_(None)
                )
            )
        )
        default_budget = default_result.scalar_one_or_none()
        if default_budget:
            filled_budget = Budget(
                id=str(uuid.uuid4()),
                user_id=current_user.id,
                family_id=None,
                category=None,
                amount=default_budget.amount,
                period="monthly",
                year=year,
                month=month
            )
            db.add(filled_budget)
            await db.commit()
            await db.refresh(filled_budget)
            budgets.append(filled_budget)
    start_date = datetime(year, month, 1)
    end_date = datetime(year + (1 if month == 12 else 0), 1 if month == 12 else month + 1, 1) - timedelta(milliseconds=1)
    items: list[BudgetStatusResponse] = []
    for b in budgets:
        spend_conditions = [
            Transaction.user_id == current_user.id,
            Transaction.license_code_id == license_code.id,
            Transaction.deleted_at.is_(None),
            Transaction.amount > 0,
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ]
        if b.category:
            spend_conditions.append(Transaction.category == b.category)
        spend_result = await db.execute(select(func.sum(Transaction.amount)).where(and_(*spend_conditions)))
        spent = float(spend_result.scalar() or 0)
        remaining = float(b.amount - spent)
        pct = 0.0 if b.amount <= 0 else (spent / b.amount) * 100
        items.append(
            BudgetStatusResponse(
                budget_id=b.id,
                category=b.category,
                budget_amount=float(b.amount),
                spent_amount=spent,
                remaining_amount=remaining,
                percentage=float(pct),
                is_over_budget=spent > float(b.amount),
                period=b.period,
                year=b.year,
                month=b.month
            )
        )
    return items


@router.delete("/budgets/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_budget_v2(
    budget_id: str,
    current_user: User = Depends(get_current_user),
    _: LicenseCode = Depends(get_bound_license_code),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Budget).where(and_(Budget.id == budget_id, Budget.user_id == current_user.id))
    )
    budget = result.scalar_one_or_none()
    if not budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="预算不存在")
    await db.delete(budget)
    await db.commit()
    return None


@router.get("/budgets/monthly-status", response_model=list[BudgetMonthlyResponse])
async def get_budget_monthly_status_v2(
    year: int = Query(...),
    current_user: User = Depends(get_current_user),
    license_code: LicenseCode = Depends(get_bound_license_code),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Budget).where(
            and_(
                Budget.user_id == current_user.id,
                Budget.year == year,
                Budget.category.is_(None)
            )
        )
    )
    budgets = result.scalars().all()
    default_budget_amount = float(next((item.amount for item in budgets if item.month is None), 0))
    budget_map = {int(item.month): float(item.amount) for item in budgets if item.month}
    items: list[BudgetMonthlyResponse] = []
    for month in range(1, 13):
        start_date = datetime(year, month, 1)
        end_date = datetime(year + (1 if month == 12 else 0), 1 if month == 12 else month + 1, 1) - timedelta(milliseconds=1)
        spend_result = await db.execute(
            select(func.sum(Transaction.amount)).where(
                and_(
                    Transaction.user_id == current_user.id,
                    Transaction.license_code_id == license_code.id,
                    Transaction.deleted_at.is_(None),
                    Transaction.amount > 0,
                    Transaction.date >= start_date,
                    Transaction.date <= end_date
                )
            )
        )
        spent = float(spend_result.scalar() or 0)
        budget_amount = float(budget_map.get(month, default_budget_amount))
        remaining = float(budget_amount - spent)
        percentage = 0.0 if budget_amount <= 0 else (spent / budget_amount) * 100
        items.append(
            BudgetMonthlyResponse(
                year=year,
                month=month,
                budget_amount=budget_amount,
                spent_amount=spent,
                remaining_amount=remaining,
                percentage=float(percentage),
                is_over_budget=budget_amount > 0 and spent > budget_amount
            )
        )
    return items
