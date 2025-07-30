"""
Gmail MCP Server Package

A Model Context Protocol (MCP) server for Gmail integration.
Provides tools for searching, reading, and sending emails via Gmail API.
"""

__version__ = "1.0.0"
__author__ = "Gmail MCP Server Team"

from .server import GmailMCPServer

__all__ = ["GmailMCPServer"] 