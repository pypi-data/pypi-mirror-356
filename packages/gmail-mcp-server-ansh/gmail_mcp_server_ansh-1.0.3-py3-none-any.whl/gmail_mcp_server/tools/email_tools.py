"""
MCP Tools for Gmail email operations
"""

import json
import asyncio
from ..models import EmailSearchParams, EmailSendParams, EmailDetailParams
from ..services import GmailClient


# Global variables for tokens (set by main server)
ACCESS_TOKEN = None
REFRESH_TOKEN = None
GMAIL_API_TIMEOUT = 30


def set_tokens(access_token: str, refresh_token: str):
    """Set the Gmail API tokens for the tools"""
    global ACCESS_TOKEN, REFRESH_TOKEN
    ACCESS_TOKEN = access_token
    REFRESH_TOKEN = refresh_token


async def search_emails(params) -> str:
    """Search Gmail emails using Gmail search syntax"""
    try:
        # Handle different parameter formats
        if isinstance(params, str):
            # If agent passes a string, treat it as a query
            search_params = EmailSearchParams(query=params, max_results=10, include_body=False)
        elif isinstance(params, dict):
            # If agent passes a dict, validate it
            try:
                search_params = EmailSearchParams(**params)
            except Exception as e:
                # If validation fails, try to extract query from the dict
                query = params.get('query', str(params))
                search_params = EmailSearchParams(query=query, max_results=10, include_body=False)
        else:
            # If agent passes EmailSearchParams object, use it directly
            search_params = params
        
        # Run Gmail API call with timeout
        loop = asyncio.get_event_loop()
        client = GmailClient(ACCESS_TOKEN, REFRESH_TOKEN)
        
        # Use asyncio.to_thread to run the synchronous Gmail API call in a thread
        result = await asyncio.wait_for(
            loop.run_in_executor(None, lambda: client.search_emails(
                query=search_params.query,
                max_results=search_params.max_results,
                include_body=search_params.include_body
            )),
            timeout=GMAIL_API_TIMEOUT
        )
        
        return json.dumps(result, indent=2, ensure_ascii=False)
    except asyncio.TimeoutError:
        error_result = {
            "success": False,
            "error": f"Gmail API request timed out after {GMAIL_API_TIMEOUT} seconds",
            "emails": []
        }
        return json.dumps(error_result, indent=2)
    except Exception as e:
        error_result = {
            "success": False,
            "error": f"Search failed: {str(e)}",
            "emails": []
        }
        return json.dumps(error_result, indent=2)


async def get_recent_emails(max_results: int = 10) -> str:
    """Get the most recent emails from inbox"""
    try:
        # Run Gmail API call with timeout
        loop = asyncio.get_event_loop()
        client = GmailClient(ACCESS_TOKEN, REFRESH_TOKEN)
        
        # Use asyncio.to_thread to run the synchronous Gmail API call in a thread
        result = await asyncio.wait_for(
            loop.run_in_executor(None, lambda: client.get_recent_emails(max_results=min(max(max_results, 1), 20))),
            timeout=GMAIL_API_TIMEOUT
        )
        
        return json.dumps(result, indent=2, ensure_ascii=False)
    except asyncio.TimeoutError:
        error_result = {
            "success": False,
            "error": f"Gmail API request timed out after {GMAIL_API_TIMEOUT} seconds",
            "emails": []
        }
        return json.dumps(error_result, indent=2)
    except Exception as e:
        error_result = {
            "success": False,
            "error": f"Failed to get recent emails: {str(e)}",
            "emails": []
        }
        return json.dumps(error_result, indent=2)


