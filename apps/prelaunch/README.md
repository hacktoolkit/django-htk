# Prelaunch App

Early access and pre-launch signup management.

## Quick Start

```python
from htk.apps.prelaunch.models import PrelaunchSignup

# Create signup
signup = PrelaunchSignup.objects.create(
    email='user@example.com',
    referral_code='friend123'
)

# Get or create
signup, created = PrelaunchSignup.objects.get_or_create_by_email(
    email='user@example.com'
)

# Grant early access
signup.grant_early_access()
```

## Models

- **`PrelaunchSignup`** - Track early access signups

## Common Patterns

```python
# Get unique signups
from htk.apps.prelaunch.utils import get_unique_signups
unique = get_unique_signups()

# Check if view is excepted
from htk.apps.prelaunch.utils import is_prelaunch_exception_view
if is_prelaunch_exception_view(request.path):
    # Allow access even in prelaunch mode
    pass

# Send Slack notification
signup.send_notification_message()
```

## Configuration

```python
# settings.py
PRELAUNCH_REDIRECT_URL = '/early-access/'
PRELAUNCH_EXCEPTED_PATHS = ['/health/', '/api/status/']
```

## Related Modules

- `htk.apps.accounts` - User registration
- `htk.apps.notifications` - Send confirmations
