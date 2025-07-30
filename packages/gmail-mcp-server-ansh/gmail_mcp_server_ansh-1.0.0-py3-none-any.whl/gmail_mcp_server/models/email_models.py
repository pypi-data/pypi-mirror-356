"""
Pydantic models for email operations
"""

from typing import Optional
from pydantic import BaseModel, Field


class EmailSearchParams(BaseModel):
    """Parameters for email search operations"""
    query: str = Field(..., description="Gmail search query (e.g., 'from:example@gmail.com', 'subject:meeting', 'is:unread')")
    max_results: int = Field(default=10, description="Maximum number of emails to return (1-50)")
    include_body: bool = Field(default=False, description="Whether to include email body content in results")


class EmailSendParams(BaseModel):
    """Parameters for sending emails"""
    to: str = Field(..., description="Recipient email address")
    subject: str = Field(..., description="Email subject line")
    body: str = Field(..., description="Email body content (plain text)")
    cc: Optional[str] = Field(None, description="CC recipients (comma-separated)")
    bcc: Optional[str] = Field(None, description="BCC recipients (comma-separated)")


class EmailDetailParams(BaseModel):
    """Parameters for getting email details"""
    message_id: str = Field(..., description="Gmail message ID to retrieve details for") 