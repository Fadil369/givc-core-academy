"""
n8n MCP Server Configuration
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class N8NSettings(BaseSettings):
    """n8n MCP server configuration"""
    
    model_config = SettingsConfigDict(env_prefix='N8N_', case_sensitive=False)
    
    # Server URL
    server_url: str = "https://n8n.srv791040.hstgr.cloud/mcp-server/http"
    
    # Authentication
    api_key: str = ""
    username: str = ""
    password: str = ""
    
    # Timeouts
    timeout: int = 120
    connection_timeout: int = 10
    
    # Retry settings
    max_retries: int = 3
    retry_delay: int = 1
    
    # Workflows
    openai_workflow: str = "openai_completion"
    nphies_workflow: str = "nphies_api_call"
    notification_workflow: str = "send_notification"
    jira_workflow: str = "create_jira_ticket"
    
    # Feature flags
    enabled: bool = True
    use_for_openai: bool = True
    use_for_nphies: bool = True
    use_for_notifications: bool = True
