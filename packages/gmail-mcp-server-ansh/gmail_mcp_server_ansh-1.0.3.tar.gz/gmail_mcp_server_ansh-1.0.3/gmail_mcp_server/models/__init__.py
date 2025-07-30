"""
Pydantic models for Gmail MCP Server
"""

from .email_models import EmailSearchParams, EmailSendParams, EmailDetailParams

__all__ = ["EmailSearchParams", "EmailSendParams", "EmailDetailParams"] 