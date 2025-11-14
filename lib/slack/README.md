# Slack Integration

Send messages, handle webhooks, and respond to Slack events.

## Quick Start

```python
from htk.lib.slack.utils import webhook_call

# Send message
webhook_call({
    'text': 'Hello from Django!',
    'channel': '#notifications'
})

# With formatting
webhook_call({
    'text': 'Important update',
    'attachments': [{
        'color': 'good',
        'title': 'Task Complete',
        'text': 'Deployment finished successfully'
    }]
})
```

## Event Handlers

```python
from htk.lib.slack.event_handlers import default, weather, github_prs

# Built-in handlers for various events
# Customize in event_handlers.py
```

## Webhook Handling

```python
from htk.lib.slack.views import slack_webhook_view

# POST /slack/webhook/
# Automatically routes to event handlers
```

## Common Patterns

```python
# Get event type
from htk.lib.slack.utils import get_event_type
event_type = get_event_type(event)

# Handle events
from htk.lib.slack.utils import handle_event
response = handle_event(event)

# Validate webhook
from htk.lib.slack.utils import is_valid_webhook_event
if is_valid_webhook_event(event):
    # Process
    pass
```

## Configuration

```python
# settings.py
SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
SLACK_SIGNING_SECRET = os.environ.get('SLACK_SIGNING_SECRET')
```

## Features

- Beacon/location tracking
- Multiple event handlers
- Webhook validation
- Error response handling
