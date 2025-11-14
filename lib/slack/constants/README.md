# Slack Constants

Configuration settings and constants for Slack integration and bot event handling.

## Event Handler Configuration

```python
from htk.lib.slack.constants import (
    HTK_SLACK_EVENT_TYPE_RESOLVER,
    HTK_SLACK_EVENT_HANDLERS,
    HTK_SLACK_EVENT_HANDLERS_EXTRAS,
    HTK_SLACK_EVENT_HANDLER_USAGES,
    HTK_SLACK_EVENT_HANDLER_USAGES_EXTRA,
)
```

**HTK_SLACK_EVENT_TYPE_RESOLVER**
- Path to function that resolves event types from Slack requests
- Default: `'htk.lib.slack.event_resolvers.default_event_type_resolver'`

**HTK_SLACK_EVENT_HANDLERS**
- Dictionary mapping event/command types to handler function paths
- Built-in handlers:
  - `'default'`, `'bart'`, `'beacon'`, `'bible'`, `'emaildig'`, `'findemail'`, `'geoip'`, `'githubprs'`, `'help'`, `'ohmygreen'`, `'stock'`, `'utcnow'`, `'weather'`, `'zesty'`
- Default handlers located in `htk.lib.slack.event_handlers`

**HTK_SLACK_EVENT_HANDLERS_EXTRAS**
- Additional custom event handlers
- Default: `{}` (empty)

**HTK_SLACK_EVENT_HANDLER_USAGES**
- Dictionary mapping handlers to usage/help documentation paths
- Provides help text for each command

**HTK_SLACK_EVENT_HANDLER_USAGES_EXTRA**
- Additional custom usage documentation
- Default: `{}` (empty)

## Trigger Commands

```python
from htk.lib.slack.constants import HTK_SLACK_TRIGGER_COMMAND_WORDS
```

**HTK_SLACK_TRIGGER_COMMAND_WORDS**
- Tuple of trigger words that are also commands
- Default: `('bart', 'bible', 'findemail', 'stock', 'weather')`
- Used for parsing Slack message text

## Notifications Configuration

```python
from htk.lib.slack.constants import (
    HTK_SLACK_NOTIFICATIONS_ENABLED,
    HTK_SLACK_BOT_ENABLED,
)
```

**HTK_SLACK_NOTIFICATIONS_ENABLED**
- Boolean flag to enable/disable Slack notifications
- Default: `False`

**HTK_SLACK_BOT_ENABLED**
- Boolean flag to enable/disable Slack bot functionality
- Default: `False`

## Notification Channels

```python
from htk.lib.slack.constants import (
    HTK_SLACK_NOTIFICATION_CHANNELS,
    HTK_SLACK_DEBUG_CHANNEL,
    HTK_SLACK_CELERY_NOTIFICATIONS_CHANNEL,
)
```

**HTK_SLACK_NOTIFICATION_CHANNELS**
- Dictionary mapping alert severity levels to Slack channel IDs
- Severity levels: `'critical'`, `'severe'`, `'danger'`, `'warning'`, `'info'`, `'debug'`
- Default channels:
  - `'critical'`: `'#alerts-p0-critical'`
  - `'severe'`: `'#alerts-p1-severe'`
  - `'danger'`: `'#alerts-p2-danger'`
  - `'warning'`: `'#alerts-p3-warning'`
  - `'info'`: `'#alerts-p4-info'`
  - `'debug'`: `'#alerts-p5-debug'`

**HTK_SLACK_DEBUG_CHANNEL**
- Debug channel for testing notifications
- Default: `'#test'`

**HTK_SLACK_CELERY_NOTIFICATIONS_CHANNEL**
- Channel for Celery task notifications
- Default: `None`

## URL and Task Configuration

```python
from htk.lib.slack.constants import (
    HTK_SLACK_BEACON_URL_NAME,
    HTK_SLACK_CELERY_TASK_GITHUB_PRS,
)
```

**HTK_SLACK_BEACON_URL_NAME**
- Django URL name for Beacon feature
- Default: `None`

**HTK_SLACK_CELERY_TASK_GITHUB_PRS**
- Celery task path for GitHub PR notifications
- Default: `None`

## Webhook Parameters

```python
from htk.lib.slack.constants import SLACK_WEBHOOK_PARAMS
```

**SLACK_WEBHOOK_PARAMS**
- Tuple of required parameters for Slack webhook validation
- Parameters: `token`, `team_id`, `team_domain`, `channel_id`, `channel_name`, `timestamp`, `user_id`, `user_name`, `text`, `trigger_word`

## Example Usage

```python
from htk.lib.slack.constants import (
    HTK_SLACK_NOTIFICATION_CHANNELS,
    HTK_SLACK_EVENT_HANDLERS,
)

# Send to critical alerts channel
critical_channel = HTK_SLACK_NOTIFICATION_CHANNELS['critical']

# Get handler for an event
handler_path = HTK_SLACK_EVENT_HANDLERS.get('bible')
```

## Configuration in settings.py

```python
HTK_SLACK_NOTIFICATIONS_ENABLED = True
HTK_SLACK_BOT_ENABLED = True

HTK_SLACK_NOTIFICATION_CHANNELS = {
    'critical': '#alerts-critical',
    'severe': '#alerts-severe',
    'danger': '#alerts-danger',
    'warning': '#alerts-warning',
    'info': '#alerts-info',
    'debug': '#test-alerts',
}

HTK_SLACK_DEBUG_CHANNEL = '#debug'

HTK_SLACK_EVENT_HANDLERS_EXTRAS = {
    'custom_command': 'myapp.slack_handlers.custom_command',
}

HTK_SLACK_BEACON_URL_NAME = 'beacon_view'
HTK_SLACK_CELERY_TASK_GITHUB_PRS = 'myapp.tasks.github_prs'
```
