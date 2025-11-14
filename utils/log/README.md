# Logging Utilities

Exception handlers for Rollbar and Slack logging.

## Quick Start

```python
from htk.utils.log.handlers import RollbarHandler, SlackDebugHandler
import logging

# Configure Rollbar handler
rollbar_handler = RollbarHandler()
logger = logging.getLogger()
logger.addHandler(rollbar_handler)

# Configure Slack handler for debugging
slack_handler = SlackDebugHandler()
debug_logger = logging.getLogger('debug')
debug_logger.addHandler(slack_handler)
```

## Common Patterns

```python
# Log exceptions to multiple destinations
logger.addHandler(RollbarHandler())  # Production monitoring
logger.addHandler(SlackDebugHandler())  # Team notifications

try:
    dangerous_operation()
except Exception as e:
    logger.exception('Operation failed')
```

## Configuration

```python
# settings.py
ROLLBAR_TOKEN = os.environ.get('ROLLBAR_TOKEN')
SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')
```
