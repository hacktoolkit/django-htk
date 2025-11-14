# Google Chat Utilities

Utilities for sending messages to Google Chat using webhooks.

## Functions

**google_chat_webhook_call(webhook_url, payload)**
- Sends a message to Google Chat via webhook
- Makes HTTP POST request with JSON payload
- Supports all Google Chat message formats (text, cards, etc.)
- Returns requests.Response object
- Raises exception on network/API errors

## Example Usage

```python
from htk.lib.google.chat.utils import google_chat_webhook_call

# Send simple text message
webhook_url = 'https://chat.googleapis.com/v1/spaces/SPACE_ID/messages?key=KEY&token=TOKEN'
payload = {
    'text': 'Hello from HTK!'
}
response = google_chat_webhook_call(webhook_url, payload)

# Send formatted card message
payload = {
    'cards': [{
        'header': {'title': 'Notification'},
        'sections': [{
            'widgets': [{
                'textParagraph': {'text': 'This is a card message'}
            }]
        }]
    }]
}
response = google_chat_webhook_call(webhook_url, payload)
```

## Configuration

Google Chat webhooks are configured per space in Google Chat:

1. Open a Google Chat space
2. Go to "Apps & integrations"
3. Create a new webhook
4. Copy the webhook URL to your settings

## Webhook URL Format

```
https://chat.googleapis.com/v1/spaces/{SPACE_ID}/messages?key={API_KEY}&token={WEBHOOK_TOKEN}
```
