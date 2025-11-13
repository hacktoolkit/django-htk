# Plivo Integration

SMS and voice communication API.

## Quick Start

```python
from htk.lib.plivo.views import plivo_message_webhook_view
from htk.lib.plivo.utils import get_plivo_number_owner, handle_message_event

# Webhook endpoint for SMS events
# POST /plivo/webhook/

# Handle incoming message
owner = get_plivo_number_owner(phone_number)
handle_message_event(event_data)
```

## Configuration

```python
# settings.py
PLIVO_AUTH_ID = os.environ.get('PLIVO_AUTH_ID')
PLIVO_AUTH_TOKEN = os.environ.get('PLIVO_AUTH_TOKEN')
```

## Related Modules

- `htk.apps.notifications` - SMS notifications
