# Facebook Integration

Facebook API and OAuth authentication.

## Quick Start

```python
from htk.lib.facebook.utils import get_long_lived_user_access_token

# Exchange short-lived token for long-lived token
long_token = get_long_lived_user_access_token(short_lived_token)
```

## Configuration

```python
# settings.py
FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID')
FACEBOOK_APP_SECRET = os.environ.get('FACEBOOK_APP_SECRET')
```

## Related Modules

- `htk.lib.google` - OAuth patterns
- `htk.apps.accounts` - Social auth
