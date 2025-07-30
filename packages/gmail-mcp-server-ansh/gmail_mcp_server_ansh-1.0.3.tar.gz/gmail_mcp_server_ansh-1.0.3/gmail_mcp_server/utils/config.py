"""
Configuration utilities for Gmail MCP Server
"""

from typing import Optional
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """Configuration settings for Gmail MCP Server"""
    
    # Server settings
    server_name: str = "gmail_server"
    server_port: int = 8010
    log_level: str = "INFO"
    cache_expiration_seconds: int = 60
    
    # Gmail API settings
    gmail_api_timeout: int = 30
    
    # Transport settings
    transport: str = "stdio"
    
    class Config:
        env_prefix = "GMAIL_MCP_"
        case_sensitive = False 