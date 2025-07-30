# Gmail MCP Server

A Model Context Protocol (MCP) server that provides Gmail integration capabilities through a clean, async API.

## Features

- 🔍 **Search emails** with Gmail's powerful search syntax
- 📧 **Send emails** with support for CC/BCC
- 📋 **Get recent emails** from inbox
- 📄 **Get detailed email content** including full body
- 🏷️ **List Gmail labels** (system and custom)
- 📁 **Get emails by label** (INBOX, STARRED, etc.)
- 💚 **Health check** to verify server and API connectivity
- ⏱️ **Timeout protection** for all API calls
- 🔄 **Token refresh** capability (requires client credentials)

## Quick Start

### 1. Install Dependencies

```bash
pip install fastmcp requests pydantic
```

### 2. Set up Gmail API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Gmail API
4. Create OAuth 2.0 credentials
5. Download the credentials file

### 3. Get Access and Refresh Tokens

You'll need to obtain OAuth 2.0 tokens for Gmail API access. You can use the Google OAuth 2.0 playground or create a simple script to get these tokens.

### 4. Run the Server

```bash
python trial1.py --access-token YOUR_ACCESS_TOKEN --refresh-token YOUR_REFRESH_TOKEN
```

### 5. Test the Server

```bash
python test_server.py
```

## Available Tools

### `search_emails`
Search Gmail using Gmail's search syntax.

**Input:**
```json
{
  "params": {
    "query": "from:example@gmail.com",
    "max_results": 10,
    "include_body": false
  }
}
```

**Examples:**
- `after:2025/06/17` - Emails after specific date
- `from:example@gmail.com` - Emails from specific sender
- `subject:meeting` - Emails with specific subject
- `is:unread` - Unread emails
- `has:attachment` - Emails with attachments

### `get_recent_emails`
Get the most recent emails from inbox.

**Input:**
```json
{
  "max_results": 10
}
```

### `get_email_details`
Get complete details of a specific email including full body content.

**Input:**
```json
{
  "params": {
    "message_id": "18c1234567890abcdef"
  }
}
```

### `send_email`
Send an email via Gmail.

**Input:**
```json
{
  "params": {
    "to": "recipient@email.com",
    "subject": "Email Subject",
    "body": "Email content",
    "cc": "cc@email.com",
    "bcc": "bcc@email.com"
  }
}
```

### `list_gmail_labels`
List all Gmail labels including system and user-created labels.

**Input:**
```json
{}
```

### `get_emails_by_label`
Fetch emails that belong to a specific Gmail label.

**Input:**
```json
{
  "label_id": "INBOX",
  "max_results": 10
}
```

### `health_check`
Check the health and connectivity of the Gmail MCP server.

**Input:**
```json
{}
```

## Configuration

### Environment Variables

You can set these environment variables instead of passing tokens as arguments:

- `GMAIL_ACCESS_TOKEN` - Your Gmail API access token
- `GMAIL_REFRESH_TOKEN` - Your Gmail API refresh token

### Server Settings

The server is configured with:
- Port: 8010
- Log level: INFO
- Cache expiration: 60 seconds
- Gmail API timeout: 30 seconds

## Error Handling

The server includes comprehensive error handling:
- Timeout protection for all API calls
- Graceful handling of expired tokens
- Detailed error messages for debugging
- Fallback responses for failed operations

## Security Considerations

- Never commit tokens to version control
- Use environment variables for sensitive data
- Consider implementing token refresh for long-running sessions
- Validate all input parameters

## Troubleshooting

### Common Issues

1. **"Invalid credentials" error**
   - Check that your access token is valid and not expired
   - Verify your refresh token is correct

2. **"Permission denied" error**
   - Ensure your Gmail API credentials have the necessary scopes
   - Check that the Gmail API is enabled in your Google Cloud project

3. **"Timeout" errors**
   - The server has a 30-second timeout for Gmail API calls
   - For large email searches, try reducing `max_results`

### Testing

Run the test script to verify your setup:

```bash
python test_server.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 