async def get_email_details(params) -> str:
    """Get complete details of a specific email including full body content"""
    try:
        # Handle different parameter formats
        if isinstance(params, str):
            # If agent passes a string, treat it as message_id
            detail_params = EmailDetailParams(message_id=params)
        elif isinstance(params, dict):
            # If agent passes a dict, validate it
            try:
                detail_params = EmailDetailParams(**params)
            except Exception as e:
                # If validation fails, try to extract message_id from the dict
                message_id = params.get('message_id', str(params))
                detail_params = EmailDetailParams(message_id=message_id)
        else:
            # If agent passes EmailDetailParams object, use it directly
            detail_params = params
        
        # Run Gmail API call with timeout
        loop = asyncio.get_event_loop()
        client = GmailClient(ACCESS_TOKEN, REFRESH_TOKEN)
        
        # Use asyncio.to_thread to run the synchronous Gmail API call in a thread
        result = await asyncio.wait_for(
            loop.run_in_executor(None, lambda: client.get_email_details(detail_params.message_id)),
            timeout=GMAIL_API_TIMEOUT
        )
        
        return json.dumps(result, indent=2, ensure_ascii=False)
    except asyncio.TimeoutError:
        error_result = {
            "success": False,
            "error": f"Gmail API request timed out after {GMAIL_API_TIMEOUT} seconds"
        }
        return json.dumps(error_result, indent=2)
    except Exception as e:
        error_result = {
            "success": False,
            "error": f"Failed to get email details: {str(e)}"
        }
        return json.dumps(error_result, indent=2)


async def send_email(params) -> str:
    """Send an email via Gmail"""
    try:
        # Handle different parameter formats
        if isinstance(params, dict):
            # If agent passes a dict, validate it
            try:
                send_params = EmailSendParams(**params)
            except Exception as e:
                # If validation fails, return error
                error_result = {
                    "success": False,
                    "error": f"Invalid parameters: {str(e)}. Required: to, subject, body"
                }
                return json.dumps(error_result, indent=2)
        else:
            # If agent passes EmailSendParams object, use it directly
            send_params = params
        
        # Run Gmail API call with timeout
        loop = asyncio.get_event_loop()
        client = GmailClient(ACCESS_TOKEN, REFRESH_TOKEN)
        
        # Use asyncio.to_thread to run the synchronous Gmail API call in a thread
        result = await asyncio.wait_for(
            loop.run_in_executor(None, lambda: client.send_email(
                to=send_params.to,
                subject=send_params.subject,
                body=send_params.body,
                cc=send_params.cc,
                bcc=send_params.bcc
            )),
            timeout=GMAIL_API_TIMEOUT
        )
        
        return json.dumps(result, indent=2, ensure_ascii=False)
    except asyncio.TimeoutError:
        error_result = {
            "success": False,
            "error": f"Gmail API request timed out after {GMAIL_API_TIMEOUT} seconds"
        }
        return json.dumps(error_result, indent=2)
    except Exception as e:
        error_result = {
            "success": False,
            "error": f"Failed to send email: {str(e)}"
        }
        return json.dumps(error_result, indent=2)


async def list_gmail_labels() -> str:
    """List all Gmail labels including system and user-created labels"""
    try:
        loop = asyncio.get_event_loop()
        client = GmailClient(ACCESS_TOKEN, REFRESH_TOKEN)

        result = await asyncio.wait_for(
            loop.run_in_executor(None, client.list_labels),
            timeout=GMAIL_API_TIMEOUT
        )

        return json.dumps(result, indent=2, ensure_ascii=False)

    except asyncio.TimeoutError:
        return json.dumps({
            "success": False,
            "error": f"Gmail API request timed out after {GMAIL_API_TIMEOUT} seconds",
            "labels": []
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Failed to list labels: {str(e)}",
            "labels": []
        }, indent=2)


async def get_emails_by_label(label_id: str, max_results: int = 10) -> str:
    """Fetch emails that belong to a specific Gmail label"""
    try:
        loop = asyncio.get_event_loop()
        client = GmailClient(ACCESS_TOKEN, REFRESH_TOKEN)

        result = await asyncio.wait_for(
            loop.run_in_executor(None, lambda: client.get_emails_by_label(
                label_id=label_id,
                max_results=min(max(max_results, 1), 20)
            )),
            timeout=GMAIL_API_TIMEOUT
        )

        return json.dumps(result, indent=2, ensure_ascii=False)

    except asyncio.TimeoutError:
        return json.dumps({
            "success": False,
            "error": f"Gmail API request timed out after {GMAIL_API_TIMEOUT} seconds",
            "emails": []
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Failed to get emails by label: {str(e)}",
            "emails": []
        }, indent=2) 