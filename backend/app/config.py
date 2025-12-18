"""Application Configuration"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "GIVC Core Academy"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./givc_academy.db"
    )
    
    # PostgreSQL for production
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "givc")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "givc123")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "givc_academy")
    
    # Redis
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    
    # Celery
    CELERY_BROKER_URL: str = os.getenv(
        "CELERY_BROKER_URL", 
        f"redis://{REDIS_HOST}:{REDIS_PORT}/1"
    )
    CELERY_RESULT_BACKEND: str = os.getenv(
        "CELERY_RESULT_BACKEND",
        f"redis://{REDIS_HOST}:{REDIS_PORT}/2"
    )
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.SECRET_KEY and not self.DEBUG:
            raise ValueError("SECRET_KEY must be set in production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # MFA
    MFA_ISSUER: str = "GIVC Core Academy"
    
    # CORS
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
    # Stripe
    STRIPE_API_KEY: str = os.getenv("STRIPE_API_KEY", "")
    STRIPE_WEBHOOK_SECRET: str = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    
    # VAT
    VAT_RATE: float = 0.15  # Saudi Arabia 15% VAT
    
    # Saudi-specific
    CHI_API_URL: Optional[str] = None
    MOH_API_URL: Optional[str] = None
    SCFHS_API_URL: Optional[str] = None
    
    # Email (for notifications)
    SMTP_HOST: str = os.getenv("SMTP_HOST", "localhost")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    
    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
