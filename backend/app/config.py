from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # 数据库配置
    DATABASE_URL: str = "mysql+aiomysql://jizhang_user:jizhang_password@localhost:3306/jizhang_db"
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379"
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ROOT_USERNAME: str = "root"
    ROOT_EMAIL: str = "root@local.dev"
    ROOT_PASSWORD: str = "root123456"
    
    # AI服务配置
    AI_API_KEY: str = "sk-ohgicalwixwraxcmzckymthpjnktwzokmuzrakwtbkibxabf"
    AI_API_BASE: str = "https://api.siliconflow.cn/v1"
    AI_TEXT_MODEL: str = "deepseek-ai/DeepSeek-V3"
    AI_VISION_MODEL: str = "Qwen/Qwen2-VL-72B-Instruct"
    
    # 应用配置
    APP_NAME: str = "记账小助手"
    APP_VERSION: str = "1.0.0"
    ENABLE_V1_PUBLIC_API: bool = False
    
    # CORS配置
    ALLOWED_ORIGINS: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
