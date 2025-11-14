# Plivo SMS Constants

Webhook parameters and message formatting for Plivo SMS integration.

## Constants

```python
from htk.lib.plivo.constants import (
    PLIVO_MESSAGE_WEBHOOK_PARAMS,
    PLIVO_SLACK_DEFAULT_MESSAGE_FORMAT,
)
```

## Webhook Parameters

Expected parameters in Plivo SMS webhook callbacks:

```python
PLIVO_MESSAGE_WEBHOOK_PARAMS = (
    'From',          # Sender phone number (e.g., 14085551212)
    'TotalRate',
    'Text',          # Message content
    'To',            # Recipient phone number (e.g., 14151234567)
    'Units',
    'TotalAmount',
    'Type',          # Message type (e.g., 'sms')
    'MessageUUID',   # Unique message identifier
)
```

## Slack Message Format

Default format string for posting Plivo messages to Slack:

```python
PLIVO_SLACK_DEFAULT_MESSAGE_FORMAT = 'Plivo Message from *%(From)s* (%(Type)s; %(MessageUUID)s)\n>>> %(Text)s'
```

## Usage Example

```python
from htk.lib.plivo.constants import PLIVO_SLACK_DEFAULT_MESSAGE_FORMAT

# Format a Plivo webhook for Slack
webhook_data = {
    'From': '14085551212',
    'Type': 'sms',
    'MessageUUID': 'abc-123',
    'Text': 'Hello world',
}
slack_message = PLIVO_SLACK_DEFAULT_MESSAGE_FORMAT % webhook_data
```
