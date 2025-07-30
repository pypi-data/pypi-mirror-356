import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly", "https://www.googleapis.com/auth/gmail.send", "https://www.googleapis.com/auth/gmail.labels"]

def _get_default_token_path():
    return os.environ.get(
        "GMAIL_TOKEN_PATH",
        os.path.expanduser("~/.gmail_mcp/token.json")
    )

def get_gmail_tokens(credentials_path, token_path=None):
    if token_path is None:
        token_path = _get_default_token_path()
    creds = None
    if os.path.exists(token_path):
        print(f"[OAuth] Loading tokens from: {os.path.abspath(token_path)}")
        with open(token_path, 'r') as token:
            creds = Credentials.from_authorized_user_info(json.load(token), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Ensure directory exists
        os.makedirs(os.path.dirname(token_path), exist_ok=True)
        print(f"[OAuth] Saving tokens to: {os.path.abspath(token_path)}")
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    return creds.token, creds.refresh_token

def load_tokens(token_path=None):
    if token_path is None:
        token_path = _get_default_token_path()
    creds = None
    if os.path.exists(token_path):
        with open(token_path, 'r') as token:
            creds = Credentials.from_authorized_user_info(json.load(token), SCOPES)
    return creds

def save_tokens(tokens: Credentials, token_path=None):
    if token_path is None:
        token_path = _get_default_token_path()
    os.makedirs(os.path.dirname(token_path), exist_ok=True)
    with open(token_path, 'w') as token:
        token.write(tokens.to_json()) 