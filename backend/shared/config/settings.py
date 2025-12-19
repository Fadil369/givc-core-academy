"""
BrainSAIT LINC Agents - Configuration Management
Centralized configuration with validation and type safety
"""

from typing import List, Optional
from functools import lru_cache
from pydantic import Field, field_validator, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Database configuration"""
    
    model_config = SettingsConfigDict(env_prefix='POSTGRES_', case_sensitive=False)
    
    host: str = "localhost"
    port: int = 5432
    db: str = "brainsait_linc"
    user: str = "brainsait"
    password: str = "password"
    pool_size: int = 20
    max_overflow: int = 10
    
    @property
    def url(self) -> str:
        """Generate PostgreSQL connection URL"""
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
    
    @property
    def sync_url(self) -> str:
        """Generate synchronous PostgreSQL connection URL"""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class RedisSettings(BaseSettings):
    """Redis cache configuration"""
    
    model_config = SettingsConfigDict(env_prefix='REDIS_', case_sensitive=False)
    
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None
    pool_size: int = 10
    ttl: int = 3600
    
    @property
    def url(self) -> str:
        """Generate Redis connection URL"""
        if self.password:
            return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"
        return f"redis://{self.host}:{self.port}/{self.db}"


class MongoDBSettings(BaseSettings):
    """MongoDB configuration"""
    
    model_config = SettingsConfigDict(env_prefix='MONGODB_', case_sensitive=False)
    
    host: str = "localhost"
    port: int = 27017
    db: str = "brainsait_analytics"
    user: Optional[str] = None
    password: Optional[str] = None
    
    @property
    def uri(self) -> str:
        """Generate MongoDB connection URI"""
        if self.user and self.password:
            return f"mongodb://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
        return f"mongodb://{self.host}:{self.port}/{self.db}"


class OpenAISettings(BaseSettings):
    """OpenAI API configuration"""
    
    model_config = SettingsConfigDict(env_prefix='OPENAI_', case_sensitive=False)
    
    api_key: str = ""
    org_id: Optional[str] = None
    model_gpt4: str = "gpt-4"
    model_gpt4_turbo: str = "gpt-4-turbo-preview"
    temperature: float = 0.3
    max_tokens: int = 2000
    timeout: int = 60


class NPHIESSettings(BaseSettings):
    """NPHIES API configuration"""
    
    model_config = SettingsConfigDict(env_prefix='NPHIES_', case_sensitive=False)
    
    base_url: str = "https://nphies.sa/api/v1"
    api_key: str = ""
    client_id: str = ""
    client_secret: str = ""
    timeout: int = 30
    environment: str = "sandbox"  # sandbox or production
    
    @property
    def claims_url(self) -> str:
        return f"{self.base_url}/claims"
    
    @property
    def referral_url(self) -> str:
        return f"{self.base_url}/referrals"
    
    @property
    def authorization_url(self) -> str:
        return f"{self.base_url}/authorizations"


class SecuritySettings(BaseSettings):
    """Security and authentication configuration"""
    
    model_config = SettingsConfigDict(case_sensitive=False)
    
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7
    encryption_key: str = ""
    phi_encryption_enabled: bool = True
    phi_encryption_algorithm: str = "AES-256-GCM"


class HIPAASettings(BaseSettings):
    """HIPAA compliance configuration"""
    
    model_config = SettingsConfigDict(env_prefix='HIPAA_', case_sensitive=False)
    
    enabled: bool = True
    audit_logging: bool = True
    data_encryption: bool = True
    access_control: bool = True
    breach_notification: bool = True


class MonitoringSettings(BaseSettings):
    """Monitoring and observability configuration"""
    
    model_config = SettingsConfigDict(case_sensitive=False)
    
    sentry_dsn: Optional[str] = None
    sentry_environment: str = "development"
    sentry_traces_sample_rate: float = 0.1
    prometheus_enabled: bool = True
    prometheus_port: int = 9090


class N8NSettings(BaseSettings):
    """n8n MCP server configuration"""
    
    model_config = SettingsConfigDict(env_prefix='N8N_', case_sensitive=False)
    
    server_url: str = "https://n8n.srv791040.hstgr.cloud/mcp-server/http"
    api_key: str = ""
    username: str = ""
    password: str = ""
    timeout: int = 120
    connection_timeout: int = 10
    max_retries: int = 3
    retry_delay: int = 1
    enabled: bool = True
    use_for_openai: bool = True
    use_for_nphies: bool = True
    use_for_notifications: bool = True


class AgentSettings(BaseSettings):
    """Agent-specific configuration"""
    
    model_config = SettingsConfigDict(case_sensitive=False)
    
    # MASTERLINC
    masterlinc_port: int = 8000
    masterlinc_health_check_interval: int = 300
    masterlinc_retry_attempts: int = 3
    masterlinc_timeout: int = 30
    
    # HEALTHCARELINC
    healthcarelinc_port: int = 8001
    healthcarelinc_fhir_validation: bool = True
    healthcarelinc_nphies_integration: bool = True
    
    # CLAIMLINC
    claimlinc_port: int = 8002
    claimlinc_auto_resubmit: bool = False
    claimlinc_manual_review_threshold: float = 0.7
    
    # TTLINC
    ttlinc_port: int = 8003
    ttlinc_quality_threshold: float = 0.85
    ttlinc_cache_translations: bool = True
    
    # POLICYLINC
    policylinc_port: int = 8004
    policylinc_cache_policies: bool = True
    
    # CLINICALLINC
    clinicallinc_port: int = 8005
    clinicallinc_use_guidelines: bool = True
    
    # RADIOLINC
    radiolinc_port: int = 8006
    radiolinc_dicom_support: bool = True


class Settings(BaseSettings):
    """Main application settings"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application
    app_name: str = "BrainSAIT LINC Agents"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = False
    log_level: str = "INFO"
    
    # Organization
    org_name: str = "BrainSAIT LTD"
    org_oid: str = "1.3.6.1.4.1.61026"
    org_region: str = "Saudi Arabia"
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_prefix: str = "/api/v1"
    api_docs_enabled: bool = True
    
    # CORS
    cors_origins: List[str] = ["*"]
    cors_credentials: bool = True
    cors_methods: List[str] = ["GET", "POST", "PUT", "DELETE", "PATCH"]
    cors_headers: List[str] = ["*"]
    
    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_per_minute: int = 60
    rate_limit_per_hour: int = 1000
    rate_limit_per_day: int = 10000
    
    # Bilingual Support
    default_language: str = "en"
    supported_languages: List[str] = ["ar", "en"]
    rtl_languages: List[str] = ["ar"]
    
    # Sub-configurations
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    mongodb: MongoDBSettings = Field(default_factory=MongoDBSettings)
    openai: OpenAISettings = Field(default_factory=OpenAISettings)
    nphies: NPHIESSettings = Field(default_factory=NPHIESSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    hipaa: HIPAASettings = Field(default_factory=HIPAASettings)
    monitoring: MonitoringSettings = Field(default_factory=MonitoringSettings)
    agents: AgentSettings = Field(default_factory=AgentSettings)
    n8n: N8NSettings = Field(default_factory=N8NSettings)
    
    @property
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.environment.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development"""
        return self.environment.lower() == "development"
    
    def get_agent_base_url(self, agent_name: str) -> str:
        """Get base URL for a specific agent"""
        agent_ports = {
            "masterlinc": self.agents.masterlinc_port,
            "healthcarelinc": self.agents.healthcarelinc_port,
            "claimlinc": self.agents.claimlinc_port,
            "ttlinc": self.agents.ttlinc_port,
            "policylinc": self.agents.policylinc_port,
            "clinicallinc": self.agents.clinicallinc_port,
            "radiolinc": self.agents.radiolinc_port,
        }
        port = agent_ports.get(agent_name.lower(), 8000)
        return f"http://localhost:{port}"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Export settings instance
settings = get_settings()
