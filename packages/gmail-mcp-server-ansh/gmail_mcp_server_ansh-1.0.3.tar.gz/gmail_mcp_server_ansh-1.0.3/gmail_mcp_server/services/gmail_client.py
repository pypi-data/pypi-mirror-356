"""
Gmail API client service
"""

import base64
import re
import requests
from datetime import datetime
from email.mime.text import MIMEText
from typing import List, Optional, Dict, Any


class GmailClient:
    """Client for interacting with Gmail API"""
    
    def __init__(self, access_token: str, refresh_token: str):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.base_url = "https://gmail.googleapis.com/gmail/v1"

    def get_headers(self) -> Dict[str, str]:
        """Get headers for Gmail API requests"""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def _format_timestamp(self, internal_date: str) -> str:
        """Convert Gmail internal date to readable format"""
        try:
            timestamp = int(internal_date) / 1000
            return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, TypeError):
            return internal_date

    def _extract_email_content(self, payload: Dict) -> Dict[str, str]:
        """Extract email body content from Gmail payload - both plain text and HTML"""
        plain_text = ""
        html_content = ""
        
        if "parts" in payload:
            for part in payload["parts"]:
                mime_type = part.get("mimeType", "")
                if mime_type == "text/plain" and "data" in part.get("body", {}):
                    try:
                        plain_text = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
                    except Exception:
                        continue
                elif mime_type == "text/html" and "data" in part.get("body", {}):
                    try:
                        html_content = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
                    except Exception:
                        continue
        elif "body" in payload and "data" in payload["body"]:
            mime_type = payload.get("mimeType", "")
            try:
                content = base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8")
                if mime_type == "text/html":
                    html_content = content
                else:
                    plain_text = content
            except Exception:
                pass
                
        return {
            "plain_text": plain_text.strip(),
            "html_content": html_content.strip()
        }

    def _clean_html_content(self, html_content: str) -> str:
        """Clean and format HTML content for better readability"""
        if not html_content:
            return ""
        
        try:
            # Basic HTML cleaning - remove script and style tags
            # Remove script tags and their content
            html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
            
            # Remove style tags and their content
            html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
            
            # Remove HTML comments
            html_content = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)
            
            # Replace common HTML entities
            html_content = html_content.replace('&nbsp;', ' ')
            html_content = html_content.replace('&amp;', '&')
            html_content = html_content.replace('&lt;', '<')
            html_content = html_content.replace('&gt;', '>')
            html_content = html_content.replace('&quot;', '"')
            html_content = html_content.replace('&#39;', "'")
            
            # Replace <br> and <br/> with newlines
            html_content = re.sub(r'<br\s*/?>', '\n', html_content, flags=re.IGNORECASE)
            
            # Replace <p> tags with double newlines for paragraph breaks
            html_content = re.sub(r'</p>', '\n\n', html_content, flags=re.IGNORECASE)
            html_content = re.sub(r'<p[^>]*>', '', html_content, flags=re.IGNORECASE)
            
            # Replace <div> tags with newlines
            html_content = re.sub(r'</div>', '\n', html_content, flags=re.IGNORECASE)
            html_content = re.sub(r'<div[^>]*>', '', html_content, flags=re.IGNORECASE)
            
            # Remove other common HTML tags but keep their content
            html_content = re.sub(r'<[^>]+>', '', html_content)
            
            # Clean up extra whitespace and newlines
            html_content = re.sub(r'\n\s*\n', '\n\n', html_content)
            html_content = re.sub(r'[ \t]+', ' ', html_content)
            html_content = html_content.strip()
            
            return html_content
            
        except Exception as e:
            print(f"Warning: Error cleaning HTML content: {str(e)}")
            return html_content

    def _extract_headers(self, headers_list: List[Dict]) -> Dict[str, str]:
        """Extract relevant headers from Gmail message"""
        headers = {}
        for header in headers_list:
            name = header.get("name", "").lower()
            if name in ["subject", "from", "to", "cc", "bcc", "date", "reply-to"]:
                headers[name] = header.get("value", "").strip()
        return headers

    def search_emails(self, query: str, max_results: int = 10, include_body: bool = False) -> Dict[str, Any]:
        """Search emails with enhanced formatting and error handling"""
        try:
            # Validate max_results
            max_results = min(max(max_results, 1), 50)
            
            url = f"{self.base_url}/users/me/messages"
            params = {"q": query, "maxResults": max_results}
            
            response = requests.get(url, headers=self.get_headers(), params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            msg_ids = [msg["id"] for msg in data.get("messages", [])]
            
            if not msg_ids:
                return {
                    "success": True,
                    "message": f"No emails found matching query: '{query}'",
                    "total_results": 0,
                    "emails": []
                }

            emails = []
            format_type = "full" if include_body else "metadata"
            
            for msg_id in msg_ids:
                try:
                    msg_url = f"{self.base_url}/users/me/messages/{msg_id}"
                    msg_response = requests.get(
                        msg_url, 
                        headers=self.get_headers(), 
                        params={"format": format_type},
                        timeout=30
                    )
                    msg_response.raise_for_status()
                    msg_data = msg_response.json()
                    
                    # Extract headers
                    headers = self._extract_headers(msg_data.get("payload", {}).get("headers", []))
                    
                    # Build email object
                    email = {
                        "id": msg_data["id"],
                        "thread_id": msg_data.get("threadId", ""),
                        "snippet": msg_data.get("snippet", "")[:200],
                        "subject": headers.get("subject", "No Subject"),
                        "from": headers.get("from", "Unknown Sender"),
                        "to": headers.get("to", ""),
                        "date": headers.get("date", ""),
                        "timestamp": self._format_timestamp(msg_data.get("internalDate", "")),
                        "labels": msg_data.get("labelIds", [])
                    }
                    
                    # Add CC/BCC if present
                    if headers.get("cc"):
                        email["cc"] = headers["cc"]
                    if headers.get("bcc"):
                        email["bcc"] = headers["bcc"]
                    
                    # Add body content if requested
                    if include_body:
                        content_data = self._extract_email_content(msg_data.get("payload", {}))
                        email["body"] = {
                            "plain_text": content_data["plain_text"],
                            "has_plain_text": bool(content_data["plain_text"])
                        }
                    
                    emails.append(email)
                    
                except Exception as e:
                    print(f"Error processing message {msg_id}: {str(e)}")
                    continue
            
            return {
                "success": True,
                "message": f"Found {len(emails)} emails matching query: '{query}'",
                "total_results": len(emails),
                "query": query,
                "emails": emails
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Gmail API request failed: {str(e)}",
                "emails": []
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "emails": []
            }

    def get_email_details(self, message_id: str) -> Dict[str, Any]:
        """Get complete email details including full body content"""
        try:
            url = f"{self.base_url}/users/me/messages/{message_id}"
            response = requests.get(url, headers=self.get_headers(), params={"format": "full"}, timeout=30)
            response.raise_for_status()
            
            msg_data = response.json()
            headers = self._extract_headers(msg_data.get("payload", {}).get("headers", []))
            content_data = self._extract_email_content(msg_data.get("payload", {}))
            
            return {
                "success": True,
                "email": {
                    "id": msg_data["id"],
                    "thread_id": msg_data.get("threadId", ""),
                    "subject": headers.get("subject", "No Subject"),
                    "from": headers.get("from", "Unknown Sender"),
                    "to": headers.get("to", ""),
                    "cc": headers.get("cc", ""),
                    "bcc": headers.get("bcc", ""),
                    "reply_to": headers.get("reply-to", ""),
                    "date": headers.get("date", ""),
                    "timestamp": self._format_timestamp(msg_data.get("internalDate", "")),
                    "snippet": msg_data.get("snippet", ""),
                    "body": {
                        "plain_text": content_data["plain_text"],
                        "has_plain_text": bool(content_data["plain_text"])
                    },
                    "labels": msg_data.get("labelIds", []),
                    "size_estimate": msg_data.get("sizeEstimate", 0)
                }
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Gmail API request failed: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }

    def send_email(self, to: str, subject: str, body: str, cc: str = None, bcc: str = None) -> Dict[str, Any]:
        """Send email with enhanced error handling and validation"""
        try:
            # Create MIME message
            message = MIMEText(body, 'plain', 'utf-8')
            message['To'] = to
            message['From'] = "me"
            message['Subject'] = subject
            
            if cc:
                message['Cc'] = cc
            if bcc:
                message['Bcc'] = bcc

            # Encode message
            raw_message = base64.urlsafe_b64encode(
                message.as_string().encode('utf-8')
            ).decode('utf-8')
            
            # Send email
            url = f"{self.base_url}/users/me/messages/send"
            payload = {"raw": raw_message}
            
            response = requests.post(url, headers=self.get_headers(), json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return {
                "success": True,
                "message": "Email sent successfully",
                "message_id": result.get("id", ""),
                "thread_id": result.get("threadId", ""),
                "recipients": {
                    "to": to,
                    "cc": cc if cc else None,
                    "bcc": bcc if bcc else None
                }
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Failed to send email: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }

    def get_recent_emails(self, max_results: int = 10) -> Dict[str, Any]:
        """Get recent emails with consistent formatting"""
        try:
            return self.search_emails("", max_results=max_results, include_body=False)
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to retrieve recent emails: {str(e)}",
                "emails": []
            }
        
    def list_labels(self):
        """List all Gmail labels"""
        url = f"{self.base_url}/users/me/labels"
        headers = self.get_headers()

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to list labels: {response.text}")

        data = response.json()
        return {"labels": [{"id": l["id"], "name": l["name"]} for l in data.get("labels", [])]}
    
    def get_emails_by_label(self, label_id: str, max_results: int = 10):
        """Get emails by specific label"""
        url = f"{self.base_url}/users/me/messages"
        headers = self.get_headers()

        params = {
            "labelIds": label_id,
            "maxResults": max_results
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Failed to get emails: {response.text}")

        messages = response.json().get("messages", [])

        # Fetch each message detail (only summary)
        emails = []
        for msg in messages:
            msg_url = f"{self.base_url}/users/me/messages/{msg['id']}"
            msg_res = requests.get(msg_url, headers=headers)
            if msg_res.status_code == 200:
                msg_data = msg_res.json()
                payload = msg_data.get("payload", {})
                headers_list = payload.get("headers", [])

                def get_header(name):
                    return next((h["value"] for h in headers_list if h["name"].lower() == name.lower()), "")

                emails.append({
                    "message_id": msg["id"],
                    "snippet": msg_data.get("snippet"),
                    "subject": get_header("Subject"),
                    "from": get_header("From"),
                    "date": get_header("Date")
                })

        return {"emails": emails} 