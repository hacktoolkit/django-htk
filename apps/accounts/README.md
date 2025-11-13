# Accounts App

User authentication, registration, and profile management.

## Overview

The `accounts` app provides:

- User registration and email verification
- Email management (multiple emails per user)
- Social authentication (OAuth, OAuth2)
- Token-based API authentication
- User profiles with timezone and locale
- Password reset and recovery
- User search by email, username, or name
- User following/follower system

## Quick Start

### Create Users

```python
from htk.apps.accounts.utils.general import create_user, get_user_by_email

# Create a new user
user = create_user('user@example.com', password='secure_password')

# Get user by email
user = get_user_by_email('user@example.com')

# Get user by username
from htk.apps.accounts.utils.general import get_user_by_username
user = get_user_by_username('john_doe')
```

### Email Management

```python
from htk.apps.accounts.models import UserEmail

# Add additional email to user
user_email = UserEmail.objects.create(
    user=user,
    email='alternate@example.com',
    verified=False
)

# Set primary email
user.profile.set_primary_email('alternate@example.com')

# Get all emails for user
emails = user.profile.get_nonprimary_emails()
```

### Token Authentication

```python
from htk.apps.accounts.utils.auth import get_user_token_auth_token

# Generate token for API authentication
token = get_user_token_auth_token(user)

# Validate token
from htk.apps.accounts.utils.auth import validate_user_token_auth_token
is_valid = validate_user_token_auth_token(user, token)
```

### Social Authentication

```python
# Configure in settings.py
AUTHENTICATION_BACKENDS = [
    'htk.apps.accounts.backends.HtkUserTokenAuthBackend',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
]

# Use in views via python-social-auth
# /login/facebook/
# /login/google-oauth2/
```

### User Search

```python
from htk.apps.accounts.search import (
    search_by_username,
    search_by_email,
    search_by_name,
    combined_user_search
)

# Search by username
users = search_by_username('john')

# Search by email
user = search_by_email('user@example.com').first()

# Combined search across username and name
users = combined_user_search('john', [search_by_username, search_by_name])
```

### Following System

```python
# Add follower
user.profile.add_follower(other_user)

# Get followers
followers = user.profile.get_followers()

# Get following
following = user.profile.get_following()

# Check if user is followed
is_followed = user.profile.has_follower(other_user)
```

## Models

- **`BaseAbstractUserProfile`** - Extend to add custom user profile fields
- **`UserEmail`** - Stores multiple emails per user

## Key Features

### Password Reset
```python
from htk.apps.accounts.utils.auth import validate_reset_password_token

# Reset password
is_valid = validate_reset_password_token(user, token)
if is_valid:
    from htk.apps.accounts.utils.auth import reset_user_password
    reset_user_password(user, new_password)
```

### User Profile

Inherit from `BaseAbstractUserProfile` to add custom fields:

```python
from htk.apps.accounts.models import BaseAbstractUserProfile

class CustomUserProfile(BaseAbstractUserProfile):
    department = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
```

### Timezone & Locale

```python
from htk.apps.accounts.utils.locale import get_local_time

# Get user's local time
local_time = get_local_time(user, aware_datetime)

# Check if user is online during specific hours
from htk.apps.accounts.filters import users_currently_at_local_time
users = users_currently_at_local_time(User.objects.all(), 9, 17)
```

### Caching

The app automatically caches:
- User followers (`UserFollowersCache`)
- User following (`UserFollowingCache`)
- Account activation reminders

## Installation

```python
# settings.py
INSTALLED_APPS = [
    'htk.apps.accounts',
    # ...
]

# Add custom user profile
AUTH_USER_PROFILE_MODEL = 'myapp.CustomUserProfile'
```

## Signals

Automatic signal handlers:
- `create_user_profile` - Creates profile when User is created
- `process_user_email_association` - Handles email verification

## Best Practices

1. **Extend BaseAbstractUserProfile** for custom user data
2. **Use search functions** for user lookups
3. **Enable social auth** for multi-provider login
4. **Cache user relationships** using provided cache classes
5. **Validate tokens** before granting access
6. **Handle multiple emails** through UserEmail model
