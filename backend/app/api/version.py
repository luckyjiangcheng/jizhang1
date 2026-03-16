from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from datetime import datetime
import uuid
import csv
import io
from fastapi.responses import StreamingResponse
from app.database import get_db
from app.models import User, Transaction, FamilyMember
from app.core.security import get_current_user
from app.core.access import get_bound_license_code
from app.schemas import MigrateRequest, MigrateResponse, ExportResponse, SwitchVersionRequest, SwitchVersionResponse, VersionStatusResponse
from app.utils.contracts import normalize_csv_headers, read_csv_value, parse_csv_date

router = APIRouter(dependencies=[Depends(get_bound_license_code)])


@router.post("/migrate-to-server", response_model=MigrateResponse)
async def migrate_to_server(
    request: MigrateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    将本地CSV数据迁移到服务端
    """
    # 获取用户的默认家庭
    result = await db.execute(
        select(FamilyMember)
        .where(FamilyMember.user_id == current_user.id)
        .order_by(FamilyMember.joined_at)
    )
    family_member = result.scalar_one_or_none()
    
    # 确定家庭ID（如果用户加入了家庭）
    family_id = family_member.family_id if family_member else None
    
    # 解析CSV数据
    try:
        reader = csv.DictReader(io.StringIO(request.csv_data))
        migrated_count = 0
        failed_count = 0
        
        for row in reader:
            try:
                normalized_row = normalize_csv_headers(row)
                if not any((v or "").strip() for v in normalized_row.values()):
                    continue

                date_value = read_csv_value(normalized_row, "date", "日期")
                time_value = read_csv_value(normalized_row, "time", "时间")
                amount_value = read_csv_value(normalized_row, "amount", "金额", default="0")
                category_value = read_csv_value(normalized_row, "category", "分类", default="其他支出")
                item_value = read_csv_value(normalized_row, "item", "项目")
                merchant_value = read_csv_value(normalized_row, "merchant", "商家")
                notes_value = read_csv_value(normalized_row, "notes", "备注")

                # 创建新交易
                new_transaction = Transaction(
                    id=str(uuid.uuid4()),
                    family_id=family_id,
                    user_id=current_user.id,
                    date=parse_csv_date(date_value),
                    time=time_value[:5] if time_value else "",
                    amount=float(amount_value or 0),
                    category=category_value or "其他支出",
                    item=item_value,
                    merchant=merchant_value,
                    notes=notes_value
                )
                
                db.add(new_transaction)
                migrated_count += 1
                
            except (ValueError, KeyError) as e:
                failed_count += 1
                continue
        
        # 提交所有交易
        await db.commit()
        
        return MigrateResponse(
            message="数据迁移完成",
            migrated_count=migrated_count,
            failed_count=failed_count,
            family_id=family_id
        )
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据迁移失败: {str(e)}"
        )


@router.get("/export-csv", response_model=ExportResponse)
async def export_csv(
    family_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    导出交易数据为CSV格式
    """
    # 构建查询条件
    from sqlalchemy import and_, or_
    
    conditions = [Transaction.user_id == current_user.id]
    
    # 如果指定了家庭ID，验证用户是否是家庭成员
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
        
        # 查询家庭交易
        conditions = [Transaction.family_id == family_id]
    
    if start_date:
        conditions.append(Transaction.date >= start_date)
    
    if end_date:
        conditions.append(Transaction.date <= end_date)

    conditions.append(Transaction.deleted_at.is_(None))
    
    # 查询交易数据
    result = await db.execute(
        select(Transaction)
        .where(and_(*conditions))
        .order_by(Transaction.date.desc())
    )
    transactions = result.scalars().all()
    
    # 生成CSV
    output = io.StringIO()
    fieldnames = ['Date', 'Time', 'Amount', 'Category', 'Item', 'Merchant', 'Notes']
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    
    # 写入表头
    writer.writeheader()
    
    # 写入数据
    for tx in transactions:
        writer.writerow({
            'Date': tx.date.strftime('%Y-%m-%d'),
            'Time': tx.time or '',
            'Amount': str(tx.amount),
            'Category': tx.category,
            'Item': tx.item or '',
            'Merchant': tx.merchant or '',
            'Notes': tx.notes or ''
        })
    
    # 返回CSV内容
    csv_content = output.getvalue()
    
    return ExportResponse(
        filename=f"transactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        content=csv_content,
        count=len(transactions)
    )


@router.get("/export-excel")
async def export_excel(
    family_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    from sqlalchemy import and_
    from openpyxl import Workbook

    conditions = [Transaction.user_id == current_user.id]
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
        conditions = [Transaction.family_id == family_id]

    if start_date:
        conditions.append(Transaction.date >= start_date)
    if end_date:
        conditions.append(Transaction.date <= end_date)
    conditions.append(Transaction.deleted_at.is_(None))

    result = await db.execute(
        select(Transaction)
        .where(and_(*conditions))
        .order_by(Transaction.date.desc(), Transaction.created_at.desc())
    )
    transactions = result.scalars().all()

    wb = Workbook()
    ws = wb.active
    ws.title = "Transactions"

    headers = ['Date', 'Time', 'Amount', 'Category', 'Item', 'Merchant', 'Notes']
    ws.append(headers)
    for tx in transactions:
        ws.append([
            tx.date.strftime('%Y-%m-%d'),
            tx.time or '',
            float(tx.amount),
            tx.category,
            tx.item or '',
            tx.merchant or '',
            tx.notes or ''
        ])

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    filename = f"transactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


@router.get("/export-pdf")
async def export_pdf(
    family_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    from sqlalchemy import and_
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    conditions = [Transaction.user_id == current_user.id]
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
        conditions = [Transaction.family_id == family_id]

    if start_date:
        conditions.append(Transaction.date >= start_date)
    if end_date:
        conditions.append(Transaction.date <= end_date)
    conditions.append(Transaction.deleted_at.is_(None))

    result = await db.execute(
        select(Transaction)
        .where(and_(*conditions))
        .order_by(Transaction.date.desc(), Transaction.created_at.desc())
    )
    transactions = result.scalars().all()

    output = io.BytesIO()
    c = canvas.Canvas(output, pagesize=A4)
    width, height = A4

    y = height - 48
    c.setFont("Helvetica", 14)
    c.drawString(36, y, "Transactions Export")
    y -= 20
    c.setFont("Helvetica", 10)
    range_text = f"Range: {start_date.isoformat() if start_date else '-'} ~ {end_date.isoformat() if end_date else '-'}"
    c.drawString(36, y, range_text)
    y -= 18
    c.drawString(36, y, f"Count: {len(transactions)}")
    y -= 22

    c.setFont("Helvetica", 9)
    for tx in transactions:
        line = f"{tx.date.strftime('%Y-%m-%d')} {tx.time or ''} | {tx.category} | {tx.item or tx.merchant or ''} | {tx.amount:.2f}"
        if y < 48:
            c.showPage()
            y = height - 48
            c.setFont("Helvetica", 9)
        c.drawString(36, y, line[:140])
        y -= 14

    c.showPage()
    c.save()
    output.seek(0)

    filename = f"transactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    return StreamingResponse(
        output,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


@router.post("/switch-version", response_model=SwitchVersionResponse)
async def switch_version(
    request: SwitchVersionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    切换版本（本地版本和服务端版本）
    """
    if request.target_version not in ["local", "server"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的版本类型，必须是 'local' 或 'server'"
        )
    
    # 这里可以记录用户的版本偏好
    # 实际的切换逻辑由前端控制
    return SwitchVersionResponse(
        message=f"已切换到{request.target_version}版本",
        target_version=request.target_version,
        timestamp=datetime.now().isoformat()
    )


@router.get("/version-status", response_model=VersionStatusResponse)
async def get_version_status(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取用户版本状态
    """
    # 检查用户是否有服务端数据（包括个人交易和家庭交易）
    result = await db.execute(
        select(Transaction)
        .where(Transaction.user_id == current_user.id)
        .limit(1)
    )
    has_server_data = result.scalar_one_or_none() is not None
    
    # 计算服务端数据数量
    server_data_count = 0
    if has_server_data:
        result = await db.execute(
            select(func.count(Transaction.id))
            .where(Transaction.user_id == current_user.id)
        )
        server_data_count = result.scalar() or 0
    
    return VersionStatusResponse(
        current_version="server" if has_server_data else "local",
        has_server_data=has_server_data,
        server_data_count=server_data_count
    )
