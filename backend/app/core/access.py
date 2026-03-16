from fastapi import Depends, HTTPException, Header, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import User, LicenseCode, SystemRole, LicenseCodeStatus
from app.core.security import get_current_user


async def get_current_root_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.system_role != SystemRole.ROOT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="仅 root 用户可访问"
        )
    return current_user


async def get_bound_license_code(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    x_license_code: str | None = Header(default=None, alias="X-License-Code")
) -> LicenseCode:
    if x_license_code:
        result = await db.execute(
            select(LicenseCode).where(LicenseCode.code == x_license_code)
        )
        license_code = result.scalar_one_or_none()
        if not license_code:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="授权码无效"
            )
        if license_code.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="授权码与当前账号不匹配"
            )
        if license_code.status != LicenseCodeStatus.USED:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="授权码不可用"
            )
        return license_code

    used_result = await db.execute(
        select(LicenseCode)
        .where(
            LicenseCode.user_id == current_user.id,
            LicenseCode.status == LicenseCodeStatus.USED
        )
        .order_by(LicenseCode.used_at.desc(), LicenseCode.created_at.desc())
    )
    fallback = used_result.scalars().first()
    if not fallback:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="未检测到已激活授权码"
        )
    return fallback
