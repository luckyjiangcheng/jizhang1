from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# 创建异步引擎
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # 开发环境显示SQL，生产环境设为False
    pool_size=10,  # 连接池大小
    max_overflow=20,  # 最大溢出连接数
    pool_pre_ping=True,  # 连接池ping检查
    pool_recycle=3600,  # 连接回收时间（秒）
)

# 创建异步会话工厂
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# 声明基类
Base = declarative_base()

# 数据库依赖
async def get_db():
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()