# Discord Integration

Discord webhook and event handling.

## Quick Start

```python
from htk.lib.discord.views import discord_webhook_relay_view

# Webhook endpoint for Discord events
# POST /discord/webhook/
```

## Webhook Relay

```python
# Discord sends webhook events to your endpoint
# Automatically handles and processes events
```

## Configuration

```python
# settings.py
DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')
DISCORD_BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
```
