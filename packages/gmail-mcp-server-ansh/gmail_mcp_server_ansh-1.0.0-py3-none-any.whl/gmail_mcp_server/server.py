"""
Main Gmail MCP Server
"""

import argparse
from fastmcp import FastMCP
from gmail_mcp_server.utils import Config
from gmail_mcp_server.tools import (
    search_emails,
    get_recent_emails,
    get_email_details,
    send_email,
    list_gmail_labels,
    get_emails_by_label,
    set_tokens
)


class GmailMCPServer:
    """Gmail MCP Server implementation"""
    
    def __init__(self, config: Config):
        self.config = config
        self.mcp = FastMCP(
            name=config.server_name,
            port=config.server_port,
            log_level=config.log_level,
            cache_expiration_seconds=config.cache_expiration_seconds,
        )
        self._register_tools()
    
    def _register_tools(self):
        """Register all MCP tools with the server"""
        
        @self.mcp.tool(
            name_or_fn="search_emails",
            description="""Search Gmail emails using Gmail search syntax.

            Input: {"params": {"query": "search_term", "max_results": 10, "include_body": false}}
            
            Examples:
            - {"params": {"query": "after:2025/06/17", "max_results": 5, "include_body": false}}
            - {"params": {"query": "from:example@gmail.com", "max_results": 10, "include_body": true}}
            - {"params": {"query": "subject:meeting", "max_results": 20, "include_body": false}}
            
            Output: JSON with success status, message, total_results, and emails array containing id, subject, from, date, snippet, and optional body content.
            
            Gmail Search Operators: after:YYYY/MM/DD, from:email, subject:term, is:unread, has:attachment, label:important"""
        )
        async def search_emails_tool(params):
            return await search_emails(params)
        
        @self.mcp.tool(
            name_or_fn="get_recent_emails", 
            description="""Get the most recent emails from inbox.

            Input: {"max_results": 10}
            
            Examples:
            - {"max_results": 5}
            - {"max_results": 20}
            
            Output: JSON with success status, message, total_results, and emails array containing id, subject, from, date, snippet.
            
            Usage: Use to quickly view latest emails. For full content, use get_email_details with returned message_id."""
        )
        async def get_recent_emails_tool(max_results: int = 10):
            return await get_recent_emails(max_results)
        
        @self.mcp.tool(
            name_or_fn="get_email_details",
            description="""Get complete details of a specific email including full body content.

            Input: {"params": {"message_id": "email_id_here"}}
            
            Examples:
            - {"params": {"message_id": "18c1234567890abcdef"}}
            
            Output: JSON with success status and email object containing id, subject, from, to, date, body (plain_text only), labels, size_estimate.
            
            Usage: Use message_id from search results or recent emails to get full email content in plain text format."""
        )
        async def get_email_details_tool(params):
            return await get_email_details(params)
        
        @self.mcp.tool(
            name_or_fn="send_email",
            description="""Send an email via Gmail.

            Input: {"params": {"to": "recipient@email.com", "subject": "Email Subject", "body": "Email content", "cc": "cc@email.com", "bcc": "bcc@email.com"}}
            
            Examples:
            - {"params": {"to": "user@gmail.com", "subject": "Hello", "body": "This is a test email"}}
            - {"params": {"to": "user@gmail.com", "subject": "Meeting", "body": "Let's meet tomorrow", "cc": "colleague@gmail.com"}}
            
            Output: JSON with success status, message, message_id, thread_id, and recipients info.
            
            Usage: CC and BCC are optional. Use comma-separated addresses for multiple recipients in CC/BCC fields."""
        )
        async def send_email_tool(params):
            return await send_email(params)
        
        @self.mcp.tool(
            name_or_fn="list_gmail_labels",
            description="""List all Gmail labels including system and user-created labels.

            Input: {}
            
            Examples:
            - {}
            
            Output: JSON with labels array containing id and name for each label.
            
            Usage: Use to get available labels like 'INBOX', 'STARRED', 'IMPORTANT', or custom labels for use with get_emails_by_label."""
        )
        async def list_gmail_labels_tool():
            return await list_gmail_labels()
        
        @self.mcp.tool(
            name_or_fn="get_emails_by_label",
            description="""Fetch emails that belong to a specific Gmail label.

            Input: {"label_id": "label_id_here", "max_results": 10}
            
            Examples:
            - {"label_id": "INBOX", "max_results": 5}
            - {"label_id": "IMPORTANT", "max_results": 20}
            
            Output: JSON with emails array containing message_id, snippet, subject, from, date.
            
            Usage: Use label_id from list_gmail_labels. Common labels: 'INBOX', 'STARRED', 'IMPORTANT', 'SENT', 'DRAFT'."""
        )
        async def get_emails_by_label_tool(label_id: str, max_results: int = 10):
            return await get_emails_by_label(label_id, max_results)
    
    def run(self, access_token: str, refresh_token: str):
        """Run the MCP server"""
        # Set tokens for the tools
        set_tokens(access_token, refresh_token)
        
        # Run the server
        self.mcp.run(transport=self.config.transport)


def main():
    """Main entry point for the Gmail MCP Server"""
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Enhanced Gmail MCP Server')
    parser.add_argument('--access-token', required=True, help='Gmail API access token')
    parser.add_argument('--refresh-token', required=True, help='Gmail API refresh token')
    parser.add_argument('--config-file', help='Path to configuration file')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Load configuration
    config = Config()
    
    # Create and run server
    server = GmailMCPServer(config)
    server.run(args.access_token, args.refresh_token)


if __name__ == "__main__":
    main() 