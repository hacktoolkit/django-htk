# Alexa Integration

Alexa skill webhook events and request handling.

## Quick Start

```python
from htk.lib.alexa.views import alexa_skill_webhook_view

# Webhook endpoint automatically handles Alexa events
# POST /alexa/webhook/
```

## Event Handling

```python
from htk.lib.alexa.utils import handle_event, get_event_type

# Validate and process Alexa webhook event
event = request.json
if is_valid_alexa_skill_webhook_event(event):
    event_type = get_event_type(event)
    handler = get_event_handler_for_type(event_type)
    response = handle_event(event)
```

## Custom Handlers

```python
from htk.lib.alexa.event_handlers import default, launch

# Built-in handlers: launch (skill opened), default (generic handler)
# zesty handler available for custom implementations
```

## Configuration

```python
# settings.py
ALEXA_SKILL_ID = os.environ.get('ALEXA_SKILL_ID')
ALEXA_WEBHOOK_PATH = 'alexa/webhook/'
```
