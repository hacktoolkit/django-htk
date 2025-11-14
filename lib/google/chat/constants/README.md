# Google Chat Constants

Configuration defaults and constants for Google Chat integration.

## Configuration Settings

```python
from htk.lib.google.chat.constants import (
    HTK_GOOGLE_CHAT_NOTIFICATIONS_ENABLED,
    HTK_GOOGLE_CHAT_DEBUG_SPACE,
    HTK_GOOGLE_CHAT_NOTIFICATIONS_SPACES,
    HTK_GOOGLE_CHAT_SPACES_WEBHOOK_URLS,
)
```

### Notifications

**HTK_GOOGLE_CHAT_NOTIFICATIONS_ENABLED**
- Boolean flag to enable/disable Google Chat notifications
- Default: `False`

**HTK_GOOGLE_CHAT_DEBUG_SPACE**
- Debug space ID for testing notifications
- Default: `'#test'`

### Spaces

**HTK_GOOGLE_CHAT_NOTIFICATIONS_SPACES**
- Dictionary mapping alert severity levels to Google Chat space IDs
- Severity levels: `critical`, `severe`, `danger`, `warning`, `info`, `debug`
- Default mapping:
  - `'critical'`: `'#alerts-p0-critical'`
  - `'severe'`: `'#alerts-p1-severe'`
  - `'danger'`: `'#alerts-p2-danger'`
  - `'warning'`: `'#alerts-p3-warning'`
  - `'info'`: `'#alerts-p4-info'`
  - `'debug'`: `'#alerts-p5-debug'`

**HTK_GOOGLE_CHAT_SPACES_WEBHOOK_URLS**
- Dictionary mapping space IDs to their webhook URLs for posting messages
- Default: `{}` (empty, must be configured per deployment)
- Example configuration:
  ```python
  HTK_GOOGLE_CHAT_SPACES_WEBHOOK_URLS = {
      '#alerts-p0-critical': 'https://chat.googleapis.com/v1/spaces/...',
      '#alerts-p1-severe': 'https://chat.googleapis.com/v1/spaces/...',
  }
  ```

## Example Usage

```python
from htk.lib.google.chat.constants import (
    HTK_GOOGLE_CHAT_NOTIFICATIONS_SPACES,
    HTK_GOOGLE_CHAT_SPACES_WEBHOOK_URLS,
)

# Get the critical alerts space
critical_space = HTK_GOOGLE_CHAT_NOTIFICATIONS_SPACES['critical']

# Get webhook URL for that space
webhook_url = HTK_GOOGLE_CHAT_SPACES_WEBHOOK_URLS.get(critical_space)
```

## Configuration in settings.py

```python
HTK_GOOGLE_CHAT_NOTIFICATIONS_ENABLED = True

HTK_GOOGLE_CHAT_DEBUG_SPACE = '#test-alerts'

HTK_GOOGLE_CHAT_NOTIFICATIONS_SPACES = {
    'critical': '#alerts-critical',
    'severe': '#alerts-severe',
    'danger': '#alerts-danger',
    'warning': '#alerts-warning',
    'info': '#alerts-info',
    'debug': '#alerts-debug',
}

HTK_GOOGLE_CHAT_SPACES_WEBHOOK_URLS = {
    '#alerts-critical': 'https://chat.googleapis.com/v1/spaces/SPACES_ID_CRITICAL/messages?key=KEY&token=TOKEN',
    '#alerts-severe': 'https://chat.googleapis.com/v1/spaces/SPACES_ID_SEVERE/messages?key=KEY&token=TOKEN',
}
```
