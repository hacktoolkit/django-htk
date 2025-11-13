# Gravatar Integration

User avatars and profile images.

## Quick Start

```python
from htk.lib.gravatar.utils import get_gravatar_for_email, get_gravatar_hash

# Get Gravatar URL for email
gravatar_url = get_gravatar_for_email('user@example.com')

# Get Gravatar hash
gravatar_hash = get_gravatar_hash('user@example.com')
```

## Configuration

```python
# settings.py
GRAVATAR_DEFAULT_IMAGE = 'identicon'  # identicon, monsterid, wavatar, retro, robohash, blank
```

## Related Modules

- `htk.apps.accounts` - User profiles
- `htk.lib.facebook` - Social profile images
