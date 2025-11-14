# Discord Constants

Constants for Discord webhook integration and message relay.

## Webhook Constants

```python
from htk.lib.discord.constants import (
    DISCORD_WEBHOOK_URL,
    DISCORD_WEBHOOK_RELAY_PARAMS,
)
```

**DISCORD_WEBHOOK_URL**
- Template URL format for Discord webhook endpoints
- Format: `'https://discord.com/api/webhooks/{webhook_id}/{webhook_token}'`
- Replace `{webhook_id}` and `{webhook_token}` with your webhook credentials

**DISCORD_WEBHOOK_RELAY_PARAMS**
- List of parameters required for relaying webhook messages
- Parameters:
  - `'webhook_id'`: Discord webhook ID
  - `'webhook_token'`: Discord webhook token
  - `'content'`: Message content to send
- Used for webhook message relay and routing

## Example Usage

```python
from htk.lib.discord.constants import (
    DISCORD_WEBHOOK_URL,
    DISCORD_WEBHOOK_RELAY_PARAMS,
)

# Build webhook URL
webhook_id = 'your_webhook_id'
webhook_token = 'your_webhook_token'
url = DISCORD_WEBHOOK_URL.format(
    webhook_id=webhook_id,
    webhook_token=webhook_token
)

# Send message using params
payload = {
    'webhook_id': webhook_id,
    'webhook_token': webhook_token,
    'content': 'Hello from HTK!'
}
```

## Getting Discord Webhook Credentials

1. Go to your Discord server settings
2. Navigate to "Webhooks" section
3. Create or select a webhook
4. Copy the Webhook URL which contains both ID and token
5. Store webhook_id and webhook_token in settings
